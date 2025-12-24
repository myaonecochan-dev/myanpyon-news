
import os
from supabase import create_client, Client
import dotenv

# Load env if available, otherwise use hardcoded for dev environment as established
url = "https://ufawzveswbnaqvfvezbb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(url, key)

def create_test_pasts():
    print("Creating test posts...")
    
    # 1. YouTube Video
    data_yt = {
        "title": "【DBテスト】Supabaseから来たYouTube動画",
        "category": "trend",
        "type": "video",
        "platform": "youtube",
        "description": "これはPythonスクリプトから挿入されたテストデータです。YouTubeの表示確認。",
        "video_id": "dQw4w9WgXcQ", # Never gonna give you up
        "image_url": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg"
    }
    
    # 2. Article
    data_article = {
        "title": "【DBテスト】Supabaseから来たテキスト記事",
        "category": "flame",
        "type": "article",
        "platform": "article",
        "description": "これは記事形式のテストデータです。",
        "content": "<h2>DB連携成功！</h2><p>PythonからSupabaseへデータを書き込み、Reactで読み込んでいます。</p>",
        "image_url": "https://via.placeholder.com/640x360.png?text=DB+Test"
    }

    try:
        res1 = supabase.table("posts").insert(data_yt).execute()
        print(f"Inserted YouTube post: {res1.data[0]['id']}")
        
        res2 = supabase.table("posts").insert(data_article).execute()
        print(f"Inserted Article post: {res2.data[0]['id']}")
        
    except Exception as e:
        print(f"Error inserting: {e}")

if __name__ == "__main__":
    create_test_pasts()
