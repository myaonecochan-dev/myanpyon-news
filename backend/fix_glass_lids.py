import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv
import google.generativeai as genai

# Load env (or hardcode if needed for one-off)
load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)

def fix_glass_lid_post():
    target_slug_partial = "why-glass-lids-shatter"
    
    print(f"Searching for post with slug containing '{target_slug_partial}'...")
    
    # 1. Fetch Post
    # Note: 'like' or 'ilike' might efficiently find it. OR just fetch all and filter since small DB.
    # Let's try ilike
    res = supabase.table("posts").select("*").ilike("slug", f"%{target_slug_partial}%").execute()
    
    if not res.data:
        print("Post not found!")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']} (ID: {post['id']})")
    
    if post.get("comment_myan") and post.get("comment_myan") != "":
        print(f"Existing Myan Comment: {post['comment_myan']}")
        # Ask user if overwrite? well script assumes fix.
        # print("Skipping...")
        # return 
    
    # 2. Generate Comments
    model = genai.GenerativeModel('gemini-2.5-pro')
    prompt = f"""
    Generate short, character-specific closing comments for this news article.
    
    News Title: {post['title']}
    News Summary: {post['description']}

    Characters:
    1. Myan (Cat): Male, Energetic, curious, slightly dumb. "〜だぜ！" "〜にゃ！"
    2. Pyon (Bunny): Female, Cool, analytical, sadistic. "〜ですわ" "〜ですね"

    Output JSON only:
    {{
        "comment_myan": "...",
        "comment_pyon": "..."
    }}
    """
    
    print("Generating comments...")
    response = model.generate_content(prompt)
    text = response.text.replace("```json", "").replace("```", "")
    
    try:
        data = json.loads(text)
        print(f"Generated Myan: {data['comment_myan']}")
        print(f"Generated Pyon: {data['comment_pyon']}")
        
        # 3. Update DB
        update_res = supabase.table("posts").update({
            "comment_myan": data['comment_myan'],
            "comment_pyon": data['comment_pyon']
        }).eq("id", post['id']).execute()
        
        print("Update Success!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_glass_lid_post()
