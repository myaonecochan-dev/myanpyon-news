/* eslint-disable */
import React, { useEffect, useState, useRef } from 'react';
import { supabase } from '../lib/supabaseClient';

const MoshimoIframe: React.FC<{ html: string }> = ({ html }) => {
    const srcDoc = `
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { margin: 0; padding: 0; overflow: hidden; background: transparent; display: flex; justify-content: center; }
                base { target: "_blank"; }
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
                height: '240px',
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

            <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '15px' }}>
                {products.map((product) => (
                    <div key={product.id} className="product-item">
                        {product.moshimo_html ? (
                            <div className="moshimo-container" style={{ maxWidth: '600px', margin: '0 auto' }}>
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
                                    <div style={{ fontSize: '0.9rem', color: '#e74c3c', fontWeight: 'bold', marginBottom: '5px' }}>
                                        {product.price}
                                    </div>
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
