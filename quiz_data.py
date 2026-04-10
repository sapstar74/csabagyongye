"""
Quiz topic data: imports, sync, and QUIZ_DATA_BY_TOPIC.
"""

from datetime import datetime
from pathlib import Path

from topics.foldrajz_complete import FOLDRAJZ_QUESTIONS_COMPLETE as FOLDRAJZ_QUESTIONS
from topics.komolyzene_uj import QUESTIONS as KOMOLYZENE_QUESTIONS


def _sync_komolyzene_questions() -> None:
    """Auto-sync: add missing Komolyzene questions from audio_files/komolyzene"""
    try:
        import os

        audio_dir = Path(__file__).parent / "audio_files/komolyzene"
        questions_file = Path(__file__).parent / "topics/komolyzene_uj.py"

        if not audio_dir.exists():
            return

        existing_files = set(
            q.get("audio_file")
            for q in KOMOLYZENE_QUESTIONS
            if isinstance(q, dict) and q.get("audio_file")
        )

        def parse_filename(filename: str):
            name = filename
            if name.lower().endswith(".mp3"):
                name = name[:-4]
            # Drop leading index like "NN. "
            parts = name.split(". ", 1)
            if len(parts) == 2 and parts[0].isdigit():
                name = parts[1]
            # Split composer and title by " - " if present
            composer = None
            title = name
            if " - " in name:
                composer, title = name.split(" - ", 1)
            # Normalize underscores
            composer = composer.replace("_", " ") if composer else None
            title = title.replace("_", " ") if title else ""
            return composer, title

        def get_smart_options(composer: str, title: str):
            """Intelligens opciók generálása a zeneszerző alapján"""
            common_composers = ["Mozart", "Beethoven", "Bach", "Haydn"]

            if composer and composer not in {"Ismeretlen", "Unknown", "Unknown Artist"}:
                options = [composer]
                for c in common_composers:
                    if c != composer and len(options) < 4:
                        options.append(c)
                more_composers = ["Chopin", "Tchaikovsky", "Vivaldi", "Handel", "Schubert"]
                for c in more_composers:
                    if c != composer and len(options) < 4:
                        options.append(c)
                return options, 0
            else:
                return common_composers, 0

        added = 0
        new_questions = []

        for fname in sorted(os.listdir(audio_dir)):
            if not fname.lower().endswith(".mp3"):
                continue
            if fname in existing_files:
                continue

            composer, title = parse_filename(fname)
            options, correct_index = get_smart_options(composer, title)

            if title:
                question_text = f'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét: "{title}"'
            else:
                question_text = "Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:"

            new_question = {
                "question": question_text,
                "options": options,
                "correct": correct_index,
                "explanation": f"{(composer or 'Ismeretlen')}: {title}" if title else (composer or "Komolyzene"),
                "audio_file": fname,
                "topic": "komolyzene",
            }

            KOMOLYZENE_QUESTIONS.append(new_question)
            new_questions.append(new_question)
            added += 1

        if added > 0 and questions_file.exists():
            try:
                all_questions = list(KOMOLYZENE_QUESTIONS)

                content = f"""# Auto-generated questions file
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

QUESTIONS = [
"""
                for q in all_questions:
                    content += "    {\n"
                    question_text = q["question"].replace('"', '\\"')
                    content += f'        "question": "{question_text}",\n'
                    content += '        "options": [\n'
                    for option in q["options"]:
                        content += f'            "{option}",\n'
                    content += '        ],\n'
                    content += f'        "correct": {q["correct"]},\n'
                    if "explanation" in q:
                        explanation_text = q["explanation"].replace('"', '\\"')
                        content += f'        "explanation": "{explanation_text}",\n'
                    if "audio_file" in q:
                        content += f'        "audio_file": "{q["audio_file"]}",\n'
                    if "song_title" in q:
                        content += f'        "song_title": "{q["song_title"]}",\n'
                    if "topic" in q:
                        content += f'        "topic": "{q["topic"]}",\n'
                    content += "    },\n"

                content += "]\n\n"
                content += "# Export alias for compatibility\n"
                content += "KOMOLYZENE_QUESTIONS = QUESTIONS\n"

                with open(questions_file, "w", encoding="utf-8") as f:
                    f.write(content)

                print(f"[AUTO-SYNC] Komolyzene: {added} új kérdés hozzáadva és elmentve a fájlba.")
            except Exception as e:
                print(f"[AUTO-SYNC] Hiba a fájl mentésekor: {e}")
    except Exception as e:
        print(f"[AUTO-SYNC] Hiba: {e}")


_sync_komolyzene_questions()

