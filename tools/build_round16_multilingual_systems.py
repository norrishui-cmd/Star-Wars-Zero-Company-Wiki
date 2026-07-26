#!/usr/bin/env python3
"""Round 16: localize a second set of confirmed systems with English visual parity."""

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
    "astromechs-unlock-early",
    "bonds-cross-training-benefits",
    "custom-names-backstories",
    "hawks-death-mission-failure",
    "hawks-required-story-missions",
    "mandalorian-armor-cly-only",
    "no-fog-of-war",
    "no-specialized-call-ins",
    "real-time-cutscenes",
    "secondary-advanced-specializations",
)

# title | direct answer | practical consequence
RAW = {
    "de": (
        "Wann kann man ein Astromech-Team aufbauen?|Astromechs werden relativ früh freigeschaltet; nach Beginn ihrer Rekrutierung ist ein vollständiges Droidenteam möglich.|In Storymissionen belegt Hawks weiterhin einen Pflichtplatz. Ein reines Astromech-Team ist deshalb vor allem für freie Einsätze relevant; genaue Rekrutierungskosten und Droidenrollen bleiben bis zum Release offen.",
        "Wie funktioniert Cross-Training durch Bonds?|Verbündete mit einem Bond können Unterstützungsfähigkeiten und Cross-Training-Vorteile freischalten, die neue Fertigkeiten und Werte teilen.|Bonds sind ein taktisches Fortschrittssystem und kein Romanzensystem. Wiederkehrende Paare können die Teamplanung verändern, aber Schwellenwerte und konkrete Belohnungen wurden noch nicht vollständig veröffentlicht.",
        "Können eigene Operatoren Namen und Hintergrundgeschichten erhalten?|Rekrutierte eigene Operatoren können mit Namen und Hintergrundgeschichten angepasst werden.|Die Identität wird bei der Rekrutierung gestaltet und nicht später über einen zufälligen XCOM-ähnlichen Spitznamenpool verdient. Kampffortschritt, Bonds und Missionshistorie bleiben davon getrennte Systeme.",
        "Was passiert, wenn Hawks stirbt?|Wenn Hawks im Kampf stirbt, scheitert die Mission automatisch und muss neu gestartet werden.|Hawks ist damit anders geschützt als normale Operatoren. Deckung, Heilung und sichere Positionierung haben in Storymissionen besondere Priorität; dies ist keine bestätigte Aussage zu Speicherslots oder Ironman-Regeln.",
        "Muss Hawks an Storymissionen teilnehmen?|Ja. Hawks muss bei Storymissionen Teil des eingesetzten Teams sein.|Der Pflichtplatz reduziert die frei wählbaren Plätze einer normalen Vierergruppe. Bei optionalen Missionen kann die Zusammenstellung flexibler sein; die offizielle Aussage nennt jedoch nicht jede missionsspezifische Ausnahme.",
        "Kann jeder Operator mandalorianische Rüstung tragen?|Nein. Vollständige mandalorianische Rüstung ist Cly vorbehalten; eigene Operatoren erhalten keine komplette Mandalorianer-Ausrüstung.|Clys visuelle und erzählerische Identität bleibt einzigartig. Kosmetische Anpassung anderer Rekruten darf nicht als Beleg für eine vollständige Mandalorianer-Klasse oder entsprechende Werte verstanden werden.",
        "Gibt es Fog of War?|Nein. Zero Company verwendet keinen klassischen Fog of War, doch große Reichweite garantiert nicht gegen jedes Ziel eine freie Sichtlinie.|Scharfschützen müssen Gelände, Deckung und Sichtwinkel weiterhin berücksichtigen. Ein Team nur aus Fernkämpfern ist möglich, aber nicht automatisch optimal und unveröffentlichte Trefferwerte werden nicht angenommen.",
        "Gibt es LAAT- oder andere Spezialunterstützung?|Nein. Es gibt keine spezialisierten Call-ins auf dem Schlachtfeld.|Spieler sollten Unterstützung, Heilung und Kontrolle in den eingesetzten Trupp einbauen, statt mit einer externen Rettung oder einem einmaligen Luftschlag zu planen. Normale Missionsereignisse sind davon zu unterscheiden.",
        "Werden die Zwischensequenzen in Echtzeit gerendert?|Die meisten Zwischensequenzen werden in Echtzeit dargestellt; wenige kleinere Ausnahmen sind vorgerendert.|Dadurch können der angepasste Hawks und eigene Rekruten in vielen Szenen konsistent erscheinen. Welche Ausnahmen Anpassungen nicht zeigen und wie Plattformen die Darstellung beeinflussen, muss zum Release geprüft werden.",
        "Was sind sekundäre und fortgeschrittene Spezialisierungen?|EA bestätigt, dass Ausrüstung und Spielstil durch sekundäre oder fortgeschrittene Spezialisierungen weiter geformt werden können.|Sie erweitern Builds über die acht Standardrollen hinaus. Eine vollständige Liste, Fähigkeitsbäume und Freischaltbedingungen sind noch nicht öffentlich und werden deshalb nicht erfunden.",
    ),
    "fr": (
        "Quand peut-on former une équipe d’astromécanos ?|Les astromécanos se débloquent assez tôt et une équipe complète devient possible dès que leur recrutement est disponible.|Hawks occupe encore une place obligatoire dans les missions principales. Une escouade uniquement composée de droïdes concerne donc surtout les missions libres ; les coûts et rôles exacts restent à vérifier à la sortie.",
        "Comment fonctionne l’entraînement croisé des Bonds ?|Des unités liées par un Bond peuvent débloquer des capacités de soutien et des avantages d’entraînement croisé partageant compétences et statistiques.|Les Bonds constituent une progression tactique, pas un système de romance. Des duos réguliers peuvent modifier la construction de l’équipe, mais les seuils et récompenses détaillés ne sont pas encore publiés.",
        "Les agents personnalisés peuvent-ils avoir un nom et une histoire ?|Les agents recrutés peuvent recevoir un nom et une histoire personnalisés.|L’identité est créée au recrutement au lieu d’être gagnée plus tard via une liste aléatoire de surnoms façon XCOM. La progression au combat, les Bonds et l’historique des missions restent des systèmes distincts.",
        "Que se passe-t-il si Hawks meurt ?|La mort de Hawks au combat provoque automatiquement l’échec de la mission, qui doit être recommencée.|Hawks n’est donc pas traité comme un agent ordinaire. Couverture, soins et position sûre deviennent prioritaires dans l’histoire ; cette règle ne confirme pas le nombre de sauvegardes ni un mode Ironman.",
        "Hawks doit-il participer aux missions principales ?|Oui. Hawks doit faire partie de l’équipe déployée dans les missions principales.|Sa place obligatoire réduit le nombre de choix libres dans une escouade standard de quatre. Les opérations facultatives peuvent être plus souples, sans que chaque exception soit détaillée officiellement.",
        "Tous les agents peuvent-ils porter une armure mandalorienne ?|Non. L’armure mandalorienne complète est réservée à Cly et n’est pas disponible pour les agents personnalisés.|L’identité visuelle et narrative de Cly reste unique. Des options cosmétiques pour les recrues ne prouvent ni l’existence d’une classe mandalorienne complète ni des statistiques associées.",
        "Y a-t-il un brouillard de guerre ?|Non. Zero Company n’utilise pas de brouillard de guerre classique, mais une longue portée ne garantit pas une ligne de vue sur chaque cible.|Les tireurs d’élite doivent toujours tenir compte du terrain, des couverts et des angles. Une équipe à distance est autorisée sans être automatiquement optimale ; aucun taux de précision inédit n’est supposé.",
        "Existe-t-il des renforts LAAT ou des appels spécialisés ?|Non. Il n’existe aucun appel de soutien spécialisé sur le champ de bataille.|Il faut intégrer soin, contrôle et soutien à l’escouade déployée plutôt que compter sur une extraction d’urgence ou une frappe externe. Les événements scénarisés d’une mission restent une catégorie différente.",
        "Les cinématiques sont-elles rendues en temps réel ?|La plupart des cinématiques sont rendues en temps réel, avec quelques petites exceptions pré-rendues.|Hawks et les recrues personnalisées peuvent ainsi apparaître de façon cohérente dans de nombreuses scènes. Les exceptions et les différences entre plateformes seront vérifiées sur la version finale.",
        "Que sont les spécialisations secondaires et avancées ?|EA indique que l’équipement et le style de jeu peuvent évoluer grâce à des spécialisations secondaires ou avancées.|Elles prolongent les builds au-delà des huit rôles standards. La liste complète, les arbres de compétences et les conditions de déblocage ne sont pas publics et ne sont donc pas inventés.",
    ),
    "it": (
        "Quando si può creare una squadra di astromech?|Gli astromech si sbloccano abbastanza presto e, quando il reclutamento è disponibile, è possibile formare una squadra completa di droidi.|Nelle missioni della storia Hawks occupa comunque un posto obbligatorio. Una squadra solo astromech riguarda soprattutto gli incarichi liberi; costi e ruoli precisi saranno verificati al lancio.",
        "Come funziona il cross-training dei Bond?|Le unità unite da un Bond possono sbloccare abilità di supporto e vantaggi di cross-training che condividono nuove capacità e statistiche.|I Bond sono progressione tattica, non romance. Coppie ricorrenti possono cambiare la costruzione della squadra, ma soglie e ricompense dettagliate non sono ancora state pubblicate.",
        "Gli operatori personalizzati possono avere nome e storia?|Gli operatori reclutati possono ricevere nomi e storie personali.|L’identità viene definita durante il reclutamento, non ottenuta in seguito da un elenco casuale di soprannomi in stile XCOM. Progressione, Bond e cronologia delle missioni restano sistemi separati.",
        "Cosa succede se Hawks muore?|La morte di Hawks in combattimento causa automaticamente il fallimento della missione e obbliga a ricominciarla.|Hawks non viene quindi trattato come un operatore normale. Copertura, cure e posizione sicura hanno priorità nelle missioni narrative; la regola non conferma slot di salvataggio o modalità Ironman.",
        "Hawks deve partecipare alle missioni della storia?|Sì. Hawks deve far parte della squadra schierata nelle missioni narrative.|Il posto obbligatorio riduce le scelte libere in una squadra standard di quattro. Gli incarichi opzionali possono essere più flessibili, ma la risposta ufficiale non elenca ogni eccezione.",
        "Ogni operatore può indossare un’armatura mandaloriana?|No. L’armatura mandaloriana completa è esclusiva di Cly e non è disponibile per gli operatori personalizzati.|L’identità visiva e narrativa di Cly rimane unica. Le opzioni cosmetiche delle reclute non dimostrano una classe mandaloriana completa né bonus di combattimento collegati.",
        "Esiste la nebbia di guerra?|No. Zero Company non usa la classica nebbia di guerra, ma la lunga distanza non garantisce una linea di tiro verso ogni bersaglio.|I tiratori devono ancora valutare terreno, coperture e angoli. Una squadra tutta a distanza è permessa senza essere automaticamente ottimale; non vengono ipotizzati valori di precisione.",
        "Ci sono supporti LAAT o richiami specializzati?|No. Non esistono richiami specializzati sul campo di battaglia.|Supporto, cure e controllo devono essere inclusi nella squadra invece di contare su un’estrazione d’emergenza o un attacco esterno. Gli eventi scriptati della missione sono un caso distinto.",
        "Le scene d’intermezzo sono in tempo reale?|La maggior parte delle scene viene renderizzata in tempo reale, con poche eccezioni minori prerenderizzate.|Hawks e le reclute personalizzate possono così apparire coerentemente in molte sequenze. Le eccezioni e le differenze tra piattaforme richiedono una verifica sulla versione finale.",
        "Cosa sono le specializzazioni secondarie e avanzate?|EA afferma che equipaggiamento e stile possono essere sviluppati con specializzazioni secondarie o avanzate.|Ampliano le build oltre gli otto ruoli standard. Elenco completo, alberi delle abilità e requisiti di sblocco non sono pubblici e non vengono presentati come dati certi.",
    ),
    "es": (
        "¿Cuándo se puede formar un equipo de astromecánicos?|Los astromecánicos se desbloquean relativamente pronto y, cuando su reclutamiento está disponible, se puede formar un equipo completo de droides.|Hawks sigue ocupando una plaza obligatoria en misiones de historia. Un equipo solo de astromecánicos encaja sobre todo en operaciones libres; costes y funciones exactas se comprobarán al lanzamiento.",
        "¿Cómo funciona el entrenamiento cruzado de Bonds?|Las unidades con un Bond pueden desbloquear habilidades de apoyo y ventajas de entrenamiento cruzado que comparten capacidades y estadísticas.|Los Bonds son progresión táctica, no romance. Las parejas habituales pueden cambiar la composición, pero todavía no se han publicado todos los umbrales ni recompensas.",
        "¿Los agentes personalizados pueden tener nombre e historia?|Los agentes reclutados pueden recibir nombres e historias personalizados.|La identidad se crea durante el reclutamiento y no se obtiene después mediante una lista aleatoria de apodos al estilo XCOM. Progreso de combate, Bonds e historial de misiones siguen siendo sistemas separados.",
        "¿Qué ocurre si Hawks muere?|Si Hawks muere en combate, la misión fracasa automáticamente y debe reiniciarse.|Hawks no funciona como un agente corriente. Cobertura, curación y posición segura son prioritarias en la historia; esta regla no confirma cantidad de guardados ni modo Ironman.",
        "¿Hawks debe participar en las misiones de historia?|Sí. Hawks tiene que formar parte del equipo desplegado en las misiones narrativas.|Su plaza obligatoria reduce las elecciones libres de un pelotón estándar de cuatro. Las operaciones opcionales pueden ser más flexibles, aunque la respuesta oficial no enumera cada excepción.",
        "¿Cualquier agente puede llevar armadura mandaloriana?|No. La armadura mandaloriana completa es exclusiva de Cly y no está disponible para agentes personalizados.|La identidad visual y narrativa de Cly se mantiene única. Las opciones cosméticas de otros reclutas no prueban una clase mandaloriana completa ni estadísticas asociadas.",
        "¿Hay niebla de guerra?|No. Zero Company no utiliza niebla de guerra clásica, pero el alcance largo no garantiza línea de visión hacia todos los objetivos.|Los tiradores aún deben considerar terreno, coberturas y ángulos. Un equipo de largo alcance está permitido sin ser automáticamente óptimo; no se inventan porcentajes de precisión.",
        "¿Existen apoyos LAAT o llamadas especializadas?|No. No hay llamadas de apoyo especializadas en el campo de batalla.|Curación, control y apoyo deben formar parte del pelotón desplegado, sin depender de una extracción de emergencia o ataque externo. Los eventos guionizados de una misión son diferentes.",
        "¿Las cinemáticas se renderizan en tiempo real?|La mayoría de cinemáticas se renderizan en tiempo real, salvo unas pocas excepciones menores prerenderizadas.|Hawks y los reclutas personalizados pueden aparecer de forma coherente en muchas escenas. Las excepciones y diferencias entre plataformas requieren comprobación en la versión final.",
        "¿Qué son las especializaciones secundarias y avanzadas?|EA afirma que el equipo y el estilo pueden evolucionar mediante especializaciones secundarias o avanzadas.|Amplían las configuraciones más allá de los ocho roles estándar. La lista completa, árboles de habilidades y requisitos no son públicos y no se presentan como hechos.",
    ),
    "ja": (
        "アストロメクだけの部隊はいつ作れる？|アストロメクは比較的早い段階で解放され、採用が可能になればドロイドだけの部隊を組めます。|ストーリー任務ではHawksが必須枠を使うため、完全なアストロメク編成は主に自由任務向けです。採用コストや各機体の最終的な役割は発売後に確認します。",
        "Bondのクロストレーニングはどう機能する？|Bondを結んだ隊員は支援アビリティやクロストレーニング効果を解放し、新しいスキルや能力値を共有できます。|Bondは恋愛ではなく戦術的な成長システムです。同じ組み合わせで出撃する価値はありますが、必要な段階や報酬の全一覧はまだ公開されていません。",
        "カスタム隊員に名前と経歴を設定できる？|採用したカスタム隊員には名前と背景設定を付けられます。|個性は採用時に作成し、XCOM風のランダムな通称を後から獲得する方式ではありません。戦闘成長、Bond、任務履歴は名前とは別の仕組みとして扱われます。",
        "Hawksが死亡するとどうなる？|戦闘中にHawksが死亡すると任務は自動的に失敗し、最初からやり直す必要があります。|Hawksは通常の隊員と同じ死亡処理ではありません。ストーリー任務では遮蔽、回復、安全な位置取りを優先すべきですが、セーブ枠やIronmanの仕様までは確認されていません。",
        "ストーリー任務にHawksは必須？|はい。ストーリー任務ではHawksを出撃部隊に入れる必要があります。|標準4人部隊のうち1枠が固定されるため、自由に選べる人数が減ります。任意のOperationでは柔軟な編成が可能でも、公式回答はすべての例外を列挙していません。",
        "全隊員がマンダロリアン装甲を着られる？|いいえ。完全なマンダロリアン装甲はCly専用で、カスタム隊員には用意されません。|Cly固有の外見と物語上の立場が保たれます。他の隊員のコスメ要素から、未発表のマンダロリアンクラスや戦闘ボーナスが存在すると推測してはいけません。",
        "戦場にFog of Warはある？|いいえ。Zero Companyは古典的なFog of Warを採用しませんが、射程が長くても全目標への視線が保証されるわけではありません。|狙撃役でも地形、遮蔽、角度の確認が必要です。遠距離中心の部隊は組めますが常に最適とは限らず、未公開の命中率は追加しません。",
        "LAATなどの特殊支援要請はある？|いいえ。戦場で使える専用の支援要請はありません。|緊急脱出や外部攻撃に頼らず、回復、制御、支援を出撃部隊の中に組み込む必要があります。任務中の演出イベントはプレイヤーが呼ぶ支援とは別です。",
        "カットシーンはリアルタイム描画？|ゲーム内カットシーンの大半はリアルタイム描画で、一部に小規模なプリレンダリング映像があります。|カスタマイズしたHawksや隊員が多くの場面で反映されます。どの映像が例外か、機種ごとの差があるかは製品版での確認が必要です。",
        "セカンダリ・上級Specializationとは？|EAは装備とプレイスタイルをセカンダリまたは上級Specializationでさらに調整できると説明しています。|8種の標準ロールを超えてBuildの個性を広げます。ただし完全な一覧、スキルツリー、解放条件は未公開なので確定情報として作成しません。",
    ),
    "ko": (
        "아스트로메크 분대는 언제 만들 수 있나요?|아스트로메크는 비교적 이른 시점에 해금되며 모집이 가능해지면 드로이드만으로 분대를 구성할 수 있습니다.|스토리 임무에서는 Hawks가 필수 슬롯을 차지합니다. 완전한 아스트로메크 편성은 주로 자유 임무에 해당하며 모집 비용과 최종 역할은 출시 후 확인합니다.",
        "Bond 교차 훈련은 어떻게 작동하나요?|Bond를 맺은 대원은 지원 능력과 교차 훈련 효과를 해금하여 새로운 기술과 능력치를 공유할 수 있습니다.|Bond는 로맨스가 아니라 전술 성장 시스템입니다. 반복해서 함께 출전하는 조합은 중요하지만 정확한 단계와 보상 전체 목록은 아직 공개되지 않았습니다.",
        "커스텀 대원에게 이름과 배경을 설정할 수 있나요?|모집한 커스텀 대원에게 이름과 배경 이야기를 지정할 수 있습니다.|정체성은 모집할 때 만들며 XCOM처럼 무작위 별명을 나중에 얻는 방식이 아닙니다. 전투 성장, Bond, 임무 기록은 이름과 별개의 시스템으로 유지됩니다.",
        "Hawks가 죽으면 어떻게 되나요?|전투 중 Hawks가 사망하면 임무가 자동 실패하고 다시 시작해야 합니다.|Hawks는 일반 대원과 다른 보호 규칙을 가집니다. 스토리 임무에서는 엄폐, 치료, 안전한 위치가 우선이지만 저장 슬롯이나 Ironman 규칙까지 확인된 것은 아닙니다.",
        "스토리 임무에 Hawks가 반드시 필요한가요?|네. 스토리 임무에서는 Hawks를 출전 분대에 포함해야 합니다.|표준 4인 분대에서 한 자리가 고정되어 자유 선택 인원이 줄어듭니다. 선택 Operation은 더 유연할 수 있지만 공식 답변은 모든 예외를 나열하지 않았습니다.",
        "모든 대원이 만달로리안 갑옷을 입을 수 있나요?|아니요. 완전한 만달로리안 갑옷은 Cly 전용이며 커스텀 대원에게 제공되지 않습니다.|Cly의 고유한 외형과 서사 정체성이 유지됩니다. 다른 대원의 장식 선택지를 근거로 미공개 만달로리안 클래스나 전투 보너스를 추정하면 안 됩니다.",
        "전장의 Fog of War가 있나요?|아니요. Zero Company는 전통적인 Fog of War를 사용하지 않지만 사거리가 길다고 모든 목표에 시야가 확보되는 것은 아닙니다.|저격수도 지형, 엄폐, 각도를 확인해야 합니다. 원거리 분대는 가능하지만 항상 최적은 아니며 공개되지 않은 명중률은 추가하지 않습니다.",
        "LAAT 같은 특수 지원 호출이 있나요?|아니요. 전장에서 사용할 수 있는 전용 지원 호출은 없습니다.|긴급 탈출이나 외부 공격에 의존하지 말고 치료, 제어, 지원을 출전 분대 안에 넣어야 합니다. 임무의 연출 이벤트는 플레이어 호출 기능과 다릅니다.",
        "컷신은 실시간 렌더링인가요?|게임 내 컷신 대부분은 실시간으로 렌더링되며 일부 작은 예외만 사전 렌더링됩니다.|커스터마이즈한 Hawks와 대원이 여러 장면에 일관되게 표시될 수 있습니다. 예외 영상과 플랫폼 차이는 정식 버전에서 확인해야 합니다.",
        "보조 및 고급 Specialization은 무엇인가요?|EA는 보조 또는 고급 Specialization으로 장비와 플레이 방식을 더 발전시킬 수 있다고 설명합니다.|8개 표준 역할을 넘어 Build 정체성을 확장합니다. 전체 목록, 스킬 트리, 해금 조건은 아직 공개되지 않아 확정 정보로 만들지 않습니다.",
    ),
    "pl": (
        "Kiedy można zbudować drużynę astromechów?|Astromechy odblokowują się dość wcześnie, a po udostępnieniu rekrutacji można stworzyć pełny zespół droidów.|W misjach fabularnych Hawks nadal zajmuje obowiązkowe miejsce. Skład wyłącznie z astromechów dotyczy głównie swobodnych zadań; koszty i dokładne role wymagają sprawdzenia po premierze.",
        "Jak działa trening krzyżowy poprzez Bonds?|Jednostki połączone Bondem mogą odblokować zdolności wsparcia oraz korzyści treningu krzyżowego, dzieląc nowe umiejętności i statystyki.|Bonds to rozwój taktyczny, a nie romans. Stałe pary mogą zmieniać budowę drużyny, lecz progi i pełne nagrody nie zostały jeszcze opublikowane.",
        "Czy własny Operator może mieć imię i historię?|Rekrutowanym własnym Operatorom można nadać imiona i historie postaci.|Tożsamość powstaje podczas rekrutacji, zamiast pojawiać się później z losowej puli pseudonimów jak w XCOM. Rozwój bojowy, Bonds i historia misji pozostają osobnymi systemami.",
        "Co się stanie, jeśli Hawks zginie?|Śmierć Hawksa w walce automatycznie kończy misję porażką i wymaga jej ponownego rozpoczęcia.|Hawks nie podlega więc dokładnie tej samej zasadzie co zwykli Operatorzy. Osłona, leczenie i bezpieczna pozycja są priorytetem; nie potwierdza to liczby zapisów ani trybu Ironman.",
        "Czy Hawks musi brać udział w misjach fabularnych?|Tak. Hawks musi znaleźć się w zespole wysłanym na misję fabularną.|Obowiązkowe miejsce ogranicza swobodny wybór w standardowej czwórce. Opcjonalne Operations mogą pozwalać na większą elastyczność, ale oficjalna odpowiedź nie wymienia wszystkich wyjątków.",
        "Czy każdy Operator może nosić zbroję mandaloriańską?|Nie. Pełna zbroja mandaloriańska jest przeznaczona wyłącznie dla Cly i nie jest dostępna dla własnych Operatorów.|Wygląd i fabularna tożsamość Cly pozostają wyjątkowe. Kosmetyka innych rekrutów nie potwierdza pełnej klasy Mandalorianina ani powiązanych premii bojowych.",
        "Czy występuje mgła wojny?|Nie. Zero Company nie korzysta z klasycznej mgły wojny, ale duży zasięg nie gwarantuje linii widzenia do każdego celu.|Strzelcy nadal muszą analizować teren, osłony i kąty. Drużyna dystansowa jest dozwolona, ale nie zawsze optymalna; nie dodajemy nieujawnionych wartości celności.",
        "Czy są wezwania LAAT lub inne wsparcie specjalne?|Nie. Na polu walki nie ma wyspecjalizowanych wezwań wsparcia.|Leczenie, kontrolę i wsparcie trzeba umieścić w wysłanym zespole, zamiast liczyć na awaryjną ewakuację lub zewnętrzny atak. Skryptowe wydarzenia misji są osobną kategorią.",
        "Czy przerywniki są renderowane w czasie rzeczywistym?|Większość przerywników powstaje w czasie rzeczywistym, a tylko kilka drobnych wyjątków jest renderowanych wcześniej.|Dzięki temu zmieniony Hawks i własni rekruci mogą być widoczni w wielu scenach. Wyjątki i różnice platformowe trzeba sprawdzić w wersji premierowej.",
        "Czym są specjalizacje dodatkowe i zaawansowane?|EA podaje, że wyposażenie i styl gry można rozwijać poprzez dodatkowe lub zaawansowane Specializations.|Rozszerzają buildy poza osiem standardowych ról. Pełna lista, drzewa umiejętności i warunki odblokowania nie są publiczne, więc nie przedstawiamy ich jako faktów.",
    ),
    "zh-cn": (
        "什么时候能组建全机械师机器人小队？|机械师机器人会在流程较早阶段解锁；开放招募后，玩家可以组建全部由机器人构成的队伍。|剧情任务仍会固定占用一个Hawks位置，因此纯机器人编队主要适用于自由任务。具体招募费用、解锁节点和每种机体的最终定位仍需在正式版中核验。",
        "Bond跨职业训练如何运作？|建立Bond的队员能够解锁支援能力与跨职业训练收益，从而共享新的技能和属性。|Bond是战术成长系统，不是恋爱系统。固定搭档可能改变小队构筑，但官方尚未公布所有阶段门槛、奖励名称和最终数值，页面不会提前编造。",
        "自定义队员可以设置姓名和背景故事吗？|招募的自定义队员可以拥有玩家设定的姓名与背景故事。|角色身份在招募时建立，不会像XCOM式随机绰号池那样等待后续自动授予。战斗成长、Bond关系与任务履历是相互关联但彼此独立的系统。",
        "Hawks死亡后会发生什么？|如果Hawks在战斗中死亡，任务会自动失败，玩家必须重新开始该任务。|Hawks与普通队员的死亡处理不同。剧情任务中应优先保证其掩体、治疗和安全位置；这一确认并不等于官方已经公布存档数量或Ironman规则。",
        "剧情任务必须带Hawks吗？|是。所有剧情任务都要求Hawks进入出战小队。|标准四人小队中会有一个固定位置，玩家可自由选择的队员数量因此减少。可选Operation可能允许更灵活的编队，但官方回答没有列出每一个特殊例外。",
        "所有队员都能穿完整曼达洛护甲吗？|不能。完整曼达洛护甲是Cly的专属装备，不提供给自定义队员。|这一限制保留Cly独特的视觉形象和剧情身份。其他队员拥有外观选项，并不能证明存在未公布的完整曼达洛职业或对应战斗属性。",
        "战场上有战争迷雾吗？|没有。Zero Company不采用经典战争迷雾，但远距离并不保证对所有目标都拥有有效视线。|狙击队员仍需判断地形、掩体与射击角度。全远程队伍可以成立却不一定总是最优；未公布的命中率和射程数值不会写成事实。",
        "能呼叫LAAT或其他特殊支援吗？|不能。游戏没有供玩家主动使用的专用战场支援呼叫。|治疗、控制和辅助能力必须安排在出战队伍内部，不能预设有紧急撤离或外部轰炸兜底。任务中的剧情演出事件与可操作支援功能不是同一概念。",
        "过场动画是实时渲染的吗？|大部分游戏内过场动画采用实时渲染，只有少量次要片段属于预渲染例外。|因此自定义Hawks和招募队员能够在许多剧情场景中保持外观一致。哪些片段属于例外、不同平台是否有差异，需要在正式版本中复核。",
        "什么是次级与高级Specialization？|EA确认装备和玩法风格可以通过次级或高级Specialization进一步塑造。|这些路线把Build成长扩展到八种标准起始职业之外。完整名称、技能树和解锁条件尚未公开，本站不会把推测列表当作正式数据库。",
    ),
    "zh-tw": (
        "何時能組建全機械師機器人小隊？|機械師機器人會在流程較早階段解鎖；開放招募後，玩家可以組建全部由機器人構成的隊伍。|劇情任務仍會固定占用一個Hawks位置，因此純機器人編隊主要適用於自由任務。具體招募費用、解鎖節點及每種機體的最終定位仍需在正式版核驗。",
        "Bond跨職業訓練如何運作？|建立Bond的隊員能夠解鎖支援能力與跨職業訓練收益，從而共享新的技能與屬性。|Bond是戰術成長系統，不是戀愛系統。固定搭檔可能改變小隊構築，但官方尚未公布所有階段門檻、獎勵名稱與最終數值，頁面不會提前編造。",
        "自訂隊員可以設定姓名和背景故事嗎？|招募的自訂隊員可以擁有玩家設定的姓名與背景故事。|角色身分在招募時建立，不會像XCOM式隨機綽號池那樣等待後續自動授予。戰鬥成長、Bond關係與任務履歷是相互關聯但彼此獨立的系統。",
        "Hawks死亡後會發生什麼？|如果Hawks在戰鬥中死亡，任務會自動失敗，玩家必須重新開始該任務。|Hawks與普通隊員的死亡處理不同。劇情任務中應優先確保其掩體、治療與安全位置；這一確認並不代表官方已公布存檔數量或Ironman規則。",
        "劇情任務必須帶Hawks嗎？|是。所有劇情任務都要求Hawks進入出戰小隊。|標準四人小隊中會有一個固定位置，玩家可自由選擇的隊員數量因而減少。可選Operation可能允許更靈活的編隊，但官方回答沒有列出每個特殊例外。",
        "所有隊員都能穿完整曼達洛護甲嗎？|不能。完整曼達洛護甲是Cly的專屬裝備，不提供給自訂隊員。|此限制保留Cly獨特的視覺形象與劇情身分。其他隊員擁有外觀選項，並不能證明存在未公布的完整曼達洛職業或對應戰鬥屬性。",
        "戰場上有戰爭迷霧嗎？|沒有。Zero Company不採用經典戰爭迷霧，但遠距離不保證對所有目標都擁有有效視線。|狙擊隊員仍需判斷地形、掩體與射擊角度。全遠程隊伍可以成立卻不一定總是最優；未公布的命中率與射程數值不會寫成事實。",
        "能呼叫LAAT或其他特殊支援嗎？|不能。遊戲沒有供玩家主動使用的專用戰場支援呼叫。|治療、控制和輔助能力必須安排在出戰隊伍內部，不能預設有緊急撤離或外部轟炸兜底。任務中的劇情演出事件與可操作支援功能不是同一概念。",
        "過場動畫是即時渲染的嗎？|大部分遊戲內過場動畫採用即時渲染，只有少量次要片段屬於預渲染例外。|因此自訂Hawks與招募隊員能在許多劇情場景保持外觀一致。哪些片段屬於例外、不同平台是否有差異，需要在正式版本中複核。",
        "什麼是次級與高級Specialization？|EA確認裝備和玩法風格可以透過次級或高級Specialization進一步塑造。|這些路線把Build成長擴展到八種標準起始職業之外。完整名稱、技能樹與解鎖條件尚未公開，本站不會把推測列表當成正式資料庫。",
    ),
    "pt-br": (
        "Quando é possível montar uma equipe de astromecânicos?|Astromecânicos são liberados relativamente cedo e, após a abertura do recrutamento, é possível formar uma equipe completa de droides.|Hawks continua ocupando uma vaga obrigatória nas missões de história. Uma composição só de astromecânicos serve principalmente para missões livres; custos e funções exatas serão verificados no lançamento.",
        "Como funciona o treinamento cruzado dos Bonds?|Unidades ligadas por um Bond podem liberar habilidades de apoio e benefícios de treinamento cruzado que compartilham novas capacidades e atributos.|Bonds são progressão tática, não romance. Duplas recorrentes podem mudar a montagem do grupo, mas todos os limites e recompensas ainda não foram publicados.",
        "Operadores personalizados podem ter nome e história?|Operadores recrutados podem receber nomes e histórias de fundo personalizados.|A identidade é criada no recrutamento, em vez de surgir depois por uma lista aleatória de apelidos no estilo XCOM. Progresso de combate, Bonds e histórico de missões continuam sendo sistemas separados.",
        "O que acontece se Hawks morrer?|Se Hawks morrer em combate, a missão falha automaticamente e precisa ser reiniciada.|Hawks não é tratado exatamente como um Operador comum. Cobertura, cura e posição segura têm prioridade na história; a regra não confirma quantidade de salvamentos nem modo Ironman.",
        "Hawks precisa participar das missões de história?|Sim. Hawks deve fazer parte da equipe enviada para missões narrativas.|A vaga obrigatória reduz as escolhas livres de um esquadrão padrão de quatro. Operations opcionais podem ser mais flexíveis, mas a resposta oficial não lista todas as exceções.",
        "Qualquer Operador pode usar armadura mandaloriana?|Não. A armadura mandaloriana completa é exclusiva de Cly e não está disponível para Operadores personalizados.|A identidade visual e narrativa de Cly permanece única. Opções cosméticas de outros recrutas não comprovam uma classe mandaloriana completa nem bônus de combate associados.",
        "Existe névoa de guerra?|Não. Zero Company não usa a névoa de guerra clássica, mas longo alcance não garante linha de visão para todos os alvos.|Atiradores ainda precisam avaliar terreno, cobertura e ângulos. Uma equipe de longo alcance é permitida sem ser sempre ideal; valores de precisão não publicados não são presumidos.",
        "Existem chamadas de LAAT ou outros apoios especiais?|Não. Não existem chamadas de apoio especializadas no campo de batalha.|Cura, controle e suporte devem estar na equipe enviada, sem depender de extração emergencial ou ataque externo. Eventos roteirizados da missão são uma categoria diferente.",
        "As cenas são renderizadas em tempo real?|A maioria das cenas do jogo é renderizada em tempo real, com poucas exceções menores pré-renderizadas.|Hawks e recrutas personalizados podem aparecer de forma consistente em muitas sequências. As exceções e diferenças de plataforma precisam ser verificadas na versão final.",
        "O que são especializações secundárias e avançadas?|A EA afirma que equipamento e estilo podem evoluir por meio de Specializations secundárias ou avançadas.|Elas ampliam as builds além das oito funções padrão. Lista completa, árvores de habilidades e requisitos ainda não são públicos e não são apresentados como fatos.",
    ),
}

