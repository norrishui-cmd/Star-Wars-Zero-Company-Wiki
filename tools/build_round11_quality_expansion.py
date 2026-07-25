#!/usr/bin/env python3
"""Round 11: source-grounded cast, mechanics, mission and tactics expansion."""

from html import escape
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
EA_QA = "https://www.ea.com/games/starwars/zero-company/news/answering-biggest-questions"
EA_GAMEPLAY = "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"
SW_CAST = "https://www.starwars.com/news/sdcc-star-wars-zero-company-cast-announce"
CHECKED = "2026-07-25"

STYLE = """:root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#9db0bd;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 520px at 80% -10%,rgba(54,224,206,.08),transparent),var(--bg);color:var(--text);font:16px/1.68 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:rgba(7,16,22,.95);position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}.nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}.nav a{color:var(--muted);font-size:14px}.hero{padding:52px 0 30px;border-bottom:1px solid var(--line)}.crumb{font-size:12px;text-transform:uppercase;letter-spacing:.15em;color:var(--teal)}h1{font-size:clamp(34px,6vw,58px);line-height:1.06;margin:14px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#c4d4dd;max-width:850px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:15px}.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card,.block{border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0}.card{display:block;color:var(--text)}.pill{display:inline-block;border:1px solid rgba(54,224,206,.45);border-radius:4px;padding:5px 9px;margin:5px 7px 0 0;color:var(--teal);font-size:12px;text-transform:uppercase;letter-spacing:.08em}.gold{color:var(--gold);border-color:rgba(233,184,74,.45)}.mini,.source{color:var(--muted);font-size:14px}.source{border-top:1px solid var(--line);padding-top:14px}li{margin:8px 0}table{width:100%;border-collapse:collapse}th,td{border:1px solid var(--line);padding:11px;text-align:left;vertical-align:top}th{color:var(--gold)}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){.two{grid-template-columns:1fr}.nav{margin-left:0}.top .wrap{padding-top:12px;padding-bottom:12px}}"""

CAST = [
    ("hawks-masculine-jonathan-freeman", "Hawks (Masculine)", "Jonathan Freeman", "the masculine voice option for the customizable former Republic officer who leads Zero Company", "Hawks is required on story missions and can be customized in species, first name, appearance, clothing and Specialization."),
    ("hawks-feminine-erica-luttrell", "Hawks (Feminine)", "Erica Luttrell", "the feminine voice option for the customizable former Republic officer who leads Zero Company", "The two credited Hawks performances support the same customizable protagonist rather than two separate Operators."),
    ("kundri-fathom-rekha-sharma", "Kundri Fathom", "Rekha Sharma", "the leader of the Separatist-aligned Infinite Coil and the central threat pursued by Zero Company", "Kundri is an authored story character; no boss statistics or encounter details have been published."),
    ("trick-dee-bradley-baker", "Trick and Clone Troopers", "Dee Bradley Baker", "Trick, CT-3301, and the game's Clone Troopers", "Trick is Hawks's old comrade and an authored Operator; the official cast article confirms the performance credit."),
    ("anakin-skywalker-matt-lanter", "Anakin Skywalker", "Matt Lanter", "Anakin Skywalker in Zero Company's Clone Wars-era story", "The credit confirms Anakin's appearance, but it does not establish that he is recruitable or playable."),
    ("runa-blask-vic-michaelis", "Runa Blask", "Vic Michaelis", "the member of The Den team associated with Operations and Finance", "Runa supports Zero Company from The Den rather than being listed among the frontline authored Operators."),
    ("kabb-uppercut-jb-blanc", "Kabb Uppercut", "JB Blanc", "the Kessurian crew member whose official footage shows him working with locks and safes", "Kabb is an authored Operator; his full launch ability tree and equipment values remain unpublished."),
    ("jae-mordant-judy-alice-lee", "Jae Mordant", "Judy Alice Lee", "the Umbaran authored Operator Jae Mordant", "Jae is part of the authored roster that can be mixed with custom recruits for Tactical Missions."),
    ("cly-kullervo-alex-mckenna", "Cly Kullervo", "Alex McKenna", "the Mandalorian warrior Cly Kullervo of Clan Verminoth", "Only Cly can wear the Mandalorian armor according to the official July Q&A."),
    ("bennic-halloren-leo-howard", "Bennic Halloren", "Leo Howard", "the Republic Intelligence contact supporting the company from The Den", "Bennic is a support character, not currently described as a deployable Operator."),
    ("visser-dylan-kenin", "Visser", "Dylan Kenin", "the character Visser in Star Wars Zero Company", "StarWars.com confirms the character and actor, while the role, faction and gameplay status have not yet been detailed."),
    ("tel-rea-nicole-rainteau", "Tel-Rea Vokoss", "Nicole Rainteau", "the Tognath Jedi Padawan and authored Operator Tel-Rea", "Tel-Rea is the only Jedi Padawan-class Operator; the official Q&A says another cannot be recruited if she dies."),
    ("neesh-renark-jim-pirri", "Neesh Renark", "Jim Pirri", "the Armory and Black Market specialist stationed at The Den", "Neesh supports equipment access and company management rather than being announced as a frontline Operator."),
    ("m3vo-meevo-dc-douglas", "M-3VO / Meevo", "D.C. Douglas", "Zero Company's droid pilot and Medbay support character", "Meevo supports the Pilot and Medbay functions at The Den; the cast credit does not make the droid a recruitable combat unit."),
    ("typhon-hunter-smith", "Typhon", "Hunter Smith", "the newly named character Typhon", "The July 23 cast announcement confirms the name and voice actor but does not yet identify Typhon's allegiance or gameplay function."),
]

