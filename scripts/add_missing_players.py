#!/usr/bin/env python3
"""
Hiányzó labdarúgók hozzáadása a labdarugo_palyafutas kérdésekhez.
Wikipedia infobox alapján generálja a pályafutás táblázatot.
"""

import json
import sys
from pathlib import Path

# Projekt gyökér a Python path-hoz
sys.path.insert(0, str(Path(__file__).parent.parent))
import re
import time
from pathlib import Path

import requests

# Ország nevek: angol -> magyar
COUNTRY_MAP = {
    "Argentina": "Argentína", "Brazil": "Brazília", "France": "Franciaország",
    "Germany": "Németország", "Spain": "Spanyolország", "Italy": "Olaszország",
    "Portugal": "Portugália", "Netherlands": "Hollandia", "England": "Anglia",
    "Belgium": "Belgium", "Croatia": "Horvátország", "Uruguay": "Uruguay",
    "Poland": "Lengyelország", "Egypt": "Egyiptom", "Norway": "Norvégia",
    "Senegal": "Szenegál", "Morocco": "Marokkó", "Serbia": "Szerbia",
    "Switzerland": "Svájc", "Denmark": "Dánia", "Sweden": "Svédország",
    "Wales": "Wales", "Scotland": "Skócia", "Ireland": "Írország",
    "Ukraine": "Ukrajna", "Romania": "Románia", "Czech Republic": "Csehország",
    "Czechia": "Csehország", "Greece": "Görögország", "Turkey": "Törökország",
    "Russia": "Oroszország", "Colombia": "Kolumbia", "Chile": "Chile",
    "Mexico": "Mexikó", "Japan": "Japán", "South Korea": "Dél-Korea",
    "Ivory Coast": "Elefántcsontpart", "Côte d'Ivoire": "Elefántcsontpart",
    "Cameroon": "Kamerun", "Ghana": "Ghána", "Nigeria": "Nigéria",
    "Algeria": "Algéria", "Tunisia": "Tunézia", "Bosnia": "Bosznia",
    "Bosnia and Herzegovina": "Bosznia-Hercegovina",
    "Slovakia": "Szlovákia", "Austria": "Ausztria", "Hungary": "Magyarország",
    "Canada": "Kanada", "United States": "USA", "Australia": "Ausztrália",
}

