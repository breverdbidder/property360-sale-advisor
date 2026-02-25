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

    const systemPrompt = `You are a real estate transaction analyst. Analyze property sale documents and determine which checklist items are evidenced.

Respond ONLY with valid JSON, no markdown fences, no preamble:
{
  "docType": "type of document (e.g. Lease Agreement, Appraisal Report, Title Search, Rent Roll)",
  "summary": "2-3 sentences describing document content and relevance",
  "completedItems": [{"id": "item_id", "confidence": 0.7, "extractedValue": "specific value found or null"}],
  "keyFindings": ["finding 1", "finding 2"],
  "warnings": ["warning 1 if any issues found"]
}

Only include completedItems with confidence >= 0.65. Be conservative. Only mark items if document clearly provides evidence.`;

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
