#!/usr/bin/env python3
"""Round 23: complete official cast parity for eight under-covered locales."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "tools" / "build_round22_locale_parity.py"
spec = importlib.util.spec_from_file_location("round22", BASE_PATH)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)

CAST = {
    "hawks-masculine-jonathan-freeman": ("Hawks (Masculine)", "Jonathan Freeman"),
    "hawks-feminine-erica-luttrell": ("Hawks (Feminine)", "Erica Luttrell"),
    "runa-blask-vic-michaelis": ("Runa Blask", "Vic Michaelis"),
    "kabb-uppercut-jb-blanc": ("Kabb Uppercut", "JB Blanc"),
    "jae-mordant-judy-alice-lee": ("Jae Mordant", "Judy Alice Lee"),
    "bennic-halloren-leo-howard": ("Bennic Halloren", "Leo Howard"),
    "visser-dylan-kenin": ("Visser", "Dylan Kenin"),
    "tel-rea-nicole-rainteau": ("Tel-Rea", "Nicole Rainteau"),
    "neesh-renark-jim-pirri": ("Neesh Renark", "Jim Pirri"),
    "m3vo-meevo-dc-douglas": ("M-3VO / Meevo", "D.C. Douglas"),
    "typhon-hunter-smith": ("Typhon", "Hunter Smith"),
}

CONTEXT = {
    "es": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman interpreta la presentación masculina de Hawks, el antiguo oficial de la República que vuelve a liderar un equipo independiente contra Infinite Coil. Hawks ocupa el papel central en las misiones de historia.",
        "hawks-feminine-erica-luttrell": "Erica Luttrell interpreta la opción de voz femenina del protagonista creado por el jugador. Este crédito no presenta una segunda Operadora: ambas voces pertenecen al mismo Hawks personalizable.",
        "runa-blask-vic-michaelis": "Runa gestiona las tareas menos visibles de la compañía desde The Den y trabaja con Zero Company por necesidad, aunque procede del bando separatista.",
        "kabb-uppercut-jb-blanc": "Kabb es un exboxeador y veterano criminal Felshi con un brazo cibernético. EA lo presenta como un Operador de autor de Zero Company.",
        "jae-mordant-judy-alice-lee": "Jae, de la Casa Mordant, fue Baronesa del Mineral en Luunata antes de que Infinite Coil tomara el planeta; ayudó a que la República contratara a Zero Company.",
        "bennic-halloren-leo-howard": "La fuente confirma a Bennic Halloren y a su intérprete, pero no publica todavía su facción, jugabilidad ni condición de Operador desplegable.",
        "visser-dylan-kenin": "La fuente confirma a Visser y a su intérprete, pero no detalla todavía su facción, función narrativa ni estado jugable.",
        "tel-rea-nicole-rainteau": "Tel-Rea es una Padawan Jedi Tognath que se une a Zero Company para honrar el legado de su Maestro Jedi fallecido.",
        "neesh-renark-jim-pirri": "La fuente confirma a Neesh Renark y a su intérprete; no permite deducir habilidades, equipo ni si participa directamente en misiones tácticas.",
        "m3vo-meevo-dc-douglas": "M-3VO, también llamado Meevo, es un personaje droide. El crédito oficial no confirma por sí solo que sea una unidad de combate reclutable.",
        "typhon-hunter-smith": "La fuente confirma el nombre Typhon y su intérprete, pero aún no identifica oficialmente su alianza o función de juego.",
    },
    "fr": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman interprète la présentation masculine de Hawks, l’ancien officier de la République qui reprend la tête d’une équipe indépendante contre l’Infinite Coil. Hawks reste au centre des missions principales.",
        "hawks-feminine-erica-luttrell": "Erica Luttrell interprète la voix féminine du protagoniste créé par le joueur. Ce crédit n’annonce pas une seconde Operator: les deux voix correspondent au même Hawks personnalisable.",
        "runa-blask-vic-michaelis": "Runa gère les tâches peu glorieuses de la compagnie depuis The Den et travaille avec Zero Company par nécessité, malgré ses origines séparatistes.",
        "kabb-uppercut-jb-blanc": "Kabb est un ancien boxeur et escroc Felshi doté d’un bras cybernétique. EA le présente comme un Operator écrit de Zero Company.",
        "jae-mordant-judy-alice-lee": "Issue de la Maison Mordant, Jae régnait sur Luunata comme Baronne du minerai avant la prise de la planète par l’Infinite Coil; elle a aidé la République à engager Zero Company.",
        "bennic-halloren-leo-howard": "La source confirme Bennic Halloren et son interprète, mais ne publie pas encore sa faction, son rôle de jeu ni un statut d’Operator déployable.",
        "visser-dylan-kenin": "La source confirme Visser et son interprète, mais ne détaille pas encore sa faction, sa fonction narrative ou son statut jouable.",
        "tel-rea-nicole-rainteau": "Tel-Rea est une Padawan Jedi Tognath qui rejoint Zero Company afin d’honorer l’héritage de son défunt Maître Jedi.",
        "neesh-renark-jim-pirri": "La source confirme Neesh Renark et son interprète; elle ne permet pas d’en déduire compétences, équipement ou présence en mission tactique.",
        "m3vo-meevo-dc-douglas": "M-3VO, aussi appelé Meevo, est un personnage droïde. Le crédit officiel ne confirme pas à lui seul une unité de combat recrutable.",
        "typhon-hunter-smith": "La source confirme le nom Typhon et son interprète, sans identifier officiellement son camp ou sa fonction de jeu.",
    },
    "it": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman interpreta la versione maschile di Hawks, l’ex ufficiale della Repubblica che torna a guidare una squadra indipendente contro Infinite Coil. Hawks è centrale nelle missioni della storia.",
        "hawks-feminine-erica-luttrell": "Erica Luttrell interpreta la voce femminile del protagonista creato dal giocatore. Il credito non introduce una seconda Operatrice: entrambe le voci appartengono allo stesso Hawks personalizzabile.",
        "runa-blask-vic-michaelis": "Runa gestisce i compiti meno appariscenti della compagnia da The Den e collabora con Zero Company per necessità, pur provenendo dai Separatisti.",
        "kabb-uppercut-jb-blanc": "Kabb è un ex pugile e criminale Felshi con un braccio cibernetico. EA lo presenta come un Operatore narrativo di Zero Company.",
        "jae-mordant-judy-alice-lee": "Nata nella Casata Mordant, Jae governava Luunata come Baronessa dei Minerali prima che Infinite Coil prendesse il pianeta; contribuì a far ingaggiare Zero Company dalla Repubblica.",
        "bennic-halloren-leo-howard": "La fonte conferma Bennic Halloren e il suo interprete, ma non pubblica ancora fazione, funzione di gioco o stato di Operatore schierabile.",
        "visser-dylan-kenin": "La fonte conferma Visser e il suo interprete, ma non descrive ancora fazione, ruolo narrativo o stato giocabile.",
        "tel-rea-nicole-rainteau": "Tel-Rea è una Padawan Jedi Tognath che si unisce a Zero Company per onorare l’eredità del suo defunto Maestro Jedi.",
        "neesh-renark-jim-pirri": "La fonte conferma Neesh Renark e il suo interprete; non consente di dedurre abilità, equipaggiamento o partecipazione alle missioni tattiche.",
        "m3vo-meevo-dc-douglas": "M-3VO, detto anche Meevo, è un personaggio droide. Il credito ufficiale non conferma da solo che sia un’unità da combattimento reclutabile.",
        "typhon-hunter-smith": "La fonte conferma il nome Typhon e il suo interprete, ma non identifica ancora ufficialmente alleanza o funzione di gioco.",
    },
    "ko": {
        "hawks-masculine-jonathan-freeman": "조너선 프리먼은 공화국 장교 출신으로 Infinite Coil에 맞서 독립 부대를 다시 이끄는 호크스의 남성 음성을 맡습니다. 호크스는 주요 스토리 임무의 중심 인물입니다.",
        "hawks-feminine-erica-luttrell": "에리카 러트렐은 플레이어가 만드는 주인공의 여성 음성을 맡습니다. 별도 오퍼레이터가 추가되는 것이 아니라 두 음성 모두 같은 커스터마이즈 가능한 호크스를 표현합니다.",
        "runa-blask-vic-michaelis": "루나는 The Den에서 회사의 실무를 담당하며, 분리주의자 출신이지만 필요에 의해 Zero Company와 협력합니다.",
        "kabb-uppercut-jb-blanc": "카브는 사이버네틱 팔을 지닌 펠시 종족의 전직 권투 선수이자 베테랑 범죄자입니다. EA는 그를 Zero Company의 고정 서사 오퍼레이터로 소개합니다.",
        "jae-mordant-judy-alice-lee": "모던트 가문 출신인 재는 Infinite Coil이 루나타를 점령하기 전 광석 남작으로 통치했으며, 공화국이 Zero Company를 고용하도록 설득하는 데 기여했습니다.",
        "bennic-halloren-leo-howard": "공식 자료는 베닉 할로렌과 배우를 확인하지만 소속, 게임플레이 역할, 출격 가능한 오퍼레이터 여부는 아직 공개하지 않았습니다.",
        "visser-dylan-kenin": "공식 자료는 비서와 배우를 확인하지만 소속, 서사적 기능, 플레이 가능 여부는 아직 설명하지 않았습니다.",
        "tel-rea-nicole-rainteau": "텔-레아는 사망한 제다이 마스터의 유산을 기리기 위해 Zero Company에 합류한 토그나스 제다이 파다완입니다.",
        "neesh-renark-jim-pirri": "공식 자료는 니시 레나크와 배우를 확인하지만 능력, 장비, 전술 임무 참여 여부를 추정할 근거는 제공하지 않습니다.",
        "m3vo-meevo-dc-douglas": "M-3VO 또는 미보는 드로이드 캐릭터입니다. 공식 성우 크레딧만으로 모집 가능한 전투 유닛임이 확인되지는 않습니다.",
        "typhon-hunter-smith": "공식 자료는 타이폰과 배우를 확인하지만 진영이나 게임 내 기능은 아직 공식적으로 밝히지 않았습니다.",
    },
    "pl": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman gra męską wersję Hawksa, byłego oficera Republiki, który ponownie prowadzi niezależny oddział przeciw Infinite Coil. Hawks pozostaje centralną postacią misji fabularnych.",
        "hawks-feminine-erica-luttrell": "Erica Luttrell gra żeński głos protagonisty tworzonego przez gracza. Kredyt nie oznacza drugiej Operatorki: oba głosy należą do tego samego personalizowanego Hawksa.",
        "runa-blask-vic-michaelis": "Runa zajmuje się codziennymi obowiązkami kompanii w The Den i współpracuje z Zero Company z konieczności, mimo separatystycznej przeszłości.",
        "kabb-uppercut-jb-blanc": "Kabb to były bokser i doświadczony przestępca rasy Felshi z cybernetycznym ramieniem. EA przedstawia go jako autorskiego Operatora Zero Company.",
        "jae-mordant-judy-alice-lee": "Jae z rodu Mordant władała Luunatą jako Baronessa Rudy, zanim planetę przejęło Infinite Coil; pomogła przekonać Republikę do wynajęcia Zero Company.",
        "bennic-halloren-leo-howard": "Źródło potwierdza Bennica Hallorena i aktora, ale nie ujawnia jeszcze frakcji, funkcji w grze ani statusu Operatora możliwego do wystawienia.",
        "visser-dylan-kenin": "Źródło potwierdza Vissera i aktora, ale nie opisuje jeszcze frakcji, roli fabularnej ani grywalności.",
        "tel-rea-nicole-rainteau": "Tel-Rea to padawanka Jedi rasy Tognath, która dołącza do Zero Company, aby uczcić dziedzictwo zmarłego Mistrza Jedi.",
        "neesh-renark-jim-pirri": "Źródło potwierdza Neesha Renarka i aktora, lecz nie pozwala wnioskować o zdolnościach, wyposażeniu ani udziale w misjach taktycznych.",
        "m3vo-meevo-dc-douglas": "M-3VO, znany też jako Meevo, jest postacią droida. Sam oficjalny kredyt nie potwierdza, że to rekrutowalna jednostka bojowa.",
        "typhon-hunter-smith": "Źródło potwierdza imię Typhon i aktora, ale nie określa jeszcze oficjalnie jego strony konfliktu ani funkcji w grze.",
    },
    "pt-br": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman interpreta a apresentação masculina de Hawks, o ex-oficial da República que volta a liderar uma equipe independente contra a Infinite Coil. Hawks ocupa o centro das missões de história.",
        "hawks-feminine-erica-luttrell": "Erica Luttrell interpreta a voz feminina do protagonista criado pelo jogador. O crédito não apresenta uma segunda Operadora: as duas vozes pertencem ao mesmo Hawks personalizável.",
        "runa-blask-vic-michaelis": "Runa cuida das tarefas administrativas da companhia em The Den e trabalha com a Zero Company por necessidade, apesar de sua origem Separatista.",
        "kabb-uppercut-jb-blanc": "Kabb é um ex-lutador e criminoso Felshi veterano com braço cibernético. A EA o apresenta como um Operador autoral da Zero Company.",
        "jae-mordant-judy-alice-lee": "Jae, da Casa Mordant, governava Luunata como Baronesa do Minério antes de a Infinite Coil tomar o planeta; ela ajudou a convencer a República a contratar a Zero Company.",
        "bennic-halloren-leo-howard": "A fonte confirma Bennic Halloren e seu intérprete, mas ainda não publica facção, função de jogo ou status de Operador mobilizável.",
        "visser-dylan-kenin": "A fonte confirma Visser e seu intérprete, mas ainda não detalha facção, função narrativa ou condição jogável.",
        "tel-rea-nicole-rainteau": "Tel-Rea é uma Padawan Jedi Tognath que entra para a Zero Company a fim de honrar o legado de seu falecido Mestre Jedi.",
        "neesh-renark-jim-pirri": "A fonte confirma Neesh Renark e seu intérprete; isso não permite deduzir habilidades, equipamento ou participação em missões táticas.",
        "m3vo-meevo-dc-douglas": "M-3VO, também chamado Meevo, é um personagem droide. O crédito oficial sozinho não confirma que ele seja uma unidade de combate recrutável.",
        "typhon-hunter-smith": "A fonte confirma o nome Typhon e seu intérprete, mas ainda não identifica oficialmente sua aliança ou função de jogo.",
    },
    "zh-cn": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman负责Hawks的男性语音。Hawks曾是共和国军官，后来重新领导独立队伍对抗Infinite Coil，并在主线任务中居于核心位置。",
        "hawks-feminine-erica-luttrell": "Erica Luttrell负责玩家自建主角的女性语音。该演员条目并不代表第二名干员；两种语音都对应同一个可自定义的Hawks。",
        "runa-blask-vic-michaelis": "Runa在The Den负责团队的日常管理事务。她虽来自分离主义阵营，却因现实需要与Zero Company合作。",
        "kabb-uppercut-jb-blanc": "Kabb是拥有义肢手臂的Felshi族前拳手和老练罪犯；EA将他列为Zero Company的固定剧情干员。",
        "jae-mordant-judy-alice-lee": "Jae出身Mordant家族，Infinite Coil占领Luunata前曾以矿石女爵身份统治当地；她促成共和国雇用Zero Company。",
        "bennic-halloren-leo-howard": "官方资料确认了Bennic Halloren及演员，但尚未公布其阵营、玩法职能或是否为可部署干员。",
        "visser-dylan-kenin": "官方资料确认了Visser及演员，但尚未说明其阵营、剧情职能或可玩状态。",
        "tel-rea-nicole-rainteau": "Tel-Rea是一名Tognath族绝地学徒，为继承已故绝地大师的遗志而加入Zero Company。",
        "neesh-renark-jim-pirri": "官方资料确认了Neesh Renark及演员；仅凭演员表不能推导其技能、装备或是否参与战术任务。",
        "m3vo-meevo-dc-douglas": "M-3VO又名Meevo，是一名机器人角色。官方配音信息本身并不能确认它是可招募战斗单位。",
        "typhon-hunter-smith": "官方资料确认了Typhon及演员，但尚未正式说明其阵营或玩法职能。",
    },
    "zh-tw": {
        "hawks-masculine-jonathan-freeman": "Jonathan Freeman負責Hawks的男性語音。Hawks曾是共和國軍官，後來重新領導獨立隊伍對抗Infinite Coil，並在主線任務中居於核心位置。",
        "hawks-feminine-erica-luttrell": "Erica Luttrell負責玩家自建主角的女性語音。此演員條目並不代表第二名幹員；兩種語音都對應同一個可自訂的Hawks。",
        "runa-blask-vic-michaelis": "Runa在The Den負責團隊的日常管理事務。她雖來自分離主義陣營，卻因現實需要與Zero Company合作。",
        "kabb-uppercut-jb-blanc": "Kabb是擁有義肢手臂的Felshi族前拳手和老練罪犯；EA將他列為Zero Company的固定劇情幹員。",
        "jae-mordant-judy-alice-lee": "Jae出身Mordant家族，Infinite Coil佔領Luunata前曾以礦石女爵身分統治當地；她促成共和國僱用Zero Company。",
        "bennic-halloren-leo-howard": "官方資料確認了Bennic Halloren及演員，但尚未公布其陣營、玩法職能或是否為可部署幹員。",
        "visser-dylan-kenin": "官方資料確認了Visser及演員，但尚未說明其陣營、劇情職能或可玩狀態。",
        "tel-rea-nicole-rainteau": "Tel-Rea是一名Tognath族絕地學徒，為繼承已故絕地大師的遺志而加入Zero Company。",
        "neesh-renark-jim-pirri": "官方資料確認了Neesh Renark及演員；僅憑演員表不能推導其技能、裝備或是否參與戰術任務。",
        "m3vo-meevo-dc-douglas": "M-3VO又名Meevo，是一名機器人角色。官方配音資訊本身並不能確認它是可招募戰鬥單位。",
        "typhon-hunter-smith": "官方資料確認了Typhon及演員，但尚未正式說明其陣營或玩法職能。",
    },
}


def main():
    base.CAST.update(CAST)
    for locale in base.LOCALES:
        base.COPY[locale]["cast_desc"].update(CONTEXT[locale])

    created = 0
    for locale in base.LOCALES:
        folder = ROOT / locale / "cast"
        for slug, (character, actor) in CAST.items():
            html = base.cast_page(locale, slug, character, actor)
            html = html.replace("23 July 2026", "26 July 2026")
            (folder / f"{slug}.html").write_text(html, encoding="utf-8")
            created += 1
        (folder / "index.html").write_text(base.hub_page(locale, "cast"), encoding="utf-8")

    base.replace_alternates(ROOT / "cast" / "index.html", "cast")
    for locale in ("de", "ja"):
        base.replace_alternates(ROOT / locale / "cast" / "index.html", "cast")
    for slug in CAST:
        base.replace_alternates(ROOT / "cast" / f"{slug}.html", "cast", slug)
        for locale in ("de", "ja"):
            base.replace_alternates(ROOT / locale / "cast" / f"{slug}.html", "cast", slug)

    print(f"Round 23 created {created} localized cast pages")


if __name__ == "__main__":
    main()
