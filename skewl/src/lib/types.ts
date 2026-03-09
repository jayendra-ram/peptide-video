export interface Video {
  id: string;
  title: string;
  description: string;
  collection: string;
  video_url: string;
  thumbnail_url: string;
  duration_seconds: number;
  created_at: string;
}

export interface Comment {
  id: string;
  video_id: string;
  author_name: string;
  body: string;
  created_at: string;
}
