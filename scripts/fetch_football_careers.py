#!/usr/bin/env python3
"""
Labdarúgó pályafutás kérdések generálása Wikipedia adatokból.
Top 150 labdarúgó (1990-2024) pályafutásának összegyűjtése.
"""

import json
import re
import time
from pathlib import Path

import requests

# Top 150 labdarúgó 1990-2024 (Wikipedia page nevek)
PLAYERS = [
    "Lionel_Messi", "Cristiano_Ronaldo", "Zinedine_Zidane", "Ronaldinho",
    "Ronaldo_(Brazilian_footballer)", "Thierry_Henry", "Kaká", "Andrés_Iniesta",
    "Xavi", "Neymar", "Kylian_Mbappé", "Erling_Haaland", "Kevin_De_Bruyne",
    "Mohamed_Salah", "Robert_Lewandowski", "Karim_Benzema", "Luka_Modrić",
    "Sergio_Ramos", "Gerard_Piqué", "Virgil_van_Dijk", "Manuel_Neuer",
    "Gianluigi_Buffon", "Iker_Casillas", "Marc-André_ter_Stegen",
    "David_Beckham", "Wayne_Rooney", "Steven_Gerrard", "Frank_Lampard",
    "Paul_Scholes", "Roy_Keane", "Patrick_Vieira", "Claude_Makélélé",
    "Andrea_Pirlo", "Sergio_Busquets", "Toni_Kroos", "Casemiro",
    "Philipp_Lahm", "Javier_Zanetti", "Paolo_Maldini", "Alessandro_Nesta",
    "Fabio_Cannavaro", "Franco_Baresi", "Roberto_Carlos", "Marcelo_(footballer)",
    "Dani_Alves", "Jordi_Alba", "Trent_Alexander-Arnold", "Achraf_Hakimi",
    "Raúl_(footballer)", "Ruud_van_Nistelrooy", "Didier_Drogba",
    "Samuel_Eto'o", "Zlatan_Ibrahimović", "Luis_Suárez", "Sergio_Agüero",
    "Edinson_Cavani", "Pierre-Emerick_Aubameyang", "Harry_Kane",
    "Antoine_Griezmann", "Eden_Hazard", "Marco_Reus", "Thomas_Müller",
    "David_Silva", "David_Villa", "Fernando_Torres", "Robin_van_Persie",
    "Carlos_Tevez", "Ángel_Di_María", "Javier_Mascherano", "Dani_Carvajal",
    "Raphaël_Varane", "Mats_Hummels", "Jérôme_Boateng", "Giorgio_Chiellini",
    "Leonardo_Bonucci", "Kalidou_Koulibaly", "Marquinhos_(footballer)",
    "Aymeric_Laporte", "Rúben_Dias", "Bernardo_Silva", "Bruno_Fernandes",
    "Jack_Grealish", "Phil_Foden", "Pedri", "Gavi_(footballer)",
    "Federico_Valverde", "Frenkie_de_Jong", "Rodri_(footballer)",
    "Declan_Rice", "Jude_Bellingham", "Vinícius_Júnior", "Bukayo_Saka",
    "Victor_Osimhen", "Lautaro_Martínez", "Christopher_Nkunku",
    "Gabriel_Jesus", "Richarlison", "Raphinha_(footballer)", "Leroy_Sané",
    "Kingsley_Coman", "Serge_Gnabry", "Kai_Havertz", "Mason_Mount",
    "Reece_James", "João_Cancelo", "Alphonso_Davies", "Theo_Hernández",
    "Roberto_Baggio", "Alessandro_Del_Piero", "Francesco_Totti",
    "Pavel_Nedvěd", "Michael_Ballack", "Bastian_Schweinsteiger",
    "Mesut_Özil", "Marco_Verratti", "N'Golo_Kanté", "Jorginho_(footballer)",
    "Hristo_Stoichkov", "George_Weah", "Rivaldo", "Luís_Figo",
    "Andriy_Shevchenko", "Dennis_Bergkamp", "Eric_Cantona",
    "Alan_Shearer", "Michael_Owen", "Gary_Lineker", "Ian_Rush",
    "Romário", "Bebeto", "Cafu", "Dida_(footballer)", "Juninho_Pernambucano",
    "Gheorghe_Hagi", "Davor_Šuker", "Luka_Modrić", "Ivan_Rakitić",
    "Mario_Mandžukić", "Dejan_Lovren", "Sime_Vrsaljko",
    "Gareth_Bale", "Cesc_Fàbregas", "Alexis_Sánchez", "Arturo_Vidal",
    "Alexandre_Lacazette", "Olivier_Giroud", "N'Golo_Kanté",
    "Hugo_Lloris", "Jan_Verthongen", "Toby_Alderweireld",
    "Christian_Eriksen", "Son_Heung-min", "Harry_Kane",
    "Pierre-Emile_Højbjerg", "Mousa_Dembélé_(Belgian_footballer)",
    "Radja_Nainggolan", "Romelu_Lukaku", "Eden_Hazard",
    "Dries_Mertens", "Yannick_Carrasco", "Axel_Witsel",
    "Edin_Džeko", "Miralem_Pjanić", "Wojciech_Szczęsny",
    "Gianluigi_Donnarumma", "Mike_Maignan", "Keylor_Navas",
    "Jan_Oblak", "Thibaut_Courtois", "Alisson_Becker", "Ederson_(footballer)",
]

