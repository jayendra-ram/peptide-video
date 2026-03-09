'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { supabase } from '@/lib/supabase';

export function UploadForm() {
  const router = useRouter();
  const [uploading, setUploading] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [collection, setCollection] = useState('');
  const [file, setFile] = useState<File | null>(null);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!file || !title.trim()) return;
    setUploading(true);

    const fileExt = file.name.split('.').pop();
    const filePath = `${Date.now()}-${title.replace(/\s+/g, '-').toLowerCase()}.${fileExt}`;

    const { error: uploadError } = await supabase.storage
      .from('videos')
      .upload(filePath, file);

    if (uploadError) {
      alert('Upload failed: ' + uploadError.message);
      setUploading(false);
      return;
    }

    const { data: urlData } = supabase.storage
      .from('videos')
      .getPublicUrl(filePath);

    const { data } = await supabase
      .from('videos')
      .insert({
        title: title.trim(),
        description: description.trim(),
        collection: collection.trim(),
        video_url: urlData.publicUrl,
      })
      .select()
      .single();

    if (data) {
      router.push(`/videos/${data.id}`);
    }
    setUploading(false);
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm text-gray-400 mb-1">Title *</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full bg-gray-900 rounded px-3 py-2"
          required
        />
      </div>
      <div>
        <label className="block text-sm text-gray-400 mb-1">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          rows={3}
          className="w-full bg-gray-900 rounded px-3 py-2"
        />
      </div>
      <div>
        <label className="block text-sm text-gray-400 mb-1">Collection</label>
        <input
          type="text"
          value={collection}
          onChange={(e) => setCollection(e.target.value)}
          placeholder="e.g. organic-chemistry"
          className="w-full bg-gray-900 rounded px-3 py-2"
        />
      </div>
      <div>
        <label className="block text-sm text-gray-400 mb-1">Video file *</label>
        <input
          type="file"
          accept="video/*"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="text-sm"
          required
        />
      </div>
      <button
        type="submit"
        disabled={uploading}
        className="bg-blue-600 hover:bg-blue-500 px-6 py-2 rounded disabled:opacity-50"
      >
        {uploading ? 'Uploading...' : 'Upload'}
      </button>
    </form>
  );
}
