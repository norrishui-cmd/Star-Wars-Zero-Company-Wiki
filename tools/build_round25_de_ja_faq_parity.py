#!/usr/bin/env python3
"""Round 25: localize the 50 Round-24 FAQ pages into German and Japanese."""

from __future__ import annotations

from html import escape
from pathlib import Path
import importlib.util
import json
import re


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = "2026-07-29"

spec = importlib.util.spec_from_file_location(
    "round24_builder", ROOT / "tools" / "build_round24_nav_news_faq.py"
)
r24 = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(r24)


DE_TSV = """
is-hawks-required-story-missions	Ist Hawks in Story-Missionen Pflicht?	Ja. Hawks muss in jeder Story-Mission eingesetzt werden.	In Gefechtsmissionen sind andere gültige Operator-Kombinationen möglich, ohne Hawks mitzunehmen.
can-skip-hawks-skirmish-missions	Kann man Hawks bei Gefechtsmissionen weglassen?	Ja. In Gefechtsmissionen ist Hawks nicht verpflichtend.	Für diese Missionen dürfen Spieler jede gültige Operator-Kombination einsetzen.
what-happens-if-hawks-dies	Was passiert, wenn Hawks im Kampf stirbt?	Die Mission scheitert automatisch und muss neu gestartet werden.	Hawks ist der spielbare Protagonist; sein Tod wird daher nicht wie ein gewöhnlicher permanenter Verlust im Kader fortgesetzt.
does-zero-company-support-mods	Unterstützt Star Wars Zero Company Mods?	Offizieller Mod-Support ist nicht geplant.	Das ist der aktuelle Stand der Entwickler und keine Aussage über inoffizielle Werkzeuge der Community.
are-cutscenes-real-time	Werden die Zwischensequenzen von Zero Company in Echtzeit gerendert?	Die meisten Zwischensequenzen werden in Echtzeit gerendert.	Einige wenige Ausnahmen sind vorgerendert; angepasste Charaktere sollen jedoch im Großteil des Spiels sichtbar bleiben.
what-is-operator-limit	Wie hoch ist das maximale Operator-Limit in The Den?	Das derzeit bestätigte Maximum liegt bei 20 Operatoren.	Die Kapazität steigt durch Den-Upgrades, Story-Fortschritt und den Beitritt vorgefertigter Operatoren.
how-many-operators-start	Wie viele Operatoren kann man zu Beginn haben?	Das anfängliche Maximum beträgt sieben Operatoren.	Die Kaderkapazität der Basis wächst später und startet nicht direkt beim Endwert von 20.
how-increase-operator-cap	Wie erhöht man das Operator-Limit?	Baue The Den aus und schreite in der Story voran.	Nach Angaben von EA tragen auch vorgefertigte Operatoren, die sich dem Trupp anschließen, zur Erweiterung bei.
how-many-weapon-classes	Wie viele Waffenklassen gibt es in Zero Company?	EA hat vier Waffenklassen bestätigt.	Die vollständige Waffenliste und die endgültigen Werte müssen nach Veröffentlichung geprüft werden.
how-many-cosmetic-models-per-weapon-class	Wie viele kosmetische Waffenmodelle gibt es pro Klasse?	Laut EA besitzt jede Waffenklasse vier bis sechs kosmetische Modelle.	Ohne Belege aus dem veröffentlichten Spiel dürfen diese Modelle nicht als eigene Balance-Klassen behandelt werden.
what-is-standard-squad-size	Wie groß ist ein Standardtrupp?	Das normale Trupplimit beträgt bis zu vier Operatoren.	Einige Missionen können zusätzliche steuerbare Charaktere über die regulären vier Einsatzplätze hinaus hinzufügen.
can-control-more-than-four-operators	Kann man mehr als vier Charaktere steuern?	Ja, in bestimmten Missionen.	Vier ist das normale Operator-Limit, einzelne Szenarien können aber weitere steuerbare Figuren hinzufügen.
what-is-intel-used-for	Wofür wird Intel auf der Galaxiekarte verwendet?	Intel wird ausgegeben, um Operationen durchzuführen.	Operationen kosten unterschiedlich viel Intel, wodurch zwischen verfügbaren Gelegenheiten abgewogen werden muss.
can-operations-expire	Können Operationen ablaufen?	Ja. Operationen auf der Galaxiekarte können ablaufen.	Spieler sollten nicht davon ausgehen, dass jede optionale Gelegenheit unbegrenzt verfügbar bleibt.
do-story-missions-become-mandatory	Werden Story-Missionen irgendwann verpflichtend?	Ja. Story-kritische Missionen werden ab einem bestimmten Punkt verpflichtend.	Die Strategieebene bietet Entscheidungen, erlaubt aber kein unbegrenztes Aufschieben der Hauptkampagne.
is-telrea-only-jedi-padawan	Ist Tel-Rea die einzige Jedi-Padawan-Operatorin?	Ja. Tel-Rea ist die einzige Operatorin der Klasse Jedi-Padawan.	Ihre einzigartige Klasse lässt sich nicht einfach über die normale Rekrutierung eigener Charaktere nachbilden.
will-missions-have-heavy-machinery	Enthalten Missionen Fahrzeuge oder schwere Maschinen?	Einige Missionen werden schwere Maschinen einbeziehen.	EA hat die genaue Liste der Fahrzeuge oder großen Droidenbegegnungen noch nicht veröffentlicht.
does-weather-affect-combat	Beeinflusst das Wetter Sicht oder Kampfeffizienz?	Nein. Wettereffekte im Kampf sind kosmetisch.	Das angekündigte Wetter verändert weder die Sichtweite noch die Effizienz des Trupps.
do-outfits-affect-gameplay	Verändern Outfits Werte oder Gameplay eines Charakters?	Nein. Outfits beeinflussen das Gameplay nicht.	Die äußere Erscheinung ist von Ausrüstung und taktischen Build-Entscheidungen getrennt.
is-arc-trooper-armor-deluxe-only	Ist die ARC-Trooper-Rüstung nur in der Deluxe Edition enthalten?	Das angekündigte ARC-Trooper-Rüstungsset gehört zum Republik-Kosmetikpaket der Deluxe Edition.	EA weist zugleich darauf hin, dass viele weitere kosmetische Optionen im Basisspiel verfügbar sind.
who-can-wear-mandalorian-armor	Kann jeder Operator mandalorianische Rüstung tragen?	Nein. Laut EA kann nur Cly die mandalorianische Rüstung tragen.	Andere Rüstungskosmetik kann breiter verfügbar sein, dieses charaktergebundene Outfit ist jedoch eingeschränkt.
does-zero-company-have-new-game-plus	Hat Zero Company einen New-Game-Plus-Modus?	Nein. New Game Plus ist zum Start nicht enthalten.	Bei späteren Spieldurchläufen werden dennoch ausgewählte Anpassungsoptionen freigeschaltet.
what-unlocks-on-later-playthroughs	Schalten spätere Spieldurchläufe etwas frei?	Ja. Einige Anpassungsoptionen werden in späteren Durchläufen freigeschaltet.	EA hat keine vollständige Liste veröffentlicht; dabei handelt es sich nicht um einen New-Game-Plus-Modus.
how-separatist-faction-fights	Wie sollte man sich auf Separatisten-Droiden vorbereiten?	EA empfiehlt, Ionenwaffen gegen Separatisten-Droiden in Betracht zu ziehen.	Endgültige Resistenzen und optimale Ausrüstungen müssen nach dem Release getestet werden.
how-infinite-coil-faction-fights	Wie fordert Infinite Coil den Trupp heraus?	Infinite-Coil-Einheiten besitzen unterschiedliche Fähigkeiten, durch die die Zielreihenfolge wichtig wird.	Die offizielle Aussage betrifft die Zielpriorität und ist keine endgültige Rangliste.
how-outlaw-faction-fights	Wie kämpfen die Outlaw-Gegner?	Outlaws können den Trupp durch zahlenmäßige Überlegenheit überwältigen.	Gebietskontrolle und Aktionsökonomie dürften wichtig sein, genaue Konter müssen jedoch nach Release geprüft werden.
when-can-recruit-astromechs	Wann kann man Astromechs rekrutieren?	Astromechs werden relativ früh im Spiel freigeschaltet.	EA hat dafür noch keine genaue Mission oder Zyklusnummer genannt.
can-build-full-astromech-squad	Kann man einen vollständigen Astromech-Trupp bauen?	Ja, nachdem die Astromech-Rekrutierung freigeschaltet wurde.	Hawks bleibt in Story-Missionen Pflicht; die übrigen verfügbaren Plätze können mit Astromechs besetzt werden.
can-recruit-separatist-droids	Kann man Separatisten-Kampfdroiden rekrutieren?	Nein. Separatisten-Droiden können nicht als Operatoren rekrutiert werden.	Das gilt, obwohl Zero Company Charaktere mit unterschiedlichen früheren Zugehörigkeiten aufnehmen kann.
does-zero-company-have-call-ins	Gibt es in Zero Company Unterstützungs-Call-ins?	Nein. Spezialisierte Call-ins sind nicht verfügbar.	EA verweist ausdrücklich auf Truppplanung statt auf Unterstützungsrufe wie LAAT-Hilfe.
can-evacuate-mission-early	Kann man eine Mission vorzeitig evakuieren?	EA hat keine Unterstützungsaktion für eine frühe Extraktion angekündigt.	Hawks muss überleben; sein Tod führt automatisch zum Scheitern der Mission.
can-custom-operators-have-backstories	Können eigene Operatoren Namen und Hintergrundgeschichten haben?	Ja. Rekrutierte Operatoren können eigene Namen und Hintergrundgeschichten erhalten.	Spitznamen werden nicht über einen XCOM-ähnlichen Fortschrittspool verdient.
can-customize-clone-armor	Können Klontruppen-Rüstung und Helme angepasst werden?	Ja. EA bestätigt mehrere Lackierungen und Muster für Helme, Rüstung und weitere Klontruppen-Optionen.	Das vollständige Kosmetikangebot wird anhand des veröffentlichten Spiels geprüft.
what-species-can-hawks-be	Welche Spezies kann Hawks angehören?	EA nennt unter anderem Devaronianer, Menschen, Togruta, Twi'lek und Zabrak und deutet weitere Optionen an.	Die Spezies ist Teil der Charakteridentität und verbessert nicht die Waffenfertigkeit.
how-many-planets-galaxy-map	Wie viele Planeten gibt es auf der Galaxiekarte?	Die Galaxiekarte umfasst mehr als 150 Planeten für mögliche strategische Operationen.	Viele dienen entscheidungsbasierten Ereignissen am Kartentisch und nicht als vollständige taktische Missionskarten.
how-many-tactical-mission-planets	Auf wie vielen Planeten finden taktische Missionen statt?	Laut EA erstrecken sich taktische Missionen über mehr als ein Dutzend einzigartige Planeten.	Diese Zahl unterscheidet sich von den über 150 strategischen Orten für Operationen.
difference-operations-tactical-missions	Was ist der Unterschied zwischen Operationen und taktischen Missionen?	Operationen werden auf der Galaxiekarte abgewickelt; taktische Missionen schicken einen Trupp auf eine Zielkarte.	Operationen können Belohnungen geben oder Inhalte freischalten, während taktische Missionen die rundenbasierten Kämpfe liefern.
what-mission-objectives-are-confirmed	Welche Missionsziele sind bestätigt?	Bestätigt sind Sabotage, Kampf, Rettung, Bergung und heldenzentrierte Story-Missionen.	EA nennt außerdem Extraktion und Nachschubverteidigung als Beispiele für das Begegnungsdesign.
can-operations-unlock-missions	Können Operationen neue Missionen freischalten?	Ja. Einige Operationen können weitere Operationen oder taktische Missionen freischalten.	Sie können außerdem sofortige Belohnungen und narrative Konsequenzen auslösen.
does-squad-choice-affect-bonds	Beeinflusst die Truppwahl Bonds und Story-Momente?	Ja. Die Zusammensetzung des Trupps kann Bonds und ausgewählte Story-Elemente verändern.	Das grundlegende Ende der Kampagne bleibt weitgehend gleich.
who-supports-zero-company-from-den	Welche Charaktere unterstützen das Team aus The Den?	Bennic, Runa, Neesh und Meevo sind als Unterstützungsfiguren in The Den bestätigt.	Ihre Aufgaben umfassen Aufklärung, Operationen, Finanzen, Ausrüstung, Schwarzmarkt, Pilotendienst und medizinische Unterstützung.
what-does-runa-do-at-den	Was macht Runa Blask in The Den?	Runa leitet Operationen und Finanzen und ist Hawks' rechte Hand.	Ihr SDCC-Profil beschreibt außerdem ihre schwierige Separatisten-Vergangenheit und ihren Widerstand gegen Infinite Coil.
what-does-neesh-do-at-den	Was macht Neesh Renark in The Den?	Neesh unterstützt die Waffenkammer und den Schwarzmarkt.	EA führt Neesh als Teil der benannten Unterstützungsbesetzung und nicht als Mitglied des Fronttrupps aus dem Trailer.
what-does-meevo-do-at-den	Was macht Meevo in The Den?	Meevo, auch M-3VO genannt, unterstützt Pilotendienst und Krankenstation.	D.C. Douglas ist als Sprecher des Charakters bestätigt.
who-voices-hawks-masculine	Wer spricht die männliche Version von Hawks?	Jonathan Freeman spricht die männliche Version von Hawks.	Die männliche und weibliche Darstellung des Protagonisten sind als getrennte offizielle Sprecherrollen aufgeführt.
who-voices-hawks-feminine	Wer spricht die weibliche Version von Hawks?	Erica Luttrell spricht die weibliche Version von Hawks.	Beide Hawks-Optionen stellen denselben vollständig anpassbaren Protagonisten dar.
who-voices-kundri-fathom	Wer spricht Kundri Fathom?	Rekha Sharma spricht Kundri Fathom.	Fathom führt Infinite Coil an und ist eine zentrale Gegenspielerin im Konflikt um die Schattenseuche.
who-voices-anakin-skywalker	Wer spricht Anakin Skywalker?	Matt Lanter spricht Anakin Skywalker.	StarWars.com bestätigte die Rückkehr des Clone-Wars-Sprechers in der SDCC-Besetzungsliste.
when-does-zero-company-soundtrack-release	Wann erscheint der Soundtrack von Zero Company?	Der Original-Soundtrack erscheint am 27. August 2026.	Das erste Stück von Gordy Haab, „Zero Company“, ist bereits vor dem vollständigen Album verfügbar.
is-zero-company-collectors-edition-announced	Gibt es eine Collectors' Edition von Star Wars Zero Company?	Ja. Auf der SDCC 2026 wurde eine Collectors' Edition angekündigt.	StarWars.com verweist Käufer an Limited Run Games; regionale Verfügbarkeit und Lieferbedingungen sollten dort geprüft werden.
""".strip()


