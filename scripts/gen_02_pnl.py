"""
Generate 02_profit_loss_T12.pdf for Palm Bay Palms Apartments case study.
Trailing 12-Month Profit & Loss statement in landscape PDF with monthly breakdown.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import *

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable,
)


# ---------------------------------------------------------------------------
# Color palette
# ---------------------------------------------------------------------------
NAVY_COLOR = colors.HexColor("#1E3A5F")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
WHITE_COLOR = colors.white
RED_COLOR = colors.HexColor("#C62828")
BLACK_COLOR = colors.black
BORDER_GRAY = colors.HexColor("#CCCCCC")
SUBTLE_GRAY = colors.HexColor("#E8E8E8")

# ---------------------------------------------------------------------------
# Paragraph styles
# ---------------------------------------------------------------------------
styles = getSampleStyleSheet()

STYLE_TITLE = ParagraphStyle(
    "PNLTitle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=16,
    textColor=WHITE_COLOR,
    alignment=TA_LEFT,
    spaceAfter=0,
    spaceBefore=0,
    leading=20,
)

STYLE_SUBTITLE = ParagraphStyle(
    "PNLSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=10,
    textColor=colors.HexColor("#B0BEC5"),
    alignment=TA_LEFT,
    spaceAfter=0,
    spaceBefore=2,
    leading=14,
)

STYLE_FOOTER = ParagraphStyle(
    "PNLFooter",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=8,
    textColor=colors.HexColor("#888888"),
    alignment=TA_CENTER,
    spaceBefore=6,
)

STYLE_SECTION = ParagraphStyle(
    "PNLSection",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=9,
    textColor=WHITE_COLOR,
    alignment=TA_LEFT,
)

# Cell text styles
STYLE_LABEL = ParagraphStyle(
    "CellLabel", fontName="Helvetica", fontSize=7.5, leading=9,
    textColor=BLACK_COLOR, alignment=TA_LEFT,
)
STYLE_LABEL_BOLD = ParagraphStyle(
    "CellLabelBold", fontName="Helvetica-Bold", fontSize=7.5, leading=9,
    textColor=BLACK_COLOR, alignment=TA_LEFT,
)
STYLE_LABEL_INDENT = ParagraphStyle(
    "CellLabelIndent", fontName="Helvetica", fontSize=7.5, leading=9,
    textColor=BLACK_COLOR, alignment=TA_LEFT, leftIndent=10,
)
STYLE_NUM = ParagraphStyle(
    "CellNum", fontName="Helvetica", fontSize=7.5, leading=9,
    textColor=BLACK_COLOR, alignment=TA_RIGHT,
)
STYLE_NUM_BOLD = ParagraphStyle(
    "CellNumBold", fontName="Helvetica-Bold", fontSize=7.5, leading=9,
    textColor=BLACK_COLOR, alignment=TA_RIGHT,
)
STYLE_NUM_RED = ParagraphStyle(
    "CellNumRed", fontName="Helvetica", fontSize=7.5, leading=9,
    textColor=RED_COLOR, alignment=TA_RIGHT,
)
STYLE_NUM_RED_BOLD = ParagraphStyle(
    "CellNumRedBold", fontName="Helvetica-Bold", fontSize=7.5, leading=9,
    textColor=RED_COLOR, alignment=TA_RIGHT,
)


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------
def fmt_currency(val, bold=False, force_red=False):
    """Format a number as currency with parentheses for negatives."""
    if val is None:
        return Paragraph("", STYLE_NUM)
    negative = val < 0
    abs_val = abs(val)
    # Format with commas
    if abs_val == int(abs_val):
        formatted = f"${abs_val:,.0f}"
    else:
        formatted = f"${abs_val:,.2f}"
    if negative:
        formatted = f"({formatted})"
    # Pick style
    if negative or force_red:
        style = STYLE_NUM_RED_BOLD if bold else STYLE_NUM_RED
    else:
        style = STYLE_NUM_BOLD if bold else STYLE_NUM
    return Paragraph(formatted, style)


def label_cell(text, bold=False, indent=False):
    """Create a label Paragraph."""
    if bold:
        return Paragraph(text, STYLE_LABEL_BOLD)
    if indent:
        return Paragraph(text, STYLE_LABEL_INDENT)
    return Paragraph(text, STYLE_LABEL)


def section_header_cell(text):
    """White text for section header rows."""
    return Paragraph(text, STYLE_SECTION)


def blank_row(ncols):
    """An empty row for spacing."""
    return [""] * ncols


# ---------------------------------------------------------------------------
# Monthly P&L data construction
# ---------------------------------------------------------------------------
MONTH_LABELS = [
    "Mar 25", "Apr 25", "May 25", "Jun 25", "Jul 25", "Aug 25",
    "Sep 25", "Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26",
]

# Annual totals from PRD
GPR_ANNUAL = 282000
VACANCY_ANNUAL = -31200
EGI_ANNUAL_VAL = 250800
LAUNDRY_ANNUAL = 4800
LATE_FEES_ANNUAL = 2400
TOTAL_REVENUE_ANNUAL_VAL = 258000

# Expenses annual
PROP_TAX_ANNUAL = 18750
INSURANCE_ANNUAL = 32400
REPAIRS_ANNUAL = 28500
MGMT_ANNUAL = 20640
UTILITIES_ANNUAL = 8400
LANDSCAPE_ANNUAL = 4800
PEST_ANNUAL = 2160
LEGAL_ANNUAL = 3600
RESERVES_ANNUAL = 4500
TOTAL_EXP_ANNUAL = 123750

NOI_ANNUAL_VAL = 134250
DEBT_SERVICE_ANNUAL = -73800
CASH_FLOW_ANNUAL = 60450


def distribute_even(annual, n=12):
    """Distribute annual amount evenly across n months, rounding to cents."""
    monthly = round(annual / n, 2)
    result = [monthly] * n
    # Adjust last month to absorb rounding error
    result[-1] = round(annual - sum(result[:-1]), 2)
    return result


def build_monthly_gpr():
    """GPR: $23,500/mo even distribution."""
    return distribute_even(GPR_ANNUAL)


def build_monthly_vacancy():
    """Vacancy loss: heavier in later months (units went vacant Dec 2025 and Jan 2026).
    Unit 206 vacant from Dec 2025 (index 9): market $1,450/mo
    Unit 105 vacant from Jan 2026 (index 10): market $1,200/mo
    Also account for delinquency-related effective vacancy.
    Distribute so annual sums to -31,200."""
    # Base: mild vacancy across all months, heavier in Dec-Feb
    # Months 0-8 (Mar-Nov): about $1,500/mo baseline vacancy (partial occupancy issues)
    # Month 9 (Dec): unit 206 goes vacant = jump
    # Month 10-11 (Jan-Feb): both units vacant = largest
    base_monthly = [1800] * 9 + [3200, 4800, 4800]
    # Scale to match annual total
    raw_total = sum(base_monthly)
    target = 31200
    scaled = [round(v * target / raw_total, 2) for v in base_monthly]
    # Fix rounding
    diff = round(target - sum(scaled), 2)
    scaled[-1] = round(scaled[-1] + diff, 2)
    return [-v for v in scaled]  # negative values


def build_monthly_laundry():
    """Laundry: $400/mo."""
    return distribute_even(LAUNDRY_ANNUAL)


def build_monthly_late_fees():
    """Late fees: $200/mo."""
    return distribute_even(LATE_FEES_ANNUAL)


def build_monthly_repairs():
    """Repairs vary: higher in summer (Jun-Aug), lower in winter."""
    weights = [1.0, 1.0, 1.0, 1.5, 1.8, 1.8, 1.2, 1.0, 0.8, 0.7, 0.6, 0.6]
    total_weight = sum(weights)
    raw = [round(w * REPAIRS_ANNUAL / total_weight, 2) for w in weights]
    diff = round(REPAIRS_ANNUAL - sum(raw), 2)
    raw[-1] = round(raw[-1] + diff, 2)
    return raw


# Build all monthly arrays
monthly_gpr = build_monthly_gpr()
monthly_vacancy = build_monthly_vacancy()
monthly_egi = [round(g + v, 2) for g, v in zip(monthly_gpr, monthly_vacancy)]
monthly_laundry = build_monthly_laundry()
monthly_late_fees = build_monthly_late_fees()
monthly_total_revenue = [
    round(e + l + f, 2)
    for e, l, f in zip(monthly_egi, monthly_laundry, monthly_late_fees)
]

monthly_prop_tax = distribute_even(PROP_TAX_ANNUAL)
monthly_insurance = distribute_even(INSURANCE_ANNUAL)
monthly_repairs = build_monthly_repairs()
monthly_mgmt = distribute_even(MGMT_ANNUAL)
monthly_utilities = distribute_even(UTILITIES_ANNUAL)
monthly_landscape = distribute_even(LANDSCAPE_ANNUAL)
monthly_pest = distribute_even(PEST_ANNUAL)
monthly_legal = distribute_even(LEGAL_ANNUAL)
monthly_reserves = distribute_even(RESERVES_ANNUAL)

monthly_total_expenses = [
    round(sum(vals), 2)
    for vals in zip(
        monthly_prop_tax, monthly_insurance, monthly_repairs, monthly_mgmt,
        monthly_utilities, monthly_landscape, monthly_pest, monthly_legal,
        monthly_reserves,
    )
]

monthly_noi = [
    round(r - e, 2)
    for r, e in zip(monthly_total_revenue, monthly_total_expenses)
]

monthly_debt = distribute_even(abs(DEBT_SERVICE_ANNUAL))

monthly_cash_flow = [
    round(n - d, 2)
    for n, d in zip(monthly_noi, monthly_debt)
]


# ---------------------------------------------------------------------------
# Table row builders
# ---------------------------------------------------------------------------
NCOLS = 14  # label + 12 months + annual total


def data_row(label_text, monthly_vals, annual_val,
             bold=False, indent=False, negative=False, force_red=False):
    """Build a single data row: label, 12 monthly values, annual total."""
    row = [label_cell(label_text, bold=bold, indent=indent)]
    for v in monthly_vals:
        row.append(fmt_currency(v, bold=bold, force_red=force_red))
    row.append(fmt_currency(annual_val, bold=bold, force_red=force_red))
    return row


def section_header_row(text, ncols=NCOLS):
    """A full-width section header row (navy background)."""
    row = [section_header_cell(text)] + [""] * (ncols - 1)
    return row


def separator_row(ncols=NCOLS):
    """A thin blank row for visual spacing."""
    return [""] * ncols


# ---------------------------------------------------------------------------
# Build the full table data
# ---------------------------------------------------------------------------
def build_table_data():
    """Return (table_data, section_header_rows, subtotal_rows, negative_rows)."""
    rows = []
    section_rows = []      # indices of navy-background section headers
    subtotal_rows = []     # indices of bold subtotal/total rows
    negative_rows = []     # indices with negative values
    bottom_line_rows = []  # NOI, debt service, cash flow

    # -- Column headers --
    header = [label_cell("", bold=True)]
    for m in MONTH_LABELS:
        header.append(Paragraph(m, STYLE_NUM_BOLD))
    header.append(Paragraph("Annual Total", STYLE_NUM_BOLD))
    rows.append(header)

    # -- INCOME SECTION HEADER --
    rows.append(section_header_row("INCOME"))
    section_rows.append(len(rows) - 1)

    # Gross Potential Rent
    rows.append(data_row(
        "Gross Potential Rent", monthly_gpr, GPR_ANNUAL, indent=True))

    # Less: Vacancy Loss (negative)
    rows.append(data_row(
        "Less: Vacancy Loss", monthly_vacancy, VACANCY_ANNUAL,
        indent=True, negative=True, force_red=True))
    negative_rows.append(len(rows) - 1)

    # Effective Gross Income (subtotal)
    rows.append(data_row(
        "Effective Gross Income", monthly_egi, EGI_ANNUAL_VAL, bold=True))
    subtotal_rows.append(len(rows) - 1)

    # Other income
    rows.append(data_row(
        "Laundry Income", monthly_laundry, LAUNDRY_ANNUAL, indent=True))
    rows.append(data_row(
        "Late Fees / Other", monthly_late_fees, LATE_FEES_ANNUAL, indent=True))

    # Total Revenue
    rows.append(data_row(
        "TOTAL REVENUE", monthly_total_revenue, TOTAL_REVENUE_ANNUAL_VAL,
        bold=True))
    subtotal_rows.append(len(rows) - 1)

    # Spacer
    rows.append(separator_row())

    # -- EXPENSES SECTION HEADER --
    rows.append(section_header_row("OPERATING EXPENSES"))
    section_rows.append(len(rows) - 1)

    # Individual expense lines
    rows.append(data_row(
        "Property Taxes", monthly_prop_tax, PROP_TAX_ANNUAL, indent=True))
    rows.append(data_row(
        "Insurance", monthly_insurance, INSURANCE_ANNUAL, indent=True))
    rows.append(data_row(
        "Repairs & Maintenance", monthly_repairs, REPAIRS_ANNUAL, indent=True))
    rows.append(data_row(
        "Property Management (8%)", monthly_mgmt, MGMT_ANNUAL, indent=True))
    rows.append(data_row(
        "Utilities (common)", monthly_utilities, UTILITIES_ANNUAL, indent=True))
    rows.append(data_row(
        "Landscaping", monthly_landscape, LANDSCAPE_ANNUAL, indent=True))
    rows.append(data_row(
        "Pest Control", monthly_pest, PEST_ANNUAL, indent=True))
    rows.append(data_row(
        "Legal / Admin", monthly_legal, LEGAL_ANNUAL, indent=True))
    rows.append(data_row(
        "Reserves ($250/unit/yr)", monthly_reserves, RESERVES_ANNUAL,
        indent=True))

    # Total Expenses
    rows.append(data_row(
        "TOTAL EXPENSES", monthly_total_expenses, TOTAL_EXP_ANNUAL, bold=True))
    subtotal_rows.append(len(rows) - 1)

    # Spacer
    rows.append(separator_row())

    # -- BOTTOM LINE SECTION --
    rows.append(section_header_row("NET OPERATING INCOME"))
    section_rows.append(len(rows) - 1)

    # NOI
    rows.append(data_row(
        "Net Operating Income (NOI)", monthly_noi, NOI_ANNUAL_VAL, bold=True))
    subtotal_rows.append(len(rows) - 1)
    bottom_line_rows.append(len(rows) - 1)

    # Debt Service (negative)
    neg_monthly_debt = [-d for d in monthly_debt]
    rows.append(data_row(
        "Less: Debt Service", neg_monthly_debt, DEBT_SERVICE_ANNUAL,
        indent=True, negative=True, force_red=True))
    negative_rows.append(len(rows) - 1)

    # Cash Flow After Debt Service
    rows.append(data_row(
        "CASH FLOW AFTER DEBT SERVICE", monthly_cash_flow, CASH_FLOW_ANNUAL,
        bold=True))
    subtotal_rows.append(len(rows) - 1)
    bottom_line_rows.append(len(rows) - 1)

    return rows, section_rows, subtotal_rows, negative_rows, bottom_line_rows


# ---------------------------------------------------------------------------
# Build document
# ---------------------------------------------------------------------------
def build_pdf():
    filepath = output_path("02_profit_loss_T12.pdf")

    page_w, page_h = landscape(LETTER)
    doc = SimpleDocTemplate(
        filepath,
        pagesize=landscape(LETTER),
        leftMargin=0.4 * inch,
        rightMargin=0.4 * inch,
        topMargin=0.4 * inch,
        bottomMargin=0.5 * inch,
    )

    elements = []

    # -- HEADER BAR (as a table) --
    header_data = [[
        Paragraph(
            "Palm Bay Palms Apartments &mdash; Trailing 12-Month P&amp;L",
            STYLE_TITLE,
        ),
        Paragraph("Property360", ParagraphStyle(
            "LogoText", fontName="Helvetica-Bold", fontSize=11,
            textColor=WHITE_COLOR, alignment=TA_RIGHT,
        )),
    ]]
    header_table = Table(header_data, colWidths=[7.5 * inch, 2.7 * inch])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_COLOR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (-1, -1), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    elements.append(header_table)

    # Subtitle bar
    subtitle_data = [[
        Paragraph("Period: March 2025 &mdash; February 2026", STYLE_SUBTITLE),
        Paragraph(
            f"{PROPERTY['address']}",
            ParagraphStyle(
                "AddrText", fontName="Helvetica", fontSize=8,
                textColor=colors.HexColor("#B0BEC5"), alignment=TA_RIGHT,
            ),
        ),
    ]]
    subtitle_table = Table(subtitle_data, colWidths=[7.5 * inch, 2.7 * inch])
    subtitle_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#263850")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 12),
        ("RIGHTPADDING", (-1, -1), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(subtitle_table)

    elements.append(Spacer(1, 8))

    # -- MAIN P&L TABLE --
    table_data, section_rows, subtotal_rows, negative_rows, bottom_line_rows = (
        build_table_data()
    )

    # Column widths: label ~1.6", months ~0.62" each, annual total ~0.78"
    # Total available width for landscape letter with 0.4" margins each side:
    # 11" - 0.8" = 10.2"
    label_w = 1.62 * inch
    month_w = 0.60 * inch
    annual_w = 0.78 * inch
    col_widths = [label_w] + [month_w] * 12 + [annual_w]

    main_table = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Build table style commands
    style_cmds = [
        # Global defaults
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),

        # Column header row (row 0) styling
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#37474F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE_COLOR),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("LINEBELOW", (0, 0), (-1, 0), 1, NAVY_COLOR),

        # Grid lines
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, BORDER_GRAY),

        # Right border on label column
        ("LINEAFTER", (0, 0), (0, -1), 0.5, BORDER_GRAY),

        # Right border before annual total
        ("LINEAFTER", (12, 0), (12, -1), 0.5, BORDER_GRAY),
    ]

    # Section header rows: navy background, span all columns
    for r in section_rows:
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), NAVY_COLOR))
        style_cmds.append(("TEXTCOLOR", (0, r), (-1, r), WHITE_COLOR))
        style_cmds.append(("SPAN", (0, r), (-1, r)))
        style_cmds.append(("TOPPADDING", (0, r), (-1, r), 5))
        style_cmds.append(("BOTTOMPADDING", (0, r), (-1, r), 5))

    # Subtotal / total rows: light background, top border
    for r in subtotal_rows:
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#E3F2FD")))
        style_cmds.append(("LINEABOVE", (0, r), (-1, r), 0.75, NAVY_COLOR))
        style_cmds.append(("LINEBELOW", (0, r), (-1, r), 0.75, NAVY_COLOR))

    # Bottom line rows (NOI, Cash Flow): stronger emphasis
    for r in bottom_line_rows:
        style_cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#C8E6C9")))
        style_cmds.append(("LINEABOVE", (0, r), (-1, r), 1.0, NAVY_COLOR))
        style_cmds.append(("LINEBELOW", (0, r), (-1, r), 1.0, NAVY_COLOR))

    # Alternating row shading for data rows (skip headers, sections, subtotals)
    special = set(section_rows) | set(subtotal_rows) | set(bottom_line_rows) | {0}
    for r in range(1, len(table_data)):
        if r in special:
            continue
        # Blank/separator rows
        if all(cell == "" for cell in table_data[r]):
            continue
        if r % 2 == 0:
            style_cmds.append(
                ("BACKGROUND", (0, r), (-1, r), LIGHT_GRAY)
            )

    main_table.setStyle(TableStyle(style_cmds))
    elements.append(main_table)

    elements.append(Spacer(1, 10))

    # -- FOOTER --
    footer_line = HRFlowable(
        width="100%", thickness=0.5, color=BORDER_GRAY, spaceAfter=4,
    )
    elements.append(footer_line)
    elements.append(Paragraph(
        "Prepared by Property360 Real Estate | Mariam Shapira",
        STYLE_FOOTER,
    ))
    elements.append(Paragraph(
        "Confidential &mdash; For Authorized Use Only",
        ParagraphStyle(
            "ConfFooter", fontName="Helvetica-Oblique", fontSize=7,
            textColor=colors.HexColor("#AAAAAA"), alignment=TA_CENTER,
            spaceBefore=2,
        ),
    ))

    # Build
    doc.build(elements)
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    filepath = build_pdf()
    size_kb = os.path.getsize(filepath) / 1024
    print(f"Created 02_profit_loss_T12.pdf at {filepath}")
    print(f"File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()
