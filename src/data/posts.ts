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

// Demo posts removed for production
export const posts: Post[] = [];
