import html, re
src = open('/workspace/prop-firm-newsletter/build_demo_email.py').read()
ns = {}
exec(src.split("\nquick = [")[0], ns)   # loads stories, e(), etc.
stories = ns["stories"]; e = ns["e"]
SUBJ = "Firms dump Prop Firm Match, a $149.99 no-challenge 50K, and Topstep\u2019s Live call-ups"
PRE = "5 prop firm moves from this week, and what each one means for your next account."
INTRO = "It was a big week. The best-known prop firm comparison site lost a batch of partner firms, FundedNext opened a limited no-challenge 50K, BrightFunded moved into futures, and Topstep explained why heavy account-buyers get moved to Live. Here are the 5 things you can\u2019t miss."
SHORT = ["Apex, Tradeify, Topstep and Goat Funded cut ties with Prop Firm Match",
         "FundedNext: $149.99 no-challenge 50K, max ~$4,800 out",
         "BrightFunded enters futures with two one-phase plans",
         "Rule changes at Alpha Futures, FFN and Blue Guardian",
         "Topstep moves heavy account-buyers to Live"]
TICK = [("PFM","4 FIRMS OUT","dn"),("FNXT 50K","$149.99","up"),("BRIGHT","FUTURES","up"),("TOPSTEP","LIVE CALLS","dn")]

def body_html(s, fs, color, font, bullet_color, lh="1.6"):
    out = ""
    for b in s.get("body", []):
        out += f'<p style="margin:0 0 12px 0;font-family:{font};font-size:{fs}px;line-height:{lh};color:{color};">{e(b)}</p>'
    if s.get("bullets"):
        out += '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">'
        for b in s["bullets"]:
            out += f'<tr><td valign="top" style="width:16px;padding:0 0 10px 0;font-family:{font};font-size:{fs}px;line-height:{lh};color:{bullet_color};">&#8226;</td><td style="padding:0 0 10px 0;font-family:{font};font-size:{fs}px;line-height:{lh};color:{color};">{b}</td></tr>'
        out += '</table>'
    if s.get("note"):
        out += f'<p style="margin:0 0 12px 0;font-family:{font};font-size:{fs-2}px;line-height:1.5;color:{color};opacity:.75;font-style:italic;">{e(s["note"])}</p>'
    return out

def sources(s, color, font, sep=" &middot; "):
    return sep.join(f'<a href="{e(u)}" style="color:{color};text-decoration:underline;font-family:{font};">{e(l)}</a>' for u, l in s["src"])

def shell(title, bodybg, inner, extra_css=""):
    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="x-apple-disable-message-reformatting"><title>{e(title)}</title>
<style>
@media only screen and (max-width:620px) {{
  .container {{ width:100% !important; }}
  .px {{ padding-left:18px !important; padding-right:18px !important; }}
  .stack {{ display:block !important; width:100% !important; }}
  .hide-m {{ display:none !important; }}
  .big {{ font-size:30px !important; }}
  {extra_css}
}}
</style></head>
<body style="margin:0;padding:0;background:{bodybg};">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{bodybg};">{e(PRE)}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{bodybg};"><tr><td align="center" style="padding:16px 8px 32px 8px;">
{inner}
</td></tr></table></body></html>'''

def demo_banner(bg, border, color, font, w=600):
    return f'''<table role="presentation" class="container" width="{w}" cellpadding="0" cellspacing="0" border="0" style="width:{w}px;max-width:{w}px;"><tr>
