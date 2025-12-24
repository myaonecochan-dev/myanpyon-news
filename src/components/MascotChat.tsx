import React from 'react';
import './MascotChat.css';

interface MascotChatProps {
    myanComment?: string;
    pyonComment?: string;
}

const MYAN_PRESETS = [
    "ねえねえ、これすごくない？😻",
    "みゃんもやってみたいにゃ～！🍖",
    "世の中には不思議なことがあるね～🔍",
    "今日の晩ごはんはこれがいいにゃ！🐟",
    "ふむふむ、勉強になるにゃ！📚"
];

const PYON_PRESETS = [
    "また変なニュース見つけてきたね...🐰",
    "まあ、確かに興味深いけど...🥕",
    "ピョンは信じないよ、そんなの！🕶️",
    "へぇ、人間界も大変だねぇ🍵",
    "ふーん、悪くないんじゃない？✨"
];

export const MascotChat: React.FC<MascotChatProps> = ({ myanComment, pyonComment }) => {
    // Pick random text if not provided
    const myanText = myanComment || MYAN_PRESETS[Math.floor(Math.random() * MYAN_PRESETS.length)];
    const pyonText = pyonComment || PYON_PRESETS[Math.floor(Math.random() * PYON_PRESETS.length)];

    return (
        <div className="mascot-chat-container">
            {/* Myan (Left) */}
            <div className="mascot-row">
                <img src="/mascot_cat.png" alt="Myan" className="chat-mascot-icon myan-icon" />
                <div className="speech-bubble">
                    {myanText}
                </div>
            </div>

            {/* Pyon (Right) */}
            <div className="mascot-row reverse">
                <img src="/mascot_bunny.png" alt="Pyon" className="chat-mascot-icon" />
                <div className="speech-bubble">
                    {pyonText}
                </div>
            </div>
        </div>
    );
};
