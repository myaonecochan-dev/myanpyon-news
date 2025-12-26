
import os
from supabase_client import supabase

print("Checking all active products...")
res = supabase.table("products").select("name, rakuten_link, amazon_link, moshimo_html").eq("active", True).execute()

for p in res.data:
    print(f"Name: {p['name']}")
    print(f"  Rakuten: {p.get('rakuten_link')}")
    print(f"  Moshimo: {'Has HTML' if p.get('moshimo_html') else 'None'}")
    print("-" * 20)
