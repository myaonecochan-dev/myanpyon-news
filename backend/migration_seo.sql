-- Add slug column for SEO-friendly URLs
ALTER TABLE posts ADD COLUMN IF NOT EXISTS slug TEXT UNIQUE;

-- Comment on column
COMMENT ON COLUMN posts.slug IS 'SEO-friendly URL slug (e.g. teacher-exam-2025)';
