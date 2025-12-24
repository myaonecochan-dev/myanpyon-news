
import os
import time
import ssl
import urllib.request
import xml.etree.ElementTree as ET
import uuid
from supabase import create_client, Client
from thumbnail_gen import generate_thumbnail

# --- Configuration ---
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
# Service Role Key (Admin)
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

RSS_FEEDS = [
    {
        "url": "https://news.yahoo.co.jp/rss/topics/it.xml",
        "category": "trend",
        "source": "Yahoo News"
    },
    {
        "url": "https://www.gizmodo.jp/index.xml",
        "category": "surprise",
        "source": "Gizmodo"
    }
]

# --- Setup Supabase ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_rss(url):
    print(f"Fetching {url}...")
    try:
        # Ignore SSL errors for simplicity in dev
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
            xml_content = response.read()
            return xml_content
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_ai_image_url(text):
    """
    Analyzes text and returns a Pollinations.ai URL for a generating a matching image.
    """
    text_lower = text.lower()
    prompt = "technology abstract wallpaper 4k" # Default
    
    keywords = {
        "iphone": "iphone 15 pro max titanium sleek cinematic lighting",
        "android": "android smartphone futuristic interface glow",
        "google": "google seamless colorful abstract shapes",
        "apple": "apple macbook pro elegant desk setup",
        "ai": "artificial intelligence brain neural network glowing blue cyber",
        "robot": "cute futuristic robot white clean design",
        "drone": "drone flying in sky 4k realistic",
        "game": "gaming setup neon lights cyber controller",
        "nintendo": "nintendo switch gaming bright pop colors",
        "ps5": "playstation 5 console futuristic white blue light",
        "twitter": "smartphone social media app icons floating glassmorphism",
        "sns": "smartphone social media app icons floating glassmorphism",
        "camera": "professional dslr camera lens reflection",
        "space": "galaxy stars nebula cosmic 4k",
        "car": "luxury electric car future concept road",
        "cat": "cute cat fluffy high quality photo",
        "dog": "cute puppy high quality photo",
        "アプリ": "smartphone application interface ios modern ui colorful",
        "スマホ": "modern smartphone device technology sleek",
        "app": "smartphone application interface modern ui",
    }
    
    found_key = None
    for key, p in keywords.items():
        if key in text_lower:
            prompt = p
            found_key = key
            break
    
    # Encode prompt
    import urllib.parse
    encoded_prompt = urllib.parse.quote(prompt)
    
    print(f"  -> Context detected: {found_key if found_key else 'default'} (Prompt: {prompt[:20]}...)")
    
    # Use Pollinations AI (free, no key)
    # nologo=true hides standard logo if supported, or crop later. 
    # model=flux is safer for quality if available, or just default.
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&nologo=true&model=flux"

def parse_and_insert(xml_content, category, source):
    if not xml_content:
        return

    try:
        root = ET.fromstring(xml_content)
        # Handle RSS 2.0 (channel/item) and Atom (entry) - roughly
        items = root.findall('./channel/item')
        if not items:
            items = root.findall('.//{http://purl.org/rss/1.0/}item') # RSS 1.0

        print(f"Found {len(items)} items.")

        count = 0
        for item in items:
            if count >= 10: # Limit to 10 per feed (total 20 for 2 feeds)
                break

            title = item.find('title').text if item.find('title') is not None else "No Title"
            link = item.find('link').text if item.find('link') is not None else ""
            description = item.find('description').text if item.find('description') is not None else ""
            
            # Basic cleanup
            if not link:
                continue

            # Check if exists (using description search as proxy for URL if schema doesn't have URL field unique)
            # Actually we'll search by title to be safe
            existing = supabase.table("posts").select("id").eq("title", title).execute()
            if existing.data:
                print(f"Skipping existing: {title[:20]}...")
                continue

            # Try to find an image
            image_source_url = None
            
            # 1. Check enclosure
            enclosure = item.find('enclosure')
            if enclosure is not None:
                image_source_url = enclosure.get('url')
            
            # 2. Check media:content / media:thumbnail (namespaces are annoying in etree)
            if not image_source_url:
                # Naive check for attributes in all tags if namespace parsing is hard
                # Or use regex on the raw XML string for the item?
                # Let's try explicit namespaces if defined, otherwise iterate
                for child in item:
                    if 'content' in child.tag or 'thumbnail' in child.tag:
                         if child.get('url'):
                             image_source_url = child.get('url')
                             break

            # 3. Regex match in description
            if not image_source_url:
                import re
                img_match = re.search(r'<img[^>]+src="([^">]+)"', description or "")
                if img_match:
                    image_source_url = img_match.group(1)

            # 4. Context-Aware Fallback (Pollinations AI)
            if not image_source_url:
                image_source_url = get_ai_image_url(title + " " + description)

            # Generate Thumbnail
            try:
                # Create a unique filename
                filename = f"thumb_{uuid.uuid4()}.png"
                # Generate!
                print(f"Generating thumbnail for: {title[:20]}...")
                
                # Pass header image (from RSS or AI)
                thumb_url = generate_thumbnail(title, filename, bg_image_url=image_source_url)
                
            except Exception as e:
                print(f"Thumbnail generation failed: {e}")
                thumb_url = "/mascot_cat.png" # Fallback to mascot


            # Insert
            post_data = {
                "title": title,
                "category": category,
                "type": "article",
                "platform": "article",
                "description": f"Starting from {source}: {description[:100]}...",
                "content": f"<p>{description}</p><p><a href='{link}' target='_blank'>続きを読む ({source})</a></p>",
                "image_url": thumb_url
            }

            try:
                supabase.table("posts").insert(post_data).execute()
                print(f"Inserted: {title[:20]}...")
                count += 1
            except Exception as e:
                print(f"Insert error: {e}")

    except Exception as e:
        print(f"Parse error: {e}")

def run_bot():
    print("Starting content bot...")
    for feed in RSS_FEEDS:
        xml_data = fetch_rss(feed["url"])
        parse_and_insert(xml_data, feed["category"], feed["source"])
    print("Bot finished.")

if __name__ == "__main__":
    run_bot()
