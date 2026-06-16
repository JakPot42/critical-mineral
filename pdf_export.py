"""ReportLab PDF export — DEMO watermark on all pages."""

from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY


TIER_COLORS = {
    "CRITICAL": colors.HexColor("#dc2626"),
    "HIGH":     colors.HexColor("#d97706"),
    "MEDIUM":   colors.HexColor("#ca8a04"),
    "LOW":      colors.HexColor("#16a34a"),
}


def generate_pdf(mineral: dict, risk: dict, asteroids: list[dict], brief: str) -> bytes:
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.85 * inch,
        rightMargin=0.85 * inch,
        topMargin=0.9 * inch,
        bottomMargin=0.9 * inch,
    )
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"],
        fontSize=18, textColor=colors.HexColor("#1e293b"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "Subtitle", parent=styles["Normal"],
        fontSize=10, textColor=colors.HexColor("#64748b"),
        spaceAfter=12,
    )
    section_style = ParagraphStyle(
        "Section", parent=styles["Heading2"],
        fontSize=12, textColor=colors.HexColor("#1e40af"),
        spaceBefore=14, spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "Body", parent=styles["Normal"],
        fontSize=9, leading=14, textColor=colors.HexColor("#334155"),
        alignment=TA_JUSTIFY,
    )
    small_style = ParagraphStyle(
        "Small", parent=styles["Normal"],
        fontSize=8, textColor=colors.HexColor("#94a3b8"),
    )
    mono_style = ParagraphStyle(
        "Mono", parent=styles["Code"],
        fontSize=8, textColor=colors.HexColor("#1e293b"),
    )

    # Header
    story.append(Paragraph(
        f"Critical Mineral Space Resource Assessment: {mineral['full_name']} ({mineral.get('symbol', '')})",
        title_style,
    ))
    story.append(Paragraph(
        f"{mineral.get('category', '')} · Supply-Chain Risk: <b><font color=\"{TIER_COLORS[risk['tier']].hexval() if hasattr(TIER_COLORS[risk['tier']], 'hexval') else '#000000'}\">{risk['tier']}</font></b> ({risk['total']:.0f}/100)",
        subtitle_style,
    ))
    story.append(Paragraph(
        "⚠️  DEMO — All data from public sources (USGS MCS 2024, JPL NHATS, NASA SBDB). Not classified.",
        ParagraphStyle("Warn", parent=styles["Normal"], fontSize=8,
                       textColor=colors.HexColor("#dc2626"), spaceAfter=12),
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#e2e8f0")))

    # Terrestrial risk section
    story.append(Paragraph("1. Terrestrial Supply Chain Risk", section_style))

    risk_rows = [
        ["Factor", "Value", "Points"],
        ["Import Dependency",
         f"{mineral['import_dependency_pct']}%",
         f"{risk['breakdown']['import_dependency']['points']:.0f} / {risk['breakdown']['import_dependency']['weight']}"],
        ["DoD Critical Materials",
         "Yes" if mineral["dod_critical"] else "No",
         f"{risk['dod_score']:.0f} / {risk['breakdown']['dod_criticality']['weight']}"],
        ["Substitutability",
         mineral["substitutability"].capitalize(),
         f"{risk['substitutability_score']} / {risk['breakdown']['substitutability']['weight']}"],
        ["TOTAL RISK SCORE", "", f"{risk['total']:.0f} / 100 — {risk['tier']}"],
    ]
    risk_table = Table(risk_rows, colWidths=[3 * inch, 2 * inch, 2.2 * inch])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e40af")),
        ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
        ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",   (0, 0), (-1, -1), 9),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.HexColor("#f8fafc"), colors.white]),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#fef9c3")),
        ("FONTNAME",   (0, -1), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(risk_table)
    story.append(Spacer(1, 8))

    suppliers_text = " | ".join(
        f"{s['country']} {s['share_pct']}%" for s in mineral.get("top_suppliers", [])
    )
    story.append(Paragraph(f"<b>Primary suppliers:</b> {suppliers_text}", body_style))
    story.append(Paragraph(f"<b>Source:</b> {mineral.get('source_note', 'USGS MCS 2024')}", small_style))

    # Defense applications
    story.append(Paragraph("Defense Applications", section_style))
    for app in mineral.get("defense_applications", []):
        story.append(Paragraph(f"• {app}", body_style))
    story.append(Spacer(1, 6))

    # Asteroid candidates
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0")))
    story.append(Paragraph("2. Near-Earth Asteroid Candidates (JPL NHATS + NASA SBDB)", section_style))

    if asteroids:
        ast_rows = [["#", "Designation", "Type", "Δv (km/s)", "Diameter (km)", "Est. Mass (Mt)"]]
        for i, a in enumerate(asteroids, 1):
            ast_rows.append([
                str(i),
                a["full_name"],
                a["spectral_class"],
                f"{a['min_dv_km_s']:.2f}",
                f"{a['diameter_km']:.3f}" if a.get("diameter_km") else "—",
                f"{a['estimated_mass_mt']:,.0f}" if a.get("estimated_mass_mt") else "—",
            ])
        ast_table = Table(ast_rows, colWidths=[0.3*inch, 2.1*inch, 0.6*inch, 0.8*inch, 1.0*inch, 1.1*inch])
        ast_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f59e0b")),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.HexColor("#1c1917")),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE",   (0, 0), (-1, -1), 8),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fffbeb"), colors.white]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("PADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(ast_table)
        story.append(Spacer(1, 4))
        story.append(Paragraph(
            "Δv = minimum delta-v from LEO per JPL NHATS. "
            "Mass estimated from SBDB diameter + spectral-class bulk density (Britt et al. 2002).",
            small_style,
        ))
    else:
        story.append(Paragraph(
            "No spectral-matched NHATS candidates identified in current accessibility window.",
            body_style,
        ))

    # Strategic brief
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#e2e8f0")))
    story.append(Paragraph("3. Strategic Brief", section_style))
    for para in brief.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        if para.isupper() or (len(para) < 40 and para == para.upper()):
            story.append(Paragraph(f"<b>{para}</b>", body_style))
        else:
            story.append(Paragraph(para, body_style))
        story.append(Spacer(1, 4))

    doc.build(story, onFirstPage=_watermark, onLaterPages=_watermark)
    return buf.getvalue()


def _watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 52)
    canvas.setFillColor(colors.HexColor("#e2e8f0"))
    canvas.setFillAlpha(0.35)
    canvas.translate(4.25 * inch, 5.5 * inch)
    canvas.rotate(45)
    canvas.drawCentredString(0, 0, "DEMO")
    canvas.restoreState()
