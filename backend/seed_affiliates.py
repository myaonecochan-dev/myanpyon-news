
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def seed_affiliates():
    products = [
        {
            "name": "【癒やし】めぐりズム 蒸気でホットアイマスク 完熟ゆずの香り 12枚入",
            "price": "¥1,180",
            "image_url": "https://tshop.r10s.jp/rakuten24/cabinet/125/4901301348036.jpg", # Examplary Real Image
            "amazon_link": "https://www.amazon.co.jp/s?k=%E3%82%81%E3%81%90%E3%82%8A%E3%82%BA%E3%83%A0",
            "rakuten_link": "https://search.rakuten.co.jp/search/mall/%E3%82%81%E3%81%90%E3%82%8A%E3%82%BA%E3%83%A0/",
            "keywords": ["family", "health", "love", "tears", "crying", "healing", "疲れ", "家族"],
            "active": True
        },
        {
            "name": "【ペット】CIAO ちゅ～る まぐろ 海鮮ミックス味 14g×20本",
            "price": "¥980",
            "image_url": "https://tshop.r10s.jp/rakuten24/cabinet/858/4901133720376.jpg",
            "amazon_link": "https://www.amazon.co.jp/s?k=%E3%81%A1%E3%82%85%E3%83%BC%E3%82%8B",
            "rakuten_link": "https://search.rakuten.co.jp/search/mall/%E3%81%A1%E3%82%85%E3%83%BC%E3%82%8B/",
            "keywords": ["animal", "cat", "dog", "healing", "pet", "funny", "猫", "動物"],
            "active": True
        },
        {
            "name": "【トレンド】楽天市場 デイリーランキング総合1位アイテム",
            "price": "Check!",
            "image_url": "https://r.r10s.jp/com/img/home/logo/rakuten_logo_color.png", # Rakuten Logo
            "amazon_link": "",
            "rakuten_link": "https://ranking.rakuten.co.jp/",
            "keywords": ["trend", "news", "japan", "money", "politics", "話題", "ニュース"],
            "active": True
        },
        {
            "name": "【ガジェット】Apple Watch Series 9",
            "price": "¥59,800~",
            "image_url": "https://tshop.r10s.jp/biccamera/cabinet/product/121/00000012117565_a01.jpg",
            "amazon_link": "https://www.amazon.co.jp/s?k=Apple+Watch",
            "rakuten_link": "https://search.rakuten.co.jp/search/mall/Apple+Watch/",
            "keywords": ["surprise", "tech", "gadget", "future", "ガジェット", "最新"],
            "active": True
        },
         {
            "name": "【防災】防災セット 地震対策30点避難セット",
            "price": "¥13,800",
            "image_url": "https://tshop.r10s.jp/pro-bousai/cabinet/03643715/imgrc0068564028.jpg",
            "amazon_link": "https://www.amazon.co.jp/s?k=%E9%98%B2%E7%81%BD%E3%82%BB%E3%83%83%E3%83%88",
            "rakuten_link": "https://search.rakuten.co.jp/search/mall/%E9%98%B2%E7%81%BD%E3%82%BB%E3%83%83%E3%83%88/",
            "keywords": ["news", "accident", "incident", "flame", "safety", "地震", "防災"],
            "active": True
        }
    ]

    print(f"--- Seeding {len(products)} Real Affiliate Products ---")
    
    for p in products:
        # Check if exists by name to avoid dupes purely for this test script
        check = supabase.table("products").select("id").eq("name", p["name"]).execute()
        if not check.data:
            res = supabase.table("products").insert(p).execute()
            if res.data:
                print(f"Inserted: {p['name']}")
        else:
             # If exists, ensure active and update keywords
             print(f"Updating existing: {p['name']}")
             supabase.table("products").update(p).eq("name", p["name"]).execute()

if __name__ == "__main__":
    seed_affiliates()
