# Funded Tape edition, Oct 27 - Nov 3, 2026, in design B ("Morning Brew-style")
import html
def e(s): return html.escape(s, quote=True)
OUT = "/workspace/prop-firm-newsletter/editions/2026-10-27_11-03-preview.html"
SUBJ = "Prop Firm Match loses ~21 partners, PipFarm kills its $5K payout cap, and a $39 50K"
PRE = "The 5 prop firm stories from Oct 27 to Nov 3 that change how you buy, trade and get paid."
INTRO = ("The comparison site a lot of traders use to pick firms spent the week losing partners, a forex firm tore up its payout ceiling, "
         "and futures firms kept finding new ways to get you funded for less. Here are the 5 things you can\u2019t miss.")

stories = [
 dict(emo="&#128680;", label="DRAMA", tint="#FFE4EC",
  h="Prop Firm Match loses about 21 partner firms over affiliate redirects",
  body=["On Oct 29, trader @traderkane, who runs rival site Prop Firm Compare, posted a video showing that clicking a firm profile or \u201cCopy Code\u201d on Prop Firm Match (PFM) sent the original browser tab through that firm\u2019s affiliate link. PFM says this ran from October 2025, spread to firm names and logos in March 2026, and was switched off on Oct 29.",
        "By Nov 2, about 21 brands had cut ties, including Apex, Tradeify, Lucid, Goat Funded Trader, FundingPips and Blue Guardian, leaving 38 partners. Topstep CEO Michael Patak said Topstep paid $10,000 a month for its listing and is dropping it. PFM\u2019s Nov 2 statement puts the impact at a \u201clow single-digit percentage\u201d of its commissions; TradeInformer says internal data it has seen points to a much bigger lift."],
  why="PFM says prices and discount codes were never affected, but rankings and \u201cbest deal\u201d lists can carry money you can\u2019t see. Judge firms on their own rule pages, and expect affiliate programs across the industry to tighten.",
  src=[("https://www.financemagnates.com/forex/2-dozen-brands-one-background-tab-how-prop-firm-matchs-affiliate-redirect-slipped-past-its-partners/","Finance Magnates"),
       ("https://fxnewsgroup.com/forex-news/retail-forex/prop-firm-match-responds-to-cookie-stuffing-affiliate-link-scandal/","PFM statement (full text)"),
       ("https://x.com/traderkane/status/2115904959401140641","@traderkane on X"),
       ("https://tradeinformer.com/broker-news/exclusive-prop-firm-match-doubled-commissions-for-one-prop-after-cookie-stuffing-code-was-added","TradeInformer")]),
 dict(emo="&#128184;", label="PAYOUTS", tint="#DCFCE7",
  h="PipFarm scraps its $5,000 payout cap on new accounts",
  body=["For accounts bought from Nov 1, PipFarm removed the $5,000 limit on a single payout and the 6% ceiling on its percentage cap. Your first payout is still capped at 3% of balance and the cap rises 1% with every payout, now with no maximum. Profit above the cap stays in the account for next time.",
        "PipFarm says the most you can request across 8 payouts on a 100K rises from $37,000 to $52,000, before profit share. Accounts bought before Nov 1 keep their old caps, and an add-on that starts the cap at 4% or 5% is \u201ccoming soon.\u201d"],
  why="If you\u2019re consistently profitable on a big account, the dollar ceiling that used to bite first is gone. It only covers new purchases, so an older account won\u2019t benefit.",
  src=[("https://updates.pipfarm.com/changelog/payout-caps-no-more-dollar5000-limit","PipFarm changelog"),
       ("https://help.pipfarm.com/articles/1900230-payout-caps","PipFarm help: Payout Caps")]),
 dict(emo="&#127919;", label="HEADS UP", tint="#FEF3C7",
  h="Topstep: heavy account-buyers will be moved to Live",
  body=["On Oct 28, Topstep replied on X to a trader upset about being moved to Live just before a payout. It said he had taken four payouts in three weeks while buying accounts \u201cat a pace that annualizes to roughly 700 per year.\u201d",
        "\u201cIt isn\u2019t a SIM lottery. Everyone is welcome, but repeatedly cycling through accounts will eventually mean proving your strategy in Live.\u201d An amount equal to his Express Funded balances will be released into Live as he builds there. TopstepX also added Live performance stats."],
  why="Buying and cycling lots of accounts can trigger a Live call-up, which changes when and how you get paid. Read Topstep\u2019s Live transition rules before you scale up.",
  src=[("https://x.com/Topstep/status/2115501066145976393","Topstep on X"),
       ("https://fundedtruth.com/prop-firm-news/topstep-adds-live-performance-stats-on-topstepx-and-explains-calls-to-live/","Funded Truth")]),
 dict(emo="&#128640;", label="NEW LAUNCH", tint="#E0F2FE",
  h="Goat Funded Futures opens a $50K evaluation for $39",
  body=["GOAT Access is a one-phase 50K: $39 to start, a $99 activation fee only after you pass ($138 total), a $2,500 (5%) target and a $2,000 end-of-day trailing drawdown that locks at $50,100. There\u2019s no daily loss limit, no time limit and no consistency rule in the evaluation (35% once funded).",
        "Payouts are weekly, $500 to $1,500 per request at an 80/20 split, after 5 profitable days of $150+. High-impact news trading and overnight holds aren\u2019t allowed, and you can hold up to 3 funded GOAT Access accounts at once."],
  why="It\u2019s one of the cheapest ways into a 50K futures eval right now, and you only pay activation if you pass. The trade-offs are the news ban, a 1-minute holding rule checked at payout, and the $1,500 payout cap.",
  src=[("https://help.goatfundedfutures.com/en/articles/17838201-goat-access-specifications-rules-and-payouts","GFF help center"),
       ("https://goatfundedfutures.com/goat-access","GOAT Access page")]),
 dict(emo="&#128221;", label="RULE BOOK", tint="#EDE9FE",
  h="Tradeify lets blown Select accounts buy their way back to funded",
  body=["New Funded Reset lets you buy a fresh Select funded account (50K, 100K or 150K, Daily or Flex) the same size as one you breached, without retaking the evaluation. The offer lasts 30 days after the breach, and the new account starts at zero profit with a full drawdown.",
        "You can\u2019t use it if that account ever paid out, if you or anyone in your household holds a Live account, or more than twice. First-use prices start at $450 (50K), $570 (100K) and $815 (150K) and move with how many payouts you\u2019ve taken across all your accounts. No refunds."],
  why="It can save you a full re-pass after one bad day, but it isn\u2019t cheap. Compare it with the price of a fresh evaluation before you buy.",
  src=[("https://help.tradeify.co/en/articles/17780377-funded-reset-faq","Tradeify help: Funded Reset")]),
]

