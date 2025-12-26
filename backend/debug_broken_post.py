
import os
from supabase import create_client, Client

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def debug_broken_post():
    print("--- Inspecting 'Muscular Dystrophy' Post ---")
    res = supabase.table("posts").select("*").ilike("title", "%筋ジストロフィー%").execute()
    
    if res.data:
        post = res.data[0]
        print(f"ID: {post['id']}")
        print(f"Title: {post['title']}")
        print(f"Image URL: {post['image_url']}")
        
        # Check Polls
        print("\n--- Checking Polls ---")
        poll_res = supabase.table("polls").select("*").eq("post_id", post['id']).execute()
        if poll_res.data:
            print(f"Poll Found: {poll_res.data[0]}")
        else:
            print("NO POLL FOUND.")
    else:
        print("Post not found.")

if __name__ == "__main__":
    debug_broken_post()
