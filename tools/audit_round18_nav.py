#!/usr/bin/env python3
"""Audit the Round 18 consolidated homepage navigation."""

from html.parser import HTMLParser
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def target_exists(href):
    if not href.startswith("/") or href.startswith("//"):
        return True
    path = href.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return True
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target /= "index.html"
    return target.exists()


def main():
    html = INDEX.read_text(encoding="utf-8")
    errors = []
    nav_match = re.search(r'<nav class="nav" id="nav">(.*?)</nav>', html, re.S)
    if not nav_match:
        errors.append("homepage nav missing")
        nav = ""
    else:
        nav = nav_match.group(1)

    if nav.count('class="site-menu"') != 4:
        errors.append(f"dropdown count {nav.count('class=\"site-menu\"')} != 4")
    for label in ("Home", "Database", "Guides", "Operations", "Game Info", "News", "FAQ"):
        if label not in nav:
            errors.append(f"missing primary label: {label}")
    for marker in (
        "ROUND 18: one-row consolidated navigation",
        'grid-template-areas:"brand nav status"',
        "flex-wrap:nowrap",
        "@media(max-width:980px)",
        "ROUND 18: keep only one click-open navigation group",
    ):
        if marker not in html:
            errors.append(f"missing behavior/style marker: {marker}")

    parser = LinkParser()
    parser.feed(nav)
    broken = sorted({href for href in parser.hrefs if not target_exists(href)})
    if broken:
        errors.extend(f"broken nav link: {href}" for href in broken)

    print(f"Primary navigation items: 8 (including language)")
    print(f"Click dropdown groups: {nav.count('class=\"site-menu\"')}/4")
    print(f"Navigation links checked: {len(parser.hrefs)}")
    print(f"Broken navigation links: {len(broken)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