UI = {
    "de": ("Bestätigte Systeme", "Direkte Antwort", "Auswirkung im Spiel", "Planungscheck", "Beweisgrenze", "Verwandte Systeme", "Quelle"),
    "fr": ("Systèmes confirmés", "Réponse directe", "Effet en jeu", "Contrôle pratique", "Limite des preuves", "Systèmes liés", "Source"),
    "it": ("Sistemi confermati", "Risposta diretta", "Impatto sul gioco", "Controllo pratico", "Limite delle prove", "Sistemi correlati", "Fonte"),
    "es": ("Sistemas confirmados", "Respuesta directa", "Impacto en el juego", "Comprobación práctica", "Límite de pruebas", "Sistemas relacionados", "Fuente"),
    "ja": ("確認済みシステム", "直接回答", "ゲーム上の影響", "実用チェック", "根拠の範囲", "関連システム", "出典"),
    "ko": ("확인된 시스템", "직접 답변", "게임 영향", "실전 확인", "근거 범위", "관련 시스템", "출처"),
    "pl": ("Potwierdzone systemy", "Bezpośrednia odpowiedź", "Wpływ na grę", "Kontrola praktyczna", "Granica dowodów", "Powiązane systemy", "Źródło"),
    "zh-cn": ("已确认系统", "直接答案", "玩法影响", "实用核对", "证据边界", "相关系统", "来源"),
    "zh-tw": ("已確認系統", "直接答案", "玩法影響", "實用核對", "證據邊界", "相關系統", "來源"),
    "pt-br": ("Sistemas confirmados", "Resposta direta", "Impacto no jogo", "Verificação prática", "Limite das provas", "Sistemas relacionados", "Fonte"),
}

