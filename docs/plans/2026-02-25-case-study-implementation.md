# PRD-P360-002: Case Study Document Generation — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Generate 12 professional document files (XLSX, PDF, DOCX, PPTX) for an 18-unit multifamily case study, push to GitHub, and create a GitHub Action to seed Supabase.

**Architecture:** A shared Python data module defines all property/unit/financial constants. Individual generator scripts produce each document using openpyxl (XLSX), reportlab (PDF), python-docx (DOCX), and python-pptx (PPTX). All files output to `case-study/palm-bay-18-unit/` in the repo.

**Tech Stack:** Python 3.13, openpyxl, reportlab, python-docx, python-pptx, Git, GitHub Actions

**Repo root:** `C:/Users/Roselyn Sheffield/OneDrive/Documents/Ariel_Documents/Babe/Property360/property360-sale-advisor`

---

### Task 0: Environment Setup

**Step 1: Install missing Python libraries**

Run: `pip install reportlab python-pptx`
Expected: Both install successfully

**Step 2: Verify all libraries**

Run: `python -c "import openpyxl, reportlab, docx, pptx; print('ALL OK')"`
Expected: `ALL OK`

**Step 3: Pull latest from remote and create output directory**

```bash
cd "C:/Users/Roselyn Sheffield/OneDrive/Documents/Ariel_Documents/Babe/Property360/property360-sale-advisor"
git pull origin main
mkdir -p case-study/palm-bay-18-unit
mkdir -p scripts
```

**Step 4: Commit setup**

No commit needed — just environment prep.

---

### Task 1: Shared Data Module

**Files:**
- Create: `scripts/data.py`

This module is the SINGLE SOURCE OF TRUTH. Every generator imports from here.

**Step 1: Create `scripts/data.py`**

