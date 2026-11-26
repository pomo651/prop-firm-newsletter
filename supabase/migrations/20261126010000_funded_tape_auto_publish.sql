-- Funded Tape site, step 3 (Nov 26, 2026): daily auto-review + publish.
--
-- pomo651 delegated the daily approval to the local FT-team. Every morning at
-- 7:45 AM ET, /api/jobs/auto-publish (called by pg_cron, see the bottom of this
-- file) runs ft_auto_publish(today ET). It publishes the draft only if every check
-- in ft_review_edition passes; otherwise the draft is held and pomo651 gets an email.
-- Every run is logged in funded_tape.publish_log.
--
-- Apply: supabase db query --linked -f supabase/migrations/20261126010000_funded_tape_auto_publish.sql
--        (run from ~/@Pomo651/blackout-clock). The cron job needs the real FT_JOB_SECRET
--        substituted for <FT_JOB_SECRET> -- never commit the value.

create table if not exists funded_tape.publish_log (
  id            bigint generated always as identity primary key,
  edition_date  date not null,
  ran_at        timestamptz not null default now(),
  result        text not null check (result in ('published','held','skipped')),
  reasons       jsonb not null default '[]'::jsonb
);
create index if not exists publish_log_date_idx on funded_tape.publish_log (edition_date, ran_at desc);
alter table funded_tape.publish_log enable row level security;

-- Returns the list of problems (empty = OK to publish).
create or replace function public.ft_review_edition(d date) returns jsonb
language plpgsql stable security definer set search_path = funded_tape, public as $$
declare
  e editions;
  s jsonb;
  i int := 0;
  srcs text[];
  bad text[] := '{}';
  alleg text;
begin
  select * into e from editions where edition_date = d;
  if not found then return jsonb_build_array(format('No draft edition for %s.', d)); end if;

  if coalesce(trim(e.subject), '') = '' then bad := array_append(bad, 'Subject is empty.'); end if;
  if jsonb_array_length(e.sections) = 0 then bad := array_append(bad, 'Edition has no sections.'); end if;

  for s in select * from jsonb_array_elements(e.sections) loop
    i := i + 1;
    if coalesce(trim(s->>'headline'), '') = '' then bad := array_append(bad, format('Section %s: no headline.', i)); end if;
    if coalesce(trim(s->>'body'), '') = '' then bad := array_append(bad, format('Section %s: no body.', i)); end if;
    if coalesce(trim(s->>'why'), '') = '' then bad := array_append(bad, format('Section %s: no "why it matters".', i)); end if;
    select coalesce(array_agg(u), '{}') into srcs
      from jsonb_array_elements_text(coalesce(s->'sources', '[]'::jsonb)) u where u ~ '^https?://';
    if cardinality(srcs) = 0 then
      bad := array_append(bad, format('Section %s: no source links.', i));
    elsif not exists (select 1 from items where url = any(srcs) and status = 'picked') then
      bad := array_append(bad, format('Section %s: none of its sources is a picked (fact-checked) item.', i));
    end if;
    for alleg in
      select url from items
       where url = any(srcs) and status = 'picked' and category = 'allegation'
         and coalesce(evidence, '') not in ('official', 'firm_x_post')
    loop
      bad := array_append(bad, format('Section %s: allegation without a firm response or official evidence (%s).', i, alleg));
    end loop;
  end loop;

  if concat_ws(' ', e.subject, e.preview, e.intro, e.outro, e.sections::text)
     ~* '(\mTBD\M|\mTODO\M|\mXXX\M|lorem ipsum|\[name)' then
    bad := array_append(bad, 'Placeholder text found (TBD / TODO / XXX / lorem ipsum / [name…]).');
  end if;

  return to_jsonb(bad);
end $$;

-- Review, then publish or hold. Logs every run. Returns {result, reasons, subject}.
create or replace function public.ft_auto_publish(d date) returns jsonb
language plpgsql security definer set search_path = funded_tape, public as $$
declare
  e editions;
  reasons jsonb;
  result text;
begin
  select * into e from editions where edition_date = d;
  if found and e.status = 'published' then
    result := 'skipped';
    reasons := '["Already published."]'::jsonb;
  else
    reasons := public.ft_review_edition(d);
    if jsonb_array_length(reasons) = 0 then
      update editions set status = 'published', published_at = now(), updated_at = now() where edition_date = d;
      result := 'published';
    else
      result := 'held';
    end if;
  end if;
  insert into publish_log (edition_date, result, reasons) values (d, result, reasons);
  return jsonb_build_object('result', result, 'reasons', reasons, 'subject', e.subject, 'edition_date', d);
end $$;

-- ft_edition now also returns the latest auto-review for that date (owner panel shows it).
create or replace function public.ft_edition(d date, include_drafts boolean default false) returns jsonb
language sql stable security definer set search_path = funded_tape, public as $$
  select (to_jsonb(e) - 'id') || jsonb_build_object(
           'video', (select to_jsonb(v) - 'id' - 'edition_date' from videos v
                      where v.edition_date = e.edition_date and (v.status <> 'draft' or include_drafts)),
           'review', case when include_drafts then
                      (select jsonb_build_object('result', l.result, 'reasons', l.reasons, 'ran_at', l.ran_at)
                         from publish_log l where l.edition_date = e.edition_date order by l.ran_at desc limit 1) end)
    from editions e
   where edition_date = d and (status = 'published' or include_drafts);
$$;

revoke all on function public.ft_review_edition(date), public.ft_auto_publish(date), public.ft_edition(date, boolean)
  from public, anon, authenticated;
grant execute on function public.ft_review_edition(date), public.ft_auto_publish(date), public.ft_edition(date, boolean)
  to service_role;

-- Daily trigger. Fires at 11:45 and 12:45 UTC; the route acts only when it is the
-- 7 o'clock hour in New York, so it lands on 7:45 AM ET in both EST and EDT.
select cron.schedule('funded-tape-auto-publish', '45 11,12 * * *', $cron$
  select net.http_post(
    url     := 'https://prop-firm-newsletter.vercel.app/api/jobs/auto-publish',
    headers := jsonb_build_object('content-type', 'application/json', 'x-job-secret', '<FT_JOB_SECRET>'),
    body    := '{}'::jsonb,
    timeout_milliseconds := 30000
  );
$cron$);

notify pgrst, 'reload schema';
