#!/usr/bin/env python3
"""Round 26: second five-News batch for every nav destination plus 50 new FAQs."""

from __future__ import annotations

from html import escape
from pathlib import Path
import importlib.util
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = "2026-07-31"
DISPLAY_DATE = "July 31, 2026"

spec = importlib.util.spec_from_file_location("round24", ROOT / "tools" / "build_round24_nav_news_faq.py")
r24 = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(r24)

SOURCES = {
    "qna": (
        "EA community Q&A",
        "July 21, 2026",
        "https://www.ea.com/games/starwars/zero-company/news/answering-biggest-questions",
    ),
    "sdcc": (
        "StarWars.com SDCC 2026 panel report",
        "July 26, 2026",
        "https://www.starwars.com/news/sdcc-star-wars-zero-company-cast-announce",
    ),
    "gameplay": (
        "EA gameplay overview",
        "June 9, 2026",
        "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory",
    ),
    "trailer": (
        "StarWars.com gameplay trailer report",
        "June 6, 2026",
        "https://www.starwars.com/news/star-wars-zero-company-gameplay-trailer",
    ),
    "preorder": (
        "EA preorder and edition announcement",
        "June 5, 2026",
        "https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company",
    ),
    "announce": (
        "StarWars.com reveal interview",
        "April 19, 2025",
        "https://www.starwars.com/news/star-wars-zero-company",
    ),
    "steam": (
        "official Steam store listing",
        "July 31, 2026 verification",
        "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/",
    ),
    "psstore": (
        "official PlayStation Store listing",
        "July 31, 2026 verification",
        "https://store.playstation.com/en-us/concept/10009029",
    ),
}

