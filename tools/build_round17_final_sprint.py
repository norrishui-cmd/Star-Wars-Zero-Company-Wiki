#!/usr/bin/env python3
"""Round 17: reach 1,000 quality URLs with localized combat systems and buyer guides."""

from datetime import date
from html import escape
import importlib.util
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = date.today().isoformat()
GAMEPLAY_SOURCE = "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"
QA_SOURCE = "https://www.ea.com/games/starwars/zero-company/news/answering-biggest-questions"
BUY_SOURCE = "https://www.ea.com/games/starwars/zero-company/news/pre-order-star-wars-zero-company"

spec = importlib.util.spec_from_file_location("r16", ROOT / "tools" / "build_round16_multilingual_systems.py")
r16 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r16)
STYLE = r16.STYLE
LOCALES = r16.LOCALES

SLUGS = (
    "squad-acts-before-enemies", "three-action-points-each-turn",
    "movement-distance-ap-cost", "weapon-type-ap-cost",
    "chance-to-hit-shot-breakdown", "shared-advantage-pool",
    "destructible-cover", "push-enemy-into-overwatch",
    "three-injuries-permadeath", "permadeath-toggle",
    "the-den-third-person-base", "holotable-cycle-planning",
    "operation-choices-affect-bonds", "pre-combat-exploration-rewards",
    "galaxy-map-150-planets",
)

