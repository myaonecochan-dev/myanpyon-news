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

    useEffect(() => {
        const handleResize = () => {
            if (window.innerWidth < 600) {
                // Mobile: Zoom in the 300x160 widget to fill screen and make images bigger
                // Scale 1.2x -> 300 * 1.2 = 360px width. Height 160 * 1.2 = 192px.
                setIframeStyle({
                    width: '300px', // Fixed base width for scaling
                    height: '160px', // Fixed base height
                    border: 'none',
                    overflow: 'hidden',
                    transform: 'scale(1.2)', // Zoom in 20%
                    transformOrigin: 'top center',
                    marginBottom: '-10px', // Compensate for bottom whitespace
                    transition: 'all 0.3s ease' // Ensure transition is applied
                });
            } else {
                // PC: Standard 728x200
                setIframeStyle({
                    width: '100%',
                    maxWidth: '728px',
                    height: '200px',
                    border: 'none',
                    overflow: 'hidden',
                    transform: 'none',
                    marginBottom: '0',
                    transition: 'all 0.3s ease' // Ensure transition is applied
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
            // Dynamic height container to accommodate the scaled iframe
            height: iframeStyle.transform && iframeStyle.transform !== 'none' ? '200px' : '200px',
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
                    src="/rakuten_widget.html"
                    style={iframeStyle}
                    scrolling="no"
                    loading="lazy"
                />
            </div>
        </div>
    );
};

export default RakutenMotionWidget;
