// app/login/page.tsx
"use client";

import { useState } from "react";
import { createClient } from "@/lib/supabase/client";


const C = {
  navy: "#1B4F72",
  accent: "#2E86C1",
  gold: "#D4AC0D",
  green: "#1E8449",
  white: "#FFFFFF",
  bg: "#F0F4F8",
  gray: "#6B7280",
  red: "#C0392B",
};

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mode, setMode] = useState<"login" | "signup" | "forgot">("login");
  const [message, setMessage] = useState<string | null>(null);

  const supabase = createClient();

  async function handleLogin(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signInWithPassword({ email, password });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    // Get redirect param or go to home
    const params = new URLSearchParams(window.location.search);
    const redirect = params.get("redirect") || "/";
    window.location.href = redirect;
  }

  async function handleSignup(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/api/auth/callback`,
      },
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    setMessage("Check your email for a confirmation link.");
    setLoading(false);
  }

  async function handleForgot(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);

    const { error } = await supabase.auth.resetPasswordForEmail(email, {
      redirectTo: `${window.location.origin}/api/auth/callback?type=recovery`,
    });

    if (error) {
      setError(error.message);
      setLoading(false);
      return;
    }

    setMessage("Password reset link sent to your email.");
    setLoading(false);
  }

  const handleSubmit = mode === "login" ? handleLogin : mode === "signup" ? handleSignup : handleForgot;
  const buttonText = mode === "login" ? "Sign In" : mode === "signup" ? "Create Account" : "Send Reset Link";
  const title = mode === "login" ? "Sign In" : mode === "signup" ? "Create Account" : "Reset Password";

  return (
    <div
      style={{
        minHeight: "100vh",
        background: `linear-gradient(135deg, ${C.navy} 0%, ${C.accent} 100%)`,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "20px",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      <div
        style={{
          background: C.white,
          borderRadius: "16px",
          padding: "48px 40px",
          maxWidth: "420px",
          width: "100%",
          boxShadow: "0 20px 60px rgba(0,0,0,0.3)",
        }}
      >
        {/* Logo */}
        <div style={{ textAlign: "center", marginBottom: "32px" }}>
          <div style={{ fontSize: "40px", marginBottom: "8px" }}>🏠</div>
          <h1 style={{ margin: 0, color: C.navy, fontSize: "24px", fontWeight: 700 }}>
            Property360
          </h1>
          <p style={{ margin: "4px 0 0", color: C.gray, fontSize: "14px" }}>
            Sale Advisor — {title}
          </p>
        </div>

        {/* Success message */}
        {message && (
          <div
            style={{
              background: "#E8F5E9",
              border: "1px solid #A9DFBF",
              borderRadius: "8px",
              padding: "12px 16px",
              marginBottom: "20px",
              color: C.green,
              fontSize: "14px",
            }}
          >
            ✅ {message}
          </div>
        )}

        {/* Error */}
        {error && (
          <div
            style={{
              background: "#FDEDEC",
              border: "1px solid #F1948A",
              borderRadius: "8px",
              padding: "12px 16px",
              marginBottom: "20px",
              color: C.red,
              fontSize: "14px",
            }}
          >
            ❌ {error}
          </div>
        )}

        {/* Form */}
        <div>
          <div style={{ marginBottom: "16px" }}>
            <label style={{ display: "block", fontSize: "13px", color: C.gray, marginBottom: "6px", fontWeight: 600 }}>
              Email
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="mariam@property360re.com"
              required
              style={{
                width: "100%",
                padding: "12px 16px",
                border: "1px solid #D1D5DB",
                borderRadius: "8px",
                fontSize: "15px",
                outline: "none",
                boxSizing: "border-box",
                transition: "border-color 0.2s",
              }}
              onFocus={(e) => (e.target.style.borderColor = C.accent)}
              onBlur={(e) => (e.target.style.borderColor = "#D1D5DB")}
            />
          </div>

          {mode !== "forgot" && (
            <div style={{ marginBottom: "24px" }}>
              <label style={{ display: "block", fontSize: "13px", color: C.gray, marginBottom: "6px", fontWeight: 600 }}>
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                minLength={8}
                style={{
                  width: "100%",
                  padding: "12px 16px",
                  border: "1px solid #D1D5DB",
                  borderRadius: "8px",
                  fontSize: "15px",
                  outline: "none",
                  boxSizing: "border-box",
                  transition: "border-color 0.2s",
                }}
                onFocus={(e) => (e.target.style.borderColor = C.accent)}
                onBlur={(e) => (e.target.style.borderColor = "#D1D5DB")}
              />
            </div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            style={{
              width: "100%",
              padding: "14px",
              background: loading ? C.gray : C.navy,
              color: C.white,
              border: "none",
              borderRadius: "8px",
              fontSize: "16px",
              fontWeight: 600,
              cursor: loading ? "not-allowed" : "pointer",
              transition: "background 0.2s",
            }}
            onMouseOver={(e) => !loading && ((e.target as HTMLButtonElement).style.background = C.accent)}
            onMouseOut={(e) => !loading && ((e.target as HTMLButtonElement).style.background = C.navy)}
          >
            {loading ? "..." : buttonText}
          </button>
        </div>

        {/* Mode switchers */}
        <div style={{ textAlign: "center", marginTop: "24px", fontSize: "14px" }}>
          {mode === "login" && (
            <>
              <button
                onClick={() => { setMode("forgot"); setError(null); setMessage(null); }}
                style={{ background: "none", border: "none", color: C.accent, cursor: "pointer", fontSize: "14px" }}
              >
                Forgot password?
              </button>
              <div style={{ marginTop: "12px", color: C.gray }}>
                No account?{" "}
                <button
                  onClick={() => { setMode("signup"); setError(null); setMessage(null); }}
                  style={{ background: "none", border: "none", color: C.accent, cursor: "pointer", fontSize: "14px", fontWeight: 600 }}
                >
                  Create one
                </button>
              </div>
            </>
          )}
          {mode === "signup" && (
            <div style={{ color: C.gray }}>
              Already have an account?{" "}
              <button
                onClick={() => { setMode("login"); setError(null); setMessage(null); }}
                style={{ background: "none", border: "none", color: C.accent, cursor: "pointer", fontSize: "14px", fontWeight: 600 }}
              >
                Sign in
              </button>
            </div>
          )}
          {mode === "forgot" && (
            <button
              onClick={() => { setMode("login"); setError(null); setMessage(null); }}
              style={{ background: "none", border: "none", color: C.accent, cursor: "pointer", fontSize: "14px" }}
            >
              ← Back to sign in
            </button>
          )}
        </div>

        {/* Footer */}
        <div style={{ textAlign: "center", marginTop: "32px", color: "#9CA3AF", fontSize: "12px" }}>
          Property360 Real Estate — Mariam Shapira
        </div>
      </div>
    </div>
  );
}
