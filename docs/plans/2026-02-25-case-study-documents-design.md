# PRD-P360-002: Case Study Document Generation — Design

**Date:** 2026-02-25
**Status:** Approved
**Scope:** Generate 12 synthetic documents for an 18-unit multifamily property case study, push to GitHub, seed Supabase via GitHub Action.

## Context

Property360 Sale Advisor needs realistic test data to validate its AI Document Intelligence Engine across all 10 phases of the income property sale checklist. This design covers generating 12 document files representing a hypothetical 18-unit multifamily in Palm Bay, FL.

## Architecture

### Document Generation
- **Runtime:** Python 3.13.7 with openpyxl, reportlab, python-docx, python-pptx
- **Strategy:** Single master data module with all property/unit/financial data; individual generator scripts per document type
- **Output:** `case-study/palm-bay-18-unit/` in the repo

### Data Consistency
All documents derive from a shared data source:
- Unit data (18 units with tenant, rent, lease info)
- Financial data (income, expenses, NOI — single source of truth)
- CapEx data (from inspection, flows to pro forma and OM)
- Security deposits (rent roll → closing worksheet)

### File Matrix

| # | Filename | Format | Library | Phases |
|---|----------|--------|---------|--------|
| 1 | 01_rent_roll_2025.xlsx | XLSX | openpyxl | 3 |
| 2 | 02_profit_loss_T12.pdf | PDF | reportlab | 1, 4 |
| 3 | 03_inspection_report.pdf | PDF | reportlab | 2 |
| 4 | 04_sample_lease_unit201.docx | DOCX | python-docx | 3, 5 |
| 5 | 05_title_search.pdf | PDF | reportlab | 5 |
| 6 | 06_valuation_comps.xlsx | XLSX | openpyxl | 6 |
| 7 | 07_offering_memorandum.pptx | PPTX | python-pptx | 7 |
| 8 | 08_loi_template.docx | DOCX | python-docx | 8 |
| 9 | 09_due_diligence_tracker.xlsx | XLSX | openpyxl | 9 |
| 10 | 10_closing_worksheet.xlsx | XLSX | openpyxl | 10 |
| 11 | 11_proforma_3yr.xlsx | XLSX | openpyxl | 4, 7 |
| 12 | 12_entity_summary.docx | DOCX | python-docx | 5 |

### GitHub Action for Supabase Seeding
- Workflow: `.github/workflows/seed-supabase.yml`
- Trigger: `workflow_dispatch` (manual)
- Uses `SUPABASE_SERVICE_ROLE_KEY` secret
- Inserts property row + 12 document metadata rows into `p360_properties` and `p360_documents`
- Uses service role key to bypass RLS

## Delivery
1. Install Python dependencies
2. Generate all 12 files locally
3. Git commit + push to `main`
4. Create GitHub Action workflow
5. Run validation checklist