JA_TSV = """
is-hawks-required-story-missions	ストーリーミッションではHawksが必須？	はい。すべてのストーリーミッションでHawksを出撃させる必要があります。	スカーミッシュミッションではHawksを必須とせず、別の有効なオペレーター編成を使用できます。
can-skip-hawks-skirmish-missions	スカーミッシュミッションでHawksを外せる？	はい。スカーミッシュミッションではHawksは必須ではありません。	その種のミッションでは、条件を満たす任意のオペレーター編成を使用できます。
what-happens-if-hawks-dies	戦闘中にHawksが死亡するとどうなる？	ミッションは自動的に失敗となり、再開する必要があります。	Hawksはプレイヤー主人公のため、通常の隊員のような永久ロストとして先へ進むことはできません。
does-zero-company-support-mods	Star Wars Zero CompanyはModに対応する？	公式Modサポートの予定はありません。	これは現在の公式見解であり、非公式なコミュニティツールについて断定するものではありません。
are-cutscenes-real-time	Zero Companyのカットシーンはリアルタイム描画？	大部分のカットシーンはリアルタイムで描画されます。	一部にプリレンダリング映像がありますが、カスタマイズしたキャラクターはゲーム全体に反映される想定です。
what-is-operator-limit	The Denで保有できるオペレーターの上限は？	現在確認されている最大数は20人です。	The Denのアップグレード、ストーリー進行、固有オペレーターの加入によって上限が増えます。
how-many-operators-start	ゲーム開始時に保有できるオペレーターは何人？	開始時の上限は7人です。	本部の隊員上限は後から拡張され、最初から最終上限の20人ではありません。
how-increase-operator-cap	オペレーターの上限を増やす方法は？	The Denをアップグレードし、ストーリーを進めます。	EAの説明では、固有オペレーターの加入も上限拡張の流れに関係します。
how-many-weapon-classes	Zero Companyの武器クラスは何種類？	EAは4種類の武器クラスを確認しています。	武器の完全な一覧と最終性能は、発売後に検証する必要があります。
how-many-cosmetic-models-per-weapon-class	各武器クラスの外見モデルは何種類？	EAによると、各武器クラスには4～6種類の外見モデルがあります。	製品版の根拠なしに、外見違いを個別の性能クラスとして扱うべきではありません。
what-is-standard-squad-size	標準的な部隊人数は？	通常の部隊上限は最大4人のオペレーターです。	一部のミッションでは、通常の4枠とは別に操作可能なキャラクターが加わる場合があります。
can-control-more-than-four-operators	4人を超えるキャラクターを操作できる？	はい、特定のミッションでは可能です。	通常の上限は4人ですが、一部のシナリオでは追加の操作キャラクターが参加します。
what-is-intel-used-for	銀河マップのIntelは何に使う？	IntelはOperationを実行するために消費します。	Operationごとに必要量が異なるため、どの機会を選ぶかという戦略判断が生まれます。
can-operations-expire	Operationには期限がある？	はい。銀河マップ上のOperationは期限切れになる場合があります。	すべての任意イベントが無期限に残るとは限りません。
do-story-missions-become-mandatory	ストーリーミッションは途中から必須になる？	はい。重要なストーリーミッションは一定段階で必須になります。	戦略レイヤーには選択肢がありますが、メインキャンペーンを無期限に先延ばしにはできません。
is-telrea-only-jedi-padawan	Tel-Reaは唯一のジェダイ・パダワンオペレーター？	はい。Tel-Reaは唯一のジェダイ・パダワンクラスのオペレーターです。	通常のカスタム採用で同じ固有クラスを再現することはできません。
will-missions-have-heavy-machinery	ミッションに乗り物や大型兵器は登場する？	一部のミッションでは大型機械が関わります。	EAは具体的な乗り物や大型ドロイドとの遭遇一覧をまだ公開していません。
does-weather-affect-combat	天候は視界や戦闘効率に影響する？	いいえ。戦闘中の天候効果は外見上の演出です。	発表済みの天候は、部隊の視界や効率を変化させません。
do-outfits-affect-gameplay	衣装はキャラクター性能やゲームプレイに影響する？	いいえ。衣装はゲームプレイに影響しません。	見た目の選択は、装備や戦術ビルドの判断とは分離されています。
is-arc-trooper-armor-deluxe-only	ARCトルーパーアーマーはDeluxe Edition限定？	発表済みのARCトルーパー・アーマーセットは、Deluxe Editionの共和国コスメパックに含まれます。	EAはベースゲームにも多数の外見オプションがあると説明しています。
who-can-wear-mandalorian-armor	全オペレーターがマンダロリアンアーマーを装備できる？	いいえ。EAによると、マンダロリアンアーマーを着用できるのはClyだけです。	他の防具外見は広く使える可能性がありますが、この衣装はキャラクター専用です。
does-zero-company-have-new-game-plus	Zero CompanyにNew Game Plusはある？	いいえ。発売時点ではNew Game Plusはありません。	ただし、2周目以降に一部のカスタマイズ項目が解放されます。
what-unlocks-on-later-playthroughs	2周目以降に解放される要素はある？	はい。後の周回で一部のカスタマイズ項目が解放されます。	EAは完全な解放一覧を公開しておらず、New Game Plusモードでもありません。
how-separatist-faction-fights	分離主義勢力のドロイドにはどう備える？	EAは分離主義勢力のドロイドに対してイオン武器を検討するよう示しています。	最終的な耐性と最適装備は、発売後の検証が必要です。
how-infinite-coil-faction-fights	Infinite Coilは部隊をどう追い詰める？	Infinite Coilの兵士は多様な能力を使うため、撃破順が重要になります。	公式情報が示すのは標的優先度の重要性であり、最終的なTier表ではありません。
how-outlaw-faction-fights	Outlawの敵はどう戦う？	Outlawは数の多さで部隊を圧倒することがあります。	エリア制御や行動効率が重要になる可能性がありますが、正確な対策は発売後に検証します。
when-can-recruit-astromechs	アストロメクはいつ採用できる？	アストロメクはゲームの比較的早い段階で解放されます。	EAは正確なミッション名やサイクル数をまだ公開していません。
can-build-full-astromech-squad	アストロメクだけの部隊を編成できる？	はい、アストロメク採用の解放後に可能です。	ストーリーミッションではHawksが必須ですが、残りの出撃枠をアストロメクで埋められます。
can-recruit-separatist-droids	分離主義勢力のバトル・ドロイドを採用できる？	いいえ。分離主義勢力のドロイドはオペレーターとして採用できません。	Zero Companyが多様な経歴の人物を採用できることとは別の制限です。
does-zero-company-have-call-ins	Zero Companyに戦場支援のCall-inはある？	いいえ。専用のCall-in支援はありません。	EAはLAAT支援のような外部要請ではなく、部隊編成で危険に備える方針を示しています。
can-evacuate-mission-early	ミッションから早期撤退できる？	EAは早期脱出用の支援アクションを発表していません。	Hawksは生存が必須で、死亡するとミッションは自動的に失敗します。
can-custom-operators-have-backstories	カスタムオペレーターに名前や経歴を設定できる？	はい。採用したオペレーターには名前と経歴を設定できます。	XCOMのような進行式ニックネーム候補から称号を獲得する仕組みではありません。
can-customize-clone-armor	クローントルーパーのアーマーやヘルメットは変更できる？	はい。EAはヘルメット、アーマーなどに複数の塗装やパターンがあると確認しています。	外見アイテムの完全な一覧は製品版で検証します。
what-species-can-hawks-be	Hawksはどの種族に設定できる？	EAはデヴァロニアン、人間、トグルータ、トワイレック、ザブラクなどを挙げ、ほかの選択肢も示しています。	種族はキャラクターの個性であり、武器習熟度を高めるものではありません。
how-many-planets-galaxy-map	銀河マップには何個の惑星がある？	銀河マップには戦略Operationの候補となる150以上の惑星があります。	多くは作戦テーブル上の選択イベントに使われ、完全な戦術ミッションマップではありません。
how-many-tactical-mission-planets	戦術ミッションがある惑星は何個？	EAによると、戦術ミッションは十数個を超える固有惑星で展開されます。	これは150以上ある戦略Operation地点とは別の数です。
difference-operations-tactical-missions	Operationと戦術ミッションの違いは？	Operationは銀河マップ上で解決し、戦術ミッションでは部隊を目標マップへ出撃させます。	Operationは報酬やコンテンツを解放し、戦術ミッションはターン制の戦闘を提供します。
what-mission-objectives-are-confirmed	確認済みのミッション目標は？	妨害、戦闘、救出、回収、ヒーロー中心の物語ミッションが確認されています。	EAは遭遇設計の例として脱出や物資防衛も挙げています。
can-operations-unlock-missions	Operationで新しいミッションを解放できる？	はい。一部のOperationは追加のOperationや戦術ミッションを解放します。	即時報酬や物語上の結果が発生する場合もあります。
does-squad-choice-affect-bonds	部隊編成はBondや物語の場面に影響する？	はい。部隊構成によってBondや一部の物語要素が変化します。	キャンペーン全体の結末はおおむね同じです。
who-supports-zero-company-from-den	The Denからチームを支援する人物は？	Bennic、Runa、Neesh、MeevoがThe Denの支援キャラクターとして確認されています。	担当は情報、作戦、財務、装備、闇市場、操縦、医療支援に及びます。
what-does-runa-do-at-den	Runa BlaskはThe Denで何を担当する？	Runaは作戦と財務を担当し、Hawksの右腕を務めます。	SDCCの紹介では、分離主義勢力での複雑な過去とInfinite Coilへの反発も示されました。
what-does-neesh-do-at-den	Neesh RenarkはThe Denで何を担当する？	Neeshは武器庫と闇市場を支援します。	EAはNeeshを、トレーラーの前線部隊ではなく名称付きの支援キャストとして挙げています。
what-does-meevo-do-at-den	MeevoはThe Denで何を担当する？	M-3VOとも呼ばれるMeevoは、操縦と医務室を支援します。	このキャラクターの声優はD.C. Douglasです。
who-voices-hawks-masculine	男性版Hawksの声優は？	男性版Hawksの声優はJonathan Freemanです。	主人公の男性版と女性版は、別々の公式キャストとして記載されています。
who-voices-hawks-feminine	女性版Hawksの声優は？	女性版Hawksの声優はErica Luttrellです。	どちらも同一の、自由にカスタマイズできる主人公Hawksを表します。
who-voices-kundri-fathom	Kundri Fathomの声優は？	Kundri Fathomの声優はRekha Sharmaです。	FathomはInfinite Coilを率い、シャドウ・プレイグを巡る争いの中心的な敵役です。
who-voices-anakin-skywalker	Anakin Skywalkerの声優は？	Anakin Skywalkerの声優はMatt Lanterです。	StarWars.comはSDCCのキャスト一覧でClone Wars版声優の続投を確認しました。
when-does-zero-company-soundtrack-release	Zero Companyのサウンドトラック発売日は？	オリジナルサウンドトラックは2026年8月27日に発売されます。	Gordy Haabによる最初の曲「Zero Company」は、アルバム全体に先行して公開済みです。
is-zero-company-collectors-edition-announced	Star Wars Zero CompanyにCollectors' Editionはある？	はい。SDCC 2026でCollectors' Editionが発表されました。	StarWars.comはLimited Run Gamesを案内しており、地域別の販売可否と配送条件は同店で確認が必要です。
""".strip()


