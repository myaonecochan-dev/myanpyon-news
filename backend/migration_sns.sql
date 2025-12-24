-- Migration to add SNS columns to posts table
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS tweet_text text;
ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS tweet_posted_at timestamptz;
