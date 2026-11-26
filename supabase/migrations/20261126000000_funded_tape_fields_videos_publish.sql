-- Funded Tape site, step 2 (Nov 26, 2026):
--   1. items: the fields FT-grok proposed in plan/DATA_FORMAT.md
--      (category, source_published_at, evidence, evidence_url, notes)
--   2. videos: one daily Short per edition
--   3. owner actions: publish / unpublish an edition, approve a Short
--   4. bot edition writes are always drafts and can no longer touch a published edition
--
-- Apply: supabase db query --linked -f supabase/migrations/20261126000000_funded_tape_fields_videos_publish.sql
--        (run from ~/@Pomo651/blackout-clock). Safe to re-run.

alter table funded_tape.items
  add column if not exists category            text check (category in ('rule_change','launch','payout','pricing','promo','allegation')),
  add column if not exists source_published_at timestamptz,
  add column if not exists evidence            text check (evidence in ('official','firm_x_post','community')),
  add column if not exists evidence_url        text,
  add column if not exists notes               text;

-- status: draft (built by FT-video) -> approved (owner OK'd upload) -> uploaded (video_url is the public one)
create table if not exists funded_tape.videos (
  id            bigint generated always as identity primary key,
  edition_date  date not null unique references funded_tape.editions(edition_date) on update cascade on delete cascade,
  video_url     text,
  title         text,
  status        text not null default 'draft' check (status in ('draft','approved','uploaded')),
  approved_at   timestamptz,
  updated_at    timestamptz not null default now()
);
alter table funded_tape.videos enable row level security;

-- ---------- read ----------

create or replace function public.ft_stats() returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select jsonb_build_object(
    'sources',        (select count(*) from sources where active),
    'sourceKinds',    (select coalesce(jsonb_object_agg(kind, n), '{}'::jsonb)
                         from (select kind, count(*) n from sources where active group by kind) k),
    'items',          (select count(*) from items),
    'items24h',       (select count(*) from items where collected_at > now() - interval '24 hours'),
    'picks',          (select count(*) from items where status = 'picked'),
    'picks24h',       (select count(*) from items where status = 'picked' and picked_at > now() - interval '24 hours'),
    'editions',       (select count(*) from editions where status = 'published'),
    'latestEdition',  (select max(edition_date) from editions where status = 'published'),
    'latest',         (select coalesce(jsonb_agg(p order by p.picked_at desc), '[]'::jsonb) from (
                         select id, title, source_name as source, url, firm, category, picked_at
                           from items where status = 'picked'
                          order by picked_at desc limit 8) p),
    'at',             now()
  );
$$;

-- edition + its Short. The Short is included only once approved, unless drafts are requested.
create or replace function public.ft_edition(d date, include_drafts boolean default false) returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select (to_jsonb(e) - 'id') || jsonb_build_object('video',
           (select to_jsonb(v) - 'id' - 'edition_date' from videos v
             where v.edition_date = e.edition_date and (v.status <> 'draft' or include_drafts)))
    from editions e
   where edition_date = d and (status = 'published' or include_drafts);
$$;

-- ---------- write (bot API) ----------

create or replace function public.ft_upsert_items(rows jsonb) returns int
language plpgsql security definer set search_path = funded_tape, public as $$
declare n int;
begin
  insert into items (url, title, summary, source_name, source_url, firm, collected_by, collected_at, status, picked_at,
                     category, source_published_at, evidence, evidence_url, notes)
  select r->>'url', r->>'title', r->>'summary', r->>'source_name',
         (select s.url from sources s where s.url = r->>'source_url'),
         r->>'firm', r->>'collected_by',
         coalesce((r->>'collected_at')::timestamptz, now()),
         coalesce(r->>'status','new'),
         case when r->>'status' = 'picked' then coalesce((r->>'picked_at')::timestamptz, now()) end,
         r->>'category', (r->>'source_published_at')::timestamptz, r->>'evidence', r->>'evidence_url', r->>'notes'
    from jsonb_array_elements(rows) r
  on conflict (url) do update set
    title               = excluded.title,
    summary             = coalesce(excluded.summary, items.summary),
    source_name         = excluded.source_name,
    source_url          = coalesce(excluded.source_url, items.source_url),
    firm                = coalesce(excluded.firm, items.firm),
    collected_by        = coalesce(excluded.collected_by, items.collected_by),
    status              = excluded.status,
    picked_at           = case when excluded.status = 'picked' then coalesce(items.picked_at, excluded.picked_at) end,
    category            = coalesce(excluded.category, items.category),
    source_published_at = coalesce(excluded.source_published_at, items.source_published_at),
    evidence            = coalesce(excluded.evidence, items.evidence),
    evidence_url        = coalesce(excluded.evidence_url, items.evidence_url),
    notes               = coalesce(excluded.notes, items.notes);
  get diagnostics n = row_count;
  return n;
end $$;

-- Bots: always saved as draft (any "status" sent is ignored). A published edition
-- is locked; the owner must unpublish it before a bot can change it.
create or replace function public.ft_upsert_edition(e jsonb) returns jsonb
language plpgsql security definer set search_path = funded_tape, public as $$
declare r editions;
begin
  if exists (select 1 from editions where edition_date = (e->>'edition_date')::date and status = 'published') then
    raise exception 'edition % is already published; ask pomo651 to unpublish it first', e->>'edition_date';
  end if;
  insert into editions (edition_date, subject, preview, intro, outro, sections, status, updated_at)
  values ((e->>'edition_date')::date, e->>'subject', e->>'preview', e->>'intro', e->>'outro',
          coalesce(e->'sections','[]'::jsonb), 'draft', now())
  on conflict (edition_date) do update set
    subject = excluded.subject, preview = excluded.preview, intro = excluded.intro, outro = excluded.outro,
    sections = excluded.sections, updated_at = now()
  returning * into r;
  return jsonb_build_object('edition_date', r.edition_date, 'status', r.status);
end $$;

-- Bots: {edition_date, video_url?, title?}. Always saved as draft; an approved/uploaded Short is locked.
create or replace function public.ft_upsert_video(v jsonb) returns jsonb
language plpgsql security definer set search_path = funded_tape, public as $$
declare r videos;
begin
  if exists (select 1 from videos where edition_date = (v->>'edition_date')::date and status <> 'draft') then
    raise exception 'the Short for % is already approved; ask pomo651 first', v->>'edition_date';
  end if;
  insert into videos (edition_date, video_url, title, status, updated_at)
  values ((v->>'edition_date')::date, v->>'video_url', v->>'title', 'draft', now())
  on conflict (edition_date) do update set
    video_url = coalesce(excluded.video_url, videos.video_url),
    title = coalesce(excluded.title, videos.title),
    updated_at = now()
  returning * into r;
  return jsonb_build_object('edition_date', r.edition_date, 'status', r.status);
end $$;

-- ---------- owner actions (site /api/owner, OWNER_KEY) ----------

-- action: publish | unpublish | approve_video | unapprove_video | mark_uploaded (+ video_url)
create or replace function public.ft_owner_action(d date, action text, video_url text default null) returns jsonb
language plpgsql security definer set search_path = funded_tape, public as $$
begin
  if action = 'publish' then
    update editions set status = 'published', published_at = coalesce(published_at, now()), updated_at = now()
     where edition_date = d;
  elsif action = 'unpublish' then
    update editions set status = 'draft', published_at = null, updated_at = now() where edition_date = d;
  elsif action = 'approve_video' then
    update videos set status = 'approved', approved_at = now(), updated_at = now() where edition_date = d;
  elsif action = 'unapprove_video' then
    update videos set status = 'draft', approved_at = null, updated_at = now() where edition_date = d;
  elsif action = 'mark_uploaded' then
    update videos set status = 'uploaded', approved_at = coalesce(approved_at, now()),
                      video_url = coalesce(ft_owner_action.video_url, videos.video_url), updated_at = now()
     where edition_date = d;
  else
    raise exception 'unknown action %', action;
  end if;
  if not found then raise exception 'nothing to % for %', action, d; end if;
  return public.ft_edition(d, true);
end $$;

revoke all on function public.ft_upsert_video(jsonb), public.ft_owner_action(date, text, text) from public, anon, authenticated;
grant execute on function public.ft_upsert_video(jsonb), public.ft_owner_action(date, text, text) to service_role;
-- re-created functions keep their grants, but re-assert them so this file stands alone
revoke all on function public.ft_stats(), public.ft_edition(date, boolean), public.ft_upsert_items(jsonb),
  public.ft_upsert_edition(jsonb) from public, anon, authenticated;
grant execute on function public.ft_stats(), public.ft_edition(date, boolean), public.ft_upsert_items(jsonb),
  public.ft_upsert_edition(jsonb) to service_role;

notify pgrst, 'reload schema';
