"""Refresh the published English FAQ pages without rebuilding navigation or other locales."""

from html import escape, unescape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
UPDATED = "2026-11-17"
EA = "https://www.ea.com/games/starwars/zero-company"
HELP = "https://help.ea.com/en/articles/star-wars/zero-company/"
PATCH = ("EA’s 1.2 patch notes", EA + "/news/patch-notes-1-2")
FAQ = ("EA’s game FAQ", EA + "/faq")
COMBAT = ("EA Help’s combat and campaign guide", HELP + "turn-based-tactics-basics/")
PLATFORMS = ("EA Help’s platforms and PC requirements", HELP + "platforms-pc-requirements-guide/")
STEAM = ("Steam store listing", "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/")
MODIFIERS = ("Campaign modifiers guide", "/guides/campaign-modifiers.html")
INJURIES = ("Permadeath and injury prevention", "/guides/permadeath-injury-prevention.html")

# Direct answer, supporting detail, optional additional sources and further reading.
UPDATES = {
    "can-you-respec": (
        "Yes. In a default campaign, Hawks and custom Operators can change Specialization. At the Den, open Personnel and choose Change Specialization. Authored Operators have character-specific restrictions.",
        "Patch 1.2 added three independent campaign locks. Locked Tactical Respec prevents primary and secondary Specialization changes. Locked Talent Respec prevents talent changes. Locked Weapon Respec prevents weapon changes, with one exception for Trick after his required switch. These options are chosen when starting a campaign and take effect after the tutorial.",
        [("EA Help’s Specialization and Weapon guide", HELP + "specialization-and-weapon-class-guide/"), ("EA Help’s squad customization guide", HELP + "build-and-customize-your-squad/"), PATCH],
        [("Personnel at the Den", "/facilities/personnel.html"), MODIFIERS]),
    "can-you-disable-permadeath": (
        "Yes. Choose New Campaign, open Difficulty Settings and turn Permadeath off before you start. An existing campaign keeps its original setting.",
        "Patch 1.2 also lets you set injury limits and add a chance of death when starting a new campaign. The default No Risk of Death option removes the extra random chance. With Permadeath on, a tactical defeat can still kill an Operator who has reached the injury limit.",
        [COMBAT, PATCH], [("How many injuries cause permanent death?", "/questions/how-many-injuries-cause-death.html"), INJURIES]),
    "how-many-injuries-cause-death": (
        "With Permadeath on and the default Three Strikes rule, a tactical defeat kills an Operator who already has two injuries. Check their injury count before deploying them.",
        "Patch 1.2 lets a new campaign use Two Strikes, where a defeat is lethal with one existing injury, or Instant Death, where a tactical defeat can kill an uninjured Operator. Trick can survive one defeat per Tactical Mission under Instant Death. The optional Static and Escalating Risk settings can cause death before the injury limit. Injuries earned during Galaxy Map Operations do not trigger these tactical-death rolls.",
        [COMBAT, PATCH], [INJURIES, MODIFIERS]),
    "how-many-specializations-are-there": (
        "There are eight standard Specializations: Assault, Gunslinger, Heavy, Medic, Scoundrel, Scout, Sharpshooter and Soldier.",
        "For a first squad, EA suggests Soldier or Assault as straightforward choices. Story-specific roles such as Jedi Padawan sit outside this list.",
        [("EA Help’s Specialization and Weapon guide", HELP + "specialization-and-weapon-class-guide/")], []),
    "how-many-abilities-per-specialization": (
        "There are three ability types: Ultimate, Standard and Passive. A Specialization can have more than one passive.",
        "For example, EA lists four Assault abilities. Sweeping Salvo is its Ultimate, Bull Rush is its Standard ability, and Fleet of Foot and Strike the Flanks are passives.",
        [("EA Help’s Specialization and Weapon guide", HELP + "specialization-and-weapon-class-guide/")], []),
    "what-ability-types-do-specializations-have": (
        "Specializations have Ultimate, Standard and Passive abilities.",
        "Standard abilities are active combat choices. Passives work automatically. An Ultimate can change the course of a turn and draws on the squad’s Advantage.",
        [("EA Help’s Specialization and Weapon guide", HELP + "specialization-and-weapon-class-guide/")], []),
    "how-many-weapon-classes": (
        "There are four standard weapon classes: Blaster Rifle, Repeater, Blaster Pistol and Longarm Blaster.",
        "EA recommends the Blaster Rifle as a flexible starting option. A Longarm Blaster is suited to precision at range and costs two Action Points to fire.",
        [("EA Help’s Specialization and Weapon guide", HELP + "specialization-and-weapon-class-guide/")], []),
    "how-do-injuries-work": (
        "Operators can carry injuries from tactical combat back to the Den. Check their injury count before deploying them again.",
        "The Medbay helps with recovery. With Permadeath enabled, the default Three Strikes rule makes a tactical defeat lethal when an Operator already has two injuries. Campaign modifiers can lower that threshold or add a chance of death on defeat.",
        [COMBAT, PATCH], [INJURIES, ("How many injuries cause permanent death?", "/questions/how-many-injuries-cause-death.html")]),
    "does-zero-company-have-limited-saves": (
        "Yes. In Beskar Mode the campaign has one save slot and manual saves are disabled.",
        "Choose Beskar Mode when setting up a new campaign. To play without it, start another campaign with Beskar turned off.",
        [COMBAT], [("Difficulty options", "/guides/difficulty-for-new-players.html")]),
    "is-zero-company-on-steam-deck": (
        "Valve rates Star Wars Zero Company Unsupported on Steam Deck.",
        "EA said the game would launch without Steam Deck verification. Valve’s device report now lists SteamOS compatibility as unsupported. Check the Steam store for rating changes.",
        [FAQ, STEAM, ("Valve’s Steam Deck compatibility report", "https://store.steampowered.com/saleaction/ajaxgetdeckappcompatibilityreport?nAppID=2075800&l=english")], []),
    "will-zero-company-have-dlc": (
        "EA’s FAQ does not announce a story expansion. The game has received post-launch updates, including the free 1.2 patch with campaign modifiers.",
        "The Deluxe Edition includes cosmetics. For new gameplay rules, check the 1.2 notes. For an expansion announcement, check EA’s game news.",
        [FAQ, PATCH, ("EA’s Zero Company news", EA + "/news")], [MODIFIERS]),
    "can-zero-company-be-played-offline": (
        "EA lists no online connection requirement for the single-player PC campaign.",
        "You may still need a connection for the initial download, updates or features supplied by your storefront.",
        [PLATFORMS], [("Single-player and offline play", "/guides/single-player-offline.html")]),
    "when-does-star-wars-zero-company-release": (
        "Star Wars Zero Company launched on August 27, 2026, for PC, PlayStation 5 and Xbox Series X|S.",
        "On PC, the game is available through the EA app, Steam and the Epic Games Store.",
        [PLATFORMS, STEAM], [("Platforms and PC options", "/guides/platforms-pc-ps5-xbox.html")]),
    "what-time-does-zero-company-release": (
        "EA listed the launch time as 3:00 PM UTC on August 27, 2026.",
        "That was 11:00 AM Eastern Daylight Time and 8:00 AM Pacific Daylight Time in the United States.",
        [], []),
    "what-platforms-is-zero-company-on": (
        "Star Wars Zero Company is available on PC, PlayStation 5 and Xbox Series X|S.",
        "The PC storefronts are the EA app, Steam and the Epic Games Store.", [PLATFORMS], []),
    "should-you-preorder": (
        "The preorder window closed when Zero Company launched on August 27, 2026. Its bonus was the Crystalline Astromech Cosmetic Pack.",
        "If you preordered and cannot find the pack, check the edition and account used for the purchase, then follow EA’s missing-content guide.",
        [("EA Help’s missing-content guide", HELP + "missing-content/")], [("What was the preorder bonus?", "/questions/what-is-the-preorder-bonus.html")]),
    "what-is-the-preorder-bonus": (
        "The preorder bonus was the Crystalline Astromech Cosmetic Pack.",
        "It included an R3 droid and crystalline heads for R4 and R5 droids. If the items are missing from an eligible purchase, EA lists checks for each platform.",
        [("EA Help’s missing-content guide", HELP + "missing-content/")], []),
    "does-zero-company-have-multiplayer": (
        "No. Star Wars Zero Company is a single-player tactics game.",
        "You control your own squad in the campaign. The game has no online multiplayer mode.", [PLATFORMS], []),
    "does-zero-company-have-coop": (
        "No. Star Wars Zero Company has a single-player campaign and does not offer co-op.",
        "You control the whole squad yourself, including Operators who assist one another during combat.", [PLATFORMS], []),
    "what-mission-types-are-confirmed": (
        "EA lists sabotage, combat, rescue, retrieval and character-focused narrative missions.",
        "Tactical Missions deploy a squad to a battlefield. Galaxy Map Operations can resolve immediately or unlock a subsequent mission.", [FAQ], []),
    "when-does-zero-company-soundtrack-release": (
        "Gordy Haab’s Star Wars: Zero Company soundtrack was released on August 27, 2026.",
        "The full album contains 25 tracks, including the title track first released as a single.",
        [("Original soundtrack on Apple Music", "https://music.apple.com/us/album/star-wars-zero-company-original-video-game-soundtrack/6793246073")], []),
}

