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
                bottom: '100px', // Stacks above ScrollToTop (30px + 56px + gap)
                right: '30px',
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                backgroundColor: '#FF5E5B', /* Ko-fi Brand Color */
                color: 'white',
                border: 'none',
                boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
                cursor: 'pointer',
                zIndex: 1000,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '28px',
                transition: 'transform 0.2s, box-shadow 0.2s',
                textDecoration: 'none'
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'scale(1.1)';
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.4)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'scale(1)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.3)';
            }}
        >
            <span role="img" aria-label="coffee">☕</span>
        </a>
    );
};
