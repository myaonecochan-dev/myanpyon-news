import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def list_and_clean_duplicates():
    print("Listing Makihara posts...")
    res = supabase.table("posts").select("id, title, slug, source_url, created_at, comment_myan").ilike("title", "%牧原%").order("created_at", desc=True).execute()
    
    if not res.data:
        print("No posts found.")
        return

    print(f"Found {len(res.data)} posts.")
    for i, post in enumerate(res.data):
        print(f"[{i}] ID: {post['id']}")
        print(f"    Slug: {post['slug']}")
        print(f"    Created: {post['created_at']}")
        print(f"    Source: {post['source_url']}")
        print(f"    Myan: {post['comment_myan']}")
        print("-" * 20)

    # Deletion Logic: Keep the first one (latest), delete others
    if len(res.data) > 1:
        print("Duplicates detected. Deleting older ones...")
        for post in res.data[1:]:
             print(f"Deleting {post['id']}...")
             supabase.table("posts").delete().eq("id", post["id"]).execute()
        print("Cleanup complete.")
    else:
        print("No duplicates to delete.")

if __name__ == "__main__":
    list_and_clean_duplicates()
