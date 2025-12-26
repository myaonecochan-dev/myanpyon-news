import os
import json
import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-pro')

def fix_starbucks():
    print("Finding Starbucks post...")
    res = supabase.table("posts").select("*").ilike("title", "%米粉カステラ%").execute()
    
    if not res.data:
        print("Post NOT found.")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    
    # Correct Info
    new_title = "スタバ「米粉カステラ」2種、販売中止の理由は『グルテン混入』…カビ報告は誤り"
    new_desc = "スターバックスは「米粉の抹茶カステラ」などの販売中止を発表。一部で『カビでは？』との噂もあったが、公式発表によると『グルテンフリー商品なのに微量の大麦麦芽（グルテン）が含まれていたため』とのこと。"
    
    # Regenerate Content with Correct Info
    prompt = f"""
    Rewrite the following news article content based on the CORRECT information.
    
    CORRECT INFO:
    - Starbucks cancelled "Rice Flour Castella" (Matcha/Hojicha).
    - Reason: Trace amounts of Barley Malt (Gluten) found.
    - It was marketed as Gluten-Free, so this is a compliance issue.
    - NOT MOLD. (Correcting previous misinformation).
    
    Structure:
    - HTML summary box: <div class="news-summary-box">...</div>
    - Dialogue: MUST use this EXACT HTML structure for images:
      <div class="chat-row chat-myan">
        <div class="chat-avatar"><img src="/mascot_cat.png" alt="Myan"></div>
        <div class="chat-bubble">Myan's text...</div>
      </div>
      <div class="chat-row chat-pyon">
        <div class="chat-avatar"><img src="/mascot_bunny.png" alt="Pyon"></div>
        <div class="chat-bubble">Pyon's text...</div>
      </div>
    - Tone: Casual Japanese (Mascot personalities).
    
    LANGUAGE: JAPANESE (Critical).
    
    Return ONLY JSON: {{ "content": "..." }}
    """
    
    resp = model.generate_content(prompt)
    text = resp.text.replace("```json", "").replace("```", "")
    try:
        data = json.loads(text)
        new_content = data["content"]
        # Image path fix
        new_content = new_content.replace("/images/myan_icon.png", "/mascot_cat.png").replace("myan.png", "/mascot_cat.png")
        new_content = new_content.replace("/images/pyon_icon.png", "/mascot_bunny.png").replace("pyon.png", "/mascot_bunny.png")

        # Comments
        new_myan_comment = "カビじゃなくてグルテンだったのか！アレルギーの人は要注意だにゃ。"
        new_pyon_comment = "グルテンフリーを信じて買った人への誠実な対応ですわね。誤情報は拡散しないように。"

        update_data = {
            "title": new_title,
            "description": new_desc,
            "content": new_content,
            "comment_myan": new_myan_comment,
            "comment_pyon": new_pyon_comment,
            "slug": "starbucks-castella-gluten-recall-correction" # Updating slug to match reality
        }
        
        supabase.table("posts").update(update_data).eq("id", post['id']).execute()
        print("Fixed Starbucks post with correct info.")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fix_starbucks()
