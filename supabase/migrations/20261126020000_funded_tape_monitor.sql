-- Funded Tape site, step 5 (Nov 26, 2026): daily pipeline monitor + alerts.
--
-- ft_monitor(days) grades every step of every day (New York dates, newest first).
-- The /admin/monitor page and the alert job (/api/jobs/monitor) both read it, so
-- the page and the emails always agree. Alerts already sent are kept in
-- funded_tape.monitor_alerts so each problem is emailed once per day.
--
-- Step states: ok (green) · late (amber, arrived after its due time) ·
--              needs (amber, waiting on pomo651) · fail (red, missing) ·
--              wait (grey, not due yet) · off (grey, step not running yet)
--
-- Apply: supabase db query --linked -f supabase/migrations/20261126020000_funded_tape_monitor.sql
--        (run from ~/@Pomo651/blackout-clock). Substitute <FT_JOB_SECRET> for the cron jobs;
--        never commit the value.

-- when a draft / Short was FIRST posted (updated_at moves on every re-send)
alter table funded_tape.editions add column if not exists created_at timestamptz;
update funded_tape.editions set created_at = updated_at where created_at is null;
alter table funded_tape.editions alter column created_at set default now();
alter table funded_tape.videos add column if not exists created_at timestamptz;
update funded_tape.videos set created_at = updated_at where created_at is null;
alter table funded_tape.videos alter column created_at set default now();

create table if not exists funded_tape.monitor_alerts (
  id            bigint generated always as identity primary key,
  edition_date  date not null,
  step          text not null,
  state         text not null,
  detail        text,
  sent_at       timestamptz not null default now(),
  unique (edition_date, step, state)
);
alter table funded_tape.monitor_alerts enable row level security;

create or replace function public.ft_monitor(days int default 14) returns jsonb
language plpgsql stable security definer set search_path = funded_tape, public as $$
declare
  out jsonb := '[]'::jsonb;
  d date;
  today date := (now() at time zone 'America/New_York')::date;
  ny text := 'America/New_York';
  w0 timestamptz; sweep timestamptz; picks_due timestamptz; draft_due timestamptz;
  review_due timestamptz; short_due timestamptz;
  n_items int; n_pick int; n_pick_late int;
  e editions; v videos; lg publish_log;
  shorts_on boolean := exists (select 1 from videos);
  steps jsonb; st text; det text; worst text;
