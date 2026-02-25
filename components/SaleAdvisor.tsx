"use client";

import { useState, useCallback, useRef } from "react";
import { PHASES, type Phase } from "@/lib/phases";

const C = {
  navy: "#1B4F72", accent: "#2E86C1", gold: "#D4AC0D",
  green: "#1E8449", greenLight: "#E8F5E9", greenBorder: "#A9DFBF",
  red: "#C0392B", redLight: "#FDEDEC", redBorder: "#F1948A",
  amber: "#E65100", amberLight: "#FFF3E0", amberBorder: "#FFCC02",
  blue: "#0D47A1", blueLight: "#E3F2FD", blueBorder: "#90CAF9",
  gray: "#6B7280", grayLight: "#F9FAFB", grayBorder: "#E5E7EB",
  bg: "#F0F4F8", white: "#FFFFFF",
};

interface AIItem { id: string; confidence: number; extractedValue: string | null; }
interface DocAnalysis {
  docType: string; summary: string;
  completedItems: AIItem[]; keyFindings: string[]; warnings: string[];
}
interface UploadedDoc {
  id: string; name: string; type: "pdf" | "docx" | "xlsx" | "pptx";
  size: number; uploadedAt: Date;
  status: "uploading" | "analyzing" | "done" | "error";
  analysis?: DocAnalysis; error?: string; applied: boolean;
}
interface Toast { id: string; message: string; type: "success" | "info" | "warning" | "error"; }
type TabId = "checklist" | "documents" | "insights";

const ALL_ITEMS = PHASES.flatMap(p => p.items);
const TOTAL = ALL_ITEMS.length;
const CRITICAL_TOTAL = ALL_ITEMS.filter(i => i.critical).length;
const fmtSize = (b: number) => b < 1048576 ? `${(b/1024).toFixed(0)} KB` : `${(b/1048576).toFixed(1)} MB`;
const docIcon = (t: string) => t === "pdf" ? "📄" : t === "docx" ? "📝" : t === "pptx" ? "📊" : "📋";

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

// ─── TOAST STACK ──────────────────────────────────────────────────────────────
function ToastStack({ toasts, onDismiss }: { toasts: Toast[]; onDismiss: (id: string) => void }) {
  const colors = {
    success: { bg: C.greenLight, border: C.green, icon: "✅" },
    info: { bg: C.blueLight, border: C.accent, icon: "ℹ️" },
    warning: { bg: C.amberLight, border: C.amber, icon: "⚠️" },
    error: { bg: C.redLight, border: C.red, icon: "❌" },
  };
  return (
    <div style={{ position: "fixed", bottom: 24, right: 24, zIndex: 1000, display: "flex", flexDirection: "column", gap: 8, maxWidth: 340 }}>
      {toasts.map(t => {
        const s = colors[t.type];
        return (
          <div key={t.id} onClick={() => onDismiss(t.id)} style={{ background: s.bg, border: `1.5px solid ${s.border}`, borderRadius: 10, padding: "11px 15px", display: "flex", alignItems: "center", gap: 10, boxShadow: "0 4px 16px rgba(0,0,0,0.12)", cursor: "pointer" }}>
            <span style={{ fontSize: 18, flexShrink: 0 }}>{s.icon}</span>
            <span style={{ fontSize: 13, color: "#222", lineHeight: 1.4 }}>{t.message}</span>
          </div>
        );
      })}
    </div>
  );
}

