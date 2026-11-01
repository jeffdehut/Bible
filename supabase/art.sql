-- Felt Stories artwork drawn in the studio and shipped to everyone.
-- Everyone (signed in or not) can read it; only the site's artist account can add, change or
-- remove it. The drawings are kept as data (colours and path shapes), never as markup, and the
-- app builds the pictures from them, so nothing written here can run as code in a reader's page.

create table if not exists public.art (
  id          text primary key check (id ~ '^[a-z0-9][a-z0-9-]{1,59}$'),
  kind        text not null check (kind in ('scene', 'person', 'object')),
  cat         text not null check (cat in ('people', 'animals', 'things', 'nature', 'scenes')),
  sub         text not null default '' check (char_length(sub) <= 40),
  name        text not null check (char_length(name) between 1 and 80),
  name_zh     text not null default '' check (char_length(name_zh) <= 40),
  tags        text[] not null default '{}' check (cardinality(tags) <= 40),
  stories     text[] not null default '{}' check (cardinality(stories) <= 20),
  w           int  not null check (w between 50 and 2000),
  h           int  not null check (h between 50 and 2000),
  s           real not null default 1 check (s between 0.05 and 5),
  color       jsonb not null default '[]',   -- the colour layer: [[fill, path], ...]
  line        jsonb not null default '[]',   -- the black lines: [path, ...]
  src         jsonb,                         -- the strokes, to draw on later in the studio
  deleted     boolean not null default false,
  updated_at  timestamptz not null default now(),
  check (pg_column_size(color) + pg_column_size(line) + coalesce(pg_column_size(src), 0) < 3000000)
);

alter table public.art enable row level security;

drop policy if exists art_read on public.art;
create policy art_read on public.art for select to anon, authenticated using (true);

drop policy if exists art_write on public.art;
create policy art_write on public.art for all to authenticated
  using ((select auth.jwt() ->> 'email') = 'jeff@jeffdehut.com')
  with check ((select auth.jwt() ->> 'email') = 'jeff@jeffdehut.com');

grant select on public.art to anon, authenticated;
grant insert, update, delete on public.art to authenticated;
