
import os
import re
import json
from supabase_client import supabase

print("Inspecting Switch 2 HTML Structure...")
res = supabase.table("products").select("name, moshimo_html").eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()

if res.data:
    html = res.data[0]['moshimo_html']
    # Extract JSON config from msmaflink({...})
    match = re.search(r'msmaflink\(({.*?})\);', html)
    if match:
        config_str = match.group(1)
        try:
            config = json.loads(config_str)
            print(f"Size Param (s): {config.get('s')}")
            print(f"Images (p): {config.get('p')}")
            print(f"Image Count: {len(config.get('p', []))}")
        except json.JSONDecodeError as e:
            print(f"JSON Error: {e}")
            print(f"Raw Config extraction: {config_str[:100]}...")
    else:
        print("Could not find msmaflink config.")
else:
    print("Product not found.")
