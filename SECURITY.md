# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.x     | ✅        |

## Security Architecture

### Data Handling
- **No server-side data storage**: All checklist state lives in React `useState` — nothing is persisted to any database.
- **No user authentication**: Tool is intended for single-user internal use.
- **No API calls**: The application makes zero external HTTP requests at runtime.
- **No cookies or localStorage**: State is intentionally ephemeral per session.

### Deployment Security
- Deployed on Cloudflare Workers with automatic DDoS protection
- HTTPS enforced by Cloudflare (no plain HTTP)
- No sensitive environment variables required

### Dependencies
- Minimal dependency surface: Next.js, React, React DOM only
- All dependencies pinned to major versions
- No analytics, telemetry, or third-party SDKs

## Reporting a Vulnerability

Contact: Mariam Shapira via Property360 official channels.  
Response SLA: 48 hours for critical, 7 days for low severity.
