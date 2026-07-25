#!/usr/bin/env python3
"""Round 14: localize ten officially confirmed mechanics with English visual parity."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = date.today().isoformat()
SOURCE = "https://www.ea.com/games/starwars/zero-company/news/answering-biggest-questions"

LOCALES = (
    ("en", "en", "English"), ("de", "de", "Deutsch"), ("fr", "fr", "Français"),
    ("it", "it", "Italiano"), ("es", "es", "Español"), ("ja", "ja", "日本語"),
    ("ko", "ko", "한국어"), ("pl", "pl", "Polski"),
    ("zh-cn", "zh-Hans", "简体中文"), ("zh-tw", "zh-Hant", "繁體中文"),
    ("pt-br", "pt-BR", "Português (Brasil)"),
)

SLUGS = (
    "operator-limit-20",
    "standard-squad-limit-four",
    "four-weapon-classes",
    "intel-operation-costs",
    "story-missions-become-obligatory",
    "no-new-game-plus-at-launch",
    "weather-cosmetic-only",
    "outfits-no-gameplay-stats",
    "tel-rea-only-jedi-padawan",
    "cannot-recruit-separatist-droids",
)

# title, direct answer, practical consequence
COPY = {
    "de": [
        ("Wie hoch ist das Operator-Limit im Hauptquartier?", "Das aktuelle Maximum im Hauptquartier beträgt 20 Operatoren. Die Kampagne beginnt jedoch mit einem Limit von sieben.", "The-Den-Upgrades, Storyfortschritt und neu beitretende vorgegebene Operatoren erhöhen die Kapazität. Das HQ-Limit beschreibt den gesamten Kader und nicht die Größe eines Einsatzteams."),
        ("Wie viele Operatoren können in einem Standardtrupp eingesetzt werden?", "Ein Standardtrupp umfasst höchstens vier Operatoren.", "Bestimmte Missionen können zusätzliche Figuren unter Spielersteuerung stellen. Das ändert die normale Vierergrenze für die selbst zusammengestellte Einsatzgruppe nicht."),
        ("Wie viele Waffenklassen gibt es?", "EA bestätigt vier Waffenklassen. Innerhalb jeder Klasse sind vier bis sechs kosmetische Modelle vorgesehen.", "Eine Waffenklasse bestimmt die spielerische Kategorie; das gewählte Modell ist eine optische Variante. Unveröffentlichte Namen, Schadenswerte oder Seltenheiten werden hier nicht ergänzt."),
        ("Wie funktionieren Intel-Kosten für Operations?", "Operations auf der Galaxiekarte kosten unterschiedlich viel Intel.", "Zwischen Missionen steht nur ein bestimmtes Intel-Budget zur Verfügung und Operations können verfallen. Deshalb sollte die Auswahl zu Spielstil, Belohnungsziel und verbleibender Zeit passen."),
        ("Werden Story-Missionen irgendwann verpflichtend?", "Ja. Storykritische Missionen werden nach einem bestimmten Punkt verpflichtend.", "Operations und andere Missionen können verfallen; die Hauptgeschichte lässt sich daher nicht unbegrenzt aufschieben. Die konkrete Zahl der Zyklen ist noch nicht veröffentlicht."),
        ("Gibt es zum Start New Game Plus?", "Nein. Star Wars Zero Company bietet kein New Game Plus.", "Spätere Durchläufe schalten dennoch bestimmte Anpassungsoptionen frei. Das ist ein Wiederspielbonus, aber kein Modus, der den kompletten Fortschritt wie klassisches New Game Plus übernimmt."),
        ("Beeinflusst das Wetter Sicht oder Effizienz?", "Nein. Wettereffekte im Kampf sind rein kosmetisch.", "Regen, Staub oder andere Effekte verändern laut Entwicklerantwort weder Sicht noch Effizienz des Trupps. Spieler müssen deshalb keine wetterabhängigen Genauigkeitswerte einplanen."),
        ("Verleihen Outfits Spielwerte?", "Nein. Outfits beeinflussen das Gameplay nicht.", "Kleidung dient der Darstellung des eigenen Teams. Sie ist von Rüstung, Waffen und Fähigkeiten zu unterscheiden und gewährt keine bestätigten Kampfboni."),
        ("Ist Tel-Rea die einzige Jedi-Padawan-Operatorin?", "Ja. Tel-Rea ist die einzige Operatorin der Klasse Jedi Padawan.", "Es können keine weiteren Jedi-Padawane erstellt oder rekrutiert werden. Wer mit permanentem Tod spielt, sollte sie daher besonders vorsichtig einsetzen."),
        ("Kann man separatistische Kampfdroiden rekrutieren?", "Nein. Separatistische Droiden können nicht als Operatoren rekrutiert werden.", "B1-, B2- und andere separatistische Einheiten bleiben Gegner und werden nicht durch Betäubung oder Hacking zu Kaderfiguren. Rekrutierbare Astromechs sind ein getrenntes System."),
    ],
    "fr": [
        ("Quelle est la limite d’agents au quartier général ?", "La limite actuelle du quartier général est de 20 agents, mais la campagne commence avec un maximum de sept.", "Les améliorations de The Den, la progression de l’histoire et l’arrivée d’agents écrits augmentent la capacité. Cette limite concerne l’effectif total, pas l’escouade déployée."),
        ("Combien d’agents composent une escouade standard ?", "Une escouade standard peut compter jusqu’à quatre agents.", "Certaines missions permettent de contrôler des personnages supplémentaires. Cette exception ne remplace pas la limite normale de quatre membres choisis pour le déploiement."),
        ("Combien existe-t-il de classes d’armes ?", "EA confirme quatre classes d’armes, avec quatre à six modèles cosmétiques dans chacune.", "La classe correspond à la fonction de l’arme, tandis que le modèle change son apparence. Les noms, dégâts et raretés non publiés ne sont pas inventés sur cette page."),
        ("Comment fonctionnent les coûts d’Intel des Operations ?", "Chaque Operation sur la carte galactique coûte une quantité variable d’Intel.", "Le budget disponible entre les missions est limité et les Operations peuvent expirer. Il faut donc choisir selon son style, la récompense recherchée et le temps restant."),
        ("Les missions principales deviennent-elles obligatoires ?", "Oui. Les missions essentielles à l’histoire deviennent obligatoires après un certain point.", "Les Operations et missions peuvent expirer : il n’est donc pas possible de repousser indéfiniment la progression principale. Le nombre exact de cycles n’est pas publié."),
        ("Y a-t-il un mode New Game Plus au lancement ?", "Non. Star Wars Zero Company ne propose pas de New Game Plus.", "Des options de personnalisation sont toutefois débloquées lors des parties suivantes. Il s’agit d’un bonus de rejouabilité, pas d’un transfert complet de progression."),
        ("La météo affecte-t-elle la visibilité ou l’efficacité ?", "Non. Les effets météorologiques en combat sont uniquement cosmétiques.", "Pluie, poussière ou autres effets ne modifient ni la visibilité ni l’efficacité de l’escouade selon l’équipe. Aucun malus de précision lié à la météo n’est donc confirmé."),
        ("Les tenues donnent-elles des statistiques ?", "Non. Les tenues n’ont aucun effet sur le gameplay.", "Les vêtements servent à personnaliser l’apparence de l’équipe. Ils sont distincts des armes, armures et capacités et n’accordent aucun bonus de combat confirmé."),
        ("Tel-Rea est-elle la seule Jedi Padawan ?", "Oui. Tel-Rea est l’unique agent de la classe Jedi Padawan.", "Il n’est pas possible de créer ou recruter un autre Padawan. Dans une campagne avec mort permanente, sa survie demande donc une attention particulière."),
        ("Peut-on recruter des droïdes séparatistes ?", "Non. Les droïdes séparatistes ne peuvent pas rejoindre l’effectif comme agents.", "Les B1, B2 et autres unités séparatistes restent des ennemis : les étourdir ou les pirater ne les rend pas recrutables. Les astromécanos suivent un système séparé."),
    ],
    "it": [
        ("Qual è il limite di operatori al quartier generale?", "Il limite attuale al quartier generale è di 20 operatori, ma la campagna inizia con un massimo di sette.", "Gli upgrade di The Den, la storia e l’ingresso di operatori predefiniti aumentano la capacità. È il limite dell’intero roster, non della squadra schierata."),
        ("Quanti operatori entrano in una squadra standard?", "La squadra standard può includere fino a quattro operatori.", "Alcune missioni permettono di controllare personaggi aggiuntivi. L’eccezione non cambia il normale limite di quattro membri scelti per lo schieramento."),
        ("Quante classi di armi ci sono?", "EA conferma quattro classi di armi, con quattro-sei modelli cosmetici per classe.", "La classe identifica la funzione di gioco, mentre il modello modifica l’aspetto. Nomi, danni e rarità non pubblicati non vengono aggiunti come se fossero dati finali."),
        ("Come funzionano i costi Intel delle Operations?", "Ogni Operation sulla Mappa Galattica costa una quantità diversa di Intel.", "Tra le missioni il budget è limitato e le Operations possono scadere. La scelta deve quindi riflettere stile di gioco, ricompensa desiderata e tempo rimasto."),
        ("Le missioni della storia diventano obbligatorie?", "Sì. Le missioni essenziali per la storia diventano obbligatorie dopo un certo punto.", "Operations e missioni possono scadere, quindi la trama principale non può essere rimandata per sempre. Il numero esatto di cicli non è stato pubblicato."),
        ("Ci sarà New Game Plus al lancio?", "No. Star Wars Zero Company non include New Game Plus.", "Le partite successive sbloccano comunque alcune opzioni estetiche. È un incentivo alla rigiocabilità, non un trasferimento completo dei progressi."),
        ("Il meteo influenza visibilità o efficienza?", "No. Gli effetti atmosferici in combattimento sono soltanto cosmetici.", "Pioggia, polvere e altri effetti non modificano visibilità o efficienza della squadra secondo gli sviluppatori. Non è confermata alcuna penalità di precisione."),
        ("Gli abiti forniscono statistiche?", "No. Gli abiti non modificano il gameplay.", "L’abbigliamento personalizza l’aspetto della squadra. È distinto da armature, armi e abilità e non offre bonus di combattimento confermati."),
        ("Tel-Rea è l’unica Jedi Padawan?", "Sì. Tel-Rea è l’unica operatrice della classe Jedi Padawan.", "Non è possibile creare o reclutare altri Padawan. In una campagna con morte permanente è quindi una risorsa da proteggere con attenzione."),
        ("Si possono reclutare droidi separatisti?", "No. I droidi separatisti non possono essere reclutati come operatori.", "B1, B2 e altre unità restano nemici: stordirle o hackerarle non le aggiunge al roster. Gli astromech reclutabili appartengono a un sistema diverso."),
    ],
    "es": [
        ("¿Cuál es el límite de agentes en el cuartel general?", "El límite actual del cuartel general es de 20 agentes, aunque la campaña empieza con un máximo de siete.", "Las mejoras de The Den, el progreso de la historia y la llegada de agentes escritos amplían la capacidad. Es el límite de toda la plantilla, no del equipo desplegado."),
        ("¿Cuántos agentes caben en un pelotón estándar?", "Un pelotón estándar admite hasta cuatro agentes.", "Algunas misiones permiten controlar personajes adicionales. Esa excepción no sustituye el límite normal de cuatro miembros seleccionados para el despliegue."),
        ("¿Cuántas clases de armas hay?", "EA confirma cuatro clases de armas y entre cuatro y seis modelos cosméticos dentro de cada clase.", "La clase define la función jugable; el modelo cambia la apariencia. Esta página no inventa nombres, daños o rarezas que todavía no se han publicado."),
        ("¿Cómo funcionan los costes de Intel de las Operations?", "Cada Operation del Mapa Galáctico consume una cantidad distinta de Intel.", "El presupuesto entre misiones es limitado y las Operations pueden caducar. Conviene priorizar según estilo, recompensa buscada y tiempo disponible."),
        ("¿Las misiones de historia se vuelven obligatorias?", "Sí. Las misiones críticas para la historia pasan a ser obligatorias después de cierto punto.", "Operations y misiones pueden caducar, así que la trama principal no puede aplazarse indefinidamente. No se ha publicado el número exacto de ciclos."),
        ("¿Hay New Game Plus en el lanzamiento?", "No. Star Wars Zero Company no incluye New Game Plus.", "Las partidas posteriores sí desbloquean determinadas opciones de personalización. Es un premio de rejugabilidad, no un modo que transfiera todo el progreso."),
        ("¿El clima afecta a la visibilidad o la eficacia?", "No. Los efectos meteorológicos del combate son únicamente cosméticos.", "Lluvia, polvo u otros efectos no cambian la visibilidad ni la eficacia del pelotón según el equipo. No hay penalización de precisión climática confirmada."),
        ("¿Los atuendos otorgan estadísticas?", "No. Los atuendos no influyen en la jugabilidad.", "La ropa sirve para personalizar el aspecto del equipo. Es distinta de armaduras, armas y habilidades y no concede bonificaciones de combate confirmadas."),
        ("¿Tel-Rea es la única Jedi Padawan?", "Sí. Tel-Rea es la única agente de la clase Jedi Padawan.", "No se pueden crear ni reclutar otros Padawan. En una campaña con muerte permanente, protegerla requiere una atención especial."),
        ("¿Se pueden reclutar droides separatistas?", "No. Los droides separatistas no pueden reclutarse como agentes.", "B1, B2 y otras unidades siguen siendo enemigos: aturdirlas o piratearlas no las incorpora a la plantilla. Los astromecánicos reclutables usan otro sistema."),
    ],
    "ja": [
        ("本部に所属できるオペレーターの上限は？", "本部の現在の上限は20人ですが、キャンペーン開始時は最大7人です。", "The Denのアップグレード、物語の進行、固有オペレーターの加入によって枠が増えます。これは全所属人数の上限であり、任務に出す部隊人数とは別です。"),
        ("標準部隊には何人まで配置できる？", "標準の出撃部隊は最大4人です。", "一部の任務では追加キャラクターを操作できますが、通常の編成で選択できる4人という上限が恒久的に増えるわけではありません。"),
        ("武器クラスはいくつある？", "EAは4種類の武器クラスを確認しており、各クラスには4～6種類の外観モデルがあります。", "クラスは戦闘上のカテゴリー、モデルは見た目の選択肢です。未公開の武器名、ダメージ値、レア度を確定情報として追加しません。"),
        ("Operationに必要なIntelはどう機能する？", "銀河マップの各Operationは異なる量のIntelを消費します。", "任務間で使えるIntelには限りがあり、Operationには期限があります。プレイスタイル、狙う報酬、残り時間を比べて選ぶ必要があります。"),
        ("ストーリー任務は強制になる？", "はい。物語上重要な任務は一定時点を過ぎると必須になります。", "Operationや任務には期限があるため、メインストーリーを無期限に先送りできません。必須になるまでの正確なCycle数は未公開です。"),
        ("発売時にNew Game Plusはある？", "いいえ。Star Wars Zero CompanyにNew Game Plusはありません。", "ただし2周目以降では一部のカスタマイズ項目が解除されます。これは周回特典であり、進行状況を丸ごと引き継ぐモードではありません。"),
        ("天候は視界や効率に影響する？", "いいえ。戦闘中の天候効果は見た目だけです。", "雨や砂塵などは部隊の視界や効率を変化させないと開発チームが回答しています。天候による命中率低下は確認されていません。"),
        ("衣装に能力値ボーナスはある？", "いいえ。衣装はゲームプレイに影響しません。", "衣服は部隊の外見を変えるためのものです。防具、武器、アビリティとは別で、確認済みの戦闘ボーナスはありません。"),
        ("Tel-Reaは唯一のJedi Padawan？", "はい。Tel-ReaはJedi Padawanクラスで唯一のオペレーターです。", "別のPadawanを作成したり採用したりすることはできません。永久死ありのキャンペーンでは特に慎重に守る価値があります。"),
        ("分離主義勢力のバトル・ドロイドを採用できる？", "いいえ。分離主義勢力のドロイドをオペレーターとして採用することはできません。", "B1やB2などを気絶・ハッキングしても所属メンバーにはなりません。採用可能なアストロメクは別のシステムです。"),
    ],
    "ko": [
        ("본부 오퍼레이터 한도는 몇 명인가요?", "현재 본부 한도는 20명이지만 캠페인은 최대 7명으로 시작합니다.", "The Den 업그레이드, 스토리 진행, 고유 오퍼레이터 합류로 수용 인원이 늘어납니다. 이는 전체 명단 한도이며 임무에 투입하는 분대 규모와 다릅니다."),
        ("표준 분대에는 몇 명까지 배치할 수 있나요?", "표준 분대는 최대 4명의 오퍼레이터로 구성됩니다.", "일부 임무에서는 추가 캐릭터를 조종할 수 있습니다. 그러나 일반적으로 직접 선택하는 배치 인원 4명 제한이 영구적으로 늘어나는 것은 아닙니다."),
        ("무기 클래스는 몇 개인가요?", "EA는 4개 무기 클래스를 확인했으며 각 클래스에는 4~6개의 외형 모델이 있습니다.", "클래스는 전투 기능을, 모델은 외형을 뜻합니다. 공개되지 않은 무기 이름, 피해량, 희귀도는 확정 정보로 작성하지 않습니다."),
        ("Operation의 Intel 비용은 어떻게 작동하나요?", "은하 지도에서 각 Operation은 서로 다른 양의 Intel을 소비합니다.", "임무 사이에 쓸 수 있는 예산은 제한되어 있고 Operation은 만료될 수 있습니다. 플레이 방식, 원하는 보상, 남은 시간을 비교해 선택해야 합니다."),
        ("스토리 임무는 의무적으로 진행해야 하나요?", "네. 스토리 핵심 임무는 일정 시점이 지나면 의무 임무가 됩니다.", "Operation과 임무에는 만료가 있으므로 메인 스토리를 무기한 미룰 수 없습니다. 의무화까지의 정확한 Cycle 수는 공개되지 않았습니다."),
        ("출시 시 New Game Plus가 있나요?", "아니요. Star Wars Zero Company에는 New Game Plus가 없습니다.", "후속 플레이에서는 일부 커스터마이즈 옵션이 열립니다. 이는 재플레이 보상이지 모든 진행도를 계승하는 전통적인 New Game Plus 모드는 아닙니다."),
        ("날씨가 시야나 효율에 영향을 주나요?", "아니요. 전투 중 날씨 효과는 순수하게 시각적입니다.", "비나 먼지 같은 효과는 분대의 시야나 효율을 바꾸지 않는다고 개발진이 답했습니다. 날씨에 따른 명중률 페널티는 확인되지 않았습니다."),
        ("의상이 능력치를 제공하나요?", "아니요. 의상은 게임플레이에 영향을 주지 않습니다.", "의상은 팀의 외형을 꾸미는 요소입니다. 방어구, 무기, 능력과 구분되며 확인된 전투 보너스를 제공하지 않습니다."),
        ("Tel-Rea가 유일한 Jedi Padawan인가요?", "네. Tel-Rea는 Jedi Padawan 클래스의 유일한 오퍼레이터입니다.", "다른 Padawan을 제작하거나 모집할 수 없습니다. 영구 사망 캠페인에서는 특히 신중하게 보호할 필요가 있습니다."),
        ("분리주의 전투 드로이드를 모집할 수 있나요?", "아니요. 분리주의 드로이드는 오퍼레이터로 모집할 수 없습니다.", "B1, B2 등은 기절시키거나 해킹해도 명단에 들어오지 않는 적입니다. 모집 가능한 아스트로메크는 별도의 시스템입니다."),
    ],
    "pl": [
        ("Jaki jest limit Operatorów w kwaterze głównej?", "Obecny limit kwatery głównej wynosi 20 Operatorów, ale kampania zaczyna się od maksymalnie siedmiu.", "Ulepszenia The Den, postęp fabuły i dołączanie autorskich Operatorów zwiększają pojemność. To limit całej kadry, a nie liczebność drużyny na misji."),
        ("Ilu Operatorów mieści standardowy oddział?", "Standardowy oddział może liczyć do czterech Operatorów.", "W wybranych misjach gracz kontroluje dodatkowe postacie. Wyjątek nie zmienia zwykłego limitu czterech samodzielnie wybranych członków."),
        ("Ile jest klas broni?", "EA potwierdza cztery klasy broni oraz od czterech do sześciu modeli kosmetycznych w każdej klasie.", "Klasa określa rolę w walce, a model wygląd. Niepublikowane nazwy, obrażenia i rzadkości nie są tu przedstawiane jako gotowe dane."),
        ("Jak działają koszty Intel dla Operations?", "Każda Operation na Mapie Galaktyki kosztuje inną liczbę punktów Intel.", "Budżet między misjami jest ograniczony, a Operations mogą wygasnąć. Wybór powinien uwzględniać styl gry, nagrodę i pozostały czas."),
        ("Czy misje fabularne stają się obowiązkowe?", "Tak. Misje kluczowe dla fabuły po pewnym czasie stają się obowiązkowe.", "Operations i misje mogą wygasać, więc głównego wątku nie da się odkładać bez końca. Dokładna liczba cykli nie została opublikowana."),
        ("Czy na premierę będzie New Game Plus?", "Nie. Star Wars Zero Company nie ma trybu New Game Plus.", "Kolejne przejścia odblokują jednak wybrane opcje personalizacji. To premia za powtórną grę, a nie pełne przeniesienie postępu."),
        ("Czy pogoda wpływa na widoczność lub skuteczność?", "Nie. Efekty pogodowe podczas walki są wyłącznie kosmetyczne.", "Deszcz, pył i inne efekty nie zmieniają widoczności ani skuteczności oddziału. Nie potwierdzono kar do celności związanych z pogodą."),
        ("Czy stroje zapewniają statystyki?", "Nie. Stroje nie wpływają na rozgrywkę.", "Odzież służy do personalizacji wyglądu drużyny. Jest czymś innym niż pancerz, broń i zdolności i nie daje potwierdzonych premii bojowych."),
        ("Czy Tel-Rea jest jedyną Jedi Padawan?", "Tak. Tel-Rea jest jedyną Operatorką klasy Jedi Padawan.", "Nie można stworzyć ani zwerbować kolejnego Padawana. W kampanii z permanentną śmiercią warto chronić ją szczególnie uważnie."),
        ("Czy można rekrutować separatystyczne droidy bojowe?", "Nie. Droidy separatystów nie mogą zostać zrekrutowane jako Operatorzy.", "B1, B2 i inne jednostki pozostają wrogami; ogłuszenie lub hakowanie nie dodaje ich do kadry. Rekrutowane astromechy mają osobny system."),
    ],
    "zh-cn": [
        ("总部最多能容纳多少名干员？", "总部当前上限为20名干员，但战役开始时最多只能拥有7名。", "The Den升级、剧情推进以及固定干员加入都会提高容量。这里说的是完整 roster 的人数上限，并不是每次任务能够派出的队伍人数。"),
        ("标准小队最多能部署多少名干员？", "标准出战小队最多由4名干员组成。", "部分特殊任务可能让玩家额外控制其他角色，但这不会永久改变玩家自行选择的标准四人出战上限。"),
        ("游戏共有多少种武器类别？", "EA确认游戏有4种武器类别，每个类别提供4至6种外观模型。", "类别决定武器的战术定位，模型主要改变视觉外观。本页不会把尚未公布的名称、伤害数值或稀有度写成正式资料。"),
        ("Operation的Intel消耗如何运作？", "银河地图上的每个Operation会消耗不同数量的Intel。", "任务之间可用的Intel有限，而且Operation可能过期。玩家需要结合玩法偏好、目标奖励与剩余时间决定优先级。"),
        ("剧情任务会变成强制任务吗？", "会。关键剧情任务在推进到一定阶段后会变成必须执行的任务。", "Operation和任务都可能过期，因此主线不能无限期延后。官方尚未公布触发强制节点所需的准确Cycle数量。"),
        ("首发版本有New Game Plus吗？", "没有。Star Wars Zero Company不提供New Game Plus模式。", "不过后续周目会解锁部分自定义选项。这属于重复游玩的奖励，并不等于完整继承进度的传统New Game Plus。"),
        ("天气会影响视野或战斗效率吗？", "不会。战斗中的天气效果仅用于视觉呈现。", "开发团队确认雨水、沙尘等效果不会改变小队视野或效率，因此目前没有得到确认的天气命中率惩罚。"),
        ("服装会提供属性加成吗？", "不会。服装不会影响实际玩法。", "衣着用于自定义队伍外观，与护甲、武器和技能系统不同；官方没有确认任何来自服装的战斗加成。"),
        ("Tel-Rea是唯一的Jedi Padawan吗？", "是。Tel-Rea是游戏中唯一属于Jedi Padawan职业的干员。", "玩家不能创建或招募另一名Padawan。在开启永久死亡的战役中，她因此是需要格外谨慎保护的独特角色。"),
        ("可以招募分离主义战斗机器人吗？", "不可以。分离主义机器人不能作为干员加入队伍。", "B1、B2等单位仍是敌人，即使眩晕或骇入也不会进入 roster；可招募的宇航技工机器人属于另一套系统。"),
    ],
    "zh-tw": [
        ("總部最多能容納多少名幹員？", "總部目前上限為20名幹員，但戰役開始時最多只能擁有7名。", "The Den升級、劇情推進與固定幹員加入都會提高容量。這是完整 roster 的人數上限，並不是每次任務可派出的隊伍人數。"),
        ("標準小隊最多能部署多少名幹員？", "標準出戰小隊最多由4名幹員組成。", "部分特殊任務可能讓玩家額外控制其他角色，但不會永久改變玩家自行選擇的標準四人出戰上限。"),
        ("遊戲共有多少種武器類別？", "EA確認遊戲有4種武器類別，每個類別提供4至6種外觀模型。", "類別決定武器的戰術定位，模型主要改變視覺外觀。本頁不會把尚未公開的名稱、傷害數值或稀有度寫成正式資料。"),
        ("Operation的Intel消耗如何運作？", "銀河地圖上的每個Operation會消耗不同數量的Intel。", "任務之間可用的Intel有限，而且Operation可能過期。玩家需要依照玩法偏好、目標獎勵與剩餘時間決定優先順序。"),
        ("劇情任務會變成強制任務嗎？", "會。關鍵劇情任務在推進到一定階段後會變成必須執行的任務。", "Operation與任務都可能過期，因此主線不能無限期延後。官方尚未公布觸發強制節點所需的準確Cycle數量。"),
        ("首發版本有New Game Plus嗎？", "沒有。Star Wars Zero Company不提供New Game Plus模式。", "不過後續周目會解鎖部分自訂選項。這屬於重複遊玩的獎勵，不等於完整繼承進度的傳統New Game Plus。"),
        ("天氣會影響視野或戰鬥效率嗎？", "不會。戰鬥中的天氣效果僅用於視覺呈現。", "開發團隊確認雨水、沙塵等效果不會改變小隊視野或效率，因此目前沒有已確認的天氣命中率懲罰。"),
        ("服裝會提供屬性加成嗎？", "不會。服裝不會影響實際玩法。", "衣著用於自訂隊伍外觀，與護甲、武器及技能系統不同；官方沒有確認任何來自服裝的戰鬥加成。"),
        ("Tel-Rea是唯一的Jedi Padawan嗎？", "是。Tel-Rea是遊戲中唯一屬於Jedi Padawan職業的幹員。", "玩家不能建立或招募另一名Padawan。在開啟永久死亡的戰役中，她因此是需要格外謹慎保護的獨特角色。"),
        ("可以招募分離主義戰鬥機器人嗎？", "不可以。分離主義機器人不能作為幹員加入隊伍。", "B1、B2等單位仍是敵人，即使暈眩或駭入也不會進入 roster；可招募的宇航技工機器人屬於另一套系統。"),
    ],
    "pt-br": [
        ("Qual é o limite de Operadores no quartel-general?", "O limite atual do quartel-general é de 20 Operadores, mas a campanha começa com no máximo sete.", "Melhorias no The Den, avanço da história e a chegada de Operadores autorais ampliam a capacidade. Esse é o limite do elenco completo, não da equipe enviada à missão."),
        ("Quantos Operadores cabem no esquadrão padrão?", "O esquadrão padrão pode ter até quatro Operadores.", "Algumas missões permitem controlar personagens adicionais. A exceção não altera o limite normal de quatro integrantes escolhidos para o envio."),
        ("Quantas classes de armas existem?", "A EA confirma quatro classes de armas, com quatro a seis modelos cosméticos em cada classe.", "A classe define a função em combate; o modelo muda a aparência. Nomes, danos e raridades ainda não publicados não são apresentados como dados finais."),
        ("Como funcionam os custos de Intel das Operations?", "Cada Operation no Mapa da Galáxia consome uma quantidade diferente de Intel.", "O orçamento entre missões é limitado e as Operations podem expirar. A prioridade deve considerar estilo de jogo, recompensa desejada e tempo restante."),
        ("As missões de história se tornam obrigatórias?", "Sim. Missões críticas para a história tornam-se obrigatórias depois de certo ponto.", "Operations e missões podem expirar, então a história principal não pode ser adiada indefinidamente. O número exato de ciclos não foi divulgado."),
        ("Existe New Game Plus no lançamento?", "Não. Star Wars Zero Company não terá New Game Plus.", "Partidas seguintes ainda desbloqueiam algumas opções de personalização. É uma recompensa de rejogabilidade, não uma transferência completa de progresso."),
        ("O clima afeta visibilidade ou eficiência?", "Não. Os efeitos climáticos em combate são apenas cosméticos.", "Chuva, poeira e outros efeitos não mudam a visibilidade nem a eficiência do esquadrão segundo a equipe. Nenhuma penalidade climática de precisão foi confirmada."),
        ("As roupas concedem atributos?", "Não. As roupas não afetam a jogabilidade.", "O vestuário personaliza a aparência da equipe. Ele é diferente de armaduras, armas e habilidades e não concede bônus de combate confirmados."),
        ("Tel-Rea é a única Jedi Padawan?", "Sim. Tel-Rea é a única Operadora da classe Jedi Padawan.", "Não é possível criar ou recrutar outro Padawan. Em uma campanha com morte permanente, ela merece proteção especialmente cuidadosa."),
        ("É possível recrutar droides separatistas?", "Não. Droides separatistas não podem ser recrutados como Operadores.", "B1, B2 e outras unidades continuam inimigas; atordoar ou hackear não as inclui no elenco. Astromecânicos recrutáveis usam outro sistema."),
    ],
}

UI = {
    "de": ("Mechaniken", "Verifizierte Antwort", "Offizielle Einordnung", "Bedeutung für Spieler", "Prüfgrenze", "Verwandte Mechaniken", "Offizielle Quelle"),
    "fr": ("Mécaniques", "Réponse vérifiée", "Cadre officiel", "Conséquence pour les joueurs", "Limite de vérification", "Mécaniques associées", "Source officielle"),
    "it": ("Meccaniche", "Risposta verificata", "Contesto ufficiale", "Impatto per i giocatori", "Limite di verifica", "Meccaniche correlate", "Fonte ufficiale"),
    "es": ("Mecánicas", "Respuesta verificada", "Contexto oficial", "Qué cambia para el jugador", "Límite de verificación", "Mecánicas relacionadas", "Fuente oficial"),
    "ja": ("ゲームシステム", "確認済みの回答", "公式情報の範囲", "プレイヤーへの影響", "確認上の注意", "関連システム", "公式ソース"),
    "ko": ("게임 시스템", "확인된 답변", "공식 정보 범위", "플레이어에게 미치는 영향", "검증 한계", "관련 시스템", "공식 출처"),
    "pl": ("Mechaniki", "Zweryfikowana odpowiedź", "Oficjalny zakres", "Znaczenie dla gracza", "Granica weryfikacji", "Powiązane mechaniki", "Oficjalne źródło"),
    "zh-cn": ("游戏机制", "已核验答案", "官方信息范围", "对玩家的影响", "核验边界", "相关机制", "官方来源"),
    "zh-tw": ("遊戲機制", "已核驗答案", "官方資訊範圍", "對玩家的影響", "核驗邊界", "相關機制", "官方來源"),
    "pt-br": ("Mecânicas", "Resposta verificada", "Contexto oficial", "Impacto para o jogador", "Limite da verificação", "Mecânicas relacionadas", "Fonte oficial"),
}

METHOD = {
    "de": "Diese Seite trennt eine wörtlich bestätigte Spielregel von noch unveröffentlichten Zahlen. Grundlage ist EAs Community-Q&A vom 21. Juli 2026. Trailerbilder, Vermutungen und Vergleiche mit anderen Taktikspielen gelten nicht als Beleg. Nach Veröffentlichung wird die Regel im Spielmenü und in einem reproduzierbaren Test erneut geprüft.",
    "fr": "Cette page sépare une règle explicitement confirmée des valeurs encore inédites. Elle s’appuie sur le questions-réponses communautaire d’EA du 21 juillet 2026. Les images de bande-annonce, suppositions et comparaisons avec d’autres jeux tactiques ne servent pas de preuve. Après la sortie, la règle sera vérifiée dans les menus et par un test reproductible.",
    "it": "Questa pagina separa una regola confermata dai valori non ancora pubblicati. La fonte è il Q&A della community EA del 21 luglio 2026. Immagini dei trailer, ipotesi e confronti con altri giochi tattici non vengono trattati come prove. Dopo l’uscita, la regola sarà controllata nei menu e con un test riproducibile.",
    "es": "Esta página separa una regla confirmada de los valores que aún no se han publicado. La fuente es el Q&A de la comunidad de EA del 21 de julio de 2026. Las imágenes de tráiler, las suposiciones y las comparaciones con otros juegos tácticos no se consideran pruebas. Tras el lanzamiento, la regla se revisará en los menús y mediante una prueba reproducible.",
    "ja": "このページでは、公式に明言されたルールと未公開の数値を分けて扱います。根拠は2026年7月21日のEAコミュニティQ&Aです。トレーラー映像、推測、他のタクティクスゲームとの比較は証拠に含めません。発売後は実際のメニューと再現可能なテストで再確認し、バージョンと確認日を更新します。",
    "ko": "이 페이지는 공식적으로 명시된 규칙과 아직 공개되지 않은 수치를 구분합니다. 근거는 2026년 7월 21일 EA 커뮤니티 Q&A입니다. 트레일러 장면, 추측, 다른 전술 게임과의 비교는 증거로 취급하지 않습니다. 출시 후에는 실제 메뉴와 반복 가능한 테스트로 다시 확인하고 버전과 검증일을 갱신합니다.",
    "pl": "Strona oddziela wyraźnie potwierdzoną zasadę od nieopublikowanych wartości. Źródłem jest Q&A społeczności EA z 21 lipca 2026 roku. Kadry zwiastuna, przypuszczenia i porównania z innymi grami taktycznymi nie są dowodem. Po premierze zasada zostanie sprawdzona w menu gry i w powtarzalnym teście.",
    "zh-cn": "本页严格区分官方明确确认的规则与仍未公布的数值，主要依据是EA在2026年7月21日发布的社区问答。预告片画面、玩家推测以及与其他战术游戏的类比都不会被当作事实证据。游戏正式发售后，编辑会通过实际菜单与可重复测试再次核验，并补充对应版本、测试条件和更新日期。",
    "zh-tw": "本頁嚴格區分官方明確確認的規則與仍未公開的數值，主要依據是EA於2026年7月21日發布的社群問答。預告片畫面、玩家推測及與其他戰術遊戲的類比都不會被視為事實證據。遊戲正式發售後，編輯會透過實際選單與可重複測試再次核驗，並補上版本、測試條件與更新日期。",
    "pt-br": "Esta página separa uma regra confirmada de valores ainda não publicados. A fonte é o Q&A da comunidade da EA de 21 de julho de 2026. Imagens de trailer, suposições e comparações com outros jogos táticos não contam como prova. Depois do lançamento, a regra será conferida nos menus e em um teste reproduzível.",
}

# This is the English mechanics-page visual system, with only additive support
# for data tables used by older localized FAQ pages.
STYLE = """:root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#a8bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1040px}*{box-sizing:border-box}body{margin:0;background:#071016;color:var(--text);font:16px/1.72 system-ui,-apple-system,'Segoe UI',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}nav>a{color:var(--muted);font-size:14px}.hero{padding:50px 0 28px;border-bottom:1px solid var(--line)}.crumb,.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.14em;color:var(--teal)}h1{font-size:clamp(34px,6vw,56px);line-height:1.08;margin:13px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#cad8e0;max-width:850px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0;color:var(--text)}.answer{border-color:rgba(54,224,206,.5)}.note,.fact{border-color:rgba(233,184,74,.45)}.pill{display:inline-block;border:1px solid #3c625f;padding:5px 9px;color:var(--teal);font-size:12px}.muted,.source{color:var(--muted);font-size:14px}table{width:100%;border-collapse:collapse;margin:15px 0}th,td{border:1px solid var(--line);padding:11px;text-align:left}th{color:var(--gold);width:28%}li{margin:8px 0}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}.lang-menu{position:relative;display:inline-block;margin-left:4px;z-index:40;font:600 14px/1.2 system-ui,-apple-system,'Segoe UI',sans-serif;color:#edf7ff}.lang-menu summary{list-style:none;cursor:pointer;border:1px solid #365264;border-radius:7px;padding:8px 28px 8px 11px;background:#0d1922;color:#edf7ff;white-space:nowrap;position:relative}.lang-menu summary::-webkit-details-marker{display:none}.lang-menu summary::after{content:'▾';position:absolute;right:10px;color:#36e0ce}.lang-menu[open] summary::after{content:'▴'}.lang-options{position:absolute;right:0;top:calc(100% + 7px);min-width:154px;padding:6px;background:#0b161e;border:1px solid #365264;border-radius:8px;box-shadow:0 12px 30px rgba(0,0,0,.38)}.lang-options a{display:block!important;padding:9px 10px!important;margin:0!important;border-radius:5px;color:#c8d8e1!important;text-decoration:none!important;white-space:nowrap;font-size:14px!important}.lang-options a:hover,.lang-options a[aria-current=page]{background:#132631;color:#36e0ce!important}.lang-options a[aria-current=page]::before{content:'✓ ';color:#e9b84a}@media(max-width:760px){nav{margin-left:0}.top .wrap{padding-top:10px;padding-bottom:10px}.lang-menu{width:100%;margin:4px 0}.lang-menu summary{width:100%}.lang-options{position:static;margin-top:6px;width:100%}}"""


