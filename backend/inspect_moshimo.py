
import os
from supabase_client import supabase

print("Inspecting Switch 2 HTML...")
res = supabase.table("products").select("name, moshimo_html").eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()

if res.data:
    print(f"HTML Content: {res.data[0]['moshimo_html']}")
else:
    print("Product not found.")
