
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def dump_content():
    target_title_part = "筋ジストロフィー"
    print(f"--- Dumping Content for: {target_title_part} ---")
    
    res = supabase.table("posts").select("*").ilike("title", f"%{target_title_part}%").execute()
    if not res.data:
        print("Post not found.")
        return

    post = res.data[0]
    content = post.get('content', '')
    
    with open('backend/dump_content.html', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Dumped {len(content)} characters to backend/dump_content.html")

if __name__ == "__main__":
    dump_content()
