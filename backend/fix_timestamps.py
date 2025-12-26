
import os
from datetime import datetime, timedelta, timezone
from supabase import create_client, Client

URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def fix_timestamps():
    print("--- Fixing Timestamps (Subtracting 9 hours from Future JST-as-UTC posts) ---")
    
    # 1. Get recent posts
    res = supabase.table("posts").select("*").order("created_at", desc=True).limit(10).execute()
    
    current_utc = datetime.now(timezone.utc)
    print(f"Current UTC: {current_utc}")
    
    for post in res.data:
        try:
            # Parse timestamp (Supabase usually returns strict ISO with Z or +00:00)
            ts_str = post['created_at']
            # Simple parse for comparison
            # Handle variable format
            if ts_str.endswith("Z"):
                ts_str = ts_str[:-1] + "+00:00"
            
            ts = datetime.fromisoformat(ts_str)
            
            # If timestamp is significantly in the future (e.g. > 1 hour ahead of now), it's likely JST-as-UTC
            # Actually, simply checking if it's > current_utc + buffer
            if ts > current_utc + timedelta(minutes=5):
                print(f"FUTURE DETECTED: {post['title']} ({ts})")
                
                # Subtract 9 hours
                new_ts = ts - timedelta(hours=9)
                print(f" -> Correcting to: {new_ts}")
                
                # Update DB
                supabase.table("posts").update({"created_at": new_ts.isoformat()}).eq("id", post['id']).execute()
            else:
                 print(f"OK: {post['title']} ({ts})")
                 
        except Exception as e:
            print(f"Error processing {post['title']}: {e}")

if __name__ == "__main__":
    fix_timestamps()