MECHANICS = [
    ("hawks-required-story-missions", "Is Hawks Required on Story Missions?", "Hawks must deploy on every story mission, while skirmish missions allow any Operator combination.", "This rule makes the protagonist a fixed planning constraint only for the main story layer.", ["Reserve one story-mission slot for Hawks.", "Use skirmishes to test squads that omit Hawks.", "Do not interpret roster freedom as permission to bench Hawks in the campaign's critical missions."]),
    ("hawks-death-mission-failure", "What Happens If Hawks Dies?", "Hawks dying in combat causes an automatic mission failure and the mission must be restarted.", "The protagonist does not follow the same campaign-loss outcome as an ordinary Operator during the failed mission.", ["Protect Hawks when an objective exposes the squad.", "Treat a lethal risk to Hawks as a mission-state risk, not only a roster risk.", "Permadeath settings do not turn Hawks's combat death into a continuing story without the protagonist."]),
    ("operator-limit-20", "Zero Company Operator Limit Explained", "The current headquarters limit is 20 Operators; the starting maximum is seven.", "The cap grows through The Den upgrades, story progress and authored Operators joining the company.", ["Plan around a small opening roster.", "Capacity upgrades create room for specialists and replacement recruits.", "The published 20-Operator figure is a current development value and should be rechecked at launch."]),
    ("standard-squad-limit-four", "Standard Squad Size and Mission Exceptions", "The standard squad limit can reach four Operators, though some missions let players control additional characters.", "Four is the normal deployment planning number, not an absolute cap for every scripted encounter.", ["Build four-role cores for normal missions.", "Expect mission-specific allies or extra controlled units in some scenarios.", "Do not assume headquarters capacity and deployed squad size are the same system."]),
    ("four-weapon-classes", "Four Weapon Classes in Zero Company", "EA says the game has four weapon classes, with four to six cosmetic models available within each class.", "The announcement confirms the structure but does not publish all class names, damage tables or acquisition sources.", ["Separate weapon performance from cosmetic model choice.", "Wait for launch data before ranking unnamed classes.", "Use the official four-class count when planning database coverage."]),
    ("real-time-cutscenes", "Are Zero Company Cutscenes Real-Time?", "Most in-game cutscenes are rendered in real time, with a few minor pre-rendered exceptions.", "Real-time rendering allows customized Hawks and recruits to appear consistently through much of the cinematic presentation.", ["Character appearance choices should be visible beyond the customization screen.", "A few cinematics may not reflect every live customization detail.", "Platform performance and final visual differences require launch testing."]),
    ("intel-operation-costs", "How Intel Limits Galaxy Map Operations", "Operations cost varying amounts of Intel, so the strategic layer is constrained by a spendable campaign resource.", "Players cannot treat every available map event as free; Operations can also expire.", ["Compare immediate rewards with expiring opportunities.", "Keep story-critical timing in view before spending Intel.", "Choose Operations that support the current roster and campaign priorities."]),
    ("story-missions-become-obligatory", "When Story Missions Become Obligatory", "Story-critical missions become mandatory after a period of time.", "The campaign offers choices between missions, but it does not allow indefinite delay of the main story.", ["Check expiry and story pressure together.", "Do not spend all Intel as if the strategic layer were timeless.", "Use optional Operations before their value is overtaken by the next required mission."]),
    ("tel-rea-only-jedi-padawan", "Can You Recruit Another Jedi Padawan?", "No. Tel-Rea is the only Jedi Padawan-class Operator in Zero Company.", "Losing her cannot be solved by recruiting a custom replacement in the same unique class.", ["Treat Tel-Rea as a one-of-one roster asset.", "Do not build pre-release guides around repeatable Jedi recruitment.", "Consider disabling permadeath if losing unique authored Operators would undermine the desired campaign experience."]),
    ("no-fog-of-war", "How Snipers Work Without Fog of War", "Zero Company does not use fog of war, but long range does not guarantee line of sight to every target.", "An all-sniper squad is allowed, yet terrain and target visibility can lower its kill rate.", ["Check sight lines rather than relying on range alone.", "Use squad composition to solve the current scenario, not a universal range rule.", "Keep tools for objectives and close threats even in a marksman-heavy squad."]),
    ("weather-cosmetic-only", "Do Weather Effects Change Combat?", "Weather effects are cosmetic and do not reduce squad visibility or efficiency.", "Rain, dust or other visual weather should not be treated as a hidden accuracy or detection modifier.", ["Read tactical visibility from the game systems, not the mood of the scene.", "Do not create weather-resistance builds.", "Recheck accessibility and graphics settings separately from combat rules."]),
    ("outfits-no-gameplay-stats", "Do Outfits Affect Gameplay Stats?", "Outfits do not affect gameplay.", "Armor looks and clothing customization are cosmetic choices unless a separate equipment item explicitly provides mechanics after launch.", ["Choose outfits for appearance.", "Do not rank preorder cosmetics as combat upgrades.", "Keep cosmetic collection pages separate from equipment-stat guides."]),
    ("no-new-game-plus-at-launch", "Does Zero Company Have New Game Plus?", "Zero Company will not have New Game+ at launch.", "Subsequent playthroughs can unlock certain customization options, but that is not a carry-over campaign mode.", ["Plan a fresh campaign rather than a full inventory transfer.", "Use later playthroughs to see alternate squads and choices.", "Do not label unlockable cosmetics as New Game+ progression."]),
    ("mandalorian-armor-cly-only", "Who Can Wear Mandalorian Armor?", "Only Cly can wear the Mandalorian armor.", "Other Operators have extensive cosmetic choices, but the official Q&A sets this armor as a character-specific exception.", ["Do not promise Beskar-style equipment for custom recruits.", "Separate Cly's identity-linked armor from universal cosmetics.", "Treat the restriction as cosmetic unless official combat stats say otherwise."]),
    ("astromechs-unlock-early", "When Can You Build an Astromech Squad?", "Astromechs unlock fairly early, and a full team can be assembled once astromech recruitment is available.", "Hawks still occupies a required slot in story missions, while the remaining slots can be astromechs.", ["Use skirmishes for a completely unrestricted astromech lineup.", "On story missions, build the droid concept around Hawks's required presence.", "Wait for launch to rank exact droid utilities and recruitment costs."]),
    ("cannot-recruit-separatist-droids", "Can You Recruit Separatist Battle Droids?", "No. B1 and other Separatist droids cannot be recruited as Operators.", "The recruitable droid fantasy centers on astromechs rather than captured Separatist combat units.", ["Do not reserve roster slots for hacked B1 or B2 recruits.", "Treat enemy droids as hostile units unless a mission explicitly changes their state.", "Keep droid customization guides focused on confirmed astromech recruitment."]),
    ("no-specialized-call-ins", "Are There LAAT or Specialized Call-Ins?", "There are no specialized battlefield call-ins.", "Players should not plan around emergency LAAT support or a comparable once-per-mission rescue button.", ["Build support into the deployed squad.", "Protect Hawks because extraction failure is automatic mission failure.", "Use positioning and roster planning instead of assuming external reinforcement."]),
    ("custom-names-backstories", "Can Custom Operators Have Names and Backstories?", "Recruited Operators can have customized names and backstories.", "Nicknames are not earned over time through an XCOM-style nickname pool.", ["Create identity during recruitment rather than waiting for a random title.", "Separate narrative customization from combat progression.", "Expect Bonds and mission history to add context without automatically renaming the recruit."]),
    ("secondary-advanced-specializations", "Secondary and Advanced Specializations", "EA says equipment and playstyle can be shaped through secondary or advanced Specializations.", "This expands build identity beyond the eight standard starting roles, but the complete trees and unlock rules are not yet public.", ["Use standard Specializations as the confirmed baseline.", "Avoid publishing complete advanced-class lists before the game reveals them.", "Track cross-training and Bonds separately from specialization unlocks."]),
    ("bonds-cross-training-benefits", "How Bond Cross-Training Works", "Bonded units can unlock support abilities and cross-training benefits that share new skills and stats.", "Bonds are a tactical progression system, not a romance system.", ["Deploy recurring pairs when their battlefield roles complement each other.", "Evaluate shared skills as part of squad construction.", "Do not assume every relationship has the same thresholds or rewards before launch data is available."]),
]

