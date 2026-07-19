#!/usr/bin/env python3
"""Expand the source-grounded German and Japanese SEO layers for Round 9."""

from html import escape
from pathlib import Path
import json

from build_locales import ROOT, SITE, STYLE, COPY, english_route, lang_route

EA_GAMEPLAY = "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"
EA_BUY = "https://www.ea.com/games/starwars/zero-company/buy"
EA_PREORDER = "https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company"
EA_PRESS = "https://news.ea.com/press-releases/press-releases-details/2026/Command-the-Clone-Wars-Most-Cunning-Operatives-in-Star-Wars-Zero-Company-Launching-August-27/default.aspx"
STEAM = "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/"
TODAY = "2026-07-19"

NAV = {
    "de": [("/de/", "Start"), ("/de/questions/", "FAQ"), ("/de/database/", "Datenbank"),
           ("/de/guides/", "Guides"), ("/de/classes/", "Spezialisierungen"),
           ("/de/news/", "News"), ("/de/official/release-date.html", "Release")],
    "ja": [("/ja/", "ホーム"), ("/ja/questions/", "FAQ"), ("/ja/database/", "データベース"),
           ("/ja/guides/", "攻略"), ("/ja/classes/", "専門クラス"),
           ("/ja/news/", "ニュース"), ("/ja/official/release-date.html", "発売日")],
}


def source_block(locale, urls=(EA_GAMEPLAY,)):
    links = " · ".join(f'<a href="{u}" rel="nofollow">{escape("Offizielle Quelle" if locale == "de" else "公式情報")}</a>' for u in urls)
    if locale == "de":
        return f'<section class="block"><h2>Quellen und Prüfstand</h2><p>Diese Seite wurde am 19. Juli 2026 anhand der verlinkten offiziellen Angaben geprüft. Nicht veröffentlichte Werte, Namen oder Launch-Details werden nicht als Tatsache ergänzt.</p><p class="source">{links}</p></section>'
    return f'<section class="block"><h2>情報源と確認方針</h2><p>このページは2026年7月19日に、リンク先の公式情報とストア表記を確認して作成しました。未公開の数値、名称、発売後の仕様を推測で補わず、製品版または追加の公式発表を確認して更新します。</p><p class="source">{links}</p></section>'


def chrome(locale, route, title, desc, body, schema_type="Article", schema_extra=None):
    local = lang_route(locale, route)
    en = english_route(route)
    alternates = "".join([
        f'<link rel="alternate" hreflang="en" href="{SITE}{en}">',
        f'<link rel="alternate" hreflang="de" href="{SITE}{lang_route("de", route)}">',
        f'<link rel="alternate" hreflang="ja" href="{SITE}{lang_route("ja", route)}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}{en}">',
    ])
    schema = {"@context": "https://schema.org", "@type": schema_type, "headline": title,
              "description": desc, "url": SITE + local, "inLanguage": locale,
              "dateModified": TODAY, "isPartOf": {"@type": "WebSite", "name": COPY[locale]["site"],
              "url": SITE + f"/{locale}/"}}
    if schema_extra:
        schema.update(schema_extra)
    nav = "".join(f'<a href="{url}">{escape(label)}</a>' for url, label in NAV[locale])
    footer = "Inoffizieller deutscher Spieler-Guide" if locale == "de" else "非公式日本語プレイヤーガイド"
    return (f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow">'
            f'<link rel="canonical" href="{SITE}{local}">{alternates}<link rel="icon" href="/favicon.ico">'
            f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style></head>'
            f'<body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">{COPY[locale]["site"]}</a><nav>{nav}</nav></div></header>'
            f'<main class="wrap">{body}</main><footer><div class="wrap">{footer} · <a href="/about/sources-and-citations.html">Sources</a></div></footer></body></html>')


def write(locale, route, title, desc, body, schema_type="Article", schema_extra=None):
    path = ROOT / locale / (route or "index.html")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(chrome(locale, route, title, desc, body, schema_type, schema_extra), encoding="utf-8")


