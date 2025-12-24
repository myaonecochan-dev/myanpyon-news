
import os
import uuid
import datetime
from thumbnail_gen import generate_thumbnail
from supabase_client import supabase

def insert_demo_post():
    # 1. Generate Clean Thumbnail
    # Use a high-quality Unsplash image (Cat)
    image_url = "https://images.unsplash.com/photo-1543852786-1cf6624b9987?q=80&w=1200"
    print("Generating clean thumbnail...")
    thumbnail_path = generate_thumbnail("Title Ignored For Photo", f"demo_clean_{uuid.uuid4().hex[:8]}.png", bg_image_url=image_url)
    print(f"Thumbnail generated: {thumbnail_path}")

    # 2. Prepare Post Data
    post_id = str(uuid.uuid4())
    title = "【デモ】文字なしサムネイルの記事テスト：写真は雄弁に語る"
    description = "これは文字入れを行わない「クリーンなサムネイル」のテスト記事です。写真のインパクトだけでクリック率がどう変わるか、実験してみましょう！みゃんもぴょんも、このスタイルの方がニュースっぽいと言っています。"
    
    # 3. Insert into Supabase
    data = {
        "id": post_id,
        "title": title,
        "description": description,
        "content": "<h2>写真サムネイルの力</h2><p>文字情報がない分、ビジュアルの力が試されます。</p><h3>メリット</h3><ul><li>プロっぽい</li><li>ごちゃごちゃしない</li></ul>",
        "category": "animals", # Use 'animals' (healing) or 'trend'
        "platform": "article",
        "type": "article",
        "image_url": thumbnail_path,
        # "source_url": ... Not in schema? Let's omit or map to thread_url if appropriate?
        # Actually schema doesn't have source_url.
        "video_id": None, 
        # "twitter_id": None # Not in schema
        "created_at": datetime.datetime.now().isoformat()
    }
    
    print("Inserting post into Supabase...")
    response = supabase.table("posts").insert(data).execute()
    print("Success!", response)

if __name__ == "__main__":
    insert_demo_post()
