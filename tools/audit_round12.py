#!/usr/bin/env python3
"""Round 12 integrity audit for all-language core pages and global navigation."""

from html import unescape
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("en", "de", "fr", "it", "es", "ja", "ko", "pl", "zh-cn", "zh-tw", "pt-br")
NEW_LOCALES = LOCALES[2:5] + LOCALES[6:]
CORE = ("index.html", "official/release-date.html", "official/platforms.html",
        "official/languages.html", "confirmed/overview.html")


def local_target(href: str):
    parts = urlsplit(unescape(href))
    if parts.scheme or parts.netloc or not parts.path.startswith("/"):
        return None
    rel = parts.path.lstrip("/")
    if not rel:
        return ROOT / "index.html"
    candidate = ROOT / rel
    if parts.path.endswith("/"):
        candidate = candidate / "index.html"
    return candidate


def main() -> int:
    pages = sorted(ROOT.rglob("*.html"))
    errors = []
    broken = set()
    json_count = 0
    menu_ok = 0
    sitemap = (ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines()

    for path in pages:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        menu = re.search(r'<div class="lang-options">(.*?)</div>', text, re.S)
        if menu and len(re.findall(r"<a\b", menu.group(1), re.I)) == 11:
            menu_ok += 1
        else:
            errors.append(f"language menu is not complete: {path.relative_to(ROOT)}")
        for href in re.findall(r'href=["\']([^"\']+)', text, re.I):
            if "${" in href:
                continue
            target = local_target(href)
            if target is not None and not target.exists():
                broken.add((path.relative_to(ROOT).as_posix(), href))
        for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
            try:
                json.loads(raw)
                json_count += 1
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON-LD: {path.relative_to(ROOT)}: {exc}")

    for locale in NEW_LOCALES:
        for rel in CORE:
            path = ROOT / locale / rel
            if not path.exists():
                errors.append(f"missing core page: {locale}/{rel}")
                continue
            text = path.read_text(encoding="utf-8")
            route = "" if rel == "index.html" else rel
            url = f"{SITE}/{locale}/" if not route else f"{SITE}/{locale}/{route}"
            if url not in sitemap:
                errors.append(f"new core page missing from sitemap: {url}")
            hreflangs = re.findall(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)', text, re.I)
            if len(hreflangs) != 12 or "x-default" not in hreflangs:
                errors.append(f"incomplete hreflang set: {locale}/{rel}")

    if broken:
        errors.extend(f"broken link from {source}: {href}" for source, href in sorted(broken))

    print(f"Round 12 audit: {len(pages)} HTML pages")
    print(f"Language dropdown: {menu_ok}/{len(pages)}")
    print(f"New localized core: {len(NEW_LOCALES) * len(CORE)}/40")
    print(f"Sitemap URLs: {len(sitemap)}")
    print(f"Valid JSON-LD blocks: {json_count}")
    print(f"Broken internal links: {len(broken)}")
    print(f"Errors: {len(errors)}")
    for error in errors[:100]:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