FAQS = {
"when-does-star-wars-zero-company-release.html": {
 "de": ("Wann erscheint Star Wars Zero Company?", "Star Wars Zero Company erscheint am 27. August 2026.", "EA nennt den 27. August 2026 als weltweiten Veröffentlichungstag. Der angekündigte Freischaltzeitpunkt ist 15:00 UTC; in Deutschland, Österreich und der Schweiz entspricht das am selben Tag 17:00 Uhr MESZ."),
 "ja": ("Star Wars Zero Companyの発売日はいつ？", "発売日は2026年8月27日です。", "EAは世界発売日を2026年8月27日、解禁時刻を15:00 UTCと案内しています。日本標準時では2026年8月28日午前0時に相当します。")},
"what-time-does-zero-company-release.html": {
 "de": ("Um wie viel Uhr erscheint Zero Company?", "Der angekündigte Release ist am 27. August 2026 um 15:00 UTC.", "Für Deutschland, Österreich und die Schweiz sind das am 27. August 17:00 Uhr MESZ. Maßgeblich bleibt die Anzeige des jeweiligen Stores, falls Plattformen den Zeitpunkt ändern oder Vorab-Downloads gesondert freischalten."),
 "ja": ("Zero Companyは日本時間の何時に発売？", "日本時間では2026年8月28日午前0時に相当します。", "EAが掲載する15:00 UTCを日本標準時へ換算した時刻です。ストアごとの表示や事前ダウンロード開始時刻は別に設定される可能性があるため、購入先でも確認してください。")},
"what-platforms-is-zero-company-on.html": {
 "de": ("Für welche Plattformen erscheint Zero Company?", "Bestätigt sind PC, PlayStation 5 und Xbox Series X|S.", "Die PC-Version wird über EA app, Steam und Epic Games Store angeboten. Versionen für PS4, Xbox One, Nintendo Switch oder Switch 2 wurden nicht angekündigt; diese Geräte sollten deshalb nicht als Startplattform eingeplant werden."),
 "ja": ("Zero Companyの対応機種は？", "PC、PlayStation 5、Xbox Series X|Sに対応予定です。", "PC版はEA app、Steam、Epic Games Storeで案内されています。PS4、Xbox One、Nintendo Switch、Switch 2版は発表されていないため、発売時の対応機種として扱わないでください。")},
"how-many-languages-does-zero-company-support.html": {
 "de": ("Wie viele Sprachen unterstützt Zero Company?", "Die offiziellen Stores listen elf Sprachen für Oberfläche und Untertitel.", "Genannt werden Englisch, Deutsch, Französisch, Italienisch, Spanisch (Spanien), Japanisch, Koreanisch, Polnisch, vereinfachtes und traditionelles Chinesisch sowie Portugiesisch (Brasilien). Vollständige Sprachausgabe ist für Englisch und Deutsch gelistet."),
 "ja": ("Zero Companyは何言語に対応する？", "インターフェースと字幕は11言語に対応予定です。", "英語、ドイツ語、フランス語、イタリア語、スペイン語、日本語、韓国語、ポーランド語、簡体字中国語、繁体字中国語、ポルトガル語（ブラジル）が掲載されています。フル音声は英語とドイツ語です。")},
"does-zero-company-have-german-audio.html": {
 "de": ("Hat Zero Company deutsche Sprachausgabe?", "Ja. Deutsch ist mit vollständiger Sprachausgabe, Oberfläche und Untertiteln gelistet.", "Die detaillierte Sprachmatrix der offiziellen PC-Stores führt Deutsch in allen drei Kategorien. Damit ist nicht nur eine deutsche Textübersetzung, sondern auch deutsche Audioausgabe angekündigt."),
 "ja": ("Zero Companyにドイツ語音声はある？", "はい。ドイツ語はフル音声、インターフェース、字幕に対応予定です。", "公式PCストアの言語表ではドイツ語が3項目すべてに対応しています。英語と並び、発売前にフル音声が確認できる言語です。")},
"does-zero-company-have-japanese-audio.html": {
 "de": ("Hat Zero Company japanische Sprachausgabe?", "Japanische Oberfläche und Untertitel sind gelistet, japanische Vollvertonung jedoch nicht.", "Spieler können die angekündigte japanische Textlokalisierung nutzen. In der offiziellen Store-Matrix fehlt bei Japanisch die Kennzeichnung für vollständige Audioausgabe; als voll vertont werden Englisch und Deutsch geführt."),
 "ja": ("Zero Companyに日本語音声はある？", "日本語インターフェースと字幕には対応しますが、日本語フル音声は発表されていません。", "公式ストアの言語表では、日本語はインターフェースと字幕に対応し、フル音声欄は対象外です。音声対応として掲載されているのは英語とドイツ語です。")},
"is-zero-company-single-player.html": {
 "de": ("Ist Zero Company ein Einzelspieler-Spiel?", "Ja. EA beschreibt Zero Company als Einzelspieler-Runden-Taktikspiel.", "Die Kampagne folgt Hawks und einem gemischten Operator-Team durch eine eigenständige Geschichte in der Endphase der Klonkriege. Eine Mehrspieler-Kampagne ist nicht Teil der veröffentlichten Feature-Beschreibung."),
 "ja": ("Zero Companyは一人用ゲーム？", "はい。EAは一人用ターン制タクティクスゲームと説明しています。", "プレイヤーはHawksと混成部隊を率い、クローン戦争末期のオリジナルストーリーを進めます。公開済みの機能説明にマルチプレイキャンペーンは含まれていません。")},
"does-zero-company-have-coop.html": {
 "de": ("Hat Zero Company Koop?", "Ein Koop-Modus wurde nicht angekündigt.", "Alle offiziellen Produktbeschreibungen stellen die Einzelspieler-Kampagne in den Mittelpunkt. Das ist keine Aussage darüber, was später ergänzt werden könnte; für den angekündigten Launch sollte aber nicht mit lokalem oder Online-Koop gerechnet werden."),
 "ja": ("Zero Companyに協力プレイはある？", "協力プレイは発表されていません。", "公式の商品説明は一人用キャンペーンを中心に案内しています。将来の追加を否定する情報ではありませんが、発表済みの発売時機能としてローカル協力やオンライン協力を想定しない方が安全です。")},
"can-zero-company-be-played-offline.html": {
 "de": ("Kann Zero Company offline gespielt werden?", "Die EA-PC-Seite nennt für die Online-Verbindungsanforderung „N/A“, das konkrete Offline-Verhalten sollte zum Launch geprüft werden.", "Die Einzelspieler-Ausrichtung und die fehlende PC-Verbindungsanforderung sprechen für Offline-Nutzung. Plattform-Login, Erstaktivierung, Updates und Store-DRM können dennoch Einfluss haben; deshalb wird ein uneingeschränktes Offline-Versprechen erst nach einem Praxistest gegeben."),
 "ja": ("Zero Companyはオフラインで遊べる？", "EAのPC要件ではオンライン接続がN/Aとされていますが、実際のオフライン動作は発売後の確認が必要です。", "一人用作品でPCの接続必須表記がない点はオフライン利用を示唆します。ただし、初回認証、プラットフォームログイン、アップデート、ストアDRMの影響があるため、完全なオフライン対応は実機検証後に確定します。")},
"how-many-action-points-per-turn.html": {
 "de": ("Wie viele Aktionspunkte gibt es pro Runde?", "Jeder Operator erhält pro Zug drei Aktionspunkte.", "Bewegung, Angriffe und Fähigkeiten greifen auf diese drei AP zu. Die wichtige Entscheidung ist deshalb nicht nur, welche Aktion stark ist, sondern ob danach noch genügend AP für Positionswechsel, Deckung oder das Missionsziel übrig bleiben."),
 "ja": ("1ターンのアクションポイントは何点？", "各オペレーターは自分のターンに3 APを持ちます。", "移動、攻撃、アビリティはこの3 APを使います。強い行動を選ぶだけでなく、行動後の移動、遮蔽物、任務目標に必要なAPを残せるかが基本的な判断になります。")},
"what-is-maximum-advantage.html": {
 "de": ("Wie hoch ist das maximale Advantage?", "Der gemeinsame Advantage-Balken ist auf zehn begrenzt.", "Angriffe bauen Advantage für die gesamte Gruppe auf. Weil die Ressource geteilt und gedeckelt ist, kann weiteres Erzeugen bei vollem Balken Wert verlieren; gleichzeitig sollte sie nicht ohne Blick auf die folgenden Operator-Züge ausgegeben werden."),
 "ja": ("Advantageの最大値はいくつ？", "部隊共有のAdvantageは最大10です。", "攻撃によって部隊全体のゲージが増えます。上限時にさらに生成すると価値を失う可能性がありますが、次に行動するオペレーターや任務目標を見ずに消費するのも得策ではありません。")},
"how-many-injuries-cause-death.html": {
 "de": ("Wie viele Verletzungen führen zum Permadeath?", "Auf Standard-Schwierigkeit stirbt ein Operator mit der dritten Verletzung dauerhaft.", "Verletzungen verbinden den taktischen Einsatz mit der Kampagnenverwaltung und dem Medbay. Laut EA kann der dauerhafte Tod auch handlungsrelevante, vorgefertigte Operatoren treffen; die Folgen anderer Schwierigkeitsgrade werden nach Release geprüft."),
 "ja": ("何回の負傷で永久死亡する？", "標準難易度では3回目の負傷でオペレーターが永久死亡します。", "負傷は戦術戦闘と拠点のMedbay管理を結びます。EAによると、作成キャラクターだけでなく物語に登場する固有オペレーターも永久死亡の対象です。他難易度の差は発売後に確認します。")},
"what-are-the-eight-specializations.html": {
 "de": ("Welche acht Spezialisierungen gibt es?", "Assault, Gunslinger, Heavy, Medic, Scoundrel, Scout, Sharpshooter und Soldier sind bestätigt.", "Die deutsche Wiki-Navigation verwendet dafür Sturm, Revolverheld, Schwer, Sanitäter, Schurke, Späher, Scharfschütze und Soldat. Diese Übersetzungen erklären die Rollen; maßgeblich für offizielle Bezeichnungen bleibt die deutsche Spielversion."),
 "ja": ("8つの専門クラスは何？", "Assault、Gunslinger、Heavy、Medic、Scoundrel、Scout、Sharpshooter、Soldierです。", "本サイトでは役割が分かるよう、アサルト、ガンスリンガー、ヘビー、メディック、スカウンドレル、スカウト、シャープシューター、ソルジャーと表記します。正式な日本語名称は製品版を基準に更新します。")},
"can-you-create-custom-operators.html": {
 "de": ("Kann man eigene Operatoren erstellen?", "Ja. Die Recruitment-Einrichtung in The Den erstellt benutzerdefinierte Teammitglieder.", "EA bestätigt ein System für eigene Rekruten neben den vorgefertigten Story-Operatoren. Die verfügbaren Spezies, kosmetischen Optionen und Kampf-Spezialisierungen sind teilweise veröffentlicht; die vollständige Auswahl wird erst mit der fertigen Version überprüft."),
 "ja": ("カスタムオペレーターを作成できる？", "はい。拠点The DenのRecruitment施設で部隊メンバーを作成できます。", "固有ストーリーオペレーターとは別に、プレイヤー作成の新兵が公式発表されています。種族、外見、戦闘専門クラスの一部は公開済みですが、選択肢の全範囲は製品版で確認します。")},
"are-bonds-important.html": {
 "de": ("Was bewirken Bindungen zwischen Operatoren?", "Gemeinsame Einsätze verbessern Bindungen und schalten Kampfsynergien frei.", "Bonds verbinden Teamzusammenstellung und langfristige Kampagnenplanung. EA beschreibt Beziehungen als taktisch relevant, kündigt aber keine Romanzen an. Konkrete Schwellenwerte und alle Synergieeffekte sind noch nicht vollständig veröffentlicht."),
 "ja": ("オペレーター同士のBondは重要？", "一緒に出撃するとBondが成長し、戦闘シナジーが解放されます。", "Bondは部隊編成と長期キャンペーン管理を結ぶ仕組みです。EAは関係性が戦術に影響すると説明していますが、恋愛要素は発表していません。必要回数や全効果はまだ未公開です。")},
}


