
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def fix_affiliate_data():
    print("--- Fixing Affiliate Data ---")

    # Update Data Map
    # name match -> new data
    updates = {
        "【癒やし】めぐりズム 蒸気でホットアイマスク 完熟ゆずの香り 12枚入": {
            "image_url": "https://image.pollinations.ai/prompt/hot%20eye%20mask%20package%20box%20japanese%20product%20photorealistic?width=800&height=800&nologo=true",
            "amazon_link": "" # Remove Amazon
        },
        "【ペット】CIAO ちゅ～る まぐろ 海鮮ミックス味 14g×20本": {
            "image_url": "https://image.pollinations.ai/prompt/ciao%20churu%20cat%20treats%20package%20tuna%20flavor%20japanese?width=800&height=800&nologo=true",
            "amazon_link": ""
        },
        "【トレンド】楽天市場 デイリーランキング総合1位アイテム": {
            # Rakuten Logo is usually stable, but let's ensure it's a good one or keep specific if it worked.
            # User didn't complain about this one specifically but "images not displaying well".
            # The uploaded screenshot shows broken images for ALL except maybe the logo?
            # Let's use a solid specific ranking icon.
            "image_url": "https://image.pollinations.ai/prompt/gold%20crown%20ranking%20number%201%20icon%203d?width=800&height=800&nologo=true",
            "amazon_link": "" 
        },
        "【ガジェット】Apple Watch Series 9": {
            "image_url": "https://image.pollinations.ai/prompt/apple%20watch%20series%209%20product%20photo%20clean%20background?width=800&height=800&nologo=true",
            "amazon_link": ""
        },
        "【防災】防災セット 地震対策30点避難セット": {
            "image_url": "https://image.pollinations.ai/prompt/emergency%20disaster%20kit%20backpack%20japanese%20bousai?width=800&height=800&nologo=true",
            "amazon_link": ""
        }
    }

    for name, data in updates.items():
        print(f"Updating: {name}")
        res = supabase.table("products").update(data).eq("name", name).execute()
        if res.data:
            print("  -> Success")
        else:
            print("  -> Failed (Not match?)")

if __name__ == "__main__":
    fix_affiliate_data()
