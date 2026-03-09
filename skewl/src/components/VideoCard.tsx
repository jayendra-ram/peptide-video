import Link from 'next/link';
import type { Video } from '@/lib/types';

export function VideoCard({ video }: { video: Video }) {
  return (
    <Link href={`/videos/${video.id}`} className="block group">
      <div className="bg-gray-900 rounded-lg overflow-hidden">
        {video.thumbnail_url ? (
          <img
            src={video.thumbnail_url}
            alt={video.title}
            className="w-full aspect-video object-cover"
          />
        ) : (
          <div className="w-full aspect-video bg-gray-800 flex items-center justify-center">
            <span className="text-gray-600 text-4xl">&#9654;</span>
          </div>
        )}
        <div className="p-4">
          <h3 className="font-semibold group-hover:text-blue-400 transition-colors">
            {video.title}
          </h3>
          {video.collection && (
            <span className="text-xs bg-blue-600/30 text-blue-300 px-2 py-0.5 rounded mt-2 inline-block">
              {video.collection}
            </span>
          )}
        </div>
      </div>
    </Link>
  );
}
