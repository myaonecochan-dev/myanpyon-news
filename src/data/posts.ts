export type Platform = 'youtube' | 'twitter' | 'tiktok' | 'article' | '2ch';
export type ContentType = 'video' | 'article' | 'thread' | 'image';
export type Category = 'animals' | 'surprise' | 'trend' | 'flame';

export interface Post {
  id: string;
  title: string;
  category: Category;
  type: ContentType;
  platform: Platform;
  description: string;

  // Video specific
  youtubeId?: string;
  embedId?: string;

  // Article/Thread specific
  content?: string; // HTML or Markdown body
  imageUrl?: string; // Thumbnail or main image
  created_at: string; // ISO Date string
}

export const posts: Post[] = [
  // --- Animals (動物) ---
  {
    id: 'a1',
    title: '【癒し】初めて雪を見た子犬の反応が可愛すぎると話題に',
    category: 'animals',
    type: 'video',
    platform: 'youtube',
    description: '生まれて初めての雪に大はしゃぎするゴールデンレトリバーの子犬。',
    youtubeId: '4W2qYq6f3Y8',
    created_at: '2025-12-20T10:00:00Z'
  },
  {
    id: 'a2',
    title: '【モフモフ】この猫、世界で一番丸いかもしれない',
    category: 'animals',
    type: 'video',
    platform: 'twitter',
    description: '冬毛に生え変わって完全にボールと化した猫ちゃん。',
    embedId: '1615392873123840000',
    created_at: '2025-12-21T15:30:00Z'
  },

  // --- Surprise (衝撃) ---
  {
    id: 's1',
    title: '【感動】ロンドン駅で突然始まったフラッシュモブ',
    category: 'surprise',
    type: 'video',
    platform: 'youtube',
    description: '数百人のダンサーが突如踊り出し、駅利用客も巻き込んで大盛り上がり！',
    youtubeId: 'dQw4w9WgXcQ',
    created_at: '2025-12-22T09:15:00Z'
  },

  // --- TREND (トレンド) - 日本語 & 詳細記事化 ---
  {
    id: 't1',
    title: '【速報】空中に映像が出るスマホ「X-Phone 16」発表！SFが現実に',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: 'ついにホログラム機能を搭載したスマートフォンが登場。予約は明日から開始。',
    imageUrl: '/trend.png',
    content: `
      <h2>SFの世界がついに現実に</h2>
      <p>大手テック企業は本日、世界初となるホログラム投影機能を搭載したスマートフォン<strong>「X-Phone 16 Pro」</strong>を発表しました。</p>
      <p>このデバイスは、画面から3D映像を空中に投影することができ、専用のメガネなしで立体的な映像楽しむことができます。</p>
      <h3>主な機能</h3>
      <ul>
        <li>6.7インチ ホログラフィック・ディスプレイ</li>
        <li>AIによるリアルタイム3D変換機能</li>
        <li>バッテリー持続時間は驚異の48時間</li>
      </ul>
      <p>専門家は「スマートフォンの歴史を変える革命的な一台になる」と絶賛しています。</p>
    `,
    created_at: '2025-12-23T08:00:00Z'
  },
  {
    id: 't2',
    title: '【時代】AIアイドル「ネオンちゃん」がレコ大新人賞を受賞！',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: 'バーチャルシンガーが人間のアーティストを抑えて受賞する初の快挙。',
    imageUrl: '/trend.png', // Reusing for demo
    content: `
      <h2>バーチャルがリアルを超えた日</h2>
      <p>今年のレコード大賞新人賞に、AI生成によるバーチャルアイドル<strong>「ネオンちゃん」</strong>が選ばれました。</p>
      <p>授賞式では、ホログラムとしてステージに登場し、デビュー曲「Digital Heart」を熱唱。会場はスタンディングオベーションに包まれました。</p>
      <p>審査員長は「彼女の歌声は、データでありながら誰よりも『心』を感じさせた」とコメントしています。</p>
    `,
    created_at: '2025-12-23T12:00:00Z'
  },
  {
    id: 't3',
    title: '【注意】クリスマスイブに関東で大雪の恐れ。交通機関への影響懸念',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: '10年に一度の寒波が到来。帰宅ラッシュを直撃する可能性も。',
    imageUrl: '/trend.png',
    content: `
      <h2>ホワイトクリスマスならぬ豪雪クリスマス？</h2>
      <p>気象庁の発表によると、24日のクリスマスイブにかけて、関東平野部でも積雪が予想されています。</p>
      <p>特に夕方から夜にかけて降雪が強まる見込みで、JRや私鉄各線では間引き運転や遅延の可能性があります。</p>
      <p>専門家は「無理な外出は控え、仕事納めの会社員は早めの帰宅を」と呼びかけています。</p>
    `,
    created_at: '2025-12-23T18:45:00Z'
  },
  {
    id: 't4',
    title: '【癒し】猫のウィスカーズ市長、新しい「さかな税」導入を肉球で承認',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: 'アラスカの小さな町の名物市長（5歳・雄）が重要書類にサイン。',
    imageUrl: '/trend.png',
    content: `
      <h2>厳粛な（？）調印式</h2>
      <p>アラスカ州の某町で市長を務める猫のウィスカーズ氏が、本日、市の新しい観光政策に関する書類に決裁を行いました。</p>
      <p>ウィスカーズ市長は報道陣が見守る中、朱肉に前足を浸し、力強く書類に肉球スタンプを押しました。</p>
      <p>なお、市長への報酬として、高級マグロ缶3年分が贈呈されるとのことです。</p>
    `,
    created_at: '2025-12-24T11:20:00Z'
  },
  {
    id: 't5',
    title: '【待望】ジブリ新作「風の残響」ティーザー公開。宮崎監督の「最後の最後」',
    category: 'trend',
    type: 'video',
    platform: 'youtube', // Hybrid type
    description: '息を呑むような美しい背景美術に、世界中から称賛の声。',
    youtubeId: 'dQw4w9WgXcQ', // Placeholder
    created_at: '2025-12-24T14:10:00Z'
  },
  {
    id: 't6',
    title: '【朗報】「食べるだけで若返るチョコ」が発見される。1日50gで肌年齢-10歳',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: '希少なカカオ豆に含まれる成分に驚異的な抗酸化作用。',
    imageUrl: '/trend.png',
    content: `
      <h2>スイーツ好きに朗報</h2>
      <p>スイスの研究チームが、特定の希少カカオ豆に含まれるポリフェノールに、細胞の老化を劇的に遅らせる効果があることを発見しました。</p>
      <p>臨床試験では、この成分を含んだチョコレートを4週間摂取した被験者の肌年齢が、平均で10歳若返ったという結果が出ています。</p>
      <p>この「若返りチョコ」は来春、ドラッグストアなどで発売される予定です。</p>
    `,
    created_at: '2025-12-24T16:50:00Z'
  },
  {
    id: 't7',
    title: '【動画】TikTokで流行中の「無重力ダンス」がヤバすぎると話題に',
    category: 'trend',
    type: 'video',
    platform: 'tiktok',
    description: 'どうなってるの？物理法則を無視したような動きに海外で1億再生。',
    embedId: '7200000000000000000',
    created_at: '2025-12-25T09:30:00Z'
  },
  {
    id: 't8',
    title: '【夢】宇宙ホテル「オービット・ワン」が2027年開業！1泊500万円から',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: '無重力プールや地球を一望できるスイートルームを完備。',
    imageUrl: '/trend.png',
    content: `
      <h2>究極のバケーション</h2>
      <p>宇宙開発企業は、地球周回軌道上に建設中のラグジュアリーホテル「オービット・ワン」の予約受付を開始しました。</p>
      <p>宿泊客は、窓から青い地球を眺めながら食事を楽しんだり、無重力空間でのスポーツ体験などが可能です。</p>
      <p>価格はスタンダードルームで1泊500万円から。既に富裕層を中心に1年先まで予約が埋まっているとのことです。</p>
    `,
    created_at: '2025-12-25T13:00:00Z'
  },
  {
    id: 't9',
    title: '【悲報】VRMMO「SAOリアル」βテスト開始もログアウトボタンが見つからない不具合',
    category: 'trend',
    type: 'thread',
    platform: '2ch',
    description: '運営「仕様ではありません。現在調査中です」',
    imageUrl: '/trend.png',
    content: `
      <div class="thread-comment">
        <div class="meta">1: <span class="name">名無しさん</span> 2025/12/28 12:00:00</div>
        <div class="body">これマジでメニューにログアウトないんだがｗｗｗ<br>どうやって抜けるの？</div>
      </div>
      <div class="thread-comment">
        <div class="meta">2: <span class="name">名無しさん</span> 2025/12/28 12:01:30</div>
        <div class="body">>>1<br>電源ボタン長押しでいけるやろ。知らんけど。</div>
      </div>
      <div class="thread-comment">
        <div class="meta">3: <span class="name">キリト</span> 2025/12/28 12:05:00</div>
        <div class="body">>>1<br>おい、これゲームじゃねえぞ...</div>
      </div>
       <div class="thread-comment">
        <div class="meta">4: <span class="name">名無しさん</span> 2025/12/28 12:06:00</div>
        <div class="body">>>3<br>なりきり乙ｗｗｗ</div>
      </div>
      </div>
    `,
    created_at: '2025-12-26T20:00:00Z'
  },
  {
    id: 't10',
    title: '【社会】ディープフェイク規制法が可決。AI生成動画には透かしが義務化へ',
    category: 'trend',
    type: 'article',
    platform: 'article',
    description: '違反者には罰金刑も。2026年4月から施行。',
    imageUrl: '/trend.png',
    content: `
      <h2>「真実」を守るための新法</h2>
      <p>本日、国会にて「AI生成コンテンツ適正化法」が可決されました。</p>
      <p>この法律により、AIを使用して作成された画像や動画には、人間の目には見えない電子透かし（ウォーターマーク）の埋め込みが義務付けられます。</p>
      <p>違反したプラットフォーム事業者や個人には、最大で1億円の罰金が科される可能性があります。</p>
    `,
    created_at: '2025-12-27T10:00:00Z'
  },

  // --- FLAME / CONTROVERSY (炎上) ---
  {
    id: 'f1',
    title: '【悲報】人気カフェチェーン「スタバックス」、全店舗閉鎖を発表',
    category: 'flame',
    type: 'thread',
    platform: '2ch',
    description: 'ネット民「嘘だろ...」「明日からどこでドヤればいいんだ」阿鼻叫喚の嵐。',
    imageUrl: '/trend.png',
    content: `
      <div class="thread-comment">
        <div class="meta">1: <span class="name">名無しさん</span> 2025/12/24 12:00:00</div>
        <div class="body">ファッ！？マジで閉店！？</div>
      </div>
      <div class="thread-comment">
        <div class="meta">2: <span class="name">名無しさん</span> 2025/12/24 12:01:30</div>
        <div class="body">新作のフラペチーノ飲もうと思ってたのに...</div>
      </div>
      <div class="thread-comment">
        <div class="meta">3: <span class="name">名無しさん</span> 2025/12/24 12:05:00</div>
        <div class="body">コーヒー豆高騰しすぎだからな。しゃーない。</div>
      </div>
      </div>
    `,
    created_at: '2025-12-24T12:00:00Z'
  },
  {
    id: 'f2',
    title: '【炎上】人気YouTuber、行き過ぎたドッキリで警察沙汰に',
    category: 'flame',
    type: 'video',
    platform: 'youtube',
    description: '謝罪動画を出すも低評価が止まらない事態に。',
    youtubeId: '9bZkp7q19f0',
    created_at: '2025-12-25T18:30:00Z'
  },
  {
    id: 'f3',
    title: '【伝説】新入社員さん、入社式から3時間で退職代行を使ってバックレるｗｗｗｗｗ',
    category: 'flame',
    type: 'thread',
    platform: '2ch',
    description: '人事「えっ？（困惑）」同期「ファッ！？」→ 衝撃の理由がこちらｗ',
    imageUrl: '/trend.png',
    content: `
      <div style="font-weight:bold; margin-bottom:1rem; color:#333;">
        1: <span style="color:green;">風吹けば名無し</span> 2026/04/01(水) 12:30:45.12 ID:NvK7s/T0p<br>
        トイレ行ってくるって言ったまま戻ってこないんだが。<br>
        さっき人事宛に退職代行から電話あったらしいｗｗｗ
      </div>

      <div class="thread-comment">
        <div class="meta">2: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:31:10.55 ID:aB3cD/Ef0</div>
        <div class="body">クソワロタｗｗｗｗ早すぎんだろ</div>
      </div>

      <div class="thread-comment">
        <div class="meta">3: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:31:45.33 ID:XyZ9/Qr1</div>
        <div class="body">判断が早い</div>
      </div>

      <div class="thread-comment">
        <div class="meta">4: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:32:20.12 ID:NvK7s/T0p</div>
        <div class="body">
          <span style="color:blue;">>>2</span><br>
          部長が顔真っ赤にして電話怒鳴ってるわ<br>
          「ふざけんな！」って聞こえてくるｗｗ
        </div>
      </div>

      <div class="thread-comment">
        <div class="meta">5: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:33:00.00 ID:Gh7jK/Lx9</div>
        <div class="body">
           なんで辞めたん？<br>
           ブラックなんか？
        </div>
      </div>

      <div class="thread-comment">
        <div class="meta">6: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:34:12.88 ID:NvK7s/T0p</div>
        <div class="body">
          <span style="color:blue;">>>5</span><br>
          入社式で社長が「うちは家族だ！」って言った瞬間にスマホいじりだして、<br>
          そのあとトイレ行ったっきりや。<br>
          たぶん「家族」ワードが地雷だったんじゃね？
        </div>
      </div>

      <div class="thread-comment">
        <div class="meta">7: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:35:55.44 ID:mN8oP/Qt2</div>
        <div class="body">
          アットホームな職場です（激怒）
        </div>
      </div>
      
      <div class="thread-comment">
        <div class="meta">8: <span class="name">風吹けば名無し</span> 2026/04/01(水) 12:36:30.11 ID:Ry4uI/Op5</div>
        <div class="body">
          <span style="color:blue;">>>6</span><br>
          優秀な危機察知能力やんけ将来有望やな
        </div>
      </div>

      <div class="thread-comment">
        <div class="meta">999: <span class="name">風吹けば名無し</span> 2026/04/01(水) 13:00:00.00 ID:Admin</div>
        <div class="body">
           <br>
           <b>【まとめ】</b><br>
           最近の若いもんは...と言いたいところだが、<br>
           「家族」とか言い出す会社は大体ヤバいから正解かもしれん。<br>
           みんなも気をつけるように。
        </div>
      </div>
      </div>
    `,
    created_at: '2026-04-01T12:30:00Z'
  }
];
