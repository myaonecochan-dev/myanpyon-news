import os
import json
import uuid
import urllib.parse
import random
from supabase import create_client, Client
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Use existing credentials
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or "fallback_key_if_needed"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def repair_post():
    slug = "child-grandparents-medicine-ingestion-1226"
    print(f"Repairing post: {slug}")
    
    # 1. Fetch post
    res = supabase.table("posts").select("*").eq("slug", slug).execute()
    if not res.data:
        print("Post not found.")
        return
    post = res.data[0]
    
    # 2. Generate missing data via Gemini
    if GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = f"""
        Generate a poll and 5 netizen reactions for this news:
        Title: {post['title']}
        Summary: {post['description']}
        
        Output JSON:
        {{
            "reactions": [{{ "name": "...", "text": "...", "color": "blue/green/red" }}],
            "poll": {{ "question": "...", "option_a": "...", "option_b": "..." }},
            "thumbnail_prompt": "A short English prompt for an AI image of grandparents medicine bottle child"
        }}
        """
        response = model.generate_content(prompt)
        import re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            new_data = json.loads(match.group())
            
            # Generate remote thumbnail URL
            thumb_prompt = new_data.get("thumbnail_prompt", "child grandparents medicine bottle")
            prompt_clean = urllib.parse.quote(thumb_prompt)
            thumb_url = f"https://image.pollinations.ai/prompt/{prompt_clean}?width=1200&height=630&nologo=true&seed={random.randint(0, 99999)}"
            
            # 3. Update Post
            update_data = {
                "image_url": thumb_url,
                "reactions": new_data.get("reactions", [])
            }
            supabase.table("posts").update(update_data).eq("id", post["id"]).execute()
            print("Post updated with image and reactions.")
            
            # 4. Insert Poll
            poll = new_data.get("poll")
            if poll:
                poll_db = {
                    "post_id": post["id"],
                    "question": poll["question"],
                    "option_a": poll["option_a"],
                    "option_b": poll["option_b"]
                }
                supabase.table("polls").insert(poll_db).execute()
                print("Poll inserted.")
                
    else:
        print("GEMINI_API_KEY missing. Cannot generate repair data.")

if __name__ == "__main__":
    repair_post()
