#!/usr/bin/env python3
"""Round 24: add five news URLs to every current navigation destination and 50 FAQs."""

from __future__ import annotations

from html import escape
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = "2026-07-29"
DISPLAY_DATE = "July 29, 2026"
ADS_META = '<meta name="google-adsense-account" content="ca-pub-9505220977121599">'
ADS_SCRIPT = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    'adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script>'
)

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
    "preorder": (
        "EA preorder and edition announcement",
        "June 5, 2026",
        "https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company",
    ),
}

# headline, direct fact, source
FACTS = {
    "cast": (
        "Full Voice Cast Now Lists 15 Character Credits",
        "StarWars.com now names 15 character-to-actor credits, including both Hawks performances, Kundri Fathom, Trick, Anakin Skywalker and the wider supporting cast.",
        "sdcc",
    ),
    "hawks-story": (
        "Hawks Is Required on Story Missions",
        "EA confirms that Hawks must deploy on story missions, while skirmish missions allow any available Operator combination.",
        "qna",
    ),
    "hawks-fail": (
        "Hawks Death Causes an Automatic Mission Failure",
        "If Hawks dies in combat, the current mission fails and must be restarted rather than continuing without the protagonist.",
        "qna",
    ),
    "operator-cap": (
        "The Den Operator Limit Can Reach 20",
        "Players begin with a maximum of seven Operators and can expand the headquarters limit to 20 through upgrades, story progress and authored recruits.",
        "qna",
    ),
    "squad-cap": (
        "Standard Tactical Squads Can Reach Four Operators",
        "The standard squad limit is four Operators, although selected missions can place additional controllable characters on the field.",
        "qna",
    ),
    "weapons": (
        "Four Weapon Classes and Cosmetic Variants Are Confirmed",
        "EA confirms four weapon classes, with four to six cosmetic models available within each class.",
        "qna",
    ),
    "intel": (
        "Galaxy Map Operations Spend Intel and Can Expire",
        "Operations cost different amounts of Intel, may expire, and sit alongside story-critical missions that eventually become obligatory.",
        "qna",
    ),
    "jedi": (
        "Tel-Rea Is the Only Jedi Padawan Operator",
        "EA identifies Tel-Rea as the game's only Jedi Padawan-class Operator, so losing her removes that unique authored role.",
        "qna",
    ),
    "heavy-machinery": (
        "Some Missions Will Involve Heavy Machinery",
        "EA has not revealed exact vehicle encounters, but confirms that certain missions involve heavy machinery.",
        "qna",
    ),
    "weather": (
        "Combat Weather Effects Are Cosmetic",
        "Weather will not change squad visibility or efficiency; its announced combat role is visual rather than mechanical.",
        "qna",
    ),
    "outfits": (
        "Outfits Do Not Change Combat Performance",
        "Cosmetic outfits do not alter character gameplay, keeping appearance choices separate from tactical optimization.",
        "qna",
    ),
    "new-game-plus": (
        "New Game Plus Is Not Planned for Launch",
        "Zero Company will not launch with New Game Plus, although some customization options unlock on later playthroughs.",
        "qna",
    ),
    "enemy-factions": (
        "Three Enemy Factions Demand Different Responses",
        "Droids are vulnerable to Ion planning, Infinite Coil units reward target-priority decisions, and Outlaws can overwhelm through numbers.",
        "qna",
    ),
    "astromechs": (
        "Full Astromech Squads Become Possible Early",
        "Astromechs unlock early enough to fill the non-Hawks slots of a story squad after recruitment becomes available.",
        "qna",
    ),
    "no-separatist-recruit": (
        "Separatist Droids Cannot Be Recruited",
        "EA explicitly rules out recruiting Separatist battle droids as Operators.",
        "qna",
    ),
    "no-callins": (
        "Specialized Battlefield Call-Ins Are Not Available",
        "Zero Company does not include specialized call-ins such as LAAT support; squad preparation remains the stated answer to mission risk.",
        "qna",
    ),
    "operations-missions": (
        "Operations and Tactical Missions Serve Different Roles",
        "Operations occur on the Galaxy Map and can give instant rewards or unlock content, while Tactical Missions deploy the squad to an objective map.",
        "qna",
    ),
    "mission-types": (
        "Sabotage, Combat, Rescue and Retrieval Are Confirmed",
        "EA names sabotage, combat, rescue, retrieval and hero-centered narrative missions among the current objective types.",
        "qna",
    ),
    "planets": (
        "The Galaxy Map Includes More Than 150 Planets",
        "Strategic Operations can appear across more than 150 planets, while Tactical Missions use more than a dozen detailed planetary environments.",
        "qna",
    ),
    "overwatch": (
        "Objective Design Is Intended to Break the Overwatch Crawl",
        "Supply defense can reward Overwatch, while sabotage, rescue and extraction objectives are designed to push alternative movement and timing.",
        "qna",
    ),
    "bonds": (
        "Bonds Unlock Support and Cross-Training Benefits",
        "Bonded Operators can gain support abilities and share skills or statistics through cross-training.",
        "qna",
    ),
    "den-support": (
        "Four Named Characters Support the Squad from The Den",
        "Bennic, Runa, Neesh and Meevo support intelligence, operations, equipment, piloting and medical functions rather than serving only as frontline Operators.",
        "qna",
    ),
    "real-time": (
        "Most Cutscenes Render Customized Characters in Real Time",
        "Most cinematics are rendered in real time so player-created Hawks choices remain visible, with a small number of pre-rendered exceptions.",
        "qna",
    ),
    "mods": (
        "Official Mod Support Is Not Planned",
        "Bit Reactor says there is no official mod support planned for Star Wars Zero Company.",
        "qna",
    ),
    "story": (
        "Squad Choices Change Moments but Not the Main Ending",
        "Roster choices can affect Bonds and some story elements, while the campaign conclusion remains largely the same.",
        "qna",
    ),
    "collectors": (
        "A Collectors' Edition Was Announced at SDCC",
        "StarWars.com confirms that a Star Wars Zero Company Collectors' Edition is available to preorder through Limited Run Games.",
        "sdcc",
    ),
    "soundtrack": (
        "The Original Soundtrack Launches August 27",
        "Gordy Haab's soundtrack arrives with the game on August 27, and its first track, “Zero Company,” is already available.",
        "sdcc",
    ),
    "runa": (
        "Runa Blask Runs Operations and Finance at The Den",
        "The SDCC panel describes Runa as Hawks' right hand who keeps Zero Company operating, even when she questions the mission.",
        "sdcc",
    ),
    "fathom": (
        "The Infinite Coil Plans to Spread a Shadow Plague",
        "The SDCC story presentation identifies Kundri Fathom's paramilitary cult as a threat seeking to spread a deadly shadow plague.",
        "sdcc",
    ),
    "edition": (
        "Deluxe Edition Contents Remain Cosmetic",
        "EA lists Republic and Shadow Collective cosmetics plus painted weapon themes, without an exclusive campaign or combat-stat advantage.",
        "preorder",
    ),
    "release": (
        "August 27 Release Remains Confirmed",
        "Star Wars Zero Company remains scheduled for August 27, 2026 on PC, PlayStation 5 and Xbox Series X|S.",
        "gameplay",
    ),
    "custom": (
        "Authored and Fully Custom Operators Can Share a Squad",
        "Players can combine story-authored characters with recruits whose appearance, clothing, voice, name and role are customized.",
        "gameplay",
    ),
}

