"""
NASA SBDB and NHATS API clients.
Sources:
  NHATS: https://ssd-api.jpl.nasa.gov/nhats.api
  SBDB:  https://ssd-api.jpl.nasa.gov/sbdb_query.api
  SBDB single: https://ssd-api.jpl.nasa.gov/sbdb.api
"""

import math
import httpx
from config import NHATS_API, SBDB_QUERY_API, SBDB_API, NHATS_MAX_DV, SPECTRAL_DENSITY, DEFAULT_DENSITY

TIMEOUT = 15.0


def fetch_nhats(max_dv: float = NHATS_MAX_DV) -> dict[str, float]:
    """
    Returns dict mapping asteroid designation → min_dv (km/s).
    Covers all NEAs accessible from LEO within max_dv.
    """
    resp = httpx.get(
        NHATS_API,
        params={"dv": max_dv, "dur": 450, "stay": 8},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        row["des"]: float(row["min_dv"])
        for row in data.get("data", [])
        if row.get("min_dv") is not None
    }


def fetch_neo_spectral_catalog() -> list[dict]:
    """
    Returns list of NEOs with known spectral types from SBDB.
    We query for all NEOs and filter to those with a spectral type set.
    """
    params = {
        "sb-class": "NEO",
        "fields": "pdes,full_name,diameter,albedo,spec_T,spec_B,H,moid",
        "limit": 5000,
    }
    resp = httpx.get(SBDB_QUERY_API, params=params, timeout=TIMEOUT)
    resp.raise_for_status()
    raw = resp.json()

    fields = raw.get("fields", [])
    rows = raw.get("data", [])

    field_idx = {f: i for i, f in enumerate(fields)}

    results = []
    for row in rows:
        spec_t = row[field_idx["spec_T"]] if "spec_T" in field_idx else None
        spec_b = row[field_idx["spec_B"]] if "spec_B" in field_idx else None
        spec = _canonical_spec(spec_t or spec_b)
        if not spec:
            continue

        diameter_km = None
        raw_diam = row[field_idx["diameter"]] if "diameter" in field_idx else None
        if raw_diam is not None:
            try:
                diameter_km = float(raw_diam)
            except (ValueError, TypeError):
                pass

        albedo = None
        raw_alb = row[field_idx["albedo"]] if "albedo" in field_idx else None
        if raw_alb is not None:
            try:
                albedo = float(raw_alb)
            except (ValueError, TypeError):
                pass

        H = None
        raw_H = row[field_idx["H"]] if "H" in field_idx else None
        if raw_H is not None:
            try:
                H = float(raw_H)
            except (ValueError, TypeError):
                pass

        if diameter_km is None and H is not None:
            assumed_albedo = albedo or _default_albedo(spec)
            diameter_km = _h_to_diameter(H, assumed_albedo)

        results.append({
            "pdes": row[field_idx["pdes"]],
            "full_name": row[field_idx["full_name"]],
            "spec": spec,
            "diameter_km": diameter_km,
            "albedo": albedo,
            "H": H,
        })
    return results


def fetch_sbdb_object(designation: str) -> dict | None:
    """Fetch detailed info for a single object by designation."""
    try:
        resp = httpx.get(SBDB_API, params={"sstr": designation, "phys-par": True}, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def estimate_tonnage(diameter_km: float, spec: str) -> float:
    """
    Estimate total mass in metric tons.
    Volume = (4/3)π r³, density from spectral type.
    """
    if diameter_km is None or diameter_km <= 0:
        return 0.0
    r_m = (diameter_km * 1000) / 2
    volume_m3 = (4 / 3) * math.pi * (r_m ** 3)
    density_g_cm3 = SPECTRAL_DENSITY.get(spec, DEFAULT_DENSITY)
    density_kg_m3 = density_g_cm3 * 1000
    mass_kg = volume_m3 * density_kg_m3
    return mass_kg / 1000  # metric tons


def _canonical_spec(raw: str | None) -> str | None:
    """Map raw spectral label to the first letter (major class)."""
    if not raw:
        return None
    cleaned = raw.strip().split("/")[0].strip()
    if not cleaned:
        return None
    # Return first letter to group subtypes (Sq → S, etc.)
    # But preserve multi-char types we have densities for
    known = {"C", "B", "P", "D", "S", "Q", "Sq", "M", "X", "E", "V", "A", "K", "L"}
    if cleaned in known:
        return cleaned
    if cleaned[0] in {"C", "B", "S", "M", "X", "E", "V", "A", "D", "P"}:
        return cleaned[0]
    return None


def _default_albedo(spec: str) -> float:
    """Typical geometric albedo by spectral type."""
    return {"C": 0.06, "B": 0.07, "P": 0.04, "D": 0.05, "S": 0.20,
            "Q": 0.20, "M": 0.17, "X": 0.12, "E": 0.45, "V": 0.35}.get(spec, 0.10)


def _h_to_diameter(H: float, albedo: float) -> float:
    """
    Convert absolute magnitude H to diameter (km).
    Formula: D (km) = (1329 / sqrt(albedo)) * 10^(-H/5)
    Source: Fowler & Chillemi (1992), used by JPL SBDB.
    """
    if albedo <= 0:
        albedo = 0.10
    return (1329.0 / math.sqrt(albedo)) * (10 ** (-H / 5))
