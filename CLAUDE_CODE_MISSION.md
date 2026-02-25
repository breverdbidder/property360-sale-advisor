# CLAUDE_CODE_MISSION.md — PRD-P360-001
# Property360 AI Document Intelligence Engine
# READ THIS FILE FIRST BEFORE WRITING ANY CODE

## SESSION INITIALIZATION PROTOCOL
1. Read this entire file
2. Load TODO.md from GitHub
3. Find first unchecked task [ ] — this is your ONLY task
4. Investigate relevant files before coding
5. Execute → Verify → Mark [x] → Push → next task
6. Never skip tasks or work out of order
7. If blocked after 3 attempts: log to insights table, report with problem + attempts + recommendation

## REPOSITORY
- GitHub: breverdbidder/property360-sale-advisor
- Live: property360-sale-advisor.pages.dev
- Stack: Next.js 15.5.2 + React 19 + TypeScript + Cloudflare Workers edge

## CURRENT STATE (as of Feb 25 2026)
- SaleAdvisor.tsx: 615 lines, partial implementation
- 3 tabs defined: checklist, documents, insights (some partial)
- /api/analyze route: COMPLETE — calls Claude API with document + checklist items
- PPTX parsing: MISSING
- XLSX real parsing: PLACEHOLDER (returns filename only)
- aiSources badge display: UNKNOWN — verify
- URL state sharing: MISSING
- ANTHROPIC_API_KEY: NOT SET in Cloudflare Pages — need env var setup

