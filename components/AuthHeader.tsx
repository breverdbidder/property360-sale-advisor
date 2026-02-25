// components/AuthHeader.tsx
"use client";

import { useAuth } from "@/lib/supabase/useAuth";

const C = {
  navy: "#1B4F72",
  accent: "#2E86C1",
  white: "#FFFFFF",
  gray: "#6B7280",
};

export default function AuthHeader() {
  const { user, loading, signOut } = useAuth();

  if (loading) return null;
  if (!user) return null;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "8px 24px",
        background: C.navy,
        color: C.white,
        fontSize: "13px",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
        <span style={{ fontSize: "16px" }}>🏠</span>
        <span style={{ fontWeight: 600 }}>Property360</span>
        <span style={{ color: "rgba(255,255,255,0.5)", margin: "0 8px" }}>|</span>
        <span style={{ color: "rgba(255,255,255,0.7)" }}>{user.email}</span>
      </div>
      <button
        onClick={signOut}
        style={{
          background: "rgba(255,255,255,0.1)",
          border: "1px solid rgba(255,255,255,0.2)",
          borderRadius: "6px",
          color: C.white,
          padding: "4px 12px",
          fontSize: "12px",
          cursor: "pointer",
          transition: "background 0.2s",
        }}
        onMouseOver={(e) => ((e.target as HTMLButtonElement).style.background = "rgba(255,255,255,0.2)")}
        onMouseOut={(e) => ((e.target as HTMLButtonElement).style.background = "rgba(255,255,255,0.1)")}
      >
        Sign Out
      </button>
    </div>
  );
}
