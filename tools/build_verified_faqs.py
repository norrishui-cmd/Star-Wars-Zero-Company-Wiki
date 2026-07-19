#!/usr/bin/env python3
"""Build 50 verified FAQ URLs and connect relevant questions to every tab hub."""

from html import escape
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
SITE='https://starwarszerocompany.cc'
TODAY='2026-07-19'
ADS_META='<meta name="google-adsense-account" content="ca-pub-9505220977121599">'
ADS_SCRIPT='<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script>'
SOURCES={
 'gameplay':('EA gameplay overview','https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory'),
 'preorder':('EA preorder announcement','https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company'),
 'reveal':('EA reveal recap','https://www.ea.com/games/starwars/zero-company/news/introducing-star-wars-zero-company'),
 'buy':('EA purchase page','https://www.ea.com/games/starwars/zero-company/buy'),
 'steam':('Steam store listing','https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/'),
}

# slug, question, direct answer, supporting detail, source, related tabs
FAQS=[
('when-does-star-wars-zero-company-release','When does Star Wars Zero Company release?','Star Wars Zero Company releases on August 27, 2026.','EA lists the same date on its purchase page and preorder announcement.','buy',['official','confirmed','start-here','media']),
('what-time-does-zero-company-release','What time does Star Wars Zero Company release?','EA lists the release time as 3:00 PM UTC on August 27, 2026.','Regional times should be converted from that UTC timestamp; store countdowns remain the final local check.','buy',['official','confirmed','start-here','planner']),
('what-platforms-is-zero-company-on','What platforms is Star Wars Zero Company on?','The announced launch platforms are PC, PlayStation 5 and Xbox Series X|S.','PC storefronts include the EA app, Steam and Epic Games Store.','preorder',['official','confirmed','start-here','planner']),
('is-zero-company-on-ps4','Is Star Wars Zero Company coming to PS4?','No PS4 version has been announced.','EA names PlayStation 5 as the PlayStation launch platform.','preorder',['official','confirmed','start-here']),
('is-zero-company-on-xbox-one','Is Star Wars Zero Company coming to Xbox One?','No Xbox One version has been announced.','EA names Xbox Series X|S as the Xbox launch platform.','preorder',['official','confirmed','start-here']),
('is-zero-company-on-nintendo-switch','Is Star Wars Zero Company coming to Nintendo Switch?','Nintendo Switch and Switch 2 versions have not been announced.','The current official platform list is PC, PS5 and Xbox Series X|S.','preorder',['official','confirmed','start-here']),
('where-can-you-buy-zero-company-on-pc','Where can you buy Star Wars Zero Company on PC?','The PC version is sold through the EA app, Steam and Epic Games Store.','Availability and regional pricing should be checked on the selected storefront.','preorder',['official','planner','start-here']),
('how-much-does-zero-company-cost','How much does Star Wars Zero Company cost?','The US storefront price for the standard edition is $49.99 before applicable taxes.','Prices can vary by region and storefront, so the local store listing is authoritative at checkout.','buy',['official','planner','start-here']),
('how-much-is-deluxe-edition','How much is the Zero Company Deluxe Edition?','The US storefront price for the Deluxe Edition is $59.99 before applicable taxes.','The Deluxe upgrade is presented around cosmetic content rather than exclusive combat power.','steam',['official','planner','start-here']),
('should-you-preorder','Should you preorder Star Wars Zero Company?','Preordering is optional; the announced incentive is the Crystalline Astromech Cosmetic Pack.','Players who do not value the cosmetic pack can wait for launch reviews and performance testing.','buy',['official','planner','start-here']),
('what-is-the-preorder-bonus','What is the Star Wars Zero Company preorder bonus?','Preorders include the Crystalline Astromech Cosmetic Pack.','EA describes R3 and translucent crystalline astromech customization items in the pack.','buy',['official','media','planner']),
('what-is-in-deluxe-edition','What is included in the Zero Company Deluxe Edition?','The Deluxe Edition adds Clone Wars-inspired cosmetic items.','EA markets the edition around squad appearance options, not a separate campaign or stronger class.','buy',['official','media','planner']),
('how-many-languages-does-zero-company-support','How many languages does Star Wars Zero Company support?','The official stores list 11 interface and subtitle languages.','The list includes English, German, French, Italian, Spanish, Japanese, Korean, Polish, Simplified Chinese, Traditional Chinese and Brazilian Portuguese.','steam',['official','confirmed','start-here']),
('does-zero-company-have-german-audio','Does Star Wars Zero Company have German voice acting?','Yes. German is listed with full audio, interface and subtitles.','English and German are the two full-audio languages shown on the current store listing.','steam',['official','confirmed','media']),
('does-zero-company-have-japanese-audio','Does Star Wars Zero Company have Japanese voice acting?','Japanese interface and subtitles are listed, but Japanese full audio is not.','The currently listed full-audio languages are English and German.','steam',['official','confirmed','media']),
('is-zero-company-single-player','Is Star Wars Zero Company single-player?','Yes. EA describes Zero Company as a single-player turn-based tactics game.','The campaign centers on commanding Hawks and a customizable squad.','preorder',['confirmed','guides','start-here','operations']),
('does-zero-company-have-multiplayer','Does Star Wars Zero Company have multiplayer?','No multiplayer mode appears in the announced feature set.','EA consistently presents the title as single-player and has not announced competitive multiplayer.','preorder',['confirmed','guides','start-here']),
('does-zero-company-have-coop','Does Star Wars Zero Company have co-op?','Co-op has not been announced.','The official descriptions and current Steam features identify a single-player experience.','steam',['confirmed','guides','start-here']),
('can-zero-company-be-played-offline','Can Star Wars Zero Company be played offline?','EA lists the PC online connection requirement as N/A, but platform-level offline behavior should be verified at launch.','This supports an offline expectation for the PC campaign without proving how every storefront check or console feature behaves.','buy',['confirmed','guides','start-here','official']),
('how-many-action-points-per-turn','How many action points does an Operator get per turn?','Each Operator receives three action points per turn.','Movement, attacks and abilities compete for those three AP.','gameplay',['official-systems','systems','guides','start-here']),
('what-do-action-points-control','What can action points be used for?','Action points pay for movement, attacks and abilities during an Operator turn.','Because the pool is limited to three, the order of actions and final position matter.','gameplay',['official-systems','systems','guides']),
('what-is-advantage','What is Advantage in Star Wars Zero Company?','Advantage is a shared squad resource generated by attacking enemies.','It powers strong options including Specialization Ultimates and certain Hawks actions.','gameplay',['official-systems','systems','guides','builds']),
('what-is-maximum-advantage','What is the maximum Advantage?','The Advantage meter is capped at 10.','Continuing to build the meter at the cap wastes potential resource generation.','gameplay',['official-systems','systems','guides']),
('should-you-save-advantage','Should you save Advantage?','Save it only when a later squad action is more valuable than the available spend now.','Because the resource is shared and capped at 10, hoarding at the cap can lose value.','gameplay',['official-systems','systems','guides','planner']),
('how-do-injuries-work','How do Injuries work in Zero Company?','Operators can carry Injuries from tactical combat into the campaign layer.','The Medbay supports recovery, and repeated Injuries increase the risk of losing a character.','gameplay',['official-systems','systems','guides','facilities']),
('how-many-injuries-cause-death','How many Injuries cause permanent death?','On standard difficulty, the third Injury permanently kills the Operator.','The rule makes recovery and roster depth part of long-term campaign planning.','gameplay',['official-systems','systems','guides','facilities','planner']),
('can-story-characters-die','Can story characters die permanently?','Yes. EA says permanent death can affect authored story Operators as well as custom recruits.','The campaign narrative is designed to respond to roster losses.','gameplay',['operatives','lore','guides','confirmed']),
('does-zero-company-have-limited-saves','Does Zero Company have limited saves?','EA says higher difficulties include limited saves.','The exact rules for each difficulty need to be checked in the released game.','reveal',['guides','confirmed','start-here']),
('what-are-mission-cycles','What are Mission Cycles?','Mission Cycles are the HoloTable structure used to present and advance campaign opportunities.','Selecting or delaying one mission can affect what remains available later.','gameplay',['operations','official-systems','systems','planner']),
('are-zero-company-maps-handcrafted','Are the tactical maps handcrafted?','Yes. EA describes the maps as handcrafted.','Randomized enemy and objective elements are intended to keep repeated campaigns from being identical.','gameplay',['operations','guides','media']),
('are-missions-randomized','Are missions randomized in Zero Company?','Missions use handcrafted maps with randomized elements rather than fully procedural maps.','EA specifically points to changing enemies and objectives within authored battlefields.','gameplay',['operations','guides','planner']),
('what-mission-types-are-confirmed','What mission types are confirmed?','EA mentions tactical operations, investigations and other missions.','A complete mission-type list and exact rewards will require launch verification.','preorder',['operations','content-map','guides']),
('how-many-specializations-are-there','How many standard Specializations are there?','EA has confirmed eight standard Specializations.','They are the shared role framework used by most Operators.','gameplay',['classes','builds','content-map','confirmed']),
('what-are-the-eight-specializations','What are the eight standard Specializations?','They are Assault, Gunslinger, Heavy, Medic, Scoundrel, Scout, Sharpshooter and Soldier.','EA provides a distinct battlefield role description for each.','gameplay',['classes','builds','content-map','start-here']),
('can-you-respec','Can Operators change Specialization?','Most Operators can change their Specialization through the Personnel facility.','The wording “most” means character-specific exceptions should be checked after launch.','gameplay',['classes','builds','facilities','planner']),
('how-many-abilities-per-specialization','How many abilities does a standard Specialization have?','Each standard Specialization has one Ultimate, one Standard Ability and one Passive.','Exact names, AP costs and final balance values vary by role and need shipped-game verification.','gameplay',['classes','builds','official-systems']),
('what-are-focus-points','What are Focus Points used for?','Focus Points improve Talents, Abilities and Passives.','They form an individual progression layer alongside equipment and Specialization selection.','gameplay',['classes','builds','official-systems','planner']),
('is-hawks-customizable','Is Hawks customizable?','Yes. Players can customize Hawks’ appearance and combat Specialization.','EA positions Hawks as the campaign leader while allowing player-defined presentation and role.','gameplay',['operatives','classes','builds']),
('can-you-create-custom-operators','Can you create custom Operators?','Yes. The Recruitment facility allows players to create custom squad members.','EA says appearance, class, outfit and abilities can be tailored.','reveal',['operatives','facilities','builds','content-map']),
('can-you-play-without-customs','Can you use only authored Operators?','EA confirms both authored and custom Operators, but it has not stated that custom recruitment is mandatory.','A fully authored roster should be treated as a launch-testing question rather than a guaranteed restriction.','reveal',['operatives','planner','start-here']),
('are-bonds-important','What do squad bonds do?','Deploying Operators together improves bonds and unlocks combat synergies.','Bonds can change tactical options and contribute to different campaign outcomes.','reveal',['operatives','guides','planner','lore']),
('which-operatives-are-confirmed','Which Zero Company Operatives are officially profiled?','EA has profiled Hawks, Trick, Tel-Rea, Cly, Luco, Jae and Kabb.','Their identities and broad roles are official; complete launch statistics are still unpublished.','gameplay',['operatives','content-map','media']),
('who-is-trick','Who is Trick in Zero Company?','Trick is a hardened Clone Trooper and a member of Zero Company.','Official material presents him as part of the squad’s mixed set of Clone Wars archetypes.','gameplay',['operatives','lore','media']),
('who-is-telrea','Who is Tel’Rea Vokoss?','Tel’Rea Vokoss is a Jedi Padawan who joins Zero Company.','Her presence is one example of the unusual alliances inside the squad.','gameplay',['operatives','lore','media']),
('who-is-cly','Who is Cly Kullervo?','Cly Kullervo is a Mandalorian warrior associated with the ancient Clan Verminoth.','EA includes her among the key authored members of Zero Company.','gameplay',['operatives','lore','media']),
('who-is-luco','Who is Luco Bronc?','Luco Bronc is an Umbaran sniper in Zero Company.','He represents the squad’s long-range specialist archetype in official descriptions.','gameplay',['operatives','lore','media']),
('what-is-the-den','What is The Den?','The Den is Zero Company’s home base between missions.','Players recruit, equip, develop and recover Operators there while managing the campaign.','reveal',['facilities','official-systems','start-here','content-map']),
('what-facilities-are-in-the-den','What facilities are in The Den?','EA describes Command Center, HoloTable, Recruitment, Personnel, Armory, Upgrade, Medbay, Customization and Memorial functions.','These rooms connect squad management, equipment, recovery and mission selection.','gameplay',['facilities','content-map','planner']),
('who-is-kundri-fathom','Who is Kundri Fathom?','Kundri Fathom is the enigmatic leader Zero Company is assigned to track and stop.','She leads the Separatist-aligned Infinite Coil.','gameplay',['lore','hostiles','operations','media']),
('where-does-zero-company-take-place','Where does Star Wars Zero Company take place?','The story is set during the twilight of the Clone Wars and spans multiple galactic locations.','EA specifically confirms locations including Vandor and Mapuzo.','reveal',['lore','operations','media','content-map']),
]

