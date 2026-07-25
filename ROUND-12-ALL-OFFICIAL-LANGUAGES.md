# Round 12 — All Official Languages

Updated: July 25, 2026

## Official language inventory

EA and Steam list 11 languages for interface and subtitles. Steam marks full
audio only for English and German.

| Language | Locale route | Interface | Subtitles | Full audio | Site status |
|---|---|---:|---:|---:|---|
| English | `/` | Yes | Yes | Yes | Existing deep layer |
| German | `/de/` | Yes | Yes | Yes | Existing deep layer |
| French | `/fr/` | Yes | Yes | No | New five-page core |
| Italian | `/it/` | Yes | Yes | No | New five-page core |
| Spanish — Spain | `/es/` | Yes | Yes | No | New five-page core |
| Japanese | `/ja/` | Yes | Yes | No | Existing deep layer |
| Korean | `/ko/` | Yes | Yes | No | New five-page core |
| Polish | `/pl/` | Yes | Yes | No | New five-page core |
| Simplified Chinese | `/zh-cn/` | Yes | Yes | No | New five-page core |
| Traditional Chinese | `/zh-tw/` | Yes | Yes | No | New five-page core |
| Portuguese — Brazil | `/pt-br/` | Yes | Yes | No | New five-page core |

Primary evidence:

- EA purchase page: <https://www.ea.com/games/starwars/zero-company/buy>
- Steam language table:
  <https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/>

## New localized core

Each previously uncovered language now has five independent, indexable pages:

1. Locale homepage and confirmed overview
2. Release date with locally converted launch time
3. Confirmed platforms and unsupported/unconfirmed boundaries
4. All supported languages and audio distinction
5. Confirmed gameplay systems

The batch adds 40 localized URLs. Every page has a distinct title, description,
H1, self-canonical, localized WebPage JSON-LD, official sources, internal core
navigation and an exact reciprocal hreflang set.

## Global navigation

The language dropdown now lists all eleven languages on all 772 HTML pages.
When the current route has an exact localized counterpart, the selector links
to it. For deeper pages that have not yet been translated, it links to the
chosen locale homepage rather than claiming a false equivalent.

## Validation

- Total HTML pages: 772
- Quality-approved sitemap URLs: 534
- New localized core pages: 40/40
- Global language dropdown: 772/772
- Valid JSON-LD blocks: 772
- Broken internal links: 0
- Structural SEO errors: 0
- New-page content-quality warnings: 0
- AdSense ownership coverage: complete

The remaining 48 audit warnings predate this batch and concern older short or
launch-boundary pages. None belongs to the 40 new localized pages.

## Next expansion rule

Do not translate all English leaves automatically. Expand each locale only when
the page has a concrete English answer and meaningful search intent. The next
safe candidates are verified FAQ, confirmed mechanics, editions, Demo status
and the official cast database.