begin
  for k in 0 .. days - 1 loop
    d := today - k;
    if d < date '2026-11-26' then  -- first live edition (7 days a week from here)
      out := out || jsonb_build_object('date', d, 'state', 'off', 'steps', '[]'::jsonb);
      continue;
    end if;
    w0         := ((d - 1)::timestamp + time '06:00') at time zone ny;
    sweep      := (d::timestamp + time '06:00') at time zone ny;
    picks_due  := (d::timestamp + time '06:45') at time zone ny;
    draft_due  := (d::timestamp + time '07:15') at time zone ny;
    review_due := (d::timestamp + time '07:45') at time zone ny;
    short_due  := (d::timestamp + time '08:45') at time zone ny;
    steps := '[]'::jsonb;

    -- 1 collect
    select count(*) into n_items from items where collected_at >= w0 and collected_at < sweep;
    st := case when n_items > 0 and now() >= sweep then 'ok'
               when now() < sweep then 'wait' else 'fail' end;
    steps := steps || jsonb_build_object('key','collect','title','Collect items','who','FT-sources · FT-community',
      'due','6:00 AM','state',st,'detail', format('%s item%s in the window', n_items, case when n_items = 1 then '' else 's' end));

    -- 2 picks
    select count(*) filter (where picked_at <= picks_due), count(*) filter (where picked_at > picks_due and picked_at <= review_due)
      into n_pick, n_pick_late
      from items where status = 'picked' and picked_at >= w0 and picked_at <= review_due;
    st := case when n_pick > 0 then 'ok' when n_pick_late > 0 then 'late'
               when now() < picks_due then 'wait' else 'fail' end;
    steps := steps || jsonb_build_object('key','picks','title','Fact-check + picks','who','FT-PM',
      'due','6:45 AM','state',st,'detail', format('%s on time · %s late', n_pick, n_pick_late));

    -- 3 draft
    select * into e from editions where edition_date = d;
    st := case when e.edition_date is null then (case when now() < draft_due then 'wait' else 'fail' end)
               when e.created_at <= draft_due then 'ok' else 'late' end;
    det := case when e.edition_date is null then 'No draft'
                else format('Posted %s ET · %s sections', to_char(e.created_at at time zone ny, 'FMHH12:MI AM'), jsonb_array_length(e.sections)) end;
    steps := steps || jsonb_build_object('key','draft','title','Post draft','who','FT-editor','due','7:15 AM','state',st,'detail',det);

    -- 4 auto-review / publish
    select * into lg from publish_log where edition_date = d order by ran_at desc limit 1;
    st := case when e.status = 'published' then 'ok'
               when lg.result = 'held' then 'fail'
               when now() < review_due + interval '10 minutes' then 'wait' else 'fail' end;
    det := case when e.status = 'published' then format('Published %s ET', to_char(e.published_at at time zone ny, 'FMHH12:MI AM'))
                when lg.result = 'held' then 'Held: ' || coalesce(lg.reasons->>0, '?')
                when now() < review_due + interval '10 minutes' then 'Runs at 7:45 AM'
                else 'Did not publish' end;
    steps := steps || jsonb_build_object('key','publish','title','Auto-review + publish','who','Auto-review','due','7:45 AM','state',st,'detail',det);

    -- 5 Short built, 6 Short approved (off until FT-video posts its first Short)
    select * into v from videos where edition_date = d;
    if not shorts_on then
      steps := steps || jsonb_build_object('key','short','title','Build Short','who','FT-video','due','8:45 AM','state','off','detail','Not started yet (FT-grok waits for pomo651)')
                     || jsonb_build_object('key','approve','title','Approve Short','who','pomo651','due','after 8:00','state','off','detail','—');
    else
      st := case when v.edition_date is null then (case when now() < short_due then 'wait' else 'fail' end)
                 when v.created_at <= short_due then 'ok' else 'late' end;
      steps := steps || jsonb_build_object('key','short','title','Build Short','who','FT-video','due','8:45 AM','state',st,
        'detail', case when v.edition_date is null then 'No Short' else format('Posted %s ET', to_char(v.created_at at time zone ny, 'FMHH12:MI AM')) end);
      st := case when v.edition_date is null then (case when now() < short_due then 'wait' else 'fail' end)
                 when v.status in ('approved','uploaded') then 'ok' else 'needs' end;
      steps := steps || jsonb_build_object('key','approve','title','Approve Short','who','pomo651','due','after 8:00','state',st,
        'detail', coalesce(v.status, 'No Short'));
    end if;

    select case when bool_or(x->>'state' = 'fail') then 'fail'
                when bool_or(x->>'state' in ('late','needs')) then 'late'
                when bool_or(x->>'state' = 'wait') then 'wait' else 'ok' end
      into worst from jsonb_array_elements(steps) x;
    out := out || jsonb_build_object('date', d, 'state', worst, 'steps', steps);
  end loop;
  return jsonb_build_object('at', now(), 'days', out,
    'alerts', (select coalesce(jsonb_agg(to_jsonb(a) - 'id' order by a.sent_at desc), '[]'::jsonb)
                 from (select * from monitor_alerts order by sent_at desc limit 30) a));
end $$;

-- Records alerts; returns only the ones not sent before (so each is emailed once).
-- rows: [{edition_date, step, state, detail}]
create or replace function public.ft_monitor_record(rows jsonb) returns jsonb
language sql security definer set search_path = funded_tape, public as $$
  with ins as (
    insert into monitor_alerts (edition_date, step, state, detail)
    select (r->>'edition_date')::date, r->>'step', r->>'state', r->>'detail' from jsonb_array_elements(rows) r
    on conflict (edition_date, step, state) do nothing
    returning edition_date, step, state, detail)
  select coalesce(jsonb_agg(to_jsonb(ins)), '[]'::jsonb) from ins;
$$;

revoke all on function public.ft_monitor(int), public.ft_monitor_record(jsonb) from public, anon, authenticated;
grant execute on function public.ft_monitor(int), public.ft_monitor_record(jsonb) to service_role;

-- Checkpoints: 7:20 AM ET (collect/picks/draft, before the 7:45 publish) and 8:55 AM ET (everything).
-- Each fires in both UTC hours; the route acts only at the right New York time (DST-safe).
select cron.schedule('funded-tape-monitor-early', '20 11,12 * * *', $cron$
  select net.http_post(url := 'https://prop-firm-newsletter.vercel.app/api/jobs/monitor',
    headers := jsonb_build_object('content-type','application/json','x-job-secret','<FT_JOB_SECRET>'),
    body := '{}'::jsonb, timeout_milliseconds := 30000);
$cron$);
select cron.schedule('funded-tape-monitor-full', '55 12,13 * * *', $cron$
  select net.http_post(url := 'https://prop-firm-newsletter.vercel.app/api/jobs/monitor',
    headers := jsonb_build_object('content-type','application/json','x-job-secret','<FT_JOB_SECRET>'),
    body := '{}'::jsonb, timeout_milliseconds := 30000);
$cron$);

notify pgrst, 'reload schema';
