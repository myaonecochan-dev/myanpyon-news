import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL") or "https://ufawzveswbnaqvfvezbb.supabase.co"
SUPABASE_KEY = os.environ.get("SUPABASE_KEY") or "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

if not SUPABASE_KEY:
    print("SUPABASE_KEY not found.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def test_keyword_storage():
    print("--- Testing Keyword Storage ---")
    
    # 1. Insert a test product with keywords
    product_data = {
        "name": "Test Keyword Product",
        "price": "¥100",
        "image_url": "https://example.com/image.jpg",
        "active": True,
        "keywords": ["winter", "test_match"]
    }
    
    print(f"Inserting product with keywords: {product_data['keywords']}")
    res_product = supabase.table("products").insert(product_data).execute()
    
    if not res_product.data:
        print("Failed to insert product.")
        return
        
    product_id = res_product.data[0]['id']
    print(f"Product inserted. ID: {product_id}")
    
    # 2. Insert a test post with matching keywords
    post_data = {
        "title": "Test Keyword Post",
        "slug": "test-keyword-post-" + str(os.getpid()),
        "content": "Test content",
        "type": "article",
        "platform": "article",
        "category": "trend",
        "description": "desc",
        "product_keywords": ["winter", "snow"]
    }
    
    print(f"Inserting post with keywords: {post_data['product_keywords']}")
    res_post = supabase.table("posts").insert(post_data).execute()
    
    if not res_post.data:
        print("Failed to insert post.")
        return
        
    post_id = res_post.data[0]['id']
    print(f"Post inserted. ID: {post_id}")
    
    # 3. Verify data retrieval
    print("\n--- Verifying Retrieval ---")
    fetched_product = supabase.table("products").select("*").eq("id", product_id).single().execute()
    fetched_post = supabase.table("posts").select("*").eq("id", post_id).single().execute()
    
    p_keywords = fetched_product.data.get('keywords')
    post_keywords = fetched_post.data.get('product_keywords')
    
    print(f"Fetched Product Keywords: {p_keywords}")
    print(f"Fetched Post Keywords: {post_keywords}")
    
    if p_keywords == ["winter", "test_match"] and post_keywords == ["winter", "snow"]:
        print("\n[SUCCESS] Keywords stored and retrieved correctly.")
        
        # Simulate Matching Logic
        print("\n--- Simulating Match Logic ---")
        match_score = 0
        for pk in post_keywords:
            if pk in p_keywords:
                match_score += 1
                
        print(f"Match Score: {match_score} (Expected: 1 for 'winter')")
        if match_score > 0:
             print("[SUCCESS] Matching logic simulation passed.")
    else:
        print("\n[FAILURE] Data mismatch.")
        
    # Cleanup
    print("\n--- Cleaning up ---")
    supabase.table("products").delete().eq("id", product_id).execute()
    supabase.table("posts").delete().eq("id", post_id).execute()
    print("Test data deleted.")

if __name__ == "__main__":
    test_keyword_storage()
