// lib/supabase/useChecklist.ts
"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { createClient } from "./client";

interface CheckedState {
  [itemId: string]: boolean;
}

/**
 * Persists checklist state to Supabase p360_checklists table.
 * Falls back to in-memory state if no user session.
 * Debounces writes to avoid hammering the DB.
 */
export function useChecklist(propertyId?: string) {
  const [checked, setChecked] = useState<CheckedState>({});
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const pendingRef = useRef<Map<string, boolean>>(new Map());
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const supabase = createClient();

  // Load saved state on mount
  useEffect(() => {
    async function load() {
      const { data: { user } } = await supabase.auth.getUser();
      if (!user) { setLoading(false); return; }

      let query = supabase
        .from("p360_checklists")
        .select("item_id, checked, notes, ai_confidence, ai_extracted_value")
        .eq("user_id", user.id);

      if (propertyId) {
        query = query.eq("property_id", propertyId);
      } else {
        query = query.is("property_id", null);
      }

      const { data, error } = await query;
      if (error) {
        console.error("Failed to load checklists:", error.message);
        setLoading(false);
        return;
      }

      const state: CheckedState = {};
      (data || []).forEach((row) => {
        state[row.item_id] = row.checked;
      });
      setChecked(state);
      setLoading(false);
    }
    load();
  }, [propertyId]);

  // Flush pending changes to Supabase
  const flush = useCallback(async () => {
    if (pendingRef.current.size === 0) return;

    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    setSyncing(true);
    const entries = Array.from(pendingRef.current.entries());
    pendingRef.current.clear();

    const rows = entries.map(([itemId, isChecked]) => ({
      user_id: user.id,
      property_id: propertyId || null,
      item_id: itemId,
      phase_id: parseInt(itemId.split("-")[0], 10),
      checked: isChecked,
      checked_at: isChecked ? new Date().toISOString() : null,
    }));

    const { error } = await supabase
      .from("p360_checklists")
      .upsert(rows, { onConflict: "user_id,property_id,item_id" });

    if (error) {
      console.error("Failed to sync checklists:", error.message);
    }
    setSyncing(false);
  }, [propertyId]);

  // Toggle a checklist item (debounced persist)
  const toggle = useCallback(
    (itemId: string) => {
      setChecked((prev) => {
        const next = { ...prev, [itemId]: !prev[itemId] };
        pendingRef.current.set(itemId, next[itemId]);

        // Debounce: flush after 500ms of no toggles
        if (timerRef.current) clearTimeout(timerRef.current);
        timerRef.current = setTimeout(flush, 500);

        return next;
      });
    },
    [flush]
  );

  // Bulk set from AI analysis
  const applyAIResults = useCallback(
    (items: { id: string; confidence: number; extractedValue?: string }[]) => {
      setChecked((prev) => {
        const next = { ...prev };
        items.forEach((item) => {
          if (item.confidence >= 0.7) {
            next[item.id] = true;
            pendingRef.current.set(item.id, true);
          }
        });
        if (timerRef.current) clearTimeout(timerRef.current);
        timerRef.current = setTimeout(flush, 300);
        return next;
      });
    },
    [flush]
  );

  // Force sync on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      flush();
    };
  }, [flush]);

  return { checked, toggle, applyAIResults, loading, syncing };
}
