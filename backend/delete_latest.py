from supabase_client import supabase

def delete_latest():
    # Get latest ID
    res = supabase.table("posts").select("id").order("created_at", desc=True).limit(1).execute()
    if res.data:
        latest_id = res.data[0]["id"]
        print(f"Deleting post: {latest_id}")
        supabase.table("posts").delete().eq("id", latest_id).execute()
        print("Deleted.")
    else:
        print("No posts to delete.")

if __name__ == "__main__":
    delete_latest()
