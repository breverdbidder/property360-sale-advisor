# CLAUDE CODE — AUTONOMOUS EXECUTION PROMPT
## Property360 Sale Advisor · AI Document Intelligence Engine
## PRD-P360-001 · All actions PRE-APPROVED by Ariel Shapira

---

## ⚡ PRE-AUTHORIZATION DECLARATION

**Ariel Shapira has pre-approved ALL of the following — zero confirmation needed:**
- All npm installs and package.json modifications
- All file creates, edits, and deletes in this repository
- All git commits and pushes to `main`
- All Cloudflare Pages deploys triggered by pushes
- All TypeScript changes, refactors, and rewrites
- Retry up to 3× on any failure before escalating
- Work through all tasks in order without stopping

**You are the engineer. Execute autonomously. Report results, not questions.**

---

## 🎯 MISSION

Complete the AI Document Intelligence Engine for `property360-sale-advisor`.

**Repo:** `github.com/breverdbidder/property360-sale-advisor`  
**Live:** `property360-sale-advisor.pages.dev`  
**Stack:** Next.js 15.5.2 · React 19 · TypeScript · Cloudflare Workers edge runtime  
**GitHub Token:** `${GITHUB_TOKEN}`  
**CF Account:** `${CF_ACCOUNT_ID}`  
**CF Token:** `${CF_API_TOKEN}`

---

## 📋 CURRENT STATE (audited Feb 25, 2026)

```
components/SaleAdvisor.tsx     615 lines — partial implementation
app/api/analyze/route.ts       COMPLETE — calls Claude, returns JSON
app/layout.tsx                 edge runtime set
app/page.tsx                   edge runtime set
lib/phases.ts                  COMPLETE — 10 phases, 60 items
```

**What exists and works:**
- 3-tab UI (checklist, documents, insights) — renders
- DropZone — drag/drop file upload — works
- PDF parsing — base64 to Claude — works
- DOCX parsing — mammoth.js — works
- `/api/analyze` — Claude Sonnet, returns completedItems — works
- applyDoc() — marks items checked — works
- InsightsTab component — partial but renders

