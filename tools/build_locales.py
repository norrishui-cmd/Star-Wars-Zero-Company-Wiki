#!/usr/bin/env python3
"""Build the quality-approved German and Japanese launch-intent layer."""

from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
EA_GAMEPLAY = "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"
EA_BUY = "https://www.ea.com/games/starwars/zero-company/buy"
STEAM = "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/"

ROUTES = {
    "home": "",
    "release": "official/release-date.html",
    "platforms": "official/platforms.html",
    "languages": "official/languages.html",
    "overview": "confirmed/overview.html",
    "classes": "classes/index.html",
}

CLASSES = {
    "assault": {
        "de": ("Sturm", "Bewegt sich aggressiv, um Ziele hinter Deckung auszuschalten.", "Frontkämpfer", "mittlere bis kurze Distanz"),
        "ja": ("アサルト", "積極的に位置を変え、遮蔽物に隠れた敵を倒す役割です。", "前線戦闘", "中～近距離"),
    },
    "gunslinger": {
        "de": ("Revolverheld", "Bekämpft mehrere Gegner und setzt dabei auf Mobilität und Präzision.", "mobiler Schütze", "kurze bis mittlere Distanz"),
        "ja": ("ガンスリンガー", "機動力と精度を生かして複数の敵に対応します。", "機動射撃", "近～中距離"),
    },
    "heavy": {
        "de": ("Schwer", "Unterdrückt Gegner mit hoher Feuerkraft und hält gefährliche Bereiche.", "Feuerunterstützung", "mittlere Distanz"),
        "ja": ("ヘビー", "高い火力で敵を制圧し、危険なエリアを押さえます。", "火力支援", "中距離"),
    },
    "medic": {
        "de": ("Sanitäter", "Hält das Team einsatzfähig und stabilisiert verwundete Verbündete.", "Heilung und Schutz", "hintere bis mittlere Linie"),
        "ja": ("メディック", "負傷した仲間を支援し、部隊の戦闘継続能力を保ちます。", "回復・防護", "後方～中距離"),
    },
    "scoundrel": {
        "de": ("Schurke", "Manipuliert den Kampf mit Tricks und nutzt günstige Gelegenheiten.", "Kontrolle und Tricks", "situationsabhängig"),
        "ja": ("スカウンドレル", "トリックで戦況を動かし、有利な機会を利用します。", "妨害・トリック", "状況依存"),
    },
    "scout": {
        "de": ("Späher", "Erkundet das Gefechtsfeld und schafft Informationen für das Team.", "Aufklärung", "mittlere bis große Distanz"),
        "ja": ("スカウト", "戦場を偵察し、部隊が判断するための情報を作ります。", "偵察", "中～遠距離"),
    },
    "sharpshooter": {
        "de": ("Scharfschütze", "Schaltet wichtige Ziele aus großer Entfernung präzise aus.", "Fernkampf-Schaden", "große Distanz"),
        "ja": ("シャープシューター", "遠距離から重要な標的を正確に排除します。", "長距離攻撃", "遠距離"),
    },
    "soldier": {
        "de": ("Soldat", "Bietet verlässliche, flexible Kampfkraft in unterschiedlichen Situationen.", "vielseitiger Kämpfer", "mittlere Distanz"),
        "ja": ("ソルジャー", "さまざまな状況に対応できる、安定した戦闘力を提供します。", "汎用戦闘", "中距離"),
    },
}