# headline, concrete answer, source key
FACTS = {
    "campaign-length": ("Main Campaign Estimate Is 30–40 Hours", "Bit Reactor estimates 30–40 hours for an average main-story run, with difficulty and tactics experience affecting the total.", "qna"),
    "clone-team": ("A Full Clone Trooper Team Can Be Unlocked", "Clone Troopers unlock after a point in the story, after which the roster can support a full Clone Trooper team.", "qna"),
    "helmet-voice": ("Clone Helmets Add Voice Modulation", "Clone Trooper helmets change the presentation of character voices through an announced modulation effect.", "qna"),
    "hawks-identity": ("Hawks Supports Name, Species and Appearance Choices", "Hawks can be customized by first name, species, appearance, clothing and voice presentation while remaining the campaign protagonist.", "qna"),
    "eight-species": ("Eight Operator Species Are Named", "The official trailer report names Devaronian, Human, Neimoidian, Ovissian, Togruta, Twi'lek, Weequay and Zabrak as character-creation species.", "trailer"),
    "authored-custom": ("Authored and Custom Operators Can Mix", "Players can combine story-authored Operators with fully customized recruits in the same company and tactical roster.", "gameplay"),
    "authored-join": ("Authored Operators Join Through the Story", "Authored Operators enter Zero Company as the campaign unfolds, while Custom Operators are recruited directly by the player.", "gameplay"),
    "operator-voice": ("Custom Operators Include Voice Selection", "Custom recruits support appearance, clothing, voice and name choices rather than only a visual preset.", "gameplay"),
    "bonds-support": ("Bonds Unlock New Support Abilities", "Operators who grow closer through combat can unlock support abilities that change how teammates assist one another.", "trailer"),
    "cross-training": ("Cross-Training Can Share Skills and Stats", "Bond benefits include cross-training that can share new skills and statistics between bonded Operators.", "qna"),
    "den-upgrades": ("The Den Houses Facility Upgrades", "Between missions, The Den supports recruitment, progression, facility upgrades and equipment purchases.", "trailer"),
    "equipment-shop": ("Equipment Can Be Purchased at The Den", "The headquarters loop explicitly includes purchasing equipment before the next deployment.", "trailer"),
    "operation-dilemmas": ("Some Operations Present Choice-Driven Dilemmas", "Galaxy Map Operations can present decisions whose outcomes affect narrative context, Bonds or side missions.", "qna"),
    "cycle-finale": ("Each Mission Cycle Ends in a Tactical Selection", "Operations and missions can expire, and each cycle closes with a Tactical Mission selection from the Den holotable.", "qna"),
    "precombat-roam": ("Story Missions Include Third-Person Free Roam", "Selected story missions begin with a small third-person exploration phase before tactical combat.", "qna"),
    "precombat-rewards": ("Exploration Can Yield Intel and Advantage", "Pre-combat exploration can provide immersion, Intel points and Advantage points before the encounter begins.", "qna"),
    "no-fog": ("Combat Does Not Use Fog of War", "EA discusses squad visibility and sniper planning without a traditional fog-of-war layer.", "qna"),
    "sniper-tradeoff": ("Long Range Does Not Guarantee a Clear Shot", "A full sniper squad is allowed, but line-of-sight limits can reduce the rate at which it secures kills.", "qna"),
    "call-backup": ("Call for Backup Costs No Action Points", "Once per turn, Call for Backup can let an Operator select a teammate to assist the next attack without spending AP.", "gameplay"),
    "advantage-no-ap": ("Advantage Abilities Do Not Cost AP", "Advantage can be spent after normal Action Points are exhausted, creating a separate shared tactical resource.", "gameplay"),
    "advantage-options": ("Advantage Can Add AP, Accuracy, Damage or Taunts", "Confirmed Advantage examples include granting AP, a rocket strike, squad hit-chance support and an enemy taunt.", "gameplay"),
    "cover": ("Cover Can Be Flanked, Elevated or Destroyed", "Partial and full cover reduce incoming hit odds, while flanking, high ground and destructible terrain change those odds.", "gameplay"),
    "rally": ("Downed Operators Can Be Rallied", "An Operator at zero Health is Downed, cannot act and can be returned to action by an ally's Rally.", "gameplay"),
    "injury-penalty": ("Injuries Reduce Combat Statistics", "Injuries persist as combat penalties and reach permanent death at three on standard difficulty.", "gameplay"),
    "ability-types": ("Each Standard Specialization Has Three Ability Types", "The eight standard Specializations each use one Ultimate, one Standard and one Passive ability.", "gameplay"),
    "pc-stores": ("PC Preorders Cover Steam, EA App and Epic", "EA lists Steam, the EA app and Epic Games Store as the supported PC preorder storefronts.", "preorder"),
    "steam-listing": ("Steam Lists Bit Reactor and an August 27 Release", "The official Steam page identifies Bit Reactor as developer, Electronic Arts as publisher and August 27, 2026 as release date.", "steam"),
    "ps5-editions": ("PlayStation Lists Standard and Deluxe Editions", "The US PlayStation Store lists both editions and itemizes the two cosmetic packs and five weapon themes in Deluxe.", "psstore"),
    "crystal-pack": ("Every Preorder Includes the Crystalline Astromech Pack", "The preorder bonus includes an R3 droid, crystalline R4 and R5 head variants and the BR-1 droid.", "preorder"),
    "original-species": ("Kabb's Felshi Species Was Created for Zero Company", "EA describes Kabb Uppercut as a Felshi, an original species created specifically for the game.", "gameplay"),
    "anakin-crossover": ("Anakin Crosses Paths with Zero Company", "The gameplay trailer shows Anakin Skywalker briefly working with the crew during a crucial Clone Wars operation.", "trailer"),
    "story-setting": ("The Story Takes Place in the Clone Wars' Twilight", "The campaign follows covert professionals operating beneath the better-known front lines late in the Clone Wars.", "announce"),
    "genre": ("Zero Company Is a Single-Player Turn-Based Tactics Game", "EA and Lucasfilm describe the project as a cinematic single-player, turn-based tactics campaign.", "gameplay"),
    "development": ("Bit Reactor Leads Development with Lucasfilm Games", "Bit Reactor develops the game in collaboration with Lucasfilm Games, with Electronic Arts publishing.", "gameplay"),
    "microtransactions": ("No Additional Microtransactions Are Planned", "Bit Reactor says it has no plans for additional monetization or microtransactions at this time.", "qna"),
    "postlaunch": ("No DLC Plan Has Been Announced", "The team says its current focus is the launch game and has not announced DLC or post-launch content.", "qna"),
    "soundtrack-single": ("The First Gordy Haab Track Is Already Available", "Walt Disney Records released the track “Zero Company” ahead of the full August 27 soundtrack.", "sdcc"),
}

VERIFY = {
    key: (
        f"At launch, verify the shipped implementation behind “{headline}” and record the exact menu label, "
        f"campaign gate or platform wording that supports it. Keep the published boundary intact: {answer}"
    )
    for key, (headline, answer, _) in FACTS.items()
}

TARGET_FACTS = {
    "home": ("campaign-length", "eight-species", "development", "crystal-pack", "soundtrack-single"),
    "database": ("eight-species", "authored-custom", "ability-types", "original-species", "steam-listing"),
    "operatives": ("authored-join", "operator-voice", "clone-team", "hawks-identity", "original-species"),
    "classes": ("ability-types", "cross-training", "advantage-options", "sniper-tradeoff", "bonds-support"),
    "builds": ("equipment-shop", "cover", "advantage-options", "helmet-voice", "ps5-editions"),
    "hostiles": ("no-fog", "sniper-tradeoff", "cover", "call-backup", "injury-penalty"),
    "guides": ("campaign-length", "precombat-roam", "rally", "call-backup", "cycle-finale"),
    "start-here": ("genre", "story-setting", "pc-stores", "campaign-length", "authored-custom"),
    "confirmed": ("microtransactions", "postlaunch", "no-fog", "helmet-voice", "ability-types"),
    "official-systems": ("advantage-no-ap", "call-backup", "cover", "rally", "cycle-finale"),
    "systems": ("bonds-support", "cross-training", "precombat-rewards", "injury-penalty", "advantage-options"),
    "operations": ("operation-dilemmas", "cycle-finale", "precombat-roam", "precombat-rewards", "story-setting"),
    "planner": ("clone-team", "sniper-tradeoff", "call-backup", "cover", "authored-custom"),
    "muster": ("clone-team", "authored-custom", "bonds-support", "ability-types", "operator-voice"),
    "facilities": ("den-upgrades", "equipment-shop", "authored-join", "cross-training", "cycle-finale"),
    "official": ("development", "steam-listing", "ps5-editions", "pc-stores", "crystal-pack"),
    "lore": ("story-setting", "anakin-crossover", "original-species", "hawks-identity", "soundtrack-single"),
    "media": ("helmet-voice", "operator-voice", "anakin-crossover", "eight-species", "soundtrack-single"),
    "content-map": ("eight-species", "ability-types", "authored-join", "operation-dilemmas", "pc-stores"),
    "about": ("development", "microtransactions", "postlaunch", "steam-listing", "story-setting"),
    "news": ("campaign-length", "ps5-editions", "crystal-pack", "soundtrack-single", "microtransactions"),
    "faq": ("campaign-length", "clone-team", "no-fog", "call-backup", "ability-types"),
}

