-- Funded Tape news site (site/): sources, collected items, picks, newsletter editions.
--
-- Lives in the blackout-clock Supabase project (ref fqgryxjuecjgelcjdvmq) in its
-- own schema `funded_tape`, so it never touches blackout-clock's tables. The
-- schema is NOT exposed through the Data API; the site and the bot API reach it
-- only through the public.ft_* functions below, which are granted to
-- service_role only (the key lives in Vercel env, never in the browser).
--
-- Apply: supabase db query --linked -f supabase/migrations/20261125000000_funded_tape_site.sql
--        (run from ~/@Pomo651/blackout-clock, which is linked to the project).
-- Not part of blackout-clock's migration history.

create schema if not exists funded_tape;
revoke all on schema funded_tape from public, anon, authenticated;

-- Everything a watcher bot looks at (a firm's X account, a help center, a news site...).
create table if not exists funded_tape.sources (
  id          bigint generated always as identity primary key,
  name        text not null,
  kind        text not null check (kind in ('official','x','press','community','youtube','review','other')),
  url         text not null unique,
  active      boolean not null default true,
  created_at  timestamptz not null default now()
);

-- One collected item = one post/article/rule change a watcher saw.
-- status: new (collected) -> picked (made the cut) | rejected.
create table if not exists funded_tape.items (
  id            bigint generated always as identity primary key,
  url           text not null unique,
  title         text not null,
  summary       text,
  source_name   text not null,
  source_url    text references funded_tape.sources(url) on update cascade on delete set null,
  firm          text,
  collected_by  text,                       -- Feed / Pulse / KFC ...
  collected_at  timestamptz not null default now(),
  status        text not null default 'new' check (status in ('new','picked','rejected')),
  picked_at     timestamptz
);
create index if not exists items_collected_at_idx on funded_tape.items (collected_at desc);
create index if not exists items_picked_at_idx on funded_tape.items (picked_at desc) where status = 'picked';

-- One newsletter issue. sections = [{headline, body, why, sources:[url]}].
-- Only status 'published' is shown on the public site; 'draft' needs the preview key.
create table if not exists funded_tape.editions (
  id            bigint generated always as identity primary key,
  edition_date  date not null unique,
  subject       text not null,
  preview       text,
  intro         text,
  outro         text,
  sections      jsonb not null default '[]'::jsonb,
  status        text not null default 'draft' check (status in ('draft','published')),
  published_at  timestamptz,
  updated_at    timestamptz not null default now()
);

alter table funded_tape.sources  enable row level security;
alter table funded_tape.items    enable row level security;
alter table funded_tape.editions enable row level security;

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
                         select id, title, source_name as source, url, firm, picked_at
                           from items where status = 'picked'
                          order by picked_at desc limit 8) p),
    'at',             now()
  );
$$;

create or replace function public.ft_editions(include_drafts boolean default false) returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select coalesce(jsonb_agg(e order by e.edition_date desc), '[]'::jsonb) from (
    select edition_date, subject, preview, status, published_at,
           jsonb_array_length(sections) as section_count,
           (select coalesce(jsonb_agg(s->>'headline'), '[]'::jsonb) from jsonb_array_elements(sections) s) as headlines
      from editions
     where status = 'published' or include_drafts) e;
$$;

create or replace function public.ft_edition(d date, include_drafts boolean default false) returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select to_jsonb(e) - 'id' from editions e
   where edition_date = d and (status = 'published' or include_drafts);
$$;

-- ---------- write (bot API) ----------

-- rows: [{name, kind, url, active?}]
create or replace function public.ft_upsert_sources(rows jsonb) returns int
language plpgsql security definer set search_path = funded_tape, public as $$
declare n int;
begin
  insert into sources (name, kind, url, active)
  select r->>'name', coalesce(r->>'kind','other'), r->>'url', coalesce((r->>'active')::boolean, true)
    from jsonb_array_elements(rows) r
  on conflict (url) do update set name = excluded.name, kind = excluded.kind, active = excluded.active;
  get diagnostics n = row_count;
  return n;
end $$;

-- rows: [{url, title, summary?, source_name, source_url?, firm?, collected_by?, collected_at?, status?}]
-- Re-sending a url updates it; setting status 'picked' stamps picked_at once.
create or replace function public.ft_upsert_items(rows jsonb) returns int
language plpgsql security definer set search_path = funded_tape, public as $$
declare n int;
begin
  insert into items (url, title, summary, source_name, source_url, firm, collected_by, collected_at, status, picked_at)
  select r->>'url', r->>'title', r->>'summary', r->>'source_name',
         (select s.url from sources s where s.url = r->>'source_url'),
         r->>'firm', r->>'collected_by',
         coalesce((r->>'collected_at')::timestamptz, now()),
         coalesce(r->>'status','new'),
         case when r->>'status' = 'picked' then coalesce((r->>'picked_at')::timestamptz, now()) end
    from jsonb_array_elements(rows) r
  on conflict (url) do update set
    title        = excluded.title,
    summary      = coalesce(excluded.summary, items.summary),
    source_name  = excluded.source_name,
    source_url   = coalesce(excluded.source_url, items.source_url),
    firm         = coalesce(excluded.firm, items.firm),
    collected_by = coalesce(excluded.collected_by, items.collected_by),
    status       = excluded.status,
    picked_at    = case when excluded.status = 'picked' then coalesce(items.picked_at, excluded.picked_at) end;
  get diagnostics n = row_count;
  return n;
end $$;

-- e: {edition_date, subject, preview?, intro?, outro?, sections:[...], status?}
create or replace function public.ft_upsert_edition(e jsonb) returns jsonb
language plpgsql security definer set search_path = funded_tape, public as $$
declare r editions;
begin
  insert into editions (edition_date, subject, preview, intro, outro, sections, status, published_at, updated_at)
  values ((e->>'edition_date')::date, e->>'subject', e->>'preview', e->>'intro', e->>'outro',
          coalesce(e->'sections','[]'::jsonb), coalesce(e->>'status','draft'),
          case when e->>'status' = 'published' then now() end, now())
  on conflict (edition_date) do update set
    subject = excluded.subject, preview = excluded.preview, intro = excluded.intro, outro = excluded.outro,
    sections = excluded.sections, status = excluded.status,
    published_at = case when excluded.status = 'published' then coalesce(editions.published_at, now()) end,
    updated_at = now()
  returning * into r;
  return jsonb_build_object('edition_date', r.edition_date, 'status', r.status);
end $$;

revoke all on function public.ft_stats(), public.ft_editions(boolean), public.ft_edition(date, boolean),
  public.ft_upsert_sources(jsonb), public.ft_upsert_items(jsonb), public.ft_upsert_edition(jsonb)
  from public, anon, authenticated;
grant execute on function public.ft_stats(), public.ft_editions(boolean), public.ft_edition(date, boolean),
  public.ft_upsert_sources(jsonb), public.ft_upsert_items(jsonb), public.ft_upsert_edition(jsonb)
  to service_role;
