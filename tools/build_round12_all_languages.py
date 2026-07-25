#!/usr/bin/env python3
"""Add a five-page core for every previously uncovered official game language."""

from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://starwarszerocompany.cc"
TODAY = date.today().isoformat()
SOURCE_EA = "https://www.ea.com/games/starwars/zero-company/buy"
SOURCE_STEAM = "https://store.steampowered.com/app/2075800/STAR_WARS_Zero_Company/"

ALL_LOCALES = (
    ("en", "en", "English"),
    ("de", "de", "Deutsch"),
    ("fr", "fr", "Français"),
    ("it", "it", "Italiano"),
    ("es", "es", "Español"),
    ("ja", "ja", "日本語"),
    ("ko", "ko", "한국어"),
    ("pl", "pl", "Polski"),
    ("zh-cn", "zh-Hans", "简体中文"),
    ("zh-tw", "zh-Hant", "繁體中文"),
    ("pt-br", "pt-BR", "Português (Brasil)"),
)

CORE_ROUTES = ("", "official/release-date.html", "official/platforms.html",
               "official/languages.html", "confirmed/overview.html")

COPY = {
    "fr": {
        "lang": "fr", "label": "Français", "brand": "Wiki Star Wars Zero Company en français",
        "nav": ("Accueil", "Sortie", "Plateformes", "Langues", "Gameplay"),
        "home": (
            "Star Wars Zero Company Wiki : guide français",
            "Guide français non officiel de Star Wars Zero Company : date de sortie, plateformes, langues, gameplay tactique et limites des informations confirmées.",
            "Le point de départ français pour préparer la sortie sans confondre annonces officielles et spéculation.",
            [
                "Star Wars Zero Company est un jeu tactique au tour par tour en solo situé à la fin de la Guerre des Clones. Electronic Arts annonce une sortie mondiale le 27 août 2026 à 15 h UTC sur PC, PlayStation 5 et Xbox Series X|S. Cette section rassemble les faits utiles déjà vérifiables et renvoie vers une page spécialisée pour chaque intention de recherche.",
                "Le cœur du jeu repose sur une escouade standard de quatre agents, trois points d’action par opérateur, la couverture, le positionnement et l’Avantage. Le quartier général, The Den, permet de développer l’équipe entre les opérations. La mort permanente est activée par défaut mais peut être désactivée : ce choix relève donc des réglages de campagne et non d’un mode séparé.",
                "Cette version française est un guide communautaire, pas un site officiel d’EA. Les valeurs d’armes, arbres de compétences et solutions de missions non publiés ne sont pas inventés. Les pages sont mises à jour à partir des annonces EA, des boutiques officielles et, après la sortie, d’observations reproductibles dans le jeu."
            ]),
        "release": (
            "Date et heure de sortie de Star Wars Zero Company",
            "Star Wars Zero Company sort le 27 août 2026 à 15 h UTC, soit 17 h en France métropolitaine, sur PC, PS5 et Xbox Series X|S.",
            "La sortie mondiale est annoncée pour le jeudi 27 août 2026 à 15 h UTC, ce qui correspond à 17 h en France métropolitaine.",
            [
                "EA affiche une heure de déverrouillage globale précise, et pas seulement une journée de lancement. Pour la France métropolitaine en heure d’été, la conversion donne 17 h CEST le 27 août. Un changement de dernière minute reste possible : la boutique de la plateforme utilisée doit donc être la dernière référence avant le téléchargement.",
                "La date concerne l’édition Standard et l’édition Deluxe. Aucun accès anticipé distinct n’est actuellement annoncé pour l’édition Deluxe. Le bonus de précommande est le pack cosmétique Crystalline Astromech ; il ne constitue pas une version jouable avant le lancement.",
                "Précharger, heure d’ouverture des serveurs et calendrier d’un éventuel patch du premier jour ne sont pas encore détaillés. Le jeu est présenté comme une expérience solo, mais les comptes de plateforme et EA peuvent rester nécessaires selon la boutique et le contenu acheté."
            ]),
        "platforms": (
            "Plateformes de Star Wars Zero Company : PC, PS5 et Xbox",
            "Liste confirmée des plateformes de Star Wars Zero Company : PC, PlayStation 5 et Xbox Series X|S, avec le statut de Switch et Steam Deck.",
            "Les versions confirmées sont PC, PlayStation 5 et Xbox Series X|S. Aucune version Switch n’est annoncée.",
            [
                "Sur PC, les pages officielles proposent EA app, Steam et Epic Games Store. La configuration minimale publiée demande Windows 10 ou 11 en 64 bits, 16 Go de mémoire et 50 Go d’espace. La configuration recommandée vise 32 Go de mémoire et 50 Go d’espace ; il faut vérifier la page boutique avant l’achat car ces exigences peuvent évoluer.",
                "Les consoles prises en charge sont exclusivement PlayStation 5 et Xbox Series X|S dans les annonces actuelles. Les anciennes générations PS4 et Xbox One ne figurent pas dans la liste. EA a également indiqué que Nintendo Switch et la compatibilité Steam Deck ne sont pas confirmées à ce stade.",
                "Cross-play n’est pas un enjeu central puisque le jeu est solo. En revanche, la progression croisée entre boutiques ou familles de consoles n’a pas été annoncée. Il ne faut donc pas supposer qu’une sauvegarde Steam sera utilisable sur PlayStation ou Xbox."
            ]),
        "languages": (
            "Langues de Star Wars Zero Company et doublage français",
            "Star Wars Zero Company prend en charge 11 langues pour l’interface et les sous-titres ; seuls l’anglais et l’allemand ont un doublage complet.",
            "Le français est confirmé pour l’interface et les sous-titres, mais pas pour le doublage intégral.",
            [
                "La liste Steam comporte onze langues : anglais, français, italien, allemand, espagnol d’Espagne, japonais, coréen, polonais, chinois simplifié, chinois traditionnel et portugais du Brésil. EA présente la même liste sur sa page d’achat.",
                "La colonne « audio intégral » n’est cochée que pour l’anglais et l’allemand. Le français dispose de l’interface et des sous-titres. Cela signifie que les menus, objectifs et dialogues écrits seront localisés, tandis que les voix resteront dans l’une des langues audio disponibles.",
                "Cette page distingue volontairement langue du jeu et langue de ce wiki. Le présent guide est une publication communautaire française. Il ne doit pas être interprété comme une traduction officielle, et les noms définitifs des compétences ou missions seront alignés sur le jeu après vérification de la version commerciale."
            ]),
        "gameplay": (
            "Gameplay de Star Wars Zero Company : aperçu confirmé",
            "Aperçu français du gameplay confirmé : escouade de quatre, 3 PA, Avantage, blessures, mort permanente, opérations et base The Den.",
            "Un jeu tactique solo où chaque opérateur dispose de trois points d’action et où la préparation compte autant que le tir.",
            [
                "Une escouade standard comprend quatre agents. À son tour, chaque opérateur possède trois points d’action à répartir entre mouvement, attaques et capacités. La couverture, les lignes de tir, le contournement et les synergies de personnages sont donc plus importants qu’une simple comparaison de dégâts.",
                "L’Avantage peut monter jusqu’à dix points et améliore les chances d’action. Les agents peuvent être blessés et la mort permanente intervient après trois blessures lorsque ce réglage est actif. EA a confirmé que la mort permanente est activée par défaut mais désactivable, ce qui permet d’adapter la pression de la campagne.",
                "Entre les missions, The Den sert de base. L’effectif peut atteindre vingt agents, tandis que les opérations consomment des renseignements et peuvent expirer. Les cartes de mission sont conçues à la main, avec des objectifs et adversaires pouvant varier. Aucun New Game Plus n’est annoncé pour le moment."
            ]),
    },
    "it": {
        "lang": "it", "label": "Italiano", "brand": "Star Wars Zero Company Wiki Italiano",
        "nav": ("Home", "Uscita", "Piattaforme", "Lingue", "Gameplay"),
        "home": (
            "Star Wars Zero Company Wiki: guida italiana",
            "Guida italiana non ufficiale a Star Wars Zero Company con uscita, piattaforme, lingue, sistemi tattici e informazioni confermate.",
            "Il punto di partenza in italiano per seguire il gioco con dati verificati e senza riempitivi speculativi.",
            [
                "Star Wars Zero Company è un gioco tattico a turni per giocatore singolo ambientato negli ultimi anni delle Guerre dei Cloni. Electronic Arts indica il 27 agosto 2026 alle 15:00 UTC come lancio globale su PC, PlayStation 5 e Xbox Series X|S. Questa sezione raccoglie le informazioni ufficiali già disponibili e le separa dalle domande che potranno essere risolte soltanto dopo l’uscita.",
                "Il sistema centrale usa squadre standard di quattro operatori, tre punti azione per personaggio, coperture, fiancheggiamento e Advantage. Tra un’operazione e l’altra si gestisce The Den e una rosa che può arrivare a venti agenti. La morte permanente è attiva per impostazione predefinita, ma EA ha confermato che può essere disattivata.",
                "Questo wiki italiano è una guida indipendente della community e non rappresenta EA o Lucasfilm. Non pubblica statistiche delle armi, alberi abilità o ricompense non confermati. Le pagine vengono corrette quando nuove fonti ufficiali o verifiche riproducibili della versione finale rendono disponibile un dato migliore."
            ]),
        "release": (
            "Data e ora di uscita di Star Wars Zero Company",
            "Star Wars Zero Company esce il 27 agosto 2026 alle 15:00 UTC, cioè alle 17:00 in Italia, su PC, PS5 e Xbox Series X|S.",
            "L’uscita globale è fissata per giovedì 27 agosto 2026 alle 15:00 UTC, equivalenti alle 17:00 CEST in Italia.",
            [
                "La pagina di acquisto EA mostra un orario preciso, non soltanto una data. In Italia la conversione estiva porta alle 17:00 del 27 agosto. Prima di avviare il download conviene comunque controllare il conto alla rovescia dello store scelto, perché orari e disponibilità regionali possono ricevere aggiornamenti.",
                "Standard Edition e Deluxe Edition riportano la stessa data. Al momento non è stato annunciato un accesso anticipato per la Deluxe. Il contenuto di prenotazione è il pacchetto cosmetico Crystalline Astromech e non dà accesso a una demo o a una fase giocabile precedente.",
                "Precaricamento, dimensione finale e orario di un’eventuale patch del day one non sono ancora stati dettagliati. I requisiti PC attuali indicano 50 GB, ma lo spazio necessario al lancio può cambiare con gli aggiornamenti obbligatori."
            ]),
        "platforms": (
            "Piattaforme di Star Wars Zero Company: PC, PS5 e Xbox",
            "Piattaforme confermate per Star Wars Zero Company: PC, PlayStation 5 e Xbox Series X|S; stato di Switch, Steam Deck e vecchie console.",
            "Le piattaforme annunciate sono PC, PlayStation 5 e Xbox Series X|S. Nintendo Switch non è confermata.",
            [
                "Su PC il gioco è venduto tramite EA app, Steam ed Epic Games Store. I requisiti minimi pubblicati includono Windows 10 o 11 a 64 bit, 16 GB di RAM e 50 GB di spazio. La configurazione consigliata sale a 32 GB di RAM; i componenti grafici completi sono elencati nella pagina ufficiale EA.",
                "Su console sono previste versioni native per PlayStation 5 e Xbox Series X|S. PlayStation 4 e Xbox One non compaiono tra le piattaforme supportate. EA ha inoltre dichiarato che Nintendo Switch e Steam Deck non sono ancora confermati, quindi non vanno presentati come versioni in sviluppo.",
                "Essendo un titolo per giocatore singolo, non esiste al momento una necessità confermata di cross-play. Anche il cross-save tra PC, PlayStation e Xbox non è annunciato: acquistare una copia su una piattaforma non garantisce l’uso della stessa campagna altrove."
            ]),
        "languages": (
            "Lingue di Star Wars Zero Company e doppiaggio italiano",
            "Star Wars Zero Company supporta 11 lingue per interfaccia e sottotitoli; l’audio completo è confermato soltanto in inglese e tedesco.",
            "L’italiano è supportato per interfaccia e sottotitoli, ma non risulta un doppiaggio completo in italiano.",
            [
                "Steam elenca undici lingue: inglese, francese, italiano, tedesco, spagnolo di Spagna, giapponese, coreano, polacco, cinese semplificato, cinese tradizionale e portoghese brasiliano. La pagina EA mostra lo stesso insieme di lingue.",
                "Nella tabella dello store la voce audio completo è selezionata soltanto per inglese e tedesco. L’italiano mantiene menu, interfaccia e sottotitoli localizzati. Le voci dei personaggi dovranno quindi essere ascoltate in una delle lingue audio disponibili usando i sottotitoli italiani.",
                "La lingua del gioco non va confusa con quella di questa guida. Il sito è un progetto editoriale non ufficiale; dopo il lancio allineerà nomi di abilità, strutture e missioni alla terminologia effettivamente mostrata nella localizzazione italiana."
            ]),
        "gameplay": (
            "Gameplay di Star Wars Zero Company: sistemi confermati",
            "Guida italiana ai sistemi confermati: squadra da quattro, 3 PA, Advantage, ferite, morte permanente, operazioni e base The Den.",
            "Tattica a turni per giocatore singolo con tre punti azione per operatore e una campagna costruita intorno alle conseguenze.",
            [
                "La squadra standard schiera quattro agenti. Ogni operatore riceve tre punti azione nel proprio turno, spendibili per muoversi, attaccare o usare capacità. Copertura, linee di tiro, fiancheggiamento e sinergie tra compagni determinano quindi l’efficacia di una scelta più del semplice valore di danno.",
                "Advantage può arrivare a dieci punti e influenza la probabilità di successo. Gli agenti subiscono ferite e, con la morte permanente attiva, la terza ferita può eliminarli definitivamente. L’opzione è abilitata per impostazione predefinita ma può essere disattivata nelle impostazioni della campagna.",
                "The Den è la base tra le missioni e la rosa può raggiungere venti agenti. Le operazioni richiedono Intel e alcune possono scadere. Le mappe sono create a mano, mentre obiettivi e nemici possono variare. Al momento EA non ha annunciato New Game Plus."
            ]),
    },
    "es": {
        "lang": "es", "label": "Español", "brand": "Wiki de Star Wars Zero Company en español",
        "nav": ("Inicio", "Lanzamiento", "Plataformas", "Idiomas", "Jugabilidad"),
        "home": (
            "Star Wars Zero Company Wiki: guía en español",
            "Guía no oficial en español de Star Wars Zero Company con fecha, plataformas, idiomas, combate táctico y datos confirmados.",
            "Una puerta de entrada en español basada en fuentes oficiales y diseñada para separar hechos de rumores antes del lanzamiento.",
            [
                "Star Wars Zero Company es un juego táctico por turnos para un jugador ambientado en el tramo final de las Guerras Clon. Electronic Arts fija el lanzamiento mundial para el 27 de agosto de 2026 a las 15:00 UTC en PC, PlayStation 5 y Xbox Series X|S. Este núcleo en español reúne la información que ya puede verificarse y enlaza cada tema con su propia página.",
                "La estructura confirmada utiliza una escuadra estándar de cuatro agentes y tres puntos de acción por operador. Cobertura, flanqueo, Advantage y sinergias de equipo forman el combate. Entre operaciones se gestiona The Den y una plantilla que puede crecer hasta veinte agentes. La muerte permanente viene activada, pero el jugador puede desactivarla.",
                "Esta wiki es una guía comunitaria independiente, no una web oficial de EA. No presenta como reales armas, cifras, árboles de habilidades o recompensas todavía no publicados. Las correcciones se apoyan en noticias oficiales, fichas de tienda y, tras el estreno, pruebas reproducibles dentro del juego."
            ]),
        "release": (
            "Fecha y hora de lanzamiento de Star Wars Zero Company",
            "Star Wars Zero Company se lanza el 27 de agosto de 2026 a las 15:00 UTC, las 17:00 en la España peninsular, para PC, PS5 y Xbox.",
            "La hora mundial anunciada es el jueves 27 de agosto de 2026 a las 15:00 UTC: 17:00 CEST en la España peninsular.",
            [
                "EA muestra una hora de desbloqueo concreta en su página de compra. La conversión para la España peninsular en horario de verano es 17:00 del mismo día; en Canarias corresponde a las 16:00. Conviene usar el contador de la tienda elegida como última comprobación por si existe un ajuste regional.",
                "Las ediciones Standard y Deluxe comparten fecha. No hay acceso anticipado anunciado para Deluxe. El incentivo de reserva es el paquete cosmético Crystalline Astromech, no una prueba jugable ni un permiso para comenzar la campaña antes.",
                "Todavía no se han confirmado la precarga, el tamaño final ni un calendario de parche de lanzamiento. La ficha actual de PC indica 50 GB, pero una actualización obligatoria puede modificar el espacio real necesario."
            ]),
        "platforms": (
            "Plataformas de Star Wars Zero Company: PC, PS5 y Xbox",
            "Plataformas confirmadas de Star Wars Zero Company y estado de Nintendo Switch, Steam Deck, PS4 y Xbox One.",
            "Star Wars Zero Company está confirmado para PC, PlayStation 5 y Xbox Series X|S; Nintendo Switch no está anunciado.",
            [
                "En PC se puede comprar mediante EA app, Steam y Epic Games Store. Los requisitos mínimos publicados incluyen Windows 10 u 11 de 64 bits, 16 GB de memoria y 50 GB de almacenamiento. La configuración recomendada pide 32 GB de memoria y hardware gráfico superior.",
                "Las consolas confirmadas son PlayStation 5 y Xbox Series X|S. No aparecen versiones para PlayStation 4 ni Xbox One. EA también ha dicho que Switch y Steam Deck no están confirmados, por lo que una posible compatibilidad futura debe mantenerse como pregunta abierta.",
                "El juego se presenta como una experiencia para un jugador, así que no se ha anunciado cross-play. Tampoco existe confirmación de guardado cruzado entre tiendas de PC y consolas. Cada compra debe valorarse como una progresión independiente hasta que EA indique lo contrario."
            ]),
        "languages": (
            "Idiomas de Star Wars Zero Company y doblaje español",
            "Star Wars Zero Company admite 11 idiomas de interfaz y subtítulos; el audio completo solo está confirmado en inglés y alemán.",
            "El español de España está confirmado para interfaz y subtítulos, pero no para audio completo.",
            [
                "Steam enumera inglés, francés, italiano, alemán, español de España, japonés, coreano, polaco, chino simplificado, chino tradicional y portugués de Brasil. Son once idiomas, la misma lista que aparece en la página de compra de EA.",
                "Las únicas casillas de audio completo marcadas son inglés y alemán. El español incluye menús, textos de interfaz y subtítulos. Por tanto, no debe describirse como doblaje español aunque el contenido escrito sí estará localizado.",
                "Esta versión del wiki está redactada en español, pero sigue siendo una guía no oficial. Después del lanzamiento se revisarán los nombres finales de habilidades, misiones y edificios con la terminología visible en el juego, evitando traducciones literales que no coincidan con la localización oficial."
            ]),
        "gameplay": (
            "Jugabilidad de Star Wars Zero Company: sistemas confirmados",
            "Resumen en español del combate y campaña: cuatro agentes, 3 PA, Advantage, heridas, muerte permanente, operaciones y The Den.",
            "Táctica por turnos para un jugador donde cada operador dispone de tres puntos de acción y las decisiones tienen consecuencias.",
            [
                "Una escuadra estándar contiene cuatro agentes. Cada operador recibe tres puntos de acción para movimiento, ataques y habilidades. La cobertura, las líneas de visión, el flanqueo y las sinergias entre compañeros convierten el posicionamiento en una parte central de cada turno.",
                "Advantage puede acumularse hasta diez puntos y mejora las probabilidades de una acción. Los agentes pueden resultar heridos y la tercera herida provoca muerte permanente cuando esa opción está activa. EA ha aclarado que viene habilitada por defecto, aunque puede desactivarse.",
                "The Den funciona como base entre misiones y la plantilla puede alcanzar veinte agentes. Las operaciones consumen Intel y algunas caducan. Los mapas están diseñados a mano, con enemigos y objetivos que pueden variar. No hay New Game Plus anunciado por ahora."
            ]),
    },
    "pl": {
        "lang": "pl", "label": "Polski", "brand": "Star Wars Zero Company Wiki po polsku",
        "nav": ("Start", "Premiera", "Platformy", "Języki", "Rozgrywka"),
        "home": (
            "Star Wars Zero Company Wiki — polski poradnik",
            "Nieoficjalny polski poradnik do Star Wars Zero Company: premiera, platformy, języki, walka taktyczna i potwierdzone informacje.",
            "Polski punkt startowy oparty na oficjalnych źródłach, bez wymyślonych statystyk i przedpremierowych domysłów.",
            [
                "Star Wars Zero Company to jednoosobowa gra taktyczna w systemie turowym, której akcja rozgrywa się pod koniec Wojen Klonów. Electronic Arts zapowiada światową premierę na 27 sierpnia 2026 roku o 15:00 UTC na PC, PlayStation 5 oraz Xbox Series X|S. Ta polska sekcja porządkuje informacje, które można już zweryfikować.",
                "Podstawowy oddział składa się z czterech agentów, a każdy operator ma w turze trzy punkty akcji. Znaczenie mają osłony, flankowanie, Advantage i synergie zespołu. Pomiędzy operacjami gracz rozwija bazę The Den i skład liczący docelowo do dwudziestu agentów. Permanentna śmierć jest domyślnie włączona, lecz można ją wyłączyć.",
                "To niezależny poradnik społeczności, a nie oficjalna strona EA ani Lucasfilm. Nie publikujemy niepotwierdzonych nazw broni, wartości obrażeń, drzewek zdolności czy nagród. Po premierze treści będą aktualizowane na podstawie powtarzalnych testów w wydanej wersji gry."
            ]),
        "release": (
            "Data i godzina premiery Star Wars Zero Company",
            "Star Wars Zero Company zadebiutuje 27 sierpnia 2026 o 15:00 UTC, czyli o 17:00 w Polsce, na PC, PS5 i Xbox Series X|S.",
            "Globalny start zaplanowano na czwartek 27 sierpnia 2026 o 15:00 UTC, co oznacza 17:00 czasu CEST w Polsce.",
            [
                "Strona zakupu EA podaje konkretną godzinę odblokowania, a nie tylko dzień premiery. W Polsce podczas czasu letniego będzie to 17:00. Bezpośrednio przed pobraniem warto sprawdzić licznik w wybranym sklepie, ponieważ regionalne godziny mogą zostać skorygowane.",
                "Edycje Standard i Deluxe mają tę samą datę. Nie ogłoszono wcześniejszego dostępu dla wersji Deluxe. Bonus za zamówienie przedpremierowe to kosmetyczny pakiet Crystalline Astromech, który nie daje dostępu do wersji demonstracyjnej ani wcześniejszego rozpoczęcia kampanii.",
                "EA nie podało jeszcze informacji o preloadzie, ostatecznym rozmiarze instalacji ani aktualizacji pierwszego dnia. Obecne wymagania PC wskazują 50 GB miejsca, ale obowiązkowe aktualizacje mogą zwiększyć tę wartość."
            ]),
        "platforms": (
            "Platformy Star Wars Zero Company: PC, PS5 i Xbox",
            "Potwierdzone platformy Star Wars Zero Company oraz status Nintendo Switch, Steam Deck, PS4 i Xbox One.",
            "Gra została potwierdzona na PC, PlayStation 5 i Xbox Series X|S. Wersja na Nintendo Switch nie została zapowiedziana.",
            [
                "Na PC sprzedaż prowadzą EA app, Steam i Epic Games Store. Minimalne wymagania obejmują 64-bitowy Windows 10 lub 11, 16 GB pamięci oraz 50 GB miejsca na dysku. Zalecana konfiguracja podnosi pamięć do 32 GB i wymaga wydajniejszej karty graficznej.",
                "Wśród konsol znajdują się wyłącznie PlayStation 5 i Xbox Series X|S. PlayStation 4 oraz Xbox One nie są wymienione. EA potwierdziło również, że obsługa Nintendo Switch i Steam Deck pozostaje obecnie niepotwierdzona.",
                "To gra jednoosobowa, dlatego nie ogłoszono funkcji cross-play. Nie potwierdzono także przenoszenia zapisów pomiędzy sklepami PC i konsolami. Do czasu oficjalnej informacji należy zakładać osobny zapis dla każdej platformy."
            ]),
        "languages": (
            "Języki Star Wars Zero Company i polski dubbing",
            "Star Wars Zero Company obsługuje 11 języków interfejsu i napisów; pełny dubbing potwierdzono tylko po angielsku i niemiecku.",
            "Polski interfejs i napisy są potwierdzone, ale pełny polski dubbing nie znajduje się na liście.",
            [
                "Steam wymienia jedenaście języków: angielski, francuski, włoski, niemiecki, hiszpański z Hiszpanii, japoński, koreański, polski, chiński uproszczony, chiński tradycyjny oraz portugalski brazylijski. Tę samą listę publikuje EA.",
                "Kolumna pełnego dźwięku jest zaznaczona wyłącznie przy języku angielskim i niemieckim. Polski obejmuje interfejs oraz napisy, więc cele, menu i dialogi tekstowe będą zlokalizowane, lecz głosy pozostaną w dostępnej wersji audio.",
                "Polska wersja tego wiki jest nieoficjalnym opracowaniem. Po premierze nazwy zdolności, misji i obiektów zostaną porównane z terminologią rzeczywiście używaną w polskiej lokalizacji gry."
            ]),
        "gameplay": (
            "Rozgrywka w Star Wars Zero Company — potwierdzone systemy",
            "Polski opis systemów: czteroosobowy oddział, 3 PA, Advantage, rany, permanentna śmierć, operacje i baza The Den.",
            "Turowa taktyka dla jednego gracza, w której operator ma trzy punkty akcji, a przygotowanie oddziału wpływa na konsekwencje kampanii.",
            [
                "Standardowa drużyna liczy czterech agentów. Każdy operator otrzymuje trzy punkty akcji na ruch, ataki i zdolności. Osłona, linia strzału, flankowanie oraz współpraca postaci sprawiają, że pozycja jest ważniejsza niż sama wartość obrażeń.",
                "Advantage może osiągnąć dziesięć punktów i zwiększa szanse powodzenia. Agenci odnoszą rany, a przy włączonej permanentnej śmierci trzecia rana może usunąć postać z kampanii. Ustawienie jest domyślnie aktywne, ale gracz może je wyłączyć.",
                "The Den służy jako baza pomiędzy misjami, a skład może rozrosnąć się do dwudziestu agentów. Operacje zużywają Intel i mogą wygasać. Mapy są projektowane ręcznie, natomiast cele i przeciwnicy mogą się zmieniać. New Game Plus nie został ogłoszony."
            ]),
    },
    "pt-br": {
        "lang": "pt-BR", "label": "Português (Brasil)", "brand": "Wiki de Star Wars Zero Company em português",
        "nav": ("Início", "Lançamento", "Plataformas", "Idiomas", "Jogabilidade"),
        "home": (
            "Star Wars Zero Company Wiki: guia em português",
            "Guia brasileiro não oficial de Star Wars Zero Company com lançamento, plataformas, idiomas, combate tático e dados confirmados.",
            "Um ponto de partida em português do Brasil, fundamentado em fontes oficiais e sem transformar rumores em páginas.",
            [
                "Star Wars Zero Company é um jogo tático em turnos para um jogador, ambientado no fim das Guerras Clônicas. A Electronic Arts informa lançamento mundial em 27 de agosto de 2026, às 15:00 UTC, para PC, PlayStation 5 e Xbox Series X|S. Esta seção reúne o que já pode ser verificado e separa cada intenção de busca em uma página própria.",
                "A estrutura confirmada utiliza um esquadrão padrão de quatro agentes e três pontos de ação por operador. Cobertura, flanqueamento, Advantage e sinergias influenciam o combate. Entre operações, o jogador administra The Den e um elenco que pode chegar a vinte agentes. A morte permanente vem ativada, mas pode ser desligada.",
                "Este wiki é um guia independente da comunidade e não representa a EA ou a Lucasfilm. Números de armas, árvores de habilidades e recompensas ainda não publicados não são inventados. Depois do lançamento, as páginas serão revisadas com testes reproduzíveis na versão comercial."
            ]),
        "release": (
            "Data e horário de lançamento de Star Wars Zero Company",
            "Star Wars Zero Company chega em 27 de agosto de 2026 às 15:00 UTC, meio-dia no horário de Brasília, para PC, PS5 e Xbox.",
            "O lançamento mundial está marcado para quinta-feira, 27 de agosto de 2026, às 15:00 UTC: 12:00 no horário de Brasília.",
            [
                "A página de compra da EA apresenta uma hora global específica. Para São Paulo e Brasília, a conversão é meio-dia de 27 de agosto. O contador da loja escolhida deve ser a última conferência antes do download, pois disponibilidade regional pode receber ajustes.",
                "As edições Standard e Deluxe compartilham a mesma data. Não foi anunciado acesso antecipado para a Deluxe. O bônus de pré-venda é o pacote cosmético Crystalline Astromech e não dá acesso a uma demonstração ou ao início antecipado da campanha.",
                "Pré-carregamento, tamanho final e eventual atualização do primeiro dia ainda não foram detalhados. Os requisitos atuais de PC indicam 50 GB, mas atualizações obrigatórias podem alterar o espaço efetivamente necessário."
            ]),
        "platforms": (
            "Plataformas de Star Wars Zero Company: PC, PS5 e Xbox",
            "Plataformas confirmadas de Star Wars Zero Company e situação de Nintendo Switch, Steam Deck, PS4 e Xbox One.",
            "O jogo está confirmado para PC, PlayStation 5 e Xbox Series X|S. Nintendo Switch não foi anunciado.",
            [
                "No PC, a compra estará disponível no EA app, Steam e Epic Games Store. Os requisitos mínimos publicados incluem Windows 10 ou 11 de 64 bits, 16 GB de memória e 50 GB de armazenamento. A configuração recomendada eleva a memória para 32 GB.",
                "Nos consoles, as versões confirmadas são PlayStation 5 e Xbox Series X|S. PlayStation 4 e Xbox One não aparecem na lista. A EA também informou que Nintendo Switch e Steam Deck continuam sem confirmação, portanto não devem ser tratados como versões em desenvolvimento.",
                "Como a experiência é para um jogador, não há anúncio de cross-play. O salvamento cruzado entre lojas de PC e consoles também não foi confirmado. Até uma declaração oficial, cada plataforma deve ser considerada uma progressão separada."
            ]),
        "languages": (
            "Idiomas de Star Wars Zero Company e dublagem em português",
            "Star Wars Zero Company oferece interface e legendas em 11 idiomas; áudio completo foi confirmado apenas em inglês e alemão.",
            "Português do Brasil está confirmado para interface e legendas, mas não para dublagem completa.",
            [
                "A Steam lista onze idiomas: inglês, francês, italiano, alemão, espanhol da Espanha, japonês, coreano, polonês, chinês simplificado, chinês tradicional e português do Brasil. A página de compra da EA apresenta o mesmo conjunto.",
                "A coluna de áudio completo está marcada somente para inglês e alemão. Em português brasileiro haverá menus, interface e legendas localizados, enquanto as vozes precisarão usar uma das faixas de áudio disponíveis.",
                "A língua do jogo não deve ser confundida com a deste guia. O wiki em português é um projeto comunitário não oficial. Após o lançamento, nomes de habilidades, missões e instalações serão alinhados à terminologia exibida na localização brasileira."
            ]),
        "gameplay": (
            "Jogabilidade de Star Wars Zero Company: sistemas confirmados",
            "Resumo em português dos sistemas: quatro agentes, 3 PA, Advantage, ferimentos, morte permanente, operações e base The Den.",
            "Tática em turnos para um jogador, com três pontos de ação por operador e decisões que deixam consequências na campanha.",
            [
                "Um esquadrão padrão possui quatro agentes. Cada operador recebe três pontos de ação para movimento, ataques e habilidades. Cobertura, linha de tiro, flanqueamento e sinergias entre companheiros tornam o posicionamento mais importante do que uma comparação isolada de dano.",
                "Advantage pode chegar a dez pontos e melhora a chance de sucesso. Agentes sofrem ferimentos e a terceira lesão pode causar morte permanente quando a opção está ativa. A EA confirmou que ela vem ligada por padrão, mas pode ser desativada.",
                "The Den funciona como base entre missões e o elenco pode alcançar vinte agentes. Operações consomem Intel e algumas expiram. Os mapas são feitos manualmente, com objetivos e inimigos que podem variar. New Game Plus não foi anunciado até o momento."
            ]),
    },
    "ko": {
        "lang": "ko", "label": "한국어", "brand": "스타워즈 제로 컴퍼니 한국어 위키",
        "nav": ("홈", "출시", "플랫폼", "언어", "게임플레이"),
        "home": (
            "스타워즈 제로 컴퍼니 위키 — 한국어 가이드",
            "스타워즈 제로 컴퍼니의 출시일, 플랫폼, 언어, 전술 전투와 공식 확인 정보를 정리한 비공식 한국어 가이드입니다.",
            "공식 자료와 추측을 분리해 출시 전에 필요한 핵심 정보를 빠르게 확인할 수 있는 한국어 시작 페이지입니다.",
            [
                "스타워즈 제로 컴퍼니는 클론 전쟁 말기를 배경으로 하는 싱글 플레이 턴제 전술 게임입니다. 일렉트로닉 아츠는 2026년 8월 27일 15:00 UTC에 PC, 플레이스테이션 5, 엑스박스 시리즈 X|S로 전 세계 출시한다고 안내합니다. 한국 시간으로는 8월 28일 00:00입니다.",
                "표준 분대는 네 명의 요원으로 구성되고 각 요원은 자기 차례에 행동 포인트 세 개를 사용합니다. 엄폐, 측면 공격, Advantage, 동료 시너지가 전투의 중심입니다. 작전 사이에는 The Den과 최대 스무 명까지 확장되는 요원 명단을 관리합니다.",
                "영구 사망은 기본 설정으로 켜져 있지만 끌 수 있습니다. 이 한국어 위키는 EA나 Lucasfilm의 공식 사이트가 아닌 독립 커뮤니티 가이드입니다. 공개되지 않은 무기 수치, 스킬 트리, 임무 보상을 만들어 내지 않으며 출시 후 재현 가능한 플레이 검증으로 내용을 갱신합니다."
            ]),
        "release": (
            "스타워즈 제로 컴퍼니 출시일과 한국 시간",
            "스타워즈 제로 컴퍼니는 2026년 8월 27일 15:00 UTC, 한국 시간 8월 28일 00:00에 PC, PS5, Xbox로 출시됩니다.",
            "공식 글로벌 출시 시각은 2026년 8월 27일 목요일 15:00 UTC이며 한국 표준시로는 8월 28일 금요일 00:00입니다.",
            [
                "EA 구매 페이지는 날짜뿐 아니라 정확한 전 세계 잠금 해제 시각을 표시합니다. 한국은 UTC보다 아홉 시간 빠르므로 달력상 다음 날 자정이 됩니다. 실제 다운로드 직전에는 선택한 스토어의 카운트다운을 마지막으로 확인하는 것이 안전합니다.",
                "스탠더드 에디션과 디럭스 에디션의 출시일은 같습니다. 디럭스 구매자용 사전 플레이는 현재 발표되지 않았습니다. 예약 특전 Crystalline Astromech Pack은 꾸미기 아이템이며 데모나 조기 캠페인 이용권이 아닙니다.",
                "사전 다운로드 시각, 최종 설치 용량, 출시일 패치 일정은 아직 상세히 공개되지 않았습니다. 현재 PC 요구 사항은 저장 공간 50GB를 적고 있지만 필수 업데이트에 따라 실제 필요 공간은 달라질 수 있습니다.",
                "한국 스토어의 날짜가 8월 28일로 표시되더라도 글로벌 발표와 충돌하는 것이 아닙니다. UTC 기준 출시는 같은 순간이며 시차 때문에 한국 달력에서 다음 날로 보이는 것입니다. 지역별 별도 조기 출시가 발표된 것은 아닙니다."
            ]),
        "platforms": (
            "스타워즈 제로 컴퍼니 플랫폼 — PC, PS5, Xbox",
            "스타워즈 제로 컴퍼니의 확정 플랫폼과 닌텐도 스위치, 스팀 덱, PS4, Xbox One 지원 상태를 정리합니다.",
            "확정 플랫폼은 PC, 플레이스테이션 5, 엑스박스 시리즈 X|S입니다. 닌텐도 스위치는 발표되지 않았습니다.",
            [
                "PC 버전은 EA app, Steam, Epic Games Store에서 판매됩니다. 공개된 최소 요구 사항은 64비트 Windows 10 또는 11, 메모리 16GB, 저장 공간 50GB입니다. 권장 환경은 메모리 32GB와 더 높은 등급의 그래픽 카드를 요구합니다.",
                "콘솔은 플레이스테이션 5와 엑스박스 시리즈 X|S만 확인되었습니다. 플레이스테이션 4와 엑스박스 원은 공식 플랫폼 목록에 없습니다. EA는 닌텐도 스위치와 스팀 덱도 아직 확정되지 않았다고 답했습니다.",
                "게임은 싱글 플레이 작품이므로 크로스 플레이 기능은 발표되지 않았습니다. PC 스토어와 콘솔 사이의 크로스 세이브도 확인되지 않았습니다. 공식 발표 전에는 플랫폼마다 별도의 진행 데이터가 필요하다고 보는 편이 정확합니다."
            ]),
        "languages": (
            "스타워즈 제로 컴퍼니 지원 언어와 한국어 음성",
            "스타워즈 제로 컴퍼니는 한국어를 포함한 11개 언어의 인터페이스와 자막을 지원하며 전체 음성은 영어와 독일어만 확인됐습니다.",
            "한국어 인터페이스와 자막은 확정됐지만 한국어 전체 음성 더빙은 공식 목록에 없습니다.",
            [
                "Steam은 영어, 프랑스어, 이탈리아어, 독일어, 스페인 스페인어, 일본어, 한국어, 폴란드어, 중국어 간체, 중국어 번체, 포르투갈 브라질어까지 모두 열한 개 언어를 표시합니다. EA 구매 페이지도 같은 목록을 제공합니다.",
                "전체 음성 항목에 체크된 언어는 영어와 독일어뿐입니다. 한국어는 인터페이스와 자막이 지원되므로 메뉴, 목표, 텍스트 대화는 현지화되지만 캐릭터 음성은 제공되는 오디오 트랙 중 하나를 사용해야 합니다.",
                "게임의 공식 한국어 지원과 이 위키의 성격은 구분해야 합니다. 이 사이트는 비공식 커뮤니티 가이드이며 출시 후 실제 한국어 버전에 표시되는 스킬, 임무, 시설 명칭을 확인해 용어를 수정할 예정입니다.",
                "인터페이스 지원은 메뉴와 사용자 화면의 번역을 뜻하고 자막 지원은 대화와 영상의 텍스트 표시를 뜻합니다. 전체 음성 지원은 별도의 항목이므로 한국어 텍스트 지원을 한국어 더빙으로 해석하면 안 됩니다."
            ]),
        "gameplay": (
            "스타워즈 제로 컴퍼니 게임플레이 — 확정 시스템",
            "4인 분대, 행동 포인트 3개, Advantage, 부상과 영구 사망, 작전, The Den을 다루는 한국어 게임플레이 안내입니다.",
            "각 요원이 행동 포인트 세 개를 사용하는 싱글 플레이 턴제 전술 게임이며 캠페인 선택에는 지속적인 결과가 남습니다.",
            [
                "표준 분대에는 네 명의 요원이 배치됩니다. 각 요원은 자신의 턴에 이동, 공격, 능력 사용을 위해 행동 포인트 세 개를 소비합니다. 엄폐, 사선, 측면 공격, 동료 시너지가 단순한 피해 수치보다 중요한 판단 요소입니다.",
                "Advantage는 최대 열 점까지 쌓이며 행동 성공 가능성에 영향을 줍니다. 요원은 부상을 입고 영구 사망 설정이 켜진 경우 세 번째 부상 뒤 캠페인에서 사라질 수 있습니다. 이 설정은 기본으로 활성화되지만 플레이어가 끌 수 있습니다.",
                "The Den은 임무 사이에 사용하는 기지이며 전체 명단은 최대 스무 명까지 늘어납니다. 작전은 Intel을 소비하고 일부 기회는 만료됩니다. 임무 지도는 수작업으로 설계되지만 목표와 적 구성은 달라질 수 있습니다. New Game Plus는 발표되지 않았습니다."
            ]),
    },
    "zh-cn": {
        "lang": "zh-Hans", "label": "简体中文", "brand": "星球大战：零号连队中文维基",
        "nav": ("首页", "发售", "平台", "语言", "玩法"),
        "home": (
            "《星球大战：零号连队》中文维基与攻略",
            "《星球大战：零号连队》非官方简体中文攻略，汇总发售时间、平台、语言、战术玩法和官方确认信息。",
            "面向中文玩家的首批核心页面，只整理可以由 EA 与官方商店核实的资料，并明确区分事实与发售前推测。",
            [
                "《星球大战：零号连队》是一款以克隆人战争末期为背景的单人回合制战术游戏。EA 公布的全球发售时间为 2026 年 8 月 27 日 15:00 UTC，对应北京时间 8 月 27 日 23:00，平台包括 PC、PlayStation 5 和 Xbox Series X|S。",
                "标准任务小队由四名成员组成，每名干员在自己的回合拥有三个行动点。掩体、侧翼、Advantage 优势值与队友协同构成战斗核心。任务之间可以经营基地 The Den，并把总部成员扩展到最多二十人。永久死亡默认开启，但官方确认玩家可以关闭。",
                "本站是玩家制作的非官方中文指南，并非 EA 或 Lucasfilm 的官方网站。尚未公开的武器数值、技能树、任务奖励与演示版日期不会被编造成可索引页面。游戏发售后，页面将依据正式版本中的简体中文术语和可重复验证的实测结果更新。"
            ]),
        "release": (
            "《星球大战：零号连队》发售日期与北京时间",
            "《星球大战：零号连队》将于 2026 年 8 月 27 日 15:00 UTC 发售，对应北京时间当日 23:00。",
            "官方全球解锁时间为 2026 年 8 月 27 日星期四 15:00 UTC，即北京时间 8 月 27 日 23:00。",
            [
                "EA 购买页面给出了精确到小时的全球时间，而不是只提供发售日期。中国大陆采用 UTC+8，因此无需跨到次日。实际下载前仍建议查看所购买商店的倒计时，因为区域上架时间或最后调整应以平台页面为准。",
                "标准版与豪华版当前显示相同的发售时间，没有公布豪华版提前游玩。预购奖励 Crystalline Astromech Pack 是机器人外观内容，不是公开 Demo，也不提供提前进入战役的资格。",
                "预载开始时间、最终安装容量与首日补丁安排尚未公布。当前 PC 配置页面写明需要 50GB 存储空间，但强制更新可能改变实际容量。任何未经官方确认的提前解锁传闻都不会在本站写成确定结论。"
            ]),
        "platforms": (
            "《星球大战：零号连队》平台：PC、PS5 与 Xbox",
            "盘点《星球大战：零号连队》已确认平台，以及 Switch、Steam Deck、PS4 和 Xbox One 的当前状态。",
            "已确认平台为 PC、PlayStation 5 与 Xbox Series X|S；目前没有公布 Nintendo Switch 版本。",
            [
                "PC 版可通过 EA app、Steam 与 Epic Games Store 购买。官方最低配置包括 64 位 Windows 10 或 11、16GB 内存与 50GB 存储空间；推荐配置为 32GB 内存并搭配更高性能显卡。购买前应再次查看商店，因为配置仍可能更新。",
                "主机版本仅确认 PlayStation 5 和 Xbox Series X|S。PlayStation 4 与 Xbox One 不在官方平台列表中。EA 在社区问答中还明确表示 Nintendo Switch 与 Steam Deck 兼容性尚未确认，因此不能写成正在开发。",
                "本作定位为单人游戏，目前没有跨平台联机需求，也没有公布 PC 与主机之间的跨平台存档。除非 EA 后续确认，否则应把不同平台的购买与战役进度视为相互独立。"
            ]),
        "languages": (
            "《星球大战：零号连队》支持语言与中文配音",
            "游戏支持 11 种界面与字幕语言，包括简体中文和繁体中文；完整配音目前只有英语与德语。",
            "简体中文界面和字幕已经确认，但官方列表没有中文完整配音。",
            [
                "Steam 列出的十一种语言为英语、法语、意大利语、德语、西班牙语（西班牙）、日语、韩语、波兰语、简体中文、繁体中文与葡萄牙语（巴西）。EA 购买页显示相同语言范围。",
                "完整音频一栏只有英语与德语被勾选。简体中文支持界面和字幕，因此菜单、任务目标和文字对白会本地化，但角色语音需要使用已提供的音轨。这里需要避免把“有中文字幕”误写成“有中文配音”。",
                "游戏官方中文支持与本站中文页面也不是同一概念。本站是非官方玩家指南。发售后会用正式简体中文版核对技能、任务、设施与专有名词，避免沿用与官方本地化不一致的直译名称。"
            ]),
        "gameplay": (
            "《星球大战：零号连队》玩法与已确认系统",
            "中文玩法总览：四人小队、每人 3 行动点、Advantage、受伤与永久死亡、行动任务和 The Den 基地。",
            "这是一款单人回合制战术游戏，每名干员拥有三个行动点，队伍建设与战场选择都会影响战役结果。",
            [
                "标准出战队伍包含四名成员。每名干员在自己的回合用三个行动点完成移动、攻击或能力操作。掩体、射线、侧翼位置与角色协同会直接改变行动效率，因此不能只依据尚未公布的伤害数字判断强弱。",
                "Advantage 优势值最高可积累到十点，并影响行动成功概率。角色可能受伤；当永久死亡选项开启时，第三次受伤可能使角色永久离队。官方说明这一选项默认开启，但玩家能够在战役设置中关闭。",
                "The Den 是任务间使用的总部，成员上限可达到二十人。Operation 行动任务会消耗 Intel 情报，部分机会可能过期。地图由开发团队手工设计，但目标与敌人组合可以变化。目前没有公布 New Game Plus。"
            ]),
    },
    "zh-tw": {
        "lang": "zh-Hant", "label": "繁體中文", "brand": "星際大戰：零號連隊繁中維基",
        "nav": ("首頁", "發售", "平台", "語言", "玩法"),
        "home": (
            "《星際大戰：零號連隊》繁體中文維基",
            "《星際大戰：零號連隊》非官方繁中攻略，整理發售時間、平台、語言、戰術玩法與官方確認資料。",
            "為繁體中文玩家建立的核心入口，只採用 EA 與官方商店可核實的資訊，不把上市前猜測包裝成攻略。",
            [
                "《星際大戰：零號連隊》是以複製人戰爭末期為背景的單人回合制戰術遊戲。EA 公布的全球發售時間為 2026 年 8 月 27 日 15:00 UTC，換算台港時間為當日 23:00，平台包括 PC、PlayStation 5 與 Xbox Series X|S。",
                "標準任務小隊由四名成員組成，每名幹員在自己的回合擁有三個行動點。掩體、側翼、Advantage 優勢值與隊友協同是戰鬥核心。任務之間可以經營基地 The Den，並把總部名單擴充至最多二十名幹員。永久死亡預設開啟，但可以關閉。",
                "本站是玩家製作的非官方繁中指南，並非 EA 或 Lucasfilm 官方網站。尚未公布的武器數值、技能樹、任務獎勵與 Demo 日期不會被虛構。遊戲發售後，頁面會依正式繁體中文版用語與可重複驗證的實測更新。"
            ]),
        "release": (
            "《星際大戰：零號連隊》發售日期與台港時間",
            "《星際大戰：零號連隊》將於 2026 年 8 月 27 日 15:00 UTC 發售，台灣與香港時間為當日 23:00。",
            "官方全球解鎖時間是 2026 年 8 月 27 日星期四 15:00 UTC，即台港時間 8 月 27 日 23:00。",
            [
                "EA 購買頁提供精確的全球解鎖時刻，而不只是日期。台灣與香港使用 UTC+8，因此換算後不會跨日。實際下載前仍應查看所選商店的倒數計時，因為區域上架或最後調整要以平台頁面為準。",
                "標準版與豪華版目前顯示相同發售時間，沒有公布豪華版搶先遊玩。預購獎勵 Crystalline Astromech Pack 是機器人造型內容，不是公開試玩版，也不提供提前開始戰役的資格。",
                "預載時間、最終安裝容量與首日更新安排仍未公開。目前 PC 規格頁標示需要 50GB 儲存空間，但強制更新可能改變實際容量。未經官方確認的提前解鎖消息不應視為事實。"
            ]),
        "platforms": (
            "《星際大戰：零號連隊》平台：PC、PS5 與 Xbox",
            "整理《星際大戰：零號連隊》已確認平台，以及 Switch、Steam Deck、PS4、Xbox One 的目前狀態。",
            "已確認平台是 PC、PlayStation 5 與 Xbox Series X|S；目前未公布 Nintendo Switch 版本。",
            [
                "PC 版可在 EA app、Steam 與 Epic Games Store 購買。官方最低需求包含 64 位元 Windows 10 或 11、16GB 記憶體與 50GB 儲存空間；建議需求提高至 32GB 記憶體並搭配更高階顯示卡。",
                "主機版本只確認 PlayStation 5 與 Xbox Series X|S。PlayStation 4 和 Xbox One 不在官方清單。EA 也在社群問答表示 Nintendo Switch 與 Steam Deck 尚未確認，因此不能把它們描述成開發中的版本。",
                "本作是單人遊戲，目前沒有跨平台連線功能的公告，也沒有確認 PC 與主機之間可共用存檔。除非 EA 後續公布，購買時應把每個平台的戰役進度視為獨立。"
            ]),
        "languages": (
            "《星際大戰：零號連隊》支援語言與中文配音",
            "遊戲支援 11 種介面與字幕語言，包括繁體中文與簡體中文；完整配音目前只有英語與德語。",
            "繁體中文介面與字幕已確認，但官方清單沒有中文完整配音。",
            [
                "Steam 列出的十一種語言為英語、法語、義大利語、德語、西班牙語（西班牙）、日語、韓語、波蘭語、簡體中文、繁體中文與葡萄牙語（巴西）。EA 購買頁顯示相同範圍。",
                "完整音訊欄只有英語與德語勾選。繁體中文支援介面與字幕，因此選單、任務目標與文字對話會本地化，但角色語音需使用現有音軌。不能把「有中文字幕」誤寫成「有中文配音」。",
                "遊戲的官方繁中支援與本站繁中頁面也需要區分。本站是非官方玩家指南。上市後會用正式繁中版本核對技能、任務、設施與專有名詞，避免採用和官方在地化不同的直譯。"
            ]),
        "gameplay": (
            "《星際大戰：零號連隊》玩法與確認系統",
            "繁中玩法總覽：四人小隊、每人 3 行動點、Advantage、受傷與永久死亡、行動任務和 The Den 基地。",
            "這是單人回合制戰術遊戲，每名幹員有三個行動點，隊伍培養與戰場選擇會留下戰役後果。",
            [
                "標準出戰隊伍包含四名成員。每名幹員在自己的回合使用三個行動點完成移動、攻擊或能力。掩體、射線、側翼位置與角色協同會直接影響效率，因此不能只用尚未公開的傷害數字判斷強弱。",
                "Advantage 優勢值最高可累積至十點，並影響行動成功機率。角色可能受傷；永久死亡開啟時，第三次受傷可能使角色永久離隊。官方說明此選項預設開啟，但玩家可以在戰役設定關閉。",
                "The Den 是任務之間使用的總部，名單上限可達二十人。Operation 行動會消耗 Intel 情報，部分機會可能過期。地圖由開發團隊手工設計，但目標與敵人組合可以變化。目前未公布 New Game Plus。"
            ]),
    },
}

