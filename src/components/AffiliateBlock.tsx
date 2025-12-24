import React, { useEffect, useState } from 'react';
import { supabase } from '../lib/supabaseClient';

interface Product {
    id: string;
    name: string;
    price: string;
    image_url: string;
    amazon_link?: string;
    rakuten_link?: string;
    active: boolean;
}

export const AffiliateBlock: React.FC = () => {
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
                    setProducts(data);
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
                    <div key={product.id} style={{
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
                ))}
            </div>

            <p style={{ fontSize: '0.75rem', color: '#999', marginTop: '15px', textAlign: 'right' }}>
                ※ 当サイトはアフィリエイトプログラムに参加しています
            </p>
        </div>
    );
};
