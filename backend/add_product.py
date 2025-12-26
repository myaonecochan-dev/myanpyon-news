import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Use environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_KEY:
    print("Error: SUPABASE_KEY not found in environment variables.")
    sys.exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def add_product():
    print("--- Add New Affiliate Product ---")
    name = input("Product Name: ")
    price = input("Price (e.g., ¥1,200): ")
    image_url = input("Image URL: ")
    amazon_link = input("Amazon Affiliate Link (Optional): ")
    amazon_impression = input("Amazon Impression URL (Optional): ")
    rakuten_link = input("Rakuten Affiliate Link (Optional): ")
    rakuten_impression = input("Rakuten Impression URL (Optional): ")
    moshimo_html = input("Moshimo HTML Snippet (Optional): ")

    data = {
        "name": name,
        "price": price,
        "image_url": image_url,
        "amazon_link": amazon_link if amazon_link else None,
        "amazon_impression_url": amazon_impression if amazon_impression else None,
        "rakuten_link": rakuten_link if rakuten_link else None,
        "rakuten_impression_url": rakuten_impression if rakuten_impression else None,
        "moshimo_html": moshimo_html if moshimo_html else None,
        "active": True
    }

    try:
        res = supabase.table("products").insert(data).execute()
        if res.data:
            print(f"\nSuccessfully added product: {res.data[0]['name']}")
            print(f"ID: {res.data[0]['id']}")
        else:
            print("\nFailed to add product (no data returned).")
    except Exception as e:
        print(f"\nError inserting to Supabase: {e}")

if __name__ == "__main__":
    add_product()
