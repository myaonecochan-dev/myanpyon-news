import React from 'react';

export const FloatingDonationButton: React.FC = () => {
    return (
        <a
            href="https://ko-fi.com/nyanpyon"
            target="_blank"
            rel="noopener noreferrer"
            aria-label="Support on Ko-fi"
            style={{
                position: 'fixed',
                bottom: '100px', // Stacks above ScrollToTop
                right: '30px',
                height: '50px', // Slightly smaller height for pill shape
                padding: '0 20px',
                borderRadius: '25px', // Pill shape
                backgroundColor: '#FF5E5B',
                color: 'white',
                border: 'none',
                boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                cursor: 'pointer',
                zIndex: 1000,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '8px',
                fontSize: '16px',
                fontWeight: 'bold',
                transition: 'all 0.2s ease',
                textDecoration: 'none',
                fontFamily: '"Noto Sans JP", sans-serif'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.4)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
            }}
        >
            <span role="img" aria-label="cat-can" style={{ fontSize: '20px' }}>🥫</span>
            <span>猫缶を贈る</span>
        </a>
    );
};