# Each row is localized title | localized direct answer. The subjects and facts
# mirror the mature English source pages and first-party EA articles.
RAW = {
    "de": (
        "Handelt die gesamte Truppe vor den Gegnern?|Ja. In einer Kampfrunde handelt zuerst die gesamte eigene Truppe, danach folgt die gegnerische Seite.",
        "Wie viele Aktionspunkte hat ein Operator?|Jeder eingesetzte Operator erhält pro Runde drei Aktionspunkte für Bewegung, Angriffe und Fähigkeiten.",
        "Wie beeinflusst die Entfernung die Bewegungskosten?|Je weiter sich ein Operator bewegt, desto mehr Aktionspunkte kostet die Bewegung.",
        "Haben Waffen unterschiedliche AP-Kosten?|Ja. Die Aktionspunktkosten eines Angriffs hängen vom Waffentyp ab; manche Angriffe verbrauchen alle verfügbaren AP.",
        "Wo sieht man Trefferchance und Berechnung?|Die Trefferchance steht am Ziel; Reichweite, Deckung und weitere Faktoren werden im Shot-Breakdown erklärt.",
        "Ist Advantage eine gemeinsame Ressource?|Ja. Advantage Points liegen in einem gemeinsamen Truppenpool, aus dem Spezialfähigkeiten verschiedener Operatoren bezahlt werden.",
        "Kann Deckung zerstört werden?|Ja. Raketen und Explosionen können gegnerische Deckung entfernen und neue Schusslinien öffnen.",
        "Kann man Gegner in Overwatch stoßen?|Ja. Force Push oder Kabb Uppercut können ein Ziel in die Overwatch-Zone eines Verbündeten befördern.",
        "Führen drei Verletzungen zum Tod?|Ein Operator, der drei Verletzungen ansammelt, stirbt dauerhaft; genaue Heilzeiten können von der finalen Version abhängen.",
        "Kann Permadeath deaktiviert werden?|Ja. Permanenter Tod ist standardmäßig aktiv, kann aber in den Spieleinstellungen ausgeschaltet werden.",
        "Was ist The Den?|The Den ist die Basis auf Kafrene; dort wechselt die Kamera in die Third-Person-Perspektive und das Team wird verwaltet.",
        "Was zeigt der Holotable pro Cycle?|Der Holotable zeigt verfügbare Operations und Tactical Missions sowie den Einfluss der Kompanie im aktuellen Cycle.",
        "Beeinflussen Operation-Entscheidungen die Bonds?|Ja. Manche Galaxy-Map-Entscheidungen können Bonds verändern und zusätzliche Operations oder Nebenmissionen freischalten.",
        "Welche Belohnungen bietet Erkundung vor dem Kampf?|Kleine Erkundungsabschnitte in Storymissionen können Weltinformationen, Intel und Advantage Points vor dem Gefecht liefern.",
        "Wie groß ist die Galaxy Map?|Die strategische Karte umfasst mehr als 150 Planeten für Operations; Tactical Missions spielen auf über einem Dutzend eigener Planeten.",
    ),
    "fr": (
        "Toute l’escouade agit-elle avant les ennemis ?|Oui. Toute l’escouade du joueur agit d’abord pendant un tour, puis le camp ennemi joue.",
        "Combien de points d’action possède un agent ?|Chaque agent déployé reçoit trois points d’action par tour pour se déplacer, attaquer ou utiliser ses capacités.",
        "La distance modifie-t-elle le coût du déplacement ?|Oui. Plus un agent se déplace loin, plus le mouvement consomme de points d’action.",
        "Le coût en PA varie-t-il selon l’arme ?|Oui. Le type d’arme détermine le coût d’une attaque et certaines actions consomment tous les PA disponibles.",
        "Où voir la chance de toucher ?|La chance de toucher apparaît près de la cible et le Shot Breakdown détaille notamment portée et couverture.",
        "Advantage est-il une ressource partagée ?|Oui. Les Advantage Points forment une réserve commune utilisée par les capacités spéciales de toute l’escouade.",
        "Peut-on détruire les couvertures ?|Oui. Roquettes et explosifs peuvent supprimer une couverture ennemie et ouvrir une nouvelle ligne de tir.",
        "Peut-on pousser une cible dans l’Overwatch ?|Oui. Force Push ou l’Uppercut de Kabb peut projeter un ennemi dans la zone d’Overwatch d’un allié.",
        "Trois blessures provoquent-elles la mort ?|Un agent qui accumule trois blessures meurt définitivement ; les délais de soin restent à vérifier dans la version finale.",
        "Peut-on désactiver la mort permanente ?|Oui. La mort permanente est activée par défaut mais peut être désactivée dans les options.",
        "Qu’est-ce que The Den ?|The Den est la base de Kafrene où la caméra passe à la troisième personne et où l’on gère la compagnie.",
        "Que montre l’Holotable à chaque Cycle ?|L’Holotable affiche les Operations, les Tactical Missions et l’Influence disponibles pour le Cycle en cours.",
        "Les choix d’Operation affectent-ils les Bonds ?|Oui. Certains choix sur la carte peuvent modifier les Bonds et débloquer d’autres Operations ou missions secondaires.",
        "Que rapporte l’exploration avant le combat ?|De courtes zones des missions principales peuvent fournir immersion, Intel et Advantage Points avant l’affrontement.",
        "Quelle est la taille de la Galaxy Map ?|La carte stratégique contient plus de 150 planètes pour les Operations et plus d’une douzaine de mondes de Tactical Missions.",
    ),
    "it": (
        "L’intera squadra agisce prima dei nemici?|Sì. Durante un turno agisce prima tutta la squadra del giocatore, poi tocca alla fazione nemica.",
        "Quanti punti azione ha un Operatore?|Ogni Operatore schierato riceve tre punti azione per turno da spendere in movimento, attacchi e abilità.",
        "La distanza cambia il costo del movimento?|Sì. Più lontano si muove un Operatore, maggiore è il costo in punti azione.",
        "Le armi hanno costi AP diversi?|Sì. Il costo dell’attacco dipende dal tipo di arma e alcune azioni consumano tutti gli AP disponibili.",
        "Dove si vede la probabilità di colpire?|La probabilità appare accanto al bersaglio; lo Shot Breakdown spiega fattori come distanza e copertura.",
        "Advantage è una risorsa condivisa?|Sì. Gli Advantage Points formano una riserva comune usata dalle abilità speciali di tutta la squadra.",
        "È possibile distruggere le coperture?|Sì. Razzi ed esplosivi possono eliminare la copertura nemica e creare nuove linee di tiro.",
        "Si può spingere un nemico nell’Overwatch?|Sì. Force Push o l’Uppercut di Kabb possono spostare un bersaglio nella zona di Overwatch di un alleato.",
        "Tre ferite causano la morte?|Un Operatore che accumula tre ferite muore definitivamente; i tempi di cura precisi saranno verificati al lancio.",
        "Si può disattivare la morte permanente?|Sì. La morte permanente è attiva per impostazione predefinita ma può essere disabilitata nelle opzioni.",
        "Che cos’è The Den?|The Den è la base su Kafrene, con visuale in terza persona e strutture per gestire la compagnia.",
        "Cosa mostra l’Holotable in ogni Cycle?|L’Holotable elenca Operations, Tactical Missions e Influence disponibili nel Cycle corrente.",
        "Le scelte nelle Operation influenzano i Bond?|Sì. Alcune scelte sulla Galaxy Map possono cambiare i Bond e sbloccare altre Operations o missioni secondarie.",
        "Cosa offre l’esplorazione prima del combattimento?|Brevi sezioni delle missioni narrative possono fornire contesto, Intel e Advantage Points prima dello scontro.",
        "Quanto è grande la Galaxy Map?|La mappa strategica include oltre 150 pianeti per le Operations e più di dodici mondi per le Tactical Missions.",
    ),
    "es": (
        "¿Actúa todo el pelotón antes que el enemigo?|Sí. En cada turno actúa primero todo el pelotón del jugador y después juega el bando enemigo.",
        "¿Cuántos puntos de acción tiene un agente?|Cada agente desplegado recibe tres puntos de acción por turno para movimiento, ataques y habilidades.",
        "¿La distancia cambia el coste de movimiento?|Sí. Cuanto más lejos se desplaza un agente, mayor es el coste en puntos de acción.",
        "¿Las armas tienen costes de AP distintos?|Sí. El coste de atacar depende del tipo de arma y algunas acciones consumen todos los AP disponibles.",
        "¿Dónde se muestra la probabilidad de impacto?|Aparece junto al objetivo y el Shot Breakdown detalla factores como alcance y cobertura.",
        "¿Advantage es un recurso compartido?|Sí. Los Advantage Points forman una reserva común que paga habilidades especiales de todo el pelotón.",
        "¿Se puede destruir la cobertura?|Sí. Cohetes y explosivos pueden eliminar cobertura enemiga y abrir nuevas líneas de tiro.",
        "¿Se puede empujar a un enemigo al Overwatch?|Sí. Force Push o el Uppercut de Kabb pueden lanzar un objetivo a la zona de Overwatch de un aliado.",
        "¿Tres heridas provocan la muerte?|Un agente que acumula tres heridas muere de forma permanente; los tiempos exactos de curación se verificarán al lanzamiento.",
        "¿Se puede desactivar la muerte permanente?|Sí. La muerte permanente está activada por defecto, pero se puede deshabilitar en las opciones.",
        "¿Qué es The Den?|The Den es la base de Kafrene, con cámara en tercera persona e instalaciones para gestionar la compañía.",
        "¿Qué muestra la Holotable en cada Cycle?|La Holotable presenta Operations, Tactical Missions e Influence disponibles durante el Cycle actual.",
        "¿Las decisiones de Operation afectan a los Bonds?|Sí. Algunas decisiones del mapa pueden cambiar Bonds y desbloquear Operations o misiones secundarias.",
        "¿Qué aporta explorar antes del combate?|Pequeñas zonas de las misiones principales pueden otorgar contexto, Intel y Advantage Points antes de luchar.",
        "¿Qué tamaño tiene la Galaxy Map?|El mapa estratégico incluye más de 150 planetas para Operations y más de doce mundos de Tactical Missions.",
    ),
    "ja": (
        "味方全員が敵より先に行動する？|はい。各ターンはプレイヤー側の部隊全員が先に行動し、その後に敵側の手番になります。",
        "隊員1人のAction Pointは何点？|出撃した各Operatorは毎ターン3 APを受け取り、移動、攻撃、アビリティに使用します。",
        "移動距離でAPコストは変わる？|はい。移動する距離が長いほど、必要なAction Pointも増加します。",
        "武器によって攻撃APは異なる？|はい。攻撃コストは武器タイプで異なり、残りAPをすべて消費する行動もあります。",
        "命中率の内訳はどこで確認できる？|命中率は対象の横に表示され、Shot Breakdownで射程や遮蔽などの要因を確認できます。",
        "Advantageは部隊共有リソース？|はい。Advantage Pointsは部隊全体の共有プールで、各隊員の特殊能力に使用します。",
        "敵の遮蔽は破壊できる？|はい。ロケットや爆発物で敵の遮蔽を除去し、新しい射線を作れます。",
        "敵をOverwatchへ押し込める？|はい。Force PushやKabbのUppercutで敵を味方のOverwatch範囲へ移動できます。",
        "負傷が3回重なると永久死亡する？|Operatorは負傷を3回蓄積すると永久に死亡します。正確な治療期間は製品版で確認します。",
        "Permadeathは無効化できる？|はい。永久死亡は初期設定で有効ですが、オプションから無効にできます。",
        "The Denとは何？|The DenはKafreneにある本拠地で、三人称視点に切り替わり部隊管理施設を利用できます。",
        "HolotableはCycleごとに何を示す？|現在のCycleで利用できるOperations、Tactical Missions、会社のInfluenceを表示します。",
        "Operationの選択はBondに影響する？|はい。Galaxy Mapの一部の選択はBondを変化させ、追加Operationやサイド任務を解放します。",
        "戦闘前探索では何を得られる？|メイン任務の短い探索区間では、世界情報、Intel、Advantage Pointsを戦闘前に獲得できます。",
        "Galaxy Mapには何個の惑星がある？|戦略Operation向けに150以上の惑星があり、Tactical Missionは12以上の固有惑星で行われます。",
    ),
    "ko": (
        "아군 전체가 적보다 먼저 행동하나요?|네. 한 턴에는 플레이어 분대 전체가 먼저 행동하고, 그다음 적 진영의 차례가 진행됩니다.",
        "오퍼레이터 한 명의 행동 포인트는 몇 개인가요?|배치된 각 오퍼레이터는 매 턴 이동, 공격, 능력에 쓸 수 있는 3 AP를 받습니다.",
        "이동 거리에 따라 AP 비용이 달라지나요?|네. 오퍼레이터가 더 멀리 이동할수록 더 많은 행동 포인트를 소비합니다.",
        "무기마다 공격 AP 비용이 다른가요?|네. 공격 비용은 무기 유형에 따라 다르며, 일부 행동은 남은 AP를 모두 소비합니다.",
        "명중 확률 계산은 어디서 확인하나요?|명중 확률은 대상 옆에 표시되고 Shot Breakdown에서 사거리와 엄폐 등 요인을 확인할 수 있습니다.",
        "Advantage는 분대 공유 자원인가요?|네. Advantage Points는 분대 전체가 공유하며 여러 오퍼레이터의 특수 능력에 사용됩니다.",
        "적 엄폐물을 파괴할 수 있나요?|네. 로켓과 폭발물로 적 엄폐를 없애 새로운 사선을 만들 수 있습니다.",
        "적을 Overwatch 구역으로 밀 수 있나요?|네. Force Push나 Kabb의 Uppercut으로 적을 아군 Overwatch 범위에 밀어 넣을 수 있습니다.",
        "부상 세 번이면 영구 사망하나요?|오퍼레이터가 부상을 세 번 누적하면 영구 사망합니다. 정확한 치료 기간은 출시 버전에서 확인합니다.",
        "Permadeath를 끌 수 있나요?|네. 영구 사망은 기본적으로 켜져 있지만 옵션에서 비활성화할 수 있습니다.",
        "The Den은 무엇인가요?|The Den은 Kafrene의 본부로, 3인칭 시점에서 중대를 관리하는 여러 시설을 이용합니다.",
        "Holotable은 Cycle마다 무엇을 보여 주나요?|현재 Cycle의 Operations, Tactical Missions, 중대 Influence를 표시합니다.",
        "Operation 선택이 Bond에 영향을 주나요?|네. Galaxy Map의 일부 선택은 Bond를 바꾸고 추가 Operation이나 보조 임무를 해제할 수 있습니다.",
        "전투 전 탐색에서 무엇을 얻나요?|메인 스토리의 짧은 탐색 구간에서 세계 정보, Intel, Advantage Points를 전투 전에 얻을 수 있습니다.",
        "Galaxy Map에는 행성이 몇 개인가요?|전략 Operation용 행성이 150개 이상이며 Tactical Mission은 12개가 넘는 고유 행성에서 진행됩니다.",
    ),
    "pl": (
        "Czy cały oddział działa przed wrogami?|Tak. W każdej turze najpierw działa cały oddział gracza, a dopiero potem strona przeciwnika.",
        "Ile punktów akcji ma Operator?|Każdy wystawiony Operator otrzymuje na turę trzy punkty akcji na ruch, ataki i zdolności.",
        "Czy dystans zmienia koszt ruchu?|Tak. Im dalej porusza się Operator, tym więcej punktów akcji wydaje.",
        "Czy broń ma różne koszty AP?|Tak. Koszt ataku zależy od rodzaju broni, a niektóre działania zużywają wszystkie dostępne AP.",
        "Gdzie widać szansę trafienia?|Szansa jest pokazana obok celu, a Shot Breakdown wyjaśnia czynniki takie jak zasięg i osłona.",
        "Czy Advantage jest wspólnym zasobem?|Tak. Advantage Points tworzą wspólną pulę oddziału używaną przez zdolności specjalne Operatorów.",
        "Czy można zniszczyć osłonę?|Tak. Rakiety i materiały wybuchowe mogą usunąć osłonę przeciwnika i otworzyć linię strzału.",
        "Czy można wepchnąć wroga w Overwatch?|Tak. Force Push lub Uppercut Kabba może przesunąć cel do strefy Overwatch sojusznika.",
        "Czy trzy obrażenia oznaczają śmierć?|Operator z trzema obrażeniami umiera na stałe; dokładny czas leczenia wymaga sprawdzenia po premierze.",
        "Czy można wyłączyć trwałą śmierć?|Tak. Permadeath jest domyślnie aktywny, lecz można go wyłączyć w opcjach.",
        "Czym jest The Den?|The Den to baza na Kafrene, gdzie kamera przechodzi do widoku trzecioosobowego i zarządza się kompanią.",
        "Co pokazuje Holotable w każdym Cycle?|Holotable pokazuje dostępne Operations, Tactical Missions i Influence dla bieżącego Cycle.",
        "Czy wybory w Operation wpływają na Bonds?|Tak. Niektóre decyzje na Galaxy Map mogą zmieniać Bonds i odblokować kolejne Operations lub misje poboczne.",
        "Co daje eksploracja przed walką?|Krótkie odcinki misji fabularnych mogą dać informacje o świecie, Intel i Advantage Points przed starciem.",
        "Jak duża jest Galaxy Map?|Mapa strategiczna obejmuje ponad 150 planet dla Operations i ponad dwanaście światów Tactical Missions.",
    ),
    "zh-cn": (
        "我方全队是否先于敌人行动？|是。每个回合先由玩家整支小队完成行动，然后才轮到敌方阵营。",
        "每名干员每回合有多少行动点？|每名出战干员每回合获得3点行动点，可用于移动、攻击和施放能力。",
        "移动距离是否影响行动点消耗？|是。干员移动距离越远，所消耗的行动点就越多。",
        "不同武器的攻击AP消耗是否不同？|是。攻击消耗取决于武器类型，部分行动会一次用完当前全部行动点。",
        "在哪里查看命中率的计算？|命中率显示在目标旁边，Shot Breakdown会解释射程、掩体等影响因素。",
        "Advantage是否为全队共享资源？|是。Advantage Points属于全队共享池，可供不同干员的特殊能力使用。",
        "能否摧毁敌人的掩体？|可以。火箭与爆炸物能够移除敌方掩体并打开新的射线。",
        "能否把敌人推入Overwatch区域？|可以。Force Push或Kabb的Uppercut能把目标推入队友的Overwatch范围。",
        "累计三次伤势是否会永久死亡？|干员累计三次伤势后会永久死亡；具体治疗周期需在正式版中复核。",
        "能否关闭永久死亡？|可以。永久死亡默认开启，但玩家可以在选项中将其关闭。",
        "The Den是什么？|The Den是位于Kafrene的基地，玩家会切换至第三人称视角并使用各类小队管理设施。",
        "Holotable每个Cycle显示什么？|Holotable会显示当前Cycle可用的Operations、Tactical Missions和小队Influence。",
        "Operation选择会影响Bond吗？|会。Galaxy Map上的部分选择可改变Bond，并解锁更多Operation或支线任务。",
        "战斗前探索可以获得什么？|主线任务中的短暂探索区段可在战斗前提供世界信息、Intel和Advantage Points。",
        "Galaxy Map有多少颗行星？|战略Operation可发生在150多颗行星上，Tactical Mission则覆盖十多个独立行星。",
    ),
    "zh-tw": (
        "我方全隊是否先於敵人行動？|是。每個回合先由玩家整支小隊完成行動，然後才輪到敵方陣營。",
        "每名幹員每回合有多少行動點？|每名出戰幹員每回合獲得3點行動點，可用於移動、攻擊及施放能力。",
        "移動距離是否影響行動點消耗？|是。幹員移動距離越遠，所消耗的行動點就越多。",
        "不同武器的攻擊AP消耗是否不同？|是。攻擊消耗取決於武器類型，部分行動會一次用完目前全部行動點。",
        "在哪裡查看命中率的計算？|命中率顯示在目標旁邊，Shot Breakdown會解釋射程、掩體等影響因素。",
        "Advantage是否為全隊共享資源？|是。Advantage Points屬於全隊共享池，可供不同幹員的特殊能力使用。",
        "能否摧毀敵人的掩體？|可以。火箭與爆炸物能夠移除敵方掩體並打開新的射線。",
        "能否把敵人推入Overwatch區域？|可以。Force Push或Kabb的Uppercut能把目標推入隊友的Overwatch範圍。",
        "累積三次傷勢是否會永久死亡？|幹員累積三次傷勢後會永久死亡；具體治療週期需在正式版中複核。",
        "能否關閉永久死亡？|可以。永久死亡預設開啟，但玩家可以在選項中將其關閉。",
        "The Den是什麼？|The Den是位於Kafrene的基地，玩家會切換至第三人稱視角並使用各類小隊管理設施。",
        "Holotable每個Cycle顯示什麼？|Holotable會顯示目前Cycle可用的Operations、Tactical Missions和小隊Influence。",
        "Operation選擇會影響Bond嗎？|會。Galaxy Map上的部分選擇可改變Bond，並解鎖更多Operation或支線任務。",
        "戰鬥前探索可以獲得什麼？|主線任務中的短暫探索區段可在戰鬥前提供世界資訊、Intel及Advantage Points。",
        "Galaxy Map有多少顆行星？|戰略Operation可發生在150多顆行星上，Tactical Mission則覆蓋十多個獨立行星。",
    ),
    "pt-br": (
        "Todo o esquadrão age antes dos inimigos?|Sim. Em cada turno, todo o esquadrão do jogador age primeiro e depois vem o turno do inimigo.",
        "Quantos pontos de ação cada Operador possui?|Cada Operador em campo recebe três pontos de ação por turno para movimento, ataques e habilidades.",
        "A distância altera o custo de movimento?|Sim. Quanto mais longe o Operador se desloca, maior é o custo em pontos de ação.",
        "Armas têm custos de AP diferentes?|Sim. O custo do ataque depende do tipo de arma e algumas ações consomem todos os AP disponíveis.",
        "Onde aparece a chance de acerto?|A chance aparece ao lado do alvo e o Shot Breakdown explica fatores como alcance e cobertura.",
        "Advantage é um recurso compartilhado?|Sim. Advantage Points formam uma reserva comum usada pelas habilidades especiais de todo o esquadrão.",
        "É possível destruir cobertura?|Sim. Foguetes e explosivos podem remover a cobertura inimiga e abrir novas linhas de tiro.",
        "É possível empurrar um inimigo para o Overwatch?|Sim. Force Push ou o Uppercut de Kabb pode lançar o alvo na zona de Overwatch de um aliado.",
        "Três ferimentos causam morte permanente?|Um Operador que acumula três ferimentos morre permanentemente; o tempo exato de tratamento será verificado no lançamento.",
        "É possível desligar a morte permanente?|Sim. A morte permanente vem ativada por padrão, mas pode ser desabilitada nas opções.",
        "O que é The Den?|The Den é a base em Kafrene, com câmera em terceira pessoa e instalações para administrar a companhia.",
        "O que a Holotable mostra em cada Cycle?|A Holotable exibe Operations, Tactical Missions e Influence disponíveis no Cycle atual.",
        "Escolhas em Operations afetam Bonds?|Sim. Algumas escolhas no Galaxy Map podem alterar Bonds e liberar Operations ou missões secundárias.",
        "O que a exploração antes do combate oferece?|Pequenas áreas da história podem conceder contexto, Intel e Advantage Points antes da batalha.",
        "Qual é o tamanho do Galaxy Map?|O mapa estratégico inclui mais de 150 planetas para Operations e mais de doze mundos de Tactical Missions.",
    ),
}