S = "'Trebuchet MS',Helvetica,Arial,sans-serif"
BG="#FFF8EC"; INK="#1E1B4B"; PINK="#FF5C8A"; BLUE="#3B5BFD"; YEL="#FFD23F"

def p(t, fs=15, color="#333", extra=""):
    return f'<p style="margin:0 0 12px 0;font-family:{S};font-size:{fs}px;line-height:1.6;color:{color};{extra}">{t}</p>'

cards = ""
for i, s in enumerate(stories):
    body = "".join(p(e(b)) for b in s["body"])
    srcs = " &middot; ".join(f'<a href="{e(u)}" style="color:{BLUE};text-decoration:underline;font-family:{S};">{e(l)}</a>' for u, l in s["src"])
    cards += f'''<tr><td class="px" style="padding:0 28px 22px 28px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:2px solid {INK};border-radius:14px;">
<tr><td class="cp" style="padding:16px 20px 0 20px;"><span style="display:inline-block;background:{s["tint"]};border-radius:20px;padding:4px 12px;font-family:{S};font-size:12px;font-weight:bold;color:{INK};letter-spacing:1px;">{s["emo"]} {s["label"]}</span></td></tr>
<tr><td class="cp" style="padding:10px 20px 8px 20px;"><h2 style="margin:0;font-family:{S};font-size:20px;line-height:1.3;color:{INK};">{i+1}. {e(s["h"])}</h2></td></tr>
<tr><td class="cp" style="padding:4px 20px 0 20px;">{body}</td></tr>
<tr><td class="cp" style="padding:0 20px 14px 20px;"><div style="background:{YEL};border-radius:10px;padding:10px 14px;font-family:{S};font-size:14px;line-height:1.5;color:{INK};"><b>&#128161; Why it matters:</b> {e(s["why"])}</div></td></tr>
<tr><td class="cp" style="padding:0 20px 18px 20px;font-family:{S};font-size:13px;line-height:1.6;color:#666;">&#128279; {srcs}</td></tr>
</table></td></tr>'''

