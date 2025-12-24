import { useState, useEffect } from 'react';
import { supabaseAdmin } from '../lib/supabaseAdminClient';
import { useNavigate } from 'react-router-dom';

export const AdminPostEditor = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    // Auth check
    useEffect(() => {
        if (sessionStorage.getItem('admin_auth') !== 'true') {
            navigate('/admin');
        }
    }, [navigate]);

    const [formData, setFormData] = useState({
        title: '',
        category: 'trend',
        type: 'article',
        platform: 'article',
        description: '',
        content: '',
        video_id: '', // Used for youtubeId or embedId
        image_url: '',
    });

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        // Prepare data for Supabase
        const dbData = {
            ...formData,
            // If article, content is required. If video, video_id is required usually.
        };

        const { error } = await supabaseAdmin
            .from('posts')
            .insert([dbData]);

        setLoading(false);

        if (error) {
            alert('Error creating post: ' + error.message);
        } else {
            alert('Post created successfully!');
            navigate('/admin');
        }
    };

    return (
        <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '2rem' }}>
                <h1>Create New Post</h1>
                <button onClick={() => navigate('/admin')} style={{ padding: '5px 10px', border: '1px solid #ccc', background: 'white', borderRadius: '4px' }}>Cancel</button>
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

                {/* Title */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <label style={{ fontWeight: 'bold' }}>Title</label>
                    <input
                        required
                        name="title"
                        value={formData.title}
                        onChange={handleChange}
                        style={{ padding: '10px', fontSize: '1.1rem' }}
                        placeholder="記事のタイトル"
                    />
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    {/* Category */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontWeight: 'bold' }}>Category</label>
                        <select name="category" value={formData.category} onChange={handleChange} style={{ padding: '10px' }}>
                            <option value="trend">Trend</option>
                            <option value="surprise">Surprise</option>
                            <option value="animals">Animals</option>
                            <option value="flame">Flame</option>
                        </select>
                    </div>

                    {/* Type */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontWeight: 'bold' }}>Type</label>
                        <select name="type" value={formData.type} onChange={handleChange} style={{ padding: '10px' }}>
                            <option value="article">Article</option>
                            <option value="video">Video</option>
                            <option value="thread">Thread</option>
                        </select>
                    </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                    {/* Platform */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontWeight: 'bold' }}>Platform</label>
                        <select name="platform" value={formData.platform} onChange={handleChange} style={{ padding: '10px' }}>
                            <option value="article">Article (None)</option>
                            <option value="youtube">YouTube</option>
                            <option value="twitter">Twitter</option>
                            <option value="tiktok">TikTok</option>
                            <option value="2ch">2ch</option>
                        </select>
                    </div>

                    {/* Video ID / Embed ID */}
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <label style={{ fontWeight: 'bold' }}>Video ID / URL Key</label>
                        <input
                            name="video_id"
                            value={formData.video_id}
                            onChange={handleChange}
                            placeholder="e.g. dQw4w9WgXcQ"
                            style={{ padding: '10px' }}
                        />
                        <small style={{ color: '#666' }}>YouTube ID, Tweet ID, or TikTok ID</small>
                    </div>
                </div>

                {/* Description */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <label style={{ fontWeight: 'bold' }}>Description (Summary)</label>
                    <textarea
                        name="description"
                        value={formData.description}
                        onChange={handleChange}
                        rows={3}
                        style={{ padding: '10px' }}
                        placeholder="一覧に表示される短い説明文"
                    />
                </div>

                {/* Image URL */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <label style={{ fontWeight: 'bold' }}>Image URL (Thumbnail)</label>
                    <input
                        name="image_url"
                        value={formData.image_url}
                        onChange={handleChange}
                        placeholder="https://..."
                        style={{ padding: '10px' }}
                    />
                </div>

                {/* Main Content */}
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    <label style={{ fontWeight: 'bold' }}>Content (HTML)</label>
                    <textarea
                        name="content"
                        value={formData.content}
                        onChange={handleChange}
                        rows={15}
                        style={{ padding: '10px', fontFamily: 'monospace' }}
                        placeholder="<p>記事の本文...</p> or <div class='thread-comment'>...</div>"
                    />
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    style={{
                        padding: '15px',
                        background: 'var(--primary)',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        fontSize: '1.2rem',
                        cursor: loading ? 'not-allowed' : 'pointer'
                    }}
                >
                    {loading ? 'Creating...' : 'Create Post'}
                </button>
            </form>
        </div>
    );
};
