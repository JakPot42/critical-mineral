"""Integration tests for FastAPI routes using TestClient."""

import os
import tempfile
import pytest

# Point DB at a temp file before importing app
os.environ["DATABASE_URL"] = tempfile.mktemp(suffix=".db")

from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="module")
def client():
    """Start the app (triggers lifespan → init_db + seed) once per module."""
    with TestClient(app, raise_server_exceptions=True) as c:
        yield c


# ── index ─────────────────────────────────────────────────────────────────────

def test_index_returns_200(client):
    r = client.get("/")
    assert r.status_code == 200


def test_index_contains_mineral_options(client):
    r = client.get("/")
    assert "neodymium" in r.text.lower()
    assert "cobalt" in r.text.lower()


def test_index_contains_demo_buttons(client):
    r = client.get("/")
    assert "/demo/neodymium" in r.text
    assert "/demo/cobalt" in r.text


# ── /analyze ──────────────────────────────────────────────────────────────────

def test_analyze_unknown_mineral_returns_400(client):
    r = client.post("/analyze", data={"mineral": "unobtanium"}, follow_redirects=False)
    assert r.status_code == 400


def test_analyze_neodymium_redirects_to_result(client):
    r = client.post("/analyze", data={"mineral": "neodymium"}, follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"].startswith("/result/")


def test_analyze_cobalt_creates_result(client):
    r = client.post("/analyze", data={"mineral": "cobalt"}, follow_redirects=True)
    assert r.status_code == 200
    assert "cobalt" in r.text.lower() or "Co" in r.text


def test_analyze_all_catalog_minerals_dont_crash(client):
    from mineral_catalog import list_minerals
    for m in list_minerals():
        r = client.post("/analyze", data={"mineral": m}, follow_redirects=False)
        assert r.status_code in (303, 400, 500), f"{m}: unexpected status {r.status_code}"
        if r.status_code == 303:
            assert "/result/" in r.headers["location"]


# ── /result/{id} ──────────────────────────────────────────────────────────────

def test_result_404_for_missing_id(client):
    r = client.get("/result/999999")
    assert r.status_code == 404


def test_result_shows_mineral_name(client):
    r = client.post("/analyze", data={"mineral": "neodymium"}, follow_redirects=True)
    assert r.status_code == 200
    assert "Neodymium" in r.text or "neodymium" in r.text.lower()


def test_result_shows_risk_tier(client):
    r = client.post("/analyze", data={"mineral": "neodymium"}, follow_redirects=True)
    assert r.status_code == 200
    assert any(tier in r.text for tier in ("CRITICAL", "HIGH", "MEDIUM", "LOW"))


def test_result_shows_strategic_brief(client):
    r = client.post("/analyze", data={"mineral": "neodymium"}, follow_redirects=True)
    assert r.status_code == 200
    assert "SITUATION" in r.text or "brief" in r.text.lower()


# ── /demo/{mineral} ───────────────────────────────────────────────────────────

def test_demo_neodymium_redirects(client):
    r = client.get("/demo/neodymium", follow_redirects=False)
    assert r.status_code in (302, 200)


def test_demo_cobalt_resolves(client):
    r = client.get("/demo/cobalt", follow_redirects=True)
    assert r.status_code == 200
    assert "Cobalt" in r.text or "cobalt" in r.text.lower()


def test_demo_unknown_returns_404(client):
    r = client.get("/demo/unobtanium")
    assert r.status_code == 404


# ── /result/{id}/pdf ──────────────────────────────────────────────────────────

def test_pdf_download_returns_bytes(client):
    r_analyze = client.post("/analyze", data={"mineral": "neodymium"}, follow_redirects=False)
    assert r_analyze.status_code == 303
    result_id = r_analyze.headers["location"].split("/")[-1]

    r_pdf = client.post(f"/result/{result_id}/pdf")
    assert r_pdf.status_code == 200
    assert r_pdf.headers["content-type"] == "application/pdf"
    assert r_pdf.content[:4] == b"%PDF"


def test_pdf_404_for_missing_analysis(client):
    r = client.post("/result/999999/pdf")
    assert r.status_code == 404


# ── /analyses ─────────────────────────────────────────────────────────────────

def test_analyses_list_returns_200(client):
    r = client.get("/analyses")
    assert r.status_code == 200


def test_analyses_list_shows_history(client):
    client.post("/analyze", data={"mineral": "tungsten"}, follow_redirects=False)
    r = client.get("/analyses")
    assert "tungsten" in r.text.lower()


# ── /health ───────────────────────────────────────────────────────────────────

def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert "demo_mode" in data
