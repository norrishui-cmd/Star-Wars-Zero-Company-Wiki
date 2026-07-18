# Star Wars Zero Company Wiki — SEO Plan to 2,000 URLs

Audit date: 2026-07-17  
Launch date: 2026-08-27  
Domain: https://starwarszerocompany.cc

## Starting point

- 339 HTML URLs in the supplied build.
- 284 pages had fewer than 200 visible words.
- Large pre-launch matrices (counter, pairing, squad and scenario pages) reused conclusions that cannot yet be validated in the shipped game.
- Titles, canonicals and H1 coverage were generally complete, but robots.txt advertised five overlapping sitemap endpoints and the home page declared a SearchAction for a route that does not exist.

The target is 2,000 useful URL records, not 2,000 pages forced into Google's index. A URL becomes indexable only after it has a concrete answer, a source or first-hand verification, unique intent and useful internal links.

## 2,000-URL architecture

| Cluster | Target URLs | Publish trigger | Page requirements |
|---|---:|---|---|
| Missions, objectives, choices and troubleshooting | 420 | Launch + verified playthrough | Requirements, exact steps, decision outcome, reward, bug fixes |
| Items, weapons, armor, mods and upgrades | 360 | In-game data captured | Stats, acquisition, upgrade path, best users, alternatives |
| Operatives, custom archetypes, classes and skills | 260 | Skill trees verified | Unlock, abilities, progression, build choices, team role |
| Enemies, bosses, weaknesses and counters | 240 | Enemy roster/stats verified | Exact behavior, weaknesses, class-specific plan, evidence |
| Squad builds, pairings and bonds | 230 | Mechanics and bond effects verified | Named loadout, mission context, turn plan, swaps, limits |
| Locations, maps, The Den facilities and collectibles | 180 | Locations captured | Route, landmarks, prerequisites, map/screenshot, nearby goals |
| Systems, difficulty, accessibility and settings | 100 | Final build/settings verified | Direct answer, tested behavior, platform differences |
| Platform, release, edition, performance and errors | 80 | Official/store/benchmark evidence | Current status, exact platform, fix steps, source/date |
| Story, factions, characters and lore | 70 | Spoiler-safe campaign verification | Context, appearances, relationships, spoiler label |
| News, patches and version changes | 60 | Official update published | Change summary, affected guides, source, date/version |
| **Total** | **2,000** |  |  |

## Release schedule

### Phase 1 — Foundation (July 17–23)

- Keep the strongest official, system, character and buyer-intent hubs indexable.
- Hold speculative matrix leaves as `noindex,follow` drafts and remove them from XML sitemaps.
- Expand verified release, platform, edition, preorder and age-rating pages.
- Run `python3 tools/seo_audit.py` and `python3 tools/build_sitemaps.py` before every deployment.

Current first-round sitemap: 150 retained URLs. Target after the next evidence pass: 180–250 quality-approved indexed URLs and 500–700 planned/draft records.

### Phase 2 — Evidence inventory (July 24–August 19)

- Build structured datasets for confirmed operatives, species, classes, abilities, Den facilities, mission types and preorder/store questions.
- Publish 15–25 verified pages per day from official gameplay articles and trailers.
- Prepare, but do not index, mission/item/enemy templates awaiting shipped-game evidence.

Target: 550–750 indexable URLs; 1,300–1,500 total URL records.

### Phase 3 — Launch window (August 20–September 3)

- Prioritize release time, preload, system requirements, crash/performance, difficulty, settings, early missions and “stuck” questions.
- On launch day, capture exact names, stats, steps, screenshots and rewards; release pages in batches of at most 80–100 after QA.
- Refresh sitemap after each meaningful approved batch, not for unverified drafts.

Target: 1,200–1,500 indexable URLs and 2,000 complete URL records by the end of launch week.

### Phase 4 — Validation and completion (September 4–17)

- Finish the 2,000-page indexable target only where the game contains enough distinct entities and search intents.
- Merge cannibalizing pages, prune weak variants and use GSC query data to prioritize missing answers.

## Quality gate

Every indexable URL must pass all of the following:

1. One unique player intent and a direct answer near the top.
2. No invented names, stats, missions, rewards or “projected meta” presented as fact.
3. Unique title, meta description, H1 and self-canonical.
4. At least two useful contextual internal links plus its hub/breadcrumb path.
5. Appropriate source link or a recorded first-hand verification date.
6. For walkthroughs: requirements, numbered steps, location, reward, failure states and related guides.
7. For database pages: concrete attributes, acquisition/unlock data, practical use and meaningful comparison.
8. Successful audit with no broken internal links or indexable uncertainty markers.

Word count is a warning signal, not the definition of quality. A short page can pass only when it completely answers a narrow question; a long page still fails if it is generic.

## First-round changes completed

