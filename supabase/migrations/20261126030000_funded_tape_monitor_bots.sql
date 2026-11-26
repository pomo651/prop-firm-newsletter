-- Funded Tape site, step 6 (Nov 26, 2026): per-bot status for /admin/monitor.
--
-- ft_monitor_bots() returns one row per FT-grok bot: when it last wrote anything,
-- what it wrote in today's window, and a state (same scale as ft_monitor):
--   ok · late · fail · wait · off. The alert job emails a silent bot even when the
--   other bots keep the combined step green.
-- We only see what reaches the DB. A bot's own crash or skipped schedule shows up
-- as "nothing arrived".
--
-- Apply: supabase db query --linked -f supabase/migrations/20261126030000_funded_tape_monitor_bots.sql

create or replace function public.ft_monitor_bots() returns jsonb
language plpgsql stable security definer set search_path = funded_tape, public as $$
declare
  ny text := 'America/New_York';
  d date := (now() at time zone ny)::date;
  w0 timestamptz := ((d - 1)::timestamp + time '06:00') at time zone ny;
  sweep timestamptz := (d::timestamp + time '06:00') at time zone ny;
  picks_due timestamptz := (d::timestamp + time '06:45') at time zone ny;
  draft_due timestamptz := (d::timestamp + time '07:15') at time zone ny;
  short_due timestamptz := (d::timestamp + time '08:45') at time zone ny;
  live boolean := d >= date '2026-11-26';  -- first live edition
  out jsonb := '[]'::jsonb;
  bot text; n int; n_late int; last timestamptz; st text;
  e editions; v videos;
begin
  -- FT-sources / FT-community: items they collected in today's window (24h up to 6:00 AM ET)
  foreach bot in array array['FT-sources', 'FT-community'] loop
    select count(*) filter (where collected_at >= w0 and collected_at < sweep), max(collected_at)
      into n, last from items where collected_by = bot;
    st := case when not live then 'off' when n > 0 then (case when now() >= sweep then 'ok' else 'wait' end)
               when now() < sweep then 'wait' else 'fail' end;
    out := out || jsonb_build_object('bot', bot, 'job', 'Collect items', 'due', '6:00 AM', 'state', st,
      'today', format('%s item%s', n, case when n = 1 then '' else 's' end), 'last', last);
  end loop;

  -- FT-PM: picks in today's window (on time = by 6:45); last write = latest pick/reject or its own item
  select count(*) filter (where status = 'picked' and picked_at >= w0 and picked_at <= picks_due),
         count(*) filter (where status = 'picked' and picked_at > picks_due and picked_at <= picks_due + interval '1 hour')
    into n, n_late from items;
  select greatest(max(picked_at), max(collected_at) filter (where collected_by = 'FT-PM')) into last from items;
  out := out || jsonb_build_object('bot', 'FT-PM', 'job', 'Fact-check + picks', 'due', '6:45 AM',
    'state', case when not live then 'off' when n > 0 then 'ok' when n_late > 0 then 'late'
                  when now() < picks_due then 'wait' else 'fail' end,
    'today', format('%s on time · %s late', n, n_late), 'last', last);

  -- FT-editor: today's draft
  select * into e from editions where edition_date = d;
  select max(updated_at) into last from editions;
  out := out || jsonb_build_object('bot', 'FT-editor', 'job', 'Post draft', 'due', '7:15 AM',
    'state', case when not live then 'off' when e.edition_date is null then (case when now() < draft_due then 'wait' else 'fail' end)
                  when e.created_at <= draft_due then 'ok' else 'late' end,
    'today', case when e.edition_date is null then 'No draft' else format('Draft, %s sections', jsonb_array_length(e.sections)) end,
    'last', last);

  -- FT-video: off until its first Short ever arrives
  select * into v from videos where edition_date = d;
  select max(updated_at) into last from videos;
  out := out || jsonb_build_object('bot', 'FT-video', 'job', 'Build Short', 'due', '8:45 AM',
    'state', case when last is null or not live then 'off' when v.edition_date is null then (case when now() < short_due then 'wait' else 'fail' end)
                  when v.created_at <= short_due then 'ok' else 'late' end,
    'today', case when last is null then 'Not started yet' when v.edition_date is null then 'No Short' else 'Short ' || v.status end,
    'last', last);

  return out;
end $$;

revoke all on function public.ft_monitor_bots() from public, anon, authenticated;
grant execute on function public.ft_monitor_bots() to service_role;

notify pgrst, 'reload schema';