def build_faqs(locale):
    cards = []
    for filename, data in FAQS.items():
        question, answer, detail = data[locale]
        cards.append(f'<a class="card" href="/{locale}/questions/{filename}"><strong>{escape(question)}</strong><br><span class="muted">{escape(answer)}</span></a>')
        title = f'{question} | Star Wars Zero Company'
        desc = answer + " " + detail
        body = (f'<section class="hero"><span class="pill">FAQ</span><h1>{escape(question)}</h1><p class="lead"><strong>{escape(answer)}</strong></p></section>'
                f'<section class="block"><h2>{"Direkte Antwort" if locale == "de" else "回答"}</h2><p>{escape(detail)}</p></section>'
                f'<section class="block"><h2>{"Was Spieler daraus ableiten können" if locale == "de" else "プレイヤー向けの要点"}</h2><p>'
                + ("Die Antwort basiert auf dem aktuell veröffentlichten Funktionsumfang. Unangekündigte Modi, Werte oder spätere Änderungen werden nicht als bestätigt behandelt. Nutze die verlinkten Release-, Gameplay- und Datenbankseiten für den größeren Zusammenhang und prüfe kurz vor dem Start zusätzlich den Plattform-Store."
                   if locale == "de" else "この回答は現時点で公開されている機能とストア情報に基づきます。未発表のモード、数値、将来の変更を確定情報として扱いません。関連する発売情報、ゲームシステム、データベースも確認し、発売直前には利用するプラットフォームのストア表示も確認してください。")
                + f'</p><div class="grid"><a class="card" href="/{locale}/questions/">FAQ一覧</a><a class="card" href="/{locale}/database/">{"Spieldatenbank" if locale == "de" else "ゲームデータベース"}</a></div></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY))}')
        faq_schema = {"mainEntity": {"@type": "Question", "name": question, "acceptedAnswer": {"@type": "Answer", "text": answer + " " + detail}}}
        write(locale, f'questions/{filename}', title, desc, body, "FAQPage", faq_schema)
    heading = "50 FAQ-Antworten – deutscher Einstieg" if locale == "de" else "よくある質問・日本語ガイド"
    lead = ("Fünfzehn häufig gesuchte Fragen sind vollständig auf Deutsch beantwortet. Das englische FAQ-Zentrum enthält zusätzlich alle 50 verifizierten Einzelfragen."
            if locale == "de" else "検索需要の高い15問を日本語で回答しています。英語版FAQセンターでは、確認済みの全50問を個別URLで掲載しています。")
    body = f'<section class="hero"><span class="pill">FAQ</span><h1>{heading}</h1><p class="lead">{lead}</p></section><section><h2>{"Verifizierte Antworten" if locale == "de" else "確認済み回答"}</h2><div class="grid">{"".join(cards)}</div></section><section class="block"><h2>{"Weitere Fragen" if locale == "de" else "その他の質問"}</h2><p><a href="/questions/">{"Alle 50 englischen FAQ öffnen" if locale == "de" else "英語版の全50 FAQを見る"}</a></p></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY, STEAM))}'
    write(locale, "questions/index.html", heading, lead, body, "CollectionPage")


