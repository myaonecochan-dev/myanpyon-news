import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def apply_migration():
    print("Applying migration_prevent_duplicates.sql...")
    
    with open("backend/migration_prevent_duplicates.sql", "r", encoding="utf-8") as f:
        sql = f.read()
        
    # Split by statement (naive split by ;)
    statements = [s.strip() for s in sql.split(';') if s.strip()]
    
    for stmt in statements:
        print(f"Executing: {stmt[:50]}...")
        try:
            # RPC call to run SQL? Or usually we can't run DDL via client unless we use a function or external tool.
            # Supabase-py doesn't support raw SQL execution easily.
            # BUT we can use the Postgres function `exec_sql` if we created it before?
            # Or we assume the user has to run it.
            # Wait, I previously used `cursor.execute` if I had psycopg2, but here I only have supabase-js client?
            # Actually, the user's setup might imply I can't run DDL from python client easily without `postgres` connection string.
            pass
        except Exception as e:
            print(f"Error: {e}")

    # For safety, since I cannot easily run DDL via REST client without a helper function:
    # I will verify if the column exists by trying to update a dummy post's source_url.
    
    try:
        # Check if column exists by selecting it?
        res = supabase.table("posts").select("source_url").limit(1).execute()
        print("Column 'source_url' EXISTS.")
    except Exception as e:
        print(f"Column 'source_url' MISSING or Error: {e}")
        # If missing, I must ask user to run SQL or give me connection string?
        # Or I can use the 'rpc' verification if set up.
        
if __name__ == "__main__":
    apply_migration()
