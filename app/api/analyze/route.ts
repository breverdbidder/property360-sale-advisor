export const runtime = "edge";

import { PHASES } from "@/lib/phases";

const ALL_ITEMS = PHASES.flatMap(p => p.items.map(i => ({
  id: i.id, phase: p.id, phaseTitle: p.title, text: i.text, critical: i.critical,
})));

export async function POST(request: Request) {
  try {
    const body = await request.json() as { content: string; fileName: string; fileType: string };
    const { content, fileName, fileType } = body;

    if (!content || content.length < 10) {
      return Response.json({ error: "Document content too short" }, { status: 400 });
    }

    const apiKey = (process.env as Record<string, string>).ANTHROPIC_API_KEY;
    if (!apiKey) {
      return Response.json({ error: "ANTHROPIC_API_KEY not configured" }, { status: 500 });
    }

    const itemsJson = JSON.stringify(ALL_ITEMS.map(i => ({ id: i.id, text: i.text, phase: i.phaseTitle })));

    // Handle PDF base64 as a vision document, otherwise text
    const isPdf = content.startsWith("__PDF_BASE64__:");
    const pdfBase64 = isPdf ? content.replace("__PDF_BASE64__:", "") : null;
    const textContent = isPdf ? null : content.slice(0, 12000);

    const userContent = isPdf && pdfBase64 ? [
      { type: "document", source: { type: "base64", media_type: "application/pdf", data: pdfBase64 } },
      { type: "text", text: `Document name: ${fileName}\n\nChecklist items:\n${itemsJson}\n\nAnalyze this PDF and return JSON as instructed.` }
    ] : [
      { type: "text", text: `Document name: ${fileName}\nType: ${fileType.toUpperCase()}\n\nContent:\n---\n${textContent}\n---\n\nChecklist items:\n${itemsJson}\n\nAnalyze and return JSON as instructed.` }
    ];

    const systemPrompt = `You are a real estate transaction analyst specializing in Florida income property sales. You analyze documents for Brevard County, FL property transactions managed by Property360.

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

    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 2000,
        system: systemPrompt,
        messages: [{ role: "user", content: userContent }],
      }),
    });

    if (!res.ok) {
      const errText = await res.text();
      return Response.json({ error: `Anthropic API error ${res.status}: ${errText.slice(0, 200)}` }, { status: 500 });
    }

    const aiData = await res.json() as { content: { type: string; text: string }[] };
    const rawText = aiData.content?.[0]?.text || "";

    // Parse JSON - strip any accidental markdown fences
    const clean = rawText.replace(/```json\s*/gi, "").replace(/```\s*/g, "").trim();
    const jsonMatch = clean.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      return Response.json({ error: "AI returned no valid JSON", preview: rawText.slice(0, 200) }, { status: 500 });
    }

    const analysis = JSON.parse(jsonMatch[0]);
    return Response.json({ success: true, analysis });

  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return Response.json({ error: message }, { status: 500 });
  }
}
