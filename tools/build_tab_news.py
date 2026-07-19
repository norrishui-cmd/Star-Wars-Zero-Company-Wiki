#!/usr/bin/env python3
"""Build five source-grounded news briefs for every primary content tab."""

from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = "2026-07-19"
ADS_META = '<meta name="google-adsense-account" content="ca-pub-9505220977121599">'
ADS_SCRIPT = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script>'
SOURCES = {
    "gameplay": ("EA gameplay overview", "June 9, 2026", "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"),
    "preorder": ("EA preorder announcement", "June 5, 2026", "https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company"),
    "reveal": ("EA reveal recap", "April 21, 2025", "https://www.ea.com/games/starwars/zero-company/news/introducing-star-wars-zero-company"),
    "buy": ("EA purchase page", "checked July 19, 2026", "https://www.ea.com/games/starwars/zero-company/buy"),
}

# slug, title, direct answer, player impact, source key
CATEGORIES = {
"operatives": ("Operatives", "/operatives/", "Confirmed character and squad-management reporting", [
 ("hawks-customization-explained", "Hawks Customization Extends Beyond Appearance", "EA says players can customize Hawks' appearance and combat Specialization.", "Hawks is designed as a player-shaped commander rather than a fixed class selection.", "gameplay"),
 ("seven-authored-operatives-profiled", "Seven Authored Operatives Now Have Official Profiles", "Hawks, Trick, Tel-Rea, Cly, Luco, Jae and Kabb are described in EA's gameplay overview.", "Players can begin planning role coverage without relying on invented launch statistics.", "gameplay"),
 ("custom-operators-confirmed", "Custom Operators Can Join the Authored Cast", "The Recruitment facility creates custom Operators alongside authored squad members.", "Campaign teams can mix story characters with player-created recruits.", "gameplay"),
 ("three-injuries-permadeath-rule", "Three Injuries Trigger Permanent Death on Standard Difficulty", "EA states that a third Injury kills an Operator permanently on the standard setting.", "Roster depth and Medbay decisions carry campaign consequences.", "gameplay"),
 ("bonds-unlock-combat-synergies", "Squad Bonds Unlock Combat Synergies", "Deploying Operators together develops bonds that can unlock new combat synergies.", "Team composition has a relationship layer beyond raw combat roles.", "reveal"),
]),
"classes": ("Specializations", "/classes/", "Official Specialization and progression reporting", [
 ("eight-standard-specializations", "EA Names All Eight Standard Specializations", "Assault, Gunslinger, Heavy, Medic, Scoundrel, Scout, Sharpshooter and Soldier are the eight standard roles.", "Players now have an official role vocabulary without speculative tier labels.", "gameplay"),
 ("ability-structure-confirmed", "Every Standard Specialization Shares a Three-Part Ability Structure", "Each standard role has an Ultimate, a Standard Ability and a Passive.", "Comparisons should focus on function until exact launch values are published.", "gameplay"),
 ("personnel-specialization-changes", "The Personnel Facility Allows Specialization Changes", "Most Operators can change Specialization through Personnel.", "Campaign mistakes may be recoverable without replacing the entire character.", "gameplay"),
 ("focus-points-upgrade-talents", "Focus Points Upgrade Talents, Abilities and Passives", "EA links Focus Points to individual progression choices.", "Long-term builds will involve more than selecting a starting role.", "gameplay"),
 ("specializations-not-tier-list", "Why the Official Specialization Reveal Is Not a Tier List", "EA described battlefield jobs but did not publish competitive rankings or final balance values.", "Pre-release class guidance should explain decisions instead of inventing a meta.", "gameplay"),
]),
"builds": ("Loadouts", "/builds/", "Equipment, progression and loadout reporting", [
 ("armory-equips-weapons-armor", "The Armory Manages Weapons and Armor", "EA identifies the Armory as the place to equip weapons and armor.", "Loadout planning is tied directly to The Den's facility loop.", "gameplay"),
 ("upgrade-facility-improves-gear", "A Dedicated Upgrade Facility Improves Gear", "The Upgrade facility raises the power of equipment used by the squad.", "Campaign resources will compete between immediate gear gains and other base priorities.", "gameplay"),
 ("operator-loadouts-customizable", "Custom Operators Include Editable Loadouts and Abilities", "EA says custom characters can be tailored by appearance, loadout and abilities.", "Build experimentation is supported for player-created squad members.", "gameplay"),
 ("specialization-changes-affect-builds", "Specialization Changes Add a Respec Layer to Loadouts", "Most Operators can change standard Specialization at Personnel.", "A useful build guide must separate character identity from the role currently equipped.", "gameplay"),
 ("launch-values-await-verification", "Launch Testing Will Decide the First Reliable Loadouts", "Named weapons, exact damage values and final upgrade costs remain unpublished.", "Players should treat pre-release build rankings as provisional rather than factual.", "gameplay"),
]),
"operations": ("Operations", "/operations/", "Mission, campaign-map and operation reporting", [
 ("mission-cycles-create-time-pressure", "Mission Cycles Create Strategic Time Pressure", "The HoloTable presents missions in Cycles instead of an unlimited static list.", "Choosing one operation may change what remains available later.", "gameplay"),
 ("missions-operations-investigations", "EA Confirms Operations, Investigations and Other Mission Types", "The campaign includes tactical operations, investigations and additional missions.", "The mission layer is broader than a sequence of identical combat maps.", "preorder"),
 ("galaxy-map-shows-consequences", "The Galaxy Map Shows the Consequences of Player Choices", "EA calls its galaxy map the largest and most interactive yet in a Star Wars game.", "Strategic decisions are intended to be visible beyond a single battlefield.", "reveal"),
 ("handcrafted-maps-random-elements", "Handcrafted Maps Include Randomized Elements", "EA describes authored battlefields with changing enemy and objective variables.", "Route knowledge may help, but missions should not play identically every campaign.", "gameplay"),
 ("august-27-campaign-start", "Zero Company's Campaign Begins August 27", "The game launches August 27, 2026 on PC, PlayStation 5 and Xbox Series X|S.", "Operation walkthroughs can be verified against the shipped build from launch day.", "preorder"),
]),
"hostiles": ("Hostiles", "/hostiles/", "Enemy, threat and encounter reporting", [
 ("infinite-coil-main-threat", "The Infinite Coil Emerges as Zero Company's Central Threat", "Kundri Fathom leads a Separatist-aligned cult called the Infinite Coil.", "The campaign's enemies extend beyond familiar Clone Wars battle lines.", "gameplay"),
 ("kundri-fathom-target", "Kundri Fathom Is the Squad's Primary Named Target", "Zero Company is tasked with tracking and stopping Kundri Fathom.", "Enemy reporting should distinguish confirmed story leadership from battlefield unit speculation.", "gameplay"),
 ("enemy-behavior-randomized", "Randomized Enemy Elements May Change Repeat Encounters", "EA says handcrafted maps incorporate randomized enemy and objective elements.", "Counter guides will need encounter-specific testing rather than one fixed script.", "gameplay"),
 ("sabotage-shapes-threat-response", "Sabotage Is Part of the Tactical Threat Model", "Official gameplay materials show objectives that go beyond eliminating every enemy.", "Players may need to prioritize mission devices and timers over damage alone.", "gameplay"),
 ("enemy-stats-launch-boundary", "Exact Enemy Stats Remain a Launch-Day Verification Task", "EA has shown combat threats without publishing a complete enemy database.", "Reliable counters require shipped-game health, armor, behavior and difficulty testing.", "gameplay"),
]),
"guides": ("Guides", "/guides/", "Player-guide and mechanics reporting", [
 ("three-action-points-per-turn", "Every Operator Receives Three Action Points per Turn", "Movement, attacks and abilities draw from three AP for each Operator.", "Beginners should plan the final position before spending the last action point.", "gameplay"),
 ("advantage-cap-ten", "Squad Advantage Is Capped at Ten", "Attacks build a shared Advantage resource up to a maximum of ten.", "Teams must decide when to spend the resource instead of hoarding beyond the cap.", "gameplay"),
 ("single-player-status", "Zero Company Is Confirmed as a Single-Player Game", "EA consistently describes the title as a single-player turn-based tactics game.", "Players should not expect cooperative or competitive multiplayer at launch.", "preorder"),
 ("cover-and-flanking-principles", "Cover and Positioning Sit at the Center of Combat", "Official footage and role descriptions emphasize movement, cover and exposing targets.", "Early guides can teach decision principles even before final damage tables exist.", "gameplay"),
 ("standard-difficulty-permadeath", "Standard Difficulty Includes Operator Permadeath", "A third Injury permanently kills an Operator on the standard setting.", "Recovery, roster depth and risk management belong in every beginner guide.", "gameplay"),
]),
"content-map": ("Content Map", "/content-map/", "Wiki coverage and verified-content reporting", [
 ("verified-content-map-expanded", "Verified Content Map Expands Around Official Gameplay Details", "The wiki now separates sourced entities and systems from launch-day placeholders.", "Readers can identify which pages contain confirmed answers and which await testing.", "gameplay"),
 ("eight-class-cluster-complete", "All Eight Standard Specializations Receive Dedicated Coverage", "Every standard role named by EA now has its own source-grounded guide.", "The class cluster no longer depends on invented roles or tier rankings.", "gameplay"),
 ("den-facility-cluster-live", "The Den Facility Cluster Covers Nine Confirmed Functions", "Command Center, HoloTable, Recruitment, Personnel, Armory, Upgrade, Medbay, Customization and Memorial have focused pages.", "Base-management searches now lead to distinct, non-overlapping explanations.", "gameplay"),
 ("multilingual-layer-live", "German and Japanese Core Guides Are Now Connected", "The site has localized release, platform, language, gameplay and Specialization pages.", "Reciprocal hreflang helps search engines serve the correct language version.", "buy"),
 ("launch-capture-plan", "Launch Coverage Will Prioritize Verifiable Mission and Item Data", "The content plan reserves detailed walkthrough expansion for the shipped game.", "This prevents empty database pages from entering the sitemap before they can answer players.", "gameplay"),
]),
"official-systems": ("Official Systems", "/official-systems/", "Verified mechanics and campaign-system reporting", [
 ("three-ap-system-confirmed", "The Three-AP Turn Structure Is Official", "Each Operator starts a turn with three action points.", "Movement, attacks and abilities create a visible action-economy puzzle.", "gameplay"),
 ("advantage-shared-resource", "Advantage Is Shared Across the Entire Squad", "Attacking builds a common meter rather than a separate resource for each character.", "Ultimate timing becomes a team decision.", "gameplay"),
 ("focus-trees-progression", "Focus Trees Shape Operator Progression", "Focus Points improve Talents, Abilities and Passives.", "Progression choices can specialize characters beyond their current battlefield role.", "gameplay"),
 ("cycle-based-missions", "The HoloTable Organizes Missions into Cycles", "Mission availability advances through a Cycle structure.", "Strategic opportunity cost is part of campaign planning.", "gameplay"),
 ("injury-recovery-loop", "Injuries Connect Tactical Combat to the Medbay", "Wounded Operators return to a campaign recovery system, with death on the third Injury at standard difficulty.", "Damage can affect several future missions rather than ending at the results screen.", "gameplay"),
]),
"facilities": ("The Den", "/facilities/", "Home-base and facility reporting", [
 ("nine-den-functions-detailed", "EA Details Nine Functions Inside The Den", "The official overview identifies command, mission, recruitment, personnel, gear, medical and memorial functions.", "Base upgrades form a second decision layer between tactical missions.", "gameplay"),
 ("holotable-controls-missions", "The HoloTable Is the Campaign Mission Interface", "Players review mission Cycles and choose deployments through the HoloTable.", "The room connects base planning directly to field operations.", "gameplay"),
 ("recruitment-builds-custom-operators", "Recruitment Creates Custom Operators", "The Recruitment facility supports player-created squad members.", "Roster replacement and experimentation have a dedicated campaign home.", "gameplay"),
 ("medbay-manages-injuries", "The Medbay Manages a High-Stakes Injury System", "Medical recovery matters because three Injuries cause permanent death on standard difficulty.", "Facility investment may protect experienced Operators across the campaign.", "gameplay"),
 ("memorial-records-fallen", "The Memorial Records Operators Lost in the Campaign", "EA includes a dedicated place for fallen squad members inside The Den.", "Permadeath is reflected in the base and narrative memory, not only a roster deletion.", "gameplay"),
]),
"lore": ("Story & Lore", "/lore/", "Story, faction and location reporting", [
 ("war-beneath-the-war", "Zero Company Fights a War Beneath the Clone Wars", "The original story follows a shadow conflict during the twilight of the Clone Wars.", "The campaign can visit familiar history while telling a separate covert story.", "gameplay"),
 ("kundri-fathom-infinite-coil", "Kundri Fathom Leads the Infinite Coil", "The principal named antagonist heads a Separatist-aligned cult.", "The threat gives Zero Company a target distinct from the Republic-Separatist frontline.", "gameplay"),
 ("ring-of-kafrene-opening", "The Ring of Kafrene Frames an Early Story Operation", "Official materials place Zero Company activity at the Ring of Kafrene.", "The campaign connects Clone Wars events with locations recognized from wider Star Wars canon.", "gameplay"),
 ("vandor-and-mapuzo-confirmed", "Vandor and Mapuzo Are Confirmed Campaign Locations", "EA names Vandor and Mapuzo among the worlds players will visit.", "The route spans locations associated with Solo and Obi-Wan Kenobi.", "reveal"),
 ("returning-characters-teased", "Familiar Star Wars Characters Will Appear", "EA promises appearances by fan favorites without publishing a complete cast list.", "Lore coverage should wait for named reveals instead of turning trailer guesses into facts.", "reveal"),
]),
"confirmed": ("Confirmed Guides", "/confirmed/", "Fact-checked feature and status reporting", [
 ("release-date-confirmed", "August 27, 2026 Release Date Is Confirmed", "EA lists a global release at 3 PM UTC on August 27.", "Players can convert one official timestamp instead of relying on regional countdown guesses.", "buy"),
 ("platforms-confirmed", "PC, PS5 and Xbox Series X|S Are the Launch Platforms", "The announced platforms are PC, PlayStation 5 and Xbox Series X|S.", "Older consoles and Nintendo Switch remain outside the announced launch lineup.", "preorder"),
 ("eleven-languages-confirmed", "Eleven Interface and Subtitle Languages Are Listed", "Official stores list eleven supported text languages.", "English and German are the two languages with full audio in the current store data.", "buy"),
 ("no-multiplayer-announced", "Official Descriptions Position Zero Company as Single Player", "EA repeatedly labels the game a single-player tactics title.", "The confirmed feature set does not include cooperative or competitive modes.", "preorder"),
 ("standard-permadeath-confirmed", "Three-Injury Permadeath Is Confirmed for Standard Difficulty", "The third Injury permanently removes an Operator on standard difficulty.", "This rule should be separated from higher-difficulty limited-save details.", "gameplay"),
]),
"official": ("Official Info", "/official/", "Release, store and publisher reporting", [
 ("august-27-3pm-utc", "EA Lists an August 27, 3 PM UTC Release", "The official purchase page provides both date and global UTC time.", "One canonical timestamp reduces confusion across regional storefronts.", "buy"),
 ("preorders-live-all-platforms", "Preorders Are Live Across PC, PlayStation and Xbox", "EA opened digital preorders on the announced launch platforms.", "Edition and retailer pages can now be compared against an official baseline.", "preorder"),
 ("crystalline-astromech-bonus", "Preorders Include the Crystalline Astromech Cosmetic Pack", "The preorder bonus contains R3 and crystalline astromech customization items.", "The bonus is cosmetic and should not be confused with a gameplay class unlock.", "buy"),
 ("deluxe-cosmetics-detailed", "Deluxe Edition Adds Clone Wars-Inspired Cosmetics", "EA describes Deluxe content as cosmetic items for the squad.", "Buyers can compare editions without assuming exclusive combat power.", "buy"),
 ("pc-requirements-published", "EA Publishes PC Requirements and 50 GB Storage", "The PC listing specifies Windows 10/11, DirectX 12 and 50 GB storage.", "Players can check hardware readiness before launch rather than relying on estimates.", "buy"),
]),
"start-here": ("Start Here", "/start-here/", "New-player orientation and launch-readiness reporting", [
 ("new-player-release-checklist", "New Player Release Checklist: Date, Platform and Language", "Release timing, supported hardware and language options are now officially listed.", "Players can resolve purchase basics before studying tactical systems.", "buy"),
 ("three-ap-first-rule", "The First Combat Rule to Learn Is the Three-AP Economy", "Every Operator receives three action points per turn.", "A new player should budget movement and a safe ending position before acting.", "gameplay"),
 ("advantage-first-look", "Advantage Gives the Squad a Shared Power Meter", "Attacks build Advantage to a maximum of ten.", "Beginners should monitor the team resource rather than only individual cooldowns.", "gameplay"),
 ("permadeath-first-look", "Injury Management Matters from the Start", "Three Injuries kill an Operator permanently on standard difficulty.", "Early roster and Medbay choices can affect the entire campaign.", "gameplay"),
 ("xcom-comparison-boundary", "What XCOM Players Should and Should Not Assume", "Zero Company shares turn-based tactical ideas but has its own AP, Advantage, bond and Den systems.", "Familiar genre experience helps, but unpublished values should not be imported from another game.", "gameplay"),
]),
"systems": ("Systems", "/systems/", "System-route consolidation and verification reporting", [
 ("official-system-pages-prioritized", "Verified System Pages Become the Primary Reference", "Source-grounded mechanics pages now take priority over older speculative route variants.", "Readers reach one maintained answer instead of overlapping pages.", "gameplay"),
 ("ap-routes-consolidated", "Action Point Coverage Centers on the Confirmed Three-AP Rule", "The official overview defines three AP per Operator.", "Duplicate action-economy pages can be merged around a precise answer.", "gameplay"),
 ("advantage-routes-consolidated", "Advantage Coverage Centers on the Shared Ten-Point Meter", "The resource is shared by the squad and capped at ten.", "One canonical explanation reduces keyword cannibalization.", "gameplay"),
 ("injury-routes-consolidated", "Injury Coverage Connects Combat, Medbay and Permadeath", "The third Injury causes death on standard difficulty.", "Related pages now link the tactical rule to its campaign consequence.", "gameplay"),
 ("mission-cycle-routes-consolidated", "Mission Cycle Coverage Moves to the HoloTable System", "The HoloTable advances missions through Cycles.", "The canonical route can explain both mission selection and time pressure.", "gameplay"),
]),
"planner": ("Planner", "/planner/", "Pre-launch planning and decision-tool reporting", [
 ("platform-buy-planner-updated", "Platform Planner Now Uses the Confirmed Launch Lineup", "PC, PS5 and Xbox Series X|S are the announced choices.", "Buyers can filter decisions without including unannounced platforms.", "preorder"),
 ("release-time-planner-updated", "Release Planner Uses EA's 3 PM UTC Timestamp", "EA provides a global launch time for August 27.", "Regional countdowns can be calculated from one official reference.", "buy"),
 ("specialization-planner-eight-roles", "Squad Planning Starts with Eight Standard Specializations", "EA names eight standard roles with distinct battlefield purposes.", "The planner can track role coverage without inventing hidden classes.", "gameplay"),
 ("injury-risk-planner", "Injury Risk Belongs in Campaign Planning", "An Operator dies after the third Injury on standard difficulty.", "A roster plan should include recovery capacity and replacement options.", "gameplay"),
 ("mission-cycle-planner", "Mission Cycles Add Opportunity Cost to Route Planning", "HoloTable missions advance in Cycles.", "A useful route planner must record skipped opportunities, not only completed missions.", "gameplay"),
]),
"media": ("Media", "/media/", "Trailer, video and official-media reporting", [
 ("gameplay-trailer-june-5", "Official Gameplay Trailer Reveals the August 27 Date", "EA's June 5 trailer announcement pairs tactical footage with the launch date.", "The video is the current baseline for visual combat analysis.", "preorder"),
 ("five-things-video-june-16", "EA Publishes a Five Things to Know Video", "The official game page highlights a June 16 overview video.", "Players have a compact introduction to story, customization and squad systems.", "buy"),
 ("announce-trailer-celebration", "Announcement Trailer Debuted at Star Wars Celebration Japan", "The first reveal introduced Hawks, the Clone Wars setting and Zero Company.", "Later footage can be compared against the original creative pillars.", "reveal"),
 ("gameplay-images-show-squad", "Official Gameplay Images Highlight a Mixed-Archetype Squad", "EA media shows Clone, Mandalorian, Jedi and specialist archetypes operating together.", "Visual evidence supports role diversity without proving exact launch stats.", "gameplay"),
 ("media-verification-policy", "Trailer Frames Are Evidence, Not Complete Stat Sheets", "Official media confirms visible characters, locations and mechanics but rarely final numbers.", "Media analysis should label inference and wait for the shipped build before publishing exact values.", "gameplay"),
]),
}

