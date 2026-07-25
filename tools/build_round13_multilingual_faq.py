#!/usr/bin/env python3
"""Round 13: extend ten verified, high-intent FAQs across all official languages."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = date.today().isoformat()
EA_QA = "https://www.ea.com/games/starwars/zero-company/news/answering-biggest-questions"
EA_BUY = "https://www.ea.com/games/starwars/zero-company/buy"
STEAM = "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/"

LOCALES = (
    ("en", "en", "English"), ("de", "de", "Deutsch"), ("fr", "fr", "Français"),
    ("it", "it", "Italiano"), ("es", "es", "Español"), ("ja", "ja", "日本語"),
    ("ko", "ko", "한국어"), ("pl", "pl", "Polski"),
    ("zh-cn", "zh-Hans", "简体中文"), ("zh-tw", "zh-Hant", "繁體中文"),
    ("pt-br", "pt-BR", "Português (Brasil)"),
)

SLUGS = (
    "when-does-star-wars-zero-company-release",
    "what-platforms-is-zero-company-on",
    "how-many-languages-does-zero-company-support",
    "is-zero-company-single-player",
    "does-zero-company-have-coop",
    "does-zero-company-have-romance",
    "can-you-disable-permadeath",
    "how-many-action-points-per-turn",
    "is-zero-company-on-steam-deck",
    "should-you-preorder",
)

# title, direct answer, player consequence, evidence boundary
COPY = {
    "fr": [
        ("Quand sort Star Wars Zero Company ?", "La sortie mondiale est fixée au 27 août 2026 à 15 h UTC sur les plateformes confirmées.", "En France métropolitaine, cela correspond à 17 h CEST. Les éditions Standard et Deluxe affichent la même date et aucun accès anticipé Deluxe n'est annoncé.", "Le préchargement et un éventuel patch du premier jour ne sont pas encore détaillés ; vérifiez le compteur de votre boutique avant le lancement."),
        ("Sur quelles plateformes sort Star Wars Zero Company ?", "Le jeu est confirmé sur PC, PlayStation 5 et Xbox Series X|S.", "Sur PC, les boutiques officielles sont EA app, Steam et Epic Games Store. PS4 et Xbox One ne figurent pas dans la liste annoncée.", "Nintendo Switch et Steam Deck restent non confirmés. L'absence d'annonce ne doit pas être transformée en promesse de version future."),
        ("Combien de langues Star Wars Zero Company prend-il en charge ?", "Onze langues sont confirmées pour l'interface et les sous-titres.", "La liste comprend anglais, français, italien, allemand, espagnol, japonais, coréen, polonais, chinois simplifié, chinois traditionnel et portugais du Brésil.", "Le doublage complet n'est indiqué qu'en anglais et en allemand ; le français concerne les textes et sous-titres."),
        ("Star Wars Zero Company est-il un jeu solo ?", "Oui. EA présente Zero Company comme une expérience tactique au tour par tour pour un joueur.", "La campagne se concentre sur la gestion de l'escouade, les opérations et la base The Den, sans dépendre d'un partenaire en ligne.", "Les exigences de connexion ou de compte propres à chaque boutique ne sont pas encore toutes détaillées et ne changent pas le statut solo du jeu."),
        ("Star Wars Zero Company propose-t-il de la coopération ?", "Non. Aucun mode coopératif ni multijoueur n'est annoncé.", "Les quatre membres déployés sont commandés par le même joueur pendant la campagne. Il ne faut donc pas acheter le jeu dans l'attente d'une coopération en ligne ou locale.", "EA peut annoncer de nouvelles fonctions plus tard, mais la version actuellement décrite est strictement solo."),
        ("Y a-t-il des romances dans Star Wars Zero Company ?", "Non. L'équipe a confirmé qu'il n'existe pas de système de romance.", "Les Bonds développent les relations et débloquent des synergies de combat, mais ils ne constituent pas des routes amoureuses. L'histoire principale reste globalement linéaire.", "Certains moments varient selon les membres présents dans l'escouade, sans créer de fins romantiques ou de branches complètes."),
        ("Peut-on désactiver la mort permanente ?", "Oui. La mort permanente est activée par défaut, mais peut être désactivée dans les réglages de campagne.", "La désactiver réduit le risque de perdre définitivement un agent après ses blessures. L'activer conserve une pression plus forte et rend la composition de l'effectif plus importante.", "Les conséquences exactes de chaque niveau de difficulté devront être vérifiées dans la version finale."),
        ("Combien de points d'action a un agent par tour ?", "Chaque agent dispose de trois points d'action pendant son tour.", "Déplacement, attaque et capacités se partagent ce budget. Le meilleur ordre dépend donc de la couverture, de la ligne de tir et des synergies disponibles.", "Les coûts précis de chaque capacité peuvent changer pendant le développement ; trois PA par agent est la règle générale montrée officiellement."),
        ("Star Wars Zero Company fonctionne-t-il sur Steam Deck ?", "La compatibilité Steam Deck n'est pas confirmée.", "Le jeu sort sur Steam pour PC, mais une fiche Steam ne garantit pas automatiquement la validation Deck ni des performances adaptées au portable.", "EA a indiqué travailler encore sur l'optimisation des plateformes annoncées. Attendez un badge Valve ou une déclaration officielle avant d'acheter pour cet usage."),
        ("Faut-il précommander Star Wars Zero Company ?", "La précommande n'est utile que si vous voulez le pack cosmétique Crystalline Astromech et acceptez d'acheter avant les tests.", "Les éditions Standard et Deluxe incluent le jeu de base ; Deluxe ajoute des cosmétiques République, Shadow Collective et des thèmes d'armes. Aucun avantage de puissance n'est annoncé.", "Attendre les tests permet d'évaluer performances et finition. Le bonus est cosmétique : il ne remplace ni une démo ni un accès anticipé."),
    ],
    "it": [
        ("Quando esce Star Wars Zero Company?", "L'uscita mondiale è fissata al 27 agosto 2026 alle 15:00 UTC.", "In Italia corrisponde alle 17:00 CEST. Standard e Deluxe riportano la stessa data e non è stato annunciato accesso anticipato per Deluxe.", "Precaricamento e patch del day one non sono ancora descritti: il conto alla rovescia dello store resta l'ultima verifica utile."),
        ("Su quali piattaforme esce Star Wars Zero Company?", "Le piattaforme confermate sono PC, PlayStation 5 e Xbox Series X|S.", "Su PC il gioco è disponibile tramite EA app, Steam ed Epic Games Store. PS4 e Xbox One non compaiono tra le versioni annunciate.", "Nintendo Switch e Steam Deck non sono confermati; una possibilità futura non va presentata come versione in sviluppo."),
        ("Quante lingue supporta Star Wars Zero Company?", "Sono confermate undici lingue per interfaccia e sottotitoli.", "L'elenco comprende inglese, francese, italiano, tedesco, spagnolo, giapponese, coreano, polacco, cinese semplificato, cinese tradizionale e portoghese brasiliano.", "L'audio completo è indicato soltanto per inglese e tedesco; l'italiano riguarda testi e sottotitoli."),
        ("Star Wars Zero Company è solo per giocatore singolo?", "Sì. EA lo descrive come un gioco tattico a turni per un giocatore.", "La campagna mette un solo giocatore al comando dell'intera squadra, delle operazioni e della base The Den.", "Eventuali requisiti di account o connessione dipendono dallo store e non trasformano il gioco in un titolo multigiocatore."),
        ("Star Wars Zero Company ha la modalità cooperativa?", "No. Non è stata annunciata alcuna modalità cooperativa o multigiocatore.", "I quattro agenti schierati vengono controllati dallo stesso giocatore. Non conviene acquistare aspettandosi cooperativa locale o online.", "Le funzioni potrebbero cambiare con annunci futuri, ma la versione descritta oggi è esclusivamente single-player."),
        ("Ci sono romance in Star Wars Zero Company?", "No. Gli sviluppatori hanno confermato che non esiste un sistema romantico.", "I Bonds fanno crescere le relazioni e sbloccano sinergie di combattimento, ma non sono percorsi sentimentali. La trama principale rimane sostanzialmente lineare.", "Alcune scene possono variare in base alla squadra presente, senza creare finali romantici o grandi rami narrativi."),
        ("Si può disattivare la morte permanente?", "Sì. La morte permanente è attiva per impostazione predefinita, ma può essere disattivata.", "Disattivarla riduce il rischio di perdere definitivamente un agente dopo le ferite; mantenerla aumenta la pressione strategica sulla rosa.", "Le differenze complete fra livelli di difficoltà andranno controllate nella versione pubblicata."),
        ("Quanti punti azione ha un agente per turno?", "Ogni agente dispone di tre punti azione nel proprio turno.", "Movimento, attacchi e abilità consumano lo stesso budget, quindi copertura e ordine delle azioni sono centrali.", "I costi delle singole capacità possono cambiare durante lo sviluppo; tre PA per agente è la regola generale confermata."),
        ("Star Wars Zero Company è compatibile con Steam Deck?", "La compatibilità con Steam Deck non è confermata.", "L'uscita su Steam non equivale automaticamente alla verifica Deck o a prestazioni adeguate sul dispositivo portatile.", "È prudente attendere il badge di Valve o una dichiarazione EA prima di comprare il gioco principalmente per Steam Deck."),
        ("Conviene prenotare Star Wars Zero Company?", "La prenotazione ha senso solo per chi desidera il pacchetto cosmetico Crystalline Astromech e accetta di acquistare prima delle recensioni.", "Standard e Deluxe includono il gioco base; Deluxe aggiunge cosmetici Repubblica, Shadow Collective e temi per armi, senza bonus di potenza annunciati.", "Aspettare permette di valutare prestazioni e qualità. Il bonus non è una demo né un accesso anticipato."),
    ],
    "es": [
        ("¿Cuándo sale Star Wars Zero Company?", "El lanzamiento mundial está fijado para el 27 de agosto de 2026 a las 15:00 UTC.", "En la España peninsular serán las 17:00 CEST y en Canarias las 16:00. Standard y Deluxe comparten fecha y no hay acceso anticipado anunciado.", "La precarga y un posible parche de lanzamiento no están detallados; revisa el contador de tu tienda antes de jugar."),
        ("¿En qué plataformas sale Star Wars Zero Company?", "Está confirmado para PC, PlayStation 5 y Xbox Series X|S.", "En PC se vende en EA app, Steam y Epic Games Store. PS4 y Xbox One no aparecen entre las versiones anunciadas.", "Nintendo Switch y Steam Deck siguen sin confirmar; no debe confundirse la falta de noticias con una promesa futura."),
        ("¿Cuántos idiomas admite Star Wars Zero Company?", "Hay once idiomas confirmados para interfaz y subtítulos.", "Son inglés, francés, italiano, alemán, español, japonés, coreano, polaco, chino simplificado, chino tradicional y portugués de Brasil.", "El audio completo solo figura para inglés y alemán; el español incluye textos y subtítulos, no doblaje completo."),
        ("¿Star Wars Zero Company es para un jugador?", "Sí. EA lo presenta como un juego táctico por turnos para un jugador.", "Una persona controla a toda la escuadra, las operaciones y la gestión de The Den durante la campaña.", "Los requisitos de cuenta o conexión de cada tienda aún pueden variar y no convierten la experiencia en multijugador."),
        ("¿Star Wars Zero Company tiene cooperativo?", "No. No se ha anunciado modo cooperativo ni multijugador.", "Los cuatro agentes desplegados los controla el mismo jugador. No conviene comprarlo esperando cooperativo local u online.", "Una actualización futura requeriría un anuncio nuevo; la propuesta confirmada actualmente es solo para un jugador."),
        ("¿Hay romances en Star Wars Zero Company?", "No. El equipo ha confirmado que no existe un sistema de romances.", "Los Bonds desarrollan relaciones y desbloquean sinergias de combate, pero no son rutas románticas. La historia principal es en gran medida lineal.", "Algunas escenas cambian según quién esté en el equipo, sin crear finales románticos ni ramas narrativas completas."),
        ("¿Se puede desactivar la muerte permanente?", "Sí. Viene activada por defecto, pero puede desactivarse en la configuración de campaña.", "Apagarla reduce el riesgo de perder definitivamente a un agente tras sus heridas; mantenerla añade presión a la gestión de la plantilla.", "Las diferencias exactas entre dificultades deberán comprobarse en la versión final."),
        ("¿Cuántos puntos de acción tiene cada agente?", "Cada agente dispone de tres puntos de acción durante su turno.", "Movimiento, ataques y habilidades comparten ese presupuesto, por lo que el orden y la cobertura importan en cada decisión.", "Los costes de habilidades concretas pueden cambiar; tres PA por agente es la regla general mostrada oficialmente."),
        ("¿Funciona Star Wars Zero Company en Steam Deck?", "La compatibilidad con Steam Deck no está confirmada.", "Que el juego salga en Steam no garantiza la verificación Deck ni un rendimiento adecuado en el dispositivo.", "Es mejor esperar una insignia de Valve o una declaración de EA antes de comprarlo principalmente para Steam Deck."),
        ("¿Merece la pena reservar Star Wars Zero Company?", "Solo si quieres el paquete cosmético Crystalline Astromech y aceptas comprar antes de ver análisis.", "Standard y Deluxe incluyen el juego base; Deluxe añade cosméticos de la República, Shadow Collective y diseños de armas, sin ventajas de potencia anunciadas.", "Esperar permite valorar rendimiento y acabado. El incentivo no es una demo ni acceso anticipado."),
    ],
    "pl": [
        ("Kiedy odbędzie się premiera Star Wars Zero Company?", "Światowa premiera nastąpi 27 sierpnia 2026 roku o 15:00 UTC.", "W Polsce będzie to 17:00 CEST. Edycje Standard i Deluxe mają ten sam termin, a wcześniejszy dostęp nie został zapowiedziany.", "Preload i aktualizacja pierwszego dnia nie są jeszcze opisane; przed startem sprawdź licznik w swoim sklepie."),
        ("Na jakich platformach ukaże się Star Wars Zero Company?", "Potwierdzono PC, PlayStation 5 oraz Xbox Series X|S.", "Na PC grę sprzedają EA app, Steam i Epic Games Store. PS4 i Xbox One nie znajdują się na ogłoszonej liście.", "Nintendo Switch i Steam Deck pozostają niepotwierdzone; brak informacji nie oznacza zapowiedzi przyszłej wersji."),
        ("Ile języków obsługuje Star Wars Zero Company?", "Interfejs i napisy będą dostępne w jedenastu językach.", "Lista obejmuje angielski, francuski, włoski, niemiecki, hiszpański, japoński, koreański, polski, chiński uproszczony i tradycyjny oraz portugalski brazylijski.", "Pełny dubbing zaznaczono tylko po angielsku i niemiecku; polski obejmuje tekst oraz napisy."),
        ("Czy Star Wars Zero Company jest grą jednoosobową?", "Tak. EA określa grę jako turową taktykę dla jednego gracza.", "Jedna osoba dowodzi całą drużyną, wybiera operacje i zarządza bazą The Den.", "Wymagania konta lub połączenia zależne od sklepu nie są jeszcze w pełni opisane i nie zmieniają jednoosobowego charakteru gry."),
        ("Czy Star Wars Zero Company ma tryb kooperacji?", "Nie. Nie zapowiedziano kooperacji ani trybu wieloosobowego.", "Czterema agentami w misji steruje jeden gracz. Nie należy kupować gry z oczekiwaniem lokalnej lub sieciowej kooperacji.", "Ewentualna zmiana wymagałaby nowego komunikatu; obecnie potwierdzona wersja jest wyłącznie single-player."),
        ("Czy w Star Wars Zero Company są romanse?", "Nie. Twórcy potwierdzili brak systemu romansów.", "Bonds rozwijają relacje i odblokowują synergie bojowe, lecz nie tworzą ścieżek romantycznych. Główna fabuła pozostaje zasadniczo liniowa.", "Niektóre sceny zależą od składu drużyny, ale nie prowadzą do romantycznych zakończeń ani pełnych gałęzi fabularnych."),
        ("Czy można wyłączyć permanentną śmierć?", "Tak. Permanentna śmierć jest domyślnie włączona, ale można ją wyłączyć.", "Wyłączenie zmniejsza ryzyko trwałej utraty agenta po obrażeniach; pozostawienie opcji zwiększa presję podczas zarządzania składem.", "Pełne różnice między poziomami trudności trzeba będzie sprawdzić w wydanej wersji."),
        ("Ile punktów akcji ma agent w turze?", "Każdy agent ma trzy punkty akcji na swoją turę.", "Ruch, ataki i zdolności korzystają z tego samego budżetu, dlatego kolejność działań i osłona są kluczowe.", "Koszty konkretnych umiejętności mogą się zmienić; trzy PA na agenta to oficjalnie pokazana reguła ogólna."),
        ("Czy Star Wars Zero Company działa na Steam Deck?", "Zgodność ze Steam Deck nie została potwierdzona.", "Obecność gry na Steam nie gwarantuje automatycznie weryfikacji Deck ani odpowiedniej wydajności.", "Przed zakupem głównie z myślą o urządzeniu warto poczekać na oznaczenie Valve lub komunikat EA."),
        ("Czy warto zamówić Star Wars Zero Company przed premierą?", "Tylko jeśli zależy ci na kosmetycznym pakiecie Crystalline Astromech i akceptujesz zakup przed recenzjami.", "Standard i Deluxe zawierają grę podstawową; Deluxe dodaje kosmetyki Republiki, Shadow Collective i motywy broni bez ogłoszonej przewagi bojowej.", "Poczekanie pozwala ocenić wydajność i jakość. Bonus nie jest demem ani wcześniejszym dostępem."),
    ],
    "pt-br": [
        ("Quando Star Wars Zero Company será lançado?", "O lançamento mundial está marcado para 27 de agosto de 2026, às 15:00 UTC.", "No horário de Brasília, será 12:00 BRT. Standard e Deluxe têm a mesma data, sem acesso antecipado anunciado.", "Pré-carregamento e patch de estreia ainda não foram detalhados; confirme o contador da loja antes do lançamento."),
        ("Em quais plataformas Star Wars Zero Company será lançado?", "O jogo está confirmado para PC, PlayStation 5 e Xbox Series X|S.", "No PC, as lojas são EA app, Steam e Epic Games Store. PS4 e Xbox One não aparecem na lista anunciada.", "Nintendo Switch e Steam Deck continuam sem confirmação; ausência de notícia não é promessa de versão futura."),
        ("Quantos idiomas Star Wars Zero Company terá?", "Onze idiomas estão confirmados para interface e legendas.", "A lista inclui inglês, francês, italiano, alemão, espanhol, japonês, coreano, polonês, chinês simplificado, chinês tradicional e português do Brasil.", "Áudio completo aparece apenas em inglês e alemão; português brasileiro cobre textos e legendas."),
        ("Star Wars Zero Company é para um jogador?", "Sim. A EA apresenta o título como um jogo tático em turnos para um jogador.", "Uma pessoa controla todo o esquadrão, escolhe operações e administra The Den ao longo da campanha.", "Requisitos de conta ou conexão da loja ainda podem variar e não transformam a experiência em multiplayer."),
        ("Star Wars Zero Company tem modo cooperativo?", "Não. Nenhum modo cooperativo ou multiplayer foi anunciado.", "Os quatro agentes da missão são controlados pelo mesmo jogador. Não compre esperando coop local ou online.", "Uma mudança futura exigiria novo anúncio; a versão confirmada hoje é exclusivamente single-player."),
        ("Há romance em Star Wars Zero Company?", "Não. A equipe confirmou que não existe sistema de romance.", "Bonds desenvolvem relações e liberam sinergias de combate, mas não são rotas românticas. A história principal é, em grande parte, linear.", "Algumas cenas podem mudar conforme o esquadrão presente, sem criar finais românticos ou grandes ramificações."),
        ("É possível desativar a morte permanente?", "Sim. A morte permanente vem ativada por padrão, mas pode ser desligada.", "Desativá-la reduz o risco de perder um agente definitivamente após ferimentos; mantê-la aumenta a pressão sobre o elenco.", "As diferenças completas entre dificuldades precisarão ser verificadas na versão lançada."),
        ("Quantos pontos de ação cada agente possui?", "Cada agente recebe três pontos de ação em seu turno.", "Movimento, ataques e habilidades compartilham esse orçamento, tornando ordem das ações e cobertura decisões centrais.", "Custos de habilidades específicas podem mudar; três PA por agente é a regra geral mostrada oficialmente."),
        ("Star Wars Zero Company funciona no Steam Deck?", "A compatibilidade com Steam Deck não está confirmada.", "O lançamento no Steam não garante verificação Deck nem desempenho adequado no portátil.", "Aguarde o selo da Valve ou uma declaração da EA antes de comprar principalmente para jogar no Steam Deck."),
        ("Vale a pena reservar Star Wars Zero Company?", "Somente se você quiser o pacote cosmético Crystalline Astromech e aceitar comprar antes das análises.", "Standard e Deluxe incluem o jogo base; Deluxe acrescenta cosméticos da República, Shadow Collective e temas de armas, sem vantagem de poder anunciada.", "Esperar permite avaliar desempenho e acabamento. O bônus não é demo nem acesso antecipado."),
    ],
    "ko": [
        ("Star Wars Zero Company 출시일은 언제인가요?", "전 세계 출시 시각은 2026년 8월 27일 15:00 UTC입니다.", "한국 시간으로는 8월 28일 00:00 KST입니다. Standard와 Deluxe의 출시일은 같고 Deluxe 조기 이용은 발표되지 않았습니다.", "사전 다운로드와 첫날 패치 일정은 아직 공개되지 않았으므로 출시 직전 스토어의 카운트다운을 확인하세요."),
        ("Star Wars Zero Company는 어떤 플랫폼으로 나오나요?", "PC, PlayStation 5, Xbox Series X|S 출시가 확정되었습니다.", "PC에서는 EA app, Steam, Epic Games Store를 이용합니다. PS4와 Xbox One 버전은 발표 목록에 없습니다.", "Nintendo Switch와 Steam Deck 지원은 미확정입니다. 소식이 없다는 사실을 향후 출시 약속으로 해석하면 안 됩니다."),
        ("Star Wars Zero Company는 몇 개 언어를 지원하나요?", "인터페이스와 자막 기준으로 11개 언어를 지원합니다.", "영어, 프랑스어, 이탈리아어, 독일어, 스페인어, 일본어, 한국어, 폴란드어, 중국어 간체와 번체, 브라질 포르투갈어입니다.", "전체 음성은 영어와 독일어만 표시되어 있으며 한국어는 인터페이스와 자막 지원입니다."),
        ("Star Wars Zero Company는 싱글 플레이 게임인가요?", "네. EA는 이 게임을 싱글 플레이 턴제 전술 게임으로 소개합니다.", "한 명의 플레이어가 전체 분대, Operation 선택, The Den 관리를 담당합니다.", "스토어별 계정이나 연결 요구 사항은 달라질 수 있지만 게임이 멀티플레이가 되는 것은 아닙니다."),
        ("Star Wars Zero Company에 협동 모드가 있나요?", "아니요. 협동이나 멀티플레이 모드는 발표되지 않았습니다.", "임무에 투입되는 네 명의 요원 모두 한 명의 플레이어가 조작합니다. 로컬 또는 온라인 협동을 기대하고 구매하면 안 됩니다.", "향후 변경에는 별도 발표가 필요하며 현재 확인된 구성은 싱글 플레이 전용입니다."),
        ("Star Wars Zero Company에 연애 시스템이 있나요?", "아니요. 개발진은 연애 시스템이 없다고 확인했습니다.", "Bonds는 관계를 성장시키고 전투 시너지를 해금하지만 연애 루트는 아닙니다. 메인 스토리는 대체로 선형입니다.", "분대 구성에 따라 일부 장면은 달라질 수 있으나 연애 엔딩이나 큰 분기 스토리는 없습니다."),
        ("영구 사망을 끌 수 있나요?", "네. 영구 사망은 기본으로 켜져 있지만 캠페인 설정에서 끌 수 있습니다.", "끄면 부상 후 요원을 영구적으로 잃을 위험이 줄고, 켜 두면 명단 관리의 압박이 커집니다.", "난이도별 세부 차이는 출시 버전에서 다시 확인해야 합니다."),
        ("요원은 턴마다 행동 포인트를 몇 개 받나요?", "각 요원은 자신의 턴에 3개의 행동 포인트를 받습니다.", "이동, 공격, 능력이 같은 예산을 사용하므로 행동 순서와 엄폐가 중요합니다.", "개별 능력 비용은 개발 중 바뀔 수 있지만 요원당 3 AP는 공식적으로 공개된 일반 규칙입니다."),
        ("Star Wars Zero Company는 Steam Deck을 지원하나요?", "Steam Deck 호환성은 아직 확인되지 않았습니다.", "Steam 출시 자체가 Deck 인증이나 휴대 기기에서의 적절한 성능을 보장하지 않습니다.", "Steam Deck용으로 구매하려면 Valve 인증 배지나 EA의 공식 안내를 기다리는 편이 안전합니다."),
        ("Star Wars Zero Company를 예약 구매해야 하나요?", "Crystalline Astromech 꾸미기 팩을 원하고 리뷰 전에 구매할 의사가 있을 때만 의미가 있습니다.", "Standard와 Deluxe 모두 기본 게임을 포함하며 Deluxe는 공화국, Shadow Collective, 무기 테마 꾸미기를 추가합니다. 전투력 보너스는 발표되지 않았습니다.", "기다리면 성능과 완성도를 확인할 수 있습니다. 예약 특전은 데모나 조기 이용권이 아닙니다."),
    ],
    "zh-cn": [
        ("Star Wars Zero Company 什么时候发售？", "全球解锁时间为2026年8月27日15:00 UTC。", "北京时间对应8月27日23:00。Standard与Deluxe版同日解锁，目前没有公布Deluxe抢先体验。", "预载时间和首日补丁尚未说明，发售前应以所购商店的倒计时为最终核验。"),
        ("Star Wars Zero Company 登陆哪些平台？", "已确认平台是PC、PlayStation 5和Xbox Series X|S。", "PC端包括EA app、Steam与Epic Games Store。官方列表没有PS4和Xbox One版本。", "Nintendo Switch和Steam Deck仍未确认；没有消息不等于官方承诺未来推出。"),
        ("Star Wars Zero Company 支持多少种语言？", "界面与字幕共确认支持11种语言。", "包括英语、法语、意大利语、德语、西班牙语、日语、韩语、波兰语、简体中文、繁体中文与巴西葡萄牙语。", "完整配音仅标注英语和德语；简体中文支持界面与字幕，并非中文全程配音。"),
        ("Star Wars Zero Company 是单人游戏吗？", "是。EA将其明确描述为单人回合制战术游戏。", "一名玩家负责控制整支小队、选择Operation并管理The Den基地。", "不同商店可能仍有账户或联网要求，但这不会把游戏变成多人作品。"),
        ("Star Wars Zero Company 有合作模式吗？", "没有。官方尚未公布合作或其他多人模式。", "任务中的四名干员都由同一名玩家操控，不应以期待本地或在线合作的前提购买。", "未来若发生变化需要新的官方公告；当前确认版本是纯单人体验。"),
        ("Star Wars Zero Company 有恋爱系统吗？", "没有。开发团队已明确确认游戏不存在恋爱系统。", "Bonds会发展角色关系并解锁战斗协同，但不是恋爱路线。主线故事整体保持线性。", "部分场景会因出战成员而变化，但不会形成恋爱结局或完整分支剧情。"),
        ("可以关闭永久死亡吗？", "可以。永久死亡默认开启，但玩家能够在战役设置中关闭。", "关闭后可降低角色因受伤而永久离队的风险；保持开启则会强化名册管理压力。", "各难度的完整差异仍需在正式版内验证。"),
        ("每名干员每回合有多少行动点？", "每名干员在自己的回合拥有3个行动点。", "移动、攻击与能力共用这一预算，因此行动顺序、掩体和射线判断非常重要。", "具体技能的AP消耗仍可能调整；每名干员3 AP是官方展示的一般规则。"),
        ("Star Wars Zero Company 支持Steam Deck吗？", "目前尚未确认Steam Deck兼容性。", "游戏登陆Steam并不自动代表通过Deck验证，也不能保证掌机性能。", "如果主要在Steam Deck游玩，建议等待Valve验证标识或EA官方说明后再购买。"),
        ("Star Wars Zero Company 值得预购吗？", "只有在你确实想要Crystalline Astromech外观包，并接受评测前购买时才有必要。", "Standard与Deluxe都含本体；Deluxe额外提供共和国、Shadow Collective与武器主题外观，未公布战力优势。", "等待评测可以核对性能和完成度。预购奖励不是Demo，也不提供抢先体验。"),
    ],
    "zh-tw": [
        ("Star Wars Zero Company 何時發售？", "全球解鎖時間是2026年8月27日15:00 UTC。", "台灣與香港時間對應8月27日23:00。Standard與Deluxe同日解鎖，目前沒有Deluxe搶先體驗公告。", "預載與首日更新仍未說明，發售前請以購買平台的倒數時間作最後確認。"),
        ("Star Wars Zero Company 登上哪些平台？", "已確認PC、PlayStation 5與Xbox Series X|S。", "PC商店包含EA app、Steam和Epic Games Store。官方清單沒有PS4與Xbox One版本。", "Nintendo Switch和Steam Deck仍未確認；沒有消息不代表官方承諾日後推出。"),
        ("Star Wars Zero Company 支援多少種語言？", "介面與字幕共確認支援11種語言。", "包含英文、法文、義大利文、德文、西班牙文、日文、韓文、波蘭文、簡體中文、繁體中文與巴西葡萄牙文。", "完整配音只標示英文與德文；繁體中文提供介面和字幕，而非中文全程配音。"),
        ("Star Wars Zero Company 是單人遊戲嗎？", "是。EA明確把本作描述為單人回合制戰術遊戲。", "一名玩家控制整支小隊、選擇Operation並管理The Den基地。", "各商店可能有帳號或連線要求，但不會因此變成多人遊戲。"),
        ("Star Wars Zero Company 有合作模式嗎？", "沒有。官方未公布合作或其他多人模式。", "任務中的四名幹員全由同一名玩家操控，不應以期待本機或線上合作的前提購買。", "未來若改變需要新的官方公告；目前確認內容是純單人體驗。"),
        ("Star Wars Zero Company 有戀愛系統嗎？", "沒有。開發團隊已明確確認不存在戀愛系統。", "Bonds會發展角色關係並解鎖戰鬥協同，但不是戀愛路線。主線故事整體維持線性。", "部分場景可因出戰成員而改變，但不會形成戀愛結局或完整分支劇情。"),
        ("可以關閉永久死亡嗎？", "可以。永久死亡預設開啟，但玩家能在戰役設定中關閉。", "關閉可降低角色因受傷永久離隊的風險；維持開啟則增加名單管理壓力。", "不同難度的完整差異仍需在正式版內驗證。"),
        ("每名幹員每回合有多少行動點？", "每名幹員在自己的回合有3個行動點。", "移動、攻擊與能力共用此預算，因此行動順序、掩體和射線判斷很重要。", "個別技能的AP消耗仍可能調整；每名幹員3 AP是官方展示的一般規則。"),
        ("Star Wars Zero Company 支援Steam Deck嗎？", "目前尚未確認Steam Deck相容性。", "遊戲登上Steam不代表自動通過Deck驗證，也不能保證掌機效能。", "若主要想在Steam Deck遊玩，建議等待Valve驗證標章或EA官方說明。"),
        ("Star Wars Zero Company 值得預購嗎？", "只有在你確實想要Crystalline Astromech外觀包，並接受評測前購買時才有必要。", "Standard與Deluxe都含本體；Deluxe另有共和國、Shadow Collective及武器主題外觀，未公布戰力優勢。", "等待評測能核對效能與完成度。預購獎勵不是Demo，也沒有搶先體驗。"),
    ],
}

# Only these four high-intent pages are missing from the existing German/Japanese sets.
EXTRA = {
    "de": {
        SLUGS[5]: ("Gibt es Romanzen in Star Wars Zero Company?", "Nein. Das Team hat bestätigt, dass es kein Romanzen-System gibt.", "Bonds entwickeln Beziehungen und Kampfsynchronien, sind aber keine Liebespfade. Die Haupthandlung bleibt weitgehend linear.", "Einzelne Szenen können sich je nach Trupp ändern, ohne Romanzen-Enden oder vollständige Handlungszweige zu erzeugen."),
        SLUGS[6]: ("Kann man Permadeath deaktivieren?", "Ja. Permadeath ist standardmäßig aktiv, kann in den Kampagneneinstellungen aber ausgeschaltet werden.", "Ohne Permadeath sinkt das Risiko, einen Operator nach Verletzungen dauerhaft zu verlieren; aktiviert erhöht es den Druck auf die Einsatzplanung.", "Die vollständigen Unterschiede der Schwierigkeitsgrade müssen in der Veröffentlichung geprüft werden."),
        SLUGS[8]: ("Läuft Star Wars Zero Company auf Steam Deck?", "Steam-Deck-Kompatibilität ist derzeit nicht bestätigt.", "Eine Steam-Veröffentlichung garantiert weder Valves Deck-Prüfsiegel noch geeignete Leistung auf dem Handheld.", "Wer hauptsächlich auf Steam Deck spielen will, sollte vor dem Kauf auf ein Valve-Siegel oder eine EA-Aussage warten."),
        SLUGS[9]: ("Sollte man Star Wars Zero Company vorbestellen?", "Eine Vorbestellung lohnt sich nur, wenn du das kosmetische Crystalline-Astromech-Paket möchtest und vor Tests kaufen willst.", "Standard und Deluxe enthalten das Basisspiel; Deluxe ergänzt Republik-, Shadow-Collective- und Waffen-Kosmetik ohne angekündigten Stärkevorteil.", "Abwarten ermöglicht Leistungs- und Qualitätschecks. Der Bonus ist weder Demo noch Vorabzugang."),
    },
    "ja": {
        SLUGS[5]: ("Star Wars Zero Companyに恋愛要素はありますか？", "いいえ。開発チームは恋愛システムが存在しないと明言しています。", "Bondsは関係性を成長させ戦闘シナジーを解除しますが、恋愛ルートではありません。メインストーリーは概ね直線的です。", "編成によって一部の場面は変化しますが、恋愛エンディングや大きな分岐にはなりません。"),
        SLUGS[6]: ("パーマデスは無効にできますか？", "はい。パーマデスは初期設定で有効ですが、キャンペーン設定から無効にできます。", "無効にすると負傷後に隊員を永久に失う危険が減り、有効のままなら人員管理の緊張感が高まります。", "難易度ごとの完全な違いは発売版で改めて確認する必要があります。"),
        SLUGS[8]: ("Star Wars Zero CompanyはSteam Deckに対応しますか？", "Steam Deck互換性は現時点で確認されていません。", "Steamで発売されること自体はDeck認証や携帯機での十分な性能を保証しません。", "Steam Deckを主目的に購入する場合は、Valveの認証表示またはEAの公式発表を待つのが安全です。"),
        SLUGS[9]: ("Star Wars Zero Companyは予約購入すべきですか？", "Crystalline Astromechの外観パックが必要で、レビュー前の購入を受け入れられる場合に限り意味があります。", "StandardとDeluxeはいずれも本編を含み、Deluxeには共和国、Shadow Collective、武器テーマの外観が追加されます。性能上の優位は発表されていません。", "待てば動作と完成度を確認できます。予約特典はデモでも先行アクセスでもありません。"),
    },
}

UI = {
    "fr": ("FAQ", "Réponse vérifiée", "Ce que cela change", "Limite de la preuve", "Questions essentielles", "Sources officielles"),
    "it": ("FAQ", "Risposta verificata", "Cosa cambia", "Limite delle prove", "Domande essenziali", "Fonti ufficiali"),
    "es": ("FAQ", "Respuesta verificada", "Qué cambia", "Límite de la evidencia", "Preguntas esenciales", "Fuentes oficiales"),
    "pl": ("FAQ", "Zweryfikowana odpowiedź", "Co to zmienia", "Granica dowodów", "Najważniejsze pytania", "Oficjalne źródła"),
    "pt-br": ("FAQ", "Resposta verificada", "O que isso muda", "Limite da evidência", "Perguntas essenciais", "Fontes oficiais"),
    "ko": ("FAQ", "확인된 답변", "플레이어에게 미치는 영향", "확인 범위", "핵심 질문", "공식 출처"),
    "zh-cn": ("常见问题", "已核实回答", "对玩家的影响", "证据边界", "核心问题", "官方来源"),
    "zh-tw": ("常見問題", "已核實回答", "對玩家的影響", "證據邊界", "核心問題", "官方來源"),
    "de": ("FAQ", "Bestätigte Antwort", "Auswirkung für Spieler", "Grenze der Belege", "Wichtige Fragen", "Offizielle Quellen"),
    "ja": ("FAQ", "確認済みの回答", "プレイヤーへの影響", "確認範囲", "重要な質問", "公式情報"),
}

NOTE = {
    "fr": "Méthode de vérification : cette réponse recoupe la FAQ communautaire EA, la page d’achat officielle et la fiche de plateforme lorsqu’elles couvrent le même sujet. Une fonctionnalité absente des annonces reste classée « non confirmée », plutôt que transformée en promesse. Après la sortie, la page devra être révisée avec le menu réel du jeu et un test reproductible.",
    "it": "Metodo di verifica: la risposta confronta la FAQ EA, la pagina di acquisto ufficiale e la scheda della piattaforma quando trattano lo stesso argomento. Una funzione assente dagli annunci resta «non confermata» e non diventa una promessa. Dopo l’uscita, la pagina dovrà essere controllata con i menu reali e un test riproducibile nel gioco.",
    "es": "Método de verificación: la respuesta contrasta la FAQ de EA, la página oficial de compra y la ficha de plataforma cuando cubren el mismo tema. Una función ausente de los anuncios sigue «sin confirmar» y no se convierte en promesa. Tras el lanzamiento, esta página deberá revisarse con los menús reales y una prueba reproducible dentro del juego.",
    "pl": "Metoda weryfikacji: odpowiedź porównuje FAQ EA, oficjalną stronę zakupu i kartę platformy, gdy dotyczą tego samego tematu. Funkcja nieobecna w komunikatach pozostaje „niepotwierdzona”, zamiast stawać się obietnicą. Po premierze stronę należy sprawdzić w rzeczywistym menu gry i za pomocą powtarzalnego testu.",
    "pt-br": "Método de verificação: a resposta compara a FAQ da EA, a página oficial de compra e a ficha da plataforma quando tratam do mesmo assunto. Um recurso ausente dos anúncios continua «não confirmado», sem virar promessa. Depois do lançamento, a página deverá ser revisada com os menus reais e um teste reproduzível dentro do jogo.",
    "ko": "검증 방법: 같은 주제를 다룰 때 EA Q&A, 공식 구매 페이지, 플랫폼 스토어 정보를 서로 대조합니다. 발표에 없는 기능은 약속으로 바꾸지 않고 ‘미확정’으로 유지합니다. 출시 후에는 실제 게임 메뉴와 반복 가능한 테스트를 이용해 이 답변을 다시 확인해야 합니다.",
    "zh-cn": "核验方法：当EA社区问答、官方购买页和平台商店涉及同一主题时，本页会交叉比对三者。公告中没有出现的功能只标为“尚未确认”，不会被写成未来承诺。正式发售后，还需要根据实际菜单与可重复测试重新核对本页结论，并记录对应版本与核验日期，避免旧答案继续误导购买或玩法判断。",
    "zh-tw": "核驗方法：當EA社群問答、官方購買頁與平台商店涉及同一主題時，本頁會交叉比對三者。公告未出現的功能只標示為「尚未確認」，不會被寫成未來承諾。正式發售後，仍需依照實際選單與可重複測試重新核對本頁結論，並記錄對應版本與核驗日期，避免舊答案繼續誤導購買或玩法判斷。",
    "de": "Prüfmethode: Die Antwort gleicht EAs Community-FAQ, die offizielle Kaufseite und den jeweiligen Plattform-Eintrag ab, wenn sie dasselbe Thema behandeln. Eine nicht angekündigte Funktion bleibt „unbestätigt“ und wird nicht zum Versprechen. Nach Veröffentlichung muss die Seite anhand echter Menüs und eines reproduzierbaren Tests erneut geprüft werden. Bis dahin nennt der Artikel bewusst keine erfundenen Leistungswerte, versteckten Optionen oder Termine.",
    "ja": "確認方法：EAのコミュニティQ&A、公式購入ページ、プラットフォームストアが同じ話題を扱う場合は相互に照合します。発表にない機能を将来の約束として扱わず「未確認」とします。発売後は実際のメニューと再現可能なテストで回答を更新します。",
}

STYLE = """:root{--bg:#071016;--panel:#0d1922;--line:#284050;--text:#edf7ff;--muted:#a9bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.72 system-ui,-apple-system,'Segoe UI',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:64px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}nav>a{color:var(--muted);font-size:14px}.hero{padding:50px 0 28px;border-bottom:1px solid var(--line)}h1{font-size:clamp(32px,5.5vw,54px);line-height:1.12;margin:12px 0}h2{font-size:23px;margin:32px 0 12px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:20px;color:#d6e5ec}.card,.block{display:block;border:1px solid var(--line);border-radius:9px;background:var(--panel);padding:20px;margin:15px 0;color:var(--text)}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(245px,1fr));gap:14px}.pill{display:inline-block;border:1px solid #3c625f;padding:5px 9px;color:var(--teal);font-size:12px}.muted{color:var(--muted);font-size:14px}.fact{font-size:18px;border-left:4px solid var(--gold)}table{width:100%;border-collapse:collapse;margin:15px 0}th,td{border:1px solid var(--line);padding:11px;text-align:left}th{color:var(--gold);width:28%}footer{border-top:1px solid var(--line);margin-top:46px;padding:28px 0;color:var(--muted);font-size:14px}.lang-menu{position:relative;display:inline-block}.lang-menu summary{cursor:pointer;border:1px solid #365264;border-radius:7px;padding:8px 11px;background:#0d1922}.lang-options{position:absolute;right:0;min-width:170px;padding:6px;background:#0b161e;border:1px solid #365264;border-radius:8px;z-index:9}.lang-options a{display:block;padding:8px}.lang-options a[aria-current=page]{color:var(--gold)}@media(max-width:760px){nav{margin-left:0}.lang-options{position:static}}"""


def route(locale: str, slug: str) -> str:
    return f"/{locale}/questions/{slug}.html" if locale != "en" else f"/questions/{slug}.html"


def hreflang(slug: str) -> str:
    links = []
    for loc, tag, _ in LOCALES:
        links.append(f'<link rel="alternate" hreflang="{tag}" href="{SITE}{route(loc, slug)}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{route("en", slug)}">')
    return "".join(links)


def menu(locale: str, slug: str) -> str:
    current = next(label for code, _, label in LOCALES if code == locale)
    items = "".join(
        f'<a href="{route(code, slug)}" lang="{tag}"{" aria-current=\"page\"" if code == locale else ""}>{escape(label)}</a>'
        for code, tag, label in LOCALES
    )
    return f'<details class="lang-menu"><summary>{escape(current)}</summary><div class="lang-options">{items}</div></details>'


def localized_page(locale: str, lang: str, slug: str, item: tuple, index: int, all_items=None) -> str:
    title, direct, impact, boundary = item
    labels = UI[locale]
    canonical = SITE + route(locale, slug)
    desc = direct + " " + impact
    schema = {
        "@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
        "mainEntity": [{"@type": "Question", "name": title,
                        "acceptedAnswer": {"@type": "Answer", "text": direct + " " + impact}}],
    }
    # Four body structures are rotated to avoid a single visual/content template.
    if index % 4 == 0:
        body = f'<section class="block fact"><h2>{escape(labels[1])}</h2><p>{escape(direct)}</p></section><section class="grid"><div class="card"><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p></div><div class="card"><h2>{escape(labels[3])}</h2><p>{escape(boundary)}</p></div></section>'
    elif index % 4 == 1:
        body = f'<section><table><tr><th>{escape(labels[1])}</th><td>{escape(direct)}</td></tr><tr><th>{escape(labels[2])}</th><td>{escape(impact)}</td></tr><tr><th>{escape(labels[3])}</th><td>{escape(boundary)}</td></tr></table></section>'
    elif index % 4 == 2:
        body = f'<section class="grid"><div class="card fact"><h2>{escape(labels[1])}</h2><p>{escape(direct)}</p></div><div class="card"><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p></div></section><section class="block"><h2>{escape(labels[3])}</h2><p>{escape(boundary)}</p></section>'
    else:
        body = f'<section class="block"><h2>{escape(labels[1])}</h2><p class="lead">{escape(direct)}</p><h2>{escape(labels[2])}</h2><p>{escape(impact)}</p><h2>{escape(labels[3])}</h2><p>{escape(boundary)}</p></section>'
    related = ""
    if all_items and len(all_items) == len(SLUGS):
        related_cards = []
        for other_index in ((index - 1) % len(SLUGS), (index + 1) % len(SLUGS)):
            other = all_items[other_index]
            related_cards.append(
                f'<a class="card" href="{route(locale, SLUGS[other_index])}"><strong>{escape(other[0])}</strong>'
                f'<br><span class="muted">{escape(other[1])}</span></a>'
            )
        related = f'<section><h2>{escape(labels[4])}</h2><div class="grid">{"".join(related_cards)}</div></section>'
    method = f'<section class="block"><h2>{escape(labels[3])}</h2><p>{escape(NOTE[locale])}</p></section>'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape(desc[:300])}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{hreflang(slug)}<link rel="icon" href="/favicon.ico"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav><a href="/{locale}/">Home</a><a href="/{locale}/questions/">{escape(labels[0])}</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a>{menu(locale, slug)}</nav></div></header><main class="wrap"><section class="hero"><span class="pill">{escape(labels[0])}</span><h1>{escape(title)}</h1><p class="lead">{escape(direct)}</p></section>{body}{method}{related}<section class="block"><h2>{escape(labels[5])}</h2><p><a href="{EA_QA}" rel="nofollow">EA community Q&amp;A</a> · <a href="{EA_BUY}" rel="nofollow">EA purchase page</a> · <a href="{STEAM}" rel="nofollow">Steam</a></p><p class="muted">Verified {TODAY}. Independent community guide; confirmed facts are separated from unannounced details.</p></section></main><footer><div class="wrap"><a href="/{locale}/questions/">{escape(labels[4])}</a> · <a href="/about/sources-and-citations.html">Sources</a></div></footer></body></html>'''


def localized_hub(locale: str, lang: str, items: list) -> str:
    labels = UI[locale]
    cards = "".join(
        f'<a class="card" href="{route(locale, slug)}"><strong>{escape(item[0])}</strong><br><span class="muted">{escape(item[1])}</span></a>'
        for slug, item in zip(SLUGS, items)
    )
    canonical = f"{SITE}/{locale}/questions/"
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(labels[4])} | Star Wars Zero Company Wiki</title><meta name="description" content="{escape(labels[4])}: release, platforms, languages, single-player, co-op, romance, permadeath, action points, Steam Deck and pre-order answers."><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><link rel="icon" href="/favicon.ico"><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">Star Wars Zero Company Wiki</a><nav><a href="/{locale}/">Home</a><a href="/{locale}/confirmed/overview.html">Gameplay</a><a href="/{locale}/official/platforms.html">Platforms</a></nav></div></header><main class="wrap"><section class="hero"><span class="pill">{escape(labels[0])}</span><h1>{escape(labels[4])}</h1><p class="lead">10 verified answers based on EA, the official purchase page and current platform listings.</p></section><section class="grid">{cards}</section></main><footer><div class="wrap">Star Wars Zero Company Wiki · {escape(labels[5])}</div></footer></body></html>'''