// ─── SCORE CARD ───────────────────────────────────────────────────────────────
function ScoreCard({ checked, docsAnalyzed, onTabChange }: { checked: Set<string>; docsAnalyzed: number; onTabChange: (t: TabId) => void; }) {
  const done = checked.size;
  const pct = Math.round((done / TOTAL) * 100);
  const critDone = ALL_ITEMS.filter(i => i.critical && checked.has(i.id)).length;
  const critPct = Math.round((critDone / CRITICAL_TOTAL) * 100);
  const readiness = critPct >= 90 ? { label: "READY TO LIST", color: C.green }
    : critPct >= 70 ? { label: "NEARLY READY", color: C.gold }
    : { label: "NOT READY", color: C.red };
  return (
    <div style={{ background: C.white, borderRadius: 14, padding: "18px 22px", marginBottom: 18, boxShadow: "0 2px 16px rgba(0,0,0,0.08)", border: `2px solid ${readiness.color}` }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 12 }}>
        <div>
          <div style={{ fontSize: 10, color: C.gray, marginBottom: 3, letterSpacing: 1 }}>SALE READINESS</div>
          <div style={{ fontSize: 24, fontWeight: 800, color: readiness.color }}>{readiness.label}</div>
        </div>
        <div style={{ display: "flex", gap: 20 }}>
          {[
            { val: `${pct}%`, label: `Overall (${done}/${TOTAL})`, tab: "checklist" as TabId },
            { val: `${critPct}%`, label: `Critical (${critDone}/${CRITICAL_TOTAL})`, tab: "checklist" as TabId },
            { val: `${docsAnalyzed}`, label: "Docs Analyzed", tab: "documents" as TabId },
          ].map(s => (
            <div key={s.label} style={{ textAlign: "center", cursor: "pointer" }} onClick={() => onTabChange(s.tab)}>
              <div style={{ fontSize: 30, fontWeight: 800, color: s.tab === "documents" ? C.accent : readiness.color }}>{s.val}</div>
              <div style={{ fontSize: 10, color: C.gray, lineHeight: 1.4 }}>{s.label}</div>
            </div>
          ))}
        </div>
      </div>
      <div style={{ marginTop: 12, background: "#E5E7EB", borderRadius: 6, height: 9, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${C.accent}, ${C.navy})`, height: "100%", borderRadius: 6, transition: "width 0.5s ease" }} />
      </div>
    </div>
  );
}

// ─── TAB BAR ──────────────────────────────────────────────────────────────────
function TabBar({ active, onChange, badge }: { active: TabId; onChange: (t: TabId) => void; badge: number; }) {
  const tabs = [
    { id: "checklist" as TabId, label: "Checklist", icon: "✅" },
    { id: "documents" as TabId, label: "Documents", icon: "📁" },
    { id: "insights" as TabId, label: "Insights", icon: "💡" },
  ];
  return (
    <div style={{ display: "flex", gap: 0, background: C.white, borderRadius: 12, padding: 4, marginBottom: 18, boxShadow: "0 1px 6px rgba(0,0,0,0.07)" }}>
      {tabs.map(t => (
        <button key={t.id} onClick={() => onChange(t.id)} style={{
          flex: 1, padding: "9px 12px", border: "none", borderRadius: 9,
          background: active === t.id ? C.navy : "transparent",
          color: active === t.id ? C.white : C.gray,
          fontWeight: active === t.id ? 700 : 500, fontSize: 13,
          cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", gap: 6, transition: "all 0.2s",
        }}>
          {t.icon} {t.label}
          {t.id === "documents" && badge > 0 && (
            <span style={{ background: C.accent, color: "white", borderRadius: 10, padding: "1px 6px", fontSize: 10, fontWeight: 700 }}>{badge}</span>
          )}
        </button>
      ))}
    </div>
  );
}

// ─── PHASE CARD ───────────────────────────────────────────────────────────────
function PhaseCard({ phase, checked, onToggle, isActive, onActivate, aiSuggested, extractedValues }: {
  phase: Phase; checked: Set<string>; onToggle: (id: string) => void;
  isActive: boolean; onActivate: () => void;
  aiSuggested: Map<string, { confidence: number; value: string | null; docName: string }>;
  extractedValues: Map<string, string>;
}) {
  const done = phase.items.filter(i => checked.has(i.id)).length;
  const total = phase.items.length;
  const pct = Math.round((done / total) * 100);
  const critPending = phase.items.filter(i => i.critical && !checked.has(i.id)).length;
  const aiPending = phase.items.filter(i => aiSuggested.has(i.id) && !checked.has(i.id)).length;

  return (
    <div style={{ background: C.white, borderRadius: 12, marginBottom: 9, boxShadow: "0 1px 8px rgba(0,0,0,0.06)", border: isActive ? `2px solid ${C.accent}` : "2px solid transparent", overflow: "hidden", transition: "all 0.2s" }}>
      <button onClick={onActivate} style={{ width: "100%", background: "none", border: "none", padding: "13px 16px", cursor: "pointer", display: "flex", alignItems: "center", gap: 11, textAlign: "left" }}>
        <div style={{ fontSize: 24, flexShrink: 0 }}>{phase.icon}</div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 6 }}>
            <div>
              <div style={{ fontSize: 10, color: C.accent, fontWeight: 700, letterSpacing: 1 }}>PHASE {phase.id}</div>
              <div style={{ fontSize: 14, fontWeight: 700, color: C.navy }}>{phase.title}</div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 7, flexShrink: 0 }}>
              {aiPending > 0 && !isActive && <span style={{ fontSize: 10, background: C.blueLight, color: C.blue, padding: "2px 7px", borderRadius: 4, fontWeight: 700, border: `1px solid ${C.blueBorder}` }}>🤖 {aiPending}</span>}
              {critPending > 0 && <span style={{ fontSize: 10, background: C.amberLight, color: C.amber, padding: "2px 7px", borderRadius: 4, fontWeight: 700 }}>⚠️ {critPending}</span>}
              <span style={{ fontSize: 13, fontWeight: 700, color: pct === 100 ? C.green : C.gray }}>{done}/{total}</span>
            </div>
          </div>
          <div style={{ background: "#E5E7EB", borderRadius: 4, height: 5, marginTop: 7, overflow: "hidden" }}>
            <div style={{ width: `${pct}%`, background: pct === 100 ? C.green : C.accent, height: "100%", borderRadius: 4, transition: "width 0.4s" }} />
          </div>
        </div>
        <div style={{ color: "#bbb", fontSize: 14, flexShrink: 0 }}>{isActive ? "▲" : "▼"}</div>
      </button>

      {isActive && (
        <div style={{ padding: "0 16px 16px", borderTop: "1px solid #F4F4F4" }}>
          <p style={{ fontSize: 12, color: C.gray, margin: "10px 0 13px" }}>{phase.description}</p>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {phase.items.map(item => {
              const isChecked = checked.has(item.id);
              const suggestion = aiSuggested.get(item.id);
              const extracted = extractedValues.get(item.id);
              const isSuggested = !!suggestion && !isChecked;
              const bg = isChecked ? C.greenLight : isSuggested ? C.blueLight : item.critical ? C.amberLight : C.grayLight;
              const border = isChecked ? C.greenBorder : isSuggested ? C.blueBorder : item.critical ? C.amberBorder : C.grayBorder;
              return (
                <label key={item.id} style={{ display: "flex", alignItems: "flex-start", gap: 9, cursor: "pointer", padding: "9px 11px", borderRadius: 8, background: bg, border: `1px solid ${border}`, transition: "all 0.2s" }}>
                  <input type="checkbox" checked={isChecked} onChange={() => onToggle(item.id)}
                    style={{ marginTop: 2, width: 15, height: 15, flexShrink: 0, accentColor: C.green }} />
                  <div style={{ flex: 1 }}>
                    <div style={{ fontSize: 13, color: "#374151", lineHeight: 1.5 }}>
                      {item.critical && <span style={{ fontSize: 10, background: "#FED7AA", color: "#92400E", padding: "1px 5px", borderRadius: 3, fontWeight: 700, marginRight: 5 }}>CRITICAL</span>}
                      {item.text}
                    </div>
                    {isSuggested && (
                      <div style={{ marginTop: 4, padding: "4px 8px", background: "rgba(13,71,161,0.06)", borderRadius: 5, fontSize: 11, color: C.blue }}>
                        <b>🤖 {Math.round(suggestion.confidence * 100)}% confidence</b>
                        {suggestion.value && <> · <em>{suggestion.value}</em></>}
                        <span style={{ color: C.gray }}> · {suggestion.docName}</span>
                      </div>
                    )}
                    {isChecked && extracted && (
                      <div style={{ marginTop: 3, fontSize: 11, color: C.green }}>✓ <em>{extracted}</em></div>
                    )}
                  </div>
                </label>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}

// ─── DROP ZONE ────────────────────────────────────────────────────────────────
function DropZone({ onFiles }: { onFiles: (files: File[]) => void }) {
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false);
    const files = Array.from(e.dataTransfer.files).filter(f => /\.(pdf|docx|xlsx|xls|pptx)$/i.test(f.name));
    if (files.length) onFiles(files);
  };
  return (
    <div onDragOver={e => { e.preventDefault(); setDragging(true); }} onDragLeave={() => setDragging(false)}
      onDrop={handleDrop} onClick={() => inputRef.current?.click()}
      style={{ border: `2px dashed ${dragging ? C.accent : C.grayBorder}`, borderRadius: 14, padding: "28px 20px", textAlign: "center", cursor: "pointer", background: dragging ? C.blueLight : C.grayLight, transition: "all 0.2s" }}>
      <div style={{ fontSize: 36, marginBottom: 10 }}>📂</div>
      <div style={{ fontSize: 15, fontWeight: 700, color: C.navy, marginBottom: 5 }}>Drop documents or click to browse</div>
      <div style={{ fontSize: 12, color: C.gray }}>PDF · DOCX · XLSX · PPTX · AI will auto-fill your checklist</div>
      <input ref={inputRef} type="file" accept=".pdf,.docx,.xlsx,.xls,.pptx" multiple style={{ display: "none" }}
        onChange={e => { const f = Array.from(e.target.files || []); if (f.length) onFiles(f); e.target.value = ""; }} />
    </div>
  );
}

// ─── DOC CARD ─────────────────────────────────────────────────────────────────
function DocCard({ doc, onApply, onPreview, onRemove }: {
  doc: UploadedDoc; onApply: (id: string) => void;
  onPreview: (id: string) => void; onRemove: (id: string) => void;
}) {
  const [expanded, setExpanded] = useState(false);
  const count = doc.analysis?.completedItems.length || 0;
  return (
    <div style={{ background: C.white, borderRadius: 12, marginBottom: 9, border: `1.5px solid ${doc.status === "error" ? C.redBorder : doc.applied ? C.greenBorder : C.grayBorder}`, overflow: "hidden", boxShadow: "0 1px 6px rgba(0,0,0,0.05)" }}>
      <div style={{ padding: "13px 15px", display: "flex", alignItems: "center", gap: 11 }}>
        <span style={{ fontSize: 26, flexShrink: 0 }}>{docIcon(doc.type)}</span>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: C.navy, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>{doc.name}</div>
          <div style={{ fontSize: 11, color: C.gray, marginTop: 2 }}>
            {fmtSize(doc.size)} · {doc.status === "analyzing" ? "🔄 AI analyzing..." : doc.status === "done" ? doc.analysis?.docType || "Done" : doc.status === "error" ? "❌ Error" : "⏳"}
          </div>
        </div>
        <div style={{ display: "flex", gap: 7, alignItems: "center", flexShrink: 0 }}>
          {doc.status === "done" && !doc.applied && count > 0 && (
            <>
              <button onClick={() => onPreview(doc.id)} style={{ background: C.blueLight, color: C.blue, border: `1px solid ${C.blueBorder}`, borderRadius: 7, padding: "5px 10px", cursor: "pointer", fontSize: 11, fontWeight: 700 }}>Preview</button>
              <button onClick={() => onApply(doc.id)} style={{ background: C.accent, color: "white", border: "none", borderRadius: 7, padding: "5px 10px", cursor: "pointer", fontSize: 11, fontWeight: 700 }}>Apply {count}</button>
            </>
          )}
          {doc.applied && <span style={{ fontSize: 11, color: C.green, fontWeight: 700 }}>✅ Applied</span>}
          {doc.status === "done" && (
            <button onClick={() => setExpanded(!expanded)} style={{ background: C.grayLight, border: "none", borderRadius: 7, padding: "5px 9px", cursor: "pointer", fontSize: 11, color: C.gray }}>
              {expanded ? "▲" : "▼"}
            </button>
          )}
          <button onClick={() => onRemove(doc.id)} style={{ background: "none", border: "none", cursor: "pointer", fontSize: 15, color: "#ccc" }}>✕</button>
        </div>
      </div>

      {doc.status === "analyzing" && (
        <div style={{ padding: "6px 15px 12px" }}>
          <div style={{ height: 4, background: "#E5E7EB", borderRadius: 2, overflow: "hidden" }}>
            <div style={{ width: "70%", height: "100%", background: `linear-gradient(90deg, ${C.accent}, ${C.navy})`, borderRadius: 2, animation: "shimmer 1.5s linear infinite" }} />
          </div>
          <div style={{ fontSize: 11, color: C.gray, marginTop: 5 }}>Reading document content with AI...</div>
        </div>
      )}
      {doc.status === "error" && <div style={{ padding: "6px 15px 12px", fontSize: 12, color: C.red }}>{doc.error}</div>}

      {expanded && doc.analysis && (
        <div style={{ padding: "0 15px 14px", borderTop: "1px solid #F0F0F0" }}>
          <div style={{ fontSize: 12, color: "#374151", marginTop: 11, lineHeight: 1.6 }}>{doc.analysis.summary}</div>
          {doc.analysis.keyFindings.length > 0 && (
            <div style={{ marginTop: 11 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.navy, marginBottom: 5, letterSpacing: 1 }}>KEY FINDINGS</div>
              {doc.analysis.keyFindings.map((f, i) => <div key={i} style={{ fontSize: 12, padding: "3px 0 3px 10px", borderLeft: `2px solid ${C.accent}`, color: "#374151", marginBottom: 3 }}>{f}</div>)}
            </div>
          )}
          {doc.analysis.warnings.length > 0 && (
            <div style={{ marginTop: 11, background: C.amberLight, borderRadius: 8, padding: "9px 11px" }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.amber, marginBottom: 5 }}>⚠️ WARNINGS</div>
              {doc.analysis.warnings.map((w, i) => <div key={i} style={{ fontSize: 12, color: "#374151", marginBottom: 2 }}>• {w}</div>)}
            </div>
          )}
          {count > 0 && (
            <div style={{ marginTop: 11 }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: C.navy, marginBottom: 5, letterSpacing: 1 }}>AUTO-FILL ITEMS ({count})</div>
              {doc.analysis.completedItems.map(ci => {
                const item = ALL_ITEMS.find(i => i.id === ci.id);
                return item ? (
                  <div key={ci.id} style={{ fontSize: 12, padding: "5px 9px", background: C.blueLight, borderRadius: 6, marginBottom: 3, display: "flex", justifyContent: "space-between", gap: 8, flexWrap: "wrap" }}>
                    <span style={{ color: "#374151", flex: 1 }}>{item.text.slice(0, 65)}{item.text.length > 65 ? "…" : ""}</span>
                    <div style={{ display: "flex", gap: 8, flexShrink: 0 }}>
                      {ci.extractedValue && <span style={{ color: C.green, fontStyle: "italic" }}>{ci.extractedValue.slice(0, 30)}</span>}
                      <span style={{ color: C.blue, fontWeight: 700 }}>{Math.round(ci.confidence * 100)}%</span>
                    </div>
                  </div>
                ) : null;
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

// ─── INSIGHTS TAB ─────────────────────────────────────────────────────────────
function InsightsTab({ checked, docs }: { checked: Set<string>; docs: UploadedDoc[]; }) {
  const phases = PHASES.map(p => {
    const done = p.items.filter(i => checked.has(i.id)).length;
    const critDone = p.items.filter(i => i.critical && checked.has(i.id)).length;
    const critTotal = p.items.filter(i => i.critical).length;
    return { ...p, done, pct: Math.round((done / p.items.length) * 100), critDone, critTotal };
  });

  const blockers = phases.filter(p => p.critDone < p.critTotal);
  const complete = phases.filter(p => p.pct === 100);
  const inProgress = phases.filter(p => p.pct > 0 && p.pct < 100);

  const docsByPhase: Record<number, string[]> = {};
  docs.forEach(d => {
    d.analysis?.completedItems.forEach(ci => {
      const p = PHASES.find(ph => ph.items.some(i => i.id === ci.id));
      if (p) { docsByPhase[p.id] = [...new Set([...(docsByPhase[p.id] || []), d.name.slice(0, 22)])]; }
    });
  });

  return (
    <div>
      {blockers.length > 0 && (
        <div style={{ background: C.redLight, border: `1.5px solid ${C.redBorder}`, borderRadius: 12, padding: "14px 16px", marginBottom: 14 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: C.red, marginBottom: 8 }}>🚨 {blockers.length} phases with critical items pending</div>
          {blockers.map(p => (
            <div key={p.id} style={{ display: "flex", justifyContent: "space-between", padding: "5px 0", borderBottom: "1px solid rgba(192,57,43,0.1)", fontSize: 12 }}>
              <span>{p.icon} Phase {p.id}: {p.title}</span>
              <span style={{ color: C.red, fontWeight: 700 }}>{p.critTotal - p.critDone} critical left</span>
            </div>
          ))}
        </div>
      )}

      {complete.length > 0 && (
        <div style={{ background: C.greenLight, border: `1.5px solid ${C.greenBorder}`, borderRadius: 12, padding: "14px 16px", marginBottom: 14 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: C.green, marginBottom: 8 }}>✅ {complete.length} phases fully complete</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
            {complete.map(p => <span key={p.id} style={{ background: C.green, color: "white", padding: "3px 10px", borderRadius: 20, fontSize: 11, fontWeight: 600 }}>{p.icon} {p.title}</span>)}
          </div>
        </div>
      )}

      {inProgress.length > 0 && (
        <div style={{ background: C.white, border: `1.5px solid ${C.grayBorder}`, borderRadius: 12, padding: "14px 16px", marginBottom: 14 }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: C.navy, marginBottom: 10 }}>🔄 In Progress</div>
          {inProgress.map(p => (
            <div key={p.id} style={{ marginBottom: 12 }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 4 }}>
                <span style={{ fontWeight: 600 }}>{p.icon} {p.title}</span>
                <span style={{ color: C.gray }}>{p.done}/{p.items.length} ({p.pct}%)</span>
              </div>
              <div style={{ background: "#E5E7EB", borderRadius: 4, height: 6, overflow: "hidden" }}>
                <div style={{ width: `${p.pct}%`, background: C.accent, height: "100%", borderRadius: 4 }} />
              </div>
              {docsByPhase[p.id] && (
                <div style={{ fontSize: 11, color: C.accent, marginTop: 3 }}>📄 {docsByPhase[p.id].join(", ")}</div>
              )}
            </div>
          ))}
        </div>
      )}

      {docs.filter(d => d.status === "done").length > 0 && (
        <div style={{ background: C.white, border: `1.5px solid ${C.grayBorder}`, borderRadius: 12, padding: "14px 16px" }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: C.navy, marginBottom: 10 }}>📊 Document Coverage</div>
          {docs.filter(d => d.status === "done").map(doc => (
            <div key={doc.id} style={{ display: "flex", justifyContent: "space-between", padding: "7px 0", borderBottom: `1px solid #F0F0F0`, fontSize: 12 }}>
              <span>{docIcon(doc.type)} {doc.name.slice(0, 38)}{doc.name.length > 38 ? "…" : ""}</span>
              <span style={{ color: doc.applied ? C.green : C.accent, fontWeight: 600 }}>
                {doc.analysis?.completedItems.length || 0} items {doc.applied ? "✓ applied" : "pending"}
              </span>
            </div>
          ))}
        </div>
      )}

      {checked.size === 0 && docs.length === 0 && (
        <div style={{ textAlign: "center", padding: "40px 0", color: C.gray }}>
          <div style={{ fontSize: 36, marginBottom: 12 }}>📈</div>
          <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 6 }}>No progress yet</div>
          <div style={{ fontSize: 12 }}>Start checking items or upload documents to see insights.</div>
        </div>
      )}
    </div>
  );
}

