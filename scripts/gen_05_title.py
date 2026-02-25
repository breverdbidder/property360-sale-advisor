"""
Generate 05_title_search.pdf — Title Search Summary Report
for Palm Bay Palms Apartments case study.

Professional title company document with chain of title, liens,
encumbrances, easements, tax status, and title examiner certification.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
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
RED_HIGHLIGHT = HexColor("#FFEBEE")
RED_TEXT = HexColor("#C62828")
RED_BORDER = HexColor("#E53935")


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def build_styles():
    """Return a dictionary of ParagraphStyles for the report."""
    styles = getSampleStyleSheet()
    custom = {}

    custom["report_title"] = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=24,
        textColor=WHITE_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0,
        spaceBefore=0,
    )
    custom["company_name"] = ParagraphStyle(
        "CompanyName",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=11,
        leading=14,
        textColor=WHITE_COLOR,
        alignment=TA_CENTER,
        spaceAfter=0,
    )
    custom["section_header"] = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=NAVY_COLOR,
        spaceAfter=8,
        spaceBefore=14,
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
    custom["body_indent"] = ParagraphStyle(
        "BodyIndent",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=DARK_GRAY,
        leftIndent=20,
        spaceAfter=4,
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
    custom["red_body"] = ParagraphStyle(
        "RedBody",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=RED_TEXT,
        leftIndent=20,
        spaceAfter=4,
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
    custom["table_cell_bold"] = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        leading=12,
        textColor=DARK_GRAY,
    )
    custom["label"] = ParagraphStyle(
        "Label",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=14,
        textColor=NAVY_COLOR,
        spaceAfter=2,
    )
    custom["certification"] = ParagraphStyle(
        "Certification",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=9,
        leading=13,
        textColor=DARK_GRAY,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=6,
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
# Footer callback
# ---------------------------------------------------------------------------
def _footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(HexColor("#888888"))
    page_num = canvas.getPageNumber()
    text = f"Title Search Summary Report  |  Brevard Title & Abstract Co.  |  Page {page_num}"
    canvas.drawCentredString(LETTER[0] / 2.0, 0.5 * inch, text)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Header bar helper
# ---------------------------------------------------------------------------
def header_bar(st):
    """Return flowables for the navy header bar with title and company name."""
    elems = []

    # Build a table that acts as a colored header bar
    header_data = [
        [Paragraph("TITLE SEARCH SUMMARY REPORT", st["report_title"])],
        [Paragraph("Brevard Title & Abstract Co.", st["company_name"])],
    ]
    header_table = Table(header_data, colWidths=[6.5 * inch])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_COLOR),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (0, 0), 16),
        ("BOTTOMPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 1), (0, 1), 2),
        ("BOTTOMPADDING", (0, 1), (0, 1), 14),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
    ]))
    elems.append(header_table)
    elems.append(Spacer(1, 20))

    return elems


# ---------------------------------------------------------------------------
# Property info block
# ---------------------------------------------------------------------------
def property_info_section(st):
    """Return flowables for the property info and preparation details."""
    elems = []

    # Info table for prepared by, date, property
    info_data = [
        [Paragraph("<b>Prepared by:</b>", st["body"]),
         Paragraph("Brevard Title & Abstract Co.", st["body"])],
        [Paragraph("<b>Date:</b>", st["body"]),
         Paragraph("February 15, 2026", st["body"])],
        [Paragraph("<b>Property:</b>", st["body"]),
         Paragraph(PROPERTY["address"], st["body"])],
    ]
    info_table = Table(info_data, colWidths=[1.5 * inch, 5.0 * inch])
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    elems.append(info_table)
    elems.append(Spacer(1, 10))

    return elems


# ---------------------------------------------------------------------------
# Legal Description section
# ---------------------------------------------------------------------------
def legal_description_section(st):
    """Return flowables for the legal description."""
    elems = []
    elems.append(Paragraph("Legal Description", st["section_header"]))
    elems.append(Paragraph(
        "Lot 142, Block 5, Palm Bay Unit 37, as recorded in Plat Book 29, Page 37, "
        "of the Public Records of Brevard County, Florida.",
        st["body_indent"],
    ))
    return elems


# ---------------------------------------------------------------------------
# Current Owner section
# ---------------------------------------------------------------------------
def current_owner_section(st):
    """Return flowables for the current owner."""
    elems = []
    elems.append(Paragraph("Current Owner", st["section_header"]))
    elems.append(Paragraph(PROPERTY["owner_entity"], st["body_indent"]))
    return elems


# ---------------------------------------------------------------------------
# Chain of Title section
# ---------------------------------------------------------------------------
def chain_of_title_section(st):
    """Return flowables for the chain of title table."""
    elems = []
    elems.append(Paragraph("Chain of Title (Last 3 Transfers)", st["section_header"]))

    chain_data = [
        [Paragraph("#", st["table_header"]),
         Paragraph("Date", st["table_header"]),
         Paragraph("Grantee", st["table_header"]),
         Paragraph("Instrument", st["table_header"]),
         Paragraph("Recording", st["table_header"])],
        [Paragraph("1", st["table_cell_center"]),
         Paragraph("2018-03-15", st["table_cell_center"]),
         Paragraph("Sunshine Palms Holdings LLC", st["table_cell"]),
         Paragraph("Warranty Deed", st["table_cell_center"]),
         Paragraph("OR Book 8234, Page 1567", st["table_cell"])],
        [Paragraph("2", st["table_cell_center"]),
         Paragraph("2012-06-20", st["table_cell_center"]),
         Paragraph("Brevard Multifamily Partners LLC", st["table_cell"]),
         Paragraph("Warranty Deed", st["table_cell_center"]),
         Paragraph("OR Book 7122, Page 893", st["table_cell"])],
        [Paragraph("3", st["table_cell_center"]),
         Paragraph("2003-09-10", st["table_cell_center"]),
         Paragraph("First Florida Development Corp", st["table_cell"]),
         Paragraph("Warranty Deed", st["table_cell_center"]),
         Paragraph("OR Book 5890, Page 2104", st["table_cell"])],
    ]

    chain_table = Table(chain_data, colWidths=[0.4 * inch, 1.0 * inch, 2.0 * inch, 1.1 * inch, 2.0 * inch])
    chain_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_COLOR),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("BACKGROUND", (0, 1), (-1, 1), LIGHT_GRAY),
        ("BACKGROUND", (0, 2), (-1, 2), WHITE_COLOR),
        ("BACKGROUND", (0, 3), (-1, 3), LIGHT_GRAY),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    elems.append(chain_table)

    return elems


# ---------------------------------------------------------------------------
# Liens and Encumbrances section
# ---------------------------------------------------------------------------
def liens_section(st):
    """Return flowables for liens and encumbrances."""
    elems = []
    elems.append(Paragraph("Liens and Encumbrances", st["section_header"]))

    # Lien 1: Mortgage
    elems.append(Paragraph(
        "<b>1. Mortgage Lien</b>",
        st["body_bold"],
    ))
    mortgage_data = [
        [Paragraph("<b>Lender</b>", st["table_cell_bold"]),
         Paragraph("First Southern Bank", st["table_cell"])],
        [Paragraph("<b>Original Amount</b>", st["table_cell_bold"]),
         Paragraph("$1,200,000", st["table_cell"])],
        [Paragraph("<b>Originated</b>", st["table_cell_bold"]),
         Paragraph("March 15, 2018", st["table_cell"])],
        [Paragraph("<b>Recorded</b>", st["table_cell_bold"]),
         Paragraph("OR Book 8234, Page 1590", st["table_cell"])],
        [Paragraph("<b>Current Est. Payoff</b>", st["table_cell_bold"]),
         Paragraph(f"${PROPERTY['current_mortgage']:,}", st["table_cell"])],
        [Paragraph("<b>Status</b>", st["table_cell_bold"]),
         Paragraph("Active", st["table_cell"])],
    ]
    mortgage_table = Table(mortgage_data, colWidths=[1.8 * inch, 4.7 * inch])
    mortgage_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), LIGHT_GRAY),
        ("BACKGROUND", (0, 1), (-1, 1), WHITE_COLOR),
        ("BACKGROUND", (0, 2), (-1, 2), LIGHT_GRAY),
        ("BACKGROUND", (0, 3), (-1, 3), WHITE_COLOR),
        ("BACKGROUND", (0, 4), (-1, 4), LIGHT_GRAY),
        ("BACKGROUND", (0, 5), (-1, 5), WHITE_COLOR),
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
    ]))
    elems.append(mortgage_table)
    elems.append(Spacer(1, 10))

    # Lien 2: Municipal Lien — highlighted in red
    elems.append(Paragraph(
        "<b>2. Municipal Lien</b>",
        st["body_bold"],
    ))
    muni_data = [
        [Paragraph("<b>Authority</b>", st["table_cell_bold"]),
         Paragraph("City of Palm Bay", st["table_cell"])],
        [Paragraph("<b>Description</b>", st["table_cell_bold"]),
         Paragraph("Code enforcement lien for landscape violation", st["table_cell"])],
        [Paragraph("<b>Amount</b>", st["table_cell_bold"]),
         Paragraph("$1,850", st["table_cell"])],
        [Paragraph("<b>Recorded</b>", st["table_cell_bold"]),
         Paragraph("2024, OR Book 9456, Page 334", st["table_cell"])],
        [Paragraph("<b>Status</b>", st["table_cell_bold"]),
         Paragraph("<b>MUST BE RESOLVED PRIOR TO CLOSING</b>", ParagraphStyle(
             "RedCell",
             fontName="Helvetica-Bold",
             fontSize=9,
             leading=12,
             textColor=RED_TEXT,
         ))],
    ]
    muni_table = Table(muni_data, colWidths=[1.8 * inch, 4.7 * inch])
    muni_style_cmds = [
        ("GRID", (0, 0), (-1, -1), 0.5, MEDIUM_GRAY),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        # Red highlight background for the entire table
        ("BACKGROUND", (0, 0), (-1, -1), RED_HIGHLIGHT),
        # Red border around entire table
        ("BOX", (0, 0), (-1, -1), 1.5, RED_BORDER),
        # Bold red background on status row
        ("BACKGROUND", (0, 4), (-1, 4), HexColor("#FFCDD2")),
    ]
    muni_table.setStyle(TableStyle(muni_style_cmds))
    elems.append(muni_table)
    elems.append(Spacer(1, 10))

    # Lien 3: HOA
    elems.append(Paragraph(
        "<b>3. HOA:</b> None \u2014 property is not within an HOA community.",
        st["body"],
    ))

    return elems


# ---------------------------------------------------------------------------
# Easements section
# ---------------------------------------------------------------------------
def easements_section(st):
    """Return flowables for the easements section."""
    elems = []
    elems.append(Paragraph("Easements", st["section_header"]))
    elems.append(Paragraph(
        "\u2022  FPL utility easement along the east boundary of the property "
        "(standard utility easement, does not affect use or development of property).",
        st["bullet"],
    ))
    return elems


# ---------------------------------------------------------------------------
# Tax Status section
# ---------------------------------------------------------------------------
def tax_status_section(st):
    """Return flowables for the tax status section."""
    elems = []
    elems.append(Paragraph("Tax Status", st["section_header"]))
    items = [
        "2025 taxes: <b>PAID IN FULL</b>",
        "No outstanding tax certificates",
        "No delinquent taxes",
    ]
    for item in items:
        elems.append(Paragraph(f"\u2022  {item}", st["bullet"]))
    return elems


# ---------------------------------------------------------------------------
# Judgments and Liens Search section
# ---------------------------------------------------------------------------
def judgments_section(st):
    """Return flowables for the judgments and liens search section."""
    elems = []
    elems.append(Paragraph("Judgments and Liens Search", st["section_header"]))
    items = [
        f"No judgments found against {PROPERTY['owner_entity']}",
        "No federal tax liens",
        "No state tax liens",
    ]
    for item in items:
        elems.append(Paragraph(f"\u2022  {item}", st["bullet"]))
    return elems


# ---------------------------------------------------------------------------
# Recommendation section
# ---------------------------------------------------------------------------
def recommendation_section(st):
    """Return flowables for the recommendation section."""
    elems = []
    elems.append(Paragraph("Recommendation", st["section_header"]))
    elems.append(Paragraph(
        "Title is insurable upon resolution of the City of Palm Bay code enforcement "
        "lien ($1,850). All other encumbrances are standard and do not impede transfer.",
        st["body"],
    ))
    return elems


# ---------------------------------------------------------------------------
# Certification section
# ---------------------------------------------------------------------------
def certification_section(st):
    """Return flowables for the certification and signature."""
    elems = []
    elems.append(Paragraph("Certification", st["section_header"]))

    # Certification text in italics with indent
    elems.append(Paragraph(
        '"This title search is based on an examination of the public records of '
        "Brevard County, Florida, and is intended for informational purposes. This "
        "report does not constitute title insurance. A full title commitment will be "
        'issued upon request."',
        st["certification"],
    ))
    elems.append(Spacer(1, 20))

    # Signature block
    sig_data = [
        [Paragraph("", st["table_cell"]), Paragraph("", st["table_cell"])],
        [Paragraph("_________________________________", st["table_cell"]),
         Paragraph("_________________________________", st["table_cell"])],
        [Paragraph("Sarah Mitchell", st["table_cell_bold"]),
         Paragraph("Date: February 15, 2026", st["table_cell"])],
        [Paragraph("Title Examiner", st["table_cell"]),
         Paragraph("", st["table_cell"])],
        [Paragraph("Brevard Title & Abstract Co.", st["table_cell"]),
         Paragraph("", st["table_cell"])],
    ]
    sig_table = Table(sig_data, colWidths=[3.25 * inch, 3.25 * inch])
    sig_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ]))
    elems.append(sig_table)

    return elems


# ===========================================================================
# Main — Build the PDF
# ===========================================================================
def main():
    filepath = output_path("05_title_search.pdf")

    doc = SimpleDocTemplate(
        filepath,
        pagesize=LETTER,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Title Search Summary Report",
        author="Brevard Title & Abstract Co.",
    )

    st = build_styles()

    # Assemble all sections
    story = []
    story += header_bar(st)
    story += property_info_section(st)
    story += legal_description_section(st)
    story += current_owner_section(st)
    story += chain_of_title_section(st)
    story += liens_section(st)
    story += easements_section(st)
    story += tax_status_section(st)
    story += judgments_section(st)
    story += recommendation_section(st)
    story += certification_section(st)

    doc.build(story, onFirstPage=_footer, onLaterPages=_footer)

    # Verify
    size = os.path.getsize(filepath)
    print(f"Created 05_title_search.pdf at {filepath}")
    print(f"File size: {size:,} bytes")


if __name__ == "__main__":
    main()