STYLE = """:root{--bg:#071016;--panel:#0d1922;--line:#284050;--text:#edf7ff;--muted:#a9bac5;--teal:#36e0ce;--gold:#e9b84a;--max:1080px}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:16px/1.72 system-ui,-apple-system,'Segoe UI',sans-serif}a{color:var(--teal);text-decoration:none}a:hover{text-decoration:underline}.wrap{max-width:var(--max);margin:auto;padding:0 22px}.top{border-bottom:1px solid var(--line);background:#071016f2;position:sticky;top:0;z-index:5}.top .wrap{min-height:64px;display:flex;align-items:center;gap:16px;flex-wrap:wrap}.brand{font-weight:900;color:var(--text)}nav{margin-left:auto;display:flex;gap:14px;align-items:center;flex-wrap:wrap}nav>a{color:var(--muted);font-size:14px}.hero{padding:52px 0 28px;border-bottom:1px solid var(--line)}h1{font-size:clamp(34px,6vw,56px);line-height:1.1;margin:12px 0}h2{font-size:23px;margin:34px 0 13px;border-left:4px solid var(--teal);padding-left:12px}.lead{font-size:19px;color:#c9d8e0;max-width:880px}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:15px}.card,.block{display:block;border:1px solid var(--line);border-radius:8px;background:var(--panel);padding:20px;margin:15px 0;color:var(--text)}.pill{display:inline-block;border:1px solid #3c625f;padding:5px 9px;color:var(--teal);font-size:12px}.muted,.source{color:var(--muted);font-size:14px}table{width:100%;border-collapse:collapse;margin:18px 0}th,td{border:1px solid var(--line);padding:10px;text-align:left}th{color:var(--gold)}footer{border-top:1px solid var(--line);margin-top:48px;padding:28px 0;color:var(--muted);font-size:14px}@media(max-width:760px){nav{margin-left:0}.top .wrap{padding:10px 22px}}"""


