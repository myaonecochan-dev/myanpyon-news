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

    useEffect(() => {
        if (!isDev) {
            try {
                // @ts-ignore
                (window.adsbygoogle = window.adsbygoogle || []).push({});
            } catch (err) {
                console.error('AdSense error:', err);
            }
        }
    }, [isDev]);

    if (isDev) {
        return (
            <div
                style={{
                    ...style,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    backgroundColor: '#e9e9e9',
                    border: '1px dashed #ccc',
                    color: '#666',
                    padding: '1rem',
                    minHeight: style.height || '250px',
                    margin: '1rem 0'
                }}
            >
                <div style={{ textAlign: 'center' }}>
                    <p style={{ fontWeight: 'bold', margin: 0 }}>AdSense Area</p>
                    <p style={{ fontSize: '0.8rem', margin: 0 }}>Slot ID: {slot}</p>
                    <p style={{ fontSize: '0.8rem', margin: 0 }}>(Visible in Production)</p>
                </div>
            </div>
        );
    }

    return (
        <div style={{ margin: '1rem 0', textAlign: 'center' }}>
            <ins
                className="adsbygoogle"
                style={adStyle}
                data-ad-client="ca-pub-XXXXXXXXXXXXXXXX" // Replace with USER's actual client ID later
                data-ad-slot={slot}
                data-ad-format={format}
                data-full-width-responsive={responsive ? "true" : "false"}
            />
        </div>
    );
};