# Disambiguation - some players need specific Wikipedia titles
PLAYER_DISAMBIG = {
    "Ronaldo_(Brazilian_footballer)": "Ronaldo",
    "Marcelo_(footballer)": "Marcelo",
    "Marquinhos_(footballer)": "Marquinhos",
    "Rodri_(footballer)": "Rodri",
    "Raphinha_(footballer)": "Raphinha",
    "Jorginho_(footballer)": "Jorginho",
    "Dida_(footballer)": "Dida",
    "Ederson_(footballer)": "Ederson",
    "Mousa_Dembélé_(Belgian_footballer)": "Mousa Dembélé",
    "Gavi_(footballer)": "Gavi",
}


def get_wikipedia_extract(title: str) -> str:
    """Wikipedia API: lekéri a cikk kivonatát."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "exsentences": 8,
        "titles": title.replace("_", " "),
        "format": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid != "-1":
                return page.get("extract", "") or ""
    except Exception as e:
        print(f"  [ERROR] {title}: {e}")
    return ""


def get_wikipedia_infobox(title: str) -> dict:
    """Wikipedia API: lekéri a cikk wikitext-jét és kinyeri az infobox adatokat."""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "prop": "revisions",
        "rvprop": "content",
        "rvslots": "main",
        "titles": title.replace("_", " "),
        "format": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for pid, page in pages.items():
            if pid == "-1":
                continue
            revs = page.get("revisions", [])
            if not revs:
                continue
            content = revs[0].get("slots", {}).get("main", {}).get("*", "")
            return parse_infobox(content)
    except Exception as e:
        print(f"  [ERROR infobox] {title}: {e}")
    return {}


def parse_infobox(wikitext: str) -> dict:
    """Infobox football biography mezők kinyerése."""
    out = {}
    # position
    m = re.search(r"\|\s*position\s*=\s*\[\[([^\]|]+)", wikitext, re.I)
    if m:
        out["position"] = m.group(1).strip()
    # clubs (years + clubs)
    clubs = []
    for i in range(1, 20):
        ym = re.search(rf"\|\s*years{i}\s*=\s*([^\n|]+)", wikitext)
        cm = re.search(rf"\|\s*clubs{i}\s*=\s*\[\[([^\]|]+)", wikitext)
        if ym and cm:
            clubs.append((ym.group(1).strip(), cm.group(1).strip()))
    out["clubs"] = clubs
    # national team (senior only)
    for nt in re.finditer(r"\|\s*nationalteam\d+\s*=\s*\[\[([^\]|]+)", wikitext):
        team = nt.group(1)
        if "under-" in team or "U20" in team or "U21" in team or "U23" in team:
            continue
        out["national_team"] = team.replace(" national football team", "").replace(" national team", "").strip()
        break
    # full name / name
    nm = re.search(r"\|\s*(?:name|full_name)\s*=\s*([^\n|{]+)", wikitext)
    if nm:
        out["name"] = re.sub(r"{{[^}]+}}", "", nm.group(1)).strip()
    return out


def clean_club_name(s: str) -> str:
    """Klubnév tisztítása."""
    s = re.sub(r"\([^)]*\)", "", s).strip()
    s = re.sub(r"FC\s*$", "", s).strip()
    return s or s


def generate_questions(players_data: list) -> list:
    """Kérdések generálása a gyűjtött adatokból."""
    questions = []
    used_club_questions = set()

    for i, pd in enumerate(players_data):
        if not pd:
            continue
        name = pd.get("name") or pd.get("display_name", "?")
        clubs = pd.get("clubs", [])
        national = pd.get("national_team", "")
        position = pd.get("position", "")

        # 1. Melyik válogatott? (ha van)
        if national and "U20" not in national and "U21" not in national and "U23" not in national:
            other_nations = ["Brazil", "Argentina", "France", "Germany", "Spain", "Italy", "Portugal", "Netherlands"]
            other_nations = [n for n in other_nations if n != national][:3]
            options = [national] + other_nations
            correct_idx = 0
            questions.append({
                "question": f"Melyik nemzet válogatottjában játszott {name}?",
                "options": options,
                "correct": correct_idx,
                "explanation": f"{name} a {national} válogatottjában szerepelt.",
                "topic": "labdarugo_palyafutas",
            })

        # 2. Melyik klub? (legtöbbet játszott vagy legismertebb)
        if clubs:
            main_clubs = [c for _, c in clubs if "Barcelona B" not in c and "Barcelona C" not in c and "youth" not in c.lower()]
            if main_clubs:
                main_club = clean_club_name(main_clubs[0]) if main_clubs else ""
                if main_club and (name, main_club) not in used_club_questions:
                    used_club_questions.add((name, main_club))
                    wrong = ["Real Madrid", "Barcelona", "Manchester United", "Juventus", "Bayern Munich", "Chelsea", "Inter Milan", "AC Milan"]
                    wrong = [w for w in wrong if w != main_club][:3]
                    options = [main_club] + wrong
                    correct_idx = 0
                    questions.append({
                        "question": f"Melyik klubnál töltötte {name} a pályafutása legnagyobb részét?",
                        "options": options,
                        "correct": correct_idx,
                        "explanation": f"{name} főleg a {main_club} csapatánál játszott.",
                        "topic": "labdarugo_palyafutas",
                    })

    return questions


def main():
    """Fő futás: adatok gyűjtése és kérdések generálása."""
    output_dir = Path(__file__).parent.parent / "topics"
    output_file = output_dir / "labdarugo_palyafutas.py"

    print("Labdarúgó pályafutás kérdések generálása Wikipedia-ból...")
    print(f"Játékosok száma: {len(PLAYERS)}")

    players_data = []
    for idx, wp_title in enumerate(PLAYERS):
        display_name = PLAYER_DISAMBIG.get(wp_title, wp_title.replace("_", " "))
        print(f"  [{idx+1}/{len(PLAYERS)}] {display_name}...")
        info = get_wikipedia_infobox(wp_title)
        if not info and "(" in wp_title:
            # Try without disambiguation
            base = wp_title.split("(")[0].strip()
            info = get_wikipedia_infobox(base)
        if info:
            info["display_name"] = display_name
            players_data.append(info)
        else:
            extract = get_wikipedia_extract(wp_title)
            if extract:
                players_data.append({
                    "display_name": display_name,
                    "extract": extract[:500],
                })
        time.sleep(0.5)  # Rate limit

    # Generate questions
    questions = generate_questions(players_data)

    # Fallback: ha kevés kérdés, egyszerűbb típusok
    if len(questions) < 50:
        for pd in players_data[:100]:
            name = pd.get("display_name", pd.get("name", "?"))
            national = pd.get("national_team", "")
            if national:
                options = [national, "Brazil", "Argentina", "Germany"]
                options = list(dict.fromkeys(options))[:4]
                correct = options.index(national) if national in options else 0
                questions.append({
                    "question": f"Melyik ország válogatottjában játszott {name}?",
                    "options": options,
                    "correct": correct,
                    "explanation": f"{name} a {national} válogatottjában szerepelt.",
                    "topic": "labdarugo_palyafutas",
                })

    # Deduplicate by question text
    seen = set()
    unique_q = []
    for q in questions:
        key = q["question"]
        if key not in seen:
            seen.add(key)
            unique_q.append(q)

    # Write Python file
    lines = [
        "# Labdarúgó pályafutás kérdések (top 150, 1990-2024)",
        "# Generálva Wikipedia adatokból",
        "",
        "LABDARUGO_PALYAFUTAS_QUESTIONS = [",
    ]
    for q in unique_q[:150]:
        lines.append("    {")
        lines.append(f'        "question": """{q["question"]}""",')
        opts = json.dumps(q["options"], ensure_ascii=False)
        lines.append(f"        \"options\": {opts},")
        lines.append(f"        \"correct\": {q['correct']},")
        lines.append(f'        "explanation": """{q["explanation"]}""",')
        lines.append(f'        "topic": "labdarugo_palyafutas"')
        lines.append("    },")
    lines.append("]")
    lines.append("")

    output_file.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n✅ Kész: {len(unique_q)} kérdés mentve ide: {output_file}")


if __name__ == "__main__":
    main()