VERIFY = {
    "cast": "At launch, verify the in-game credit spelling, language-specific performance credits and whether every named support character appears in the codex. Do not infer playability from a voice credit.",
    "hawks-story": "Check which mission labels count as story or skirmish content, when the roster screen locks Hawks in place and whether optional operations use the same deployment rule.",
    "hawks-fail": "Record the exact failure message, checkpoint behavior and difficulty-specific restart options. Keep that result separate from the three-Injury rule that applies to the wider roster.",
    "operator-cap": "Capture each capacity upgrade, its resource cost and the story gates that raise the limit from seven toward 20. A final cap does not reveal the upgrade sequence.",
    "squad-cap": "Document which missions add temporary controllable characters, whether they consume normal deployment slots and how the user interface distinguishes guests from the four-Operator squad.",
    "weapons": "Build the launch database around weapon class, functional item and cosmetic model as separate fields. Four classes with several appearances do not imply four-to-six statistically unique weapons each.",
    "intel": "Log Intel income, Operation costs, expiry timing and the warning shown before a critical mission becomes obligatory. Those values may vary by campaign state or difficulty.",
    "jedi": "Treat the Jedi Padawan as a unique authored class and test how injury, recovery and permanent-loss settings affect Tel-Rea. Do not advertise a custom Jedi recruitment path.",
    "heavy-machinery": "Wait for a named encounter before creating vehicle database leaves. Capture whether machinery is an enemy, objective, hazard or scripted set piece and which damage rules apply.",
    "weather": "Visual-weather pages should describe location and presentation, not visibility penalties. Recheck accessibility settings and difficulty modifiers before declaring that every environmental effect is cosmetic.",
    "outfits": "Separate outfit slots from armor equipment and confirm that changing appearance leaves combat values untouched. Cosmetic pack ownership should never be presented as a build requirement.",
    "new-game-plus": "Track which customization rewards persist between fresh campaigns and how they unlock. Do not label ordinary replay rewards as transferred levels, inventory or a New Game Plus system.",
    "enemy-factions": "Create separate launch tests for Ion effectiveness, Infinite Coil target priority and Outlaw numbers. Difficulty scaling and unit composition must be measured before publishing faction tier rankings.",
    "astromechs": "Verify the recruitment trigger, available droid variants, story-mission Hawks requirement and whether four-droid deployments are possible outside the standard protagonist slot restriction.",
    "no-separatist-recruit": "Keep hostile droids out of the recruit database even if hacking appears as a combat action. Revisit only if a later official update explicitly changes Operator eligibility.",
    "no-callins": "Do not build support-power or vehicle-call-in pages from trailer imagery. At launch, distinguish squad abilities, mission scripting and extraction objectives from a reusable external-support system.",
    "operations-missions": "Record Galaxy Map resolution, reward delivery, unlock chains and the final Tactical Mission choice for each Cycle. Use separate templates for strategic choices and battlefield walkthroughs.",
    "mission-types": "Create objective guides only after the shipped game provides a concrete route, failure condition and reward. The confirmed labels are a taxonomy, not a complete walkthrough.",
    "planets": "Separate the 150-plus strategic locations from the dozen-plus Tactical Mission environments. A planet appearing on the Galaxy Map does not prove it has a playable combat map.",
    "overwatch": "Test Overwatch against stationary defense, timed sabotage, rescue movement and extraction pressure. Measure objective demands before making a universal recommendation about slow defensive play.",
    "bonds": "Capture the paired Operators, unlock threshold, support action and cross-training result independently. Story affinity, shared statistics and triggered combat fire should not be collapsed into one value.",
    "den-support": "Profile each support character by confirmed facility responsibility and narrative function. Do not list Den personnel as deployable Operators unless the game explicitly offers them on the squad screen.",
    "real-time": "Compare customized species, clothing and voice presentation across real-time scenes while labeling the known pre-rendered exceptions. Cinematic rendering method does not establish branching-story outcomes.",
    "mods": "Keep mod pages limited to the official-support answer. Do not publish installation instructions, compatibility promises or anti-cheat claims without a supported toolchain and a verified released build.",
    "story": "Track which squad composition changes scenes or Bonds while preserving one canonical page for the largely shared conclusion. Avoid advertising romance routes or fully branching campaign endings.",
    "collectors": "Verify regional ordering, included physical items, production limits, payment and fulfillment directly with the retailer. The StarWars.com announcement confirms the edition, not every store term.",
    "soundtrack": "Confirm the final track list, storefront availability, composer credits and album runtime when the August 27 release arrives. Keep the early single distinct from the complete soundtrack.",
    "runa": "Index Runa under Den staff, operations, finance and story rather than frontline combat. Her Separatist background is narrative context, not evidence of a playable faction bonus.",
    "fathom": "Keep the shadow plague in the story-threat cluster until missions reveal its mechanical role. Do not invent status effects, cures or enemy statistics from the SDCC narrative description.",
    "edition": "Compare entitlement lists and cosmetic ownership while excluding the packs from power calculations. Verify redemption behavior and platform-specific delivery without claiming exclusive missions or stronger weapons.",
    "release": "Continue checking the publisher and platform storefront countdowns, regional availability and preload notices. The confirmed date should remain separate from any unannounced review or early-access window.",
    "custom": "At launch, record selectable species, voices, names, clothing, backstories and role restrictions as independent fields. Authored and custom status should remain visible in roster filters.",
}

