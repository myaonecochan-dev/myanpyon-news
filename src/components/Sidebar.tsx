import React from 'react';

import { AdSenseDisplay } from './AdSenseDisplay';
import './Sidebar.css';

export const Sidebar: React.FC = () => {
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

            {/* Daily Ranking Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">デイリーランキング</h3>
                <ul className="ranking-list">
                    <li className="ranking-item">
                        <span className="rank-number rank-1">1</span>
                        <img src="/trend.png" alt="Rank 1" className="rank-thumbnail" style={{ objectPosition: '0 0' }} />
                        <div className="rank-content">
                            <p className="rank-title">【時代】AIアイドル「ネオンちゃん」がレコ大新人賞を受賞！</p>
                            <span className="rank-meta">1025 comments</span>
                        </div>
                    </li>
                    <li className="ranking-item">
                        <span className="rank-number rank-2">2</span>
                        <img src="/trend.png" alt="Rank 2" className="rank-thumbnail" />
                        <div className="rank-content">
                            <p className="rank-title">【炎上】人気YouTuber、行き過ぎたドッキリで警察沙汰に</p>
                            <span className="rank-meta">856 comments</span>
                        </div>
                    </li>
                    <li className="ranking-item">
                        <span className="rank-number rank-3">3</span>
                        <img src="https://img.youtube.com/vi/4W2qYq6f3Y8/mqdefault.jpg" alt="Rank 3" className="rank-thumbnail" />
                        <div className="rank-content">
                            <p className="rank-title">【癒し】初めて雪を見た子犬の反応が可愛すぎると話題に</p>
                            <span className="rank-meta">612 comments</span>
                        </div>
                    </li>
                </ul>
            </div>

            {/* Monthly Ranking Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">月間ランキング</h3>
                <ul className="ranking-list">
                    <li className="ranking-item">
                        <span className="rank-number rank-1">1</span>
                        <img src="/trend.png" alt="Rank 1" className="rank-thumbnail" />
                        <div className="rank-content">
                            <p className="rank-title">【伝説】新入社員さん、入社式から3時間で退職代行を使ってバックレるｗｗｗｗｗ</p>
                            <span className="rank-meta">5012 comments</span>
                        </div>
                    </li>
                    <li className="ranking-item">
                        <span className="rank-number rank-2">2</span>
                        <img src="/trend.png" alt="Rank 2" className="rank-thumbnail" />
                        <div className="rank-content">
                            <p className="rank-title">【速報】空中に映像が出るスマホ「X-Phone 16」発表！SFが現実に</p>
                            <span className="rank-meta">3400 comments</span>
                        </div>
                    </li>
                    <li className="ranking-item">
                        <span className="rank-number rank-3">3</span>
                        <img src="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg" alt="Rank 3" className="rank-thumbnail" />
                        <div className="rank-content">
                            <p className="rank-title">【感動】ロンドン駅で突然始まったフラッシュモブ</p>
                            <span className="rank-meta">2890 comments</span>
                        </div>
                    </li>
                </ul>
            </div>

            {/* Categories Widget */}
            <div className="sidebar-widget">
                <h3 className="widget-title">Categories</h3>
                <ul className="category-list">
                    <li><a href="#">Surprise Videos (42)</a></li>
                    <li><a href="#">Animal Healing (156)</a></li>
                    <li><a href="#">Funny Fails (89)</a></li>
                    <li><a href="#">Amazing Talents (34)</a></li>
                </ul>
            </div>

            {/* Ad Placeholder */}
            <div className="sidebar-widget ad-widget">
                <AdSenseDisplay slot="1234567890" style={{ height: '300px' }} />
            </div>
        </aside>
    );
};