LABELS = {
    "de": ("Kampfsystem", "Bestätigte Regel", "Taktische Bedeutung", "Planungscheck", "Beweisgrenze", "Verwandte Systeme", "Quelle"),
    "fr": ("Système de combat", "Règle confirmée", "Conséquence tactique", "Contrôle pratique", "Limite des preuves", "Systèmes liés", "Source"),
    "it": ("Sistema di combattimento", "Regola confermata", "Impatto tattico", "Controllo pratico", "Limite delle prove", "Sistemi correlati", "Fonte"),
    "es": ("Sistema de combate", "Regla confirmada", "Impacto táctico", "Comprobación práctica", "Límite de pruebas", "Sistemas relacionados", "Fuente"),
    "ja": ("戦闘システム", "確認済みルール", "戦術上の意味", "実戦チェック", "根拠の範囲", "関連システム", "出典"),
    "ko": ("전투 시스템", "확인된 규칙", "전술적 의미", "실전 확인", "근거 범위", "관련 시스템", "출처"),
    "pl": ("System walki", "Potwierdzona zasada", "Znaczenie taktyczne", "Kontrola praktyczna", "Granica dowodów", "Powiązane systemy", "Źródło"),
    "zh-cn": ("战斗系统", "已确认规则", "战术意义", "实用核对", "证据边界", "相关系统", "来源"),
    "zh-tw": ("戰鬥系統", "已確認規則", "戰術意義", "實用核對", "證據邊界", "相關系統", "來源"),
    "pt-br": ("Sistema de combate", "Regra confirmada", "Impacto tático", "Verificação prática", "Limite das provas", "Sistemas relacionados", "Fonte"),
}