<td style="background:{bg};border:1px dashed {border};padding:9px 14px;font-family:{font};font-size:12px;line-height:1.5;color:{color};">
<b>DEMO &mdash; NOT SENT.</b> Template preview, not approved or published.<br><b>Subject:</b> {e(SUBJ)}<br><b>Preview:</b> {e(PRE)}</td></tr>
<tr><td style="height:12px;font-size:0;line-height:12px;">&nbsp;</td></tr></table>'''

# ---------------- A: Trading terminal ----------------
def design_a():
    M = "'Courier New',Courier,monospace"; S = "Helvetica,Arial,sans-serif"
    BG="#0A0E14"; PANEL="#111821"; LINE="#1E2A38"; G="#22C55E"; R="#EF4444"; Y="#FACC15"; TXT="#D1D5DB"; DIM="#7A8796"
    tick = "".join(f'<td class="{"hide-m" if n>=2 else ""}" style="padding:8px 9px;border-right:1px solid {LINE};white-space:nowrap;font-family:{M};font-size:11px;color:{TXT};"><b style="color:#fff;">{a}</b> <span style="color:{G if c=="up" else R};">{"&#9650;" if c=="up" else "&#9660;"} {b}</span></td>' for n,(a,b,c) in enumerate(TICK))
    cards = ""
    for i,s in enumerate(stories,1):
        up = i in (2,3)
        tag = f'<span style="font-family:{M};font-size:11px;color:{G if up else R};border:1px solid {G if up else R};padding:2px 6px;">{["","WATCH OUT","NEW DEAL","NEW LAUNCH","","WATCH OUT"][i]}</span>'
        if i==4: tag = f'<span style="font-family:{M};font-size:11px;color:{Y};border:1px solid {Y};padding:2px 6px;">RULE CHANGE</span>'
        cards += f'''<tr><td class="px" style="padding:0 24px 16px 24px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:{PANEL};border:1px solid {LINE};border-left:3px solid {G if up else (Y if i==4 else R)};">
<tr><td style="padding:16px 18px 4px 18px;font-family:{M};font-size:12px;color:{DIM};">[{i:02d}/05] &nbsp;{tag}</td></tr>
<tr><td style="padding:8px 18px 10px 18px;"><h2 style="margin:0;font-family:{S};font-size:18px;line-height:1.3;color:#FFFFFF;">{e(s["h"])}</h2></td></tr>
<tr><td style="padding:0 18px;">{body_html(s,14,TXT,S,G)}</td></tr>
<tr><td style="padding:2px 18px 12px 18px;font-family:{M};font-size:13px;line-height:1.55;color:{TXT};"><span style="color:{G};">&gt; why_it_matters:</span> {e(s["why"])}</td></tr>
<tr><td style="padding:0 18px 16px 18px;font-family:{M};font-size:12px;line-height:1.6;color:{DIM};">src: {sources(s,"#60A5FA",M," | ")}</td></tr>
</table></td></tr>'''
    inner = demo_banner("#1F1A05", Y, Y, M) + f'''
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:{BG};border:1px solid {LINE};">
<tr><td style="background:#000;border-bottom:1px solid {LINE};"><div style="overflow:hidden;white-space:nowrap;max-width:100%;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>{tick}</tr></table></div></td></tr>
<tr><td class="px" style="padding:26px 24px 8px 24px;">
 <div style="font-family:{M};font-size:12px;color:{G};">&#9679; LIVE &nbsp;<span style="color:{DIM};">FT-WEEKLY // OCT 26 &ndash; NOV 01 2026 // ED.000 DEMO</span></div>
 <h1 class="big" style="margin:10px 0 4px 0;font-family:{M};font-size:38px;line-height:1.1;color:#FFFFFF;letter-spacing:-1px;">FUNDED_TAPE<span style="color:{G};">&#9608;</span></h1>
 <div style="font-family:{M};font-size:13px;color:{DIM};">$ cat ./this_week --top 5 --sourced</div>
