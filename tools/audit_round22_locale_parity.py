#!/usr/bin/env python3
"""Round 22 release gate for localized cast and specialization pages."""

from html import unescape
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("es", "fr", "it", "ko", "pl", "pt-br", "zh-cn", "zh-tw")
CAST = ("anakin-skywalker-matt-lanter", "cly-kullervo-alex-mckenna",
        "kundri-fathom-rekha-sharma", "trick-dee-bradley-baker")
CLASSES = ("assault", "gunslinger", "heavy", "medic", "scoundrel",
           "scout", "sharpshooter", "soldier")


def style(path):
    text = path.read_text(encoding="utf-8")
    return re.search(r"<style>(.*?)</style>", text, re.S).group(1)


def route_to_path(href):
    clean = href.split("#", 1)[0].split("?", 1)[0]
    if not clean or clean.startswith(("http:", "https:", "mailto:", "javascript:")):
        return None
    clean = clean.lstrip("/")
    target = ROOT / clean
    if href.endswith("/") or (target.exists() and target.is_dir()):
        target = target / "index.html"
    return target


def main():
    errors = []
    sitemap = set((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines())
    cast_style = style(ROOT / "cast" / "trick-dee-bradley-baker.html")
    class_style = style(ROOT / "classes" / "assault.html")
    pages = []
    for locale in LOCALES:
        pages.extend((ROOT / locale / family / "index.html", family, None)
                     for family in ("cast", "classes"))
        pages.extend((ROOT / locale / "cast" / f"{slug}.html", "cast", slug)
                     for slug in CAST)
        pages.extend((ROOT / locale / "classes" / f"{slug}.html", "classes", slug)
                     for slug in CLASSES)

    for path, family, slug in pages:
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        route = "/" + (rel[:-10] if rel.endswith("/index.html") else rel)
        canonical = SITE + route
        if canonical not in sitemap:
            errors.append(f"not in sitemap {route}")
        if f'<link rel="canonical" href="{canonical}">' not in text:
            errors.append(f"bad canonical {route}")
        if len(re.findall(r'<link rel="alternate" hreflang=', text)) != 12:
            errors.append(f"hreflang count {route}")
        if 'meta name="robots" content="index,follow"' not in text:
            errors.append(f"robots {route}")
        if 'class="lang-menu"' not in text:
            errors.append(f"language menu {route}")
        if 'ca-pub-9505220977121599' not in text:
            errors.append(f"adsense {route}")
        expected_style = cast_style if family == "cast" else class_style
        if style(path) != expected_style:
            errors.append(f"English visual parity {route}")
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.S):
            try:
                json.loads(unescape(raw))
            except json.JSONDecodeError:
                errors.append(f"JSON-LD {route}")
        for href in re.findall(r'href="([^"]+)"', text):
            target = route_to_path(href)
            if target is not None and not target.exists():
                errors.append(f"broken link {route} -> {href}")

    # Existing English, German and Japanese counterparts must now point to all
    # eleven exact language routes plus x-default.
    for family, slugs in (("cast", CAST), ("classes", CLASSES)):
        for slug in slugs:
            for locale in ("", "de", "ja"):
                path = ROOT / locale / family / f"{slug}.html"
                text = path.read_text(encoding="utf-8")
                if len(re.findall(r'<link rel="alternate" hreflang=', text)) != 12:
                    errors.append(f"counterpart hreflang {path.relative_to(ROOT)}")

    print(f"Round 22 audited localized pages: {len(pages)}")
    print(f"Sitemap quality URLs: {len(sitemap)}")
    print(f"Errors: {len(errors)}")
    for item in errors[:80]:
        print("ERROR", item)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