MISSIONS = [
    ("operations-vs-tactical-missions", "Operations vs Tactical Missions", "Operations resolve on the Galaxy Map and can give instant rewards or unlock content; Tactical Missions deploy a squad into playable encounters.", "Both can expire, and each campaign cycle ends with a Tactical Mission selection."),
    ("sabotage-missions", "Sabotage Mission Type", "Sabotage is one of the general Tactical Mission types confirmed by EA.", "The exact targets vary, so this page focuses on the objective category rather than inventing a specific walkthrough."),
    ("combat-missions", "Combat Mission Type", "Combat missions are a confirmed general objective type.", "Squad composition, enemy faction and terrain can change the correct plan even when direct combat is the primary goal."),
    ("rescue-missions", "Rescue Mission Type", "Rescue missions are part of the confirmed Tactical Mission framework.", "These scenarios add an objective-protection problem beyond simply eliminating enemies."),
    ("retrieval-missions", "Retrieval Mission Type", "Retrieval missions are confirmed as a general Tactical Mission type.", "Movement budget, extraction routes and item control are likely to matter, while exact rules await launch verification."),
    ("hero-narrative-missions", "Hero-Centered Narrative Missions", "Some narrative missions tell unique stories centered on one hero.", "These authored scenarios should be distinguished from generic objective missions and map-level Operations."),
    ("galaxy-map-150-planets", "150+ Galaxy Map Planets Explained", "The Galaxy Map includes more than 150 planets where strategic Operations can potentially occur.", "Tactical Missions take place on more than a dozen unique planets with detailed playable environments; the two figures describe different layers."),
]

TACTICS = [
    ("ion-weapons-vs-separatist-droids", "Ion Weapons vs Separatist Droids", "EA recommends Ion weapons as a direct answer to Separatist droid forces.", "Use this as a faction-preparation clue, not as a complete damage chart before launch."),
    ("infinite-coil-kill-order", "Infinite Coil Target Priority", "Infinite Coil units have varied abilities, making kill order an important part of the encounter.", "Identify the unit that changes the fight before spending actions on the nearest target."),
    ("outlaws-anti-swarm-plan", "How to Handle Outlaw Numbers", "Outlaws can overwhelm the squad through numbers.", "Area control, safe positioning and action economy matter more than a single high-value target plan."),
    ("all-sniper-squad", "Can an All-Sniper Squad Work?", "The developers allow sniper-heavy strategies, but long range does not ensure visibility or a high kill rate.", "Plan objective tools and line-of-sight solutions around the map rather than assuming range solves every encounter."),
    ("force-push-into-overwatch", "Force Push and Overwatch Combo", "A confirmed developer tactic is pushing or pulling an enemy into a squadmate's Overwatch zone.", "The combo turns forced movement into a trigger for coordinated fire."),
    ("bull-rush-environmental-kill", "Bull-Rush Environmental Kills", "Enemies can be pushed into hazards such as shafts, water or cliffs for an instant kill.", "Check the destination and objective consequences before spending the action."),
    ("reinforcement-overwatch-zones", "Layering Overwatch on Reinforcements", "Multiple Overwatch zones can be placed over reinforcement areas.", "The tactic trades current actions for control of a predictable future entry point."),
    ("gunslinger-action-points-on-kill", "Gunslinger Extended-Turn Tactic", "A Gunslinger can gain action points on a kill, enabling an extended turn.", "Sequence a reliable finishing shot first when the extra AP can convert into movement, another attack or objective progress."),
    ("bonded-backup-fire", "Bonded Backup Fire", "A confirmed Bond tactic lets multiple bonded units fire on one target in a single action.", "This concentrates squad synergy into a priority-target burst rather than treating Bonds as passive story flavor."),
    ("destroy-enemy-cover", "Clearing Cover with Rockets and Explosives", "Rocket launchers and explosives can remove enemy cover.", "Opening the target can improve the rest of the squad's turn, so action order matters."),
    ("weaponized-astromech", "Weapon-Packed Astromech Build Concept", "Developers highlight astromechs using firebombs, thermal detonators and droid poppers.", "The example confirms an aggressive utility-droid concept without publishing a final item list or best build."),
    ("scan-cloaked-targets", "Scanning for Cloaked Targets", "A droid scan can reveal a cloaked target.", "Reserve detection tools when the enemy roster suggests concealment instead of spending every utility action on damage."),
]

NEWS = [
    ("full-voice-cast-revealed-july-23", "Zero Company Full Voice Cast Revealed", "StarWars.com published 15 character-and-actor credits on July 23, 2026.", "The announcement covers both Hawks voice options, authored Operators, Den support staff, the antagonist Kundri Fathom, Anakin Skywalker and newly named characters."),
    ("sdcc-2026-panel-guide", "Zero Company at SDCC 2026", "The July 25 panel was scheduled for 4:00 PM PT in Room 6BCF.", "The announced participants include narrative, Lucasfilm, development and cast representatives. This page records the official schedule without claiming panel revelations before publication."),
    ("four-weapon-classes-confirmed", "Four Weapon Classes Confirmed", "EA's July community Q&A confirmed four weapon classes with four to six cosmetic models in each.", "Names, stats and acquisition tables remain launch-data items, but the official structure is now suitable for the Wiki database."),
    ("150-planets-galaxy-map-confirmed", "Galaxy Map Has More Than 150 Planets", "EA confirmed over 150 potential Operation locations and more than a dozen Tactical Mission planets.", "The distinction prevents the strategic map count from being misreported as 150 fully playable tactical environments."),
    ("gordy-haab-composer-confirmed", "Gordy Haab Confirmed as Composer", "EA named Gordy Haab as the composer for Star Wars Zero Company.", "The credit is part of the July 21 official FAQ and expands the site's verified production and credits coverage."),
]

LOCALE = {
    "de": {
        "site": "Star Wars Zero Company Wiki Deutsch", "cast": "Besetzung & Sprecher", "home": "Start",
        "lead": "Offiziell bestätigte Sprecherzuordnung", "answer": "Direkte Antwort",
        "confirmed": "Bestätigt", "boundary": "Was diese Meldung nicht bestätigt",
        "source": "Quelle und Prüfstand", "profile": "Rollenprofil",
    },
    "ja": {
        "site": "Star Wars Zero Company 日本語Wiki", "cast": "キャスト・声優", "home": "ホーム",
        "lead": "公式発表済みの出演情報", "answer": "結論",
        "confirmed": "確認済み情報", "boundary": "未発表の範囲",
        "source": "情報源と確認日", "profile": "役柄プロフィール",
    },
}

CAST_LOCAL = {
    "de": {
        "intro": "{actor} spricht {character}. StarWars.com bestätigte diese Zuordnung am 23. Juli 2026.",
        "detail": "Die Seite trennt die offizielle Sprecherangabe klar von noch nicht veröffentlichten Fähigkeiten, Missionsrollen und Kampfwerten.",
        "limit": "Aus einer Sprecherliste lassen sich keine Spielbarkeit, Skillwerte oder Missionsauftritte ableiten. Solche Angaben werden erst nach einer weiteren offiziellen Meldung oder dem Release ergänzt.",
    },
    "ja": {
        "intro": "{character}の担当声優は{actor}です。StarWars.comが2026年7月23日に公式キャストとして発表しました。",
        "detail": "このページでは、公式の出演情報と、まだ公開されていないアビリティ、ミッションでの役割、戦闘数値を明確に分けています。",
        "limit": "キャスト一覧だけでは、操作可能か、どの任務に登場するか、能力値はいくつかを判断できません。追加の公式発表または製品版を確認して更新します。",
    },
}


