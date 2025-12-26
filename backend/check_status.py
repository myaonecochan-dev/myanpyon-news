import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_status():
    print("--- Investigating Snow Posts ---")
    slugs = ["record-snow-hits-japan-holiday-travel-1226", "winter-storm-heavy-snow-japan-1226"]
    res = supabase.table("posts").select("*").in_("slug", slugs).execute()
    
    if not res.data:
        print("Posts not found.")
        return

    for post in res.data:
        print(f"Title: {post['title']}")
        print(f"Slug: {post['slug']}")
        print(f"Source URL: {post['source_url']}")
        print(f"Created At: {post['created_at']}")
        print("-" * 30)

if __name__ == "__main__":
    check_status()
