import React from 'react';

interface Product {
    name: string;
    price: string;
    image: string;
    link: string;
}

const SAMPLE_PRODUCTS: Product[] = [
    {
        name: "Dell 4Kモニター 27インチ U2720QM",
        price: "¥64,800",
        image: "https://m.media-amazon.com/images/I/61yFkmwMh-L._AC_SX679_.jpg", // Placeholder or generic tech image
        link: "https://www.amazon.co.jp/"
    },
    {
        name: "Anker Soundcore Liberty 4 (ワイヤレスイヤホン)",
        price: "¥14,990",
        image: "https://m.media-amazon.com/images/I/51r2K-N2+HL._AC_SX679_.jpg", // Placeholder
        link: "https://www.amazon.co.jp/"
    }
];

export const AffiliateBlock: React.FC = () => {
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
                {/* In a real app, you would map this. For design, let's hardcode a robust layout */}
                {SAMPLE_PRODUCTS.map((product, idx) => (
                    <div key={idx} style={{
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
                            flexShrink: 0
                        }}>
                            {/* Placeholder for actual product image */}
                            <span style={{ fontSize: '2rem' }}>📦</span>
                        </div>

                        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
                            <div style={{ fontWeight: 'bold', fontSize: '0.95rem', lineHeight: '1.4' }}>
                                {product.name}
                            </div>
                            <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
                                <a href={product.link} target="_blank" rel="noopener noreferrer" style={{
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
                                <a href={product.link} target="_blank" rel="noopener noreferrer" style={{
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