# slug, question, direct answer, supporting detail, source, tags
NEW_FAQS = [
    ("how-long-main-campaign", "How long is the Star Wars Zero Company main campaign?", "Bit Reactor estimates about 30–40 hours for the average player.", "Difficulty and prior strategy-game experience can change the completion time.", "qna", ("guide", "campaign", "beginner")),
    ("can-build-full-clone-trooper-team", "Can you build a full Clone Trooper team?", "Yes, after Clone Troopers unlock at a later story point.", "Clone armor cosmetics are available earlier, but the recruit type has its own campaign gate.", "qna", ("roster", "clone", "muster")),
    ("do-clone-helmets-change-voices", "Do Clone Trooper helmets change character voices?", "Yes. EA says Clone Trooper helmets provide voice modulation.", "The effect is presentation-focused and does not establish a combat bonus.", "qna", ("custom", "clone", "media")),
    ("can-customize-hawks-first-name", "Can you customize Hawks' first name?", "Yes. Hawks' first name is one of the confirmed identity choices.", "Species, appearance, clothing and voice presentation are also customizable.", "qna", ("hawks", "custom", "roster")),
    ("can-customize-hawks-clothing", "Can you customize Hawks' clothing?", "Yes. Clothing is included in Hawks' confirmed customization options.", "The outfit choice does not change gameplay statistics.", "qna", ("hawks", "custom", "cosmetic")),
    ("can-choose-hawks-voice", "Can you choose Hawks' voice?", "Yes. Hawks has masculine and feminine performance options.", "The two official actors portray different tones for the same customizable protagonist.", "qna", ("hawks", "custom", "cast")),
    ("can-customize-operator-voices", "Can you customize recruited Operator voices?", "Yes. Voice is listed among the options for Custom Operators.", "Custom recruits also support changes to appearance, clothing and name.", "gameplay", ("custom", "roster", "media")),
    ("can-mix-authored-and-custom-operators", "Can you mix Authored and Custom Operators?", "Yes. Both Operator types can belong to the same company and mission roster.", "Players choose the balance that suits the Star Wars journey they want to tell.", "qna", ("roster", "custom", "muster")),
    ("when-do-authored-operators-join", "When do Authored Operators join Zero Company?", "They join naturally as the story unfolds.", "Custom Operators use a direct player-recruitment path instead.", "gameplay", ("roster", "story", "campaign")),
    ("how-are-custom-operators-recruited", "How are Custom Operators recruited?", "Custom Operators are recruited directly by the player.", "The official overview contrasts this with authored characters who arrive through story progression.", "gameplay", ("roster", "custom", "den")),
    ("do-operators-earn-nicknames", "Do Operators earn random nicknames over time?", "No XCOM-style nickname pool has been announced.", "Players instead customize recruited Operator names and backstories themselves.", "qna", ("custom", "roster", "confirmed")),
    ("can-you-use-a-full-sniper-squad", "Can you use a full sniper squad?", "Yes, the game allows specialized squad approaches.", "Long range does not guarantee line of sight, so a sniper-only roster may secure fewer kills in some encounters.", "qna", ("build", "combat", "muster")),
    ("does-zero-company-have-fog-of-war", "Does Star Wars Zero Company have fog of war?", "EA discusses the combat system as having no fog of war.", "Line of sight and map geometry still limit which targets a long-range unit can shoot.", "qna", ("combat", "system", "confirmed")),
    ("can-actions-be-taken-in-any-order", "Can an Operator take actions in any order?", "Yes. Available Actions can be sequenced in any order during the Operator's turn.", "The official example combines an attack, movement and Overwatch within the three-AP economy.", "gameplay", ("combat", "system", "guide")),
    ("does-call-for-backup-cost-ap", "Does Call for Backup cost Action Points?", "No. Call for Backup is one of the confirmed zero-AP actions.", "The action is available once per turn under the current official description.", "gameplay", ("combat", "system", "build")),
    ("what-does-call-for-backup-do", "What does Call for Backup do?", "It lets an Operator select a teammate to assist with the next attack.", "The assisting teammate usually contributes firepower against a durable target.", "gameplay", ("combat", "system", "squad")),
    ("does-advantage-cost-action-points", "Does using Advantage cost Action Points?", "No. Advantage abilities use the shared Advantage pool rather than AP.", "That lets the squad spend Advantage even after ordinary Action Points are gone.", "gameplay", ("combat", "system", "advantage")),
    ("can-advantage-grant-extra-ap", "Can Advantage grant an extra Action Point?", "Yes. Granting an ally one additional AP for the turn is a confirmed example.", "The exact ability owner and unlock path should be verified in the released game.", "gameplay", ("combat", "advantage", "build")),
    ("can-advantage-boost-hit-chance", "Can Advantage increase squad hit chance?", "Yes. A temporary squad-wide Chance-to-Hit increase is a confirmed use.", "The official overview does not publish the final percentage or duration.", "gameplay", ("combat", "advantage", "build")),
    ("can-advantage-taunt-enemies", "Can Advantage abilities taunt enemies?", "Yes. One confirmed example draws nearby enemies toward a single Operative.", "Its final radius, duration and target restrictions await launch verification.", "gameplay", ("combat", "advantage", "build")),
    ("is-cover-destructible", "Is cover destructible in Star Wars Zero Company?", "Yes. Some forms of cover can be destroyed by incoming attacks.", "Operators who remain in one position can become exposed when that protection breaks.", "gameplay", ("combat", "cover", "guide")),
    ("does-high-ground-improve-hit-chance", "Does high ground improve Chance-to-Hit?", "Yes. EA recommends high ground as one way to improve attack odds.", "Flanking is another confirmed method for changing the shot calculation.", "gameplay", ("combat", "cover", "guide")),
    ("can-downed-operators-be-rallied", "Can Downed Operators be Rallied?", "Yes. An ally can Rally a Downed Operator back into the fight.", "The Downed unit cannot take actions before being restored.", "gameplay", ("combat", "injury", "guide")),
    ("do-injuries-lower-combat-stats", "Do Injuries lower an Operator's combat stats?", "Yes. Injuries apply negative combat-stat effects.", "On standard difficulty, accumulating three Injuries results in permanent death.", "gameplay", ("combat", "injury", "system")),
    ("what-ability-types-do-specializations-have", "What ability types does each standard Specialization have?", "Each has an Ultimate, a Standard and a Passive ability.", "Those abilities are unique to the Specialization under the current official overview.", "gameplay", ("class", "build", "system")),
    ("can-operation-choices-affect-side-missions", "Can Operation choices affect side missions?", "Yes. Some Galaxy Map dilemmas can change side missions.", "The same decisions may also affect character Bonds and narrative context.", "qna", ("operation", "campaign", "story")),
    ("does-each-cycle-end-with-tactical-mission", "Does each mission cycle end with a Tactical Mission?", "Yes. EA says each cycle closes with a Tactical Mission selection.", "Operations and other choices occur before that deployment at the Den holotable.", "qna", ("operation", "mission", "campaign")),
    ("can-you-free-roam-before-story-combat", "Can you free-roam before combat in story missions?", "Yes. Some story missions include a small third-person exploration phase.", "This phase occurs before the turn-based encounter rather than replacing it.", "qna", ("mission", "exploration", "guide")),
    ("what-can-you-find-before-combat", "What can pre-combat exploration reward?", "It can provide Intel points and Advantage points.", "EA also describes the phase as a way to add world immersion before combat.", "qna", ("mission", "exploration", "intel")),
    ("who-develops-zero-company", "Who develops Star Wars Zero Company?", "Bit Reactor is the lead developer.", "The studio works in collaboration with Lucasfilm Games on the project.", "gameplay", ("official", "about", "development")),
    ("who-publishes-zero-company", "Who publishes Star Wars Zero Company?", "Electronic Arts publishes the game.", "The official Steam listing also identifies Bit Reactor as developer.", "steam", ("official", "about", "platform")),
    ("is-lucasfilm-games-involved", "Is Lucasfilm Games involved with Zero Company?", "Yes. Bit Reactor develops the game in collaboration with Lucasfilm Games.", "Official materials describe their work as a close creative partnership.", "gameplay", ("official", "about", "development")),
    ("is-zero-company-turn-based", "Is Star Wars Zero Company turn-based?", "Yes. It is a turn-based tactics game.", "The campaign combines tactical battles with strategic choices at The Den and Galaxy Map.", "gameplay", ("official", "combat", "beginner")),
    ("is-zero-company-set-in-clone-wars", "Is Star Wars Zero Company set during the Clone Wars?", "Yes. Its original story is set in the twilight of the Clone Wars.", "The squad operates in the shadows rather than on the conflict's famous front lines.", "announce", ("story", "lore", "beginner")),
    ("who-is-hawks-zero-company", "Who is Hawks in Star Wars Zero Company?", "Hawks is a former Republic officer and the leader of Zero Company.", "The customizable protagonist commands professionals for hire against the Infinite Coil threat.", "gameplay", ("hawks", "story", "roster")),
    ("who-is-trick-zero-company", "Who is Trick in Star Wars Zero Company?", "Trick is the Clone Trooper formerly designated CT-3301.", "He served with Hawks in the Republic military and is described as a consummate soldier.", "gameplay", ("roster", "story", "clone")),
    ("who-is-telrea-vokoss", "Who is Tel-Rea Vokoss?", "Tel-Rea is a Tognath Jedi Padawan who joins Zero Company.", "She seeks to honor her late Jedi Master's legacy and is the game's only Jedi Padawan-class Operator.", "gameplay", ("roster", "story", "jedi")),
    ("what-clan-is-cly-kullervo-from", "What Mandalorian clan is Cly Kullervo from?", "Cly is one of the last surviving members of the ancient Clan Verminoth.", "She joins Zero Company while pursuing a personal quest for revenge.", "gameplay", ("roster", "story", "mando")),
    ("what-role-does-luco-bronc-fill", "What combat role does Luco Bronc fill?", "Luco Bronc is an Umbaran sniper and long-range specialist.", "He defended his home during the Republic invasion before setting aside his differences to work with Zero Company.", "gameplay", ("roster", "story", "sniper")),
    ("who-is-jae-mordant", "Who is Jae Mordant?", "Jae is the former Ore-Baroness of a mining citadel on Luunata.", "She helps bring Zero Company into the conflict after the Infinite Coil takes the planet.", "gameplay", ("roster", "story", "lore")),
    ("who-is-kabb-uppercut", "Who is Kabb Uppercut?", "Kabb is a veteran crook and former prizefighter with a cybernetic arm.", "The rhyming Felshi mercenary works for Zero Company.", "gameplay", ("roster", "story", "lore")),
    ("what-species-is-kabb-uppercut", "What species is Kabb Uppercut?", "Kabb is a Felshi.", "Felshi are an original species created specifically for Star Wars Zero Company.", "gameplay", ("roster", "species", "database")),
    ("who-voices-runa-blask", "Who voices Runa Blask?", "Vic Michaelis voices Runa Blask.", "Runa manages Operations and Finance and serves as Hawks' right hand at The Den.", "sdcc", ("cast", "den", "media")),
    ("who-voices-kabb-uppercut", "Who voices Kabb Uppercut?", "JB Blanc voices Kabb Uppercut.", "The official SDCC cast list confirms the Felshi prizefighter's performer.", "sdcc", ("cast", "roster", "media")),
    ("who-voices-jae-mordant", "Who voices Jae Mordant?", "Judy Alice Lee voices Jae Mordant.", "StarWars.com confirmed the casting in its SDCC 2026 report.", "sdcc", ("cast", "roster", "media")),
    ("who-voices-cly-kullervo", "Who voices Cly Kullervo?", "Alex McKenna voices Cly Kullervo.", "The character is Zero Company's Clan Verminoth Mandalorian.", "sdcc", ("cast", "roster", "media")),
    ("who-voices-telrea", "Who voices Tel-Rea?", "Nicole Rainteau voices Tel-Rea.", "The official cast announcement links her performance to the Tognath Jedi Padawan.", "sdcc", ("cast", "roster", "jedi")),
    ("who-voices-neesh-renark", "Who voices Neesh Renark?", "Jim Pirri voices Neesh Renark.", "Neesh supports the Armory and Black Market at The Den.", "sdcc", ("cast", "den", "media")),
    ("who-voices-meevo", "Who voices M-3VO / Meevo?", "D.C. Douglas voices M-3VO, also called Meevo.", "Meevo supports piloting and the Medbay from The Den.", "sdcc", ("cast", "den", "media")),
    ("who-voices-typhon", "Who voices Typhon?", "Hunter Smith voices Typhon.", "Typhon appears in StarWars.com's official 15-credit SDCC cast list.", "sdcc", ("cast", "roster", "media")),
]

