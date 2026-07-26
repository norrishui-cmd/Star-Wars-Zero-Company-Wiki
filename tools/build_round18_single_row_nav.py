#!/usr/bin/env python3
"""Round 18: consolidate the homepage navigation into one desktop row."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

NAV = """<nav class="nav" id="nav">
      <a class="nav-direct" data-route="home" href="#home" onclick="go('home')">Home</a>
      <details class="site-menu">
        <summary>Database</summary>
        <div class="site-menu-panel">
          <a href="/database/"><strong>Database Overview</strong><span>Confirmed game data</span></a>
          <a href="/operatives/">Operatives</a>
          <a href="/classes/">Specializations</a>
          <a href="/builds/">Loadouts</a>
          <a href="/hostiles/">Hostiles</a>
        </div>
      </details>
      <details class="site-menu">
        <summary>Guides</summary>
        <div class="site-menu-panel">
          <a href="/guides/"><strong>All Guides</strong><span>Walkthroughs and tactics</span></a>
          <a href="/start-here/">Start Here</a>
          <a href="/confirmed/">Confirmed Guides</a>
          <a href="/official-systems/">Official Systems</a>
          <a href="/systems/">Systems</a>
        </div>
      </details>
      <details class="site-menu">
        <summary>Operations</summary>
        <div class="site-menu-panel">
          <a href="/operations/"><strong>Operations Hub</strong><span>Mission planning</span></a>
          <a href="/planner/">Planner</a>
          <a data-route="muster" href="#muster" onclick="go('muster')">Muster Board</a>
          <a href="/facilities/">The Den</a>
        </div>
      </details>
      <details class="site-menu">
        <summary>Game Info</summary>
        <div class="site-menu-panel">
          <a href="/official/"><strong>Official Info</strong><span>Release and platforms</span></a>
          <a href="/lore/">Story &amp; Lore</a>
          <a href="/media/">Media</a>
          <a href="/content-map/">Content Map</a>
          <a href="/about/">About</a>
        </div>
      </details>
      <a class="nav-direct" href="/news/">News</a>
      <a class="nav-direct" href="/questions/">FAQ</a>
      {language}
    </nav>"""

CSS = r"""
/* ROUND 18: one-row consolidated navigation */
.topbar-inner{
  grid-template-columns:minmax(260px,auto) minmax(0,1fr) auto;
  grid-template-areas:"brand nav status";
  gap:8px 14px;
  min-height:72px;
}
.nav{
  align-items:center;
  justify-content:center;
  flex-wrap:nowrap;
  gap:3px;
  padding-left:0;
}
.nav > .nav-direct,
.site-menu > summary{
  min-height:38px;
  display:flex;
  align-items:center;
  border:1px solid transparent;
  border-radius:5px;
  color:var(--muted);
  cursor:pointer;
  font-family:var(--fd);
  font-size:clamp(11px,.82vw,13px);
  font-weight:650;
  letter-spacing:.035em;
  line-height:1;
  list-style:none;
  padding:0 9px;
  position:relative;
  text-decoration:none;
  white-space:nowrap;
}
.site-menu > summary{padding-right:25px}
.site-menu > summary::-webkit-details-marker{display:none}
.site-menu > summary::after{
  content:"";
  position:absolute;
  right:9px;
  top:50%;
  width:5px;
  height:5px;
  border-right:1.5px solid var(--teal);
  border-bottom:1.5px solid var(--teal);
  transform:translateY(-65%) rotate(45deg);
  transition:transform .16s ease;
}
.site-menu[open] > summary::after{transform:translateY(-30%) rotate(225deg)}
.nav > .nav-direct:hover,
.site-menu > summary:hover,
.site-menu[open] > summary{
  color:var(--text);
  background:rgba(255,255,255,.04);
  border-color:var(--line);
  text-decoration:none;
}
.site-menu{position:relative}
.site-menu-panel{
  position:absolute;
  z-index:80;
  top:calc(100% + 8px);
  left:0;
  width:220px;
  padding:8px;
  border:1px solid var(--line-2);
  border-radius:7px;
  background:rgba(8,11,15,.99);
  box-shadow:0 22px 55px -24px rgba(0,0,0,.95);
}
.site-menu-panel::before{
  content:"";
  position:absolute;
  left:18px;
  top:-5px;
  width:8px;
  height:8px;
  border-left:1px solid var(--line-2);
  border-top:1px solid var(--line-2);
  background:#080b0f;
  transform:rotate(45deg);
}
.site-menu-panel a{
  display:block;
  padding:9px 10px;
  border-radius:4px;
  color:var(--muted);
  font-family:var(--fd);
  font-size:12px;
  line-height:1.25;
  text-decoration:none;
}
.site-menu-panel a:hover{background:rgba(52,224,196,.08);color:var(--teal)}
.site-menu-panel a strong{display:block;color:var(--text);font-weight:700}
.site-menu-panel a span{
  display:block;
  margin-top:3px;
  color:var(--faint);
  font-family:var(--fm);
  font-size:9px;
  letter-spacing:.05em;
  text-transform:uppercase;
}
.nav > .lang-menu{flex:0 0 auto;margin-left:3px}
.nav > .lang-menu summary{min-height:38px;padding-top:0;padding-bottom:0;display:flex;align-items:center}
@media(max-width:1180px) and (min-width:981px){
  .topbar-inner{
    grid-template-columns:minmax(220px,auto) minmax(0,1fr) auto;
    grid-template-areas:"brand nav status";
  }
  .brand span{display:none}
  .brand b{font-size:16px}
  .nav > .nav-direct,.site-menu > summary{padding-left:7px;padding-right:7px}
  .site-menu > summary{padding-right:21px}
  .site-menu > summary::after{right:7px}
  .tminus{font-size:9px;gap:6px}
}
@media(max-width:980px){
  .nav,.tminus{display:none}
  .burger{display:block}
  .topbar-inner{
    grid-template-columns:1fr auto;
    grid-template-areas:"brand status";
  }
  .topbar.open .nav{
    display:flex;
    position:absolute;
    top:100%;
    left:0;
    right:0;
    max-height:calc(100vh - 72px);
    overflow:auto;
    flex-direction:column;
    align-items:stretch;
    background:var(--void);
    border-bottom:1px solid var(--line);
    padding:10px 18px 16px;
  }
  .topbar.open .nav > .nav-direct,
  .topbar.open .site-menu > summary{width:100%;padding:12px 8px}
  .site-menu{width:100%}
  .site-menu-panel{
    position:static;
    width:100%;
    margin:0 0 6px;
    box-shadow:none;
    background:rgba(255,255,255,.02);
  }
  .site-menu-panel::before{display:none}
  .nav > .lang-menu{width:100%;margin:4px 0 0}
}
"""

JS = r"""
// ROUND 18: keep only one click-open navigation group at a time.
document.querySelectorAll('.site-menu').forEach(menu=>{
  menu.addEventListener('toggle',()=>{
    if(!menu.open)return;
    document.querySelectorAll('.site-menu[open]').forEach(other=>{
      if(other!==menu)other.removeAttribute('open');
    });
  });
});
document.addEventListener('click',event=>{
  if(!event.target.closest('.site-menu')){
    document.querySelectorAll('.site-menu[open]').forEach(menu=>menu.removeAttribute('open'));
  }
});
"""


def main():
    html = INDEX.read_text(encoding="utf-8")
    language_match = re.search(
        r'(<details class="lang-menu">.*?</details>)</nav>',
        html,
        flags=re.S,
    )
    if not language_match:
        raise SystemExit("Language dropdown not found in homepage navigation.")
    language = language_match.group(1)

    html, count = re.subn(
        r'<nav class="nav" id="nav">.*?</nav>',
        NAV.format(language=language),
        html,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise SystemExit(f"Expected one homepage navigation, changed {count}.")

    html = re.sub(
        r'\n?/\* ROUND 18: one-row consolidated navigation \*/.*?(?=</style>)',
        "",
        html,
        flags=re.S,
    )
    html = html.replace("</style>", CSS + "\n</style>", 1)

    html = re.sub(
        r'\n?// ROUND 18: keep only one click-open navigation group at a time\..*?(?=</script>)',
        "",
        html,
        flags=re.S,
    )
    html = html.replace("</script>\n</body>", JS + "\n</script>\n</body>", 1)
    INDEX.write_text(html, encoding="utf-8")
    print("Round 18 homepage navigation consolidated into one desktop row.")


if __name__ == "__main__":
    main()
