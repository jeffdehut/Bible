-- Accounts for the Plain English Bible: each reader's highlights and notes, one row per verse,
-- and the reading plan they follow.
--
-- Run this once in the Supabase project's SQL editor (see DEPLOY.md, "Accounts"). It is safe
-- to run again: it replaces the functions and policies and leaves the data alone.
--
-- How sync works (account.js): every change on a device carries the time it was made
-- (updated_at, milliseconds since 1970). push_annotations stores a change only if it is newer
-- than what the account already holds for that verse, so the newest change wins, whichever
-- device sends it first. A highlight and note removed on a device is kept as a row marked
-- deleted, so the other devices remove it too. Devices fetch what changed since they last
-- looked by synced_at, the server's own time of each write.

create table if not exists public.annotations (
  user_id    uuid    not null default auth.uid() references auth.users (id) on delete cascade,
  verse      text    not null check (verse ~ '^[1-3]?[A-Za-z]+\.[0-9]+\.[0-9]+$'),   -- "John.3.16"
  highlight  text,                                   -- a color's name (see below)
  note       text    check (char_length(note) <= 20000),
  updated_at bigint  not null,                       -- when the device made the change
  deleted    boolean not null default false,         -- removed on a device
  synced_at  timestamptz not null default clock_timestamp(),   -- when the server took it in
  primary key (user_id, verse)
);
create index if not exists annotations_synced on public.annotations (user_id, synced_at);
-- Highlights on part of a verse: [[start, end, color], ...], counting the characters of the
-- verse's words as the reader shows them. Added October 2026; safe to run on an older table.
alter table public.annotations add column if not exists ranges jsonb
  check (ranges is null or (jsonb_typeof(ranges) = 'array' and jsonb_array_length(ranges) <= 200));
-- A bookmark on the verse: {"e": "John.3.18"} for a passage to that verse, {} for the verse
-- alone. Added October 2026; safe to run on an older table.
alter table public.annotations add column if not exists bookmark jsonb
  check (bookmark is null or (jsonb_typeof(bookmark) = 'object' and pg_column_size(bookmark) <= 400));

-- The whole-verse highlight: a color's name, from those the reader has offered (the rainbow
-- since November 2026, and the earlier pink, teal and gray). Safe to run on an older table.
alter table public.annotations drop constraint if exists annotations_highlight_check;
alter table public.annotations add constraint annotations_highlight_check
  check (highlight in ('red', 'orange', 'yellow', 'green', 'blue', 'purple', 'violet', 'pink', 'teal', 'gray'));

-- Each person sees and changes only their own rows.
alter table public.annotations enable row level security;
drop policy if exists "Read own annotations" on public.annotations;
drop policy if exists "Add own annotations" on public.annotations;
drop policy if exists "Change own annotations" on public.annotations;
drop policy if exists "Remove own annotations" on public.annotations;
create policy "Read own annotations" on public.annotations
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Add own annotations" on public.annotations
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Change own annotations" on public.annotations
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "Remove own annotations" on public.annotations
  for delete to authenticated using ((select auth.uid()) = user_id);
revoke all on public.annotations from anon;

-- Store a device's changes, keeping whichever version of each verse is newer. Returns how
-- many were stored. Runs as the signed-in person, so the policies above apply.
create or replace function public.push_annotations(rows jsonb)
returns integer
language sql
security invoker
set search_path = ''
as $$
  with incoming as (
    select distinct on (r.verse) r.verse, r.highlight, r.ranges, r.note, r.bookmark, r.updated_at, coalesce(r.deleted, false) as deleted
    from jsonb_to_recordset(rows) as r(verse text, highlight text, ranges jsonb, note text, bookmark jsonb, updated_at bigint, deleted boolean)
    order by r.verse, r.updated_at desc
  ), written as (
    insert into public.annotations as a (user_id, verse, highlight, ranges, note, bookmark, updated_at, deleted, synced_at)
    select (select auth.uid()), verse, highlight, ranges, note, bookmark, updated_at, deleted, clock_timestamp() from incoming
    on conflict (user_id, verse) do update
      set highlight = excluded.highlight, ranges = excluded.ranges, note = excluded.note, bookmark = excluded.bookmark, updated_at = excluded.updated_at,
          deleted = excluded.deleted, synced_at = clock_timestamp()
      where a.updated_at < excluded.updated_at
    returning 1
  )
  select count(*)::integer from written;
