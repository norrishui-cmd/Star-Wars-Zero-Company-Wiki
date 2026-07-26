#!/usr/bin/env python3
"""Quality gate for the Round 17 final 1,000-URL sprint."""

from html import unescape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("de","fr","it","es","ja","ko","pl","zh-cn","zh-tw","pt-br")
SLUGS = (
    "squad-acts-before-enemies","three-action-points-each-turn",
    "movement-distance-ap-cost","weapon-type-ap-cost",
    "chance-to-hit-shot-breakdown","shared-advantage-pool",
    "destructible-cover","push-enemy-into-overwatch",
    "three-injuries-permadeath","permadeath-toggle",
    "the-den-third-person-base","holotable-cycle-planning",
    "operation-choices-affect-bonds","pre-combat-exploration-rewards",
    "galaxy-map-150-planets",
)
BUYERS = (
    "index","ea-app-release-time-price","standard-edition-contents",
    "deluxe-edition-contents","crystalline-astromech-pack",
    "grand-army-republic-pack","shadow-collective-pack",
    "painted-weapon-themes","preorder-redemption-deadline",
)
STYLE_MARKERS = (
    "radial-gradient(900px 520px","--panel2:#101f2a",
    "linear-gradient(180deg,var(--panel),var(--panel2))",
    ".answer{border-color:",".note{border-color:",".two{display:grid",
    ".lang-menu summary::after","@media(max-width:760px)",
)


def visible(html):
    html = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", html, flags=re.I|re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def grams(text):
    cjk = "".join(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", text))
    if len(cjk) > 100:
        return {cjk[i:i+12] for i in range(max(0,len(cjk)-11))}
    words = re.findall(r"[a-zà-ž0-9]+", text.lower())
    return {" ".join(words[i:i+5]) for i in range(max(0,len(words)-4))}


def validate(path, url, sitemap, expect_hreflang=False):
    errors = []
    if not path.exists():
        return [f"missing {path.relative_to(ROOT)}"], ""
    html = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = visible(html)
    if url not in sitemap:
        errors.append(f"not in sitemap: {url}")
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if not canonical or canonical.group(1) != url:
        errors.append(f"bad canonical: {path.relative_to(ROOT)}")
    if expect_hreflang:
        tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)"', html)
        if len(tags) != 12 or len(set(tags)) != 12 or "x-default" not in tags:
            errors.append(f"bad hreflang: {path.relative_to(ROOT)}")
    if not all(marker in html for marker in STYLE_MARKERS):
        errors.append(f"English visual parity missing: {path.relative_to(ROOT)}")
    if "ca-pub-9505220977121599" not in html:
        errors.append(f"AdSense missing: {path.relative_to(ROOT)}")
    blocks = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S|re.I)
    if not blocks:
        errors.append(f"JSON-LD missing: {path.relative_to(ROOT)}")
    for block in blocks:
        try:
            json.loads(block)
        except json.JSONDecodeError:
            errors.append(f"invalid JSON-LD: {path.relative_to(ROOT)}")
    return errors, text


def main():
    sitemap = set((ROOT/"sitemap.txt").read_text().splitlines())
    errors, contents = [], {}
    localized = english = buyers = parity = 0
    for slug in SLUGS:
        path = ROOT/"systems"/f"{slug}.html"
        found, text = validate(path, f"{SITE}/systems/{slug}.html", sitemap, True)
        errors.extend(found)
        english += int(not found)
        parity += int(all(x in path.read_text(errors="ignore") for x in STYLE_MARKERS))
        for locale in LOCALES:
            path = ROOT/locale/"mechanics"/f"{slug}.html"
            found, text = validate(path, f"{SITE}/{locale}/mechanics/{slug}.html", sitemap, True)
            errors.extend(found)
            html = path.read_text(encoding="utf-8-sig",errors="ignore") if path.exists() else ""
            if html.count("/questions/") < 4:
                errors.append(f"FAQ access missing: {path.relative_to(ROOT)}")
            if locale in ("ja","ko","zh-cn","zh-tw"):
                count = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", text))
                if count < 300:
                    errors.append(f"thin CJK {count}: {path.relative_to(ROOT)}")
            elif len(text.split()) < 190:
                errors.append(f"thin page {len(text.split())}: {path.relative_to(ROOT)}")
            contents[(locale,slug)] = text
            localized += int(not found)
            parity += int(all(x in html for x in STYLE_MARKERS))

    for slug in BUYERS:
        path = ROOT/"preorder"/("index.html" if slug == "index" else f"{slug}.html")
        url = f"{SITE}/preorder/" if slug == "index" else f"{SITE}/preorder/{slug}.html"
        found, text = validate(path, url, sitemap)
        errors.extend(found)
        if len(text.split()) < 145:
            errors.append(f"thin buyer page {len(text.split())}: {path.relative_to(ROOT)}")
        buyers += int(not found)

    maximum = (0.0,"")
    for locale in LOCALES:
        pages = [(slug,grams(contents[(locale,slug)])) for slug in SLUGS]
        for i,(a_slug,a) in enumerate(pages):
            for b_slug,b in pages[i+1:]:
                score = len(a&b)/max(1,len(a|b))
                if score > maximum[0]:
                    maximum = (score,f"{locale}:{a_slug} vs {b_slug}")
                if score >= .72:
                    errors.append(f"near duplicate {score:.3f}: {locale}:{a_slug} vs {b_slug}")

    expected = 1016
    if len(sitemap) != expected:
        errors.append(f"sitemap count {len(sitemap)} != {expected}")
    print(f"Round 17 localized combat pages: {localized}/150")
    print(f"English reciprocal pages: {english}/15")
    print(f"Buyer hub and guides: {buyers}/9")
    print(f"English visual parity: {parity}/165")
    print(f"Sitemap quality URLs: {len(sitemap)}")
    print(f"Highest same-language similarity: {maximum[0]:.3f} ({maximum[1]})")
    print(f"Errors: {len(errors)}")
    for error in errors[:160]:
        print("ERROR",error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