PRACTICE = {
    "de": "Nutze diese bestätigte Grenze für die Planung, aber erfinde keine unveröffentlichten Schadenswerte, Abklingzeiten oder Ausnahmen. Prüfe beim Release zuerst Tooltip, Aktionsvorschau und reproduzierbare Mission. Dokumentiere Plattform, Schwierigkeit und Build-Version, bevor eine Abweichung als Regel gilt.",
    "fr": "Utilisez cette limite confirmée pour planifier sans inventer dégâts, délais ou exceptions non publiés. À la sortie, contrôlez d’abord l’infobulle, l’aperçu de l’action et une mission reproductible. Notez plateforme, difficulté et version avant de traiter une différence comme une règle.",
    "it": "Usa questo limite confermato per pianificare senza inventare danni, tempi o eccezioni non pubblicati. Al lancio controlla tooltip, anteprima dell’azione e una missione ripetibile. Registra piattaforma, difficoltà e versione prima di considerare una differenza come regola.",
    "es": "Usa este límite confirmado para planificar sin inventar daño, tiempos ni excepciones no publicadas. Al estrenarse, revisa primero la descripción, la vista previa y una misión repetible. Anota plataforma, dificultad y versión antes de convertir una diferencia en regla.",
    "ja": "この確認済み範囲を編成判断に使い、未公開のダメージ値、待ち時間、例外は作りません。発売後はツールチップ、行動プレビュー、再現可能な任務の順に確認します。差異をルール化する前に機種、難易度、ビルド番号も記録します。",
    "ko": "확인된 범위만 계획에 사용하고 공개되지 않은 피해량, 대기 시간, 예외를 만들지 않습니다. 출시 후에는 툴팁, 행동 미리 보기, 반복 가능한 임무 순서로 확인합니다. 차이를 규칙으로 기록하기 전에 플랫폼, 난이도, 빌드 버전을 함께 남깁니다.",
    "pl": "Używaj tej potwierdzonej granicy do planowania, lecz nie wymyślaj obrażeń, czasów ani wyjątków. Po premierze sprawdź opis, podgląd akcji i powtarzalną misję. Zapisz platformę, trudność i wersję, zanim uznasz różnicę za regułę.",
    "zh-cn": "规划时只采用这条已确认边界，不虚构尚未公布的伤害、冷却、费用或例外。发售后应依次检查说明文字、行动预览和可重复任务，并记录平台、难度与版本号，再判断差异是否属于正式规则。",
    "zh-tw": "規劃時只採用這條已確認邊界，不虛構尚未公布的傷害、冷卻、費用或例外。發售後應依次檢查說明文字、行動預覽及可重複任務，並記錄平台、難度與版本號，再判斷差異是否屬於正式規則。",
    "pt-br": "Use esse limite confirmado para planejar sem inventar dano, recarga ou exceções não publicadas. No lançamento, confira descrição, prévia da ação e uma missão reproduzível. Registre plataforma, dificuldade e versão antes de tratar uma diferença como regra.",
}