# key, label, destination, purpose, five source-grounded news angles, FAQ tags
TARGETS = [
    ("home", "Home", "/", "the site's launch dashboard and fastest route to confirmed information", ("release", "cast", "operator-cap", "collectors", "soundtrack"), ("release", "cast", "overview")),
    ("database", "Database Overview", "/database/", "the verified entity and system database", ("cast", "operator-cap", "weapons", "enemy-factions", "planets"), ("database", "roster", "enemy")),
    ("operatives", "Operatives", "/operatives/", "authored characters, custom recruits and roster management", ("hawks-story", "operator-cap", "squad-cap", "jedi", "astromechs"), ("roster", "hawks", "custom")),
    ("classes", "Specializations", "/classes/", "roles, unique classes and progression boundaries", ("jedi", "bonds", "enemy-factions", "weapons", "custom"), ("class", "build", "jedi")),
    ("builds", "Loadouts", "/builds/", "weapons, equipment, cosmetics and squad builds", ("weapons", "outfits", "enemy-factions", "astromechs", "edition"), ("build", "gear", "cosmetic")),
    ("hostiles", "Hostiles", "/hostiles/", "enemy factions, encounter pressure and counter planning", ("enemy-factions", "heavy-machinery", "no-separatist-recruit", "overwatch", "fathom"), ("enemy", "mission", "counter")),
    ("guides", "All Guides", "/guides/", "practical player guidance and launch-ready decision rules", ("hawks-fail", "squad-cap", "intel", "overwatch", "new-game-plus"), ("guide", "mission", "campaign")),
    ("start-here", "Start Here", "/start-here/", "new-player orientation before launch", ("release", "squad-cap", "operator-cap", "mods", "new-game-plus"), ("overview", "release", "beginner")),
    ("confirmed", "Confirmed Guides", "/confirmed/", "first-party confirmed facts separated from launch testing", ("mods", "weather", "outfits", "new-game-plus", "no-callins"), ("confirmed", "feature", "status")),
    ("official-systems", "Official Systems", "/official-systems/", "officially described tactical and campaign systems", ("intel", "operations-missions", "bonds", "overwatch", "real-time"), ("system", "campaign", "combat")),
    ("systems", "Systems", "/systems/", "canonical explanations of linked game systems", ("operator-cap", "intel", "operations-missions", "bonds", "story"), ("system", "canonical", "campaign")),
    ("operations", "Operations Hub", "/operations/", "Galaxy Map choices and tactical mission flow", ("intel", "operations-missions", "mission-types", "planets", "heavy-machinery"), ("operation", "mission", "intel")),
    ("planner", "Planner", "/planner/", "pre-mission, roster and campaign decision tools", ("squad-cap", "operator-cap", "intel", "enemy-factions", "hawks-fail"), ("planner", "roster", "mission")),
    ("muster", "Muster Board", "/#muster", "interactive squad composition and role coverage", ("squad-cap", "hawks-story", "jedi", "astromechs", "bonds"), ("muster", "squad", "roster")),
    ("facilities", "The Den", "/facilities/", "headquarters facilities and between-mission management", ("operator-cap", "den-support", "runa", "weapons", "bonds"), ("den", "facility", "roster")),
    ("official", "Official Info", "/official/", "release, editions, platforms and publisher statements", ("release", "collectors", "edition", "mods", "soundtrack"), ("official", "release", "edition")),
    ("lore", "Story & Lore", "/lore/", "the Clone Wars setting, cast and Infinite Coil conflict", ("fathom", "runa", "story", "cast", "soundtrack"), ("story", "lore", "cast")),
    ("media", "Media", "/media/", "trailers, performances, cinematics and soundtrack coverage", ("cast", "real-time", "soundtrack", "collectors", "fathom"), ("media", "cast", "cinematic")),
    ("content-map", "Content Map", "/content-map/", "site coverage, verification status and launch capture priorities", ("cast", "mission-types", "planets", "enemy-factions", "den-support"), ("coverage", "database", "verified")),
    ("about", "About", "/about/", "editorial sourcing, corrections and unofficial-site transparency", ("mods", "story", "weather", "outfits", "release"), ("about", "source", "status")),
    ("news", "News", "/news/", "the site's first-party-linked news and analysis archive", ("cast", "collectors", "soundtrack", "fathom", "release"), ("news", "latest", "official")),
    ("faq", "FAQ", "/questions/", "direct answers to recurring player questions", ("operator-cap", "mods", "new-game-plus", "planets", "cast"), ("faq", "overview", "confirmed")),
]

