import { supabase } from '@/lib/supabase';
import { VideoPlayer } from '@/components/VideoPlayer';
import { CommentSection } from '@/components/CommentSection';
import { notFound } from 'next/navigation';

export default async function VideoPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;

  const { data: video } = await supabase
    .from('videos')
    .select('*')
    .eq('id', id)
    .single();

  if (!video) notFound();

  const { data: comments } = await supabase
    .from('comments')
    .select('*')
    .eq('video_id', id)
    .order('created_at', { ascending: true });

  return (
    <div className="max-w-4xl mx-auto">
      <VideoPlayer url={video.video_url} />
      <h1 className="text-2xl font-bold mt-4">{video.title}</h1>
      {video.collection && (
        <span className="inline-block bg-blue-600 text-sm px-2 py-1 rounded mt-2">
          {video.collection}
        </span>
      )}
      <p className="text-gray-400 mt-2">{video.description}</p>
      <hr className="border-gray-800 my-8" />
      <CommentSection videoId={id} initialComments={comments || []} />
    </div>
  );
}
