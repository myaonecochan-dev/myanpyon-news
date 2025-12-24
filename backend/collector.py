import os
import json
import uuid
import datetime
import urllib.request
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
from thumbnail_gen import generate_thumbnail
from supabase import create_client, Client
from dotenv import load_dotenv

# Load env
load_dotenv()

# Initial configuration
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
RSS_URL = "https://news.yahoo.co.jp/rss/topics/top-picks.xml"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def fetch_og_image(url):
    """
    Fetches the og:image URL from the given page URL.
    """
    print(f"Scraping OG Image from: {url}")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"]
        
        # Try thumbnail for Yahoo News specifically if needed, but og:image usually works
        return None
    except Exception as e:
        print(f"Error scraping OG image: {e}")
        return None

def fetch_rss_trends():
    """
    Fetches trending topics from Yahoo News RSS.
    Returns a list of dicts: {'title': str, 'link': str, 'description': str}
    """
    print(f"Fetching trends from {RSS_URL}...")
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            items = []
            # Parse RSS items (channel -> item)
            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text
                desc = item.find("description").text if item.find("description") is not None else ""
                
                items.append({
                    "title": title,
                    "link": link,
                    "description": desc,
                    "traffic": "News"
                })
            
            print(f" -> Found {len(items)} trends.")
            return items
            
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def generate_content_with_gemini(trend_item):
    """
    Uses Gemini API to generate an article.
    If API key is missing or error occurs, falls back to simple formatting.
    """
    topic = trend_item['title']
    print(f"Generating content for: {topic}...")

    # Try to import Gemini
    try:
        import google.generativeai as genai
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set")
            
        genai.configure(api_key=GEMINI_API_KEY)
        # Use a model confirmed to exist via list_models.py
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Act as a news commentary duo for a popular Japanese summary blog.
        Topic: "{topic}"
        Context: "{trend_item.get('description', '')}"

        Characters:
        Characters:
        1. Myan (Cat): Male. Mischievous, curious, and energetic. He is the reader's avatar asking "Why?" or "What's the point?". Tone: Casual male speech (ore-sama style but friendly). NO weird sentence endings like "da ora". Calls partner "ぴょん" (in Hiragana).
        2. Pyon (Bunny): Female. Intelligent, calm, and cool. She explains the news logically. Tone: Polite, analytical, "Ara ara" vibes. Ends with "ですわ" or "ですね". Calls partner "みゃん" (in Hiragana).

        CRITICAL INSTRUCTIONS:
        - **DO NOT** say "Check the link for details" or "Read the news". The reader wants to know EVERYTHING here.
        - **EXPLAIN** the background, reasons, and implications deeply. Use your knowledge base to supplement the context.
        - If it's a complex topic (politics, economy), simplify it but keep the detail.
        - Make the conversation long enough (6-8 turns) to cover the topic well.
        - **IMPORTANT**: Keep bullet points in "30-second summary" MODERATE length (around 40-50 chars). Not too short, not too long.
        - **IMPORTANT**: In dialogue, use natural pauses (punctuation) to help text wrapping.
        - **SNS CONTENT**: Generate a short, casual tweet (under 140 chars) from **Myan's perspective ONLY**.
          - Do NOT include "Myan:" prefix. Just the text.
          - **WARM-UP MODE**: DO NOT include any URL. Just state the impression or shock.
          - Tone: Casual, rough, spoken like a young male cat ("〜だぜ", "〜なのか？", "マジかよ").
          - Example: "診療報酬上がるのかよ... 給料増えるのはいいけど保険料上がるのは勘弁だぜ #News"

        Format:
        Return ONLY valid JSON with keys: "title", "content", "description", "tweet_text".
        
        "title": Catchy Japanese title (start with 【話題】).
        "tweet_text": The casual tweet content (NO URL).
        "description": A short summary of the news (2-3 sentences).
        "content": HTML format.
           
           <!-- 1. Summary Box -->
           <div class="news-summary-box">
             <h3>30秒でわかるポイント</h3>
             <ul>
               <li>Point 1 (Key fact)</li>
               <li>Point 2 (Background/Reason)</li>
               <li>Point 3 (Conclusion/Impact)</li>
             </ul>
           </div>

           <!-- 1.5 Intro Text -->
           <div class="intro-text">
             (Write a compelling 2-3 sentence introduction here. E.g. "The budget has swelled to... What is the 'Takaichi Color'? We explain thoroughly below.")
           </div>

           <!-- 2. Dialogue -->
           <div class="chat-row chat-pyon">
             <div class="chat-avatar"><img src="/mascot_bunny.png"></div>
             <div class="chat-bubble">Pyon's line</div>
           </div>
           <div class="chat-row chat-myan">
             <div class="chat-avatar"><img src="/mascot_cat.png"></div>
             <div class="chat-bubble">Myan's line</div>
           </div>
           Structure:
        1. Myan (Cat) brings up the topic with curiosity or a misunderstanding.
        2. Pyon (Bunny) corrects him and explains the details calmly.
        3. Myan asks a sharp or naive question ("Is that actually good?").
        4. Pyon gives a deep insight or conclusion.
        5. Include <h2> headlines for sections if needed.

        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Simple cleanup if the model returns markdown code blocks
        if "```json" in text:
            text = text.replace("```json", "").replace("```", "")
        
        data = json.loads(text)
        return data

    except Exception as e:
        import traceback
        print(f"AI Generation skipped/failed. Error: {e}")
        traceback.print_exc()
        
        # Fallback content
        return {
            "title": f"【話題】{topic}",
            "description": f"現在、ニュースで「{topic}」が話題になっています。詳細をチェックしましょう。",
            "content": f"""
            <div class="news-summary-box">
             <h3>30秒でわかるポイント</h3>
             <ul>
               <li>{topic}が話題になっています</li>
               <li>詳細な情報は現在調査中です</li>
               <li>新しい情報が入り次第更新します</li>
             </ul>
           </div>
            <div class="chat-row chat-pyon">
                <div class="chat-avatar"><img src="/mascot_bunny.png"></div>
                <div class="chat-bubble">わあ！ {topic} だって！ すごいニュースだぴょん！</div>
            </div>
            <div class="chat-row chat-myan">
               <div class="chat-avatar"><img src="/mascot_cat.png"></div>
               <div class="chat-bubble">ふーん、まあ悪くないニュースだにゃ。詳細はリンク先を確認するにゃ。</div>
            </div>
            <p><strong>ソース:</strong> News</p>
            """
        }

