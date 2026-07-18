#!/usr/bin/env python3
"""Fail CI on structural SEO errors and report content-quality risks."""

from collections import Counter
from html import unescape
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"


def first(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    if not match:
        return ""
    value = match.groupdict().get("value") or match.group(1)
    return unescape(re.sub(r"<[^>]+>", " ", value).strip())


def visible_word_count(text: str) -> int:
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
    return len(unescape(re.sub(r"<[^>]+>", " ", text)).split())


def visible_cjk_count(text: str) -> int:
    """Count CJK characters so Japanese pages are not judged by whitespace tokens."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
    visible = unescape(re.sub(r"<[^>]+>", " ", text))
    return len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", visible))


def route_for(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return "/"
    if relative.endswith("/index.html"):
        return "/" + relative[:-10]
    return "/" + relative


def main() -> int:
    rows, errors, warnings = [], [], []
    for path in sorted(ROOT.rglob("*.html")):
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        route = route_for(path)
        title = first(r"<title[^>]*>(.*?)</title>", text)
        desc = first(r'<meta\s+name=["\']description["\']\s+content=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', text)
        canonical = first(r'<link\s+rel=["\']canonical["\']\s+href=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', text)
        visible_markup = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
        h1s = re.findall(r"<h1[^>]*>.*?</h1>", visible_markup, re.I | re.S)
        robots = first(r'<meta\s+name=["\']robots["\']\s+content=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', text)
        words = visible_word_count(text)
        cjk_chars = visible_cjk_count(text)
        rows.append((route, title, desc, canonical))
        expected = SITE + route
        h1_ok = len(h1s) >= 1 if route == "/" else len(h1s) == 1
        if not title or not desc or not canonical or not h1_ok:
            errors.append(f"{route}: missing title/description/canonical or H1 count is {len(h1s)}")
        if canonical and canonical != expected:
            errors.append(f"{route}: canonical {canonical} != {expected}")
        # A focused Japanese answer can be complete at roughly 250 CJK characters;
        # whitespace-token counts are not comparable to English or German words.
        if "noindex" not in robots.lower() and words < 180 and cjk_chars < 250:
            warnings.append(f"{route}: indexable page has only {words} visible words")
        if "noindex" not in robots.lower() and re.search(r"\b(placeholder|TBD|not confirmed)\b", text, re.I):
            warnings.append(f"{route}: indexable page contains an uncertainty marker")
    for label, index in (("title", 1), ("description", 2), ("canonical", 3)):
        counts = Counter(row[index] for row in rows if row[index])
        for value, count in counts.items():
            if count > 1:
                errors.append(f"duplicate {label} used {count} times: {value}")
    print(f"SEO audit: {len(rows)} HTML pages, {len(errors)} errors, {len(warnings)} quality warnings")
    for item in errors:
        print("ERROR", item)
    for item in warnings[:40]:
        print("WARN ", item)
    if len(warnings) > 40:
        print(f"WARN  ... {len(warnings) - 40} more warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
