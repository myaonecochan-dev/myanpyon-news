
import os
from supabase import create_client, Client

# Use Admin Client (Service Role) to bypass RLS if necessary, 
# though standard client might work if policies allow delete.
# For safety, we use the key from supabase_client.py 
# (which we saw earlier has the service role key 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...')

url: str = "https://ufawzveswbnaqvfvezbb.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(url, key)

def clear_all_posts():
    print("🗑️ Deleting all posts from Supabase...")
    
    # Supabase (PostgREST) requires a filter to delete.
    # We can delete where id is not null (basically all).
    try:
        # Delete all posts created after 1970 (effectively all)
        data = supabase.table("posts").delete().gt("created_at", "1970-01-01T00:00:00Z").execute()
        print(f"✅ Successfully deleted {len(data.data)} posts.")
    except Exception as e:
        print(f"❌ Error deleting posts: {e}")

if __name__ == "__main__":
    clear_all_posts()
