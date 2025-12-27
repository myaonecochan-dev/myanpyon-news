import React from 'react';

const RakutenMotionWidget: React.FC = () => {
    // Construct the HTML content for the iframe
    // This perfectly isolates the aggressive Moshimo script
    const srcDoc = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { margin: 0; padding: 0; display: flex; justify-content: center; background: transparent; }
            </style>
        </head>
        <body>
            <!-- MAF Rakuten Widget FROM HERE -->
            <script type="text/javascript">
                MafRakutenWidgetParam=function() { return{ size:'728x200',design:'slide',recommend:'on',auto_mode:'on',a_id:'5317132', border:'off'};};
            </script>
            <script type="text/javascript" src="https://image.moshimo.com/static/publish/af/rakuten/widget.js"></script>
            <!-- MAF Rakuten Widget TO HERE -->
        </body>
        </html>
    `;

    return (
        <div className="rakuten-motion-widget-wrapper" style={{ margin: '2rem auto', maxWidth: '100%', textAlign: 'center', overflow: 'hidden' }}>
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
                srcDoc={srcDoc}
                style={{
                    width: '100%',
                    maxWidth: '728px',
                    height: '200px',
                    border: 'none',
                    overflow: 'hidden'
                }}
                scrolling="no"
            />
        </div>
    );
};

export default RakutenMotionWidget;