STYLE = """:root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#a8bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1040px}*{box-sizing:border-box}body{margin:0;background:#071016;color:var(--text);font:16px/1.72 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}nav a{color:var(--muted);font-size:14px}.hero{padding:50px 0 28px;border-bottom:1px solid var(--line)}.crumb,.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--teal)}h1{font-size:clamp(34px,6vw,56px);line-height:1.08;margin:13px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#cad8e0;max-width:840px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0;color:var(--text)}.card time,.muted,.source{color:var(--muted);font-size:14px}.facts li{margin:9px 0}.note{border-color:rgba(233,184,74,.48)}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){nav{margin-left:0}.top .wrap{padding-top:10px;padding-bottom:10px}}"""

def article_html(category, hub, section_desc, items, index, item):
    slug,title,answer,impact,source_key=item
    label=CATEGORIES[category][0]
    src_name,src_date,src_url=SOURCES[source_key]
    route=f"/news/{category}/{slug}.html"
    desc=f"{answer} Read the verified {label.lower()} news brief and what it means for players."
    related=[x for i,x in enumerate(items) if i!=index][:2]
    schema={"@context":"https://schema.org","@type":"NewsArticle","headline":title,"description":desc,"url":SITE+route,"mainEntityOfPage":SITE+route,"image":[SITE+"/assets/zero-company-hero.png"],"datePublished":TODAY,"dateModified":TODAY,"inLanguage":"en","author":{"@type":"Organization","name":"Star Wars Zero Company Wiki Editorial Team"},"publisher":{"@type":"Organization","name":"Star Wars Zero Company Wiki"},"isPartOf":{"@type":"WebSite","name":"Star Wars Zero Company Wiki","url":SITE+"/"}}
    related_html=''.join(f'<a class="card" href="/news/{category}/{x[0]}.html"><strong>{escape(x[1])}</strong><br><span class="muted">More {escape(label)} coverage</span></a>' for x in related)
    body=f'''<section class="hero"><div class="crumb"><a href="/news/">News</a> / <a href="{hub}">{escape(label)}</a></div><p class="eyebrow">Verified news analysis · Published July 19, 2026</p><h1>{escape(title)}</h1><p class="lead">{escape(answer)}</p></section>
<section class="block"><h2>Quick Read</h2><p>{escape(answer)} This brief focuses on one specific part of {escape(section_desc.lower())}. It does not add unofficial ability names, numerical values or launch behavior beyond the cited material.</p></section>
<section class="block"><h2>What the Official Update Establishes</h2><ul class="facts"><li>{escape(answer)}</li><li>The underlying source is the {escape(src_name)}, dated {escape(src_date)}.</li><li>Star Wars Zero Company remains scheduled for August 27, 2026 on PC, PlayStation 5 and Xbox Series X|S.</li></ul></section>
<section class="block"><h2>Why It Matters</h2><p>{escape(impact)} For readers following the {escape(label)} section, this narrows what can be planned before launch and what still needs direct testing in the released game.</p><p>The practical boundary is important: official descriptions can establish a role, system or availability detail, but they do not automatically establish final balance, optimal strategy or every interaction. Our corresponding hub keeps those categories separate. That distinction will also make future patch updates easier to identify and audit.</p></section>
<section class="block note"><h2>Editorial Verification</h2><p>We checked this article against the linked first-party source on July 19, 2026. If EA changes the feature before release, the article and its related hub will be revised together. Exact launch values will be added only after they can be observed in the shipped game or a later official breakdown.</p><p class="source"><a href="{src_url}" rel="nofollow">Read the {escape(src_name)}</a></p></section>
<section><h2>Related {escape(label)} News</h2><div class="grid">{related_html}<a class="card" href="{hub}"><strong>Browse the {escape(label)} hub</strong><br><span class="muted">Guides and verified reference pages</span></a></div></section>'''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company News</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}{route}"><meta property="og:type" content="article"><meta property="og:url" content="{SITE}{route}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:image" content="{SITE}/assets/zero-company-hero.png"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav><a href="/news/">News</a><a href="/operatives/">Operatives</a><a href="/classes/">Specializations</a><a href="/official-systems/">Systems</a><a href="/official/">Official Info</a></nav></div></header><main class="wrap">{body}</main><footer><div class="wrap">Unofficial, source-linked news and player guide. <a href="/about/sources-and-citations.html">Sources policy</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''