def parse_tsv(raw: str) -> dict[str, tuple[str, str, str]]:
    result = {}
    for line in raw.splitlines():
        slug, question, answer, detail = line.split("\t")
        result[slug] = (question, answer, detail)
    return result


TRANSLATIONS = {"de": parse_tsv(DE_TSV), "ja": parse_tsv(JA_TSV)}

COPY = {
    "de": {
        "name": "Star Wars Zero Company Wiki auf Deutsch",
        "home": "Start",
        "database": "Datenbank",
        "guides": "Guides",
        "operations": "Operationen",
        "news": "News",
        "faq": "FAQ",
        "language": "Sprache",
        "crumb": "Neue verifizierte Antwort",
        "checked": "Geprüft am 29. Juli 2026",
        "quick": "Direkte Antwort",
        "source": "Was die offizielle Quelle bestätigt",
        "source_p1": "Die Antwort stützt sich auf {source}, veröffentlicht am {date}. Die Formulierung bewahrt die bestätigte Grenze der Quelle und macht daraus kein unbelegtes Funktionsversprechen.",
        "source_p2": "{detail} Dieser Unterschied ist wichtig, weil Zero Company erst am 27. August erscheint und genaue Freischaltungen, Schwierigkeitsmodifikatoren oder Plattformabweichungen teilweise noch nicht veröffentlicht sind.",
        "use": "So nutzt du diese Antwort",
        "use_p1": "Nutze die direkte Antwort für Kauf-, Trupp-, Missions- oder Kampagnenentscheidungen. Hängt eine Frage von einer finalen Zahl oder einer nicht genannten Ausnahme ab, prüfe zusätzlich den verlinkten Hub und das Datum der letzten Verifizierung.",
        "use_p2": "Diese URL beantwortet genau eine Suchintention. Die verwandten Fragen behandeln angrenzende Entscheidungen, statt dieselbe Antwort unter mehreren Überschriften zu wiederholen.",
        "boundary": "Prüfgrenze",
        "boundary_p": "Diese Seite gibt den aktuellen Stand aus erster Hand wieder. Sie verwendet keine Leaks, aus Trailern abgeleiteten Werte oder Regeln anderer Taktikspiele. Bei einer abweichenden Mitteilung von EA oder Lucasfilm wird die Antwort aktualisiert.",
        "related": "Verwandte Fragen",
        "browse": "Alle 69 deutschen FAQ öffnen",
        "browse_note": "Kader, Systeme, Missionen, Story, Editionen und Release",
        "footer": "Inoffizielles, quellenbasiertes FAQ",
        "sources": "Quellenrichtlinie",
        "hub_title": "69 verifizierte FAQ-Antworten auf Deutsch",
        "hub_desc": "Direkte, quellenbasierte Antworten zu Kader, Missionen, Systemen, Story, Editionen und Veröffentlichung von Star Wars Zero Company.",
        "hub_lead": "Die deutsche FAQ-Sammlung umfasst jetzt 69 eigenständige Antworten. Diese 50 neuen Seiten übertragen die offiziellen Angaben aus dem Juli-Q&A und der SDCC-Präsentation vollständig ins Deutsche.",
        "hub_section": "50 neue verifizierte Antworten",
    },
    "ja": {
        "name": "スター・ウォーズ ゼロ・カンパニー攻略Wiki",
        "home": "ホーム",
        "database": "データベース",
        "guides": "攻略",
        "operations": "Operation",
        "news": "ニュース",
        "faq": "FAQ",
        "language": "言語",
        "crumb": "新しい確認済み回答",
        "checked": "2026年7月29日確認",
        "quick": "結論",
        "source": "公式情報で確認できること",
        "source_p1": "この回答は、{date}公開の{source}に基づきます。公式文の範囲を保ち、未確認の機能まで拡大解釈していません。",
        "source_p2": "{detail} Zero Companyは8月27日の発売前であり、正確な解放時期、難易度補正、機種別の挙動がまだ公開されていない場合があるため、この区別が重要です。",
        "use": "この回答の使い方",
        "use_p1": "購入、部隊編成、ミッション、キャンペーンの判断には上の結論を使えます。最終数値や未公開の例外に左右される場合は、関連ハブと発売後の確認日も確認してください。",
        "use_p2": "このURLは1つの検索意図だけを扱います。下の関連記事は、同じ回答を別タイトルで繰り返さず、隣接する判断を補います。",
        "boundary": "検証範囲",
        "boundary_p": "このページは現在の一次情報を掲載しています。リーク、トレーラーから推測した数値、他のタクティクスゲームのルールには依存しません。EAまたはLucasfilmが異なる内容を発表した場合は更新します。",
        "related": "関連する質問",
        "browse": "日本語FAQ 69件をすべて見る",
        "browse_note": "部隊、システム、ミッション、物語、エディション、発売情報",
        "footer": "非公式・公式情報リンク付きFAQ",
        "sources": "情報源ポリシー",
        "hub_title": "Star Wars Zero Company 日本語FAQ 69問",
        "hub_desc": "部隊、ミッション、システム、物語、エディション、発売情報を扱う、一次情報に基づく日本語FAQです。",
        "hub_lead": "日本語FAQは69件の独立した回答に拡大しました。今回の50ページは、7月の公式Q&AとSDCC発表の内容を英語版と同じ構造で日本語化しています。",
        "hub_section": "新しい確認済み回答 50件",
    },
}

