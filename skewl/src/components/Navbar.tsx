import Link from 'next/link';

export function Navbar() {
  return (
    <nav className="border-b border-gray-800 px-4 py-3">
      <div className="max-w-6xl mx-auto flex items-center justify-between">
        <Link href="/" className="text-xl font-bold">
          skewl
        </Link>
        <Link
          href="/upload"
          className="bg-blue-600 hover:bg-blue-500 px-4 py-1.5 rounded text-sm"
        >
          Upload
        </Link>
      </div>
    </nav>
  );
}