# Earlier first-party evidence still answers these questions, but the original
# supporting sentence promised future launch testing or described an upcoming release.
DETAILS = {
    "does-zero-company-have-new-game-plus": ("Zero Company launched without New Game Plus.", "Some customization options unlock on subsequent playthroughs."),
    "is-zero-company-on-nintendo-switch": (None, "EA lists PC, PlayStation 5 and Xbox Series X|S as its platforms."),
    "can-advantage-grant-extra-ap": (None, "Use the extra action on an ally who can reach an objective or take a useful shot this turn."),
    "can-advantage-taunt-enemies": (None, "The ability description shows which targets are in range when you select it."),
    "how-separatist-faction-fights": (None, "Inspect the droid’s abilities before deciding where to spend your Ion attacks."),
    "can-customize-clone-armor": (None, "The choices include helmet and armor paint schemes."),
    "how-infinite-coil-faction-fights": (None, "Check each enemy’s abilities before deciding which one the squad should target first."),
    "how-outlaw-faction-fights": (None, "Check how many enemies can reach your position before committing the squad to one target."),
    "how-many-cosmetic-models-per-weapon-class": (None, "The model changes the weapon’s appearance within its existing weapon class."),
    "which-operatives-are-confirmed": (None, "These are named Operators profiled by EA. Custom recruits are separate."),
    "will-missions-have-heavy-machinery": ("Yes. Some missions involve heavy machinery.", "EA’s community Q&A describes these encounters without listing every vehicle or droid."),
}

