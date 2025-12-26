
import os
import sys
from supabase import create_client, Client

# Load env variables (assuming they are set in the environment or we need to load them)
# In this environment, we might not have python-dotenv, so let's check os.environ
# But usually we need to set them.
# I'll check how keys are managed. unique keys are usually in env vars.

try:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not found in environment variables.")
        # Try to load from a local .env file or similar if possible, but let's assume they are present for now
        # or we might need to ask the user.
        # Actually, let's look at backend/collector.py to see how it loads credentials.
        sys.exit(1)

    supabase: Client = create_client(url, key)

    # Try to select the new columns from products table
    try:
        response = supabase.table("products").select("rakuten_impression_url,amazon_impression_url,moshimo_html").limit(1).execute()
        print("Schema check passed: New columns found.")
    except Exception as e:
        print(f"Schema check failed: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
