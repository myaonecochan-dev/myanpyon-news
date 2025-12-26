import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_and_fix_ekiden():
    print("Checking Ekiden post...")
    res = supabase.table("posts").select("*").ilike("title", "%箱根駅伝%").execute()
    
    if not res.data:
        print("Ekiden post NOT found.")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    print(f"Current Comment Myan: '{post.get('comment_myan')}'")
    print(f"Current Comment Pyon: '{post.get('comment_pyon')}'")
    
    # If empty, update
    if not post.get('comment_myan'):
        print("Comments missing! Updating...")
        update_data = {
            "comment_myan": "来年の箱根が待ちきれないにゃ！26校も出るなんてお祭り騒ぎだぜ！",
            "comment_pyon": "学生たちの熱い走りに期待しましょう。記念大会ならではのドラマが生まれそうですわね。"
        }
        supabase.table("posts").update(update_data).eq("id", post['id']).execute()
        print("Update Success!")
    else:
        print("Comments exist (maybe I misread or it's just user cache?)")

if __name__ == "__main__":
    check_and_fix_ekiden()
