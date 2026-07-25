#!/usr/bin/env python3
"""Quality gate for the Round 13 multilingual FAQ batch."""

from html import unescape
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
LOCALES = ("en", "de", "fr", "it", "es", "ja", "ko", "pl", "zh-cn", "zh-tw", "pt-br")
NEW_LOCALES = ("fr", "it", "es", "ko", "pl", "zh-cn", "zh-tw", "pt-br")
SLUGS = (
    "when-does-star-wars-zero-company-release", "what-platforms-is-zero-company-on",
    "how-many-languages-does-zero-company-support", "is-zero-company-single-player",
    "does-zero-company-have-coop", "does-zero-company-have-romance",
    "can-you-disable-permadeath", "how-many-action-points-per-turn",
    "is-zero-company-on-steam-deck", "should-you-preorder",
)


def visible(text: str) -> str:
    text = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", text, flags=re.I | re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", text))).strip()


def grams(text: str) -> set:
    cjk = "".join(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", text))
    if len(cjk) > 80:
        return {cjk[i:i + 12] for i in range(max(0, len(cjk) - 11))}
    words = re.findall(r"[a-zà-ž0-9]+", text.lower())
    return {" ".join(words[i:i + 5]) for i in range(max(0, len(words) - 4))}


def main() -> int:
    sitemap = set((ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines())
    errors = []
    contents = {}
    checked = 0
    for locale in LOCALES:
        for slug in SLUGS:
            rel = Path("questions") / f"{slug}.html"
            path = ROOT / rel if locale == "en" else ROOT / locale / rel
            if not path.exists():
                errors.append(f"missing equivalent: {locale}/{rel}")
                continue
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            url = SITE + (f"/{rel.as_posix()}" if locale == "en" else f"/{locale}/{rel.as_posix()}")
            if url not in sitemap:
                errors.append(f"not indexed in sitemap: {url}")
            tags = re.findall(r'<link\s+rel=["\']alternate["\']\s+hreflang=["\']([^"\']+)', text, re.I)
            if len(tags) != 12 or len(set(tags)) != 12 or "x-default" not in tags:
                errors.append(f"bad hreflang set: {path.relative_to(ROOT)}")
            canon = re.search(r'<link\s+rel=["\']canonical["\']\s+href=["\']([^"\']+)', text, re.I)
            if not canon or canon.group(1) != url:
                errors.append(f"bad canonical: {path.relative_to(ROOT)}")
            for raw in re.findall(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', text, re.I | re.S):
                try:
                    json.loads(raw)
                except json.JSONDecodeError:
                    errors.append(f"invalid JSON-LD: {path.relative_to(ROOT)}")
            if locale in NEW_LOCALES or (locale in ("de", "ja") and slug in SLUGS[5:]):
                body = visible(text)
                if locale in ("ja", "ko", "zh-cn", "zh-tw"):
                    if len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]", body)) < 260:
                        errors.append(f"thin CJK page: {path.relative_to(ROOT)}")
                elif len(body.split()) < 180:
                    errors.append(f"thin page: {path.relative_to(ROOT)} ({len(body.split())} words)")
                contents[(locale, slug)] = body
                checked += 1

    # Compare only pages in the same language. Cross-language equivalents target separate SERPs.
    max_similarity = (0.0, None)
    for locale in NEW_LOCALES:
        locale_pages = [(slug, contents[(locale, slug)]) for slug in SLUGS]
        for i, (a_slug, a_text) in enumerate(locale_pages):
            a = grams(a_text)
            for b_slug, b_text in locale_pages[i + 1:]:
                b = grams(b_text)
                score = len(a & b) / max(1, len(a | b))
                if score > max_similarity[0]:
                    max_similarity = (score, f"{locale}:{a_slug} vs {b_slug}")
                if score >= 0.72:
                    errors.append(f"near duplicate {score:.3f}: {locale}:{a_slug} vs {b_slug}")

    print(f"Round 13 audited localized pages: {checked}")
    print(f"Exact multilingual equivalents: {len(LOCALES) * len(SLUGS)}")
    print(f"Sitemap URLs: {len(sitemap)}")
    print(f"Highest same-language five-gram similarity: {max_similarity[0]:.3f} ({max_similarity[1]})")
    print(f"Errors: {len(errors)}")
    for error in errors[:100]:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
