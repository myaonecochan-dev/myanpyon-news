
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def debug_content():
    # Check the Muscular Dystrophy post
    target_title_part = "筋ジストロフィー"
    print(f"--- Inspecting Content for: {target_title_part} ---")
    
    res = supabase.table("posts").select("*").ilike("title", f"%{target_title_part}%").execute()
    if not res.data:
        print("Post not found.")
        return

    post = res.data[0]
    print(f"ID: {post.get('id')}")
    print(f"Type: {post.get('type')}")
    content = post.get('content')
    print(f"Content Length: {len(content) if content else 0}")
    print(f"Content Preview: {content[:100] if content else 'NONE'}")
    print("-" * 20)

    # Check another one: Premium Friday
    target_title_part_2 = "プレミアムフライデー"
    print(f"--- Inspecting Content for: {target_title_part_2} ---")
    res2 = supabase.table("posts").select("*").ilike("title", f"%{target_title_part_2}%").execute()
    if res2.data:
        post2 = res2.data[0]
        c2 = post2.get('content')
        print(f"Content Length: {len(c2) if c2 else 0}")
        print(f"Content Preview: {c2[:100] if c2 else 'NONE'}")

if __name__ == "__main__":
    debug_content()
