import { useState, useEffect } from 'react';
import { MetaHead } from '../components/MetaHead';
import { PostCard } from '../components/PostCard';
import { SkeletonCard } from '../components/SkeletonCard';
import { type Post } from '../data/posts';

interface HomePageProps {
    posts: Post[];
    onLoadMore: () => void;
    hasMore: boolean;
    loading: boolean;
}

// HomePage.tsx (Simplified)
export const HomePage = ({ posts, onLoadMore, hasMore, loading }: HomePageProps) => {
    // No local filter state needed anymore

    const isInitialLoading = loading && posts.length === 0;

    useEffect(() => {
        if (typeof window !== 'undefined') window.scrollTo(0, 0);
    }, []);

    return (
        <div className="home-page">
            <MetaHead />
            <div className="summary-box">
                <h2>⚡ 今日の３行まとめ</h2>
                <ul>
                    <li>猫がピアノを弾く動画が100万再生突破！🎹</li>
                    <li>新作ゲームのバグが「逆に面白い」と話題に🎮</li>
                    <li>AIが書いた小説が文学賞の一次審査を通過📚</li>
                </ul>
            </div>

            <div className="intro-text-container">
                <p className="intro-text">
                    ここは、ネットで話題の動画やニュースを<br className="mobile-break" />サクッとまとめたサイトです。<br />
                    忙しいあなたも、<span className="mascot-name">みゃん</span>と<span className="mascot-name">ぴょん</span>と一緒に<br className="mobile-break" />世の中のトレンドをチェックしよう！
                </p>
            </div>

            {/* Filter Bar Removed - Handled by Header & App */}

            <div className="video-grid">
                {isInitialLoading ? (
                    Array.from({ length: 8 }).map((_, i) => (
                        <div key={i} className="video-card-skeleton-wrapper" style={{ animationDelay: `${i * 0.05}s` }}>
                            <SkeletonCard />
                        </div>
                    ))
                ) : (
                    posts.map((post, index) => (
                        <PostCard
                            key={post.id}
                            post={post}
                            className={index < 4 ? 'featured-post' : ''}
                        />
                    ))
                )}
            </div>

            {hasMore && (
                <div style={{ textAlign: 'center', marginTop: '2rem', marginBottom: '4rem' }}>
                    <button
                        onClick={onLoadMore}
                        disabled={loading}
                        style={{
                            padding: '12px 30px',
                            fontSize: '1.1rem',
                            background: 'white',
                            border: '2px solid var(--primary)',
                            color: 'var(--primary)',
                            borderRadius: '30px',
                            cursor: loading ? 'wait' : 'pointer',
                            fontWeight: 'bold',
                            transition: 'all 0.2s',
                            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
                        }}
                    >
                        {loading ? 'Reading...' : 'もっと読む ⤵'}
                    </button>
                </div>
            )}
        </div>
    );
};
