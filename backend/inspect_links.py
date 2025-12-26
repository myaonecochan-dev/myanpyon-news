
import os
import re
import json
from supabase_client import supabase

print("Inspecting Switch 2 Link Data...")
res = supabase.table("products").select("name, moshimo_html").eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()

if res.data:
    html = res.data[0]['moshimo_html']
    match = re.search(r'msmaflink\(({.*?})\);', html)
    if match:
        config = json.loads(match.group(1))
        # Check the button links
        buttons = config.get('b_l', [])
        for btn in buttons:
            print(f"Shop: {btn.get('s_n')}")
            print(f"URL: {btn.get('u_url')}")
            # Check if it looks like an affiliate link (moshimo/rakuten tracker)
            # Usually Moshimo links go through a tracker or require the script to generate it.
            # Use 'u' (main url) as well
        print(f"Main URL (u): {config.get('u', {}).get('u')}")
else:
    print("Product not found.")