def route(locale: str, slug: str) -> str:
    return f"/mechanics/{slug}.html" if locale == "en" else f"/{locale}/mechanics/{slug}.html"


def alternates(slug: str) -> str:
    links = "".join(
        f'<link rel="alternate" hreflang="{tag}" href="{SITE}{route(code, slug)}">'
        for code, tag, _ in LOCALES
    )
    return links + f'<link rel="alternate" hreflang="x-default" href="{SITE}{route("en", slug)}">'


def menu(locale: str, slug: str) -> str:
    current = next(label for code, _, label in LOCALES if code == locale)
    items = "".join(
        f'<a href="{route(code, slug)}" lang="{tag}"{" aria-current=\"page\"" if code == locale else ""}>{escape(label)}</a>'
        for code, tag, label in LOCALES
    )
    return f'<details class="lang-menu"><summary aria-label="Choose language">{escape(current)}</summary><div class="lang-options">{items}</div></details>'


def page(locale: str, lang: str, index: int, item: tuple) -> str:
    title, direct, impact = item
    slug = SLUGS[index]
    labels = UI[locale]
    canonical = SITE + route(locale, slug)
    next_ids = ((index - 1) % len(SLUGS), (index + 1) % len(SLUGS), (index + 3) % len(SLUGS))
    related = "".join(
        f'<a class="card" href="{route(locale, SLUGS[n])}"><strong>{escape(COPY[locale][n][0])}</strong>'
        f'<br><span class="muted">{escape(COPY[locale][n][1])}</span></a>'
        for n in next_ids
    )
    schema = {
        "@context": "https://schema.org", "@type": "Article", "inLanguage": lang,
        "headline": title, "description": direct, "url": canonical,
        "dateModified": TODAY, "about": "Star Wars Zero Company gameplay mechanics",
        "isPartOf": {"@type": "WebSite", "name": "Star Wars Zero Company Wiki", "url": SITE + "/"},
    }
    scope = {
        "de": "Die Antwort gilt für die offiziell beschriebene Vorabversion. Sie macht aus einer allgemeinen Regel keine erfundene Fähigkeit, keinen endgültigen Schwierigkeitswert und keine Garantie für spätere Updates.",
        "fr": "La réponse concerne la version décrite officiellement avant la sortie. Elle ne transforme pas une règle générale en capacité inventée, valeur finale de difficulté ou garantie de mise à jour.",
        "it": "La risposta riguarda la versione descritta ufficialmente prima dell’uscita. Non trasforma una regola generale in un’abilità inventata, un valore finale di difficoltà o una promessa di aggiornamento.",
        "es": "La respuesta corresponde a la versión descrita oficialmente antes del lanzamiento. No convierte una regla general en habilidad inventada, valor final de dificultad o promesa de actualización.",
        "ja": "この回答は発売前に公式説明されたバージョンを対象とします。一般ルールから未公開のアビリティ、最終難易度の数値、将来アップデートの約束を作り出すものではありません。",
        "ko": "이 답변은 출시 전에 공식 설명된 버전을 기준으로 합니다. 일반 규칙을 근거로 공개되지 않은 능력, 최종 난이도 수치, 향후 업데이트 약속을 만들어 내지 않습니다.",
        "pl": "Odpowiedź dotyczy wersji oficjalnie opisanej przed premierą. Nie zamienia ogólnej zasady w wymyśloną zdolność, końcową wartość trudności ani obietnicę aktualizacji.",
        "zh-cn": "本答案适用于官方在发售前描述的版本，不会从一条总体规则推导出未公布的技能、最终难度数值或未来更新承诺。任何超出来源范围的细节都不会进入结构化数据和Sitemap摘要。",
        "zh-tw": "本答案適用於官方在發售前描述的版本，不會從一條整體規則推導出未公開的技能、最終難度數值或未來更新承諾。任何超出來源範圍的細節都不會進入結構化資料與Sitemap摘要。",
        "pt-br": "A resposta vale para a versão descrita oficialmente antes do lançamento. Ela não transforma uma regra geral em habilidade inventada, valor final de dificuldade ou promessa de atualização.",
    }[locale]
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape((direct + ' ' + impact)[:300])}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates(slug)}<meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(direct)}"><meta property="og:image" content="{SITE}/assets/zero-company-hero.png"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav><a href="/{locale}/questions/">FAQ</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a><a href="/{locale}/mechanics/">Systems</a>{menu(locale, slug)}</nav></div></header><main class="wrap"><section class="hero"><div class="crumb"><a href="/{locale}/mechanics/">{escape(labels[0])}</a> / {escape(labels[1])}</div><p class="eyebrow">{escape(labels[1])} · {TODAY}</p><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section><section class="block answer"><h2>{escape(labels[1])}</h2><p><strong>{escape(direct)}</strong></p></section><section class="block"><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p><p>{escape(scope)}</p></section><section class="block"><h2>{escape(labels[3])}</h2><p>{escape(impact)}</p><p>{escape(direct)} {escape(scope)}</p></section><section class="block note"><h2>{escape(labels[4])}</h2><p>{escape(METHOD[locale])}</p></section><section><h2>{escape(labels[5])}</h2><div class="grid">{related}</div></section><section class="block"><h2>{escape(labels[6])}</h2><p><a href="{SOURCE}" rel="nofollow">EA community Q&amp;A — July 21, 2026</a></p><p class="source">Independent community guide. Confirmed facts are separated from unannounced values and will be checked again after release.</p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">{escape(labels[6])}</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def hub(locale: str, lang: str) -> str:
    labels = UI[locale]
    canonical = f"{SITE}/{locale}/mechanics/"
    cards = "".join(
        f'<a class="card" href="{route(locale, slug)}"><strong>{escape(item[0])}</strong>'
        f'<br><span class="muted">{escape(item[1])}</span></a>'
        for slug, item in zip(SLUGS, COPY[locale])
    )
    schema = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "inLanguage": lang, "name": labels[0], "url": canonical,
        "dateModified": TODAY, "about": "Star Wars Zero Company gameplay mechanics",
    }
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(labels[0])} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape(labels[0])}: 10 source-linked answers about roster, squad size, weapons, Intel, missions, replay, weather, outfits, Jedi and droids."><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav><a href="/{locale}/questions/">FAQ</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a></nav></div></header><main class="wrap"><section class="hero"><p class="eyebrow">{escape(labels[0])}</p><h1>{escape(labels[0])}</h1><p class="lead">{escape(METHOD[locale])}</p></section><section><h2>{escape(labels[1])}</h2><div class="grid">{cards}</div></section><section class="block note"><h2>{escape(labels[4])}</h2><p>{escape(METHOD[locale])}</p><p><a href="{SOURCE}" rel="nofollow">EA community Q&amp;A — July 21, 2026</a></p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">{escape(labels[6])}</a></div></footer></body></html>'''


def add_english_alternates(path: Path, slug: str) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    text = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*>', "", text, flags=re.I)
    canonical = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', text, re.I)
    if not canonical:
        raise ValueError(f"Missing canonical in {path}")
    text = text[:canonical.end()] + alternates(slug) + text[canonical.end():]
    path.write_text(text, encoding="utf-8")


def normalize_round13_faq_style() -> int:
    """Give the prior localized FAQ batch the same CSS system as English."""
    changed = 0
    for locale, _, _ in LOCALES:
        if locale == "en":
            continue
        for path in (ROOT / locale / "questions").glob("*.html"):
            text = path.read_text(encoding="utf-8-sig", errors="ignore")
            revised, count = re.subn(r"<style>.*?</style>", f"<style>{STYLE}</style>", text, count=1, flags=re.I | re.S)
            if count and revised != text:
                path.write_text(revised, encoding="utf-8")
                changed += 1
    return changed


def main() -> None:
    created = 0
    for locale, lang, _ in LOCALES:
        if locale == "en":
            for slug in SLUGS:
                add_english_alternates(ROOT / "mechanics" / f"{slug}.html", slug)
            continue
        out = ROOT / locale / "mechanics"
        out.mkdir(parents=True, exist_ok=True)
        for index, item in enumerate(COPY[locale]):
            (out / f"{SLUGS[index]}.html").write_text(page(locale, lang, index, item), encoding="utf-8")
            created += 1
        (out / "index.html").write_text(hub(locale, lang), encoding="utf-8")
    normalized = normalize_round13_faq_style()
    print(f"Round 14 created {created} localized mechanics pages")
    print(f"Round 14 normalized {normalized} existing localized FAQ pages to English visual CSS")


if __name__ == "__main__":
    main()
