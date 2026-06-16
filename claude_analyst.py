"""
Claude generates the strategic brief.
The brief synthesizes deterministic outputs — Claude writes prose, not policy.
Pattern: catch Exception (not anthropic.APIError) per portfolio standard.
"""

import anthropic
from config import CLAUDE_MODEL


class MineralAnalysisError(Exception):
    pass


def generate_brief(
    mineral: dict,
    risk: dict,
    asteroids: list[dict],
    demo_mode: bool = True,
) -> str:
    """
    Generate a one-page strategic brief synthesizing terrestrial risk + space alternatives.
    Returns the brief as a plain-text string.
    """
    if demo_mode:
        return _demo_brief(mineral["full_name"])

    client = anthropic.Anthropic()

    asteroid_text = ""
    for i, a in enumerate(asteroids, 1):
        diameter = f"{a['diameter_km']:.2f} km" if a.get("diameter_km") else "diameter unknown"
        tonnage = f"{a['estimated_mass_mt']:,.0f} metric tons" if a.get("estimated_mass_mt") else "mass unestimated"
        asteroid_text += (
            f"  {i}. {a['full_name']} ({a['designation']})\n"
            f"     Spectral class: {a['spectral_class']}-type | "
            f"Delta-v from LEO: {a['min_dv_km_s']} km/s | "
            f"Diameter: {diameter} | Estimated mass: {tonnage}\n"
            f"     Match rationale: {a['mineral_match_rationale']}\n"
        )
    if not asteroid_text:
        asteroid_text = "  No spectral-matched candidates found in current NHATS accessibility window.\n"

    top_suppliers = ", ".join(
        f"{s['country']} ({s['share_pct']}%)" for s in mineral.get("top_suppliers", [])
    )
    defense_apps = "\n".join(f"  - {d}" for d in mineral.get("defense_applications", []))

    prompt = f"""You are a strategic analyst preparing a one-page classified-adjacent brief for a DoD policy audience.
The subject is supply chain risk and space-based resource alternatives for {mineral['full_name']}.

TERRESTRIAL RISK DATA:
- Mineral: {mineral['full_name']} ({mineral.get('symbol', '')})
- Category: {mineral.get('category', '')}
- Import dependency: {mineral['import_dependency_pct']}% of US supply imported
- Primary suppliers: {top_suppliers}
- Substitutability: {mineral['substitutability'].upper()}
- DoD Critical Materials designation: {'YES' if mineral['dod_critical'] else 'NO'}
- Risk score: {risk['total']:.0f}/100 ({risk['tier']})
- Defense applications:
{defense_apps}

NEAR-EARTH ASTEROID CANDIDATES (JPL NHATS + SBDB, spectral match to {mineral['full_name']}):
{asteroid_text}

Write a one-page strategic brief with these four sections:
1. SITUATION: The current import dependency problem — what makes this mineral strategically vulnerable right now.
2. DEFENSE EXPOSURE: What specific defense capabilities are at risk and why substitution is difficult.
3. SPACE HEDGE: What the asteroid data says — be honest about the timeline (space mining is a 2040s+ proposition), but explain why the strategic case for tracking these resources today is sound.
4. NEAR-TERM RECOMMENDATIONS: 2–3 concrete, realistic recommendations a DoD planner could act on within the next 3–5 years (domestic stockpiling, allied nation sourcing, processing capacity investment, R&D).

Tone: authoritative, direct, no hedging or padding. Target length: 400–500 words.
Do not include any classification markings. This is unclassified analytical work."""

    try:
        msg = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return msg.content[0].text
    except MineralAnalysisError:
        raise
    except Exception as exc:
        raise MineralAnalysisError(f"Claude API error: {exc}") from exc