**What is MISSING (your exact task list):**
1. PPTX parser — `extractDocContent()` has no `.pptx` branch
2. XLSX real parser — currently `FileReader.readAsText()` placeholder, not SheetJS
3. `UploadedDoc.type` only allows `"pdf" | "docx" | "xlsx"` — needs `"pptx"` added
4. `docIcon()` has no pptx case
5. DropZone accept attr missing `.pptx`
6. AI source badges — `aiSuggested` map exists but badges not shown on applied items in checklist
7. `manualOverrides` state — missing entirely (user can't uncheck AI items distinctly)
8. URL state share — missing entirely (no serialize/deserialize/share button)
9. ANTHROPIC_API_KEY missing error — no graceful UI, just crashes
10. File size guard — no 10MB check before processing

---

## 🔧 EXECUTION PROTOCOL

```
For each task below:
  1. Read the relevant file first
  2. Make the exact change described
  3. Run: npx tsc --noEmit
  4. If errors → fix them before proceeding
  5. Commit with message: "feat(prd-p360-001): [task description]"
  6. Move to next task
  7. After ALL tasks done → push once → verify CF build
```

**Never commit broken TypeScript. Never skip the tsc check.**

---

## 📦 TASK 1 — Install Dependencies

```bash
npm install jszip xlsx --legacy-peer-deps
```

Verify both installed:
```bash
node -e "require('jszip'); require('xlsx'); console.log('OK')"
```

Commit: `feat(prd-p360-001): add jszip + xlsx for PPTX/Excel parsing`

---

## 📝 TASK 2 — Update TypeScript Interfaces

In `components/SaleAdvisor.tsx`, make these exact changes:

**Change 1** — `UploadedDoc.type` union (line ~21):
```typescript
// BEFORE:
interface UploadedDoc {
  id: string; name: string; type: "pdf" | "docx" | "xlsx";

// AFTER:
interface UploadedDoc {
  id: string; name: string; type: "pdf" | "docx" | "xlsx" | "pptx";
```

**Change 2** — Add `manualOverrides` to the AISource suggestion map. Find the `aiSuggested` state and add a new state right after it:
```typescript
// Find this line (around line ~530):
const [aiSuggested, setAiSuggested] = useState<Map<string, { confidence: number; value: string | null; docName: string }>>(new Map());

// ADD this line immediately after:
const [manualOverrides, setManualOverrides] = useState<Set<string>>(new Set());
```

**Change 3** — `docIcon()` helper (line ~32):
```typescript
// BEFORE:
const docIcon = (t: string) => t === "pdf" ? "📄" : t === "docx" ? "📝" : "📊";

// AFTER:
const docIcon = (t: string) => t === "pdf" ? "📄" : t === "docx" ? "📝" : t === "pptx" ? "📊" : "📋";
```

**Change 4** — DropZone `accept` attribute. Find the `<input>` inside `DropZone` component:
```typescript
// BEFORE:
<input ref={inputRef} type="file" accept=".pdf,.docx,.xlsx,.xls" multiple ...

// AFTER:
<input ref={inputRef} type="file" accept=".pdf,.docx,.xlsx,.xls,.pptx" multiple ...
```

**Change 5** — DropZone `filter` for drag-drop. Find the `handleDrop` function:
```typescript
// BEFORE:
const files = Array.from(e.dataTransfer.files).filter(f => /\.(pdf|docx|xlsx|xls)$/i.test(f.name));

// AFTER:
const files = Array.from(e.dataTransfer.files).filter(f => /\.(pdf|docx|xlsx|xls|pptx)$/i.test(f.name));
```

**Change 6** — DropZone hint text:
```typescript
// BEFORE:
<div style={{ fontSize: 12, color: C.gray }}>PDF · DOCX · XLSX · AI will auto-fill your checklist</div>

// AFTER:
<div style={{ fontSize: 12, color: C.gray }}>PDF · DOCX · XLSX · PPTX · AI will auto-fill your checklist</div>
```

Run `npx tsc --noEmit` — fix any errors before continuing.

Commit: `feat(prd-p360-001): add pptx type, manualOverrides state, update file filters`

---

## 📝 TASK 3 — Replace extractDocContent() with Complete Parser

Find the entire `extractDocContent` function in `SaleAdvisor.tsx` (starts around line ~36, ends before `// ─── TOAST STACK`).

**Replace the entire function** with this exact implementation:

```typescript
async function extractDocContent(file: File): Promise<string> {
  const ext = file.name.split(".").pop()?.toLowerCase() || "";

  // ── PPTX ──────────────────────────────────────────────────────────────────
  if (ext === "pptx") {
    try {
      const JSZip = (await import("jszip")).default;
      const buf = await file.arrayBuffer();
      const zip = await JSZip.loadAsync(buf);
      const slideFiles = Object.keys(zip.files)
        .filter(f => /^ppt\/slides\/slide\d+\.xml$/.test(f))
        .sort((a, b) => {
          const na = parseInt(a.match(/\d+/)?.[0] || "0");
          const nb = parseInt(b.match(/\d+/)?.[0] || "0");
          return na - nb;
        });
      const texts: string[] = [];
      for (const sf of slideFiles) {
        const xml = await zip.files[sf].async("text");
        // Extract text from <a:t> tags (DrawingML text runs)
        const matches = xml.match(/<a:t[^>]*>([^<]*)<\/a:t>/g) || [];
        const slideText = matches
          .map(m => m.replace(/<[^>]+>/g, "").trim())
          .filter(t => t.length > 0)
          .join(" ");
        if (slideText.length > 5) texts.push(`[Slide ${texts.length + 1}] ${slideText}`);
      }
      if (texts.length === 0) return `[PowerPoint: ${file.name} — no text extracted]`;
      return `[PowerPoint: ${file.name} — ${texts.length} slides]\n\n${texts.join("\n\n").slice(0, 12000)}`;
    } catch (err) {
      const msg = err instanceof Error ? err.message : "parse error";
      return `[PPTX parse failed: ${file.name} — ${msg}]`;
    }
  }

  // ── XLSX / XLS ─────────────────────────────────────────────────────────────
  if (ext === "xlsx" || ext === "xls") {
    try {
      const XLSX = await import("xlsx");
      const buf = await file.arrayBuffer();
      const wb = XLSX.read(buf, { type: "array" });
      const parts: string[] = [`[Excel: ${file.name} — ${wb.SheetNames.length} sheet(s)]`];

      for (const sheetName of wb.SheetNames) {
        const ws = wb.Sheets[sheetName];
        if (!ws || !ws["!ref"]) continue;

        // Try to detect rent roll pattern
        const headers: string[] = [];
        const range = XLSX.utils.decode_range(ws["!ref"]!);
        for (let C2 = range.s.c; C2 <= Math.min(range.e.c, 15); C2++) {
          const cell = ws[XLSX.utils.encode_cell({ r: range.s.r, c: C2 })];
          if (cell?.v) headers.push(String(cell.v).toLowerCase());
        }
        const isRentRoll = headers.some(h => h.includes("unit") || h.includes("tenant") || h.includes("rent") || h.includes("lease"));

        const csv = XLSX.utils.sheet_to_csv(ws);
        if (csv.trim().length < 3) continue;

        if (isRentRoll) {
          parts.push(`Sheet "${sheetName}" [RENT ROLL DETECTED — columns: ${headers.slice(0,8).join(", ")}]\n${csv.slice(0, 4000)}`);
        } else {
          parts.push(`Sheet "${sheetName}"\n${csv.slice(0, 3000)}`);
        }
      }
      return parts.join("\n\n---\n\n").slice(0, 12000);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "parse error";
      return `[Excel parse failed: ${file.name} — ${msg}]`;
    }
  }

  // ── DOCX ───────────────────────────────────────────────────────────────────
  if (ext === "docx") {
    try {
      const mammoth = await import("mammoth");
      const buf = await file.arrayBuffer();
      const res = await mammoth.extractRawText({ arrayBuffer: buf });
      if (!res.value || res.value.trim().length < 10) return `[DOCX: ${file.name} — no text extracted]`;
      return res.value.slice(0, 12000);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "parse error";
      return `[DOCX parse failed: ${file.name} — ${msg}]`;
    }
  }

  // ── PDF — send as base64 for Claude vision ─────────────────────────────────
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target?.result as string;
      const b64 = dataUrl?.split(",")[1] || "";
      if (!b64) { resolve(`[PDF: ${file.name} — could not read]`); return; }
      // Claude handles up to ~50 pages; truncate base64 at ~4MB raw
      resolve(`__PDF_BASE64__:${b64.slice(0, 4_000_000)}`);
    };
    reader.onerror = () => reject(new Error("FileReader failed"));
    reader.readAsDataURL(file);
  });
}
```

Run `npx tsc --noEmit`. Fix any type errors.

Commit: `feat(prd-p360-001): complete PPTX + XLSX parsers in extractDocContent`

---

## 📝 TASK 4 — Add File Size Guard

In the `processFile` function, add a size check **before** calling `extractDocContent`. Find this block:

```typescript
const processFile = useCallback(async (file: File) => {
  const ext = file.name.split(".").pop()?.toLowerCase() || "";
```

Add immediately after the `ext` line:

```typescript
  // File size guard — 10MB max
  if (file.size > 10 * 1024 * 1024) {
    addToast(`❌ ${file.name} exceeds 10MB limit (${fmtSize(file.size)})`, "error");
    return;
  }
```

Commit: `feat(prd-p360-001): add 10MB file size guard`

---

## 📝 TASK 5 — Add ANTHROPIC_API_KEY Error Handling

In `processFile`, find the error handling block inside the `try` block after the fetch:

```typescript
const data = await res.json();
if (!data.success) throw new Error(data.error || "Analysis failed");
```

Replace with:

```typescript
const data = await res.json();
if (!data.success) {
  const errMsg = data.error || "Analysis failed";
  // Check for API key configuration error
  if (errMsg.includes("not configured") || errMsg.includes("ANTHROPIC_API_KEY")) {
    throw new Error("AI analysis unavailable — ANTHROPIC_API_KEY not set in Cloudflare Pages environment variables");
  }
  if (errMsg.includes("429") || errMsg.includes("rate limit")) {
    throw new Error("AI rate limit reached — please wait 60 seconds and retry");
  }
  throw new Error(errMsg);
}
```

Commit: `feat(prd-p360-001): graceful ANTHROPIC_API_KEY and rate limit error handling`

---

## 📝 TASK 6 — AI Source Badges on Applied Items

The current `applyDoc` applies items but loses the attribution (which doc applied which item). Fix this:

**Step 6a** — In `applyDoc`, also update `aiSuggested` to store attribution even after applying:

Find the `applyDoc` function. Currently it does `setAiSuggested(prev => { const n = new Map(prev); doc.analysis!.completedItems.forEach(ci => n.delete(ci.id)); return n; });`

**Replace the entire `applyDoc` function** with:

```typescript
const applyDoc = useCallback((docId: string) => {
  const doc = docs.find(d => d.id === docId);
  if (!doc?.analysis) return;

  setChecked(prev => {
    const n = new Set(prev);
    doc.analysis!.completedItems.forEach(ci => {
      if (!manualOverrides.has(ci.id)) n.add(ci.id);
    });
    return n;
  });

  // Store AI attribution so badges show in checklist after apply
  setAiSuggested(prev => {
    const n = new Map(prev);
    doc.analysis!.completedItems.forEach(ci => {
      if (!manualOverrides.has(ci.id)) {
        const existing = n.get(ci.id);
        // Higher confidence wins
        if (!existing || ci.confidence > existing.confidence) {
          n.set(ci.id, {
            confidence: ci.confidence,
            value: ci.extractedValue,
            docName: doc.name.length > 20 ? doc.name.slice(0, 18) + "…" : doc.name,
          });
        }
      }
    });
    return n;
  });

  setExtractedValues(prev => {
    const n = new Map(prev);
    doc.analysis!.completedItems.forEach(ci => {
      if (ci.extractedValue && !manualOverrides.has(ci.id)) n.set(ci.id, ci.extractedValue);
    });
    return n;
  });

  setDocs(prev => prev.map(d => d.id === docId ? { ...d, applied: true } : d));
  addToast(`✅ Applied ${doc.analysis.completedItems.length} items from ${doc.name.slice(0, 25)}`, "success");
}, [docs, manualOverrides, addToast]);
```

**Step 6b** — Update `toggle` to track manual overrides:

Find `const toggle = useCallback((id: string) => {` and replace with:

```typescript
const toggle = useCallback((id: string) => {
  setChecked(prev => {
    const n = new Set(prev);
    if (n.has(id)) {
      n.delete(id);
      // If this was AI-applied, mark as manual override so reapply doesn't re-check it
      if (aiSuggested.has(id)) {
        setManualOverrides(mo => new Set([...mo, id]));
      }
    } else {
      n.add(id);
      // User manually checked — remove from overrides
      setManualOverrides(mo => { const nm = new Set(mo); nm.delete(id); return nm; });
    }
    return n;
  });
}, [aiSuggested]);
```

**Step 6c** — Show AI badge on CHECKED items in `PhaseCard`. Find the item render inside `PhaseCard` — the label with the checkbox. After the `{item.text}` text render, find where `isSuggested` badge shows and ADD a badge for already-checked AI items:

Find this block in `PhaseCard`:
```typescript
{isSuggested && (
  <div style={{ marginTop: 4, padding: "4px 8px", background: "rgba(13,71,161,0.06)", ...
```

Add this block **after** the `isSuggested` block and **after** the `extracted` block:

```typescript
{isChecked && aiSuggested.has(item.id) && (
  <div style={{ display: "inline-flex", alignItems: "center", gap: 4, marginTop: 3 }}>
    <span style={{
      fontSize: 10, padding: "1px 7px", borderRadius: 10,
      background: "#DBEAFE", color: "#1D4ED8", fontWeight: 700,
      border: "1px solid #BFDBFE", whiteSpace: "nowrap",
      title: aiSuggested.get(item.id)!.value || "AI detected",
    }}>
      🤖 {aiSuggested.get(item.id)!.docName} · {Math.round(aiSuggested.get(item.id)!.confidence * 100)}%
    </span>
  </div>
)}
```

Run `npx tsc --noEmit`. Fix any errors.

Commit: `feat(prd-p360-001): AI source badges on applied items, manualOverrides tracking`

---

## 📝 TASK 7 — URL State Sharing

Add serialize/deserialize state to URL hash and a Share button in the header.

**Step 7a** — Add `useEffect` import. Find the imports line at top of file:

```typescript
// BEFORE:
import { useState, useCallback, useRef } from "react";

// AFTER:
import { useState, useCallback, useRef, useEffect } from "react";
```

**Step 7b** — Add these utility functions **before** the `export default function SaleAdvisor()` line:

```typescript
// ─── URL STATE ────────────────────────────────────────────────────────────────
function serializeState(
  checked: Set<string>,
  aiSuggested: Map<string, { confidence: number; value: string | null; docName: string }>
): string {
  try {
    const data = {
      c: Array.from(checked),
      a: Object.fromEntries(
        Array.from(aiSuggested.entries()).map(([k, v]) => [k, [v.confidence, v.value, v.docName]])
      ),
    };
    return btoa(encodeURIComponent(JSON.stringify(data)));
  } catch { return ""; }
}

function deserializeState(hash: string): {
  checked: Set<string>;
  aiSuggested: Map<string, { confidence: number; value: string | null; docName: string }>;
} | null {
  try {
    const raw = decodeURIComponent(atob(hash));
    const data = JSON.parse(raw) as {
      c?: string[];
      a?: Record<string, [number, string | null, string]>;
    };
    const checked = new Set<string>(data.c || []);
    const aiSuggested = new Map<string, { confidence: number; value: string | null; docName: string }>();
    for (const [k, v] of Object.entries(data.a || {})) {
      aiSuggested.set(k, { confidence: v[0], value: v[1], docName: v[2] });
    }
    return { checked, aiSuggested };
  } catch { return null; }
}
```

**Step 7c** — Inside `SaleAdvisor()`, after all the `useState` declarations, add:

```typescript
  // Restore state from URL hash on mount
  useEffect(() => {
    const hash = window.location.hash.slice(1);
    if (hash.length > 10) {
      const restored = deserializeState(hash);
      if (restored) {
        setChecked(restored.checked);
        setAiSuggested(restored.aiSuggested);
        addToast(`🔗 Restored ${restored.checked.size} items from shared link`, "success");
      }
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
```

**Step 7d** — Add a `handleShare` function inside `SaleAdvisor()`, after `applyAll`:

```typescript
  const handleShare = useCallback(() => {
    const hash = serializeState(checked, aiSuggested);
    if (!hash) { addToast("Nothing to share yet — check some items first", "warning"); return; }
    const url = `${window.location.origin}${window.location.pathname}#${hash}`;
    navigator.clipboard.writeText(url).then(() => {
      addToast(`🔗 Link copied! ${checked.size} items + ${aiSuggested.size} AI sources`, "success");
    }).catch(() => {
      // Fallback for browsers without clipboard API
      window.location.hash = hash;
      addToast("🔗 URL updated with current state — copy from address bar", "info");
    });
  }, [checked, aiSuggested, addToast]);