HUBS=['operatives','classes','builds','operations','hostiles','guides','content-map','official-systems','facilities','lore','confirmed','official','start-here','systems','planner','media']

STYLE=""":root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#a8bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1040px}*{box-sizing:border-box}body{margin:0;background:#071016;color:var(--text);font:16px/1.72 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}nav a{color:var(--muted);font-size:14px}.hero{padding:50px 0 28px;border-bottom:1px solid var(--line)}.crumb,.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--teal)}h1{font-size:clamp(34px,6vw,56px);line-height:1.08;margin:13px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#cad8e0;max-width:850px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0;color:var(--text)}.answer{border-color:rgba(54,224,206,.5)}.note{border-color:rgba(233,184,74,.45)}.muted,.source{color:var(--muted);font-size:14px}li{margin:8px 0}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){nav{margin-left:0}.top .wrap{padding-top:10px;padding-bottom:10px}}"""

def faq_page(item,index):
 slug,q,a,detail,source,tabs=item; src_name,src_url=SOURCES[source]
 route=f'/questions/{slug}.html'; desc=f'{q} {a} Verified from current official Star Wars Zero Company information.'
 related=[x for i,x in enumerate(FAQS) if i!=index and set(x[5])&set(tabs)][:3]
 rel=''.join(f'<a class="card" href="/questions/{x[0]}.html"><strong>{escape(x[1])}</strong><br><span class="muted">{escape(x[2])}</span></a>' for x in related)
 schema={"@context":"https://schema.org","@type":"FAQPage","url":SITE+route,"inLanguage":"en","dateModified":TODAY,"mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a+' '+detail}}]}
 body=f'''<section class="hero"><div class="crumb"><a href="/questions/">FAQ</a> / Verified Answer</div><p class="eyebrow">Fact-checked July 19, 2026</p><h1>{escape(q)}</h1><p class="lead">{escape(a)}</p></section><section class="block answer"><h2>Quick Answer</h2><p><strong>{escape(a)}</strong></p><p>{escape(detail)}</p></section><section class="block"><h2>What the Official Information Says</h2><p>The current answer is based on the <a href="{src_url}" rel="nofollow">{escape(src_name)}</a>. That source establishes the core fact above without requiring an inferred class statistic, hidden feature or unofficial leak.</p><p>Star Wars Zero Company is scheduled for August 27, 2026. Features and store details can change before release, so this page records both the answer and the date it was checked.</p></section><section class="block"><h2>What Players Should Take From This</h2><p>{escape(detail)} Use this answer as a purchase or planning baseline, while treating unpublished launch values and platform-specific behavior as items for release-day verification.</p><p>We keep a narrow scope on this URL so it answers one search question directly. Broader mechanics, character and campaign context is linked through the relevant section hubs below.</p></section><section class="block note"><h2>Verification Boundary</h2><p>This FAQ reports the current first-party position. It does not turn trailer interpretation into a final statistic, promise an unannounced platform, or present a pre-release tactic as a proven optimal build. The page will be revised if EA publishes a conflicting update.</p></section><section><h2>Related Questions</h2><div class="grid">{rel}<a class="card" href="/questions/"><strong>Browse all 50 FAQs</strong><br><span class="muted">Release, gameplay, Operators, The Den and story</span></a></div></section>'''
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(q)} | Zero Company FAQ</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}{route}"><meta property="og:type" content="article"><meta property="og:url" content="{SITE}{route}"><meta property="og:title" content="{escape(q)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:image" content="{SITE}/assets/zero-company-hero.png"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav><a href="/questions/">FAQ</a><a href="/news/">News</a><a href="/guides/">Guides</a><a href="/official-systems/">Systems</a><a href="/official/">Official Info</a></nav></div></header><main class="wrap">{body}</main><footer><div class="wrap">Unofficial, source-linked FAQ. <a href="/about/sources-and-citations.html">Sources policy</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''

def build_hub():
 groups=[('Release, Platforms & Editions',range(0,15)),('Game Modes & Tactical Systems',range(15,32)),('Specializations & Operators',range(32,46)),('The Den, Story & Locations',range(46,50))]
 sections=[]
 for label,idxs in groups:
  cards=''.join(f'<a class="card" href="/questions/{FAQS[i][0]}.html"><strong>{escape(FAQS[i][1])}</strong><br><span class="muted">{escape(FAQS[i][2])}</span></a>' for i in idxs)
  sections.append(f'<section><h2>{escape(label)}</h2><div class="grid">{cards}</div></section>')
 schema={"@context":"https://schema.org","@type":"CollectionPage","name":"Star Wars Zero Company FAQ","description":"Fifty verified answers about release, platforms, gameplay, Operators, The Den and story.","url":SITE+'/questions/',"dateModified":TODAY,"inLanguage":"en"}
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Star Wars Zero Company FAQ — 50 Verified Answers</title><meta name="description" content="Fifty source-linked Star Wars Zero Company FAQs covering release date, platforms, languages, gameplay, Operators, The Den and story."><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}/questions/"><script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav><a href="/questions/">FAQ</a><a href="/news/">News</a><a href="/guides/">Guides</a><a href="/confirmed/">Confirmed</a><a href="/official/">Official Info</a></nav></div></header><main class="wrap"><section class="hero"><p class="eyebrow">50 source-linked answers</p><h1>Star Wars Zero Company FAQ</h1><p class="lead">Direct answers to real pre-release questions. Every FAQ has its own URL, current source and explicit boundary between confirmed information and launch-day testing.</p></section>{''.join(sections)}</main><footer><div class="wrap">Unofficial FAQ · <a href="/about/sources-and-citations.html">Sources policy</a></div></footer></body></html>'''

