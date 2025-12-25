import os
from supabase_client import supabase
from datetime import datetime

BASE_URL = "https://myanpyon.com"  # Update this if the domain changes
SITEMAP_PATH = "../public/sitemap.xml" # Assumes running from backend directory

def generate_sitemap():
    print("Fetching posts for sitemap...")
    try:
        # Fetch all posts, selecting id, slug, created_at
        response = supabase.table("posts").select("id, slug, created_at").execute()
        posts = response.data
        
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Static Routes
        static_routes = [
            {"loc": "/", "priority": "1.0", "changefreq": "daily"},
            {"loc": "/about", "priority": "0.5", "changefreq": "monthly"},
             # Add other static routes as needed
        ]
        
        for route in static_routes:
            xml_content += '  <url>\n'
            xml_content += f'    <loc>{BASE_URL}{route["loc"]}</loc>\n'
            xml_content += f'    <priority>{route["priority"]}</priority>\n'
            xml_content += f'    <changefreq>{route["changefreq"]}</changefreq>\n'
            xml_content += '  </url>\n'

        # Dynamic Post Routes
        for post in posts:
            slug = post.get("slug")
            post_id = post.get("id")
            created_at = post.get("created_at")
            
            # Prefer slug, fallback to ID
            url_suffix = f"/post/{slug}" if slug else f"/post/{post_id}"
            
            # Format date (Supabase returns ISO string, sitemap expects YYYY-MM-DD or ISO)
            # Simple truncation to YYYY-MM-DD usually works and is safe
            last_mod = created_at.split("T")[0] if created_at else datetime.now().strftime("%Y-%m-%d")

            xml_content += '  <url>\n'
            xml_content += f'    <loc>{BASE_URL}{url_suffix}</loc>\n'
            xml_content += f'    <lastmod>{last_mod}</lastmod>\n'
            xml_content += '    <changefreq>never</changefreq>\n' # News articles generally don't change
            xml_content += '  </url>\n'
            
        xml_content += '</urlset>'
        
        # Ensure public directory exists (relative to script execution)
        # Verify where we are running
        target_path = os.path.join(os.path.dirname(__file__), SITEMAP_PATH)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
            
        print(f"Sitemap generated successfully at: {target_path}")
        print(f"Total URLs: {len(static_routes) + len(posts)}")

    except Exception as e:
        print(f"Error generating sitemap: {e}")

if __name__ == "__main__":
    generate_sitemap()
