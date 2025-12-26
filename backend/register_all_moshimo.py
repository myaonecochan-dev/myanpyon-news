import os
from supabase_client import supabase

# Removed duplicate init code

# 1. Nintendo Switch 2 (Update to XS size)
switch_html = """<!-- START MoshimoAffiliateEasyLink -->
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

# 2. MegRhythm (New Item)
megrhythm_html = """<!-- START MoshimoAffiliateEasyLink -->
<script type="text/javascript">
(function(b,c,f,g,a,d,e){b.MoshimoAffiliateObject=a;
b[a]=b[a]||function(){arguments.currentScript=c.currentScript
||c.scripts[c.scripts.length-2];(b[a].q=b[a].q||[]).push(arguments)};
c.getElementById(a)||(d=c.createElement(f),d.src=g,
d.id=a,e=c.getElementsByTagName("body")[0],e.appendChild(d))})
(window,document,"script","//dn.msmstatic.com/site/cardlink/bundle.js?20220329","msmaflink");
msmaflink({"n":"めぐりズム 蒸気めぐるアイマスク ひのき(12枚入)【めぐりズム】","b":"","t":"","d":"https:\/\/thumbnail.image.rakuten.co.jp","c_p":"\/@0_mall\/rakuten24\/cabinet\/277","p":["\/4901301455277.jpg"],"u":{"u":"https:\/\/item.rakuten.co.jp\/rakuten24\/4901301455277\/","t":"rakuten","r_v":""},"v":"2.1","b_l":[{"id":1,"u_tx":"楽天市場で見る","u_bc":"#f76956","u_url":"https:\/\/item.rakuten.co.jp\/rakuten24\/4901301455277\/","a_id":5317132,"p_id":54,"pl_id":27059,"pc_id":54,"s_n":"rakuten","u_so":1}],"eid":"9ZTEx","s":"s"});
</script>
<div id="msmaflink-9ZTEx">リンク</div>
<!-- MoshimoAffiliateEasyLink END -->"""

# Update Switch 2
print("Updating Switch 2 to XS size...")
res = supabase.table("products").update({"moshimo_html": switch_html}).eq("name", "Nintendo Switch 2 (Moshimo Test)").execute()
print(res)

# Register MegRhythm
print("Registering MegRhythm...")
# Check if exists first to avoid duplicates or update if exists
existing = supabase.table("products").select("*").eq("name", "MegRhythm Hinoki").execute()
if existing.data:
    res = supabase.table("products").update({"moshimo_html": megrhythm_html, "active": True}).eq("name", "MegRhythm Hinoki").execute()
    print("Updated MegRhythm.")
else:
    res = supabase.table("products").insert({
        "name": "MegRhythm Hinoki",
        "price": "Check Rakuten", # Not shown but required schema usually
        "image_url": "", # Handled by Moshimo
        "moshimo_html": megrhythm_html,
        "active": True,
        "keywords": ["relax", "eye", "health", "sleep", "gift", "hinoki"]
    }).execute()
    print("Inserted MegRhythm.")

print("Done.")