</td></tr>
<tr><td class="px" style="padding:14px 24px 20px 24px;"><p style="margin:0;font-family:{S};font-size:15px;line-height:1.6;color:{TXT};"><b style="color:#fff;">Happy Sunday, traders.</b> {e(INTRO)}</p></td></tr>
{cards}
<tr><td class="px" style="padding:6px 24px 10px 24px;font-family:{S};font-size:14px;line-height:1.6;color:{TXT};">That&rsquo;s the tape. Always read the current terms on the firm&rsquo;s own page before you buy. Hit reply and tell us which firm to dig into next. We&rsquo;re independent; any affiliate link will be labeled.<br><span style="font-family:{M};color:{G};">-- Funded Tape // see you next Sunday</span></td></tr>
<tr><td class="px" style="padding:12px 24px 22px 24px;"><div style="border:1px solid {LINE};padding:10px 12px;font-family:{M};font-size:11px;line-height:1.6;color:{DIM};">DISCLAIMER: Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</div></td></tr>
<tr><td align="center" style="background:#000;padding:16px;font-family:{M};font-size:11px;line-height:1.7;color:{DIM};"><a href="#" style="color:{DIM};">unsubscribe</a> | <a href="#" style="color:{DIM};">preferences</a> | <a href="#" style="color:{DIM};">view_in_browser</a><br>[mailing address placeholder]</td></tr>
</table>'''
    return shell(SUBJ, "#05080C", inner)

# ---------------- B: Morning Brew-style ----------------
def design_b():
    S = "'Trebuchet MS',Helvetica,Arial,sans-serif"
    BG="#FFF8EC"; INK="#1E1B4B"; PINK="#FF5C8A"; BLUE="#3B5BFD"; YEL="#FFD23F"
    emo = ["&#128680;","&#127915;","&#128640;","&#128221;","&#127919;"]
    tint = ["#FFE4EC","#E0F2FE","#FEF3C7","#EDE9FE","#DCFCE7"]
    labels = ["DRAMA","DEAL WATCH","NEW LAUNCH","RULE BOOK","HEADS UP"]
    cards=""
    for i,s in enumerate(stories):
        cards += f'''<tr><td class="px" style="padding:0 28px 22px 28px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#FFFFFF;border:2px solid {INK};border-radius:14px;">
<tr><td style="padding:16px 20px 0 20px;"><span style="display:inline-block;background:{tint[i]};border-radius:20px;padding:4px 12px;font-family:{S};font-size:12px;font-weight:bold;color:{INK};letter-spacing:1px;">{emo[i]} {labels[i]}</span></td></tr>
<tr><td style="padding:10px 20px 8px 20px;"><h2 style="margin:0;font-family:{S};font-size:20px;line-height:1.3;color:{INK};">{i+1}. {e(s["h"])}</h2></td></tr>
<tr><td style="padding:4px 20px 0 20px;">{body_html(s,15,"#333",S,PINK)}</td></tr>
<tr><td style="padding:0 20px 14px 20px;"><div style="background:{YEL};border-radius:10px;padding:10px 14px;font-family:{S};font-size:14px;line-height:1.5;color:{INK};"><b>&#128161; Why it matters:</b> {e(s["why"])}</div></td></tr>
<tr><td style="padding:0 20px 18px 20px;font-family:{S};font-size:13px;color:#666;">&#128279; {sources(s,BLUE,S)}</td></tr>
</table></td></tr>'''
    inner = demo_banner("#FFFFFF", PINK, PINK, S) + f'''
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:{BG};border-radius:16px;overflow:hidden;">
<tr><td align="center" class="px" style="background:{BLUE};padding:30px 28px 26px 28px;">
 <div style="font-family:{S};font-size:44px;line-height:1;">&#9749;&#128200;</div>
 <h1 class="big" style="margin:10px 0 6px 0;font-family:'Arial Black',{S};font-size:42px;line-height:1.05;color:#FFFFFF;letter-spacing:-1px;">FUNDED TAPE</h1>
 <div style="font-family:{S};font-size:16px;color:#E0E7FF;">Your Sunday cheat sheet for the prop firm world.</div>
</td></tr>
<tr><td align="center" style="background:{PINK};padding:9px 20px;font-family:{S};font-size:13px;font-weight:bold;color:#FFFFFF;letter-spacing:1px;">OCT 26 &ndash; NOV 1, 2026 &nbsp;&#183;&nbsp; DEMO EDITION &nbsp;&#183;&nbsp; 5 MIN READ</td></tr>
<tr><td class="px" style="padding:26px 28px 18px 28px;">
 <p style="margin:0 0 10px 0;font-family:{S};font-size:20px;font-weight:bold;color:{INK};">Happy Sunday, traders &#128075;</p>
 <p style="margin:0;font-family:{S};font-size:16px;line-height:1.6;color:#333;">{e(INTRO)}</p>
