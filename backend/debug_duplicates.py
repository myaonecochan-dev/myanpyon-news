import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_duplicate_details():
    # User provided slugs:
    # japan-record-snow-warning-1226
    # winter-storm-heavy-snow-japan-1226
    
    slugs = ["japan-record-snow-warning-1226", "winter-storm-heavy-snow-japan-1226"]
    
    for slug in slugs:
        res = supabase.table("posts").select("*").ilike("slug", f"{slug}%").execute()
        if res.data:
            post = res.data[0]
            print(f"--- Post: {slug} ---")
            print(f"Title: {post['title']}")
            print(f"Source URL: {post['source_url']}")
            print(f"Created At: {post['created_at']}")
        else:
             print(f"Post not found for slug: {slug}")

if __name__ == "__main__":
    check_duplicate_details()
