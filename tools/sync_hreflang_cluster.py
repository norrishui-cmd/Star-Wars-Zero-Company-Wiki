#!/usr/bin/env python3
"""Synchronize one group of translated HTML pages after indexing decisions are applied."""

import argparse
from html import escape
from pathlib import Path
import re

from build_sitemaps import is_draft_leaf, url_for
from configure_language_dropdown import LANG_TAGS, route_for


CANONICAL = re.compile(r'<link\s+rel="canonical"\s+href="([^"]+)"[^>]*>', re.I)
ALTERNATE = re.compile(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"[^>]*>', re.I)
NOINDEX = re.compile(r'<meta\s+name="robots"\s+content="[^"]*\bnoindex\b', re.I)


def sync_cluster(paths):
    pages = {}
    alternatives = {}
    locales = set()
    routes = set()
    for path in paths:
        path = path.resolve()
        locale, route = route_for(path)
        routes.add(route)
        lang = LANG_TAGS[locale]
        if lang in locales or len(routes) > 1:
            raise ValueError("Pass one file per language, all for the same topic route")
        locales.add(lang)
        text = path.read_text(encoding="utf-8")
        canonical = CANONICAL.search(text)
        if canonical is None:
            raise ValueError(f"Missing canonical on {path}")
        url = url_for(path)
        eligible = canonical.group(1) == url and not NOINDEX.search(text) and not is_draft_leaf(path)
        pages[path] = (text, eligible)
        if eligible:
            alternatives[lang] = url

    if "en" in alternatives:
        alternatives["x-default"] = alternatives["en"]
    links = "".join(f'<link rel="alternate" hreflang="{lang}" href="{escape(url)}">'
                    for lang, url in alternatives.items())
    for path, (text, _) in pages.items():
        if set(ALTERNATE.findall(text)) - locales - {"x-default"}:
            raise ValueError(f"Cluster contains another language in {path}. Include its counterpart.")
    changed = 0
    for path, (text, eligible) in pages.items():
        clean = ALTERNATE.sub("", text)
        updated = CANONICAL.sub(lambda match: match[0] + (links if eligible else ""), clean, count=1)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pages", nargs="+", type=Path,
                        help="Explicit paths for all translations, e.g. news/index.html de/news/index.html ja/news/index.html")
    print(f"Updated hreflang on {sync_cluster(parser.parse_args().pages)} pages")