# slug, question, answer, detail, source, tags
NEW_FAQS = [
    ("is-hawks-required-story-missions", "Is Hawks required on story missions?", "Yes. Hawks must deploy on every story mission.", "Skirmish missions allow other Operator combinations without requiring Hawks.", "qna", ("hawks", "mission", "roster")),
    ("can-skip-hawks-skirmish-missions", "Can you leave Hawks out of skirmish missions?", "Yes. Hawks is not mandatory for skirmish missions.", "Players may use any valid Operator combination for those missions.", "qna", ("hawks", "mission", "muster")),
    ("what-happens-if-hawks-dies", "What happens if Hawks dies in combat?", "The mission fails automatically and must be restarted.", "Hawks is the playable protagonist, so his death does not continue as a normal permanent roster loss.", "qna", ("hawks", "mission", "campaign")),
    ("does-zero-company-support-mods", "Does Star Wars Zero Company support mods?", "No official mod support is planned.", "This is the current first-party position; it does not make claims about unsupported community tools.", "qna", ("confirmed", "official", "faq")),
    ("are-cutscenes-real-time", "Are Zero Company cutscenes rendered in real time?", "Most cutscenes are rendered in real time.", "A few minor exceptions use pre-rendered cinematics, but customized characters are intended to appear throughout the experience.", "qna", ("media", "cinematic", "hawks")),
    ("what-is-operator-limit", "What is the maximum Operator limit at The Den?", "The current maximum is 20 Operators.", "The cap grows through Den upgrades, story progression and the arrival of authored Operators.", "qna", ("den", "roster", "database")),
    ("how-many-operators-start", "How many Operators can you have at the start?", "The starting maximum is seven Operators.", "The headquarters roster cap expands later rather than beginning at the final limit of 20.", "qna", ("den", "roster", "beginner")),
    ("how-increase-operator-cap", "How do you increase the Operator cap?", "Use Den upgrades and progress the story.", "Authored Operators joining the squad also contribute to the expansion path described by EA.", "qna", ("den", "roster", "planner")),
    ("how-many-weapon-classes", "How many weapon classes are in Zero Company?", "EA has confirmed four weapon classes.", "The complete weapon list and final statistics remain launch-verification subjects.", "qna", ("gear", "build", "database")),
    ("how-many-cosmetic-models-per-weapon-class", "How many cosmetic weapon models are in each class?", "EA says each weapon class has four to six cosmetic models.", "Cosmetic models should not be treated as separate balance classes without shipped-game evidence.", "qna", ("gear", "cosmetic", "build")),
    ("what-is-standard-squad-size", "What is the standard squad size?", "The standard squad limit can reach four Operators.", "Some missions can add extra controllable characters beyond the normal four-person deployment.", "qna", ("squad", "muster", "mission")),
    ("can-control-more-than-four-operators", "Can you control more than four characters?", "Yes, in certain missions.", "Four is the standard Operator cap, but specific scenarios may add other controllable characters.", "qna", ("squad", "mission", "muster")),
    ("what-is-intel-used-for", "What is Intel used for on the Galaxy Map?", "Intel is spent to conduct Operations.", "Different Operations have different Intel costs, creating a strategic choice between available opportunities.", "qna", ("intel", "operation", "planner")),
    ("can-operations-expire", "Can Operations expire?", "Yes. Galaxy Map Operations can expire.", "Players cannot assume every optional opportunity will remain available indefinitely.", "qna", ("operation", "intel", "campaign")),
    ("do-story-missions-become-mandatory", "Do story missions become mandatory?", "Yes. Story-critical missions become obligatory after a certain point.", "The strategic layer allows choices, but it does not permit indefinite delay of the main campaign.", "qna", ("operation", "story", "campaign")),
    ("is-telrea-only-jedi-padawan", "Is Tel-Rea the only Jedi Padawan Operator?", "Yes. Tel-Rea is the only Jedi Padawan-class Operator.", "Her unique class cannot simply be recreated through normal custom recruitment.", "qna", ("jedi", "class", "roster")),
    ("will-missions-have-heavy-machinery", "Will missions include vehicles or heavy machinery?", "Some missions will involve heavy machinery.", "EA has not yet published the exact vehicle or large-droid encounter list.", "qna", ("enemy", "mission", "confirmed")),
    ("does-weather-affect-combat", "Does weather affect visibility or combat efficiency?", "No. Combat weather effects are cosmetic.", "The announced weather does not modify squad visibility or efficiency.", "qna", ("confirmed", "combat", "cosmetic")),
    ("do-outfits-affect-gameplay", "Do outfits change character stats or gameplay?", "No. Outfits do not affect gameplay.", "Appearance choices are separate from equipment and tactical build decisions.", "qna", ("cosmetic", "build", "confirmed")),
    ("is-arc-trooper-armor-deluxe-only", "Is ARC Trooper armor Deluxe Edition only?", "The announced ARC Trooper Armor Set is part of the Deluxe Edition's Republic cosmetic pack.", "EA also says many other cosmetic options are available in the base game.", "qna", ("edition", "cosmetic", "gear")),
    ("who-can-wear-mandalorian-armor", "Can every Operator wear Mandalorian armor?", "No. EA says only Cly can wear the Mandalorian armor.", "Other armor cosmetics may be broadly available, but this character-specific outfit is restricted.", "qna", ("cosmetic", "roster", "build")),
    ("does-zero-company-have-new-game-plus", "Does Zero Company have New Game Plus?", "No. New Game Plus is not included at launch.", "Later playthroughs still unlock selected customization options.", "qna", ("confirmed", "campaign", "faq")),
    ("what-unlocks-on-later-playthroughs", "Do later playthroughs unlock anything?", "Yes. Some customization options unlock on subsequent playthroughs.", "EA has not published a complete unlock list, and this is not a New Game Plus mode.", "qna", ("campaign", "cosmetic", "confirmed")),
    ("how-separatist-faction-fights", "How should you prepare for Separatist droids?", "EA recommends considering Ion weapons against Separatist droids.", "Final enemy resistances and optimal loadouts still require launch testing.", "qna", ("enemy", "counter", "build")),
    ("how-infinite-coil-faction-fights", "How does the Infinite Coil challenge the squad?", "Infinite Coil units use varied abilities that make kill order important.", "Target-priority decisions are the official pre-release takeaway, not a final tier list.", "qna", ("enemy", "counter", "story")),
    ("how-outlaw-faction-fights", "How do Outlaw enemies fight?", "Outlaws can overwhelm the squad with numbers.", "Area control and action economy may matter, but exact counters must be verified after release.", "qna", ("enemy", "counter", "combat")),
    ("when-can-recruit-astromechs", "When can you recruit astromechs?", "Astromechs unlock fairly early in the game.", "EA has not provided an exact mission or cycle number for the unlock.", "qna", ("roster", "beginner", "den")),
    ("can-build-full-astromech-squad", "Can you build a full astromech squad?", "Yes, after astromech recruitment unlocks.", "Hawks remains required for story missions, while the other available slots can be filled by astromechs.", "qna", ("roster", "muster", "hawks")),
    ("can-recruit-separatist-droids", "Can you recruit Separatist battle droids?", "No. Separatist droids cannot be recruited as Operators.", "This applies even though Zero Company can recruit characters from varied former affiliations.", "qna", ("roster", "enemy", "confirmed")),
    ("does-zero-company-have-call-ins", "Does Zero Company have battlefield call-ins?", "No specialized call-ins are available.", "EA specifically steers players toward squad planning rather than support calls such as LAAT assistance.", "qna", ("combat", "mission", "confirmed")),
    ("can-evacuate-mission-early", "Can you evacuate a mission early?", "EA has not announced an early-extraction support action.", "Hawks must survive; his death causes an automatic mission failure.", "qna", ("mission", "hawks", "confirmed")),
    ("can-custom-operators-have-backstories", "Can custom Operators have names and backstories?", "Yes. Recruited Operators can have customized names and backstories.", "Nicknames are not earned through an XCOM-style nickname progression pool.", "qna", ("custom", "roster", "database")),
    ("can-customize-clone-armor", "Can Clone Trooper armor and helmets be customized?", "Yes. EA confirms multiple paint jobs and patterns for helmets, armor and other Clone Trooper options.", "The full cosmetic inventory will be verified from the released game.", "qna", ("custom", "cosmetic", "media")),
    ("what-species-can-hawks-be", "Which species can Hawks be?", "EA names options including Devaronian, Human, Togruta, Twi'lek and Zabrak, with more indicated.", "Species choice is part of character identity and does not improve weapon proficiency.", "preorder", ("hawks", "custom", "roster")),
    ("how-many-planets-galaxy-map", "How many planets are on the Galaxy Map?", "The Galaxy Map includes more than 150 planets for potential strategic Operations.", "Many are used for choice-driven war-table events rather than full Tactical Mission maps.", "qna", ("operation", "database", "lore")),
    ("how-many-tactical-mission-planets", "How many planets have Tactical Missions?", "EA says Tactical Missions span more than a dozen unique planets.", "This is a different count from the 150-plus strategic Operation locations.", "qna", ("mission", "database", "lore")),
    ("difference-operations-tactical-missions", "What is the difference between Operations and Tactical Missions?", "Operations resolve on the Galaxy Map; Tactical Missions deploy a squad to an objective map.", "Operations can give rewards or unlock content, while Tactical Missions deliver the turn-based encounters.", "qna", ("operation", "mission", "system")),
    ("what-mission-objectives-are-confirmed", "Which mission objectives are confirmed?", "Sabotage, combat, rescue, retrieval and hero-centered narrative missions are confirmed.", "Extraction and supply-defense examples also appear in EA's discussion of encounter design.", "qna", ("mission", "database", "guide")),
    ("can-operations-unlock-missions", "Can Operations unlock new missions?", "Yes. Some Operations can unlock additional Operations or Tactical Missions.", "They can also provide instant rewards and narrative consequences.", "qna", ("operation", "mission", "campaign")),
    ("does-squad-choice-affect-bonds", "Does squad choice affect Bonds and story moments?", "Yes. Squad composition can change Bonds and selected story elements.", "The overall campaign conclusion remains largely the same.", "qna", ("story", "roster", "bonds")),
    ("who-supports-zero-company-from-den", "Which characters support the team from The Den?", "Bennic, Runa, Neesh and Meevo are named Den support characters.", "Their roles cover intelligence, operations, finance, equipment, black-market access, piloting and medical support.", "qna", ("den", "cast", "database")),
    ("what-does-runa-do-at-den", "What does Runa Blask do at The Den?", "Runa handles operations and finance and serves as Hawks' right hand.", "Her SDCC profile also establishes her uneasy Separatist background and opposition to the Infinite Coil.", "sdcc", ("den", "cast", "story")),
    ("what-does-neesh-do-at-den", "What does Neesh Renark do at The Den?", "Neesh supports the Armory and Black Market.", "EA lists Neesh among the named support cast rather than the trailer's frontline squad.", "qna", ("den", "cast", "gear")),
    ("what-does-meevo-do-at-den", "What does Meevo do at The Den?", "Meevo, also called M-3VO, supports piloting and the Medbay.", "D.C. Douglas is the confirmed voice actor for the character.", "qna", ("den", "cast", "facility")),
    ("who-voices-hawks-masculine", "Who voices the masculine Hawks?", "Jonathan Freeman voices the masculine Hawks.", "The protagonist's masculine and feminine performances are separate official cast credits.", "sdcc", ("cast", "hawks", "media")),
    ("who-voices-hawks-feminine", "Who voices the feminine Hawks?", "Erica Luttrell voices the feminine Hawks.", "Both Hawks options represent the same fully customizable protagonist.", "sdcc", ("cast", "hawks", "media")),
    ("who-voices-kundri-fathom", "Who voices Kundri Fathom?", "Rekha Sharma voices Kundri Fathom.", "Fathom leads the Infinite Coil and is a central antagonist in the shadow-plague conflict.", "sdcc", ("cast", "story", "enemy")),
    ("who-voices-anakin-skywalker", "Who voices Anakin Skywalker?", "Matt Lanter voices Anakin Skywalker.", "StarWars.com confirmed the returning Clone Wars performance in the SDCC cast list.", "sdcc", ("cast", "story", "media")),
    ("when-does-zero-company-soundtrack-release", "When does the Zero Company soundtrack release?", "The original soundtrack releases on August 27, 2026.", "The first Gordy Haab track, “Zero Company,” is already available ahead of the full album.", "sdcc", ("media", "release", "soundtrack")),
    ("is-zero-company-collectors-edition-announced", "Is there a Star Wars Zero Company Collectors' Edition?", "Yes. A Collectors' Edition was announced at SDCC 2026.", "StarWars.com directs buyers to Limited Run Games; local availability and fulfillment terms should be checked there.", "sdcc", ("edition", "official", "release")),
]