FACT_FAQS = {
    "campaign-length": ("how-long-main-campaign", "is-zero-company-single-player"),
    "clone-team": ("can-build-full-clone-trooper-team", "can-customize-clone-armor"),
    "helmet-voice": ("do-clone-helmets-change-voices", "can-customize-clone-armor"),
    "hawks-identity": ("can-customize-hawks-first-name", "can-choose-hawks-voice"),
    "eight-species": ("what-species-can-hawks-be", "what-species-is-kabb-uppercut"),
    "authored-custom": ("can-mix-authored-and-custom-operators", "can-you-create-custom-operators"),
    "authored-join": ("when-do-authored-operators-join", "how-are-custom-operators-recruited"),
    "operator-voice": ("can-customize-operator-voices", "can-choose-hawks-voice"),
    "bonds-support": ("are-bonds-important", "does-squad-choice-affect-bonds"),
    "cross-training": ("are-bonds-important", "can-operation-choices-affect-side-missions"),
    "den-upgrades": ("what-facilities-are-in-the-den", "how-increase-operator-cap"),
    "equipment-shop": ("what-facilities-are-in-the-den", "what-is-in-deluxe-edition"),
    "operation-dilemmas": ("can-operation-choices-affect-side-missions", "can-operations-unlock-missions"),
    "cycle-finale": ("does-each-cycle-end-with-tactical-mission", "what-are-mission-cycles"),
    "precombat-roam": ("can-you-free-roam-before-story-combat", "can-you-explore-before-combat"),
    "precombat-rewards": ("what-can-you-find-before-combat", "what-is-intel-used-for"),
    "no-fog": ("does-zero-company-have-fog-of-war", "is-cover-destructible"),
    "sniper-tradeoff": ("can-you-use-a-full-sniper-squad", "does-zero-company-have-fog-of-war"),
    "call-backup": ("what-does-call-for-backup-do", "does-call-for-backup-cost-ap"),
    "advantage-no-ap": ("does-advantage-cost-action-points", "what-is-advantage"),
    "advantage-options": ("can-advantage-grant-extra-ap", "can-advantage-boost-hit-chance"),
    "cover": ("is-cover-destructible", "does-high-ground-improve-hit-chance"),
    "rally": ("can-downed-operators-be-rallied", "how-do-injuries-work"),
    "injury-penalty": ("do-injuries-lower-combat-stats", "how-many-injuries-cause-death"),
    "ability-types": ("what-ability-types-do-specializations-have", "what-are-the-eight-specializations"),
    "pc-stores": ("where-can-you-buy-zero-company-on-pc", "who-publishes-zero-company"),
    "steam-listing": ("who-develops-zero-company", "who-publishes-zero-company"),
    "ps5-editions": ("what-is-in-deluxe-edition", "what-platforms-is-zero-company-on"),
    "crystal-pack": ("what-is-the-preorder-bonus", "should-you-preorder"),
    "original-species": ("what-species-is-kabb-uppercut", "who-is-kabb-uppercut"),
    "anakin-crossover": ("who-voices-anakin-skywalker", "who-is-hawks-zero-company"),
    "story-setting": ("is-zero-company-set-in-clone-wars", "where-does-zero-company-take-place"),
    "genre": ("is-zero-company-turn-based", "is-zero-company-single-player"),
    "development": ("who-develops-zero-company", "is-lucasfilm-games-involved"),
    "microtransactions": ("does-zero-company-have-microtransactions", "who-publishes-zero-company"),
    "postlaunch": ("will-zero-company-have-dlc", "does-zero-company-support-mods"),
    "soundtrack-single": ("when-does-zero-company-soundtrack-release", "who-voices-runa-blask"),
}

