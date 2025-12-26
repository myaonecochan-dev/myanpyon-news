
import os
import urllib.parse
from supabase import create_client, Client

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def fix_image_stable():
    target_title_part = "筋ジストロフィー"
    print(f"--- Fixing Image (Stable Provider) for: {target_title_part} ---")
    
    res = supabase.table("posts").select("id").ilike("title", f"%{target_title_part}%").execute()
    if not res.data:
        print("Post not found.")
        return

    post_id = res.data[0]['id']
    
    # Use reliable PICSUM
    new_image_url = "https://picsum.photos/seed/brothers_love/1200/630"
    
    print(f"New Stable URL: {new_image_url}")
    supabase.table("posts").update({"image_url": new_image_url}).eq("id", post_id).execute()
    print("Update Done.")

if __name__ == "__main__":
    fix_image_stable()
