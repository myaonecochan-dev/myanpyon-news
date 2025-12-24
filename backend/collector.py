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

        Characters (ENFORCE THESE PERSONALITIES):
        1. Myan (Cat): Male. Selfish, lazy, and rough but curious. He's often looking for the "lazy" angle (e.g. "Will this mean more food for me?" or "Humans are annoying"). 
           Tone: Young male cat ("〜だぜ", "〜かよ", "〜かもな"). Rough but not violent.
           Calls partner "ぴょん".
        2. Pyon (Bunny): Female. High-spec, analytical, and slightly "toxic" or "cold" (S-character). She explains things logically but often insults Myan's intelligence.
           Tone: Intellectual, elegant yet sharp ("〜ですわ", "〜ですよ"). "Ara ara" vibes when pitying Myan.
           Calls partner "みゃん".

        CRITICAL INSTRUCTIONS:
        - **DO NOT** say "Check the link for details". The reader wants EVERYTHING here.
        - **EXPLAIN** background, reasons, and implications deeply.
        - **NETIZEN REACTIONS**: Generate 5-8 simulated "Netizen comments" reacting to this news. 
          - Make them feel like a Japanese BBS (2ch/5ch). 
          - Mix of: Enthusiastic, critical, cynical, and weird/funny.
        - **POLL**: Suggest a 2-option poll question relevant to the news.
        - **SNS CONTENT**: Generate a short, rough, lazy tweet from Myan. (NO URL).

        Format:
        Return ONLY valid JSON with keys: "title", "content", "description", "tweet_text", "reactions", "poll".
        
        "title": Catchy title starting with 【話題】.
        "tweet_text": Myan's lazy tweet.
        "description": Short news summary.
        "reactions": List of objects: [{"name": "名無しさん", "text": "...", "color": "green/blue/red"}]
        "poll": {"question": "...", "option_a": "...", "option_b": "..."}
        "content": HTML format (Summary Box + Character Dialogue). Use <div class="news-summary-box"> and <div class="chat-row chat-myan/pyon">.
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Simple cleanup
        if "```json" in text:
            text = text.replace("```json", "").replace("```", "")
        
        data = json.loads(text)
        return data

    except Exception as e:
        import traceback
        print(f"AI Generation failed. Error: {e}")
        traceback.print_exc()
        return None

def insert_post_to_supabase(post_data, poll_data=None):
    """
    Inserts post and optional poll.
    """
    try:
        # 1. Insert Post
        db_data = {
            "title": post_data["title"],
            "description": post_data["description"],
            "content": post_data["content"],
            "category": post_data["category"],
            "type": post_data["type"],
            "platform": post_data["platform"],
            "image_url": post_data["imageUrl"],
            "tweet_text": post_data.get("tweet_text", ""),
            "reactions": post_data.get("reactions", []), # New Reactions column
            "created_at": post_data["created_at"]
        }
        
        res = supabase.table("posts").insert(db_data).execute()
        new_post = res.data[0]
        post_id = new_post["id"]
        print(f"Inserted post: {post_id}")

        # 2. Insert Poll if exists
        if poll_data:
            poll_db = {
                "post_id": post_id,
                "question": poll_data["question"],
                "option_a": poll_data["option_a"],
                "option_b": poll_data["option_b"]
            }
            supabase.table("polls").insert(poll_db).execute()
            print("Inserted poll.")

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
        "reactions": ai_content.get("reactions", []), # Extract reactions
        "category": "trend",
        "type": "article",
        "platform": "article",
        "imageUrl": thumb_url, 
        "tweet_text": ai_content.get("tweet_text", ""),
        "created_at": datetime.datetime.now().isoformat()
    }
    
    poll_data = ai_content.get("poll") # Extract poll
    
    # Debug: Print Tweet
    if post["tweet_text"]:
        print(f"\n[Generated Tweet]: {post['tweet_text']}\n")
        # Try to post (Dry Run if no keys)
        from x_client import post_tweet
        post_tweet(post["tweet_text"])

    # 5. Save
    insert_post_to_supabase(post, poll_data=poll_data)
    print("--- Done ---")

if __name__ == "__main__":
    main()