def news_cards(category, label, items):
    cards=''.join(f'<a href="/news/{category}/{slug}.html" style="display:block;border:1px solid #284050;border-radius:7px;padding:16px;color:inherit;text-decoration:none;background:#0d1922"><small style="color:#9db0bd">JUL 19, 2026 · NEWS</small><br><strong style="color:#36e0ce">{escape(title)}</strong><br><span style="color:#9db0bd;font-size:14px">{escape(answer)}</span></a>' for slug,title,answer,_,_ in items)
    return f'''<!-- TAB_NEWS_START --><section class="tab-news" aria-labelledby="tab-news-title" style="margin:42px 0"><h2 id="tab-news-title">Latest {escape(label)} News</h2><p style="color:#9db0bd">Five source-linked updates and editorial explainers for this section.</p><div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px">{cards}</div><p><a href="/news/#{category}">Browse all {escape(label)} news →</a></p></section><!-- TAB_NEWS_END -->'''

def update_hub(category,label,hub,items):
    route=hub.strip('/')
    path=ROOT/route/'index.html'
    if not path.exists(): raise FileNotFoundError(path)
    text=path.read_text(encoding='utf-8-sig',errors='ignore')
    text=re.sub(r'<!-- TAB_NEWS_START -->.*?<!-- TAB_NEWS_END -->','',text,flags=re.S)
    if '</main>' not in text.lower(): raise ValueError(f'Missing main close: {path}')
    text=re.sub(r'</main>',news_cards(category,label,items)+'</main>',text,count=1,flags=re.I)
    path.write_text(text,encoding='utf-8')

