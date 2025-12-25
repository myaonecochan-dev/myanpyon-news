-- Add source_url column to posts table if it doesn't exist
ALTER TABLE posts 
ADD COLUMN IF NOT EXISTS source_url TEXT;

-- Create an index on source_url for faster lookups
CREATE INDEX IF NOT EXISTS idx_posts_source_url ON posts(source_url);
