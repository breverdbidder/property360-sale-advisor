import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Hardcode NEXT_PUBLIC_ vars to prevent CF Pages env overrides
  // These are PUBLIC keys by design (Supabase anon key is client-safe)
  env: {
    NEXT_PUBLIC_SUPABASE_URL: "https://mocerqjnksmhcjzxrewo.supabase.co",
    NEXT_PUBLIC_SUPABASE_ANON_KEY: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1vY2VycWpua3NtaGNqenhyZXdvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjQ1MzI1MjYsImV4cCI6MjA4MDEwODUyNn0.ySFJIOngWWB0aqYra4PoGFuqcbdHOx1ZV6T9-klKQDw",
  },
};

export default nextConfig;
