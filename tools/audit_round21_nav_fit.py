#!/usr/bin/env python3
"""Audit the Round 21 compact navigation safeguards."""

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"


def main():
    html = INDEX.read_text(encoding="utf-8")
    checks = {
        "Round 21 CSS is present":
            "ROUND 21: compact, collision-safe desktop navigation" in html,
        "compact desktop grid":
            "grid-template-columns:minmax(210px,230px) minmax(0,1fr) minmax(238px,256px)"
            in html,
        "brand has a hard maximum":
            re.search(r"\.brand\{\s*width:100%;\s*max-width:230px;", html) is not None,
        "brand title cannot overflow":
            "text-overflow:ellipsis;" in html and "white-space:nowrap;" in html,
        "compact action columns":
            "grid-template-columns:82px minmax(150px,168px)" in html,
        "language button has fixed compact width":
            re.search(r"\.nav-actions > \.lang-menu\{width:82px\}", html) is not None,
        "search can shrink safely":
            re.search(r"\.nav-search\{\s*height:36px\}", html) is not None,
        "mid-size desktop override":
            "@media(max-width:1180px) and (min-width:981px)" in html
            and "grid-template-columns:minmax(174px,182px)" in html,
        "mid-size subtitle is hidden":
            ".brand span{display:none}" in html,
        "mobile navigation breakpoint retained":
            "@media(max-width:980px)" in html
            and ".nav-actions{display:none}" in html,
        "desktop search is retained":
            html.count('id="navSearch"') == 1
            and html.count('id="navSearchResults"') == 1,
        "all consolidated menu groups retained":
            all(f"<summary>{label}</summary>" in html for label in
                ("Database", "Guides", "Operations", "Game Info")),
    }
    failed = [label for label, passed in checks.items() if not passed]
    print(f"Checks passed: {len(checks) - len(failed)}/{len(checks)}")
    print(f"Errors: {len(failed)}")
    for label in failed:
        print("ERROR", label)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
