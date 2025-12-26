
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def deactivate_product():
    # ID for "楽天市場" (Generic Moshimo Banner)
    target_id = "192e2b99-65ca-422c-9c27-c3f8b9491c74"
    print(f"--- Deactivating Product ID: {target_id} ---")
    
    res = supabase.table("products").update({"active": False}).eq("id", target_id).execute()
    
    if res.data:
        print(f"Successfully deactivated: {res.data[0]['name']}")
    else:
        print("Failed to update or product not found.")

if __name__ == "__main__":
    deactivate_product()