def _demo_brief(mineral_name: str) -> str:
    briefs = {
        "Neodymium": """SITUATION
The United States imports 94% of its neodymium supply, with approximately 85% of that originating from China. Neodymium is not a technology risk — it is a manufacturing and processing chokepoint. China controls not only the majority of global mine production but also the downstream separation, alloying, and magnet fabrication capacity. An export restriction on neodymium compounds — similar to China's 2023 restrictions on gallium and germanium — could affect US defense procurement within 6–18 months given current stockpile levels.

DEFENSE EXPOSURE
Every NdFeB (neodymium-iron-boron) permanent magnet in US defense systems runs through this supply chain. The F-35's flight control actuators, the precision guidance fins on AGM-88 HARMs, and the drive motors in next-generation unmanned platforms all use NdFeB magnets. There is no commercial-scale alternative: samarium-cobalt magnets (a rare substitute) require cobalt, which is itself critically dependent on DRC and Chinese refining. Ferrite magnets are inadequate for high-performance applications. The substitutability rating is correctly classified as NONE for high-performance defense use cases.

SPACE HEDGE
Carbonaceous (C-type) near-Earth asteroids contain rare earth elements at concentrations consistent with CI chondrite analogs — roughly 10–20 ppm for neodymium. Three NHATS-accessible C-type candidates are identified above, all reachable from LEO at delta-v values comparable to or below the Earth-Moon transfer. Space mining is realistically a 2040s-and-beyond proposition; no current architecture makes asteroid REE extraction economically competitive with terrestrial mining. The strategic case is not economics — it is optionality. Characterizing these resources now, through robotic missions and spectral surveys, positions the US to exercise that option if terrestrial supply is weaponized.

NEAR-TERM RECOMMENDATIONS
1. STOCKPILE: Expand the National Defense Stockpile target for neodymium oxide from its current level to a 3-year defense industrial base consumption reserve. Current stockpile holdings are classified; the gap is known to be significant.
2. PROCESSING CAPACITY: Fund domestic rare earth separation capacity at MP Materials (Mountain Pass) and Lynas USA (Texas) through DoD's Defense Production Act Title III authorities. Processing independence from Chinese facilities is achievable within 5 years if investment is sustained.
3. SURVEY: Commission spectral characterization of the top 10 NHATS-accessible C-type NEAs via next available Earth-flyby opportunities. Low-cost characterization missions (SCOUT-class) can confirm composition at a fraction of a mining mission cost.""",
        "Cobalt": """SITUATION
The United States imports 76% of its cobalt, with the Democratic Republic of Congo producing approximately 70% of world mine supply. While the DRC is not an adversary nation, it presents a different category of supply risk: political instability, artisanal mining dependence, and the fact that approximately 65% of global cobalt refining capacity is controlled by Chinese firms operating in the DRC. An effective chokepoint therefore exists at the refining stage even for non-Chinese ore. Secondary exposure exists through Russia (Norilsk Nickel), which contributes roughly 4% of global cobalt production.

DEFENSE EXPOSURE
Cobalt's defense exposure operates across two distinct threat surfaces. First, superalloy applications: cobalt-based superalloys are used in the hot sections of every US jet engine in service (F-135 for the F-35, F-110 for F-16 variants, T-700 for helicopters). These cannot be substituted in existing engine designs without re-engineering and re-certification. Second, samarium-cobalt permanent magnets are used in applications requiring high-temperature stability where NdFeB magnets fail — including radar systems and some weapons guidance components. Both uses are DoD-critical and both lack near-term substitutes.

SPACE HEDGE
Cobalt is a siderophile (iron-loving) element concentrated in metallic asteroid cores. Both C-type (carbonaceous chondrite) and M-type (metallic) near-Earth asteroids carry cobalt at concentrations above Earth's crustal average. M-type asteroids are particularly compelling: the nickel-iron matrix of metallic asteroids contains cobalt at concentrations comparable to the DRC's highest-grade ore deposits. The three NHATS candidates above include at least one M-type object, which represents the highest cobalt density per unit volume of any accessible asteroid class. As with all space resources, the relevant timeline is 2040s for extraction; the relevant action today is characterization and strategic awareness.

NEAR-TERM RECOMMENDATIONS
1. ALLIED SOURCING: Prioritize cobalt sourcing agreements with Australia, Canada, and Finland — all have domestic cobalt production or refining capacity and are Five Eyes or NATO partners. The Biden-era Critical Minerals Agreement framework should be extended specifically to cover DoD procurement.
2. REFINING INDEPENDENCE: Fund domestic cobalt sulfate refining capacity through DPA Title III. The US currently has essentially no commercial cobalt refining capacity — all ore is processed abroad, primarily in China.
3. RECYCLING: Mandate end-of-life cobalt recovery from retired defense systems. Superalloy scrap from decommissioned engines is a significant secondary supply source that is currently underutilized.""",
    }
    return briefs.get(mineral_name, f"[Demo brief not pre-generated for {mineral_name}. Provide ANTHROPIC_API_KEY to generate live briefs.]")
