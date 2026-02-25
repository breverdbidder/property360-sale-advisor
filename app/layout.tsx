import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Property360 Sale Advisor | Mariam Shapira",
  description: "Income-Producing Property Sale Advisor — 10-Phase System",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif", background: "#f8f9fa" }}>
        {children}
      </body>
    </html>
  );
}
