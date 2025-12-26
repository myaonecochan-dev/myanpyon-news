/* eslint-disable */
import React, { useEffect, useState, useRef } from 'react';
import { supabase } from '../lib/supabaseClient';

const SafeMoshimoScript: React.FC<{ html: string }> = ({ html }) => {
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!containerRef.current || !html) return;

        // Generate a unique namespace for this instance to prevent SPA conflicts
        const uniqueId = Math.random().toString(36).substring(2, 9);
        const namespace = `msmaflink_${uniqueId}`;

        // Replace all occurrences of 'msmaflink' with the new namespace
        // This updates:
        // 1. The IIFE argument (global variable name)
        // 2. The function call (msmaflink({...}))
        // 3. The container DIV id (id="msmaflink-...") if present
        const namespacedHtml = html.split('msmaflink').join(namespace);

        // Clear and set new HTML
        containerRef.current.innerHTML = namespacedHtml;

        // Execute the new scripts
        const scripts = containerRef.current.getElementsByTagName('script');
        Array.from(scripts).forEach(script => {
            const newScript = document.createElement('script');
            Array.from(script.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
            newScript.appendChild(document.createTextNode(script.innerHTML));
            script.parentNode?.replaceChild(newScript, script);
        });

        // Cleanup: Remove the specific script tag and global variable to prevent leaks
        return () => {
            // We can try to cleanup the script tag corresponding to this namespace
            const scriptTag = document.getElementById(namespace);
            if (scriptTag) scriptTag.remove();

            // Optional: Cleanup global object if possible, but might be tricky if external script holds ref
            if ((window as any)[namespace]) {
                delete (window as any)[namespace];
            }
        };
    }, [html]);

    return <div ref={containerRef} />;
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

    // If loading or no products, we can hide the block or show nothing to avoid layout shifts.
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
