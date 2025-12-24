import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';
import './CommentSection.css';

interface Comment {
    id: string;
    content: string;
    author_name: string;
    created_at: string;
}

interface CommentSectionProps {
    postId: string;
}

export const CommentSection: React.FC<CommentSectionProps> = ({ postId }) => {
    const [comments, setComments] = useState<Comment[]>([]);
    const [newComment, setNewComment] = useState('');
    const [authorName, setAuthorName] = useState('名無しさん');
    const [loading, setLoading] = useState(true);

    const fetchComments = async () => {
        setLoading(true);
        // Ensure postId is valid UUID before querying to avoid 400 errors
        if (!postId || postId.length < 20) {
            setLoading(false);
            return;
        }

        const { data, error } = await supabase
            .from('comments')
            .select('*')
            .eq('post_id', postId)
            .order('created_at', { ascending: false });

        if (error) {
            console.error('Error fetching comments:', error);
        } else {
            setComments(data || []);
        }
        setLoading(false);
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!newComment.trim()) return;

        const { error } = await supabase
            .from('comments')
            .insert([
                { post_id: postId, content: newComment, author_name: authorName || '名無しさん' }
            ]);

        if (error) {
            alert('コメントの投稿に失敗しました: ' + error.message);
            console.error(error);
        } else {
            setNewComment('');
            fetchComments(); // Refresh list immediately
        }
    };

    useEffect(() => {
        fetchComments();
    }, [postId]);

    return (
        <div className="comment-section">
            <h3 className="comment-title">コメント ({comments.length})</h3>

            <div className="comment-list">
                {loading ? (
                    <p style={{ textAlign: 'center', color: '#666' }}>読み込み中...</p>
                ) : comments.length === 0 ? (
                    <p className="no-comments">コメントはまだありません。一番乗りしよう！</p>
                ) : (
                    comments.map((comment) => (
                        <div key={comment.id} className="comment-item">
                            <div className="comment-header">
                                <span className="comment-number">No.{comment.id.slice(0, 4)}</span>
                                <span className="comment-author">{comment.author_name}</span>
                                <span className="comment-date">{new Date(comment.created_at).toLocaleString()}</span>
                            </div>
                            <p className="comment-content">{comment.content}</p>
                        </div>
                    ))
                )}
            </div>

            <form onSubmit={handleSubmit} className="comment-form">
                <div className="form-group">
                    <label>お名前</label>
                    <input
                        type="text"
                        className="author-input"
                        placeholder="名無しさん"
                        value={authorName}
                        onChange={(e) => setAuthorName(e.target.value)}
                    />
                </div>
                <div className="form-group">
                    <label>コメント</label>
                    <textarea
                        className="comment-textarea"
                        placeholder="コメントを書く..."
                        value={newComment}
                        onChange={(e) => setNewComment(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="submit-button">書き込む</button>
            </form>
        </div>
    );
};
