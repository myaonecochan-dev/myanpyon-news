
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
URL = "https://ufawzveswbnaqvfvezbb.supabase.co"
KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYXd6dmVzd2JuYXF2ZnZlemJiIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2NjU1MjQyNywiZXhwIjoyMDgyMTI4NDI3fQ.uf7mi1zUvLD9CmbAcwIgUNwHhQXUOg9cZ9Pk67C85iQ"

supabase = create_client(URL, KEY)

def register_moshimo():
    print("--- Registering Moshimo Item: Nintendo Switch 2 ---")
    
    # User provided HTML
    html_code = """<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"【新品】【日曜日以外即日発送】最安値挑戦！Nintendo Switch 2 国内版 マリオカート ワールド セット BEE-S-KB6PA 【送料無料】","b":"","t":"","d":"https:\/\/thumbnail.image.rakuten.co.jp","c_p":"","p":["\/@0_mall\/keitai-god2a\/cabinet\/11328076\/4902370553031.jpg"],"u":{"u":"https:\/\/item.rakuten.co.jp\/keitai-god2a\/4902370553031\/","t":"rakuten","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/item.rakuten.co.jp\/keitai-god2a\/4902370553031\/","a_id":5317132,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":1}],"eid":"F5Ujx","s":"s"});
</script>
<div id="msmaflink-F5Ujx">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->"""

    product = {
        "name": "Nintendo Switch 2 (Moshimo Test)",
        "price": "Check!", # Price is handled by widget
        "image_url": "", # Handled by widget
        "amazon_link": "",
        "rakuten_link": "",
        "moshimo_html": html_code,
        "keywords": ["game", "gadget", "trend", "switch", "nintendo", "gift", "surprise", "latest"],
        "active": True
    }
    
    # Update existing "Nintendo Switch 2"
    res = supabase.table("products").update({"moshimo_html": html_code}).eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()
    
    if res.data:
        print(f"Registered: {res.data[0]['name']}")

if __name__ == "__main__":
    register_moshimo()
