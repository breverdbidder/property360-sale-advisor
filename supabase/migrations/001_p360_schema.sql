-- ============================================================================
-- Property360 Sale Advisor — Database Schema
-- Mariam Shapira | Property360 Real Estate
-- Migration 001: Core tables, RLS policies, seed data
-- ============================================================================

-- 1. PROFILES (extends Supabase auth.users)
-- ============================================================================
CREATE TABLE IF NOT EXISTS p360_profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  full_name TEXT,
  role TEXT NOT NULL DEFAULT 'agent' CHECK (role IN ('admin', 'agent', 'viewer')),
  avatar_url TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO p360_profiles (id, email, full_name)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1))
  );
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

DROP TRIGGER IF EXISTS on_auth_user_created ON auth.users;
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- 2. PROPERTIES
-- ============================================================================
CREATE TABLE IF NOT EXISTS p360_properties (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  address TEXT NOT NULL,
  city TEXT,
  state TEXT DEFAULT 'FL',
  zip TEXT,
  parcel_id TEXT,
  property_type TEXT DEFAULT 'single_family'
    CHECK (property_type IN ('single_family','multi_family','condo','townhouse','commercial','land')),
  beds INTEGER,
  baths NUMERIC(3,1),
  sqft INTEGER,
  year_built INTEGER,
  lot_size_sqft INTEGER,
  estimated_value NUMERIC(12,2),
  mortgage_payoff NUMERIC(12,2),
  monthly_rent NUMERIC(10,2),
  occupancy_status TEXT DEFAULT 'occupied'
    CHECK (occupancy_status IN ('occupied','vacant','partial','owner_occupied')),
  notes TEXT,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_p360_properties_user ON p360_properties(user_id);
CREATE INDEX idx_p360_properties_zip ON p360_properties(zip);

-- 3. CHECKLISTS (per-property, per-phase checklist state)
-- ============================================================================
CREATE TABLE IF NOT EXISTS p360_checklists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  property_id UUID REFERENCES p360_properties(id) ON DELETE CASCADE,
  item_id TEXT NOT NULL,          -- e.g. "1-1", "3-4"
  phase_id INTEGER NOT NULL,      -- 1-10
  checked BOOLEAN NOT NULL DEFAULT FALSE,
  checked_at TIMESTAMPTZ,
  notes TEXT,
  ai_confidence NUMERIC(3,2),    -- 0.00-1.00 from doc analysis
  ai_extracted_value TEXT,        -- value extracted by AI
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, property_id, item_id)
);

CREATE INDEX idx_p360_checklists_user ON p360_checklists(user_id);
CREATE INDEX idx_p360_checklists_property ON p360_checklists(property_id);

-- 4. DOCUMENTS (uploaded docs + AI analysis results)
-- ============================================================================
CREATE TABLE IF NOT EXISTS p360_documents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  property_id UUID REFERENCES p360_properties(id) ON DELETE SET NULL,
  filename TEXT NOT NULL,
  file_type TEXT NOT NULL CHECK (file_type IN ('pdf','docx','xlsx','pptx','csv','jpg','png')),
  file_size INTEGER,
  storage_path TEXT,              -- Supabase Storage path
  status TEXT NOT NULL DEFAULT 'uploaded'
    CHECK (status IN ('uploaded','analyzing','done','error')),
  analysis JSONB,                 -- Full AI analysis result
  doc_type TEXT,                  -- AI-detected: "lease", "inspection", "appraisal", etc.
  summary TEXT,                   -- AI-generated summary
  key_findings JSONB DEFAULT '[]',
  warnings JSONB DEFAULT '[]',
  completed_items JSONB DEFAULT '[]', -- items auto-checked by AI
  applied BOOLEAN DEFAULT FALSE,
  error_message TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_p360_documents_user ON p360_documents(user_id);
CREATE INDEX idx_p360_documents_property ON p360_documents(property_id);

-- 5. SESSIONS (track user activity for analytics)
-- ============================================================================
CREATE TABLE IF NOT EXISTS p360_sessions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  property_id UUID REFERENCES p360_properties(id) ON DELETE SET NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ended_at TIMESTAMPTZ,
  actions JSONB DEFAULT '[]',     -- [{action, timestamp, details}]
  progress_snapshot JSONB,        -- {total, checked, critical_checked, score}
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_p360_sessions_user ON p360_sessions(user_id);

-- ============================================================================
-- ROW-LEVEL SECURITY POLICIES
-- ============================================================================

ALTER TABLE p360_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE p360_properties ENABLE ROW LEVEL SECURITY;
ALTER TABLE p360_checklists ENABLE ROW LEVEL SECURITY;
ALTER TABLE p360_documents ENABLE ROW LEVEL SECURITY;
ALTER TABLE p360_sessions ENABLE ROW LEVEL SECURITY;

-- Profiles: users see own profile, admins see all
CREATE POLICY "profiles_select_own" ON p360_profiles
  FOR SELECT USING (auth.uid() = id);
CREATE POLICY "profiles_update_own" ON p360_profiles
  FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "profiles_admin_select" ON p360_profiles
  FOR SELECT USING (
    EXISTS (SELECT 1 FROM p360_profiles WHERE id = auth.uid() AND role = 'admin')
  );

-- Properties: users CRUD own properties only
CREATE POLICY "properties_select_own" ON p360_properties
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "properties_insert_own" ON p360_properties
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "properties_update_own" ON p360_properties
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "properties_delete_own" ON p360_properties
  FOR DELETE USING (auth.uid() = user_id);

-- Checklists: users CRUD own checklists
CREATE POLICY "checklists_select_own" ON p360_checklists
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "checklists_insert_own" ON p360_checklists
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "checklists_update_own" ON p360_checklists
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "checklists_delete_own" ON p360_checklists
  FOR DELETE USING (auth.uid() = user_id);

-- Documents: users CRUD own documents
CREATE POLICY "documents_select_own" ON p360_documents
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "documents_insert_own" ON p360_documents
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "documents_update_own" ON p360_documents
  FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "documents_delete_own" ON p360_documents
  FOR DELETE USING (auth.uid() = user_id);

-- Sessions: users see own sessions
CREATE POLICY "sessions_select_own" ON p360_sessions
  FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "sessions_insert_own" ON p360_sessions
  FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "sessions_update_own" ON p360_sessions
  FOR UPDATE USING (auth.uid() = user_id);

-- ============================================================================
-- UPDATED_AT TRIGGER
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER p360_profiles_updated
  BEFORE UPDATE ON p360_profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER p360_properties_updated
  BEFORE UPDATE ON p360_properties
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER p360_checklists_updated
  BEFORE UPDATE ON p360_checklists
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER p360_documents_updated
  BEFORE UPDATE ON p360_documents
  FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================================
-- STORAGE BUCKET FOR DOCUMENTS
-- ============================================================================
INSERT INTO storage.buckets (id, name, public)
VALUES ('p360-documents', 'p360-documents', false)
ON CONFLICT (id) DO NOTHING;

-- Storage RLS: users can only access own files
CREATE POLICY "p360_docs_select" ON storage.objects
  FOR SELECT USING (
    bucket_id = 'p360-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );
CREATE POLICY "p360_docs_insert" ON storage.objects
  FOR INSERT WITH CHECK (
    bucket_id = 'p360-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );
CREATE POLICY "p360_docs_delete" ON storage.objects
  FOR DELETE USING (
    bucket_id = 'p360-documents' AND
    (storage.foldername(name))[1] = auth.uid()::text
  );

-- ============================================================================
-- DONE
-- ============================================================================
