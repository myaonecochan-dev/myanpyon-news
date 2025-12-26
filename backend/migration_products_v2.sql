-- Add impression tracker and custom HTML support to products table
ALTER TABLE public.products 
ADD COLUMN IF NOT EXISTS rakuten_impression_url TEXT,
ADD COLUMN IF NOT EXISTS amazon_impression_url TEXT,
ADD COLUMN IF NOT EXISTS moshimo_html TEXT;

COMMENT ON COLUMN public.products.rakuten_impression_url IS 'URL for Rakuten impression tracking pixel';
COMMENT ON COLUMN public.products.amazon_impression_url IS 'URL for Amazon impression tracking pixel';
COMMENT ON COLUMN public.products.moshimo_html IS 'Full HTML snippet from Moshimo (e.g. Easy Link)';