METHOD = {
    "de": "Die Seite trennt eine ausdrücklich bestätigte Regel von noch unbekannten Zahlen. Grundlage ist die EA-Community-Antwort vom 21. Juli 2026. Trailerbilder, Genrevergleiche und Spielerannahmen gelten nicht als Nachweis. Zum Release wird die Regel im Menü und in einer wiederholbaren Spielsituation geprüft; Plattform, Schwierigkeit und Version werden dokumentiert.",
    "fr": "Cette page sépare la règle explicitement confirmée des chiffres encore inconnus. La référence est la réponse communautaire d’EA du 21 juillet 2026. Une image de bande-annonce, une comparaison de genre ou une hypothèse de joueur ne vaut pas preuve. À la sortie, la règle sera reproduite en jeu avec plateforme, difficulté et version notées.",
    "it": "La pagina separa la regola confermata dai valori ancora sconosciuti. La fonte è la risposta alla community pubblicata da EA il 21 luglio 2026. Trailer, confronti con altri tattici e ipotesi dei giocatori non sono prove. Al lancio la regola sarà riprodotta nel gioco annotando piattaforma, difficoltà e versione.",
    "es": "La página separa la regla confirmada de los valores que siguen sin publicarse. La fuente es la respuesta de EA a la comunidad del 21 de julio de 2026. Tráilers, comparaciones con otros juegos tácticos y suposiciones no cuentan como prueba. En el lanzamiento se reproducirá la regla indicando plataforma, dificultad y versión.",
    "ja": "本ページは公式に確認されたルールと未公開の数値を分けます。根拠は2026年7月21日のEAコミュニティQ&Aです。予告映像、他作品との比較、プレイヤーの推測は証拠に含めません。発売後はメニューと再現可能なプレイ状況で確認し、機種、難易度、バージョンを記録します。",
    "ko": "이 페이지는 공식 확인된 규칙과 아직 공개되지 않은 수치를 구분합니다. 근거는 2026년 7월 21일 EA 커뮤니티 Q&A입니다. 트레일러 장면, 장르 비교, 이용자 추측은 증거가 아닙니다. 출시 후 메뉴와 반복 가능한 플레이 상황에서 확인하고 플랫폼, 난이도, 버전을 기록합니다.",
    "pl": "Strona oddziela potwierdzoną regułę od nieujawnionych wartości. Źródłem jest odpowiedź EA dla społeczności z 21 lipca 2026 roku. Zwiastuny, porównania gatunkowe i przypuszczenia graczy nie są dowodem. Po premierze zasada zostanie odtworzona w grze z zapisem platformy, poziomu trudności i wersji.",
    "zh-cn": "本页严格区分官方已确认规则与尚未公开的具体数值，依据为EA于2026年7月21日发布的社区问答。预告片画面、与其他战术游戏的类比和玩家推测都不作为事实证据。正式发售后，编辑会在菜单和可重复的实战场景中复核，并记录平台、难度、版本与测试条件。",
    "zh-tw": "本頁嚴格區分官方已確認規則與尚未公開的具體數值，依據為EA於2026年7月21日發布的社群問答。預告片畫面、與其他戰術遊戲的類比及玩家推測都不作為事實證據。正式發售後，編輯會在選單與可重複的實戰情境中複核，並記錄平台、難度、版本及測試條件。",
    "pt-br": "A página separa a regra confirmada dos valores ainda não publicados. A fonte é a resposta da EA à comunidade em 21 de julho de 2026. Trailer, comparação com outros jogos táticos e suposição de jogador não são provas. No lançamento, a regra será reproduzida com plataforma, dificuldade e versão registradas.",
}