BUYERS = (
    ("ea-app-release-time-price", "EA App release time and listed starting price", "EA lists the PC release for August 27, 2026 at 3 PM UTC and shows the base game starting at $49.99 on the EA App. Regional prices and taxes can differ.", "Check the storefront in your own region before paying. The official listing is a current snapshot, not a promise that every platform unlocks at the same local minute."),
    ("standard-edition-contents", "Standard Edition contents", "The Standard Edition includes the base game. Eligible pre-orders also receive the Crystalline Astromech Cosmetic Pack.", "It does not include the three Deluxe cosmetic groups. There is no published gameplay expansion or season pass inside either edition."),
    ("deluxe-edition-contents", "Deluxe Edition contents", "The Deluxe Edition includes the base game, Grand Army of the Republic cosmetics, Shadow Collective cosmetics, five painted weapon themes, and the pre-order pack when purchased in time.", "The announced extras are cosmetic. Compare the actual regional price difference against the listed appearance items rather than assuming mechanical power."),
    ("crystalline-astromech-pack", "Crystalline Astromech pre-order pack explained", "The pre-order pack contains the R3 droid, translucent crystalline heads for R4 and R5 variants, and the new BR-1 droid.", "EA describes this as cosmetic content. Digital pre-orders are automatically entitled; physical purchases use the retailer-provided code."),
    ("grand-army-republic-pack", "Grand Army of the Republic cosmetic pack", "This Deluxe-only pack lists a Republic Officer Uniform, 100th Clone Company Armor Set, and ARC Trooper Armor Set.", "The official description does not assign combat stats to these outfits. Treat the pack as appearance customization unless EA publishes a mechanical change."),
    ("shadow-collective-pack", "Shadow Collective cosmetic pack", "This Deluxe-only pack includes a Pyke Helmet and five tattoo cosmetics themed after Pyke Syndicate, Hutt Cartel, Death Watch, Black Sun, and Crimson Dawn.", "The named factions describe visual themes and do not indicate playable faction campaigns or recruitable classes."),
    ("painted-weapon-themes", "Five Deluxe painted weapon themes", "The Deluxe Edition includes five cosmetic weapon themes: 100th Clone Company, Kafrene Informant, Black Sun Enforcer, Bespin Security, and Separatist Warrior.", "These are painted appearance sets. EA has not described damage bonuses, exclusive weapon classes, or progression boosts attached to them."),
    ("preorder-redemption-deadline", "Pre-order code redemption deadline", "EA's current terms say eligible pre-order codes must be redeemed by August 27, 2027. Digital products are automatically entitled, while physical products require the code from the receipt or email.", "Retailer distribution and local terms can vary. Keep the receipt and verify the code destination before the deadline; do not buy a resold code based only on this guide."),
)


