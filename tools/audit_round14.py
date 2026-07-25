#!/usr/bin/env python3
"""Round 14 quality gate for localized mechanics and English visual parity."""

from html import unescape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("de", "fr", "it", "es", "ja", "ko", "pl", "zh-cn", "zh-tw", "pt-br")
SLUGS = (
    "operator-limit-20", "standard-squad-limit-four", "four-weapon-classes",
    "intel-operation-costs", "story-missions-become-obligatory",
    "no-new-game-plus-at-launch", "weather-cosmetic-only",
    "outfits-no-gameplay-stats", "tel-rea-only-jedi-padawan",
    "cannot-recruit-separatist-droids",
)
STYLE_MARKERS = (
    "--panel2:#101f2a", "linear-gradient(180deg,var(--panel),var(--panel2))",
    ".answer{border-color:", ".note,.fact{border-color:", ".lang-menu summary::after",
    "@media(max-width:760px)",
)


def visible(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", html, flags=re.I | re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def grams(text: str) -> set[str]:
    cjk = "".join(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", text))
    if len(cjk) > 100:
        return {cjk[i:i + 12] for i in range(max(0, len(cjk) - 11))}
    words = re.findall(r"[a-zà-ž0-9]+", text.lower())
    return {" ".join(words[i:i + 5]) for i in range(max(0, len(words) - 4))}


def main() -> int:
    sitemap = set((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines())
    errors = []
    contents = {}
    style_parity = 0
    for locale in LOCALES:
        for slug in SLUGS:
            path = ROOT / locale / "mechanics" / f"{slug}.html"
            if not path.exists():
                errors.append(f"missing {path.relative_to(ROOT)}")
                continue
            html = path.read_text(encoding="utf-8-sig", errors="ignore")
            text = visible(html)
            url = f"{SITE}/{locale}/mechanics/{slug}.html"
            if url not in sitemap:
                errors.append(f"not in sitemap: {url}")
            canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
            if not canonical or canonical.group(1) != url:
                errors.append(f"bad canonical: {path.relative_to(ROOT)}")
            tags = re.findall(r'<link rel="alternate" hreflang="([^"]+)"', html)
            if len(tags) != 12 or len(set(tags)) != 12 or "x-default" not in tags:
                errors.append(f"bad hreflang: {path.relative_to(ROOT)}")
            if all(marker in html for marker in STYLE_MARKERS):
                style_parity += 1
            else:
                errors.append(f"English visual system missing: {path.relative_to(ROOT)}")
            blocks = re.findall(r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>', html, re.S | re.I)
            if not blocks:
                errors.append(f"missing JSON-LD: {path.relative_to(ROOT)}")
            for block in blocks:
                try:
                    json.loads(block)
                except json.JSONDecodeError:
                    errors.append(f"invalid JSON-LD: {path.relative_to(ROOT)}")
            if locale in ("ja", "ko", "zh-cn", "zh-tw"):
                count = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", text))
                if count < 260:
                    errors.append(f"thin CJK {count}: {path.relative_to(ROOT)}")
            elif len(text.split()) < 180:
                errors.append(f"thin page {len(text.split())} words: {path.relative_to(ROOT)}")
            if "EA community Q&amp;A" not in html or "July 21, 2026" not in html:
                errors.append(f"official evidence missing: {path.relative_to(ROOT)}")
            contents[(locale, slug)] = text

    max_similarity = (0.0, "")
    for locale in LOCALES:
        pages = [(slug, grams(contents[(locale, slug)])) for slug in SLUGS if (locale, slug) in contents]
        for i, (a_slug, a) in enumerate(pages):
            for b_slug, b in pages[i + 1:]:
                score = len(a & b) / max(1, len(a | b))
                if score > max_similarity[0]:
                    max_similarity = (score, f"{locale}:{a_slug} vs {b_slug}")
                if score >= 0.72:
                    errors.append(f"near duplicate {score:.3f}: {locale}:{a_slug} vs {b_slug}")

    # English source pages must reciprocate the same complete hreflang set.
    for slug in SLUGS:
        html = (ROOT / "mechanics" / f"{slug}.html").read_text(encoding="utf-8-sig", errors="ignore")
        tags = re.findall(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)', html, re.I)
        if len(tags) != 12 or len(set(tags)) != 12:
            errors.append(f"English reciprocal hreflang missing: mechanics/{slug}.html")

    print(f"Round 14 localized mechanics pages: {len(contents)}/100")
    print(f"English visual-system parity: {style_parity}/100")
    print(f"Sitemap quality URLs: {len(sitemap)}")
    print(f"Highest same-language five-gram similarity: {max_similarity[0]:.3f} ({max_similarity[1]})")
    print(f"Errors: {len(errors)}")
    for error in errors[:100]:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
