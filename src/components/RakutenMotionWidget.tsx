import React from 'react';

const RakutenMotionWidget: React.FC = () => {
    return (
        <div className="rakuten-motion-widget-wrapper" style={{ margin: '2rem auto', maxWidth: '100%', textAlign: 'center', minHeight: '200px' }}>
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
                    height: '200px',
                    border: 'none',
                    overflow: 'hidden'
                }}
                scrolling="no"
                loading="lazy"
            />
        </div>
    );
};

export default RakutenMotionWidget;