COPY = {
"de": {
 "lang":"de", "label":"Deutsch", "site":"Star Wars Zero Company Wiki auf Deutsch",
 "nav":[("/de/","Start"),("/de/classes/","Spezialisierungen"),("/de/confirmed/overview.html","Spielübersicht"),("/de/official/release-date.html","Release"),("/de/official/languages.html","Sprachen")],
 "home": ("Star Wars Zero Company Wiki – Deutscher Guide", "Deutscher Star Wars Zero Company Guide mit Release-Zeit, Plattformen, Sprachen, Spielsystemen und den acht offiziell bestätigten Spezialisierungen."),
 "release": ("Star Wars Zero Company Release: Datum und Uhrzeit", "Star Wars Zero Company erscheint am 27. August 2026 um 15:00 UTC für PC, PlayStation 5 und Xbox Series X|S."),
 "platforms": ("Star Wars Zero Company Plattformen: PC, PS5 und Xbox", "Bestätigte Plattformen für Star Wars Zero Company: PC über Steam und Epic Games Store, PlayStation 5 und Xbox Series X|S."),
 "languages": ("Star Wars Zero Company Sprachen und deutsche Synchro", "Star Wars Zero Company unterstützt 11 Textsprachen. Vollständige Sprachausgabe ist für Deutsch und Englisch bestätigt."),
 "overview": ("Star Wars Zero Company Gameplay: Deutscher Überblick", "Star Wars Zero Company ist ein Einzelspieler-Runden-Taktikspiel mit drei Aktionspunkten pro Operator, Deckung, Advantage, Basisbau und Permadeath."),
 "classes": ("Alle 8 Spezialisierungen in Star Wars Zero Company", "Die acht offiziellen Standard-Spezialisierungen: Sturm, Revolverheld, Schwer, Sanitäter, Schurke, Späher, Scharfschütze und Soldat."),
},
"ja": {
 "lang":"ja", "label":"日本語", "site":"スター・ウォーズ ゼロ・カンパニー攻略Wiki",
 "nav":[("/ja/","ホーム"),("/ja/classes/","専門クラス"),("/ja/confirmed/overview.html","ゲーム概要"),("/ja/official/release-date.html","発売日"),("/ja/official/languages.html","対応言語")],
 "home": ("Star Wars Zero Company 日本語攻略Wiki", "『Star Wars Zero Company』の日本語攻略ガイド。発売日時、対応機種、対応言語、戦闘システム、公式発表済みの8つの専門クラスを解説します。"),
 "release": ("Star Wars Zero Company 発売日・日本での発売時刻", "『Star Wars Zero Company』は2026年8月27日15:00 UTC発売予定。日本時間では2026年8月28日午前0時に相当します。"),
 "platforms": ("Star Wars Zero Company 対応機種：PC・PS5・Xbox", "対応機種はPC（Steam／Epic Games Store）、PlayStation 5、Xbox Series X|Sです。PS4、Xbox One、Nintendo Switch版は発表されていません。"),
 "languages": ("Star Wars Zero Company 対応言語・日本語対応", "『Star Wars Zero Company』は日本語のインターフェースと字幕に対応予定です。フル音声は英語とドイツ語のみ発表されています。"),
 "overview": ("Star Wars Zero Company ゲームシステム概要", "本作は一人用ターン制タクティクス。各オペレーターは1ターン3 APを使い、遮蔽物、Advantage、拠点育成、負傷と永久死亡を管理します。"),
 "classes": ("Star Wars Zero Company 全8専門クラス一覧", "公式発表済みの標準専門クラスは、アサルト、ガンスリンガー、ヘビー、メディック、スカウンドレル、スカウト、シャープシューター、ソルジャーの8種類です。"),
}}

STYLE = """:root{--bg:#071016;--panel:#0d1922;--line:#284050;--text:#edf7ff;--muted:#a9bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:#071016;color:var(--text);font:16px/1.72 system-ui,-apple-system,'Segoe UI',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:64px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;flex-wrap:wrap}nav a{color:var(--muted);font-size:14px}.hero{padding:52px 0 28px;border-bottom:1px solid var(--line)}h1{font-size:clamp(34px,6vw,56px);line-height:1.1;margin:12px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#c9d8e0;max-width:850px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:20px;margin:15px 0;color:var(--text)}.pill{display:inline-block;border:1px solid #3c625f;padding:5px 9px;margin:5px 7px 0 0;color:var(--teal);font-size:12px}.muted,.source{color:var(--muted);font-size:14px}table{width:100%;border-collapse:collapse}th,td{border:1px solid var(--line);padding:11px;text-align:left;vertical-align:top}th{color:var(--gold)}li{margin:8px 0}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){nav{margin-left:0}.top .wrap{padding-top:10px;padding-bottom:10px}}"""

def lang_route(locale, route):
    if route == "": return f"/{locale}/"
    if route.endswith("index.html"): return f"/{locale}/{route[:-10]}"
    return f"/{locale}/{route}"

def english_route(route):
    if route == "": return "/"
    if route.endswith("index.html"): return "/" + route[:-10]
    return "/" + route

