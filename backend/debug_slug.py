import json
from supabase_client import supabase

def check_slug():
    try:
        response = supabase.table("posts").select("id, title, slug, created_at").order("created_at", desc=True).limit(5).execute()
        if response.data:
            print(f"Checking latest 5 posts:")
            for post in response.data:
                print(f"ID: {post['id']}")
                print(f"Title: {post['title']}")
                print(f"Slug: [{post.get('slug')}]")
                print(f"Created: {post['created_at']}")
                print("-" * 20)
        else:
            print("No content found")
    except Exception as e:
        print(f"Error: {e}")

check_slug()
