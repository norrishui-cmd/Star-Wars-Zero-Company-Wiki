#!/usr/bin/env python3
"""Round 22: add cast and specialization parity to eight under-covered locales."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = date.today().isoformat()
CAST_SOURCE = "https://www.starwars.com/news/sdcc-star-wars-zero-company-cast-announce"
GAMEPLAY_SOURCE = "https://www.ea.com/games/starwars/zero-company/news/lead-zero-company-to-victory"

LOCALES = {
    "es": ("es", "Español"),
    "fr": ("fr", "Français"),
    "it": ("it", "Italiano"),
    "ko": ("ko", "한국어"),
    "pl": ("pl", "Polski"),
    "pt-br": ("pt-BR", "Português (Brasil)"),
    "zh-cn": ("zh-Hans", "简体中文"),
    "zh-tw": ("zh-Hant", "繁體中文"),
}
ALL = (
    ("en", "en", "English"), ("de", "de", "Deutsch"),
    ("fr", "fr", "Français"), ("it", "it", "Italiano"),
    ("es", "es", "Español"), ("ja", "ja", "日本語"),
    ("ko", "ko", "한국어"), ("pl", "pl", "Polski"),
    ("zh-cn", "zh-Hans", "简体中文"),
    ("zh-tw", "zh-Hant", "繁體中文"),
    ("pt-br", "pt-BR", "Português (Brasil)"),
)

CLASSES = {
    "assault": "Assault", "gunslinger": "Gunslinger", "heavy": "Heavy",
    "medic": "Medic", "scoundrel": "Scoundrel", "scout": "Scout",
    "sharpshooter": "Sharpshooter", "soldier": "Soldier",
}
CAST = {
    "anakin-skywalker-matt-lanter": ("Anakin Skywalker", "Matt Lanter"),
    "cly-kullervo-alex-mckenna": ("Cly Kullervo", "Alex McKenna"),
    "kundri-fathom-rekha-sharma": ("Kundri Fathom", "Rekha Sharma"),
    "trick-dee-bradley-baker": ("Trick and Clone Troopers", "Dee Bradley Baker"),
}

COPY = {
    "es": {
        "nav": ("Inicio", "Reparto", "Especializaciones", "FAQ", "Noticias"),
        "cast": ("Reparto oficial", "Respuesta directa", "Contexto del personaje",
                 "Qué confirma la fuente", "Límite de la evidencia", "Fuente oficial"),
        "class": ("Especialización confirmada", "Función táctica", "Cómo interpretar la función",
                  "Estructura de habilidades", "Qué falta por verificar", "Fuente oficial"),
        "cast_intro": "{actor} interpreta oficialmente a {character} en Star Wars Zero Company.",
        "cast_body": "El anuncio oficial del reparto confirma la relación entre personaje e intérprete. Esta página responde a la búsqueda de voz y producción sin convertir ese crédito en estadísticas, habilidades o apariciones de misión no publicadas.",
        "class_intro": "{name} es una de las ocho especializaciones estándar confirmadas para la mayoría de los Operadores.",
        "class_body": "Cada especialización estándar tiene una habilidad Ultimate, una Standard y una Passive propias. El perfil explica la función publicada por EA, pero no inventa valores, costes, enfriamientos ni un orden de mejoras antes de probar la versión final.",
        "boundary": "Los detalles de desarrollo pueden cambiar. Solo se indexan afirmaciones respaldadas por EA o StarWars.com; las cifras y excepciones no anunciadas quedan fuera.",
        "hub_cast": ("Reparto de Star Wars Zero Company", "Créditos oficiales de personajes e intérpretes confirmados por StarWars.com."),
        "hub_class": ("Especializaciones de Zero Company", "Las ocho funciones estándar confirmadas y su propósito táctico."),
        "class_desc": {
            "assault": "Combatiente de primera línea que maniobra para eliminar objetivos a corta y media distancia, especialmente enemigos tras cobertura.",
            "gunslinger": "Especialista en ataques rápidos con bláster y acciones contra varios objetivos.",
            "heavy": "Combatiente blindado de primera línea centrado en supervivencia y en absorber ataques a campo abierto.",
            "medic": "Especialista en curación, prevención de heridas y apoyo físico y psicológico al equipo.",
            "scoundrel": "Comodín capaz de aprovechar oportunidades de combate con poca preparación previa.",
            "scout": "Operador de reconocimiento cuya planificación y sincronización crean oportunidades para toda la escuadra.",
            "sharpshooter": "Tirador experto en enfrentamientos de largo alcance y en eliminar objetivos prioritarios.",
            "soldier": "Unidad ofensiva versátil para corto y medio alcance con cuerpo a cuerpo, granadas, fuego pesado y lanzacohetes.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "Anakin aparece como General Jedi en una misión crucial cuyo camino se cruza brevemente con Zero Company.",
            "cly-kullervo-alex-mckenna": "Cly es una guerrera mandaloriana del antiguo Clan Verminoth que se une al grupo por su búsqueda de venganza.",
            "kundri-fathom-rekha-sharma": "Kundri Fathom es la líder de Infinite Coil, un culto aliado con los Separatistas y la amenaza central que persigue el equipo.",
            "trick-dee-bradley-baker": "Trick, antes CT-3301, es un clon veterano y antiguo compañero militar de Hawks; el crédito también cubre a los Clone Troopers.",
        },
    },
    "fr": {
        "nav": ("Accueil", "Casting", "Spécialisations", "FAQ", "Actualités"),
        "cast": ("Casting officiel", "Réponse directe", "Contexte du personnage",
                 "Ce que confirme la source", "Limite des preuves", "Source officielle"),
        "class": ("Spécialisation confirmée", "Rôle tactique", "Comment lire ce rôle",
                  "Structure des capacités", "À vérifier au lancement", "Source officielle"),
        "cast_intro": "{actor} interprète officiellement {character} dans Star Wars Zero Company.",
        "cast_body": "L’annonce officielle établit le lien entre le personnage et son interprète. Cette page répond à une recherche de casting sans transformer ce crédit en statistiques, compétences ou apparitions de mission non publiées.",
        "class_intro": "{name} fait partie des huit spécialisations standard confirmées pour la plupart des Operators.",
        "class_body": "Chaque spécialisation standard possède une capacité Ultimate, une Standard et une Passive qui lui sont propres. Ce profil reprend le rôle publié par EA sans inventer valeurs, coûts, délais ni ordre d’amélioration avant le test de la version finale.",
        "boundary": "Les éléments en développement peuvent changer. Seules les affirmations soutenues par EA ou StarWars.com sont indexées; les chiffres et exceptions non annoncés sont exclus.",
        "hub_cast": ("Casting de Star Wars Zero Company", "Crédits officiels des personnages et interprètes confirmés par StarWars.com."),
        "hub_class": ("Spécialisations de Zero Company", "Les huit rôles standard confirmés et leur fonction tactique."),
        "class_desc": {
            "assault": "Combattant de première ligne mobile, efficace à courte et moyenne portée contre les cibles à couvert.",
            "gunslinger": "Spécialiste des attaques rapides au blaster et des frappes visant plusieurs ennemis.",
            "heavy": "Combattant lourdement protégé, axé sur la survie et l’absorption des attaques à découvert.",
            "medic": "Spécialiste des soins, de la prévention des blessures et du soutien physique ou psychologique.",
            "scoundrel": "Joker capable d’exploiter les occasions de combat avec peu de préparation.",
            "scout": "Opérateur de reconnaissance dont la préparation et le timing créent des ouvertures pour l’équipe.",
            "sharpshooter": "Tireur d’élite spécialisé dans la longue portée et l’élimination d’une cible prioritaire.",
            "soldier": "Unité offensive polyvalente à courte et moyenne portée, avec mêlée, grenades, tir lourd et roquette.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "Anakin apparaît comme général Jedi lors d’une mission cruciale où sa route croise brièvement celle de Zero Company.",
            "cly-kullervo-alex-mckenna": "Cly est une guerrière mandalorienne de l’ancien clan Verminoth qui rejoint le groupe pour poursuivre sa vengeance.",
            "kundri-fathom-rekha-sharma": "Kundri Fathom dirige l’Infinite Coil, un culte allié aux Séparatistes et la menace centrale traquée par l’équipe.",
            "trick-dee-bradley-baker": "Trick, autrefois CT-3301, est un clone vétéran et ancien compagnon d’armes de Hawks; le crédit couvre aussi les Clone Troopers.",
        },
    },
    "it": {
        "nav": ("Home", "Cast", "Specializzazioni", "FAQ", "Notizie"),
        "cast": ("Cast ufficiale", "Risposta diretta", "Contesto del personaggio",
                 "Cosa conferma la fonte", "Limite delle prove", "Fonte ufficiale"),
        "class": ("Specializzazione confermata", "Ruolo tattico", "Come leggere il ruolo",
                  "Struttura delle abilità", "Da verificare al lancio", "Fonte ufficiale"),
        "cast_intro": "{actor} interpreta ufficialmente {character} in Star Wars Zero Company.",
        "cast_body": "L’annuncio ufficiale collega il personaggio al suo interprete. Questa pagina risponde alla ricerca sul cast senza trasformare il credito in statistiche, abilità o presenze nelle missioni non ancora pubblicate.",
        "class_intro": "{name} è una delle otto specializzazioni standard confermate per la maggior parte degli Operatori.",
        "class_body": "Ogni specializzazione standard include un’abilità Ultimate, una Standard e una Passive uniche. Il profilo riporta il ruolo pubblicato da EA senza inventare valori, costi, tempi o ordini di potenziamento prima della verifica sulla versione finale.",
        "boundary": "I dettagli in sviluppo possono cambiare. Sono indicizzate solo affermazioni supportate da EA o StarWars.com; numeri ed eccezioni non annunciati restano esclusi.",
        "hub_cast": ("Cast di Star Wars Zero Company", "Crediti ufficiali di personaggi e interpreti confermati da StarWars.com."),
        "hub_class": ("Specializzazioni di Zero Company", "Gli otto ruoli standard confermati e il loro scopo tattico."),
        "class_desc": {
            "assault": "Combattente mobile di prima linea, efficace a corto e medio raggio contro bersagli dietro copertura.",
            "gunslinger": "Specialista in rapidi attacchi blaster e colpi distribuiti su più bersagli.",
            "heavy": "Combattente corazzato di prima linea, orientato alla sopravvivenza e ad assorbire gli attacchi allo scoperto.",
            "medic": "Specialista nella cura, nella prevenzione delle ferite e nel supporto fisico e psicologico.",
            "scoundrel": "Jolly capace di sfruttare opportunità di combattimento con poca preparazione.",
            "scout": "Operatore da ricognizione la cui pianificazione e tempistica creano occasioni per la squadra.",
            "sharpshooter": "Tiratore esperto negli scontri a lungo raggio e nell’eliminazione di bersagli prioritari.",
            "soldier": "Unità offensiva versatile a corto e medio raggio con mischia, granate, fuoco pesante e lanciarazzi.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "Anakin appare come Generale Jedi in una missione cruciale e il suo cammino incrocia brevemente quello di Zero Company.",
            "cly-kullervo-alex-mckenna": "Cly è una guerriera mandaloriana dell’antico Clan Verminoth che si unisce al gruppo per perseguire la vendetta.",
            "kundri-fathom-rekha-sharma": "Kundri Fathom guida l’Infinite Coil, un culto alleato dei Separatisti e la minaccia centrale inseguita dalla squadra.",
            "trick-dee-bradley-baker": "Trick, un tempo CT-3301, è un clone veterano e vecchio compagno militare di Hawks; il credito include anche i Clone Troopers.",
        },
    },
    "ko": {
        "nav": ("홈", "성우진", "전문화", "FAQ", "뉴스"),
        "cast": ("공식 성우진", "직접 답변", "캐릭터 배경", "공식 출처가 확인한 내용", "근거 범위", "공식 출처"),
        "class": ("확인된 전문화", "전술 역할", "역할 해석", "능력 구성", "출시 후 확인 사항", "공식 출처"),
        "cast_intro": "{actor}은(는) Star Wars Zero Company에서 {character} 역으로 공식 발표되었습니다.",
        "cast_body": "공식 성우 발표는 캐릭터와 연기자의 연결을 확인합니다. 이 페이지는 성우 검색 의도에 답하며, 공개되지 않은 능력치·스킬·임무 등장 정보를 성우 크레딧에서 추정하지 않습니다.",
        "class_intro": "{name}은(는) 대부분의 오퍼레이터가 선택할 수 있는 8개 표준 전문화 중 하나입니다.",
        "class_body": "각 표준 전문화에는 고유한 Ultimate, Standard, Passive 능력이 하나씩 있습니다. 이 문서는 EA가 공개한 역할만 설명하며 정식 버전을 확인하기 전 수치, 비용, 재사용 시간, 성장 순서를 만들지 않습니다.",
        "boundary": "개발 중인 세부 내용은 바뀔 수 있습니다. EA 또는 StarWars.com이 뒷받침한 정보만 색인하며 발표되지 않은 수치와 예외는 제외합니다.",
        "hub_cast": ("Star Wars Zero Company 성우진", "StarWars.com이 확인한 캐릭터와 연기자 공식 크레딧입니다."),
        "hub_class": ("Zero Company 전문화", "공식 확인된 8개 표준 역할과 전술 목적입니다."),
        "class_desc": {
            "assault": "엄폐한 적을 상대로 근·중거리 처치에 강한 기동형 최전선 전투원입니다.",
            "gunslinger": "빠른 블래스터 공격과 다수 표적 공격에 특화된 역할입니다.",
            "heavy": "높은 생존력으로 노출된 위치에서 적의 공격을 받아내는 중장갑 전방 전투원입니다.",
            "medic": "치유와 부상 예방, 신체적·심리적 팀 지원에 특화됩니다.",
            "scoundrel": "많은 준비 없이도 전투 기회를 포착해 활용하는 변수형 역할입니다.",
            "scout": "정찰, 계획, 타이밍으로 분대 전체에 새로운 기회를 만드는 역할입니다.",
            "sharpshooter": "장거리 교전과 지정한 우선 표적 제거에 집중하는 명사수입니다.",
            "soldier": "근·중거리에서 근접전, 수류탄, 중화기와 로켓 발사기를 다루는 공격형 역할입니다.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "아나킨은 중요한 임무에서 제다이 장군으로 등장하며 Zero Company와 잠시 협력합니다.",
            "cly-kullervo-alex-mckenna": "클라이는 고대 베르미노스 클랜의 만달로리안 전사로, 복수를 위해 부대에 합류합니다.",
            "kundri-fathom-rekha-sharma": "쿤드리 패덤은 분리주의자와 손잡은 컬트 Infinite Coil의 지도자이자 부대가 추적하는 핵심 위협입니다.",
            "trick-dee-bradley-baker": "트릭은 CT-3301로 알려졌던 베테랑 클론이자 호크스의 옛 전우이며, 크레딧은 Clone Troopers도 포함합니다.",
        },
    },
    "pl": {
        "nav": ("Start", "Obsada", "Specjalizacje", "FAQ", "Aktualności"),
        "cast": ("Oficjalna obsada", "Krótka odpowiedź", "Kontekst postaci",
                 "Co potwierdza źródło", "Granica dowodów", "Oficjalne źródło"),
        "class": ("Potwierdzona specjalizacja", "Rola taktyczna", "Jak rozumieć rolę",
                  "Struktura zdolności", "Do sprawdzenia po premierze", "Oficjalne źródło"),
        "cast_intro": "{actor} oficjalnie użycza głosu postaci {character} w Star Wars Zero Company.",
        "cast_body": "Oficjalne ogłoszenie łączy postać z wykonawcą. Strona odpowiada na pytanie o obsadę, ale nie zamienia kredytu aktorskiego w nieopublikowane statystyki, umiejętności ani występy w misjach.",
        "class_intro": "{name} to jedna z ośmiu standardowych specjalizacji potwierdzonych dla większości Operatorów.",
        "class_body": "Każda standardowa specjalizacja ma własną zdolność Ultimate, Standard oraz Passive. Profil opisuje rolę podaną przez EA, lecz przed testem wersji finalnej nie wymyśla wartości, kosztów, czasów odnowienia ani kolejności rozwoju.",
        "boundary": "Szczegóły wersji rozwojowej mogą się zmienić. Indeksowane są wyłącznie twierdzenia poparte przez EA lub StarWars.com; nieogłoszone liczby i wyjątki są pomijane.",
        "hub_cast": ("Obsada Star Wars Zero Company", "Oficjalne kredyty postaci i wykonawców potwierdzone przez StarWars.com."),
        "hub_class": ("Specjalizacje Zero Company", "Osiem potwierdzonych standardowych ról i ich zastosowanie taktyczne."),
        "class_desc": {
            "assault": "Mobilny wojownik pierwszej linii skuteczny na krótkim i średnim dystansie przeciw celom za osłoną.",
            "gunslinger": "Specjalista od szybkich ataków blasterem i uderzeń rozłożonych na wiele celów.",
            "heavy": "Ciężko opancerzony wojownik pierwszej linii nastawiony na przetrwanie i przyjmowanie ataków na otwartej pozycji.",
            "medic": "Specjalista od leczenia, zapobiegania obrażeniom oraz fizycznego i psychologicznego wsparcia.",
            "scoundrel": "Nieprzewidywalny Operator wykorzystujący okazje bojowe bez długiego przygotowania.",
            "scout": "Operator zwiadowczy, którego planowanie i wyczucie czasu tworzą możliwości dla całego zespołu.",
            "sharpshooter": "Strzelec wyborowy skupiony na dalekim dystansie i eliminowaniu priorytetowego celu.",
            "soldier": "Wszechstronna jednostka ofensywna na krótki i średni dystans z walką wręcz, granatami, ciężkim ogniem i rakietą.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "Anakin występuje jako generał Jedi podczas ważnej misji, w której jego droga na krótko krzyżuje się z Zero Company.",
            "cly-kullervo-alex-mckenna": "Cly to mandaloriańska wojowniczka starożytnego klanu Verminoth, która dołącza do grupy, realizując swoją zemstę.",
            "kundri-fathom-rekha-sharma": "Kundri Fathom przewodzi Infinite Coil, kultowi sprzymierzonemu z Separatystami i głównemu zagrożeniu ściganemu przez zespół.",
            "trick-dee-bradley-baker": "Trick, dawniej CT-3301, jest doświadczonym klonem i dawnym towarzyszem Hawksa; kredyt obejmuje też Clone Troopers.",
        },
    },
    "pt-br": {
        "nav": ("Início", "Elenco", "Especializações", "FAQ", "Notícias"),
        "cast": ("Elenco oficial", "Resposta direta", "Contexto do personagem",
                 "O que a fonte confirma", "Limite das evidências", "Fonte oficial"),
        "class": ("Especialização confirmada", "Função tática", "Como interpretar a função",
                  "Estrutura de habilidades", "O que verificar no lançamento", "Fonte oficial"),
        "cast_intro": "{actor} interpreta oficialmente {character} em Star Wars Zero Company.",
        "cast_body": "O anúncio oficial liga personagem e intérprete. Esta página responde à busca sobre elenco sem transformar o crédito em atributos, habilidades ou aparições em missões que ainda não foram publicados.",
        "class_intro": "{name} é uma das oito especializações padrão confirmadas para a maioria dos Operadores.",
        "class_body": "Cada especialização padrão possui habilidades próprias Ultimate, Standard e Passive. O perfil explica a função publicada pela EA, sem inventar valores, custos, recargas ou ordem de melhorias antes de testar a versão final.",
        "boundary": "Detalhes em desenvolvimento podem mudar. Somente afirmações apoiadas pela EA ou StarWars.com são indexadas; números e exceções não anunciados ficam de fora.",
        "hub_cast": ("Elenco de Star Wars Zero Company", "Créditos oficiais de personagens e intérpretes confirmados pela StarWars.com."),
        "hub_class": ("Especializações de Zero Company", "As oito funções padrão confirmadas e seu propósito tático."),
        "class_desc": {
            "assault": "Combatente móvel de linha de frente, forte a curta e média distância contra alvos em cobertura.",
            "gunslinger": "Especialista em ataques rápidos de blaster e ações contra vários alvos.",
            "heavy": "Combatente blindado de linha de frente focado em sobrevivência e em absorver ataques exposto.",
            "medic": "Especialista em cura, prevenção de ferimentos e apoio físico ou psicológico à equipe.",
            "scoundrel": "Curinga capaz de aproveitar oportunidades de combate com pouca preparação.",
            "scout": "Operador de reconhecimento cujo planejamento e timing criam oportunidades para a equipe.",
            "sharpshooter": "Atirador especializado em longa distância e na eliminação de um alvo prioritário.",
            "soldier": "Unidade ofensiva versátil de curta e média distância com corpo a corpo, granadas, fogo pesado e lança-foguetes.",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "Anakin aparece como General Jedi em uma missão crucial e cruza brevemente o caminho da Zero Company.",
            "cly-kullervo-alex-mckenna": "Cly é uma guerreira Mandaloriana do antigo Clã Verminoth que se junta ao grupo em busca de vingança.",
            "kundri-fathom-rekha-sharma": "Kundri Fathom lidera a Infinite Coil, culto alinhado aos Separatistas e ameaça central perseguida pela equipe.",
            "trick-dee-bradley-baker": "Trick, antes CT-3301, é um clone veterano e antigo companheiro militar de Hawks; o crédito também cobre os Clone Troopers.",
        },
    },
    "zh-cn": {
        "nav": ("首页", "配音阵容", "专精", "FAQ", "新闻"),
        "cast": ("官方配音阵容", "直接答案", "角色背景", "官方来源确认了什么", "证据边界", "官方来源"),
        "class": ("已确认专精", "战术定位", "如何理解该定位", "能力结构", "发售后核验", "官方来源"),
        "cast_intro": "{actor}已被官方确认为Star Wars Zero Company中{character}的配音演员。",
        "cast_body": "官方演员公告确认了角色与演员的对应关系。本页只回答配音与制作人员搜索意图，不会把演员名单推导成尚未公开的数值、技能或任务出场信息。",
        "class_intro": "{name}是大多数干员可选的八种标准专精之一。",
        "class_body": "每种标准专精均拥有独立的Ultimate、Standard和Passive能力。本页只解释EA公布的战术定位，在正式版实测前不会编造数值、消耗、冷却时间或升级顺序。",
        "boundary": "开发阶段的细节可能变化。仅收录EA或StarWars.com支持的事实；未公布的数值和例外情况不会进入索引内容。",
        "hub_cast": ("Star Wars Zero Company配音阵容", "由StarWars.com确认的角色与演员官方对应资料。"),
        "hub_class": ("Zero Company专精", "八种已确认标准定位及其战术用途。"),
        "class_desc": {
            "assault": "机动型前线战士，擅长在中近距离消灭躲在掩体后的目标。",
            "gunslinger": "擅长快速爆能枪攻击，并可把输出分散到多个目标。",
            "heavy": "重甲前线战士，强调生存能力并能在开阔位置承受敌方攻击。",
            "medic": "专注治疗、预防伤势，并为队友提供身体与心理支持。",
            "scoundrel": "能够在准备有限的情况下抓住战斗机会的多变角色。",
            "scout": "依靠侦察、规划与时机为全队创造机会的战术干员。",
            "sharpshooter": "擅长远距离交战并集中消灭优先目标的神射手。",
            "soldier": "中近距离通用进攻单位，可使用近战、手雷、重型火力与火箭发射器。",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "安纳金以绝地将军身份出现在一项关键任务中，并与Zero Company短暂交会。",
            "cly-kullervo-alex-mckenna": "Cly是古老Verminoth氏族的曼达洛战士，为追求复仇而加入队伍。",
            "kundri-fathom-rekha-sharma": "Kundri Fathom是亲分离主义邪教Infinite Coil的领袖，也是小队追捕的核心威胁。",
            "trick-dee-bradley-baker": "Trick原名CT-3301，是经验丰富的克隆人士兵和Hawks的旧战友；该演员条目也覆盖Clone Troopers。",
        },
    },
    "zh-tw": {
        "nav": ("首頁", "配音陣容", "專精", "FAQ", "新聞"),
        "cast": ("官方配音陣容", "直接答案", "角色背景", "官方來源確認了什麼", "證據邊界", "官方來源"),
        "class": ("已確認專精", "戰術定位", "如何理解該定位", "能力結構", "發售後核驗", "官方來源"),
        "cast_intro": "{actor}已獲官方確認為Star Wars Zero Company中{character}的配音演員。",
        "cast_body": "官方演員公告確認了角色與演員的對應關係。本頁只回答配音與製作人員搜尋意圖，不會把演員名單推導成尚未公開的數值、技能或任務登場資訊。",
        "class_intro": "{name}是大多數幹員可選的八種標準專精之一。",
        "class_body": "每種標準專精均擁有獨立的Ultimate、Standard及Passive能力。本頁只解釋EA公布的戰術定位，在正式版實測前不會編造數值、消耗、冷卻時間或升級順序。",
        "boundary": "開發階段的細節可能變更。僅收錄EA或StarWars.com支持的事實；未公布的數值與例外情況不會進入索引內容。",
        "hub_cast": ("Star Wars Zero Company配音陣容", "由StarWars.com確認的角色與演員官方對應資料。"),
        "hub_class": ("Zero Company專精", "八種已確認標準定位及其戰術用途。"),
        "class_desc": {
            "assault": "機動型前線戰士，擅長在中近距離消滅躲在掩體後方的目標。",
            "gunslinger": "擅長快速爆能槍攻擊，並可把輸出分散至多個目標。",
            "heavy": "重甲前線戰士，強調生存能力並能在開闊位置承受敵方攻擊。",
            "medic": "專注治療、預防傷勢，並為隊友提供身體與心理支援。",
            "scoundrel": "能夠在準備有限時抓住戰鬥機會的多變角色。",
            "scout": "依靠偵察、規劃與時機為全隊創造機會的戰術幹員。",
            "sharpshooter": "擅長遠距離交戰並集中消滅優先目標的神射手。",
            "soldier": "中近距離通用進攻單位，可使用近戰、手榴彈、重型火力及火箭發射器。",
        },
        "cast_desc": {
            "anakin-skywalker-matt-lanter": "安納金以絕地將軍身分出現在一項關鍵任務中，並與Zero Company短暫交會。",
            "cly-kullervo-alex-mckenna": "Cly是古老Verminoth氏族的曼達洛戰士，為追求復仇而加入隊伍。",
            "kundri-fathom-rekha-sharma": "Kundri Fathom是親分離主義邪教Infinite Coil的領袖，也是小隊追捕的核心威脅。",
            "trick-dee-bradley-baker": "Trick原名CT-3301，是經驗豐富的複製人士兵及Hawks的舊戰友；該演員條目也涵蓋Clone Troopers。",
        },
    },
}

STYLE_CAST = re.search(r"<style>(.*?)</style>", (ROOT / "cast" / "trick-dee-bradley-baker.html").read_text(), re.S).group(1)
STYLE_CLASS = re.search(r"<style>(.*?)</style>", (ROOT / "classes" / "assault.html").read_text(), re.S).group(1)


def localized_path(locale, family, slug=None):
    suffix = f"{family}/{slug}.html" if slug else f"{family}/"
    return f"/{locale}/{suffix}"


def alternates(family, slug=None):
    suffix = f"{family}/{slug}.html" if slug else f"{family}/"
    rows = []
    for locale, lang, _ in ALL:
        path = f"/{suffix}" if locale == "en" else f"/{locale}/{suffix}"
        rows.append(f'<link rel="alternate" hreflang="{lang}" href="{SITE}{path}">')
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/{suffix}">')
    return "".join(rows)


def language_menu(locale, family, slug=None):
    suffix = f"{family}/{slug}.html" if slug else f"{family}/"
    links = []
    for code, lang, label in ALL:
        path = f"/{suffix}" if code == "en" else f"/{code}/{suffix}"
        current = ' aria-current="page"' if code == locale else ""
        links.append(f'<a href="{path}" lang="{lang}"{current}>{escape(label)}</a>')
    return ('<details class="lang-menu"><summary aria-label="Choose language">'
            f'{escape(LOCALES[locale][1])}</summary><div class="lang-options">'
            + "".join(links) + "</div></details>")


def header(locale):
    nav = COPY[locale]["nav"]
    return (f'<header class="top"><div class="wrap"><a class="brand" href="/{locale}/">'
            f'Star Wars Zero Company Wiki</a><nav class="nav">'
            f'<a href="/{locale}/">{nav[0]}</a><a href="/{locale}/cast/">{nav[1]}</a>'
            f'<a href="/{locale}/classes/">{nav[2]}</a><a href="/{locale}/questions/">{nav[3]}</a>'
            f'<a href="/news/">{nav[4]}</a>{{menu}}</nav></div></header>')


def shell(locale, family, slug, title, desc, body, schema_type="Article"):
    canonical = SITE + localized_path(locale, family, slug)
    schema = {
        "@context": "https://schema.org", "@type": schema_type,
        "headline": title, "description": desc, "url": canonical,
        "inLanguage": LOCALES[locale][0], "dateModified": TODAY,
        "isPartOf": {"@type": "WebSite", "name": "Star Wars Zero Company Wiki", "url": SITE + "/"},
    }
    menu = language_menu(locale, family, slug)
    style = STYLE_CAST if family == "cast" else STYLE_CLASS
    return (f'<!doctype html><html lang="{LOCALES[locale][0]}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | {escape(LOCALES[locale][1])} Zero Company Wiki</title>'
            f'<meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow">'
            f'<link rel="canonical" href="{canonical}">{alternates(family, slug)}<link rel="icon" href="/favicon.ico">'
            f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{style}</style>'
            '<meta name="google-adsense-account" content="ca-pub-9505220977121599">'
            '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script>'
            f'</head><body>{header(locale).format(menu=menu)}<main class="wrap">{body}</main>'
            f'<footer><div class="wrap">Star Wars Zero Company Wiki · <a href="/about/sources-and-citations.html">Sources</a> · {TODAY}</div></footer></body></html>')


def cast_page(locale, slug, character, actor):
    c = COPY[locale]
    labels = c["cast"]
    direct = c["cast_intro"].format(actor=actor, character=character)
    context = c["cast_desc"][slug]
    title = f"{character} — {actor}"
    desc = direct + " " + context
    body = f'''<section class="hero"><div class="crumb">{escape(labels[0])}</div><h1>{escape(title)}</h1><p class="lead"><strong>{escape(direct)}</strong></p><span class="pill">{escape(labels[0])}</span></section>
<section class="two"><div class="block"><h2>{escape(labels[1])}</h2><p>{escape(direct)}</p><table><tr><th>Character</th><td>{escape(character)}</td></tr><tr><th>Actor</th><td>{escape(actor)}</td></tr><tr><th>Status</th><td>StarWars.com · 23 July 2026</td></tr></table></div><div class="block"><h2>{escape(labels[2])}</h2><p>{escape(context)}</p><p>{escape(c["cast_body"])}</p></div></section>
<section class="block"><h2>{escape(labels[3])}</h2><p>{escape(direct)} {escape(context)}</p><ul><li>{escape(character)} — {escape(actor)}</li><li>StarWars.com · 23 July 2026</li><li>Star Wars Zero Company · August 27, 2026</li></ul></section>
<section class="block"><h2>{escape(labels[4])}</h2><p>{escape(c["boundary"])}</p><p>{escape(c["cast_body"])}</p></section>
<section><h2>FAQ</h2><div class="grid"><a class="card" href="/{locale}/questions/is-zero-company-single-player.html">Single-player</a><a class="card" href="/{locale}/questions/when-does-star-wars-zero-company-release.html">Release date</a><a class="card" href="/{locale}/questions/what-platforms-is-zero-company-on.html">Platforms</a></div></section>
<section class="block"><h2>{escape(labels[5])}</h2><p><a href="{CAST_SOURCE}" rel="nofollow">StarWars.com official cast announcement</a></p><p class="source">{escape(c["boundary"])}</p></section>'''
    return shell(locale, "cast", slug, title, desc, body)


def class_page(locale, slug, name):
    c = COPY[locale]
    labels = c["class"]
    direct = c["class_intro"].format(name=name)
    role = c["class_desc"][slug]
    title = f"{name} — Star Wars Zero Company"
    desc = direct + " " + role
    body = f'''<section class="hero"><div class="crumb">{escape(labels[0])}</div><h1>{escape(name)}</h1><p class="lead"><strong>{escape(direct)}</strong></p><span class="pill">{escape(labels[0])}</span></section>
<section class="two"><div class="block"><h2>{escape(labels[1])}</h2><p>{escape(role)}</p><p>{escape(direct)}</p></div><div class="block"><h2>{escape(labels[2])}</h2><p>{escape(c["class_body"])}</p><p>{escape(role)}</p></div></section>
<section class="block"><h2>{escape(labels[3])}</h2><table><tr><th>Ultimate</th><td>1</td></tr><tr><th>Standard</th><td>1</td></tr><tr><th>Passive</th><td>1</td></tr></table><p>{escape(c["class_body"])}</p></section>
<section class="block"><h2>{escape(labels[4])}</h2><p>{escape(c["boundary"])}</p><p>{escape(role)} {escape(c["class_body"])}</p></section>
<section><h2>FAQ</h2><div class="grid"><a class="card" href="/{locale}/questions/is-zero-company-single-player.html">Single-player</a><a class="card" href="/{locale}/questions/how-many-action-points-per-turn.html">Action Points</a><a class="card" href="/{locale}/questions/can-you-disable-permadeath.html">Permadeath</a></div></section>
<section class="block"><h2>{escape(labels[5])}</h2><p><a href="{GAMEPLAY_SOURCE}" rel="nofollow">EA official gameplay deep dive</a></p><p class="source">{escape(c["boundary"])}</p></section>'''
    return shell(locale, "classes", slug, title, desc, body)


def hub_page(locale, family):
    c = COPY[locale]
    title, desc = c["hub_cast" if family == "cast" else "hub_class"]
    items = CAST if family == "cast" else CLASSES
    cards = "".join(
        f'<a class="card" href="/{locale}/{family}/{slug}.html">'
        f'<strong>{escape(vals[0] if family == "cast" else vals)}</strong><br>'
        f'<span class="mini">{escape((vals[1] + " · " + c["cast_desc"][slug]) if family == "cast" else c["class_desc"][slug])}</span></a>'
        for slug, vals in items.items()
    )
    source = CAST_SOURCE if family == "cast" else GAMEPLAY_SOURCE
    overview = c["cast_body"] if family == "cast" else c["class_body"]
    body = f'''<section class="hero"><div class="crumb">{escape(title)}</div><h1>{escape(title)}</h1><p class="lead">{escape(desc)}</p><span class="pill">Officially confirmed</span></section>
<section class="block"><h2>Overview</h2><p>{escape(overview)}</p><p>{escape(c["boundary"])}</p></section>
<section><h2>{escape(title)}</h2><div class="grid">{cards}</div></section>
<section class="block"><h2>Evidence</h2><p>{escape(overview)}</p><p>{escape(c["boundary"])}</p><p><a href="{source}" rel="nofollow">Official source</a></p></section>'''
    return shell(locale, family, None, title, desc, body, "CollectionPage")


def replace_alternates(path, family, slug=None):
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8")
    text = re.sub(r'<link rel="alternate"[^>]+>', "", text)
    text = re.sub(r'(<link rel="canonical"[^>]+>)',
                  lambda m: m.group(1) + alternates(family, slug),
                  text, count=1)
    path.write_text(text, encoding="utf-8")


def main():
    created = 0
    for locale in LOCALES:
        for family in ("cast", "classes"):
            folder = ROOT / locale / family
            folder.mkdir(parents=True, exist_ok=True)
            (folder / "index.html").write_text(hub_page(locale, family), encoding="utf-8")
            created += 1
        for slug, (character, actor) in CAST.items():
            (ROOT / locale / "cast" / f"{slug}.html").write_text(
                cast_page(locale, slug, character, actor), encoding="utf-8")
            created += 1
        for slug, name in CLASSES.items():
            (ROOT / locale / "classes" / f"{slug}.html").write_text(
                class_page(locale, slug, name), encoding="utf-8")
            created += 1

    for family, items in (("cast", CAST), ("classes", CLASSES)):
        replace_alternates(ROOT / family / "index.html", family)
        for locale in ("de", "ja"):
            replace_alternates(ROOT / locale / family / "index.html", family)
        for slug in items:
            replace_alternates(ROOT / family / f"{slug}.html", family, slug)
            for locale in ("de", "ja"):
                replace_alternates(ROOT / locale / family / f"{slug}.html", family, slug)
    print(f"Round 22 created {created} localized pages")


if __name__ == "__main__":
    main()