def replace_alternates(path: Path, slug: str) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    revised = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*>', "", text, flags=re.I)
    match = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', revised, re.I)
    if not match:
        raise ValueError(f"missing canonical: {path}")
    revised = revised[:match.end()] + hreflang(slug) + revised[match.end():]
    path.write_text(revised, encoding="utf-8")


def inject_hub_links(path: Path, locale: str, items: list) -> None:
    text = path.read_text(encoding="utf-8-sig", errors="ignore")
    marker = "<!-- ROUND13-FAQ-LINKS -->"
    if marker in text:
        return
    labels = UI[locale]
    links = "".join(f'<a class="card" href="{route(locale, slug)}">{escape(item[0])}</a>' for slug, item in zip(SLUGS, items))
    block = f'{marker}<section class="block"><h2>{escape(labels[4])}</h2><div class="grid">{links}</div></section>'
    text = text.replace("</main>", block + "</main>")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    created = 0
    for locale, lang, _ in LOCALES:
        if locale in COPY:
            items = COPY[locale]
            qdir = ROOT / locale / "questions"
            qdir.mkdir(parents=True, exist_ok=True)
            for index, (slug, item) in enumerate(zip(SLUGS, items)):
                (qdir / f"{slug}.html").write_text(localized_page(locale, lang, slug, item, index, items), encoding="utf-8")
                created += 1
            (qdir / "index.html").write_text(localized_hub(locale, lang, items), encoding="utf-8")
            created += 1
        elif locale in EXTRA:
            # Existing German/Japanese pages stay intact; add only missing equivalents.
            source_items = []
            for index, slug in enumerate(SLUGS):
                path = ROOT / locale / "questions" / f"{slug}.html"
                if slug in EXTRA[locale]:
                    item = EXTRA[locale][slug]
                    path.write_text(localized_page(locale, lang, slug, item, index), encoding="utf-8")
                    created += 1
                if path.exists():
                    title = re.search(r"<h1>(.*?)</h1>", path.read_text(encoding="utf-8-sig", errors="ignore"), re.S)
                    source_items.append((title.group(1) if title else slug, ""))
            inject_hub_links(ROOT / locale / "questions" / "index.html", locale, source_items)

    # Every equivalent page receives one exact 11-language hreflang set.
    for slug in SLUGS:
        for locale, _, _ in LOCALES:
            path = ROOT / "questions" / f"{slug}.html" if locale == "en" else ROOT / locale / "questions" / f"{slug}.html"
            if not path.exists():
                raise FileNotFoundError(path)
            replace_alternates(path, slug)
    # These two older English answers were previously noindex when the evidence
    # was weaker. EA's July 21 Q&A and purchase page now support direct answers.
    for slug in ("does-zero-company-have-coop", "should-you-preorder"):
        path = ROOT / "questions" / f"{slug}.html"
        text = path.read_text(encoding="utf-8")
        text = re.sub(
            r'<meta\s+name=["\']robots["\']\s+content=["\']noindex,follow["\']>',
            '<meta name="robots" content="index,follow">', text, count=1, flags=re.I,
        )
        path.write_text(text, encoding="utf-8")
    print(f"Round 13 created {created} localized FAQ pages")


if __name__ == "__main__":
    main()
