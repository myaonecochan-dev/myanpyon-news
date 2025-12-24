# 🚀 デプロイ＆独自ドメイン設定ガイド

AIエージェントによる開発作業は完了しました！
ここからは、**「あなた（ユーザー様）」** に実施していただく作業になります。

このガイド通りに進めれば、世界に一つだけのWebサイトが完成します！

---

## 📋 事前準備（アカウント作成）

まだお持ちでない場合は、以下のアカウントを作成してください（全て無料プランでOK）。

1.  **GitHub**: [https://github.com/](https://github.com/) (ソースコード置き場)
2.  **Vercel**: [https://vercel.com/](https://vercel.com/) (Webサイト公開サーバー)
    *   *Sign Up with GitHub* を選ぶと楽です。

---

## ステップ 1: コードをGitHubにアップロード

あなたのPCにあるコードをGitHubに送ります。
PowerShellなどで、プロジェクトフォルダ（`c:\AI\myanpyonsokumato`）で以下のコマンドを実行してください。

```powershell
# 1. ユーザー名とメール未設定の場合のみ実行
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 2. リポジトリの初期化
git init
git add .
git commit -m "First commit: MyanPyon Site"

# 3. GitHubで「New Repository」を作成し、そのURLを登録
# (画面に表示されるコマンドをコピペするのが一番確実です)
# 例: git remote add origin https://github.com/YourName/repo-name.git

# 4. アップロード
git push -u origin main
```

---

## ステップ 2: Vercelでサイトを公開

1.  **Vercel Dashboard** ([https://vercel.com/dashboard](https://vercel.com/dashboard)) にアクセス。
2.  **"Add New..."** -> **"Project"** をクリック。
3.  **"Import Git Repository"** で、先ほどアップロードしたリポジトリの **"Import"** ボタンを押します。
4.  **"Configure Project"** 画面で設定を行います。
    *   **Project Name**: 好きな名前（例: `myanpyon-news`）
    *   **Framework Preset**: `Vite` (自動検出されます)
    *   **Environment Variables**: 以下のキーと値を入力して **Add** してください。
        *   `VITE_SUPABASE_URL`: (あなたのSupabase URL)
        *   `VITE_SUPABASE_ANON_KEY`: (あなたのSupabase Anon Key)
5.  **"Deploy"** ボタンをクリック！
    *   1分ほど待つと、花吹雪が舞って公開完了です！🎉

---

## ステップ 3: 独自ドメインを設定（推奨）

サイトの信頼性を高めるため、独自ドメインの設定をおすすめします。

### 1. ドメインの購入
お名前.com, Xserverドメイン, Google Domainsなどで好きなドメイン（例: `myanpyon.com`）を購入します。

### 2. Vercelで設定
1.  Vercelのプロジェクト画面で **Settings** > **Domains** を開きます。
2.  **Add** フォームに、購入したドメインを入力します（例: `myanpyon.com`）。
3.  **"Recommended"** の設定を選んで追加します。

### 3. DNSの設定
Vercelの画面に「**Invalid Configuration**」と表示され、以下のような数値（IPアドレス）などが表示されます。

*   **Type**: A Record
*   **Value**: `76.76.21.21` (例)

これを、**ドメインを購入したサイトの管理画面（DNS設定）** に入力します。
*   「ホスト名」は空欄（または @）
*   「TYPE」は A
*   「VALUE / 転送先」に `76.76.21.21`

### 4. 待つ
DNS設定が世界中に反映されるまで、数分〜最大24時間かかります。
Vercelの画面が緑色のチェックマーク ✅ になれば接続完了です！

---

## ⚠️ 注意点：Pythonスクリプトについて

今回のデプロイ（Vercel）は「フロントエンド（Webサイトの見た目）」の公開です。

*   `rss_bot.py` （記事収集）
*   `thumbnail_gen.py` （画像生成）

これら **Pythonの自動化スクリプトは、Vercel上では動きません。**
**あなたのPC（ローカル環境）で、毎日1回実行する** 必要があります。

（※将来的にこれも完全自動化したい場合は、「GitHub Actions」や「Supabase Edge Functions」への移行が必要になりますが、まずはローカル実行で十分運用可能です！）

---
**Enjoy your new media site!** 🐱🐰
