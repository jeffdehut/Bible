-- Accounts for the Plain English Bible: each reader's highlights and notes, one row per verse.
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
  highlight  text    check (highlight in ('yellow', 'green', 'blue', 'pink', 'orange')),
  note       text    check (char_length(note) <= 20000),
  updated_at bigint  not null,                       -- when the device made the change
  deleted    boolean not null default false,         -- removed on a device
  synced_at  timestamptz not null default clock_timestamp(),   -- when the server took it in
  primary key (user_id, verse)
);
create index if not exists annotations_synced on public.annotations (user_id, synced_at);

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
    select distinct on (r.verse) r.verse, r.highlight, r.note, r.updated_at, coalesce(r.deleted, false) as deleted
    from jsonb_to_recordset(rows) as r(verse text, highlight text, note text, updated_at bigint, deleted boolean)
    order by r.verse, r.updated_at desc
  ), written as (
    insert into public.annotations as a (user_id, verse, highlight, note, updated_at, deleted, synced_at)
    select (select auth.uid()), verse, highlight, note, updated_at, deleted, clock_timestamp() from incoming
    on conflict (user_id, verse) do update
      set highlight = excluded.highlight, note = excluded.note, updated_at = excluded.updated_at,
          deleted = excluded.deleted, synced_at = clock_timestamp()
      where a.updated_at < excluded.updated_at
    returning 1
  )
  select count(*)::integer from written;
$$;
revoke all on function public.push_annotations(jsonb) from public, anon;
grant execute on function public.push_annotations(jsonb) to authenticated;

-- Delete the signed-in person's account, and with it all their highlights and notes.
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

