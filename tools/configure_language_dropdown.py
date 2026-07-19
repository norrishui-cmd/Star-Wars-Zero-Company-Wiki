#!/usr/bin/env python3
"""Install an accessible EN/DE/JA dropdown in every HTML page navigation."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

CSS = """
.lang-menu{position:relative;display:inline-block;margin-left:4px;z-index:40;font:600 14px/1.2 system-ui,-apple-system,'Segoe UI',sans-serif;color:#edf7ff}
.lang-menu summary{list-style:none;cursor:pointer;border:1px solid #365264;border-radius:7px;padding:8px 28px 8px 11px;background:#0d1922;color:#edf7ff;white-space:nowrap;position:relative}
.lang-menu summary::-webkit-details-marker{display:none}.lang-menu summary::after{content:'▾';position:absolute;right:10px;color:#36e0ce}
.lang-menu[open] summary::after{content:'▴'}.lang-options{position:absolute;right:0;top:calc(100% + 7px);min-width:154px;padding:6px;background:#0b161e;border:1px solid #365264;border-radius:8px;box-shadow:0 12px 30px rgba(0,0,0,.38)}
.lang-options a{display:block!important;padding:9px 10px!important;margin:0!important;border-radius:5px;color:#c8d8e1!important;text-decoration:none!important;white-space:nowrap;font-size:14px!important}
.lang-options a:hover,.lang-options a[aria-current="page"]{background:#132631;color:#36e0ce!important}.lang-options a[aria-current="page"]::before{content:'✓ ';color:#e9b84a}
@media(max-width:760px){.lang-menu{width:100%;margin:4px 0}.lang-menu summary{width:100%}.lang-options{position:static;margin-top:6px;width:100%}}
""".strip()


def route_for(path: Path):
    rel = path.relative_to(ROOT).as_posix()
    locale = "en"
    if rel.startswith("de/"):
        locale, rel = "de", rel[3:]
    elif rel.startswith("ja/"):
        locale, rel = "ja", rel[3:]
    if rel == "index.html":
        route = ""
    else:
        route = rel
    return locale, route


def href_for(locale, route):
    if locale == "en":
        path = ROOT / (route or "index.html")
        if not path.exists():
            return "/"
        if route == "":
            return "/"
        return "/" + (route[:-10] if route.endswith("index.html") else route)
    path = ROOT / locale / (route or "index.html")
    if not path.exists():
        return f"/{locale}/"
    if route == "":
        return f"/{locale}/"
    return f"/{locale}/" + (route[:-10] if route.endswith("index.html") else route)


def menu(current, route):
    labels = {"en": "English", "de": "Deutsch", "ja": "日本語"}
    links = []
    for locale in ("en", "de", "ja"):
        active = ' aria-current="page"' if locale == current else ""
        links.append(f'<a href="{href_for(locale, route)}" lang="{locale}"{active}>{labels[locale]}</a>')
    return (f'<details class="lang-menu"><summary aria-label="Choose language / Sprache wählen / 言語を選択">'
            f'{labels[current]}</summary><div class="lang-options">{"".join(links)}</div></details>')


def main():
    changed = 0
    nav_count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if "tools" in path.parts:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        original = text
        current, route = route_for(path)
        text = re.sub(r'<details class="lang-menu">.*?</details>', '', text, flags=re.S)
        text = text.replace('<a href="/de/" lang="de">Deutsch</a>', '')
        text = text.replace('<a href="/ja/" lang="ja">日本語</a>', '')
        if ".lang-menu{" not in text:
            if "</style>" in text:
                text = text.replace("</style>", CSS + "</style>", 1)
            else:
                text = text.replace("</head>", f"<style>{CSS}</style></head>", 1)
        dropdown = menu(current, route)
        nav_match = re.search(r"</nav>", text, re.I)
        if nav_match:
            text = text[:nav_match.start()] + dropdown + text[nav_match.start():]
            nav_count += 1
        else:
            text = text.replace("<body>", f'<body><nav class="wrap" aria-label="Language navigation">{dropdown}</nav>', 1)
        if text != original:
            path.write_text(text, encoding="utf-8")
            changed += 1
    print(f"Language dropdown configured on {changed} HTML pages ({nav_count} existing navs)")


if __name__ == "__main__":
    main()
