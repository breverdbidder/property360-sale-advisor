"use client";

import { useState, useCallback } from "react";
import { PHASES, type Phase } from "@/lib/phases";

const BRAND = {
  primary: "#1B4F72",
  accent: "#2E86C1",
  gold: "#D4AC0D",
  light: "#EBF5FB",
  success: "#1E8449",
  danger: "#C0392B",
  bg: "#F4F6F7",
};

function ScoreCard({ checked }: { checked: Set<string> }) {
  const total = PHASES.reduce((s, p) => s + p.items.length, 0);
  const criticalTotal = PHASES.reduce((s, p) => s + p.items.filter(i => i.critical).length, 0);
  const criticalDone = PHASES.reduce((s, p) => s + p.items.filter(i => i.critical && checked.has(i.id)).length, 0);
  const done = checked.size;
  const pct = Math.round((done / total) * 100);
  const critPct = Math.round((criticalDone / criticalTotal) * 100);

  const readiness = critPct >= 90 ? { label: "READY TO LIST", color: BRAND.success } :
    critPct >= 70 ? { label: "NEARLY READY", color: BRAND.gold } :
    { label: "NOT READY", color: BRAND.danger };

  return (
    <div style={{ background: "white", borderRadius: 12, padding: "20px 24px", marginBottom: 24, boxShadow: "0 2px 12px rgba(0,0,0,0.08)", border: `2px solid ${readiness.color}` }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", flexWrap: "wrap", gap: 16 }}>
        <div>
          <div style={{ fontSize: 13, color: "#666", marginBottom: 4 }}>SALE READINESS</div>
          <div style={{ fontSize: 28, fontWeight: 800, color: readiness.color }}>{readiness.label}</div>
        </div>
        <div style={{ display: "flex", gap: 32 }}>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 36, fontWeight: 800, color: BRAND.primary }}>{pct}%</div>
            <div style={{ fontSize: 12, color: "#888" }}>Overall<br/>({done}/{total})</div>
          </div>
          <div style={{ textAlign: "center" }}>
            <div style={{ fontSize: 36, fontWeight: 800, color: readiness.color }}>{critPct}%</div>
            <div style={{ fontSize: 12, color: "#888" }}>Critical Items<br/>({criticalDone}/{criticalTotal})</div>
          </div>
        </div>
      </div>
      <div style={{ marginTop: 16, background: "#eee", borderRadius: 8, height: 10, overflow: "hidden" }}>
        <div style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${BRAND.accent}, ${BRAND.primary})`, height: "100%", borderRadius: 8, transition: "width 0.4s ease" }} />
      </div>
    </div>
  );
}

function PhaseCard({ phase, checked, onToggle, isActive, onActivate }: {
  phase: Phase;
  checked: Set<string>;
  onToggle: (id: string) => void;
  isActive: boolean;
  onActivate: () => void;
}) {
  const done = phase.items.filter(i => checked.has(i.id)).length;
  const total = phase.items.length;
  const pct = Math.round((done / total) * 100);
  const critDone = phase.items.filter(i => i.critical && checked.has(i.id)).length;
  const critTotal = phase.items.filter(i => i.critical).length;
  const allCritDone = critDone === critTotal;

  return (
    <div style={{ background: "white", borderRadius: 10, marginBottom: 12, boxShadow: "0 1px 6px rgba(0,0,0,0.07)", border: isActive ? `2px solid ${BRAND.accent}` : "2px solid transparent", overflow: "hidden" }}>
      <button
        onClick={onActivate}
        style={{ width: "100%", background: "none", border: "none", padding: "16px 20px", cursor: "pointer", display: "flex", alignItems: "center", gap: 12, textAlign: "left" }}
      >
        <div style={{ fontSize: 28, flexShrink: 0 }}>{phase.icon}</div>
        <div style={{ flex: 1 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: 8 }}>
            <div>
              <span style={{ fontSize: 11, color: BRAND.accent, fontWeight: 700, letterSpacing: 1 }}>PHASE {phase.id}</span>
              <div style={{ fontSize: 16, fontWeight: 700, color: BRAND.primary, marginTop: 2 }}>{phase.title}</div>
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
              {!allCritDone && <span style={{ fontSize: 11, background: "#FEF9C3", color: "#854D0E", padding: "2px 8px", borderRadius: 4, fontWeight: 600 }}>⚠️ Critical Pending</span>}
              <span style={{ fontSize: 14, fontWeight: 700, color: pct === 100 ? BRAND.success : BRAND.primary }}>{done}/{total}</span>
            </div>
          </div>
          <div style={{ background: "#eee", borderRadius: 4, height: 5, marginTop: 8, overflow: "hidden" }}>
            <div style={{ width: `${pct}%`, background: pct === 100 ? BRAND.success : BRAND.accent, height: "100%", borderRadius: 4, transition: "width 0.3s" }} />
          </div>
        </div>
        <div style={{ color: "#aaa", fontSize: 18 }}>{isActive ? "▲" : "▼"}</div>
      </button>

      {isActive && (
        <div style={{ padding: "0 20px 20px", borderTop: "1px solid #f0f0f0" }}>
          <p style={{ fontSize: 13, color: "#666", margin: "12px 0 16px" }}>{phase.description}</p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {phase.items.map(item => (
              <label
                key={item.id}
                style={{ display: "flex", alignItems: "flex-start", gap: 10, cursor: "pointer", padding: "10px 12px", borderRadius: 8, background: checked.has(item.id) ? "#F0FDF4" : item.critical ? "#FFF7ED" : "#FAFAFA", border: checked.has(item.id) ? "1px solid #BBF7D0" : item.critical ? "1px solid #FED7AA" : "1px solid #E5E7EB", transition: "all 0.2s" }}
              >
                <input
                  type="checkbox"
                  checked={checked.has(item.id)}
                  onChange={() => onToggle(item.id)}
                  style={{ marginTop: 2, width: 16, height: 16, flexShrink: 0, accentColor: BRAND.success }}
                />
                <span style={{ fontSize: 14, color: "#374151", lineHeight: 1.5 }}>
                  {item.critical && <span style={{ fontSize: 11, background: "#FED7AA", color: "#92400E", padding: "1px 6px", borderRadius: 3, fontWeight: 700, marginRight: 6 }}>CRITICAL</span>}
                  {item.text}
                </span>
              </label>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function SaleAdvisor() {
  const [checked, setChecked] = useState<Set<string>>(new Set());
  const [activePhase, setActivePhase] = useState<number | null>(1);

  const toggle = useCallback((id: string) => {
    setChecked(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  }, []);

  const resetAll = () => {
    if (confirm("Reset all checkboxes?")) setChecked(new Set());
  };

  return (
    <div style={{ minHeight: "100vh", background: BRAND.bg }}>
      {/* Header */}
      <div style={{ background: `linear-gradient(135deg, ${BRAND.primary} 0%, #2980B9 100%)`, padding: "24px 20px", color: "white" }}>
        <div style={{ maxWidth: 800, margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 12 }}>
            <div>
              <div style={{ fontSize: 11, letterSpacing: 2, opacity: 0.8, marginBottom: 6 }}>PROPERTY360 · MARIAM SHAPIRA · BREVARD COUNTY</div>
              <h1 style={{ margin: 0, fontSize: 26, fontWeight: 800, lineHeight: 1.2 }}>Income Property Sale Advisor</h1>
              <p style={{ margin: "8px 0 0", opacity: 0.85, fontSize: 14 }}>10-Phase System to Maximize Your Investment Sale</p>
            </div>
            <button onClick={resetAll} style={{ background: "rgba(255,255,255,0.15)", border: "1px solid rgba(255,255,255,0.3)", color: "white", padding: "8px 16px", borderRadius: 8, cursor: "pointer", fontSize: 13 }}>
              Reset All
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div style={{ maxWidth: 800, margin: "0 auto", padding: "24px 16px" }}>
        <ScoreCard checked={checked} />

        {/* Phase navigation */}
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 20 }}>
          {PHASES.map(p => {
            const done = p.items.filter(i => checked.has(i.id)).length;
            const pct = Math.round((done / p.items.length) * 100);
            return (
              <button
                key={p.id}
                onClick={() => setActivePhase(activePhase === p.id ? null : p.id)}
                style={{ padding: "5px 12px", borderRadius: 20, border: "none", cursor: "pointer", fontSize: 12, fontWeight: 600, background: pct === 100 ? BRAND.success : activePhase === p.id ? BRAND.accent : "#ddd", color: activePhase === p.id || pct === 100 ? "white" : "#555" }}
              >
                {p.icon} {p.id} {pct === 100 ? "✓" : ""}
              </button>
            );
          })}
        </div>

        {PHASES.map(phase => (
          <PhaseCard
            key={phase.id}
            phase={phase}
            checked={checked}
            onToggle={toggle}
            isActive={activePhase === phase.id}
            onActivate={() => setActivePhase(activePhase === phase.id ? null : phase.id)}
          />
        ))}

        {/* Footer */}
        <div style={{ textAlign: "center", padding: "24px 0 8px", color: "#aaa", fontSize: 12 }}>
          Property360 · Mariam Shapira, FL Licensed Broker · (321) 000-0000<br/>
          Built with Vinext · Cloudflare Workers · © {new Date().getFullYear()}
        </div>
      </div>
    </div>
  );
}