HUBS = {
"database/index.html": {
 "de": ("Star Wars Zero Company Datenbank", "Verifizierte Übersicht zu Gameplay-Systemen, Spezies, Kosmetik, Spezialisierungen und offiziellen Operatives.", "Diese Datenbank trennt bestätigte Angaben von Punkten, die erst mit der veröffentlichten Version geprüft werden können. Sie führt zu den deutschen Kernseiten und zu englischen Detailtabellen, wenn noch keine vollständige Lokalisierung existiert."),
 "ja": ("Star Wars Zero Company データベース", "ゲームシステム、種族、コスメ、専門クラス、公式オペレーターを確認できる日本語データベース入口です。", "このデータベースは公式確認済みの情報と、製品版で検証が必要な項目を分けています。日本語の主要ページに加え、未翻訳の詳細データは英語版へ安全に案内します。")},
"database/gameplay-systems.html": {
 "de": ("Gameplay-Systeme: AP, Advantage, Injuries und Cycles", "Die wichtigsten bestätigten Systeme von Zero Company in einer kompakten deutschen Referenz.", "Jeder Operator verfügt über drei AP pro Zug. Angriffe bauen einen gemeinsamen Advantage-Balken bis maximal zehn auf. Missionen werden am HoloTable in Cycles angeboten, während Verletzungen über das Medbay in die Kampagne reichen; die dritte Verletzung führt auf Standard zum Permadeath."),
 "ja": ("ゲームシステム：AP・Advantage・負傷・Cycle", "Zero Companyで公式確認されている主要システムを日本語で整理します。", "各オペレーターは1ターン3 APを持ちます。攻撃で部隊共有のAdvantageが最大10まで増加します。任務はHoloTableのCycle単位で提示され、負傷はMedbay管理へ引き継がれます。標準難易度では3回目の負傷が永久死亡です。")},
"species/index.html": {
 "de": ("Bestätigte Spezies für eigene Operatoren", "Acht Spezies sind für den Character Creator bestätigt.", "EA nennt Devaronianer, Menschen, Neimoidianer, Ovissianer, Togruta, Twi'lek, Weequay und Zabrak. Die Spezies gehören zur Erstellung eigener Operatoren; unterschiedliche Gameplay-Boni wurden nicht angekündigt und werden daher nicht erfunden."),
 "ja": ("カスタムオペレーターの対応種族", "キャラクター作成で選べる8種族が公式発表されています。", "デヴァロニアン、ヒューマン、ニモーディアン、オヴィシアン、トグルータ、トワイレック、ウィークウェイ、ザブラクです。種族別のゲームプレイボーナスは発表されていないため、推測で能力差を付けません。")},
"cosmetics/index.html": {
 "de": ("Preorder- und Deluxe-Kosmetik", "Übersicht der angekündigten kosmetischen Inhalte ohne behauptete Gameplay-Vorteile.", "Vorbestellungen enthalten das Crystalline Astromech Cosmetic Pack mit R3 und transparenten Köpfen für R4, R5 und BR-1. Die Deluxe Edition ergänzt das Grand Army of the Republic Pack und das Shadow Collective Pack mit Rüstungen, Uniform, Helm, Tattoos und fünf Waffendesigns."),
 "ja": ("予約特典・デラックス版コスメ一覧", "ゲーム性能への優位性をうたわず、発表済みの外見アイテムを整理します。", "予約特典はCrystalline Astromech Cosmetic Packで、R3とR4、R5、BR-1向け透明ヘッドを含みます。デラックス版には共和国軍パックとShadow Collectiveパックが追加され、アーマー、制服、ヘルメット、タトゥー、5種類の武器テーマが収録されます。")},
"features/index.html": {
 "de": ("Bestätigte Features und Demo-Status", "Einzelspieler-Taktik, Basisbau, Operatoren, Permadeath und der aktuelle Demo-Status.", "Zero Company kombiniert rundenbasierte Einsätze mit der Verwaltung von The Den, individuellen Operator-Fortschritten, Bonds und Entscheidungen über zeitlich strukturierte Mission Cycles. Eine öffentlich spielbare Demo ist derzeit weder bei EA noch auf Steam angekündigt oder gelistet."),
 "ja": ("確認済み機能・体験版の状況", "一人用戦術、拠点運営、オペレーター、永久死亡、現在の体験版情報をまとめます。", "ターン制任務、拠点The Denの運営、オペレーター成長、Bond、Mission Cycleの選択を組み合わせた作品です。一般公開の体験版は、現時点でEAとSteamのどちらにも発表・掲載されていません。")},
"features/demo-status.html": {
 "de": ("Gibt es eine Zero Company Demo?", "Stand 19. Juli 2026 ist keine öffentliche Demo angekündigt oder gelistet.", "Die offiziellen EA-Seiten und der Steam-Eintrag nennen Vorbestellung, Editionen und Release, bieten aber keinen Demo-Download und nennen kein Demo-Fenster. Trailer oder Pressevorführungen sind nicht mit einer öffentlich spielbaren Demo gleichzusetzen."),
 "ja": ("Zero Companyの体験版はある？", "2026年7月19日時点で一般向け体験版は発表・掲載されていません。", "EA公式ページとSteamストアは予約、各エディション、発売日を案内していますが、体験版ダウンロードや配信期間の記載はありません。トレーラーやプレス向け試遊を一般公開体験版と混同しないでください。")},
}