def route_url(locale: str, route: str) -> str:
    prefix = "" if locale == "en" else f"/{locale}"
    if not route:
        return f"{SITE}{prefix}/"
    if route.endswith("index.html"):
        route = route[:-10]
    return f"{SITE}{prefix}/{route}"


def alternates(route: str) -> str:
    links = []
    for directory, tag, _ in ALL_LOCALES:
        links.append(f'<link rel="alternate" hreflang="{tag}" href="{route_url(directory, route)}">')
    links.append(f'<link rel="alternate" hreflang="x-default" href="{route_url("en", route)}">')
    return "".join(links)


def json_ld(title: str, desc: str, url: str, lang: str) -> str:
    data = {"@context": "https://schema.org", "@type": "WebPage", "headline": title,
            "description": desc, "url": url, "inLanguage": lang,
            "dateModified": TODAY,
            "isPartOf": {"@type": "WebSite", "name": "Star Wars Zero Company Wiki", "url": SITE + "/"}}
    return json.dumps(data, ensure_ascii=False)


def nav(locale: str, data: dict) -> str:
    labels = data["nav"]
    hrefs = (f"/{locale}/", f"/{locale}/official/release-date.html",
             f"/{locale}/official/platforms.html", f"/{locale}/official/languages.html",
             f"/{locale}/confirmed/overview.html")
    return "".join(f'<a href="{href}">{escape(label)}</a>' for href, label in zip(hrefs, labels))


