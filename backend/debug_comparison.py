
import os
from supabase import create_client, Client
from dotenv import load_dotenv

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(URL, KEY)

def debug_sort_order():
    print("--- Searching for 'Foreign Driver' (外国人ドライバー) post ---")
    res = supabase.table("posts").select("title, created_at").ilike("title", "%外国人ドライバー%").execute()
    
    truck_post_time = None
    if res.data:
        truck_post = res.data[0]
        truck_post_time = truck_post['created_at']
        print(f"FOUND: {truck_post['title']}")
        print(f"Created At: {truck_post['created_at']}")
    else:
        print("NOT FOUND in DB.")
        
    print("\n--- Comparing with 'Nigeria' post ---")
    res_nigeria = supabase.table("posts").select("title, created_at").ilike("title", "%ナイジェリア%").execute()
    
    nigeria_post_time = None
    if res_nigeria.data:
        nigeria_post = res_nigeria.data[0]
        nigeria_post_time = nigeria_post['created_at']
        print(f"FOUND: {nigeria_post['title']}")
        print(f"Created At: {nigeria_post['created_at']}")
        
    if truck_post_time and nigeria_post_time:
        print(f"\nIs Truck newer than Nigeria? {truck_post_time > nigeria_post_time}")

if __name__ == "__main__":
    debug_sort_order()
