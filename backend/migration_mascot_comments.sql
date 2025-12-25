-- Add columns for mascot closing comments
ALTER TABLE posts ADD COLUMN IF NOT EXISTS comment_myan TEXT;
ALTER TABLE posts ADD COLUMN IF NOT EXISTS comment_pyon TEXT;
