"""
Deterministic supply-chain risk scoring.
Claude never touches this — all logic is traceable to config weights.
"""

from config import RISK_WEIGHTS, SUBSTITUTABILITY_SCORES, RISK_TIERS


def compute_risk_score(mineral: dict) -> dict:
    import_pct = mineral.get("import_dependency_pct", 0)
    substitutability = mineral.get("substitutability", "medium")
    dod_critical = mineral.get("dod_critical", False)

    import_score = round((import_pct / 100) * RISK_WEIGHTS["import_dependency"], 1)
    dod_score = RISK_WEIGHTS["dod_criticality"] if dod_critical else 0
    sub_score = SUBSTITUTABILITY_SCORES.get(substitutability, SUBSTITUTABILITY_SCORES["medium"])

    total = min(100, import_score + dod_score + sub_score)

    tier = "LOW"
    for label, (lo, hi) in RISK_TIERS.items():
        if lo <= total <= hi:
            tier = label
            break

    return {
        "import_score": import_score,
        "dod_score": dod_score,
        "substitutability_score": sub_score,
        "total": total,
        "tier": tier,
        "breakdown": {
            "import_dependency": {
                "value_pct": import_pct,
                "weight": RISK_WEIGHTS["import_dependency"],
                "points": import_score,
            },
            "dod_criticality": {
                "value": dod_critical,
                "weight": RISK_WEIGHTS["dod_criticality"],
                "points": dod_score,
            },
            "substitutability": {
                "value": substitutability,
                "weight": RISK_WEIGHTS["substitutability"],
                "points": sub_score,
            },
        },
    }