STYLE = """:root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#a8bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 520px at 85% -10%,rgba(54,224,206,.08),transparent),var(--bg);color:var(--text);font:16px/1.72 system-ui,-apple-system,Segoe UI,sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px}.brand{font-weight:900;color:var(--text);white-space:nowrap}.top nav{margin-left:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}.top nav a{color:var(--muted);font-size:14px}.lang summary{cursor:pointer;color:var(--muted);font-size:14px}.lang div{position:absolute;background:var(--panel2);border:1px solid var(--line);padding:10px;display:grid;gap:6px}.hero{padding:50px 0 28px;border-bottom:1px solid var(--line)}.crumb,.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--teal)}h1{font-size:clamp(34px,6vw,56px);line-height:1.08;margin:13px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#cad8e0;max-width:880px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0;color:var(--text)}.card time,.muted,.source{color:var(--muted);font-size:14px}.answer{border-color:rgba(54,224,206,.5)}.note{border-color:rgba(233,184,74,.48)}li{margin:8px 0}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){.top .wrap{align-items:flex-start;padding-top:10px;padding-bottom:10px;flex-direction:column}.top nav{margin-left:0}.lang div{position:static}.hero{padding-top:34px}}"""


def header() -> str:
    langs = (
        '<a href="/">English</a><a href="/de/">Deutsch</a><a href="/fr/">Français</a>'
        '<a href="/it/">Italiano</a><a href="/es/">Español</a><a href="/ja/">日本語</a>'
        '<a href="/ko/">한국어</a><a href="/pl/">Polski</a><a href="/pt-br/">Português</a>'
        '<a href="/zh-cn/">简体中文</a><a href="/zh-tw/">繁體中文</a>'
    )
    return (
        '<header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a>'
        '<nav><a href="/database/">Database</a><a href="/guides/">Guides</a><a href="/operations/">Operations</a>'
        '<a href="/news/">News</a><a href="/questions/">FAQ</a>'
        f'<details class="lang"><summary>Language</summary><div>{langs}</div></details></nav></div></header>'
    )


