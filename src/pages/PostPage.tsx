import { useParams, Link } from 'react-router-dom';
import { useEffect } from 'react';
import { type Post } from '../data/posts';
import { MetaHead } from '../components/MetaHead';
import { AdSenseDisplay } from '../components/AdSenseDisplay';
import { DonationWidget } from '../components/DonationWidget';
import { AffiliateBlock } from '../components/AffiliateBlock';
import { CommentSection } from '../components/CommentSection';
import { MascotChat } from '../components/MascotChat';
import { PollWidget } from '../components/PollWidget';
import { NetizenReactions } from '../components/NetizenReactions';
import './PostPage.css';

interface PostPageProps {
    posts: Post[];
}

export const PostPage = ({ posts }: PostPageProps) => {
    const { id } = useParams<{ id: string }>();

    // Find post by ID or Slug
    const post = posts.find(p => p.id === id || p.slug === id);

    useEffect(() => {
        window.scrollTo(0, 0);
    }, [id]);

    if (!post) {
        return (
            <div className="not-found" style={{ textAlign: 'center', padding: '4rem' }}>
                <h2>記事が見つかりません (Article Not Found)</h2>
                <Link to="/" className="back-link">Return Home</Link>
            </div>
        );
    }

    const renderContent = () => {
        if (post.type === 'video' && post.platform === 'youtube') {
            return (
                <div className="video-container">
                    <iframe
                        src={`https://www.youtube.com/embed/${post.youtubeId}?autoplay=0`} // Autoplay 0 for better UX on refresh
                        title={post.title}
                        frameBorder="0"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    />
                </div>
            );
        }

        if (post.type === 'video' && post.platform === 'tiktok') {
            return (
                <div className="video-wrapper tiktok-embed">
                    {/* Placeholder for TikTok Embed - In real app, use react-tiktok or iframe */}
                    <div style={{ textAlign: 'center', margin: '2rem 0' }}>
                        <p>TikTok Video Loading...</p>
                        <blockquote
                            className="tiktok-embed"
                            cite={`https://www.tiktok.com/@user/video/${post.embedId}`}
                            data-video-id={post.embedId}
                            style={{ maxWidth: '605px', minWidth: '325px' }}
                        >
                            <section>
                                <a target="_blank" href={`https://www.tiktok.com/@user/video/${post.embedId}`}>@{post.embedId}</a>
                            </section>
                        </blockquote>
                        <script async src="https://www.tiktok.com/embed.js"></script>
                    </div>
                </div>
            );
        }

        if (post.type === 'video' && post.platform === 'twitter') {
            return (
                <div className="video-wrapper twitter-embed">
                    {/* Placeholder for Twitter Embed */}
                    <div style={{ display: 'flex', justifyContent: 'center', margin: '2rem 0' }}>
                        <blockquote className="twitter-tweet">
                            <a href={`https://twitter.com/x/status/${post.embedId}`}></a>
                        </blockquote>
                        <script async src="https://platform.twitter.com/widgets.js"></script>
                    </div>
                </div>
            );
        }

        if (post.type === 'image') {
            return (
                <div className="image-container">
                    <img src={post.imageUrl} alt={post.title} />
                </div>
            );
        }

        if (post.type === 'article') {
            return (
                <div className="article-content">
                    {post.imageUrl && (
                        <div className="image-container">
                            <img src={post.imageUrl} alt={post.title} />
                        </div>
                    )}
                    <div dangerouslySetInnerHTML={{ __html: post.content || '' }} />
                </div>
            );
        }

        // Just display text content for fallback or thread
        return (
            <div className="thread-content" dangerouslySetInnerHTML={{ __html: post.content || '' }} />
        );
    };

    // Safe content truncate for description
    const description = post.description
        ? post.description
        : post.content
            ? post.content.substring(0, 100).replace(/<[^>]*>/g, '') + '...'
            : `【${post.category}】${post.title}の話題まとめ動画！`;

    // JSON-LD Structured Data
    const structuredData = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": post.title,
        "image": post.imageUrl ? [post.imageUrl] : [],
        "datePublished": post.created_at,
        "dateModified": post.created_at, // TODO: Add updated_at if available
        "author": [{
            "@type": "Person",
            "name": "Myan & Pyon",
            "url": "https://myanpyon.com"
        }],
        "description": description,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": `https://myanpyon.com/post/${post.slug || post.id}`
        }
    };

    return (
        <div className="post-page">
            <MetaHead
                title={post.title}
                description={description}
                image={post.imageUrl}
                type="article"
                structuredData={structuredData}
            />
            <div className="nav-area">
                <Link to="/" className="back-link">
                    ← Top Page
                </Link>
            </div>

            <article className="post-detail">
                <header className="post-header">
                    <span className={`category-badge-lg ${post.category}`}>
                        {post.category.toUpperCase()}
                    </span>
                    <h1>{post.title}</h1>
                    <div className="post-meta">
                        <span className="post-date">
                            {new Date(post.created_at).toLocaleDateString()}
                        </span>
                        {' • '}
                        <span className="post-author">Myan & Pyon</span>
                    </div>
                </header>

                <div className="post-body">
                    {renderContent()}

                    {/* Interactive Poll */}
                    <PollWidget postId={post.id} />

                    {/* Netizen Reactions */}
                    {post.reactions && <NetizenReactions reactions={post.reactions} />}
                </div>

                {/* Affiliate Block */}
                <AffiliateBlock postKeywords={post.product_keywords} />

                {/* Mascot Chat Area */}
                <MascotChat myanComment={post.comment_myan} pyonComment={post.comment_pyon} />

                {/* Comment Section */}
                <CommentSection postId={post.id} />

                {/* Donation Widget */}
                <DonationWidget />

                {/* Article Bottom Ad */}
                <AdSenseDisplay slot="0987654321" style={{ height: '250px', marginTop: '30px' }} />

                <div className="post-footer">
                    <h3>この記事をシェアする</h3>
                    <div className="share-buttons">
                        <button
                            className="share-btn twitter"
                            onClick={() => {
                                const url = `${window.location.origin}/post/${post.slug || post.id}`;
                                const text = `${post.title} | みゃんぴょんそくまと！！`;
                                window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
                            }}
                        >
                            X (Twitter)
                        </button>
                        <button
                            className="share-btn line"
                            onClick={() => {
                                const url = `${window.location.origin}/post/${post.slug || post.id}`;
                                window.open(`https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}`, '_blank');
                            }}
                        >
                            LINE
                        </button>
                        <button
                            className="share-btn copy"
                            onClick={() => {
                                const url = `${window.location.origin}/post/${post.slug || post.id}`;
                                navigator.clipboard.writeText(url);
                                alert('リンクをコピーしました！');
                            }}
                            style={{ background: '#666', color: 'white' }}
                        >
                            リンクをコピー
                        </button>
                    </div>
                </div>
            </article>
        </div>
    );
};