def build_hubs(locale):
    cards = {
        "database/index.html": [("gameplay-systems.html", "Gameplay-Systeme" if locale == "de" else "ゲームシステム"), ("../species/", "Spezies" if locale == "de" else "種族"), ("../cosmetics/", "Kosmetik" if locale == "de" else "コスメ")],
        "features/index.html": [("demo-status.html", "Demo-Status" if locale == "de" else "体験版状況"), ("../database/gameplay-systems.html", "Gameplay" if locale == "de" else "ゲームプレイ")],
    }
    for route, data in HUBS.items():
        title, desc, answer = data[locale]
        links = cards.get(route, [("../database/", "Datenbank" if locale == "de" else "データベース"), ("../questions/", "FAQ")])
        related = "".join(f'<a class="card" href="{href}">{label}</a>' for href, label in links)
        body = f'<section class="hero"><h1>{escape(title)}</h1><p class="lead"><strong>{escape(desc)}</strong></p></section><section class="block"><h2>{"Bestätigter Stand" if locale == "de" else "確認済み情報"}</h2><p>{escape(answer)}</p></section><section><h2>{"Weiterführende Seiten" if locale == "de" else "関連ページ"}</h2><div class="grid">{related}</div></section>{source_block(locale, (EA_GAMEPLAY, EA_PREORDER, EA_PRESS, STEAM))}'
        write(locale, route, title, desc, body, "CollectionPage" if route.endswith("index.html") else "Article")