def head(locale, route, title, desc, page_type="Article"):
    local = lang_route(locale, route)
    en = english_route(route)
    links = [f'<link rel="alternate" hreflang="en" href="{SITE}{en}">',
             f'<link rel="alternate" hreflang="de" href="{SITE}{lang_route("de",route)}">',
             f'<link rel="alternate" hreflang="ja" href="{SITE}{lang_route("ja",route)}">',
             f'<link rel="alternate" hreflang="x-default" href="{SITE}{en}">']
    schema = {"@context":"https://schema.org","@type":page_type,"headline":title,"description":desc,"url":SITE+local,"inLanguage":COPY[locale]["lang"],"dateModified":"2026-07-18","isPartOf":{"@type":"WebSite","name":COPY[locale]["site"],"url":SITE+f'/{locale}/'}}
    return f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}{local}">{"".join(links)}<link rel="icon" href="/favicon.ico"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><style>{STYLE}</style></head>'

def chrome(locale, route, title, desc, body, page_type="Article"):
    nav = ''.join(f'<a href="{u}">{escape(t)}</a>' for u,t in COPY[locale]["nav"])
    switch = f'<a href="{english_route(route)}">English</a> · <a href="{lang_route("de",route)}">Deutsch</a> · <a href="{lang_route("ja",route)}">日本語</a>'
    return head(locale,route,title,desc,page_type)+f'<body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">{COPY[locale]["site"]}</a><nav>{nav}</nav></div></header><main class="wrap">{body}</main><footer><div class="wrap">{switch}<br>{"Inoffizieller Spieler-Guide" if locale=="de" else "非公式プレイヤーガイド"} · <a href="/about/sources-and-citations.html">Sources</a></div></footer></body></html>'

def source(locale, buy=False):
    label = "Offizielle Quellen und Prüfstand" if locale=="de" else "公式情報源と確認状況"
    note = "Zuletzt anhand der offiziellen Angaben geprüft: 18. Juli 2026. Details können sich bis zum Release ändern." if locale=="de" else "公式情報に基づく最終確認日：2026年7月18日。発売までに仕様が変更される可能性があります。"
    url = EA_BUY if buy else EA_GAMEPLAY
    return f'<section class="block"><h2>{label}</h2><p>{note}</p><p class="source"><a href="{url}" rel="nofollow">Electronic Arts</a></p></section>'

def write(locale, route, key, body, page_type="Article"):
    title, desc = COPY[locale][key]
    path = ROOT / locale / route if route else ROOT / locale / "index.html"
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(chrome(locale,route,title,desc,body,page_type),encoding="utf-8")

