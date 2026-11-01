-- Felt Stories: saved boards, synced with the account. Paste all of this into the Supabase
-- SQL Editor (Plain Bible project → SQL Editor → New query) and click Run. Safe to run again.

-- Story Board scenes (storyboard.html), one row per board: its name, the folder it is kept in,
-- and the scene itself ({bg, items: [{k, a, x, y, s, r, f}]}). As with the notes, the newer
-- change wins and a board removed on a device is kept as a row marked deleted. The folder list
-- itself is the "board_folders" pref. Added November 2026; safe to run again.
create table if not exists public.boards (
  user_id    uuid    not null default auth.uid() references auth.users (id) on delete cascade,
  id         text    not null check (id ~ '^[A-Za-z0-9_-]{6,40}$'),
  name       text    not null default '' check (char_length(name) <= 120),
  folder     text    not null default '' check (char_length(folder) <= 80),
  data       jsonb   check (data is null or (jsonb_typeof(data) = 'object' and pg_column_size(data) <= 200000)),
  updated_at bigint  not null,
  deleted    boolean not null default false,
  synced_at  timestamptz not null default clock_timestamp(),
  primary key (user_id, id)
);
create index if not exists boards_synced on public.boards (user_id, synced_at);
alter table public.boards enable row level security;
drop policy if exists "Read own boards" on public.boards;
drop policy if exists "Add own boards" on public.boards;
drop policy if exists "Change own boards" on public.boards;
create policy "Read own boards" on public.boards
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Add own boards" on public.boards
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Change own boards" on public.boards
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
revoke all on public.boards from anon;

-- Store a board if it is newer than the account's copy. Returns whether it was stored.
create or replace function public.push_board(id text, name text, folder text, data jsonb, updated_at bigint, deleted boolean)
returns boolean
language sql
security invoker
set search_path = ''
as $$
  with written as (
    insert into public.boards as b (user_id, id, name, folder, data, updated_at, deleted, synced_at)
    values ((select auth.uid()), push_board.id, push_board.name, push_board.folder,
            case when push_board.deleted then null else push_board.data end,
            push_board.updated_at, push_board.deleted, clock_timestamp())
    on conflict (user_id, id) do update
      set name = excluded.name, folder = excluded.folder, data = excluded.data,
          updated_at = excluded.updated_at, deleted = excluded.deleted, synced_at = clock_timestamp()
      where b.updated_at < excluded.updated_at
    returning 1
  )
  select exists (select 1 from written);
$$;
revoke all on function public.push_board(text, text, text, jsonb, bigint, boolean) from public, anon;
grant execute on function public.push_board(text, text, text, jsonb, bigint, boolean) to authenticated;
