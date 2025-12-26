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
import re
try:
    from Levenshtein import ratio
except ImportError:
    ratio = None # Fallback if missing

# Load env
load_dotenv()

# Initial configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

if not SUPABASE_KEY:
    print("WARNING: SUPABASE_KEY is missing!")

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
        print(f"Error checking duplicates: {e}")
    # Default to False (allow) but risky
    return False

def normalize_title(title):
    """
    Cleans title for better comparison:
    - Removes 【...】 content
    - Removes punctuation and spaces
    """
    if not title: return ""
    # Remove metadata in brackets
    title = re.sub(r'【[^】]+】', '', title)
    title = re.sub(r'\[[^\]]+\]', '', title)
    # Remove punctuation and whitespace
    title = re.sub(r'[！？?!\s「」『』…、。・：:;]', '', title)
    return title.strip().lower()

def check_is_duplicate(title, link, threshold=0.7):
    """
    Checks if a post is a duplicate based on:
    1. Exact Source URL match (Fast)
    2. Normalized Title containment or similarity
    3. Keyword overlap (for same news with different wording)
    """
    try:
        # 1. Source URL Check 
        if link:
            res = supabase.table("posts").select("id").eq("source_url", link).execute()
            if res.data and len(res.data) > 0:
                print(f"DEBUG: Duplicate found via Source URL: {link}")
                return True
        
        # 2. Title Normalized Check
        n_title = normalize_title(title)
        if not n_title: return False

        # Extract "keywords" (simple: strings of 2+ chars excluding common particles)
        # For Japanese, a simple bigram or word-like chunking can work
        title_keywords = set(re.findall(r'[一-龠ぁ-ゔァ-ヴー]{2,}', n_title))

        # Fetch last 50 posts to compare
        res = supabase.table("posts").select("title").order("created_at", desc=True).limit(50).execute()
        if not res.data:
            return False
            
        for post in res.data:
            db_title = post.get('title', '')
            if not db_title: continue
            
            n_db_title = normalize_title(db_title)
            if not n_db_title: continue

            # A. Simple containment check
            if n_title in n_db_title or n_db_title in n_title:
                 print(f"DEBUG: Duplicate found via Normalized Title Containment: {n_db_title}")
                 return True
                 
            # B. Levenshtein check
            if ratio:
                sim = ratio(n_title, n_db_title)
                if sim > threshold:
                    print(f"DEBUG: Duplicate found via Normalized Levenshtein ({sim:.2f}): {n_db_title}")
                    return True

            # C. Keyword Overlap (Robust for same news, different title)
            db_keywords = set(re.findall(r'[一-龠ぁ-ゔァ-ヴー]{2,}', n_db_title))
            overlap = title_keywords.intersection(db_keywords)
            
            # If 3 or more substantial keywords (min 2 chars) overlap, it's likely the same news
            if len(overlap) >= 3:
                print(f"DEBUG: Duplicate found via Keyword Overlap ({list(overlap)}): {n_db_title}")
                return True
                    
        return False

    except Exception as e:
        print(f"Error in duplicate check: {e}")
        return False

