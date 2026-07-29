#!/usr/bin/env python3
"""Audit Round 24 navigation News and FAQ expansion."""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import importlib.util
import itertools
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"

spec = importlib.util.spec_from_file_location(
    "round24_builder", ROOT / "tools" / "build_round24_nav_news_faq.py"
)
builder = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(builder)


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def file_for_route(route: str) -> Path | None:
    route = route.split("?", 1)[0]
    if route == "/":
        return ROOT / "index.html"
    clean = route.lstrip("/")
    candidates = []
    if route.endswith("/"):
        candidates.append(ROOT / clean / "index.html")
    else:
        candidates.extend([ROOT / clean, ROOT / clean / "index.html"])
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return unescape(re.sub(r"<[^>]+>", "", match.group(1)).strip()) if match else ""


def visible_text(text: str) -> str:
    text = re.sub(r"<(script|style|header|footer)\b.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(unescape(text).split())


def shingles(text: str, n: int = 5):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(words[i:i+n]) for i in range(max(0, len(words) - n + 1))}


errors = []
sitemap = set((ROOT / "sitemap.txt").read_text().splitlines())

new_news = []
for target in builder.TARGETS:
    key, _, _, _, facts, _ = target
    for fact in facts:
        new_news.append(ROOT / "news" / key / f"{key}-{fact}-update.html")

new_faqs = [ROOT / "questions" / f"{item[0]}.html" for item in builder.NEW_FAQS]

if len(new_news) != 110 or len(set(new_news)) != 110:
    errors.append(f"expected 110 unique News paths, got {len(set(new_news))}")
if len(new_faqs) != 50 or len(set(new_faqs)) != 50:
    errors.append(f"expected 50 unique FAQ paths, got {len(set(new_faqs))}")

titles = {}
descriptions = {}
new_word_counts = {}
for kind, paths, schema_type in (
    ("News", new_news, "NewsArticle"),
    ("FAQ", new_faqs, "FAQPage"),
):
    for path in paths:
        if not path.exists():
            errors.append(f"missing {kind} page {path.relative_to(ROOT)}")
            continue
        text = read(path)
        title = extract(r"<title>(.*?)</title>", text)
        description = extract(r'<meta\s+name="description"\s+content="(.*?)"', text)
        canonical = extract(r'<link\s+rel="canonical"\s+href="(.*?)"', text)
        h1s = re.findall(r"<h1\b[^>]*>(.*?)</h1>", text, re.I | re.S)
        if not title or not description or len(h1s) != 1:
            errors.append(f"{kind} metadata/H1 error {path.relative_to(ROOT)}")
        if title in titles:
            errors.append(f"duplicate title: {title}")
        titles[title] = path
        if description in descriptions:
            errors.append(f"duplicate description: {path.relative_to(ROOT)}")
        descriptions[description] = path
        expected = SITE + route_for(path)
        if canonical != expected:
            errors.append(f"canonical mismatch {path.relative_to(ROOT)}")
        if expected not in sitemap:
            errors.append(f"missing from sitemap {path.relative_to(ROOT)}")
        if not re.search(r'<meta\s+name="robots"\s+content="index,follow"', text, re.I):
            errors.append(f"not indexable {path.relative_to(ROOT)}")
        schemas = re.findall(
            r'<script\s+type="application/ld\+json">(.*?)</script>',
            text,
            re.I | re.S,
        )
        parsed = []
        for raw in schemas:
            try:
                parsed.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON-LD {path.relative_to(ROOT)}: {exc}")
        if not any(x.get("@type") == schema_type for x in parsed if isinstance(x, dict)):
            errors.append(f"missing {schema_type} schema {path.relative_to(ROOT)}")
        if text.count("ca-pub-9505220977121599") < 2:
            errors.append(f"AdSense ownership missing {path.relative_to(ROOT)}")
        if text.count("<summary>Language</summary>") != 1:
            errors.append(f"language dropdown error {path.relative_to(ROOT)}")
        new_word_counts[path] = len(re.findall(r"[A-Za-z0-9']+", visible_text(text)))

