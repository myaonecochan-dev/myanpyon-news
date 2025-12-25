import React from 'react';
import { Link } from 'react-router-dom';
import type { Post } from '../data/posts';
import './VideoCard.css'; // Keep CSS file name for now or rename. Let's keep it to verify logic first.

interface PostCardProps {
    post: Post;
    className?: string;
}

export const PostCard: React.FC<PostCardProps> = ({ post, className = '' }) => {
    // Simple thumbnail logic
    let thumbnailSrc = post.imageUrl || ''; // Use provided image first

    if (!thumbnailSrc) {
        if (post.platform === 'youtube' && post.youtubeId) {
            thumbnailSrc = `https://img.youtube.com/vi/${post.youtubeId}/mqdefault.jpg`;
        } else if (post.platform === 'twitter') {
            thumbnailSrc = 'https://abs.twimg.com/icons/apple-touch-icon-192x192.png';
        } else if (post.platform === 'tiktok') {
            thumbnailSrc = 'https://sf16-scmcdn-sg.ibytedtos.com/goofy/tiktok/web/node/_next/static/images/logo-dark-e95da587b61837f72eb2e389e81d77cb.png';
        } else if (post.type === 'thread') {
            thumbnailSrc = 'https://via.placeholder.com/640x360/333/fff?text=Thread';
        } else if (post.type === 'article') {
            thumbnailSrc = 'https://via.placeholder.com/640x360/eee/333?text=Article';
        }
    }

    return (
        <Link to={`/post/${post.slug || post.id}`} className={`video-card-link ${className}`}>
            <div className="video-card">
                <div className="video-thumbnail-wrapper">
                    <img src={thumbnailSrc} alt={post.title} className="video-thumbnail" loading="lazy" />
                </div>
                <div className="video-info">
                    <h3 className="video-title">{post.title}</h3>
                    <p className="video-description">{post.description}</p>
                </div>
            </div>
        </Link>
    );
};