## ARCHITECTURE RULES (NON-NEGOTIABLE)
- Edge runtime: export const runtime = "edge" on ALL /api/* routes — NEVER remove
- No Node.js built-ins: no fs, path, os, Buffer (use Web APIs only)
- All file parsing: client-side only (FileReader, ArrayBuffer, browser APIs)
- State: ALL state in SaleAdvisor.tsx parent — never in child components
- Styles: inline only — no CSS modules, no Tailwind classes
- "use client" on ALL components that use hooks

## PARSER IMPLEMENTATION GUIDE

### PPTX (MISSING — implement with JSZip)
```typescript
if (ext === "pptx") {
  try {
    const JSZip = (await import("jszip")).default;
    const buf = await file.arrayBuffer();
    const zip = await JSZip.loadAsync(buf);
    const slideFiles = Object.keys(zip.files).filter(f => f.match(/^ppt\/slides\/slide\d+\.xml$/)).sort();
    const texts: string[] = [];
    for (const slideFile of slideFiles) {
      const xml = await zip.files[slideFile].async("text");
      const clean = xml.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
      if (clean.length > 10) texts.push(clean);
    }
    return `[PowerPoint: ${file.name}]
${texts.join("

").slice(0, 12000)}`;
  } catch { return `[PPTX: ${file.name}]`; }
}
```

### XLSX (PLACEHOLDER — fix with SheetJS)
```typescript
if (ext === "xlsx" || ext === "xls") {
  try {
    const XLSX = await import("xlsx");
    const buf = await file.arrayBuffer();
    const wb = XLSX.read(buf, { type: "array" });
    const parts: string[] = [`[Excel: ${file.name}]`];
    for (const sheetName of wb.SheetNames) {
      const ws = wb.Sheets[sheetName];
      const csv = XLSX.utils.sheet_to_csv(ws);
      if (csv.trim().length > 0) {
        parts.push(`Sheet: ${sheetName}
${csv.slice(0, 3000)}`);
      }
    }
    return parts.join("

").slice(0, 12000);
  } catch { return `[Excel: ${file.name}]`; }
}
```

## STATE SHAPE (must match exactly)
```typescript
interface AISource { docId: string; docName: string; confidence: number; extractedValue: string | null; }
// In component:
const [checked, setChecked] = useState<Set<string>>(new Set());
const [aiSources, setAiSources] = useState<Map<string, AISource>>(new Map());
const [manualOverrides, setManualOverrides] = useState<Set<string>>(new Set());
const [documents, setDocuments] = useState<UploadedDoc[]>([]);
const [activeTab, setActiveTab] = useState<TabId>("checklist");
```

## applyAnalysis() IMPLEMENTATION
```typescript
const applyAnalysis = useCallback((docId: string) => {
  const doc = documents.find(d => d.id === docId);
  if (!doc?.analysis) return;
  const newChecked = new Set(checked);
  const newSources = new Map(aiSources);
  for (const item of doc.analysis.completedItems) {
    if (item.confidence >= 0.65 && !manualOverrides.has(item.id)) {
      newChecked.add(item.id);
      const existing = newSources.get(item.id);
      if (!existing || item.confidence > existing.confidence) {
        newSources.set(item.id, { docId, docName: doc.name, confidence: item.confidence, extractedValue: item.extractedValue });
      }
    }
  }
  setChecked(newChecked);
  setAiSources(newSources);
}, [documents, checked, aiSources, manualOverrides]);
```

## AI BADGE COMPONENT
```typescript
// In item render, after the checkbox label:
{aiSources.has(item.id) && !manualOverrides.has(item.id) && (
  <span title={aiSources.get(item.id)!.extractedValue || "AI detected"} style={{
    fontSize: 10, padding: "1px 6px", borderRadius: 8,
    background: "#DBEAFE", color: "#1D4ED8", fontWeight: 700, marginLeft: 6,
    cursor: "help", whiteSpace: "nowrap"
  }}>
    {aiSources.get(item.id)!.docName.slice(0, 8)}… {Math.round(aiSources.get(item.id)!.confidence * 100)}%
  </span>
)}
```

## URL STATE SHARING
```typescript
// Serialize
const serializeState = () => {
  const data = { c: Array.from(checked), s: Object.fromEntries(aiSources) };
  return btoa(JSON.stringify(data));
};
// Deserialize on mount
useEffect(() => {
  if (window.location.hash.length > 1) {
    try {
      const data = JSON.parse(atob(window.location.hash.slice(1)));
      if (data.c) setChecked(new Set(data.c));
      if (data.s) setAiSources(new Map(Object.entries(data.s)));
    } catch {}
  }
}, []);
// Share button
const handleShare = () => {
  const url = window.location.origin + window.location.pathname + "#" + serializeState();
  navigator.clipboard.writeText(url);
  // show toast
};
```

## DEPENDENCIES TO ADD
- jszip: PPTX parsing (browser-compatible)
- xlsx: XLSX real parsing (browser-compatible, SheetJS)
- Both are edge-compatible (no Node.js built-ins)
- Install: npm install jszip xlsx --legacy-peer-deps

## SYSTEM PROMPT UPDATE FOR /api/analyze
Add to the systemPrompt in route.ts — append this to existing prompt:
"FLORIDA-SPECIFIC CONTEXT: Reference FL Statute 83.49 for security deposit compliance,
FL Statute 83.50 for ownership notice requirements. Flag any lease expiring within 90 days.
For rent rolls: calculate vacancy rate, flag below-market rents, note stabilized vs actual NOI."

## QUALITY GATES — ALL MUST PASS BEFORE PUSH
1. npx tsc --noEmit → 0 errors
2. npx @cloudflare/next-on-pages → build success, no warnings about Node.js APIs
3. Upload test.pdf (any PDF) → analysis JSON returned from API
4. Upload test.xlsx → SheetJS extracts real cell data (not placeholder)
5. Upload test.pptx → slide text extracted
6. Apply button → items checked → badges visible in checklist
7. Share URL → state restored on reload

## GIT COMMIT FORMAT
feat(prd-p360-001): [what was added]
fix(prd-p360-001): [what was fixed]
test(prd-p360-001): [what was verified]

## ESCALATION
If truly blocked after 3 attempts on any task:
- Log to Supabase insights table (URL: mocerqjnksmhcjzxrewo.supabase.co)
- Create GitHub Issue with: BLOCKED: [task], Tried: [3 attempts], Recommend: [solution]
- Move to next non-blocked task, do not halt session

