"""
Match minerals to asteroid candidates using spectral type and delta-v.
Returns the top-3 most accessible matching asteroids.
"""

from config import SPECTRAL_MINERAL_MAP
from asteroid_client import estimate_tonnage


def find_candidates(
    mineral_name: str,
    nhats: dict[str, float],
    neo_catalog: list[dict],
    top_n: int = 3,
) -> list[dict]:
    """
    mineral_name: lowercase mineral name
    nhats: {des → min_dv} from NHATS API
    neo_catalog: list of NEOs with spectral types from SBDB

    Returns top_n asteroids sorted by ascending delta-v.
    """
    target_specs = SPECTRAL_MINERAL_MAP.get(mineral_name.lower(), [])

    # Build NHATS lookup (normalize whitespace in designations)
    nhats_norm = {_norm(k): v for k, v in nhats.items()}

    candidates = []
    for neo in neo_catalog:
        spec = neo.get("spec")
        if not spec:
            continue
        if spec not in target_specs:
            continue

        des = neo["pdes"]
        dv = nhats_norm.get(_norm(des))
        if dv is None:
            continue

        diameter_km = neo.get("diameter_km")
        tonnage = estimate_tonnage(diameter_km, spec) if diameter_km else None

        candidates.append({
            "designation": des,
            "full_name": neo.get("full_name", des).strip(),
            "spectral_class": spec,
            "diameter_km": round(diameter_km, 3) if diameter_km else None,
            "albedo": neo.get("albedo"),
            "H": neo.get("H"),
            "min_dv_km_s": round(dv, 2),
            "estimated_mass_mt": round(tonnage) if tonnage else None,
            "mineral_match_rationale": _rationale(mineral_name, spec),
        })

    # Primary sort: delta-v ascending; secondary: diameter descending (bigger is better)
    candidates.sort(
        key=lambda x: (x["min_dv_km_s"], -(x["diameter_km"] or 0))
    )
    return candidates[:top_n]


def _rationale(mineral: str, spec: str) -> str:
    """Short one-sentence rationale for why this spectral type matches the mineral."""
    notes = {
        ("neodymium",  "C"): "Carbonaceous chondrites contain REEs at cosmic abundance ratios; CI/CM classes elevated vs Earth's crust.",
        ("neodymium",  "B"): "B-type (C subclass) are primitive carbonaceous bodies with REE content comparable to CI chondrites.",
        ("neodymium",  "P"): "P-type dark primitive bodies are compositionally similar to carbonaceous chondrites.",
        ("neodymium",  "D"): "D-type outer-belt bodies are carbon-rich with similar REE profiles to CI chondrites.",
        ("cobalt",     "C"): "CI carbonaceous chondrites have cobalt concentrations ~700 ppm — above Earth's crustal average.",
        ("cobalt",     "M"): "Metallic M-type asteroids contain cobalt as a trace component of the nickel-iron alloy.",
        ("cobalt",     "S"): "S-type silicaceous asteroids contain cobalt in olivine and pyroxene phases.",
        ("cobalt",     "B"): "B-type (C subclass) bodies contain cobalt in carbonaceous chondrite-like concentrations.",
        ("platinum",   "C"): "Carbonaceous chondrites (CI) have PGM concentrations 10–100× Earth's mantle — the strongest case for space PGMs.",
        ("platinum",   "M"): "M-type metallic asteroids likely contain PGMs concentrated in the nickel-iron phase, as in iron meteorites.",
        ("platinum",   "B"): "B-type bodies are primitive carbonaceous objects with elevated PGM content vs terrestrial ores.",
        ("gallium",    "C"): "Gallium occurs at ~10 ppm in CI chondrites; byproduct of zinc smelting makes it asteroid-extractable.",
        ("gallium",    "M"): "Metallic M-type asteroids concentrate gallium in the nickel-iron phase.",
        ("germanium",  "C"): "Germanium found at ~30 ppm in CI chondrites; concentrated in metallic phases of iron meteorites.",
        ("germanium",  "M"): "Iron meteorites (M-type analogs) contain germanium in the Widmanstätten pattern nickel-iron.",
        ("tungsten",   "M"): "M-type metallic asteroids contain tungsten as a siderophile (iron-loving) trace element.",
        ("dysprosium", "C"): "Heavy REEs including dysprosium present in CI/CM carbonaceous chondrites at ppm levels.",
        ("manganese",  "C"): "Manganese is lithophile and present in carbonaceous chondrites; elevated in some aqueously altered bodies.",
        ("manganese",  "S"): "S-type silicaceous bodies contain manganese in olivine and pyroxene phases.",
        ("niobium",    "C"): "Niobium is refractory and present in primitive carbonaceous bodies at sub-ppm levels.",
        ("chromium",   "S"): "Chromium present in S-type silicates (chromite phase in ordinary chondrites).",
        ("lithium",    "C"): "Lithium present in CI chondrites; CI/CM meteorites show some of the highest cosmic Li concentrations.",
        ("vanadium",   "C"): "Vanadium is lithophile and present in carbonaceous chondrites at ~60 ppm.",
        ("tantalum",   "C"): "Tantalum is refractory and present in primitive carbonaceous chondrites at sub-ppm trace levels.",
        ("indium",     "C"): "Indium is a chalcophile trace element; present in carbonaceous chondrites at ppb levels.",
        ("palladium",  "C"): "Palladium is a PGM; CI chondrites have Pd ~500 ppb — far above Earth's crustal average of ~1.5 ppb.",
        ("palladium",  "M"): "M-type metallic bodies likely contain PGMs concentrated in the nickel-iron phase.",
    }
    key = (mineral.lower(), spec)
    return notes.get(key, f"{spec}-type asteroids are compositionally associated with {mineral} occurrence in meteorite analogs.")


def _norm(des: str) -> str:
    return des.strip().lower().replace("  ", " ")
