-- =============================================================
-- VIDEOS TABLE
-- =============================================================
create table public.videos (
  id              uuid primary key default gen_random_uuid(),
  title           text not null,
  description     text default '',
  collection      text default '',
  video_url       text not null,
  thumbnail_url   text default '',
  duration_seconds integer default 0,
  created_at      timestamptz default now()
);

alter table public.videos enable row level security;

create policy "public read videos"
  on public.videos for select
  using (true);

create policy "public insert videos"
  on public.videos for insert
  with check (true);

-- =============================================================
-- COMMENTS TABLE
-- =============================================================
create table public.comments (
  id          uuid primary key default gen_random_uuid(),
  video_id    uuid not null references public.videos(id) on delete cascade,
  author_name text not null default 'Anonymous',
  body        text not null,
  created_at  timestamptz default now()
);

create index idx_comments_video_id on public.comments(video_id);

alter table public.comments enable row level security;

create policy "public read comments"
  on public.comments for select
  using (true);

create policy "public insert comments"
  on public.comments for insert
  with check (true);

-- =============================================================
-- STORAGE BUCKET
-- =============================================================
insert into storage.buckets (id, name, public)
values ('videos', 'videos', true);

create policy "public upload videos"
  on storage.objects for insert
  with check (bucket_id = 'videos');

create policy "public read videos bucket"
  on storage.objects for select
  using (bucket_id = 'videos');
