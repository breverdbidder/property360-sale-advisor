# Property360 Sale Advisor

**Income-Producing Property Sale Advisor** for Brevard County, FL  
Built by Property360 · Mariam Shapira, Licensed Broker

## Overview

A 10-phase interactive checklist system that guides income property sellers through every step from financial assessment to closing. Built with [Vinext](https://github.com/cloudflare/vinext) — Cloudflare's Vite-based Next.js reimplementation.

## Features

- **10 Phases, 60+ Checkpoints** covering the complete sale lifecycle
- **Critical Item Flagging** — highlights must-complete items with FL statute references
- **Live Sale Readiness Score** — NOT READY → NEARLY READY → READY TO LIST
- **Phase Navigation** — jump directly to any phase
- **Zero Dependencies** beyond Next.js and React — no analytics, no tracking

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Vinext v0.0.8 (Next.js App Router compatible) |
| Runtime | React 19 |
| Language | TypeScript 5 |
| Deployment | Cloudflare Workers (via `wrangler`) |
| Styling | Inline styles (zero CSS framework dependency) |

## Getting Started

```bash
npm install
npm run dev        # → http://localhost:3000
npm run build      # production build
npm run deploy     # → Cloudflare Workers
```

## Security Notes

- No user data transmitted to any server
- All state is in-memory (React useState)
- No authentication required — single-user tool
- No analytics or tracking scripts
- CSP headers via Cloudflare Workers

## Phase Coverage

1. 💰 Financial Assessment
2. 🔍 Property Condition Review
3. 📋 Tenancy & Lease Audit
4. 📈 Income Optimization
5. ⚖️ Legal & Title Prep
6. 🏷️ Valuation & Pricing
7. 📦 Marketing Package
8. 🤝 Offer & Negotiation
9. 🔬 Due Diligence Support
10. 🎉 Closing & Transition

## License

Proprietary — Property360 / Mariam Shapira. All rights reserved.
