// lib/supabase/useDocuments.ts
"use client";

import { useState, useCallback } from "react";
import { createClient } from "./client";

interface DocRecord {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: "uploaded" | "analyzing" | "done" | "error";
  doc_type?: string;
  summary?: string;
  key_findings?: string[];
  warnings?: string[];
  completed_items?: { id: string; confidence: number; extractedValue?: string }[];
  applied: boolean;
  error_message?: string;
  created_at: string;
}

export function useDocuments(propertyId?: string) {
  const [docs, setDocs] = useState<DocRecord[]>([]);
  const [loading, setLoading] = useState(false);
  const supabase = createClient();

  // Load saved documents
  const loadDocs = useCallback(async () => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return;

    setLoading(true);
    let query = supabase
      .from("p360_documents")
      .select("*")
      .eq("user_id", user.id)
      .order("created_at", { ascending: false });

    if (propertyId) {
      query = query.eq("property_id", propertyId);
    }

    const { data, error } = await query;
    if (!error && data) {
      setDocs(data as DocRecord[]);
    }
    setLoading(false);
  }, [propertyId]);

  // Save a new document record
  const saveDoc = useCallback(async (doc: {
    filename: string;
    file_type: string;
    file_size: number;
    status: string;
    analysis?: any;
    doc_type?: string;
    summary?: string;
    key_findings?: string[];
    warnings?: string[];
    completed_items?: any[];
    applied?: boolean;
    error_message?: string;
  }) => {
    const { data: { user } } = await supabase.auth.getUser();
    if (!user) return null;

    const { data, error } = await supabase
      .from("p360_documents")
      .insert({
        user_id: user.id,
        property_id: propertyId || null,
        ...doc,
      })
      .select()
      .single();

    if (error) {
      console.error("Failed to save document:", error.message);
      return null;
    }

    setDocs((prev) => [data as DocRecord, ...prev]);
    return data;
  }, [propertyId]);

  // Update document status/analysis
  const updateDoc = useCallback(async (docId: string, updates: Partial<DocRecord>) => {
    const { error } = await supabase
      .from("p360_documents")
      .update(updates)
      .eq("id", docId);

    if (!error) {
      setDocs((prev) =>
        prev.map((d) => (d.id === docId ? { ...d, ...updates } : d))
      );
    }
  }, []);

  return { docs, loadDocs, saveDoc, updateDoc, loading };
}
