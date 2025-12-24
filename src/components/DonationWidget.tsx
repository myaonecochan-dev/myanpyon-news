import React from 'react';

export const DonationWidget: React.FC = () => {
    return (
        <div className="donation-widget" style={{
            background: 'linear-gradient(135deg, #fff5f5 0%, #fff 100%)',
            border: '2px solid #ffb6b9',
            borderRadius: '16px',
            padding: '1.5rem',
            textAlign: 'center',
            margin: '2rem 0',
            boxShadow: '0 4px 15px rgba(255, 182, 185, 0.2)'
        }}>
            <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'flex-end', justifyContent: 'center', height: '110px', paddingRight: '40px' }}>
                <img src="/mascot_cat.png" alt="Myan" style={{ width: 'auto', height: '105px', objectFit: 'contain', zIndex: 2 }} />
                <img src="/mascot_bunny.png" alt="Pyon" style={{ width: 'auto', height: '110px', objectFit: 'contain', zIndex: 1, marginLeft: '-60px' }} />
            </div>
            <h3 style={{ margin: '0 0 0.5rem 0', color: '#ff6b6b' }}>運営をサポートするだにゃ！</h3>
            <p style={{ fontSize: '0.9rem', color: '#666', marginBottom: '1.5rem' }}>
                みなさまの応援が、みゃん＆ぴょんの活動（と缶詰代）になります。<br />
                気に入ったらサポートしてね！
            </p>

            <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
                <a href="https://ko-fi.com/nyanpyon" target="_blank" rel="noopener noreferrer" style={{ textDecoration: 'none' }}>
                    <button style={{
                        padding: '12px 25px',
                        background: '#FF5E5B', /* Ko-fi Color */
                        border: 'none',
                        borderRadius: '25px',
                        fontWeight: 'bold',
                        color: 'white',
                        cursor: 'pointer',
                        boxShadow: '0 2px 5px rgba(0,0,0,0.1)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        fontSize: '1rem',
                        transition: 'transform 0.2s'
                    }}
                        onMouseOver={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                        onMouseOut={(e) => e.currentTarget.style.transform = 'scale(1)'}
                    >
                        <span style={{ fontSize: '1.2rem' }}>☕</span> Support Me on Ko-fi
                    </button>
                </a>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#999', marginTop: '1rem' }}>
                ご支援ありがとうございます！励みになります！
            </p>
        </div>
    );
};