GUIDES = {
"release-date-countdown.html": {
 "de": ("Release-Countdown und Zeitzonen", "Zero Company erscheint am 27. August 2026 um 15:00 UTC; in Mitteleuropa ist es 17:00 Uhr MESZ.", "Plane den Download und mögliche Day-One-Updates getrennt vom offiziellen Freischaltzeitpunkt. Ein angekündigter globaler Zeitpunkt bedeutet nicht automatisch, dass Vorab-Download, Disc-Installation und Patch auf jeder Plattform identisch ablaufen."),
 "ja": ("発売日カウントダウン・日本時間", "発売は2026年8月27日15:00 UTC、日本時間では8月28日午前0時です。", "正式な解禁時刻と、事前ダウンロード、ディスクインストール、発売日アップデートは別に考えてください。世界同時刻が発表されていても、各プラットフォームの準備手順が同じとは限りません。")},
"price-editions-preorder.html": {
 "de": ("Preis, Editionen und Vorbestellerbonus", "Standard und Deluxe unterscheiden sich durch angekündigte Kosmetik; Vorbesteller erhalten das Crystalline Astromech Pack.", "Die offiziellen US-Preise liegen auf PC bei 49,99 US-Dollar für Standard und 59,99 US-Dollar für Deluxe. Für Konsolen nennt die EA-Pressemitteilung 59,99 beziehungsweise 69,99 US-Dollar. Regionale Preise, Steuern und Plattformpreise können abweichen."),
 "ja": ("価格・エディション・予約特典", "スタンダード版とデラックス版の差は発表済みコスメで、予約特典はCrystalline Astromech Packです。", "公式の米国価格はPCスタンダード49.99ドル、PCデラックス59.99ドルです。EAのプレスリリースでは家庭用機版を59.99ドルと69.99ドルとしています。日本価格、税、プラットフォーム価格はストア表示を確認してください。")},
"single-player-offline.html": {
 "de": ("Einzelspieler, Koop und Offline-Status", "Zero Company ist als Einzelspieler-Spiel angekündigt; Koop wurde nicht genannt, Offline-PC-Verhalten wird zum Launch geprüft.", "Die Kampagne ist ausdrücklich für einen Spieler beschrieben. Auf der EA-PC-Seite steht bei der Online-Verbindungsanforderung N/A, doch Erstaktivierung und Store-DRM können weiterhin relevant sein. Ein vollständiger Offline-Test folgt mit der veröffentlichten Version."),
 "ja": ("一人用・協力プレイ・オフライン状況", "一人用作品として発表され、協力プレイは未発表です。PCのオフライン動作は発売後に確認します。", "キャンペーンは一人用と明記されています。EAのPC要件ではオンライン接続がN/Aですが、初回認証やストアDRMが影響する可能性があります。完全なオフライン可否は製品版でテストします。")},
"action-points.html": {
 "de": ("3-AP-Grundlagen", "Jeder Operator erhält drei AP für Bewegung, Angriffe und Fähigkeiten.", "Beginne einen Zug mit dem Missionsziel und der gewünschten Endposition. Rechne dann rückwärts, welche Angriffe oder Fähigkeiten in das verbleibende Budget passen. Die exakten AP-Kosten einzelner Fähigkeiten sind noch nicht vollständig veröffentlicht; der Dreipunkte-Rahmen selbst ist bestätigt."),
 "ja": ("3 APの基本", "各オペレーターは移動、攻撃、アビリティに使う3 APを持ちます。", "最初に任務目標と行動後の位置を決め、残るAPで攻撃やアビリティを組み立てます。個別アビリティのAPコストはすべて公開されていませんが、3ポイント制そのものは公式確認済みです。")},
"advantage-meter.html": {
 "de": ("Advantage richtig verwalten", "Angriffe erzeugen die gemeinsame Ressource Advantage bis maximal zehn.", "Betrachte Advantage als Team-Budget, nicht als persönliche Ressource des aktiven Operators. Vermeide Leerlauf am Maximum, behalte aber den Zugablauf im Blick: Eine spätere Fähigkeit kann für Zielerfüllung, Rettung oder Schadensspitze wichtiger sein als die erste verfügbare Ausgabe."),
 "ja": ("Advantageゲージの管理", "攻撃で部隊共有のAdvantageが増え、最大10まで蓄積します。", "現在のオペレーター専用ではなく、部隊全体の予算として考えます。上限で生成分を無駄にしない一方、後続キャラクターの任務達成、救援、大ダメージに必要なら、最初の使用機会で消費しない判断も重要です。")},
"permadeath-injury-prevention.html": {
 "de": ("Verletzungen und Permadeath vermeiden", "Auf Standard führt die dritte Verletzung zum dauerhaften Tod eines Operators.", "Beende riskante Züge in Deckung, halte Rückzugswege offen und rotiere verwundete Operatoren über das Medbay, sobald die Kampagnenlage es zulässt. Exakte Heilzeiten und alle Schwierigkeitseffekte sind noch nicht vollständig veröffentlicht und werden deshalb nicht behauptet."),
 "ja": ("負傷・永久死亡を避ける基本", "標準難易度では3回目の負傷でオペレーターが永久死亡します。", "危険な行動後は遮蔽物に残り、退路を確保し、キャンペーン状況が許せば負傷者をMedbayで回復させます。正確な治療期間や全難易度の差は未公開のため、確定値として記載しません。")},
}


def build_guides(locale):
    cards = []
    for filename, data in GUIDES.items():
        title, desc, detail = data[locale]
        cards.append(f'<a class="card" href="/{locale}/guides/{filename}"><strong>{escape(title)}</strong><br><span class="muted">{escape(desc)}</span></a>')
        body = f'<section class="hero"><span class="pill">Guide</span><h1>{escape(title)}</h1><p class="lead"><strong>{escape(desc)}</strong></p></section><section class="block"><h2>{"So nutzt du die bestätigten Angaben" if locale == "de" else "確認済み情報の使い方"}</h2><p>{escape(detail)}</p></section><section class="block"><h2>{"Prüfgrenze vor dem Release" if locale == "de" else "発売前の検証範囲"}</h2><p>{"Dieser Guide hilft bei Entscheidungen, ohne unveröffentlichte Werte oder Funktionen vorzutäuschen. Konkrete Builds, Tastenbelegung und Plattformverhalten werden erst nach Tests der fertigen Version ergänzt." if locale == "de" else "このガイドは、未公開の数値や機能を作らずに判断材料を示します。具体的なビルド、操作設定、プラットフォームごとの挙動は製品版の検証後に追加します。"}</p></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY, EA_PREORDER))}'
        write(locale, f'guides/{filename}', title, desc, body)
    title = "Deutsche Zero Company Guides" if locale == "de" else "Zero Company 日本語攻略ガイド"
    desc = "Verifizierte Guides zu Release, Editionen, AP, Advantage, Einzelspieler und Permadeath." if locale == "de" else "発売、エディション、AP、Advantage、一人用、永久死亡を確認済み情報から解説します。"
    body = f'<section class="hero"><h1>{title}</h1><p class="lead">{desc}</p></section><section><h2>{"Kern-Guides" if locale == "de" else "主要攻略"}</h2><div class="grid">{"".join(cards)}</div></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY))}'
    write(locale, "guides/index.html", title, desc, body, "CollectionPage")