QUESTIONS = {
    "when-does-star-wars-zero-company-release": "When did Star Wars Zero Company release?",
    "what-time-does-zero-company-release": "What time did Star Wars Zero Company launch?",
    "when-does-zero-company-soundtrack-release": "When was the Zero Company soundtrack released?",
    "should-you-preorder": "Can you still preorder Star Wars Zero Company?",
    "what-is-the-preorder-bonus": "What was the Star Wars Zero Company preorder bonus?",
    "is-zero-company-on-steam-deck": "Is Star Wars Zero Company Steam Deck Verified?",
    "will-zero-company-have-dlc": "Has EA announced story DLC for Zero Company?",
    "will-missions-have-heavy-machinery": "Do missions feature heavy machinery?",
}

# Each topic pairs a reference guide with a question that helps the reader act.
TOPICS = [
    ("Choose a Specialization", "/classes/", "can-you-respec", "Can you change Specialization?", """
        how-many-specializations-are-there what-are-the-eight-specializations can-you-respec
        how-many-abilities-per-specialization what-ability-types-do-specializations-have"""),
    ("Weapon classes and equipment", "/official-systems/armory-weapons-guide.html", "how-many-weapon-classes", "How many weapon classes are there?", """
        how-many-weapon-classes how-many-cosmetic-models-per-weapon-class do-species-affect-weapon-proficiency can-you-use-a-full-sniper-squad"""),
    ("Operator injuries and recovery", "/guides/permadeath-injury-prevention.html", "how-many-injuries-cause-death", "When is an injury fatal?", """
        can-you-disable-permadeath how-many-injuries-cause-death how-do-injuries-work do-injuries-lower-combat-stats can-downed-operators-be-rallied can-story-characters-die what-happens-if-hawks-dies"""),
    ("Campaign difficulty and settings", "/guides/difficulty-for-new-players.html", "can-you-disable-permadeath", "How do you turn off permadeath?", "does-zero-company-have-limited-saves"),
    ("Bonds and cross-training", "/guides/bonds-squad-synergy.html", "does-squad-choice-affect-bonds", "How does squad choice affect Bonds?", """
        are-bonds-important what-are-focus-points does-squad-choice-affect-bonds does-zero-company-have-romance"""),
    ("Recruit and deploy a squad", "/guides/beginner-first-squad.html", "what-is-standard-squad-size", "How many Operators can deploy together?", """
        can-build-full-clone-trooper-team can-control-more-than-four-operators can-mix-authored-and-custom-operators
        can-you-create-custom-operators can-recruit-separatist-droids how-are-custom-operators-recruited
        how-increase-operator-cap what-is-operator-limit how-many-operators-start what-is-standard-squad-size when-do-authored-operators-join"""),
    ("Building an Astromech", "/guides/astromech-builder.html", "when-can-recruit-astromechs", "When can you recruit Astromechs?", "when-can-recruit-astromechs can-build-full-astromech-squad"),
    ("Hawks and character customization", "/guides/custom-hawks-options.html", "is-hawks-customizable", "Which parts of Hawks can you customize?", """
        can-choose-hawks-voice can-customize-hawks-clothing can-customize-hawks-first-name what-species-can-hawks-be is-hawks-customizable"""),
    ("Customization at the Den", "/facilities/customization.html", "do-outfits-affect-gameplay", "Do outfits change how an Operator fights?", """
        can-custom-operators-have-backstories can-customize-clone-armor can-customize-operator-voices do-operators-earn-nicknames
        do-clone-helmets-change-voices do-outfits-affect-gameplay who-can-wear-mandalorian-armor"""),
    ("Spend Action Points", "/guides/action-points.html", "how-many-action-points-per-turn", "How many Action Points do Operators get?", """
        can-actions-be-taken-in-any-order how-many-action-points-per-turn what-do-action-points-control is-zero-company-turn-based"""),
    ("Build and spend Advantage", "/guides/advantage-meter.html", "what-is-maximum-advantage", "How much Advantage can the squad store?", """
        can-advantage-boost-hit-chance can-advantage-grant-extra-ap can-advantage-taunt-enemies does-advantage-cost-action-points what-is-advantage what-is-maximum-advantage"""),
    ("Team attacks and Bonds", "/official-systems/squad-bonds-training.html", "what-does-call-for-backup-do", "How does Call for Backup work?", """
        does-call-for-backup-cost-ap what-does-call-for-backup-do does-zero-company-have-call-ins"""),
    ("Cover, flanking and sightlines", "/guides/cover-flanking-basics.html", "does-high-ground-improve-hit-chance", "Does high ground improve hit chance?", """
        is-cover-destructible does-high-ground-improve-hit-chance does-zero-company-have-fog-of-war does-weather-affect-combat"""),
    ("Tactical Mission types", "/missions/", "difference-operations-tactical-missions", "How do Operations differ from Tactical Missions?", """
        can-evacuate-mission-early will-missions-have-heavy-machinery what-mission-types-are-confirmed what-mission-objectives-are-confirmed difference-operations-tactical-missions"""),
    ("Mission cycles and deadlines", "/guides/cycles-time-limited-missions.html", "can-operations-expire", "Can Operations expire?", """
        can-operation-choices-affect-side-missions can-operations-expire can-operations-unlock-missions does-each-cycle-end-with-tactical-mission do-story-missions-become-mandatory what-are-mission-cycles what-is-intel-used-for"""),
    ("Story missions and Hawks", "/mechanics/hawks-required-story-missions.html", "is-hawks-required-story-missions", "When is Hawks required?", """
        can-skip-hawks-skirmish-missions is-hawks-required-story-missions"""),
    ("Exploration before combat", "/guides/third-person-exploration.html", "what-can-you-find-before-combat", "What can you collect before combat?", """
        can-you-explore-before-combat can-you-free-roam-before-story-combat what-can-you-find-before-combat"""),
    ("Handcrafted maps and randomized encounters", "/guides/handcrafted-maps-random-enemies.html", "are-missions-randomized", "Which parts of missions are randomized?", """
        are-missions-randomized are-zero-company-maps-handcrafted"""),
    ("Galaxy Map locations", "/missions/galaxy-map-150-planets.html", "how-many-tactical-mission-planets", "How many planets have Tactical Missions?", """
        how-many-planets-galaxy-map how-many-tactical-mission-planets where-does-zero-company-take-place"""),
    ("Enemy profiles", "/hostiles/", "how-separatist-faction-fights", "What works against Separatist droids?", """
        how-infinite-coil-faction-fights how-outlaw-faction-fights how-separatist-faction-fights"""),
    ("The Den and its facilities", "/guides/the-den-base-upgrades.html", "what-facilities-are-in-the-den", "Which facilities are at the Den?", """
        what-does-meevo-do-at-den what-does-neesh-do-at-den what-does-runa-do-at-den what-facilities-are-in-the-den what-is-the-den who-supports-zero-company-from-den"""),
    ("Play the single-player campaign", "/guides/single-player-offline.html", "can-zero-company-be-played-offline", "Can you play offline?", """
        can-zero-company-be-played-offline does-zero-company-have-coop does-zero-company-have-multiplayer is-zero-company-single-player"""),
    ("Supported platforms and PC options", "/guides/platforms-pc-ps5-xbox.html", "what-platforms-is-zero-company-on", "Which platforms can play Zero Company?", """
        is-zero-company-on-nintendo-switch is-zero-company-on-steam-deck is-zero-company-on-ps4 is-zero-company-on-xbox-one what-platforms-is-zero-company-on where-can-you-buy-zero-company-on-pc"""),
    ("Available languages and audio", "/official/languages.html", "how-many-languages-does-zero-company-support", "Which languages are supported?", """
        how-many-languages-does-zero-company-support does-zero-company-have-german-audio does-zero-company-have-japanese-audio"""),
    ("Editions and cosmetic bonuses", "/guides/price-editions-preorder.html", "what-is-in-deluxe-edition", "What comes with the Deluxe Edition?", """
        should-you-preorder what-is-the-preorder-bonus what-is-in-deluxe-edition how-much-does-zero-company-cost how-much-is-deluxe-edition
        does-zero-company-have-microtransactions is-zero-company-collectors-edition-announced is-arc-trooper-armor-deluxe-only"""),
    ("Release date and platforms", "/official/release-date.html", "what-time-does-zero-company-release", "What time did the game launch?", """
        when-does-star-wars-zero-company-release what-time-does-zero-company-release"""),
    ("Zero Company’s story and setting", "/lore/zero-company.html", "does-zero-company-have-multiple-endings", "How do endings vary?", """
        are-cutscenes-real-time does-zero-company-have-branching-paths does-zero-company-have-multiple-endings how-long-main-campaign is-zero-company-set-in-clone-wars"""),
    ("Replay and customization unlocks", "/mechanics/no-new-game-plus-at-launch.html", "what-unlocks-on-later-playthroughs", "What unlocks on later playthroughs?", """
        does-zero-company-have-new-game-plus what-unlocks-on-later-playthroughs"""),
    ("Meet the Operators", "/operatives/", "which-operatives-are-confirmed", "Which Operators appear in the story?", """
        what-clan-is-cly-kullervo-from is-telrea-only-jedi-padawan what-role-does-luco-bronc-fill what-species-is-kabb-uppercut which-operatives-are-confirmed
        who-is-hawks-zero-company who-is-jae-mordant who-is-kabb-uppercut who-is-telrea-vokoss who-is-trick-zero-company"""),
    ("The Infinite Coil and its leader", "/lore/infinite-coil.html", "how-infinite-coil-faction-fights", "How does the Infinite Coil fight?", "who-is-kundri-fathom"),
    ("Cast and performances", "/cast/", "can-choose-hawks-voice", "Can you choose Hawks’ voice?", """
        who-voices-anakin-skywalker who-voices-cly-kullervo who-voices-hawks-feminine who-voices-hawks-masculine who-voices-jae-mordant
        who-voices-kabb-uppercut who-voices-kundri-fathom who-voices-meevo who-voices-neesh-renark who-voices-runa-blask
        who-voices-telrea who-voices-trick-and-clone-troopers who-voices-typhon"""),
    ("Official news and announcements", "/official/official-news-tracker.html", "who-develops-zero-company", "Who developed Zero Company?", """
        is-lucasfilm-games-involved who-develops-zero-company who-publishes-zero-company when-does-zero-company-soundtrack-release
        will-zero-company-have-dlc does-zero-company-support-mods"""),
]
TOPIC_LINKS = {}
for guide_title, guide_url, peer_slug, peer_title, members in TOPICS:
    for member in members.split():
        if member in TOPIC_LINKS:
            raise ValueError(f"Duplicate FAQ topic for {member}")
        links = [(guide_title, guide_url)]
        if member != peer_slug:
            links.append((peer_title, f"/questions/{peer_slug}.html"))
        TOPIC_LINKS[member] = links


