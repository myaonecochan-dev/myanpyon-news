import os
from supabase import create_client
from dotenv import load_dotenv
import json

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_latest():
    response = supabase.table("posts").select("*").order("created_at", desc=True).limit(1).execute()
    if response.data:
        post = response.data[0]
        print(f"Title: {post.get('title')}")
        print(f"Image URL: {post.get('image_url')}")
    else:
        print("No posts found.")

if __name__ == "__main__":
    check_latest()
