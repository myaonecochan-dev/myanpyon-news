import React, { useEffect, useRef } from 'react';

const RakutenMotionWidget: React.FC = () => {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current) return;

        // Clean up previous injection if any (though StrictMode might run this twice)
        containerRef.current.innerHTML = '';

        // 1. Define the parameter function on the window object
        // This tells the Moshimo script what to render
        (window as any).MafRakutenWidgetParam = function () {
            return {
                size: '728x200',
                design: 'slide',
                recommend: 'on',
                auto_mode: 'on',
                a_id: '5317132',
                border: 'off'
            };
        };

        // 2. Create the script element
        const script = document.createElement('script');
        script.src = "https://image.moshimo.com/static/publish/af/rakuten/widget.js";
        script.type = "text/javascript";
        script.async = true; // Non-blocking

        // 3. Append to container
        // The widget usually renders at the script's location
        containerRef.current.appendChild(script);

        return () => {
            // Cleanup is tricky for external scripts, but we can clear the container
            if (containerRef.current) {
                containerRef.current.innerHTML = '';
            }
        };
    }, []);

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
            <div ref={containerRef} style={{ display: 'flex', justifyContent: 'center' }} />
        </div>
    );
};

export default RakutenMotionWidget;
