# Funded Tape: send schedule (decided Nov 3, 2026)

**Send:** Sunday 9:00 AM ET = 8:00 AM Edmonton = 14:00 UTC (2 PM London, 10 PM Singapore)
**Backup:** Monday 7:00 AM ET = 6:00 AM Edmonton

## Weekly timeline (all ET / Edmonton)
- Collection window: rolling 7 days, Sat 5:00 PM ET (4:00 PM Edmonton) of last week -> Sat 5:00 PM ET this week. Next window starts exactly at the previous cutoff. Weekends included.
- Draft ready for approval: Sat 8:00 PM ET (7:00 PM Edmonton)
- Approve by: Sat 10:00 PM ET (9:00 PM Edmonton); schedule in Beehiiv
- Send: Sun 9:00 AM ET (8:00 AM Edmonton)
- CORRECTION (Nov 3, KFC): Edmonton is now UTC-6 year-round while ET moved to UTC-5 on Nov 1, so Edmonton is 1 hour behind ET this winter. Always schedule in ET (America/New_York) and convert with a tz library, never a fixed offset.
- Monday-send weeks (Nov 16, Nov 30): cutoff Sun 5:00 PM ET, draft to pomo651 Sun 8:00 PM ET, approve by Sun 10:00 PM ET. Windows run previous cutoff -> next cutoff; see cutoffs.md (source of truth).

## Why
- beehiiv 2025 data: day barely matters (Mon 40.45% vs Sun 40.15% opens), and Sunday has the highest click rate (3.40%). https://www.beehiiv.com/blog/best-times-to-send-a-newsletter
- MailerLite 2.14M campaigns: weekend opens peak at 9 AM local; Sunday 9 AM 48.9% vs best slot 49.7%. https://www.mailerlite.com/blog/best-time-to-send-email
- Trader fit: weekly prep on Sunday, before CME Globex futures reopen Sunday 6 PM ET; 9 AM ET reaches Europe in the afternoon and Asia in the evening.
- Opens are inflated by Apple Mail Privacy Protection, so judge on clicks. https://www.distinctful.com/blog/best-time-to-send-newsletter

## Test (first 4 editions)
Beehiiv's free plan has no A/B testing (paid plans only: https://www.beehiiv.com/pricing), so alternate weeks: Sun Nov 8 and Sun Nov 22 at 9 AM ET vs Mon Nov 16 and Mon Nov 30 at 7 AM ET. SUPERSEDED: Monday-send weeks use a Sunday 5 PM ET cutoff (see cutoffs.md). Compare unique click rate and replies within 48h. Opens only as a tiebreaker.
