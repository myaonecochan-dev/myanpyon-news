
import os
import random
import urllib.parse
from supabase import create_client, Client

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def repair_post():
    target_title_part = "筋ジストロフィー"
    print(f"--- Repairing Post: {target_title_part} ---")
    
    # 1. Find Post
    res = supabase.table("posts").select("*").ilike("title", f"%{target_title_part}%").execute()
    if not res.data:
        print("Post not found.")
        return

    post = res.data[0]
    post_id = post['id']
    print(f"Found Post ID: {post_id}")
    
    # 2. Update Image URL (Use Pollinations)
    # Prompt: "Brothers supporting muscular dystrophy family love heartwarming"
    prompt = "Brothers supporting muscular dystrophy family love heartwarming anime style"
    clean_prompt = urllib.parse.quote(prompt)
    new_image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width=1200&height=630&nologo=true&seed={random.randint(0, 999)}"
    
    print(f"New Image URL: {new_image_url}")
    supabase.table("posts").update({"image_url": new_image_url}).eq("id", post_id).execute()
    
    # 3. Check/Insert Poll
    poll_res = supabase.table("polls").select("*").eq("post_id", post_id).execute()
    if not poll_res.data:
        print("Inserting Missing Poll...")
        poll_data = {
            "post_id": post_id,
            "question": "この兄弟の絆についてどう思いますか？",
            "option_a": "とても感動した",
            "option_b": "応援したい"
        }
        supabase.table("polls").insert(poll_data).execute()
    else:
        print("Poll already exists.")

if __name__ == "__main__":
    repair_post()