```python
"""
Property360 Case Study — Shared Data Module
All property, unit, financial, and CapEx data for Palm Bay Palms Apartments.
Every generator script imports from this module.
"""

# ── Property Info ──────────────────────────────────────────────
PROPERTY = {
    "name": "Palm Bay Palms Apartments",
    "address": "2750 Malabar Road SE, Palm Bay, FL 32907",
    "parcel_id": "29-37-05-00-00142.0-0000",
    "property_type": "Multi-family (18 units)",
    "year_built": 1986,
    "lot_acres": 1.2,
    "lot_sqft": 52272,
    "total_sqft": 14400,
    "zoning": "RM-13 (Residential Multifamily)",
    "flood_zone": "X (minimal risk)",
    "owner_entity": "Sunshine Palms Holdings LLC",
    "purchase_date": "2018-03-15",
    "purchase_price": 1450000,
    "current_mortgage": 980000,
    "mortgage_rate": 0.0475,
    "mortgage_term": 30,
    "mortgage_originated": 2018,
    "monthly_debt_service": 6150,
    "annual_taxes": 18750,
    "annual_insurance": 32400,
}

# ── Unit Mix ───────────────────────────────────────────────────
# Each unit: (unit_num, type, sf, tenant, lease_start, lease_end, rent, market_rent, deposit, status, delinquent, notes)
UNITS = [
    ("101", "1BR/1BA", 650, "Maria Santos",         "2025-09-01", "2026-08-31", 1050, 1200, 1050, "Occupied", "No", ""),
    ("102", "1BR/1BA", 650, "James Wilson",          "2025-06-01", "2026-05-31", 1100, 1200, 1100, "Occupied", "No", ""),
    ("103", "1BR/1BA", 650, "Tanya Brown",           "2024-03-01", "MTM",        950,  1200, 950,  "Occupied", "Yes - 60 days", "Delinquent — 60 days past due"),
    ("104", "1BR/1BA", 650, "Robert Chen",           "2025-12-01", "2026-11-30", 1150, 1200, 1150, "Occupied", "No", ""),
    ("105", "1BR/1BA", 650, "",                      "",           "",           0,    1200, 0,    "Vacant",   "No", "Vacant since Jan 2026"),
    ("106", "1BR/1BA", 650, "Lisa Park",             "2024-06-01", "MTM",        1000, 1200, 1000, "Occupied", "No", ""),
    ("201", "2BR/1BA", 850, "David & Ana Rodriguez", "2025-10-01", "2026-09-30", 1350, 1450, 1350, "Occupied", "No", ""),
    ("202", "2BR/1BA", 850, "Michael Turner",        "2026-02-01", "2027-01-31", 1400, 1450, 1400, "Occupied", "No", ""),
    ("203", "2BR/1BA", 850, "Sarah Johnson",         "2025-05-01", "2026-04-30", 1250, 1450, 1250, "Occupied", "No", ""),
    ("204", "2BR/1BA", 850, "Kevin Lee",             "2024-09-01", "MTM",        1300, 1450, 1300, "Occupied", "No", ""),
    ("205", "2BR/1BA", 850, "Patricia Martinez",     "2026-01-01", "2026-12-31", 1350, 1450, 1350, "Occupied", "No", ""),
    ("206", "2BR/1BA", 850, "",                      "",           "",           0,    1450, 0,    "Vacant",   "No", "Vacant since Dec 2025"),
    ("207", "2BR/1BA", 850, "Anthony Williams",      "2024-07-01", "MTM",        1200, 1450, 1200, "Occupied", "Yes - 30 days", "Delinquent — 30 days past due"),
    ("208", "2BR/1BA", 850, "Jennifer Davis",        "2025-08-01", "2026-07-31", 1400, 1450, 1400, "Occupied", "No", ""),
    ("301", "3BR/2BA", 1100, "The Nguyen Family",    "2025-11-01", "2026-10-31", 1650, 1750, 1650, "Occupied", "No", ""),
    ("302", "3BR/2BA", 1100, "Carlos & Maria Gonzalez","2026-04-01","2027-03-31",1700, 1750, 1700, "Occupied", "No", ""),
    ("303", "3BR/2BA", 1100, "Derek Thompson",       "2024-05-01", "MTM",        1550, 1750, 1550, "Occupied", "No", ""),
    ("304", "3BR/2BA", 1100, "Amanda Foster",        "2025-07-01", "2026-06-30", 1600, 1750, 1600, "Occupied", "No", ""),
]

# Column indices for UNITS tuples
U_NUM, U_TYPE, U_SF, U_TENANT, U_LEASE_START, U_LEASE_END, U_RENT, U_MARKET, U_DEPOSIT, U_STATUS, U_DELINQ, U_NOTES = range(12)

# ── Derived Financial Constants ────────────────────────────────
TOTAL_UNITS = 18
OCCUPIED_UNITS = sum(1 for u in UNITS if u[U_STATUS] == "Occupied")
VACANT_UNITS = TOTAL_UNITS - OCCUPIED_UNITS
VACANCY_RATE = VACANT_UNITS / TOTAL_UNITS

GROSS_POTENTIAL_RENT_MONTHLY = sum(u[U_MARKET] for u in UNITS)  # All at market
GROSS_POTENTIAL_RENT_ANNUAL = GROSS_POTENTIAL_RENT_MONTHLY * 12  # $298,800
ACTUAL_MONTHLY_RENT = sum(u[U_RENT] for u in UNITS)
ACTUAL_ANNUAL_RENT = ACTUAL_MONTHLY_RENT * 12
VACANCY_LOSS_ANNUAL = sum(u[U_MARKET] for u in UNITS if u[U_STATUS] == "Vacant") * 12

LAUNDRY_INCOME_ACTUAL = 4800
LAUNDRY_INCOME_PROFORMA = 6000
LATE_FEES_ACTUAL = 2400
LATE_FEES_PROFORMA = 3000

# ── Expenses (Annual) ─────────────────────────────────────────
EXPENSES = {
    "Property Taxes":       18750,
    "Insurance":            32400,
    "Repairs & Maintenance":28500,
    "Property Management":  None,  # Calculated as 8% of EGI
    "Utilities (common)":   8400,
    "Landscaping":          4800,
    "Pest Control":         2160,
    "Legal/Admin":          3600,
    "Reserves":             4500,  # $250/unit/yr
}
MGMT_FEE_PCT = 0.08

EXPENSES_PROFORMA = {
    "Property Taxes":       18750,
    "Insurance":            32400,
    "Repairs & Maintenance":22000,
    "Property Management":  None,
    "Utilities (common)":   8400,
    "Landscaping":          4800,
    "Pest Control":         2160,
    "Legal/Admin":          2400,
    "Reserves":             4500,
}

# ── Trailing 12 Financials ─────────────────────────────────────
EGI_ACTUAL = ACTUAL_ANNUAL_RENT + LAUNDRY_INCOME_ACTUAL + LATE_FEES_ACTUAL  # $258,000
MGMT_FEE_ACTUAL = round(EGI_ACTUAL * MGMT_FEE_PCT)  # ~$20,640
TOTAL_EXPENSES_ACTUAL = sum(v for v in EXPENSES.values() if v is not None) + MGMT_FEE_ACTUAL
NOI_ACTUAL = EGI_ACTUAL - TOTAL_EXPENSES_ACTUAL  # ~$134,250

ANNUAL_DEBT_SERVICE = PROPERTY["monthly_debt_service"] * 12  # $73,800
CASH_FLOW_AFTER_DS = NOI_ACTUAL - ANNUAL_DEBT_SERVICE

# Pro Forma
VACANCY_PROFORMA_PCT = 0.05
EGI_PROFORMA = (GROSS_POTENTIAL_RENT_ANNUAL * (1 - VACANCY_PROFORMA_PCT)) + LAUNDRY_INCOME_PROFORMA + LATE_FEES_PROFORMA
MGMT_FEE_PROFORMA = round(EGI_PROFORMA * MGMT_FEE_PCT)
TOTAL_EXPENSES_PROFORMA = sum(v for v in EXPENSES_PROFORMA.values() if v is not None) + MGMT_FEE_PROFORMA
NOI_PROFORMA = EGI_PROFORMA - TOTAL_EXPENSES_PROFORMA

# ── Asking Price & Valuation ──────────────────────────────────
ASKING_PRICE = 1950000
CAP_RATE_ACTUAL = NOI_ACTUAL / ASKING_PRICE
CAP_RATE_PROFORMA = NOI_PROFORMA / ASKING_PRICE

# ── CapEx Items ────────────────────────────────────────────────
CAPEX = [
    ("Roof replacement",      "Medium", 50000, "3-5 years"),
    ("HVAC (3 units)",        "High",   13500, "Immediate"),
    ("Water heaters (6)",     "Medium",  4800, "1-2 years"),
    ("Stucco repair Bldg 2",  "Low",    8000, "1 year"),
    ("Unit 103 turn",         "High",    2500, "Before listing"),
    ("Unit 207 turn",         "Medium",  2500, "Before listing"),
    ("Parking lot reseal",    "Low",     6000, "1 year"),
]
TOTAL_CAPEX = sum(c[2] for c in CAPEX)  # $87,300

# ── Comparable Sales ───────────────────────────────────────────
COMPS = [
    (1, "1520 Emerson Dr NE, Palm Bay",   12, "2025-09", 1380000, 115000, 0.072, 8.4),
    (2, "890 Americana Blvd, Melbourne",   20, "2025-11", 2450000, 122500, 0.069, 8.8),
    (3, "3200 Dixie Hwy NE, Palm Bay",     16, "2025-06", 1680000, 105000, 0.075, 7.9),
    (4, "445 Sarno Rd, Melbourne",          24, "2025-08", 3120000, 130000, 0.065, 9.2),
    (5, "2100 Palm Bay Rd NE",              14, "2025-04", 1540000, 110000, 0.078, 8.1),
]

# ── Security Deposits (total for occupied units) ──────────────
TOTAL_SECURITY_DEPOSITS = sum(u[U_DEPOSIT] for u in UNITS if u[U_STATUS] == "Occupied")

# ── Styling Constants ─────────────────────────────────────────
NAVY = "1E3A5F"
WHITE = "FFFFFF"
RED_BG = "FFEBEE"
YELLOW_BG = "FFF3E0"
GREEN_BG = "E8F5E9"

# ── Monthly Collection Data (12 months: Mar 2025 – Feb 2026) ──
# Each unit gets monthly collection amounts. Vacancies=$0, delinquent=partial.
MONTHS = ["Mar 2025","Apr 2025","May 2025","Jun 2025","Jul 2025","Aug 2025",
           "Sep 2025","Oct 2025","Nov 2025","Dec 2025","Jan 2026","Feb 2026"]

def get_monthly_collections():
    """Return dict of unit_num -> [12 monthly amounts].
    Vacancies get $0 for months they're vacant.
    Delinquent units get partial/zero for recent months.
    """
    collections = {}
    for u in UNITS:
        num = u[U_NUM]
        rent = u[U_RENT]
        status = u[U_STATUS]
        delinq = u[U_DELINQ]

        if status == "Vacant":
            # 105 vacant since Jan 2026 (index 10), 206 vacant since Dec 2025 (index 9)
            if num == "105":
                collections[num] = [1050]*10 + [0, 0]  # Had tenant until Jan
            elif num == "206":
                collections[num] = [1300]*9 + [0, 0, 0]  # Had tenant until Dec
            continue

        months_data = [rent] * 12
        if "60 days" in delinq:
            # Unit 103: 60 days late as of Feb 2026 -> missed Jan + Feb
            months_data[10] = 0  # Jan
            months_data[11] = 0  # Feb
        elif "30 days" in delinq:
            # Unit 207: 30 days late -> missed Feb
            months_data[11] = 0  # Feb
        collections[num] = months_data
    return collections

# ── DD Checklist Items ─────────────────────────────────────────
DD_ITEMS = [
    ("Trailing 12-Month P&L", "Financial", "Received", "Seller", True),
    ("Current Rent Roll", "Financial", "Received", "Seller", True),
    ("Tax Returns (2 years)", "Financial", "Requested", "Seller", True),
    ("Insurance Policy (current)", "Financial", "Received", "Seller", True),
    ("All Lease Agreements (16)", "Legal", "Received", "Seller", True),
    ("Security Deposit Ledger", "Financial", "Received", "Seller", True),
    ("Utility Bills (12 months)", "Financial", "Requested", "Seller", False),
    ("Vendor Contracts", "Operational", "Pending", "Seller", False),
    ("Property Tax Bills (3 years)", "Financial", "Received", "Seller", False),
    ("Survey", "Legal", "Requested", "Title Co", True),
    ("Phase I Environmental", "Environmental", "Pending", "Buyer", True),
    ("Title Commitment", "Legal", "Received", "Title Co", True),
    ("Zoning Verification Letter", "Legal", "Requested", "Seller", False),
    ("Certificate of Occupancy", "Legal", "Pending", "Seller", True),
    ("Building Permits (history)", "Legal", "Pending", "Seller", False),
    ("HOA Documents", "Legal", "Cleared", "Seller", False),
    ("Estoppel Letters (16 tenants)", "Legal", "Requested", "Seller", True),
    ("Inspection Report", "Physical", "Received", "Inspector", True),
    ("Appraisal", "Financial", "Pending", "Buyer", True),
    ("Bank Statements (6 months)", "Financial", "Requested", "Seller", False),
    ("Loan Payoff Letter", "Financial", "Requested", "Seller", True),
    ("LLC Operating Agreement", "Legal", "Received", "Seller", True),
    ("Articles of Organization", "Legal", "Received", "Seller", False),
    ("Property Management Agreement", "Operational", "Received", "Seller", False),
    ("Roof Warranty", "Physical", "Requested", "Seller", False),
    ("HVAC Service Records", "Physical", "Requested", "Seller", False),
    ("Fire Inspection Report", "Physical", "Pending", "Seller", True),
    ("ADA Compliance Documentation", "Legal", "Pending", "Seller", False),
    ("Flood Zone Certification", "Environmental", "Received", "Title Co", False),
    ("Lead Paint Disclosure", "Environmental", "Cleared", "Seller", False),
]
```