def build_core(locale):
    de = locale == "de"
    title, desc = COPY[locale]["home"]
    intro = ("Diese deutschsprachige Startseite bündelt nur Informationen, die von EA oder den offiziellen Store-Seiten bestätigt sind. Sie ist als schneller Einstieg vor dem Release gedacht; konkrete Builds, Missionslösungen und Werte werden erst nach Prüfung der veröffentlichten Spielversion ergänzt."
             if de else "この日本語ページでは、EAおよび公式ストアで確認できる情報を中心に掲載しています。発売前の段階で未確認のビルド、ミッション手順、数値を事実として扱わず、製品版で検証した後に追加します。")
    cards = ''.join(f'<a class="card" href="/{locale}/{r}"><strong>{escape(COPY[locale][k][0])}</strong><br><span class="muted">{escape(COPY[locale][k][1])}</span></a>' for k,r in [("release",ROUTES["release"]),("platforms",ROUTES["platforms"]),("languages",ROUTES["languages"]),("overview",ROUTES["overview"]),("classes","classes/")])
    body=f'<section class="hero"><span class="pill">{COPY[locale]["label"]}</span><h1>{escape(title)}</h1><p class="lead">{escape(desc)}</p></section><section class="block"><h2>{"Schnelleinstieg" if de else "クイックスタート"}</h2><p>{intro}</p></section><section><h2>{"Bestätigte Guides" if de else "確認済みガイド"}</h2><div class="grid">{cards}</div></section>{source(locale)}'
    write(locale,"","home",body,"WebPage")

    if de:
      release = '<section class="hero"><h1>Release-Datum und Uhrzeit</h1><p class="lead"><strong>Star Wars Zero Company erscheint am 27. August 2026 um 15:00 UTC.</strong></p></section><section class="block"><h2>Uhrzeit im deutschsprachigen Raum</h2><p>15:00 UTC entspricht am 27. August 2026 um 17:00 Uhr in Deutschland, Österreich und der Schweiz, solange dort die mitteleuropäische Sommerzeit gilt. Die Store-Seite ist die maßgebliche Quelle, falls sich der Freischaltzeitpunkt ändert.</p><table><tr><th>Region</th><th>Zeit</th></tr><tr><td>UTC</td><td>27. August, 15:00</td></tr><tr><td>Deutschland / Österreich / Schweiz</td><td>27. August, 17:00 MESZ</td></tr></table></section><section class="block"><h2>Plattformen zum Start</h2><p>Der Termin gilt für PC, PlayStation 5 und Xbox Series X|S. Eine Version für PS4, Xbox One oder Nintendo Switch wurde nicht angekündigt.</p></section>'
      platforms = '<section class="hero"><h1>Bestätigte Plattformen</h1><p class="lead">Zum Start erscheint das Spiel für PC, PlayStation 5 und Xbox Series X|S.</p></section><section class="block"><h2>Wo kann man spielen?</h2><table><tr><th>Plattform</th><th>Status</th></tr><tr><td>PC</td><td>Bestätigt über Steam und Epic Games Store</td></tr><tr><td>PlayStation 5</td><td>Bestätigt</td></tr><tr><td>Xbox Series X|S</td><td>Bestätigt</td></tr><tr><td>PS4 / Xbox One / Switch</td><td>Nicht angekündigt</td></tr></table><p>Die PC-Systemanforderungen nennen 50 GB Speicher und Windows 10/11 in 64 Bit. Eine Online-Verbindung wird auf der EA-Seite nicht als Voraussetzung angegeben.</p></section><section class="block"><h2>Einzelspieler</h2><p>EA beschreibt Zero Company als Einzelspieler-Runden-Taktikspiel. Koop- oder Mehrspieler-Modi wurden nicht angekündigt.</p></section>'
      languages = '<section class="hero"><h1>Sprachen und deutsche Sprachausgabe</h1><p class="lead">Es sind 11 Sprachen für Oberfläche und Untertitel angekündigt. Deutsch und Englisch erhalten vollständige Sprachausgabe.</p></section><section class="block"><h2>Alle unterstützten Sprachen</h2><p>Englisch, Deutsch, Französisch, Italienisch, Spanisch (Spanien), Japanisch, Koreanisch, Polnisch, Chinesisch (vereinfacht), Chinesisch (traditionell) und Portugiesisch (Brasilien).</p><table><tr><th>Funktion</th><th>Deutsch</th></tr><tr><td>Benutzeroberfläche</td><td>Ja</td></tr><tr><td>Untertitel</td><td>Ja</td></tr><tr><td>Vollständige Sprachausgabe</td><td>Ja</td></tr></table><p>Die detaillierte Zuordnung stammt aus den offiziellen Store-Angaben. Die allgemeine EA-Kaufseite listet dieselben elf Sprachen, trennt Text und Audio aber nicht.</p></section>'
      overview = '<section class="hero"><h1>Gameplay im Überblick</h1><p class="lead">Ein storybasiertes Einzelspieler-Taktikspiel in der Endphase der Klonkriege.</p></section><section class="block"><h2>Kampfsystem</h2><p>Jeder Operator verfügt pro Runde über drei Aktionspunkte (AP). Bewegung, Angriffe und Fähigkeiten konkurrieren um diese Punkte. Angriffe erzeugen die gemeinsame Ressource Advantage bis zu einem Maximum von zehn; sie kann für mächtige Optionen wie Ultimates genutzt werden.</p></section><section class="block"><h2>Kampagne und The Den</h2><p>Zwischen den Einsätzen wird die Basis „The Den“ ausgebaut. Einrichtungen unterstützen Personal, Ausrüstung, medizinische Versorgung und weitere Kampagnenfunktionen. Missionen laufen in Zyklen, sodass die Auswahl eines Einsatzes Auswirkungen auf andere Möglichkeiten haben kann.</p></section><section class="block"><h2>Verletzungen und Permadeath</h2><p>Auf dem Standard-Schwierigkeitsgrad führt die dritte Verletzung eines Operators zum dauerhaften Tod. Das betrifft laut EA auch handlungsrelevante Figuren. Die genaue Wirkung anderer Schwierigkeitsgrade wird nach Veröffentlichung geprüft.</p></section>'
    else:
      release = '<section class="hero"><h1>発売日と日本での解禁時刻</h1><p class="lead"><strong>発売予定は2026年8月27日15:00 UTCです。日本標準時では8月28日午前0時に相当します。</strong></p></section><section class="block"><h2>地域別の時刻</h2><table><tr><th>地域</th><th>発売予定時刻</th></tr><tr><td>UTC</td><td>8月27日 15:00</td></tr><tr><td>日本（JST）</td><td>8月28日 0:00</td></tr></table><p>これはEA購入ページの世界同時刻を日本時間へ換算したものです。ストア側の表示やプリロード開始時刻は変更される可能性があるため、購入したプラットフォームでも確認してください。</p></section><section class="block"><h2>発売対象機種</h2><p>PC、PlayStation 5、Xbox Series X|Sで発売予定です。PS4、Xbox One、Nintendo Switch版は現時点で発表されていません。</p></section>'
      platforms = '<section class="hero"><h1>対応機種</h1><p class="lead">PC、PlayStation 5、Xbox Series X|Sで発売予定です。</p></section><section class="block"><h2>機種別の対応状況</h2><table><tr><th>機種</th><th>状況</th></tr><tr><td>PC</td><td>SteamおよびEpic Games Storeで発売予定</td></tr><tr><td>PlayStation 5</td><td>対応</td></tr><tr><td>Xbox Series X|S</td><td>対応</td></tr><tr><td>PS4 / Xbox One / Nintendo Switch</td><td>未発表</td></tr></table><p>PC版の公式要件では、64ビット版Windows 10/11と50 GBの空き容量が案内されています。EA購入ページではオンライン接続が必須要件として記載されていません。</p></section><section class="block"><h2>一人用ゲーム</h2><p>EAは本作を一人用ターン制タクティクスゲームと説明しています。協力プレイや対戦マルチプレイは発表されていません。</p></section>'
      languages = '<section class="hero"><h1>対応言語と日本語対応</h1><p class="lead">日本語のインターフェースと字幕に対応予定です。日本語フル音声は発表されていません。</p></section><section class="block"><h2>発表済みの11言語</h2><p>英語、ドイツ語、フランス語、イタリア語、スペイン語（スペイン）、日本語、韓国語、ポーランド語、簡体字中国語、繁体字中国語、ポルトガル語（ブラジル）です。</p><table><tr><th>機能</th><th>日本語</th></tr><tr><td>インターフェース</td><td>対応</td></tr><tr><td>字幕</td><td>対応</td></tr><tr><td>フル音声</td><td>非対応（発表済みは英語・ドイツ語）</td></tr></table><p>EA購入ページは11言語を掲載し、SteamとEpic Games Storeはテキストと音声の内訳を示しています。</p></section>'
      overview = '<section class="hero"><h1>ゲームシステム概要</h1><p class="lead">クローン戦争末期を舞台にした、物語重視の一人用ターン制タクティクスゲームです。</p></section><section class="block"><h2>戦闘と3 AP</h2><p>各オペレーターは1ターンに3アクションポイント（AP）を持ち、移動、攻撃、アビリティに使います。攻撃すると部隊共有のAdvantageが増え、最大10まで蓄積可能です。これは各専門クラスのUltimateなど、強力な選択肢に利用します。</p></section><section class="block"><h2>キャンペーンと拠点The Den</h2><p>任務の合間には拠点「The Den」の施設を拡張します。人員、装備、医療などの施設が部隊運営を支えます。ミッションはCycle単位で進み、どの任務を選ぶかが他の機会に影響する設計です。</p></section><section class="block"><h2>負傷と永久死亡</h2><p>標準難易度では、オペレーターが3回目の負傷を受けると永久死亡します。EAによれば、物語に登場する固有キャラクターも対象です。他難易度での詳細は発売後に検証します。</p></section>'
    for key,body,buy in [("release",release,True),("platforms",platforms,True),("languages",languages,True),("overview",overview,False)]:
      write(locale,ROUTES[key],key,body+source(locale,buy))

