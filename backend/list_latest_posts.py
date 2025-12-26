
import os
from supabase import create_client, Client

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def check_timestamps():
    titles_to_check = [
        "筋ジストロフィー",
        "ナイジェリア",
        "飲食料品",
        "外国人ドライバー"
    ]
    
    print("--- Detailed Timestamps ---")
    for t in titles_to_check:
        res = supabase.table("posts").select("title, created_at").ilike("title", f"%{t}%").execute()
        for p in res.data:
            print(f"[{p['title'][:10]}...] : {p['created_at']}")

if __name__ == "__main__":
    check_timestamps()
