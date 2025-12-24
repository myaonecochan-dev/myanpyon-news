import React, { useEffect } from 'react';

interface AdSenseDisplayProps {
    slot: string;
    style?: React.CSSProperties;
    format?: 'auto' | 'fluid' | 'rectangle';
    responsive?: boolean;
}

export const AdSenseDisplay: React.FC<AdSenseDisplayProps> = ({
    slot,
    style = {},
    format = 'auto',
    responsive = true
}) => {
    // Check if we are in production mode (or use a specific flag)
    // For this demo, we assume 'development' means show placeholder
    const isDev = import.meta.env.DEV;

    const adStyle: React.CSSProperties = {
        display: 'block',
        textAlign: 'center',
        ...style,
    };

    // Safe AdSense loader
    useEffect(() => {
        if (!isDev) {
            try {
                // Check if script is loaded
                if (document.querySelectorAll('script[src*="adsbygoogle"]').length === 0) {
                    const script = document.createElement('script');
                    script.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX";
                    script.async = true;
                    script.crossOrigin = "anonymous";
                    document.head.appendChild(script);
                }

                // Push ad
                // @ts-ignore
                (window.adsbygoogle = window.adsbygoogle || []).push({});
            } catch (err) {
                console.error('AdSense error:', err);
            }
        }
    }, [isDev, slot]);

    if (isDev) {
        return (
            <div
                style={{
                    ...style,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: '#f0f0f0',
                    border: '2px dashed #ccc',
                    color: '#888',
                    padding: '1rem',
                    minHeight: style.height || '250px',
                    margin: '1rem 0',
                    borderRadius: '8px'
                }}
            >
                <span style={{ fontSize: '2rem' }}>📢</span>
                <p style={{ fontWeight: 'bold', margin: '0.5rem 0' }}>Google AdSense</p>
                <div style={{ fontSize: '0.8rem', textAlign: 'center' }}>
                    Slot ID: {slot}<br />
                    Format: {format}<br />
                    (Visible in Production)
                </div>
            </div>
        );
    }

    return (
        <div className="adsense-container" style={{ margin: '1rem 0', textAlign: 'center', overflow: 'hidden' }}>
            <ins
                className="adsbygoogle"
                style={adStyle}
                data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" // TODO: Replace with user's ID
                data-ad-slot={slot}
                data-ad-format={format}
                data-full-width-responsive={responsive ? "true" : "false"}
            />
        </div>
    );
};
