import sys
import datetime
import uuid
import random
# Import necessary functions from collector
from collector import generate_content_with_gemini, insert_post_to_supabase

def create_manual_post():
    print("--- Manual Post Creator ---")
    
    # Define the "Trend" object manually with gathered details
    # Define the "Trend" object manually with gathered details
    topic_data = {
        "title": "【生存確認】今日は2025年最後の「プレミアムフライデー」です…覚えてますか？ネットで「死語」「幻」と話題に",
        "link": "https://news.yahoo.co.jp/search?p=premium+friday+2025", 
        "description": """
        本日12月26日は、2025年最後の金曜日、つまり「プレミアムフライデー」である。
        かつて政府が推進したこのキャンペーンだが、現在では実施している企業はごくわずか。
        ネット上では「プレ金？都市伝説でしょ」「仕事納めだし早く帰れるわけない」「まだ存在したのか」といった自虐や驚きの声が溢れている。
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
        # Fallback prompt for this specific news (Lonely office or confused calendar)
        thumb_url = "https://image.pollinations.ai/prompt/Empty%20japanese%20office%20at%203pm,%20lonely%20salaryman%20looking%20at%20watch,%20sunset%20light,%20melancholic%20anime%20style,%20premium%20friday%20poster%20peeling%20off?width=1200&height=630&nologo=true"
    
    print(f"Using Thumbnail: {thumb_url}")

    # 3. Assemble Post
    post = {
        "id": str(uuid.uuid4()),
        "title": post_title,
        "description": ai_content.get("description", ""),
        "content": ai_content.get("content", ""),
        "reactions": ai_content.get("reactions", []),
        "category": ai_content.get("category", "healing"), 
        "comment_myan": str(ai_content.get("comment_myan") or ""),
        "comment_pyon": str(ai_content.get("comment_pyon") or ""),
        "type": "article",
        "platform": "article",
        "imageUrl": thumb_url, 
        "tweet_text": ai_content.get("tweet_text", ""),
        "slug": f"{ai_content.get('slug', 'year-end-holidays-2025-9-days-golden-calendar')}-{datetime.datetime.now().strftime('%m%d')}", # Ensure unique
        "created_at": datetime.datetime.now().isoformat(),
        "source_url": topic_data["link"] # Add source_url for duplicate prevention
    }
    
    # Debug print slug
    print(f"Slug: {post['slug']}")

    # 4. Insert
    poll_data = ai_content.get("poll")
    insert_post_to_supabase(post, poll_data=poll_data)
    print("--- Manual Post Completed ---")

if __name__ == "__main__":
    create_manual_post()