</td></tr>
{cards}
<tr><td class="px" style="padding:4px 28px 18px 28px;font-family:{S};font-size:15px;line-height:1.6;color:#333;">That&rsquo;s a wrap! &#127881; Rules and deals change constantly, so always check the firm&rsquo;s own page before you buy. <b>Hit reply</b> and tell us which firm we should dig into next. We&rsquo;re independent, and any affiliate link will be labeled.<br><br>See you next Sunday,<br><b style="color:{INK};">The Funded Tape crew</b></td></tr>
<tr><td class="px" style="padding:0 28px 24px 28px;"><div style="background:#FFFFFF;border:1px dashed #BBB;border-radius:10px;padding:10px 14px;font-family:{S};font-size:12px;line-height:1.5;color:#777;">&#9888;&#65039; Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</div></td></tr>
<tr><td align="center" style="background:{INK};padding:18px;font-family:{S};font-size:12px;line-height:1.7;color:#C7D2FE;">Made with &#9749; for prop traders &middot; <a href="#" style="color:#fff;">Unsubscribe</a> &middot; <a href="#" style="color:#fff;">Preferences</a><br>[Mailing address placeholder]</td></tr>
</table>'''
    return shell(SUBJ, "#FFE9C7", inner)

# ---------------- C: FT / Bloomberg editorial ----------------
def design_c():
    SER = "Georgia,'Times New Roman',Times,serif"; SAN = "Helvetica,Arial,sans-serif"
    BG="#FFF1E5"; INK="#33302E"; RULE="#CCC1B7"; ACC="#990F3D"
    lead = stories[0]
    rest = ""
    for i,s in enumerate(stories[1:],2):
        rest += f'''<tr><td class="px" style="padding:0 36px;"><div style="border-top:1px solid {RULE};font-size:0;line-height:0;">&nbsp;</div></td></tr>
<tr><td class="px" style="padding:18px 36px 18px 36px;">
<div style="font-family:{SAN};font-size:11px;letter-spacing:1.5px;color:{ACC};font-weight:bold;text-transform:uppercase;">No. {i}</div>
<h2 style="margin:6px 0 10px 0;font-family:{SER};font-size:22px;line-height:1.25;color:#000;font-weight:normal;">{e(s["h"])}</h2>
{body_html(s,15,INK,SER,ACC)}
<p style="margin:0 0 10px 0;font-family:{SER};font-size:15px;line-height:1.55;color:{INK};"><i><b>Why it matters.</b> {e(s["why"])}</i></p>
<p style="margin:0;font-family:{SAN};font-size:12px;line-height:1.6;color:#66605C;">SOURCES: {sources(s,"#0F5499",SAN," / ")}</p>
</td></tr>'''
    inner = demo_banner("#F2DFCE", "#990F3D", ACC, SAN) + f'''
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:{BG};">
<tr><td class="px" style="padding:22px 36px 0 36px;">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0"><tr>
  <td style="font-family:{SAN};font-size:11px;letter-spacing:1px;color:#66605C;text-transform:uppercase;">Sunday, November 1, 2026</td>
  <td align="right" style="font-family:{SAN};font-size:11px;letter-spacing:1px;color:#66605C;text-transform:uppercase;">Demo edition</td></tr></table>
</td></tr>
<tr><td align="center" class="px" style="padding:12px 36px 10px 36px;border-bottom:3px double #000;">
 <h1 class="big" style="margin:0;font-family:{SER};font-size:48px;line-height:1.05;color:#000;font-weight:normal;letter-spacing:-0.5px;">Funded Tape</h1>
 <div style="margin-top:6px;font-family:{SER};font-size:15px;font-style:italic;color:{INK};">The weekly record of the prop trading industry</div>
