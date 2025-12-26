
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def fix_images_picsum():
    print("--- Fixing Affiliate Images to Picsum ---")

    # Update Data Map
    # Picsum is stable. active=True, amazon_link=""
    updates = {
        "【癒やし】めぐりズム 蒸気でホットアイマスク 完熟ゆずの香り 12枚入": {
            "image_url": "https://picsum.photos/seed/healing_eye/300/300"
        },
        "【ペット】CIAO ちゅ～る まぐろ 海鮮ミックス味 14g×20本": {
            "image_url": "https://picsum.photos/seed/cat_treats/300/300"
        },
        "【トレンド】楽天市場 デイリーランキング総合1位アイテム": {
            "image_url": "https://picsum.photos/seed/rakuten_rank/300/300"
        },
        "【ガジェット】Apple Watch Series 9": {
            "image_url": "https://picsum.photos/seed/apple_watch/300/300" 
        },
        "【防災】防災セット 地震対策30点避難セット": {
            "image_url": "https://picsum.photos/seed/disaster_kit/300/300"
        }
    }

    for name, data in updates.items():
        print(f"Updating Image: {name}")
        res = supabase.table("products").update(data).eq("name", name).execute()
        if res.data:
            print(f"  -> Success: {data['image_url']}")
        else:
            print("  -> Failed (Not match?)")

if __name__ == "__main__":
    fix_images_picsum()