def build_classes(locale):
    de = locale == "de"
    cards=''.join(f'<a class="card" href="/{locale}/classes/{slug}.html"><strong>{escape(data[locale][0])}</strong><br><span class="muted">{escape(data[locale][1])}</span></a>' for slug,data in CLASSES.items())
    intro = ('EA hat acht Standard-Spezialisierungen bestätigt. Eine Spezialisierung besitzt eine Ultimate, eine Standardfähigkeit und eine passive Fähigkeit. Die Namen, AP-Kosten und Zahlenwerte vieler Fähigkeiten sind noch nicht offiziell veröffentlicht.' if de else 'EAは8つの標準専門クラスを発表しています。各クラスにはUltimate、Standard Ability、Passiveがありますが、多くの名称、APコスト、数値はまだ公式公開されていません。')
    body=f'<section class="hero"><h1>{escape(COPY[locale]["classes"][0])}</h1><p class="lead">{escape(COPY[locale]["classes"][1])}</p></section><section class="block"><h2>{"Bestätigtes System" if de else "確認済みの仕組み"}</h2><p>{intro}</p></section><section><h2>{"Spezialisierungen" if de else "専門クラス一覧"}</h2><div class="grid">{cards}</div></section>{source(locale)}'
    write(locale,"classes/index.html","classes",body)
    for slug,data in CLASSES.items():
      name,role,field,range_ = data[locale]
      if de:
        title=f'{name}-Spezialisierung Guide | Star Wars Zero Company'
        desc=f'Bestätigter {name}-Guide: offizielle Rolle, taktische Grundsätze, Fortschritt und die noch ungeklärten Details vor dem Release.'
        body=f'<section class="hero"><span class="pill">Offiziell bestätigte Spezialisierung</span><h1>{name}</h1><p class="lead">{role}</p></section><section class="block"><h2>Schnellantwort</h2><table><tr><th>Aufgabe</th><td>{field}</td></tr><tr><th>Typische Distanz</th><td>{range_}</td></tr><tr><th>Struktur</th><td>Eine Ultimate, eine Standardfähigkeit und eine passive Fähigkeit</td></tr></table></section><section class="block"><h2>Taktische Einordnung</h2><p>Die Rollenbeschreibung zeigt, welchen Beitrag {name} im Team leisten soll. Plane die Aktivierung so, dass Bewegung, Angriff und eine sichere Endposition innerhalb der drei verfügbaren AP bleiben. Advantage ist eine gemeinsame Ressource; gib sie deshalb nicht automatisch für die erste verfügbare Ultimate aus, wenn ein anderer Operator den Missionsausgang stärker beeinflussen kann.</p><p>Diese Hinweise sind Entscheidungsprinzipien aus den bestätigten Systemen, keine fertige Tier-Liste oder ein behaupteter Launch-Build.</p></section><section class="block"><h2>Noch nicht bestätigt</h2><p>EA hat für diese Spezialisierung noch nicht alle Namen der Fähigkeiten, AP-Kosten, Waffenbindungen, Schadenswerte oder optimalen Teamkombinationen veröffentlicht. Diese Angaben werden erst nach Prüfung der fertigen Version ergänzt.</p></section><section><h2>Weitere Guides</h2><div class="grid"><a class="card" href="/de/classes/">Alle Spezialisierungen</a><a class="card" href="/de/confirmed/overview.html">Gameplay-Systeme</a></div></section>{source(locale)}'
      else:
        title=f'{name}専門クラス攻略 | Star Wars Zero Company'
        desc=f'{name}の公式役割、戦術上の考え方、成長システム、発売後に検証すべき未発表情報を整理します。'
        body=f'<section class="hero"><span class="pill">公式発表済み専門クラス</span><h1>{name}</h1><p class="lead">{role}</p></section><section class="block"><h2>要点</h2><table><tr><th>主な役割</th><td>{field}</td></tr><tr><th>想定距離</th><td>{range_}</td></tr><tr><th>能力構成</th><td>Ultimate 1つ、Standard Ability 1つ、Passive 1つ</td></tr></table></section><section class="block"><h2>戦術的な考え方</h2><p>{name}は、公式の役割説明に沿って部隊内の仕事を決めると理解しやすくなります。各オペレーターは1ターン3 APなので、移動と攻撃だけで使い切らず、行動後に安全な位置へ残れるかも判断してください。</p><p>Advantageは部隊共有で最大10まで蓄積します。使用可能になったUltimateをすぐ使うのではなく、任務目標や他メンバーの行動と比較して使いどころを選ぶのが基本です。ここで示すのは発表済みシステムから導ける判断基準であり、未検証の最強ビルドやTier評価ではありません。</p></section><section class="block"><h2>発売後に確認する項目</h2><p>固有アビリティ名、APコスト、対応武器、ダメージ値、Focus Tree、最適な組み合わせはすべて公開されていません。製品版または追加の公式情報で確認してから追記します。</p></section><section><h2>関連ガイド</h2><div class="grid"><a class="card" href="/ja/classes/">全専門クラス</a><a class="card" href="/ja/confirmed/overview.html">ゲームシステム概要</a></div></section>{source(locale)}'
      path=ROOT/locale/'classes'/f'{slug}.html'; path.write_text(chrome(locale,f'classes/{slug}.html',title,desc,body),encoding='utf-8')

