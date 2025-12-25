import sys
import datetime
import uuid
import random
# Import necessary functions from collector
from collector import generate_content_with_gemini, insert_post_to_supabase

def create_manual_post():
    print("--- Manual Post Creator ---")
    
    # Define the "Trend" object manually with gathered details
    topic_data = {
        "title": "スマホも「世界的メモリ不足」で値上がりへ AI需要でDRAM不足深刻",
        "link": "https://news.yahoo.co.jp/", 
        "description": """
        世界的なメモリ不足の影響で、スマートフォンの価格が今後値上がりする見通しだ。
        調査会社によると、2025年から2026年にかけてAIサーバー向けの高性能メモリ需要が急増し、スマホ用メモリの生産ラインが圧迫されているという。
        これによりメモリ価格が高騰し、スマホ本体価格も6.9%〜20%ほど上昇する可能性がある。
        16GBメモリ搭載のハイエンド機が減り、4GBモデルが復活するなど「スペックダウン」の懸念も出ている。
        """
    }

    print(f"Generating content for: {topic_data['title']}")

    # 1. Generate Content using AI
    ai_content = generate_content_with_gemini(topic_data)
    
    if not ai_content:
        print("Failed to generate content.")
        return

    # 2. Thumbnail
    post_title = ai_content.get("title")
    
    # Use AI prompt if available, or force a news-style prompt
    if ai_content.get("thumbnail_prompt"):
        prompt_clean = ai_content["thumbnail_prompt"].replace(" ", "%20")
        thumb_url = f"https://image.pollinations.ai/prompt/{prompt_clean}?width=1200&height=630&nologo=true&seed={random.randint(0, 99999)}"
    else:
        # Fallback prompt for this specific news
        thumb_url = "https://image.pollinations.ai/prompt/Smartphone%20price%20chart%20going%20up,%20red%20arrow,%20memory%20chip%20background,%20tech%20news%20style?width=1200&height=630&nologo=true"
    
    print(f"Using Thumbnail: {thumb_url}")

    # 3. Assemble Post
    post = {
        "id": str(uuid.uuid4()),
        "title": post_title,
        "description": ai_content.get("description", ""),
        "content": ai_content.get("content", ""),
        "reactions": ai_content.get("reactions", []),
        "category": ai_content.get("category", "trend"), 
        "comment_myan": ai_content.get("comment_myan", ""),
        "comment_pyon": ai_content.get("comment_pyon", ""),
        "type": "article",
        "platform": "article",
        "imageUrl": thumb_url, 
        "tweet_text": ai_content.get("tweet_text", ""),
        "slug": f"{ai_content.get('slug', 'sim-shortage-price-hike')}-{datetime.datetime.now().strftime('%m%d')}", # Ensure unique
        "created_at": datetime.datetime.now().isoformat()
    }
    
    # Debug print slug
    print(f"Slug: {post['slug']}")

    # 4. Insert
    poll_data = ai_content.get("poll")
    insert_post_to_supabase(post, poll_data=poll_data)
    print("--- Manual Post Completed ---")

if __name__ == "__main__":
    create_manual_post()
