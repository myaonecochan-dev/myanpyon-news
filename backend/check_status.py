import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_status():
    print("--- Latest 5 Posts Status ---")
    res = supabase.table("posts").select("*").order("created_at", desc=True).limit(5).execute()
    
    if not res.data:
        print("No posts found.")
        return

    for post in res.data:
        print(f"Title: {post['title']}")
        print(f"Slug: {post['slug']}")
        print(f"Created At: {post['created_at']}")
        print(f"Source URL: {post['source_url']}")
        print(f"Myan: {post.get('comment_myan', 'MISSING')[:50]}...")
        print(f"Pyon: {post.get('comment_pyon', 'MISSING')[:50]}...")
        print("-" * 30)

if __name__ == "__main__":
    check_status()