# Hiányzó játékosok - Wikipedia cím -> megjelenített név
MISSING_PLAYERS = [
    ("Achraf_Hakimi", "Achraf Hakimi", "Marokkó"),
    ("Alessandro_Nesta", "Alessandro Nesta", "Olaszország"),
    ("Alexandre_Lacazette", "Alexandre Lacazette", "Franciaország"),
    ("Alexis_Sánchez", "Alexis Sánchez", "Chile"),
    ("Alisson_Becker", "Alisson Becker", "Brazília"),
    ("Alphonso_Davies", "Alphonso Davies", "Kanada"),
    ("Arturo_Vidal", "Arturo Vidal", "Chile"),
    ("Axel_Witsel", "Axel Witsel", "Belgium"),
    ("Aymeric_Laporte", "Aymeric Laporte", "Spanyolország"),
    ("Bebeto", "Bebeto", "Brazília"),
    ("Bernardo_Silva", "Bernardo Silva", "Portugália"),
    ("Bruno_Fernandes", "Bruno Fernandes", "Portugália"),
    ("Bukayo_Saka", "Bukayo Saka", "Anglia"),
    ("Carlos_Tevez", "Carlos Tevez", "Argentína"),
    ("Casemiro", "Casemiro", "Brazília"),
    ("Cesc_Fàbregas", "Cesc Fàbregas", "Spanyolország"),
    ("Christian_Eriksen", "Christian Eriksen", "Dánia"),
    ("Christopher_Nkunku", "Christopher Nkunku", "Franciaország"),
    ("Claude_Makélélé", "Claude Makélélé", "Franciaország"),
    ("Dani_Carvajal", "Dani Carvajal", "Spanyolország"),
    ("David_Villa", "David Villa", "Spanyolország"),
    ("Declan_Rice", "Declan Rice", "Anglia"),
    ("Dejan_Lovren", "Dejan Lovren", "Horvátország"),
    ("Dida_(footballer)", "Dida", "Brazília"),
    ("Dries_Mertens", "Dries Mertens", "Belgium"),
    ("Ederson_(footballer)", "Ederson", "Brazília"),
    ("Edin_Džeko", "Edin Džeko", "Bosznia-Hercegovina"),
    ("Edinson_Cavani", "Edinson Cavani", "Uruguay"),
    ("Federico_Valverde", "Federico Valverde", "Uruguay"),
    ("Fernando_Torres", "Fernando Torres", "Spanyolország"),
    ("Franco_Baresi", "Franco Baresi", "Olaszország"),
    ("Frenkie_de_Jong", "Frenkie de Jong", "Hollandia"),
    ("Gabriel_Jesus", "Gabriel Jesus", "Brazília"),
    ("Gary_Lineker", "Gary Lineker", "Anglia"),
    ("Gavi_(footballer)", "Gavi", "Spanyolország"),
    ("Gianluigi_Donnarumma", "Gianluigi Donnarumma", "Olaszország"),
    ("Harry_Kane", "Harry Kane", "Anglia"),
    ("Hugo_Lloris", "Hugo Lloris", "Franciaország"),
    ("Ian_Rush", "Ian Rush", "Wales"),
    ("Ivan_Rakitić", "Ivan Rakitić", "Horvátország"),
    ("Jack_Grealish", "Jack Grealish", "Anglia"),
    ("Jan_Oblak", "Jan Oblak", "Szlovénia"),
    ("Jan_Verthongen", "Jan Vertonghen", "Belgium"),
    ("Javier_Mascherano", "Javier Mascherano", "Argentína"),
    ("Jordi_Alba", "Jordi Alba", "Spanyolország"),
    ("Jorginho_(footballer)", "Jorginho", "Olaszország"),
    ("João_Cancelo", "João Cancelo", "Portugália"),
    ("Juninho_Pernambucano", "Juninho Pernambucano", "Brazília"),
    ("Jérôme_Boateng", "Jérôme Boateng", "Németország"),
    ("Kai_Havertz", "Kai Havertz", "Németország"),
    ("Kalidou_Koulibaly", "Kalidou Koulibaly", "Szenegál"),
    ("Keylor_Navas", "Keylor Navas", "Costa Rica"),
    ("Kingsley_Coman", "Kingsley Coman", "Franciaország"),
    ("Lautaro_Martínez", "Lautaro Martínez", "Argentína"),
    ("Leonardo_Bonucci", "Leonardo Bonucci", "Olaszország"),
    ("Leroy_Sané", "Leroy Sané", "Németország"),
    ("Marc-André_ter_Stegen", "Marc-André ter Stegen", "Németország"),
    ("Marcelo_(footballer)", "Marcelo", "Brazília"),
    ("Marco_Verratti", "Marco Verratti", "Olaszország"),
    ("Mario_Mandžukić", "Mario Mandžukić", "Horvátország"),
    ("Marquinhos_(footballer)", "Marquinhos", "Brazília"),
    ("Mason_Mount", "Mason Mount", "Anglia"),
    ("Mesut_Özil", "Mesut Özil", "Németország"),
    ("Mike_Maignan", "Mike Maignan", "Franciaország"),
    ("Miralem_Pjanić", "Miralem Pjanić", "Bosznia-Hercegovina"),
    ("Mousa_Dembélé_(Belgian_footballer)", "Mousa Dembélé", "Belgium"),
    ("N'Golo_Kanté", "N'Golo Kanté", "Franciaország"),
    ("Olivier_Giroud", "Olivier Giroud", "Franciaország"),
    ("Pedri", "Pedri", "Spanyolország"),
    ("Phil_Foden", "Phil Foden", "Anglia"),
    ("Pierre-Emerick_Aubameyang", "Pierre-Emerick Aubameyang", "Gabon"),
    ("Pierre-Emile_Højbjerg", "Pierre-Emile Højbjerg", "Dánia"),
    ("Radja_Nainggolan", "Radja Nainggolan", "Belgium"),
    ("Raphaël_Varane", "Raphaël Varane", "Franciaország"),
    ("Raphinha_(footballer)", "Raphinha", "Brazília"),
    ("Reece_James", "Reece James", "Anglia"),
    ("Richarlison", "Richarlison", "Brazília"),
    ("Roberto_Carlos", "Roberto Carlos", "Brazília"),
    ("Robin_van_Persie", "Robin van Persie", "Hollandia"),
    ("Romelu_Lukaku", "Romelu Lukaku", "Belgium"),
    ("Ruud_van_Nistelrooy", "Ruud van Nistelrooy", "Hollandia"),
    ("Rúben_Dias", "Rúben Dias", "Portugália"),
    ("Serge_Gnabry", "Serge Gnabry", "Németország"),
    ("Sergio_Busquets", "Sergio Busquets", "Spanyolország"),
    ("Sime_Vrsaljko", "Sime Vrsaljko", "Horvátország"),
    ("Theo_Hernández", "Theo Hernández", "Franciaország"),
    ("Thibaut_Courtois", "Thibaut Courtois", "Belgium"),
    ("Toby_Alderweireld", "Toby Alderweireld", "Belgium"),
    ("Trent_Alexander-Arnold", "Trent Alexander-Arnold", "Anglia"),
    ("Victor_Osimhen", "Victor Osimhen", "Nigéria"),
    ("Wojciech_Szczęsny", "Wojciech Szczęsny", "Lengyelország"),
    ("Yannick_Carrasco", "Yannick Carrasco", "Belgium"),
]

