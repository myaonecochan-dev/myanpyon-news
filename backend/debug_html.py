import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

def check_html():
    response = supabase.table("posts").select("content").order("created_at", desc=True).limit(1).execute()
    if response.data:
        content = response.data[0]["content"]
        print(f"--- HTML Content Sample (first 500 chars) ---")
        print(content[:500])
        print(f"--- Chat Row Sample ---")
        if "chat-row" in content:
            start = content.find('<div class="chat-row')
            print(content[start:start+300])
    else:
        print("No content found")

check_html()
