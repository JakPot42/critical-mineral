"""
Pre-seeded demo analyses for two flagship minerals.
Asteroid data verified against JPL NHATS (2024) and NASA SBDB.
Used when DEMO_MODE=True or when live NASA APIs are unavailable.
"""

DEMO_ANALYSES = {
    "neodymium": {
        "mineral_name": "neodymium",
        "asteroids": [
            {
                "designation": "101955",
                "full_name": "(101955) Bennu",
                "spectral_class": "B",
                "diameter_km": 0.492,
                "albedo": 0.044,
                "H": 20.7,
                "min_dv_km_s": 5.06,
                "estimated_mass_mt": 8.5e10,
                "mineral_match_rationale": (
                    "B-type (C subclass): OSIRIS-REx confirmed carbonaceous composition. "
                    "Returned samples show hydrated silicates and organic-rich material; "
                    "REE content consistent with CI chondrite analog at ~10–20 ppm Nd."
                ),
            },
            {
                "designation": "162173",
                "full_name": "(162173) Ryugu",
                "spectral_class": "C",
                "diameter_km": 0.900,
                "albedo": 0.045,
                "H": 18.8,
                "min_dv_km_s": 5.29,
                "estimated_mass_mt": 4.5e11,
                "mineral_match_rationale": (
                    "C-type: Hayabusa2 sample return confirmed Ivuna-type carbonaceous chondrite analog. "
                    "Aqueous alteration products present; REEs at cosmic abundance ratios."
                ),
            },
            {
                "designation": "65803",
                "full_name": "(65803) Didymos",
                "spectral_class": "S",
                "diameter_km": 0.780,
                "albedo": 0.150,
                "H": 18.2,
                "min_dv_km_s": 5.11,
                "estimated_mass_mt": 5.3e11,
                "mineral_match_rationale": (
                    "Sq-type (S subclass, closest to ordinary chondrites): lower REE density than C-type. "
                    "Included as third candidate given low delta-v; REE extraction would be less favorable "
                    "than carbonaceous bodies but physical accessibility is excellent. DART mission target."
                ),
            },
        ],
        "brief_used_demo": True,
    },
    "cobalt": {
        "mineral_name": "cobalt",
        "asteroids": [
            {
                "designation": "6178",
                "full_name": "(6178) 1986 DA",
                "spectral_class": "M",
                "diameter_km": 1.700,
                "albedo": 0.173,
                "H": 15.7,
                "min_dv_km_s": 6.82,
                "estimated_mass_mt": 1.4e13,
                "mineral_match_rationale": (
                    "M-type metallic asteroid: radar observations and albedo confirm metallic composition. "
                    "Radar cross-section of ~0.88 km² consistent with nickel-iron body. "
                    "Cobalt at ~0.5 wt% in NiFe alloy — same concentration as iron meteorites. "
                    "Estimated cobalt inventory: ~70 million metric tons."
                ),
            },
            {
                "designation": "3554",
                "full_name": "(3554) Amun",
                "spectral_class": "M",
                "diameter_km": 2.500,
                "albedo": 0.170,
                "H": 15.0,
                "min_dv_km_s": 7.50,
                "estimated_mass_mt": 4.4e13,
                "mineral_match_rationale": (
                    "M-type metallic asteroid: composition consistent with NiFe metallic core fragment. "
                    "Cobalt estimated at ~0.5 wt% in metallic phase. Often cited in early asteroid "
                    "resource economics literature (Lewis 1993) as a benchmark metallic NEA."
                ),
            },
            {
                "designation": "101955",
                "full_name": "(101955) Bennu",
                "spectral_class": "B",
                "diameter_km": 0.492,
                "albedo": 0.044,
                "H": 20.7,
                "min_dv_km_s": 5.06,
                "estimated_mass_mt": 8.5e10,
                "mineral_match_rationale": (
                    "B-type (C subclass): CI chondrites contain cobalt at ~700 ppm (above Earth crust avg of ~25 ppm). "
                    "Lower delta-v than the M-type candidates makes Bennu the most accessible option, "
                    "though at lower cobalt concentration per unit mass."
                ),
            },
        ],
        "brief_used_demo": True,
    },
}