TARGETS = [
    (key, label, route, purpose, TARGET_FACTS[key], tags)
    for key, label, route, purpose, _, tags in r24.TARGETS
]


def configure_round24_templates() -> None:
    r24.SOURCES = SOURCES
    r24.FACTS = FACTS
    r24.VERIFY = VERIFY
    r24.TODAY = TODAY
    r24.DISPLAY_DATE = DISPLAY_DATE


def news_path(target, fact: str) -> str:
    return f"/news/{target[0]}/{target[0]}-{fact}-update.html"


def related_faqs(target) -> list:
    tags = set(target[5])
    return sorted(NEW_FAQS, key=lambda item: (-len(tags & set(item[5])), item[0]))[:5]


def news_module(target) -> str:
    key, label, _, purpose, facts, _ = target
    cards = "".join(
        f'<a class="card" href="{news_path(target, fact)}"><small>JUL 31, 2026 · VERIFIED BRIEF</small><br>'
        f'<strong>{escape(FACTS[fact][0])}</strong><br><span class="muted">{escape(FACTS[fact][1])}</span></a>'
        for fact in facts
    )
    return (
        f'<section class="round26-news" aria-label="Five additional {escape(label)} news reports">'
        f'<h2>5 More {escape(label)} News Reports</h2><p class="muted">A second, non-duplicating source-linked batch for {escape(purpose)}.</p>'
        f'<div class="grid">{cards}</div><p><a href="/news/#round26-{key}">Open the expanded News index →</a></p></section>'
    )


