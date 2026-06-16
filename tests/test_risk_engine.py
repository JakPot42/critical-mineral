"""Tests for risk_engine.py"""

import pytest
from risk_engine import compute_risk_score


def _mineral(import_pct=50, substitutability="medium", dod_critical=False):
    return {
        "import_dependency_pct": import_pct,
        "substitutability": substitutability,
        "dod_critical": dod_critical,
    }


def test_neodymium_is_critical():
    m = _mineral(import_pct=94, substitutability="none", dod_critical=True)
    result = compute_risk_score(m)
    assert result["tier"] == "CRITICAL"
    assert result["total"] >= 81


def test_dysprosium_is_critical():
    m = _mineral(import_pct=100, substitutability="none", dod_critical=True)
    result = compute_risk_score(m)
    assert result["tier"] == "CRITICAL"
    assert result["total"] == 100


def test_low_import_no_dod_is_low():
    m = _mineral(import_pct=10, substitutability="high", dod_critical=False)
    result = compute_risk_score(m)
    assert result["tier"] == "LOW"
    assert result["total"] <= 30


def test_import_score_scales_with_percentage():
    low = compute_risk_score(_mineral(import_pct=10))
    high = compute_risk_score(_mineral(import_pct=90))
    assert high["import_score"] > low["import_score"]


def test_dod_critical_adds_25_points():
    base = compute_risk_score(_mineral(import_pct=50, dod_critical=False))
    with_dod = compute_risk_score(_mineral(import_pct=50, dod_critical=True))
    assert with_dod["dod_score"] == 25
    assert base["dod_score"] == 0
    assert with_dod["total"] == base["total"] + 25


def test_substitutability_none_is_25():
    result = compute_risk_score(_mineral(substitutability="none"))
    assert result["substitutability_score"] == 25


def test_substitutability_high_is_0():
    result = compute_risk_score(_mineral(substitutability="high"))
    assert result["substitutability_score"] == 0


def test_total_never_exceeds_100():
    m = _mineral(import_pct=200, substitutability="none", dod_critical=True)
    result = compute_risk_score(m)
    assert result["total"] <= 100


def test_result_has_all_keys():
    result = compute_risk_score(_mineral())
    for key in ("import_score", "dod_score", "substitutability_score", "total", "tier", "breakdown"):
        assert key in result, f"Missing key: {key}"


def test_breakdown_has_three_factors():
    result = compute_risk_score(_mineral())
    bd = result["breakdown"]
    assert "import_dependency" in bd
    assert "dod_criticality" in bd
    assert "substitutability" in bd


def test_breakdown_points_sum_to_total():
    m = _mineral(import_pct=60, substitutability="low", dod_critical=True)
    result = compute_risk_score(m)
    bd = result["breakdown"]
    computed_sum = (
        bd["import_dependency"]["points"]
        + bd["dod_criticality"]["points"]
        + bd["substitutability"]["points"]
    )
    assert abs(computed_sum - result["total"]) < 0.01


def test_tier_boundaries():
    assert compute_risk_score(_mineral(import_pct=0, substitutability="high", dod_critical=False))["tier"] == "LOW"
    assert compute_risk_score(_mineral(import_pct=50, substitutability="medium", dod_critical=False))["tier"] in ("MEDIUM", "LOW")
    assert compute_risk_score(_mineral(import_pct=100, substitutability="none", dod_critical=True))["tier"] == "CRITICAL"


def test_lithium_is_medium():
    # lithium: 25% import dep, medium sub, dod_critical=True
    m = _mineral(import_pct=25, substitutability="medium", dod_critical=True)
    result = compute_risk_score(m)
    # 12.5 + 25 + 10 = 47.5 → MEDIUM
    assert result["tier"] == "MEDIUM"


def test_cobalt_is_high():
    # cobalt: 76% import, low sub, dod_critical=True
    m = _mineral(import_pct=76, substitutability="low", dod_critical=True)
    result = compute_risk_score(m)
    # 38 + 25 + 18 = 81 → CRITICAL
    assert result["tier"] == "CRITICAL"
