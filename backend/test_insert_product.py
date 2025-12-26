
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    # Fallback values from collector.py if env vars are missing in this context
    url = "https://ufawzveswbnaqvfvezbb.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(url, key)

product_data = {
    "name": "Test Rakuten Product",
    "price": "1000",
    "image_url": "https://example.com/image.jpg",
    "rakuten_link": "https://rakuten.co.jp/item",
    "rakuten_impression_url": "https://rakuten.co.jp/tracker.gif",
    "amazon_impression_url": "https://amazon.co.jp/tracker.gif",
    "moshimo_html": "<div>Test Moshimo HTML</div>",
    "active": True
}

try:
    print("Inserting test product...")
    data = supabase.table("products").insert(product_data).execute()
    print(f"Success! Inserted product: {data.data}")
except Exception as e:
    print(f"Insertion failed: {e}")
