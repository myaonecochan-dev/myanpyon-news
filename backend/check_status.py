import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_status():
    print("--- Investigating Incomplete Post ---")
    slug = "child-grandparents-medicine-ingestion-1226"
    res = supabase.table("posts").select("*").eq("slug", slug).execute()
    
    if not res.data:
        print("Post not found.")
        return

    post = res.data[0]
    print(f"Title: {post['title']}")
    print(f"image_url (DB): {post.get('image_url', 'MISSING')}")
    print(f"reactions (DB): {post.get('reactions', 'MISSING')}")
    print(f"Created At: {post['created_at']}")
    
    # Check polls
    poll_res = supabase.table("polls").select("*").eq("post_id", post["id"]).execute()
    if poll_res.data:
        print(f"Poll found: {poll_res.data[0]['question']}")
    else:
        print("Poll NOT found.")
    print("-" * 30)

if __name__ == "__main__":
    check_status()