doc = f'''<!DOCTYPE html>
<!-- PREVIEW, NOT SENT. Funded Tape edition Oct 27 - Nov 3, 2026. Subject: {e(SUBJ)} -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting"><title>{e(SUBJ)}</title>
<style>
@media only screen and (max-width:620px) {{
  .container {{ width:100% !important; }}
  .px {{ padding-left:14px !important; padding-right:14px !important; }}
  .cp {{ padding-left:16px !important; padding-right:16px !important; }}
  .big {{ font-size:34px !important; }}
}}
</style></head>
<body style="margin:0;padding:0;background:#FFE9C7;">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:#FFE9C7;">{e(PRE)}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFE9C7;"><tr><td align="center" style="padding:6px 8px 32px 8px;">
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;">
<tr><td align="center" style="padding:0 0 6px 0;font-family:{S};font-size:10px;color:#A8A29E;">Preview, not sent</td></tr></table>
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:{BG};border-radius:16px;overflow:hidden;">
<tr><td align="center" class="px" style="background:{BLUE};padding:30px 28px 26px 28px;">
 <div style="font-family:{S};font-size:44px;line-height:1;">&#9749;&#128200;</div>
 <h1 class="big" style="margin:10px 0 6px 0;font-family:'Arial Black',{S};font-size:42px;line-height:1.05;color:#FFFFFF;letter-spacing:-1px;">FUNDED TAPE</h1>
 <div style="font-family:{S};font-size:16px;color:#E0E7FF;">Your weekly cheat sheet for the prop firm world.</div>
</td></tr>
<tr><td align="center" style="background:{PINK};padding:9px 20px;font-family:{S};font-size:13px;font-weight:bold;color:#FFFFFF;letter-spacing:1px;"><span style="white-space:nowrap;">OCT 27 &ndash; NOV 3, 2026</span> &nbsp;&#183;&nbsp; <span style="white-space:nowrap;">ISSUE #1</span> &nbsp;&#183;&nbsp; <span style="white-space:nowrap;">5 MIN READ</span></td></tr>
<tr><td class="px" style="padding:26px 28px 18px 28px;">
 {p("Hey traders &#128075;", 20, INK, "font-weight:bold;margin-bottom:10px;")}
 <p style="margin:0;font-family:{S};font-size:16px;line-height:1.6;color:#333;">{e(INTRO)}</p>
</td></tr>
{cards}
<tr><td class="px" style="padding:4px 28px 18px 28px;font-family:{S};font-size:15px;line-height:1.6;color:#333;">That&rsquo;s a wrap! &#127881; Rules and deals change constantly, so always check the firm&rsquo;s own page before you buy. <b>Hit reply</b> and tell us which firm we should dig into next. We&rsquo;re independent, and if we ever use an affiliate link, we&rsquo;ll label it.<br><br>See you next week,<br><b style="color:{INK};">The Funded Tape crew</b></td></tr>
<tr><td class="px" style="padding:0 28px 24px 28px;"><div style="background:#FFFFFF;border:1px dashed #BBB;border-radius:10px;padding:10px 14px;font-family:{S};font-size:12px;line-height:1.5;color:#777;">&#9888;&#65039; Not financial advice. Funded Tape is for information only. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</div></td></tr>
<tr><td align="center" style="background:{INK};padding:18px;font-family:{S};font-size:12px;line-height:1.7;color:#C7D2FE;">You&rsquo;re getting this because you subscribed to Funded Tape.<br><a href="#" style="color:#fff;">Unsubscribe</a> &middot; <a href="#" style="color:#fff;">Preferences</a> &middot; <a href="#" style="color:#fff;">View in browser</a><br>Funded Tape &middot; [mailing address]</td></tr>
</table>
</td></tr></table></body></html>'''
open(OUT, "w").write(doc); print("wrote", OUT)