**Step 2: Verify data module**

Run: `python -c "import sys; sys.path.insert(0,'scripts'); from data import *; print(f'Units: {TOTAL_UNITS}, NOI: ${NOI_ACTUAL:,.0f}, CapEx: ${TOTAL_CAPEX:,.0f}')"`
Expected: `Units: 18, NOI: $134,250, CapEx: $87,300` (approximately)

**Step 3: Commit**

```bash
git add scripts/data.py
git commit -m "feat(prd-p360-002): add shared data module for case study"
```

---

### Task 2: Rent Roll (XLSX) — 01_rent_roll_2025.xlsx

**Files:**
- Create: `scripts/gen_01_rent_roll.py`
- Output: `case-study/palm-bay-18-unit/01_rent_roll_2025.xlsx`

**Step 1: Create generator script**

The script must create 3 sheets:
- **Rent Roll**: All 18 units with columns A-M, formulas for Rent Delta, conditional formatting
- **Monthly Collections**: 12 months × 18 units with actual collections, summary row
- **Summary**: Occupancy rate, avg rent, total income, upside — all as formulas

Key requirements:
- Header: Navy (#1E3A5F) bg, white bold text, Arial 10pt
- Vacant rows: Red (#FFEBEE) bg
- Below-market rents: Yellow (#FFF3E0) bg
- Currency format `$#,##0`
- Freeze top row, auto-filter on all sheets
- Column I (Rent Delta) = formula `=H{row}-G{row}`
- Summary sheet: all formulas referencing Rent Roll sheet

Full script at `scripts/gen_01_rent_roll.py`. Implementation uses openpyxl with:
- `PatternFill` for conditional row backgrounds
- `Font(name='Arial', size=10)` throughout
- `ws.freeze_panes = 'A2'` and `ws.auto_filter.ref`
- Named number formats `'$#,##0'`

**Step 2: Run generator**

Run: `python scripts/gen_01_rent_roll.py`
Expected: File created at `case-study/palm-bay-18-unit/01_rent_roll_2025.xlsx`

**Step 3: Verify** — Open file or check it exists and has 3 sheets:

Run: `python -c "import openpyxl; wb=openpyxl.load_workbook('case-study/palm-bay-18-unit/01_rent_roll_2025.xlsx'); print(wb.sheetnames)"`
Expected: `['Rent Roll', 'Monthly Collections', 'Summary']`

**Step 4: Commit**

```bash
git add scripts/gen_01_rent_roll.py case-study/palm-bay-18-unit/01_rent_roll_2025.xlsx
git commit -m "feat(prd-p360-002): Create 12-Month Rent Roll for case study validation"
```

---

### Task 3: Profit & Loss Statement (PDF) — 02_profit_loss_T12.pdf

**Files:**
- Create: `scripts/gen_02_pnl.py`
- Output: `case-study/palm-bay-18-unit/02_profit_loss_T12.pdf`

**Step 1: Create generator script**

Uses reportlab to generate a professional P&L with:
- Header: "Palm Bay Palms Apartments — Trailing 12-Month P&L"
- Period: March 2025 – February 2026
- Income section: Rental Income, Laundry, Late Fees, Other
- 12 monthly columns + Total column
- Expense section: all categories from `data.EXPENSES`
- NOI line
- Debt Service: $6,150/month = $73,800/yr
- Cash Flow After Debt Service
- Footer: "Prepared by Property360 Real Estate | Mariam Shapira"
- Alternating row shading, subtotals in bold, negatives in red parens
- Professional letterhead style

Uses `reportlab.platypus` with `Table`, `TableStyle`, custom `Paragraph` styles.

**Step 2: Run generator**

Run: `python scripts/gen_02_pnl.py`
Expected: PDF file at `case-study/palm-bay-18-unit/02_profit_loss_T12.pdf`

**Step 3: Verify**

Run: `python -c "import os; f='case-study/palm-bay-18-unit/02_profit_loss_T12.pdf'; print(f'Exists: {os.path.exists(f)}, Size: {os.path.getsize(f)} bytes')"`
Expected: Exists: True, Size: > 5000 bytes

**Step 4: Commit**

```bash
git add scripts/gen_02_pnl.py case-study/palm-bay-18-unit/02_profit_loss_T12.pdf
git commit -m "feat(prd-p360-002): Create Profit & Loss Statement for case study validation"
```

---

### Task 4: Inspection Report (PDF) — 03_inspection_report.pdf

**Files:**
- Create: `scripts/gen_03_inspection.py`
- Output: `case-study/palm-bay-18-unit/03_inspection_report.pdf`

**Step 1: Create generator script**

Multi-page PDF with reportlab:
1. Cover page: Property address, date (Feb 10, 2026), inspector "John Martinez, HI-3847"
2. Executive Summary: Fair-to-Good condition, major items listed
3. Sections: Structural, Roofing, Plumbing, Electrical, HVAC, Environmental, Unit Interiors
4. CapEx Summary Table from `data.CAPEX` — must total $87,300
5. Each section has detailed findings per PRD

**Step 2: Run, verify, commit** (same pattern as above)

```bash
git add scripts/gen_03_inspection.py case-study/palm-bay-18-unit/03_inspection_report.pdf
git commit -m "feat(prd-p360-002): Create Pre-Listing Inspection Report for case study validation"
```

---

### Task 5: Sample Lease (DOCX) — 04_sample_lease_unit201.docx

**Files:**
- Create: `scripts/gen_04_lease.py`
- Output: `case-study/palm-bay-18-unit/04_sample_lease_unit201.docx`

**Step 1: Create generator script**

Uses python-docx to create a Florida Residential Lease Agreement:
- Landlord: Sunshine Palms Holdings LLC
- Tenant: David & Ana Rodriguez, Unit 201, 2BR/1BA, 850 sf
- Term: Oct 1, 2025 – Sep 30, 2026
- Rent: $1,350, due 1st, late after 5th, $50 late fee
- Security deposit: $1,350 per FL Statute 83.49
- FL-specific clauses: 83.49, 83.50, 83.56, 404.056
- Pet policy, utilities, signatures, notary block

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_04_lease.py case-study/palm-bay-18-unit/04_sample_lease_unit201.docx
git commit -m "feat(prd-p360-002): Create Sample Lease Agreement for case study validation"
```

---

### Task 6: Title Search Summary (PDF) — 05_title_search.pdf

**Files:**
- Create: `scripts/gen_05_title.py`
- Output: `case-study/palm-bay-18-unit/05_title_search.pdf`

**Step 1: Create generator script**

PDF with:
- Title company: "Brevard Title & Abstract Co."
- Legal description with Plat Book/Page references
- Chain of title (3 transfers: 2003, 2012, 2018)
- Liens: Mortgage ($980K), Municipal code lien ($1,850 — MUST RESOLVE)
- Easements: FPL utility easement
- Tax status: 2025 paid current
- Recommendation: Title insurable upon lien resolution

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_05_title.py case-study/palm-bay-18-unit/05_title_search.pdf
git commit -m "feat(prd-p360-002): Create Title Search Summary for case study validation"
```

---

### Task 7: Valuation Comps (XLSX) — 06_valuation_comps.xlsx

**Files:**
- Create: `scripts/gen_06_comps.py`
- Output: `case-study/palm-bay-18-unit/06_valuation_comps.xlsx`

**Step 1: Create generator script**

3-sheet Excel workbook:
- **Comparable Sales**: 5 comps from `data.COMPS` with columns: #, Address, Units, Sale Date, Sale Price, Price/Unit, Cap Rate, GRM
- **Valuation Scenarios**: Income Approach (NOI/cap at 6.5%, 7.0%, 7.5%), GRM Approach, Price Per Unit — ALL AS FORMULAS
- **Buyer Underwriting**: 3 scenarios (Conservative/Base/Aggressive) with DSCR, Cash-on-Cash, Cap Rate, IRR formulas

Same styling as rent roll (Navy headers, Arial 10pt, currency format).

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_06_comps.py case-study/palm-bay-18-unit/06_valuation_comps.xlsx
git commit -m "feat(prd-p360-002): Create Valuation Comps for case study validation"
```

---

### Task 8: Offering Memorandum (PPTX) — 07_offering_memorandum.pptx

**Files:**
- Create: `scripts/gen_07_om.py`
- Output: `case-study/palm-bay-18-unit/07_offering_memorandum.pptx`

**Step 1: Create generator script**

10-slide PowerPoint using python-pptx:
1. Cover: Title + price + branding
2. Investment Highlights: 4 bullets
3. Property Overview: key facts
4. Unit Mix Table
5. Financial Summary: T12 NOI, Pro Forma NOI, Cap Rates
6. Rent Comparables
7. CapEx Summary from inspection
8. Location/Demographics
9. Pro Forma 3-year projection
10. Offer Terms

Uses consistent color scheme (Navy primary), tables on data slides.

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_07_om.py case-study/palm-bay-18-unit/07_offering_memorandum.pptx
git commit -m "feat(prd-p360-002): Create Offering Memorandum for case study validation"
```

---

### Task 9: LOI Template (DOCX) — 08_loi_template.docx

**Files:**
- Create: `scripts/gen_08_loi.py`
- Output: `case-study/palm-bay-18-unit/08_loi_template.docx`

**Step 1: Create generator script**

Standard commercial LOI with python-docx:
- Buyer: "[BUYER NAME]", Seller: Sunshine Palms Holdings LLC
- Blank fields for Purchase Price, Earnest Money
- Terms: 15-day inspection, 30-day financing, 45-day closing
- 1031 Exchange cooperation clause
- Non-binding except confidentiality + exclusivity (30 days)
- Signature blocks

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_08_loi.py case-study/palm-bay-18-unit/08_loi_template.docx
git commit -m "feat(prd-p360-002): Create LOI Template for case study validation"
```

---

### Task 10: Due Diligence Tracker (XLSX) — 09_due_diligence_tracker.xlsx

**Files:**
- Create: `scripts/gen_09_dd.py`
- Output: `case-study/palm-bay-18-unit/09_due_diligence_tracker.xlsx`

**Step 1: Create generator script**

Excel with 30+ rows from `data.DD_ITEMS`:
- Columns: DD Item, Category, Status, Responsible Party, Date Requested, Date Received, Days Outstanding (formula), Notes, Critical?
- Conditional formatting: Green=Cleared, Yellow=Received, Red=Pending
- Days Outstanding = `=IF(F{row}="",TODAY()-E{row},F{row}-E{row})`
- Same styling conventions

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_09_dd.py case-study/palm-bay-18-unit/09_due_diligence_tracker.xlsx
git commit -m "feat(prd-p360-002): Create Due Diligence Tracker for case study validation"
```

---

### Task 11: Closing Worksheet (XLSX) — 10_closing_worksheet.xlsx

**Files:**
- Create: `scripts/gen_10_closing.py`
- Output: `case-study/palm-bay-18-unit/10_closing_worksheet.xlsx`

**Step 1: Create generator script**

3-sheet Excel:
- **Settlement Statement**: Buyer/Seller columns, purchase price $1,950,000, earnest money $50,000, prorations (taxes, rents, deposits=$21,500), seller debits (mortgage payoff $980K, commission 5% $97,500, title insurance $4,200, lien $1,850, doc stamps $13,650, recording $250), Net Proceeds formula
- **Security Deposit Transfer**: 16 occupied units with deposits, total formula, transfer acknowledgment text
- **Tenant Notification**: Template letter per FL Statute 83.50

Security deposits MUST match rent roll total. Use formulas for all calculated fields.

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_10_closing.py case-study/palm-bay-18-unit/10_closing_worksheet.xlsx
git commit -m "feat(prd-p360-002): Create Closing Worksheet for case study validation"
```

---

### Task 12: 3-Year Pro Forma (XLSX) — 11_proforma_3yr.xlsx

**Files:**
- Create: `scripts/gen_11_proforma.py`
- Output: `case-study/palm-bay-18-unit/11_proforma_3yr.xlsx`

**Step 1: Create generator script**

Excel with assumption cells (blue text) and Year 1/2/3 columns:
- Assumptions: 3% rent growth, 2% expense growth, vacancy 11.1%→5% by Y2, CapEx $87,300 Y1/$10K thereafter, 8% mgmt fee
- All values as formulas referencing assumption cells
- Income, Expenses, NOI, Debt Service, Cash Flow rows
- CapEx $87,300 in Year 1 MUST match inspection report total

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_11_proforma.py case-study/palm-bay-18-unit/11_proforma_3yr.xlsx
git commit -m "feat(prd-p360-002): Create 3-Year Pro Forma for case study validation"
```

---

### Task 13: Entity Summary (DOCX) — 12_entity_summary.docx

**Files:**
- Create: `scripts/gen_12_entity.py`
- Output: `case-study/palm-bay-18-unit/12_entity_summary.docx`

**Step 1: Create generator script**

Word doc with python-docx:
- Entity: Sunshine Palms Holdings LLC
- State: Florida, Doc# L18000045678, Filed Feb 1, 2018
- Registered Agent: Mariam Shapira
- Members: Mariam Shapira (100% Managing Member)
- Status: Active, Annual Report filed through 2026
- EIN: 82-XXXXXXX
- Operating Agreement Summary: Single-member, full authority to sell

**Step 2: Run, verify, commit**

```bash
git add scripts/gen_12_entity.py case-study/palm-bay-18-unit/12_entity_summary.docx
git commit -m "feat(prd-p360-002): Create Entity Summary for case study validation"
```

---

### Task 14: GitHub Action for Supabase Seeding

**Files:**
- Create: `.github/workflows/seed-supabase.yml`

**Step 1: Create workflow**

```yaml
name: Seed Supabase — Case Study Data
on:
  workflow_dispatch:
    inputs:
      confirm:
        description: 'Type "seed" to confirm'
        required: true

jobs:
  seed:
    if: github.event.inputs.confirm == 'seed'
    runs-on: ubuntu-latest
    steps:
      - name: Insert Property
        run: |
          curl -s -X POST \
            "${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}/rest/v1/p360_properties" \
            -H "apikey: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Content-Type: application/json" \
            -H "Prefer: return=representation" \
            -d '[JSON with property data]'

      - name: Insert Documents (12 rows)
        run: |
          # Insert all 12 document metadata rows
          curl -s -X POST \
            "${{ secrets.NEXT_PUBLIC_SUPABASE_URL }}/rest/v1/p360_documents" \
            -H "apikey: ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Authorization: Bearer ${{ secrets.SUPABASE_SERVICE_ROLE_KEY }}" \
            -H "Content-Type: application/json" \
            -d '[12 document rows]'
```

**Step 2: Commit and push**

```bash
git add .github/workflows/seed-supabase.yml
git commit -m "feat(prd-p360-002): Add GitHub Action for Supabase seeding"
```

---

### Task 15: Push All to GitHub + Validate

**Step 1: Push to main**

```bash
git push origin main
```

**Step 2: Run validation**

Verify:
- All 12 files exist in `case-study/palm-bay-18-unit/`
- XLSX files load without errors and have correct sheet counts
- PDF files exist and are > 5KB
- DOCX files load without errors
- Data consistency: rent roll totals match P&L, CapEx matches pro forma, security deposits match closing

Run validation script that checks all the above programmatically.

---

## Execution Notes

- Tasks 2-13 are independent of each other (all depend only on Task 1 data module)
- Tasks 2-13 CAN be parallelized with subagents
- Task 14 depends on knowing the exact data (after Task 1)
- Task 15 depends on all prior tasks
- Each commit follows format: `feat(prd-p360-002): Create [doc name] for case study validation`