def fetch_mascot_comments_persistent(model, title, summary, safety_settings, max_retries=3):
    """
    Attempts to generate unique mascot comments with persistent retries.
    If fails, returns generic comments.
    """
    print(f"DEBUG: Starting persistent comment generation (Max {max_retries} attempts)...")
    
    import google.generativeai as genai
    
    for attempt in range(max_retries):
        try:
            # Vary prompt slightly to break loops?
            prompt_modifier = ""
            if attempt > 0:
                prompt_modifier = "Please be very creative and ensure valid JSON output."

            comment_prompt = f"""
            The following news article needs short mascot comments.
            Title: {title}
            Summary: {summary}
            {prompt_modifier}
            
            Characters:
            Myan (Cat): Energetic, dumb. "〜だぜ！" "〜にゃ！"
            Pyon (Bunny): Cool, sarcastic. "〜ですわ"

            Output JSON only:
            {{
                "comment_myan": "...",
                "comment_pyon": "..."
            }}
            """
            
            # Increase temperature for retries to avoid sticking to refusal
            gen_config = genai.GenerationConfig(temperature=0.7 + (attempt * 0.1))
            
            comment_resp = model.generate_content(
                comment_prompt, 
                safety_settings=safety_settings,
                generation_config=gen_config
            )
            comment_text = comment_resp.text.replace("```json", "").replace("```", "")
            comment_json = json.loads(comment_text)
            
            new_myan = comment_json.get("comment_myan")
            new_pyon = comment_json.get("comment_pyon")
            
            # Strict Validation
            is_myan_missing = new_myan is None or not str(new_myan).strip() or str(new_myan).lower() == "none"
            is_pyon_missing = new_pyon is None or not str(new_pyon).strip() or str(new_pyon).lower() == "none"
            
            if not is_myan_missing and not is_pyon_missing:
                print(f"DEBUG: Persistent comment generation success on attempt {attempt + 1}")
                return new_myan, new_pyon
            else:
                print(f"DEBUG: Attempt {attempt + 1} produced empty comments. Retrying...")
                
        except Exception as e:
            print(f"DEBUG: Attempt {attempt + 1} failed with error: {e}")
            
    print("DEBUG: All retry attempts failed. Using generic fallback.")
    return (
        "今日のニュースはこれだにゃ！要チェックだぜ！",
        "詳しくは記事を読んでくださいね。しっかり理解しましょう。"
    )


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
        
        # Configure safety settings to allow controversial news (Flame/Surprise categories)
        from google.generativeai.types import HarmCategory, HarmBlockThreshold
        SAFETY_SETTINGS = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        # Use a model confirmed to exist via list_models.py
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        today_str = datetime.date.today().strftime("%Y-%m-%d")
        prompt = f"""
        Act as a news commentary duo for a popular Japanese summary blog.
        Current Date: {today_str}
        Topic: "{topic}"
        Context: "{trend_item.get('description', '')}"

        Characters (ENFORCE THESE PERSONALITIES - NO GENERIC ROBOTS):
        1. Myan (Cat): Male. **EXTREMELY EMOTIONAL & SUBJECTIVE**.
           - He reacts with raw instinct (Hunger, Sleep, Fun, Fear).
           - He DOES NOT summarize. He *feels* the news.
           - If news is sad -> He cries loudly ("うわあああん！").
           - If news is angry -> He rages ("ふざけんなだぜ！").
           - If news is complex -> He gives up ("わからん！とにかく有名になりたい！").
           - Tone: "〜だぜ！", "〜にゃ！", "〜してやる！".

        2. Pyon (Bunny): Female. **CYNICAL REALIST & SHARP TONGUED**.
           - She analyzes the *implications* of the news, often pointing out the dark side of society or human stupidity.
           - She insults Myan's shallow takes immediately.
           - She uses data or logic to cut through hype.
           - Tone: "〜ですわ", "あらあら...", "〜ですね（呆れ）".

        CRITICAL STYLE RULES (TO PASS ADSENSE):
        - **FORBIDDEN**: "Here is a summary of the news." / "Let's look at the details." (Robot talk).
        - **REQUIRED**: "Subjective Opinions". The characters must say things like "I think this is stupid" or "I want this right now!"
        - **REQUIRED**: "Conversational flow". They must argue with each other. Myan says something stupid -> Pyon corrects him coldly -> Myan gets mad.
        
        - **NETIZEN REACTIONS**: Generate 5-8 simulated "Netizen comments" reacting to this news. 
          - Make them feel like a Japanese BBS (2ch/5ch). 
          - Mix of: Enthusiastic, critical, cynical, and weird/funny.
        - **POLL**: Suggest a 2-option poll question relevant to the news.
        - **SNS CONTENT**: Generate a short, energetic, curious tweet from Myan. (STRICTLY NO URL). Just a simple "tsubuyaki" or comment on the news.

        Format:
        Return ONLY valid JSON with keys: "title", "content", "description", "tweet_text", "reactions", "poll", "thumbnail_prompt", "slug".
        
        "title": Catchy title starting with 【話題】 or 【衝撃】. Make it clickbaity.
        "slug": English URL-friendly string (kebab-case, lowercase).
        "tweet_text": Myan's tweet (Max 140 chars).
        "description": Short news summary (MUST be in Japanese).
        "reactions": List of objects: [{{"name": "名無しさん", "text": "...", "color": "green/blue/red"}}]
        "poll": {{ "question": "...", "option_a": "...", "option_b": "..." }}
        "thumbnail_prompt": Short English prompt for AI image.
        "product_keywords": List of 3-5 keywords.
        "category": "trend" | "healing" | "surprise" | "flame".
        "comment_myan": Energy burst closing.
        "comment_pyon": Calm closing.
        "content": HTML format (Summary Box + Character Dialogue).
           - Summary Box:
             <div class="news-summary-box">
               <h3>ニュースのポイント</h3>
               <p>[Write a factual, dry summary here (3-5 sentences). This is the ONLY place for neutral facts.]</p>
             </div>
           - Dialogue:
             <div class="chat-row chat-myan">
               <div class="chat-avatar"><img src="/mascot_cat.png" alt="Myan"></div>
               <div class="chat-bubble">Myan's subjective, emotional take...</div>
             </div>
             <div class="chat-row chat-pyon">
               <div class="chat-avatar"><img src="/mascot_bunny.png" alt="Pyon"></div>
               <div class="chat-bubble">Pyon's sharp, analytical rebuttal...</div>
             </div>
             (Continue the argument for at least 4-5 turns)
        """
        
        response = model.generate_content(prompt, safety_settings=SAFETY_SETTINGS)
        text = response.text
        
        # Robust JSON extraction
        try:
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(), strict=False)
                if not isinstance(data, dict):
                    print(f"DEBUG: Initial JSON is not a dict, it is {type(data)}. Triggers repair.")
                    raise ValueError("JSON is not a dictionary")
                    
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
                    slug_response = model.generate_content(slug_prompt, safety_settings=SAFETY_SETTINGS)
                    clean_slug = slug_response.text.strip().lower().replace(" ", "-").replace('"', '').replace("'", "").replace("`", "")
                    # Ensure only valid chars
                    clean_slug = re.sub(r'[^a-z0-9-]', '', clean_slug)
                    print(f"DEBUG: Generated dedicated slug: {clean_slug}")
                    data["slug"] = clean_slug
                except Exception as e:
                    print(f"DEBUG: Failed to generate dedicated slug: {e}")
                    # Fallback to None, will use ID
                
                # --- NEW: Ensure reactions and poll exist ---
                is_reactions_ok = isinstance(data.get("reactions"), list) and len(data.get("reactions", [])) >= 3
                is_poll_ok = isinstance(data.get("poll"), dict) and "question" in data.get("poll", {})
                
                if not is_reactions_ok or not is_poll_ok:
                    print(f"DEBUG: Missing mandatory fields (Reactions: {is_reactions_ok}, Poll: {is_poll_ok}).")
                    # We can try to repair or just accept it, but for high quality, let's try to fill them if missing
                    if not is_reactions_ok:
                        data["reactions"] = [
                            {"name": "名無しさん", "text": "これマジかよ…衝撃的すぎるだぜ！", "color": "blue"},
                            {"name": "通りすがりの猫", "text": "世の中何が起こるかわからないにゃ。怖いぜ！", "color": "green"},
                            {"name": "匿名ウサギ", "text": "冷静に分析する必要がありますわね。興味深いですわ。", "color": "red"}
                        ]
                    if not is_poll_ok:
                        data["poll"] = {
                            "question": "このニュース、どう思いますか？",
                            "option_a": "驚いた",
                            "option_b": "やっぱりな"
                        }
                # ---------------------------------------------
                
                print(f"DEBUG: Final Data keys: {list(data.keys())}")
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
                {{
                    "title": "...",
                    "content": "...",
                    "comment_myan": "...",
                    "comment_pyon": "...",
                    "slug": "..."
                }}

                Input:
                {text}
                """
                repair_resp = model.generate_content(repair_prompt, safety_settings=SAFETY_SETTINGS)
                repair_text = repair_resp.text
                repair_match = re.search(r'\{.*\}', repair_text, re.DOTALL)
                if repair_match:
                    data = json.loads(repair_match.group(), strict=False)
                    if not isinstance(data, dict):
                         print(f"DEBUG: Repaired JSON is not a dict, it is {type(data)}. Abort.")
                         return None
                         
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

                    # --- NEW: Ensure comments exist (Retry Logic - Repair Path) ---
                    raw_myan = data.get("comment_myan")
                    raw_pyon = data.get("comment_pyon")
                    
                    # Check for None, Empty String, or "None" string
                    is_myan_missing = raw_myan is None or not str(raw_myan).strip() or str(raw_myan).lower() == "none"
                    is_pyon_missing = raw_pyon is None or not str(raw_pyon).strip() or str(raw_pyon).lower() == "none"

                    if is_myan_missing or is_pyon_missing:
                        print("DEBUG: Comments missing (Repair). Invoking Persistent Retry Loop...")
                        m, p = fetch_mascot_comments_persistent(
                            model, 
                            trend_data['title'], 
                            data.get('description', ''), 
                            SAFETY_SETTINGS
                        )
                        data["comment_myan"] = m
                        data["comment_pyon"] = p
                    # ---------------------------------------------

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
                            slug_response = model.generate_content(slug_prompt, safety_settings=SAFETY_SETTINGS)
                            clean_slug = slug_response.text.strip().lower().replace(" ", "-").replace('"', '').replace("'", "").replace("`", "")
                            clean_slug = re.sub(r'[^a-z0-9-]', '', clean_slug)
                            print(f"DEBUG: Generated dedicated slug (in repair): {clean_slug}")
                            data["slug"] = clean_slug
                        except Exception as e:
                            print(f"DEBUG: Failed to generate dedicated slug in repair: {e}")
                            
                    print(f"DEBUG: Final Data comments (Repair): Myan={data.get('comment_myan')}, Pyon={data.get('comment_pyon')}")
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
            "platform": post_data["platform"],
            "image_url": post_data["imageUrl"],
            "comment_myan": post_data.get("comment_myan"),
            "comment_pyon": post_data.get("comment_pyon"),
            "tweet_text": post_data.get("tweet_text", ""),
            "reactions": post_data.get("reactions", []), # New Reactions column
            "created_at": post_data["created_at"],
            "slug": post_data.get("slug", None), # Save SEO slug
            "source_url": post_data.get("source_url", None), # Save source URL for duplicate check
            "product_keywords": post_data.get("product_keywords", []) # Save AI generated keywords
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
        # Check duplication
        if check_is_duplicate(trend['title'], trend['link']):
             print(f"Skipping duplicate: {trend['title']}")
             continue
        else:
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
    
    # Check if running in GitHub Actions (where local files are volatile)
    is_gha = os.environ.get('GITHUB_ACTIONS') == 'true'
    
    # If GHA or AI prompt exists, use a remote URL (Pollinations)
    # FORCE REMOTE: To avoid local file path issues on live site, always use Pollinations or OgImage.
    # If we have a good OG Image, use it? No, keeping consistent style is better.
    # Let's use Pollinations by default for reliability unless user sets up Storage.
    prompt_text = ai_content.get("thumbnail_prompt", post_title)
    import urllib.parse
    prompt_clean = urllib.parse.quote(prompt_text)
    ai_thumb_url = f"https://image.pollinations.ai/prompt/{prompt_clean}?width=1200&height=630&nologo=true&seed={random.randint(0, 99999)}"
    print(f"Using remote thumbnail (Forced): {ai_thumb_url}")
    thumb_url = ai_thumb_url 
    
    # Ensure Fallback Poll
    if not poll_data:
        print("WARNING: Poll data missing. using fallback.")
        poll_data = {
            "question": "このニュース、どう思いますか？",
            "option_a": "驚いた！",
            "option_b": "想定内"
        }

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
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
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
    
    # 6. Update sitemap
    print("\n--- Updating Sitemap ---")
    try:
        from generate_sitemap import generate_sitemap
        generate_sitemap()
    except Exception as e:
        print(f"Sitemap update failed: {e}")
        
    print("--- Done ---")

if __name__ == "__main__":
    main()