def get_wikipedia_infobox(title: str) -> dict:
    """Wikipedia API: infobox adatok."""
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
        print(f"  [ERROR] {title}: {e}")
    return {}

def parse_infobox(wikitext: str) -> dict:
    """Infobox kinyerése."""
    out = {"clubs": [], "national_team": ""}
    for i in range(1, 25):
        ym = re.search(rf"\|\s*years{i}\s*=\s*([^\n|\[\]]+)", wikitext)
        cm = re.search(rf"\|\s*clubs{i}\s*=\s*\[\[([^\]|]+)", wikitext)
        if ym and cm:
            years = re.sub(r"{{[^}]+}}", "", ym.group(1)).strip()
            club = cm.group(1).strip()
            out["clubs"].append((years, club))
    for nt in re.finditer(r"\|\s*nationalteam\d+\s*=\s*\[\[([^\]|]+)", wikitext):
        team = nt.group(1)
        if "under-" in team or "U20" in team or "U21" in team or "U23" in team:
            continue
        country = team.replace(" national football team", "").replace(" national team", "").strip()
        out["national_team"] = COUNTRY_MAP.get(country, country)
        break
    return out

def clean_club(s: str) -> str:
    """Klubnév tisztítása."""
    s = re.sub(r"\([^)]*\)", "", s).strip()
    return s or s

def format_career_table(display_name: str, national: str, clubs: list) -> str:
    """Pályafutás táblázat generálása."""
    lines = [
        "**Kinek a pályafutása?**",
        "",
        "| # | Klub | Időszak | Gól |",
        "|---|------|---------|-----|",
    ]
    for i, (years, club) in enumerate(clubs[:15], 1):
        club_clean = clean_club(club)
        if club_clean and "youth" not in club.lower() and "B team" not in club:
            lines.append(f"| {i} | {club_clean} | {years} | — |")
    lines.append(f"| | **Válogatott:** {national} | | |")
    lines.append("| | **Megjegyzés:** | | |")
    return "\n".join(lines)

def get_wrong_options(display_name: str, all_players: list) -> list:
    """3 helytelen opció."""
    wrong = [p for p in all_players if p != display_name]
    import random
    return random.sample(wrong, min(3, len(wrong)))

def main():
    from topics.labdarugo_palyafutas import LABDARUGO_PALYAFUTAS_QUESTIONS
    current = set(q['options'][q['correct']] for q in LABDARUGO_PALYAFUTAS_QUESTIONS)
    all_players = list(current) + [m[1] for m in MISSING_PLAYERS]
    
    new_questions = []
    for wp_title, display_name, fallback_nat in MISSING_PLAYERS:
        if display_name in current:
            continue
        print(f"  {display_name}...")
        info = get_wikipedia_infobox(wp_title)
        if not info and "(" in wp_title:
            base = wp_title.split("(")[0].strip()
            info = get_wikipedia_infobox(base)
        
        national = info.get("national_team") or fallback_nat
        clubs = info.get("clubs", [])
        
        if not clubs:
            # Fallback: egyszerű kérdés
            clubs = [("—", "—")]
        
        table = format_career_table(display_name, national, clubs)
        wrong = get_wrong_options(display_name, all_players)
        options = [display_name] + wrong
        
        new_questions.append({
            "question": table,
            "options": options,
            "correct": 0,
            "explanation": f"{display_name} pályafutása.",
            "topic": "labdarugo_palyafutas",
        })
        current.add(display_name)
        all_players.append(display_name)
        time.sleep(0.4)
    
    # Hozzáfűzés a fájlhoz
    topics_dir = Path(__file__).parent.parent / "topics"
    py_file = topics_dir / "labdarugo_palyafutas.py"
    content = py_file.read_text(encoding="utf-8")
    
    # Utolsó ] előtt beszúrás
    insert = ""
    for q in new_questions:
        q_text = q["question"].replace('"""', '\\"\\"\\"')
        opts = json.dumps(q["options"], ensure_ascii=False)
        insert += f'''    {{
        "question": """{q["question"]}""",
        "options": {opts},
        "correct": 0,
        "explanation": "{q["explanation"]}",
        "topic": "labdarugo_palyafutas"
    }},
'''
    
    # Cseréljük az utolsó ],-t (a listában) hogy beszúrjunk előtte
    last_bracket = content.rfind("]")
    content = content[:last_bracket] + insert + content[last_bracket:]
    
    py_file.write_text(content, encoding="utf-8")
    print(f"\n✅ {len(new_questions)} új játékos hozzáadva.")

if __name__ == "__main__":
    main()
