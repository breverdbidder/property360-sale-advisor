# CLAUDE_CODE_CASE_STUDY.md — PRD-P360-002
# Property360 Sale Advisor — End-to-End Validation Case Study
# 18-Unit Multifamily | Palm Bay, Florida
# READ THIS FILE FIRST. Execute tasks in order.

## SESSION INITIALIZATION PROTOCOL
1. Read this entire file
2. `cd` to a working directory
3. Clone `breverdbidder/property360-sale-advisor` (token: ${{ secrets.WORKFLOW_TOKEN }})
4. Execute tasks sequentially — each task produces a deliverable file
5. Push all files to GitHub under `case-study/palm-bay-18-unit/`
6. Insert property + document metadata to Supabase
7. After ALL files created: run validation checklist

## GITHUB
- Repo: `breverdbidder/property360-sale-advisor`
- Branch: `main`
- Path: `case-study/palm-bay-18-unit/`
- Token: `${{ secrets.WORKFLOW_TOKEN }}`

## SUPABASE
- URL: `https://mocerqjnksmhcjzxrewo.supabase.co`
- Service Key: ends with `...Tqp9nE` (get from SUPABASE_CREDENTIALS.md or GitHub secret SUPABASE_SERVICE_KEY)
- Anon Key: `${{ secrets.SUPABASE_KEY }}`

---

## 🏢 THE PROPERTY — HYPOTHETICAL CASE STUDY

### Subject Property
| Field | Value |
|-------|-------|
| **Name** | Palm Bay Palms Apartments |
| **Address** | 2750 Malabar Road SE, Palm Bay, FL 32907 |
| **Parcel ID** | 29-37-05-00-00142.0-0000 (hypothetical) |
| **Property Type** | Multi-family (18 units) |
| **Year Built** | 1986 |
| **Lot Size** | 1.2 acres (52,272 sq ft) |
| **Total Building SF** | 14,400 sq ft |
| **Unit Mix** | 6x 1BR/1BA (650 sf) + 8x 2BR/1BA (850 sf) + 4x 3BR/2BA (1,100 sf) |
| **Zoning** | RM-13 (Residential Multifamily) |
| **Flood Zone** | X (minimal risk) |
| **Owner Entity** | Sunshine Palms Holdings LLC |
| **Purchase Date** | March 15, 2018 |
| **Purchase Price** | $1,450,000 |
| **Current Mortgage** | $980,000 remaining @ 4.75% (30yr fixed, originated 2018) |
| **Annual Taxes** | $18,750 |
| **Annual Insurance** | $32,400 (post-2024 FL market) |

### Unit Mix Detail
| Unit # | Type | SF | Current Rent | Market Rent | Status | Tenant | Lease Expires |
|--------|------|-----|-------------|-------------|--------|--------|---------------|
| 101 | 1BR/1BA | 650 | $1,050 | $1,200 | Occupied | Maria Santos | 2026-08-31 |
| 102 | 1BR/1BA | 650 | $1,100 | $1,200 | Occupied | James Wilson | 2026-05-31 |
| 103 | 1BR/1BA | 650 | $950 | $1,200 | Occupied | Tanya Brown | MTM |
| 104 | 1BR/1BA | 650 | $1,150 | $1,200 | Occupied | Robert Chen | 2026-11-30 |
| 105 | 1BR/1BA | 650 | $0 | $1,200 | VACANT | — | — |
| 106 | 1BR/1BA | 650 | $1,000 | $1,200 | Occupied | Lisa Park | MTM |
| 201 | 2BR/1BA | 850 | $1,350 | $1,450 | Occupied | David & Ana Rodriguez | 2026-09-30 |
| 202 | 2BR/1BA | 850 | $1,400 | $1,450 | Occupied | Michael Turner | 2027-01-31 |
| 203 | 2BR/1BA | 850 | $1,250 | $1,450 | Occupied | Sarah Johnson | 2026-04-30 |
| 204 | 2BR/1BA | 850 | $1,300 | $1,450 | Occupied | Kevin Lee | MTM |
| 205 | 2BR/1BA | 850 | $1,350 | $1,450 | Occupied | Patricia Martinez | 2026-12-31 |
| 206 | 2BR/1BA | 850 | $0 | $1,450 | VACANT | — | — |
| 207 | 2BR/1BA | 850 | $1,200 | $1,450 | Occupied | Anthony Williams | MTM |
| 208 | 2BR/1BA | 850 | $1,400 | $1,450 | Occupied | Jennifer Davis | 2026-07-31 |
| 301 | 3BR/2BA | 1,100 | $1,650 | $1,750 | Occupied | The Nguyen Family | 2026-10-31 |
| 302 | 3BR/2BA | 1,100 | $1,700 | $1,750 | Occupied | Carlos & Maria Gonzalez | 2027-03-31 |
| 303 | 3BR/2BA | 1,100 | $1,550 | $1,750 | Occupied | Derek Thompson | MTM |
| 304 | 3BR/2BA | 1,100 | $1,600 | $1,750 | Occupied | Amanda Foster | 2026-06-30 |

