
from supabase_client import supabase

def check_latest():
    try:
        response = supabase.table('posts').select('*').order('created_at', desc=True).limit(1).execute()
        print("Latest Post in DB:", response.data)
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    check_latest()
