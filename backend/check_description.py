
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def check_descriptions():
    # Check the reported post: Child/Grandparents (from URL/Screenshot)
    # Title likely similar to "【話題】「お菓子と間違えた…」子が祖父母の薬を誤飲する事故が"
    target_part = "お菓子と間違えた"
    print(f"--- Checking Description for: {target_part} ---")
    
    res = supabase.table("posts").select("id, title, description, content").ilike("title", f"%{target_part}%").execute()
    if not res.data:
        print("Post not found.")
    else:
        for p in res.data:
            desc = p.get('description')
            print(f"Title: {p['title']}")
            print(f"Description: '{desc}' (Type: {type(desc)})")
            print(f"Content Length: {len(p.get('content') or '')}")
            print("-" * 20)

if __name__ == "__main__":
    check_descriptions()
