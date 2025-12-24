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
                        background: '#FF9F43', /* Neko Can Orange */
                        border: 'none',
                        borderRadius: '50px',
                        fontWeight: 'bold',
                        color: 'white',
                        cursor: 'pointer',
                        boxShadow: '0 4px 10px rgba(255, 159, 67, 0.4)',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '12px',
                        fontSize: '1rem',
                        transition: 'all 0.2s',
                        borderBottom: '4px solid #E67E22'
                    }}
                        onMouseOver={(e) => {
                            e.currentTarget.style.transform = 'translateY(2px)';
                            e.currentTarget.style.borderBottom = '2px solid #E67E22';
                            e.currentTarget.style.boxShadow = '0 2px 5px rgba(255, 159, 67, 0.4)';
                        }}
                        onMouseOut={(e) => {
                            e.currentTarget.style.transform = 'translateY(0)';
                            e.currentTarget.style.borderBottom = '4px solid #E67E22';
                            e.currentTarget.style.boxShadow = '0 4px 10px rgba(255, 159, 67, 0.4)';
                        }}
                    >
                        <span style={{ fontSize: '1.4rem' }}>🥫</span> 猫缶を贈る (Ko-fi)
                    </button>
                </a>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#999', marginTop: '1rem' }}>
                ご支援ありがとうございます！励みになります！
            </p>
        </div>
    );
};