$$;
revoke all on function public.push_annotations(jsonb) from public, anon;
grant execute on function public.push_annotations(jsonb) to authenticated;

-- The reading plan each person follows, one row each: {"id", "start", "done": [days]}, or null
-- when they stopped following one. Added October 2026; safe to run on an older database.
create table if not exists public.plans (
  user_id    uuid   primary key default auth.uid() references auth.users (id) on delete cascade,
  plan       jsonb  check (plan is null or (jsonb_typeof(plan) = 'object' and pg_column_size(plan) <= 8000)),
  updated_at bigint not null,                        -- when the device made the change
  synced_at  timestamptz not null default clock_timestamp()
);
alter table public.plans enable row level security;
drop policy if exists "Read own plan" on public.plans;
drop policy if exists "Add own plan" on public.plans;
drop policy if exists "Change own plan" on public.plans;
create policy "Read own plan" on public.plans
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Add own plan" on public.plans
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Change own plan" on public.plans
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
revoke all on public.plans from anon;

-- Store a device's plan if it is newer than the account's. Returns whether it was stored.
create or replace function public.push_plan(plan jsonb, updated_at bigint)
returns boolean
language sql
security invoker
set search_path = ''
as $$
  with written as (
    insert into public.plans as p (user_id, plan, updated_at, synced_at)
    values ((select auth.uid()), push_plan.plan, push_plan.updated_at, clock_timestamp())
    on conflict (user_id) do update
      set plan = excluded.plan, updated_at = excluded.updated_at, synced_at = clock_timestamp()
      where p.updated_at < excluded.updated_at
    returning 1
  )
  select exists (select 1 from written);
$$;
revoke all on function public.push_plan(jsonb, bigint) from public, anon;
grant execute on function public.push_plan(jsonb, bigint) to authenticated;

-- Other things a reader keeps, one row each by key: "marks", the markings they made themselves
-- ([{id, n: name, s: symbol, c: color, st: style}, ...]). Added November 2026; safe to run again.
create table if not exists public.prefs (
  user_id    uuid   not null default auth.uid() references auth.users (id) on delete cascade,
  key        text   not null check (key ~ '^[a-z][a-z0-9_]{0,31}$'),
  value      jsonb  check (value is null or pg_column_size(value) <= 32000),
  updated_at bigint not null,                        -- when the device made the change
  synced_at  timestamptz not null default clock_timestamp(),
  primary key (user_id, key)
);
alter table public.prefs enable row level security;
drop policy if exists "Read own prefs" on public.prefs;
drop policy if exists "Add own prefs" on public.prefs;
drop policy if exists "Change own prefs" on public.prefs;
create policy "Read own prefs" on public.prefs
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Add own prefs" on public.prefs
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Change own prefs" on public.prefs
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
revoke all on public.prefs from anon;

-- Store one of a device's keys if it is newer than the account's. Returns whether it was stored.
create or replace function public.push_pref(key text, value jsonb, updated_at bigint)
returns boolean
language sql
security invoker
set search_path = ''
as $$
  with written as (
    insert into public.prefs as p (user_id, key, value, updated_at, synced_at)
    values ((select auth.uid()), push_pref.key, push_pref.value, push_pref.updated_at, clock_timestamp())
    on conflict (user_id, key) do update
      set value = excluded.value, updated_at = excluded.updated_at, synced_at = clock_timestamp()
      where p.updated_at < excluded.updated_at
    returning 1
  )
  select exists (select 1 from written);
$$;
revoke all on function public.push_pref(text, jsonb, bigint) from public, anon;
grant execute on function public.push_pref(text, jsonb, bigint) to authenticated;

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

-- Delete the signed-in person's account, and with it all their highlights, notes and plan.
create or replace function public.delete_account()
returns void
language sql
security definer
set search_path = ''
as $$
  delete from auth.users where id = (select auth.uid());
$$;
revoke all on function public.delete_account() from public, anon;
grant execute on function public.delete_account() to authenticated;