</td></tr>
<tr><td class="px" style="padding:8px 36px;border-bottom:1px solid #000;font-family:{SAN};font-size:11px;letter-spacing:1px;color:#000;text-transform:uppercase;" align="center">Week of Oct 26 &ndash; Nov 1 &nbsp;&#124;&nbsp; Five stories &nbsp;&#124;&nbsp; Independent &amp; sourced</td></tr>
<tr><td class="px" style="padding:24px 36px 6px 36px;">
 <div style="font-family:{SAN};font-size:11px;letter-spacing:1.5px;color:{ACC};font-weight:bold;text-transform:uppercase;">The lead &middot; No. 1</div>
 <h2 class="big" style="margin:8px 0 12px 0;font-family:{SER};font-size:32px;line-height:1.15;color:#000;font-weight:normal;">{e(lead["h"])}</h2>
 <p style="margin:0 0 14px 0;font-family:{SER};font-size:17px;line-height:1.5;color:{INK};font-style:italic;">Happy Sunday, traders. {e(INTRO)}</p>
 {body_html(lead,15,INK,SER,ACC)}
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:4px 0 12px 0;"><tr><td style="border-left:3px solid {ACC};padding:4px 0 4px 14px;font-family:{SER};font-size:18px;line-height:1.4;color:#000;">&ldquo;This should not have happened. We take full responsibility for it.&rdquo;<div style="margin-top:4px;font-family:{SAN};font-size:12px;color:#66605C;">&mdash; Prop Firm Match</div></td></tr></table>
 <p style="margin:0 0 10px 0;font-family:{SER};font-size:15px;line-height:1.55;color:{INK};"><i><b>Why it matters.</b> {e(lead["why"])}</i></p>
 <p style="margin:0 0 18px 0;font-family:{SAN};font-size:12px;line-height:1.6;color:#66605C;">SOURCES: {sources(lead,"#0F5499",SAN," / ")}</p>
</td></tr>
{rest}
<tr><td class="px" style="padding:0 36px;"><div style="border-top:3px double #000;font-size:0;line-height:0;">&nbsp;</div></td></tr>
<tr><td class="px" style="padding:18px 36px 10px 36px;font-family:{SER};font-size:15px;line-height:1.6;color:{INK};">Rules and deals change constantly; always read the current terms on the firm&rsquo;s own page before you buy. Reply to tell us which firm we should examine next. We are independent, and any affiliate link will be labelled.<br><br><i>&mdash; The Editors, Funded Tape</i></td></tr>
<tr><td class="px" style="padding:6px 36px 24px 36px;font-family:{SAN};font-size:11px;line-height:1.6;color:#66605C;">Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</td></tr>
<tr><td align="center" style="background:#262A33;padding:16px;font-family:{SAN};font-size:11px;line-height:1.7;color:#B8B8B8;"><a href="#" style="color:#fff;">Unsubscribe</a> &nbsp;&middot;&nbsp; <a href="#" style="color:#fff;">Manage preferences</a> &nbsp;&middot;&nbsp; <a href="#" style="color:#fff;">View in browser</a><br>[Mailing address placeholder]</td></tr>
</table>'''
    return shell(SUBJ, "#F2DFCE", inner)

# ---------------- D: Clean minimal / Stripe-like ----------------
def design_d():
    S = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
    INK="#0A2540"; BODY="#425466"; MUTE="#8792A2"; ACC="#635BFF"; LINE="#E6EBF1"
    tldr = "".join(f'<tr><td valign="top" style="width:26px;padding:0 0 8px 0;font-family:{S};font-size:14px;font-weight:600;color:{ACC};">{i}</td><td style="padding:0 0 8px 0;font-family:{S};font-size:14px;line-height:1.5;color:{INK};">{e(t)}</td></tr>' for i,t in enumerate(SHORT,1))
    items=""
    for i,s in enumerate(stories,1):
        items += f'''<tr><td class="px" style="padding:0 48px;"><div style="border-top:1px solid {LINE};font-size:0;line-height:0;">&nbsp;</div></td></tr>
