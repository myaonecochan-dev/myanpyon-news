import { useState, useEffect } from 'react';
import { supabaseAdmin } from '../lib/supabaseAdminClient';
import type { Post } from '../data/posts';
import { Link } from 'react-router-dom';

export const AdminPage = () => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [password, setPassword] = useState('');
    const [posts, setPosts] = useState<Post[]>([]);
    const [loading, setLoading] = useState(false);


    // specific simple password for now
    const SECRET_PIN = '1224'; // Christmas Eve PIN

    useEffect(() => {
        const storedAuth = sessionStorage.getItem('admin_auth');
        if (storedAuth === 'true') {
            setIsAuthenticated(true);
            fetchPosts();
        }
    }, []);

    const handleLogin = (e: React.FormEvent) => {
        e.preventDefault();
        if (password === SECRET_PIN) {
            setIsAuthenticated(true);
            sessionStorage.setItem('admin_auth', 'true');
            fetchPosts();
        } else {
            alert('Incorrect PIN');
        }
    };

    const handleLogout = () => {
        setIsAuthenticated(false);
        sessionStorage.removeItem('admin_auth');
    };

    const fetchPosts = async () => {
        setLoading(true);
        const { data, error } = await supabaseAdmin
            .from('posts')
            .select('*')
            .order('created_at', { ascending: false });

        if (error) {
            console.error('Error fetching posts:', error);
        } else if (data) {
            // Basic mapping to match Post interface roughly for display
            const mapped: Post[] = data.map((item: any) => ({
                id: item.id,
                title: item.title,
                category: item.category,
                type: item.type,
                platform: item.platform,
                created_at: item.created_at,
                description: item.description,
                // other fields not strictly needed for list view
            }));
            setPosts(mapped);
        }
        setLoading(false);
    };

    const handleDelete = async (id: string) => {
        if (!window.confirm('Are you sure you want to delete this post?')) return;

        const { error } = await supabaseAdmin
            .from('posts')
            .delete()
            .eq('id', id);

        if (error) {
            alert('Error deleting post: ' + error.message);
        } else {
            setPosts(posts.filter(p => p.id !== id));
        }
    };

    if (!isAuthenticated) {
        return (
            <div style={{ padding: '4rem', maxWidth: '400px', margin: '0 auto', textAlign: 'center' }}>
                <h2>Admin Login</h2>
                <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter PIN"
                        style={{ padding: '10px', fontSize: '16px' }}
                    />
                    <button type="submit" style={{ padding: '10px', background: 'var(--primary)', color: 'white', border: 'none', borderRadius: '4px' }}>
                        Login
                    </button>
                </form>
            </div>
        );
    }

    return (
        <div className="admin-dashboard" style={{ padding: '2rem', maxWidth: '1000px', margin: '0 auto' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Admin Dashboard</h1>
                <div style={{ display: 'flex', gap: '1rem' }}>
                    <Link to="/admin/create" className="btn-primary" style={{ padding: '10px 20px', background: 'var(--primary)', color: 'white', textDecoration: 'none', borderRadius: '4px' }}>
                        + New Post
                    </Link>
                    <button onClick={handleLogout} style={{ padding: '10px 20px', background: '#ccc', border: 'none', borderRadius: '4px' }}>
                        Logout
                    </button>
                </div>
            </div>

            {loading ? (
                <p>Loading posts...</p>
            ) : (
                <div className="post-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                    {posts.map(post => (
                        <div key={post.id} style={{
                            padding: '1rem',
                            background: 'white',
                            borderRadius: '8px',
                            border: '1px solid #eee',
                            display: 'flex',
                            justifyContent: 'space-between',
                            alignItems: 'center'
                        }}>
                            <div>
                                <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>{post.title}</h3>
                                <div style={{ fontSize: '0.85rem', color: '#666', display: 'flex', gap: '10px' }}>
                                    <span style={{
                                        padding: '2px 8px',
                                        background: '#f0f0f0',
                                        borderRadius: '4px',
                                        textTransform: 'uppercase',
                                        fontSize: '0.7rem'
                                    }}>{post.category}</span>
                                    <span>{post.type} / {post.platform}</span>
                                    <span>{new Date(post.created_at).toLocaleDateString()}</span>
                                </div>
                            </div>
                            <button
                                onClick={() => handleDelete(post.id)}
                                style={{
                                    padding: '5px 10px',
                                    background: '#ff4444',
                                    color: 'white',
                                    border: 'none',
                                    borderRadius: '4px',
                                    cursor: 'pointer'
                                }}
                            >
                                Delete
                            </button>
                        </div>
                    ))}
                    {posts.length === 0 && <p>No posts found.</p>}
                </div>
            )}
        </div>
    );
};
