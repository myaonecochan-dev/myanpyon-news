import { Helmet } from 'react-helmet-async';

interface MetaHeadProps {
    title?: string;
    description?: string;
    image?: string; // For OGP
    type?: 'website' | 'article';
    url?: string;
    structuredData?: object;
}

export const MetaHead = ({
    title = 'みゃんぴょんそくまと！！ | 話題の動画・ニュースまとめ',
    description = '世界中の面白い動画、衝撃映像、トレンドニュースを毎日更新！みゃん＆ぴょんが厳選してお届けします。癒やし、びっくり、炎上、トレンドなど幅広いジャンルをカバー。',
    image = '/mascot_cat.png', // Default OGP
    type = 'website',
    url,
    structuredData
}: MetaHeadProps) => {

    const siteTitle = 'みゃんぴょんそくまと！！';
    const fullTitle = title === siteTitle ? title : `${title} | ${siteTitle}`;
    const effectiveUrl = url || window.location.href.split('?')[0];

    return (
        <Helmet>
            {/* Basic */}
            <title>{fullTitle}</title>
            <meta name="description" content={description} />
            <link rel="canonical" href={effectiveUrl} />

            {/* OGP / Social */}
            <meta property="og:title" content={fullTitle} />
            <meta property="og:description" content={description} />
            <meta property="og:type" content={type} />
            <meta property="og:url" content={effectiveUrl} />
            <meta property="og:image" content={image} />
            <meta property="og:site_name" content={siteTitle} />

            {/* Twitter Card */}
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content={fullTitle} />
            <meta name="twitter:description" content={description} />
            <meta name="twitter:image" content={image} />

            {structuredData && (
                <script type="application/ld+json">
                    {JSON.stringify(structuredData)}
                </script>
            )}
        </Helmet>
    );
};
