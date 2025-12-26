import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def register_banner():
    html = """<a href="//af.moshimo.com/af/c/click?a_id=5317132&p_id=54&pc_id=54&pl_id=1223" rel="nofollow" referrerpolicy="no-referrer-when-downgrade" attributionsrc><img src="//image.moshimo.com/af-img/0032/000000001223.gif" width="120" height="120" style="border:none;"></a><img src="//i.moshimo.com/af/i/impression?a_id=5317132&p_id=54&pc_id=54&pl_id=1223" width="1" height="1" style="border:none;" loading="lazy">"""
    
    data = {
        "name": "楽天市場",
        "price": "お買い物はこちら",
        "image_url": "https://image.moshimo.com/af-img/0032/000000001223.gif",
        "moshimo_html": html,
        "active": True
    }
    
    try:
        res = supabase.table("products").insert(data).execute()
        if res.data:
            print(f"Successfully registered banner product: {res.data[0]['name']}")
        else:
            print("Failed to register (no data returned).")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    register_banner()
