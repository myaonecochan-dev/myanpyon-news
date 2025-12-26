
import os
from supabase import create_client, Client
from dotenv import load_dotenv

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(URL, KEY)

def find_missing_post():
    print("--- Searching for 'Truck' (トラック) posts ---")
    # Search for titles containing "トラック" (Truck) or just list latest 10 to see if it's buried
    res = supabase.table("posts").select("title, created_at").ilike("title", "%トラック%").execute()
    
    if res.data:
        print(f"Found {len(res.data)} posts matching 'トラック':")
        for post in res.data:
            print(f"- {post['title']} ({post['created_at']})")
    else:
        print("No posts found with 'トラック' in title.")

    print("\n--- Listing Latest 10 Posts (Raw) ---")
    res_latest = supabase.table("posts").select("title, created_at").order("created_at", desc=True).limit(10).execute()
    for post in res_latest.data:
        print(f"- {post['created_at']}: {post['title']}")

if __name__ == "__main__":
    find_missing_post()
