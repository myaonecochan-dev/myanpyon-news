/* eslint-disable @typescript-eslint/no-explicit-any */

import { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, useLocation, Link, useSearchParams } from 'react-router-dom';
import { type Post, type Category } from './data/posts';
import { supabase } from './lib/supabaseClient';
import { Sidebar } from './components/Sidebar';
import './App.css';
import { HomePage } from './pages/HomePage';
import { PostPage } from './pages/PostPage';
import { AdminPage } from './pages/AdminPage';
import { AdminPostEditor } from './pages/AdminPostEditor';
import { PrivacyPolicy } from './pages/PrivacyPolicy';
import { ScrollToTopButton } from './components/ScrollToTopButton';
import { FloatingDonationButton } from './components/FloatingDonationButton';


// Wrapper to handle global title/meta logic if needed
const AppContent = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const categoryRaw = searchParams.get('cat') || 'all';
  const category = (['all', 'trend', 'surprise', 'animals', 'flame'].includes(categoryRaw) ? categoryRaw : 'all') as Category | 'all';

  const [allPosts, setAllPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const POSTS_PER_PAGE = 12;
  const location = useLocation();

  // Load generated posts from Supabase
  useEffect(() => {
    fetchSupabasePosts(0, true);
  }, []);

  const fetchSupabasePosts = async (pageIndex: number, reset: boolean = false) => {
    if (reset) {
      setLoading(true);
      setAllPosts([]);
    }

    const start = pageIndex * POSTS_PER_PAGE;
    const end = start + POSTS_PER_PAGE - 1;

    try {
      const { data, error } = await supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })
        .range(start, end);

      if (error) throw error;

      if (data) {

        const formattedPosts: Post[] = data.map((item: any) => {
          // Generate fallback description if missing
          let description = item.description;
          if (!description && item.content) {
            // Strip HTML tags and truncate
            description = item.content.replace(/<[^>]*>?/gm, '').substring(0, 120) + '...';
          }

          return {
            id: item.id,
            title: item.title,
            description: description,
            content: item.content,
            category: item.category as Category,
            type: item.type as any, // Cast to any or strict type if possible
            platform: item.platform as any || 'article',
            youtubeId: item.platform === 'youtube' ? item.video_id : undefined,
            embedId: item.platform !== 'youtube' ? item.video_id : undefined, // Map video_id to embedId for TikTok/Twitter
            imageUrl: item.image_url,
            created_at: item.created_at,
            slug: item.slug,
            comment_myan: item.comment_myan,
            comment_pyon: item.comment_pyon
          };
        });

        console.log("Loaded generated posts from Supabase:", formattedPosts);
        setAllPosts(prev => {
          const combined = reset ? formattedPosts : [...prev, ...formattedPosts];
          // Ensure strictly sorted by date descending for every update
          return combined.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());
        });
        setHasMore(data.length === POSTS_PER_PAGE);
      }
    } catch (err) {
      console.error("Failed to load posts from Supabase:", err);
    } finally {
      setLoading(false);
    }
  };

  const loadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    fetchSupabasePosts(nextPage, false);
  };

  // Scroll to top on route change
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname, category]);

  // Update theme based on category
  useEffect(() => {
    const root = document.documentElement;
    if (category === 'surprise') {
      root.style.setProperty('--primary', '#ff4081');
      root.style.setProperty('--secondary', '#ff80ab');
      root.style.setProperty('--accent', '#c51162');
    } else if (category === 'trend') {
      root.style.setProperty('--primary', '#007bff');
      root.style.setProperty('--secondary', '#69b3ff');
      root.style.setProperty('--accent', '#0056b3');
    } else if (category === 'flame') {
      root.style.setProperty('--primary', '#dc3545');
      root.style.setProperty('--secondary', '#e4606d');
      root.style.setProperty('--accent', '#bd2130');
    } else {
      root.style.setProperty('--primary', '#00bfa5');
      root.style.setProperty('--secondary', '#64ffda');
      root.style.setProperty('--accent', '#009688');
    }
  }, [category]);

  const getHeaderTitle = () => {
    return 'みゃんぴょんそくまと！！';
  };

  const getHeaderSubtitle = (cat: Category | 'all') => {
    if (cat === 'animals') return '世界中の癒し動物動画コレクション';
    if (cat === 'surprise') return '衝撃映像・ハプニング・びっくり動画まとめ';
    if (cat === 'trend') return '最新トレンド＆ニュース';
    if (cat === 'flame') return 'ネットの話題・議論・炎上まとめ';
    return '話題の動画・ニュースまとめサイト';
  };

  const handleCategoryChange = (newCat: string) => {
    setSearchParams({ cat: newCat });
  };

  const displayedPosts = (category === 'all'
    ? allPosts
    : allPosts.filter(p => p.category === category))
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-inner">
          <Link
            to="/"
            className="header-branding"
            onClick={() => {
              window.scrollTo({ top: 0, behavior: 'smooth' });
              // Force refresh if already on home or just generally
              fetchSupabasePosts(0, true);
              // Also clear category if needed manually, but Link to="/" does it mostly.
              // We can ensure state reset:
              setPage(0);
            }}
            style={{ textDecoration: 'none', color: 'inherit', display: 'flex', alignItems: 'center', gap: '15px' }}
          >
            <img src="/mascot_cat.png" alt="Mofu" className="header-mascot" style={{ height: '50px', width: 'auto' }} />
            <div className="header-text">
              <h1>{getHeaderTitle()}</h1>
              <span className="subtitle">{getHeaderSubtitle(category)}</span>
            </div>
          </Link>

          <nav className="category-nav">
            <button
              className={category === 'all' ? 'active' : ''}
              onClick={() => handleCategoryChange('all')}
            >
              すべて
            </button>
            <button
              className={category === 'animals' ? 'active' : ''}
              onClick={() => handleCategoryChange('animals')}
            >
              癒やし
            </button>
            <button
              className={category === 'surprise' ? 'active' : ''}
              onClick={() => handleCategoryChange('surprise')}
            >
              驚き
            </button>
            <button
              className={category === 'flame' ? 'active' : ''}
              onClick={() => handleCategoryChange('flame')}
            >
              炎上
            </button>
            <button
              className={category === 'trend' ? 'active' : ''}
              onClick={() => handleCategoryChange('trend')}
            >
              トレンド
            </button>
          </nav>
        </div>
      </header>

      <div className="main-layout">
        <div className="content-area">
          <Routes>
            <Route path="/" element={
              <HomePage
                posts={displayedPosts}
                onLoadMore={loadMore}
                hasMore={hasMore && category === 'all'} // Only show load more on 'all' because filtering reduces count
                loading={loading}
              />
            } />
            <Route path="/post/:id" element={
              <PostPage posts={allPosts} />
            } />
            <Route path="/privacy" element={<PrivacyPolicy />} />
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/admin/create" element={<AdminPostEditor />} />
          </Routes>
        </div>
        {!location.pathname.startsWith('/admin') && <Sidebar posts={allPosts} />}
      </div>

      <footer className="app-footer">
        <p>© 2025 Summary Site. Content for demo purposes.</p>
      </footer>
      <FloatingDonationButton />
      <ScrollToTopButton />
    </div>
  );
};

import { HelmetProvider } from 'react-helmet-async';
import { GoogleAnalytics } from './components/Analytics';

function App() {
  return (
    <HelmetProvider>
      <BrowserRouter>
        <GoogleAnalytics />
        <AppContent />
      </BrowserRouter>
    </HelmetProvider>
  );
}

export default App;