def body_for(locale: str, topic: str, data: dict) -> str:
    title, _, lead, paragraphs = data[topic]
    paras = "".join(f"<p>{escape(p)}</p>" for p in paragraphs)
    if topic == "home":
        cards = "".join(
            f'<a class="card" href="/{locale}/{route}"><strong>{escape(data[key][0])}</strong>'
            f'<br><span class="muted">{escape(data[key][2])}</span></a>'
            for key, route in (("release", "official/release-date.html"),
                               ("platforms", "official/platforms.html"),
                               ("languages", "official/languages.html"),
                               ("gameplay", "confirmed/overview.html")))
        return f'<section class="block"><h2>{escape(labels_for(locale)[0])}</h2>{paras}</section><section><h2>{escape(labels_for(locale)[1])}</h2><div class="grid">{cards}</div></section>'
    if topic == "release":
        return f'<section class="block"><h2>{escape(labels_for(locale)[2])}</h2>{paras}</section><section><h2>UTC</h2><table><tr><th>UTC</th><th>{escape(data["label"])}</th></tr><tr><td>2026-08-27 15:00</td><td>{escape(local_time(locale))}</td></tr></table></section>'
    if topic == "platforms":
        rows = (("PC", "EA app · Steam · Epic Games Store"), ("PlayStation", "PlayStation 5"),
                ("Xbox", "Xbox Series X|S"), ("Nintendo Switch / Steam Deck", status_unknown(locale)))
        table = "".join(f"<tr><td>{escape(a)}</td><td>{escape(b)}</td></tr>" for a, b in rows)
        return f'<section class="block"><h2>{escape(labels_for(locale)[3])}</h2>{paras}</section><section><table><tr><th>Platform</th><th>Status</th></tr>{table}</table></section>'
    if topic == "languages":
        names = " · ".join(label for _, _, label in ALL_LOCALES)
        return f'<section class="block"><h2>11</h2>{paras}</section><section><h2>{escape(labels_for(locale)[4])}</h2><p>{escape(names)}</p><p class="muted">Full audio: English · Deutsch</p></section>'
    cards = "".join(f'<div class="card"><strong>{escape(a)}</strong><br><span class="muted">{escape(b)}</span></div>'
                    for a, b in gameplay_facts(locale))
    return f'<section class="block"><h2>{escape(labels_for(locale)[5])}</h2>{paras}</section><section><h2>{escape(labels_for(locale)[6])}</h2><div class="grid">{cards}</div></section>'


