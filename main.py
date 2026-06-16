"""
Critical Mineral Space Resource Intelligence Monitor.
Input a critical mineral → terrestrial risk profile + top-3 asteroid candidates + strategic brief.

Data sources:
  - USGS Mineral Commodity Summaries 2024 (pre-populated catalog)
  - NASA JPL NHATS API (delta-v accessibility)
  - NASA JPL SBDB Query API (spectral types)
  - Claude Haiku (strategic brief synthesis)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import DEMO_MODE
from database import init_db, save_analysis, get_analysis, get_latest_by_mineral, list_analyses
from mineral_catalog import get_mineral, list_minerals
from risk_engine import compute_risk_score
from asteroid_client import fetch_nhats, fetch_neo_spectral_catalog
from asteroid_matcher import find_candidates
from claude_analyst import generate_brief, MineralAnalysisError
from pdf_export import generate_pdf
from seed_data import DEMO_ANALYSES


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    _seed_demos()
    yield


app = FastAPI(
    title="Critical Mineral Space Resource Intelligence Monitor",
    lifespan=lifespan,
)
templates = Jinja2Templates(directory="templates")


# ── helpers ────────────────────────────────────────────────────────────────────


def _seed_demos():
    """Pre-seed neodymium and cobalt analyses so /demo/* always resolves immediately."""
    for mineral_key, demo in DEMO_ANALYSES.items():
        if get_latest_by_mineral(mineral_key) is not None:
            continue
        mineral = get_mineral(mineral_key)
        if mineral is None:
            continue
        risk = compute_risk_score(mineral)
        brief = generate_brief(mineral, risk, demo["asteroids"], demo_mode=True)
        save_analysis(mineral_key, risk, demo["asteroids"], brief, demo=True)


def _run_pipeline(mineral_key: str, demo_mode: bool) -> tuple[dict, list, str]:
    """Run risk score + asteroid match + Claude brief. Returns (risk, asteroids, brief)."""
    mineral = get_mineral(mineral_key)
    if mineral is None:
        raise ValueError(f"Unknown mineral: {mineral_key!r}")

    risk = compute_risk_score(mineral)

    # Check seed data first (fast, no network) for demo minerals
    if demo_mode and mineral_key in DEMO_ANALYSES:
        asteroids = DEMO_ANALYSES[mineral_key]["asteroids"]
    else:
        asteroids = _fetch_asteroids(mineral_key, demo_mode)

    brief = generate_brief(mineral, risk, asteroids, demo_mode=demo_mode)
    return risk, asteroids, brief


def _fetch_asteroids(mineral_key: str, demo_mode: bool) -> list:
    """Call NASA APIs; on any failure return empty list (never hard-crash a demo)."""
    try:
        nhats = fetch_nhats()
        neo_catalog = fetch_neo_spectral_catalog()
        return find_candidates(mineral_key, nhats, neo_catalog, top_n=3)
    except Exception:
        if demo_mode:
            return []
        raise


def _tier_color(tier: str) -> str:
    return {"CRITICAL": "#dc2626", "HIGH": "#d97706", "MEDIUM": "#ca8a04", "LOW": "#16a34a"}.get(tier, "#64748b")


# ── routes ─────────────────────────────────────────────────────────────────────


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {
        "minerals": list_minerals(),
        "demo_minerals": list(DEMO_ANALYSES.keys()),
        "recent": list_analyses(limit=5),
        "demo_mode": DEMO_MODE,
    })


@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, mineral: str = Form(...)):
    mineral_key = mineral.strip().lower()
    record = get_mineral(mineral_key)
    if record is None:
        return templates.TemplateResponse(request, "index.html", {
            "minerals": list_minerals(),
            "demo_minerals": list(DEMO_ANALYSES.keys()),
            "recent": list_analyses(limit=5),
            "demo_mode": DEMO_MODE,
            "error": f"'{mineral}' is not in the catalog. Select a mineral from the list.",
        }, status_code=400)

    try:
        risk, asteroids, brief = _run_pipeline(mineral_key, DEMO_MODE)
    except MineralAnalysisError as exc:
        return templates.TemplateResponse(request, "index.html", {
            "minerals": list_minerals(),
            "demo_minerals": list(DEMO_ANALYSES.keys()),
            "recent": list_analyses(limit=5),
            "demo_mode": DEMO_MODE,
            "error": str(exc),
        }, status_code=500)

    analysis_id = save_analysis(mineral_key, risk, asteroids, brief, demo=DEMO_MODE)
    return RedirectResponse(f"/result/{analysis_id}", status_code=303)


@app.get("/demo/{mineral_key}", response_class=HTMLResponse)
async def demo_redirect(request: Request, mineral_key: str):
    mineral_key = mineral_key.lower()
    existing = get_latest_by_mineral(mineral_key)
    if existing:
        return RedirectResponse(f"/result/{existing['id']}", status_code=302)

    # Not yet seeded (shouldn't happen after lifespan, but defensive)
    mineral = get_mineral(mineral_key)
    if mineral is None:
        raise HTTPException(404, f"Demo not available for '{mineral_key}'")

    if mineral_key in DEMO_ANALYSES:
        demo = DEMO_ANALYSES[mineral_key]
        risk = compute_risk_score(mineral)
        brief = generate_brief(mineral, risk, demo["asteroids"], demo_mode=True)
        analysis_id = save_analysis(mineral_key, risk, demo["asteroids"], brief, demo=True)
    else:
        raise HTTPException(404, f"No pre-built demo for '{mineral_key}'. Use /analyze instead.")

    return RedirectResponse(f"/result/{analysis_id}", status_code=302)


@app.get("/result/{analysis_id}", response_class=HTMLResponse)
async def result(request: Request, analysis_id: int):
    analysis = get_analysis(analysis_id)
    if analysis is None:
        raise HTTPException(404, "Analysis not found")

    mineral = get_mineral(analysis["mineral_name"])
    tier_color = _tier_color(analysis["risk"]["tier"])

    return templates.TemplateResponse(request, "result.html", {
        "analysis": analysis,
        "mineral": mineral,
        "tier_color": tier_color,
        "demo_mode": analysis["demo_mode"],
        "brief_paragraphs": [p.strip() for p in analysis["brief"].split("\n\n") if p.strip()],
    })


@app.post("/result/{analysis_id}/pdf")
async def download_pdf(analysis_id: int):
    analysis = get_analysis(analysis_id)
    if analysis is None:
        raise HTTPException(404, "Analysis not found")

    mineral = get_mineral(analysis["mineral_name"])
    if mineral is None:
        raise HTTPException(400, "Mineral data not found")

    pdf_bytes = generate_pdf(mineral, analysis["risk"], analysis["asteroids"], analysis["brief"])
    filename = f"critical_mineral_{analysis['mineral_name']}_report.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@app.get("/analyses", response_class=HTMLResponse)
async def analyses_list(request: Request):
    return templates.TemplateResponse(request, "analysis_list.html", {
        "analyses": list_analyses(limit=50),
        "demo_mode": DEMO_MODE,
    })


@app.get("/health")
async def health():
    return {"status": "ok", "demo_mode": DEMO_MODE}
