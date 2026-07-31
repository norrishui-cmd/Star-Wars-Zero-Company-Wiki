#!/usr/bin/env python3
"""Audit Round 26 navigation News and FAQ expansion."""

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

spec = importlib.util.spec_from_file_location("round26", ROOT / "tools" / "build_round26_nav_news_faq.py")
builder = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(builder)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs: list[str] = []
        self.ids: set[str] = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "a" and data.get("href"):
            self.hrefs.append(data["href"])


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def file_for(route: str) -> Path | None:
    clean = route.lstrip("/")
    candidates = [ROOT / clean] if clean else [ROOT / "index.html"]
    if clean:
        candidates.append(ROOT / clean / "index.html")
    return next((path for path in candidates if path.is_file()), None)


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return unescape(re.sub(r"<[^>]+>", "", match.group(1)).strip()) if match else ""


def visible(text: str) -> str:
    text = re.sub(r"<(script|style|header|footer)\b.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<!--.*?-->|<[^>]+>", " ", text, flags=re.S)
    return " ".join(unescape(text).split())


def shingles(text: str, n: int = 5):
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {tuple(words[i:i+n]) for i in range(max(0, len(words) - n + 1))}


errors: list[str] = []
sitemap = set((ROOT / "sitemap.txt").read_text().splitlines())
news = [
    ROOT / "news" / target[0] / f"{target[0]}-{fact}-update.html"
    for target in builder.TARGETS for fact in target[4]
]
faqs = [ROOT / "questions" / f"{item[0]}.html" for item in builder.NEW_FAQS]

if len(news) != 110 or len(set(news)) != 110:
    errors.append(f"expected 110 unique News paths, got {len(set(news))}")
if len(faqs) != 50 or len(set(faqs)) != 50:
    errors.append(f"expected 50 unique FAQ paths, got {len(set(faqs))}")

titles: dict[str, Path] = {}
descriptions: dict[str, Path] = {}
word_counts: dict[Path, int] = {}
for kind, paths, schema_type in (("News", news, "NewsArticle"), ("FAQ", faqs, "FAQPage")):
    for path in paths:
        if not path.exists():
            errors.append(f"missing {kind} {path.relative_to(ROOT)}")
            continue
        text = read(path)
        title = extract(r"<title>(.*?)</title>", text)
        description = extract(r'<meta\s+name="description"\s+content="(.*?)"', text)
        canonical = extract(r'<link\s+rel="canonical"\s+href="(.*?)"', text)
        h1s = re.findall(r"<h1\b[^>]*>.*?</h1>", text, re.I | re.S)
        if not title or not description or len(h1s) != 1:
            errors.append(f"{kind} metadata/H1 error {path.relative_to(ROOT)}")
        if title in titles:
            errors.append(f"duplicate new title: {title}")
        titles[title] = path
        if description in descriptions:
            errors.append(f"duplicate new description: {path.relative_to(ROOT)}")
        descriptions[description] = path
        expected = SITE + route_for(path)
        if canonical != expected or expected not in sitemap:
            errors.append(f"canonical/sitemap mismatch {path.relative_to(ROOT)}")
        schemas = re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', text, re.I | re.S)
        parsed = []
        for raw in schemas:
            try:
                parsed.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSON-LD {path.relative_to(ROOT)}: {exc}")
        if not any(item.get("@type") == schema_type for item in parsed if isinstance(item, dict)):
            errors.append(f"missing {schema_type} {path.relative_to(ROOT)}")
        if text.count("ca-pub-9505220977121599") < 2:
            errors.append(f"AdSense ownership missing {path.relative_to(ROOT)}")
        if text.count("<summary>Language</summary>") != 1:
            errors.append(f"language menu error {path.relative_to(ROOT)}")
        word_counts[path] = len(re.findall(r"[A-Za-z0-9']+", visible(text)))