def labels_for(locale: str):
    labels = {
        "fr": ("Ce que couvre ce guide", "Guides essentiels", "Heure officielle", "Compatibilité confirmée", "Liste officielle", "Fonctionnement de la campagne", "Repères tactiques"),
        "it": ("Cosa contiene questa guida", "Guide essenziali", "Orario ufficiale", "Compatibilità confermata", "Elenco ufficiale", "Come funziona la campagna", "Riferimenti tattici"),
        "es": ("Qué cubre esta guía", "Guías esenciales", "Hora oficial", "Compatibilidad confirmada", "Lista oficial", "Cómo funciona la campaña", "Claves tácticas"),
        "pl": ("Zakres poradnika", "Najważniejsze poradniki", "Oficjalna godzina", "Potwierdzona zgodność", "Oficjalna lista", "Przebieg kampanii", "Podstawy taktyczne"),
        "pt-br": ("O que este guia cobre", "Guias essenciais", "Horário oficial", "Compatibilidade confirmada", "Lista oficial", "Como funciona a campanha", "Referências táticas"),
        "ko": ("가이드 범위", "핵심 가이드", "공식 시각", "확정 지원", "공식 목록", "캠페인 구조", "전술 핵심"),
        "zh-cn": ("本指南覆盖范围", "核心指南", "官方时间", "已确认兼容性", "官方语言列表", "战役如何运作", "战术要点"),
        "zh-tw": ("本指南涵蓋範圍", "核心指南", "官方時間", "已確認相容性", "官方語言清單", "戰役如何運作", "戰術重點"),
    }
    return labels[locale]


