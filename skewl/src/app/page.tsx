import { supabase } from '@/lib/supabase';
import type { Video } from '@/lib/types';
import { VideoCard } from '@/components/VideoCard';
import { CollectionFilter } from '@/components/CollectionFilter';

export default async function HomePage({
  searchParams,
}: {
  searchParams: Promise<{ collection?: string }>;
}) {
  const { collection } = await searchParams;

  let query = supabase
    .from('videos')
    .select('*')
    .order('created_at', { ascending: false });

  if (collection) {
    query = query.eq('collection', collection);
  }

  const { data: videos } = await query;

  const { data: allVideos } = await supabase
    .from('videos')
    .select('collection');

  const collections = [
    ...new Set(
      (allVideos || []).map((v: { collection: string }) => v.collection).filter(Boolean)
    ),
  ];

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">Lectures</h1>
      <CollectionFilter collections={collections} active={collection || ''} />
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {(videos || []).map((video: Video) => (
          <VideoCard key={video.id} video={video} />
        ))}
      </div>
    </div>
  );
}