for target in builder.TARGETS:
    key, _, route, _, facts, _ = target
    path = ROOT / "index.html" if key in {"home", "muster"} else ROOT / route.strip("/") / "index.html"
    text = read(path)
    marker = f"ROUND26_{key.upper()}_MODULES"
    if text.count(f"<!-- {marker}_START -->") != 1 or text.count(f"<!-- {marker}_END -->") != 1:
        errors.append(f"module wrapper error {key}")
    for fact in facts:
        if builder.news_path(target, fact) not in text:
            errors.append(f"{key} missing News {fact}")
    for item in builder.related_faqs(target):
        if f'/questions/{item[0]}.html' not in text:
            errors.append(f"{key} missing FAQ {item[0]}")

news_hub = read(ROOT / "news" / "index.html")
faq_hub = read(ROOT / "questions" / "index.html")
for path in news:
    if route_for(path) not in news_hub:
        errors.append(f"News hub missing {route_for(path)}")
for path in faqs:
    if route_for(path) not in faq_hub:
        errors.append(f"FAQ hub missing {route_for(path)}")

indexable_faqs = []
faq_intents: dict[str, Path] = {}
for path in (ROOT / "questions").glob("*.html"):
    if path.name == "index.html":
        continue
    text = read(path)
    if re.search(r'<meta\s+name="robots"\s+content="[^"]*noindex', text, re.I):
        continue
    indexable_faqs.append(path)
    h1 = extract(r"<h1\b[^>]*>(.*?)</h1>", text)
    if h1 in faq_intents:
        errors.append(f"duplicate FAQ intent: {h1}")
    faq_intents[h1] = path
if len(indexable_faqs) != 152:
    errors.append(f"expected 152 indexable English FAQs, got {len(indexable_faqs)}")

sets = {path: shingles(visible(read(path))) for path in news}
maximum = (0.0, None, None)
for left, right in itertools.combinations(news, 2):
    a, b = sets[left], sets[right]
    score = len(a & b) / max(1, len(a | b))
    if score > maximum[0]:
        maximum = (score, left, right)
if maximum[0] >= 0.72:
    errors.append(f"News similarity too high: {maximum[0]:.3f} between {maximum[1]} and {maximum[2]}")

broken = []
link_count = 0
for path in ROOT.rglob("*.html"):
    parser = Parser()
    parser.feed(read(path))
    base = SITE + route_for(path)
    for href in parser.hrefs:
        if href.startswith(("mailto:", "tel:", "javascript:", "data:")) or "${" in href:
            continue
        parsed = urlparse(urljoin(base, href))
        if parsed.netloc not in {"", "starwarszerocompany.cc"}:
            continue
        link_count += 1
        target = file_for(parsed.path or "/")
        if target is None:
            broken.append((path.relative_to(ROOT).as_posix(), href))
            continue
        if parsed.fragment:
            target_parser = Parser()
            target_parser.feed(read(target))
            accepted = {parsed.fragment}
            if target == ROOT / "index.html" and parsed.fragment in {"home", "muster"}:
                accepted.add("view-" + parsed.fragment)
            if not accepted & target_parser.ids:
                broken.append((path.relative_to(ROOT).as_posix(), href))
if broken:
    errors.extend(f"broken {source} -> {href}" for source, href in broken[:40])

print(f"Round 26 audit: {len(news)}/110 News; {len(faqs)}/50 new FAQs; {len(indexable_faqs)}/152 English FAQs")
print(f"New visible words: min {min(word_counts.values())}; avg {sum(word_counts.values()) // len(word_counts)}; max {max(word_counts.values())}")
print(f"Highest News similarity: {maximum[0]:.3f} ({maximum[1].relative_to(ROOT)} vs {maximum[2].relative_to(ROOT)})")
print(f"Internal links: {link_count}; broken: {len(broken)}")
print(f"Sitemap URLs: {len(sitemap)}")
if errors:
    print(f"FAIL: {len(errors)} errors")
    for error in errors[:100]:
        print("ERROR", error)
    raise SystemExit(1)
print("PASS: all Round 26 quality gates")
