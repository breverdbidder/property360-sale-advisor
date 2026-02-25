# TODO.md — Property360 AI Document Intelligence Engine
# PRD-P360-001 | Sprint: Feb 26 – Mar 5, 2026
# PROTOCOL: Load this file. Find first [ ] task. Execute. Mark [x]. Push.

## PHASE 0 — FOUNDATION AUDIT
- [ ] 0.1 Pull latest main, run tsc --noEmit, document any existing type errors
- [ ] 0.2 Run dev server, verify all 3 tabs render (checklist, documents, insights)
- [ ] 0.3 Test /api/analyze with sample payload via curl, verify Claude responds
- [ ] 0.4 Document current state in PR comment before any changes

## PHASE 1 — PARSER COMPLETENESS
- [ ] 1.1 Add JSZip: npm install jszip --legacy-peer-deps, update package.json
- [ ] 1.2 Add SheetJS: npm install xlsx --legacy-peer-deps, update package.json
- [ ] 1.3 Implement PPTX parser: unzip .pptx with JSZip → extract ppt/slides/*.xml → strip XML tags → concat slide text
- [ ] 1.4 Implement XLSX real parser: SheetJS XLSX.read() → iterate sheets → XLSX.utils.sheet_to_csv() → concat
- [ ] 1.5 Detect rent roll pattern (Unit/Tenant/Rent columns) → emit structured summary for AI
- [ ] 1.6 Test all 4 file types: PDF + DOCX + XLSX + PPTX → each returns non-empty content string

## PHASE 2 — AUTO-APPLY ENGINE
- [ ] 2.1 Add aiSources: Map<itemId, {docName, confidence, extractedValue, docId}> to component state
- [ ] 2.2 applyAnalysis(docId) function: merge completedItems into checked Set AND aiSources Map
- [ ] 2.3 PhaseCard item render: show AI badge if aiSources.has(item.id) → "Lease 87%"
- [ ] 2.4 Badge design: small pill, source doc abbreviation + confidence %, tooltip with extractedValue
- [ ] 2.5 Allow manual uncheck of AI-applied items → sets manualOverrides Set, badge shows strikethrough
- [ ] 2.6 Multi-doc merge: if two docs apply same item, higher confidence source wins in badge

## PHASE 3 — CROSS-TAB SYNC
- [ ] 3.1 Audit state hoisting — ALL state must live in SaleAdvisor parent, never in tabs
- [ ] 3.2 Tab switching must NOT reset any state (no local state in tab components)
- [ ] 3.3 Documents tab: show which phases each document unlocked (phase badge list per doc)
- [ ] 3.4 Checklist tab: show AI-source indicator (doc icon) per auto-applied item
- [ ] 3.5 Insights tab: aggregate all findings + warnings + multi-doc cross-reference
- [ ] 3.6 Live tab badge counts: Checklist shows completed count, Documents shows doc count

## PHASE 4 — INSIGHTS TAB COMPLETION
- [ ] 4.1 Confidence matrix table: Phase (rows) vs Document (cols) → coverage % per cell
- [ ] 4.2 Aggregated key findings list (deduplicated across all uploaded docs)
- [ ] 4.3 Warnings list with source document reference and severity
- [ ] 4.4 Items confirmed by 2+ docs → highlight as HIGH CONFIDENCE with green border
- [ ] 4.5 Missing evidence section: critical items (critical:true) with zero doc support listed prominently

## PHASE 5 — URL STATE SHARING
- [ ] 5.1 serializeState(): {checked, aiSources} → JSON.stringify → btoa → window.location.hash
- [ ] 5.2 deserializeState(): window.location.hash → atob → JSON.parse → setState calls
- [ ] 5.3 useEffect on mount: if hash present → deserializeState()
- [ ] 5.4 Share button in header: navigator.clipboard.writeText(window.location.href) + toast
- [ ] 5.5 Test: 60 checked items → URL under 4000 chars (use LZ compression if needed: lz-string)

## PHASE 6 — ERROR STATES & API KEY UX
- [ ] 6.1 Detect missing API key: 500 with "not configured" → show setup card in Documents tab
- [ ] 6.2 Setup card text: "AI analysis unavailable. Set ANTHROPIC_API_KEY in Cloudflare Pages > Settings > Environment Variables"
- [ ] 6.3 Rate limit: 429 → "AI busy, retrying in 60s" with visible countdown
- [ ] 6.4 File too large: >10MB → show error before attempting parse
- [ ] 6.5 Unsupported format: show "Supported: PDF, DOCX, XLSX, PPTX" tooltip on upload zone

## PHASE 7 — QUALITY GATES (ALL MUST PASS)
- [ ] 7.1 npx tsc --noEmit → MUST return 0 errors
- [ ] 7.2 npx @cloudflare/next-on-pages → MUST build successfully
- [ ] 7.3 Upload PDF inspection report → Phase 2 items auto-checked
- [ ] 7.4 Upload XLSX rent roll → Phase 3 items auto-checked
- [ ] 7.5 Upload DOCX lease agreement → Phase 3 + 5 items auto-checked
- [ ] 7.6 Upload PPTX → any relevant items extracted and returned
- [ ] 7.7 Share URL → paste in new tab → identical checklist state restored

## PHASE 8 — DEPLOY & RELEASE
- [ ] 8.1 Commit all with descriptive message referencing PRD-P360-001
- [ ] 8.2 Push to main → verify CF Pages auto-deploys
- [ ] 8.3 Verify property360-sale-advisor.pages.dev HTTP 200
- [ ] 8.4 Mark all completed items [x] in this file and push final state
- [ ] 8.5 Create GitHub Release v1.1.0 with tag "ai-document-intelligence"


## CASE STUDY - PRD-P360-002 (Claude Code Task)
- [ ] CS.1 Create 01_rent_roll_2025.xlsx
- [ ] CS.2 Create 02_profit_loss_T12.pdf
- [ ] CS.3 Create 03_inspection_report.pdf
- [ ] CS.4 Create 04_sample_lease_unit201.docx
- [ ] CS.5 Create 05_title_search.pdf
- [ ] CS.6 Create 06_valuation_comps.xlsx
- [ ] CS.7 Create 07_offering_memorandum.pptx
- [ ] CS.8 Create 08_loi_template.docx
- [ ] CS.9 Create 09_due_diligence_tracker.xlsx
- [ ] CS.10 Create 10_closing_worksheet.xlsx
- [ ] CS.11 Create 11_proforma_3yr.xlsx
- [ ] CS.12 Create 12_entity_summary.docx
- [ ] CS.13 Push all to case-study/palm-bay-18-unit/
- [ ] CS.14 Insert property + documents to Supabase
- [ ] CS.15 Validate data consistency across all docs
- [ ] CS.16 Test AI Document Intelligence Engine
