import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fix_holiday_year():
    print("Searching for Holiday post...")
    res = supabase.table("posts").select("*").ilike("title", "%連休%").order("created_at", desc=True).limit(1).execute()
    
    if not res.data:
        print("Post NOT found.")
        return

    post = res.data[0]
    print(f"Found: {post['title']}")
    
    # Check Pyon's comment
    pyon = post.get('comment_pyon', '')
    myan = post.get('comment_myan', '')
    content = post.get('content', '')
    
    print(f"Current Pyon: {pyon}")
    
    updates = {}
    if "2024" in pyon:
        print("Found 2024 in Pyon comment. Fixing...")
        updates["comment_pyon"] = pyon.replace("2024", "2025")
        
    if "2024" in myan:
        print("Found 2024 in Myan comment. Fixing...")
        updates["comment_myan"] = myan.replace("2024", "2025")

    if "2024" in content:
        print("Found 2024 in Content using simple replace (might be risky if legitimate 2024 ref exists, but for 9-day holiday likely error). Fixing...")
        updates["content"] = content.replace("2024", "2025")

    if updates:
        supabase.table("posts").update(updates).eq("id", post['id']).execute()
        print(f"Fixed {len(updates)} fields.")
    else:
        print("No '2024' found in key fields. Maybe checking logic needs adjustment.")

if __name__ == "__main__":
    fix_holiday_year()