```

**Step 7e** — Add Share button in the header. Find the Reset button in the JSX:

```typescript
// BEFORE (the Reset button):
<button onClick={() => { if (confirm("Reset everything?")) { setChecked(new Set()); ...

// ADD Share button BEFORE the Reset button:
<button onClick={handleShare}
  style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.3)", color: "white", padding: "6px 13px", borderRadius: 8, cursor: "pointer", fontSize: 12, marginRight: 6 }}>
  🔗 Share
</button>
```

Run `npx tsc --noEmit`. Fix any errors.

Commit: `feat(prd-p360-001): URL state sharing with Share button`

---

## 📝 TASK 8 — Update /api/analyze System Prompt

Open `app/api/analyze/route.ts`. Find the `systemPrompt` constant. **Replace the entire string** with this improved version:

```typescript
const systemPrompt = `You are a real estate transaction analyst specializing in Florida income property sales.
You analyze documents for Brevard County, FL property transactions managed by Property360.

DOCUMENT TYPES YOU WILL SEE AND HOW TO HANDLE EACH:
- Lease Agreement: extract tenant names, unit IDs, rent amounts, lease start/end dates, security deposit amounts, renewal options
- Inspection Report: extract deferred maintenance items, HVAC/roof/plumbing condition scores, permit status, estimated repair costs
- Rent Roll (Excel/CSV): extract unit count, occupancy rate, total monthly rent, below-market units, vacancy, lease expiration dates
- Appraisal Report: extract ARV/appraised value, cap rate, NOI, comparable sales, GRM
- Title Search: extract lien count, judgment amounts, easements, tax certificate status, encumbrances
- Financial Statement/P&L: extract NOI, gross rent, expense ratio, utility billing, ancillary income streams
- Settlement Statement (HUD-1/ALTA): extract closing costs, proration amounts, security deposit transfer, net proceeds
- Tax Certificate: extract certificate number, amount, year, interest rate, redemption status
- PowerPoint Presentation: extract any property data, financial projections, market analysis

CHECKLIST ITEMS PROVIDED: Use the item IDs exactly as given. Only mark items where the document provides clear evidence.

RESPOND WITH ONLY VALID JSON — no markdown fences, no explanation outside JSON:
{
  "docType": "exact document type (e.g. Lease Agreement, Rent Roll, Inspection Report)",
  "summary": "2-3 sentences: what this document is, what property it covers, what it proves for the sale",
  "completedItems": [
    { "id": "3-1", "confidence": 0.91, "extractedValue": "specific value found, e.g. $2,450/mo, expires Dec 2026" }
  ],
  "keyFindings": [
    "Specific actionable finding relevant to the sale preparation"
  ],
  "warnings": [
    "Issues affecting the sale, e.g. lease expires in 45 days, lien of $12,500 on title"
  ]
}

CONFIDENCE RULES:
- 0.90-1.00: document explicitly states this item is complete with specific data
- 0.75-0.89: document strongly implies completion, specific data extractable
- 0.65-0.74: document provides partial evidence, reasonable inference
- Below 0.65: DO NOT INCLUDE — too uncertain

FLORIDA-SPECIFIC FLAGS:
- FL Statute 83.49: security deposit must be in separate account — flag if unclear
- FL Statute 83.50: written notice of ownership change required at closing — always flag this reminder
- Tax certificates: redemption within 2 years or foreclosure proceeds — flag outstanding certs
- Lease expiration within 90 days of projected close: flag as urgent

extractedValue: always include specific data found (dollar amounts, dates, names, percentages) or null if not found.
keyFindings: 2-5 items max, each must be actionable, no generic statements.
warnings: only include real issues found in this specific document.`;
```

Commit: `feat(prd-p360-001): enhanced system prompt with FL-specific context and document type handling`

---

## 📝 TASK 9 — Update package.json for PPTX type hint

In `package.json`, verify `jszip` and `xlsx` appear in dependencies. If they're in `devDependencies`, move them to `dependencies` since they're used client-side at runtime:

```json
"dependencies": {
  "jszip": "^3.10.1",
  "next": "^15.5.2",
  "react": "^19.0.0",
  "react-dom": "^19.0.0",
  "xlsx": "^0.18.5"
},
```

Commit: `chore(prd-p360-001): move jszip + xlsx to dependencies (runtime client-side usage)`

---

## ✅ TASK 10 — Quality Gates

Run ALL of these. Fix any failure before pushing:

```bash
# Gate 1: TypeScript — must be zero errors
npx tsc --noEmit

# Gate 2: Cloudflare build — must succeed
npx @cloudflare/next-on-pages

# Gate 3: Verify file exists
ls -la .vercel/output/static/ | head -5
```

If Gate 2 fails:
- Check error for Node.js API usage (`fs`, `path`, `Buffer`, `crypto`)
- If `jszip` or `xlsx` use Node APIs, they must be dynamic imports (`await import(...)`) inside client components only — never in edge route files
- The `extractDocContent` function is in the client component (`"use client"`), so dynamic imports are safe there

---

## 🚀 TASK 11 — Commit All, Push, Verify Deploy

```bash
# Final commit with everything
git add -A
git commit -m "feat(prd-p360-001): AI Document Intelligence Engine complete

- PPTX parser: JSZip slide text extraction
- XLSX real parser: SheetJS with rent roll detection  
- AI source badges on applied items in checklist
- manualOverrides: user can uncheck AI items distinctly
- URL state sharing: serialize/deserialize + Share button
- ANTHROPIC_API_KEY graceful error + rate limit handling
- 10MB file size guard
- Enhanced system prompt with FL-specific context
- All 4 file formats: PDF + DOCX + XLSX + PPTX

PRD-P360-001 | property360-sale-advisor.pages.dev"

git push origin main
```

Then poll until deploy succeeds:
```bash
# Use CF API to check build status
CF_TOKEN="${CF_API_TOKEN}"
ACCOUNT_ID="${CF_ACCOUNT_ID}"

for i in $(seq 1 20); do
  sleep 25
  STATUS=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
    "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/property360-sale-advisor/deployments" \
    | python3 -c "
import json,sys
d=json.load(sys.stdin)
dep=d.get('result',[{}])[0]
stage=dep.get('latest_stage',{})
print(stage.get('name'), '-', stage.get('status'))
")
  echo "[$i] $STATUS"
  if echo "$STATUS" | grep -q "success\|failure"; then break; fi
done
```

If failure, read logs:
```bash
DEP_ID=$(curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/property360-sale-advisor/deployments" \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['result'][0]['id'])")

curl -s -H "Authorization: Bearer $CF_TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/pages/projects/property360-sale-advisor/deployments/$DEP_ID/history/logs" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
for l in d.get('result',{}).get('data',[])[-50:]:
    print(l.get('line',''))
"
```

Fix any CF-specific errors (usually Node.js API usage in edge context) and push again.

---

## 📝 TASK 12 — Verify Live

```bash
# HTTP check
curl -s -o /dev/null -w "%{http_code}" https://property360-sale-advisor.pages.dev

# Should return: 200
```

---

## 📝 TASK 13 — Create GitHub Release

```bash
TOKEN="${GITHUB_TOKEN}"

curl -s -X POST \
  "https://api.github.com/repos/breverdbidder/property360-sale-advisor/releases" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_name": "v1.1.0",
    "name": "v1.1.0 — AI Document Intelligence Engine",
    "body": "## PRD-P360-001 Complete\n\n### New Features\n- **PPTX Support**: PowerPoint slide text extraction via JSZip\n- **XLSX Real Parsing**: SheetJS with rent roll auto-detection\n- **AI Source Badges**: Per-item attribution showing doc name + confidence %\n- **Manual Overrides**: User can uncheck AI-applied items distinctly\n- **URL State Sharing**: Full session state in URL hash, Share button in header\n- **Error Handling**: Graceful ANTHROPIC_API_KEY missing UI + rate limit countdown\n- **File Size Guard**: 10MB limit enforced before processing\n- **Enhanced AI Prompts**: FL-specific context (83.49, 83.50 statutes)\n\n### All 4 formats supported\nPDF · DOCX · XLSX · PPTX → AI analysis → auto-fill 10-phase checklist\n\n**Live:** https://property360-sale-advisor.pages.dev",
    "draft": false,
    "prerelease": false
  }' | python3 -c "import json,sys; d=json.load(sys.stdin); print('Release:', d.get('name'), '|', d.get('html_url','ERROR'))"
```

---

## 🛑 ESCALATION PROTOCOL (only if truly blocked)

After 3 attempts on any single task:

```bash
TOKEN="${GITHUB_TOKEN}"

curl -s -X POST \
  "https://api.github.com/repos/breverdbidder/property360-sale-advisor/issues" \
  -H "Authorization: token $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"BLOCKED: [describe task that failed]\",
    \"body\": \"## Task\\n[task number and description]\\n\\n## Attempts\\n1. [what tried]\\n2. [what tried]\\n3. [what tried]\\n\\n## Error\\n[exact error]\\n\\n## Recommendation\\n[what should be done]\",
    \"labels\": [\"blocked\", \"prd-p360-001\"]
  }"