def local_time(locale: str) -> str:
    return {
        "fr": "27 août 2026, 17:00 CEST", "it": "27 agosto 2026, 17:00 CEST",
        "es": "27 agosto 2026, 17:00 CEST", "pl": "27 sierpnia 2026, 17:00 CEST",
        "pt-br": "27 de agosto de 2026, 12:00 BRT", "ko": "2026년 8월 28일 00:00 KST",
        "zh-cn": "2026年8月27日 23:00（北京时间）", "zh-tw": "2026年8月27日 23:00（台港時間）",
    }[locale]


def status_unknown(locale: str) -> str:
    return {
        "fr": "Non confirmé", "it": "Non confermato", "es": "No confirmado",
        "pl": "Niepotwierdzone", "pt-br": "Não confirmado", "ko": "미확정",
        "zh-cn": "尚未确认", "zh-tw": "尚未確認",
    }[locale]


def gameplay_facts(locale: str):
    values = {
        "fr": (("Escouade", "4 agents"), ("Actions", "3 PA par opérateur"), ("Avantage", "Maximum 10"), ("Effectif", "Maximum 20 agents")),
        "it": (("Squadra", "4 agenti"), ("Azioni", "3 PA per operatore"), ("Advantage", "Massimo 10"), ("Rosa", "Massimo 20 agenti")),
        "es": (("Escuadra", "4 agentes"), ("Acciones", "3 PA por operador"), ("Advantage", "Máximo 10"), ("Plantilla", "Máximo 20 agentes")),
        "pl": (("Oddział", "4 agentów"), ("Akcje", "3 PA na operatora"), ("Advantage", "Maksymalnie 10"), ("Skład", "Maksymalnie 20 agentów")),
        "pt-br": (("Esquadrão", "4 agentes"), ("Ações", "3 PA por operador"), ("Advantage", "Máximo 10"), ("Elenco", "Máximo 20 agentes")),
        "ko": (("분대", "요원 4명"), ("행동", "요원당 3 AP"), ("Advantage", "최대 10"), ("명단", "최대 요원 20명")),
        "zh-cn": (("出战小队", "4名成员"), ("行动", "每名干员3 AP"), ("Advantage", "最高10点"), ("总部名册", "最多20名干员")),
        "zh-tw": (("出戰小隊", "4名成員"), ("行動", "每名幹員3 AP"), ("Advantage", "最高10點"), ("總部名單", "最多20名幹員")),
    }
    return values[locale]


