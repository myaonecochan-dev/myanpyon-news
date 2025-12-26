import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def debug_akasaka():
    print("Checking Akasaka post...")
    res = supabase.table("posts").select("*").ilike("title", "%赤坂個室サウナ%").execute()
    
    if not res.data:
        print("Post NOT found.")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    val_myan = post.get('comment_myan')
    val_pyon = post.get('comment_pyon')
    
    print(f"DB Value Myan: '{val_myan}' (Type: {type(val_myan)})")
    print(f"DB Value Pyon: '{val_pyon}' (Type: {type(val_pyon)})")

    # Fix if empty
    if not val_myan or val_myan.strip() == "":
        print("Empty! Generating specific comments...")
        # Since I am in python, I can just hardcode or call AI. 
        # For speed/certainty, I hardcode RELEVANT comments.
        update_data = {
            "comment_myan": "個室サウナでこんな事故が起きるなんて怖いぜ… お店選びは気をつけなきゃな。",
            "comment_pyon": "換気設備の不備は命に関わりますわ。業界全体の安全管理が見直されるべきです。"
        }
        supabase.table("posts").update(update_data).eq("id", post['id']).execute()
        print("Fixed with hardcoded context-aware comments.")
    else:
        print("Values exist. Why default shown?")

if __name__ == "__main__":
    debug_akasaka()
