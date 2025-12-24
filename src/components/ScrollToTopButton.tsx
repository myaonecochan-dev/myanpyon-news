import { useState, useEffect } from 'react';

export const ScrollToTopButton = () => {
    const [isVisible, setIsVisible] = useState(false);

    // Toggle visibility based on scroll position
    useEffect(() => {
        const toggleVisibility = () => {
            if (window.scrollY > 300) {
                setIsVisible(true);
            } else {
                setIsVisible(false);
            }
        };

        window.addEventListener('scroll', toggleVisibility);
        return () => window.removeEventListener('scroll', toggleVisibility);
    }, []);

    const scrollToTop = () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth',
        });
    };

    if (!isVisible) return null;

    return (
        <button
            onClick={scrollToTop}
            aria-label="Scroll to top"
            style={{
                position: 'fixed',
                bottom: '30px',
                right: '30px',
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                backgroundColor: 'var(--primary)',
                color: '#fff',
                border: 'none',
                boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
                cursor: 'pointer',
                zIndex: 1000,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '24px',
                transition: 'all 0.3s ease',
                opacity: isVisible ? 1 : 0,
                transform: isVisible ? 'translateY(0)' : 'translateY(20px)',
            }}
            onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-4px)';
                e.currentTarget.style.boxShadow = '0 6px 16px rgba(0,0,0,0.3)';
            }}
            onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.2)';
            }}
        >
            ↑
        </button>
    );
};
