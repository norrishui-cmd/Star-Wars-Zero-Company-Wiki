#!/usr/bin/env python3
"""Build sitemaps from canonical, indexable HTML files only."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

from configure_adsense import main as configure_adsense

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "seo-index-policy.json").read_text())
SITE = POLICY["site"].rstrip("/")


def is_draft_leaf(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    if relative.as_posix() in POLICY.get("approved_draft_routes", []):
        return False
    return len(relative.parts) > 1 and relative.parts[0] in POLICY["draft_leaf_directories"] and path.name != "index.html"


def url_for(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return SITE + "/"
    if relative.endswith("/index.html"):
        return SITE + "/" + relative[:-10]
    return SITE + "/" + relative


def indexable_pages():
    for path in sorted(ROOT.rglob("*.html")):
        if "tools" in path.parts or is_draft_leaf(path):
            continue
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        if re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', text, re.I):
            continue
        yield path


def main() -> None:
    today = date.today().isoformat()
    pages = list(indexable_pages())
    urls = [(url_for(path), today, "1.0" if path == ROOT / "index.html" else "0.8" if path.name == "index.html" else "0.7") for path in pages]
    body = "\n".join(f"  <url><loc>{escape(url)}</loc><lastmod>{modified}</lastmod><priority>{priority}</priority></url>" for url, modified, priority in urls)
    urlset = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'
    (ROOT / "sitemap-pages.xml").write_text(urlset, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(urlset, encoding="utf-8")
    index = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>{SITE}/sitemap-pages.xml</loc><lastmod>{today}</lastmod></sitemap>
</sitemapindex>
'''
    (ROOT / "sitemap-index.xml").write_text(index, encoding="utf-8")
    (ROOT / "sitemap.txt").write_text("\n".join(url for url, _, _ in urls) + "\n", encoding="utf-8")

    groups = {}
    for path, (url, _, _) in zip(pages, urls):
        relative = path.relative_to(ROOT)
        group = "Home" if len(relative.parts) == 1 else relative.parts[0].replace("-", " ").title()
        label = "Home" if path == ROOT / "index.html" else path.stem.replace("-", " ").title()
        groups.setdefault(group, []).append((url.removeprefix(SITE), label))
    sections = []
    for group, links in sorted(groups.items()):
        items = "".join(f'<a href="{escape(url)}">{escape(label)}</a>' for url, label in links)
        sections.append(f'<section><h2>{escape(group)} <span>{len(links)}</span></h2><div class="links">{items}</div></section>')
    html_map = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HTML Sitemap | Star Wars Zero Company Wiki</title><meta name="description" content="Browse all quality-approved Star Wars Zero Company Wiki pages by topic."><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}/sitemap.html"><style>body{{margin:0;background:#071016;color:#edf7ff;font:16px/1.6 system-ui}}main{{max-width:1100px;margin:auto;padding:42px 22px}}a{{color:#36e0ce;text-decoration:none}}h1{{font-size:clamp(34px,6vw,58px)}}h2{{border-left:4px solid #36e0ce;padding-left:12px}}h2 span{{color:#9db0bd;font-size:14px}}section{{border:1px solid #284050;background:#0d1922;padding:20px;margin:18px 0;border-radius:8px}}.links{{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:9px 16px}}</style></head><body><main><p><a href="/">← Home</a></p><h1>HTML Sitemap</h1><p>Quality-approved, canonical pages included in the current XML sitemap.</p>{''.join(sections)}</main></body></html>'''
    (ROOT / "sitemap.html").write_text(html_map, encoding="utf-8")
    # sitemap.html is regenerated above, so apply the global publisher tags last.
    configure_adsense()
    print(f"Built sitemap with {len(urls)} quality-approved URLs")


if __name__ == "__main__":
    main()