def add_english_language_page():
    path=ROOT/'official/languages.html'
    title='Supported Languages and Audio | Star Wars Zero Company'
    desc='Star Wars Zero Company supports 11 interface and subtitle languages, with full audio confirmed in English and German.'
    body='<section class="hero"><h1>Supported Languages</h1><p class="lead"><strong>Eleven interface and subtitle languages are confirmed. Full audio is available in English and German.</strong></p></section><section class="block"><h2>Full language list</h2><p>English, French, Italian, German, Spanish (Spain), Japanese, Korean, Polish, Simplified Chinese, Traditional Chinese and Portuguese (Brazil).</p><table><tr><th>Language feature</th><th>Availability</th></tr><tr><td>Interface and subtitles</td><td>All 11 listed languages</td></tr><tr><td>Full audio</td><td>English and German</td></tr></table><p>EA lists the eleven supported languages on its purchase page. Steam and the Epic Games Store provide the more detailed separation between text and full audio.</p></section><section class="block"><h2>Related official information</h2><div class="grid"><a class="card" href="/official/release-date.html">Release date</a><a class="card" href="/official/platforms.html">Platforms</a></div></section><section class="block"><h2>Sources</h2><p class="source"><a href="'+EA_BUY+'" rel="nofollow">EA purchase page</a> · <a href="'+STEAM+'" rel="nofollow">Steam store page</a> · Checked July 18, 2026</p></section>'
    # Reuse the site's compact article chrome through the English Assault page, replacing its content safely is unnecessary; create standalone consistent markup.
    schema={"@context":"https://schema.org","@type":"Article","headline":title,"description":desc,"url":SITE+'/official/languages.html',"inLanguage":"en","dateModified":"2026-07-18"}
    links=''.join([f'<link rel="alternate" hreflang="en" href="{SITE}/official/languages.html">',f'<link rel="alternate" hreflang="de" href="{SITE}/de/official/languages.html">',f'<link rel="alternate" hreflang="ja" href="{SITE}/ja/official/languages.html">',f'<link rel="alternate" hreflang="x-default" href="{SITE}/official/languages.html">'])
    html=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><meta name="description" content="{desc}"><meta name="robots" content="index,follow"><link rel="canonical" href="{SITE}/official/languages.html">{links}<script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style></head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav><a href="/classes/">Specializations</a><a href="/confirmed/overview.html">Gameplay</a><a href="/official/">Official Info</a></nav></div></header><main class="wrap">{body}</main><footer><div class="wrap"><a href="/official/languages.html">English</a> · <a href="/de/official/languages.html">Deutsch</a> · <a href="/ja/official/languages.html">日本語</a></div></footer></body></html>'
    path.write_text(html,encoding='utf-8')

def add_hreflang_to_english():
    route_list=list(ROUTES.values())+[f'classes/{s}.html' for s in CLASSES]
    for route in route_list:
      path=ROOT/(route or 'index.html')
      if not path.exists(): continue
      text=path.read_text(encoding='utf-8-sig')
      text=re.sub(r'<link rel="alternate" hreflang="(?:en|de|ja|x-default)"[^>]*>','',text)
      en=english_route(route); tags=''.join([f'<link rel="alternate" hreflang="en" href="{SITE}{en}">',f'<link rel="alternate" hreflang="de" href="{SITE}{lang_route("de",route)}">',f'<link rel="alternate" hreflang="ja" href="{SITE}{lang_route("ja",route)}">',f'<link rel="alternate" hreflang="x-default" href="{SITE}{en}">'])
      text=text.replace('</head>',tags+'</head>',1)
      path.write_text(text,encoding='utf-8')

def main():
    add_english_language_page()
    for locale in ('de','ja'):
      build_core(locale); build_classes(locale)
    add_hreflang_to_english()
    print('Built 29 pages: one English language page plus 14 German and 14 Japanese pages')

if __name__ == '__main__': main()
