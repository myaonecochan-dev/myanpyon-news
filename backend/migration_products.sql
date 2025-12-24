-- Create products table
CREATE TABLE IF NOT EXISTS public.products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    price TEXT,
    image_url TEXT,
    amazon_link TEXT,
    rakuten_link TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now()) NOT NULL
);

-- Enable RLS
ALTER TABLE public.products ENABLE ROW LEVEL SECURITY;

-- Policy: Everyone can read active products (modified to allow reading all for simplicity if needed, but active=true is better)
CREATE POLICY "Allow public read access" ON public.products
    FOR SELECT USING (true);

-- Policy: Only authenticated (service_role/admin) can insert/update/delete
-- For simplicity in this app context, we might rely on the client using service_role for admin tasks or anon for read.
-- If we want admin dashboard to write, we need a policy for that.
-- For now, let's allow anon read, and we will use service role for writes in admin scripts.

-- Insert dummy data if table is empty
INSERT INTO public.products (name, price, image_url, amazon_link, rakuten_link, active)
SELECT 'Dell 4Kモニター 27インチ U2720QM', '¥64,800', 'https://m.media-amazon.com/images/I/61yFkmwMh-L._AC_SX679_.jpg', 'https://www.amazon.co.jp/', NULL, true
WHERE NOT EXISTS (SELECT 1 FROM public.products);

INSERT INTO public.products (name, price, image_url, amazon_link, rakuten_link, active)
SELECT 'Anker Soundcore Liberty 4', '¥14,990', 'https://m.media-amazon.com/images/I/51r2K-N2+HL._AC_SX679_.jpg', 'https://www.amazon.co.jp/', 'https://www.rakuten.co.jp/', true
WHERE NOT EXISTS (SELECT 1 FROM public.products LIMIT 1 OFFSET 1);
