import React, { useEffect, useState } from 'react';

const RakutenMotionWidget: React.FC = () => {
    const [iframeStyle, setIframeStyle] = useState<React.CSSProperties>({
        width: '100%',
        maxWidth: '728px',
        height: '200px',
        border: 'none',
        overflow: 'hidden',
        transition: 'all 0.3s ease'
    });

    // Default to Desktop file
    const [widgetUrl, setWidgetUrl] = useState('/rakuten_widget_pc.html?v=3');

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth < 600) {
                // Mobile: Load the dedicated Mobile file (300x160)
                setWidgetUrl('/rakuten_widget_mobile.html?v=3');
                setIframeStyle({
                    width: '300px',
                    height: '160px',
                    border: 'none',
                    overflow: 'hidden',
                    transform: 'scale(1.2)',
                    transformOrigin: 'top center',
                    marginBottom: '-10px',
                    transition: 'all 0.3s ease'
                });
            } else {
                // PC: Load the dedicated PC file (728x200)
                setWidgetUrl('/rakuten_widget_pc.html?v=3');
                setIframeStyle({
                    width: '100%',
                    maxWidth: '728px',
                    height: '200px',
                    border: 'none',
                    overflow: 'hidden',
                    transform: 'none',
                    marginBottom: '0',
                    transition: 'all 0.3s ease'
                });
            }
        };

        handleResize();
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    return (
        <div className="rakuten-motion-widget-wrapper" style={{
            margin: '2rem auto',
            maxWidth: '100%',
            textAlign: 'center',
            // Dynamic height container
            height: '200px',
            display: 'flex',
            justifyContent: 'center',
            overflow: 'hidden'
        }}>
            <div style={{ position: 'relative' }}>
                <div style={{
                    marginBottom: '10px',
                    fontSize: '0.85rem',
                    color: '#666',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '6px'
                }}>
                    <span>👀</span>
                    <span>あなたにおすすめのアイテム</span>
                </div>
                <iframe
                    title="Rakuten Motion Widget"
                    src={widgetUrl}
                    style={iframeStyle}
                    scrolling="no"
                    loading="lazy"
                />
            </div>
        </div>
    );
};

export default RakutenMotionWidget;