### Financial Summary
| Metric | Actual (Trailing 12) | Stabilized (Pro Forma) |
|--------|---------------------|----------------------|
| Gross Potential Rent | $282,000/yr | $298,800/yr |
| Vacancy Loss (2 units = 11.1%) | ($31,200) | ($14,940) 5% |
| Effective Gross Income | $250,800 | $283,860 |
| Laundry Income | $4,800 | $6,000 |
| Late Fees/Other | $2,400 | $3,000 |
| **Total Revenue** | **$258,000** | **$292,860** |
| Property Taxes | ($18,750) | ($18,750) |
| Insurance | ($32,400) | ($32,400) |
| Repairs & Maintenance | ($28,500) | ($22,000) |
| Property Management (8%) | ($20,640) | ($23,429) |
| Utilities (common area) | ($8,400) | ($8,400) |
| Landscaping | ($4,800) | ($4,800) |
| Pest Control | ($2,160) | ($2,160) |
| Legal/Admin | ($3,600) | ($2,400) |
| Reserves ($250/unit/yr) | ($4,500) | ($4,500) |
| **Total Expenses** | **($123,750)** | **($118,839)** |
| **NOI** | **$134,250** | **$174,021** |
| Expense Ratio | 47.9% | 40.6% |
| Cap Rate (at $1.95M) | 6.88% | 8.92% |

---

## 📋 DOCUMENT CREATION TASKS

Each task creates ONE deliverable file. Format matters — these files will be uploaded into the Property360 Sale Advisor to test the AI Document Intelligence Engine.

---

### TASK 1: 12-Month Rent Roll (XLSX)
**File:** `case-study/palm-bay-18-unit/01_rent_roll_2025.xlsx`
**Format:** Excel with formulas
**Phase Coverage:** Phase 3 (Tenancy & Lease Audit)

**Sheet 1: "Rent Roll"**
- Column A: Unit # (101-304)
- Column B: Unit Type (1BR/1BA, 2BR/1BA, 3BR/2BA)
- Column C: SF
- Column D: Tenant Name
- Column E: Lease Start
- Column F: Lease Expiration (or "MTM")
- Column G: Monthly Rent
- Column H: Market Rent
- Column I: Rent Delta (formula: =H-G)
- Column J: Security Deposit
- Column K: Status (Occupied/Vacant)
- Column L: Delinquent? (Yes/No — Mark Unit 103 Tanya Brown as 60 days late, Unit 207 Anthony Williams as 30 days late)
- Column M: Notes

**Sheet 2: "Monthly Collections"**
- 12 months of rent collection data (Mar 2025 – Feb 2026)
- Rows = 18 units, Columns = months
- Show actual collected amounts (vacancies = $0, delinquent = partial)
- Summary row: Total Collected, Vacancy Loss, Delinquency Loss
- Use formulas for all totals

