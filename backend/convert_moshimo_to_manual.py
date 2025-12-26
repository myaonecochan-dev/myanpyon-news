
import os
from supabase_client import supabase

print("Converting Switch 2...")
# Switch 2 Data
switch_img = "https://thumbnail.image.rakuten.co.jp/@0_mall/keitai-god2a/cabinet/11328076/4902370553031.jpg"
switch_link = "https://item.rakuten.co.jp/keitai-god2a/4902370553031/"

res = supabase.table("products").update({
    "image_url": switch_img,
    "rakuten_link": switch_link,
    "moshimo_html": None, # Clear this to force manual rendering
    "price": "" # Ensure price is empty as requested
}).eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()
print(f"Switch 2 Updated: {res}")


print("Converting MegRhythm...")
# MegRhythm Data
meg_img = "https://thumbnail.image.rakuten.co.jp/@0_mall/rakuten24/cabinet/277/4901301455277.jpg"
meg_link = "https://item.rakuten.co.jp/rakuten24/4901301455277/"

res = supabase.table("products").update({
    "image_url": meg_img,
    "rakuten_link": meg_link,
    "moshimo_html": None, # Clear this to force manual rendering
    "price": "" # Ensure price is empty as requested
}).eq("name", "MegRhythm Hinoki").execute()
print(f"MegRhythm Updated: {res}")

print("Done. Items should now use standard manual layout.")