SCHEMA = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
CARD = re.compile(r'(<a\b[^>]*\bhref="/questions/([a-z0-9-]+)\.html"[^>]*>(?:<small>[^<]*</small><br>)?<strong>)(.*?)(</strong><br><span class="muted">)(.*?)(</span></a>)', re.S)


def card_copy(match):
    opening, slug, title, middle, lead, closing = match.groups()
    answer = UPDATES[slug][0] if slug in UPDATES else DETAILS.get(slug, (None,))[0]
    title = escape(QUESTIONS[slug]) if slug in QUESTIONS else title
    return opening + title + middle + (escape(answer) if answer else lead) + closing


def link_list(items):
    return " · ".join(f'<a href="{escape(url, quote=True)}">{escape(label)}</a>' for label, url in items)


def refresh_page(slug, text):
    """Keep shared navigation, styling, robots directives and related-page cards intact."""
    text = CARD.sub(card_copy, text)
    text = re.sub(r'Browse all (?:50|100|102|152)(?: English)? FAQs', 'Browse all English FAQs', text)
    meta = SCHEMA.search(text)
    if not meta or '"FAQPage"' not in meta[2]:
        return text
    schema = json.loads(meta[2])
    quick = re.search(r'<section class="block answer">\s*<h2>Quick Answer</h2>\s*<p><strong>(.*?)</strong></p>\s*<p>(.*?)</p>', text, re.S)
    if not quick:
        raise ValueError(f"Missing quick answer on {slug}")
    first, second = (unescape(s) for s in quick.groups())
    entity = schema['mainEntity'][0]
    question = QUESTIONS.get(slug, entity['name'])
    old_source = re.search(r'<section class="block"><h2>(?:What the Official (?:Source|Information) Says|Sources?)</h2>(.*?)</section>', text, re.S)
    if old_source is None:
        raise ValueError(f"Missing sources on {slug}")
    source_links = [(unescape(label), unescape(url)) for url, label in re.findall(r'<a href="(https?://[^"]+)"[^>]*>(.*?)</a>', old_source[1])]
    more = []
    if slug in UPDATES:
        first, second, extra_sources, more = UPDATES[slug]
        source_links.extend(extra_sources)
    elif slug in DETAILS:
        new_answer, second = DETAILS[slug]
        first = new_answer or first
    unique = {url: label for label, url in source_links}
    sources = [(label, url) for url, label in unique.items()]
    if not sources:
        raise ValueError(f"Missing source URL on {slug}")
    entity['name'] = question
    entity['acceptedAnswer']['text'] = first + ' ' + second
    schema['dateModified'] = UPDATED
    text = SCHEMA.sub(lambda m: m[1] + json.dumps(schema, ensure_ascii=False) + m[3], text, count=1)
    for pattern,val in [
        (r'(<title>).*?(</title>)', escape(question) + ' | Zero Company FAQ'),
        (r'(<h1>).*?(</h1>)', escape(question)),
        (r'(<meta property="og:title" content=").*?(">)', escape(question)),
        (r'(<meta (?:name="description"|property="og:description") content=").*?(">)', escape(first)),
        (r'(<p class="lead">).*?(</p>)', escape(first)),
    ]:
        text = re.sub(pattern, lambda m: m[1] + val + m[2], text, flags=re.S)
    if slug in UPDATES or slug in DETAILS:
        text = re.sub(r'(<p class="eyebrow">)(?:Fact-checked|Updated) [A-Z][a-z]+ \d+, \d{4}(</p>)',
                      r'\g<1>Updated November 17, 2026\g<2>', text, count=1)
    quick_html = f'<section class="block answer"><h2>Quick Answer</h2><p><strong>{escape(first)}</strong></p><p>{escape(second)}</p></section>'
    source_html = f'<section class="block"><h2>Sources</h2><p>{link_list(sources)}</p></section>'
    more_html = f'<section class="block"><h2>Related guides</h2><p>{link_list(more)}</p></section>' if more else ''
    text, replaced = re.subn(r'<section class="block answer">.*?(?=<section><h2>Related Questions</h2>)',
                             lambda _: quick_html + source_html + more_html, text, count=1, flags=re.S)
    if slug in TOPIC_LINKS:
        candidates = TOPIC_LINKS[slug] + [("Browse all English FAQs", "/questions/")]
        existing_urls = {url for _, url in more}
        cards = ''.join(f'<a class="card" href="{escape(url, quote=True)}"><strong>{escape(label)}</strong></a>' for label, url in candidates if url not in existing_urls)
        text = re.sub(r'<section><h2>Related Questions</h2>.*?</section>', lambda _: '<section><h2>Related Questions</h2><div class="grid">' + cards + '</div></section>', text, count=1, flags=re.S)
    if not replaced:
        raise ValueError(f"Missing related questions on {slug}")
    return text