def route_url(route: str) -> str:
    if route == "index.html":
        return SITE + "/"
    if route.endswith("/index.html"):
        return SITE + "/" + route[:-10]
    return SITE + "/" + route


def nav(locale="en"):
    if locale == "de":
        links = [("/de/", "Start"), ("/de/cast/", "Besetzung"), ("/de/questions/", "FAQ"), ("/de/database/", "Datenbank"), ("/de/news/", "News")]
    elif locale == "ja":
        links = [("/ja/", "ホーム"), ("/ja/cast/", "キャスト"), ("/ja/questions/", "FAQ"), ("/ja/database/", "データベース"), ("/ja/news/", "ニュース")]
    else:
        links = [("/", "Home"), ("/cast/", "Cast"), ("/mechanics/", "Mechanics"), ("/missions/", "Missions"), ("/tactics/", "Tactics"), ("/questions/", "FAQ"), ("/news/", "News")]
    return "".join(f'<a href="{u}">{escape(label)}</a>' for u, label in links)


def chrome(route, title, desc, body, locale="en", schema_type="Article", published=None):
    canonical = route_url(route)
    schema = {
        "@context": "https://schema.org", "@type": schema_type, "headline": title,
        "description": desc, "url": canonical, "inLanguage": locale,
        "dateModified": CHECKED, "isPartOf": {"@type": "WebSite", "name": "Star Wars Zero Company Wiki", "url": SITE + "/"},
    }
    if published:
        schema["datePublished"] = published
    if locale in ("de", "ja") and route.startswith(locale + "/cast/"):
        tail = route[len(locale) + 1:]
        en = route_url(tail)
        de = route_url("de/" + tail)
        ja = route_url("ja/" + tail)
        alternates = f'<link rel="alternate" hreflang="en" href="{en}"><link rel="alternate" hreflang="de" href="{de}"><link rel="alternate" hreflang="ja" href="{ja}"><link rel="alternate" hreflang="x-default" href="{en}">'
    elif route.startswith("cast/"):
        de = route_url("de/" + route)
        ja = route_url("ja/" + route)
        alternates = f'<link rel="alternate" hreflang="en" href="{canonical}"><link rel="alternate" hreflang="de" href="{de}"><link rel="alternate" hreflang="ja" href="{ja}"><link rel="alternate" hreflang="x-default" href="{canonical}">'
    else:
        alternates = ""
    site_name = LOCALE.get(locale, {}).get("site", "Star Wars Zero Company Wiki")
    html = f'''<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates}<link rel="icon" href="/favicon.ico"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale + '/' if locale != 'en' else ''}">{escape(site_name)}</a><nav class="nav">{nav(locale)}</nav></div></header><main class="wrap">{body}</main><footer><div class="wrap">Unofficial player guide · <a href="/about/sources-and-citations.html">Sources policy</a> · Updated July 25, 2026</div></footer></body></html>'''
    path = ROOT / route
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def source_block(url, label):
    return f'<section class="block"><h2>Source and evidence boundary</h2><p>The direct answer on this page is grounded in a first-party publication. It does not convert unreleased values, inferred story beats or marketing footage into confirmed gameplay data. Any development-stage value will be checked again against the launch build.</p><p class="source"><a href="{url}" rel="nofollow">{escape(label)}</a> · Fact-check: July 25, 2026</p></section>'


def build_cast():
    cards = []
    for idx, (slug, character, actor, role, note) in enumerate(CAST):
        route = f"cast/{slug}.html"
        title = f"{character} Voice Actor: {actor} | Zero Company Cast"
        desc = f"{actor} voices {character} in Star Wars Zero Company. See the official credit, confirmed role context and evidence limits."
        cards.append(f'<a class="card" href="/{route}"><strong>{escape(character)}</strong><br>{escape(actor)}<br><span class="mini">{escape(role)}</span></a>')
        if idx % 3 == 0:
            body = f'''<section class="hero"><div class="crumb">Official cast profile</div><h1>{escape(character)} — {escape(actor)}</h1><p class="lead"><strong>{escape(actor)}</strong> is officially credited as {escape(role)}.</p><span class="pill">Cast confirmed</span><span class="pill gold">July 23 announcement</span></section>
<section class="two"><div class="block"><h2>Quick credit</h2><table><tr><th>Character</th><td>{escape(character)}</td></tr><tr><th>Performer</th><td>{escape(actor)}</td></tr><tr><th>Credit status</th><td>Confirmed by StarWars.com</td></tr></table></div><div class="block"><h2>Role context</h2><p>{escape(note)}</p><p>The cast announcement establishes who performs the role. It does not replace the separate gameplay evidence needed for a build, recruitment or mission guide.</p></div></section>
<section class="block"><h2>What players can rely on</h2><p>The name-to-performer match is a first-party credit published ahead of San Diego Comic-Con 2026. {escape(character)} is therefore a verified part of the game's cast. The wording above stays within the official role context and does not add an invented biography.</p><ul><li>The performer credit is confirmed.</li><li>The described role context comes from EA or StarWars.com.</li><li>Unannounced combat statistics, appearance timing and mission outcomes are excluded.</li></ul></section>
<section class="block"><h2>Why this page is separate from a character guide</h2><p>Players searching for a voice actor need a direct production credit, while players searching for a build need abilities, equipment and verified tactical data. Keeping those intents separate prevents a short cast answer from being padded with speculative gameplay advice and prevents the operative database from being duplicated.</p></section>
{source_block(SW_CAST, "StarWars.com: Meet the Cast Before SDCC 2026")}'''
        elif idx % 3 == 1:
            body = f'''<section class="hero"><div class="crumb">Voice and performance record</div><h1>Who Voices {escape(character)}?</h1><p class="lead">{escape(actor)} performs {escape(character)} in Star Wars Zero Company.</p><span class="pill">First-party credit</span></section>
<section class="block"><h2>Credit record</h2><table><tr><th>Role</th><td>{escape(character)}</td></tr><tr><th>Actor</th><td>{escape(actor)}</td></tr><tr><th>Published</th><td>July 23, 2026</td></tr><tr><th>Source</th><td>StarWars.com cast announcement</td></tr></table></section>
<section class="two"><div class="block"><h2>Character classification</h2><p>{escape(role.capitalize())}.</p><p>{escape(note)}</p></div><div class="block"><h2>Evidence test</h2><ul><li>Identity and performer: verified.</li><li>Role context: limited to published descriptions.</li><li>Combat data and story outcome: not derived from the credit.</li></ul></div></section>
<section class="block"><h2>How this record will be maintained</h2><p>Credits rarely change, but role descriptions can become more precise as trailers, interviews and the final game add context. This record will link outward to an operative guide only when that separate page can answer recruitment, abilities and equipment with game evidence. Until then, the cast query receives a concise factual answer instead of a speculative build.</p></section>
{source_block(SW_CAST, "StarWars.com official voice-cast list")}'''
        else:
            body = f'''<section class="hero"><div class="crumb">Cast evidence file</div><h1>{escape(actor)} as {escape(character)}</h1><p class="lead">Official answer: {escape(actor)} is the credited performer for {escape(character)}.</p></section>
<section class="two"><div class="block"><h2>Identity snapshot</h2><p><strong>{escape(character)}</strong> is described as {escape(role)}.</p><p>{escape(note)}</p></div><div class="block"><h2>Production snapshot</h2><p>The credit appeared in the July 23 pre-SDCC cast feature. It verifies the pairing without assigning unannounced mechanics to the character.</p></div></section>
<section class="block"><h2>Confirmed / unresolved</h2><table><tr><th>Confirmed</th><td>{escape(actor)} performs {escape(character)}.</td></tr><tr><th>Supported context</th><td>{escape(note)}</td></tr><tr><th>Unresolved by this source</th><td>Exact screen time, mission sequence, skill values and every gameplay state.</td></tr></table></section>
<section class="block"><h2>Editorial boundary</h2><p>A cast database and a tactical database answer different questions. This URL owns the performer query. It will not repeat a generic character build, and it will not claim that appearing in the cast makes a story or support character deployable. That boundary keeps the answer useful even before launch.</p></section>
{source_block(SW_CAST, "StarWars.com: Zero Company cast reveal")}'''
        chrome(route, title, desc, body)
    hub_body = f'''<section class="hero"><div class="crumb">Production database</div><h1>Star Wars Zero Company Voice Cast</h1><p class="lead">The complete 15-credit cast list published by StarWars.com on July 23, 2026, with separate evidence notes for playable Operators, Den support characters and story roles.</p></section><section><h2>Character and performer directory</h2><div class="grid">{''.join(cards)}</div></section><section class="block"><h2>How to read the credits</h2><p>A voice credit confirms that a character appears in the production. It does not automatically mean that the character is recruitable, playable or present in every campaign. Hawks has two credited voice options because Hawks is customizable; support staff such as Runa, Bennic, Neesh and Meevo are associated with The Den; other newly named roles still await fuller official descriptions.</p></section>{source_block(SW_CAST, "StarWars.com official cast announcement")}'''
    chrome("cast/index.html", "Star Wars Zero Company Voice Cast — 15 Official Credits", "Browse all 15 officially announced Star Wars Zero Company character and voice actor credits, with role context and evidence boundaries.", hub_body, schema_type="CollectionPage")