SOURCE_LOCAL = {
    "de": {
        "qna": ("EA-Community-Q&A", "21. Juli 2026"),
        "sdcc": ("StarWars.com-Bericht zur SDCC 2026", "26. Juli 2026"),
        "gameplay": ("EA-Gameplay-Übersicht", "9. Juni 2026"),
        "preorder": ("EA-Ankündigung zu Vorbestellung und Editionen", "5. Juni 2026"),
    },
    "ja": {
        "qna": ("EAコミュニティQ&A", "2026年7月21日"),
        "sdcc": ("StarWars.comのSDCC 2026レポート", "2026年7月26日"),
        "gameplay": ("EAゲームプレイ概要", "2026年6月9日"),
        "preorder": ("EA予約・エディション発表", "2026年6月5日"),
    },
}

LANG_LABELS = [
    ("en", "English", ""),
    ("de", "Deutsch", "de"),
    ("fr", "Français", "fr"),
    ("it", "Italiano", "it"),
    ("es", "Español", "es"),
    ("ja", "日本語", "ja"),
    ("ko", "한국어", "ko"),
    ("pl", "Polski", "pl"),
    ("pt-BR", "Português", "pt-br"),
    ("zh-Hans", "简体中文", "zh-cn"),
    ("zh-Hant", "繁體中文", "zh-tw"),
]


