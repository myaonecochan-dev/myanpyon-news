import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from thumbnail_gen import generate_thumbnail, download_image
import os

def test_thumb():
    print("--- Starting Thumbnail Debug ---")
    
    # 1. Test Pollinations URL (AI Image)
    ai_prompt = "Cyberpunk Tokyo city at night"
    ai_url = f"https://image.pollinations.ai/prompt/{ai_prompt.replace(' ', '%20')}?width=1200&height=630&nologo=true"
    print(f"Testing AI URL: {ai_url}")
    
    try:
        img = download_image(ai_url)
        if img:
            print(f"✅ AI Image Downloaded: {img.size}")
            url = generate_thumbnail("AI Thumb Test", "debug_ai.png", bg_image_url=ai_url)
            print(f"✅ Thumbnail Generated: {url}")
        else:
            print("❌ AI Image Download Failed")
    except Exception as e:
        print(f"❌ AI Test Error: {e}")

    # 2. Test Real News URL (Yahoo)
    # Use a static one that is likely to exist or a generic one
    news_url = "https://news-pctr.c.yimg.jp/u/f/jpg/20250101/... (simulated)" 
    # Actually let's try a real one from a recent scraping or just a known image
    news_url = "https://s.yimg.jp/images/news/ogp/2024/kiji_ogp_1200_630.png" # Generic Yahoo OGP
    
    print(f"\nTesting News URL: {news_url}")
    try:
        img = download_image(news_url)
        if img:
            print(f"✅ News Image Downloaded: {img.size}")
            url = generate_thumbnail("News Thumb Test", "debug_news.png", bg_image_url=news_url)
            print(f"✅ Thumbnail Generated: {url}")
        else:
            print("❌ News Image Download Failed")
    except Exception as e:
        print(f"❌ News Test Error: {e}")

if __name__ == "__main__":
    test_thumb()
