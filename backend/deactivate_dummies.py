
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def deactivate_dummies():
    # Dell, Anker, Test Rakuten
    target_ids = [
        "c3ae8444-e481-4c00-8d80-58b9c76fe838",
        "40462bb9-2bf5-4584-b27c-087f23da447d",
        "7f172b71-67eb-41fd-a307-ec07cc231788"
    ]
    print(f"--- Deactivating {len(target_ids)} Dummy Products ---")
    
    for tid in target_ids:
        res = supabase.table("products").update({"active": False}).eq("id", tid).execute()
        if res.data:
            print(f"Deactivated: {res.data[0]['name']}")
        else:
            print(f"Failed/Not Found: {tid}")

if __name__ == "__main__":
    deactivate_dummies()