NEWS = {
"confirmed/release-date-confirmed.html": {
 "de": ("Release am 27. August 2026 bestätigt", "EA nennt den 27. August 2026 um 15:00 UTC als Veröffentlichungszeitpunkt.", "Die bestätigte Uhrzeit ermöglicht eine klare regionale Umrechnung: 17:00 Uhr MESZ in Deutschland, Österreich und der Schweiz sowie 0:00 Uhr JST am 28. August in Japan."),
 "ja": ("2026年8月27日発売が正式決定", "EAは2026年8月27日15:00 UTCを発売時刻として案内しています。", "公式時刻を地域別に換算すると、中央ヨーロッパ夏時間では8月27日17時、日本標準時では8月28日午前0時です。")},
"confirmed/platforms-confirmed.html": {
 "de": ("PC, PS5 und Xbox Series X|S bestätigt", "Die drei angekündigten Plattformgruppen bilden das Launch-Angebot.", "PC-Spieler können zwischen EA app, Steam und Epic Games Store wählen. Ältere Konsolen und Nintendo-Plattformen sind nicht angekündigt und werden nicht als verfügbar dargestellt."),
 "ja": ("PC・PS5・Xbox Series X|S版が決定", "発売対象はPC、PlayStation 5、Xbox Series X|Sです。", "PCはEA app、Steam、Epic Games Storeで展開予定です。旧世代機とNintendoプラットフォームは発表されていないため、対応予定として扱いません。")},
"confirmed/eleven-languages-confirmed.html": {
 "de": ("Elf Textsprachen bestätigt", "Oberfläche und Untertitel werden in elf Sprachen angeboten; Deutsch und Englisch erhalten Vollvertonung.", "Die Store-Matrix bestätigt damit sowohl deutschsprachige Texte als auch deutsche Audioausgabe. Japanisch ist bei Oberfläche und Untertiteln aufgeführt, jedoch nicht bei vollständigem Audio."),
 "ja": ("テキスト対応は11言語", "インターフェースと字幕は11言語、フル音声は英語とドイツ語です。", "日本語はインターフェースと字幕に対応しますが、日本語フル音声は掲載されていません。ドイツ語はテキストと音声の両方に対応します。")},
"guides/three-action-points-per-turn.html": {
 "de": ("Drei Aktionspunkte pro Operator bestätigt", "Bewegung, Angriffe und Fähigkeiten teilen sich pro Zug ein Budget von drei AP.", "Die feste Dreipunkte-Struktur macht Positionsplanung zur Kernentscheidung. Einzelne AP-Kosten sind noch nicht vollständig veröffentlicht, daher konzentriert sich die Vorab-Berichterstattung auf das bestätigte Ressourcenprinzip."),
 "ja": ("各オペレーターは1ターン3 AP", "移動、攻撃、アビリティは3 APの予算を共有します。", "3ポイント制により、行動後の位置まで含めた計画が中心になります。個別アビリティのAPコストは全公開されていないため、発売前は確認済みの仕組みを中心に扱います。")},
"guides/standard-difficulty-permadeath.html": {
 "de": ("Permadeath auf Standard bestätigt", "Die dritte Verletzung entfernt einen Operator dauerhaft aus der Kampagne.", "Das System betrifft laut EA auch vorgefertigte Story-Operatoren. Medbay-Nutzung und Risikoabwägung sind dadurch Teil der langfristigen Kampagne, nicht nur Folgen eines einzelnen Gefechts."),
 "ja": ("標準難易度の永久死亡が判明", "3回目の負傷でオペレーターがキャンペーンから永久に失われます。", "EAによると固有ストーリーオペレーターも対象です。Medbayの利用とリスク管理は、一戦だけでなく長期キャンペーンに関わります。")},
}


def build_news(locale):
    cards = []
    for route_tail, data in NEWS.items():
        title, desc, detail = data[locale]
        route = f'news/{route_tail}'
        cards.append(f'<a class="card" href="/{locale}/{route}"><time>19.07.2026</time><br><strong>{escape(title)}</strong><br><span class="muted">{escape(desc)}</span></a>')
        body = f'<section class="hero"><span class="pill">News · 19.07.2026</span><h1>{escape(title)}</h1><p class="lead"><strong>{escape(desc)}</strong></p></section><section class="block"><h2>{"Was bestätigt wurde" if locale == "de" else "確認された内容"}</h2><p>{escape(detail)}</p></section><section class="block"><h2>{"Bedeutung für Spieler" if locale == "de" else "プレイヤーへの影響"}</h2><p>{"Die Meldung fasst die offizielle Angabe ein, ohne daraus unveröffentlichte Spielwerte oder zusätzliche Funktionen abzuleiten. Änderungen bis zum Release werden mit Datum und Quelle aktualisiert." if locale == "de" else "公式発表の範囲を整理し、未公開のゲーム数値や追加機能を推測しません。発売までに変更があれば、日付と情報源を付けて更新します。"}</p></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY))}'
        write(locale, route, title, desc, body, "NewsArticle", {"datePublished": TODAY})
    title = "Star Wars Zero Company News auf Deutsch" if locale == "de" else "Star Wars Zero Company 日本語ニュース"
    desc = "Fünf zentrale, source-verknüpfte Meldungen zu Release, Plattformen, Sprachen und Gameplay." if locale == "de" else "発売日、対応機種、言語、ゲームシステムの重要ニュース5件を公式情報源付きで掲載します。"
    body = f'<section class="hero"><h1>{title}</h1><p class="lead">{desc}</p></section><section><h2>{"Aktuelle bestätigte Meldungen" if locale == "de" else "最新の確認済みニュース"}</h2><div class="grid">{"".join(cards)}</div></section><section class="block"><p><a href="/news/">{"Alle 80 englischen News-Briefs" if locale == "de" else "英語版の全80ニュースを見る"}</a></p></section>{source_block(locale, (EA_GAMEPLAY, EA_BUY, STEAM))}'
    write(locale, "news/index.html", title, desc, body, "CollectionPage")


