#!/usr/bin/env python3
"""Audit the Round 19 navigation search replacement."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def main():
    html = INDEX.read_text(encoding="utf-8")
    errors = []

    checks = {
        "navigation search form": 'class="nav-search"' in html,
        "accessible search role": 'role="search"' in html,
        "search input": 'id="navSearch"' in html,
        "suggestion container": 'id="navSearchResults"' in html,
        "search submit handler": "function runNavSearch(event)" in html,
        "live suggestion handler": "function renderNavSearch()" in html,
        "search CSS marker": "/* ROUND 19: navigation search */" in html,
        "mobile rule": re.search(r"@media\(max-width:980px\)\{\s*\.nav-search\{display:none\}", html) is not None,
        "old status removed": 'id="tminus"' not in html and 'id="tdays"' not in html,
        "single-row navigation retained": "/* ROUND 18: one-row consolidated navigation */" in html,
        "homepage search retained": 'id="search"' in html and "function runSearch()" in html,
        "release countdown retained": 'id="cdDays"' in html and "function countdown()" in html,
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