def insert_post_to_supabase(post_data):
    """
    Inserts the generated post into Supabase 'posts' table.
    """
    try:
        # Convert keys to match DB columns (camelCase -> snake_case)
        # imageUrl -> image_url, videoId -> video_id
        db_data = {
            "title": post_data["title"],
            "description": post_data["description"],
            "content": post_data["content"],
            "category": post_data["category"],
            "type": post_data["type"],
            "platform": post_data["platform"],
            "image_url": post_data["imageUrl"],
            "tweet_text": post_data.get("tweet_text", ""), # Add tweet text
            "created_at": post_data["created_at"]
        }
        
        data, count = supabase.table("posts").insert(db_data).execute()
        print(f"Successfully inserted post to Supabase: {post_data['title']}")
    except Exception as e:
        print(f"Error inserting to Supabase: {e}")
        # Could fallback to local JSON here if needed, but for now just log error

def main():
    print("--- Trend Bot Started ---")
    
    # 0. Check connection and table
    try:
        print("Checking Supabase connection...")
        # Try to select 1 row
        test_data = supabase.table("posts").select("count", count="exact").limit(1).execute()
        print(f"Connection OK. Current post count: {test_data.count}")
    except Exception as e:
        print(f"Connection Check Failed: {e}")
        print("!! PLEASE ENSURE YOU RAN THE SQL TO CREATE THE 'posts' TABLE !!")
        return

    # 1. Fetch
    trends = fetch_rss_trends()
    if not trends:
        print("No trends found. Exiting.")
        return

    # 2. Pick a random trend (or top one)
    # Let's pick the top one that isn't already in our 'processed' list (simplification: just pick random top 5)
    target_trend = trends[0] # Always picking top 1 for demo stability, or random.choice(trends[:5])
    
    # 3. Generate Content
    ai_content = generate_content_with_gemini(target_trend)
    
    # 3.5 Generate Thumbnail
    post_title = ai_content.get("title", target_trend['title'])
    
    # Try to extract real image from the news link
    news_link = target_trend.get('link')
    bg_image_url = fetch_og_image(news_link) if news_link else None
    
    thumb_filename = f"thumb_{uuid.uuid4()}.png"
    # Pass bg_image_url to generator
    thumb_url = generate_thumbnail(post_title, thumb_filename, bg_image_url=bg_image_url)

    # 4. Assembled Post Object
    post = {
        "id": str(uuid.uuid4()),
        "title": post_title,
        "description": ai_content.get("description", ""),
        "content": ai_content.get("content", ""),
        "category": "trend",
        "type": "article",
        "platform": "article",
        "imageUrl": thumb_url, 
        "tweet_text": ai_content.get("tweet_text", ""), # Add tweet text
        "created_at": datetime.datetime.now().isoformat()
    }
    
    # Debug: Print Tweet
    if post["tweet_text"]:
        print(f"\n[Generated Tweet]: {post['tweet_text']}\n")
        # Try to post (Dry Run if no keys)
        from x_client import post_tweet
        post_tweet(post["tweet_text"])

    # 5. Save
    insert_post_to_supabase(post)
    print("--- Done ---")

if __name__ == "__main__":
    main()
