import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MetaHead } from '../components/MetaHead';

export const PrivacyPolicy = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <div className="privacy-policy-page" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', lineHeight: '1.6' }}>
            <MetaHead
                title="プライバシーポリシー"
                description="みゃんぴょんそくまと！！のプライバシーポリシーです。"
            />

            <h1 style={{ borderBottom: '2px solid #ddd', paddingBottom: '10px', marginBottom: '20px' }}>プライバシーポリシー</h1>

            <section style={{ marginBottom: '30px' }}>
                <h2>広告の配信について</h2>
                <p>当サイトでは、第三者配信の広告サービス（Googleアドセンス、A8.net、もしもアフィリエイトなど）を利用しています。</p>
                <p>このような広告配信事業者は、ユーザーの興味に応じた商品やサービスの広告を表示するため、当サイトや他サイトへのアクセスに関する情報『Cookie』(氏名、住所、メールアドレス、電話番号は含まれません) を使用することがあります。</p>
                <p>またGoogleアドセンスに関して、このプロセスの詳細やこのような情報が広告配信事業者に使用されないようにする方法については、<a href="https://policies.google.com/technologies/ads?hl=ja" target="_blank" rel="noopener noreferrer" style={{ color: '#007bff' }}>こちら</a>をご覧ください。</p>
            </section>

            <section style={{ marginBottom: '30px' }}>
                <h2>アクセス解析ツールについて</h2>
                <p>当サイトでは、Googleによるアクセス解析ツール「Googleアナリティクス」を利用しています。</p>
                <p>このGoogleアナリティクスはトラフィックデータの収集のためにCookieを使用しています。このトラフィックデータは匿名で収集されており、個人を特定するものではありません。</p>
                <p>この機能はCookieを無効にすることで収集を拒否することが出来ますので、お使いのブラウザの設定をご確認ください。この規約に関して、詳しくは<a href="https://marketingplatform.google.com/about/analytics/terms/jp/" target="_blank" rel="noopener noreferrer" style={{ color: '#007bff' }}>こちら</a>をご覧ください。</p>
            </section>

            <section style={{ marginBottom: '30px' }}>
                <h2>著作権について</h2>
                <p>当サイトで掲載している画像の著作権・肖像権等は各権利所有者に帰属致します。権利を侵害する目的ではございません。</p>
                <p>記事の内容や掲載画像等に問題がございましたら、各権利所有者様本人が直接メールでご連絡下さい。確認後、対応させて頂きます。</p>
            </section>

            <section style={{ marginBottom: '30px' }}>
                <h2>免責事項</h2>
                <p>当サイトからリンクやバナーなどによって他のサイトに移動された場合、移動先サイトで提供される情報、サービス等について一切の責任を負いません。</p>
                <p>当サイトのコンテンツ・情報につきまして、可能な限り正確な情報を掲載するよう努めておりますが、誤情報が入り込んだり、情報が古くなっていることもございます。</p>
                <p>当サイトに掲載された内容によって生じた損害等の一切の責任を負いかねますのでご了承ください。</p>
            </section>

            <div style={{ marginTop: '50px', borderTop: '1px solid #eee', paddingTop: '20px', textAlign: 'center' }}>
                <Link to="/" style={{ color: '#666', textDecoration: 'none' }}>← トップページに戻る</Link>
            </div>
        </div>
    );
};