def exact_url(locale: str, slug: str) -> str:
    return f"/{locale}/questions/{slug}.html" if locale else f"/questions/{slug}.html"


def alternates(slug: str) -> str:
    return "".join([
        f'<link rel="alternate" hreflang="en" href="{SITE}{exact_url("", slug)}">',
        f'<link rel="alternate" hreflang="de" href="{SITE}{exact_url("de", slug)}">',
        f'<link rel="alternate" hreflang="ja" href="{SITE}{exact_url("ja", slug)}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE}{exact_url("", slug)}">',
    ])


def language_menu(locale: str, slug: str) -> str:
    links = []
    for code, label, prefix in LANG_LABELS:
        href = exact_url(prefix, slug) if prefix in {"de", "ja"} else (exact_url("", slug) if not prefix else f"/{prefix}/")
        current = ' aria-current="page"' if prefix == locale else ""
        links.append(f'<a href="{href}" lang="{code}"{current}>{label}</a>')
    return (
        '<details class="lang"><summary>Language</summary><div>'
        + "".join(links)
        + "</div></details>"
    )


def header(locale: str, slug: str) -> str:
    c = COPY[locale]
    return (
        '<header class="top"><div class="wrap">'
        f'<a class="brand" href="/{locale}/">{escape(c["name"])}</a><nav>'
        f'<a href="/{locale}/database/">{escape(c["database"])}</a>'
        f'<a href="/{locale}/guides/">{escape(c["guides"])}</a>'
        f'<a href="/operations/">{escape(c["operations"])}</a>'
        f'<a href="/{locale}/news/">{escape(c["news"])}</a>'
        f'<a href="/{locale}/questions/">{escape(c["faq"])}</a>'
        f'{language_menu(locale, slug)}</nav></div></header>'
    )