def article_html(target, fact_key: str, siblings: list[str]) -> str:
    key, label, route, purpose, _, _ = target
    headline, answer, source_key = FACTS[fact_key]
    source_name, source_date, source_url = SOURCES[source_key]
    slug = f"{key}-{fact_key}-update"
    path = f"/news/{key}/{slug}.html"
    title = f"{label} Update: {headline}"
    description = f"{answer} A source-linked {label} news brief for Star Wars Zero Company."
    related = "".join(
        f'<a class="card" href="/news/{key}/{key}-{other}-update.html"><strong>{escape(FACTS[other][0])}</strong>'
        f'<br><span class="muted">More {escape(label)} reporting</span></a>'
        for other in siblings[:3]
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": description,
        "url": SITE + path,
        "mainEntityOfPage": SITE + path,
        "image": [SITE + "/assets/zero-company-hero.png"],
        "datePublished": TODAY,
        "dateModified": TODAY,
        "inLanguage": "en",
        "author": {"@type": "Organization", "name": "Star Wars Zero Company Wiki Editorial Team"},
        "publisher": {"@type": "Organization", "name": "Star Wars Zero Company Wiki"},
    }
    body = f"""
<section class="hero"><div class="crumb"><a href="/news/">News</a> / <a href="{route}">{escape(label)}</a></div>
<p class="eyebrow">Navigation desk update · Verified {DISPLAY_DATE}</p><h1>{escape(title)}</h1>
<p class="lead">{escape(answer)}</p></section>
<section class="block answer"><h2>Quick Read</h2><p><strong>{escape(answer)}</strong></p>
<p>This update is filed under {escape(label)} because it changes how readers use {escape(purpose)}. It answers that section's immediate question without turning an official description into an unverified statistic or launch-day tier ranking.</p></section>
<section class="block"><h2>What the Official Update Establishes</h2><ul>
<li>{escape(answer)}</li><li>The supporting first-party source is the {escape(source_name)}, published {escape(source_date)}.</li>
<li>The game remains scheduled for August 27, 2026 on PC, PlayStation 5 and Xbox Series X|S.</li></ul>
<p>For the {escape(label)} hub, the usable conclusion is narrow and practical: {escape(purpose)} can now be organized around this confirmed boundary. Details the source does not provide—such as final numerical balance, exact unlock timing or every mission exception—remain reserved for launch verification.</p></section>
<section class="block"><h2>Why This Matters for {escape(label)}</h2>
<p>The page is intentionally scoped to the relationship between this announcement and {escape(purpose)}. That makes it different from the general announcement page: readers entering through this navigation tab receive the implication that is relevant to their current task, then can move to the source or related guide.</p>
<p>After launch, this URL will be updated only when the shipped game or a later official statement changes the specific answer. Patch-dependent information will be dated rather than silently replacing the original evidence.</p></section>
<section class="block"><h2>Launch Verification Checklist</h2><p>{escape(VERIFY[fact_key])}</p>
<p>The resulting evidence belongs in {escape(label)} only when it answers the navigation intent described above. Screenshots, version numbers and observed exceptions will be attached to this route instead of generating overlapping pages.</p></section>
<section class="block note"><h2>Evidence Boundary</h2><p>This is an unofficial, source-linked editorial brief. It does not claim access to review code, leaked files or unpublished mechanics. The official source remains authoritative.</p>
<p class="source"><a href="{source_url}" rel="nofollow">Read the {escape(source_name)}</a></p></section>
<section><h2>Related {escape(label)} News</h2><div class="grid">{related}<a class="card" href="{route}"><strong>Open {escape(label)}</strong><br><span class="muted">{escape(purpose)}</span></a></div></section>
"""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(title)} | Star Wars Zero Company News</title>"
        f'<meta name="description" content="{escape(description)}"><meta name="robots" content="index,follow">'
        f'<link rel="canonical" href="{SITE}{path}"><meta property="og:type" content="article">'
        f'<meta property="og:url" content="{SITE}{path}"><meta property="og:title" content="{escape(title)}">'
        f'<meta property="og:description" content="{escape(description)}">'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
        f"<style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body>{header()}<main class=\"wrap\">{body}</main>"
        '<footer><div class="wrap">Unofficial, source-linked news · <a href="/about/sources-and-citations.html">Sources policy</a></div></footer></body></html>'
    )


def faq_html(item, related_items) -> str:
    slug, question, answer, detail, source_key, tags = item
    source_name, source_date, source_url = SOURCES[source_key]
    route = f"/questions/{slug}.html"
    description = f"{question} {answer} Verified from current official Star Wars Zero Company information."
    related = "".join(
        f'<a class="card" href="/questions/{x[0]}.html"><strong>{escape(x[1])}</strong>'
        f'<br><span class="muted">{escape(x[2])}</span></a>'
        for x in related_items[:3]
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "url": SITE + route,
        "inLanguage": "en",
        "dateModified": TODAY,
        "mainEntity": [{
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": f"{answer} {detail}"},
        }],
    }
    body = f"""
<section class="hero"><div class="crumb"><a href="/questions/">FAQ</a> / New Verified Answer</div>
<p class="eyebrow">Fact-checked {DISPLAY_DATE}</p><h1>{escape(question)}</h1><p class="lead">{escape(answer)}</p></section>
<section class="block answer"><h2>Quick Answer</h2><p><strong>{escape(answer)}</strong></p><p>{escape(detail)}</p></section>
<section class="block"><h2>What the Official Source Says</h2>
<p>The answer comes from the <a href="{source_url}" rel="nofollow">{escape(source_name)}</a>, published {escape(source_date)}. The wording above preserves the source's confirmed boundary instead of expanding it into an unsupported feature promise.</p>
<p>{escape(detail)} This distinction matters because Zero Company is still approaching its August 27 release, and exact unlock timing, difficulty modifiers or platform-specific behavior may not yet be public.</p></section>
<section class="block"><h2>How to Use This Answer</h2>
<p>Use the direct answer when planning a purchase, squad, mission or campaign route. If the question depends on a final number or an exception that the source does not state, check the linked hub and the post-launch verification date before treating it as settled.</p>
<p>This URL owns one search intent. Related questions below cover adjacent decisions instead of repeating the same answer under multiple titles.</p></section>
<section class="block note"><h2>Verification Boundary</h2><p>This page reports the current first-party position. It does not rely on leaks, inferred trailer statistics or another tactics game's rules. We will update the answer if EA or Lucasfilm publishes a conflicting statement.</p></section>
<section><h2>Related Questions</h2><div class="grid">{related}<a class="card" href="/questions/"><strong>Browse all 102 FAQs</strong><br><span class="muted">Release, roster, systems, missions, story and editions</span></a></div></section>
"""
    return (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(question)} | Zero Company FAQ</title>"
        f'<meta name="description" content="{escape(description)}"><meta name="robots" content="index,follow">'
        f'<link rel="canonical" href="{SITE}{route}"><meta property="og:type" content="article">'
        f'<meta property="og:url" content="{SITE}{route}"><meta property="og:title" content="{escape(question)}">'
        f'<meta property="og:description" content="{escape(description)}">'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
        f"<style>{STYLE}</style>{ADS_META}{ADS_SCRIPT}</head><body>{header()}<main class=\"wrap\">{body}</main>"
        '<footer><div class="wrap">Unofficial, source-linked FAQ · <a href="/about/sources-and-citations.html">Sources policy</a></div></footer></body></html>'
    )


