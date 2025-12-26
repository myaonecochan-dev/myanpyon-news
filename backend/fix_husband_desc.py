import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fix_english_description():
    print("Searching for Husband post...")
    # Search for "husband" in slug or title part
    res = supabase.table("posts").select("*").ilike("slug", "%husband%").limit(1).execute()
    
    if not res.data:
        print("Post NOT found via slug. Trying title...")
        res = supabase.table("posts").select("*").ilike("title", "%夫の%").limit(1).execute()
        if not res.data:
             print("Post NOT found.")
             return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    print(f"Current Description: {post['description']}")

    # Japanese Text for replacement
    # Based on the screenshot context: "unborn son's ectrodactyly diagnosis..."
    # Translation: "お腹の子が『裂手症』と診断され、絶望の淵に立たされた妻。しかし、夫が放った『ある一言』が彼女を救い、ネット上で「天才すぎる」「泣ける」と称賛の嵐を呼んでいます。"
    
    new_description = "お腹の子が『裂手症』と診断され、絶望の淵に立たされた妻。しかし、夫が放った『ある一言』が彼女を救い、ネット上で「天才すぎる」「泣ける」と称賛の嵐を呼んでいます。"
    
    supabase.table("posts").update({"description": new_description}).eq("id", post['id']).execute()
    print("Description updated to Japanese.")

if __name__ == "__main__":
    fix_english_description()