def faq_page(locale: str, item, related_items) -> str:
    slug, _, _, _, source_key, _ = item
    question, answer, detail = TRANSLATIONS[locale][slug]
    c = COPY[locale]
    source_name, source_date = SOURCE_LOCAL[locale][source_key]
    source_url = r24.SOURCES[source_key][2]
    route = exact_url(locale, slug)
    description = f"{question} {answer} {detail}"
    related = "".join(
        f'<a class="card" href="{exact_url(locale, other[0])}"><strong>{escape(TRANSLATIONS[locale][other[0]][0])}</strong>'
        f'<br><span class="muted">{escape(TRANSLATIONS[locale][other[0]][1])}</span></a>'
        for other in related_items[:3]
    )
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "url": SITE + route,
        "inLanguage": locale,
        "dateModified": TODAY,
        "mainEntity": [{
            "@type": "Question",
            "name": question,
            "acceptedAnswer": {"@type": "Answer", "text": f"{answer} {detail}"},
        }],
    }
    body = f"""
<section class="hero"><div class="crumb"><a href="/{locale}/questions/">FAQ</a> / {escape(c["crumb"])}</div>
<p class="eyebrow">{escape(c["checked"])}</p><h1>{escape(question)}</h1><p class="lead">{escape(answer)}</p></section>
<section class="block answer"><h2>{escape(c["quick"])}</h2><p><strong>{escape(answer)}</strong></p><p>{escape(detail)}</p></section>
<section class="block"><h2>{escape(c["source"])}</h2>
<p>{c["source_p1"].format(source=f'<a href="{source_url}" rel="nofollow">{escape(source_name)}</a>', date=escape(source_date))}</p>
<p>{escape(c["source_p2"].format(detail=detail))}</p></section>
<section class="block"><h2>{escape(c["use"])}</h2><p>{escape(c["use_p1"])}</p><p>{escape(c["use_p2"])}</p></section>
<section class="block note"><h2>{escape(c["boundary"])}</h2><p>{escape(c["boundary_p"])}</p></section>
<section><h2>{escape(c["related"])}</h2><div class="grid">{related}
<a class="card" href="/{locale}/questions/"><strong>{escape(c["browse"])}</strong><br><span class="muted">{escape(c["browse_note"])}</span></a>
</div></section>
"""
    return (
        f'<!doctype html><html lang="{locale}"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{escape(question)} | Zero Company FAQ</title>"
        f'<meta name="description" content="{escape(description)}"><meta name="robots" content="index,follow">'
        f'<link rel="canonical" href="{SITE}{route}">{alternates(slug)}'
        f'<meta property="og:type" content="article"><meta property="og:url" content="{SITE}{route}">'
        f'<meta property="og:title" content="{escape(question)}"><meta property="og:description" content="{escape(description)}">'
        f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
        f"<style>{r24.STYLE}</style>{r24.ADS_META}{r24.ADS_SCRIPT}</head><body>"
        f'{header(locale, slug)}<main class="wrap">{body}</main>'
        f'<footer><div class="wrap">{escape(c["footer"])} · '
        f'<a href="/about/sources-and-citations.html">{escape(c["sources"])}</a></div></footer></body></html>'
    )