def parsed(locale):
    return [tuple(row.split("|", 1)) for row in RAW[locale]]


def route(locale, slug):
    return f"/systems/{slug}.html" if locale == "en" else f"/{locale}/mechanics/{slug}.html"


def alternates(slug):
    links = "".join(f'<link rel="alternate" hreflang="{tag}" href="{SITE}{route(code, slug)}">' for code, tag, _ in LOCALES)
    return links + f'<link rel="alternate" hreflang="x-default" href="{SITE}{route("en", slug)}">'


def menu(locale, slug):
    current = next(label for code, _, label in LOCALES if code == locale)
    items = "".join(
        f'<a href="{route(code, slug)}" lang="{tag}"{" aria-current=\"page\"" if code == locale else ""}>{escape(label)}</a>'
        for code, tag, label in LOCALES
    )
    return f'<details class="lang-menu"><summary aria-label="Choose language">{escape(current)}</summary><div class="lang-options">{items}</div></details>'


def localized_page(locale, lang, index, item):
    title, direct = item
    slug = SLUGS[index]
    labels = LABELS[locale]
    title = f"{title} — {labels[0]}"
    canonical = SITE + route(locale, slug)
    items = parsed(locale)
    related_ids = ((index + 1) % 15, (index + 5) % 15, (index + 9) % 15)
    related = "".join(
        f'<a class="card" href="{route(locale, SLUGS[n])}"><strong>{escape(items[n][0])}</strong><br><span class="muted">{escape(items[n][1])}</span></a>'
        for n in related_ids
    )
    faq_slugs = ("how-many-action-points-per-turn", "can-you-disable-permadeath", "is-zero-company-single-player")
    faq = "".join(f'<a class="card" href="/{locale}/questions/{s}.html"><strong>FAQ</strong><br><span class="muted">{escape(items[(index+n+2)%15][0])}</span></a>' for n, s in enumerate(faq_slugs))
    schema = {"@context":"https://schema.org","@type":"Article","inLanguage":lang,"headline":title,"description":direct,"url":canonical,"dateModified":TODAY,"about":"Star Wars Zero Company combat system","isPartOf":{"@type":"WebSite","name":"Star Wars Zero Company Wiki","url":SITE+"/"}}
    source = QA_SOURCE if index in (9, 12, 13, 14) else GAMEPLAY_SOURCE
    source_label = "EA official gameplay overview / community Q&A — verified July 26, 2026"
    impact = PRACTICE[locale]
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape(direct)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates(slug)}<meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(direct)}"><meta property="og:image" content="{SITE}/assets/zero-company-hero.png"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav class="nav"><a href="/{locale}/questions/">FAQ</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a><a href="/{locale}/mechanics/">Systems</a>{menu(locale,slug)}</nav></div></header><main class="wrap"><section class="hero"><div class="crumb"><a href="/{locale}/mechanics/">{escape(labels[0])}</a> / {escape(labels[1])}</div><p class="eyebrow">{escape(labels[0])} · {TODAY}</p><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section><section class="block answer"><h2>{escape(labels[1])}</h2><p><strong>{escape(direct)}</strong></p></section><div class="two"><section class="block"><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p><p>{escape(direct)}</p></section><section class="block"><h2>{escape(labels[3])}</h2><ul><li>{escape(direct)}</li><li>{escape(impact)}</li><li>{escape(items[(index+3)%15][1])}</li></ul></section></div><section class="block note"><h2>{escape(labels[4])}</h2><p>{escape(r16.METHOD[locale])}</p><p>{escape(impact)}</p></section><section><h2>{escape(labels[5])}</h2><div class="grid">{related}</div></section><section><h2>FAQ</h2><div class="grid">{faq}</div></section><section class="block"><h2>{escape(labels[6])}</h2><p><a href="{source}" rel="nofollow">{escape(source_label)}</a></p><p class="source">{escape(r16.METHOD[locale])}</p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">{escape(labels[6])}</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def english_system_page(index):
    slug = SLUGS[index]
    # English text is deliberately specific to each topic and matches the localized fact.
    english = (
        ("Does the whole squad act before enemies?", "Yes. During each turn the player's entire squad acts first, followed by the enemy side."),
        ("How many Action Points does each Operator get?", "Every deployed Operator receives three Action Points each turn for movement, attacks, and abilities."),
        ("Does movement distance change AP cost?", "Yes. Moving farther costs more Action Points, so position and route length directly affect the rest of an Operator's turn."),
        ("Do weapon types have different AP costs?", "Yes. Attack cost varies by weapon type, and some attacks consume all Action Points currently available."),
        ("Where can you see Chance-to-Hit details?", "Chance-to-Hit appears beside the target, while the Shot Breakdown panel explains factors including range and cover."),
        ("Are Advantage Points shared by the squad?", "Yes. Advantage Points form a shared squad pool used to activate special abilities across different Operators."),
        ("Can enemy cover be destroyed?", "Yes. Rockets and explosives can remove enemy cover and create a new line of fire for the rest of the squad."),
        ("Can you push an enemy into Overwatch?", "Yes. Force Push or Kabb's Uppercut can move a target into an ally's Overwatch zone and trigger a combined attack."),
        ("Do three Injuries cause permanent death?", "An Operator who accumulates three Injuries dies permanently. Exact recovery timing still needs launch-build verification."),
        ("Can permanent death be disabled?", "Yes. Permadeath is enabled by default, but players can turn it off in the game options."),
        ("What is The Den?", "The Den is Zero Company's base on Kafrene, presented in third person and used to manage Operators, treatment, equipment, and planning."),
        ("What does the Holotable show each Cycle?", "The Holotable displays the Operations, Tactical Missions, and company Influence available during the current Cycle."),
        ("Can Operation choices affect Bonds?", "Yes. Some Galaxy Map choices can affect character Bonds and unlock additional Operations or side missions."),
        ("What can pre-combat exploration reward?", "Short main-story exploration sections can grant world context, Intel, and Advantage Points before turn-based combat begins."),
        ("How many planets are on the Galaxy Map?", "More than 150 planets can host strategic Operations, while Tactical Missions take place across more than a dozen distinct planets."),
    )
    title, direct = english[index]
    canonical = SITE + route("en", slug)
    schema = {"@context":"https://schema.org","@type":"Article","inLanguage":"en","headline":title,"description":direct,"url":canonical,"dateModified":TODAY}
    related = "".join(f'<a class="card" href="{route("en",SLUGS[n])}"><strong>{escape(english[n][0])}</strong><br><span class="muted">{escape(english[n][1])}</span></a>' for n in ((index+1)%15,(index+5)%15,(index+9)%15))
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape(direct)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates(slug)}<script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav class="nav"><a href="/questions/">FAQ</a><a href="/gameplay/">Gameplay</a><a href="/platforms/">Platforms</a><a href="/systems/">Systems</a>{menu("en",slug)}</nav></div></header><main class="wrap"><section class="hero"><div class="crumb"><a href="/systems/">Combat Systems</a> / Confirmed Rule</div><p class="eyebrow">Combat system · {TODAY}</p><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section><section class="block answer"><h2>Direct answer</h2><p><strong>{escape(direct)}</strong></p></section><div class="two"><section class="block"><h2>How to use the rule</h2><p>Build a turn around the confirmed rule above, then inspect the action preview before committing. Preserve enough movement, cover, and shared resources for the objective rather than optimizing only the first shot.</p></section><section class="block"><h2>Launch verification</h2><ul><li>Check the tooltip and action preview.</li><li>Repeat the situation in a normal mission.</li><li>Record platform, difficulty, and build version.</li></ul></section></div><section class="block note"><h2>Evidence boundary</h2><p>This page separates a first-party rule from unpublished balance values. It does not invent damage, cooldowns, costs, unlock timing, or exceptions. Development details remain subject to change until the release build is tested.</p></section><section><h2>Related systems</h2><div class="grid">{related}</div></section><section><h2>Related FAQ</h2><div class="grid"><a class="card" href="/questions/how-many-action-points-per-turn.html">How many AP per turn?</a><a class="card" href="/questions/can-you-disable-permadeath.html">Can permadeath be disabled?</a><a class="card" href="/questions/is-zero-company-single-player.html">Is Zero Company single-player?</a></div></section><section class="block"><h2>Official source</h2><p><a href="{GAMEPLAY_SOURCE}" rel="nofollow">EA gameplay overview</a> · <a href="{QA_SOURCE}" rel="nofollow">EA community Q&amp;A</a></p><p class="source">Checked July 26, 2026. Trailer interpretation and genre comparison are not treated as proof.</p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">Sources</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def mark_english_detail_faq(path):
    html = path.read_text(encoding="utf-8")
    html = html.replace('href="/gameplay/"', 'href="/confirmed/"')
    html = html.replace('href="/platforms/"', 'href="/official/platforms.html"')
    html = html.replace(
        "<section><h2>Related FAQ</h2>",
        "<!-- DETAIL_FAQ_START --><section><h2>Related FAQ</h2>",
        1,
    )
    html = html.replace(
        '</div></section><section class="block"><h2>Official source</h2>',
        '</div></section><!-- DETAIL_FAQ_END --><section class="block"><h2>Official source</h2>',
        1,
    )
    path.write_text(html, encoding="utf-8")