def build_mechanics():
    cards = []
    for idx, (slug, title, answer, meaning, actions) in enumerate(MECHANICS):
        route = f"mechanics/{slug}.html"
        desc = f"{answer} Official July 2026 explanation, player impact and launch verification boundary."
        cards.append(f'<a class="card" href="/{route}"><strong>{escape(title)}</strong><br><span class="mini">{escape(answer)}</span></a>')
        action_html = "".join(f"<li>{escape(a)}</li>" for a in actions)
        if idx % 4 == 0:
            body = f'''<section class="hero"><div class="crumb">Confirmed mechanic</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(answer)}</strong></p><span class="pill">Official answer</span></section>
<section class="two"><div class="block"><h2>Direct answer</h2><p>{escape(answer)}</p></div><div class="block"><h2>Why it matters</h2><p>{escape(meaning)}</p></div></section>
<section class="block"><h2>Practical planning rules</h2><ol>{action_html}</ol><p>These rules translate the published mechanic into a pre-release planning checklist. They are not a tier list and do not assume unpublished costs, damage values or difficulty modifiers.</p></section>
<section class="block"><h2>Launch-day verification</h2><p>At release, this page will be checked against menus, tooltips and live mission behavior. If the development build changed, the dated official statement will remain in the update history while the direct answer is corrected for the shipping version.</p></section>
{source_block(EA_QA, "EA: Answering the Internet's Biggest Questions")}'''
        elif idx % 4 == 1:
            body = f'''<section class="hero"><div class="crumb">System answer</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p></section>
<section class="block"><h2>Rule in one sentence</h2><p><strong>{escape(answer)}</strong></p><p>{escape(meaning)}</p></section>
<section class="two"><div class="block"><h2>Decision checklist</h2><ul>{action_html}</ul></div><div class="block"><h2>Evidence boundary</h2><p>The official answer establishes the rule, but it does not publish every numeric modifier, menu label or difficulty exception. Those details remain outside this pre-release answer.</p></div></section>
<section class="block"><h2>Test case for August 27</h2><p>The shipping build will be checked in a repeatable state: record the relevant setting or tooltip, reproduce the behavior, note platform and difficulty, then update the direct answer only if the observed rule differs from EA's July statement.</p></section>
{source_block(EA_QA, "EA July 21 developer Q&A")}'''
        elif idx % 4 == 2:
            body = f'''<section class="hero"><div class="crumb">Verified gameplay note</div><h1>{escape(title)}</h1><p class="lead"><strong>Confirmed:</strong> {escape(answer)}</p></section>
<section class="two"><div class="block"><h2>Published fact</h2><p>{escape(answer)}</p></div><div class="block"><h2>Player consequence</h2><p>{escape(meaning)}</p></div></section>
<section class="block"><h2>Use the fact without overreaching</h2><p>Apply the following only where the official rule is relevant:</p><ol>{action_html}</ol><p>Do not turn a development answer into an invented best-in-slot list or pretend that unreleased balance values are settled.</p></section>
<section class="block"><h2>Change log policy</h2><p>If a day-one patch changes the behavior, the Wiki will preserve the July source date, add the tested version number and rewrite this page around the live rule. This makes the URL durable without freezing pre-release information forever.</p></section>
{source_block(EA_QA, "EA official community answers")}'''
        else:
            body = f'''<section class="hero"><div class="crumb">Mechanic fact sheet</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p><span class="pill gold">Checked July 25</span></section>
<section class="block"><h2>Fact → implication</h2><table><tr><th>Official fact</th><td>{escape(answer)}</td></tr><tr><th>Campaign or combat implication</th><td>{escape(meaning)}</td></tr></table></section>
<section class="two"><div class="block"><h2>Recommended interpretation</h2><ol>{action_html}</ol></div><div class="block"><h2>Excluded claims</h2><p>No hidden percentage, unrevealed ability name, final balance ranking or unsupported platform difference is added to this fact sheet.</p></div></section>
<section class="block"><h2>Verification target</h2><p>Release testing will capture the relevant interface and reproduce the rule in play. The page can then add exact steps, exceptions and screenshots while retaining the same single search intent.</p></section>
{source_block(EA_QA, "EA: official Zero Company Q&A")}'''
        chrome(route, f"{title} | Star Wars Zero Company", desc, body)
    hub = f'''<section class="hero"><div class="crumb">Evidence-led system guide</div><h1>Confirmed Mechanics Database</h1><p class="lead">Twenty mechanics newly documented from EA's July 21 community Q&A, organized as direct answers rather than speculative build templates.</p></section><section><h2>Roster, missions, equipment and customization</h2><div class="grid">{''.join(cards)}</div></section><section class="block"><h2>Quality rule</h2><p>Every leaf resolves one mechanic with a first-party answer, a player-facing consequence and a launch verification step. Unknown weapon names, percentages, skill trees and difficulty values are deliberately excluded.</p></section>{source_block(EA_QA, "EA official community Q&A")}'''
    chrome("mechanics/index.html", "Star Wars Zero Company Confirmed Mechanics Database", "Official answers for squad size, roster cap, weapons, Intel, customization, New Game Plus, weather, cutscenes and more.", hub, schema_type="CollectionPage")