for target in builder.TARGETS:
    key, _, route, _, facts, _ = target
    if key in {"home", "muster"}:
        path = ROOT / "index.html"
    else:
        path = ROOT / route.strip("/") / "index.html"
    text = read(path)
    wrapper = f"ROUND24_{key.upper()}_MODULES"
    if text.count(f"<!-- {wrapper}_START -->") != 1 or text.count(f"<!-- {wrapper}_END -->") != 1:
        errors.append(f"module wrapper error for {key}")
    for fact in facts:
        href = f'/news/{key}/{key}-{fact}-update.html'
        if href not in text:
            errors.append(f"{key} missing News link {href}")
    related = builder.related_faqs(target)
    if len(related) != 5:
        errors.append(f"{key} does not have five related FAQs")
    for item in related:
        href = f'/questions/{item[0]}.html'
        if href not in text:
            errors.append(f"{key} missing FAQ link {href}")

news_hub = read(ROOT / "news" / "index.html")
faq_hub = read(ROOT / "questions" / "index.html")
for path in new_news:
    if route_for(path) not in news_hub:
        errors.append(f"News hub missing {route_for(path)}")
for path in new_faqs:
    if route_for(path) not in faq_hub:
        errors.append(f"FAQ hub missing {route_for(path)}")
if "110 New Navigation News Reports" not in news_hub:
    errors.append("News hub count copy is missing")
if "102 Verified Answers" not in faq_hub:
    errors.append("FAQ hub count copy is missing")

indexable_faqs = 0
faq_h1s = {}
for path in (ROOT / "questions").glob("*.html"):
    if path.name == "index.html":
        continue
    text = read(path)
    if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', text, re.I):
        continue
    indexable_faqs += 1
    h1 = extract(r"<h1\b[^>]*>(.*?)</h1>", text)
    if h1 in faq_h1s:
        errors.append(f"duplicate indexable FAQ intent: {h1}")
    faq_h1s[h1] = path
if indexable_faqs != 102:
    errors.append(f"expected 102 indexable FAQ leaves, got {indexable_faqs}")

news_sets = {path: shingles(visible_text(read(path))) for path in new_news}
max_similarity = (0.0, None, None)
for a, b in itertools.combinations(new_news, 2):
    left, right = news_sets[a], news_sets[b]
    similarity = len(left & right) / max(1, len(left | right))
    if similarity > max_similarity[0]:
        max_similarity = (similarity, a, b)
if max_similarity[0] >= 0.72:
    errors.append(
        "News similarity too high: "
        f"{max_similarity[0]:.3f} between {max_similarity[1]} and {max_similarity[2]}"
    )

all_pages = list(ROOT.rglob("*.html"))
broken = []
link_count = 0
for path in all_pages:
    parser = PageParser()
    text = read(path)
    parser.feed(text)
    base_url = SITE + route_for(path)
    for href in parser.hrefs:
        if href.startswith(("mailto:", "tel:", "javascript:", "data:")) or "${" in href:
            continue
        absolute = urljoin(base_url, href)
        parsed = urlparse(absolute)
        if parsed.netloc not in {"", "starwarszerocompany.cc"}:
            continue
        link_count += 1
        target = file_for_route(parsed.path or "/")
        if target is None:
            broken.append((path.relative_to(ROOT).as_posix(), href))
            continue
        if parsed.fragment:
            target_parser = PageParser()
            target_parser.feed(read(target))
            accepted_fragments = {parsed.fragment}
            if target == ROOT / "index.html" and parsed.fragment in {"home", "muster"}:
                accepted_fragments.add("view-" + parsed.fragment)
            if not accepted_fragments & target_parser.ids:
                broken.append((path.relative_to(ROOT).as_posix(), href))
if broken:
    errors.extend(f"broken link {source} -> {href}" for source, href in broken[:30])

print(
    f"Round 24 audit: {len(new_news)}/110 News, {len(new_faqs)}/50 new FAQs, "
    f"{indexable_faqs}/102 indexable FAQs"
)
print(
    f"New page word counts: min {min(new_word_counts.values())}, "
    f"avg {sum(new_word_counts.values()) // len(new_word_counts)}, "
    f"max {max(new_word_counts.values())}"
)
print(
    f"Highest News five-word similarity: {max_similarity[0]:.3f} "
    f"({max_similarity[1].relative_to(ROOT)} vs {max_similarity[2].relative_to(ROOT)})"
)
print(f"Internal links checked: {link_count}; broken: {len(broken)}")
print(f"Sitemap URLs: {len(sitemap)}")
if errors:
    print(f"FAIL: {len(errors)} errors")
    for error in errors[:80]:
        print("ERROR", error)
    raise SystemExit(1)
print("PASS: all Round 24 quality gates")
