"""Tests for asteroid_matcher.py and asteroid_client.py helpers."""

import pytest
from asteroid_matcher import find_candidates, _rationale, _norm
from asteroid_client import estimate_tonnage, _h_to_diameter, _default_albedo


# ── asteroid_client helpers ────────────────────────────────────────────────────


def test_h_to_diameter_bennu():
    # Bennu: H=20.7, albedo=0.044 → ~0.49 km known
    d = _h_to_diameter(20.7, 0.044)
    assert 0.45 < d < 0.55, f"Bennu diameter estimate off: {d}"


def test_h_to_diameter_low_albedo_gives_larger():
    d_dark = _h_to_diameter(18.0, 0.04)
    d_bright = _h_to_diameter(18.0, 0.30)
    assert d_dark > d_bright


def test_h_to_diameter_zero_albedo_handled():
    # Should not raise ZeroDivisionError
    d = _h_to_diameter(20.0, 0.0)
    assert d > 0


def test_estimate_tonnage_positive():
    mass = estimate_tonnage(0.5, "C")
    assert mass > 0


def test_estimate_tonnage_m_type_denser():
    mass_c = estimate_tonnage(1.0, "C")
    mass_m = estimate_tonnage(1.0, "M")
    assert mass_m > mass_c


def test_estimate_tonnage_zero_diameter():
    assert estimate_tonnage(0, "C") == 0.0


def test_estimate_tonnage_none_diameter():
    assert estimate_tonnage(None, "C") == 0.0


def test_default_albedo_known_types():
    assert _default_albedo("C") == pytest.approx(0.06)
    assert _default_albedo("M") == pytest.approx(0.17)
    assert _default_albedo("S") == pytest.approx(0.20)


def test_default_albedo_unknown_type():
    assert _default_albedo("Z") == pytest.approx(0.10)


# ── asteroid_matcher ──────────────────────────────────────────────────────────


def _make_neo(pdes, spec, diameter_km=None, H=20.0):
    return {
        "pdes": pdes,
        "full_name": f"({pdes}) Test",
        "spec": spec,
        "diameter_km": diameter_km,
        "albedo": None,
        "H": H,
    }


def test_find_candidates_filters_by_spectral_type():
    nhats = {"101955": 5.06, "3554": 7.50, "999999": 4.50}
    neo_catalog = [
        _make_neo("101955", "B"),   # matches neodymium (B in spectral map)
        _make_neo("3554", "M"),     # does NOT match neodymium
        _make_neo("999999", "C"),   # matches neodymium
    ]
    results = find_candidates("neodymium", nhats, neo_catalog)
    designations = [r["designation"] for r in results]
    assert "101955" in designations
    assert "999999" in designations
    assert "3554" not in designations


def test_find_candidates_sorted_by_dv():
    nhats = {"A": 7.0, "B": 5.0, "C": 6.0}
    neo_catalog = [
        _make_neo("A", "C"),
        _make_neo("B", "C"),
        _make_neo("C", "C"),
    ]
    results = find_candidates("neodymium", nhats, neo_catalog, top_n=3)
    dvs = [r["min_dv_km_s"] for r in results]
    assert dvs == sorted(dvs)


def test_find_candidates_top_n_limit():
    nhats = {str(i): float(5 + i) for i in range(10)}
    neo_catalog = [_make_neo(str(i), "C") for i in range(10)]
    results = find_candidates("neodymium", nhats, neo_catalog, top_n=3)
    assert len(results) <= 3


def test_find_candidates_requires_nhats_intersection():
    nhats = {"101955": 5.06}
    neo_catalog = [
        _make_neo("101955", "B"),
        _make_neo("999999", "C"),   # not in NHATS → excluded
    ]
    results = find_candidates("neodymium", nhats, neo_catalog)
    assert len(results) == 1
    assert results[0]["designation"] == "101955"


def test_find_candidates_empty_nhats():
    results = find_candidates("neodymium", {}, [_make_neo("101955", "B")])
    assert results == []


def test_find_candidates_unknown_mineral():
    nhats = {"X": 5.0}
    neo_catalog = [_make_neo("X", "C")]
    results = find_candidates("unobtanium", nhats, neo_catalog)
    assert results == []


def test_find_candidates_result_has_required_keys():
    nhats = {"101955": 5.06}
    neo_catalog = [_make_neo("101955", "B", diameter_km=0.49)]
    results = find_candidates("neodymium", nhats, neo_catalog)
    assert len(results) == 1
    r = results[0]
    for key in ("designation", "full_name", "spectral_class", "min_dv_km_s", "mineral_match_rationale"):
        assert key in r, f"Missing key: {key}"


def test_rationale_known_pair():
    text = _rationale("neodymium", "C")
    assert len(text) > 20


def test_rationale_unknown_pair_returns_fallback():
    text = _rationale("unobtanium", "Z")
    assert "unobtanium" in text.lower() or "Z" in text


def test_norm_strips_whitespace():
    assert _norm("  101955 ") == "101955"
    assert _norm("101955") == "101955"


def test_norm_lowercases():
    assert _norm("BENNU") == "bennu"
