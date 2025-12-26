import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_duplicate():
    target_slug = "japan-record-snow-warning-1226" # This is the duplicate (later one)
    print(f"Deleting post with slug: {target_slug}...")
    
    # Verify before delete
    res = supabase.table("posts").select("*").eq("slug", target_slug).execute()
    if not res.data:
        print("Post not found.")
        return

    supabase.table("posts").delete().eq("slug", target_slug).execute()
    print("Delete successful.")

if __name__ == "__main__":
    delete_duplicate()
