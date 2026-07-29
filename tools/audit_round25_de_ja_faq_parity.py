#!/usr/bin/env python3
"""Audit Round 25 German/Japanese FAQ parity."""

from __future__ import annotations

from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
import hashlib
import importlib.util
import itertools
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"

spec = importlib.util.spec_from_file_location(
    "round25_builder", ROOT / "tools" / "build_round25_de_ja_faq_parity.py"
)
builder = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(builder)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def extract(pattern: str, text: str) -> str:
    match = re.search(pattern, text, re.I | re.S)
    return unescape(re.sub(r"<[^>]+>", "", match.group(1)).strip()) if match else ""


def visible(text: str) -> str:
    text = re.sub(r"<(script|style|header|footer)\b.*?</\1>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(unescape(text).split())


def route_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-10]
    return "/" + rel


def file_for_route(route: str) -> Path | None:
    clean = route.lstrip("/")
    candidates = [ROOT / clean]
    if route.endswith("/"):
        candidates = [ROOT / clean / "index.html"]
    else:
        candidates.append(ROOT / clean / "index.html")
    for path in candidates:
        if path.exists() and path.is_file():
            return path
    return None


errors = []
warnings = []
sitemap = set((ROOT / "sitemap.txt").read_text().splitlines())
slugs = [item[0] for item in builder.r24.NEW_FAQS]
pages = [ROOT / locale / "questions" / f"{slug}.html" for locale in ("de", "ja") for slug in slugs]

if len(pages) != 100 or len(set(pages)) != 100:
    errors.append(f"expected 100 unique pages, got {len(set(pages))}")

style_hashes = set()
titles = set()
locale_bodies = {"de": {}, "ja": {}}
for path in pages:
    locale = path.parts[-3]
    slug = path.stem
    if not path.exists():
        errors.append(f"missing {path.relative_to(ROOT)}")
        continue
    text = read(path)
    title = extract(r"<title>(.*?)</title>", text)
    description = extract(r'<meta name="description" content="(.*?)"', text)
    canonical = extract(r'<link rel="canonical" href="(.*?)"', text)
    expected = SITE + route_for(path)
    h1s = re.findall(r"<h1\b[^>]*>.*?</h1>", text, re.I | re.S)
    if not title or not description or len(h1s) != 1:
        errors.append(f"metadata/H1 error {path.relative_to(ROOT)}")
    if title in titles:
        errors.append(f"duplicate title {title}")
    titles.add(title)
    if canonical != expected:
        errors.append(f"canonical error {path.relative_to(ROOT)}")
    if expected not in sitemap:
        errors.append(f"sitemap missing {path.relative_to(ROOT)}")
    if f'<html lang="{locale}">' not in text:
        errors.append(f"html language error {path.relative_to(ROOT)}")
    for code, href in (
        ("en", f"{SITE}/questions/{slug}.html"),
        ("de", f"{SITE}/de/questions/{slug}.html"),
        ("ja", f"{SITE}/ja/questions/{slug}.html"),
        ("x-default", f"{SITE}/questions/{slug}.html"),
    ):
        tag = f'<link rel="alternate" hreflang="{code}" href="{href}">'
        if text.count(tag) != 1:
            errors.append(f"hreflang {code} error {path.relative_to(ROOT)}")
    if text.count("ca-pub-9505220977121599") < 2:
        errors.append(f"AdSense error {path.relative_to(ROOT)}")
    schemas = re.findall(r'<script type="application/ld\+json">(.*?)</script>', text, re.I | re.S)
    try:
        parsed = [json.loads(raw) for raw in schemas]
    except json.JSONDecodeError as exc:
        errors.append(f"JSON-LD error {path.relative_to(ROOT)}: {exc}")
        parsed = []
    if not any(x.get("@type") == "FAQPage" and x.get("inLanguage") == locale for x in parsed):
        errors.append(f"FAQ schema/language error {path.relative_to(ROOT)}")
    styles = re.findall(r"<style>(.*?)</style>", text, re.I | re.S)
    if len(styles) != 1:
        errors.append(f"style count error {path.relative_to(ROOT)}")
    else:
        style_hashes.add(hashlib.sha256(styles[0].encode()).hexdigest())
    body = visible(text)
    locale_bodies[locale][path] = body
    count = len(re.findall(r"[A-Za-zÀ-ž0-9']+", body)) if locale == "de" else len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", body))
    threshold = 190 if locale == "de" else 300
    if count < threshold:
        errors.append(f"thin localized body {path.relative_to(ROOT)}: {count}")

