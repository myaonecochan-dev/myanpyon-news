-- Create Comments table
create table public.comments (
  id uuid not null default uuid_generate_v4() primary key,
  post_id uuid not null references public.posts(id) on delete cascade,
  author_name text not null,
  content text not null,
  created_at timestamptz default now()
);

-- Enable Row Level Security (RLS)
alter table public.comments enable row level security;

-- Create Policy: Allow public read access
create policy "Allow public read comments"
  on public.comments for select
  using (true);

-- Create Policy: Allow anon insert (Anyone can comment)
create policy "Allow anon insert comments"
  on public.comments for insert
  with check (true);

-- Create index for faster sorting
create index comments_post_id_idx on public.comments (post_id);
create index comments_created_at_idx on public.comments (created_at desc);

-- Grant privileges
grant select, insert on public.comments to anon;
grant select, insert, update, delete on public.comments to service_role;
