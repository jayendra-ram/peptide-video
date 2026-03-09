'use client';

import { useState } from 'react';
import { supabase } from '@/lib/supabase';
import type { Comment } from '@/lib/types';

export function CommentSection({
  videoId,
  initialComments,
}: {
  videoId: string;
  initialComments: Comment[];
}) {
  const [comments, setComments] = useState(initialComments);
  const [authorName, setAuthorName] = useState('');
  const [body, setBody] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!body.trim()) return;
    setSubmitting(true);

    const { data } = await supabase
      .from('comments')
      .insert({
        video_id: videoId,
        author_name: authorName.trim() || 'Anonymous',
        body: body.trim(),
      })
      .select()
      .single();

    if (data) {
      setComments([...comments, data]);
      setBody('');
    }
    setSubmitting(false);
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4">
        Comments ({comments.length})
      </h2>

      <div className="space-y-4 mb-8">
        {comments.map((c) => (
          <div key={c.id} className="bg-gray-900 rounded p-4">
            <div className="text-sm text-gray-400 mb-1">
              {c.author_name} &middot;{' '}
              {new Date(c.created_at).toLocaleDateString()}
            </div>
            <p>{c.body}</p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="text"
          placeholder="Your name (optional)"
          value={authorName}
          onChange={(e) => setAuthorName(e.target.value)}
          className="w-full bg-gray-900 rounded px-3 py-2 text-sm"
        />
        <textarea
          placeholder="Write a comment..."
          value={body}
          onChange={(e) => setBody(e.target.value)}
          rows={3}
          className="w-full bg-gray-900 rounded px-3 py-2 text-sm"
          required
        />
        <button
          type="submit"
          disabled={submitting}
          className="bg-blue-600 hover:bg-blue-500 px-4 py-2 rounded text-sm disabled:opacity-50"
        >
          {submitting ? 'Posting...' : 'Post Comment'}
        </button>
      </form>
    </div>
  );
}
