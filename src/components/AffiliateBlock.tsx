/* eslint-disable */
import React, { useEffect, useState, useRef } from 'react';
import { supabase } from '../lib/supabaseClient';

const MoshimoIframe: React.FC<{ html: string }> = ({ html }) => {
    // Wrap HTML in a mobile-friendly template script
    const srcDoc = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { margin: 0; padding: 0; overflow: hidden; background: transparent; font-family: sans-serif; }
                base { target: "_blank"; }

                /* CSS HACK for MOSHIMO MEDIUM SIZE */
                /* Use FLOAT to force Image Left, Text Right (Robust against nesting) */

                div[id^="msmaflink"] {
                    width: 100% !important;
                    padding: 5px !important;
                    box-sizing: border-box !important;
                    overflow: visible !important; /* Allow content to flow */
                }

                /* IMAGE CONTAINER: Float Left */
                div[class*="image"], div[class*="img"] {
                    float: left !important;
                    width: 90px !important;
                    height: 90px !important;
                    margin: 0 10px 0 0 !important;
                    padding: 0 !important;
                    display: block !important;
                }
                
                img {
                    width: 90px !important;
                    height: 90px !important;
                    object-fit: contain !important;
                    border: 1px solid #eee !important;
                    border-radius: 4px !important;
                }

                /* TEXT CONTAINER: Float Right (Fill remaining) */
                div[class*="txt"], div[class*="box"] {
                    float: none !important; /* Don't float the container itself, just let it flow? Or float right? */
                    /* Best practice for "rest of width": overflow hidden or calc width */
                    width: auto !important;
                    overflow: hidden !important; /* Triggers BFC to sit next to float */
                    padding: 0 !important;
                    margin: 0 !important;
                    display: block !important; /* Override flex if present */
                }

                /* Clearfix for main container children if needed */
                div[id^="msmaflink"]::after {
                    content: "";
                    display: table;
                    clear: both;
                }

                /* HIDE ARROWS (Carousel navigation) */
                div[class*="arrow"], 
                div[class*="prev"], 
                div[class*="next"],
                .slick-prev, .slick-next {
                    display: none !important;
                }

                /* TITLE TEXT */
                p, a[class*="link"] {
                    font-size: 12px !important; /* Slightly smaller text */
                    font-weight: bold !important;
                    color: #333 !important;
                    text-decoration: none !important;
                    text-align: left !important;
                    line-height: 1.4 !important;
                    margin: 4px 0 6px 0 !important;
                    
                    display: -webkit-box;
                    -webkit-line-clamp: 2;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    white-space: normal !important;
                }

                /* BUTTON */
                div[class*="btn"], a[class*="btn"] {
                    display: block !important;
                    background: #BF0000 !important;
                    color: white !important;
                    text-align: center !important;
                    padding: 6px 0 !important; /* Reduced padding */
                    border-radius: 4px !important;
                    text-decoration: none !important;
                    font-size: 10px !important; /* Reduced font size */
                    font-weight: bold !important;
                    width: 100% !important;
                    margin: 0 !important;
                    box-shadow: none !important;
                    border: none !important;
                    position: static !important;
                }
                
                /* Hide Price (Compliance) */
                div[class*="price"] {
                    display: none !important;
                }

                /* Hide Header/Footer garbage */
                div[class*="head"], div[class*="foot"], div[class*="credit"] { 
                    display: none !important; 
                }
            </style>
        </head>
        <body>
            ${html}
        </body>
        </html>
    `;

    return (
        <iframe
            title="Affiliate Link"
            srcDoc={srcDoc}
            style={{
                width: '100%',
                height: '160px', /* Increased height to prevent cutoff */
                border: 'none',
                overflow: 'hidden'
            }}
            sandbox="allow-scripts allow-same-origin allow-popups allow-forms"
        />
    );
};


interface Product {
    id: string;
    name: string;
    price: string;
    image_url: string;
    amazon_link?: string;
    amazon_impression_url?: string;
    rakuten_link?: string;
    rakuten_impression_url?: string;
    moshimo_html?: string;
    keywords?: string[];
    active: boolean;
}

interface AffiliateBlockProps {
    postKeywords?: string[];
}

export const AffiliateBlock: React.FC<AffiliateBlockProps> = ({ postKeywords = [] }) => {
    const [products, setProducts] = useState<Product[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const { data, error } = await supabase
                    .from('products')
                    .select('*')
                    .eq('active', true)
                    .order('created_at', { ascending: false });

                if (error) {
                    console.error('Error fetching products:', error);
                } else if (data) {
                    let sortedProducts = data;

                    if (postKeywords.length > 0) {
                        // Calculate match score for each product
                        const scoredProducts = data.map(product => {
                            let score = 0;
                            if (product.keywords && Array.isArray(product.keywords)) {
                                const productKeywords = product.keywords.map((k: string) => k.toLowerCase());
                                postKeywords.forEach(pk => {
                                    if (productKeywords.some((k: string) => k.includes(pk.toLowerCase()) || pk.toLowerCase().includes(k))) {
                                        score += 1;
                                    }
                                });
                            }
                            return { ...product, score };
                        });

                        // Sort by score (descending), then by date
                        sortedProducts = scoredProducts.sort((a, b) => {
                            // Manual override: Pin 'Nintendo Switch 2' to top
                            const isSwitchA = a.name.includes('Nintendo Switch 2');
                            const isSwitchB = b.name.includes('Nintendo Switch 2');
                            if (isSwitchA && !isSwitchB) return -1;
                            if (!isSwitchA && isSwitchB) return 1;

                            if (b.score !== a.score) return b.score - a.score;
                            return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
                        });
                    }

                    setProducts(sortedProducts);
                }
            } catch (err) {
                console.error('Unexpected error:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchProducts();
    }, []);

    if (loading) return null;
    if (products.length === 0) return null;

    return (
        <div className="affiliate-block" style={{
            background: '#fff',
            padding: '20px',
            borderRadius: '12px',
            marginTop: '30px',
            border: '1px solid #e0e0e0',
            boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
        }}>
            <h4 style={{
                margin: '0 0 15px 0',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '1.1rem',
                borderBottom: '2px solid #f0f0f0',
                paddingBottom: '10px'
            }}>
                <span style={{ fontSize: '1.4rem' }}>🛍️</span>
                <span>気になったアイテムをチェック！</span>
            </h4>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px' }}>
                {products.map((product) => (
                    <div key={product.id} className="product-item">
                        {product.moshimo_html ? (
                            <div className="moshimo-container">
                                <MoshimoIframe html={product.moshimo_html} />
                            </div>
                        ) : (
                            <div style={{
                                display: 'flex',
                                gap: '15px',
                                background: '#f9f9f9',
                                padding: '10px',
                                borderRadius: '8px'
                            }}>
                                <div style={{
                                    width: '80px',
                                    height: '80px',
                                    background: '#fff',
                                    borderRadius: '4px',
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    border: '1px solid #eee',
                                    flexShrink: 0,
                                    overflow: 'hidden'
                                }}>
                                    {product.image_url ? (
                                        <img src={product.image_url} alt={product.name} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />
                                    ) : (
                                        <span style={{ fontSize: '2rem' }}>📦</span>
                                    )}
                                </div>

                                <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                                    <div style={{ fontWeight: 'bold', fontSize: '0.95rem', lineHeight: '1.4' }}>
                                        {product.name}
                                    </div>
                                    {/* Price display removed for compliance */}
                                    <div style={{ display: 'flex', gap: '8px', marginTop: 'auto' }}>
                                        {product.amazon_link && (
                                            <a href={product.amazon_link} target="_blank" rel="noopener noreferrer" style={{
                                                flex: 1,
                                                background: '#FF9900',
                                                color: 'white',
                                                textAlign: 'center',
                                                padding: '6px',
                                                borderRadius: '4px',
                                                fontSize: '0.8rem',
                                                fontWeight: 'bold',
                                                textDecoration: 'none',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center'
                                            }}>
                                                Amazon
                                            </a>
                                        )}
                                        {product.rakuten_link && (
                                            <a href={product.rakuten_link} target="_blank" rel="noopener noreferrer" style={{
                                                flex: 1,
                                                background: '#BF0000',
                                                color: 'white',
                                                textAlign: 'center',
                                                padding: '6px',
                                                borderRadius: '4px',
                                                fontSize: '0.8rem',
                                                fontWeight: 'bold',
                                                textDecoration: 'none',
                                                display: 'flex',
                                                alignItems: 'center',
                                                justifyContent: 'center'
                                            }}>
                                                楽天
                                            </a>
                                        )}
                                    </div>
                                </div>
                            </div>
                        )}
                        {/* Impression Trackers */}
                        {product.rakuten_impression_url && (
                            <img src={product.rakuten_impression_url} width="1" height="1" style={{ border: 'none', display: 'none' }} loading="lazy" alt="" />
                        )}
                        {product.amazon_impression_url && (
                            <img src={product.amazon_impression_url} width="1" height="1" style={{ border: 'none', display: 'none' }} loading="lazy" alt="" />
                        )}
                    </div>
                ))}
            </div>

            <p style={{ fontSize: '0.75rem', color: '#999', marginTop: '15px', textAlign: 'right' }}>
                ※ 当サイトはアフィリエイトプログラムに参加しています
            </p>
        </div>
    );
};