STYLE = """:root{--bg:#071016;--panel:#0d1922;--panel2:#101f2a;--line:#284050;--text:#edf7ff;--muted:#9db0bd;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:radial-gradient(900px 520px at 80% -10%,rgba(54,224,206,.08),transparent),var(--bg);color:var(--text);font:16px/1.68 system-ui,-apple-system,'Segoe UI',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:rgba(7,16,22,.95);position:sticky;top:0;z-index:5}.top .wrap{min-height:62px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}.nav{margin-left:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}.nav>a{color:var(--muted);font-size:14px}.hero{padding:52px 0 30px;border-bottom:1px solid var(--line)}.crumb,.eyebrow{font-size:12px;text-transform:uppercase;letter-spacing:.15em;color:var(--teal)}h1{font-size:clamp(34px,6vw,58px);line-height:1.06;margin:14px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#c4d4dd;max-width:850px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(235px,1fr));gap:15px}.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:linear-gradient(180deg,var(--panel),var(--panel2));padding:20px;margin:15px 0;color:var(--text)}.answer{border-color:rgba(54,224,206,.5)}.note{border-color:rgba(233,184,74,.45)}.pill{display:inline-block;border:1px solid rgba(54,224,206,.45);border-radius:4px;padding:5px 9px;color:var(--teal);font-size:12px}.muted,.source{color:var(--muted);font-size:14px}.source{border-top:1px solid var(--line);padding-top:14px}li{margin:8px 0}table{width:100%;border-collapse:collapse}th,td{border:1px solid var(--line);padding:11px;text-align:left;vertical-align:top}th{color:var(--gold);width:28%}.lang-menu{position:relative;display:inline-block;margin-left:4px;z-index:40;font:600 14px/1.2 system-ui,-apple-system,'Segoe UI',sans-serif;color:#edf7ff}.lang-menu summary{list-style:none;cursor:pointer;border:1px solid #365264;border-radius:7px;padding:8px 28px 8px 11px;background:#0d1922;color:#edf7ff;white-space:nowrap;position:relative}.lang-menu summary::-webkit-details-marker{display:none}.lang-menu summary::after{content:'▾';position:absolute;right:10px;color:#36e0ce}.lang-menu[open] summary::after{content:'▴'}.lang-options{position:absolute;right:0;top:calc(100% + 7px);min-width:154px;padding:6px;background:#0b161e;border:1px solid #365264;border-radius:8px;box-shadow:0 12px 30px rgba(0,0,0,.38)}.lang-options a{display:block!important;padding:9px 10px!important;margin:0!important;border-radius:5px;color:#c8d8e1!important;text-decoration:none!important;white-space:nowrap;font-size:14px!important}.lang-options a:hover,.lang-options a[aria-current=page]{background:#132631;color:#36e0ce!important}.lang-options a[aria-current=page]::before{content:'✓ ';color:#e9b84a}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){.two{grid-template-columns:1fr}.nav{margin-left:0}.top .wrap{padding-top:12px;padding-bottom:12px}.lang-menu{width:100%;margin:4px 0}.lang-menu summary{width:100%}.lang-options{position:static;margin-top:6px;width:100%}}"""


