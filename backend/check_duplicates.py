from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_recent_posts():
    print("Fetching last 10 posts...")
    response = supabase.table("posts").select("title, created_at, slug, comment_myan, comment_pyon").order("created_at", desc=True).limit(5).execute()
    
    for post in response.data:
        # Print simplistic output to avoid encoding issues in some terminals
        print(f"Slug: {post['slug']}")
        print(f"Myan: {post.get('comment_myan')}")
        print(f"Pyon: {post.get('comment_pyon')}")
        print("-" * 20)

if __name__ == "__main__":
    check_recent_posts()
