#!/usr/bin/env python3
"""Refresh the 80 tab-news URLs and 50 FAQs with EA's July 21 community Q&A."""

from pathlib import Path
import re

import build_tab_news as news
import build_verified_faqs as faq


TODAY = "2026-07-25"
COMMUNITY_URL = (
    "https://www.ea.com/games/starwars/zero-company/news/"
    "answering-biggest-questions"
)

news.TODAY = TODAY
news.DISPLAY_DATE = "July 25, 2026"
news.CARD_DATE = "JUL 25, 2026"
news.SOURCES["community"] = (
    "EA community Q&A",
    "July 21, 2026",
    COMMUNITY_URL,
)

# Replace one older brief per tab with the newest official information while
# retaining exactly five featured News URLs per navigation tab.
NEWS_REFRESH = {
    "operatives": (
        "bonds-cross-training-confirmed",
        "Bonds Unlock Support Abilities and Cross-Training Benefits",
        "EA says bonded Operators can gain support abilities and share skills and stats through cross-training.",
        "Squad relationships have a confirmed tactical effect, not just narrative flavor.",
        "community",
    ),
    "classes": (
        "species-no-weapon-proficiency-bonus",
        "Species Choice Does Not Change Weapon Proficiency",
        "EA confirms that no species or faction has superior weapon proficiency.",
        "Players can choose a species for identity rather than feeling forced into a combat meta.",
        "community",
    ),
    "builds": (
        "secondary-advanced-specializations",
        "Secondary and Advanced Specializations Expand Builds",
        "EA says equipment, secondary Specializations and advanced Specializations can further shape playstyle.",
        "Launch build guides will need to account for progression beyond the starting standard role.",
        "community",
    ),
    "operations": (
        "pre-combat-exploration-intel-advantage",
        "Limited Pre-Combat Exploration Can Grant Intel and Advantage",
        "Some main-story missions include small exploration segments before tactical combat.",
        "Exploration choices can affect the following battle by granting Intel and Advantage Points.",
        "community",
    ),
    "hostiles": (
        "espionage-can-change-next-battle",
        "Espionage Segments Can Change the Following Encounter",
        "EA says mission-specific exploration can provide benefits before combat begins.",
        "Enemy and objective preparation may start before the tactical map loads.",
        "community",
    ),
    "guides": (
        "permadeath-can-be-disabled",
        "Permadeath Is Enabled by Default but Can Be Turned Off",
        "EA confirms that players may disable permadeath in the game settings.",
        "Beginner guidance can separate the default high-stakes experience from an optional accessibility choice.",
        "community",
    ),
    "content-map": (
        "july-community-qa-coverage",
        "EA's July Community Q&A Opens New Verified Guide Clusters",
        "The July 21 Q&A confirms story structure, exploration, settings, monetization and performance boundaries.",
        "The wiki can replace speculative placeholders with first-party answers across several hubs.",
        "community",
    ),
    "official-systems": (
        "optional-permadeath-setting",
        "The Permadeath System Has an Optional Toggle",
        "Permadeath is on by default, but EA says players can switch it off.",
        "The injury system remains meaningful without forcing every campaign to use permanent roster loss.",
        "community",
    ),
    "facilities": (
        "bonds-share-skills-and-stats",
        "Bonded Operators Can Share Skills and Stats",
        "Cross-training benefits can pass new skills and statistics between bonded units.",
        "Personnel planning at The Den connects directly to relationships built on missions.",
        "community",
    ),
    "lore": (
        "linear-story-no-romance",
        "Zero Company Has a Linear Story and No Romance System",
        "EA confirms there are no romance systems or branching story paths.",
        "Squad selection can alter some moments, but the campaign follows one main narrative.",
        "community",
    ),
    "confirmed": (
        "switch-steam-deck-status",
        "Switch and Steam Deck Versions Remain Unconfirmed",
        "EA is optimizing the announced PC, PS5 and Xbox Series X|S versions and has no Switch or Steam Deck announcement.",
        "Players should not treat compatibility speculation as a confirmed platform promise.",
        "community",
    ),
    "official": (
        "no-microtransactions-planned",
        "EA Says No Additional Microtransactions Are Planned",
        "The July community Q&A states that there are no current plans for monetization or microtransactions.",
        "Edition cosmetics should not be confused with an announced live-service store.",
        "community",
    ),
    "start-here": (
        "story-romance-choices-explained",
        "New Player Story Guide: No Romance or Branching Ending",
        "The campaign has no romance system, and its conclusion is largely the same for everyone.",
        "New players can focus decisions on squad composition, Bonds, battles and difficulty rather than a branching romance route.",
        "community",
    ),
    "systems": (
        "story-choice-boundary-confirmed",
        "Squad Choices Change Moments, Not the Overall Ending",
        "EA says roster choices affect Bonds and some scenes while the main conclusion stays largely consistent.",
        "The site can separate tactical choice systems from claims about a branching narrative.",
        "community",
    ),
    "planner": (
        "permadeath-campaign-setting",
        "Campaign Planning Can Start With Permadeath On or Off",
        "Permadeath is the default setting but can be disabled.",
        "Players can choose the desired consequence level before building a long-term roster plan.",
        "community",
    ),
    "media": (
        "gordy-haab-dee-bradley-baker",
        "Gordy Haab and Dee Bradley Baker Join Zero Company",
        "EA names Gordy Haab as composer and Dee Bradley Baker as the voice of Trick and the Clone Troopers.",
        "The official Q&A adds confirmed music and performance credits ahead of the full cast reveal.",
        "community",
    ),
}

