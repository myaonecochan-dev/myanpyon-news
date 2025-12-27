import React, { useEffect, useState } from 'react';

const RakutenMotionWidget: React.FC = () => {
    const [iframeHeight, setIframeHeight] = useState('200px');

    useEffect(() => {
        const handleResize = () => {
            // Match the logic in rakuten_widget.html
            // Mobile (468x60) needs less height (around 80px), PC (728x200) needs 200px
            if (window.innerWidth < 600) {
                setIframeHeight('75px'); // Tight fit for 60px banner
            } else {
                setIframeHeight('200px');
            }
        };

        // Initial check
        handleResize();

        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div className="rakuten-motion-widget-wrapper" style={{ margin: '2rem auto', maxWidth: '100%', textAlign: 'center', minHeight: iframeHeight }}>
            <h4 style={{
                margin: '0 0 10px 0',
                fontSize: '0.9rem',
                color: '#666',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px'
            }}>
                <span>👀</span>
                <span>あなたにおすすめのアイテム</span>
            </h4>
            <iframe
                title="Rakuten Motion Widget"
                src="/rakuten_widget.html"
                style={{
                    width: '100%',
                    maxWidth: '728px',
                    height: iframeHeight,
                    border: 'none',
                    overflow: 'hidden',
                    transition: 'height 0.3s ease'
                }}
                scrolling="no"
                loading="lazy"
            />
        </div>
    );
};

export default RakutenMotionWidget;
