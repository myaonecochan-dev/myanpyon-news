import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';

interface Poll {
    id: string;
    question: string;
    option_a: string;
    option_b: string;
    votes_a: number;
    votes_b: number;
}

interface PollWidgetProps {
    postId: string;
}

export const PollWidget: React.FC<PollWidgetProps> = ({ postId }) => {
    const [poll, setPoll] = useState<Poll | null>(null);
    const [voted, setVoted] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPoll = async () => {
            const { data, error } = await supabase
                .from('polls')
                .select('*')
                .eq('post_id', postId)
                .single();

            if (!error && data) {
                setPoll(data);
            }
            setLoading(false);
        };

        fetchPoll();

        // Check if already voted in this session (simple local storage)
        const hasVoted = localStorage.getItem(`voted_${postId}`);
        if (hasVoted) setVoted(true);
    }, [postId]);

    const handleVote = async (option: 'a' | 'b') => {
        if (voted || !poll) return;

        const column = option === 'a' ? 'votes_a' : 'votes_b';
        const newValue = (option === 'a' ? poll.votes_a : poll.votes_b) + 1;

        const { error } = await supabase
            .from('polls')
            .update({ [column]: newValue })
            .eq('id', poll.id);

        if (!error) {
            setPoll({ ...poll, [column]: newValue });
            setVoted(true);
            localStorage.setItem(`voted_${postId}`, 'true');
        }
    };

    if (loading || !poll) return null;

    const totalVotes = poll.votes_a + poll.votes_b;
    const percentA = totalVotes === 0 ? 0 : Math.round((poll.votes_a / totalVotes) * 100);
    const percentB = totalVotes === 0 ? 0 : 100 - percentA;

    return (
        <div className="poll-widget" style={{
            marginTop: '30px',
            background: 'linear-gradient(135deg, #fff 0%, #f0f7ff 100%)',
            padding: '24px',
            borderRadius: '16px',
            border: '2px solid #3498db',
            boxShadow: '0 6px 16px rgba(52,152,219,0.1)'
        }}>
            <h3 style={{
                margin: '0 0 20px 0',
                fontSize: '1.2rem',
                textAlign: 'center',
                color: '#2c3e50'
            }}>
                <span style={{ marginRight: '8px' }}>📊</span>
                {poll.question}
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
                {/* Option A */}
                <button
                    onClick={() => handleVote('a')}
                    disabled={voted}
                    style={{
                        position: 'relative',
                        width: '100%',
                        padding: '15px',
                        border: '2px solid #3498db',
                        borderRadius: '10px',
                        background: voted ? '#fff' : '#3498db',
                        color: voted ? '#3498db' : '#fff',
                        fontWeight: 'bold',
                        fontSize: '1rem',
                        cursor: voted ? 'default' : 'pointer',
                        overflow: 'hidden',
                        transition: 'all 0.2s'
                    }}
                >
                    {/* Progress Bar Background */}
                    {voted && (
                        <div style={{
                            position: 'absolute',
                            left: 0,
                            top: 0,
                            height: '100%',
                            width: `${percentA}%`,
                            background: 'rgba(52,152,219,0.15)',
                            zIndex: 0
                        }} />
                    )}
                    <span style={{ position: 'relative', zIndex: 1 }}>
                        {poll.option_a} {voted && `(${percentA}%)`}
                    </span>
                </button>

                {/* Option B */}
                <button
                    onClick={() => handleVote('b')}
                    disabled={voted}
                    style={{
                        position: 'relative',
                        width: '100%',
                        padding: '15px',
                        border: '2px solid #e67e22',
                        borderRadius: '10px',
                        background: voted ? '#fff' : '#e67e22',
                        color: voted ? '#e67e22' : '#fff',
                        fontWeight: 'bold',
                        fontSize: '1rem',
                        cursor: voted ? 'default' : 'pointer',
                        overflow: 'hidden',
                        transition: 'all 0.2s'
                    }}
                >
                    {/* Progress Bar Background */}
                    {voted && (
                        <div style={{
                            position: 'absolute',
                            left: 0,
                            top: 0,
                            height: '100%',
                            width: `${percentB}%`,
                            background: 'rgba(230,126,34,0.15)',
                            zIndex: 0
                        }} />
                    )}
                    <span style={{ position: 'relative', zIndex: 1 }}>
                        {poll.option_b} {voted && `(${percentB}%)`}
                    </span>
                </button>
            </div>

            {voted && (
                <p style={{
                    textAlign: 'center',
                    fontSize: '0.85rem',
                    color: '#7f8c8d',
                    marginTop: '15px',
                    fontWeight: 'bold'
                }}>
                    ご投票ありがとうございました！ (合計: {totalVotes}票)
                </p>
            )}
        </div>
    );
};
