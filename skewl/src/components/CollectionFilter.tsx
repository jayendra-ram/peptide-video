import Link from 'next/link';

export function CollectionFilter({
  collections,
  active,
}: {
  collections: string[];
  active: string;
}) {
  return (
    <div className="flex gap-2 flex-wrap">
      <Link
        href="/"
        className={`px-3 py-1 rounded-full text-sm ${
          !active ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'
        }`}
      >
        All
      </Link>
      {collections.map((c) => (
        <Link
          key={c}
          href={`/?collection=${encodeURIComponent(c)}`}
          className={`px-3 py-1 rounded-full text-sm ${
            active === c ? 'bg-blue-600' : 'bg-gray-800 hover:bg-gray-700'
          }`}
        >
          {c}
        </Link>
      ))}
    </div>
  );
}