old_news_paths = []
for category, replacement in NEWS_REFRESH.items():
    items = news.CATEGORIES[category][3]
    old_news_paths.append(news.ROOT / "news" / category / f"{items[-1][0]}.html")
    items[-1] = replacement

faq.TODAY = TODAY
faq.DISPLAY_DATE = "July 25, 2026"
faq.SOURCES["community"] = ("EA community Q&A", COMMUNITY_URL)

FAQ_REPLACEMENTS = {
    "should-you-preorder": (
        "will-zero-company-have-dlc",
        "Will Star Wars Zero Company have DLC or post-launch content?",
        "EA has not announced DLC or post-launch content.",
        "The development team says it is currently focused on delivering the launch game.",
        "community",
        ["official", "confirmed", "start-here", "content-map"],
    ),
    "does-zero-company-have-multiplayer": (
        "does-zero-company-have-microtransactions",
        "Does Star Wars Zero Company have microtransactions?",
        "EA says it has no current plans for additional monetization or microtransactions.",
        "The announced preorder and Deluxe bonuses are cosmetic edition content, not a confirmed recurring in-game store.",
        "community",
        ["official", "confirmed", "guides", "start-here"],
    ),
    "does-zero-company-have-coop": (
        "does-zero-company-have-romance",
        "Does Star Wars Zero Company have romance?",
        "No. EA confirms there is no romance system.",
        "Bonds affect support abilities and some character moments, but they are not romance routes.",
        "community",
        ["lore", "operatives", "guides", "start-here"],
    ),
    "should-you-save-advantage": (
        "does-zero-company-have-branching-paths",
        "Does Star Wars Zero Company have branching story paths?",
        "No. EA describes the overall campaign as a linear story.",
        "Squad composition can alter some scenes and Bonds, but it does not create fully branching campaign routes.",
        "community",
        ["lore", "operations", "confirmed", "systems"],
    ),
    "does-zero-company-have-limited-saves": (
        "does-zero-company-have-multiple-endings",
        "Does Star Wars Zero Company have multiple endings?",
        "The ending is expected to be largely the same for every player.",
        "EA says choices can change Bonds and some story elements without substantially changing the conclusion.",
        "community",
        ["lore", "operations", "confirmed", "start-here"],
    ),
    "can-you-play-without-customs": (
        "can-you-explore-before-combat",
        "Can you explore planets before combat?",
        "Yes, in limited main-story segments on some planets.",
        "These espionage-focused sections may grant Intel and Advantage Points for the following tactical battle.",
        "community",
        ["operations", "guides", "official-systems", "lore"],
    ),
    "who-is-trick": (
        "can-you-disable-permadeath",
        "Can you disable permadeath in Star Wars Zero Company?",
        "Yes. Permadeath is enabled by default but can be turned off.",
        "EA encourages players to adjust the setting to match their preferred campaign experience.",
        "community",
        ["official-systems", "systems", "guides", "start-here", "planner"],
    ),
    "who-is-telrea": (
        "who-voices-trick-and-clone-troopers",
        "Who voices Trick and the Clone Troopers?",
        "Dee Bradley Baker voices Trick and the Clone Troopers.",
        "EA confirmed the casting in its July 21 community Q&A.",
        "community",
        ["operatives", "media", "lore"],
    ),
    "who-is-cly": (
        "do-species-affect-weapon-proficiency",
        "Do species or factions affect weapon proficiency?",
        "No. Species and faction choices do not grant better weapon proficiency.",
        "EA designed the system so players are not pushed toward one species for optimization.",
        "community",
        ["operatives", "classes", "builds"],
    ),
    "who-is-luco": (
        "is-zero-company-on-steam-deck",
        "Will Star Wars Zero Company support Steam Deck?",
        "Steam Deck support has not been announced.",
        "EA says it is currently developing and optimizing for Steam and the announced PC, PS5 and Xbox Series X|S platforms.",
        "community",
        ["official", "confirmed", "guides", "planner"],
    ),
}

faq.FAQS = [FAQ_REPLACEMENTS.get(item[0], item) for item in faq.FAQS]

# Update the existing Switch FAQ to use the direct July 21 first-party answer.
for i, item in enumerate(faq.FAQS):
    if item[0] == "is-zero-company-on-nintendo-switch":
        faq.FAQS[i] = (
            item[0],
            item[1],
            "Nintendo Switch and Switch 2 versions have not been announced.",
            "EA says it is focused on Steam/PC, PS5 and Xbox Series X|S and will share news if that changes.",
            "community",
            item[5],
        )


def noindex_obsolete_news():
    active = {
        news.ROOT / "news" / category / f"{item[0]}.html"
        for category, data in news.CATEGORIES.items()
        for item in data[3]
    }
    for path in old_news_paths:
        if path in active or not path.exists():
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        if re.search(r'<meta\s+name="robots"', text, re.I):
            text = re.sub(
                r'<meta\s+name="robots"\s+content="[^"]*"\s*/?>',
                '<meta name="robots" content="noindex,follow">',
                text,
                count=1,
                flags=re.I,
            )
        else:
            text = text.replace("</head>", '<meta name="robots" content="noindex,follow"></head>', 1)
        path.write_text(text, encoding="utf-8")


def main():
    assert len(faq.FAQS) == 50
    assert len(news.CATEGORIES) == 16
    assert all(len(data[3]) == 5 for data in news.CATEGORIES.values())
    news.main()
    noindex_obsolete_news()
    faq.main()
    print("Round 10 refresh complete: 80 featured News URLs and 50 verified FAQ URLs.")


if __name__ == "__main__":
    main()
