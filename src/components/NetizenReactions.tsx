import React from 'react';

interface Reaction {
    name: string;
    text: string;
    color?: string;
}

interface NetizenReactionsProps {
    reactions: Reaction[];
}

export const NetizenReactions: React.FC<NetizenReactionsProps> = ({ reactions }) => {
    if (!reactions || reactions.length === 0) return null;

    return (
        <div className="netizen-reactions" style={{
            marginTop: '40px',
            backgroundColor: '#fff',
            padding: '20px',
            borderRadius: '12px',
            border: '2px solid #5cb85c', // 2ch signature green
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
        }}>
            <h3 style={{
                margin: '0 0 15px 0',
                fontSize: '1.2rem',
                color: '#5cb85c',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                borderBottom: '1px solid #eee',
                paddingBottom: '10px'
            }}>
                <span style={{ fontSize: '1.4rem' }}>💬</span>
                ネットの反応（架空）
            </h3>

            <div className="reactions-list">
                {reactions.map((res, index) => (
                    <div key={index} style={{
                        marginBottom: '15px',
                        paddingBottom: '10px',
                        borderBottom: '1px dashed #eee'
                    }}>
                        <div style={{ fontSize: '0.85rem', marginBottom: '4px' }}>
                            <span style={{ color: '#5cb85c', fontWeight: 'bold' }}>{index + 1}: </span>
                            <span style={{ color: res.color === 'red' ? '#e74c3c' : res.color === 'blue' ? '#3498db' : '#2ecc71', fontWeight: 'bold' }}>
                                {res.name}
                            </span>
                            <span style={{ color: '#999', marginLeft: '10px' }}>
                                {new Date().toLocaleDateString()} 12:34:56.78
                            </span>
                        </div>
                        <div style={{
                            fontSize: '1rem',
                            lineHeight: '1.5',
                            paddingLeft: '1.2rem',
                            color: '#333'
                        }}>
                            {res.text}
                        </div>
                    </div>
                ))}
            </div>

            <p style={{ fontSize: '0.75rem', color: '#999', marginTop: '10px', textAlign: 'right' }}>
                ※この反応はAIによるシミュレーションです
            </p>
        </div>
    );
};
