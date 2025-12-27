
export default async function handler(request, response) {
    // Allow robust handling of CORS if needed, though Vercel handles same-origin usually.
    if (request.method === 'OPTIONS') {
        return response.status(200).end();
    }

    if (request.method !== 'POST') {
        return response.status(405).json({ error: 'Method Not Allowed' });
    }

    try {
        const { author, content, post_title, post_id } = request.body;
        const webhookUrl = process.env.DISCORD_WEBHOOK_URL;

        if (!webhookUrl) {
            console.error("DISCORD_WEBHOOK_URL is missing in environment variables.");
            return response.status(500).json({ error: 'Server Configuration Error: Missing Webhook URL' });
        }

        // Discord Webhook Payload
        const payload = {
            username: "みゃんぴょん速報 コメント通知",
            avatar_url: "https://myanpyonsokumato.com/favicon.png", // Optional: Use site favicon
            embeds: [
                {
                    title: "💬 新しいコメントが投稿されました！",
                    description: content,
                    color: 5957084, // Greenish
                    fields: [
                        { name: "記事", value: post_title || "不明な記事", inline: true },
                        { name: "投稿者", value: author || "名無しさん", inline: true }
                    ],
                    footer: { text: `Post ID: ${post_id}` },
                    timestamp: new Date().toISOString()
                }
            ]
        };

        // Send to Discord
        const discordRes = await fetch(webhookUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!discordRes.ok) {
            const errText = await discordRes.text();
            throw new Error(`Discord API Error: ${discordRes.status} ${errText}`);
        }

        return response.status(200).json({ success: true });

    } catch (error) {
        console.error("Notification Failed:", error);
        return response.status(500).json({ error: 'Failed to send notification' });
    }
}
