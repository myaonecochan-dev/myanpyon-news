
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def list_active_products():
    print("--- Listing Active Products ---")
    res = supabase.table("products").select("id, name, keywords").eq("active", True).execute()
    
    if not res.data:
        print("No active products found.")
    else:
        for p in res.data:
            print(f"ID: {p['id']}")
            print(f"Name: {p['name']}")
            print(f"Keywords: {p.get('keywords')}")
            print("-" * 20)

if __name__ == "__main__":
    list_active_products()
