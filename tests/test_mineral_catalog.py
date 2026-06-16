"""Tests for mineral_catalog.py"""

import pytest
from mineral_catalog import get_mineral, list_minerals, CATALOG


def test_list_minerals_returns_sorted():
    minerals = list_minerals()
    assert minerals == sorted(minerals)
    assert len(minerals) == len(CATALOG)


def test_get_mineral_case_insensitive():
    assert get_mineral("Neodymium") is not None
    assert get_mineral("NEODYMIUM") is not None
    assert get_mineral("neodymium") is not None


def test_get_mineral_returns_none_for_unknown():
    assert get_mineral("unobtanium") is None
    assert get_mineral("") is None


def test_neodymium_fields():
    m = get_mineral("neodymium")
    assert m["full_name"] == "Neodymium"
    assert m["symbol"] == "Nd"
    assert m["import_dependency_pct"] == 94
    assert m["dod_critical"] is True
    assert m["substitutability"] == "none"
    assert len(m["top_suppliers"]) >= 1
    assert len(m["defense_applications"]) >= 1
    assert len(m["spectral_match"]) >= 1


def test_cobalt_fields():
    m = get_mineral("cobalt")
    assert m["symbol"] == "Co"
    assert m["import_dependency_pct"] == 76
    assert m["dod_critical"] is True
    assert m["substitutability"] == "low"


def test_all_minerals_have_required_keys():
    required = {"full_name", "symbol", "import_dependency_pct", "top_suppliers",
                "substitutability", "dod_critical", "defense_applications",
                "spectral_match", "source_note"}
    for name, mineral in CATALOG.items():
        missing = required - set(mineral.keys())
        assert not missing, f"{name} missing keys: {missing}"


def test_import_dependency_in_range():
    for name, mineral in CATALOG.items():
        pct = mineral["import_dependency_pct"]
        assert 0 <= pct <= 100, f"{name}: import_dependency_pct={pct} out of range"


def test_substitutability_values_valid():
    valid = {"none", "low", "medium", "high"}
    for name, mineral in CATALOG.items():
        assert mineral["substitutability"] in valid, f"{name}: invalid substitutability"


def test_top_suppliers_have_country_and_share():
    for name, mineral in CATALOG.items():
        for s in mineral["top_suppliers"]:
            assert "country" in s, f"{name}: supplier missing 'country'"
            assert "share_pct" in s, f"{name}: supplier missing 'share_pct'"
            assert 0 <= s["share_pct"] <= 100, f"{name}: share_pct out of range"


def test_spectral_match_contains_valid_classes():
    valid_classes = {"C", "B", "P", "D", "S", "Q", "Sq", "M", "X", "E", "V", "A", "K", "L"}
    for name, mineral in CATALOG.items():
        for cls in mineral["spectral_match"]:
            assert cls in valid_classes, f"{name}: invalid spectral class '{cls}'"


def test_gallium_has_export_control_note():
    m = get_mineral("gallium")
    assert "2023" in m["source_note"] or "export" in m["source_note"].lower()


def test_dysprosium_near_total_china_dependency():
    m = get_mineral("dysprosium")
    assert m["import_dependency_pct"] == 100
    china_supplier = next((s for s in m["top_suppliers"] if s["country"] == "China"), None)
    assert china_supplier is not None
    assert china_supplier["share_pct"] >= 90
