"""
All configuration in one place. Every number has a source.
"""

DEMO_MODE = True
CLAUDE_MODEL = "claude-haiku-4-5-20251001"

# NASA API endpoints
NHATS_API = "https://ssd-api.jpl.nasa.gov/nhats.api"
SBDB_QUERY_API = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
SBDB_API = "https://ssd-api.jpl.nasa.gov/sbdb.api"

# NHATS accessibility threshold (km/s from LEO)
# 12 km/s covers ~95% of known accessible NEAs per JPL NHATS documentation
NHATS_MAX_DV = 12.0

# Risk scoring weights (sum to 100)
# Higher weight on import dependency — it's the most measurable and policy-relevant factor
RISK_WEIGHTS = {
    "import_dependency": 50,   # 0–50 pts
    "dod_criticality":   25,   # 0 or 25 pts
    "substitutability":  25,   # 0–25 pts
}

# Substitutability → score mapping
# Source: USGS Mineral Commodity Summaries substitutability ratings
SUBSTITUTABILITY_SCORES = {
    "none":   25,
    "low":    18,
    "medium": 10,
    "high":    0,
}

# Risk tiers
RISK_TIERS = {
    "CRITICAL": (81, 100),
    "HIGH":     (61, 80),
    "MEDIUM":   (31, 60),
    "LOW":      (0, 30),
}

# Asteroid density by spectral type (g/cm³)
# Source: Britt et al. (2002), Carry (2012) bulk density review
SPECTRAL_DENSITY = {
    "C":  1.33,   # carbonaceous — porous, water-rich
    "B":  1.26,   # B-type (C subclass) — even more porous
    "P":  1.50,   # P-type (dark primitive)
    "D":  1.50,   # D-type (dark, outer belt)
    "S":  2.71,   # silicaceous — olivine/pyroxene mix
    "Q":  2.60,   # Q-type (S subclass, freshly exposed)
    "Sq": 2.65,   # Sq-type
    "M":  5.32,   # metallic — nickel-iron
    "X":  3.00,   # X-type (ambiguous — could be M, E, or P)
    "E":  3.20,   # enstatite chondrite
    "V":  3.35,   # V-type (basaltic — Vesta-like)
    "A":  3.70,   # olivine-dominated
    "K":  2.90,   # K-type
    "L":  2.90,   # L-type
}
DEFAULT_DENSITY = 2.0   # g/cm³ — conservative for unknown types

# Spectral type → matched minerals
# Source: Rivkin et al. (2015) mineral/spectral review; Bottke et al. space resource literature
SPECTRAL_MINERAL_MAP = {
    "platinum":   ["C", "B", "P", "D", "M"],
    "palladium":  ["C", "B", "P", "D", "M"],
    "iridium":    ["C", "B", "M"],
    "rhodium":    ["C", "B", "M"],
    "neodymium":  ["C", "B", "P", "D"],
    "dysprosium": ["C", "B", "P", "D"],
    "cobalt":     ["C", "B", "M", "S"],
    "nickel":     ["S", "M", "X"],
    "iron":       ["S", "M", "X"],
    "tungsten":   ["M", "S"],
    "chromium":   ["S", "V"],
    "manganese":  ["C", "S"],
    "vanadium":   ["C", "S"],
    "lithium":    ["C", "B"],
    "gallium":    ["C", "M"],
    "germanium":  ["C", "M"],
    "indium":     ["C"],
    "niobium":    ["C", "P"],
    "tantalum":   ["C", "P"],
}
