import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def debug_holiday():
    print("Checking Holiday post...")
    # Search for "連休" (Consecutive Holidays) or "9連休"
    res = supabase.table("posts").select("*").ilike("title", "%連休%").order("created_at", desc=True).limit(1).execute()
    
    if not res.data:
        print("Post NOT found.")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    val_myan = post.get('comment_myan')
    val_pyon = post.get('comment_pyon')
    
    print(f"DB Value Myan: '{val_myan}'")
    print(f"DB Value Pyon: '{val_pyon}'")

    if not val_myan or str(val_myan) == "None":
         print("ALERT: Comments are MISSING!")
    else:
         print("SUCCESS: Comments exist! Final Verification Complete.")

if __name__ == "__main__":
    debug_holiday()
