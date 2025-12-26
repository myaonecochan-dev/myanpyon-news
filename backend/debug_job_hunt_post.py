import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_post():
    slug = "government-reviews-job-hunt-rules-1226" # Derived from user URL (assuming ID might be appended or part of slug)
    # User URL: https://myanpyonsokumato.com/post/government-reviews-job-hunt-rules-1226
    # The slug in DB is likely just "government-reviews-job-hunt-rules-1226"
    
    print(f"Checking post with slug: {slug}")
    
    res = supabase.table("posts").select("*").eq("slug", slug).execute()
    if res.data:
        post = res.data[0]
        print(f"Title: {post['title']}")
        print(f"Created At: {post['created_at']}")
        print(f"Source URL: {post.get('source_url')}")
    else:
        # Try without ID if needed, or searching likeness
        print("Exact slug match failed. Searching partial...")
        res = supabase.table("posts").select("*").ilike("slug", "government-reviews-job-hunt%").execute()
        if res.data:
            post = res.data[0]
            print(f"Found nearby match: {post['slug']}")
            print(f"Title: {post['title']}")
            print(f"Created At: {post['created_at']}")
        else:
            print("No matching post found.")

if __name__ == "__main__":
    check_post()
