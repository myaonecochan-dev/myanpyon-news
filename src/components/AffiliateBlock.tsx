import React from 'react';

interface Product {
    name: string;
    price: string;
    image: string;
    link: string;
}

const SAMPLE_PRODUCTS: Product[] = [
    {
        name: "最新スマホスタンド (猫型)",
        price: "¥1,980",
        image: "https://via.placeholder.com/150",
        link: "#"
    },
    {
        name: "AIスマートスピーカー",
        price: "¥5,400",
        image: "https://via.placeholder.com/150",
        link: "#"
    }
];

export const AffiliateBlock: React.FC = () => {
    return (
        <div className="affiliate-block" style={{
            background: '#f8f9fa',
            padding: '1.5rem',
            borderRadius: '12px',
            marginTop: '2rem',
            border: '1px solid #eee'
        }}>
            <h4 style={{ margin: '0 0 1rem 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.2rem' }}>🛍️</span>
                <span>管理人のおすすめアイテム</span>
            </h4>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                {SAMPLE_PRODUCTS.map((product, idx) => (
                    <a key={idx} href={product.link} style={{ textDecoration: 'none', color: 'inherit', display: 'block', background: 'white', borderRadius: '8px', padding: '10px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                        <div style={{ height: '100px', background: '#ddd', borderRadius: '4px', marginBottom: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#666', fontSize: '0.8rem' }}>
                            No Image
                        </div>
                        <div style={{ fontSize: '0.9rem', fontWeight: 'bold', lineHeight: '1.4', marginBottom: '4px' }}>{product.name}</div>
                        <div style={{ color: '#e74c3c', fontWeight: 'bold' }}>{product.price}</div>
                        <div style={{ marginTop: '8px', textAlign: 'center' }}>
                            <span style={{ display: 'inline-block', padding: '4px 12px', background: '#f39c12', color: 'white', borderRadius: '20px', fontSize: '0.8rem', fontWeight: 'bold' }}>Amazonで見る</span>
                        </div>
                    </a>
                ))}
            </div>
            <p style={{ fontSize: '0.75rem', color: '#999', marginTop: '10px', textAlign: 'right' }}>
                ※ アフィリエイトリンクを含みます
            </p>
        </div>
    );
};
