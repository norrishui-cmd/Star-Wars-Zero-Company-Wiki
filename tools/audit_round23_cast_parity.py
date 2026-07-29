#!/usr/bin/env python3
"""Release gate for Round 23 multilingual cast parity."""

from html import unescape
from collections import Counter
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("es", "fr", "it", "ko", "pl", "pt-br", "zh-cn", "zh-tw")
SLUGS = (
    "hawks-masculine-jonathan-freeman",
    "hawks-feminine-erica-luttrell",
    "runa-blask-vic-michaelis",
    "kabb-uppercut-jb-blanc",
    "jae-mordant-judy-alice-lee",
    "bennic-halloren-leo-howard",
    "visser-dylan-kenin",
    "tel-rea-nicole-rainteau",
    "neesh-renark-jim-pirri",
    "m3vo-meevo-dc-douglas",
    "typhon-hunter-smith",
)


def style(text):
    match = re.search(r"<style>(.*?)</style>", text, re.S)
    return match.group(1) if match else ""


def visible_words(text):
    text = re.sub(r"<script.*?</script>|<style.*?</style>", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.findall(r"[\wÀ-ž가-힣一-龥]+", unescape(text).lower())


def route_to_path(href):
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith(("http:", "https:", "mailto:", "javascript:")):
        return None
    target = ROOT / clean.lstrip("/")
    if href.endswith("/") or (target.exists() and target.is_dir()):
        target = target / "index.html"
    return target


def main():
    errors = []
    warnings = []
    sitemap = set((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines())
    english_style = style((ROOT / "cast" / "trick-dee-bradley-baker.html").read_text(encoding="utf-8"))
    titles = {}
    locale_docs = {locale: [] for locale in LOCALES}
    checked = 0

    for locale in LOCALES:
        hub_text = (ROOT / locale / "cast" / "index.html").read_text(encoding="utf-8")
        for slug in SLUGS:
            path = ROOT / locale / "cast" / f"{slug}.html"
            if not path.exists():
                errors.append(f"missing {path.relative_to(ROOT)}")
                continue
            checked += 1
            text = path.read_text(encoding="utf-8")
            route = f"/{locale}/cast/{slug}.html"
            canonical = SITE + route

            if canonical not in sitemap:
                errors.append(f"not in sitemap {route}")
            if f'<link rel="canonical" href="{canonical}">' not in text:
                errors.append(f"canonical {route}")
            if len(re.findall(r'<link rel="alternate" hreflang=', text)) != 12:
                errors.append(f"hreflang count {route}")
            if 'meta name="robots" content="index,follow"' not in text:
                errors.append(f"robots {route}")
            if 'class="lang-menu"' not in text:
                errors.append(f"language dropdown {route}")
            if 'ca-pub-9505220977121599' not in text:
                errors.append(f"adsense {route}")
            if style(text) != english_style:
                errors.append(f"English visual parity {route}")
            if f'href="{route}"' not in hub_text:
                errors.append(f"missing hub link {route}")

            title_match = re.search(r"<title>(.*?)</title>", text, re.S)
            title = unescape(title_match.group(1)).strip() if title_match else ""
            if not title:
                errors.append(f"title {route}")
            elif title in titles:
                errors.append(f"duplicate title {route} and {titles[title]}")
            else:
                titles[title] = route

            words = visible_words(text)
            if not locale.startswith("zh") and len(words) < 180:
                warnings.append(f"short visible copy {route}: {len(words)}")
            main_match = re.search(r"<main.*?>(.*?)</main>", text, re.S)
            main = main_match.group(1) if main_match else ""
            segments = [
                re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", raw))).strip().lower()
                for raw in re.findall(r"<(?:p|li|td|th)[^>]*>(.*?)</(?:p|li|td|th)>", main, re.S)
            ]
            locale_docs[locale].append((route, segments))

            schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S)
            if not schemas:
                errors.append(f"missing JSON-LD {route}")
            for raw in schemas:
                try:
                    json.loads(unescape(raw))
                except json.JSONDecodeError:
                    errors.append(f"invalid JSON-LD {route}")
            for href in re.findall(r'href="([^"]+)"', text):
                target = route_to_path(href)
                if target is not None and not target.exists():
                    errors.append(f"broken link {route} -> {href}")

    max_similarity = (0.0, "", "")
    for locale, docs in locale_docs.items():
        frequency = Counter(segment for _, segments in docs for segment in set(segments))
        residual_docs = []
        for route, segments in docs:
            residual = " ".join(segment for segment in segments if frequency[segment] <= 2)
            residual_docs.append((route, set(re.findall(r"[\wÀ-ž가-힣一-龥]+", residual))))
        for idx, (route_a, words_a) in enumerate(residual_docs):
            for route_b, words_b in residual_docs[idx + 1:]:
                union = words_a | words_b
                score = len(words_a & words_b) / len(union) if union else 0
                if score > max_similarity[0]:
                    max_similarity = (score, route_a, route_b)
                if score >= 0.70:
                    errors.append(f"near duplicate {route_a} {route_b}: {score:.3f}")

    for slug in SLUGS:
        for prefix in ("", "de/", "ja/"):
            path = ROOT / prefix / "cast" / f"{slug}.html"
            text = path.read_text(encoding="utf-8")
            if len(re.findall(r'<link rel="alternate" hreflang=', text)) != 12:
                errors.append(f"counterpart hreflang {path.relative_to(ROOT)}")

    print(f"Round 23 pages checked: {checked}")
    print(f"Sitemap quality URLs: {len(sitemap)}")
    print(f"Highest same-locale Jaccard similarity: {max_similarity[0]:.3f}")
    print(f"Warnings: {len(warnings)}")
    print(f"Errors: {len(errors)}")
    for item in warnings[:30]:
        print("WARN", item)
    for item in errors[:80]:
        print("ERROR", item)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
