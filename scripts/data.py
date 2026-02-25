"""
Property360 Case Study - Shared Data Module
All property, unit, financial, and CapEx data for Palm Bay Palms Apartments.
Every generator script imports from this module.
"""

# -- Property Info -----------------------------------------------------------
PROPERTY = {
    "name": "Palm Bay Palms Apartments",
    "address": "2750 Malabar Road SE, Palm Bay, FL 32907",
    "city": "Palm Bay",
    "state": "FL",
    "zip": "32907",
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

# -- Unit Mix ----------------------------------------------------------------
# (unit_num, type, sf, tenant, lease_start, lease_end, rent, market_rent,
#  deposit, status, delinquent, notes)
UNITS = [
    ("101", "1BR/1BA", 650, "Maria Santos",          "2025-09-01", "2026-08-31", 1050, 1200, 1050, "Occupied", "No", ""),
    ("102", "1BR/1BA", 650, "James Wilson",           "2025-06-01", "2026-05-31", 1100, 1200, 1100, "Occupied", "No", ""),
    ("103", "1BR/1BA", 650, "Tanya Brown",            "2024-03-01", "MTM",         950, 1200,  950, "Occupied", "Yes - 60 days", "Delinquent - 60 days past due"),
    ("104", "1BR/1BA", 650, "Robert Chen",            "2025-12-01", "2026-11-30", 1150, 1200, 1150, "Occupied", "No", ""),
    ("105", "1BR/1BA", 650, "",                       "",           "",              0, 1200,    0, "Vacant",   "No", "Vacant since Jan 2026"),
    ("106", "1BR/1BA", 650, "Lisa Park",              "2024-06-01", "MTM",        1000, 1200, 1000, "Occupied", "No", ""),
    ("201", "2BR/1BA", 850, "David & Ana Rodriguez",  "2025-10-01", "2026-09-30", 1350, 1450, 1350, "Occupied", "No", ""),
    ("202", "2BR/1BA", 850, "Michael Turner",         "2026-02-01", "2027-01-31", 1400, 1450, 1400, "Occupied", "No", ""),
    ("203", "2BR/1BA", 850, "Sarah Johnson",          "2025-05-01", "2026-04-30", 1250, 1450, 1250, "Occupied", "No", ""),
    ("204", "2BR/1BA", 850, "Kevin Lee",              "2024-09-01", "MTM",        1300, 1450, 1300, "Occupied", "No", ""),
    ("205", "2BR/1BA", 850, "Patricia Martinez",      "2026-01-01", "2026-12-31", 1350, 1450, 1350, "Occupied", "No", ""),
    ("206", "2BR/1BA", 850, "",                       "",           "",              0, 1450,    0, "Vacant",   "No", "Vacant since Dec 2025"),
    ("207", "2BR/1BA", 850, "Anthony Williams",       "2024-07-01", "MTM",        1200, 1450, 1200, "Occupied", "Yes - 30 days", "Delinquent - 30 days past due"),
    ("208", "2BR/1BA", 850, "Jennifer Davis",         "2025-08-01", "2026-07-31", 1400, 1450, 1400, "Occupied", "No", ""),
    ("301", "3BR/2BA", 1100, "The Nguyen Family",     "2025-11-01", "2026-10-31", 1650, 1750, 1650, "Occupied", "No", ""),
    ("302", "3BR/2BA", 1100, "Carlos & Maria Gonzalez","2026-04-01","2027-03-31", 1700, 1750, 1700, "Occupied", "No", ""),
    ("303", "3BR/2BA", 1100, "Derek Thompson",        "2024-05-01", "MTM",        1550, 1750, 1550, "Occupied", "No", ""),
    ("304", "3BR/2BA", 1100, "Amanda Foster",         "2025-07-01", "2026-06-30", 1600, 1750, 1600, "Occupied", "No", ""),
]

# Column indices
U_NUM, U_TYPE, U_SF, U_TENANT, U_LEASE_START, U_LEASE_END = range(6)
U_RENT, U_MARKET, U_DEPOSIT, U_STATUS, U_DELINQ, U_NOTES = range(6, 12)

# -- Derived Financial Constants ---------------------------------------------
TOTAL_UNITS = 18
OCCUPIED_UNITS = sum(1 for u in UNITS if u[U_STATUS] == "Occupied")
VACANT_UNITS = TOTAL_UNITS - OCCUPIED_UNITS
VACANCY_RATE = VACANT_UNITS / TOTAL_UNITS

GROSS_POTENTIAL_RENT_MONTHLY = sum(u[U_MARKET] for u in UNITS)
GROSS_POTENTIAL_RENT_ANNUAL = GROSS_POTENTIAL_RENT_MONTHLY * 12  # $298,800
ACTUAL_MONTHLY_RENT = sum(u[U_RENT] for u in UNITS)
ACTUAL_ANNUAL_RENT = ACTUAL_MONTHLY_RENT * 12
VACANCY_LOSS_ANNUAL = sum(u[U_MARKET] for u in UNITS if u[U_STATUS] == "Vacant") * 12

LAUNDRY_INCOME_ACTUAL = 4800
LAUNDRY_INCOME_PROFORMA = 6000
LATE_FEES_ACTUAL = 2400
LATE_FEES_PROFORMA = 3000

# -- Expenses (Annual, Trailing 12) -----------------------------------------
EXPENSES_ACTUAL = [
    ("Property Taxes",        18750),
    ("Insurance",             32400),
    ("Repairs & Maintenance", 28500),
    ("Property Management",   None),   # 8% of EGI, calculated below
    ("Utilities (common)",     8400),
    ("Landscaping",            4800),
    ("Pest Control",           2160),
    ("Legal/Admin",            3600),
    ("Reserves",               4500),  # $250/unit/yr
]

EXPENSES_PROFORMA = [
    ("Property Taxes",        18750),
    ("Insurance",             32400),
    ("Repairs & Maintenance", 22000),
    ("Property Management",   None),
    ("Utilities (common)",     8400),
    ("Landscaping",            4800),
    ("Pest Control",           2160),
    ("Legal/Admin",            2400),
    ("Reserves",               4500),
]

MGMT_FEE_PCT = 0.08

# -- PRD-stated Financial Summary (use these for P&L and other docs) ---------
# These are the authoritative numbers from the PRD. Minor differences from
# bottom-up unit calculations are expected in a hypothetical case study.
GPR_ACTUAL = 282000          # Gross Potential Rent (T12)
VACANCY_LOSS_ACTUAL_PRD = 31200  # 2 units, 11.1%
EGI_ACTUAL = 250800          # GPR - vacancy
TOTAL_REVENUE_ACTUAL = 258000  # EGI + laundry + late fees
MGMT_FEE_ACTUAL = 20640       # 8% of total revenue
TOTAL_EXPENSES_ACTUAL = 123750
NOI_ACTUAL = 134250

GPR_PROFORMA = 298800         # All units at market rent
VACANCY_PROFORMA_PCT = 0.05
VACANCY_LOSS_PROFORMA = 14940  # 5% of GPR
EGI_PROFORMA = 283860         # GPR - 5% vacancy
TOTAL_REVENUE_PROFORMA = 292860  # EGI + laundry + late fees
MGMT_FEE_PROFORMA = 23429     # 8% of total revenue
TOTAL_EXPENSES_PROFORMA = 118839
NOI_PROFORMA = 174021

ANNUAL_DEBT_SERVICE = PROPERTY["monthly_debt_service"] * 12  # $73,800
CASH_FLOW_AFTER_DS = NOI_ACTUAL - ANNUAL_DEBT_SERVICE

# -- Asking Price & Valuation -----------------------------------------------
ASKING_PRICE = 1950000
CAP_RATE_ACTUAL = NOI_ACTUAL / ASKING_PRICE
CAP_RATE_PROFORMA = NOI_PROFORMA / ASKING_PRICE

# -- CapEx -------------------------------------------------------------------
CAPEX = [
    ("Roof replacement",       "Medium", 50000, "3-5 years"),
    ("HVAC (3 units)",         "High",   13500, "Immediate"),
    ("Water heaters (6)",      "Medium",  4800, "1-2 years"),
    ("Stucco repair Bldg 2",  "Low",     8000, "1 year"),
    ("Unit 103 turn",          "High",    2500, "Before listing"),
    ("Unit 207 turn",          "Medium",  2500, "Before listing"),
    ("Parking lot reseal",     "Low",     6000, "1 year"),
]
TOTAL_CAPEX = sum(c[2] for c in CAPEX)  # $87,300

# -- Comparable Sales --------------------------------------------------------
COMPS = [
    (1, "1520 Emerson Dr NE, Palm Bay",  12, "2025-09", 1380000, 115000, 0.072, 8.4),
    (2, "890 Americana Blvd, Melbourne",  20, "2025-11", 2450000, 122500, 0.069, 8.8),
    (3, "3200 Dixie Hwy NE, Palm Bay",   16, "2025-06", 1680000, 105000, 0.075, 7.9),
    (4, "445 Sarno Rd, Melbourne",        24, "2025-08", 3120000, 130000, 0.065, 9.2),
    (5, "2100 Palm Bay Rd NE",            14, "2025-04", 1540000, 110000, 0.078, 8.1),
]

# -- Security Deposits -------------------------------------------------------
TOTAL_SECURITY_DEPOSITS = sum(u[U_DEPOSIT] for u in UNITS if u[U_STATUS] == "Occupied")

# -- Styling Constants -------------------------------------------------------
NAVY = "1E3A5F"
WHITE = "FFFFFF"
RED_BG = "FFEBEE"
YELLOW_BG = "FFF3E0"
GREEN_BG = "E8F5E9"

# -- Monthly Collection Data (Mar 2025 - Feb 2026) --------------------------
MONTHS = [
    "Mar 2025", "Apr 2025", "May 2025", "Jun 2025", "Jul 2025", "Aug 2025",
    "Sep 2025", "Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026",
]


def get_monthly_collections():
    """Return dict of unit_num -> [12 monthly amounts].
    Vacancies=$0 for vacant months. Delinquent=partial/zero for recent months.
    """
    collections = {}
    for u in UNITS:
        num, rent, status, delinq = u[U_NUM], u[U_RENT], u[U_STATUS], u[U_DELINQ]

        if status == "Vacant":
            if num == "105":
                # Had tenant at $1,050 until Jan 2026 (index 10)
                collections[num] = [1050] * 10 + [0, 0]
            elif num == "206":
                # Had tenant at $1,300 until Dec 2025 (index 9)
                collections[num] = [1300] * 9 + [0, 0, 0]
            continue

        months_data = [rent] * 12
        if "60 days" in delinq:
            # Unit 103: missed Jan + Feb 2026
            months_data[10] = 0
            months_data[11] = 0
        elif "30 days" in delinq:
            # Unit 207: missed Feb 2026
            months_data[11] = 0
        collections[num] = months_data
    return collections


# -- Due Diligence Items -----------------------------------------------------
DD_ITEMS = [
    ("Trailing 12-Month P&L",           "Financial",      "Received",  "Seller",    True),
    ("Current Rent Roll",               "Financial",      "Received",  "Seller",    True),
    ("Tax Returns (2 years)",           "Financial",      "Requested", "Seller",    True),
    ("Insurance Policy (current)",      "Financial",      "Received",  "Seller",    True),
    ("All Lease Agreements (16)",       "Legal",          "Received",  "Seller",    True),
    ("Security Deposit Ledger",         "Financial",      "Received",  "Seller",    True),
    ("Utility Bills (12 months)",       "Financial",      "Requested", "Seller",    False),
    ("Vendor Contracts",                "Operational",    "Pending",   "Seller",    False),
    ("Property Tax Bills (3 years)",    "Financial",      "Received",  "Seller",    False),
    ("Survey",                          "Legal",          "Requested", "Title Co",  True),
    ("Phase I Environmental",           "Environmental",  "Pending",   "Buyer",     True),
    ("Title Commitment",                "Legal",          "Received",  "Title Co",  True),
    ("Zoning Verification Letter",      "Legal",          "Requested", "Seller",    False),
    ("Certificate of Occupancy",        "Legal",          "Pending",   "Seller",    True),
    ("Building Permits (history)",      "Legal",          "Pending",   "Seller",    False),
    ("HOA Documents",                   "Legal",          "Cleared",   "Seller",    False),
    ("Estoppel Letters (16 tenants)",   "Legal",          "Requested", "Seller",    True),
    ("Inspection Report",               "Physical",       "Received",  "Inspector", True),
    ("Appraisal",                       "Financial",      "Pending",   "Buyer",     True),
    ("Bank Statements (6 months)",      "Financial",      "Requested", "Seller",    False),
    ("Loan Payoff Letter",              "Financial",      "Requested", "Seller",    True),
    ("LLC Operating Agreement",         "Legal",          "Received",  "Seller",    True),
    ("Articles of Organization",        "Legal",          "Received",  "Seller",    False),
    ("Property Management Agreement",   "Operational",    "Received",  "Seller",    False),
    ("Roof Warranty",                   "Physical",       "Requested", "Seller",    False),
    ("HVAC Service Records",            "Physical",       "Requested", "Seller",    False),
    ("Fire Inspection Report",          "Physical",       "Pending",   "Seller",    True),
    ("ADA Compliance Documentation",    "Legal",          "Pending",   "Seller",    False),
    ("Flood Zone Certification",        "Environmental",  "Received",  "Title Co",  False),
    ("Lead Paint Disclosure",           "Environmental",  "Cleared",   "Seller",    False),
]

# -- Output path helper ------------------------------------------------------
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(REPO_ROOT, "case-study", "palm-bay-18-unit")


def output_path(filename):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return os.path.join(OUTPUT_DIR, filename)
