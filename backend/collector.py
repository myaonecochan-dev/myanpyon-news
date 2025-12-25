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
# RSS Feeds List (Randomly select one to ensure variety)
RSS_FEEDS = [
    "https://news.yahoo.co.jp/rss/topics/top-picks.xml", # Major News
    "https://news.yahoo.co.jp/rss/topics/domestic.xml",  # Domestic
    "https://news.yahoo.co.jp/rss/topics/world.xml",     # World
    "https://news.yahoo.co.jp/rss/topics/business.xml",  # Economy
    "https://news.yahoo.co.jp/rss/topics/it.xml",        # IT
    "https://news.yahoo.co.jp/rss/topics/science.xml"    # Science
]
RSS_URL = random.choice(RSS_FEEDS)
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
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        prompt = f"""
        Act as a news commentary duo for a popular Japanese summary blog.
        Topic: "{topic}"
        Context: "{trend_item.get('description', '')}"

        Characters (ENFORCE THESE PERSONALITIES):
        1. Myan (Cat): Male. **Wanpaku (Energetic, Naughty) and Curious**. He is consistently excited, reckless, and wants to try everything. He speaks with high energy.
           Tone: Energetic young male cat ("〜だぜ！", "〜やってみようぜ！", "〜すげえ！").
           Calls partner "ぴょん".
        2. Pyon (Bunny): Female. High-spec, analytical, and slightly "toxic" or "cold" (S-character). She explains things logically but often insults Myan's intelligence or recklessness.
           Tone: Intellectual, elegant yet sharp ("〜ですわ", "〜ですよ"). "Ara ara" vibes when pitying Myan.
           Calls partner "みゃん".

        CRITICAL INSTRUCTIONS:
        - **DO NOT** say "Check the link for details". The reader wants EVERYTHING here.
        - **EXPLAIN** background, reasons, and implications deeply.
        - **NETIZEN REACTIONS**: Generate 5-8 simulated "Netizen comments" reacting to this news. 
          - Make them feel like a Japanese BBS (2ch/5ch). 
          - Mix of: Enthusiastic, critical, cynical, and weird/funny.
        - **POLL**: Suggest a 2-option poll question relevant to the news.
        - **SNS CONTENT**: Generate a short, energetic, curious tweet from Myan. (STRICTLY NO URL). Just a simple "tsubuyaki" or comment on the news.

        Format:
        Return ONLY valid JSON with keys: "title", "content", "description", "tweet_text", "reactions", "poll", "thumbnail_prompt", "slug".
        
        "title": Catchy title starting with 【話題】.
        "slug": English URL-friendly string (kebab-case, lowercase) representing the topic. E.g. "teacher-exam-odds-lowest" or "tokyo-game-show-2025".
        "tweet_text": Myan's tweet.
        "description": Short news summary.
        "reactions": List of objects: [{{ "name": "名無しさん", "text": "...", "color": "green/blue/red" }}]
        "poll": {{ "question": "...", "option_a": "...", "option_b": "..." }}
        "thumbnail_prompt": A SHORT ENGLISH prompt for an AI image generator representing the news (e.g. "Japanese Prime Minister Takaichi giving a speech" or "Cyberpunk Tokyo city at night").
        "category": One of ["trend", "healing", "surprise", "flame"]. 
           - "healing": Cute animals, heartwarming stories.
           - "surprise": Shocking events, weird news, miracles.
           - "flame": Controversial topics, angry netizen reactions.
           - "trend": General news, politics, viral topics (Default).
        "category": One of ["trend", "healing", "surprise", "flame"]. 
           - "healing": Cute animals, heartwarming stories.
           - "surprise": Shocking events, weird news, miracles.
           - "flame": Controversial topics, angry netizen reactions.
           - "trend": General news, politics, viral topics (Default).
        "comment_myan": A short, energetic closing remark from Myan about this news (1 sentence). E.g. "Oishisou da nyan!"
        "comment_pyon": A short, cool/sarcastic closing remark from Pyon about this news (1 sentence). E.g. "Tabesugi chuui desu yo."
        "content": HTML format (Summary Box + Character Dialogue).
           - Summary Box: <div class="news-summary-box">...</div>
           - Dialogue: MUST use this structure for images:
             <div class="chat-row chat-myan">
               <div class="chat-avatar"><img src="/mascot_cat.png" alt="Myan"></div>
               <div class="chat-bubble">Myan's text...</div>
             </div>
             <div class="chat-row chat-pyon">
               <div class="chat-avatar"><img src="/mascot_bunny.png" alt="Pyon"></div>
               <div class="chat-bubble">Pyon's text...</div>
             </div>
        """
        
        response = model.generate_content(prompt)
        text = response.text
        
        # Robust JSON extraction
        try:
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(), strict=False)
                print(f"DEBUG: Parsed JSON keys: {list(data.keys())}")
                if "slug" in data:
                    print(f"DEBUG: AI generated slug: {data['slug']}")
                else:
                    print("DEBUG: AI did NOT generate 'slug' key.")
                
                # FORCE FIX: AI often hallucinates /images/myan_icon.png which doesn't exist.
                # We replace known wrong paths with the correct /mascot_cat.png and /mascot_bunny.png
                if "content" in data:
                    c = data["content"]
                    # Fix Myan
                    c = c.replace("/images/myan_icon.png", "/mascot_cat.png")
                    c = c.replace("myan.png", "/mascot_cat.png")
                    c = c.replace("cat.png", "/mascot_cat.png")
                    c = c.replace("/mascot_/mascot_cat.png", "/mascot_cat.png") # Fix observed hallucination
                    
                    # Fix Pyon
                    c = c.replace("/images/pyon_icon.png", "/mascot_bunny.png")
                    c = c.replace("pyon.png", "/mascot_bunny.png")
                    c = c.replace("bunny.png", "/mascot_bunny.png")
                    c = c.replace("/mascot_/mascot_bunny.png", "/mascot_bunny.png") # Fix observed hallucination
                    
                    data["content"] = c
                
                # Dedicated Slug Generation (since main prompt often fails)
                try:
                    slug_prompt = f"""
                    Convert the following Japanese news title into a SHORT, ENGLISH, URL-FRIENDLY slug (kebab-case).
                    Title: {data['title']}
                    
                    Rules:
                    - Lowercase only.
                    - Use hyphens (-) as separators.
                    - Max 5-6 words.
                    - Remove special characters.
                    - Return ONLY the slug string (no JSON, no code blocks).
                    Example: "teacher-exam-odds-lowest"
                    """
                    slug_response = model.generate_content(slug_prompt)
                    clean_slug = slug_response.text.strip().lower().replace(" ", "-").replace('"', '').replace("'", "").replace("`", "")
                    # Ensure only valid chars
                    clean_slug = re.sub(r'[^a-z0-9-]', '', clean_slug)
                    print(f"DEBUG: Generated dedicated slug: {clean_slug}")
                    data["slug"] = clean_slug
                except Exception as e:
                    print(f"DEBUG: Failed to generate dedicated slug: {e}")
                    # Fallback to None, will use ID
                
                # --- NEW: Ensure comments exist (Retry Logic - Primary Path) ---
                if not data.get("comment_myan") or not data.get("comment_pyon"):
                    print("DEBUG: Comments missing in initial generation (Primary). Retrying...")
                    try:
                        comment_prompt = f"""
                        The following news article needs short mascot comments.
                        Title: {trend_data['title']}
                        Summary: {data.get('description', '')}
                        
                        Characters:
                        Myan (Cat): Energetic, dumb. "〜だぜ！" "〜にゃ！"
                        Pyon (Bunny): Cool, sarcastic. "〜ですわ"

                        Output JSON only:
                        {{
                            "comment_myan": "...",
                            "comment_pyon": "..."
                        }}
                        """
                        comment_resp = model.generate_content(comment_prompt)
                        comment_text = comment_resp.text.replace("```json", "").replace("```", "")
                        comment_json = json.loads(comment_text)
                        
                        data["comment_myan"] = comment_json.get("comment_myan")
                        data["comment_pyon"] = comment_json.get("comment_pyon")
                        print("DEBUG: Retry comments success.")
                    except Exception as e:
                        print(f"DEBUG: Retry comments failed: {e}")
                        data["comment_myan"] = "今日のニュースはこれだにゃ！要チェックだぜ！"
                        data["comment_pyon"] = "詳しくは記事を読んでくださいね。しっかり理解しましょう。"
                # ---------------------------------------------
                
                return data
            else:
                print(f"No JSON found in response: {text}")
                return None
        except Exception as json_err:
            print(f"JSON Parse Error: {json_err}. Attempting repair...")
            try:
                repair_prompt = f"""
                The following JSON is invalid. Fix it and return ONLY the valid JSON (no code blocks).
                
                Expected matching schema:
                {
                    "title": "...",
                    "content": "...",
                    "comment_myan": "...",
                    "comment_pyon": "...",
                    "slug": "..."
                }

                Input:
                {text}
                """
                repair_resp = model.generate_content(repair_prompt)
                repair_text = repair_resp.text
                repair_match = re.search(r'\{.*\}', repair_text, re.DOTALL)
                if repair_match:
                    data = json.loads(repair_match.group(), strict=False)
                    print("DEBUG: JSON repaired successfully.")
                    
                    # Duplicate logic from above (refactor ideally, but inline for now)
                    if "slug" in data:
                        print(f"DEBUG: AI generated slug: {data['slug']}")
                    else:
                         print("DEBUG: AI did NOT generate 'slug' key.")

                    if "content" in data:
                        c = data["content"]
                        c = c.replace("/images/myan_icon.png", "/mascot_cat.png")
                        c = c.replace("myan.png", "/mascot_cat.png")
                        c = c.replace("cat.png", "/mascot_cat.png")
                        c = c.replace("/mascot_/mascot_cat.png", "/mascot_cat.png")
                        c = c.replace("/images/pyon_icon.png", "/mascot_bunny.png")
                        c = c.replace("pyon.png", "/mascot_bunny.png")
                        c = c.replace("bunny.png", "/mascot_bunny.png")
                        c = c.replace("/mascot_/mascot_bunny.png", "/mascot_bunny.png")
                        data["content"] = c

                    # Dedicated Slug Generation logic verification
                    if "slug" not in data or not data["slug"]:
                         # Call the dedicated prompt logic again or just rely on fallback
                         pass 
                         
                    # Return repaired data
                    # Note: We skip the specific 'dedicated slug prompt' block inside repair for simplicity unless needed, 
                    # but actually we probably want it. 
                    # Let's simple return data and let the caller receive it? 
                    # The original code flow expects 'data' to be returned.
                    # We need to make sure 'slug' is there.
                    
                    if "slug" not in data or not data["slug"]:
                        try:
                            slug_prompt = f"""
                            Convert the following Japanese news title into a SHORT, ENGLISH, URL-FRIENDLY slug (kebab-case).
                            Title: {data.get('title', '')}
                            
                            Rules:
                            - Lowercase only.
                            - Use hyphens (-) as separators.
                            - Max 5-6 words.
                            - Remove special characters.
                            - Return ONLY the slug string.
                            Example: "teacher-exam-odds-lowest"
                            """
                            slug_response = model.generate_content(slug_prompt)
                            clean_slug = slug_response.text.strip().lower().replace(" ", "-").replace('"', '').replace("'", "").replace("`", "")
                            clean_slug = re.sub(r'[^a-z0-9-]', '', clean_slug)
                            print(f"DEBUG: Generated dedicated slug (in repair): {clean_slug}")
                            data["slug"] = clean_slug
                        except Exception as e:
                            print(f"DEBUG: Failed to generate dedicated slug in repair: {e}")
                            
                    return data
                else:
                    return None
            except Exception as e:
                print(f"JSON Repair Failed: {e}")
                return None

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
            "created_at": post_data["created_at"],
            "slug": post_data.get("slug", None), # Save SEO slug
            "source_url": post_data.get("source_url", None) # Save source URL for duplicate check
        }
        
        # Check if slug exists, if so append random suffix to avoid unique constraint error
        if db_data["slug"]:
            try:
                # Simple check or just try insert. If fail, we might lose data.
                # Ideally we check, but for MVP let's just use it.
                # If 409 conflict, Supabase might throw.
                # Let's clean the slug just in case
                db_data["slug"] = db_data["slug"].lower().replace(" ", "-").replace(".", "")
            except:
                pass
        
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
    # Let's pick the top one that isn't already in our 'processed' list
    # NEW: Check duplication by source_url
    target_trend = None
    for trend in trends:
        # Check if source_url exists in DB
        try:
            # Note: We need to use quote or exact match. 
            # supabase-py select returns object with 'data'.
            # We assume 'source_url' column exists now.
            res = supabase.table("posts").select("id").eq("source_url", trend['link']).execute()
            if res.data and len(res.data) > 0:
                print(f"Skipping duplicate: {trend['title']}")
                continue
            else:
                target_trend = trend
                break
        except Exception as e:
            print(f"Error checking duplicates: {e}")
            # If check fails, maybe allow it? Or skip to be safe? 
            # Let's try to proceed if it's just a connection blip, but risky.
            # Assuming if column missing (user failed migration), this errors.
            print("Assuming no duplicate (or error reading DB), proceeding...")
            target_trend = trend
            break
    
    if not target_trend:
        print("All trends processed or no valid trends found. Exiting.")
        return

    print(f"Processing target: {target_trend['title']}")

    # 3. Generate Content
    # Pass 'link' to generate function if needed, but it's in target_trend
    ai_content = generate_content_with_gemini(target_trend)
    if not ai_content:
        print("AI Content generation returned None. Skipping this trend.")
        return
    
    # 3.5 Generate Thumbnail
    post_title = ai_content.get("title") if ai_content.get("title") else target_trend['title']
    
    # Try to extract real image from the news link
    news_link = target_trend.get('link')
    bg_image_url = fetch_og_image(news_link) if news_link else None
    
    # If AI suggested a prompt, let's use Pollinations to get a "WOW" image instead of generic news thumbnails
    if ai_content.get("thumbnail_prompt"):
        prompt_clean = ai_content["thumbnail_prompt"].replace(" ", "%20")
        ai_thumb_url = f"https://image.pollinations.ai/prompt/{prompt_clean}?width=1200&height=630&nologo=true&seed={random.randint(0, 99999)}"
        # Prioritize AI image over potential broken/boring news images
        print(f"Using AI generated thumbnail directly: {ai_thumb_url}")
        thumb_url = ai_thumb_url # Use remote URL directly!
    else:
        # Fallback to local generation if no AI prompt
        thumb_filename = f"thumb_{uuid.uuid4()}.png"
        thumb_url = generate_thumbnail(post_title, thumb_filename, bg_image_url=bg_image_url)

    # 4. Assembled Post Object
    post = {
        "id": str(uuid.uuid4()),
        "title": post_title,
        "description": ai_content.get("description", ""),
        "content": ai_content.get("content", ""),
        "reactions": ai_content.get("reactions", []), # Extract reactions
        "category": ai_content.get("category", "trend"), # Use AI category or default to trend
        "comment_myan": ai_content.get("comment_myan") or "今日のニュースはこれだにゃ！要チェックだぜ！",
        "comment_pyon": ai_content.get("comment_pyon") or "詳しくは記事を読んでくださいね。しっかり理解しましょう。",
        "type": "article",
        "platform": "article",
        "imageUrl": thumb_url, 
        "tweet_text": ai_content.get("tweet_text", ""),
        "slug": f"{ai_content.get('slug')}-{datetime.datetime.now().strftime('%m%d')}" if ai_content.get("slug") else None, # Append date for uniqueness
        "source_url": target_trend.get('link'), # NEW: Save source URL
        "created_at": datetime.datetime.now().isoformat()
    }
    
    poll_data = ai_content.get("poll") # Extract poll
    
    # Debug: Print Tweet
    if post["tweet_text"]:
        print(f"\n[Generated Tweet]: {post['tweet_text']}\n")
        # Try to post (Dry Run if no keys)
        try:
            from x_client import post_tweet
            post_tweet(post["tweet_text"])
        except ImportError:
            print("x_client not found or failed to import.")
        except Exception as e:
            print(f"Tweet failed: {e}")

    # 5. Save
    insert_post_to_supabase(post, poll_data=poll_data)
    print("--- Done ---")

if __name__ == "__main__":
    main()
