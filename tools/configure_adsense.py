#!/usr/bin/env python3
"""Apply one consistent AdSense ownership configuration to every HTML page."""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
PUBLISHER_ID = "ca-pub-9505220977121599"
META = f'<meta name="google-adsense-account" content="{PUBLISHER_ID}">'
SCRIPT = (
    '<script async src="https://pagead2.googlesyndication.com/pagead/js/'
    f'adsbygoogle.js?client={PUBLISHER_ID}" crossorigin="anonymous"></script>'
)


def configure(path: Path) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    # Make the operation repeatable: remove any existing account meta or loader first.
    text = re.sub(
        r'\s*<meta\s+name=["\']google-adsense-account["\'][^>]*>',
        "",
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\s*<script[^>]+pagead2\.googlesyndication\.com/pagead/js/adsbygoogle\.js[^>]*>\s*</script>',
        "",
        text,
        flags=re.I,
    )
    if "</head>" not in text.lower():
        raise ValueError(f"Missing </head>: {path.relative_to(ROOT)}")
    text = re.sub(r"</head>", f"{META}\n{SCRIPT}\n</head>", text, count=1, flags=re.I)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    pages = sorted(ROOT.rglob("*.html"))
    for page in pages:
        configure(page)
    (ROOT / "ads.txt").write_text(
        "google.com, pub-9505220977121599, DIRECT, f08c47fec0942fa0\n",
        encoding="utf-8",
    )
    print(f"Configured AdSense ownership on {len(pages)} HTML pages and wrote /ads.txt")


if __name__ == "__main__":
    main()
