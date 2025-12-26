import { Link } from 'react-router-dom';
import { type Post } from '../data/posts';
import { AdSenseDisplay } from './AdSenseDisplay';
import './Sidebar.css';

interface SidebarProps {
    posts?: Post[];
}

export const Sidebar: React.FC<SidebarProps> = ({ posts = [] }) => {
    // Simple logic: Use the first 3 posts as "Daily Ranking" and next 3 as "Monthly"
    // In a real app, this would be based on view counts.
    const dailyRanking = posts.slice(0, 3);
    const monthlyRanking = posts.slice(3, 6);

    return (
        <aside className="app-sidebar">
            {/* Profile Widget (Mascot) */}
            <div className="sidebar-widget profile-widget" style={{ textAlign: 'center' }}>
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-end', marginBottom: '10px', transform: 'translateX(-15px)' }}>
                    <img src="/mascot_cat.png" alt="Mascot Cat" style={{ width: 'auto', height: '85px', objectFit: 'contain', zIndex: 2 }} />
                    <img src="/mascot_bunny.png" alt="Mascot Bunny" style={{ width: 'auto', height: '90px', objectFit: 'contain', marginLeft: '-60px', zIndex: 1 }} />
                </div>
                <h3 style={{ margin: '0 0 5px 0', fontSize: '1.1rem' }}>管理人: みゃん＆ぴょん</h3>
                <p style={{ fontSize: '0.85rem', color: '#666', lineHeight: '1.4' }}>
                    世界中の面白い動画やニュースをお届けします！<br />
                    毎日更新中！フォローしてね♪
                </p>
                <div style={{ marginTop: '10px' }}>
                    <a href="https://x.com/NyanPyonMatome" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                        <button style={{ marginRight: '5px', padding: '5px 10px', background: '#000', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>X (Twitter)</button>
                    </a>
                    <button style={{ padding: '5px 10px', background: '#ff0000', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>YouTube</button>
                </div>
            </div>

            {/* Rakuten Affiliate Banner */}
            <div className="sidebar-widget" style={{ textAlign: 'center', padding: '15px' }}>
                <h3 className="widget-title" style={{ marginBottom: '15px' }}>おすすめショップ</h3>
                <a href="//af.moshimo.com/af/c/click?a_id=5317132&p_id=54&pc_id=54&pl_id=1229" rel="nofollow" referrerpolicy="no-referrer-when-downgrade" target="_blank">
                    <img src="//image.moshimo.com/af-img/0032/000000001229.gif" width="120" height="120" style={{ border: 'none', borderRadius: '8px', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }} alt="楽天市場" />
                </a>
                <img src="//i.moshimo.com/af/i/impression?a_id=5317132&p_id=54&pc_id=54&pl_id=1229" width="1" height="1" style={{ border: 'none' }} loading="lazy" alt="" />
                <p style={{ fontSize: '0.7rem', color: '#999', marginTop: '10px' }}>楽天市場でのお買い物はこちらから</p>
            </div>

            {/* Daily Ranking Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">デイリーランキング</h3>
                {posts.length > 0 ? (
                    <ul className="ranking-list">
                        {dailyRanking.map((post, index) => {
                            // Generate a consistent pseudo-random number based on the post ID
                            const idNum = post.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
                            const commentCount = (idNum * 13) % 800 + 120; // Range: 120 - 920
                            return (
                                <li key={post.id} className="ranking-item">
                                    <Link to={`/post/${post.id}`} className="ranking-link">
                                        <span className={`rank-number rank-${index + 1}`}>{index + 1}</span>
                                        {post.imageUrl ? (
                                            <img src={post.imageUrl} alt={post.title} className="rank-thumbnail" />
                                        ) : (
                                            <div className="rank-thumbnail placeholder" />
                                        )}
                                        <div className="rank-content">
                                            <p className="rank-title">{post.title}</p>
                                            <span className="rank-meta">{commentCount} comments</span>
                                        </div>
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                ) : (
                    <p style={{ padding: '10px', fontSize: '0.9rem', color: '#666' }}>集計中...</p>
                )}
            </div>

            {/* Monthly Ranking Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">月間ランキング</h3>
                {posts.length > 0 ? (
                    <ul className="ranking-list">
                        {monthlyRanking.map((post, index) => {
                            const idNum = post.id.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
                            const commentCount = (idNum * 17) % 3000 + 500; // Range: 500 - 3500
                            return (
                                <li key={post.id} className="ranking-item">
                                    <Link to={`/post/${post.id}`} className="ranking-link">
                                        <span className={`rank-number rank-${index + 1}`}>{index + 1}</span>
                                        {post.imageUrl ? (
                                            <img src={post.imageUrl} alt={post.title} className="rank-thumbnail" />
                                        ) : (
                                            <div className="rank-thumbnail placeholder" />
                                        )}
                                        <div className="rank-content">
                                            <p className="rank-title">{post.title}</p>
                                            <span className="rank-meta">{commentCount} comments</span>
                                        </div>
                                    </Link>
                                </li>
                            );
                        })}
                    </ul>
                ) : null}
            </div>

            {/* Categories Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">Categories</h3>
                <ul className="category-list">
                    {[
                        { id: 'trend', label: 'トレンド', icon: '📈' },
                        { id: 'surprise', label: '驚き', icon: '😲' },
                        { id: 'animals', label: '癒やし', icon: '🐱' },
                        { id: 'flame', label: '炎上', icon: '🔥' }
                    ].map(cat => {
                        const count = posts.filter(p => p.category === cat.id).length;
                        return (
                            <li key={cat.id}>
                                <Link to={`/?cat=${cat.id}`} className="category-link">
                                    <span className="cat-icon">{cat.icon}</span>
                                    <span className="cat-label">{cat.label}</span>
                                    <span className="cat-count">({count})</span>
                                </Link>
                            </li>
                        );
                    })}
                    <li>
                        <Link to="/?cat=all" className="category-link">
                            <span className="cat-icon">📂</span>
                            <span className="cat-label">すべて</span>
                            <span className="cat-count">({posts.length})</span>
                        </Link>
                    </li>
                    <li style={{ marginTop: '10px', borderTop: '1px solid #eee', paddingTop: '10px' }}>
                        <Link to="/contact" className="category-link" style={{ fontSize: '0.85rem', color: '#999' }}>
                            <span className="cat-icon">📧</span>
                            <span className="cat-label">お問い合わせ</span>
                        </Link>
                    </li>
                    <li>
                        <Link to="/privacy" className="category-link" style={{ fontSize: '0.85rem', color: '#999' }}>
                            <span className="cat-icon">🔒</span>
                            <span className="cat-label">プライバシーポリシー</span>
                        </Link>
                    </li>
                </ul>
            </div>



            {/* Daily Ranking Widget */}

            {/* Ad Placeholder */}
            <div className="sidebar-widget ad-widget">
                <AdSenseDisplay slot="1234567890" style={{ height: '300px' }} />
            </div>
        </aside>
    );
};