def build_missions():
    cards = []
    for idx, (slug, title, answer, distinction) in enumerate(MISSIONS):
        route = f"missions/{slug}.html"
        cards.append(f'<a class="card" href="/{route}"><strong>{escape(title)}</strong><br><span class="mini">{escape(answer)}</span></a>')
        if idx % 3 == 0:
            body = f'''<section class="hero"><div class="crumb">Mission handbook</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(answer)}</strong></p></section>
<section class="block"><h2>Where it fits in the campaign</h2><p>{escape(distinction)}</p><p>Zero Company's cycle structure separates Galaxy Map decisions from deployed tactical encounters. That distinction determines whether a choice spends Intel and resolves strategically or sends a selected squad into a playable objective.</p></section>
<section class="two"><div class="block"><h2>Prepare before selection</h2><ul><li>Check expiry and story-critical timing.</li><li>Compare the objective with the current roster.</li><li>Reserve resources for the next required mission.</li></ul></div><div class="block"><h2>Do not assume yet</h2><ul><li>No exact reward table is published.</li><li>No universal turn limit is claimed.</li><li>No invented map or planet is assigned to this type.</li></ul></div></section>
<section class="block"><h2>Post-launch data to add</h2><p>The final guide will record objective rules, failure states, reward ranges, map variants, enemy pools and known bugs from verified gameplay. Until then, the page answers the mission-type query with only confirmed structure.</p></section>
{source_block(EA_QA, "EA official mission-type explanation")}'''
        elif idx % 3 == 1:
            body = f'''<section class="hero"><div class="crumb">Objective file</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p><span class="pill">Confirmed category</span></section>
<section class="two"><div class="block"><h2>Definition</h2><p>{escape(answer)}</p><p>{escape(distinction)}</p></div><div class="block"><h2>Campaign position</h2><p>Tactical Missions follow squad deployment, while map-level Operations can resolve instantly, spend Intel or unlock later opportunities. Expiry and obligatory story beats prevent unlimited delay.</p></div></section>
<section class="block"><h2>Selection questions</h2><ol><li>Does the objective reward match the current campaign need?</li><li>Which four-Operator core covers movement, survival and the objective?</li><li>Will choosing it allow another valuable event to expire?</li><li>Is a hero or Hawks mandatory for this authored scenario?</li></ol></section>
<section class="block"><h2>Why there is no fabricated walkthrough</h2><p>A mission category can be confirmed before its maps and rules are public. This page owns the category query now; exact steps, rewards and failure triggers will be added only after a real instance can be played and documented.</p></section>
{source_block(EA_QA, "EA mission framework answer")}'''
        else:
            body = f'''<section class="hero"><div class="crumb">Campaign objective database</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(answer)}</strong></p></section>
<section class="block"><h2>Confirmed scope</h2><table><tr><th>Category</th><td>{escape(title)}</td></tr><tr><th>Official description</th><td>{escape(answer)}</td></tr><tr><th>Important distinction</th><td>{escape(distinction)}</td></tr></table></section>
<section class="two"><div class="block"><h2>Before deployment</h2><ul><li>Read the objective, expiry and story status.</li><li>Match the roster to the required interaction.</li><li>Plan a safe route for Hawks when he is mandatory.</li></ul></div><div class="block"><h2>After release</h2><ul><li>Record objective variants.</li><li>Measure reward and failure rules.</li><li>Add screenshots only where they clarify the route.</li></ul></div></section>
<section class="block"><h2>Single-intent rule</h2><p>This URL explains one official mission concept. It does not copy a generic combat guide, list fictional mission names or compete with a future walkthrough for a specific operation.</p></section>
{source_block(EA_QA, "EA July mission details")}'''
        chrome(route, f"{title} | Zero Company Mission Guide", f"{answer} Learn how it fits the campaign, how to prepare and which details remain launch-dependent.", body)
    body = f'''<section class="hero"><div class="crumb">Campaign structure</div><h1>Operations and Mission Types</h1><p class="lead">A source-grounded guide to Galaxy Map Operations, Tactical Missions, Sabotage, Combat, Rescue, Retrieval and hero-centered narrative missions.</p></section><div class="grid">{''.join(cards)}</div>{source_block(EA_QA, "EA official community Q&A")}'''
    chrome("missions/index.html", "Star Wars Zero Company Mission Types and Operations", "Browse confirmed mission categories, Operations versus Tactical Missions and the 150-plus planet Galaxy Map distinction.", body, schema_type="CollectionPage")


