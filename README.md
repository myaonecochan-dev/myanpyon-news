# みゃんぴょんそくまと！！ (MyanPyon Sokumato!!)

**Net-Wadai Video & News Summary Media** featuring AI Mascots "Myan" (Cat) and "Pyon" (Rabbit).

![Key Visual](/public/mascot_myan.png) 

## 📝 Overview
This is a modern "Matome" (Summary) site built with **React** and **Supabase**. It automatically collects trending news/videos via RSS, generates AI summaries, and displays them in a "Pop & Premium" design.

## ✨ Key Features
-   **AI Automation**: 
    -   `rss_bot.py`: Fetches news from Yahoo/Gizmodo and inserts into DB.
    -   `thumbnail_gen.py`: Auto-generates thumbnails for text-only articles.
-   **Modern UX**:
    -   **Glassmorphism Header** & **Masonry Grid Layout**.
    -   **Infinite Scroll** & **Skeleton Loading**.
    -   **Mascot Dialogue**: AI characters comment on every article (Soul System).
-   **Admin System**:
    -   `/admin`: PIN-protected dashboard to Manage/Delete/Create posts.
-   **Interactive**:
    -   **Real-time Comments** (Supabase DB).
    -   **Dynamic Ranking**: Top summary box updates automatically.

## 🛠 Tech Stack
-   **Frontend**: React (Vite), TypeScript, CSS Modules (PostCSS)
-   **Backend (BaaS)**: Supabase (PostgreSQL, Auth, Realtime)
-   **Automation**: Python 3.x (Feedparser, Pillow)

## 🚀 Setup & Run
### 1. Install Dependencies
```bash
npm install
```

### 2. Environment Variables
Create `.env` file (or set in Vercel):
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Run Development Server
```bash
npm run dev
```

### 4. Build for Production
```bash
npm run build
```

## 📂 Project Structure
-   `/src`: Frontend React Code
    -   `/components`: Reusable UI (PostCard, MascotChat, etc.)
    -   `/pages`: Route Pages (Home, Post, Admin)
    -   `/lib`: Supabase Clients
-   `/backend`: Python Automation Scripts
    -   `rss_bot.py`: Content Collector
    -   `thumbnail_gen.py`: Image Processor

## 📄 License
MIT License