def render(locale: str, route: str, topic: str, data: dict) -> str:
    title, desc, lead, _ = data[topic]
    canonical = route_url(locale, route)
    content = body_for(locale, topic, data)
    source_label = {"fr": "Sources officielles", "it": "Fonti ufficiali", "es": "Fuentes oficiales",
                    "pl": "Oficjalne źródła", "pt-br": "Fontes oficiais", "ko": "공식 출처",
                    "zh-cn": "官方来源", "zh-tw": "官方來源"}[locale]
    return f'''<!doctype html><html lang="{data["lang"]}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">{alternates(route)}<link rel="icon" href="/favicon.ico"><script type="application/ld+json">{json_ld(title, desc, canonical, data["lang"])}</script><style>{STYLE}</style><meta name="google-adsense-account" content="ca-pub-9505220977121599"><script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-9505220977121599" crossorigin="anonymous"></script></head><body><header class="top"><div class="wrap"><a class="brand" href="/{locale}/">{escape(data["brand"])}</a><nav>{nav(locale, data)}</nav></div></header><main class="wrap"><section class="hero"><span class="pill">{escape(data["label"])}</span><h1>{escape(title)}</h1><p class="lead">{escape(lead)}</p></section>{content}<section class="block"><h2>{escape(source_label)}</h2><p class="source"><a href="{SOURCE_EA}" rel="nofollow">Electronic Arts</a> · <a href="{SOURCE_STEAM}" rel="nofollow">Steam</a></p><p class="muted">Verified {TODAY}. Unofficial community guide.</p></section></main><footer><div class="wrap"><a href="/{locale}/">{escape(data["brand"])}</a> · <a href="/about/sources-and-citations.html">Sources</a></div></footer></body></html>'''