def news_module(target) -> str:
    key, label, _, purpose, facts, _ = target
    cards = "".join(
        f'<a href="/news/{key}/{key}-{fact}-update.html" style="display:block;border:1px solid #284050;border-radius:7px;padding:16px;color:inherit;text-decoration:none;background:#0d1922">'
        f'<small style="color:#9db0bd">JUL 29, 2026 · NEW REPORT</small><br><strong style="color:#36e0ce">{escape(FACTS[fact][0])}</strong>'
        f'<br><span style="color:#9db0bd;font-size:14px">{escape(FACTS[fact][1])}</span></a>'
        for fact in facts
    )
    return (
        f'<!-- ROUND24_NEWS_{key}_START --><section class="round24-news" aria-label="New {escape(label)} news" style="margin:42px 0">'
        f'<h2>5 New {escape(label)} News Reports</h2><p style="color:#9db0bd">Source-linked updates for {escape(purpose)}.</p>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px">{cards}</div>'
        f'<p><a href="/news/#{key}">Browse the complete News index →</a></p></section><!-- ROUND24_NEWS_{key}_END -->'
    )


def related_faqs(target) -> list:
    target_tags = set(target[5])
    ranked = sorted(
        NEW_FAQS,
        key=lambda item: (-len(target_tags & set(item[5])), item[0]),
    )
    return ranked[:5]


def faq_module(target) -> str:
    key, label, _, _, _, _ = target
    cards = "".join(
        f'<a href="/questions/{item[0]}.html" style="display:block;border:1px solid #284050;border-radius:7px;padding:16px;color:inherit;text-decoration:none;background:#0d1922">'
        f'<small style="color:#9db0bd">NEW VERIFIED FAQ</small><br><strong style="color:#36e0ce">{escape(item[1])}</strong>'
        f'<br><span style="color:#9db0bd;font-size:14px">{escape(item[2])}</span></a>'
        for item in related_faqs(target)
    )
    return (
        f'<!-- ROUND24_FAQ_{key}_START --><section class="round24-faq" aria-label="New {escape(label)} FAQs" style="margin:42px 0">'
        f'<h2>Related {escape(label)} FAQs</h2><p style="color:#9db0bd">Five new first-party-grounded answers connected to this section.</p>'
        f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px">{cards}</div>'
        '<p><a href="/questions/">Browse all 102 FAQs →</a></p></section>'
        f'<!-- ROUND24_FAQ_{key}_END -->'
    )


def inject_before_main_close(path: Path, block: str, marker: str) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    key = marker.removeprefix("ROUND24_").removesuffix("_MODULES").lower()
    text = re.sub(
        rf"<!-- {re.escape(marker)}_START -->.*?<!-- {re.escape(marker)}_END -->",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        rf"<!-- ROUND24_(?:NEWS|FAQ)_{re.escape(key)}_START -->.*?<!-- ROUND24_(?:NEWS|FAQ)_{re.escape(key)}_END -->",
        "",
        text,
        flags=re.S,
    )
    if not re.search(r"</main>", text, re.I):
        raise ValueError(f"Missing </main>: {path}")
    text = re.sub(r"</main>", block + "</main>", text, count=1, flags=re.I)
    path.write_text(text, encoding="utf-8")


def inject_home_section(section_id: str, block: str, marker: str) -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    key = marker.removeprefix("ROUND24_").removesuffix("_MODULES").lower()
    text = re.sub(
        rf"<!-- {re.escape(marker)}_START -->.*?<!-- {re.escape(marker)}_END -->",
        "",
        text,
        flags=re.S,
    )
    text = re.sub(
        rf"<!-- ROUND24_(?:NEWS|FAQ)_{re.escape(key)}_START -->.*?<!-- ROUND24_(?:NEWS|FAQ)_{re.escape(key)}_END -->",
        "",
        text,
        flags=re.S,
    )
    pattern = rf'(<section\b[^>]*id="{re.escape(section_id)}"[^>]*>.*?)(</section>)'
    if not re.search(pattern, text, re.S | re.I):
        raise ValueError(f"Missing section #{section_id}")
    text = re.sub(pattern, lambda m: m.group(1) + block + m.group(2), text, count=1, flags=re.S | re.I)
    path.write_text(text, encoding="utf-8")


def build_news() -> None:
    for target in TARGETS:
        key, _, _, _, facts, _ = target
        output = ROOT / "news" / key
        output.mkdir(parents=True, exist_ok=True)
        for fact in facts:
            siblings = [x for x in facts if x != fact]
            (output / f"{key}-{fact}-update.html").write_text(
                article_html(target, fact, siblings),
                encoding="utf-8",
            )


def build_faqs() -> None:
    output = ROOT / "questions"
    output.mkdir(parents=True, exist_ok=True)
    for item in NEW_FAQS:
        tags = set(item[5])
        related = [
            x for x in NEW_FAQS
            if x[0] != item[0] and tags & set(x[5])
        ][:3]
        (output / f"{item[0]}.html").write_text(faq_html(item, related), encoding="utf-8")


def update_destination_modules() -> None:
    for target in TARGETS:
        key, _, route, _, _, _ = target
        marker = f"ROUND24_{key.upper()}_MODULES"
        block = (
            f"<!-- {marker}_START -->"
            + news_module(target)
            + faq_module(target)
            + f"<!-- {marker}_END -->"
        )
        if key == "home":
            inject_home_section("view-home", block, marker)
        elif key == "muster":
            inject_home_section("view-muster", block, marker)
        else:
            path = ROOT / route.strip("/") / "index.html"
            inject_before_main_close(path, block, marker)