<tr><td class="px" style="padding:36px 48px 36px 48px;">
<div class="bigd" style="font-family:{S};font-size:56px;line-height:1;font-weight:300;color:{ACC};letter-spacing:-2px;">0{i}</div>
<h2 style="margin:14px 0 14px 0;font-family:{S};font-size:21px;line-height:1.35;color:{INK};font-weight:600;letter-spacing:-0.2px;">{e(s["h"])}</h2>
{body_html(s,15,BODY,S,ACC,"1.7")}
<p style="margin:6px 0 14px 0;font-family:{S};font-size:15px;line-height:1.6;color:{INK};"><span style="color:{ACC};font-weight:600;">Why it matters &rarr;</span> {e(s["why"])}</p>
<p style="margin:0;font-family:{S};font-size:13px;line-height:1.6;color:{MUTE};">{sources(s,MUTE,S," &nbsp;&middot;&nbsp; ")}</p>
</td></tr>'''
    inner = demo_banner("#F6F9FC", MUTE, BODY, S) + f'''
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#FFFFFF;border:1px solid {LINE};border-radius:12px;">
<tr><td class="px" style="padding:44px 48px 0 48px;">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
  <td style="width:22px;height:22px;background:{ACC};border-radius:6px;font-size:0;">&nbsp;</td>
  <td style="padding-left:10px;font-family:{S};font-size:17px;font-weight:600;color:{INK};letter-spacing:-0.2px;">Funded Tape</td></tr></table>
</td></tr>
<tr><td class="px" style="padding:40px 48px 8px 48px;">
 <div style="font-family:{S};font-size:13px;color:{MUTE};">Oct 26 &ndash; Nov 1, 2026 &nbsp;&middot;&nbsp; Demo edition</div>
 <h1 class="big" style="margin:10px 0 14px 0;font-family:{S};font-size:34px;line-height:1.15;color:{INK};font-weight:600;letter-spacing:-0.8px;">The prop firm week, in five stories.</h1>
 <p style="margin:0;font-family:{S};font-size:16px;line-height:1.7;color:{BODY};">Happy Sunday, traders. {e(INTRO)}</p>
</td></tr>
<tr><td class="px" style="padding:28px 48px 36px 48px;">
 <table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F6F9FC;border-radius:10px;">
  <tr><td style="padding:20px 22px 4px 22px;font-family:{S};font-size:12px;font-weight:600;letter-spacing:1px;color:{ACC};">TL;DR</td></tr>
  <tr><td style="padding:8px 22px 12px 22px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{tldr}</table></td></tr>
 </table>
</td></tr>
{items}
<tr><td class="px" style="padding:0 48px;"><div style="border-top:1px solid {LINE};font-size:0;line-height:0;">&nbsp;</div></td></tr>
<tr><td class="px" style="padding:32px 48px 12px 48px;font-family:{S};font-size:15px;line-height:1.7;color:{BODY};">That&rsquo;s the week. Always read the current terms on the firm&rsquo;s own page before you buy, and hit reply to tell us which firm to dig into next. We&rsquo;re independent; any affiliate link will be labeled.<br><br><span style="color:{INK};font-weight:600;">Funded Tape</span></td></tr>
<tr><td class="px" style="padding:12px 48px 40px 48px;font-family:{S};font-size:12px;line-height:1.6;color:{MUTE};">Not financial advice. Prop firm accounts are mostly simulated, and most traders do not receive a payout.</td></tr>
</table>
<table role="presentation" class="container" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;"><tr><td align="center" style="padding:22px 16px;font-family:{S};font-size:12px;line-height:1.7;color:{MUTE};"><a href="#" style="color:{MUTE};">Unsubscribe</a> &nbsp;&middot;&nbsp; <a href="#" style="color:{MUTE};">Preferences</a> &nbsp;&middot;&nbsp; <a href="#" style="color:{MUTE};">View in browser</a><br>[Mailing address placeholder]</td></tr></table>'''
    return shell(SUBJ, "#F6F9FC", inner, ".bigd { font-size:44px !important; }")

for key, name, fn in [("a","terminal",design_a),("b","playful",design_b),("c","editorial",design_c),("d","minimal",design_d)]:
    open(f"design-{key}-{name}.html","w").write(fn()); print("wrote", key)
