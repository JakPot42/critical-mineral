"""
USGS Critical Minerals catalog — pre-populated from USGS Mineral Commodity Summaries 2024.
Source: U.S. Geological Survey, Mineral Commodity Summaries 2024,
        https://doi.org/10.3133/mcs2024
DoD criticality flags from: DoD Critical Materials Strategy and EO 14017 (Feb 2021)
        supply chain resilience review, released Feb 2022.

VERIFY: These figures are sourced from MCS 2024 and DoD documents current as of
June 2026. Import dependency percentages can shift year to year.
"""

CATALOG = {
    "neodymium": {
        "full_name": "Neodymium",
        "symbol": "Nd",
        "atomic_number": 60,
        "category": "Rare Earth Element (Light REE)",
        "import_dependency_pct": 94,
        "top_suppliers": [
            {"country": "China", "share_pct": 85, "note": "Dominant global producer and processor"},
            {"country": "Malaysia", "share_pct": 8, "note": "Lynas processing facility"},
            {"country": "Other", "share_pct": 7, "note": ""},
        ],
        "substitutability": "none",
        "dod_critical": True,
        "defense_applications": [
            "NdFeB permanent magnets in F-35 actuators, EAP motors, precision-guided munitions",
            "Electric motors in next-generation military vehicles",
            "Wind turbine generators for DoD installation energy independence",
        ],
        "spectral_match": ["C", "B", "P", "D"],
        "source_note": "USGS MCS 2024 p.124; DoD EO 14017 review (2022)",
    },
    "cobalt": {
        "full_name": "Cobalt",
        "symbol": "Co",
        "atomic_number": 27,
        "category": "Battery / Superalloy Metal",
        "import_dependency_pct": 76,
        "top_suppliers": [
            {"country": "Democratic Republic of Congo", "share_pct": 70, "note": "~70% of world mine production"},
            {"country": "China", "share_pct": 65, "note": "~65% of global refining capacity"},
            {"country": "Russia", "share_pct": 4, "note": "Norilsk Nickel operations"},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Superalloys in jet engine turbine blades (F-135, F-110)",
            "Samarium-cobalt permanent magnets (radiation-hard alternative to NdFeB)",
            "High-strength steel in munitions casings",
        ],
        "spectral_match": ["C", "B", "M", "S"],
        "source_note": "USGS MCS 2024 p.54; DoD EO 14017 review (2022)",
    },
    "tungsten": {
        "full_name": "Tungsten",
        "symbol": "W",
        "atomic_number": 74,
        "category": "Refractory Metal",
        "import_dependency_pct": 79,
        "top_suppliers": [
            {"country": "China", "share_pct": 82, "note": "Dominates global mine production"},
            {"country": "Vietnam", "share_pct": 5, "note": ""},
            {"country": "Russia", "share_pct": 3, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Kinetic energy penetrators (armor-piercing rounds)",
            "Radiation shielding in nuclear applications",
            "High-temperature aerospace components",
        ],
        "spectral_match": ["M", "S"],
        "source_note": "USGS MCS 2024 p.190; DoD EO 14017 review (2022)",
    },
    "platinum": {
        "full_name": "Platinum",
        "symbol": "Pt",
        "atomic_number": 78,
        "category": "Platinum-Group Metal (PGM)",
        "import_dependency_pct": 87,
        "top_suppliers": [
            {"country": "South Africa", "share_pct": 72, "note": "Bushveld Complex — world's largest PGM reserve"},
            {"country": "Russia", "share_pct": 12, "note": "Norilsk — geopolitically sensitive"},
            {"country": "Zimbabwe", "share_pct": 8, "note": ""},
        ],
        "substitutability": "medium",
        "dod_critical": True,
        "defense_applications": [
            "Catalytic converters in military vehicles",
            "Fuel cell catalysts for next-gen submarine power",
            "Electronic contacts and sensors in weapons systems",
        ],
        "spectral_match": ["C", "B", "P", "D", "M"],
        "source_note": "USGS MCS 2024 p.136; DoD EO 14017 review (2022)",
    },
    "palladium": {
        "full_name": "Palladium",
        "symbol": "Pd",
        "atomic_number": 46,
        "category": "Platinum-Group Metal (PGM)",
        "import_dependency_pct": 43,
        "top_suppliers": [
            {"country": "South Africa", "share_pct": 38, "note": ""},
            {"country": "Russia", "share_pct": 42, "note": "~42% of world production — critical exposure"},
            {"country": "Canada", "share_pct": 10, "note": ""},
        ],
        "substitutability": "medium",
        "dod_critical": True,
        "defense_applications": [
            "Catalytic converters",
            "Multi-layer ceramic capacitors in electronics",
            "Hydrogen purification membranes",
        ],
        "spectral_match": ["C", "B", "P", "D", "M"],
        "source_note": "USGS MCS 2024 p.136; DoD EO 14017 review (2022)",
    },
    "dysprosium": {
        "full_name": "Dysprosium",
        "symbol": "Dy",
        "atomic_number": 66,
        "category": "Rare Earth Element (Heavy REE)",
        "import_dependency_pct": 100,
        "top_suppliers": [
            {"country": "China", "share_pct": 99, "note": "Near-total monopoly on processing"},
            {"country": "Other", "share_pct": 1, "note": ""},
        ],
        "substitutability": "none",
        "dod_critical": True,
        "defense_applications": [
            "NdFeB magnet additive — prevents demagnetization at high temperatures (essential for F-35 at operating temps)",
            "Nuclear reactor control rods",
            "Laser materials for targeting systems",
        ],
        "spectral_match": ["C", "B", "P", "D"],
        "source_note": "USGS MCS 2024 p.60; DoD EO 14017 review (2022)",
    },
    "gallium": {
        "full_name": "Gallium",
        "symbol": "Ga",
        "atomic_number": 31,
        "category": "Semiconductor Metal",
        "import_dependency_pct": 100,
        "top_suppliers": [
            {"country": "China", "share_pct": 98, "note": "China imposed export controls on Ga in July 2023"},
            {"country": "Other", "share_pct": 2, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "GaN (gallium nitride) semiconductors in radar and electronic warfare",
            "GaAs (gallium arsenide) in satellite communications",
            "IR detectors and laser diodes in targeting systems",
        ],
        "spectral_match": ["C", "M"],
        "source_note": "USGS MCS 2024 p.72; China export controls: July 2023 MofCOM announcement",
    },
    "germanium": {
        "full_name": "Germanium",
        "symbol": "Ge",
        "atomic_number": 32,
        "category": "Semiconductor Metal",
        "import_dependency_pct": 95,
        "top_suppliers": [
            {"country": "China", "share_pct": 60, "note": "China imposed export controls on Ge in July 2023"},
            {"country": "Russia", "share_pct": 5, "note": ""},
            {"country": "Canada", "share_pct": 15, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Infrared optics in thermal imaging (FLIR) for aircraft and armored vehicles",
            "Fiber optic cables in military communications",
            "Night-vision devices",
        ],
        "spectral_match": ["C", "M"],
        "source_note": "USGS MCS 2024 p.76; China export controls: July 2023 MofCOM announcement",
    },
    "manganese": {
        "full_name": "Manganese",
        "symbol": "Mn",
        "atomic_number": 25,
        "category": "Ferroalloy Metal",
        "import_dependency_pct": 100,
        "top_suppliers": [
            {"country": "South Africa", "share_pct": 37, "note": ""},
            {"country": "Gabon", "share_pct": 20, "note": ""},
            {"country": "Australia", "share_pct": 16, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Steelmaking — no substitute at commercial scale (100% import dependency, zero domestic mining)",
            "Aluminum alloy strengthening in aircraft and armor",
            "Lithium-manganese-oxide (LMO) batteries",
        ],
        "spectral_match": ["C", "S"],
        "source_note": "USGS MCS 2024 p.106; DLA Strategic Materials list",
    },
    "niobium": {
        "full_name": "Niobium",
        "symbol": "Nb",
        "atomic_number": 41,
        "category": "Refractory Metal",
        "import_dependency_pct": 100,
        "top_suppliers": [
            {"country": "Brazil", "share_pct": 94, "note": "CBMM controls ~85% of world production — extreme concentration"},
            {"country": "Canada", "share_pct": 5, "note": ""},
            {"country": "Other", "share_pct": 1, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "High-strength low-alloy (HSLA) steels in armored vehicles and naval vessels",
            "Superalloys in jet engine hot sections",
            "Superconducting magnets in research reactors",
        ],
        "spectral_match": ["C", "P"],
        "source_note": "USGS MCS 2024 p.118; DoD EO 14017 review (2022)",
    },
    "chromium": {
        "full_name": "Chromium",
        "symbol": "Cr",
        "atomic_number": 24,
        "category": "Ferroalloy Metal",
        "import_dependency_pct": 72,
        "top_suppliers": [
            {"country": "South Africa", "share_pct": 44, "note": "Bushveld Complex dominates reserves"},
            {"country": "Kazakhstan", "share_pct": 19, "note": ""},
            {"country": "India", "share_pct": 12, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Stainless and tool steels in weapons and vehicles",
            "Chrome plating on aircraft hydraulics and landing gear",
            "Superalloys in gas turbine hot sections",
        ],
        "spectral_match": ["S", "V"],
        "source_note": "USGS MCS 2024 p.52; DLA Strategic Materials list",
    },
    "lithium": {
        "full_name": "Lithium",
        "symbol": "Li",
        "atomic_number": 3,
        "category": "Battery Metal",
        "import_dependency_pct": 25,
        "top_suppliers": [
            {"country": "Chile", "share_pct": 26, "note": "Atacama brine deposits"},
            {"country": "Argentina", "share_pct": 6, "note": ""},
            {"country": "Australia", "share_pct": 49, "note": "Hard rock spodumene — geopolitically stable"},
        ],
        "substitutability": "medium",
        "dod_critical": True,
        "defense_applications": [
            "Li-ion batteries in unmanned systems (UAVs, UUVs, UGVs)",
            "Next-generation soldier power systems",
            "Grid storage for DoD installation energy resilience",
        ],
        "spectral_match": ["C", "B"],
        "source_note": "USGS MCS 2024 p.100; DoD EO 14017 review (2022)",
    },
    "vanadium": {
        "full_name": "Vanadium",
        "symbol": "V",
        "atomic_number": 23,
        "category": "Ferroalloy / Battery Metal",
        "import_dependency_pct": 96,
        "top_suppliers": [
            {"country": "China", "share_pct": 57, "note": ""},
            {"country": "Russia", "share_pct": 19, "note": "Dual China+Russia exposure is significant"},
            {"country": "South Africa", "share_pct": 9, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "High-strength steel in armor plate and submarine hulls",
            "Vanadium redox flow batteries for stationary installation energy storage",
            "Aerospace titanium-vanadium alloys",
        ],
        "spectral_match": ["C", "S"],
        "source_note": "USGS MCS 2024 p.192; DoD EO 14017 review (2022)",
    },
    "tantalum": {
        "full_name": "Tantalum",
        "symbol": "Ta",
        "atomic_number": 73,
        "category": "Refractory Metal",
        "import_dependency_pct": 78,
        "top_suppliers": [
            {"country": "DRC", "share_pct": 40, "note": "Conflict minerals oversight required"},
            {"country": "Rwanda", "share_pct": 25, "note": ""},
            {"country": "Nigeria", "share_pct": 11, "note": ""},
        ],
        "substitutability": "low",
        "dod_critical": True,
        "defense_applications": [
            "Tantalum capacitors in nearly all electronics — ubiquitous in weapons systems",
            "Superalloys in jet engine components",
            "Medical and implant-grade applications (no DoD defense use)",
        ],
        "spectral_match": ["C", "P"],
        "source_note": "USGS MCS 2024 p.174; DoD conflict minerals policy 2012",
    },
    "indium": {
        "full_name": "Indium",
        "symbol": "In",
        "atomic_number": 49,
        "category": "Semiconductor Metal",
        "import_dependency_pct": 76,
        "top_suppliers": [
            {"country": "China", "share_pct": 57, "note": "Dominant refiner"},
            {"country": "South Korea", "share_pct": 13, "note": ""},
            {"country": "Japan", "share_pct": 9, "note": ""},
        ],
        "substitutability": "medium",
        "dod_critical": False,
        "defense_applications": [
            "Indium tin oxide (ITO) transparent conductors in cockpit displays and touchscreens",
            "InGaAs detectors in night vision and LIDAR",
        ],
        "spectral_match": ["C"],
        "source_note": "USGS MCS 2024 p.86",
    },
}


def get_mineral(name: str) -> dict | None:
    """Case-insensitive lookup."""
    return CATALOG.get(name.lower().strip())


def list_minerals() -> list[str]:
    return sorted(CATALOG.keys())