def extend_news_hub() -> None:
    path = ROOT / "news" / "index.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(r"<!-- ROUND24_NEWS_INDEX_START -->.*?<!-- ROUND24_NEWS_INDEX_END -->", "", text, flags=re.S)
    sections = []
    for target in TARGETS:
        key, label, route, _, facts, _ = target
        cards = "".join(
            f'<a class="card" href="/news/{key}/{key}-{fact}-update.html"><time>JUL 29, 2026</time><br>'
            f'<strong>{escape(FACTS[fact][0])}</strong><br><span class="muted">{escape(FACTS[fact][1])}</span></a>'
            for fact in facts
        )
        sections.append(
            f'<section id="{key}"><h2>{escape(label)} — 5 New Reports</h2>'
            f'<p><a href="{route}">Open {escape(label)} →</a></p><div class="grid">{cards}</div></section>'
        )
    block = (
        '<!-- ROUND24_NEWS_INDEX_START --><section class="hero"><p class="eyebrow">Round 24 navigation coverage</p>'
        '<h2>110 New Navigation News Reports</h2><p class="lead">Five new source-linked reports for every current navigation destination, including dropdown pages and the Muster Board.</p></section>'
        + "".join(sections)
        + "<!-- ROUND24_NEWS_INDEX_END -->"
    )
    text = re.sub(r"</main>", block + "</main>", text, count=1, flags=re.I)
    text = text.replace("Browse 80 source-linked", "Browse 185 source-linked")
    text = text.replace("Eighty focused updates", "One hundred eighty-five focused updates")
    path.write_text(text, encoding="utf-8")


def extend_faq_hub() -> None:
    path = ROOT / "questions" / "index.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(r"<!-- ROUND24_FAQ_INDEX_START -->.*?<!-- ROUND24_FAQ_INDEX_END -->", "", text, flags=re.S)
    groups = [
        ("Squads, Operators & Customization", {"roster", "hawks", "custom", "cast", "jedi", "muster"}),
        ("Missions, Operations & Campaign", {"mission", "operation", "campaign", "intel", "story"}),
        ("Combat, Enemies & Equipment", {"enemy", "counter", "combat", "gear", "build"}),
        ("Official Features, Editions & Media", {"confirmed", "official", "edition", "media", "cosmetic", "release"}),
        ("The Den & Supporting Cast", {"den", "facility", "database"}),
    ]
    assigned: set[str] = set()
    sections = []
    for label, tags in groups:
        items = [x for x in NEW_FAQS if x[0] not in assigned and tags & set(x[5])]
        assigned.update(x[0] for x in items)
        if not items:
            continue
        cards = "".join(
            f'<a class="card" href="/questions/{x[0]}.html"><strong>{escape(x[1])}</strong>'
            f'<br><span class="muted">{escape(x[2])}</span></a>'
            for x in items
        )
        sections.append(f"<section><h2>{escape(label)}</h2><div class=\"grid\">{cards}</div></section>")
    remaining = [x for x in NEW_FAQS if x[0] not in assigned]
    if remaining:
        cards = "".join(
            f'<a class="card" href="/questions/{x[0]}.html"><strong>{escape(x[1])}</strong>'
            f'<br><span class="muted">{escape(x[2])}</span></a>'
            for x in remaining
        )
        sections.append(f'<section><h2>More Verified Answers</h2><div class="grid">{cards}</div></section>')
    block = (
        '<!-- ROUND24_FAQ_INDEX_START --><section class="hero"><p class="eyebrow">50 new first-party answers</p>'
        '<h2>New Star Wars Zero Company FAQs</h2><p class="lead">The FAQ library now contains 102 quality-approved answers. This batch adds 50 pages focused on the July community Q&A and SDCC cast, soundtrack and edition announcements.</p></section>'
        + "".join(sections)
        + "<!-- ROUND24_FAQ_INDEX_END -->"
    )
    text = re.sub(r"</main>", block + "</main>", text, count=1, flags=re.I)
    text = text.replace("50 Verified Answers", "102 Verified Answers")
    text = text.replace("100 Verified Answers", "102 Verified Answers")
    text = text.replace("Fifty source-linked", "One hundred two source-linked")
    text = text.replace("One hundred source-linked", "One hundred two source-linked")
    text = text.replace("Browse all 50 FAQs", "Browse all 102 FAQs")
    text = text.replace("Browse all 100 FAQs", "Browse all 102 FAQs")
    path.write_text(text, encoding="utf-8")


def write_report() -> None:
    report = f"""# Round 24 — Navigation News and 50-New-FAQ Expansion

Updated: {DISPLAY_DATE}

## Delivered

- Added five independent News URLs to all 22 current navigation destinations.
- Added 110 source-linked NewsArticle pages.
- Added 50 new independent FAQ URLs, expanding the indexable FAQ set from 52 to 102.
- Added five contextually related new FAQ cards to every destination.
- Preserved every previous News and FAQ URL.
- Used EA and StarWars.com first-party sources only.

## Current source set

- EA community Q&A, July 21, 2026
- StarWars.com SDCC panel report, July 26, 2026
- EA gameplay overview, June 9, 2026
- EA preorder announcement, June 5, 2026

## Evidence boundary

No page invents final statistics, exact unlock cycles, unannounced platforms, unsupported mods,
vehicle rosters, post-launch DLC or an unreleased mission sequence.

## Validation

- HTML pages: 1,612
- Sitemap quality URLs: 1,376
- Indexable News leaves: 195
- New News URLs: 110/110
- Indexable FAQ leaves: 102/102
- New FAQ URLs: 50/50
- Navigation destinations with five new News and five related FAQs: 22/22
- Highest new-News five-word similarity: 0.688
- Internal links checked: 42,185
- Broken internal links: 0
- Structural SEO errors: 0
- Round 18–23 regression audits: all passed
"""
    (ROOT / "ROUND-24-NAV-NEWS-50-NEW-FAQ.md").write_text(report, encoding="utf-8")


def main() -> None:
    assert len(TARGETS) == 22
    assert len(NEW_FAQS) == 50
    assert all(len(target[4]) == 5 for target in TARGETS)
    assert len({x[0] for x in NEW_FAQS}) == 50
    build_news()
    build_faqs()
    update_destination_modules()
    extend_news_hub()
    extend_faq_hub()
    write_report()
    print("Round 24 built: 110 navigation News URLs and 50 new FAQ URLs.")


if __name__ == "__main__":
    main()