def refresh_hub(text, directory=ROOT / "questions"):
    indexed = {}
    for path in sorted(directory.glob("*.html")):
        if path.name == "index.html":
            continue
        body = path.read_text(encoding="utf-8")
        if re.search(r'<meta name="robots" content="[^"]*noindex', body, re.I):
            continue
        match = SCHEMA.search(body)
        if match and '"FAQPage"' in match[2]:
            entry = json.loads(match[2])['mainEntity'][0]
            title = entry['name']
            lead = unescape(re.search(r'<p class="lead">(.*?)</p>', body, re.S)[1])
            indexed[path.stem] = (title, lead)
    count = len(indexed)
    if not count:
        return text
    text = CARD.sub(card_copy, text)
    text = re.sub(r'<!-- FAQ_REMAINING_START -->.*?<!-- FAQ_REMAINING_END -->', '', text, flags=re.S)
    linked = set(re.findall(r'href="/questions/([a-z0-9-]+)\.html"', text.split('<main', 1)[1].split('</main>', 1)[0]))
    missing = set(indexed) - linked
    if missing:
        cards = ''.join(f'<a class="card" href="/questions/{slug}.html"><strong>{escape(indexed[slug][0])}</strong><br><span class="muted">{escape(indexed[slug][1])}</span></a>' for slug in sorted(missing))
        text = text.replace('</main>', '<!-- FAQ_REMAINING_START --><section><h2>More player questions</h2><div class="grid">' + cards + '</div></section><!-- FAQ_REMAINING_END --></main>', 1)
    desc = f'{count} English answers about Star Wars Zero Company, including combat, campaign settings, Operators, platforms and editions.'
    text = re.sub(r'(<title>Star Wars Zero Company FAQ).*?(</title>)', rf'\g<1> — {count} Answers\2', text)
    text = re.sub(r'(<meta name="description" content=").*?(">)', lambda m: m[1] + desc + m[2], text, count=1)
    text = re.sub(r'(<p class="eyebrow">)\d+ (?:English |source-linked )?answers</p>', rf'\g<1>{count} English answers</p>', text, count=1)
    text = re.sub(r'(<h1>Star Wars Zero Company FAQ</h1><p class="lead">).*?</p>', r'\1Find answers about combat, recruiting Operators, campaign settings and buying the game.</p>', text, count=1)
    text = re.sub(r'<section class="hero"><p class="eyebrow">50 new first-party answers.*?</section>', '<section class="hero"><h2>Squads, missions and editions</h2></section>', text, flags=re.S)
    text = re.sub(r'<section class="hero"><p class="eyebrow">50 additional verified answers.*?</section>', '<section class="hero"><h2>Combat, roster and cast</h2></section>', text, flags=re.S)
    text = re.sub(r'(?:Browse|Explore) all (?:50|100|102|152)(?: English)? FAQs', 'Browse all English FAQs', text)
    text = text.replace('More Related FAQ FAQs', 'More player questions').replace('Related FAQ FAQs', 'Related questions').replace('Additional FAQ FAQs', 'Additional player questions').replace('Five direct answers selected from the new 50-page FAQ batch.', 'Answers about roster choices, combat and the campaign.')
    meta = SCHEMA.search(text)
    if meta:
        schema = json.loads(meta[2])
        schema.update(description=desc, dateModified=UPDATED)
        text = SCHEMA.sub(lambda m: m[1] + json.dumps(schema, ensure_ascii=False) + m[3], text, count=1)
    return text


def main():
    directory = ROOT / "questions"
    for path in sorted(directory.glob("*.html")):
        if path.name == "index.html":
            continue
        text = path.read_text(encoding="utf-8")
        if 'content="noindex' in text:
            continue
        updated = refresh_page(path.stem, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
    hub = directory / "index.html"
    original = hub.read_text(encoding="utf-8")
    updated = refresh_hub(original)
    if updated != original:
        hub.write_text(updated, encoding="utf-8")


if __name__ == '__main__':
    main()
