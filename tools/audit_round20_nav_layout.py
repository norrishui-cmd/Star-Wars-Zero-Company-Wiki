#!/usr/bin/env python3
"""Audit the Round 20 language/search separation in the homepage navigation."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def main():
    html = INDEX.read_text(encoding="utf-8")
    errors = []

    checks = {
        "dedicated navigation actions wrapper":
            '<div class="nav-actions">' in html,
        "desktop language switcher":
            'class="lang-menu desktop-lang"' in html,
        "mobile language switcher":
            'class="lang-menu mobile-lang"' in html,
        "search nested in actions wrapper":
            re.search(
                r'<div class="nav-actions">\s*<details class="lang-menu desktop-lang".*?'
                r'<form class="nav-search"',
                html,
                re.S,
            ) is not None,
        "two explicit desktop columns":
            "grid-template-columns:max-content minmax(176px,226px)" in html,
        "search fills only its own column":
            re.search(
                r"\.nav-search\{\s*position:relative;\s*width:100%;\s*min-width:0;",
                html,
            ) is not None,
        "desktop language minimum width":
            ".nav-actions > .lang-menu summary{" in html
            and "min-width:108px" in html,
        "desktop actions hidden on mobile":
            re.search(r"@media\(max-width:980px\).*?\.nav-actions\{display:none\}", html, re.S)
            is not None,
        "mobile language shown in open menu":
            ".topbar.open .nav > .mobile-lang{display:block}" in html,
        "single search input id":
            html.count('id="navSearch"') == 1,
        "single search results id":
            html.count('id="navSearchResults"') == 1,
        "all eleven language choices retained":
            all(
                f'lang="{lang}"' in html
                for lang in (
                    "en", "de", "fr", "it", "es", "ja", "ko", "pl",
                    "zh-Hans", "zh-Hant", "pt-BR",
                )
            ),
    }

    for label, passed in checks.items():
        if not passed:
            errors.append(label)

    print(f"Checks passed: {len(checks) - len(errors)}/{len(checks)}")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print("ERROR", error)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