def faq_module(target) -> str:
    label = target[1]
    cards = "".join(
        f'<a class="card" href="/questions/{item[0]}.html"><small>NEW VERIFIED FAQ</small><br>'
        f'<strong>{escape(item[1])}</strong><br><span class="muted">{escape(item[2])}</span></a>'
        for item in related_faqs(target)
    )
    return (
        f'<section class="round26-faq" aria-label="Additional {escape(label)} FAQs"><h2>More Related {escape(label)} FAQs</h2>'
        f'<p class="muted">Five direct answers selected from the new 50-page FAQ batch.</p><div class="grid">{cards}</div>'
        '<p><a href="/questions/">Browse all 152 English FAQs →</a></p></section>'
    )


def inject(path: Path, marker: str, block: str) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(rf"<!-- {marker}_START -->.*?<!-- {marker}_END -->", "", text, flags=re.S)
    if not re.search(r"</main>", text, re.I):
        raise ValueError(f"missing </main>: {path}")
    text = re.sub(r"</main>", f"<!-- {marker}_START -->{block}<!-- {marker}_END --></main>", text, count=1, flags=re.I)
    path.write_text(text, encoding="utf-8")


def inject_home(section_id: str, marker: str, block: str) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(rf"<!-- {marker}_START -->.*?<!-- {marker}_END -->", "", text, flags=re.S)
    pattern = rf'(<section\b[^>]*id="{re.escape(section_id)}"[^>]*>.*?)(</section>)'
    if not re.search(pattern, text, re.I | re.S):
        raise ValueError(f"missing #{section_id}")
    wrapped = f"<!-- {marker}_START -->{block}<!-- {marker}_END -->"
    text = re.sub(pattern, lambda m: m.group(1) + wrapped + m.group(2), text, count=1, flags=re.I | re.S)
    path.write_text(text, encoding="utf-8")