def update_english_alternates(slug: str) -> None:
    path = ROOT / "questions" / f"{slug}.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(r'<link rel="alternate" hreflang="(?:en|de|ja|x-default)"[^>]*>', "", text)
    text = text.replace('<meta property="og:type"', alternates(slug) + '<meta property="og:type"', 1)
    path.write_text(text, encoding="utf-8")


def update_hub(locale: str) -> None:
    c = COPY[locale]
    path = ROOT / locale / "questions" / "index.html"
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(r"<!-- ROUND25_FAQ_START -->.*?<!-- ROUND25_FAQ_END -->", "", text, flags=re.S)
    cards = "".join(
        f'<a class="card" href="{exact_url(locale, item[0])}"><strong>{escape(TRANSLATIONS[locale][item[0]][0])}</strong>'
        f'<br><span class="muted">{escape(TRANSLATIONS[locale][item[0]][1])}</span></a>'
        for item in r24.NEW_FAQS
    )
    block = (
        '<!-- ROUND25_FAQ_START --><section class="block answer">'
        f'<p class="eyebrow">{escape(c["checked"])}</p><h2>{escape(c["hub_section"])}</h2>'
        f'<p>{escape(c["hub_lead"])}</p></section><section><div class="grid">{cards}</div></section>'
        '<!-- ROUND25_FAQ_END -->'
    )
    text = re.sub(r"</main>", block + "</main>", text, count=1, flags=re.I)
    title = escape(c["hub_title"])
    desc = escape(c["hub_desc"])
    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content=".*?">', f'<meta name="description" content="{desc}">', text, count=1, flags=re.S)
    text = text.replace("50 FAQ-Antworten – deutscher Einstieg", c["hub_title"])
    text = text.replace("よくある質問・日本語ガイド", c["hub_title"])
    text = re.sub(
        r'<p class="lead">.*?</p>',
        f'<p class="lead">{escape(c["hub_lead"])}</p>',
        text,
        count=1,
        flags=re.S,
    )
    text = text.replace("englische FAQ-Zentrum enthält zusätzlich alle 50", "deutsche FAQ-Sammlung enthält jetzt 69")
    text = text.replace("英語版の全50 FAQを見る", "日本語FAQ 69件をすべて見る")
    path.write_text(text, encoding="utf-8")


