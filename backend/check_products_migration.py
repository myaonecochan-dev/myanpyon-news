import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check_migration():
    print("Checking migration status for 'products' table...")
    columns_to_check = ["rakuten_impression_url", "amazon_impression_url", "moshimo_html"]
    
    try:
        # Try to select the specific columns from the products table
        res = supabase.table("products").select(",".join(columns_to_check)).limit(1).execute()
        print("\n[SUCCESS] All expected columns exist in 'products' table:")
        for col in columns_to_check:
            print(f" - {col}")
    except Exception as e:
        print(f"\n[FAILURE] One or more columns are MISSING or there was an error.")
        print(f"Error detail: {e}")
        print("\nPlease ensure you have executed the SQL migration in the Supabase Dashboard.")

if __name__ == "__main__":
    check_migration()
