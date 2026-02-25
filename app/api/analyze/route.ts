export const runtime = "edge";

import Anthropic from "@anthropic-ai/sdk";
import { PHASES } from "@/lib/phases";

const client = new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY });

// Build a flat map of all checklist items for the AI to reference
const ALL_ITEMS = PHASES.flatMap(p => p.items.map(i => ({
  id: i.id,
  phase: p.id,
  phaseTitle: p.title,
  text: i.text,
  critical: i.critical,
})));

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const { content, fileName, fileType } = body as {
      content: string;        // text content extracted client-side
      fileName: string;
      fileType: "pdf" | "docx" | "xlsx";
    };

    if (!content || content.length < 10) {
      return Response.json({ error: "Document content too short or empty" }, { status: 400 });
    }

    const itemsJson = JSON.stringify(ALL_ITEMS.map(i => ({ id: i.id, text: i.text, phase: i.phaseTitle })));

    const prompt = `You are a real estate transaction analyst reviewing documents for an income-producing property sale.

DOCUMENT NAME: ${fileName}
DOCUMENT TYPE: ${fileType.toUpperCase()}
DOCUMENT CONTENT:
---
${content.slice(0, 12000)}
---

CHECKLIST ITEMS (JSON):
${itemsJson}

TASK: Analyze this document and determine which checklist items it provides evidence for completing.

For each item that this document supports, extract the relevant data value found.

Respond ONLY with valid JSON in this exact format:
{
  "docType": "string (what type of document is this - e.g. 'Lease Agreement', 'Appraisal Report', 'Title Search', 'Rent Roll', 'Tax Certificate', etc.)",
  "summary": "2-3 sentence summary of what this document contains and its relevance to the sale",
  "completedItems": [
    {
      "id": "phase_item_id",
      "confidence": 0.0-1.0,
      "extractedValue": "the specific data found (dollar amount, date, name, etc.) or null if just confirmed present"
    }
  ],
  "keyFindings": [
    "bullet point finding 1",
    "bullet point finding 2"
  ],
  "warnings": [
    "any red flags or issues found in this document that the seller should know about"
  ]
}

Only include items with confidence >= 0.6. Be conservative - only mark items complete if there is clear evidence.`;

    const message = await client.messages.create({
      model: "claude-sonnet-4-20250514",
      max_tokens: 2000,
      messages: [{ role: "user", content: prompt }],
    });

    const rawText = message.content[0].type === "text" ? message.content[0].text : "";
    
    // Parse JSON response
    const jsonMatch = rawText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      return Response.json({ error: "AI returned invalid response", raw: rawText.slice(0, 200) }, { status: 500 });
    }
    
    const analysis = JSON.parse(jsonMatch[0]);
    return Response.json({ success: true, analysis });
    
  } catch (err) {
    const message = err instanceof Error ? err.message : "Unknown error";
    return Response.json({ error: message }, { status: 500 });
  }
}
