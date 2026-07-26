#!/usr/bin/env python3
"""Add contextual FAQ access to every English navigation-tab detail page."""

from html import escape, unescape
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_round10_news_faq as round10


FAQS = round10.faq.FAQS
HUBS = round10.faq.HUBS
LOCALE_LABELS = {
    "de": "FAQ",
    "fr": "FAQ",
    "it": "FAQ",
    "es": "FAQ",
    "ja": "FAQ",
    "ko": "자주 묻는 질문",
    "pl": "FAQ",
    "zh-cn": "常见问题",
    "zh-tw": "常見問題",
    "pt-br": "FAQ",
}
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "can", "company", "does",
    "for", "from", "have", "how", "in", "is", "of", "on", "or", "star",
    "the", "to", "wars", "what", "which", "who", "will", "with", "zero",
}


def visible_text(html: str) -> str:
    html = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", html, flags=re.I | re.S)
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", " ", html))).strip()


def tokens(text: str) -> set[str]:
    return {
        word for word in re.findall(r"[a-z0-9]+", text.lower())
        if len(word) > 2 and word not in STOPWORDS
    }


def choose_faqs(tab: str, html: str, count: int = 3):
    page_tokens = tokens(visible_text(html))
    candidates = [item for item in FAQS if tab in item[5]]
    if len(candidates) < count:
        candidates.extend(item for item in FAQS if item not in candidates)

    def score(item):
        question_tokens = tokens(item[1] + " " + item[2] + " " + item[3])
        overlap = len(page_tokens & question_tokens)
        phrase_bonus = sum(
            3 for word in question_tokens
            if re.search(rf"\b{re.escape(word)}\b", html, flags=re.I)
        )
        return overlap + phrase_bonus

    return sorted(candidates, key=lambda item: (-score(item), item[0]))[:count]


def detail_module(items) -> str:
    cards = "".join(
        (
            f'<a href="/questions/{item[0]}.html" '
            'style="display:block;border:1px solid #284050;border-radius:7px;'
            'padding:16px;color:inherit;text-decoration:none;background:#0d1922">'
            '<small style="color:#9db0bd">VERIFIED FAQ</small><br>'
            f'<strong style="color:#36e0ce">{escape(item[1])}</strong><br>'
            f'<span style="color:#9db0bd;font-size:14px">{escape(item[2])}</span></a>'
        )
        for item in items
    )
    return (
        '<!-- DETAIL_FAQ_START --><section class="detail-faq" '
        'aria-labelledby="detail-faq-title" style="margin:42px 0">'
        '<h2 id="detail-faq-title">Related FAQs</h2>'
        '<p style="color:#9db0bd">Three source-linked answers selected for this guide.</p>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));'
        f'gap:14px">{cards}</div>'
        '<p><a href="/questions/">Browse all 50 verified FAQs →</a></p>'
        '</section><!-- DETAIL_FAQ_END -->'
    )


def update_detail_pages() -> int:
    changed = 0
    for tab in HUBS:
        for path in sorted((ROOT / tab).glob("*.html")):
            if path.name == "index.html":
                continue
            html = path.read_text(encoding="utf-8-sig", errors="ignore")
            html = re.sub(
                r"<!-- DETAIL_FAQ_START -->.*?<!-- DETAIL_FAQ_END -->",
                "",
                html,
                flags=re.S,
            )
            module = detail_module(choose_faqs(tab, html))
            updated, replacements = re.subn(
                r"</main>", module + "</main>", html, count=1, flags=re.I
            )
            if replacements != 1:
                raise RuntimeError(f"Missing </main> in {path.relative_to(ROOT)}")
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def add_missing_localized_nav() -> int:
    changed = 0
    # Localized pages should link to the FAQ center in the same language.
    for locale, label in LOCALE_LABELS.items():
        for path in sorted((ROOT / locale).rglob("*.html")):
            html = path.read_text(encoding="utf-8-sig", errors="ignore")
            if not re.search(r"<nav\b", html, flags=re.I):
                continue
            href = f"/{locale}/questions/"
            if href in html:
                continue
            updated, replacements = re.subn(
                r"(<nav[^>]*>)",
                rf'\1<a href="{href}">{escape(label)}</a>',
                html,
                count=1,
                flags=re.I,
            )
            if replacements:
                path.write_text(updated, encoding="utf-8")
                changed += 1
    # English pages retain the canonical English FAQ route.
    for path in sorted(ROOT.glob("*.html")):
        html = path.read_text(encoding="utf-8-sig", errors="ignore")
        if not re.search(r"<nav\b", html, flags=re.I) or 'href="/questions/"' in html:
            continue
        updated, replacements = re.subn(
            r"(<nav[^>]*>)",
            r'\1<a href="/questions/">FAQ</a>',
            html,
            count=1,
            flags=re.I,
        )
        if replacements:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    assert len(FAQS) == 50
    detail_count = update_detail_pages()
    nav_count = add_missing_localized_nav()
    print(f"Added contextual FAQ modules to {detail_count} tab detail pages")
    print(f"Added localized FAQ navigation to {nav_count} pages")


if __name__ == "__main__":
    main()
