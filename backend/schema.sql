-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- Create Posts table
create table public.posts (
  id uuid not null default uuid_generate_v4() primary key,
  title text not null,
  description text,
  content text,
  category text not null,
  type text not null, -- 'video', 'article', 'thread'
  platform text,
  image_url text,
  video_id text,
  thread_url text,
  tweet_text text, -- Auto-generated tweet content
  tweet_posted_at timestamptz, -- When it was posted to X
  created_at timestamptz default now()
);

-- Enable Row Level Security (RLS)
alter table public.posts enable row level security;

-- Create Policy: Allow public read access (Anyone can view posts)
create policy "Allow public read access"
  on public.posts for select
  using (true);

-- Create Policy: Allow backend write access
-- (In Supabase, the 'service_role' key bypasses RLS, but for good measure or if we use authenticated users later)
-- For now, we rely on the Service Role Key for writing, which bypasses RLS.
-- But if we wanted to allow anon inserts (NOT RECOMMENDED without checks), we would add a policy here.
-- We will stick to Service Role Key for the python script.

-- Create index for faster sorting by date
create index posts_created_at_idx on public.posts (created_at desc);

-- Grant usage to anon and service_role
grant select on public.posts to anon;
grant select, insert, update, delete on public.posts to service_role;