def build_news_hub():
    sections=[]
    for category,(label,hub,_,items) in CATEGORIES.items():
        cards=''.join(f'<a class="card" href="/news/{category}/{x[0]}.html"><time>JUL 19, 2026</time><br><strong>{escape(x[1])}</strong><br><span class="muted">{escape(x[2])}</span></a>' for x in items)
        sections.append(f'<section id="{category}"><h2>{escape(label)} News</h2><p><a href="{hub}">Open {escape(label)} hub →</a></p><div class="grid">{cards}</div></section>')
    desc='Browse 80 source-linked Star Wars Zero Company news briefs across every primary guide and database section.'
    schema={"@context":"https://schema.org","@type":"CollectionPage","name":"Star Wars Zero Company News","description":desc,"url":SITE+'/news/',"dateModified":TODAY,"inLanguage":"en"}
    html=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Star Wars Zero Company News and Updates</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}/news/"><script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav><a href="/news/">News</a><a href="/guides/">Guides</a><a href="/confirmed/">Confirmed</a><a href="/official/">Official Info</a></nav></div></header><main class="wrap"><section class="hero"><p class="eyebrow">Source-linked editorial coverage</p><h1>Star Wars Zero Company News</h1><p class="lead">Eighty focused updates organized around the site's primary content tabs. Every brief links to the first-party material used and labels the boundary between published facts and launch-day testing.</p></section>{''.join(sections)}</main><footer><div class="wrap">Unofficial news index · <a href="/about/sources-and-citations.html">Sources policy</a></div></footer></body></html>'''
    path=ROOT/'news/index.html'; path.parent.mkdir(parents=True,exist_ok=True); path.write_text(html,encoding='utf-8')

def add_home_nav():
    path=ROOT/'index.html'; text=path.read_text(encoding='utf-8-sig')
    if 'href="/news/"' not in text:
        text=text.replace('<a href="/guides/">Guides</a>','<a href="/guides/">Guides</a>\n      <a href="/news/">News</a>',1)
    path.write_text(text,encoding='utf-8')

def main():
    total=0
    for category,(label,hub,desc,items) in CATEGORIES.items():
        update_hub(category,label,hub,items)
        out=ROOT/'news'/category; out.mkdir(parents=True,exist_ok=True)
        for index,item in enumerate(items):
            (out/f'{item[0]}.html').write_text(article_html(category,hub,desc,items,index,item),encoding='utf-8')
            total+=1
    build_news_hub(); add_home_nav()
    print(f'Built {total} independent news URLs across {len(CATEGORIES)} tabs plus the news hub')

if __name__=='__main__': main()
