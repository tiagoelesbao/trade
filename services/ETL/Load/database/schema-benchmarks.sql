-- Viral ETL Service: Benchmarking Schema
-- Enable pgvector extension for semantic search on content analysis
CREATE EXTENSION IF NOT EXISTS vector;

-- Enums for content categorization
DO $$ BEGIN
    CREATE TYPE platform_type AS ENUM ('instagram', 'tiktok', 'youtube', 'linkedin');
    CREATE TYPE content_category AS ENUM ('video', 'image', 'carousel', 'text');
    CREATE TYPE processing_status AS ENUM ('pending', 'processing', 'completed', 'error');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Main Benchmarks table
CREATE TABLE IF NOT EXISTS public.benchmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform platform_type NOT NULL,
    original_url TEXT UNIQUE NOT NULL,
    author_handle TEXT,
    content_type content_category DEFAULT 'video',
    
    -- Post Metadata (Likes, Views, Shares, Original Caption)
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- AI Multimodal Analysis (Hook, Transcription, Visual Dynamics)
    analysis JSONB DEFAULT '{}'::jsonb,
    
    -- Vector Embedding (1536 is standard for OpenAI, but can be adjusted for Gemini/Others)
    embedding vector(1536),
    
    status processing_status DEFAULT 'pending',
    error_log TEXT,
    
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Performance Indexes
CREATE INDEX IF NOT EXISTS idx_benchmarks_platform ON public.benchmarks(platform);
CREATE INDEX IF NOT EXISTS idx_benchmarks_status ON public.benchmarks(status);
CREATE INDEX IF NOT EXISTS idx_benchmarks_url ON public.benchmarks(original_url);

-- Vector Index (HNSW for high performance similarity search)
-- Note: Requires pgvector 0.5.0+
CREATE INDEX IF NOT EXISTS idx_benchmarks_embedding ON public.benchmarks USING hnsw (embedding vector_cosine_ops);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

DO $$ BEGIN
    CREATE TRIGGER update_benchmarks_updated_at
        BEFORE UPDATE ON public.benchmarks
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column();
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
