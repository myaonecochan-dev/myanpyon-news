from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fix_latest_post_comments():
    print("Fetching latest post...")
    # Filter for the Smartphone article
    response = supabase.table("posts").select("id, title, slug").ilike("title", "%スマホ%").order("created_at", desc=True).limit(1).execute()
    
    if not response.data:
        print("No posts found.")
        return

    post = response.data[0]
    print(f"Updating post: {post['title']} ({post['slug']})")

    # Update with specific comments
    update_data = {
        "comment_myan": "えーっ！スマホ高くなるの！？困るにゃ〜😿 ゲームできなくなる〜！",
        "comment_pyon": "半導体不足ですから仕方ないですね。今のうちにハイスペック機を買うべきかしら？🐇"
    }

    supabase.table("posts").update(update_data).eq("id", post['id']).execute()
    print("Successfully updated mascot comments.")

if __name__ == "__main__":
    fix_latest_post_comments()