from topics.tudosok import TUDOSOK_QUESTIONS
from topics.mitologia_all_questions import MITOLOGIA_QUESTIONS_ALL
from topics.haboru_all_questions import HABORU_QUESTIONS_ALL
from topics.kiralyok import KIRALYOK_QUESTIONS
from topics.allatok_balanced import ALLATOK_QUESTIONS_BALANCED
from topics.dramak import DRAMAK_QUESTIONS
from topics.sport_logok import SPORT_LOGOK_QUESTIONS
from topics.zaszlok_all_questions import ZASZLOK_QUESTIONS_ALL
from topics.zaszlok_reszletek import ZASZLOK_RESZLETEK_QUESTIONS
from topics.magyar_zenekarok_uj import QUESTIONS as MAGYAR_ZENEKAROK_QUESTIONS_UJ
from topics.nemzetkozi_zenekarok_final_fixed_with_real_audio import QUESTIONS as NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak import IDIOTA_SZAVAK_QUESTIONS
from topics.festmenyek import FESTMENY_QUESTIONS
from topics.magyar_festmenyek import QUESTIONS as MAGYAR_FESTMENYEK_QUESTIONS
from topics.one_hit_wonders import QUESTIONS as ONE_HIT_WONDERS_QUESTIONS
from topics.sorozat_focimek import QUESTIONS as SOROZAT_FOCIMEK_QUESTIONS
from topics.regények import REGÉNYEK_QUESTIONS
from topics.labdarugo_palyafutas import LABDARUGO_PALYAFUTAS_QUESTIONS
from topics.vallas_egyhaztortenet import VALLAS_EGYHAZTORTENET_QUESTIONS
from topics.muveszet import MUVESZET_QUESTIONS
from topics.termeszettudomany import TERMESZETTUDOMANY_QUESTIONS
from topics.irodalom import IRODALOM_QUESTIONS
from topics.politika import POLITIKA_QUESTIONS
from topics.vilagtortenelm import VILAGTORTENELM_QUESTIONS
from topics.magyar_tortenelm import MAGYAR_TORTENELM_QUESTIONS
from topics.biologia import BIOLOGIA_QUESTIONS
from topics.sport import SPORT_QUESTIONS
from topics.hires_magyarok import HIRES_MAGYAROK_QUESTIONS
from topics.becenevek import BECENEVEK_QUESTIONS
from topics.hip_hop import HIP_HOP_QUESTIONS
from topics.rock_metal import ROCK_METAL_QUESTIONS
from topics.dj_producer import DJ_PRODUCER_QUESTIONS
from topics.almombol_felebresztve import ALMOMBOL_FELEBRESZTVE_QUESTIONS

# Összevont témakörök: Magyar királyok+Magyar történelem, Háborúk+Világtörténelem, Földrajz+Természettudomány
# Zászlók és zászlórészlet külön témakörök
MAGYAR_TORTENELM_OSSZES = list(KIRALYOK_QUESTIONS) + list(MAGYAR_TORTENELM_QUESTIONS)
VILAGTORTENELM_OSSZES = list(HABORU_QUESTIONS_ALL) + list(VILAGTORTENELM_QUESTIONS)
TERMESZETTUDOMANY_OSSZES = list(FOLDRAJZ_QUESTIONS) + list(TERMESZETTUDOMANY_QUESTIONS)

QUIZ_DATA_BY_TOPIC = {
    "komolyzene": KOMOLYZENE_QUESTIONS,
    "magyar_zenekarok": MAGYAR_ZENEKAROK_QUESTIONS_UJ,
    "nemzetkozi_zenekarok": NEMZETKOZI_ZENEKAROK_QUESTIONS,
    "one_hit_wonders": ONE_HIT_WONDERS_QUESTIONS,
    "sorozat_focimek": SOROZAT_FOCIMEK_QUESTIONS,
    "hip_hop": HIP_HOP_QUESTIONS,
    "rock_metal": ROCK_METAL_QUESTIONS,
    "dj_producer": DJ_PRODUCER_QUESTIONS,
    "almombol_felebresztve": ALMOMBOL_FELEBRESZTVE_QUESTIONS,
    "tudósok": TUDOSOK_QUESTIONS,
    "mitológia": MITOLOGIA_QUESTIONS_ALL,
    "állatok": ALLATOK_QUESTIONS_BALANCED,
    "sport_logók": SPORT_LOGOK_QUESTIONS,
    "zászlók": list(ZASZLOK_QUESTIONS_ALL),
    "zászlórészlet": list(ZASZLOK_RESZLETEK_QUESTIONS),
    "idióta_szavak": IDIOTA_SZAVAK_QUESTIONS,
    "festmények": FESTMENY_QUESTIONS,
    "magyar_festmenyek": MAGYAR_FESTMENYEK_QUESTIONS,
    "regények": REGÉNYEK_QUESTIONS,
    "labdarugo_palyafutas": LABDARUGO_PALYAFUTAS_QUESTIONS,
    "vallás és egyháztörténet": VALLAS_EGYHAZTORTENET_QUESTIONS,
    "művészet": MUVESZET_QUESTIONS,
    "természettudomány": TERMESZETTUDOMANY_OSSZES,
    "irodalom": list(IRODALOM_QUESTIONS) + list(DRAMAK_QUESTIONS),
    "politika": POLITIKA_QUESTIONS,
    "világtörténelem": VILAGTORTENELM_OSSZES,
    "magyar történelem": MAGYAR_TORTENELM_OSSZES,
    "biológia": BIOLOGIA_QUESTIONS,
    "sport": SPORT_QUESTIONS,
    "híres magyarok": HIRES_MAGYAROK_QUESTIONS,
    "becenevek": BECENEVEK_QUESTIONS,
}

__all__ = ["QUIZ_DATA_BY_TOPIC", "KOMOLYZENE_QUESTIONS", "MAGYAR_TORTENELM_OSSZES", "ZASZLOK_OSSZES", "VILAGTORTENELM_OSSZES", "TERMESZETTUDOMANY_OSSZES"]