def build_tactics():
    cards = []
    for idx, (slug, title, answer, use) in enumerate(TACTICS):
        route = f"tactics/{slug}.html"
        cards.append(f'<a class="card" href="/{route}"><strong>{escape(title)}</strong><br><span class="mini">{escape(answer)}</span></a>')
        if idx % 4 == 0:
            body = f'''<section class="hero"><div class="crumb">Developer-confirmed tactic</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(answer)}</strong></p></section>
<section class="two"><div class="block"><h2>Setup</h2><p>{escape(use)}</p><p>Read the battlefield state first: objective, remaining actions, target order, line of sight and the next Operator's options all affect whether the tactic creates value.</p></div><div class="block"><h2>Execution check</h2><ol><li>Identify the specific problem this tactic solves.</li><li>Confirm that the required unit, item or position is available.</li><li>Sequence the enabling action before the payoff.</li><li>Leave a safe end position or objective path.</li></ol></div></section>
<section class="block"><h2>Confirmed example, not a universal best build</h2><p>EA presented this as an example of the game's tactical flexibility. The page therefore explains the interaction without inventing damage, range, cooldown or drop-rate values. A tactic can be valid while still depending on map geometry, enemy faction and mission objective.</p></section>
<section class="block"><h2>What launch testing will measure</h2><p>After release, testing will add exact action costs, valid targets, line-of-sight rules, failure conditions and representative screenshots. Any ranking will be based on repeatable results rather than trailer impressions.</p></section>
{source_block(EA_QA, "EA developer strategy examples")}'''
        elif idx % 4 == 1:
            body = f'''<section class="hero"><div class="crumb">Tactical interaction</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p><span class="pill">Developer example</span></section>
<section class="block"><h2>Battlefield idea</h2><p>{escape(use)}</p><p>The tactic is strongest when it solves the active objective or removes a threat that would otherwise consume more squad actions.</p></section>
<section class="two"><div class="block"><h2>Sequence</h2><ol><li>Locate the enabling unit, item or terrain feature.</li><li>Check range and line of sight.</li><li>Act with the enabler before the damage or control unit.</li><li>Re-evaluate the board before spending the remaining AP.</li></ol></div><div class="block"><h2>Abort conditions</h2><ul><li>The setup exposes Hawks to mission failure.</li><li>The target is irrelevant to the objective.</li><li>The action cost blocks extraction or rescue.</li></ul></div></section>
<section class="block"><h2>Evidence limit</h2><p>EA confirms the interaction as a viable example, not a guaranteed best move on every map. Exact numerical efficiency will be measured after launch rather than reverse-engineered from footage.</p></section>
{source_block(EA_QA, "EA tactical examples and faction answers")}'''
        elif idx % 4 == 2:
            body = f'''<section class="hero"><div class="crumb">Combat lab</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(answer)}</strong></p></section>
<section class="two"><div class="block"><h2>Problem</h2><p>{escape(use)}</p></div><div class="block"><h2>Confirmed response</h2><p>{escape(answer)}</p></div></section>
<section class="block"><h2>Four checks before committing</h2><table><tr><th>Objective</th><td>Does the action advance the mission rather than only add damage?</td></tr><tr><th>Order</th><td>Will another Operator improve the setup first?</td></tr><tr><th>Safety</th><td>Where will the acting unit finish?</td></tr><tr><th>Resource</th><td>Are AP, Advantage or consumables better reserved?</td></tr></table></section>
<section class="block"><h2>Data still needed</h2><p>The published example does not provide every cost, range, immunity or difficulty modifier. The launch guide will add only values reproduced in the shipping build and will keep platform or patch differences dated.</p></section>
{source_block(EA_QA, "EA official strategy Q&A")}'''
        else:
            body = f'''<section class="hero"><div class="crumb">Field doctrine</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p></section>
<section class="block"><h2>Doctrine</h2><p>{escape(use)}</p><p>Use the interaction as a tool for a defined battlefield state, not as a fixed opening for every mission.</p></section>
<section class="two"><div class="block"><h2>Good fit</h2><ul><li>The required target or terrain is present.</li><li>The squad can afford the enabling action.</li><li>The payoff improves survival or objective tempo.</li></ul></div><div class="block"><h2>Poor fit</h2><ul><li>Setup costs more actions than it saves.</li><li>Line of sight or positioning breaks the chain.</li><li>A timed objective demands immediate movement.</li></ul></div></section>
<section class="block"><h2>Test protocol</h2><p>On release, reproduce the tactic against several targets, record AP and resource costs, note invalid targets and compare the result with a simpler alternative. Only then should the Wiki call it efficient or assign a build priority.</p></section>
{source_block(EA_QA, "EA developer-favorite tactics")}'''
        chrome(route, f"{title} | Zero Company Tactics", f"{answer} See the setup, execution sequence, limits and launch-test checklist.", body)
    body = f'''<section class="hero"><div class="crumb">Tactical field manual</div><h1>Official Strategy Examples</h1><p class="lead">Twelve distinct tactics and faction counters taken from developer answers, each separated from unsupported damage numbers and pre-release tier claims.</p></section><div class="grid">{''.join(cards)}</div>{source_block(EA_QA, "EA official community Q&A")}'''
    chrome("tactics/index.html", "Star Wars Zero Company Tactics and Confirmed Combos", "Developer-confirmed tactics for faction counters, Overwatch, forced movement, Bonds, explosives, astromechs and cloaked targets.", body, schema_type="CollectionPage")


def build_news():
    cards = []
    for slug, title, answer, detail in NEWS:
        route = f"news/latest/{slug}.html"
        cards.append(f'<a class="card" href="/{route}"><time>July 2026</time><br><strong>{escape(title)}</strong><br><span class="mini">{escape(answer)}</span></a>')
        source = SW_CAST if "cast" in slug or "sdcc" in slug else EA_QA
        body = f'''<article><section class="hero"><div class="crumb">Verified news brief</div><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p><span class="pill">Source checked</span></section>
<section class="block"><h2>What changed</h2><p>{escape(detail)}</p><p>This brief records a newly published fact and links to permanent database pages where the subject can be maintained after the announcement leaves the news cycle.</p></section>
<section class="two"><div class="block"><h2>Confirmed now</h2><p>{escape(answer)}</p></div><div class="block"><h2>Still awaiting launch data</h2><p>Unpublished statistics, acquisition tables and mission outcomes are not inferred from the announcement. The article will be updated only when a dated first-party source or verified game build supplies them.</p></div></section>
{source_block(source, "Official July 2026 source")}</article>'''
        chrome(route, f"{title} | Zero Company News", f"{answer} Read the verified change, player impact and remaining evidence limits.", body, schema_type="NewsArticle", published="2026-07-23" if source == SW_CAST else "2026-07-21")
    body = f'''<section class="hero"><div class="crumb">July 2026 updates</div><h1>Latest Verified Zero Company Updates</h1><p class="lead">Five non-duplicative briefs covering the official cast, SDCC schedule, weapon structure, Galaxy Map scale and composer credit.</p></section><div class="grid">{''.join(cards)}</div>{source_block(EA_QA, "EA and StarWars.com official updates")}'''
    chrome("news/latest/index.html", "Latest Star Wars Zero Company News — July 2026", "Verified July 2026 updates for the full cast, SDCC, four weapon classes, 150-plus planets and composer Gordy Haab.", body, schema_type="CollectionPage")


