#!/usr/bin/env python3
"""Build sitemaps from canonical, indexable HTML files only."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "seo-index-policy.json").read_text())
SITE = POLICY["site"].rstrip("/")


def is_draft_leaf(path: Path) -> bool:
    relative = path.relative_to(ROOT)
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
    urls = [(url_for(path), today, "1.0" if path == ROOT / "index.html" else "0.8" if path.name == "index.html" else "0.7") for path in indexable_pages()]
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
    print(f"Built sitemap with {len(urls)} quality-approved URLs")


if __name__ == "__main__":
    main()