// ─── MAIN ─────────────────────────────────────────────────────────────────────
export default function SaleAdvisor() {
  const [activeTab, setActiveTab] = useState<TabId>("checklist");
  const [checked, setChecked] = useState<Set<string>>(new Set());
  const [activePhase, setActivePhase] = useState<number | null>(1);
  const [docs, setDocs] = useState<UploadedDoc[]>([]);
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [extractedValues, setExtractedValues] = useState<Map<string, string>>(new Map());
  const [aiSuggested, setAiSuggested] = useState<Map<string, { confidence: number; value: string | null; docName: string }>>(new Map());
  const [manualOverrides, setManualOverrides] = useState<Set<string>>(new Set());

  const addToast = useCallback((message: string, type: Toast["type"] = "info") => {
    const id = Math.random().toString(36).slice(2);
    setToasts(prev => [...prev, { id, message, type }]);
    setTimeout(() => setToasts(prev => prev.filter(t => t.id !== id)), 4500);
  }, []);

  const toggle = useCallback((id: string) => {
    setChecked(prev => { const n = new Set(prev); n.has(id) ? n.delete(id) : n.add(id); return n; });
  }, []);

  const pendingBadge = docs.filter(d => d.status === "done" && !d.applied && (d.analysis?.completedItems.length || 0) > 0).length;

  const processFile = useCallback(async (file: File) => {
    const ext = file.name.split(".").pop()?.toLowerCase() || "";
    const fileType = (ext === "pdf" ? "pdf" : ext === "docx" ? "docx" : "xlsx") as UploadedDoc["type"];
    const docId = Math.random().toString(36).slice(2);

    setDocs(prev => [{ id: docId, name: file.name, type: fileType, size: file.size, uploadedAt: new Date(), status: "uploading", applied: false }, ...prev]);

    try {
      const content = await extractDocContent(file);
      setDocs(prev => prev.map(d => d.id === docId ? { ...d, status: "analyzing" } : d));

      const res = await fetch("/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content, fileName: file.name, fileType }),
      });
      const data = await res.json();
      if (!data.success) throw new Error(data.error || "Analysis failed");

      setDocs(prev => prev.map(d => d.id === docId ? { ...d, status: "done", analysis: data.analysis } : d));

      const count = data.analysis.completedItems?.length || 0;
      addToast(`📄 ${file.name}: ${count} item${count !== 1 ? "s" : ""} identified`, count > 0 ? "success" : "info");
      if (count > 0) setActiveTab("documents");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      setDocs(prev => prev.map(d => d.id === docId ? { ...d, status: "error", error: msg } : d));
      addToast(`❌ ${file.name}: ${msg}`, "error");
    }
  }, [addToast]);

  const handleFiles = useCallback((files: File[]) => files.forEach(f => processFile(f)), [processFile]);

  const applyDoc = useCallback((docId: string) => {
    const doc = docs.find(d => d.id === docId);
    if (!doc?.analysis) return;
    setChecked(prev => { const n = new Set(prev); doc.analysis!.completedItems.forEach(ci => n.add(ci.id)); return n; });
    setAiSuggested(prev => { const n = new Map(prev); doc.analysis!.completedItems.forEach(ci => n.delete(ci.id)); return n; });
    setExtractedValues(prev => {
      const n = new Map(prev);
      doc.analysis!.completedItems.forEach(ci => { if (ci.extractedValue) n.set(ci.id, ci.extractedValue); });
      return n;
    });
    setDocs(prev => prev.map(d => d.id === docId ? { ...d, applied: true } : d));
    addToast(`✅ Applied ${doc.analysis.completedItems.length} items from ${doc.name}`, "success");
  }, [docs, addToast]);

  const previewDoc = useCallback((docId: string) => {
    const doc = docs.find(d => d.id === docId);
    if (!doc?.analysis) return;
    setAiSuggested(prev => {
      const n = new Map(prev);
      doc.analysis!.completedItems.forEach(ci => {
        if (!checked.has(ci.id)) n.set(ci.id, { confidence: ci.confidence, value: ci.extractedValue, docName: doc.name });
      });
      return n;
    });
    setActiveTab("checklist");
    addToast(`🤖 ${doc.analysis.completedItems.length} suggestions shown in checklist`, "info");
  }, [docs, checked, addToast]);

  const removeDoc = useCallback((docId: string) => {
    const doc = docs.find(d => d.id === docId);
    if (doc?.analysis && !doc.applied) {
      setAiSuggested(prev => { const n = new Map(prev); doc.analysis!.completedItems.forEach(ci => n.delete(ci.id)); return n; });
    }
    setDocs(prev => prev.filter(d => d.id !== docId));
  }, [docs]);

  const applyAll = useCallback(() => {
    docs.filter(d => d.status === "done" && !d.applied).forEach(d => applyDoc(d.id));
  }, [docs, applyDoc]);

  return (
    <div style={{ minHeight: "100vh", background: C.bg }}>
      <div style={{ background: `linear-gradient(135deg, ${C.navy} 0%, #2980B9 100%)`, padding: "18px 16px", color: "white" }}>
        <div style={{ maxWidth: 820, margin: "0 auto", display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 10 }}>
          <div>
            <div style={{ fontSize: 10, letterSpacing: 2, opacity: 0.8, marginBottom: 3 }}>PROPERTY360 · MARIAM SHAPIRA · BREVARD COUNTY FL</div>
            <h1 style={{ margin: 0, fontSize: 20, fontWeight: 800 }}>Income Property Sale Advisor</h1>
            <p style={{ margin: "4px 0 0", opacity: 0.85, fontSize: 12 }}>10-Phase Checklist · AI Document Analysis · Auto-Fill</p>
          </div>
          <button onClick={() => { if (confirm("Reset everything?")) { setChecked(new Set()); setDocs([]); setAiSuggested(new Map()); setExtractedValues(new Map()); } }}
            style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.3)", color: "white", padding: "6px 13px", borderRadius: 8, cursor: "pointer", fontSize: 12 }}>
            Reset
          </button>
        </div>
      </div>

      <div style={{ maxWidth: 820, margin: "0 auto", padding: "18px 12px" }}>
        <ScoreCard checked={checked} docsAnalyzed={docs.filter(d => d.status === "done").length} onTabChange={setActiveTab} />
        <TabBar active={activeTab} onChange={setActiveTab} badge={pendingBadge} />

        {activeTab === "checklist" && (
          <div>
            {aiSuggested.size > 0 && (
              <div style={{ background: C.blueLight, border: `1.5px solid ${C.blueBorder}`, borderRadius: 12, padding: "11px 15px", marginBottom: 14, display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 9 }}>
                <div style={{ fontSize: 13, color: C.blue, fontWeight: 600 }}>🤖 {aiSuggested.size} AI suggestions — review below or apply all</div>
                <div style={{ display: "flex", gap: 7 }}>
                  <button onClick={() => {
                    const nc = new Set(checked); const ne = new Map(extractedValues);
                    aiSuggested.forEach((s, id) => { nc.add(id); if (s.value) ne.set(id, s.value); });
                    setChecked(nc); setExtractedValues(ne); setAiSuggested(new Map());
                    addToast(`✅ Applied all ${aiSuggested.size} AI suggestions`, "success");
                  }} style={{ background: C.accent, color: "white", border: "none", borderRadius: 8, padding: "6px 12px", cursor: "pointer", fontSize: 12, fontWeight: 700 }}>Apply All</button>
                  <button onClick={() => setAiSuggested(new Map())} style={{ background: C.white, color: C.gray, border: `1px solid ${C.grayBorder}`, borderRadius: 8, padding: "6px 10px", cursor: "pointer", fontSize: 12 }}>Dismiss</button>
                </div>
              </div>
            )}

            <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: 13 }}>
              {PHASES.map(p => {
                const pct = Math.round(p.items.filter(i => checked.has(i.id)).length / p.items.length * 100);
                const hasSug = p.items.some(i => aiSuggested.has(i.id));
                return (
                  <button key={p.id} onClick={() => setActivePhase(activePhase === p.id ? null : p.id)}
                    style={{ padding: "4px 10px", borderRadius: 20, border: hasSug ? `2px solid ${C.accent}` : "none", cursor: "pointer", fontSize: 11, fontWeight: 600, background: pct === 100 ? C.green : activePhase === p.id ? C.navy : "#ddd", color: (pct === 100 || activePhase === p.id) ? "white" : "#555" }}>
                    {p.icon}{p.id}{pct === 100 ? "✓" : hasSug ? "🤖" : ""}
                  </button>
                );
              })}
            </div>

            {PHASES.map(p => (
              <PhaseCard key={p.id} phase={p} checked={checked} onToggle={toggle}
                isActive={activePhase === p.id} onActivate={() => setActivePhase(activePhase === p.id ? null : p.id)}
                aiSuggested={aiSuggested} extractedValues={extractedValues} />
            ))}
          </div>
        )}

        {activeTab === "documents" && (
          <div>
            <DropZone onFiles={handleFiles} />
            {docs.length > 0 && (
              <div style={{ marginTop: 14 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
                  <div style={{ fontSize: 13, fontWeight: 700, color: C.navy }}>{docs.length} Document{docs.length > 1 ? "s" : ""}</div>
                  {pendingBadge > 0 && (
                    <div style={{ display: "flex", gap: 7 }}>
                      <button onClick={() => { docs.filter(d => d.status === "done" && !d.applied).forEach(d => previewDoc(d.id)); }}
                        style={{ background: C.blueLight, color: C.blue, border: `1px solid ${C.blueBorder}`, borderRadius: 8, padding: "6px 12px", cursor: "pointer", fontSize: 12, fontWeight: 700 }}>Preview All</button>
                      <button onClick={applyAll}
                        style={{ background: C.green, color: "white", border: "none", borderRadius: 8, padding: "6px 12px", cursor: "pointer", fontSize: 12, fontWeight: 700 }}>Apply All ({pendingBadge})</button>
                    </div>
                  )}
                </div>
                {docs.map(doc => <DocCard key={doc.id} doc={doc} onApply={applyDoc} onPreview={previewDoc} onRemove={removeDoc} />)}
              </div>
            )}
            {docs.length === 0 && (
              <div style={{ textAlign: "center", padding: "28px 0", color: C.gray }}>
                <div style={{ fontSize: 32, marginBottom: 10 }}>🤖</div>
                <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 5 }}>AI Document Analysis</div>
                <div style={{ fontSize: 12 }}>Upload appraisals, leases, title reports, rent rolls, tax certs and more.<br/>AI extracts data and auto-fills all 10 phases.</div>
              </div>
            )}
          </div>
        )}

        {activeTab === "insights" && <InsightsTab checked={checked} docs={docs} />}

        <div style={{ textAlign: "center", padding: "22px 0 6px", color: "#aaa", fontSize: 11 }}>
          Property360 · Mariam Shapira FL Licensed Broker · AI: Claude Sonnet · Cloudflare Workers
        </div>
      </div>

      <ToastStack toasts={toasts} onDismiss={id => setToasts(p => p.filter(t => t.id !== id))} />
      <style>{`@keyframes shimmer{0%{transform:translateX(-100%)}100%{transform:translateX(200%)}}`}</style>
    </div>
  );
}
