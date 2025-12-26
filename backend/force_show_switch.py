
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def force_show_switch():
    print("--- Forcing Switch to Show on Family Articles ---")
    # Add 'family', 'healing', 'love' to keywords so it matches the current post
    
    target_name = "Nintendo Switch 2 (Moshimo Test)"
    
    # Fetch current
    res = supabase.table("products").select("keywords").eq("name", target_name).execute()
    if not res.data:
        print("Product not found.")
        return

    current_keywords = res.data[0]['keywords']
    new_keywords = list(set(current_keywords + ["family", "healing", "love", "tears"]))
    
    update_res = supabase.table("products").update({"keywords": new_keywords}).eq("name", target_name).execute()
    
    if update_res.data:
        print(f"Updated keywords: {update_res.data[0]['keywords']}")

if __name__ == "__main__":
    force_show_switch()
