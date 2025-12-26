
import os
from supabase import create_client, Client

# Hardcode creds to avoid env loading issues in one-liners
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(URL, KEY)

def check_dates():
    print("--- Checking Top 5 Posts by Created Date ---")
    res = supabase.table("posts").select("title, created_at").order("created_at", desc=True).limit(5).execute()
    
    for i, post in enumerate(res.data):
        print(f"{i+1}. {post['created_at']} - {post['title']}")

if __name__ == "__main__":
    check_dates()