```

Then **skip that task**, move to the next one, and continue. Do NOT stop the session.

---

## 📊 KNOWN EDGE CASES

### jszip/xlsx with Cloudflare Workers
Both `jszip` and `xlsx` are browser-compatible but may have edge cases with CF Workers:
- Use `await import("jszip")` — dynamic import ensures it's loaded client-side
- Use `await import("xlsx")` — same pattern
- If CF build fails with these: move the imports to be lazily loaded only in the browser check:
  ```typescript
  if (typeof window === "undefined") return `[${ext.toUpperCase()}: ${file.name}]`;
  ```

### XLSX package size
SheetJS `xlsx` is ~1MB. If CF Pages bundle limit is hit:
- Use `xlsx/dist/xlsx.mini.min.js` which is ~300KB: `const XLSX = await import("xlsx/dist/xlsx.mini.min.js")`

### btoa/atob with Unicode
If state contains non-ASCII (unlikely but possible in extracted values):
```typescript
// Safe encode
btoa(unescape(encodeURIComponent(JSON.stringify(data))))
// Safe decode
JSON.parse(decodeURIComponent(escape(atob(hash))))
```
The implementation above already uses `btoa(encodeURIComponent(...))` for safety.

---

## 🔑 ENV VAR REMINDER

`ANTHROPIC_API_KEY` must be set in Cloudflare Pages:
- Dashboard: dash.cloudflare.com → Pages → property360-sale-advisor → Settings → Environment Variables
- This is the only thing Claude Code cannot set — Ariel must do this manually
- Without it, the app runs but AI analysis returns "AI analysis unavailable" error card

---

## ✅ DEFINITION OF DONE

All of these must be true:

| Check | Criteria |
|-------|----------|
| TypeScript | `npx tsc --noEmit` → 0 errors |
| CF Build | `npx @cloudflare/next-on-pages` → success |
| Live | `https://property360-sale-advisor.pages.dev` → HTTP 200 |
| PDF | Upload any PDF → analysis JSON returned → items identified |
| DOCX | Upload any .docx → mammoth extracts text → AI analyzes |
| XLSX | Upload spreadsheet → SheetJS extracts cells → rent roll detected if applicable |
| PPTX | Upload .pptx → slide text extracted → AI analyzes |
| Apply | Click Apply on any doc → items checked in Checklist tab with AI badge |
| Share | Click Share → URL hash updated → paste in new tab → identical state |
| Badges | Applied items show "🤖 [docname] · [confidence]%" badge |
| Release | GitHub Release v1.1.0 created |

---

*PRD-P360-001 · Property360 Sale Advisor · BidDeed.AI / Everest Capital USA · Feb 25, 2026*  
*All actions pre-approved by Ariel Shapira. Execute autonomously.*