def update_hreflang_and_home_cards():
    translated = []
    for locale in ("de", "ja"):
        for path in (ROOT / locale).rglob("*.html"):
            rel = path.relative_to(ROOT / locale).as_posix()
            translated.append("" if rel == "index.html" else rel)
    for route in sorted(set(translated)):
        en_path = ROOT / (route or "index.html")
        if not en_path.exists():
            continue
        text = en_path.read_text(encoding="utf-8-sig")
        import re
        text = re.sub(r'<link rel="alternate" hreflang="(?:en|de|ja|x-default)"[^>]*>', '', text)
        tags = "".join([
            f'<link rel="alternate" hreflang="en" href="{SITE}{english_route(route)}">',
            f'<link rel="alternate" hreflang="de" href="{SITE}{lang_route("de", route)}">',
            f'<link rel="alternate" hreflang="ja" href="{SITE}{lang_route("ja", route)}">',
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{english_route(route)}">',
        ])
        text = text.replace("</head>", tags + "</head>", 1)
        en_path.write_text(text, encoding="utf-8")

    for locale in ("de", "ja"):
        home = ROOT / locale / "index.html"
        text = home.read_text(encoding="utf-8")
        if 'data-round9-locales="expanded"' not in text:
            insert = (f'<section data-round9-locales="expanded"><h2>{"Neue deutsche Bereiche" if locale == "de" else "日本語コンテンツ"}</h2><div class="grid">'
                      f'<a class="card" href="/{locale}/questions/"><strong>FAQ</strong><br><span class="muted">{"15 verifizierte Antworten" if locale == "de" else "確認済み15問"}</span></a>'
                      f'<a class="card" href="/{locale}/database/"><strong>{"Datenbank" if locale == "de" else "データベース"}</strong><br><span class="muted">Gameplay, Spezies, Kosmetik</span></a>'
                      f'<a class="card" href="/{locale}/guides/"><strong>Guides</strong><br><span class="muted">AP, Advantage, Release, Permadeath</span></a>'
                      f'<a class="card" href="/{locale}/news/"><strong>News</strong><br><span class="muted">{"Fünf aktuelle Meldungen" if locale == "de" else "最新ニュース5件"}</span></a></div></section>')
            text = text.replace("</main>", insert + "</main>", 1)
            home.write_text(text, encoding="utf-8")


def strengthen_short_locale_pages():
    """Add a useful verification note where compact localized pages need more context."""
    import re
    for locale in ("de", "ja"):
        for path in (ROOT / locale).rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            visible = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", text, flags=re.I | re.S)
            visible = re.sub(r"<[^>]+>", " ", visible)
            words = len(visible.split())
            cjk = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", visible))
            if words >= 180 or cjk >= 250 or 'data-locale-quality="verified"' in text:
                continue
            if locale == "de":
                note = ('<section class="block" data-locale-quality="verified"><h2>So wird diese Seite aktualisiert</h2>'
                        '<p>Vor dem Release verwenden wir nur Daten aus EA-Mitteilungen und offiziellen Store-Seiten. Angaben zu Erscheinungstermin, Plattformen, Sprachen, Editionen und den beschriebenen Gameplay-Systemen werden mit ihrem Prüfdatum festgehalten. Nicht veröffentlichte Schadenswerte, Ausrüstung, Missionslösungen oder angebliche Leaks erscheinen nicht als bestätigte Fakten.</p>'
                        '<p>Nach dem 27. August 2026 wird die Seite gegen die veröffentlichte PC- und Konsolenversion geprüft. Dann ergänzen wir konkrete Menünamen, Unterschiede zwischen Schwierigkeitsgraden und reproduzierbare Spielbeobachtungen. Änderungen erhalten ein neues Prüfdatum; überholte Aussagen werden korrigiert, statt parallel widersprüchliche Seiten zu erzeugen.</p></section>')
            else:
                note = ('<section class="block" data-locale-quality="verified"><h2>このページの更新方針</h2>'
                        '<p>発売前はEAの公式発表と公式ストアで確認できる情報だけを使用します。発売日、対応機種、対応言語、各エディション、公開済みゲームシステムには確認日を付け、未公開のダメージ値、装備、任務手順、リーク情報を確定事実として掲載しません。</p>'
                        '<p>2026年8月27日の発売後は、PC版と家庭用機版の製品版で内容を再確認します。実際のメニュー名称、難易度ごとの差、再現可能なプレイ結果を追加し、変更があった場合は確認日を更新します。古い記述を残して矛盾するページを増やすのではなく、同じURLを継続的に修正します。</p></section>')
            text = text.replace("</main>", note + "</main>", 1)
            path.write_text(text, encoding="utf-8")


def main():
    for locale in ("de", "ja"):
        build_faqs(locale)
        build_hubs(locale)
        build_guides(locale)
        build_news(locale)
    update_hreflang_and_home_cards()
    strengthen_short_locale_pages()
    counts = {locale: len(list((ROOT / locale).rglob("*.html"))) for locale in ("de", "ja")}
    print(f"Round 9 locale expansion complete: {counts}")


if __name__ == "__main__":
    main()
