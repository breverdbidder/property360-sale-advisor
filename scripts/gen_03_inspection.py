"""
Generate 03_inspection_report.pdf — Pre-Listing Property Inspection Report
for Palm Bay Palms Apartments case study.

Multi-page professional inspection report (10 pages) covering structural,
roofing, plumbing, electrical, HVAC, environmental, unit interiors, and
a capital expenditure summary.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Table,
    TableStyle,
    Spacer,
    PageBreak,
)


# ---------------------------------------------------------------------------
# Color constants
# ---------------------------------------------------------------------------
NAVY_COLOR = HexColor(f"#{NAVY}")
LIGHT_GRAY = HexColor("#F5F5F5")
MEDIUM_GRAY = HexColor("#E0E0E0")
DARK_GRAY = HexColor("#333333")
WHITE_COLOR = white
HIGH_COLOR = HexColor("#FFEBEE")
MEDIUM_COLOR = HexColor("#FFF3E0")
LOW_COLOR = HexColor("#E8F5E9")


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles():
    """Return a dictionary of ParagraphStyles for the report."""
    styles = getSampleStyleSheet()

    custom = {}

    custom["cover_title"] = ParagraphStyle(
        "CoverTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=28,
        textColor=NAVY_COLOR,
        alignment=TA_CENTER,
        spaceAfter=24,
    )
    custom["cover_subtitle"] = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=18,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=8,
    )
    custom["cover_detail"] = ParagraphStyle(
        "CoverDetail",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=16,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    custom["page_title"] = ParagraphStyle(
        "PageTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=22,
        textColor=NAVY_COLOR,
        spaceAfter=14,
        spaceBefore=4,
    )
    custom["section_header"] = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=NAVY_COLOR,
        spaceAfter=8,
        spaceBefore=12,
    )
    custom["body"] = ParagraphStyle(
        "BodyText2",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=DARK_GRAY,
        spaceAfter=6,
    )
    custom["body_bold"] = ParagraphStyle(
        "BodyBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=DARK_GRAY,
        spaceAfter=6,
    )
    custom["bullet"] = ParagraphStyle(
        "BulletItem",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=DARK_GRAY,
        leftIndent=20,
        spaceAfter=4,
        bulletIndent=8,
    )
    custom["table_header"] = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=WHITE_COLOR,
        alignment=TA_CENTER,
    )
    custom["table_cell"] = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
    )
    custom["table_cell_center"] = ParagraphStyle(
        "TableCellCenter",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
        alignment=TA_CENTER,
    )
    custom["table_cell_right"] = ParagraphStyle(
        "TableCellRight",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
        alignment=TA_RIGHT,
    )
    custom["table_cell_bold"] = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
    )
    custom["table_cell_bold_right"] = ParagraphStyle(
        "TableCellBoldRight",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
        alignment=TA_RIGHT,
    )
    custom["footer"] = ParagraphStyle(
        "Footer",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=HexColor("#888888"),
        alignment=TA_CENTER,
    )

    return custom


# ---------------------------------------------------------------------------
# Footer callback — adds page numbers
# ---------------------------------------------------------------------------
def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#888888"))
    page_num = canvas.getPageNumber()
    text = f"Pre-Listing Inspection Report  |  Palm Bay Palms Apartments  |  Page {page_num}"
    canvas.drawCentredString(LETTER[0] / 2.0, 0.5 * inch, text)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Helper: bullet list
# ---------------------------------------------------------------------------
def bullet_items(items, st):
    """Return a list of Paragraph flowables with bullet markers."""
    result = []
    for item in items:
        result.append(
            Paragraph(f"\u2022  {item}", st["bullet"])
        )
    return result


# ---------------------------------------------------------------------------
# Helper: section with heading and body paragraphs
# ---------------------------------------------------------------------------
def section(title, paragraphs, st):
    """Return list of flowables for a titled section."""
    elems = [Paragraph(title, st["section_header"])]
    for p in paragraphs:
        elems.append(Paragraph(p, st["body"]))
    return elems


# ---------------------------------------------------------------------------
# Page 1: Cover Page
# ---------------------------------------------------------------------------
def page_cover(st):
    elems = []
    elems.append(Spacer(1, 1.5 * inch))

    # Horizontal rule at top
    rule_data = [["" ]]
    rule_table = Table(rule_data, colWidths=[6.5 * inch])
    rule_table.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 2, NAVY_COLOR),
    ]))
    elems.append(rule_table)
    elems.append(Spacer(1, 0.4 * inch))

    elems.append(Paragraph("PRE-LISTING PROPERTY<br/>INSPECTION REPORT", st["cover_title"]))
    elems.append(Spacer(1, 0.3 * inch))

    # Property info block
    cover_lines = [
        f"<b>Property:</b> {PROPERTY['name']}",
        f"<b>Address:</b> {PROPERTY['address']}",
        "",
        "<b>Inspection Date:</b> February 10, 2026",
        "<b>Inspector:</b> John Martinez, HI-3847, FL Licensed Inspector",
        "",
        f"<b>Client:</b> {PROPERTY['owner_entity']}",
    ]
    for line in cover_lines:
        if line == "":
            elems.append(Spacer(1, 8))
        else:
            elems.append(Paragraph(line, st["cover_detail"]))

    elems.append(Spacer(1, 0.6 * inch))

    # Bottom rule
    elems.append(rule_table)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 2: Executive Summary
# ---------------------------------------------------------------------------
def page_executive_summary(st):
    elems = []
    elems.append(Paragraph("EXECUTIVE SUMMARY", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        "<b>Overall Condition:</b> Fair-to-Good", st["body"]
    ))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        "This inspection was conducted on February 10, 2026, covering all common areas, "
        "building exteriors, roofing, and a representative sample of six (6) of the "
        "eighteen (18) residential units. The property is generally well-maintained with "
        "several items requiring attention prior to or shortly after listing.",
        st["body"],
    ))
    elems.append(Spacer(1, 10))

    elems.append(Paragraph("Major Items Requiring Attention", st["section_header"]))

    major_items = [
        "<b>1. Roof</b> &mdash; Approximately 12 years old with an estimated 5 years of "
        "remaining useful life. Granule loss observed on south-facing exposure. Budget "
        "$45,000&ndash;$55,000 for full replacement within 3&ndash;5 years.",

        "<b>2. HVAC</b> &mdash; Three units (103, 206, 303) have failing compressors and "
        "require immediate replacement. Estimated cost: $4,500 per unit ($13,500 total).",

        "<b>3. Building 2 Exterior</b> &mdash; Stucco cracking observed at window headers "
        "on east and north elevations. Currently cosmetic but should be repaired to prevent "
        "moisture intrusion. Estimated cost: $8,000.",
    ]
    for item in major_items:
        elems.append(Paragraph(item, st["bullet"]))
        elems.append(Spacer(1, 4))

    elems.append(Spacer(1, 12))

    # Summary of estimated capital needs
    elems.append(Paragraph("Capital Expenditure Overview", st["section_header"]))
    elems.append(Paragraph(
        f"Total estimated capital expenditures over the next 1&ndash;5 years: "
        f"<b>${TOTAL_CAPEX:,.0f}</b>. A detailed breakdown is provided on the final page "
        f"of this report.",
        st["body"],
    ))

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 3: Structural
# ---------------------------------------------------------------------------
def page_structural(st):
    elems = []
    elems.append(Paragraph("STRUCTURAL", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems += section("Foundation", [
        "Type: Slab on grade.",
        "No visible settlement, cracking, or structural concerns were observed at either "
        "building. The foundation appears to be performing as intended with no evidence of "
        "differential movement.",
    ], st)

    elems += section("Exterior Walls", [
        "Finish: Stucco over concrete block construction.",
        "<b>Building 1:</b> Good condition. No significant cracking, staining, or damage "
        "observed. Stucco finish is intact with no signs of moisture intrusion.",
        "<b>Building 2:</b> Hairline cracks observed at window headers on the east and "
        "north elevations. These cracks appear cosmetic in nature at this time. "
        "Recommend monitoring for progression and sealing to prevent moisture penetration. "
        "Estimated repair cost: $8,000.",
    ], st)

    elems += section("Windows and Doors", [
        "Type: Single-hung aluminum frame windows throughout both buildings.",
        "All windows inspected were functional with intact weather seals. No fogging "
        "between panes was observed, indicating seals are performing adequately.",
        "Entry doors are solid-core with deadbolt locks. All operated properly during "
        "inspection.",
    ], st)

    elems += section("Stairs and Walkways", [
        "Exterior concrete stairways and walkways are in good condition. Handrails are "
        "secure and meet current code requirements. No trip hazards were identified.",
    ], st)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 4: Roofing
# ---------------------------------------------------------------------------
def page_roofing(st):
    elems = []
    elems.append(Paragraph("ROOFING", st["page_title"]))
    elems.append(Spacer(1, 6))

    # Summary table
    roof_data = [
        [Paragraph("<b>Attribute</b>", st["table_cell_bold"]),
         Paragraph("<b>Details</b>", st["table_cell_bold"])],
        [Paragraph("Roof Type", st["table_cell"]),
         Paragraph("Architectural shingle", st["table_cell"])],
        [Paragraph("Year Installed", st["table_cell"]),
         Paragraph("2014 (approximately 12 years old)", st["table_cell"])],
        [Paragraph("Estimated Remaining Life", st["table_cell"]),
         Paragraph("5 years", st["table_cell"])],
        [Paragraph("Active Leaks", st["table_cell"]),
         Paragraph("None observed", st["table_cell"])],
        [Paragraph("Replacement Budget", st["table_cell"]),
         Paragraph("$45,000 - $55,000", st["table_cell"])],
    ]

    roof_table = Table(roof_data, colWidths=[2.2 * inch, 4.3 * inch])
    roof_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE_COLOR),
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT_GRAY),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE_COLOR),
        ("BACKGROUND", (0, 5), (-1, 5), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(roof_table)
    elems.append(Spacer(1, 14))

    elems.append(Paragraph("Observations", st["section_header"]))
    observations = [
        "No active leaks were observed during the inspection. Attic spaces inspected in "
        "both buildings showed no signs of water staining or moisture damage.",
        "Some granule loss was noted on south-facing roof sections, which is consistent "
        "with the age of the roofing material and exposure to direct sunlight. This is "
        "a normal wear pattern and does not indicate an immediate failure.",
        "Flashing around roof penetrations (vents, exhaust fans) appears intact and "
        "properly sealed.",
        "Gutters and downspouts are present and functional. Minor debris accumulation "
        "noted; recommend routine cleaning schedule.",
    ]
    for obs in observations:
        elems.append(Paragraph(f"\u2022  {obs}", st["bullet"]))
        elems.append(Spacer(1, 2))

    elems.append(Spacer(1, 10))
    elems.append(Paragraph("Recommendation", st["section_header"]))
    elems.append(Paragraph(
        "Plan for full roof replacement within 3&ndash;5 years. Budget $45,000&ndash;$55,000 "
        "for architectural shingle replacement on both buildings. Recommend obtaining "
        "competitive bids 12&ndash;18 months prior to anticipated replacement to lock in "
        "favorable pricing.",
        st["body"],
    ))

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 5: Plumbing
# ---------------------------------------------------------------------------
def page_plumbing(st):
    elems = []
    elems.append(Paragraph("PLUMBING", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems += section("Supply Lines", [
        "Material: Copper throughout both buildings.",
        "Condition: Good. No evidence of corrosion, pinhole leaks, or past repairs. "
        "Water pressure tested at representative units was within normal range "
        "(45&ndash;60 PSI).",
    ], st)

    elems += section("Drain Lines", [
        "Material: PVC (polyvinyl chloride).",
        "Condition: Good. No blockages, slow drains, or evidence of past backups were "
        "noted during inspection. Clean-outs are accessible at grade level.",
    ], st)

    elems += section("Water Heaters", [
        "Configuration: 18 individual tank-type water heaters (one per unit).",
        "Six (6) units have water heaters that are 8+ years old and approaching the end "
        "of their expected useful life. Recommend proactive replacement within 1&ndash;2 "
        "years to avoid emergency failures and potential water damage.",
        "Estimated cost: $800 per unit x 6 units = <b>$4,800</b>.",
    ], st)

    elems += section("Polybutylene Piping", [
        "<b>No polybutylene piping was found.</b> This is a positive finding, as "
        "polybutylene supply lines (common in 1980s construction) are prone to failure "
        "and are a significant insurance and liability concern.",
    ], st)

    elems += section("Additional Plumbing Notes", [
        "Hose bibs at building exteriors are functional with proper anti-siphon devices.",
        "Main shut-off valves for each building are accessible and operational.",
        "No evidence of slab leaks or unusual water usage patterns per utility records.",
    ], st)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 6: Electrical
# ---------------------------------------------------------------------------
def page_electrical(st):
    elems = []
    elems.append(Paragraph("ELECTRICAL", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems += section("Main Service", [
        "Each building is served by a 200-amp main panel, which is adequate for the "
        "number and type of units served.",
    ], st)

    elems += section("Panel Type", [
        "All panels have been updated to circuit breakers. No fuse boxes were found "
        "on the property. This is a positive finding for both safety and insurability.",
    ], st)

    elems += section("GFCI Protection", [
        "Ground Fault Circuit Interrupter (GFCI) protection is present and functional "
        "in all kitchens and bathrooms inspected. This meets current safety standards.",
    ], st)

    elems += section("Exterior Lighting", [
        "Exterior lighting is adequate for security purposes. Building-mounted fixtures "
        "illuminate walkways, stairways, and parking areas. All fixtures observed were "
        "operational at the time of inspection.",
    ], st)

    elems += section("Smoke and CO Detectors", [
        "Smoke detectors and carbon monoxide (CO) detectors are present in all inspected "
        "units. Detectors appeared to be of recent manufacture and in working condition. "
        "Recommend verifying battery replacement schedule with property management.",
    ], st)

    elems += section("Electrical Summary", [
        "The electrical systems are in good overall condition with no significant "
        "deficiencies noted. No immediate capital expenditures are anticipated for "
        "electrical components.",
    ], st)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 7: HVAC
# ---------------------------------------------------------------------------
def page_hvac(st):
    elems = []
    elems.append(Paragraph("HVAC", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems += section("System Configuration", [
        "The property has 18 individual split systems (one per unit), each consisting "
        "of an exterior condensing unit and interior air handler. This configuration "
        "allows each tenant to control their own heating and cooling independently.",
    ], st)

    elems += section("System Age", [
        "Average system age across all 18 units: approximately <b>8 years</b>.",
        "Expected useful life for split systems in this climate: 12&ndash;15 years.",
    ], st)

    elems.append(Paragraph("Units Requiring Immediate Attention", st["section_header"]))

    # HVAC issue table
    hvac_data = [
        [Paragraph("Unit", st["table_header"]),
         Paragraph("Issue", st["table_header"]),
         Paragraph("Recommendation", st["table_header"]),
         Paragraph("Est. Cost", st["table_header"])],
        [Paragraph("103", st["table_cell_center"]),
         Paragraph("Compressor failing; excessive noise and poor cooling output", st["table_cell"]),
         Paragraph("Immediate replacement", st["table_cell"]),
         Paragraph("$4,500", st["table_cell_right"])],
        [Paragraph("206", st["table_cell_center"]),
         Paragraph("Compressor failing; unit cycling on/off repeatedly", st["table_cell"]),
         Paragraph("Immediate replacement", st["table_cell"]),
         Paragraph("$4,500", st["table_cell_right"])],
        [Paragraph("303", st["table_cell_center"]),
         Paragraph("Compressor failing; refrigerant leak detected", st["table_cell"]),
         Paragraph("Immediate replacement", st["table_cell"]),
         Paragraph("$4,500", st["table_cell_right"])],
        [Paragraph("<b>Total</b>", st["table_cell_bold"]),
         Paragraph("", st["table_cell"]),
         Paragraph("", st["table_cell"]),
         Paragraph("<b>$13,500</b>", st["table_cell_bold_right"])],
    ]

    hvac_table = Table(hvac_data, colWidths=[0.7 * inch, 2.8 * inch, 1.6 * inch, 1.0 * inch])
    hvac_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE_COLOR),
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT_GRAY),
        ("BACKGROUND", (0, 4), (-1, 4), MEDIUM_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(hvac_table)
    elems.append(Spacer(1, 14))

    elems += section("Remaining Systems", [
        "The remaining 15 HVAC systems are operational and performing within acceptable "
        "parameters. Air filters were checked in all inspected units; several were due "
        "for replacement (normal maintenance item).",
        "Recommend continued annual preventive maintenance service for all 18 systems "
        "to maximize useful life and efficiency.",
    ], st)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 8: Environmental
# ---------------------------------------------------------------------------
def page_environmental(st):
    elems = []
    elems.append(Paragraph("ENVIRONMENTAL", st["page_title"]))
    elems.append(Spacer(1, 6))

    # Environmental summary table
    env_data = [
        [Paragraph("Concern", st["table_header"]),
         Paragraph("Finding", st["table_header"]),
         Paragraph("Risk Level", st["table_header"]),
         Paragraph("Action Required", st["table_header"])],
        [Paragraph("Mold", st["table_cell"]),
         Paragraph("No visible mold observed in inspected units or common areas", st["table_cell"]),
         Paragraph("Low", st["table_cell_center"]),
         Paragraph("None at this time", st["table_cell"])],
        [Paragraph("Asbestos", st["table_cell"]),
         Paragraph("Building constructed 1986 &mdash; possible asbestos in popcorn ceilings", st["table_cell"]),
         Paragraph("Moderate", st["table_cell_center"]),
         Paragraph("Recommend testing before any removal or renovation", st["table_cell"])],
        [Paragraph("Lead Paint", st["table_cell"]),
         Paragraph("Unlikely &mdash; post-1978 construction", st["table_cell"]),
         Paragraph("Low", st["table_cell_center"]),
         Paragraph("None", st["table_cell"])],
        [Paragraph("Radon", st["table_cell"]),
         Paragraph("Low risk area (Palm Bay, FL)", st["table_cell"]),
         Paragraph("Low", st["table_cell_center"]),
         Paragraph("None", st["table_cell"])],
        [Paragraph("Termites / WDO", st["table_cell"]),
         Paragraph("No visible evidence of wood-destroying organisms", st["table_cell"]),
         Paragraph("Low", st["table_cell_center"]),
         Paragraph("Recommend annual WDO inspection", st["table_cell"])],
    ]

    env_table = Table(env_data, colWidths=[1.0 * inch, 2.3 * inch, 0.9 * inch, 2.3 * inch])
    env_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE_COLOR),
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT_GRAY),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE_COLOR),
        ("BACKGROUND", (0, 5), (-1, 5), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(env_table)
    elems.append(Spacer(1, 14))

    elems.append(Paragraph("Detailed Notes", st["section_header"]))

    elems += section("Mold", [
        "A visual inspection for mold was conducted in all common areas, building "
        "exteriors, and the six (6) sampled residential units. No visible mold growth, "
        "musty odors, or signs of chronic moisture were observed. HVAC condensate "
        "drain lines appeared clear and properly routed.",
    ], st)

    elems += section("Asbestos", [
        "The property was constructed in 1986, which is within the era when asbestos-"
        "containing materials were commonly used in popcorn ceilings (acoustic texture), "
        "floor tiles, and pipe insulation. While no friable asbestos was observed, the "
        "presence of textured ceilings warrants laboratory testing before any renovation, "
        "scraping, or removal work is performed.",
        "<b>Recommendation:</b> Obtain an asbestos survey from a licensed environmental "
        "consultant before undertaking any ceiling modifications.",
    ], st)

    elems += section("Lead Paint", [
        "The property was built in 1986, after the federal ban on lead-based paint "
        "(effective 1978). The risk of lead paint is considered low. No peeling or "
        "deteriorating paint was observed during inspection.",
    ], st)

    elems += section("Termites", [
        "No visible evidence of termite activity or damage was observed at either "
        "building. However, South Florida properties are in a high-risk zone for "
        "subterranean termites. Recommend maintaining an annual Wood-Destroying "
        "Organism (WDO) inspection program.",
    ], st)

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 9: Unit Interiors
# ---------------------------------------------------------------------------
def page_unit_interiors(st):
    elems = []
    elems.append(Paragraph("UNIT INTERIORS", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        "A representative sample of six (6) units was inspected to assess interior "
        "conditions, deferred maintenance, and overall habitability. Units were selected "
        "to include a mix of unit types and floors.",
        st["body"],
    ))
    elems.append(Spacer(1, 8))

    # Unit inspection table
    unit_data = [
        [Paragraph("Unit", st["table_header"]),
         Paragraph("Type", st["table_header"]),
         Paragraph("Condition", st["table_header"]),
         Paragraph("Notes", st["table_header"]),
         Paragraph("Est. Cost", st["table_header"])],
        [Paragraph("101", st["table_cell_center"]),
         Paragraph("1BR/1BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
        [Paragraph("103", st["table_cell_center"]),
         Paragraph("1BR/1BA", st["table_cell_center"]),
         Paragraph("Fair", st["table_cell_center"]),
         Paragraph("Deferred maintenance: damaged vinyl flooring in kitchen, stained carpet in bedroom", st["table_cell"]),
         Paragraph("$2,500", st["table_cell_right"])],
        [Paragraph("201", st["table_cell_center"]),
         Paragraph("2BR/1BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
        [Paragraph("202", st["table_cell_center"]),
         Paragraph("2BR/1BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
        [Paragraph("208", st["table_cell_center"]),
         Paragraph("2BR/1BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
        [Paragraph("301", st["table_cell_center"]),
         Paragraph("3BR/2BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
        [Paragraph("302", st["table_cell_center"]),
         Paragraph("3BR/2BA", st["table_cell_center"]),
         Paragraph("Good", st["table_cell_center"]),
         Paragraph("Normal wear; no significant issues", st["table_cell"]),
         Paragraph("$0", st["table_cell_right"])],
    ]

    unit_table = Table(unit_data, colWidths=[0.6 * inch, 0.8 * inch, 0.8 * inch, 3.0 * inch, 0.9 * inch])
    unit_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
        ("BACKGROUND", (0, 2), (-1, 2), HIGH_COLOR),  # Unit 103 highlighted
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT_GRAY),
        ("BACKGROUND", (0, 4), (-1, 4), WHITE_COLOR),
        ("BACKGROUND", (0, 5), (-1, 5), LIGHT_GRAY),
        ("BACKGROUND", (0, 6), (-1, 6), WHITE_COLOR),
        ("BACKGROUND", (0, 7), (-1, 7), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(unit_table)
    elems.append(Spacer(1, 14))

    elems.append(Paragraph("Units Not Inspected — Noted Conditions", st["section_header"]))
    elems.append(Paragraph(
        "<b>Unit 207</b> (not in inspection sample): Property management reports deferred "
        "maintenance including worn carpet and minor wall damage. Budget approximately "
        "<b>$2,500</b> for full unit turn.",
        st["body"],
    ))
    elems.append(Spacer(1, 10))

    elems.append(Paragraph("Common Areas", st["section_header"]))
    elems.append(Paragraph(
        "Common areas including hallways, stairwells, laundry rooms, and exterior "
        "walkways are in good condition. Interior common areas appear to have been "
        "recently painted. Flooring in common areas is clean and in acceptable condition. "
        "Laundry equipment (coin-operated) is functional.",
        st["body"],
    ))

    elems.append(PageBreak())
    return elems


# ---------------------------------------------------------------------------
# Page 10: Capital Expenditure Summary
# ---------------------------------------------------------------------------
def page_capex_summary(st):
    elems = []
    elems.append(Paragraph("CAPITAL EXPENDITURE SUMMARY", st["page_title"]))
    elems.append(Spacer(1, 6))

    elems.append(Paragraph(
        "The following table summarizes anticipated capital expenditures identified "
        "during this inspection, organized by priority level. These estimates are based "
        "on observed conditions and current market pricing for the Palm Bay, FL area.",
        st["body"],
    ))
    elems.append(Spacer(1, 10))

    # Build table from CAPEX data
    header_row = [
        Paragraph("Item", st["table_header"]),
        Paragraph("Priority", st["table_header"]),
        Paragraph("Est. Cost", st["table_header"]),
        Paragraph("Timeline", st["table_header"]),
    ]

    capex_rows = [header_row]
    for item_name, priority, cost, timeline in CAPEX:
        capex_rows.append([
            Paragraph(item_name, st["table_cell"]),
            Paragraph(priority, st["table_cell_center"]),
            Paragraph(f"${cost:,.0f}", st["table_cell_right"]),
            Paragraph(timeline, st["table_cell_center"]),
        ])

    # Total row
    capex_rows.append([
        Paragraph("<b>Total</b>", st["table_cell_bold"]),
        Paragraph("", st["table_cell"]),
        Paragraph(f"<b>${TOTAL_CAPEX:,.0f}</b>", st["table_cell_bold_right"]),
        Paragraph("", st["table_cell"]),
    ])

    capex_table = Table(capex_rows, colWidths=[2.4 * inch, 1.0 * inch, 1.2 * inch, 1.5 * inch])

    # Build style commands
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]

    # Alternating row shading for data rows
    for i in range(1, len(CAPEX) + 1):
        if i % 2 == 1:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), LIGHT_GRAY))
        else:
            style_cmds.append(("BACKGROUND", (0, i), (-1, i), WHITE_COLOR))

    # Priority-based color coding in the priority column
    for i, (_, priority, _, _) in enumerate(CAPEX, start=1):
        if priority == "High":
            style_cmds.append(("BACKGROUND", (1, i), (1, i), HIGH_COLOR))
        elif priority == "Medium":
            style_cmds.append(("BACKGROUND", (1, i), (1, i), MEDIUM_COLOR))
        elif priority == "Low":
            style_cmds.append(("BACKGROUND", (1, i), (1, i), LOW_COLOR))

    # Total row styling
    total_row_idx = len(CAPEX) + 1
    style_cmds.append(("BACKGROUND", (0, total_row_idx), (-1, total_row_idx), MEDIUM_GRAY))
    style_cmds.append(("LINEABOVE", (0, total_row_idx), (-1, total_row_idx), 1.5, NAVY_COLOR))

    capex_table.setStyle(TableStyle(style_cmds))
    elems.append(capex_table)
    elems.append(Spacer(1, 20))

    # Priority legend
    elems.append(Paragraph("Priority Definitions", st["section_header"]))
    legend_items = [
        "<b>High:</b> Immediate attention required. Address before or concurrent "
        "with listing to avoid buyer objections or safety concerns.",
        "<b>Medium:</b> Important but not urgent. Should be budgeted for within the "
        "stated timeline. May be negotiation points during sale.",
        "<b>Low:</b> Routine maintenance or cosmetic items. Can be addressed on a "
        "standard maintenance schedule.",
    ]
    for item in legend_items:
        elems.append(Paragraph(f"\u2022  {item}", st["bullet"]))
        elems.append(Spacer(1, 2))

    elems.append(Spacer(1, 20))

    # Disclaimer
    elems.append(Paragraph("Disclaimer", st["section_header"]))
    elems.append(Paragraph(
        "This inspection report reflects conditions observed on February 10, 2026. "
        "Cost estimates are approximate and based on current market conditions. Actual "
        "costs may vary. This report does not constitute a warranty or guarantee of "
        "property condition. A full home warranty or structural warranty should be "
        "considered as part of any transaction.",
        st["body"],
    ))
    elems.append(Spacer(1, 20))

    # Inspector signature block
    sig_data = [
        [Paragraph("", st["table_cell"]), Paragraph("", st["table_cell"])],
        [Paragraph("_________________________________", st["table_cell"]),
         Paragraph("_________________________________", st["table_cell"])],
        [Paragraph("John Martinez, HI-3847", st["table_cell"]),
         Paragraph("Date: February 10, 2026", st["table_cell"])],
        [Paragraph("FL Licensed Home Inspector", st["table_cell"]),
         Paragraph("", st["table_cell"])],
    ]
    sig_table = Table(sig_data, colWidths=[3.25 * inch, 3.25 * inch])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    elems.append(sig_table)

    return elems


# ===========================================================================
# Main — Build the PDF
# ===========================================================================
def main():
    filepath = output_path("03_inspection_report.pdf")

    doc = SimpleDocTemplate(
        filepath,
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Pre-Listing Property Inspection Report",
        author="John Martinez, HI-3847",
    )

    st = build_styles()

    # Assemble all pages
    story = []
    story += page_cover(st)
    story += page_executive_summary(st)
    story += page_structural(st)
    story += page_roofing(st)
    story += page_plumbing(st)
    story += page_electrical(st)
    story += page_hvac(st)
    story += page_environmental(st)
    story += page_unit_interiors(st)
    story += page_capex_summary(st)

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)

    # Verify
    size = os.path.getsize(filepath)
    print(f"Created 03_inspection_report.pdf at {filepath}")
    print(f"File size: {size:,} bytes")


if __name__ == "__main__":
    main()
