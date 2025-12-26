import os
import random
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fix_holiday_image():
    print("Searching for Holiday post...")
    # Search by part of the slug provided by user
    slug_part = "2025-new-year-9-day-holiday"
    res = supabase.table("posts").select("*").ilike("slug", f"%{slug_part}%").limit(1).execute()
    
    if not res.data:
        print("Post NOT found.")
        return

    post = res.data[0]
    print(f"Found Post: {post['title']}")
    print(f"Old Image: {post['image_url']}")

    # Generate new robust URL
    # Prompt focus: Specific Japanese items (Shimekazari, Kagami Mochi, Tatami) to force "Japanese" look
    # Avoiding 'festive' to prevent Chinese Lunar New Year bias (red/gold).
    prompt = "Japanese 2025 calendar on a coaster, kagami mochi (japanese rice cake) on wooden desk, tatami mat background, soft sunlight, slice of life anime style, pastel colors"
    prompt_encoded = prompt.replace(" ", "%20")
    seed = random.randint(0, 99999)
    new_url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=1200&height=630&nologo=true&seed={seed}"
    
    print(f"New Image: {new_url}")

    supabase.table("posts").update({"image_url": new_url}).eq("id", post['id']).execute()
    print("Update complete.")

if __name__ == "__main__":
    fix_holiday_image()
