#!/usr/bin/env python3
"""Round 9 release gate: links, schema, i18n, sitemap, ads and dropdown."""

from pathlib import Path
from urllib.parse import urlparse
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
ADS_META = '<meta name="google-adsense-account" content="ca-pub-9505220977121599">'
ADS_CLIENT = "ca-pub-9505220977121599"


def local_path(href):
    parsed = urlparse(href)
    if parsed.scheme and parsed.netloc != "starwarszerocompany.cc":
        return None
    path = parsed.path
    if not path.startswith("/"):
        return None
    if path == "/":
        return ROOT / "index.html"
    candidate = ROOT / path.lstrip("/")
    if path.endswith("/"):
        return candidate / "index.html"
    return candidate


def route(path):
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def main():
    htmls = sorted(ROOT.rglob("*.html"))
    errors = []
    schemas = 0
    links = 0
    locale_counts = {"de": 0, "ja": 0}
    translated = set()

    for path in htmls:
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        r = route(path)
        if r.startswith("/de/"):
            locale_counts["de"] += 1
            translated.add(r[3:])
        elif r.startswith("/ja/"):
            locale_counts["ja"] += 1
            translated.add(r[3:])
        if text.count('class="lang-menu"') != 1:
            errors.append(f"{r}: language dropdown count {text.count('class=\"lang-menu\"')}")
        if ADS_META not in text or ADS_CLIENT not in text:
            errors.append(f"{r}: missing AdSense ownership tags")
        for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
            try:
                json.loads(raw)
                schemas += 1
            except json.JSONDecodeError as exc:
                errors.append(f"{r}: invalid JSON-LD {exc}")
        for href in re.findall(r'href=["\']([^"\']+)["\']', text, re.I):
            if href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            if "${" in href:
                continue
            target = local_path(href)
            if target is None:
                continue
            links += 1
            if not target.exists():
                errors.append(f"{r}: broken link {href}")

    for base in translated:
        for prefix in ("", "de/", "ja/"):
            href = "/" + prefix + base.lstrip("/")
            target = local_path(href)
            if target and not target.exists():
                errors.append(f"translation set missing {href}")

    sitemap = (ROOT / "sitemap-pages.xml").read_text(encoding="utf-8")
    sitemap_urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
    for url in sitemap_urls:
        target = local_path(url)
        if target is None or not target.exists():
            errors.append(f"sitemap target missing {url}")
    ads_txt = (ROOT / "ads.txt").read_text(encoding="utf-8").strip()
    expected_ads = "google.com, pub-9505220977121599, DIRECT, f08c47fec0942fa0"
    if expected_ads not in ads_txt:
        errors.append("ads.txt publisher line missing")

    print(f"Round 9 audit: {len(htmls)} HTML, {len(sitemap_urls)} sitemap URLs, {links} internal links, {schemas} JSON-LD blocks")
    print(f"Locale pages: DE {locale_counts['de']}, JA {locale_counts['ja']}; dropdown {len(htmls)}/{len(htmls)}")
    print(f"Errors: {len(errors)}")
    for item in errors[:80]:
        print("ERROR", item)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
