#!/usr/bin/env python3
"""Round 15 quality gate for verified FAQ inventory and contextual access."""

from html import unescape
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_round10_news_faq as round10


FAQS = round10.faq.FAQS
HUBS = round10.faq.HUBS


def main() -> int:
    errors = []
    sitemap = set((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines())
    active = {item[0] for item in FAQS}

    for slug in active:
        path = ROOT / "questions" / f"{slug}.html"
        if not path.exists():
            errors.append(f"missing FAQ: {slug}")
            continue
        html = path.read_text(encoding="utf-8-sig", errors="ignore")
        if "noindex" in html.lower():
            errors.append(f"active FAQ is noindex: {slug}")
        if f"{SITE}/questions/{slug}.html" not in sitemap:
            errors.append(f"FAQ missing from sitemap: {slug}")
        if "FAQPage" not in html:
            errors.append(f"FAQ schema missing: {slug}")
        for block in re.findall(
            r'<script[^>]+type="application/ld\+json"[^>]*>(.*?)</script>',
            html,
            flags=re.I | re.S,
        ):
            try:
                json.loads(unescape(block))
            except json.JSONDecodeError:
                errors.append(f"invalid JSON-LD: questions/{slug}.html")

    hub_count = 0
    detail_count = 0
    for tab in HUBS:
        hub = ROOT / tab / "index.html"
        html = hub.read_text(encoding="utf-8-sig", errors="ignore")
        match = re.search(
            r"<!-- TAB_FAQ_START -->(.*?)<!-- TAB_FAQ_END -->", html, flags=re.S
        )
        if not match:
            errors.append(f"hub FAQ module missing: {tab}")
        else:
            links = re.findall(r'href="/questions/([^"]+)\.html"', match.group(1))
            if len(links) != 5 or len(set(links)) != 5:
                errors.append(f"hub must contain five unique FAQs: {tab}")
            if any(slug not in active for slug in links):
                errors.append(f"hub links non-active FAQ: {tab}")
            hub_count += 1

        for path in sorted((ROOT / tab).glob("*.html")):
            if path.name == "index.html":
                continue
            html = path.read_text(encoding="utf-8-sig", errors="ignore")
            match = re.search(
                r"<!-- DETAIL_FAQ_START -->(.*?)<!-- DETAIL_FAQ_END -->",
                html,
                flags=re.S,
            )
            if not match:
                errors.append(f"detail FAQ module missing: {path.relative_to(ROOT)}")
                continue
            links = re.findall(r'href="/questions/([^"]+)\.html"', match.group(1))
            if len(links) != 3 or len(set(links)) != 3:
                errors.append(f"detail must contain three unique FAQs: {path.relative_to(ROOT)}")
            if any(slug not in active for slug in links):
                errors.append(f"detail links non-active FAQ: {path.relative_to(ROOT)}")
            detail_count += 1

    nav_pages = 0
    nav_covered = 0
    for path in ROOT.rglob("*.html"):
        html = path.read_text(encoding="utf-8-sig", errors="ignore")
        if not re.search(r"<nav\b", html, flags=re.I):
            continue
        nav_pages += 1
        relative = path.relative_to(ROOT)
        locale = relative.parts[0] if len(relative.parts) > 1 else ""
        expected = (
            f'href="/{locale}/questions/"'
            if locale and (ROOT / locale / "questions" / "index.html").exists()
            else 'href="/questions/"'
        )
        if expected in html:
            nav_covered += 1
        else:
            errors.append(f"FAQ nav missing: {relative}")

    print(f"Verified FAQ set: {len(active)}/50")
    print(f"Tab hubs with five related FAQs: {hub_count}/16")
    print(f"Tab detail pages with three related FAQs: {detail_count}")
    print(f"Navigation FAQ coverage: {nav_covered}/{nav_pages}")
    print(f"Errors: {len(errors)}")
    for error in errors[:100]:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