def noindex_legacy():
 valid={x[0]+'.html' for x in FAQS}|{'index.html'}
 for p in (ROOT/'questions').glob('*.html'):
  if p.name in valid: continue
  s=p.read_text(encoding='utf-8-sig',errors='ignore')
  if re.search(r'<meta\s+name=["\']robots["\']',s,re.I):
   s=re.sub(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*["\']\s*/?>','<meta name="robots" content="noindex,follow">',s,count=1,flags=re.I)
  else: s=re.sub(r'</head>','<meta name="robots" content="noindex,follow"></head>',s,count=1,flags=re.I)
  p.write_text(s,encoding='utf-8')

def faq_module(tab):
 items=[x for x in FAQS if tab in x[5]][:5]
 if len(items)<3: items=(items+FAQS[:5])[:5]
 cards=''.join(f'<a href="/questions/{x[0]}.html" style="display:block;border:1px solid #284050;border-radius:7px;padding:16px;color:inherit;text-decoration:none;background:#0d1922"><small style="color:#9db0bd">VERIFIED FAQ</small><br><strong style="color:#36e0ce">{escape(x[1])}</strong><br><span style="color:#9db0bd;font-size:14px">{escape(x[2])}</span></a>' for x in items)
 return f'''<!-- TAB_FAQ_START --><section class="tab-faq" aria-labelledby="tab-faq-title" style="margin:42px 0"><h2 id="tab-faq-title">Related FAQs</h2><p style="color:#9db0bd">Verified answers connected to this section.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px">{cards}</div><p><a href="/questions/">Browse all 50 FAQs →</a></p></section><!-- TAB_FAQ_END -->'''

def update_hubs():
 for tab in HUBS:
  p=ROOT/tab/'index.html'; s=p.read_text(encoding='utf-8-sig',errors='ignore')
  s=re.sub(r'<!-- TAB_FAQ_START -->.*?<!-- TAB_FAQ_END -->','',s,flags=re.S)
  s=re.sub(r'</main>',faq_module(tab)+'</main>',s,count=1,flags=re.I)
  p.write_text(s,encoding='utf-8')

def add_faq_navigation():
 for p in ROOT.rglob('*.html'):
  s=p.read_text(encoding='utf-8-sig',errors='ignore')
  s=re.sub(r'<a href="/questions/">Questions</a>','<a href="/questions/">FAQ</a>',s,flags=re.I)
  if 'href="/questions/"' not in s and re.search(r'<nav[^>]*>',s,re.I):
   s=re.sub(r'(<nav[^>]*>)',r'\1<a href="/questions/">FAQ</a>',s,count=1,flags=re.I)
  p.write_text(s,encoding='utf-8')

def main():
 out=ROOT/'questions'; out.mkdir(exist_ok=True)
 noindex_legacy()
 for i,item in enumerate(FAQS): (out/f'{item[0]}.html').write_text(faq_page(item,i),encoding='utf-8')
 (out/'index.html').write_text(build_hub(),encoding='utf-8')
 update_hubs(); add_faq_navigation()
 print(f'Built {len(FAQS)} verified FAQ URLs, updated {len(HUBS)} tab hubs and added sitewide FAQ navigation')

if __name__=='__main__': main()
