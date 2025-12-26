import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { MetaHead } from '../components/MetaHead';

export const Contact = () => {
    useEffect(() => {
        window.scrollTo(0, 0);
    }, []);

    return (
        <div className="contact-page" style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', lineHeight: '1.6' }}>
            <MetaHead
                title="お問い合わせ"
                description="みゃんぴょんそくまと！！へのお問い合わせはこちらから。"
            />

            <h1 style={{ borderBottom: '2px solid #ddd', paddingBottom: '10px', marginBottom: '20px' }}>お問い合わせ</h1>

            <section style={{ marginBottom: '30px' }}>
                <p>当サイトに関するお問い合わせ、ご意見、ご感想は、以下のメールアドレス、または公式X（旧Twitter）のDMまでお願いいたします。</p>

                <div style={{ background: '#f9f9f9', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
                    <h3 style={{ marginTop: 0 }}>📩 メールでのお問い合わせ</h3>
                    <p style={{ fontWeight: 'bold' }}>info.myanpyon@gmail.com</p>
                    <p style={{ fontSize: '0.9rem', color: '#666' }}>※（仮のアドレスです。実際のアドレスに変更してください）</p>
                </div>

                <div style={{ background: '#f0f8ff', padding: '20px', borderRadius: '8px', marginTop: '20px' }}>
                    <h3 style={{ marginTop: 0 }}>🐦 SNSでのお問い合わせ</h3>
                    <p>公式X（旧Twitter）のダイレクトメッセージ（DM）でも受け付けております。</p>
                    <a href="https://x.com/NyanPyonMatome" target="_blank" rel="noopener noreferrer"
                        style={{
                            display: 'inline-block',
                            background: 'black',
                            color: 'white',
                            padding: '10px 20px',
                            borderRadius: '20px',
                            textDecoration: 'none',
                            fontWeight: 'bold',
                            marginTop: '10px'
                        }}>
                        X(Twitter)でDMを送る
                    </a>
                </div>
            </section>

            <section>
                <h2>お問い合わせへの対応について</h2>
                <p>いただいたお問い合わせには可能な限り迅速に返信できるよう努めておりますが、内容によってはお時間をいただく場合や、お答えできない場合がございます。あらかじめご了承ください。</p>
            </section>

            <div style={{ marginTop: '50px', borderTop: '1px solid #eee', paddingTop: '20px', textAlign: 'center' }}>
                <Link to="/" style={{ color: '#666', textDecoration: 'none' }}>← トップページに戻る</Link>
            </div>
        </div>
    );
};