- Corrected the home title and removed invalid SearchAction schema for the nonexistent `/search` route.
- Updated the countdown to EA's stated August 27, 2026, 3 PM UTC PC time.
- Consolidated robots.txt to one sitemap index.
- Deepened release date, platform, Deluxe Edition, preorder bonus and rating pages with current official facts and dated sources.
- Added an explicit draft/index policy and marked speculative matrix leaves `noindex,follow`.
- Rebuilt XML sitemaps from canonical, approved pages only.
- Added repeatable sitemap and SEO audit scripts.
- Reduced the XML sitemap from 339 URLs to 150 crawl priorities; 189 speculative leaves remain available as `noindex,follow` drafts for launch verification instead of being deleted.

## Next three actions

1. Expand the official June 9 gameplay overview into verified entity pages for Hawks, Trick, Tel-Rea, the Den, mission types and combat systems without creating overlapping intents.
2. Create the launch-day data capture sheet/schema for missions, items, enemies, abilities, rewards, locations and bugs so verified pages can be generated quickly.
3. Export GSC 7-day and 28-day query/page data after deployment; use it to choose the next 25-page cluster and identify existing cannibalization.

## Round 2 — July 18, 2026

- Replaced seven speculative Operative pages with source-grounded profiles for Hawks, Trick, Tel-Rea, Cly, Luco, Jae and Kabb.
- Removed invented tier rankings, Focus Tree nodes, percentages and unverified signature abilities from those pages.
- Added nine focused Den facility pages plus a facility hub: Command Center, HoloTable, Recruitment, Personnel, Armory, Upgrade, Medbay, Customization and Memorial.
- Added four story-entity pages plus a lore hub: Kundri Fathom, the Infinite Coil, Zero Company and the Ring of Kafrene.
- Corrected the obsolete EA gameplay-overview source path across the official-systems cluster.
- Added prominent homepage links to the new source-grounded clusters.
- Held the older `/systems/` leaf set as `noindex,follow` because it overlaps the stronger `/official-systems/` cluster; the `/systems/` hub remains available while consolidation decisions are made.

Round 3 priority: turn the eight confirmed standard Specializations into complete, evidence-based class pages and replace the current speculative class leaves before they are allowed back into the sitemap.

## Round 3 — July 18, 2026

- Rebuilt the Classes hub around the eight standard Specializations officially named by EA: Assault, Gunslinger, Heavy, Medic, Scoundrel, Scout, Sharpshooter and Soldier.
- Replaced eight speculative class leaves with 400+ word source-grounded guides covering official role, tactical decision principles, shared Ability structure, progression and launch-verification boundaries.
- Removed all S/A/B tiers, invented Ability names, fictional percentages and unsupported weapon locks from the class cluster.
- Restored only the eight verified standard Specialization pages to the sitemap through an explicit route allowlist.
- Reframed Astromech, Jedi, Mandalorian and “secret class” URLs as `noindex,follow` boundary pages because EA has not named them among the eight standard Specializations.
- Replaced the homepage's embedded pre-launch tier list with an official Specialization browser and direct links to the full verified guides.

Round 4 priority: consolidate the overlapping buyer-intent and beginner guide pages, then rebuild the highest-value FAQ cluster around exact official answers such as offline/single-player status, three AP per turn, maximum Advantage, Injury rules, mission Cycles and Custom Operator creation.

## Round 4 — July 18, 2026

- Added a quality-approved German layer under `/de/` and Japanese layer under `/ja/`, with 14 pages per language.
- Localized the highest-confidence pre-release intents: home, release date and local time, platforms, supported languages, gameplay overview, Specializations hub and all eight confirmed standard Specializations.
- Added a new English supported-languages page and corrected the site-wide answer to 11 interface/subtitle languages, with full audio in English and German.
- Added reciprocal `hreflang` annotations for English, German, Japanese and `x-default`, while keeping every localized page self-canonical.
- Added language switching, localized navigation, dated official sources, distinct metadata and language-specific structured data.
- Updated the audit to use a CJK character threshold for Japanese pages instead of treating whitespace-based English word count as a valid quality test.

Round 5 priority: use GSC country/query data to decide whether German or Japanese deserves the next localized cluster, then expand only the winning language into FAQ pages for single-player/offline, three AP, Advantage, Injuries, mission Cycles and Custom Operators.

## AdSense ownership configuration — July 18, 2026

- Added publisher account `ca-pub-9505220977121599` to every HTML page through both the AdSense account meta tag and the asynchronous AdSense loader.
- Added the required root-level `/ads.txt` declaration for publisher `pub-9505220977121599`.
- Added explicit plain-text response headers for `/ads.txt` on both Vercel and Netlify-style deployments.
- Kept the configuration repeatable through `tools/configure_adsense.py`, which removes duplicates before applying the current publisher ID.
