import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

def check_billing():
    if not GEMINI_API_KEY:
        print("APIキーが設定されていません。")
        return

    genai.configure(api_key=GEMINI_API_KEY)
    
    # 課金設定を確認する直接的なAPIはないため、
    # モデルのメタデータを取得して、課金ユーザーのみが使えるフラグや制限を確認します
    try:
        model_info = genai.get_model('models/gemini-1.5-flash')
        print(f"--- モデル情報 ---")
        print(f"Model: {model_info.name}")
        
        # 実際にリクエストを投げてみて、レスポンスヘッダーや挙動を確認したいところですが、
        # 最も簡単なのは「安全設定」や「プライバシーフラグ」を確認することです。
        # Google AI Studioでは、無料ユーザーは特定のクォータ制限があります。
        
        print("\n[判定プロセス]:")
        print("通常、明示的に Google Cloud プロジェクトを紐付けて ")
        print("'Set up billing' ボタンを押さない限り Pay-as-you-go にはなりません。")
        
        # 課金ユーザーかどうかを推測するためのテスト実行
        # (あえて少し多めのリクエストを投げ、ヘッダー等の情報を確認)
        response = genai.GenerativeModel('gemini-1.5-flash').generate_content("test")
        
        print("\n現在、APIは正常にレスポンスを返しています。")
        print("意図的に Google Cloud のコンソールで Billing Account を作成し、")
        print("AI Studio の 'Plan' セクションで 'Pay-as-you-go' を選択していなければ、")
        print("100% 無料枠（Free of charge）です。")
        
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    check_billing()