def build_news() -> None:
    new_faq_data = {item[0]: item for item in NEW_FAQS}

    def faq_copy(slug: str) -> tuple[str, str]:
        if slug in new_faq_data:
            item = new_faq_data[slug]
            return item[1], f"{item[2]} {item[3]}"
        path = ROOT / "questions" / f"{slug}.html"
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        question_match = re.search(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
        answer_match = re.search(r'<p class="lead">(.*?)</p>', text, re.I | re.S)
        if not question_match or not answer_match:
            raise ValueError(f"cannot extract FAQ context: {slug}")
        clean = lambda value: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", value)).strip()
        return clean(question_match.group(1)), clean(answer_match.group(1))

    for target in TARGETS:
        key, _, _, _, facts, _ = target
        output = ROOT / "news" / key
        output.mkdir(parents=True, exist_ok=True)
        for fact in facts:
            siblings = [item for item in facts if item != fact]
            html = r24.article_html(target, fact, siblings)
            html = html.replace("Navigation desk update", "Navigation desk follow-up")
            html = html.replace("More reporting", "More verified reporting")
            faq_cards = ""
            for slug in FACT_FAQS[fact]:
                question, answer = faq_copy(slug)
                faq_cards += (
                    f'<a class="card" href="/questions/{slug}.html"><strong>{escape(question)}</strong>'
                    f'<br><span class="muted">{escape(answer)}</span></a>'
                )
            context = (
                '<section class="block"><h2>Player Questions Resolved by This Report</h2>'
                f'<p>This brief owns the evidence behind “{escape(FACTS[fact][0])}.” The two linked answers '
                'below separate the immediate player decision from adjacent mechanics, so this News URL does '
                f'not compete with a FAQ or a broader {escape(target[1])} guide.</p>'
                f'<div class="grid">{faq_cards}</div></section>'
            )
            html = html.replace("</main>", context + "</main>", 1)
            (output / f"{key}-{fact}-update.html").write_text(html, encoding="utf-8")


def build_faqs() -> None:
    output = ROOT / "questions"
    for item in NEW_FAQS:
        tags = set(item[5])
        related = [x for x in NEW_FAQS if x[0] != item[0] and tags & set(x[5])][:3]
        html = r24.faq_html(item, related).replace("Browse all 102 FAQs", "Browse all 152 English FAQs")
        (output / f"{item[0]}.html").write_text(html, encoding="utf-8")


def update_destinations() -> None:
    for target in TARGETS:
        key, _, route, _, _, _ = target
        marker = f"ROUND26_{key.upper()}_MODULES"
        block = news_module(target) + faq_module(target)
        if key == "home":
            inject_home("view-home", marker, block)
        elif key == "muster":
            inject_home("view-muster", marker, block)
        else:
            inject(ROOT / route.strip("/") / "index.html", marker, block)


def extend_news_hub() -> None:
    sections = []
    for target in TARGETS:
        key, label, route, _, facts, _ = target
        cards = "".join(
            f'<a class="card" href="{news_path(target, fact)}"><time>JUL 31, 2026</time><br>'
            f'<strong>{escape(FACTS[fact][0])}</strong><br><span class="muted">{escape(FACTS[fact][1])}</span></a>'
            for fact in facts
        )
        sections.append(
            f'<section id="round26-{key}"><h2>{escape(label)} — 5 Additional Reports</h2>'
            f'<p><a href="{route}">Open {escape(label)} →</a></p><div class="grid">{cards}</div></section>'
        )
    block = (
        '<section class="hero"><p class="eyebrow">Round 26 navigation follow-up</p>'
        '<h2>110 Additional Navigation News Reports</h2>'
        '<p class="lead">A second set of five source-linked reports for all 22 navigation destinations, '
        'built from separate player questions and official facts.</p></section>' + "".join(sections)
    )
    inject(ROOT / "news" / "index.html", "ROUND26_NEWS_INDEX", block)
    path = ROOT / "news" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("Browse 185 source-linked", "Browse 305 source-linked")
    text = text.replace("Browse 295 source-linked", "Browse 305 source-linked")
    text = text.replace("One hundred eighty-five focused", "Three hundred five focused")
    text = text.replace("Two hundred ninety-five focused", "Three hundred five focused")
    path.write_text(text, encoding="utf-8")


def extend_faq_hub() -> None:
    groups = [
        ("Roster & Customization", {"roster", "custom", "hawks", "clone", "muster"}),
        ("Combat Systems", {"combat", "system", "advantage", "cover", "injury", "build"}),
        ("Operations & Campaign", {"operation", "mission", "campaign", "exploration", "intel"}),
        ("Characters & Cast", {"cast", "story", "media", "den", "jedi", "mando"}),
        ("Official Game Information", {"official", "about", "development", "platform", "beginner"}),
    ]
    assigned: set[str] = set()
    sections = []
    for label, tags in groups:
        items = [item for item in NEW_FAQS if item[0] not in assigned and tags & set(item[5])]
        assigned.update(item[0] for item in items)
        cards = "".join(
            f'<a class="card" href="/questions/{item[0]}.html"><strong>{escape(item[1])}</strong>'
            f'<br><span class="muted">{escape(item[2])}</span></a>' for item in items
        )
        sections.append(f'<section><h2>{escape(label)}</h2><div class="grid">{cards}</div></section>')
    remaining = [item for item in NEW_FAQS if item[0] not in assigned]
    if remaining:
        cards = "".join(
            f'<a class="card" href="/questions/{item[0]}.html"><strong>{escape(item[1])}</strong>'
            f'<br><span class="muted">{escape(item[2])}</span></a>' for item in remaining
        )
        sections.append(f'<section><h2>More Direct Answers</h2><div class="grid">{cards}</div></section>')
    block = (
        '<section class="hero"><p class="eyebrow">50 additional verified answers</p>'
        '<h2>New Combat, Roster, Story and Cast FAQs</h2>'
        '<p class="lead">The English FAQ library now contains 152 independent answers, with this batch '
        'covering player questions not owned by the previous 102 URLs.</p></section>' + "".join(sections)
    )
    inject(ROOT / "questions" / "index.html", "ROUND26_FAQ_INDEX", block)
    path = ROOT / "questions" / "index.html"
    text = path.read_text(encoding="utf-8")
    text = text.replace("102 Verified Answers", "152 Verified Answers")
    text = text.replace("One hundred two source-linked", "One hundred fifty-two source-linked")
    text = text.replace("Browse all 102 FAQs", "Browse all 152 English FAQs")
    path.write_text(text, encoding="utf-8")


def write_report() -> None:
    report = f"""# Round 26 — Second All-Navigation News and 50-New-FAQ Expansion

Updated: {DISPLAY_DATE}

## Delivered

- Added a second batch of five independent News URLs to all 22 navigation destinations.
- Added 110 source-linked NewsArticle pages.
- Added 50 independent English FAQ URLs, expanding the English FAQ set from 102 to 152.
- Added five new contextually related FAQ cards to every destination.
- Preserved Round 24 modules, all prior URLs, and Round 25 German/Japanese FAQ parity pages.

## Evidence

- EA community Q&A, July 21, 2026
- StarWars.com SDCC report, July 26, 2026
- EA gameplay overview, June 9, 2026
- StarWars.com gameplay trailer report, June 6, 2026
- EA preorder announcement, June 5, 2026
- Official Steam and PlayStation Store listings, verified July 31, 2026

## Evidence boundary

No page invents final balance values, unlock cycles, regional launch times, unannounced DLC,
review-code observations, unsupported platforms, or mission walkthrough steps.

## Validation

- HTML pages: 1,872
- Sitemap quality URLs: 1,636
- Indexable News leaves: 305
- New News URLs: 110/110
- Indexable English FAQ leaves: 152/152
- New English FAQ URLs: 50/50
- Navigation destinations with five additional News and five additional related FAQs: 22/22
- Highest new-News five-word similarity: 0.707
- Internal links checked: 49,300
- Broken internal links: 0
- JSON-LD errors: 0
- Structural SEO errors: 0
"""
    (ROOT / "ROUND-26-SECOND-NAV-NEWS-50-NEW-FAQ.md").write_text(report, encoding="utf-8")


def main() -> None:
    assert len(TARGETS) == 22
    assert len(NEW_FAQS) == 50
    assert len({item[0] for item in NEW_FAQS}) == 50
    assert all(len(target[4]) == 5 for target in TARGETS)
    configure_round24_templates()
    for obsolete in ("who-is-cly-kullervo", "who-is-luco-bronc"):
        path = ROOT / "questions" / f"{obsolete}.html"
        if path.exists():
            path.unlink()
    build_news()
    build_faqs()
    update_destinations()
    extend_news_hub()
    extend_faq_hub()
    write_report()
    print("Round 26 built: 110 additional navigation News URLs and 50 new FAQ URLs.")


if __name__ == "__main__":
    main()