**Sheet 3: "Summary"**
- Occupancy Rate (formula)
- Average Rent per Unit (formula)
- Average Rent per SF (formula)
- Total Monthly Income (formula)
- Total Annual Income (formula)
- Below-market units count
- Total upside if raised to market (formula)

**Formatting:**
- Header row: Navy (#1E3A5F) background, white text, bold
- Vacant units: Red (#FFEBEE) background
- Below-market rents: Yellow (#FFF3E0) background
- Currency format: $#,##0
- Professional font: Arial 10pt
- Freeze top row, auto-filter enabled

---

### TASK 2: Profit & Loss Statement (PDF)
**File:** `case-study/palm-bay-18-unit/02_profit_loss_T12.pdf`
**Format:** PDF (generate via reportlab or weasyprint)
**Phase Coverage:** Phase 1 (Financial Assessment), Phase 4 (Income Optimization)

**Content:**
- Header: "Palm Bay Palms Apartments — Trailing 12-Month P&L"
- Period: March 2025 – February 2026
- Income section (Rental Income, Laundry, Late Fees, Other)
- Monthly breakdown columns (12 months)
- Expense section (all categories from Financial Summary above)
- NOI line
- Debt Service line ($6,150/month = $73,800/yr)
- Cash Flow After Debt Service
- Footer: "Prepared by Property360 Real Estate | Mariam Shapira"

**Formatting:**
- Professional letterhead style
- Table with alternating row shading
- Subtotals in bold
- Negative numbers in parentheses and red

---

### TASK 3: Pre-Listing Inspection Report (PDF)
**File:** `case-study/palm-bay-18-unit/03_inspection_report.pdf`
**Format:** PDF
**Phase Coverage:** Phase 2 (Property Condition Review)

**Content — Multi-page report:**
1. **Cover Page:** Property address, inspection date (Feb 10, 2026), inspector name: "John Martinez, HI-3847, FL Licensed Inspector"
2. **Executive Summary:** Overall condition: Fair-to-Good. Major items: Roof (12 yr old, ~5 yr remaining), 3 HVAC units need replacement, Building 2 exterior stucco cracking.
3. **Structural:** Foundation — slab on grade, no visible settlement. Stucco exterior — Building 1 good, Building 2 has hairline cracks at window headers (cosmetic, monitor).
4. **Roofing:** Architectural shingle, installed 2014, ~5-year remaining life. No active leaks. Some granule loss on south exposure. Budget $45,000-55,000 for replacement.
5. **Plumbing:** Copper supply lines (good). PVC drain lines. Water heaters: 6 individual units need replacement within 2 years ($800 each). No polybutylene.
6. **Electrical:** 200A main panel. Updated to circuit breakers (no fuse boxes). GFCIs present in kitchens/baths. Exterior lighting adequate.
7. **HVAC:** 18 individual split systems. Units 103, 206, 303 have failing compressors — budget $4,500 each replacement. Average system age: 8 years.
8. **Environmental:** No visible mold. No asbestos suspected (built 1986 — possible in popcorn ceilings, recommend test before removal). Lead paint unlikely (post-1978). Radon: low risk area.
9. **Unit Interiors (sample of 6 units inspected):** General good condition. Units 103 and 207 show deferred maintenance (damaged flooring, stained carpet). Budget $2,500/unit for turn.
10. **Capital Expenditure Summary Table:**

| Item | Priority | Est. Cost | Timeline |
|------|----------|-----------|----------|
| Roof replacement | Medium | $50,000 | 3-5 years |
| HVAC (3 units) | High | $13,500 | Immediate |
| Water heaters (6) | Medium | $4,800 | 1-2 years |
| Stucco repair Bldg 2 | Low | $8,000 | 1 year |
| Unit 103 turn | High | $2,500 | Before listing |
| Unit 207 turn | Medium | $2,500 | Before listing |
| Parking lot reseal | Low | $6,000 | 1 year |
| **Total CapEx** | | **$87,300** | |

---

### TASK 4: Sample Lease Agreement (DOCX)
**File:** `case-study/palm-bay-18-unit/04_sample_lease_unit201.docx`
**Format:** Word Document
**Phase Coverage:** Phase 3 (Tenancy & Lease Audit), Phase 5 (Legal & Title Prep)

**Content:**
- Florida Residential Lease Agreement
- Landlord: Sunshine Palms Holdings LLC
- Tenant: David & Ana Rodriguez
- Unit: 201 — 2BR/1BA, 850 sq ft
- Term: October 1, 2025 – September 30, 2026
- Monthly Rent: $1,350 (due on 1st, late after 5th, $50 late fee)
- Security Deposit: $1,350 (held per FL Statute 83.49 — specify holding method)
- Utilities: Tenant pays electric & water; Landlord pays trash, sewer, common area
- Pet Policy: No pets without written addendum ($250 pet deposit + $25/month pet rent)
- FL-specific clauses: Right to notice per 83.56, Security deposit return per 83.49(3), Mold disclosure per 404.056
- Signatures: Landlord and Tenant lines
- Notary block (not required but included)

---

### TASK 5: Title Search Summary (PDF)
**File:** `case-study/palm-bay-18-unit/05_title_search.pdf`
**Format:** PDF
**Phase Coverage:** Phase 5 (Legal & Title Prep)

**Content:**
- Title search performed by: "Brevard Title & Abstract Co."
- Property: 2750 Malabar Road SE, Palm Bay, FL 32907
- Legal Description: Lot 142, Block 5, Palm Bay Unit 37, as recorded in Plat Book 29, Page 37
- **Chain of Title (last 3 transfers):**
  1. 2018-03-15: Sunshine Palms Holdings LLC (current) — WD OR Book 8234, Page 1567
  2. 2012-06-20: Brevard Multifamily Partners LLC — WD OR Book 7122, Page 893
  3. 2003-09-10: First Florida Development Corp — WD OR Book 5890, Page 2104
- **Liens/Encumbrances Found:**
  1. Mortgage: First Southern Bank, $1,200,000 originated 2018-03-15, OR Book 8234, Page 1590 (current payoff est. $980,000)
  2. Municipal Lien: City of Palm Bay — Code enforcement lien $1,850 for landscape violation (2024), OR Book 9456, Page 334 — **MUST RESOLVE BEFORE SALE**
  3. HOA: None (not within HOA community)
- **Easements:** FPL utility easement along east boundary (standard, does not affect use)
- **Taxes:** 2025 paid current. No outstanding tax certificates.
- **Judgments:** None found against Sunshine Palms Holdings LLC
- **Recommendation:** Title insurable upon resolution of City code enforcement lien ($1,850)

---

### TASK 6: Comparative Market Analysis / Appraisal (XLSX)
**File:** `case-study/palm-bay-18-unit/06_valuation_comps.xlsx`
**Format:** Excel
**Phase Coverage:** Phase 6 (Valuation & Pricing)

**Sheet 1: "Comparable Sales"**
| # | Address | Units | Sale Date | Sale Price | Price/Unit | Cap Rate | GRM |
|---|---------|-------|-----------|------------|------------|----------|-----|
| 1 | 1520 Emerson Dr NE, Palm Bay | 12 | 2025-09 | $1,380,000 | $115,000 | 7.2% | 8.4 |
| 2 | 890 Americana Blvd, Melbourne | 20 | 2025-11 | $2,450,000 | $122,500 | 6.9% | 8.8 |
| 3 | 3200 Dixie Hwy NE, Palm Bay | 16 | 2025-06 | $1,680,000 | $105,000 | 7.5% | 7.9 |
| 4 | 445 Sarno Rd, Melbourne | 24 | 2025-08 | $3,120,000 | $130,000 | 6.5% | 9.2 |
| 5 | 2100 Palm Bay Rd NE | 14 | 2025-04 | $1,540,000 | $110,000 | 7.8% | 8.1 |

**Sheet 2: "Valuation Scenarios"**
- Income Approach: NOI / Cap Rate at 6.5%, 7.0%, 7.5%
- GRM Approach: Gross Rent × GRM at 8.0, 8.5, 9.0
- Price Per Unit: 18 × ($105K, $115K, $125K)
- **Recommended List Price: $1,950,000 ($108,333/unit, 6.88% cap on actual NOI)**
- All values as formulas

**Sheet 3: "Buyer Underwriting"**
- 3 scenarios: Conservative / Base / Aggressive
- Inputs: Purchase Price, Down Payment (25%), Interest Rate (7.25%), NOI
- Outputs: DSCR, Cash-on-Cash Return, Cap Rate, IRR (5-year hold)

---

### TASK 7: Offering Memorandum (PPTX)
**File:** `case-study/palm-bay-18-unit/07_offering_memorandum.pptx`
**Format:** PowerPoint
**Phase Coverage:** Phase 7 (Marketing Package)

**Slides:**
1. **Cover:** "Palm Bay Palms Apartments | 18-Unit Value-Add Opportunity | $1,950,000" + Property360 branding
2. **Investment Highlights:** 4 bullet points (below-market rents, CapEx done, strong demographics, 1031 eligible)
3. **Property Overview:** Address, unit mix, year built, lot size, zoning
4. **Unit Mix Table:** Type, count, SF, current rent, market rent, upside
5. **Financial Summary:** T12 NOI, Pro Forma NOI, Cap Rates
6. **Rent Comparables:** Market rent comparison table
7. **CapEx Summary:** From inspection report — what's done, what's needed
8. **Location Map:** Palm Bay demographic highlights (population, median income, growth)
9. **Pro Forma Projections:** 3-year stabilized income/expense projection
10. **Offer Terms:** Asking price, earnest money, inspection period, target close

---

### TASK 8: Letter of Intent Template (DOCX)
**File:** `case-study/palm-bay-18-unit/08_loi_template.docx`
**Format:** Word Document
**Phase Coverage:** Phase 8 (Offer & Negotiation)

**Content:**
- Standard commercial LOI format
- Buyer: "[BUYER NAME]"
- Seller: Sunshine Palms Holdings LLC
- Property: 2750 Malabar Road SE, Palm Bay, FL 32907
- Purchase Price: $________
- Earnest Money: $________ (hard after 15-day inspection)
- Inspection Period: 15 business days
- Financing Contingency: 30 days
- Closing Date: 45 days from execution
- Included: All fixtures, appliances, laundry equipment
- Excluded: Personal property of tenants
- 1031 Exchange: Buyer/Seller may structure as 1031; each cooperates
- Non-binding except confidentiality and exclusivity (30 days)
- Signature blocks for Buyer and Seller

---

### TASK 9: Due Diligence Checklist (XLSX)
**File:** `case-study/palm-bay-18-unit/09_due_diligence_tracker.xlsx`
**Format:** Excel
**Phase Coverage:** Phase 9 (Due Diligence Support)

**Columns:**
- A: DD Item
- B: Category (Financial/Legal/Physical/Environmental/Operational)
- C: Status (Pending/Requested/Received/Reviewed/Cleared)
- D: Responsible Party (Seller/Buyer/Title Co/Inspector)
- E: Date Requested
- F: Date Received
- G: Days Outstanding (formula)
- H: Notes
- I: Critical? (Yes/No)

**Items (30+ rows):**
- T12 P&L, Rent Roll, Tax Returns (2 years), Insurance Policy, Leases (all 16), Security Deposit Ledger, Utility Bills (12 months), Vendor Contracts, Property Tax Bills, Survey, Phase I Environmental, Title Commitment, Zoning Letter, Certificate of Occupancy, Building Permits, HOA docs (N/A), Estoppel Letters, Inspection Report, Appraisal, Bank Statements, Loan Payoff Letter, Entity Docs (LLC Operating Agreement, Articles), Property Management Agreement, Roof Warranty, HVAC Service Records, Fire Inspection Report, ADA Compliance, Flood Cert, Lead Paint Disclosure

**Formatting:** Conditional formatting on Status column (green=Cleared, yellow=Received, red=Pending)

---

### TASK 10: Settlement Statement / Closing Worksheet (XLSX)
**File:** `case-study/palm-bay-18-unit/10_closing_worksheet.xlsx`
**Format:** Excel
**Phase Coverage:** Phase 10 (Closing & Transition)

**Sheet 1: "Settlement Statement"**
- Buyer side and Seller side columns
- Purchase Price: $1,950,000
- Earnest Money Credit: $50,000
- Prorated Items:
  - Property taxes (prorate from Jan 1)
  - Rents collected (prorate current month)
  - Security deposits transferred: $21,500 (sum of all deposits)
  - Insurance (if assigned)
- Seller Credits:
  - Mortgage payoff: $980,000
  - Commission (5%): $97,500
  - Title insurance: $4,200
  - Code enforcement lien: $1,850
  - Documentary stamps: $13,650 (FL: $0.70 per $100)
  - Recording fees: $250
- Buyer Credits:
  - Loan origination
  - Appraisal
  - Inspection
  - Title search
  - Survey
- **Seller Net Proceeds** (formula)
- **Buyer Total Due at Closing** (formula)

**Sheet 2: "Security Deposit Transfer"**
- All 16 occupied units with deposit amounts
- Total: Sum formula
- Signed transfer acknowledgment template text

**Sheet 3: "Tenant Notification"**
- Template letter text per FL Statute 83.50
- Fields: Tenant name, unit, new owner, new rent payment address, effective date

---

### TASK 11: 3-Year Pro Forma (XLSX)
**File:** `case-study/palm-bay-18-unit/11_proforma_3yr.xlsx`
**Format:** Excel with formulas
**Phase Coverage:** Phase 4 (Income Optimization), Phase 7 (Marketing Package)

**Assumptions (separate cells, blue text):**
- Rent growth: 3% annually
- Expense growth: 2% annually
- Vacancy stabilization: 11.1% → 5% by Year 2
- CapEx: $87,300 in Year 1, $10,000/yr thereafter
- Management fee: 8%

**Year 1 / Year 2 / Year 3 columns, all formulas referencing assumptions**

---

### TASK 12: Entity Documentation Summary (DOCX)
**File:** `case-study/palm-bay-18-unit/12_entity_summary.docx`
**Format:** Word Document
**Phase Coverage:** Phase 5 (Legal & Title Prep)

**Content:**
- Entity: Sunshine Palms Holdings LLC
- State: Florida
- Document Number: L18000045678
- Filing Date: February 1, 2018
- Registered Agent: Mariam Shapira, 123 Ocean Ave, Satellite Beach, FL 32937
- Members: Mariam Shapira (100% — Managing Member)
- Status: Active
- Annual Report: Filed current through 2026
- EIN: 82-XXXXXXX
- Operating Agreement Summary: Single-member LLC, full authority to sell without additional consent

---

## 🗄️ SUPABASE SEED DATA

After creating all files, insert into Supabase tables:

### Insert Property
```sql
INSERT INTO p360_properties (
  id, user_id, address, city, state, zip, parcel_id,
  property_type, beds, baths, sqft, year_built, lot_size_sqft,
  estimated_value, mortgage_payoff, monthly_rent, occupancy_status, notes, metadata
) VALUES (
  'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
  -- user_id: use the first user in p360_profiles, or create a test user
  (SELECT id FROM p360_profiles LIMIT 1),
  '2750 Malabar Road SE', 'Palm Bay', 'FL', '32907',
  '29-37-05-00-00142.0-0000',
  'multi_family', 38, 22, 14400, 1986, 52272,
  1950000.00, 980000.00, 20900.00, 'partial',
  '18-unit case study for system validation',
  '{"units": 18, "unit_mix": "6x1BR+8x2BR+4x3BR", "case_study": true}'
);
```

### Insert Documents (after uploading files)
For each of the 12 files, insert a row into `p360_documents` with:
- property_id: the UUID above
- filename: e.g., "01_rent_roll_2025.xlsx"
- file_type: "xlsx", "pdf", "docx", "pptx"
- status: "uploaded"
- doc_type: e.g., "rent_roll", "inspection", "lease", "title_search", "appraisal", "om", "loi", "dd_tracker", "closing", "proforma", "entity_docs", "pnl"

---

## ✅ VALIDATION CHECKLIST

After all 12 documents are created and pushed:

### File Integrity
- [ ] All 12 files exist in `case-study/palm-bay-18-unit/`
- [ ] XLSX files open without errors and formulas calculate
- [ ] PDF files render correctly with all pages
- [ ] DOCX files open with proper formatting
- [ ] PPTX has all 10 slides

### Data Consistency
- [ ] Rent roll totals match P&L income
- [ ] CapEx in inspection report matches pro forma Year 1
- [ ] Security deposits in rent roll match closing worksheet
- [ ] NOI in P&L matches valuation comps input
- [ ] Mortgage payoff consistent across all documents
- [ ] All 18 units accounted for in every relevant document
- [ ] FL statute references are correct (83.49, 83.50, 83.56)

### Phase Coverage Matrix
| Phase | Doc(s) | Checklist Items Targeted |
|-------|--------|------------------------|
| 1. Financial Assessment | 02_pnl, 11_proforma | 1-1, 1-2, 1-3, 1-6 |
| 2. Property Condition | 03_inspection | 2-1, 2-2, 2-4, 2-5, 2-6 |
| 3. Tenancy & Lease Audit | 01_rent_roll, 04_lease | 3-1, 3-2, 3-3, 3-4, 3-5, 3-6 |
| 4. Income Optimization | 02_pnl, 11_proforma | 4-1, 4-2, 4-4, 4-5, 4-6 |
| 5. Legal & Title Prep | 05_title, 04_lease, 12_entity | 5-1, 5-2, 5-3, 5-4, 5-5 |
| 6. Valuation & Pricing | 06_comps | 6-1, 6-2, 6-3, 6-4, 6-5, 6-6 |
| 7. Marketing Package | 07_om, 11_proforma | 7-1, 7-2, 7-3 |
| 8. Offer & Negotiation | 08_loi | 8-1, 8-2, 8-3, 8-4, 8-5, 8-6 |
| 9. Due Diligence | 09_dd_tracker | 9-1, 9-2, 9-4 |
| 10. Closing & Transition | 10_closing | 10-1, 10-2, 10-3, 10-4, 10-5 |

### AI Document Intelligence Test
After documents are in the system:
- [ ] Upload rent roll → Phase 3 items auto-checked
- [ ] Upload P&L → Phase 1 + 4 items auto-checked
- [ ] Upload inspection → Phase 2 items auto-checked
- [ ] Upload lease → Phase 3 + 5 items auto-checked
- [ ] Upload title search → Phase 5 items auto-checked
- [ ] Upload all docs → cross-tab sync works
- [ ] Insights tab shows confidence matrix
- [ ] Missing evidence section shows uncovered critical items

---

## 📁 EXPECTED OUTPUT

```
case-study/palm-bay-18-unit/
├── 01_rent_roll_2025.xlsx          (Phase 3)
├── 02_profit_loss_T12.pdf          (Phase 1, 4)
├── 03_inspection_report.pdf        (Phase 2)
├── 04_sample_lease_unit201.docx    (Phase 3, 5)
├── 05_title_search.pdf             (Phase 5)
├── 06_valuation_comps.xlsx         (Phase 6)
├── 07_offering_memorandum.pptx     (Phase 7)
├── 08_loi_template.docx            (Phase 8)
├── 09_due_diligence_tracker.xlsx   (Phase 9)
├── 10_closing_worksheet.xlsx       (Phase 10)
├── 11_proforma_3yr.xlsx            (Phase 4, 7)
├── 12_entity_summary.docx          (Phase 5)
└── README.md                       (This case study overview)
```

## GIT COMMIT FORMAT
```
feat(prd-p360-002): Create [document name] for case study validation
```

## ESCALATION
If blocked after 3 attempts: log to Supabase insights, create GitHub Issue, move to next task.
