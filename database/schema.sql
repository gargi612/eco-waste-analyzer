-- =========================================================================================
-- SUPABASE DATABASE SETUP SCRIPT
-- Project: AI-Based Waste Segregation & Carbon Footprint Analyzer
-- =========================================================================================

-- Enable UUID extension if not present
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- -----------------------------------------------------------------------------------------
-- 1. PREDICTIONS LOG (Raw Telemetry)
-- -----------------------------------------------------------------------------------------
CREATE TABLE public.predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL,
    category TEXT NOT NULL CHECK (category IN ('biodegradable', 'recyclable', 'hazardous')),
    confidence FLOAT NOT NULL,
    weight_grams FLOAT NOT NULL DEFAULT 0.0,
    co2_saved_grams FLOAT NOT NULL DEFAULT 0.0,
    eco_fact TEXT
);

-- Index for faster analytics querying by time and category
CREATE INDEX idx_predictions_category on public.predictions (category);
CREATE INDEX idx_predictions_created_at on public.predictions (created_at);

-- -----------------------------------------------------------------------------------------
-- 2. ANALYTICS_DAILY (Aggregated by day for charts)
-- -----------------------------------------------------------------------------------------
CREATE TABLE public.analytics_daily (
    date DATE PRIMARY KEY DEFAULT CURRENT_DATE,
    total_scans INTEGER DEFAULT 0,
    co2_saved_total FLOAT DEFAULT 0.0,
    biodegradable_count INTEGER DEFAULT 0,
    recyclable_count INTEGER DEFAULT 0,
    hazardous_count INTEGER DEFAULT 0
);

-- -----------------------------------------------------------------------------------------
-- 3. STORED PROCEDURE / TRIGGER (Auto-update Daily Analytics)
-- -----------------------------------------------------------------------------------------
-- This trigger automatically rolls up the predictions table into the analytics_daily table.
CREATE OR REPLACE FUNCTION update_daily_analytics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.analytics_daily (
        date, 
        total_scans, 
        co2_saved_total, 
        biodegradable_count, 
        recyclable_count, 
        hazardous_count
    )
    VALUES (
        CURRENT_DATE,
        1,
        NEW.co2_saved_grams,
        CASE WHEN NEW.category = 'biodegradable' THEN 1 ELSE 0 END,
        CASE WHEN NEW.category = 'recyclable' THEN 1 ELSE 0 END,
        CASE WHEN NEW.category = 'hazardous' THEN 1 ELSE 0 END
    )
    ON CONFLICT (date) DO UPDATE SET
        total_scans = public.analytics_daily.total_scans + 1,
        co2_saved_total = public.analytics_daily.co2_saved_total + NEW.co2_saved_grams,
        biodegradable_count = public.analytics_daily.biodegradable_count + CASE WHEN NEW.category = 'biodegradable' THEN 1 ELSE 0 END,
        recyclable_count = public.analytics_daily.recyclable_count + CASE WHEN NEW.category = 'recyclable' THEN 1 ELSE 0 END,
        hazardous_count = public.analytics_daily.hazardous_count + CASE WHEN NEW.category = 'hazardous' THEN 1 ELSE 0 END;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_analytics
AFTER INSERT ON public.predictions
FOR EACH ROW
EXECUTE FUNCTION update_daily_analytics();

-- -----------------------------------------------------------------------------------------
-- 4. ROW LEVEL SECURITY (RLS) POLICIES
-- -----------------------------------------------------------------------------------------
-- Enable RLS on both tables
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.analytics_daily ENABLE ROW LEVEL SECURITY;

-- Allow ONLY the Backend (using Service Role Key) to insert new predictions
CREATE POLICY "Allow Service Role Insert Only" ON public.predictions
    FOR INSERT
    TO service_role
    WITH CHECK (true);

-- Allow Anonymous (frontend) read-access to the analytics
CREATE POLICY "Allow Public Analytics Read" ON public.analytics_daily
    FOR SELECT
    TO public
    USING (true);

-- Allow Public select on predictions if you want historical data feeds
CREATE POLICY "Allow Public Predictions Read" ON public.predictions
    FOR SELECT
    TO public
    USING (true);
