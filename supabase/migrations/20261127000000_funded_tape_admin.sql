-- Funded Tape site, step 4 (Nov 27, 2026): read-only snapshot for the /admin pages.
--
-- One call returns everything the admin shows: items (newest 500, every status),
-- sources with their item counts, editions with their Short and latest auto-review,
-- and the auto-publish log. It only READS. Nothing is written or changed.
-- Granted to service_role only, like every other ft_* function.
--
-- Until this is applied, /admin still works in "partial" mode from ft_stats /
-- ft_editions / ft_edition (no item list, no source list).
--
-- Apply: supabase db query --linked -f supabase/migrations/20261127000000_funded_tape_admin.sql
--        (run from ~/@Pomo651/blackout-clock). Safe to re-run.

create or replace function public.ft_admin_snapshot(recent_days int default 14) returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select jsonb_build_object(
    'at', now(),
    'totals', jsonb_build_object(
      'items',    (select count(*) from items),
      'new',      (select count(*) from items where status = 'new'),
      'picked',   (select count(*) from items where status = 'picked'),
      'rejected', (select count(*) from items where status = 'rejected')),
    'items', (select coalesce(jsonb_agg(to_jsonb(i) order by i.collected_at desc), '[]'::jsonb) from (
        select id, url, title, summary, source_name, source_url, firm, collected_by, collected_at,
               status, picked_at, category, source_published_at, evidence, evidence_url, notes
          from items order by collected_at desc limit 500) i),
    'sources', (select coalesce(jsonb_agg(to_jsonb(s) order by s.kind, s.name), '[]'::jsonb) from (
        select s.id, s.name, s.kind, s.url, s.active, s.created_at,
               (select count(*) from items i where i.source_url = s.url) as items_total,
               (select count(*) from items i where i.source_url = s.url
                   and i.collected_at > now() - recent_days * interval '1 day') as items_recent,
               (select count(*) from items i where i.source_url = s.url and i.status = 'picked') as picks_total,
               (select max(i.collected_at) from items i where i.source_url = s.url) as last_item_at
          from sources s) s),
    'editions', (select coalesce(jsonb_agg(to_jsonb(e) order by e.edition_date desc), '[]'::jsonb) from (
        select e.edition_date, e.subject, e.status, e.published_at, e.updated_at,
               jsonb_array_length(e.sections) as section_count,
               (select jsonb_build_object('status', v.status, 'video_url', v.video_url, 'title', v.title,
                                          'approved_at', v.approved_at, 'updated_at', v.updated_at)
                  from videos v where v.edition_date = e.edition_date) as video,
               (select jsonb_build_object('result', l.result, 'reasons', l.reasons, 'ran_at', l.ran_at)
                  from publish_log l where l.edition_date = e.edition_date
                 order by l.ran_at desc limit 1) as review
          from editions e order by e.edition_date desc limit 60) e),
    'log', (select coalesce(jsonb_agg(to_jsonb(l) order by l.ran_at desc), '[]'::jsonb) from (
        select edition_date, ran_at, result, reasons from publish_log order by ran_at desc limit 30) l)
  );
$$;

revoke all on function public.ft_admin_snapshot(int) from public, anon, authenticated;
grant execute on function public.ft_admin_snapshot(int) to service_role;

notify pgrst, 'reload schema';