def fix_buyer_links(path):
    html = path.read_text(encoding="utf-8")
    html = html.replace('href="/platforms/"', 'href="/official/platforms.html"')
    html = html.replace(
        'href="/questions/can-you-preorder-zero-company.html"',
        'href="/questions/should-you-preorder.html"',
    )
    html = html.replace(
        'href="/questions/when-does-zero-company-release.html"',
        'href="/questions/when-does-star-wars-zero-company-release.html"',
    )
    path.write_text(html, encoding="utf-8")


def buyer_page(item):
    slug, title, direct, boundary = item
    canonical = f"{SITE}/preorder/{slug}.html"
    related = "".join(f'<a class="card" href="/preorder/{x[0]}.html"><strong>{escape(x[1])}</strong><br><span class="muted">{escape(x[2])}</span></a>' for x in BUYERS if x[0] != slug)[:4200]
    schema = {"@context":"https://schema.org","@type":"Article","inLanguage":"en","headline":title,"description":direct,"url":canonical,"dateModified":TODAY}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Zero Company Wiki</title><meta name="description" content="{escape(direct)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav class="nav"><a href="/questions/">FAQ</a><a href="/news/">News</a><a href="/platforms/">Platforms</a><a href="/preorder/">Pre-order</a></nav></div></header><main class="wrap"><section class="hero"><div class="crumb"><a href="/preorder/">Buyer Guide</a> / Verified contents</div><p class="eyebrow">Purchase decision · checked {TODAY}</p><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section><section class="block answer"><h2>Direct answer</h2><p><strong>{escape(direct)}</strong></p></section><div class="two"><section class="block"><h2>What the listing confirms</h2><p>{escape(direct)}</p><p>The comparison uses EA's published product description and terms. It distinguishes the base-game license, pre-order entitlement, and Deluxe-only appearance packs.</p></section><section class="block"><h2>Before you buy</h2><p>{escape(boundary)}</p><ul><li>Confirm region and platform.</li><li>Compare the live checkout price.</li><li>Save any physical redemption code.</li></ul></section></div><section class="block note"><h2>Evidence boundary</h2><p>{escape(boundary)}</p><p>Prices, taxes, retailer availability, and local unlock timing can change. This unofficial guide does not sell a key and does not treat cosmetic names as proof of gameplay bonuses.</p></section><section><h2>Related buyer guides</h2><div class="grid">{related}</div></section><section><h2>Related FAQ</h2><div class="grid"><a class="card" href="/questions/can-you-preorder-zero-company.html">Can you pre-order?</a><a class="card" href="/questions/what-platforms-is-zero-company-on.html">Supported platforms</a><a class="card" href="/questions/when-does-zero-company-release.html">Release date</a></div></section><section class="block"><h2>Official source</h2><p><a href="{BUY_SOURCE}" rel="nofollow">EA pre-order announcement and edition list</a></p><p class="source">Checked July 26, 2026 against EA's purchase page and published terms.</p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">Sources</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def buyer_hub(cards):
    canonical = f"{SITE}/preorder/"
    schema = {"@context":"https://schema.org","@type":"CollectionPage","inLanguage":"en","name":"Zero Company verified edition and pre-order guides","url":canonical,"dateModified":TODAY}
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Zero Company Editions &amp; Pre-order Guide</title><meta name="description" content="Verified comparison of Zero Company Standard and Deluxe editions, cosmetic packs, price, release time, and redemption terms."><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><script type="application/ld+json">{json.dumps(schema)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/">Star Wars Zero Company Wiki</a><nav class="nav"><a href="/questions/">FAQ</a><a href="/news/">News</a><a href="/platforms/">Platforms</a><a href="/preorder/">Pre-order</a></nav></div></header><main class="wrap"><section class="hero"><p class="eyebrow">Verified buyer guide · {TODAY}</p><h1>Zero Company Editions &amp; Pre-order Guide</h1><p class="lead">Compare only the contents EA currently lists. These guides separate base-game access, time-limited pre-order entitlement, and Deluxe cosmetic packs.</p></section><section class="block answer"><h2>Quick decision</h2><p>Choose Standard for the base game. Choose Deluxe only if the listed appearance packs justify the regional price difference for you. Pre-ordering either eligible edition adds the Crystalline Astromech Cosmetic Pack.</p></section><section><h2>Verified edition and pre-order guides</h2><div class="grid">{cards}</div></section><section class="block note"><h2>Evidence boundary</h2><p>Prices, tax, retailer availability and platform unlock timing may differ by region. Cosmetic names are not treated as gameplay bonuses, playable factions, or extra campaign content.</p></section><section class="block"><h2>Official source</h2><p><a href="{BUY_SOURCE}" rel="nofollow">EA pre-order announcement and edition list</a></p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">Sources</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def update_hub(path, marker, heading, cards):
    html = path.read_text(encoding="utf-8-sig", errors="ignore")
    html = re.sub(fr'<!-- {marker}-START -->.*?<!-- {marker}-END -->', "", html, flags=re.S)
    section = f'<!-- {marker}-START --><section><h2>{escape(heading)}</h2><div class="grid">{cards}</div></section><!-- {marker}-END -->'
    if "</main>" not in html:
        raise ValueError(f"No main close in {path}")
    path.write_text(html.replace("</main>", section + "</main>", 1), encoding="utf-8")


def main():
    created = 0
    for locale, lang, _ in LOCALES:
        if locale == "en":
            out = ROOT / "systems"
            for i, slug in enumerate(SLUGS):
                path = out / f"{slug}.html"
                path.write_text(english_system_page(i), encoding="utf-8")
                mark_english_detail_faq(path)
                created += 1
            continue
        out = ROOT / locale / "mechanics"
        out.mkdir(parents=True, exist_ok=True)
        items = parsed(locale)
        for i, item in enumerate(items):
            (out / f"{SLUGS[i]}.html").write_text(localized_page(locale, lang, i, item), encoding="utf-8")
            created += 1
        cards = "".join(f'<a class="card" href="{route(locale,slug)}"><strong>{escape(item[0])}</strong><br><span class="muted">{escape(item[1])}</span></a>' for slug, item in zip(SLUGS, items))
        update_hub(out / "index.html", "ROUND17-SYSTEMS", LABELS[locale][0], cards)

    preorder = ROOT / "preorder"
    preorder.mkdir(exist_ok=True)
    for item in BUYERS:
        path = preorder / f"{item[0]}.html"
        path.write_text(buyer_page(item), encoding="utf-8")
        fix_buyer_links(path)
        created += 1
    cards = "".join(f'<a class="card" href="/preorder/{x[0]}.html"><strong>{escape(x[1])}</strong><br><span class="muted">{escape(x[2])}</span></a>' for x in BUYERS)
    path = preorder / "index.html"
    path.write_text(buyer_hub(cards), encoding="utf-8")
    fix_buyer_links(path)
    print(f"Round 17 created {created} pages")


if __name__ == "__main__":
    main()