def write_report() -> None:
    report = """# Round 25 — German and Japanese FAQ Parity

Updated: July 29, 2026

## Delivered

- Added 50 German FAQ pages and 50 Japanese FAQ pages.
- Localized every Round 24 FAQ question, direct answer, evidence detail, source note and related-question card.
- Reused the exact Round 24 English FAQ stylesheet and component order.
- Added reciprocal English/German/Japanese hreflang clusters plus x-default.
- Expanded both locale FAQ hubs to 69 indexable answers.
- Preserved the evidence boundary of the EA Q&A and StarWars.com SDCC report.

## Expected totals after sitemap rebuild

- New localized URLs: 100
- Sitemap quality URLs: 1,476
- HTML pages: 1,712
- German HTML pages: 155
- Japanese HTML pages: 155
"""
    (ROOT / "ROUND-25-DE-JA-FAQ-PARITY.md").write_text(report, encoding="utf-8")


def main() -> None:
    slugs = {item[0] for item in r24.NEW_FAQS}
    assert len(slugs) == 50
    assert set(TRANSLATIONS["de"]) == slugs
    assert set(TRANSLATIONS["ja"]) == slugs
    for locale in ("de", "ja"):
        output = ROOT / locale / "questions"
        output.mkdir(parents=True, exist_ok=True)
        for item in r24.NEW_FAQS:
            tags = set(item[5])
            related = [
                other for other in r24.NEW_FAQS
                if other[0] != item[0] and tags & set(other[5])
            ][:3]
            (output / f"{item[0]}.html").write_text(
                faq_page(locale, item, related), encoding="utf-8"
            )
        update_hub(locale)
    for slug in slugs:
        update_english_alternates(slug)
    write_report()
    print("Round 25 built: 50 German and 50 Japanese FAQ pages.")


if __name__ == "__main__":
    main()