english_style = re.search(
    r"<style>(.*?)</style>",
    read(ROOT / "questions" / f"{slugs[0]}.html"),
    re.I | re.S,
).group(1)
english_hash = hashlib.sha256(english_style.encode()).hexdigest()
if style_hashes != {english_hash}:
    errors.append(f"English-style parity failed: {style_hashes} vs {english_hash}")

for slug in slugs:
    english = read(ROOT / "questions" / f"{slug}.html")
    for code, href in (
        ("en", f"{SITE}/questions/{slug}.html"),
        ("de", f"{SITE}/de/questions/{slug}.html"),
        ("ja", f"{SITE}/ja/questions/{slug}.html"),
        ("x-default", f"{SITE}/questions/{slug}.html"),
    ):
        if english.count(f'<link rel="alternate" hreflang="{code}" href="{href}">') != 1:
            errors.append(f"English reciprocal hreflang {code} error: {slug}")

for locale in ("de", "ja"):
    hub = read(ROOT / locale / "questions" / "index.html")
    if hub.count("<!-- ROUND25_FAQ_START -->") != 1 or hub.count("<!-- ROUND25_FAQ_END -->") != 1:
        errors.append(f"{locale} hub marker error")
    for slug in slugs:
        if f'/{locale}/questions/{slug}.html' not in hub:
            errors.append(f"{locale} hub missing {slug}")

# Similarity is evaluated on page-specific answer content, excluding shared explanatory blocks.
for locale in ("de", "ja"):
    specific = {}
    for path in locale_bodies[locale]:
        text = read(path)
        chunks = re.findall(
            r'<section class="(?:hero|block answer)".*?</section>',
            text,
            re.I | re.S,
        )
        normalized = visible(" ".join(chunks))
        tokens = (
            re.findall(r"[a-zà-ž0-9']+", normalized.lower())
            if locale == "de"
            else list(re.sub(r"\s+", "", normalized))
        )
        specific[path] = set(zip(tokens, tokens[1:], tokens[2:]))
    maximum = (0.0, None, None)
    for left, right in itertools.combinations(specific, 2):
        a, b = specific[left], specific[right]
        score = len(a & b) / max(1, len(a | b))
        maximum = max(maximum, (score, left, right), key=lambda x: x[0])
    if maximum[0] >= 0.72:
        errors.append(f"{locale} page-specific similarity {maximum[0]:.3f}: {maximum[1]} / {maximum[2]}")

all_pages = list(ROOT.rglob("*.html"))
broken = []
links = 0
for path in all_pages:
    parser = Parser()
    parser.feed(read(path))
    base = SITE + route_for(path)
    for href in parser.hrefs:
        if href.startswith(("mailto:", "tel:", "javascript:", "data:")) or "${" in href:
            continue
        target = urlparse(urljoin(base, href))
        if target.netloc not in {"", "starwarszerocompany.cc"}:
            continue
        links += 1
        target_file = file_for_route(target.path or "/")
        if target_file is None:
            broken.append((path.relative_to(ROOT).as_posix(), href))
            continue
        if target.fragment:
            target_parser = Parser()
            target_parser.feed(read(target_file))
            accepted = {target.fragment}
            if target_file == ROOT / "index.html":
                accepted.add(f"view-{target.fragment}")
            if not (accepted & target_parser.ids):
                broken.append((path.relative_to(ROOT).as_posix(), href))

if broken:
    errors.append(f"broken internal links: {len(broken)}; sample={broken[:5]}")

if len(sitemap) != 1476:
    errors.append(f"expected 1476 sitemap URLs, got {len(sitemap)}")
if len(all_pages) != 1712:
    errors.append(f"expected 1712 HTML pages, got {len(all_pages)}")

print(f"Round 25 pages: {len(pages)}/100")
print(f"Sitemap URLs: {len(sitemap)}")
print(f"HTML pages: {len(all_pages)}")
print(f"Internal links: {links}; broken: {len(broken)}")
print(f"English style parity hashes: {len(style_hashes)}")
print(f"Errors: {len(errors)}")
for error in errors:
    print("ERROR:", error)
for warning in warnings:
    print("WARN:", warning)
raise SystemExit(1 if errors else 0)
