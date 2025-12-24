-- Create polls table for interactive voting
CREATE TABLE IF NOT EXISTS public.polls (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    post_id UUID REFERENCES public.posts(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    votes_a INTEGER DEFAULT 0,
    votes_b INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Add reactions column to posts table to store simulated netizen comments as JSON
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS reactions JSONB DEFAULT '[]'::jsonb;

-- Enable RLS for polls
ALTER TABLE public.polls ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read access to polls" ON public.polls FOR SELECT USING (true);
-- For voting, we allow anyone to update votes (with caution, but for this demo it's fine)
CREATE POLICY "Allow public update to votes" ON public.polls FOR UPDATE USING (true);