def parsed(locale: str):
    return [tuple(row.split("|")) for row in RAW[locale]]


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


def page(locale: str, lang: str, index: int, item: tuple[str, str, str]) -> str:
    title, direct, impact = item
    slug = SLUGS[index]
    labels = UI[locale]
    canonical = SITE + route(locale, slug)
    items = parsed(locale)
    related_ids = ((index + 1) % 10, (index + 4) % 10, (index + 7) % 10)
    related = "".join(
        f'<a class="card" href="{route(locale, SLUGS[n])}"><strong>{escape(items[n][0])}</strong>'
        f'<br><span class="muted">{escape(items[n][1])}</span></a>' for n in related_ids
    )
    faq_slugs = (
        "can-you-disable-permadeath",
        "is-zero-company-single-player",
        "how-many-action-points-per-turn",
    )
    faq = "".join(
        f'<a class="card" href="/{locale}/questions/{slug}.html"><strong>FAQ</strong>'
        f'<br><span class="muted">{escape(items[(index + offset + 2) % 10][1])}</span></a>'
        for offset, slug in enumerate(faq_slugs)
    )
    schema = {
        "@context": "https://schema.org", "@type": "Article", "inLanguage": lang,
        "headline": title, "description": direct, "url": canonical,
        "dateModified": TODAY, "about": "Star Wars Zero Company gameplay systems",
        "isPartOf": {"@type": "WebSite", "name": "Star Wars Zero Company Wiki", "url": SITE + "/"},
    }
    checks = [direct, impact, METHOD[locale]]
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape((direct + ' ' + impact)[:300])}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates(slug)}<meta property="og:type" content="article"><meta property="og:url" content="{canonical}"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(direct)}"><meta property="og:image" content="{SITE}/assets/zero-company-hero.png"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav class="nav"><a href="/{locale}/questions/">FAQ</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a><a href="/{locale}/mechanics/">Systems</a>{menu(locale, slug)}</nav></div></header><main class="wrap"><section class="hero"><div class="crumb"><a href="/{locale}/mechanics/">{escape(labels[0])}</a> / {escape(labels[1])}</div><p class="eyebrow">{escape(labels[0])} · {TODAY}</p><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section><section class="block answer"><h2>{escape(labels[1])}</h2><p><strong>{escape(direct)}</strong></p></section><div class="two"><section class="block"><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p></section><section class="block"><h2>{escape(labels[3])}</h2><ul><li>{escape(checks[index % 3])}</li><li>{escape(checks[(index + 1) % 3])}</li><li>{escape(checks[(index + 2) % 3])}</li></ul></section></div><section class="block note"><h2>{escape(labels[4])}</h2><p>{escape(METHOD[locale])}</p><p>{escape(impact)}</p></section><section><h2>{escape(labels[5])}</h2><div class="grid">{related}</div></section><section><h2>FAQ</h2><div class="grid">{faq}</div></section><section class="block"><h2>{escape(labels[6])}</h2><p><a href="{SOURCE}" rel="nofollow">EA community Q&amp;A — July 21, 2026</a></p><p class="source">{escape(METHOD[locale])}</p></section></main><footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">{escape(labels[6])}</a> · <a href="/sitemap.xml">Sitemap</a></div></footer></body></html>'''


def add_english_alternates(path: Path, slug: str) -> None:
    html = path.read_text(encoding="utf-8-sig", errors="ignore")
    html = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*>', "", html, flags=re.I)
    canonical = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', html, re.I)
    if not canonical:
        raise ValueError(f"English source has no canonical: {path}")
    html = html[:canonical.end()] + alternates(slug) + html[canonical.end():]
    path.write_text(html, encoding="utf-8")


def update_hub(locale: str) -> None:
    path = ROOT / locale / "mechanics" / "index.html"
    html = path.read_text(encoding="utf-8-sig", errors="ignore")
    html = re.sub(
        r'<!-- ROUND16-SYSTEMS-START -->.*?<!-- ROUND16-SYSTEMS-END -->',
        "",
        html,
        flags=re.S,
    )
    items = parsed(locale)
    cards = "".join(
        f'<a class="card" href="{route(locale, slug)}"><strong>{escape(item[0])}</strong>'
        f'<br><span class="muted">{escape(item[1])}</span></a>'
        for slug, item in zip(SLUGS, items)
    )
    section = (
        '<!-- ROUND16-SYSTEMS-START --><section><h2>'
        + escape(UI[locale][0])
        + f'</h2><div class="grid">{cards}</div></section><!-- ROUND16-SYSTEMS-END -->'
    )
    if "</main>" not in html:
        raise ValueError(f"Localized mechanics hub has no main close: {path}")
    html = html.replace("</main>", section + "</main>", 1)
    path.write_text(html, encoding="utf-8")


def main() -> None:
    created = 0
    for locale, lang, _ in LOCALES:
        if locale == "en":
            for slug in SLUGS:
                add_english_alternates(ROOT / "mechanics" / f"{slug}.html", slug)
            continue
        out = ROOT / locale / "mechanics"
        out.mkdir(parents=True, exist_ok=True)
        for index, item in enumerate(parsed(locale)):
            (out / f"{SLUGS[index]}.html").write_text(page(locale, lang, index, item), encoding="utf-8")
            created += 1
        update_hub(locale)
    print(f"Round 16 created {created} localized system pages")


if __name__ == "__main__":
    main()