def update_existing_alternates() -> int:
    changed = 0
    for locale in ("en", "de", "ja"):
        for route in CORE_ROUTES:
            relative = Path(route or "index.html")
            path = ROOT / relative if locale == "en" else ROOT / locale / relative
            if not path.exists():
                raise FileNotFoundError(path)
            text = path.read_text(encoding="utf-8-sig")
            revised = re.sub(r'<link\s+rel=["\']alternate["\'][^>]*>', "", text, flags=re.I)
            canonical_match = re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', revised, re.I)
            if not canonical_match:
                raise ValueError(f"Missing canonical: {path}")
            revised = revised[:canonical_match.end()] + alternates(route) + revised[canonical_match.end():]
            if revised != text:
                path.write_text(revised, encoding="utf-8")
                changed += 1
    return changed


def main():
    created = 0
    mapping = {"": "home", "official/release-date.html": "release",
               "official/platforms.html": "platforms", "official/languages.html": "languages",
               "confirmed/overview.html": "gameplay"}
    for locale, data in COPY.items():
        for route, topic in mapping.items():
            path = ROOT / locale / (route or "index.html")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(render(locale, route, topic, data), encoding="utf-8")
            created += 1
    updated = update_existing_alternates()
    print(f"Created {created} localized core pages; updated {updated} existing counterparts")


if __name__ == "__main__":
    main()