def build_localized_cast():
    for locale in ("de", "ja"):
        copy = LOCALE[locale]
        local = CAST_LOCAL[locale]
        cards = []
        for idx, (slug, character, actor, role, note) in enumerate(CAST):
            route = f"{locale}/cast/{slug}.html"
            intro = local["intro"].format(actor=actor, character=character)
            if locale == "de":
                title = f"{character} Sprecher: {actor} | Zero Company"
                desc = f"{actor} spricht {character} in Star Wars Zero Company. Offizielle Besetzung, Rollenhinweis und klarer Prüfstand."
                role_text = f"Die offizielle englische Rollenbeschreibung ordnet {character} als {role} ein. {note}"
                use_text = "Diese Zuordnung hilft bei der Suche nach der Besetzung und bleibt bewusst getrennt von einem Build-Guide. Eine Sprecherangabe bestätigt keine Skillwerte, Ausrüstung oder Spielbarkeit. Auch Erscheinungszeitpunkt, Missionsfolge und mögliche Storyfolgen werden nicht aus der Rollenliste abgeleitet."
            else:
                title = f"{character}の声優は{actor}｜Zero Company"
                desc = f"Star Wars Zero Companyで{character}を演じるのは{actor}です。公式キャスト、役柄、未発表情報の境界を整理します。"
                role_text = f"公式英語資料では、{character}は{role}として紹介されています。{note}"
                use_text = "声優を調べる検索意図と、ビルド・攻略を調べる検索意図を分けています。出演情報だけからスキル数値、装備、操作可能かどうかを推測しません。"
            cards.append(f'<a class="card" href="/{route}"><strong>{escape(character)}</strong><br>{escape(actor)}</a>')
            if idx % 3 == 0:
                body = f'''<section class="hero"><div class="crumb">{escape(copy["profile"])}</div><h1>{escape(character)} — {escape(actor)}</h1><p class="lead"><strong>{escape(intro)}</strong></p><span class="pill">{escape(copy["confirmed"])}</span></section>
<section class="two"><div class="block"><h2>{escape(copy["answer"])}</h2><p>{escape(intro)}</p><p>{escape(role_text)}</p></div><div class="block"><h2>{escape(copy["lead"])}</h2><table><tr><th>Character</th><td>{escape(character)}</td></tr><tr><th>Actor</th><td>{escape(actor)}</td></tr><tr><th>Status</th><td>StarWars.com · 23 July 2026</td></tr></table></div></section>
<section class="block"><h2>{escape(copy["boundary"])}</h2><p>{escape(local["limit"])}</p><p>{escape(use_text)}</p></section>
<section class="block"><h2>{escape(copy["source"])}</h2><p>{escape(local["detail"])}</p><p class="source"><a href="{SW_CAST}" rel="nofollow">StarWars.com official cast announcement</a> · 2026-07-25</p></section>'''
            elif idx % 3 == 1:
                body = f'''<section class="hero"><div class="crumb">{escape(copy["lead"])}</div><h1>{escape(character)} / {escape(actor)}</h1><p class="lead">{escape(intro)}</p></section>
<section class="block"><h2>{escape(copy["confirmed"])}</h2><table><tr><th>Role</th><td>{escape(character)}</td></tr><tr><th>Voice</th><td>{escape(actor)}</td></tr><tr><th>Announcement</th><td>23 July 2026</td></tr></table><p>{escape(role_text)}</p></section>
<section class="two"><div class="block"><h2>{escape(copy["answer"])}</h2><p>{escape(use_text)}</p></div><div class="block"><h2>{escape(copy["boundary"])}</h2><p>{escape(local["limit"])}</p></div></section>
<section class="block"><h2>{escape(copy["source"])}</h2><p>{escape(local["detail"])}</p><p class="source"><a href="{SW_CAST}" rel="nofollow">StarWars.com cast reveal</a> · 2026-07-25</p></section>'''
            else:
                body = f'''<section class="hero"><div class="crumb">{escape(copy["cast"])}</div><h1>{escape(actor)} — {escape(character)}</h1><p class="lead"><strong>{escape(intro)}</strong></p></section>
<section class="two"><div class="block"><h2>{escape(copy["profile"])}</h2><p>{escape(role_text)}</p></div><div class="block"><h2>{escape(copy["answer"])}</h2><p>{escape(intro)}</p><p>{escape(use_text)}</p></div></section>
<section class="block"><h2>{escape(copy["boundary"])}</h2><table><tr><th>{escape(copy["confirmed"])}</th><td>{escape(actor)} / {escape(character)}</td></tr><tr><th>{escape(copy["boundary"])}</th><td>{escape(local["limit"])}</td></tr></table></section>
<section class="block"><h2>{escape(copy["source"])}</h2><p>{escape(local["detail"])}</p><p class="source"><a href="{SW_CAST}" rel="nofollow">StarWars.com · official cast list</a> · 2026-07-25</p></section>'''
            chrome(route, title, desc, body, locale=locale)
        if locale == "de":
            title = "Star Wars Zero Company Besetzung und deutsche Sprecher"
            desc = "Alle 15 offiziell bestätigten Figuren und Sprecher aus der StarWars.com-Ankündigung vom 23. Juli 2026."
            intro = "Die vollständige, offiziell veröffentlichte Besetzung umfasst beide Hawks-Stimmen, Frontkämpfer, Den-Mitarbeiter und Storyfiguren."
            method = "Jeder Eintrag beantwortet zuerst die konkrete Sprecherfrage und erklärt danach, welcher Teil der Rolle offiziell beschrieben ist. Zwei getrennte Hawks-Stimmen gehören zum anpassbaren Hauptcharakter. Eine Nennung in der Besetzung bedeutet dagegen nicht automatisch, dass eine Figur als Operator rekrutiert oder im Kampf gesteuert werden kann. Deshalb bleiben Besetzungsseiten, Charakterdossiers und spätere Build-Guides als unterschiedliche Suchintentionen getrennt. Neue Angaben aus dem SDCC-Panel oder der veröffentlichten Spielversion werden mit Datum und Primärquelle ergänzt."
        else:
            title = "Star Wars Zero Company 声優・キャスト一覧"
            desc = "2026年7月23日にStarWars.comが発表した15組のキャラクターと担当声優を一覧化。"
            intro = "カスタマイズ可能なHawksの2種類の声、固有オペレーター、The Denの支援キャラクター、物語の登場人物を公式情報に基づいて整理します。"
            method = "各ページは最初に「誰が演じるか」を直接回答し、その後に公式資料で確認できる役柄だけを整理しています。Hawksの2名は別キャラクターではなく、カスタマイズ可能な主人公の音声選択肢です。一方、キャストに名前があるだけでは、戦闘で操作できる、仲間として加入する、特定のミッションに登場すると判断できません。そのため、声優ページ、キャラクター資料、発売後のビルド攻略を別の検索意図として分離しました。SDCCや製品版で新情報が確認できた場合は、確認日と一次情報を付けて更新します。"
        body = f'''<section class="hero"><div class="crumb">{escape(copy["cast"])}</div><h1>{escape(title)}</h1><p class="lead">{escape(intro)}</p></section><div class="grid">{''.join(cards)}</div><section class="block"><h2>{escape(copy["confirmed"])}</h2><p>{escape(method)}</p></section><section class="block"><h2>{escape(copy["boundary"])}</h2><p>{escape(local["limit"])}</p></section>'''
        chrome(f"{locale}/cast/index.html", title, desc, body, locale=locale, schema_type="CollectionPage")


def add_hub_links():
    targets = {
        ROOT / "index.html": '<a class="card" href="/mechanics/"><strong>Confirmed Mechanics</strong><br><span class="mini">20 official July answers</span></a><a class="card" href="/cast/"><strong>Voice Cast</strong><br><span class="mini">15 official credits</span></a><a class="card" href="/missions/"><strong>Mission Types</strong><br><span class="mini">Operations and objectives</span></a><a class="card" href="/tactics/"><strong>Tactics Lab</strong><br><span class="mini">Developer-confirmed combos</span></a>',
        ROOT / "operatives/index.html": '<a class="card" href="/cast/"><strong>Official Voice Cast</strong><br><span class="mini">Match 15 characters to performers</span></a>',
        ROOT / "official-systems/index.html": '<a class="card" href="/mechanics/"><strong>July Mechanics Database</strong><br><span class="mini">Roster, weapons, Intel and customization</span></a>',
        ROOT / "operations/index.html": '<a class="card" href="/missions/"><strong>Confirmed Mission Types</strong><br><span class="mini">Operations, Tactical Missions and objectives</span></a>',
        ROOT / "guides/index.html": '<a class="card" href="/tactics/"><strong>Developer Strategy Examples</strong><br><span class="mini">12 source-grounded tactical interactions</span></a>',
    }
    for path, cards in targets.items():
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig")
        if "data-round11-quality" in text:
            continue
        section = f'<section data-round11-quality="true"><h2>July 2026 Verified Expansion</h2><div class="grid">{cards}</div></section>'
        text = text.replace("</main>", section + "</main>", 1)
        path.write_text(text, encoding="utf-8")


def main():
    build_cast()
    build_mechanics()
    build_missions()
    build_tactics()
    build_news()
    build_localized_cast()
    add_hub_links()
    print("Round 11 generated 96 source-grounded HTML pages")


if __name__ == "__main__":
    main()
