export function VideoPlayer({ url }: { url: string }) {
  return (
    <video
      src={url}
      controls
      className="w-full rounded-lg aspect-video bg-black"
    />
  );
}
