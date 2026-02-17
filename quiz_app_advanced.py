"""
🎯 Csabagyöngye Tréning Center 😄
Kiegészített funkciókkal: Analytics, Quiz módok, Nehézségi szintek
"""

import streamlit as st
from typing import Optional

from i18n import init_i18n, render_language_selector, t, translate_text

init_i18n()


def _normalize_answer_text(value: str) -> str:
    return value.lower().strip() if isinstance(value, str) else ""


def _is_text_answer_correct(user_answer: str, correct_answer: str) -> bool:
    user_clean = _normalize_answer_text(user_answer)
    if not user_clean:
        return False
    variants = {correct_answer}
    translated_correct = translate_text(correct_answer) if correct_answer else ""
    if translated_correct and translated_correct != correct_answer:
        variants.add(translated_correct)

    for variant in variants:
        variant_clean = _normalize_answer_text(variant)
        if not variant_clean:
            continue
        if user_clean == variant_clean:
            return True
        variant_keywords = [keyword for keyword in variant_clean.split() if len(keyword) > 3]
        user_keywords = [keyword for keyword in user_clean.split() if len(keyword) > 3]
        if any(keyword in user_clean for keyword in variant_keywords):
            return True
        if any(keyword in variant_clean for keyword in user_keywords):
            return True
    return False


def _extract_ip_from_headers(headers) -> Optional[str]:
    if not headers:
        return None
    try:
        header_get = headers.get
    except AttributeError:
        try:
            header_get = dict(headers).get
        except Exception:
            return None
    for key in ("X-Forwarded-For", "X-Real-IP", "CF-Connecting-IP", "True-Client-IP"):
        value = header_get(key)
        if value:
            return value.split(",")[0].strip()
    return None


def get_client_ip() -> str:
    """Best-effort client IP lookup (may be unavailable in some envs)."""
    # Streamlit context headers (if available)
    try:
        if hasattr(st, "context") and getattr(st.context, "headers", None):
            ip = _extract_ip_from_headers(st.context.headers)
            if ip:
                return ip
    except Exception:
        pass

    # Script run context (internal API)
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
        request = getattr(ctx, "request", None) if ctx else None
        if request is not None:
            ip = _extract_ip_from_headers(getattr(request, "headers", None))
            if ip:
                return ip
            remote_ip = getattr(request, "remote_ip", None)
            if remote_ip:
                return remote_ip
    except Exception:
        pass

    return "Ismeretlen"
import random
import time
from datetime import datetime
import os
from pathlib import Path
import base64
from topics.foldrajz_complete import FOLDRAJZ_QUESTIONS_COMPLETE as FOLDRAJZ_QUESTIONS
from topics.komolyzene_uj import QUESTIONS as KOMOLYZENE_QUESTIONS

# --- Auto-sync: add missing Komolyzene questions from audio_files/komolyzene ---
def _sync_komolyzene_questions() -> None:
    try:
        import os
        import json
        from pathlib import Path

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
            # Alapértelmezett opciók
            common_composers = ["Mozart", "Beethoven", "Bach", "Haydn"]
            
            if composer and composer not in {"Ismeretlen", "Unknown", "Unknown Artist"}:
                # Ha van zeneszerző, az legyen az első opció
                options = [composer]
                # Töltsük fel a többi opciót más zeneszerzőkkel
                for c in common_composers:
                    if c != composer and len(options) < 4:
                        options.append(c)
                # Ha nincs elég opció, adjunk hozzá még néhányat
                more_composers = ["Chopin", "Tchaikovsky", "Vivaldi", "Handel", "Schubert"]
                for c in more_composers:
                    if c != composer and len(options) < 4:
                        options.append(c)
                return options, 0
            else:
                # Ha nincs zeneszerző, használjunk általános opciókat
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
            
            # Kérdés szövegének generálása - ha van cím, szerepeljen benne
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
        
        # Ha volt új kérdés, mentjük el a fájlba
        if added > 0 and questions_file.exists():
            try:
                # Beolvassuk a teljes kérdéslistát
                all_questions = list(KOMOLYZENE_QUESTIONS)
                
                # Generáljuk a fájl tartalmát
                content = f"""# Auto-generated questions file
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

QUESTIONS = [
"""
                for q in all_questions:
                    content += "    {\n"
                    # Escape quotes in question text
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
                
                # Mentjük a fájlba
                with open(questions_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[AUTO-SYNC] Komolyzene: {added} új kérdés hozzáadva és elmentve a fájlba.")
            except Exception as e:
                print(f"[AUTO-SYNC] Hiba a fájl mentésekor: {e}")
    except Exception as e:
        # Ne törje meg az appot, ha bármi gond van
        print(f"[AUTO-SYNC] Hiba: {e}")
        pass

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
from custom_audio_player import audio_player_with_download
from youtube_audio_mapping import get_youtube_audio_filename_cached, get_youtube_audio_info
from magyar_audio_mapping_uj import MAGYAR_AUDIO_MAPPING_UJ, get_magyar_audio_uj_path
from nemzetkozi_audio_mapping_updated import get_nemzetkozi_audio_path
from quiz_analytics import QuizAnalytics
from quiz_modes import QuizModeManager, QuizMode, DifficultyLevel, QuizModeUI, QuizScoring
from auto_audio_player import auto_audio_player_simple
import subprocess
import json
import glob

def sync_with_github():
    """GitHub-ról szinkronizálja az audiofájlokat és kérdéseket"""
    try:
        st.info(t("🔄 GitHub szinkronizálás indítása..."))
        
        # 1. Git pull - legfrissebb változások letöltése
        st.markdown(t("### 📥 1. Legfrissebb változások letöltése..."))
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'], 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        
        if pull_result.returncode != 0:
            st.error(t("❌ Git pull hiba: {error}", error=pull_result.stderr))
            return False
            
        st.success(t("✅ Git pull sikeres!"))
        
        # 2. Új audiofájlok keresése
        st.markdown(t("### 🎵 2. Új audiofájlok keresése..."))
        
        # Összes audio track összegyűjtése
        all_tracks = get_all_audio_tracks()
        audio_files = [track["audio_path"] for track in all_tracks]
        
        st.info(t("📊 {count} audiofájl található", count=len(audio_files)))
        
        # Kategóriánkénti statisztika
        category_stats = {}
        for track in all_tracks:
            directory = track["directory"]
            if directory not in category_stats:
                category_stats[directory] = 0
            category_stats[directory] += 1
        
        st.markdown(t("**📁 Kategóriánkénti eloszlás:**"))
        for directory, count in category_stats.items():
            st.markdown(t("- {directory}: {count} track", directory=directory, count=count))
        
        # 3. Új kérdés fájlok keresése
        st.markdown(t("### 📝 3. Új kérdés fájlok keresése..."))
        question_files = []
        
        # Keresés a topics könyvtárban
        topics_patterns = [
            "topics/*.py",
            "topics/*_questions.py",
            "topics/*_complete.py"
        ]
        
        for pattern in topics_patterns:
            files = glob.glob(pattern)
            question_files.extend(files)
        
        st.info(t("📊 {count} kérdés fájl található", count=len(question_files)))
        
        # 4. Új tartalmak listázása
        st.markdown(t("### 📋 4. Új tartalmak összefoglalása..."))
        
        if audio_files:
            st.markdown(t("**🎵 Új audiofájlok:**"))
            for file in audio_files:
                st.markdown(t("- {filename}", filename=os.path.basename(file)))
        
        if question_files:
            st.markdown(t("**📝 Kérdés fájlok:**"))
            for file in question_files:
                st.markdown(t("- {filename}", filename=os.path.basename(file)))
        
        # 5. Alkalmazás újraindítása javaslat
        st.markdown(t("### 🔄 5. Alkalmazás újraindítása..."))
        st.warning(t("⚠️ A szinkronizálás után javasolt az alkalmazás újraindítása a legfrissebb tartalmak betöltéséhez."))
        
        if st.button(t("🔄 Alkalmazás újraindítása"), type="primary"):
            st.rerun()
        
        st.success(t("✅ GitHub szinkronizálás sikeresen befejezve!"))
        return True
        
    except Exception as e:
        st.error(t("❌ Szinkronizálási hiba: {error}", error=e))
        return False

def sync_komolyzene_with_github(question_file_path: Optional[str] = None) -> bool:
    """Teljes komolyzene Git sync (pull + add/commit/push)"""
    try:
        repo_root = Path(__file__).parent
        if not (repo_root / ".git").exists():
            st.error(t("❌ Git repo nem található, szinkronizálás nem lehetséges."))
            return False

        st.info(t("🔄 Komolyzene Git sync indítása..."))

        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if pull_result.returncode != 0:
            st.error(t("❌ Git pull hiba: {error}", error=pull_result.stderr or pull_result.stdout))
            return False
        st.success(t("✅ Git pull sikeres!"))

        sync_paths = []
        if question_file_path:
            sync_paths.append(question_file_path)
        else:
            sync_paths.append("topics/komolyzene_uj.py")

        candidate_dirs = [
            "audio_files/komolyzene",
        ]
        for path in candidate_dirs:
            if (repo_root / path).exists():
                sync_paths.append(path)

        # Csak létező útvonalakat hagyunk meg
        existing_paths = [p for p in dict.fromkeys(sync_paths) if (repo_root / p).exists()]
        if not existing_paths:
            st.warning(t("⚠️ Nincsenek komolyzene fájlok a szinkronhoz."))
            return False

        add_result = subprocess.run(
            ['git', 'add', '-A', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if add_result.returncode != 0:
            st.error(t("❌ Git add hiba: {error}", error=add_result.stderr or add_result.stdout))
            return False

        diff_result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if diff_result.returncode != 0:
            st.error(t("❌ Git diff hiba: {error}", error=diff_result.stderr or diff_result.stdout))
            return False

        if not diff_result.stdout.strip():
            st.info(t("ℹ️ Nincs komolyzene változás a szinkronhoz."))
            return True

        commit_msg = f"Komolyzene sync - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_msg, '--', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if commit_result.returncode != 0:
            st.error(t("❌ Git commit hiba: {error}", error=commit_result.stderr or commit_result.stdout))
            return False

        push_result = subprocess.run(
            ['git', 'push'],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if push_result.returncode != 0:
            st.error(t("❌ Git push hiba: {error}", error=push_result.stderr or push_result.stdout))
            return False

        st.success(t("✅ Komolyzene Git sync sikeres!"))
        return True
    except Exception as e:
        st.error(t("❌ Komolyzene sync hiba: {error}", error=e))
        return False

@st.cache_data(ttl=3600, show_spinner=False)
def get_image_base64(image_path):
    """Kép konvertálása base64 formátumra"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except Exception as e:
        st.error(t("Hiba a kép betöltése során: {error}", error=e))
        return ""

# Page config
st.set_page_config(
    page_title=t("Csabagyöngye Tréning Center"),
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .topic-button {
        background-color: #f0f2f6;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .topic-button:hover {
        background-color: #e0e0e0;
        border-color: #1f77b4;
    }
    .topic-button.selected {
        background-color: #1f77b4;
        color: white;
        border-color: #1f77b4;
    }
    .quiz-container {
        background-color: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    .question-text {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        color: #87CEEB;
    }
    /* Pályafutás táblázat stílusa */
    div[data-testid="stMarkdown"] table {
        font-size: 0.95rem;
        margin: 1rem 0;
        border-collapse: collapse;
    }
    div[data-testid="stMarkdown"] table th, div[data-testid="stMarkdown"] table td {
        padding: 0.5rem 1rem;
        border: 1px solid #e0e0e0;
    }
    .option-button {
        width: 100%;
        text-align: left;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    /* Egységes gomb magasság és igazítás */
    .stButton > button {
        height: 60px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: 10px !important;
    }
    /* Témakör oszlopok egységes magasság */
    .topic-column {
        min-height: 400px;
        display: flex;
        flex-direction: column;
    }
    .topic-column > div {
        flex: 1;
    }
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        background-color: transparent;
        transition: all 0.3s ease;
    }
    .option-button:hover {
        background-color: #e9ecef;
        border-color: #1f77b4;
    }
    .option-button.selected {
        background-color: #1f77b4;
        color: white;
        border-color: #1f77b4;
    }
    .option-button.correct {
        background-color: #28a745;
        color: white;
        border-color: #28a745;
    }
    .option-button.incorrect {
        background-color: #dc3545;
        color: white;
        border-color: #dc3545;
    }
    .score-display {
        font-size: 1.2rem;
        font-weight: bold;
        text-align: center;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin: 1rem 0;
        color: #333;
    }
    .summary-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
        color: #333;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .summary-box h3, .summary-box h4 {
        color: #1f77b4;
        margin-bottom: 0.75rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    .summary-box p {
        color: #333;
        margin: 0.5rem 0;
        font-size: 1rem;
        line-height: 1.4;
    }
    .summary-box strong {
        color: #1f77b4;
        font-weight: 600;
    }
    .mode-info {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .timer-warning {
        background-color: #ffc107;
        color: #333;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .timer-danger {
        background-color: #dc3545;
        color: white;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 2rem 0;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .image-container img {
        max-width: 100%;
        height: auto;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .image-container img:hover {
        transform: scale(1.05);
    }
    .image-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        cursor: pointer;
        backdrop-filter: blur(5px);
    }
    .modal-buttons {
        position: fixed;
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1001;
        background-color: rgba(255,255,255,0.9);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    .image-modal img {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.5);
    }
    .image-caption {
        text-align: center;
        font-style: italic;
        color: #666;
        margin-top: 0.5rem;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

# Quiz adatok témakörök szerint csoportosítva
QUIZ_DATA_BY_TOPIC = {
    "földrajz": FOLDRAJZ_QUESTIONS,
    "komolyzene": KOMOLYZENE_QUESTIONS,
    "magyar_zenekarok": MAGYAR_ZENEKAROK_QUESTIONS_UJ,
    "nemzetkozi_zenekarok": NEMZETKOZI_ZENEKAROK_QUESTIONS,
    "one_hit_wonders": ONE_HIT_WONDERS_QUESTIONS,
    "sorozat_focimek": SOROZAT_FOCIMEK_QUESTIONS,
    "háborúk": HABORU_QUESTIONS_ALL,
    "magyar_királyok": KIRALYOK_QUESTIONS,
    "tudósok": TUDOSOK_QUESTIONS,
    "mitológia": MITOLOGIA_QUESTIONS_ALL,
    "állatok": ALLATOK_QUESTIONS_BALANCED,
    "drámák": DRAMAK_QUESTIONS,
    "sport_logók": SPORT_LOGOK_QUESTIONS,
    "zászlók": ZASZLOK_QUESTIONS_ALL,
    "zaszlok_reszletek": ZASZLOK_RESZLETEK_QUESTIONS,
    "idióta_szavak": IDIOTA_SZAVAK_QUESTIONS,
    "festmények": FESTMENY_QUESTIONS,
    "magyar_festmenyek": MAGYAR_FESTMENYEK_QUESTIONS,
    "regények": REGÉNYEK_QUESTIONS,
    "labdarugo_palyafutas": LABDARUGO_PALYAFUTAS_QUESTIONS,
}

# Initialize session state
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = 'selection'
    st.session_state.selected_topics = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = []
    st.session_state.show_image_modal = False
    st.session_state.image_modal_states = {}  # Külön modal állapot minden kérdéshez
    st.session_state.quiz_start_time = None
    st.session_state.mode_manager = QuizModeManager()
    st.session_state.analytics = QuizAnalytics()
    st.session_state.question_start_time = None
    st.session_state.font_size = 'normal'  # 'normal' vagy 'large'

def get_font_style():
    """Betűméret stílus visszaadása a jelenlegi beállítás alapján"""
    font_size = st.session_state.get('font_size', 'normal')
    
    if font_size == 'large':
        return {
            'question': 'font-size: 1.8rem !important; line-height: 1.4;',
            'option': 'font-size: 1.4rem !important; line-height: 1.3; padding: 12px;',
            'explanation': 'font-size: 1.3rem !important; line-height: 1.4;',
            'button': 'font-size: 1.2rem !important; padding: 12px 24px;',
            'title': 'font-size: 2.2rem !important;',
            'subtitle': 'font-size: 1.6rem !important;'
        }
    else:  # normal
        return {
            'question': 'font-size: 1.4rem !important; line-height: 1.3;',
            'option': 'font-size: 1.1rem !important; line-height: 1.2; padding: 8px;',
            'explanation': 'font-size: 1.1rem !important; line-height: 1.3;',
            'button': 'font-size: 1rem !important; padding: 8px 16px;',
            'title': 'font-size: 1.8rem !important;',
            'subtitle': 'font-size: 1.3rem !important;'
        }

def reset_quiz():
    """Quiz állapot visszaállítása"""
    st.session_state.quiz_state = 'selection'
    st.session_state.selected_topics = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = []
    st.session_state.quiz_start_time = None
    st.session_state.question_answers = {}
    st.session_state.question_options = {}
    st.session_state.mode_manager = QuizModeManager()
    st.session_state.question_start_time = None
    st.session_state.show_image_modal = False
    st.session_state.image_modal_states = {}
    
    # Checkbox állapotok törlése
    topics = {
        "földrajz": "🌍 Földrajz",
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar könnyűzene",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi zenekarok",
        "sorozat_focimek": "📺 Sorozat főcímek",
        "festmények": "🎨 Festmények",
        "magyar_festmenyek": "🇭🇺 Magyar festmények",
        "regények": "📚 Regények",
        "háborúk": "⚔️ Háborúk",
        "magyar_királyok": "👑 Magyar királyok",
        "tudósok": "🔬 Tudósok",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "drámák": "🎭 Drámák",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "zaszlok_reszletek": "🔍 Zászlók részlete",
        "idióta_szavak": "🤪 Idióta szavak",
        "labdarugo_palyafutas": "⚽ Labdarúgó pályafutás",
    }
    
    for topic_key in topics.keys():
        checkbox_key = f"topic_{topic_key}"
        if checkbox_key in st.session_state:
            del st.session_state[checkbox_key]

def get_audio_file_for_question(question, topic):
    """Visszaadja az audio fájl elérési útját a kérdéshez"""
    if topic == "magyar_zenekarok" or topic == "magyar_zenekarok_uj":
        if "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_path = get_magyar_audio_uj_path(index)
                if audio_path and os.path.exists(audio_path):
                    return str(audio_path)
            except Exception as e:
                pass
        elif "audio_file" in question and question["audio_file"]:
            # Ha van audio_file mező, próbáljuk közvetlenül az új mappából
            audio_dir = Path(__file__).parent / "audio_files/magyar_zenekarok"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            # Fallback: régi mappa
            audio_dir = Path(__file__).parent / "audio_files_magyar_uj"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
        return None
    elif topic == "nemzetkozi_zenekarok":
        # Nemzetközi zenekarok - audio_file vagy original_index alapú
        if "audio_file" in question and question["audio_file"]:
            # ÚJ: próbáljuk az új mappából
            audio_dir = Path(__file__).parent / "audio_files/nemzetkozi_zenekarok"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            # Fallback: régi mappa
            audio_dir = Path(__file__).parent / "audio_files"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
        elif "original_index" in question:
            try:
                # Biztosan integer legyen az index
                index = int(question["original_index"])
                audio_path = get_nemzetkozi_audio_path(index)
                if audio_path and audio_path.exists():
                    return str(audio_path)
            except Exception as e:
                print(f"[DEBUG] Hiba az original_index használatánál: {e}")
        elif "spotify_embed" in question:
            # Spotify embed esetén próbáljuk meg az original_index alapján találni az audio fájlt
            if "original_index" in question:
                try:
                    # Biztosan integer legyen az index
                    index = int(question["original_index"])
                    audio_path = get_nemzetkozi_audio_path(index)
                    if audio_path and audio_path.exists():
                        return str(audio_path)
                    else:
                        print(f"[DEBUG] Nemzetközi audio fájl nem található index {index}: {audio_path}")
                except Exception as e:
                    print(f"[DEBUG] Hiba az original_index használatánál: {e}")
            else:
                print(f"[DEBUG] Spotify embed található, de nincs original_index")
            pass
    elif topic == "sorozat_focimek":
        # Sorozat főcímek - audio_file alapú
        if "audio_file" in question and question["audio_file"]:
            audio_dir = Path(__file__).parent / "audio_files/sorozat_focimek"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            # Fallback: audio_files gyökér
            audio_dir = Path(__file__).parent / "audio_files"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
    elif topic == "komolyzene":
        # Komolyzene: original_index alapú mapping használata
        audio_dirs = [
            Path(__file__).parent / "audio_files/komolyzene",
        ]
        audio_file = question.get("audio_file")
        if "original_index" in question:
            # ÚJ: komolyzene_audio_mapping.get_komolyzene_audio_path használata
            from komolyzene_audio_mapping import get_komolyzene_audio_path
            try:
                # Biztosan integer legyen az index
                index = int(question["original_index"])
                audio_path = get_komolyzene_audio_path(index)
                if audio_path and audio_path.exists():
                    return str(audio_path)
            except Exception as e:
                pass
        if audio_file:
            # Direkt egyezés
            for audio_dir in audio_dirs:
                audio_path = audio_dir / audio_file
                if audio_path.exists():
                    return str(audio_path)
            # Fallback: sorszám alapján keresés (pl. 43. -> 43_*)
            try:
                import re
                match = re.match(r"^\s*(\d+)", audio_file)
                if match:
                    num = match.group(1)
                    for audio_dir in audio_dirs:
                        if not audio_dir.exists():
                            continue
                        for candidate in audio_dir.glob(f"{num}*"):
                            if not candidate.is_file() or candidate.suffix.lower() != ".mp3":
                                continue
                            if re.match(fr"^{num}(\D|$)", candidate.name):
                                return str(candidate)
            except Exception:
                pass
        # Fallback: zeneszerző alapján (ha pontos fájlnév nincs)
        try:
            import re
            composer_candidates = []
            explanation = question.get("explanation")
            if explanation and ":" in explanation:
                composer_candidates.append(explanation.split(":", 1)[0])
            if "options" in question and "correct" in question:
                options = question.get("options") or []
                correct_index = question.get("correct")
                if isinstance(correct_index, int) and 0 <= correct_index < len(options):
                    composer_candidates.append(options[correct_index])
            if audio_file:
                base = os.path.splitext(os.path.basename(audio_file))[0]
                base = base.replace("Unknown Artist", "").replace("Unknown_Artist", "")
                composer_candidates.append(base)

            def _normalize_text(value: str) -> str:
                cleaned = value.lower().replace("_", " ")
                cleaned = re.sub(r"[^\w\s]", " ", cleaned, flags=re.UNICODE)
                return re.sub(r"\s+", " ", cleaned).strip()

            normalized_candidates = [_normalize_text(c) for c in composer_candidates if c]
            if normalized_candidates:
                matches = []
                for audio_dir in audio_dirs:
                    if not audio_dir.exists():
                        continue
                    for candidate in audio_dir.glob("*.mp3"):
                        candidate_norm = _normalize_text(candidate.stem)
                        if any(c and c in candidate_norm for c in normalized_candidates):
                            matches.append(candidate)
                if len(matches) == 1:
                    return str(matches[0])
                if audio_file:
                    match = re.match(r"^\s*(\d+)", audio_file)
                    if match:
                        num = match.group(1)
                        num_matches = [m for m in matches if re.match(fr"^{num}(\D|$)", m.name)]
                        if len(num_matches) == 1:
                            return str(num_matches[0])
        except Exception:
            pass
    elif topic == "one_hit_wonders":
        # One Hit Wonders audio fájl kezelése
        if "original_index" in question:
            try:
                # Audio fájl elérési útja az új mappából
                index = int(question["original_index"])
                audio_dir = Path(__file__).parent / "audio_files"
                # Fájlnév keresése az index alapján
                for filename in os.listdir(audio_dir):
                    if filename.endswith('.mp3') and filename.startswith(f"{index:02d}_"):
                        audio_path = audio_dir / filename
                        if audio_path.exists():
                            # Audio fájl megtalálva
                            return str(audio_path)
            except Exception as e:
                pass
        
        # Fallback: dal cím alapján keresés
        try:
            import re
            # Keresd meg a dal címét a kérdésben
            question_text = question.get("question", "")
            # Keresd meg a 'dal cím' mintát
            match = re.search(r"'([^']+)'", question_text)
            if match:
                song_title = match.group(1)
                # Keresd meg a megfelelő audio fájlt a One Hit Wonders almappában
                audio_dir = Path(__file__).parent / "audio_files/one_hit_wonders"
                if audio_dir.exists():
                    for filename in os.listdir(audio_dir):
                        # Normalizáljuk a keresést: szóköz -> aláhúzás
                        normalized_song_title = song_title.lower().replace(' ', '_')
                        normalized_filename = filename.lower()
                        if filename.endswith('.mp3') and (song_title.lower() in normalized_filename or normalized_song_title in normalized_filename):
                            audio_path = audio_dir / filename
                            if audio_path.exists():
                                return str(audio_path)
        except Exception as e:
            pass
            
        # Spotify preview URL fallback
        if "spotify_preview_url" in question and question["spotify_preview_url"]:
            return question["spotify_preview_url"]
        return None
    else:
        # Egyéb témakörök - youtube_audio_mapping használata
        if "original_index" in question:
            try:
                # Biztosan integer legyen az index
                index = int(question["original_index"])
                audio_filename = get_youtube_audio_filename_cached(index, topic)
                if audio_filename:
                    audio_dir = Path(__file__).parent / "audio_files"
                    audio_path = audio_dir / audio_filename
                    if audio_path.exists():
                        return str(audio_path)
            except Exception as e:
                print(f"[DEBUG] Hiba az egyéb témakör original_index használatánál: {e}")
    return None

def show_answer_popup(question, user_answer, correct_answer):
    """Tartós popup üzenet a válaszról és helyes válaszról"""
    music_topics = {"komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"}
    topic = question.get("topic") if isinstance(question, dict) else None
    show_piece_title = bool(
        topic in music_topics
        or (isinstance(question, dict) and (question.get("audio_file") or question.get("spotify_embed")))
    )
    piece_title = _get_piece_title_for_question(question) if show_piece_title else None
    if piece_title:
        piece_title = translate_text(piece_title)

    st.session_state.answer_popup = {
        "user_answer": user_answer if user_answer else t("N/A"),
        "correct_answer": correct_answer if correct_answer else t("N/A"),
        "piece_title": piece_title,
    }

def render_answer_popup():
    """Popup megjelenítése, amíg a felhasználó be nem zárja"""
    popup = st.session_state.get("answer_popup")
    if not popup:
        return

    st.markdown(
        """
        <style>
        .answer-popup {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #1f2937;
            color: #ffffff;
            padding: 16px 20px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            z-index: 10000;
            max-width: 90%;
            width: 900px;
            font-size: 16px;
            pointer-events: none;
            animation: answerPopupFadeOut 0.4s ease 3.5s forwards;
        }

        @keyframes answerPopupFadeOut {
            to {
                opacity: 0;
                visibility: hidden;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    piece_line = ""
    if "piece_title" in popup:
        piece_value = popup["piece_title"] or t("N/A")
        piece_line = f"<br/><strong>{t('Darab címe:')}</strong> {piece_value}"

    user_answer_label = t("Válaszod:")
    correct_answer_label = t("Helyes válasz:")

    st.markdown(
        f"""
        <div class="answer-popup">
            <strong>{user_answer_label}</strong> {popup["user_answer"]}
            &nbsp;|&nbsp;
            <strong>{correct_answer_label}</strong> {popup["correct_answer"]}
            {piece_line}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Egyszeri megjelenítés: a következő rerunban már nem jelenik meg
    st.session_state.pop("answer_popup", None)

def start_quiz():
    """Quiz indítása"""
    if not st.session_state.selected_topics:
        st.error(t("Kérlek válassz ki legalább egy témaköröt!"))
        return
    
    player_name = st.session_state.get("selected_player", "").strip()
    if not player_name:
        st.error(t("Add meg a neved a quiz indításához."))
        return
    st.session_state.selected_player = player_name
    
    # Végleges kérdésszám használata - ha nincs beállítva, akkor 0 (a tényleges kérdések számától függ)
    final_question_count = st.session_state.get('final_question_count', 0)
    
    all_questions = []
    total_selected_questions = 0
    invalid_questions = 0
    
    # Minden témakör kezelése egyedi sliders alapján
    for topic in st.session_state.selected_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            print(f"[DEBUG] {topic} összes kérdés: {len(topic_questions)}")
            # Egyedi témakör slider használata
            questions_count = st.session_state.get(f'final_{topic}_questions', min(3, len(topic_questions)))
            # Ha nincs beállítva slider érték, használjuk az alapértelmezett értéket
            if questions_count == 0:
                questions_count = min(3, len(topic_questions))
            questions_count = min(questions_count, len(topic_questions))
            print(f"[DEBUG] {topic} kiválasztott kérdésszám: {questions_count}")
            
            if questions_count > 0:
                total_selected_questions += questions_count
                # Véletlenszerű kérdések kiválasztása
                selected_indices = random.sample(range(len(topic_questions)), questions_count)
                for idx in selected_indices:
                    question = topic_questions[idx].copy()
                    # Ellenőrizzük, hogy a kérdés rendelkezik-e a szükséges mezőkkel
                    # Text input kérdések esetén correct_answer mezőt használunk
                    if question.get("question_type") == "text_input":
                        if "correct_answer" not in question:
                            invalid_questions += 1
                            continue
                    else:
                        # Többválasztós kérdések esetén options és correct mezők szükségesek
                        if "options" not in question or "correct" not in question:
                            invalid_questions += 1
                            continue
                    question['topic'] = topic
                    

                    # --- Magyar zenekarok: opciók és helyes válasz igazítása ---
                    if topic == "magyar_zenekarok" or topic == "magyar_zenekarok_uj":
                        # A fájlnév alapján keressük meg a mapping indexét
                        audio_file = question.get("audio_file", "")
                        if audio_file:
                            # Keressük meg a fájlt a mappingben
                            mapping_index = None
                            for map_idx, map_fname in MAGYAR_AUDIO_MAPPING_UJ.items():
                                if map_fname == audio_file:
                                    mapping_index = map_idx
                                    break
                            
                            if mapping_index is not None:
                                question['original_index'] = mapping_index
                                # A mappingből kinyerjük a helyes előadót
                                mapping_fname = MAGYAR_AUDIO_MAPPING_UJ.get(mapping_index)
                                if mapping_fname:
                                    # Előadó név a fájlnévből (első kétjegyű szám + _ levágva, .mp3 nélkül)
                                    artist = mapping_fname.split('_', 1)[-1].replace('.mp3', '').replace('_', ' ')
                                    # Csak akkor adjuk hozzá, ha nincs már a listában
                                    if artist not in question["options"]:
                                        question["options"].append(artist)
                                    # A helyes válasz indexét állítjuk be
                                    if artist in question["options"]:
                                        question["correct"] = question["options"].index(artist)
                            else:
                                print(f"[DEBUG] Fájl nem található a mappingben: {audio_file}")
                                question['original_index'] = idx  # Fallback
                        else:
                            question['original_index'] = idx  # Fallback
                    else:
                        # One Hit Wonders esetén megtartjuk az eredeti original_index-et
                        if topic == "one_hit_wonders":
                            # Az original_index már be van állítva a kérdésben, ne módosítsuk
                            pass
                        else:
                            question['original_index'] = idx
                    all_questions.append(question)
    
    if not all_questions:
        st.error(t("Nem található érvényes kérdés a kiválasztott témakörökben!"))
        if invalid_questions > 0:
            st.warning(
                t(
                    "{count} érvénytelen kérdés kihagyva (hiányzó adatok)",
                    count=invalid_questions,
                )
            )
        return
    
    # Kérdések keverése
    random.shuffle(all_questions)
    
    # Végleges kérdésszám alkalmazása - csak akkor, ha több kérdés van, mint amit kértünk
    if final_question_count > 0 and len(all_questions) > final_question_count:
        all_questions = all_questions[:final_question_count]
    
    if final_question_count > 0:
        st.info(
            t(
                "Kiválasztott kérdések: {selected} / {limit}",
                selected=len(all_questions),
                limit=final_question_count,
            )
        )
    else:
        st.info(t("Kiválasztott kérdések: {selected}", selected=len(all_questions)))
    if invalid_questions > 0:
        st.warning(t("{count} érvénytelen kérdés kihagyva", count=invalid_questions))
    
    st.session_state.quiz_questions = all_questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_state = 'quiz'
    st.session_state.quiz_start_time = datetime.now()
    st.session_state.question_start_time = datetime.now()
    st.rerun()

def main():
    """Fő alkalmazás"""
    # Session state inicializálása
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = 'selection'
    if 'selected_topics' not in st.session_state:
        st.session_state.selected_topics = []
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = []
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'quiz_start_time' not in st.session_state:
        st.session_state.quiz_start_time = None
    if 'question_answers' not in st.session_state:
        st.session_state.question_answers = {}
    if 'question_options' not in st.session_state:
        st.session_state.question_options = {}
    if 'mode_manager' not in st.session_state:
        st.session_state.mode_manager = QuizModeManager()
    if 'question_start_time' not in st.session_state:
        st.session_state.question_start_time = None
    if 'show_image_modal' not in st.session_state:
        st.session_state.show_image_modal = False
    if 'image_modal_states' not in st.session_state:
        st.session_state.image_modal_states = {}
    if 'other_total_questions' not in st.session_state:
        st.session_state.other_total_questions = st.session_state.get('default_other_questions', 40)
    if 'music_total_questions' not in st.session_state:
        st.session_state.music_total_questions = st.session_state.get('default_music_questions', 10)
    if 'selected_player' not in st.session_state:
        st.session_state.selected_player = ""
    
    font_style = get_font_style()
    header_col_left, header_col_right = st.columns([6, 1])
    with header_col_right:
        render_language_selector()
    st.markdown(
        f'<h1 style="text-align: center; {font_style["title"]} color: #1f77b4; margin-bottom: 2rem;">{t("🎯 Csabagyöngye Tréning Center 😄")}</h1>',
        unsafe_allow_html=True,
    )
    
    # Sidebar navigáció
    with st.sidebar:
        st.markdown(t("## 🧭 Navigáció"))
        page_labels = {
            "Quiz": "🎯 Quiz",
            "Spotify Playlist": "🎵 Spotify Playlist",
            "Analytics": "📊 Analytics",
            "Beállítások": "⚙️ Beállítások",
            "Audio hozzáadása": "🎵 Audio hozzáadása",
            "GitHub Szinkronizálás": "🔄 GitHub Szinkronizálás",
            "Audio Track Kezelés": "🎵 Audio Track Kezelés",
            "Előadók szerinti lista": "🎼 Előadók szerinti lista",
        }
        page = st.selectbox(
            t("Válassz oldalt:"),
            list(page_labels.keys()),
            format_func=lambda x: t(page_labels[x]),
        )
        
        # Betűméret váltó
        st.markdown("---")
        st.markdown(t("## 🔤 Betűméret"))
        font_size_options = {
            "normal": "📝 Normál",
            "large": "🔍 Nagy"
        }
        
        current_font = st.session_state.get('font_size', 'normal')
        new_font = st.selectbox(
            t("Válassz betűméretet:"),
            options=list(font_size_options.keys()),
            format_func=lambda x: t(font_size_options[x]),
            index=list(font_size_options.keys()).index(current_font)
        )
        
        if new_font != current_font:
            st.session_state.font_size = new_font
            st.rerun()

        st.markdown("---")
        if st.button(t("🗑️ Cache törlése")):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success(t("Cache törölve!"))
            st.rerun()
        
                # Spotify playlist funkció eltávolítva a navigációs sávból
        # Most a középső képernyőn lesz elérhető
    
    if page == "Quiz":
        show_quiz_page()
    elif page == "Analytics":
        show_analytics_page()
    elif page == "Beállítások":
        show_settings_page()
    elif page == "Spotify Playlist":
        show_spotify_playlist_main()
    elif page == "Audio hozzáadása":
        show_audio_addition_page()
    elif page == "GitHub Szinkronizálás":
        show_github_sync_page()
    elif page == "Audio Track Kezelés":
        show_audio_track_management_page()
    elif page == "Előadók szerinti lista":
        show_artist_list_page()

def show_quiz_page():
    """Quiz oldal megjelenítése"""
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()
    elif st.session_state.quiz_state == 'results':
        show_results()

def get_all_audio_tracks():
    """Összes audio track összegyűjtése"""
    all_tracks = []
    
    # Minden lehetséges audio könyvtár
    audio_dirs = [
        "audio_files",
        "audio_files/sorozat_focimek",
        "magyar_audio", 
        "nemzetkozi_audio",
        "komolyzene_audio",
        "one_hit_wonders_audio"
    ]
    
    # Minden lehetséges formátum
    audio_extensions = ["*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg"]
    
    for audio_dir in audio_dirs:
        if os.path.exists(audio_dir):
            for ext in audio_extensions:
                audio_files = glob.glob(f"{audio_dir}/{ext}")
                for audio_file in audio_files:
                    track_name = os.path.splitext(os.path.basename(audio_file))[0]
                    
                    # Duplikációk elkerülése
                    if not any(track["name"] == track_name for track in all_tracks):
                        all_tracks.append({
                            "name": track_name,
                            "audio_path": audio_file,
                            "directory": audio_dir
                        })
    
    return all_tracks

def get_audio_tracks_by_category():
    """Audio track-ek kategóriánként összegyűjtése"""
    categories = {
        "magyar_zenekarok": {
            "title": "🎵 Magyar Zenekarok",
            "audio_dirs": ["audio_files/magyar_zenekarok", "audio_files"],
            "question_file": "topics/magyar_zenekarok_uj.py"
        },
        "nemzetkozi_zenekarok": {
            "title": "🌍 Nemzetközi Zenekarok", 
            "audio_dirs": ["audio_files/nemzetkozi_zenekarok", "audio_files"],
            "question_file": "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py"
        },
        "komolyzene": {
            "title": "🎼 Komolyzene",
            "audio_dirs": ["audio_files/komolyzene", "audio_files"], 
            "question_file": "topics/komolyzene_uj.py"
        },
        "one_hit_wonders": {
            "title": "⭐ One Hit Wonders",
            "audio_dirs": ["audio_files/one_hit_wonders", "audio_files"],
            "question_file": "topics/one_hit_wonders.py"
        },
        "sorozat_focimek": {
            "title": "📺 Sorozat főcímek",
            "audio_dirs": ["audio_files/sorozat_focimek", "audio_files"],
            "question_file": "topics/sorozat_focimek.py"
        }
    }
    
    tracks_by_category = {}
    
    for category_key, category_info in categories.items():
        tracks = []
        audio_dirs = category_info["audio_dirs"]
        question_file = category_info["question_file"]
        
        # Audiofájlok keresése minden könyvtárban
        for audio_dir in audio_dirs:
            if os.path.exists(audio_dir):
                # MP3, WAV, M4A fájlok keresése
                for ext in ["*.mp3", "*.wav", "*.m4a"]:
                    audio_files = glob.glob(f"{audio_dir}/{ext}")
                    
                    for audio_file in audio_files:
                        track_name = os.path.splitext(os.path.basename(audio_file))[0]
                        
                        # Duplikációk elkerülése
                        if not any(track["name"] == track_name for track in tracks):
                            tracks.append({
                                "name": track_name,
                                "audio_path": audio_file,
                                "question_file": question_file
                            })
        
        tracks_by_category[category_key] = {
            "title": category_info["title"],
            "tracks": tracks
        }
    
    return tracks_by_category

def _parse_artist_and_title(track_name: str):
    """Egyszerű előadó és cím kinyerés track névből"""
    name = track_name.strip()
    if ". " in name:
        name = name.split(". ", 1)[1]
    if " - " in name:
        artist, title = name.split(" - ", 1)
        return artist.strip(), title.strip()
    if "_" in name:
        parts = [p for p in name.split("_") if p]
        if parts and parts[0].isdigit():
            parts = parts[1:]
        if len(parts) >= 2:
            return parts[0].replace("_", " ").strip(), " ".join(parts[1:]).replace("_", " ").strip()
    return "Ismeretlen", name

def _parse_artist_title_from_youtube(youtube_title: str, channel: Optional[str] = None):
    """YouTube cím alapján előadó és cím kinyerése"""
    import re
    if not youtube_title:
        return channel or "Ismeretlen", "Ismeretlen cím"

    title = str(youtube_title).strip()
    # Felesleges zárójelek eltávolítása (pl. Official, HD)
    title = re.sub(r"\s*\[[^\]]*\]\s*", " ", title)
    title = re.sub(r"\s*\([^)]*\)\s*", " ", title)
    title = re.sub(r"\s+", " ", title).strip()

    for sep in [" - ", " – ", " — ", " | "]:
        if sep in title:
            artist, song = title.split(sep, 1)
            return artist.strip() or (channel or "Ismeretlen"), song.strip() or title

    if channel:
        return channel.strip(), title
    return "Ismeretlen", title

def _get_piece_title_for_question(question: dict) -> Optional[str]:
    """Darab címének becsült kinyerése a kérdésből"""
    if not isinstance(question, dict):
        return None
    song_title = question.get("song_title")
    if song_title:
        return str(song_title).strip().strip('"')
    explanation = question.get("explanation")
    if explanation:
        explanation = str(explanation).strip()
        if ":" in explanation:
            title = explanation.split(":", 1)[1].strip()
            if title:
                return title
        if " - " in explanation:
            title = explanation.split(" - ", 1)[1].strip()
            if title:
                return title
    audio_file = question.get("audio_file")
    if audio_file:
        filename = os.path.splitext(os.path.basename(str(audio_file)))[0]
        _, title = _parse_artist_and_title(filename)
        if title and title != "Ismeretlen":
            return title.strip()
        cleaned = filename
        if ". " in cleaned:
            cleaned = cleaned.split(". ", 1)[1]
        cleaned = cleaned.replace("_", " ").strip()
        return cleaned or None
    return None

def show_artist_list_page():
    """Szerző szerinti lista önálló oldal"""
    st.markdown(
        f'<h2 style="text-align: center; color: #1f77b4;">{t("🎼 Szerző szerinti lista")}</h2>',
        unsafe_allow_html=True,
    )
    
    tracks_by_category = get_audio_tracks_by_category()
    music_categories = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"]
    music_options = {k: v["title"] for k, v in tracks_by_category.items() if k in music_categories}
    
    if not music_options:
        st.info(t("📭 Nincs elérhető zenei kategória."))
        return
    
    st.markdown(t("### 🎵 Zenei kategória választás"))
    current_category = st.session_state.get("artist_list_category", list(music_options.keys())[0])
    selected_category = None
    cols = st.columns(2)
    for i, (key, title) in enumerate(music_options.items()):
        with cols[i % 2]:
            button_type = "primary" if key == current_category else "secondary"
            if st.button(t(title), key=f"artist_list_cat_{key}", type=button_type, use_container_width=True):
                selected_category = key
                st.session_state.artist_list_category = key
                st.rerun()
    if selected_category is None:
        selected_category = current_category
    
    category_info = tracks_by_category.get(selected_category, {})
    tracks = category_info.get("tracks", [])
    if not tracks:
        st.info(t("📭 Nincsenek track-ek ebben a kategóriában."))
        return
    
    if "artist_list_playing" not in st.session_state:
        st.session_state.artist_list_playing = None

    artist_map = {}
    for track in tracks:
        artist, title = _parse_artist_and_title(track.get("name", ""))
        audio_path = track.get("audio_path")
        filename = os.path.basename(audio_path) if audio_path else "N/A"
        artist_map.setdefault(artist, []).append({
            "title": title,
            "filename": filename,
            "audio_path": audio_path,
        })
    
    st.markdown(t("### {category}", category=t(category_info.get("title", selected_category))))
    st.markdown(
        t(
            "📊 **{track_count} track**, **{artist_count} előadó**",
            track_count=len(tracks),
            artist_count=len(artist_map),
        )
    )
    
    for artist in sorted(artist_map.keys(), key=lambda x: x.lower()):
        items = sorted(artist_map[artist], key=lambda x: x["title"].lower())
        with st.expander(t("{artist} ({count})", artist=artist, count=len(items)), expanded=False):
            for idx, item in enumerate(items):
                title = item["title"]
                filename = item["filename"]
                audio_path = item["audio_path"]
                has_audio = bool(audio_path and os.path.exists(audio_path))

                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(t("{title} ({filename})", title=title, filename=filename))
                with col2:
                    if not has_audio:
                        st.button(t("▶️ Lejátszás"), key=f"play_{selected_category}_{artist}_{idx}", disabled=True)
                    else:
                        if st.session_state.artist_list_playing == audio_path:
                            if st.button(t("⏹ Stop"), key=f"stop_{selected_category}_{artist}_{idx}"):
                                st.session_state.artist_list_playing = None
                        else:
                            if st.button(t("▶️ Lejátszás"), key=f"play_{selected_category}_{artist}_{idx}"):
                                st.session_state.artist_list_playing = audio_path

                if has_audio and st.session_state.artist_list_playing == audio_path:
                    st.audio(audio_path, format="audio/mp3")

                if has_audio:
                    with st.expander(t("🔧 Audio módosítás"), expanded=False):
                        st.caption(t("A feltöltött fájl felülírja az eredeti tracket (név változatlan)."))
                        uploaded_file = st.file_uploader(
                            t("Új MP3 feltöltése"),
                            type=["mp3"],
                            key=f"upload_{selected_category}_{artist}_{idx}",
                        )
                        confirm_replace = st.checkbox(
                            t("Igen, felülírom az eredeti fájlt"),
                            key=f"confirm_replace_{selected_category}_{artist}_{idx}",
                        )
                        if st.button(t("💾 Csere mentése"), key=f"replace_{selected_category}_{artist}_{idx}"):
                            if uploaded_file is None:
                                st.warning(t("⚠️ Előbb válassz ki egy MP3 fájlt!"))
                            elif not confirm_replace:
                                st.warning(t("⚠️ Jelöld be a megerősítést a felülíráshoz!"))
                            else:
                                try:
                                    import tempfile
                                    from pathlib import Path

                                    target_path = Path(audio_path)
                                    with tempfile.NamedTemporaryFile(delete=False, dir=str(target_path.parent), suffix=target_path.suffix) as tmp:
                                        tmp.write(uploaded_file.getbuffer())
                                        tmp_path = tmp.name
                                    os.replace(tmp_path, target_path)

                                    # Cache frissítése
                                    cache_keys_to_delete = []
                                    for key in st.session_state.keys():
                                        if (key.startswith("audio_track_data_") or
                                            key.startswith("duration_") or
                                            key.startswith("track_cache_")):
                                            cache_keys_to_delete.append(key)
                                    for key in cache_keys_to_delete:
                                        if key in st.session_state:
                                            del st.session_state[key]
                                    st.session_state['force_refresh'] = True

                                    # Git szinkronizáció
                                    try:
                                        subprocess.run(['git', 'add', str(target_path)], check=True)
                                        commit_msg = f"Replace audio: {artist} - {title}"
                                        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                                        subprocess.run(['git', 'push'], check=True)
                                        st.success(t("✅ Audio cserélve és GitHub-ra feltöltve."))
                                    except subprocess.CalledProcessError as e:
                                        st.warning(t("⚠️ Git szinkronizáció sikertelen: {error}", error=e))
                                        st.success(t("✅ Audio cserélve, de Git sync nem futott le."))

                                    # Lejátszás reset
                                    if st.session_state.artist_list_playing == str(target_path):
                                        st.session_state.artist_list_playing = None
                                    st.rerun()
                                except Exception as e:
                                    st.error(t("❌ Audio csere hiba: {error}", error=e))

def _make_safe_filename(artist: str, title: str) -> str:
    """Biztonságos fájlnév generálása az előadó és cím alapján"""
    import re
    safe_artist = re.sub(r'[^\w\s-]', '', artist).strip() or "Ismeretlen"
    safe_title = re.sub(r'[^\w\s-]', '', title).strip() or "Ismeretlen"
    safe_artist = re.sub(r'[-\s]+', '_', safe_artist)[:30]
    safe_title = re.sub(r'[-\s]+', '_', safe_title)[:40]
    return f"{safe_artist}_{safe_title}.mp3"

def load_questions_from_file(file_path):
    """Kérdések betöltése Python fájlból"""
    try:
        if not os.path.exists(file_path):
            return []
        
        # 1. Próbáljuk meg közvetlenül importálni a fájlt
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("questions_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Különböző kérdés változók keresése
            question_vars = ['QUESTIONS', 'NEMZETKOZI_ZENEKAROK_QUESTIONS', 'ONE_HIT_WONDERS_QUESTIONS', 'MAGYAR_ZENEKAROK_QUESTIONS', 'KOMOLYZENE_QUESTIONS']
            
            for var_name in question_vars:
                if hasattr(module, var_name):
                    questions = []
                    question_list = getattr(module, var_name)
                    for q in question_list:
                        if isinstance(q, dict) and 'question' in q and 'options' in q and 'correct' in q:
                            question_data = {
                                "question": q['question'],
                                "options": q['options'],
                                "correct": q['correct']
                            }
                            # További mezők hozzáadása, ha vannak
                            if 'audio_file' in q:
                                question_data['audio_file'] = q['audio_file']
                            if 'spotify_embed' in q:
                                question_data['spotify_embed'] = q['spotify_embed']
                            if 'explanation' in q:
                                question_data['explanation'] = q['explanation']
                            if 'topic' in q:
                                question_data['topic'] = q['topic']
                            questions.append(question_data)
                    if questions:
                        return questions
        except Exception as import_error:
            pass
        
        # 2. Ha az import nem sikerült, regex-szel próbáljuk
        # Fájl tartalmának beolvasása
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Kérdések kinyerése regex-szel
        import re
        questions = []
        
        # Kérdés minták keresése - bővített minták
        question_patterns = [
            r'{\s*"question":\s*"([^"]+)",\s*"options":\s*\[([^\]]+)\],\s*"correct":\s*(\d+)\s*}',
            r'{\s*"question":\s*"([^"]+)",\s*"options":\s*\[([^\]]+)\],\s*"correct_answer":\s*(\d+)\s*}',
            r'{\s*"question":\s*"([^"]+)",\s*"options":\s*\[([^\]]+)\],\s*"correct":\s*(\d+)\s*,',
            r'{\s*"question":\s*"([^"]+)",\s*"options":\s*\[([^\]]+)\],\s*"correct_answer":\s*(\d+)\s*,'
        ]
        
        for pattern in question_patterns:
            matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                question_text = match[0]
                options_str = match[1]
                correct = int(match[2])
                
                # Opciók feldolgozása
                options = []
                option_matches = re.findall(r'"([^"]+)"', options_str)
                options = option_matches
                
                if len(options) >= 4:
                    question_data = {
                        "question": question_text,
                        "options": options,
                        "correct": correct
                    }
                    
                    # További mezők keresése a kérdés környékén
                    # Audio file keresése
                    audio_match = re.search(r'"audio_file":\s*"([^"]+)"', content)
                    if audio_match:
                        question_data['audio_file'] = audio_match.group(1)
                    
                    # Spotify embed keresése
                    spotify_match = re.search(r'"spotify_embed":\s*"([^"]+)"', content)
                    if spotify_match:
                        question_data['spotify_embed'] = spotify_match.group(1)
                    
                    questions.append(question_data)
        
        return questions
    except Exception as e:
        st.error(f"Hiba a kérdések betöltésekor: {e}")
        return []

def find_matching_question(track_name, questions):
    """Kérdés keresése track név alapján"""
    track_name_lower = track_name.lower()
    
    # 1. Audio file alapján keresés (legpontosabb)
    for q in questions:
        if 'audio_file' in q:
            audio_file = q['audio_file'].lower()
            # Kiterjesztés nélküli fájlnév összehasonlítása
            audio_file_no_ext = os.path.splitext(audio_file)[0]
            track_name_no_ext = os.path.splitext(track_name)[0]
            
            if audio_file_no_ext == track_name_no_ext:
                return q
            
            # Ha a track név szám előtaggal van (pl. "37_Pokolgép"), 
            # próbáljuk meg a szám nélküli verziót is
            if '_' in track_name_no_ext and track_name_no_ext.split('_')[0].isdigit():
                track_name_without_number = '_'.join(track_name_no_ext.split('_')[1:])
                if audio_file_no_ext.endswith(track_name_without_number):
                    return q
    
    # 2. Pontos egyezés keresése a kérdésben
    for q in questions:
        if track_name_lower in q['question'].lower() or q['question'].lower() in track_name_lower:
            return q
    
    # 3. Ha nincs pontos egyezés, keresés a track nevének részei alapján
    track_words = [word.strip() for word in track_name_lower.replace('-', ' ').replace('_', ' ').split() if len(word.strip()) > 2]
    
    for q in questions:
        question_lower = q['question'].lower()
        # Ellenőrizzük, hogy a track szavak közül hány szerepel a kérdésben
        matching_words = sum(1 for word in track_words if word in question_lower)
        if matching_words >= 2:  # Legalább 2 szó egyezik
            return q
    
    # 4. Ha még mindig nincs találat, keresés az előadó neve alapján
    if '-' in track_name_lower:
        artist_name = track_name_lower.split('-')[0].strip()
        for q in questions:
            if artist_name in q['question'].lower():
                return q
    
    return None



def check_github_sync_status():
    """GitHub szinkronizáció állapotának ellenőrzése"""
    try:
        # Git status ellenőrzése
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
        
        if result.returncode != 0:
            return {"error": "Git status hiba", "details": result.stderr}
        
        local_changes = result.stdout.strip()
        
        # Remote fetch
        fetch_result = subprocess.run(['git', 'fetch', 'origin'], 
                                    capture_output=True, text=True, cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
        
        if fetch_result.returncode != 0:
            return {"error": "Git fetch hiba", "details": fetch_result.stderr}
        
        # Remote és local branch összehasonlítása
        diff_result = subprocess.run(['git', 'diff', 'HEAD', 'origin/main', '--name-only'], 
                                   capture_output=True, text=True, cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
        
        if diff_result.returncode != 0:
            return {"error": "Git diff hiba", "details": diff_result.stderr}
        
        remote_changes = diff_result.stdout.strip()
        
        return {
            "local_changes": local_changes,
            "remote_changes": remote_changes,
            "has_local_changes": bool(local_changes),
            "has_remote_changes": bool(remote_changes)
        }
        
    except Exception as e:
        return {"error": "Szinkronizáció ellenőrzés hiba", "details": str(e)}


def show_github_sync_dialog():
    """GitHub szinkronizáció dialógus megjelenítése"""
    st.markdown("### 🔄 GitHub Szinkronizáció")
    
    # Szinkronizáció állapot ellenőrzése
    with st.spinner("GitHub állapot ellenőrzése..."):
        sync_status = check_github_sync_status()
    
    if "error" in sync_status:
        st.error(f"❌ Hiba a szinkronizáció ellenőrzése során: {sync_status['error']}")
        if sync_status.get('details'):
            st.code(sync_status['details'])
        return False
    
    # Lokális változások megjelenítése
    if sync_status["has_local_changes"]:
        st.warning("⚠️ **Lokális változások vannak:**")
        st.code(sync_status["local_changes"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lokális változások mentése", type="primary"):
                try:
                    subprocess.run(['git', 'add', '.'], cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
                    subprocess.run(['git', 'commit', '-m', 'Auto-save before sync'], cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
                    subprocess.run(['git', 'push'], cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
                    st.success("✅ Lokális változások mentve!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba a mentés során: {e}")
        
        with col2:
            if st.button("🗑️ Lokális változások eldobása", type="secondary"):
                try:
                    subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
                    st.success("✅ Lokális változások eldobva!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba az eldobás során: {e}")
        
        st.markdown("---")
    
    # Remote változások megjelenítése
    if sync_status["has_remote_changes"]:
        st.info("📥 **Új változások érkeztek a GitHub-ról:**")
        st.code(sync_status["remote_changes"])
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Változások letöltése", type="primary"):
                try:
                    subprocess.run(['git', 'pull', 'origin', 'main'], cwd='/Users/zsigagabor/qr_decoder_project/pdf_analyzer_project')
                    st.success("✅ Változások letöltve!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba a letöltés során: {e}")
        
        with col2:
            if st.button("⏭️ Kihagyás", type="secondary"):
                st.info("ℹ️ Változások kihagyva. Folytathatod a munkát.")
        
        st.markdown("---")
    
    # Ha nincs változás
    if not sync_status["has_local_changes"] and not sync_status["has_remote_changes"]:
        st.success("✅ **Minden szinkronizálva!** Nincs új változás.")
        
        if st.button("🔄 Frissítés ellenőrzése", type="secondary"):
            st.rerun()
    
    return True


def show_audio_track_management_page():
    """Audio track kezelési oldal megjelenítése"""
    st.markdown('<h2 style="text-align: center; color: #1f77b4;">🎵 Audio Track Kezelés</h2>', unsafe_allow_html=True)
    
    # GitHub szinkronizáció megjelenítése
    if not show_github_sync_dialog():
        return
    
    st.markdown("""
    ### 📋 Mit csinál ez a funkció?
    
    Ez a funkció lehetővé teszi, hogy:
    - 📁 **Megtekintsd az összes audio track-et** táblázatos formában
    - ✏️ **Szerkeszd a válaszopciókat** közvetlenül a táblázatban
    - 💾 **Mentsd el a változásokat** lokálisan és GitHub-ra
    - 🔄 **Frissítsd a kérdésbankot** automatikusan
    
    ---
    """)
    
    # Cache törlés gomb
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Cache törlése", type="secondary", use_container_width=True):
            # Cache kulcsok törlése
            cache_keys_to_delete = [key for key in st.session_state.keys() if key.startswith("audio_track_data_") or key.startswith("duration_")]
            for key in cache_keys_to_delete:
                del st.session_state[key]
            st.success("✅ Cache törölve! Az oldal újratöltődik...")
            st.rerun()
    
    # Track-ek betöltése kategóriánként
    tracks_by_category = get_audio_tracks_by_category()
    
    # Kategória választó - kattintható gombokkal
    st.markdown("### 📁 Kategória választás")
    category_options = {key: info["title"] for key, info in tracks_by_category.items()}
    
    # Kategória gombok 3 oszlopban
    cols = st.columns(3)
    selected_category = None
    
    # Először beállítjuk a kiválasztott kategóriát
    current_selected = st.session_state.get('selected_category', list(category_options.keys())[0])
    
    for i, (key, title) in enumerate(category_options.items()):
        col_index = i % 3
        with cols[col_index]:
            # Szín meghatározása
            is_selected = key == current_selected
            button_type = "primary" if is_selected else "secondary"
            
            # Streamlit gomb kattinthatóként
            if st.button(f"📂 {title}", key=f"cat_{key}", use_container_width=True, type=button_type):
                selected_category = key
                st.session_state.selected_category = key
                
                # Cache törlése kategória váltáskor
                cache_keys_to_delete = []
                for cache_key in st.session_state.keys():
                    if (cache_key.startswith("simple_audio_data_") or 
                        cache_key.startswith("audio_track_data_") or 
                        cache_key.startswith("duration_") or 
                        cache_key.startswith("track_cache_")):
                        cache_keys_to_delete.append(cache_key)
                
                for cache_key in cache_keys_to_delete:
                    del st.session_state[cache_key]
                
                st.rerun()
    
    # Ha van kiválasztott kategória a session state-ben, használjuk azt
    if selected_category is None:
        selected_category = current_selected
    
    if selected_category:
        category_info = tracks_by_category[selected_category]
        st.markdown(f"### {category_info['title']}")
        
        if selected_category == "komolyzene":
            komoly_question_file = category_info['tracks'][0]['question_file'] if category_info['tracks'] else "topics/komolyzene_uj.py"
            st.markdown("### 🔄 Komolyzene Git sync")
            st.caption("Teljes szinkron: git pull + komolyzene fájlok commit/push.")
            if st.button("🔄 Teljes komolyzene Git sync", type="primary", use_container_width=True):
                sync_komolyzene_with_github(komoly_question_file)
        
        # Lista v. Szerkesztés választó közvetlenül a kategória alatt
        edit_mode = st.radio(
            "Nézet mód:",
            ["📋 Lista nézet", "✏️ Szerkesztés"],
            horizontal=True,
            key="edit_mode_radio"
        )
        
        if not category_info['tracks']:
            st.info("📭 Nincsenek track-ek ebben a kategóriában.")
        else:
            st.markdown(f"📊 **{len(category_info['tracks'])} track található**")
            

            # EGYSZERŰ CACHE RENDSZER
            cache_key = f"simple_audio_data_{selected_category}"
            # Kérdésfájl útvonal és módosítási idő a cache érvényesítéséhez
            question_file_path = category_info['tracks'][0]['question_file'] if category_info['tracks'] else None
            question_file_mtime = None
            if question_file_path and os.path.exists(question_file_path):
                question_file_mtime = os.path.getmtime(question_file_path)
            cache_meta_key = f"{cache_key}_meta"
            
            # Cache törlése gomb
            if st.button("🗑️ Cache törlése"):
                if cache_key in st.session_state:
                    del st.session_state[cache_key]
                if cache_meta_key in st.session_state:
                    del st.session_state[cache_meta_key]
                st.rerun()
            
            # Cache ellenőrzése
            force_refresh = st.session_state.get('force_refresh', False)
            cached_meta = st.session_state.get(cache_meta_key, {})
            cache_is_valid = cached_meta.get("questions_mtime") == question_file_mtime
            if cache_key in st.session_state and not force_refresh and cache_is_valid:
                table_data = st.session_state[cache_key]
                st.info(f"📊 Cache betöltve: {len(table_data)} sor")
            else:
                if cache_key in st.session_state and not cache_is_valid and not force_refresh:
                    st.info("🔄 Kérdésfájl változott, cache frissítése...")
                if force_refresh:
                    st.info("🔄 Kényszerített frissítés...")
                    # Összes kapcsolódó cache törlése
                    cache_keys_to_delete = []
                    for key in st.session_state.keys():
                        if (key.startswith("audio_track_data_") or 
                            key.startswith("duration_") or 
                            key.startswith("track_cache_")):
                            cache_keys_to_delete.append(key)
                    
                    for key in cache_keys_to_delete:
                        del st.session_state[key]
                    
                    st.session_state['force_refresh'] = False
                st.info("🔄 Új adatok betöltése...")
                
                # Kérdések betöltése
                question_file_path = category_info['tracks'][0]['question_file'] if category_info['tracks'] else None
                if question_file_path:
                    questions = load_questions_from_file(question_file_path)
                    st.info(f"📚 Kérdések betöltve: {len(questions)} kérdés")
                else:
                    questions = []
                    st.info("❌ Nincs kérdésfájl!")
                
                # Track cache létrehozása
                track_cache = {}
                for track in category_info['tracks']:
                    # A track['name'] már kiterjesztés nélküli, nem kell újra feldolgozni
                    track_cache[track['name']] = track
                
                st.info(f"🎵 Track cache létrehozva: {len(track_cache)} track")
                
                # EGYSZERŰ TÁBLÁZAT LÉTREHOZÁS
                table_data = []
                st.info(f"🔄 Táblázat létrehozása {len(questions)} kérdésből...")
                
                # Progress bar egyszerű százalékkal
                progress_bar = st.progress(0)
                progress_text = st.empty()
                
                for i, question in enumerate(questions):
                    # Alapvető adatok kinyerése
                    question_text = question['question']
                    artist = question['options'][question['correct']] if question['correct'] < len(question['options']) else "Ismeretlen"
                    correct_answer = question['options'][question['correct']] if question['correct'] < len(question['options']) else "N/A"
                    options = question['options'] + [""] * (4 - len(question['options']))
                    
                    # Audio fájl keresése
                    matching_track = None
                    if 'audio_file' in question:
                        question_audio_file = question['audio_file']
                        # Ha teljes útvonal van, csak a fájlnév kiterjesztés nélküli részét vesszük
                        question_audio_filename = os.path.basename(question_audio_file)
                        question_audio_no_ext = os.path.splitext(question_audio_filename)[0]
                        matching_track = track_cache.get(question_audio_no_ext)
                    
                    # Song title meghatározása
                    song_title = "Ismeretlen szám"
                    
                    # Először nézzük meg, hogy van-e mentett song_title
                    if 'song_title' in question and question['song_title']:
                        song_title = question['song_title']
                    elif matching_track and 'name' in matching_track:
                        # Ha a track name tartalmaz fájlnév részeket, tisztítsuk meg
                        track_name = matching_track['name']
                        
                        # Új formátum kezelése: "72. Depeche Mode - Policy Of Truth" vagy "45. Delibes - Delibes"
                        if '. ' in track_name and ' - ' in track_name:
                            # Formátum: "szám. Előadó - Szám címe"
                            parts = track_name.split(' - ', 1)
                            if len(parts) == 2:
                                song_title = parts[1].strip()  # Csak a szám címet vesszük ki
                                
                                # Speciális eset: ha a szám címe ugyanaz, mint az előadó (pl. "45. Delibes - Delibes")
                                # akkor csak az előadó nevet használjuk
                                artist_part = parts[0].strip()
                                if '. ' in artist_part:
                                    artist_name = artist_part.split('. ', 1)[1].strip()
                                    if song_title.lower() == artist_name.lower():
                                        song_title = artist_name  # Csak az előadó nevet használjuk
                            else:
                                song_title = track_name
                        # Régi formátum kezelése: "72_Depeche_Mode_Policy_Of_Truth"
                        elif '_' in track_name and any(part.isdigit() for part in track_name.split('_')):
                            # Ha van sorszám és előadó a névben, csak a szám címet vegyük ki
                            parts = track_name.split('_')
                            # Keressük meg az utolsó részt ami nem sorszám és nem előadó
                            for j in range(len(parts)-1, -1, -1):
                                if not parts[j].isdigit() and parts[j].lower() not in [artist.lower().replace(' ', '_'), 'unknown_artist']:
                                    song_title = '_'.join(parts[j:]).replace('_', ' ')
                                    break
                            else:
                                song_title = track_name.replace('_', ' ')
                        else:
                            song_title = track_name.replace('_', ' ')
                    elif 'audio_file' in question:
                        audio_file = question['audio_file']
                        filename = os.path.basename(audio_file)
                        filename_no_ext = os.path.splitext(filename)[0]
                        # Fájlnév tisztítása
                        if '_' in filename_no_ext and any(part.isdigit() for part in filename_no_ext.split('_')):
                            parts = filename_no_ext.split('_')
                            for j in range(len(parts)-1, -1, -1):
                                if not parts[j].isdigit() and parts[j].lower() not in [artist.lower().replace(' ', '_'), 'unknown_artist']:
                                    song_title = '_'.join(parts[j:]).replace('_', ' ')
                                    break
                            else:
                                song_title = filename_no_ext.replace('_', ' ')
                        else:
                            song_title = filename_no_ext.replace('_', ' ')
                    
                    # Duration meghatározása
                    duration_str = "N/A"
                    if matching_track:
                        duration_cache_key = f"duration_{matching_track['audio_path']}"
                        if duration_cache_key in st.session_state:
                            duration_str = st.session_state[duration_cache_key]
                        else:
                            try:
                                duration_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', matching_track['audio_path']]
                                duration_result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=3)
                                if duration_result.returncode == 0 and duration_result.stdout.strip():
                                    duration_seconds = float(duration_result.stdout.strip())
                                    duration_str = f"{int(duration_seconds // 60)}:{int(duration_seconds % 60):02d}"
                                    st.session_state[duration_cache_key] = duration_str
                            except:
                                duration_str = "N/A"
                                st.session_state[duration_cache_key] = duration_str
                    
                    # Sor hozzáadása
                    table_data.append({
                        "Előadó": artist,
                        "Szám címe": song_title,
                        "Hossz": duration_str,
                        "Helyes válasz": correct_answer,
                        "Opció1": options[0] if len(options) > 0 else "",
                        "Opció2": options[1] if len(options) > 1 else "",
                        "Opció3": options[2] if len(options) > 2 else "",
                        "Opció4": options[3] if len(options) > 3 else "",
                        "question_index": i,
                        "question_text": question_text,
                        "matching_track": matching_track
                    })
                    
                    # Progress frissítése
                    progress = (i + 1) / len(questions)
                    progress_bar.progress(progress)
                    progress_text.text(f"Feldolgozás: {int(progress * 100)}% ({i + 1}/{len(questions)})")
                
                # Cache mentése
                st.session_state[cache_key] = table_data
                st.session_state[cache_meta_key] = {"questions_mtime": question_file_mtime}
                st.info(f"💾 Cache mentve: {len(table_data)} sor")
                st.success(f"✅ Táblázat létrehozva: {len(table_data)} sor")
            
            # Táblázat megjelenítése
            if table_data:
                # DataFrame létrehozása
                import pandas as pd
                df = pd.DataFrame(table_data)
                
                # Sorszámok hozzáadása a fájlnévből
                row_numbers = []
                filenames = []
                
                for row in table_data:
                    if row['matching_track'] and 'audio_path' in row['matching_track']:
                        audio_path = row['matching_track']['audio_path']
                        filename = os.path.basename(audio_path)
                        filename_no_ext = os.path.splitext(filename)[0]
                        filenames.append(filename)
                        # Szám kinyerése a fájlnévből (pl. "41_Alvin_és_a_Mókusok" -> "41")
                        if '_' in filename_no_ext and filename_no_ext.split('_')[0].isdigit():
                            row_numbers.append(filename_no_ext.split('_')[0])
                        else:
                            row_numbers.append("N/A")
                    else:
                        filenames.append("N/A")
                        row_numbers.append("N/A")
                
                # DataFrame létrehozása sorszámokkal és fájlnévvel
                display_df = df[["Előadó", "Szám címe", "Opció1", "Opció2", "Opció3", "Opció4"]].copy()
                display_df.insert(0, "Sorszám", row_numbers)
                display_df.insert(1, "Fájlnév", filenames)
                
                # Stílusok hozzáadása
                def style_dataframe(df):
                    # CSS stílusok
                    css = """
                    <style>
                    .dataframe {
                        font-size: 12px !important;
                    }
                    .dataframe th {
                        font-size: 12px !important;
                        font-weight: bold !important;
                    }
                    .dataframe td {
                        font-size: 12px !important;
                    }
                    .artist-column {
                        font-weight: bold !important;
                    }
                    .song-title-column {
                        font-weight: bold !important;
                    }
                    .correct-answer-column {
                        font-size: 12px !important;
                        color: #1f77b4 !important;
                        font-weight: bold !important;
                    }
                    </style>
                    """
                    st.markdown(css, unsafe_allow_html=True)
                    
                    # DataFrame megjelenítése
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Sorszám": st.column_config.TextColumn("Sorszám", width="small"),
                            "Fájlnév": st.column_config.TextColumn("Fájlnév", width="medium"),
                            "Előadó": st.column_config.TextColumn("Előadó", width="medium"),
                            "Szám címe": st.column_config.TextColumn("Szám címe", width="large"),
                            "Opció1": st.column_config.TextColumn("Opció1", width="medium"),
                            "Opció2": st.column_config.TextColumn("Opció2", width="medium"),
                            "Opció3": st.column_config.TextColumn("Opció3", width="medium"),
                            "Opció4": st.column_config.TextColumn("Opció4", width="medium")
                        }
                    )
                
                # Stílusok alkalmazása a display_df-re
                style_dataframe(display_df)
                
                # Egyszerű táblázat megjelenítés
                
                # Teljes táblázat megjelenítés
                
                # Sor kiválasztás a táblázatból
                selected_row_index = st.selectbox(
                    "Válassz egy sort:",
                    options=[f"{i+1}. {row['Előadó']} - {row['Szám címe']}" for i, row in enumerate(table_data)],
                    key="audio_row_selector"
                )
                
                # Play gomb a kijelölt sorhoz
                if selected_row_index:
                    selected_index = int(selected_row_index.split('.')[0]) - 1
                    selected_data = table_data[selected_index]
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(f"🎵 Play {selected_data['Előadó']} - {selected_data['Szám címe']}", type="primary", use_container_width=True):
                            if selected_data['matching_track'] and 'audio_path' in selected_data['matching_track']:
                                audio_path = selected_data['matching_track']['audio_path']
                                st.audio(audio_path, format='audio/mp3')
                                st.success(f"✅ Lejátszás: {selected_data['Előadó']} - {selected_data['Szám címe']}")
                            else:
                                st.warning(f"⚠️ Nincs audio fájl: {selected_data['Előadó']} - {selected_data['Szám címe']}")
                
                # DataFrame megjelenítés már megtörtént a style_dataframe függvényben
                

                
                # Szerkesztési funkció - soronkénti szerkesztés
                st.markdown("### ✏️ Szerkesztés")
                
                # Módosított kérdések követése
                if 'modified_questions' not in st.session_state:
                    st.session_state.modified_questions = set()
                
                # Szerkesztési mód már be van állítva fentebb
                
                # Módosított kérdések megjelenítése
                if st.session_state.modified_questions:
                    st.info(f"📝 **{len(st.session_state.modified_questions)} kérdés módosítva** - Ne felejtsd el menteni a változásokat!")
                
                if edit_mode == "✏️ Szerkesztés":
                    st.markdown("**Válassz egy sort a szerkesztéshez:**")
                    
                    # Kérdések betöltése szerkesztéshez
                    if question_file_path:
                        questions = load_questions_from_file(question_file_path)
                    else:
                        questions = []
                        st.error("❌ Nincs kérdésfájl!")
                    
                    if question_file_path and len(table_data) != len(questions):
                        st.warning("⚠️ A kérdéslista megváltozott. Cache frissítés szükséges.")
                        if cache_key in st.session_state:
                            del st.session_state[cache_key]
                        if cache_meta_key in st.session_state:
                            del st.session_state[cache_meta_key]
                        st.session_state['force_refresh'] = True
                        st.rerun()
                    
                    # Szerkesztési űrlapok minden sorhoz
                    for i, row in enumerate(table_data):
                        # Módosított kérdés jelölése
                        is_modified = row['question_index'] in st.session_state.modified_questions
                        expander_title = f"📝 {i+1}. {row['Előadó']} - {row['Szám címe']}"
                        if is_modified:
                            expander_title += " ✏️ (módosítva)"
                        
                        with st.expander(expander_title, expanded=False):
                            question_index = row['question_index']
                            if question_index < 0 or question_index >= len(questions):
                                st.warning("⚠️ Hibás kérdésindex. Kérlek frissítsd a cache-t.")
                                continue
                            current_question = questions[question_index]
                            
                            # Kérdés szerkesztése
                            question_text = st.text_input(
                                "Kérdés:",
                                value=current_question['question'],
                                key=f"question_edit_{i}"
                            )
                            
                            # Szám címe szerkesztése
                            current_song_title = row['Szám címe']
                            song_title = st.text_input(
                                "Szám címe:",
                                value=current_song_title,
                                key=f"song_title_edit_{i}"
                            )
                            
                            # Opciók szerkesztése
                            st.markdown("**Válaszopciók:**")
                            col1, col2 = st.columns(2)
                            
                            options = []
                            with col1:
                                for j in range(2):
                                    option = st.text_input(
                                        f"Opció {j+1}:",
                                        value=current_question['options'][j] if j < len(current_question['options']) else "",
                                        key=f"option_edit_{i}_{j}"
                                    )
                                    options.append(option)
                            
                            with col2:
                                for j in range(2, 4):
                                    option = st.text_input(
                                        f"Opció {j+1}:",
                                        value=current_question['options'][j] if j < len(current_question['options']) else "",
                                        key=f"option_edit_{i}_{j}"
                                    )
                                    options.append(option)
                            
                            # Helyes válasz kiválasztása
                            correct_answer = st.selectbox(
                                "Helyes válasz:",
                                options=options,
                                index=current_question['correct'] if current_question['correct'] < len(options) else 0,
                                key=f"correct_edit_{i}"
                            )
                            
                            # Mentés gomb
                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("💾 Mentés", key=f"save_edit_{i}", type="primary"):
                                    try:
                                        # Kérdés frissítése
                                        updated_question = {
                                            "question": question_text,
                                            "options": options,
                                            "correct": options.index(correct_answer) if correct_answer in options else 0,
                                            "song_title": song_title
                                        }
                                        
                                        # További mezők megtartása
                                        if 'audio_file' in current_question:
                                            updated_question['audio_file'] = current_question['audio_file']
                                        if 'explanation' in current_question:
                                            updated_question['explanation'] = current_question['explanation']
                                        if 'topic' in current_question:
                                            updated_question['topic'] = current_question['topic']
                                        
                                        # Kérdés frissítése a listában
                                        questions[question_index] = updated_question
                                        
                                        # Módosított kérdés jelölése
                                        st.session_state.modified_questions.add(question_index)
                                        
                                        # Fájl mentése
                                        if save_questions_to_file(questions, question_file_path, "QUESTIONS"):
                                            st.success("✅ Kérdés sikeresen mentve!")
                                            
                                            # Audio fájl átnevezése, ha a szám címe változott VAGY ha a fájlnév nem illeszkedik a várható formátumra
                                            if 'audio_file' in current_question and (song_title != current_song_title or not os.path.basename(current_question['audio_file']).startswith(f"{i+1:02d}.")):
                                                try:
                                                    import shutil
                                                    
                                                    # Előadó meghatározása a kérdésből
                                                    artist = current_question['options'][current_question['correct']] if current_question['correct'] < len(current_question['options']) else "Unknown_Artist"
                                                    
                                                    old_audio_file = current_question['audio_file']
                                                    old_audio_path = None
                                                    
                                                    # Régi fájl teljes útvonalának megkeresése
                                                    old_audio_filename = os.path.basename(old_audio_file)
                                                    old_audio_name = os.path.splitext(old_audio_filename)[0]
                                                    for track in category_info['tracks']:
                                                        if track['name'] == old_audio_name:
                                                            old_audio_path = track['audio_path']
                                                            break
                                                    
                                                    if old_audio_path and os.path.exists(old_audio_path):
                                                        # Új fájlnév generálása a szám címéből
                                                        # Biztonságos fájlnév létrehozása - csak a tiszta szám címet használjuk
                                                        clean_song_title = song_title
                                                        # Ha a song_title tartalmaz fájlnév részeket, tisztítsuk meg
                                                        if '_' in clean_song_title and any(part.isdigit() for part in clean_song_title.split('_')):
                                                            # Ha van sorszám és előadó a névben, csak a szám címet vegyük ki
                                                            parts = clean_song_title.split('_')
                                                            # Keressük meg az utolsó részt ami nem sorszám és nem előadó
                                                            for j in range(len(parts)-1, -1, -1):
                                                                if not parts[j].isdigit() and parts[j].lower() not in [artist.lower().replace(' ', '_'), 'unknown_artist']:
                                                                    clean_song_title = '_'.join(parts[j:])
                                                                    break
                                                        
                                                        safe_song_title = "".join(c for c in clean_song_title if c.isalnum() or c in (' ', '-')).rstrip()
                                                        # Szóközök megtartása, csak speciális karakterek eltávolítása
                                                        safe_song_title = safe_song_title.replace('  ', ' ')  # Dupla szóközök egyszerűsítése
                                                        
                                                        # Új fájlnév: sorszám. Előadó - Szám címe.mp3
                                                        artist_safe = "".join(c for c in artist if c.isalnum() or c in (' ', '-')).rstrip()
                                                        artist_safe = artist_safe.replace('  ', ' ')  # Dupla szóközök egyszerűsítése
                                                        new_filename = f"{i+1:02d}. {artist_safe} - {safe_song_title}.mp3"
                                                        new_audio_path = os.path.join(os.path.dirname(old_audio_path), new_filename)
                                                        
                                                        # Fájl átnevezése
                                                        shutil.move(old_audio_path, new_audio_path)
                                                        
                                                        # Kérdésben az audio_file frissítése
                                                        updated_question['audio_file'] = new_filename
                                                        questions[question_index] = updated_question
                                                        
                                                        # Kérdés újramentése az új fájlnévvel
                                                        save_questions_to_file(questions, question_file_path, "QUESTIONS")
                                                        
                                                        st.success(f"✅ Audio fájl átnevezve: {new_filename}")
                                                        
                                                except Exception as e:
                                                    st.warning(f"⚠️ Fájl átnevezése sikertelen: {str(e)}")
                                            
                                            # Teljes cache törlése a táblázat frissítéséhez
                                            cache_keys_to_delete = []
                                            for key in st.session_state.keys():
                                                if (key.startswith("audio_track_data_") or 
                                                    key.startswith("duration_") or 
                                                    key.startswith("track_cache_") or
                                                    key == "modified_questions"):
                                                    cache_keys_to_delete.append(key)
                                            
                                            for key in cache_keys_to_delete:
                                                if key in st.session_state:
                                                    del st.session_state[key]
                                            
                                            # Cache invalidation flag beállítása
                                            st.session_state['force_refresh'] = True
                                            
                                            # Git műveletek
                                            try:
                                                subprocess.run(['git', 'add', question_file_path], check=True)
                                                subprocess.run(['git', 'commit', '-m', f'Update question for {row["Előadó"]} - {row["Szám címe"]}'], check=True)
                                                subprocess.run(['git', 'push'], check=True)
                                                st.success("✅ Változások GitHub-ra feltöltve!")
                                                st.info("🔄 Oldal frissítése...")
                                                import time
                                                time.sleep(0.5)  # Kis késleltetés a cache törléshez
                                                st.rerun()
                                            except subprocess.CalledProcessError as e:
                                                st.error(f"❌ Git hiba: {e}")
                                        else:
                                            st.error("❌ Hiba a fájl mentésekor!")
                                    except Exception as e:
                                        st.error(f"❌ Hiba a mentés során: {e}")
                            
                            # Törlés funkció - track + kérdés + GitHub sync
                            st.markdown("---")
                            st.markdown("### 🗑️ Törlés")
                            st.warning("⚠️ Ez a művelet visszavonhatatlan: a kérdés és az audio fájl is törlődik.")
                            confirm_delete = st.checkbox(
                                "Igen, törlöm ezt a tracket és a kérdést",
                                key=f"confirm_delete_{i}"
                            )
                            
                            if st.button("🗑️ Track + kérdés törlése és GitHub sync", key=f"delete_track_{i}", type="secondary"):
                                if not confirm_delete:
                                    st.warning("⚠️ A törléshez jelöld be a megerősítést.")
                                else:
                                    try:
                                        if not question_file_path:
                                            st.error("❌ Nincs kérdésfájl, törlés nem lehetséges.")
                                        else:
                                            # Audio fájl útvonal megkeresése
                                            audio_path = None
                                            if row.get("matching_track") and row["matching_track"].get("audio_path"):
                                                audio_path = row["matching_track"]["audio_path"]
                                            elif 'audio_file' in current_question and current_question['audio_file']:
                                                audio_filename = os.path.basename(current_question['audio_file'])
                                                audio_name = os.path.splitext(audio_filename)[0]
                                                for track in category_info['tracks']:
                                                    if track['name'] == audio_name:
                                                        audio_path = track['audio_path']
                                                        break
                                                if audio_path is None and os.path.exists(current_question['audio_file']):
                                                    audio_path = current_question['audio_file']
                                            
                                            # Kérdés törlése
                                            updated_questions = [q for idx, q in enumerate(questions) if idx != question_index]
                                            if save_questions_to_file(updated_questions, question_file_path, "QUESTIONS"):
                                                # Audio fájl törlése, ha létezik
                                                if audio_path and os.path.exists(audio_path):
                                                    os.remove(audio_path)
                                                    st.success(f"✅ Audio fájl törölve: {os.path.basename(audio_path)}")
                                                else:
                                                    st.warning("⚠️ Audio fájl nem található, csak a kérdés törölve.")
                                                
                                                # Git műveletek
                                                try:
                                                    subprocess.run(['git', 'add', '-A', question_file_path], check=True)
                                                    if audio_path:
                                                        subprocess.run(['git', 'add', '-A', audio_path], check=True)
                                                    commit_msg = f'Delete track {row["Előadó"]} - {row["Szám címe"]}'
                                                    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                                                    subprocess.run(['git', 'push'], check=True)
                                                    st.success("✅ Törlés GitHub-ra szinkronizálva!")
                                                except subprocess.CalledProcessError as e:
                                                    st.error(f"❌ Git hiba: {e}")
                                                
                                                # Cache törlése
                                                cache_keys_to_delete = []
                                                for key in st.session_state.keys():
                                                    if (key.startswith("audio_track_data_") or 
                                                        key.startswith("duration_") or 
                                                        key.startswith("track_cache_") or
                                                        key == "modified_questions"):
                                                        cache_keys_to_delete.append(key)
                                                
                                                for key in cache_keys_to_delete:
                                                    if key in st.session_state:
                                                        del st.session_state[key]
                                                
                                                if cache_key in st.session_state:
                                                    del st.session_state[cache_key]
                                                if cache_meta_key in st.session_state:
                                                    del st.session_state[cache_meta_key]
                                                
                                                st.session_state['force_refresh'] = True
                                                st.rerun()
                                            else:
                                                st.error("❌ Hiba a kérdésfájl mentésekor!")
                                    except Exception as e:
                                        st.error(f"❌ Törlés sikertelen: {e}")
                
                else:
                    # Lista nézet - csak megjelenítés
                    st.markdown("**Válassz a fenti opciók közül a szerkesztéshez.**")
                
                # Összes változás mentése gomb
                if edit_mode == "✏️ Szerkesztés" and st.session_state.modified_questions:
                    st.markdown("---")
                    st.markdown("### 💾 Összes változás mentése")
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("🚀 Összes változás mentése és Git Push", type="primary", use_container_width=True):
                            try:
                                # Fájl mentése
                                if save_questions_to_file(questions, question_file_path, "QUESTIONS"):
                                    st.success("✅ Kérdések sikeresen mentve!")
                                    
                                    # Git műveletek
                                    try:
                                        subprocess.run(['git', 'add', question_file_path], check=True)
                                        subprocess.run(['git', 'commit', '-m', f'Update multiple questions in {selected_category}'], check=True)
                                        subprocess.run(['git', 'push'], check=True)
                                        st.success("✅ Összes változás GitHub-ra feltöltve!")
                                        
                                        # Módosított kérdések listájának törlése
                                        st.session_state.modified_questions.clear()
                                        
                                        st.rerun()
                                    except subprocess.CalledProcessError as e:
                                        st.error(f"❌ Git hiba: {e}")
                                else:
                                    st.error("❌ Hiba a fájl mentésekor!")
                            except Exception as e:
                                st.error(f"❌ Hiba a mentés során: {e}")

def show_github_sync_page():
    """GitHub szinkronizációs oldal megjelenítése"""
    st.markdown('<h2 style="text-align: center; color: #1f77b4;">🔄 GitHub Szinkronizálás</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 Mit csinál ez a funkció?
    
    Ez a funkció lehetővé teszi, hogy:
    - 📥 **Letöltsd a legfrissebb változásokat** a GitHub-ról
    - 🎵 **Frissítsd az audiofájlokat** - új trackek, amiket webes felhasználók töltöttek fel
    - 📝 **Frissítsd a kérdéseket** - új kérdések, amiket webes felhasználók adtak hozzá
    - 🔄 **Szinkronizáld a lokális adatbázist** a GitHub repository-val
    
    ### ⚠️ Fontos információk:
    - A szinkronizálás **nem törli** a lokális fájlokat
    - Csak **új tartalmakat** tölt le és frissít
    - A szinkronizálás után **javasolt az alkalmazás újraindítása**
    
    ---
    """)
    
    # Szinkronizálás gomb
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 GitHub Szinkronizálás Indítása", type="primary", use_container_width=True):
            sync_with_github()
    
    # Statisztikák megjelenítése
    st.markdown("### 📊 Jelenlegi állapot")
    
    # Audiofájlok számolása
    all_tracks = get_all_audio_tracks()
    audio_count = len(all_tracks)
    
    # Kategóriánkénti statisztika
    category_stats = {}
    for track in all_tracks:
        directory = track["directory"]
        if directory not in category_stats:
            category_stats[directory] = 0
        category_stats[directory] += 1
    
    # Kérdés fájlok számolása
    question_count = 0
    topics_patterns = [
        "topics/*.py",
        "topics/*_questions.py",
        "topics/*_complete.py"
    ]
    
    for pattern in topics_patterns:
        files = glob.glob(pattern)
        question_count += len(files)
    
    # Metrikák megjelenítése
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🎵 Audiofájlok", audio_count)
    with col2:
        st.metric("📝 Kérdés fájlok", question_count)
    
    # Kategóriánkénti statisztika
    st.markdown("### 📊 Kategóriánkénti eloszlás")
    for directory, count in category_stats.items():
        st.markdown(f"**{directory}**: {count} track")
    
    # Utolsó szinkronizálás információ
    st.markdown("### 📅 Utolsó szinkronizálás")
    st.info("Az utolsó szinkronizálás időpontja: **Még nem történt szinkronizálás**")
    
    # Manuális frissítés gomb
    if st.button("🔄 Frissítés", type="secondary"):
        st.rerun()

def show_search_page():
    """Keresési oldal megjelenítése"""
    try:
        from search_functionality import display_search_interface
        display_search_interface()
    except ImportError as e:
        st.error(t("Hiba a keresési funkció betöltésekor: {error}", error=e))
        st.info(t("A keresési funkció nem érhető el. Ellenőrizd a search_functionality.py fájlt."))

def show_topic_selection():
    """Témakör kiválasztás"""
    
    # Felhasználó kiválasztás
    st.markdown(t("### 👤 Játékos név megadása"))
    
    player_input = st.text_input(
        t("Add meg a neved:"),
        value=st.session_state.get("selected_player", ""),
        key="player_name_input",
    )
    player_name = player_input.strip()
    st.session_state.selected_player = player_name
    if not player_name:
        st.warning(t("A játékos név megadása kötelező."))
    
    # Quiz mód kiválasztás
    selected_mode, selected_difficulty = QuizModeUI.show_mode_selection()
    
    # Mód beállítása
    mode_mapping = {
        "normál": QuizMode.NORMAL,
        "időzített": QuizMode.TIMED,
        "túlélés": QuizMode.SURVIVAL,
        "gyakorlás": QuizMode.PRACTICE,
        "kihívás": QuizMode.CHALLENGE
    }
    
    difficulty_mapping = {
        "könnyű": DifficultyLevel.EASY,
        "közepes": DifficultyLevel.MEDIUM,
        "nehéz": DifficultyLevel.HARD
    }
    
    st.session_state.mode_manager.set_mode(mode_mapping[selected_mode])
    st.session_state.mode_manager.set_difficulty(difficulty_mapping[selected_difficulty])
    
    # Témakörök definiálása
    topics = {
        "földrajz": "🌍 Földrajz",
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar könnyűzene",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi zenekarok",
        "one_hit_wonders": "⭐ One Hit Wonders",
        "sorozat_focimek": "📺 Sorozat főcímek",
        "festmények": "🎨 Festmények",
        "magyar_festmenyek": "🇭🇺 Magyar festmények",
        "regények": "📚 Regények",
        "háborúk": "⚔️ Háborúk",
        "magyar_királyok": "👑 Magyar királyok",
        "tudósok": "🔬 Tudósok, művészek, híres emberek",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "drámák": "🎭 Drámák",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "zaszlok_reszletek": "🔍 Zászlók részlete",
        "idióta_szavak": "🤪 Idióta szavak",
        "labdarugo_palyafutas": "⚽ Labdarúgó pályafutás",
    }
    
    # Randomizáló funkció
    st.markdown(t("### 🎲 Randomizáló Funkció"))
    
    # Kérdésszám beállítás csúszkával
    col1, col2 = st.columns(2)
    with col1:
        random_question_count = st.slider(
            t("Randomizáláshoz használandó kérdésszám"),
            10,
            100,
            st.session_state.get('default_other_questions', 40),
            key="random_question_count",
        )
    
    with col2:
        random_music_question_count = st.slider(
            t("Zenei randomizáláshoz használandó kérdésszám"),
            5,
            50,
            st.session_state.get('default_music_questions', 10),
            key="random_music_question_count",
        )
    
    # Randomizáló gombok egy sorban
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(t("🎯 Teljes kvíz létrehozása"), type="primary", use_container_width=True):
            # Összes témakör kiválasztása
            st.session_state.selected_topics = list(topics.keys())
            
            # Zenei és egyéb témakörök szétválasztása
            music_topics = [t for t in topics.keys() if "zene" in t or "zenekar" in t or t in {"one_hit_wonders", "sorozat_focimek"}]
            other_topics = [t for t in topics.keys() if "zene" not in t and "zenekar" not in t and t not in {"one_hit_wonders", "sorozat_focimek"}]
            
            # Kérdések elosztása a zenei témakörök között
            if music_topics:
                questions_per_music_topic = random_music_question_count // len(music_topics)
                remaining_music_questions = random_music_question_count % len(music_topics)
                
                # Random kiválasztás, hogy melyik témakörök kapjanak extra kérdést
                extra_questions_topics = random.sample(music_topics, remaining_music_questions) if remaining_music_questions > 0 else []
                
                for topic_key in music_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    topic_questions = questions_per_music_topic + (1 if topic_key in extra_questions_topics else 0)
                    topic_questions = min(topic_questions, max_questions)
                    st.session_state[f'final_{topic_key}_questions'] = topic_questions
            
            # Kérdések elosztása az egyéb témakörök között
            if other_topics:
                questions_per_other_topic = random_question_count // len(other_topics)
                remaining_other_questions = random_question_count % len(other_topics)
                
                # Random kiválasztás, hogy melyik témakörök kapjanak extra kérdést
                extra_questions_topics = random.sample(other_topics, remaining_other_questions) if remaining_other_questions > 0 else []
                
                for topic_key in other_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    topic_questions = questions_per_other_topic + (1 if topic_key in extra_questions_topics else 0)
                    topic_questions = min(topic_questions, max_questions)
                    st.session_state[f'final_{topic_key}_questions'] = topic_questions
            
            # Összesítő értékek beállítása
            total_music_questions = sum(st.session_state.get(f'final_{topic}_questions', 0) for topic in music_topics)
            st.session_state['music_total_questions'] = total_music_questions
            
            total_other_questions = sum(st.session_state.get(f'final_{topic}_questions', 0) for topic in other_topics)
            st.session_state['other_total_questions'] = total_other_questions
            
            st.success(
                t(
                    "✅ Teljes kvíz létrehozva! {topic_count} témakör kiválasztva, összesen {question_count} kérdés!",
                    topic_count=len(topics),
                    question_count=total_music_questions + total_other_questions,
                )
            )
            st.rerun()
        
    with col2:
        if st.button(t("🎵 Random zenei témakörök kiválasztása"), type="secondary", use_container_width=True):
            # Zenei témakörök kiválasztása
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"]
            num_music_topics = random.randint(2, 3)  # 2-3 zenei témakör
            selected_music_topics = random.sample(music_topics, num_music_topics)
            
            # Kérdések elosztása a zenei témakörök között
            questions_per_music_topic = random_music_question_count // num_music_topics
            remaining_music_questions = random_music_question_count % num_music_topics
            
            # Meglévő nem-zenei témakörök megtartása
            existing_other_topics = [topic for topic in st.session_state.selected_topics if topic not in music_topics]
            
            # Témakörök kiválasztása (nem-zenei + új zenei)
            st.session_state.selected_topics = existing_other_topics + selected_music_topics
            
            # Gomb állapotok frissítése (checkbox helyett)
            for topic_key in topics.keys():
                if topic_key in selected_music_topics or topic_key in existing_other_topics:
                    # A gombok állapota automatikusan frissül a selected_topics alapján
                    pass
                elif topic_key in music_topics:  # Csak zenei témakörök törlése
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
            
            # Kérdésszámok beállítása
            # Random kiválasztás, hogy melyik témakörök kapjanak extra kérdést
            extra_questions_topics = random.sample(selected_music_topics, remaining_music_questions) if remaining_music_questions > 0 else []
            
            for topic in selected_music_topics:
                topic_questions = questions_per_music_topic + (1 if topic in extra_questions_topics else 0)
                max_available = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                topic_questions = min(topic_questions, max_available)
                st.session_state[f'{topic}_questions'] = topic_questions
                # Ne módosítsuk a final_ értékeket, ha már létrejöttek a slider-ek
                if f'final_{topic}_questions' not in st.session_state:
                    st.session_state[f'final_{topic}_questions'] = topic_questions
            
            # Alapértelmezett értékek beállítása
            st.session_state['music_total_questions'] = random_music_question_count
            
            st.success(
                t(
                    "✅ {topic_count} zenei témakör kiválasztva + meglévő nem-zenei témakörök megtartva, {question_count} kérdés elosztva!",
                    topic_count=num_music_topics,
                    question_count=random_music_question_count,
                )
            )
            st.rerun()
        
    with col3:
        if st.button(t("🎲 Random témakörök kiválasztása (zene nélkül)"), type="secondary", use_container_width=True):
            # Legalább 5 témakör kiválasztása (zenei témakörök nélkül)
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"]
            available_topics = [topic for topic in topics.keys() if topic not in music_topics]
            num_topics = random.randint(5, min(8, len(available_topics)))  # 5-8 témakör között
            selected_random_topics = random.sample(available_topics, num_topics)
            
            # Kérdések elosztása a kiválasztott témakörök között
            questions_per_topic = random_question_count // num_topics
            remaining_questions = random_question_count % num_topics
            
            # Meglévő zenei témakörök megtartása
            existing_music_topics = [topic for topic in st.session_state.selected_topics if topic in music_topics]
            
            # Témakörök kiválasztása (zenei + új random)
            st.session_state.selected_topics = existing_music_topics + selected_random_topics
            
            # Gomb állapotok frissítése (checkbox helyett)
            for topic_key in topics.keys():
                if topic_key in selected_random_topics or topic_key in existing_music_topics:
                    # A gombok állapota automatikusan frissül a selected_topics alapján
                    pass
                elif topic_key not in music_topics:  # Csak nem-zenei témakörök törlése
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
            
            # Kérdésszámok beállítása
            # Random kiválasztás, hogy melyik témakörök kapjanak extra kérdést
            extra_questions_topics = random.sample(selected_random_topics, remaining_questions) if remaining_questions > 0 else []
            
            for topic in selected_random_topics:
                topic_questions = questions_per_topic + (1 if topic in extra_questions_topics else 0)
                max_available = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                topic_questions = min(topic_questions, max_available)
                st.session_state[f'{topic}_questions'] = topic_questions
                # Ne módosítsuk a final_ értékeket, ha már létrejöttek a slider-ek
                if f'final_{topic}_questions' not in st.session_state:
                    st.session_state[f'final_{topic}_questions'] = topic_questions
            
            # Alapértelmezett értékek beállítása
            st.session_state['other_total_questions'] = random_question_count
            st.session_state['music_total_questions'] = random_music_question_count
            
            st.success(
                t(
                    "✅ {topic_count} témakör kiválasztva (zene nélkül) + meglévő zenei témakörök megtartva, {question_count} kérdés elosztva!",
                    topic_count=num_topics,
                    question_count=random_question_count,
                )
            )
            st.rerun()
    
    with col2:
        pass
    
    with col3:
        pass
    
    st.markdown("---")
    
    # Témakörök kiválasztása
    col1, col2, col3 = st.columns(3)
    
    # Egyenlő elosztás kiszámítása a kiválasztott témakörök között
    selected_topics = st.session_state.selected_topics if 'selected_topics' in st.session_state else []
    num_selected = len(selected_topics)
    final_question_count = st.session_state.get('final_question_count', 40)
    fair_share = final_question_count // num_selected if num_selected > 0 else 0
    remainder = final_question_count % num_selected if num_selected > 0 else 0
    fair_distribution = {}
    for i, topic in enumerate(selected_topics):
        fair_distribution[topic] = fair_share + (1 if i < remainder else 0)


    with col1:
        st.markdown(t("### 🎵 Zenei témakörök"))
        for topic_key, topic_name in topics.items():
            if "zene" in topic_key or "zenekar" in topic_key or topic_key in {"one_hit_wonders", "sorozat_focimek"}:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{topic_key}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 3 minden témakörnél
                    default_questions = min(3, max_questions)
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    with col2:
        st.markdown(t("### 📚 Egyéb témakörök"))
        other_topics_list = [t for t in topics.items() if "zene" not in t[0] and "zenekar" not in t[0] and t[0] not in {"one_hit_wonders", "sorozat_focimek"}]
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 0:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{topic_key}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 3 minden témakörnél
                    default_questions = min(3, max_questions)
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    with col3:
        st.markdown("### &nbsp;")  # Üres cím a cím magasságához
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 1:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{topic_key}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 3 minden témakörnél
                    default_questions = min(3, max_questions)
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    # Kérdésszámok beállítása
    if st.session_state.selected_topics:
        st.markdown(t("### ⚙️ Kérdésszámok beállítása"))
        
        music_topics = [t for t in st.session_state.selected_topics if "zene" in t or "zenekar" in t or t in {"one_hit_wonders", "sorozat_focimek"}]
        other_topics = [t for t in st.session_state.selected_topics if "zene" not in t and "zenekar" not in t and t not in {"one_hit_wonders", "sorozat_focimek"}]
        
        if music_topics:
            st.markdown(t("#### 🎵 Zenei kérdések beállításai"))
            # Összes zenei kérdés számának kiszámítása
            total_music_questions = sum(len(QUIZ_DATA_BY_TOPIC.get(topic, [])) for topic in music_topics)
            
            # Jelenlegi zenei kérdések összege az egyedi sliders alapján
            current_music_total = sum(st.session_state.get(f'final_{topic}_questions', 0) for topic in music_topics)
            
            col1, col2 = st.columns(2)
            with col1:
                music_total_questions = st.slider(
                    t("Összes zenei kérdés száma"),
                    1,
                    total_music_questions,
                    st.session_state.get('default_music_questions', current_music_total),
                    key="music_total_questions",
                )
            with col2:
                music_auto_distribute = st.checkbox(
                    t("Automatikus elosztás a zenei témakörök között"),
                    True,
                    key="music_auto_distribute",
                )
            
            if not music_auto_distribute:
                st.markdown(t("##### Manuális elosztás:"))
                for topic in music_topics:
                    topic_name = topics.get(topic, topic)
                    if topic == "magyar_zenekarok":
                        max_questions = len(MAGYAR_AUDIO_MAPPING_UJ)
                    else:
                        max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    questions_count = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        0,
                        max_questions,
                        key=f"{topic}_questions",
                    )
        
        if other_topics:
            st.markdown(t("#### 📚 Egyéb témakörök kérdésszámai"))
            
            # Automatikus elosztás egyéb témakörök között
            col1, col2 = st.columns(2)
            with col1:
                other_total_questions = st.slider(
                    t("Összes egyéb kérdés száma"),
                    1,
                    200,
                    st.session_state.get('default_other_questions', 40),
                    key="other_total_questions",
                )
            
            with col2:
                other_auto_distribute = st.checkbox(
                    t("Automatikus elosztás az egyéb témakörök között"),
                    True,
                    key="other_auto_distribute",
                )
            
            if not other_auto_distribute:
                st.markdown(t("##### Manuális elosztás:"))
                cols = st.columns(3)
                for i, topic in enumerate(other_topics):
                    topic_name = topics.get(topic, topic)
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    with cols[i % 3]:
                        questions_count = st.slider(
                            t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                            0,
                            max_questions,
                            key=f"{topic}_questions",
                        )
        

    
    # Quiz indítása
    if st.session_state.selected_topics:
        st.markdown(t("### 🎯 Végleges Kérdésszám Beállítása"))
        
        # Összes elérhető kérdés számának kiszámítása
        total_available_questions = 0
        music_questions = 0
        other_questions = 0
        
        for topic in st.session_state.selected_topics:
            topic_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
            if "zene" in topic or "zenekar" in topic:
                music_questions += topic_questions
            else:
                other_questions += topic_questions
            total_available_questions += topic_questions
        
        # Jelenlegi beállított kérdésszámok összegzése az egyedi sliders alapján
        current_total = 0
        for topic in st.session_state.selected_topics:
            topic_questions = st.session_state.get(f'final_{topic}_questions', 0)
            current_total += topic_questions
        
        # Végleges kérdésszám automatikusan a csúszkák összege (nem módosítható)
        final_question_count = current_total
        
        # Információk megjelenítése
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(t("🎵 Zenei kérdések: {count}", count=music_questions))
        with col2:
            st.info(t("📚 Egyéb kérdések: {count}", count=other_questions))
        with col3:
            st.info(t("📊 Összes elérhető: {count}", count=total_available_questions))
        with col4:
            st.success(t("🎯 Végleges kérdésszám: {count}", count=final_question_count))
        
        # Quiz indítás gomb
        if st.button(t("🚀 Quiz indítása"), type="primary", use_container_width=True):
            # Végleges kérdésszám beállítása mindig a jelenlegi értékre
            st.session_state.final_question_count = final_question_count
            start_quiz()

def show_quiz():
    """Quiz megjelenítése"""
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        st.session_state.quiz_state = 'results'
        st.rerun()
        return
    
    question = st.session_state.quiz_questions[st.session_state.current_question]
    topic = question.get('topic', 'unknown')
    
    # Extra biztonsági ellenőrzés - ha a kérdés érvénytelen, ugorjunk a következőre
    if question.get("question_type") != "text_input" and ("options" not in question or "correct" not in question):
        st.warning(
            t(
                "Érvénytelen kérdés kihagyva: {question}",
                question=question.get("question") or t("Ismeretlen"),
            )
        )
        st.session_state.current_question += 1
        if st.session_state.current_question >= len(st.session_state.quiz_questions):
            st.session_state.quiz_state = 'results'
            st.rerun()
        else:
            st.rerun()
        return
    
    # Navigációs gombok
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_question > 0:
            font_style = get_font_style()
            if st.button(t("⬅️ Előző"), key=f"prev_{st.session_state.current_question}"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        # Központi üres tér a navigációs gombok között
        st.markdown("<div style='text-align: center; padding: 10px;'></div>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
            if st.button(t("Következő ➡️"), key=f"next_{st.session_state.current_question}"):
                st.session_state.current_question += 1
                st.rerun()
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
    st.progress(
        progress,
        text=t(
            "Haladás: {current}/{total}",
            current=st.session_state.current_question + 1,
            total=len(st.session_state.quiz_questions),
        ),
    )
    
    # Pontszám és kérdés sorszám külön mezőkben, 50-50% szélesség
    col1, col2 = st.columns(2)
    
    with col1:
        # Pontszám mező
        score_label = t("🎯 PONTSZÁM")
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #ff6b6b, #ee5a24); border-radius: 15px; border: 3px solid #d32f2f; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <div style='font-size: 16px; color: white; font-weight: bold; margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>{score_label}</div>
            <div style='font-size: 32px; color: white; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{st.session_state.score}</div>
            <div style='font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 5px;'>{(st.session_state.score / len(st.session_state.quiz_questions) * 100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Kérdés sorszám mező
        question_label = t("📝 KÉRDÉS")
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #4CAF50, #45a049); border-radius: 15px; border: 3px solid #2E7D32; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <div style='font-size: 16px; color: white; font-weight: bold; margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>{question_label}</div>
            <div style='font-size: 32px; color: white; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{st.session_state.current_question + 1}</div>
            <div style='font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 5px;'>/ {len(st.session_state.quiz_questions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Egyéb metrikák megjelenítése
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(t("Százalék"), f"{(st.session_state.score / len(st.session_state.quiz_questions) * 100):.1f}%")
    
    with col2:
        # Jelenlegi streak és legmagasabb streak együtt
        current_streak = st.session_state.mode_manager.streak
        max_streak = st.session_state.mode_manager.max_streak
        streak_text = f"{current_streak} ({max_streak})"
        st.metric(t("Streak"), streak_text)
    
    with col3:
        # Mód és nehézségi szint együtt megjelenítése
        mode_text = st.session_state.mode_manager.current_mode.value
        
        # Mód nevek magyarul
        mode_names = {
            "normal": "normál",
            "timed": "időzített",
            "survival": "túlélés",
            "practice": "gyakorlás",
            "challenge": "kihívás"
        }
        mode_name = t(mode_names.get(mode_text, mode_text))
        
        # Nehézségi szint ikonok - string értékekkel
        difficulty_icons = {
            "easy": "🟢",
            "medium": "🟡", 
            "hard": "🔴"
        }
        current_difficulty_value = st.session_state.mode_manager.current_difficulty.value
        difficulty_icon = difficulty_icons.get(current_difficulty_value, "⚪")
        
        # Nehézségi szint szövege - string értékekkel
        difficulty_names = {
            "easy": "könnyű",
            "medium": "közepes", 
            "hard": "nehéz"
        }
        difficulty_name = t(difficulty_names.get(current_difficulty_value, "Ismeretlen"))
        
        # Mód és nehézségi szint együtt
        combined_text = f"{mode_name} {difficulty_icon} {difficulty_name}"
        st.metric(t("Mód"), combined_text)
        
        # Életek megjelenítése külön sorban, ha van
        if st.session_state.mode_manager.lives is not None:
            lives_text = t("Életek: {count}", count=st.session_state.mode_manager.lives)
            st.markdown(
                f"<div style='text-align: center; font-size: 14px; color: #666; margin-top: -10px;'>{lives_text}</div>",
                unsafe_allow_html=True,
            )
    
    # Időzítő (ha van)
    if st.session_state.mode_manager.time_limit:
        time_elapsed = (datetime.now() - st.session_state.question_start_time).total_seconds()
        time_remaining = max(0, st.session_state.mode_manager.time_limit - time_elapsed)
        
        if time_remaining <= 0:
            handle_time_up()
            return
        
        # Időzítő megjelenítése
        timer_text = t("⏱️ Hátralévő idő: {seconds} másodperc", seconds=f"{time_remaining:.1f}")
        st.markdown(
            f"<div style='text-align: center; font-size: 16px; color: {'red' if time_remaining < 10 else 'orange' if time_remaining < 30 else 'green'};'>{timer_text}</div>",
            unsafe_allow_html=True,
        )
    
    # Kérdés megjelenítése
    font_style = get_font_style()
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    
    # Kérdés szövege
    question_text = question.get("question") or t("Ismeretlen kérdés")
    question_number = st.session_state.current_question + 1
    display_question_text = f"{question_number}. {translate_text(question_text)}"
    # Táblázatos kérdések (pl. labdarúgó pályafutás) markdown-ként jelenítjük meg a táblázat megjelenítéséhez
    if "|" in question_text and "---" in question_text:
        st.markdown(display_question_text)
    else:
        st.markdown(f"<div class='question-text' style='{font_style['question']}'>{display_question_text}</div>", unsafe_allow_html=True)

    # Tartós popup megjelenítése (ha van)
    render_answer_popup()
    
    # Audio, Spotify embed vagy kép megjelenítése
    audio_file = get_audio_file_for_question(question, topic)
    if topic in {"nemzetkozi_zenekarok", "magyar_zenekarok", "one_hit_wonders", "sorozat_focimek"}:
        # Minden zenei kérdésnél megpróbáljuk megjeleníteni az audio playert
        if audio_file and os.path.exists(audio_file):
            try:
                abs_path = os.path.abspath(audio_file)
                
                st.audio(abs_path, format="audio/mp3")
            except Exception as e:
                st.error(t("Audio fájl lejátszási hiba: {error}", error=e))
        else:
            st.warning(t("Audio fájl nem található"))
    else:
        # Eredeti logika más témakörökre
        if "audio_file" in question and question["audio_file"]:
            if audio_file and os.path.exists(audio_file):
                try:
                    abs_path = os.path.abspath(audio_file)
                    st.audio(abs_path, format="audio/mp3")
                except Exception as e:
                    st.error(t("Audio fájl lejátszási hiba: {error}", error=e))
            else:
                st.warning(t("Audio fájl nem található"))
    

    
    # Logó vagy festmény kép megjelenítése
    if "logo_path" in question and question["logo_path"]:
        logo_path = question["logo_path"]
        
        # Zászló képek útvonal javítása
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if logo_path.startswith("data/flags/"):
            # Zászlók és zászló részletek (data/flags/, data/flags/crop/)
            if not os.path.exists(logo_path):
                logo_path = os.path.join(current_dir, logo_path)
        
        if os.path.exists(logo_path):
            # Logó középre pozícionálása
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo_path, width=400)
        else:
            st.warning(t("Logó fájl nem található: {path}", path=logo_path))
    
    # Festmény kép megjelenítése
    elif "image_file" in question and question["image_file"]:
        image_file = question["image_file"]
        
        # Festmény képek útvonal javítása
        if not image_file.startswith("/"):
            # Magyar festmények esetén külön mappa
            if question.get("topic") == "magyar_festmenyek":
                image_path = os.path.join("magyar_festmeny_kepek", image_file)
            else:
                image_path = os.path.join("festmény_képek", image_file)
        else:
            image_path = image_file
        
        if os.path.exists(image_path):
            # Ha nagyított állapotban vagyunk, nagyobb képet jelenítünk meg
            if st.session_state.image_modal_states.get(st.session_state.current_question, False):
                # Nagyított kép megjelenítése - nagyobb mérethez igazított oszlopok
                col1, col2, col3 = st.columns([1, 4, 1])
                with col2:
                    # Kép megjelenítése felirat nélkül
                    st.image(image_path, width=800)

                    # Automatikus bezárás időzítő alapérték
                    modal_time_key = f"modal_start_time_{st.session_state.current_question}"
                    modal_started_at = st.session_state.get(modal_time_key)
                    if not isinstance(modal_started_at, (int, float)):
                        modal_started_at = time.time()
                        st.session_state[modal_time_key] = modal_started_at
                    
                    # Bezárás gomb
                    if st.button(t("❌ Kép bezárása"), key=f"close_modal_{st.session_state.current_question}", type="primary", use_container_width=True):
                        st.session_state.image_modal_states[st.session_state.current_question] = False
                        st.session_state.pop(modal_time_key, None)
                        st.rerun()
                    
                    # Automatikus bezárás 30 másodperc után
                    st.info(t("💡 Tipp: A modal automatikusan bezáródik 30 másodperc múlva!"))
                    
                    elapsed_time = time.time() - modal_started_at
                    if elapsed_time > 30:  # 30 másodperc
                        if st.session_state.image_modal_states.get(st.session_state.current_question, False):
                            st.session_state.image_modal_states[st.session_state.current_question] = False
                        st.session_state.pop(modal_time_key, None)
                        st.rerun()
            else:
                # Eredeti kép megjelenítése - eredeti mérethez igazított oszlopok
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.markdown("""
                    <div class="image-container">
                        <img src="data:image/jpeg;base64,{}" alt="Festmény" style="width: 100%; max-width: 400px; height: auto;">
                    </div>
                    """.format(get_image_base64(image_path)), unsafe_allow_html=True)
                    
                    # Kép felirat eltávolítva
                    
                    # Nagyítás gomb
                    if st.button(t("🔍 Kép nagyítása"), key=f"zoom_{st.session_state.current_question}"):
                        st.session_state.image_modal_states[st.session_state.current_question] = True
                        st.rerun()
        else:
            st.warning(t("Festmény kép nem található: {path}", path=image_path))
    
    # Session state inicializálása
    if 'question_answers' not in st.session_state:
        st.session_state.question_answers = {}
    if 'question_options' not in st.session_state:
        st.session_state.question_options = {}
    
    # Válaszlehetőségek randomizálása - csak többválasztós kérdések esetén
    question_type = question.get("question_type", "multiple_choice")
    
    if question_type == "text_input":
        # Text input kérdések esetén nincs szükség options randomizálásra
        pass
    else:
        # Többválasztós kérdések esetén options randomizálás
        if st.session_state.current_question not in st.session_state.question_options:
            try:
                # Minden hozzáférést a try blokkon belül végezünk
                options = question["options"].copy()
                # Biztosan integer legyen a correct index
                correct_index = int(question["correct"])
                correct_answer = options[correct_index]
                random.shuffle(options)
                new_correct_index = options.index(correct_answer)
                display_options = [translate_text(option) for option in options]
                st.session_state.question_options[st.session_state.current_question] = {
                    'options': options,
                    'display_options': display_options,
                    'lang': st.session_state.get("language", "hu"),
                    'correct_index': new_correct_index
                }
            except (KeyError, IndexError, ValueError, TypeError) as e:
                st.error(
                    t(
                        "Hibás kérdés adatok: {error}. Kérdés: {question}",
                        error=e,
                        question=question.get("question") or t("Ismeretlen"),
                    )
                )
                # Automatikusan folytatjuk a következő kérdéssel
                st.session_state.current_question += 1
                if st.session_state.current_question >= len(st.session_state.quiz_questions):
                    st.session_state.quiz_state = 'results'
                    st.rerun()
                else:
                    st.rerun()
                return
        
        # Extra biztonsági ellenőrzés az options_data elérése előtt
        if st.session_state.current_question not in st.session_state.question_options:
            st.error(t("Hibás kérdés adatok - automatikus folytatás"))
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(st.session_state.quiz_questions):
                st.session_state.quiz_state = 'results'
                st.rerun()
            else:
                st.rerun()
            return
        
        options_data = st.session_state.question_options[st.session_state.current_question]
        options = options_data['options']
        current_lang = st.session_state.get("language", "hu")
        if options_data.get('lang') != current_lang:
            options_data['display_options'] = [translate_text(option) for option in options]
            options_data['lang'] = current_lang
            st.session_state.question_options[st.session_state.current_question] = options_data
        display_options = options_data.get('display_options', options)
        new_correct_index = options_data['correct_index']
    
    # Válasz megjelenítése
    selected_answer = st.session_state.question_answers.get(st.session_state.current_question)
    
    # Ha már válaszoltunk, mutassuk meg az eredményt
    if selected_answer is not None:
        if question_type == "text_input":
            # Text input kérdések esetén a válasz szöveges
            is_correct = _is_text_answer_correct(selected_answer, question.get("correct_answer", ""))
        else:
            # Többválasztós kérdések esetén index alapú
            is_correct = selected_answer == new_correct_index
        # --- Helyes válasz gomb (Könnyű módban) ---
        difficulty = st.session_state.mode_manager.current_difficulty
        if question_type == "text_input":
            # Text input kérdések esetén nincs helyes válasz gomb
            pass
        elif difficulty == DifficultyLevel.EASY and new_correct_index < len(options):
            st.markdown(f"""
                            <div style=\"position: fixed; bottom: 40px; right: 20px; z-index: 1000;\">
                <div class=\"rotated-answer\">
                    <button style=\"background-color: #28a745; color: white; border: none; border-radius: 8px; padding: 10px 15px; font-size: 16px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.3);\">
                        {display_options[new_correct_index]}
                    </button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Kérdés típus és nehézségi szint alapú válasz megjelenítés
        difficulty = st.session_state.mode_manager.current_difficulty
        question_type = question.get("question_type", "multiple_choice")
        
        # Idióta szavak kérdések vagy nehéz mód (kivéve mitológia): szöveges bevitel
        if question_type == "text_input":
            # Text input kérdések mindig szöveges bevitellel
            st.markdown(t("### 💬 Írd be a válaszod:"))
            
            # Idióta szavak kérdéseknél a correct_answer mezőt használjuk
            correct_answer_raw = question.get("correct_answer", "")
            user_answer = st.text_input(t("Válasz:"), key=f"text_input_{st.session_state.current_question}")
            
            if st.button(t("✅ Válasz beküldése"), key=f"submit_{st.session_state.current_question}", use_container_width=True):
                if user_answer:
                    # Válasz ellenőrzése (case-insensitive) - részleges egyezés is elfogadható
                    is_correct = _is_text_answer_correct(user_answer, correct_answer_raw)
                    
                    if is_correct:
                        st.session_state.score += 1
                    
                    show_answer_popup(question, user_answer, translate_text(correct_answer_raw or ""))
                    
                    # Válasz mentése
                    st.session_state.question_answers[st.session_state.current_question] = user_answer
                    st.session_state.answers.append({
                        'question': question.get("question", t("Ismeretlen kérdés")),
                        'selected': user_answer,
                        'correct': question.get('correct_answer', ''),
                        'options': [],
                        'is_correct': is_correct,
                        'time_taken': (datetime.now() - st.session_state.question_start_time).total_seconds()
                    })
                    
                    # Streak frissítése
                    st.session_state.mode_manager.update_streak(is_correct)
                    
                    # Következő kérdés
                    if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                        st.session_state.current_question += 1
                        st.session_state.question_start_time = datetime.now()
                    else:
                        st.session_state.quiz_state = 'results'
                    st.rerun()
                else:
                    st.warning(t("Kérlek, írj be egy választ!"))
        elif difficulty == DifficultyLevel.HARD and question.get("topic") != "mitológia" and 'options' in locals() and 'new_correct_index' in locals():
            # Nehéz mód: feleletválasztós kérdések szöveges bevitellel
            st.markdown(t("### 💬 Írd be a válaszod:"))
            
            # Nehéz mód kérdéseknél az options alapján
            if 'options' in locals() and 'new_correct_index' in locals():
                correct_answer_raw = question.get("correct_answer") or options[new_correct_index]
                user_answer = st.text_input(t("Válasz:"), key=f"text_input_{st.session_state.current_question}")
                
                if st.button(t("✅ Válasz beküldése"), key=f"submit_{st.session_state.current_question}", use_container_width=True):
                    if user_answer:
                        # Válasz ellenőrzése (case-insensitive)
                        is_correct = _is_text_answer_correct(user_answer, correct_answer_raw)
                        
                        if is_correct:
                            st.session_state.score += 1

                        display_correct = translate_text(correct_answer_raw or "")
                        show_answer_popup(question, user_answer, display_correct)
                        
                        # Válasz mentése
                        st.session_state.question_answers[st.session_state.current_question] = user_answer
                        st.session_state.answers.append({
                            'question': question.get("question", t("Ismeretlen kérdés")),
                            'selected': user_answer,
                            'correct': question.get('correct_answer', ''),
                            'options': [],
                            'is_correct': is_correct,
                            'time_taken': (datetime.now() - st.session_state.question_start_time).total_seconds()
                        })
                        
                        # Streak frissítése
                        st.session_state.mode_manager.update_streak(is_correct)
                        
                        # Következő kérdés
                        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                            st.session_state.current_question += 1
                            st.session_state.question_start_time = datetime.now()
                        else:
                            st.session_state.quiz_state = 'results'
                        st.rerun()
                    else:
                        st.warning(t("Kérlek, írj be egy választ!"))
            else:
                # Nehéz mód: feleletválasztós kérdések szöveges bevitellel
                user_answer = st.text_input(t("Válasz:"), key=f"text_input_{st.session_state.current_question}")
                
                if st.button(t("✅ Válasz beküldése"), key=f"submit_{st.session_state.current_question}", use_container_width=True):
                    if user_answer:
                        # Válasz ellenőrzése (case-insensitive)
                        correct_answer_raw = options[new_correct_index]
                        is_correct = _is_text_answer_correct(user_answer, correct_answer_raw)
                        
                        if is_correct:
                            st.session_state.score += 1

                        show_answer_popup(question, user_answer, translate_text(correct_answer_raw))
                        
                        # Válasz mentése
                        st.session_state.question_answers[st.session_state.current_question] = user_answer
                        st.session_state.answers.append({
                            'question': question.get("question", t("Ismeretlen kérdés")),
                            'selected': user_answer,
                            'correct': options[new_correct_index],
                            'options': options,
                            'is_correct': is_correct,
                            'time_taken': (datetime.now() - st.session_state.question_start_time).total_seconds()
                        })
                        
                        # Streak frissítése
                        st.session_state.mode_manager.update_streak(is_correct)
                        
                        # Következő kérdés
                        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                            st.session_state.current_question += 1
                            st.session_state.question_start_time = datetime.now()
                        else:
                            st.session_state.quiz_state = 'results'
                        st.rerun()
                    else:
                        st.warning(t("Kérlek, írj be egy választ!"))
        
        else:
            # Könnyű és Közepes mód: feleletválasztós
            # CSS stílus a betűméret alapján
            st.markdown(f"""
            <style>
            .big-answer-button {{
                {font_style['option']} !important;
                margin: 10px 0 !important;
                height: auto !important;
                min-height: 60px !important;
            }}
            .rotated-answer {{
                transform: rotate(180deg);
                display: inline-block;
            }}
            /* Streamlit gombok nagyobbítása */
            .stButton > button {{
                font-size: 24px !important;
                padding: 20px !important;
                height: auto !important;
                min-height: 60px !important;
                line-height: 1.5 !important;
            }}
            
            /* Dinamikus gomb stílusok */
            .stButton > button[data-selected="correct"] {{
                background-color: #28a745 !important;
                color: white !important;
                border: 3px solid #28a745 !important;
            }}
            
            .stButton > button[data-selected="incorrect"] {{
                background-color: #dc3545 !important;
                color: white !important;
                border: 3px solid #dc3545 !important;
            }}
            

            </style>
            """, unsafe_allow_html=True)
            

                

                

            
            # Válaszlehetőségek elrendezése
            col1, col2 = st.columns(2)
            
            # Első sor: 2 válaszlehetőség
            with col1:
                for i in range(0, min(2, len(options))):
                    option = display_options[i]
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help=t("Válaszlehetőség")):
                        handle_answer(i, new_correct_index, options, question, display_options)
            
            with col2:
                for i in range(2, min(4, len(options))):
                    option = display_options[i]
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help=t("Válaszlehetőség")):
                        handle_answer(i, new_correct_index, options, question, display_options)
            
            # Helyes válasz megjelenítése (csak Könnyű módban)
            if difficulty == DifficultyLevel.EASY and new_correct_index < len(options):
                st.markdown(f"""
                <div style="position: fixed; bottom: 40px; right: 20px; z-index: 1000;">
                    <div class="rotated-answer">
                        <button style="background-color: #28a745; color: white; border: none; border-radius: 8px; padding: 10px 15px; font-size: 16px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                            {display_options[new_correct_index]}
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            

            
            # Automatikus válasz beküldés (opcionális)
            if st.button(t("😊 Jó napom van!"), key=f"auto_answer_{st.session_state.current_question}", use_container_width=True):
                # Véletlenszerű válasz kiválasztása
                random_answer = random.randint(0, len(options) - 1)
                handle_answer(random_answer, new_correct_index, options, question, display_options)
    
    # Kvíz újraindítás gomb minden kérdéshez (a válaszlehetőségek után)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(t("🔄 Kvíz újraindítása"), key=f"restart_{st.session_state.current_question}", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_answer(selected_index, correct_index, options, question, display_options=None):
    """Válasz kezelése"""
    is_correct = selected_index == correct_index
    
    # Pontszám frissítése
    if is_correct:
        st.session_state.score += 1
    
    # Streak frissítése
    st.session_state.mode_manager.update_streak(is_correct)
    
    # Élet elvesztése (Survival mód)
    if not is_correct and st.session_state.mode_manager.lives is not None:
        if not st.session_state.mode_manager.lose_life():
            # Nincs több élet - játék vége
            st.session_state.quiz_state = 'results'
            st.rerun()
            return
    
    # Válasz mentése
    display_options = display_options or options
    selected_text = display_options[selected_index] if 0 <= selected_index < len(display_options) else ""
    correct_text = display_options[correct_index] if 0 <= correct_index < len(display_options) else ""
    show_answer_popup(question, selected_text, correct_text)
    st.session_state.question_answers[st.session_state.current_question] = selected_index
    st.session_state.answers.append({
        'question': question.get("question", t("Ismeretlen kérdés")),
        'selected': selected_index,
        'correct': correct_index,
        'options': options,
        'is_correct': is_correct,
        'time_taken': (datetime.now() - st.session_state.question_start_time).total_seconds()
    })
    
    # Következő kérdésre lépés
    if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
        st.session_state.current_question += 1
        st.session_state.question_start_time = datetime.now()
    else:
        st.session_state.quiz_state = 'results'
    st.rerun()

def handle_time_up():
    """Idő lejárt kezelése"""
    question = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Ellenőrizzük, hogy van-e options_data
    if st.session_state.current_question not in st.session_state.question_options:
        # Ha nincs options_data, automatikusan rossz válasz
        st.session_state.question_answers[st.session_state.current_question] = -1
        st.session_state.answers.append({
            'question': question.get("question", t("Ismeretlen kérdés")),
            'selected': -1,
            'correct': -1,
            'options': [],
            'is_correct': False,
            'time_taken': st.session_state.mode_manager.time_limit
        })
    else:
        options_data = st.session_state.question_options[st.session_state.current_question]
        
        # Automatikusan rossz válasz
        st.session_state.question_answers[st.session_state.current_question] = -1
        st.session_state.answers.append({
            'question': question["question"],
            'selected': -1,
            'correct': options_data['correct_index'],
            'options': options_data['options'],
            'is_correct': False,
            'time_taken': st.session_state.mode_manager.time_limit
        })
    
    # Streak reset
    st.session_state.mode_manager.update_streak(False)
    
    # Élet elvesztése (ha van)
    if st.session_state.mode_manager.lives is not None:
        if not st.session_state.mode_manager.lose_life():
            st.session_state.quiz_state = 'results'
            st.rerun()
    
    # Következő kérdés
    if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
        st.session_state.current_question += 1
        st.session_state.question_start_time = datetime.now()
        st.rerun()
    else:
        st.session_state.quiz_state = 'results'
        st.rerun()

def show_results():
    """Eredmények megjelenítése"""
    st.title(t("🏆 Quiz Eredmények"))
    st.markdown("---")
    
    # Eredmények számítása
    total_questions = len(st.session_state.quiz_questions)
    correct_answers = st.session_state.score
    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Idő számítása
    if st.session_state.quiz_start_time:
        end_time = datetime.now()
        duration = end_time - st.session_state.quiz_start_time
        duration_seconds = duration.total_seconds()
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
    else:
        duration_seconds = 0
        minutes, seconds = 0, 0
    
    # Pontszám kiszámítása (fejlett módokhoz)
    scoring_result = QuizScoring.calculate_score(
        st.session_state.mode_manager.current_mode,
        st.session_state.mode_manager.current_difficulty,
        correct_answers,
        total_questions,
        duration_seconds,
        st.session_state.mode_manager.max_streak,
        st.session_state.mode_manager.lives
    )
    
    # Analytics rögzítése
    player_name = st.session_state.get("selected_player", "").strip() or "Ismeretlen"
    quiz_data = {
        "player": player_name,
        "client_ip": get_client_ip(),
        "topics": st.session_state.selected_topics,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percentage": percentage,
        "duration_seconds": duration_seconds,
        "question_details": st.session_state.answers
    }
    
    # Analytics objektum ellenőrzése és inicializálása ha szükséges
    if 'analytics' not in st.session_state:
        st.session_state.analytics = QuizAnalytics()
    
    try:
        st.session_state.analytics.record_quiz_session(quiz_data)
    except Exception as e:
        st.warning(t("Analytics rögzítés sikertelen: {error}", error=e))
    
    # Eredmények megjelenítése - jobb formázással
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=t("📊 Alap Pontszám"),
            value=f"{correct_answers}/{total_questions}",
            delta=f"{percentage:.1f}%"
        )
    
    with col2:
        st.metric(
            label=t("⏱️ Idő"),
            value=t("{minutes} perc {seconds} mp", minutes=minutes, seconds=seconds),
        )
    
    with col3:
        st.metric(
            label=t("🏆 Végső Pontszám"),
            value=scoring_result['final_score'],
            delta=t("Szorzó: {multiplier}x", multiplier=scoring_result['difficulty_multiplier']),
        )
    
    with col4:
        # Értékelés
        if scoring_result['final_score'] >= 90:
            grade = t("🏅 Kiváló")
            grade_color = "success"
        elif scoring_result['final_score'] >= 80:
            grade = t("🥈 Jó")
            grade_color = "success"
        elif scoring_result['final_score'] >= 70:
            grade = t("🥉 Közepes")
            grade_color = "warning"
        elif scoring_result['final_score'] >= 60:
            grade = t("📝 Megfelelő")
            grade_color = "warning"
        else:
            grade = t("❌ Elégtelen")
            grade_color = "error"
        
        st.metric(
            label=t("📈 Értékelés"),
            value=grade
        )
    
    # Részletes pontszámítás
    st.markdown(t("### 📋 Részletes Pontszámítás"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_streak_label = t("🔥 Maximális streak")
        max_streak_value = t("{count} kérdés", count=st.session_state.mode_manager.max_streak)
        avg_time_label = t("⏱️ Átlagos válaszidő")
        avg_time_value = t("{seconds} másodperc", seconds=f"{duration_seconds/total_questions:.1f}")
        st.markdown(f"""
        <div class="summary-box">
            <h4>{max_streak_label}</h4>
            <p><strong>{max_streak_value}</strong></p>
            
            <h4>{avg_time_label}</h4>
            <p><strong>{avg_time_value}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        mode_label = t("🎮 Mód")
        difficulty_label = t("🎯 Nehézség")
        mode_names = {
            "normal": "normál",
            "timed": "időzített",
            "survival": "túlélés",
            "practice": "gyakorlás",
            "challenge": "kihívás",
        }
        difficulty_names = {
            "easy": "könnyű",
            "medium": "közepes",
            "hard": "nehéz",
        }
        mode_display = t(mode_names.get(st.session_state.mode_manager.current_mode.value, st.session_state.mode_manager.current_mode.value))
        difficulty_display = t(difficulty_names.get(st.session_state.mode_manager.current_difficulty.value, st.session_state.mode_manager.current_difficulty.value))
        st.markdown(f"""
        <div class="summary-box">
            <h4>{mode_label}</h4>
            <p><strong>{mode_display}</strong></p>
            
            <h4>{difficulty_label}</h4>
            <p><strong>{difficulty_display}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Játékos statisztika
    player_name = st.session_state.get("selected_player", "").strip() or "Ismeretlen"
    st.markdown(t("### 👤 Játékos: {player}", player=t(player_name)))
    
    # Játékos teljesítmény lekérdezése
    if 'analytics' in st.session_state:
        player_performance = st.session_state.analytics.get_player_performance()
        if player_name in player_performance:
            player_data = player_performance[player_name]
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(t("📊 Összes Quiz"), player_data["total_quizzes"])
            with col2:
                st.metric(t("🎯 Átlagos Pontszám"), f"{player_data['average_score']:.1f}%")
            with col3:
                st.metric(t("🏆 Legjobb Pontszám"), f"{player_data['best_score']:.1f}%")
            with col4:
                st.metric(t("📝 Összes Kérdés"), player_data["total_questions"])
    
    # Részletes eredmények
    st.markdown(t("### 📋 Kérdésenkénti eredmények"))
    
    font_style = get_font_style()
    
    question_label = t("Kérdés:")
    your_answer_label = t("Válaszod:")
    correct_answer_label = t("Helyes válasz:")
    answer_time_label = t("Válaszidő:")
    time_up_text = t("Idő lejárt")
    quiz_questions = st.session_state.get("quiz_questions", [])
    music_topics = {"komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"}

    for i, answer in enumerate(st.session_state.answers):
        is_correct = answer['is_correct']
        status = "✅" if is_correct else "❌"
        question_heading = t("{status} Kérdés {index}", status=status, index=i + 1)
        display_question = translate_text(answer.get('question', ''))
        selected_answer = (
            answer['selected']
            if isinstance(answer['selected'], str)
            else (translate_text(answer['options'][answer['selected']]) if answer['selected'] >= 0 else time_up_text)
        )
        correct_answer = (
            translate_text(answer['correct'])
            if isinstance(answer['correct'], str)
            else translate_text(answer['options'][answer['correct']])
        )
        answer_time = t("{seconds} másodperc", seconds=f"{answer['time_taken']:.1f}")
        
        st.markdown(f"""
        <div class="summary-box">
            <h4 style="{font_style['subtitle']}">{question_heading}</h4>
            <p style="{font_style['explanation']}"><strong>{question_label}</strong> {display_question}</p>
            <p style="{font_style['explanation']}"><strong>{your_answer_label}</strong> {selected_answer}</p>
            <p style="{font_style['explanation']}"><strong>{correct_answer_label}</strong> {correct_answer}</p>
            <p style="{font_style['explanation']}"><strong>{answer_time_label}</strong> {answer_time}</p>
        </div>
        """, unsafe_allow_html=True)

        if not is_correct and i < len(quiz_questions):
            question_data = quiz_questions[i]
            if isinstance(question_data, dict):
                topic = question_data.get("topic")
                has_audio = (
                    topic in music_topics
                    or question_data.get("audio_file")
                    or question_data.get("spotify_preview_url")
                    or question_data.get("spotify_embed")
                )
                if has_audio:
                    with st.expander(t("🎵 Track újra lejátszása"), expanded=False):
                        audio_path = get_audio_file_for_question(question_data, topic)
                        if audio_path:
                            if isinstance(audio_path, str) and os.path.exists(audio_path):
                                st.audio(audio_path, format="audio/mp3")
                            else:
                                st.audio(audio_path)
                        else:
                            st.info(t("Nincs elérhető audio ehhez a kérdéshez."))
    
    # Új quiz indítása
    if st.button(t("🔄 Új quiz indítása"), type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()

def show_analytics_page():
    """Analytics oldal megjelenítése"""
    from quiz_analytics import show_analytics_dashboard
    show_analytics_dashboard()

def show_settings_page():
    """Beállítások oldal megjelenítése"""
    font_style = get_font_style()
    st.markdown(t("## ⚙️ Beállítások"))
    
    st.markdown(t("### 🎯 Quiz Beállítások"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(t("#### Alapértelmezett beállítások"))
        default_music_questions = st.number_input(
            t("Alapértelmezett zenei kérdések"),
            1,
            20,
            st.session_state.get('default_music_questions', 10),
        )
        default_other_questions = st.number_input(
            t("Alapértelmezett egyéb kérdések"),
            1,
            100,
            st.session_state.get('default_other_questions', 40),
        )
    
    with col2:
        st.markdown(t("#### Időzítő beállítások"))
        default_timed_limit = st.number_input(
            t("Alapértelmezett időkorlát (másodperc)"),
            10,
            60,
            st.session_state.get('default_timed_limit', 30),
        )
        default_challenge_limit = st.number_input(
            t("Kihívás mód időkorlát (másodperc)"),
            10,
            30,
            st.session_state.get('default_challenge_limit', 20),
        )
    
    st.markdown(t("### 🎵 Audio Beállítások"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_play_audio = st.checkbox(t("Automatikus audio lejátszás"), st.session_state.get('auto_play_audio', False))
        show_audio_filename = st.checkbox(t("Audio fájlnév megjelenítése"), st.session_state.get('show_audio_filename', True))
    
    with col2:
        audio_volume = st.slider(t("Alapértelmezett hangerő"), 0, 100, st.session_state.get('audio_volume', 50))
        audio_quality_options = ["Alacsony", "Közepes", "Magas"]
        audio_quality = st.selectbox(
            t("Audio minőség"),
            audio_quality_options,
            index=audio_quality_options.index(st.session_state.get('audio_quality', "Közepes")),
            format_func=lambda option: t(option),
        )
    
    st.markdown(t("### 📊 Analytics Beállítások"))
    
    col1, col2 = st.columns(2)
    
    with col1:
        track_performance = st.checkbox(t("Teljesítmény követése"), st.session_state.get('track_performance', True))
        save_detailed_results = st.checkbox(t("Részletes eredmények mentése"), st.session_state.get('save_detailed_results', True))
    
    with col2:
        analytics_retention_days = st.number_input(
            t("Analytics adatok megőrzése (nap)"),
            30,
            365,
            st.session_state.get('analytics_retention_days', 90),
        )
        export_analytics = st.checkbox(t("Analytics exportálása"), st.session_state.get('export_analytics', False))
    
    # Beállítások mentése
    if st.button(t("💾 Beállítások mentése"), type="primary"):
        # Beállítások mentése session state-be
        st.session_state.default_music_questions = default_music_questions
        st.session_state.default_other_questions = default_other_questions
        st.session_state.default_timed_limit = default_timed_limit
        st.session_state.default_challenge_limit = default_challenge_limit
        st.session_state.auto_play_audio = auto_play_audio
        st.session_state.show_audio_filename = show_audio_filename
        st.session_state.audio_volume = audio_volume
        st.session_state.audio_quality = audio_quality
        st.session_state.track_performance = track_performance
        st.session_state.save_detailed_results = save_detailed_results
        st.session_state.analytics_retention_days = analytics_retention_days
        st.session_state.export_analytics = export_analytics
        st.success(t("Beállítások mentve!"))

def show_audio_addition_page():
    """Audio hozzáadása oldal megjelenítése"""
    st.markdown(t("## 🎵 Audio Hozzáadása"))
    
    # Két fő opció
    option = st.radio(
        t("Válassz hozzáadási módszert:"),
        [
            "A) Track hozzáadása YouTube kereséssel",
            "B) Spotify playlist alapú keresés",
            "C) Tömeges feltöltés yt-link alapján",
        ],
        format_func=lambda x: t({
            "A) Track hozzáadása YouTube kereséssel": "🎵 A) YouTube Keresés",
            "B) Spotify playlist alapú keresés": "🎵 B) Spotify Playlist",
            "C) Tömeges feltöltés yt-link alapján": "📥 C) Tömeges YouTube linkek",
        }[x]),
    )
    
    if option == "A) Track hozzáadása YouTube kereséssel":
        show_youtube_search_tab()
    elif option == "B) Spotify playlist alapú keresés":
        show_spotify_playlist_tab()
    else:
        show_bulk_youtube_upload_tab()

def show_bulk_youtube_upload_tab():
    """Tömeges YouTube link integrálás"""
    st.markdown(t("### 📥 Tömeges feltöltés yt-link alapján"))
    st.caption(t("Minden link ugyanabba a kategóriába kerül. 1 sor = 1 link."))

    music_categories = {
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi",
        "one_hit_wonders": "⭐ One Hit Wonders",
        "sorozat_focimek": "📺 Sorozat főcímek",
    }
    category_options = ["— Válassz kategóriát —"] + list(music_categories.keys())
    selected_category = st.selectbox(
        t("Kategória (kötelező):"),
        category_options,
        format_func=lambda x: t(music_categories.get(x, x)),
        index=0,
        key="bulk_category_select",
    )
    if selected_category == "— Válassz kategóriát —":
        selected_category = None

    links_text = st.text_area(
        t("YouTube linkek"),
        placeholder=t("https://www.youtube.com/watch?v=...\nhttps://youtu.be/..."),
        height=200,
        key="bulk_links_text",
    )

    cookies_file = st.file_uploader(
        t("Cookies.txt (opcionális, 403 tiltás ellen)"),
        type=["txt"],
        key="bulk_cookies_file",
        help=t("Netscape formátumú cookie fájl. Bejelentkezett böngészőből exportálható."),
    )

    if st.button(t("🚀 Tömeges integrálás"), type="primary"):
        if not selected_category:
            st.warning(t("⚠️ Válassz kötelező kategóriát!"))
            return
        links = [line.strip() for line in links_text.splitlines() if line.strip()]
        links = [ln for ln in links if "youtu" in ln]
        links = list(dict.fromkeys(links))
        if not links:
            st.warning(t("⚠️ Adj meg legalább egy érvényes YouTube linket!"))
            return

        cookies_path = None
        if cookies_file is not None:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
                tmp.write(cookies_file.getbuffer())
                cookies_path = tmp.name

        progress_bar = st.progress(0)
        status_text = st.empty()

        successes = []
        failures = []
        added_audio_paths = []

        for idx, link in enumerate(links):
            status_text.info(
                t("🔄 Feldolgozás: {current}/{total}", current=idx + 1, total=len(links))
            )
            normalized_link = link
            if "youtube.com/results?search_query=" in link:
                import urllib.parse
                parsed = urllib.parse.urlparse(link)
                query = urllib.parse.parse_qs(parsed.query).get("search_query", [""])[0]
                if query:
                    normalized_link = f"ytsearch1:{query}"
            track_info = {"url": normalized_link}
            result = download_and_integrate_track(
                track_info,
                selected_category,
                custom_options=None,
                require_review=False,
                clip_seconds=180,
                return_metadata=True,
                cookies_path=cookies_path,
            )
            if isinstance(result, dict) and result.get("success"):
                successes.append(link)
                if result.get("audio_file"):
                    added_audio_paths.append(result["audio_file"])
            else:
                failures.append(link)
            progress_bar.progress((idx + 1) / len(links))

        # Cache frissítés
        cache_keys_to_delete = []
        for key in st.session_state.keys():
            if (key.startswith("audio_track_data_") or
                key.startswith("duration_") or
                key.startswith("track_cache_") or
                key == "modified_questions"):
                cache_keys_to_delete.append(key)
        for key in cache_keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state['force_refresh'] = True

        # Git sync (kérdés + audio)
        if successes:
            question_file_by_category = {
                "magyar_zenekarok": "topics/magyar_zenekarok_uj.py",
                "nemzetkozi_zenekarok": "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py",
                "komolyzene": "topics/komolyzene_uj.py",
                "one_hit_wonders": "topics/one_hit_wonders.py",
                "sorozat_focimek": "topics/sorozat_focimek.py",
            }
            question_file_path = question_file_by_category.get(selected_category)
            try:
                if question_file_path:
                    subprocess.run(['git', 'add', question_file_path], check=True)
                for audio_path in added_audio_paths:
                    if audio_path:
                        subprocess.run(['git', 'add', audio_path], check=True)
                commit_msg = f"Bulk add tracks ({selected_category})"
                subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                subprocess.run(['git', 'push'], check=True)
                st.success(t("✅ Tömeges integráció kész, GitHub szinkronizálva."))
            except subprocess.CalledProcessError as e:
                st.warning(t("⚠️ Git szinkronizáció sikertelen: {error}", error=e))
                st.success(t("✅ Tömeges integráció kész, cache frissítve."))

        if cookies_path:
            try:
                import os
                os.remove(cookies_path)
            except Exception:
                pass

        if failures:
            st.warning(t("⚠️ Sikertelen linkek: {count}", count=len(failures)))
            st.code("\n".join(failures))
        else:
            st.success(t("✅ Feldolgozva: {count} link", count=len(successes)))

def show_spotify_playlist_main():
    """Spotify playlist fő képernyő"""
    
    try:
        from spotify_playlist_integration import SpotifyPlaylistQuiz, format_duration, format_views
        
        # Spotify Playlist Quiz inicializálása
        if 'spotify_quiz' not in st.session_state:
            st.session_state.spotify_quiz = SpotifyPlaylistQuiz()
        
        # OAuth token visszaállítása session state-ből
        if 'oauth_token' in st.session_state and 'oauth_token_expires' in st.session_state:
            if time.time() < st.session_state.oauth_token_expires:
                st.session_state.spotify_quiz.restore_oauth_token(
                    st.session_state.oauth_token, 
                    st.session_state.oauth_token_expires
                )
        
        # CSS stílus a rejtett st.button-ok elrejtéséhez
        st.markdown("""
        <style>
        /* Rejtett st.button-ok elrejtése */
        .stButton > button {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
        }
        
        /* Rejtett st.button-ok teljes elrejtése */
        div[data-testid="stButton"] {
            display: none !important;
        }
        
        /* Rejtett st.button-ok konténer elrejtése */
        .stButton {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.header("🎵 Spotify Playlist Feldolgozás")
        
        # OAuth beállítás szekció
        with st.expander("🔐 Spotify OAuth Beállítás (Nyilvános playlistekhez)", expanded=False):
            st.markdown("**A nyilvános Spotify playlistek eléréséhez OAuth autentikáció szükséges.**")
            
            # OAuth URL generálás
            if st.button("🔗 OAuth URL Generálása"):
                auth_url = st.session_state.spotify_quiz.get_oauth_authorization_url()
                st.markdown(f"**Nyisd meg ezt a linket a böngészőben:**")
                st.code(auth_url)
                st.info("1. Kattints a linkre és engedélyezd a hozzáférést")
                st.info("2. Másold ki az authorization code-ot az URL-ből")
                st.info("3. Illeszd be az authorization code-ot alább")
            
            # Authorization code bevitel
            auth_code = st.text_input(
                "Authorization Code:",
                placeholder="Például: AQAA...",
                help="Illeszd be az authorization code-ot a Spotify OAuth flow-ból"
            )
            
            if st.button("🔑 OAuth Token Beállítása"):
                if auth_code:
                    with st.spinner("OAuth token beállítása..."):
                        success = st.session_state.spotify_quiz.set_oauth_access_token(auth_code)
                        if success:
                            st.success("✅ OAuth token sikeresen beállítva!")
                            st.info("Most már elérheted a nyilvános Spotify playlisteket!")
                        else:
                            st.error("❌ OAuth token beállítása sikertelen!")
                else:
                    st.warning("⚠️ Kérlek add meg az authorization code-ot!")
            
            # OAuth állapot megjelenítése
            if hasattr(st.session_state.spotify_quiz.playlist_manager, 'oauth_access_token') and st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                if time.time() < token_expires:
                    remaining_time = int(token_expires - time.time())
                    st.success(f"✅ OAuth token aktív (Hátralévő idő: {remaining_time} másodperc)")
                else:
                    st.warning("⚠️ OAuth token lejárt, újra kell autentikálni!")
            else:
                st.info("ℹ️ Nincs aktív OAuth token")
        
        # Spotify playlist URL beviteli mező
        playlist_url = st.text_input(
            "Spotify Playlist URL:",
            placeholder="https://open.spotify.com/playlist/...",
            help="Add meg a Spotify playlist URL-jét"
        )
        
        # Playlist betöltés gomb
        if st.button("📥 Playlist Betöltése", type="primary"):
            if playlist_url:
                with st.spinner("Playlist betöltése..."):
                    try:
                        # Spotify playlist betöltése
                        tracks = st.session_state.spotify_quiz.get_playlist_tracks(playlist_url)
                        if tracks:
                            st.session_state.playlist_tracks = tracks
                            st.success(f"✅ {len(tracks)} track betöltve!")
                            st.rerun()
                        else:
                            st.error("❌ Nem sikerült betölteni a playlist-et")
                    except Exception as e:
                        st.error(f"❌ Hiba a playlist betöltésekor: {e}")
            else:
                st.warning("⚠️ Kérlek add meg a playlist URL-jét!")
        
        # Playlist elemek megjelenítése
        if hasattr(st.session_state, 'playlist_tracks') and st.session_state.playlist_tracks:
            st.subheader(f"📋 Playlist Elemek ({len(st.session_state.playlist_tracks)} track)")
            
            # Statisztikák
            downloaded_count = sum(1 for track in st.session_state.playlist_tracks if track.get('downloaded', False))
            youtube_ready_count = sum(1 for track in st.session_state.playlist_tracks if track.get('youtube_url'))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Összesen", len(st.session_state.playlist_tracks))
            with col2:
                st.metric("✅ Letöltve", downloaded_count)
            with col3:
                st.metric("📺 YouTube kész", youtube_ready_count)
            
            # Grid layout a trackekhez
            cols_per_row = 3
            for i in range(0, len(st.session_state.playlist_tracks), cols_per_row):
                row_tracks = st.session_state.playlist_tracks[i:i + cols_per_row]
                cols = st.columns(cols_per_row)

                for j, track in enumerate(row_tracks):
                    with cols[j]:
                        # Track azonosító
                        track_id = track.get('id', f"track_{i}_{j}")
                        
                        # Album Art Work megjelenítése kattinthatóként
                        if track.get('album_art_url'):
                            # Album art megjelenítése
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="{track['album_art_url']}" 
                                     alt="Album Art" 
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Placeholder kép megjelenítése
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="https://picsum.photos/150/150?random={i}_{j}" 
                                     alt="No Image" 
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Kattintható gomb a letöltéshez
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button(
                                f"🎵 {track['name']}",
                                key=f"download_{track_id}",
                                help=f"Kattints a letöltéshez: {track['name']}",
                                use_container_width=True
                            ):
                                # YouTube keresés csak kattintás után
                                if not track.get('youtube_url'):
                                    with st.spinner(f"YouTube keresés: {track['name']}..."):
                                        youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                        if youtube_result:
                                            track['youtube_url'] = youtube_result.get('url')
                                            track['youtube_title'] = youtube_result.get('title')
                                            track['youtube_views'] = youtube_result.get('views')
                                            track['youtube_duration'] = youtube_result.get('duration')
                                            track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')  # Thumbnail URL mentése
                                            track['youtube_found'] = True
                                            st.success("✅ YouTube találat!")
                                            st.rerun()  # Frissítés a thumbnail megjelenítéséhez
                                        else:
                                            # Csak egy egyszerű üzenet, nem hiba
                                            st.info("ℹ️ YouTube keresés folyamatban...")
                                            st.rerun()
                                            return
                                
                                # MP3 letöltés YouTube URL-rel
                                if track.get('youtube_url'):
                                    with st.spinner(f"MP3 letöltés: {track['name']}..."):
                                        try:
                                            # Audio letöltés
                                            audio_path = st.session_state.spotify_quiz.audio_downloader.download_track(
                                                track['youtube_url'], 
                                                track
                                            )
                                            if audio_path:
                                                # Sikeres letöltés - track állapot frissítése
                                                track['downloaded'] = True
                                                track['audio_path'] = audio_path
                                                st.success(f"✅ MP3 letöltve: {os.path.basename(audio_path)}")
                                                # Audio fájl megjelenítése
                                                with open(audio_path, "rb") as audio_file:
                                                    st.audio(audio_file.read(), format="audio/mp3")
                                                st.rerun()  # Frissítés a zöld állapot megjelenítéséhez
                                            else:
                                                st.error("❌ MP3 letöltés sikertelen")
                                        except Exception as e:
                                            st.error(f"❌ Letöltési hiba: {e}")
                                        else:
                                            st.info("ℹ️ YouTube keresés szükséges a letöltéshez")
                        
                        # Track információk
                        st.markdown(f"**{track['name']}**")
                        st.markdown(f"*{', '.join(track['artists'])}*")
                        st.markdown(f"⏱️ {format_duration(track['duration_ms'])}")
                        

                        # Linkek
                        if track.get('external_url'):
                            st.markdown(f"[🎵 Spotify]({track['external_url']})")
                        if track.get('youtube_url'):
                            st.markdown(f"[📺 YouTube]({track['youtube_url']})")
                        
                        # Letöltési állapot megjelenítése
                        if track.get('downloaded', False):
                            st.markdown(
                                f"<div style='color: green; font-weight: bold;'>✅ Letöltve</div>", 
                                unsafe_allow_html=True
                            )

                        st.markdown("---")
            
            # Részletes táblázat is elérhető
            with st.expander("📊 Részletes Táblázat"):
                # Táblázat adatok előkészítése
                table_data = []
                for i, track in enumerate(st.session_state.playlist_tracks):
                    row = {
                        "Sorszám": i + 1,
                        "Cím": track['name'],
                        "Előadó": ", ".join(track['artists']),
                        "Album": track['album'],
                        "Hossz": format_duration(track['duration_ms']),
                        "YouTube": "✅" if track.get('youtube_url') else "❌"
                    }

                    if track.get('youtube_url'):
                        row["YouTube Cím"] = track.get('youtube_title', 'N/A')
                        row["YouTube Hossz"] = format_duration(track.get('youtube_duration', 0) * 1000) if track.get('youtube_duration') else 'N/A'
                        row["Nézettség"] = format_views(track.get('youtube_views', 0)) if track.get('youtube_views') else 'N/A'

                    table_data.append(row)

                # Táblázat megjelenítése
                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )
    
    except ImportError:
        st.error("❌ Spotify playlist funkció nem elérhető")
        st.info("A spotify_playlist_integration.py fájl szükséges")
        st.code("pip install yt-dlp")

def show_spotify_playlist_tab():
    """Spotify playlist tab megjelenítése"""
    st.markdown("### 🎵 Spotify Playlist Feldolgozás")
    
    try:
        from spotify_playlist_integration import SpotifyPlaylistQuiz, format_duration, format_views
        
        # Spotify Playlist Quiz inicializálása
        if 'spotify_quiz' not in st.session_state:
            st.session_state.spotify_quiz = SpotifyPlaylistQuiz()
        
        # OAuth beállítás szekció
        with st.expander("🔐 Spotify OAuth Beállítás (Nyilvános playlistekhez)", expanded=False):
            st.markdown("**A nyilvános Spotify playlistek eléréséhez OAuth autentikáció szükséges.**")
            
            # OAuth URL generálás
            if st.button("🔗 OAuth URL Generálása", key="oauth_url_audio"):
                auth_url = st.session_state.spotify_quiz.get_oauth_authorization_url()
                st.markdown(f"**Nyisd meg ezt a linket a böngészőben:**")
                st.code(auth_url)
                st.info("1. Kattints a linkre és engedélyezd a hozzáférést")
                st.info("2. Másold ki az authorization code-ot az URL-ből")
                st.info("3. Illeszd be az authorization code-ot alább")
            
            # Authorization code bevitel
            auth_code = st.text_input(
                "Authorization Code:",
                placeholder="Például: AQAA...",
                help="Illeszd be az authorization code-ot a Spotify OAuth flow-ból",
                key="auth_code_audio"
            )
            
            if st.button("🔑 OAuth Token Beállítása", key="oauth_token_audio"):
                if auth_code:
                    with st.spinner("OAuth token beállítása..."):
                        success = st.session_state.spotify_quiz.set_oauth_access_token(auth_code)
                        if success:
                            st.success("✅ OAuth token sikeresen beállítva!")
                            st.info("Most már elérheted a nyilvános Spotify playlisteket!")
                            # Token mentése session state-be
                            st.session_state.oauth_token = st.session_state.spotify_quiz.playlist_manager.oauth_access_token
                            st.session_state.oauth_token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                            st.rerun()
                        else:
                            st.error("❌ OAuth token beállítása sikertelen!")
                else:
                    st.warning("⚠️ Kérlek add meg az authorization code-ot!")
            
            # OAuth állapot megjelenítése
            if hasattr(st.session_state.spotify_quiz.playlist_manager, 'oauth_access_token') and st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                if time.time() < token_expires:
                    remaining_time = int(token_expires - time.time())
                    st.success(f"✅ OAuth token aktív (Hátralévő idő: {remaining_time} másodperc)")
                    # Token mentése session state-be
                    st.session_state.oauth_token = st.session_state.spotify_quiz.playlist_manager.oauth_access_token
                    st.session_state.oauth_token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                else:
                    st.warning("⚠️ OAuth token lejárt, újra kell autentikálni!")
            else:
                st.info("ℹ️ Nincs aktív OAuth token")
        
        # Fő tartalom
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📋 Playlist Feldolgozás")
            
            # Playlist URL input
            playlist_url = st.text_input(
                "Spotify Playlist URL",
                value="https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF",
                placeholder="https://open.spotify.com/playlist/...",
                help="Illeszd be a Spotify playlist URL-jét (alapértelmezett: Global Top 50)"
            )
            
            # Playlist feldolgozása
            if st.button("🎵 Playlist Feldolgozása", key="process_playlist"):
                if 'spotify_quiz' not in st.session_state:
                    st.session_state.spotify_quiz = SpotifyPlaylistQuiz()
                
                # OAuth token ellenőrzése
                if not hasattr(st.session_state.spotify_quiz, 'playlist_manager') or \
                   not st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                    st.error("❌ Nincs aktív OAuth token!")
                    st.info("🔐 Kérlek állítsd be az OAuth tokent a fenti expanderben!")
                    return
                
                # Token lejárat ellenőrzése
                if time.time() >= st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at:
                    st.error("❌ Az OAuth token lejárt!")
                    st.info("🔄 Kérlek generálj új tokent!")
                    return
                
                with st.spinner("Playlist feldolgozása..."):
                    try:
                        tracks = st.session_state.spotify_quiz.get_playlist_tracks_only(playlist_url)
                        
                        if tracks:
                            st.session_state.spotify_playlist_tracks = tracks
                            st.success(f"✅ {len(tracks)} track betöltve!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Nincsenek trackek a playlistben!")
                            st.info("🔍 Lehetséges okok:")
                            st.info("• Privát playlist")
                            st.info("• Érvénytelen playlist URL")
                            st.info("• Spotify API hiba")
                    except Exception as e:
                        st.error(f"❌ Hiba a playlist feldolgozásakor: {e}")
                        st.info("🔐 Ellenőrizd az OAuth tokent vagy próbálj másik playlistet!")
        
        with col2:
            st.markdown("### 📊 Debug Információk")
            
            # Debug információk
            if 'spotify_quiz' in st.session_state and hasattr(st.session_state.spotify_quiz, 'playlist_manager'):
                manager = st.session_state.spotify_quiz.playlist_manager
                if manager.oauth_access_token:
                    token_expires = manager.oauth_token_expires_at
                    time_left = token_expires - time.time()
                    if time_left > 0:
                        st.success(f"🔐 OAuth Token aktív ({time_left:.0f}s hátra)")
                        
                        # API teszt gomb
                        if st.button("🧪 API Teszt", key="api_test"):
                            import requests
                            headers = {
                                'Authorization': f'Bearer {manager.oauth_access_token}',
                                'Content-Type': 'application/json'
                            }
                            
                            # Teszt playlist
                            test_url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"
                            response = requests.get(test_url, headers=headers)
                            
                            if response.status_code == 200:
                                data = response.json()
                                st.success(f"✅ API működik!")
                                st.info(f"Playlist: {data.get('name')}")
                                st.info(f"Tracks: {len(data.get('tracks', {}).get('items', []))}")
                            else:
                                st.error(f"❌ API hiba: {response.status_code}")
                                st.error(f"Response: {response.text}")
                    else:
                        st.error("❌ OAuth Token lejárt!")
                else:
                    st.warning("⚠️ Nincs OAuth token")
            
            # Session state debug
            st.markdown("### 🔍 Session State")
            if 'oauth_token' in st.session_state:
                st.info("✅ Token mentve session state-ben")
            else:
                st.warning("⚠️ Token nincs mentve session state-ben")
            
            if hasattr(st.session_state, 'spotify_playlist_tracks') and st.session_state.spotify_playlist_tracks:
                total_tracks = len(st.session_state.spotify_playlist_tracks)
                youtube_tracks = len([t for t in st.session_state.spotify_playlist_tracks if t.get('youtube_url')])
                
                st.metric("Összes track", total_tracks)
                st.metric("🎬 YouTube", youtube_tracks)
                st.metric("Találati arány", f"{youtube_tracks/total_tracks*100:.1f}%")
        
        # Playlist megjelenítése (ha van)
        if hasattr(st.session_state, 'spotify_playlist_tracks') and st.session_state.spotify_playlist_tracks:
            st.markdown("---")
            st.markdown("### 🎵 Playlist Elemek")
            
            # Grid layout a trackekhez
            cols_per_row = 3
            for i in range(0, len(st.session_state.spotify_playlist_tracks), cols_per_row):
                row_tracks = st.session_state.spotify_playlist_tracks[i:i + cols_per_row]
                cols = st.columns(cols_per_row)
                
                for j, track in enumerate(row_tracks):
                    with cols[j]:
                        # Track azonosító
                        track_id = track.get('id', f"track_{i}_{j}")
                        
                        # Album Art Work megjelenítése
                        image_url = None
                        
                        # 1. Először YouTube thumbnail próbálása
                        if track.get('youtube_thumbnail_url'):
                            image_url = track['youtube_thumbnail_url']
                        # 2. Ha nincs YouTube thumbnail, album art
                        elif track.get('album_art_url'):
                            image_url = track['album_art_url']
                        
                        # Kép megjelenítése (csak ha van valódi kép)
                        if image_url:
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="{image_url}" 
                                     alt="Track Image" 
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Ha nincs kép, csak egy üres hely
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0; width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px; display: flex; align-items: center; justify-content: center; background-color: #f0f0f0;">
                                <span style="color: #666; font-size: 12px;">Nincs kép</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Kattintható gomb a letöltéshez
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button(
                                f"🎵 {track['name']}",
                                key=f"download_{track_id}_audio",
                                help=f"Kattints a letöltéshez: {track['name']}",
                                use_container_width=True
                            ):
                                # YouTube keresés csak kattintás után
                                if not track.get('youtube_url'):
                                    with st.spinner(f"YouTube keresés: {track['name']}..."):
                                        youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                        if youtube_result:
                                            track['youtube_url'] = youtube_result.get('url')
                                            track['youtube_title'] = youtube_result.get('title')
                                            track['youtube_views'] = youtube_result.get('views')
                                            track['youtube_duration'] = youtube_result.get('duration')
                                            track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')  # Thumbnail URL mentése
                                            track['youtube_found'] = True
                                            st.success("✅ YouTube találat!")
                                            st.rerun()  # Frissítés a thumbnail megjelenítéséhez
                                        else:
                                            # Csak egy egyszerű üzenet, nem hiba
                                            st.info("ℹ️ YouTube keresés folyamatban...")
                                            st.rerun()
                                            return
                                
                                # MP3 letöltés YouTube URL-rel
                                if track.get('youtube_url'):
                                    with st.spinner(f"MP3 letöltés: {track['name']}..."):
                                        try:
                                            # Audio letöltés
                                            audio_path = st.session_state.spotify_quiz.audio_downloader.download_track(
                                                track['youtube_url'], 
                                                track
                                            )
                                            if audio_path:
                                                # Sikeres letöltés - track állapot frissítése
                                                track['downloaded'] = True
                                                track['audio_path'] = audio_path
                                                st.success(f"✅ MP3 letöltve: {os.path.basename(audio_path)}")
                                                # Audio fájl megjelenítése
                                                with open(audio_path, "rb") as audio_file:
                                                    st.audio(audio_file.read(), format="audio/mp3")
                                                st.rerun()  # Frissítés a zöld állapot megjelenítéséhez
                                            else:
                                                st.error("❌ MP3 letöltés sikertelen")
                                        except Exception as e:
                                            st.error(f"❌ Letöltési hiba: {e}")
                                else:
                                    st.info("ℹ️ YouTube keresés szükséges a letöltéshez")
                        
                        # Track információk
                        st.markdown(f"**{track['name']}**")
                        st.markdown(f"*{', '.join(track['artists'])}*")
                        st.markdown(f"💿 {track['album']}")
                        
                        # Album Art Work megjelenítése
                        image_url = None
                        
                        # 1. Először YouTube thumbnail próbálása
                        if track.get('youtube_thumbnail_url'):
                            image_url = track['youtube_thumbnail_url']
                        # 2. Ha nincs YouTube thumbnail, album art
                        elif track.get('album_art_url'):
                            image_url = track['album_art_url']
                        
                        # Kép megjelenítése (csak ha van valódi kép)
                        if image_url:
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="{image_url}" 
                                     alt="Track Image" 
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Ha nincs kép, csak egy üres hely
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0; width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px; display: flex; align-items: center; justify-content: center; background-color: #f0f0f0;">
                                <span style="color: #666; font-size: 12px;">Nincs kép</span>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        # Kattintható gomb a letöltéshez
                        if not track.get('youtube_url'):
                            if st.button(f"🔍 YouTube Keresés", key=f"youtube_search_{i}_{j}"):
                                with st.spinner(f"YouTube keresés: {track['name']}..."):
                                    youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                    if youtube_result:
                                        track['youtube_url'] = youtube_result.get('url')
                                        track['youtube_title'] = youtube_result.get('title')
                                        track['youtube_views'] = youtube_result.get('views')
                                        track['youtube_duration'] = youtube_result.get('duration')
                                        track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')  # Thumbnail URL mentése
                                        track['youtube_found'] = True
                                        st.success("✅ YouTube találat!")
                                        st.rerun()  # Frissítés a thumbnail megjelenítéséhez
                                    else:
                                        st.info("ℹ️ YouTube keresés folyamatban...")
                                        st.rerun()
                                        return
                        else:
                            if st.button(f"💾 Letöltés", key=f"download_{i}_{j}"):
                                with st.spinner(f"Letöltés: {track['name']}..."):
                                    downloaded_file = st.session_state.spotify_quiz.download_selected_tracks([track], [0])
                                    if downloaded_file:
                                        track['downloaded'] = True
                                        st.success(f"✅ Letöltve: {downloaded_file[0]}")
                                    else:
                                        st.error("❌ Letöltési hiba!")
                        
                        # YouTube információk megjelenítése
                        if track.get('youtube_url'):
                            st.write(f"🎬 [YouTube]({track['youtube_url']})")
                            if track.get('youtube_views'):
                                st.write(f"👁️ {format_views(track['youtube_views'])} nézettség")
                            if track.get('youtube_duration'):
                                st.write(f"⏱️ {format_duration(track['youtube_duration'] * 1000)}")
                        
                        st.divider()
            else:
                st.info("ℹ️ Nincsenek trackek betöltve. Feldolgozz egy playlistet!")
    
    except ImportError:
        st.error("❌ Spotify playlist funkció nem elérhető")
        st.info("A spotify_playlist_integration.py fájl szükséges")
        st.code("pip install yt-dlp")

def show_local_files_tab():
    """Helyi fájlok tab megjelenítése"""
    st.markdown("### 📁 Helyi Audio Fájlok")
    
    st.info("""
    **Helyi audio fájlok kezelése:**
    
    - 📂 Fájl feltöltés
    - 🎵 Audio konvertálás
    - 📝 Metaadatok szerkesztése
    - 🔗 Kvíz kapcsolódás
    
    *Ez a funkció fejlesztés alatt áll...*
    """)
    
    # Fájl feltöltés
    uploaded_file = st.file_uploader(
        "Válassz audio fájlt",
        type=['mp3', 'wav', 'm4a', 'flac'],
        help="Támogatott formátumok: MP3, WAV, M4A, FLAC"
    )
    
    if uploaded_file is not None:
        st.success(f"✅ Fájl feltöltve: {uploaded_file.name}")
        st.info(f"📏 Fájlméret: {uploaded_file.size} bytes")
        
        # Audio lejátszás
        st.audio(uploaded_file, format='audio/mp3')
        
        # Metaadatok szerkesztése
        with st.expander("📝 Metaadatok szerkesztése"):
            col1, col2 = st.columns(2)
            
            with col1:
                title = st.text_input("Cím", value="")
                artist = st.text_input("Előadó", value="")
            
            with col2:
                album = st.text_input("Album", value="")
                year = st.number_input("Év", min_value=1900, max_value=2024, value=2024)
            
            if st.button("💾 Metaadatok mentése"):
                st.success("✅ Metaadatok mentve!")

def show_youtube_links_tab():
    """YouTube linkek tab megjelenítése"""
    st.markdown("### 🔗 YouTube Linkek Feldolgozása")
    
    st.info("""
    **YouTube linkek kezelése:**
    
    - 🔗 YouTube URL feldolgozás
    - 🎵 Audio letöltés
    - 📝 Metaadatok kinyerés
    - 🔍 Keresés és szűrés
    
    *Ez a funkció fejlesztés alatt áll...*
    """)
    
    # YouTube URL input
    youtube_url = st.text_input(
        "YouTube URL",
        placeholder="https://www.youtube.com/watch?v=...",
        help="Illeszd be a YouTube videó URL-jét"
    )
    
    if youtube_url:
        st.info(f"🔗 URL: {youtube_url}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Metaadatok lekérése", type="primary"):
                st.info("🔍 Metaadatok lekérése...")
                # Itt lenne a YouTube metaadatok lekérése
                st.success("✅ Metaadatok lekérve!")
        
        with col2:
            if st.button("⬇️ Audio letöltés", type="primary"):
                st.info("⬇️ Audio letöltés...")
                # Itt lenne a YouTube audio letöltés
                st.success("✅ Audio letöltve!")
        
        # Példa metaadatok
        with st.expander("📋 Példa metaadatok"):
            st.markdown("""
            **Videó információk:**
            - **Cím:** Bohemian Rhapsody - Queen
            - **Csatorna:** Queen Official
            - **Hossz:** 5:55
            - **Nézettség:** 1.2M
            - **Feltöltés dátuma:** 2009.10.02
            
            **Audio információk:**
            - **Minőség:** 192 kbps
            - **Formátum:** MP3
            - **Méret:** 8.2 MB
            """)

def show_youtube_search_tab():
    """YouTube keresés alapú track hozzáadás"""
    st.markdown("### 🎵 YouTube Keresés")
    
    # YouTube keresés
    st.markdown("#### 🔍 YouTube Keresés")
    search_query = st.text_input(
        "Keresési kifejezés:",
        placeholder="Például: Queen Bohemian Rhapsody",
        help="Add meg a keresendő zene címét és előadóját"
    )
    
    if st.button("🔍 Keresés indítása", type="primary"):
        if search_query:
            with st.spinner("YouTube keresés folyamatban..."):
                try:
                    # YouTube keresés implementáció
                    search_results = search_youtube_tracks(search_query)
                    if search_results:
                        st.session_state.youtube_search_results = search_results
                        st.success(f"✅ {len(search_results)} találat!")
                        st.rerun()
                    else:
                        st.error("❌ Nem találtam megfelelő találatokat")
                except Exception as e:
                    st.error(f"❌ Hiba a keresés során: {e}")
        else:
            st.warning("⚠️ Kérlek add meg a keresési kifejezést!")
    
    # Keresési eredmények megjelenítése
    if hasattr(st.session_state, 'youtube_search_results') and st.session_state.youtube_search_results:
        st.markdown("#### 📋 Keresési eredmények")
        
        for i, result in enumerate(st.session_state.youtube_search_results):
            # Pontszám megjelenítése
            score = result.get('score', 0)
            score_emoji = "🏆" if score >= 10 else "⭐" if score >= 5 else "📌"
            
            with st.expander(f"{score_emoji} {result['title']} - {result['channel']} (Pontszám: {score})", expanded=(i == 0)):
                col1, col2, col3 = st.columns([1, 2, 1])
                
                with col1:
                    if result.get('thumbnail'):
                        st.image(result['thumbnail'], width=120)
                    else:
                        st.markdown("📷 Nincs kép")
                
                with col2:
                    st.markdown(f"**Cím:** {result['title']}")
                    st.markdown(f"**Csatorna:** {result['channel']}")
                    st.markdown(f"**Hossz:** {result.get('duration', 'Ismeretlen')}")
                    st.markdown(f"**Nézők:** {result.get('views', 'Ismeretlen')}")
                
                # Középre igazított paraméterezési konténer
                st.markdown("""
                <div style="
                    text-align: center; 
                    margin: 20px auto; 
                    max-width: 600px; 
                    padding: 20px; 
                    background-color: #f8f9fa; 
                    border-radius: 10px; 
                    border: 2px solid #e9ecef;
                ">
                <h4 style="color: #495057; margin-bottom: 15px;">⚙️ Letöltési és integrálási beállítások</h4>
                </div>
                """, unsafe_allow_html=True)
                
                # Középre igazított paraméterek
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    # Kategória választás
                    music_categories = {
                        "magyar_zenekarok": "🎵 Magyar",
                        "nemzetkozi_zenekarok": "🌍 Nemzetközi", 
                        "komolyzene": "🎼 Komolyzene",
                        "one_hit_wonders": "⭐ One Hit Wonders",
                        "sorozat_focimek": "📺 Sorozat főcímek",
                    }
                    
                    selected_category = st.selectbox(
                        "Kategória:",
                        list(music_categories.keys()),
                        key=f"category_{i}",
                        format_func=lambda x: music_categories[x]
                    )
                    
                    # Szerkeszthető válasz opciók
                    st.markdown("**Válasz opciók:**")
                    option_1 = st.text_input("1. helyes válasz:", value=result.get('channel', 'Ismeretlen előadó'), key=f"opt1_{i}")
                    option_2 = st.text_input("2. opció:", value="Bastille", key=f"opt2_{i}")
                    option_3 = st.text_input("3. opció:", value="Imagine Dragons", key=f"opt3_{i}")
                    option_4 = st.text_input("4. opció:", value="The Weeknd", key=f"opt4_{i}")
                    
                    # Letöltés gomb
                    if st.button(f"📥 Letöltés és integrálás", key=f"download_{i}", type="primary", use_container_width=True):
                        st.session_state.integration_status = "starting"
                        st.session_state.integration_error = ""
                        # Középre igazított státuszjelentés konténer
                        st.markdown("""
                        <div style="
                            text-align: center; 
                            margin: 20px auto; 
                            max-width: 800px; 
                            padding: 20px; 
                            background-color: #f0f2f6; 
                            border-radius: 10px; 
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                            font-size: 12px;
                        ">
                        <h3 style="color: #1f77b4; margin-bottom: 20px; font-size: 12px;">📋 Letöltési és integrálási folyamat</h3>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Középre igazított progress konténer
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            progress_bar = st.progress(0)
                            
                            # Státuszjelentés konténer
                            status_container = st.container()
                            
                            with status_container:
                                try:
                                    st.info("🔄 Integráció indult...")
                                    # Egyedi opciók használata
                                    custom_options = [option_1, option_2, option_3, option_4]
                                    
                                    # 1. Lépés: YouTube információk lekérése
                                    st.markdown('<div style="font-size: 12px;">🔍 1. YouTube információk lekérése...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(16)
                                    
                                    # 2. Lépés: Audio letöltése
                                    st.markdown('<div style="font-size: 12px;">📥 2. Audio fájl letöltése...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(33)
                                    
                                    # 3. Lépés: 2 perc kivágása
                                    st.markdown('<div style="font-size: 12px;">✂️ 3. 2 perces rész kivágása...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(50)
                                    
                                    # 4. Lépés: Quiz kérdés generálása
                                    st.markdown('<div style="font-size: 12px;">🎯 4. Quiz kérdés generálása...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(66)
                                    
                                    # 5. Lépés: Kategóriába integrálás
                                    st.markdown('<div style="font-size: 12px;">📂 5. Kategóriába integrálás...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(83)
                                    
                                    # 6. Lépés: GitHub frissítés
                                    st.markdown('<div style="font-size: 12px;">🚀 6. GitHub frissítés...</div>', unsafe_allow_html=True)
                                    progress_bar.progress(100)
                                    
                                    # Track letöltése és integrálása (mentés előtt szerkesztéssel)
                                    integration_result = download_and_integrate_track(
                                        result, selected_category, custom_options, require_review=True
                                    )

                                    if isinstance(integration_result, dict) and integration_result.get("success"):
                                        st.success("✅ Letöltés kész. A mentés előtt még szerkesztheted a kérdést lent.")
                                        st.session_state.pending_integration = integration_result
                                        st.session_state.pending_integration["custom_options"] = custom_options
                                        st.session_state.pending_integration["selected_category"] = selected_category
                                        st.session_state.pending_integration["result_title"] = result.get("title", "Ismeretlen")
                                        st.session_state.integration_status = "ready"
                                        st.rerun()
                                    elif integration_result is True:
                                        st.success("✅ Letöltés és integrálás befejezve.")
                                        st.session_state.integration_status = "done"
                                    else:
                                        st.session_state.integration_status = "error"
                                        st.session_state.integration_error = "Nem jött vissza érvényes integrációs eredmény."
                                        st.error("❌ Integráció nem adott vissza eredményt.")
                                        
                                except Exception as e:
                                    st.session_state.integration_status = "error"
                                    st.session_state.integration_error = str(e)
                                    st.markdown(f'<div style="font-size: 12px;">❌ Hiba: {e}</div>', unsafe_allow_html=True)

    # Mentés előtti szerkesztés (önálló blokk)
    if "pending_integration" in st.session_state:
        pending = st.session_state.pending_integration
        question = pending.get("question", {})
        category = pending.get("category")
        result_title = pending.get("result_title", "Ismeretlen")
        audio_file = question.get("audio_file", "N/A")
        
        st.markdown("---")
        st.markdown("### ✏️ Mentés előtti szerkesztés")
        st.info(f"Letöltött track: {result_title} | Kategória: {category} | Fájl: {audio_file}")
        
        question_text = st.text_input("Kérdés szövege:", value=question.get("question", ""))
        explanation = st.text_input("Magyarázat:", value=question.get("explanation", ""))
        fallback_artist = ""
        if question.get("options"):
            fallback_artist = question["options"][0]
        else:
            fallback_artist = pending.get("track_info", {}).get("channel", "")
        fallback_title = question.get("song_title") or pending.get("track_info", {}).get("title", "") or result_title
        approved_artist = st.text_input("Előadó / Szerző:", value=fallback_artist)
        approved_title = st.text_input("Szám címe:", value=fallback_title)
        
        options = question.get("options", []) + [""] * (4 - len(question.get("options", [])))
        option_1 = st.text_input("Opció 1 (helyes):", value=approved_artist or (options[0] if len(options) > 0 else ""))
        option_2 = st.text_input("Opció 2:", value=options[1] if len(options) > 1 else "")
        option_3 = st.text_input("Opció 3:", value=options[2] if len(options) > 2 else "")
        option_4 = st.text_input("Opció 4:", value=options[3] if len(options) > 3 else "")
        
        updated_options = [option_1, option_2, option_3, option_4]
        correct_answer = st.selectbox(
            "Helyes válasz:",
            options=updated_options,
            index=0
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Mentés és integrálás", type="primary", use_container_width=True):
                safe_name = _make_safe_filename(approved_artist, approved_title)
                new_audio_file = safe_name
                audio_source_path = pending.get("audio_file")
                new_path = audio_source_path
                if audio_source_path and os.path.exists(audio_source_path):
                    new_path = os.path.join(os.path.dirname(audio_source_path), safe_name)
                    try:
                        if audio_source_path != new_path:
                            os.replace(audio_source_path, new_path)
                        new_audio_file = os.path.basename(new_path)
                    except Exception as e:
                        st.warning(f"⚠️ Fájlnév átnevezés sikertelen: {e}")
                else:
                    st.warning("⚠️ Nem található letöltött fájl az átnevezéshez, csak a kérdésbe kerül be az új név.")

                new_question = {
                    "question": question_text,
                    "options": updated_options,
                    "correct": updated_options.index(correct_answer),
                    "explanation": explanation or f"{approved_artist} - {approved_title}",
                    "audio_file": new_audio_file,
                    "song_title": approved_title,
                    "topic": category,
                }
                add_question_to_category(new_question, category)

                # Cache frissítése
                cache_keys_to_delete = []
                for key in st.session_state.keys():
                    if (key.startswith("audio_track_data_") or
                        key.startswith("duration_") or
                        key.startswith("track_cache_") or
                        key == "modified_questions"):
                        cache_keys_to_delete.append(key)
                for key in cache_keys_to_delete:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state['force_refresh'] = True

                # Git szinkronizáció (kérdés + audio)
                question_file_by_category = {
                    "magyar_zenekarok": "topics/magyar_zenekarok_uj.py",
                    "nemzetkozi_zenekarok": "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py",
                    "komolyzene": "topics/komolyzene_uj.py",
                    "one_hit_wonders": "topics/one_hit_wonders.py",
                    "sorozat_focimek": "topics/sorozat_focimek.py",
                }
                question_file_path = question_file_by_category.get(category)
                final_audio_path = new_path if new_path and os.path.exists(new_path) else None
                try:
                    if question_file_path:
                        subprocess.run(['git', 'add', question_file_path], check=True)
                    if final_audio_path:
                        subprocess.run(['git', 'add', final_audio_path], check=True)
                    commit_msg = f"Add track: {approved_artist} - {approved_title}"
                    subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
                    subprocess.run(['git', 'push'], check=True)
                    st.success("✅ Kérdés mentve, cache frissítve és GitHub-ra feltöltve.")
                except subprocess.CalledProcessError as e:
                    st.warning(f"⚠️ Git szinkronizáció sikertelen: {e}")
                    st.success("✅ Kérdés mentve és cache frissítve.")

                del st.session_state.pending_integration
                st.rerun()
        with col2:
            if st.button("🗑️ Elvetés", type="secondary", use_container_width=True):
                del st.session_state.pending_integration
                st.info("ℹ️ Integráció elvetve.")
                st.rerun()
                                        
    # Diagnosztika
    if st.session_state.get("integration_status") == "error":
        st.warning(f"⚠️ Integrációs hiba: {st.session_state.get('integration_error', 'Ismeretlen hiba')}")


def search_youtube_tracks(query):
    """YouTube keresés implementáció"""
    try:
        import requests
        import json
        import re
        
        # YouTube keresés közvetlenül a YouTube API nélkül - pontosabb keresés
        # Hozzáadunk specifikus kulcsszavakat a jobb eredményekért
        if "one night in bangkok" in query.lower():
            enhanced_query = f"{query} Murray Head official music video"
        elif "murray head" in query.lower():
            enhanced_query = f"{query} One Night in Bangkok official music video"
        else:
            enhanced_query = f"{query} official music video"
        
        search_url = f"https://www.youtube.com/results?search_query={enhanced_query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            # YouTube oldal tartalmából kinyerjük a videó adatokat
            html_content = response.text
            
            # ytInitialData keresése
            yt_initial_data_match = re.search(r'var ytInitialData = ({.*?});', html_content)
            
            if yt_initial_data_match:
                try:
                    yt_data = json.loads(yt_initial_data_match.group(1))
                    
                    # Videó adatok kinyerése
                    videos = []
                    
                    # Keresési eredmények keresése a JSON-ben
                    def extract_videos(data):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if key == 'videoRenderer':
                                    video_info = value
                                    
                                    # Title kinyerése
                                    title_obj = video_info.get('title', {})
                                    if isinstance(title_obj, dict) and 'runs' in title_obj:
                                        title = title_obj['runs'][0].get('text', '') if title_obj['runs'] else ''
                                    else:
                                        title = str(title_obj)
                                    
                                    # Channel kinyerése
                                    channel_obj = video_info.get('ownerText', {})
                                    if isinstance(channel_obj, dict) and 'runs' in channel_obj:
                                        channel = channel_obj['runs'][0].get('text', '') if channel_obj['runs'] else ''
                                    else:
                                        channel = str(channel_obj)
                                    
                                    video_id = video_info.get('videoId', '')
                                    
                                    # Duration kinyerése
                                    duration_obj = video_info.get('lengthText', {})
                                    if isinstance(duration_obj, dict):
                                        duration = duration_obj.get('simpleText', '')
                                    else:
                                        duration = str(duration_obj)
                                    
                                    # Views kinyerése
                                    views_obj = video_info.get('viewCountText', {})
                                    if isinstance(views_obj, dict):
                                        views = views_obj.get('simpleText', '')
                                    else:
                                        views = str(views_obj)
                                    
                                    # Thumbnail kinyerése
                                    thumbnail_obj = video_info.get('thumbnail', {})
                                    if isinstance(thumbnail_obj, dict) and 'thumbnails' in thumbnail_obj:
                                        thumbnails = thumbnail_obj['thumbnails']
                                        if thumbnails and len(thumbnails) > 0:
                                            thumbnail = thumbnails[-1].get('url', '')
                                        else:
                                            thumbnail = f"https://i.ytimg.com/vi/{video_id}/default.jpg"
                                    else:
                                        thumbnail = f"https://i.ytimg.com/vi/{video_id}/default.jpg"
                                    
                                    if video_id and title:
                                        videos.append({
                                            'title': title,
                                            'channel': channel,
                                            'duration': duration,
                                            'views': views,
                                            'url': f"https://www.youtube.com/watch?v={video_id}",
                                            'thumbnail': thumbnail
                                        })
                                elif isinstance(value, (dict, list)):
                                    extract_videos(value)
                        elif isinstance(data, list):
                            for item in data:
                                extract_videos(item)
                    
                    extract_videos(yt_data)
                    
                    # Sponsored találatok kiszűrése és jobb eredmények kiválasztása
                    processed_results = []
                    for video in videos[:10]:  # Több találat ellenőrzése
                        title = video.get('title', '').lower()
                        channel = video.get('channel', '').lower()
                        
                        # Sponsored és reklám találatok kiszűrése
                        if 'sponsored' in title or 'reklám' in title:
                            continue
                        
                        # Jobb eredmények prioritása
                        score = 0
                        
                        # Official/VEVO csatornák prioritása
                        if 'official' in title or 'vevo' in channel:
                            score += 10
                        
                        # Music kulcsszó prioritása
                        if 'music' in title or 'music' in channel:
                            score += 5
                        
                        # Rövidebb címek prioritása (kevesebb "fehér zaj")
                        if len(title) < 100:
                            score += 3
                        
                        # Specifikus dalok prioritása
                        if "one night in bangkok" in query.lower():
                            if "murray head" in title.lower() and "one night in bangkok" in title.lower():
                                score += 20
                            elif "murray head" in channel.lower():
                                score += 15
                            elif "one night in bangkok" in title.lower():
                                score += 10
                        
                        # Rossz találatok kiszűrése
                        if "stacy's mom" in title.lower() or "fountains of wayne" in title.lower():
                            score -= 50
                        
                        # Hozzáadjuk a pontszámot
                        video['score'] = score
                        processed_results.append(video)
                    
                    # Rendezés pontszám szerint (csökkenő)
                    processed_results.sort(key=lambda x: x.get('score', 0), reverse=True)
                    
                    return processed_results[:5]  # Top 5 eredmény
                    
                except json.JSONDecodeError:
                    st.error("Hiba a YouTube adatok feldolgozásakor")
                    return []
            else:
                st.error("Nem sikerült megtalálni a YouTube adatokat")
                return []
        else:
            st.error(f"YouTube oldal betöltési hiba: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"YouTube keresési hiba: {e}")
        return []

def download_and_integrate_track(track_info, category, custom_options=None, require_review=False, clip_seconds=120, return_metadata=False, cookies_path=None):
    """Track letöltése és integrálása"""
    try:
        import yt_dlp
    except ImportError:
        st.error("❌ yt-dlp modul nincs telepítve! Telepítsd: pip install yt-dlp")
        return False
    
    import os
    from pathlib import Path
    
    # Ellenőrizzük, hogy track_info dict-e
    if not isinstance(track_info, dict):
        st.error(f"Track info nem dict típusú: {type(track_info)}")
        return False
    
    # Kategória alapján letöltési könyvtár meghatározása
    category_mapping = {
        "magyar_zenekarok": "audio_files/magyar_zenekarok",
        "nemzetkozi_zenekarok": "audio_files/nemzetkozi_zenekarok", 
        "komolyzene": "audio_files/komolyzene",
        "one_hit_wonders": "audio_files/one_hit_wonders",
        "sorozat_focimek": "audio_files/sorozat_focimek",
    }
    
    download_dir = Path(category_mapping.get(category, "audio_files"))
    download_dir.mkdir(parents=True, exist_ok=True)
    
    def _yt_dlp_hint(error_message: str) -> None:
        if "Failed to extract any player response" in error_message:
            version = getattr(yt_dlp, "__version__", "ismeretlen")
            st.error(
                "❌ YouTube player response hiba (yt-dlp). "
                f"Frissítsd a yt-dlp-t: pip install -U yt-dlp (aktuális: {version})"
            )
        if "HTTP Error 403" in error_message or "403" in error_message:
            st.error("❌ YouTube 403 tiltás. Próbáld meg cookie fájllal (bejelentkezett böngészőből exportálva).")

    def _looks_like_url(value) -> bool:
        if not isinstance(value, str):
            return False
        lowered = value.lower()
        return lowered.startswith("http") or "youtu" in lowered
    
    # yt-dlp konfiguráció - 403 Forbidden hiba javítása - teljesen új megközelítés
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': str(download_dir / '%(id)s.%(ext)s'),  # YouTube ID használata fájlnévként
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
        # 403 Forbidden hiba javítása - teljesen új megközelítés
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
        },
        'extractor_retries': 10,
        'fragment_retries': 10,
        'retries': 10,
        # Cookie és referer beállítások
        'cookiefile': None,
        'referer': 'https://www.youtube.com/',
        # Proxy és timeout beállítások
        'socket_timeout': 120,
        'retry_sleep_functions': {'http': lambda n: min(1.5 ** n, 60)},
        # Egyszerűsített extractor beállítások
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_skip': ['configs', 'webpage'],
                'player_client': ['android', 'web', 'ios', 'tv_embedded'],
            }
        },
        # További beállítások
        'no_check_certificate': True,
        'prefer_insecure': True,
        'geo_bypass': True,
        'geo_bypass_country': 'US',
        # Rate limiting
        'sleep_interval': 1,
        'max_sleep_interval': 5,
        # Alternative extractors
        'extractor_retries': 10,
        'fragment_retries': 10,
        'retries': 10,
        # IPv4 kényszerítés macOS-en
        'force_ipv4': True,
        'source_address': '0.0.0.0',
        # Egyszerű beállítások
        'no_color': True,
    }
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path
    
    # Letöltés - több próbálkozás különböző konfigurációkkal
    url = track_info.get('url', '')
    if not url:
        st.error("Nincs érvényes URL a track_info-ban")
        return False
    
    success = False
    info = {}
    
    # Próbálkozás 1: Egyszerű konfiguráció
    try:
        simple_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_skip': ['configs', 'webpage'],
                    'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                }
            },
        }
        if cookies_path:
            simple_opts['cookiefile'] = cookies_path
        with yt_dlp.YoutubeDL(simple_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                ydl.download([url])
                success = True
            else:
                success = False
    except Exception as e:
        st.error(f"Egyszerű konfiguráció is sikertelen: {str(e)}")
        _yt_dlp_hint(str(e))
        success = False
    
    # Próbálkozás 2: Részletes konfiguráció (ha az első sikertelen)
    if not success:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.warning(f"Letöltés sikertelen: {str(e)}")
            _yt_dlp_hint(str(e))
            success = False
    
    # Próbálkozás 4: VPN/Proxy beállításokkal (ha mindhárom sikertelen)
    if not success:
        try:
            vpn_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # VPN/Proxy beállítások
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                },
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'geo_bypass_ip_block': '0.0.0.0/0',
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls'],
                        'player_skip': ['configs', 'webpage'],
                        'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                    }
                },
                'socket_timeout': 30,
                'retries': 5,
                'fragment_retries': 5,
            }
            if cookies_path:
                vpn_opts['cookiefile'] = cookies_path
            with yt_dlp.YoutubeDL(vpn_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.error(f"VPN/Proxy konfiguráció is sikertelen: {str(e)}")
            _yt_dlp_hint(str(e))
            success = False
    
    # Próbálkozás 5: Teljesen más megközelítés - yt-dlp alternatív beállítások
    if not success:
        try:
            alt_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # Alternatív beállítások
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls', 'translated_subs'],
                        'player_skip': ['configs', 'webpage'],
                        'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                    }
                },
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'socket_timeout': 60,
                'retries': 3,
                'fragment_retries': 3,
                'no_check_certificate': True,
                'prefer_insecure': True,
            }
            if cookies_path:
                alt_opts['cookiefile'] = cookies_path
            with yt_dlp.YoutubeDL(alt_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.error(f"Alternatív konfiguráció is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 6: Teljesen más URL formátum - ytsearch használata
    if not success:
        try:
            # YouTube URL helyett ytsearch használata
            search_query = track_info.get('title', '') + ' ' + track_info.get('artist', '')
            if search_query.strip():
                search_url = f"ytsearch1:{search_query}"
                st.info(f"🔍 Keresés: {search_query}")
                
                search_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {
                        'youtube': {
                            'skip': ['dash', 'hls'],
                        }
                    },
                    'geo_bypass': True,
                    'geo_bypass_country': 'US',
                    'socket_timeout': 30,
                    'retries': 3,
                }
                if cookies_path:
                    search_opts['cookiefile'] = cookies_path
                with yt_dlp.YoutubeDL(search_opts) as ydl:
                    info = ydl.extract_info(search_url, download=False)
                    if info and 'entries' in info and info['entries']:
                        # Az első találatot használjuk
                        first_result = info['entries'][0]
                        ydl.download([first_result['webpage_url']])
                        success = True
                        info = first_result  # Az info változót frissítjük
                    else:
                        success = False
            else:
                success = False
        except Exception as e:
            st.error(f"Keresés alapú letöltés is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 7: Teljesen más megközelítés - YouTube API közvetlen használata
    if not success:
        try:
            st.info("🔄 Próbálkozás YouTube API közvetlen használatával...")
            
            # YouTube API kulcs nélküli keresés
            import urllib.parse
            import urllib.request
            import json
            
            search_query = track_info.get('title', '') + ' ' + track_info.get('artist', '')
            if search_query.strip():
                # YouTube keresési URL
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
                st.info(f"🔍 YouTube keresés: {search_url}")
                
                # Próbáljuk meg a YouTube oldal tartalmát lekérni
                req = urllib.request.Request(
                    search_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    html_content = response.read().decode('utf-8')
                    
                    # YouTube videó ID keresése a HTML-ben
                    import re
                    video_ids = re.findall(r'"videoId":"([^"]+)"', html_content)
                    
                    if video_ids:
                        video_id = video_ids[0]  # Az első találatot használjuk
                        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                        st.info(f"📺 Talált videó: {youtube_url}")
                        
                        # Most próbáljuk meg letölteni ezt a videót
                        direct_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True,
                            'quiet': True,
                            'no_warnings': True,
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            },
                            'extractor_args': {
                                'youtube': {
                                    'skip': ['dash', 'hls'],
                                }
                            },
                            'geo_bypass': True,
                            'geo_bypass_country': 'US',
                            'socket_timeout': 30,
                            'retries': 3,
                        }
                        if cookies_path:
                            direct_opts['cookiefile'] = cookies_path
                        
                        with yt_dlp.YoutubeDL(direct_opts) as ydl:
                            info = ydl.extract_info(youtube_url, download=False)
                            if info:
                                ydl.download([youtube_url])
                                success = True
                            else:
                                success = False
                    else:
                        st.warning("⚠️ Nem találtam videó ID-t a keresési eredményekben")
                        success = False
            else:
                success = False
                
        except Exception as e:
            st.error(f"YouTube API közvetlen használat is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 8: Intelligens proxy rendszer
    if not success:
        try:
            st.info("🔄 Próbálkozás intelligens proxy rendszerrel...")
            
            # 1. Webes proxy szolgáltatások (CroxyProxy, ProxySite)
            web_proxies = [
                'https://www.croxyproxy.com/',
                'https://www.proxysite.com/',
                'https://www.kproxy.com/',
            ]
            
            # 2. Friss HTTP proxy lista
            import requests
            import random
            
            try:
                st.info("🔍 Friss proxy lista letöltése...")
                proxy_response = requests.get(
                    'https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
                    timeout=10
                )
                
                if proxy_response.status_code == 200:
                    proxy_list = proxy_response.text.strip().split('\n')
                    # Véletlenszerűen választunk 3 proxy-t
                    selected_proxies = random.sample(proxy_list, min(3, len(proxy_list)))
                    st.info(f"✅ Találtam {len(selected_proxies)} friss proxy-t")
                else:
                    selected_proxies = []
                    st.warning("⚠️ Nem sikerült letölteni a proxy listát")
                    
            except Exception as e:
                st.warning(f"⚠️ Proxy lista letöltés hiba: {str(e)}")
                selected_proxies = []
            
            # 3. Proxy-k tesztelése és használata
            all_proxies = []
            
            # Webes proxy-k hozzáadása
            for web_proxy in web_proxies:
                all_proxies.append(('web', web_proxy))
            
            # HTTP proxy-k hozzáadása
            for proxy in selected_proxies:
                all_proxies.append(('http', f"http://{proxy}"))
            
            # Proxy-k tesztelése
            for proxy_type, proxy_url in all_proxies:
                try:
                    if proxy_type == 'web':
                        st.info(f"🌐 Webes proxy tesztelése: {proxy_url}")
                        # Webes proxy-knál más a tesztelés
                        test_success = True
                    else:
                        st.info(f"🌐 HTTP proxy tesztelése: {proxy_url}")
                        # HTTP proxy gyors teszt
                        test_response = requests.get(
                            'http://httpbin.org/ip',
                            proxies={'http': proxy_url, 'https': proxy_url},
                            timeout=5
                        )
                        test_success = test_response.status_code == 200
                    
                    if test_success:
                        st.info(f"✅ Proxy működik: {proxy_url}")
                        
                        # YouTube letöltés proxy-val
                        proxy_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True,
                            'quiet': True,
                            'no_warnings': True,
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            },
                            'extractor_args': {
                                'youtube': {
                                    'skip': ['dash', 'hls'],
                                }
                            },
                            'geo_bypass': True,
                            'geo_bypass_country': 'US',
                            'socket_timeout': 30,
                            'retries': 2,
                        }
                        if cookies_path:
                            proxy_opts['cookiefile'] = cookies_path
                        
                        # Proxy hozzáadása ha HTTP proxy
                        if proxy_type == 'http':
                            proxy_opts['proxy'] = proxy_url
                        
                        with yt_dlp.YoutubeDL(proxy_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if info:
                                ydl.download([url])
                                success = True
                                st.success(f"🎉 Sikeres letöltés {proxy_type} proxy-val: {proxy_url}")
                                break
                            else:
                                st.warning(f"⚠️ {proxy_type} proxy nem működik YouTube-nál: {proxy_url}")
                    else:
                        st.warning(f"⚠️ {proxy_type} proxy nem elérhető: {proxy_url}")
                        
                except Exception as e:
                    st.warning(f"⚠️ {proxy_type} proxy hiba ({proxy_url}): {str(e)}")
                    continue
                    
        except Exception as e:
            st.error(f"Intelligens proxy rendszer sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 9: Egyszerű megközelítés (minimális beállításokkal)
    if not success:
        try:
            st.info("🔄 Próbálkozás egyszerű megközelítéssel...")
            
            # Minimális yt-dlp konfiguráció
            simple_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
            if cookies_path:
                simple_opts['cookiefile'] = cookies_path
            
            with yt_dlp.YoutubeDL(simple_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                    st.success("✅ Sikeres letöltés egyszerű megközelítéssel")
                else:
                    success = False
                    
        except Exception as e:
            st.error(f"Egyszerű megközelítés is sikertelen: {str(e)}")
            success = False
    
    if not success:
        st.error("❌ Minden letöltési módszer sikertelen volt")
        st.error("🔍 YouTube valószínűleg blokkolja a letöltéseket ezen a szerveren")
        st.info("💡 Alternatív megoldások:")
        st.info("1. Használj VPN-t a szerveren")
        st.info("2. Próbáld meg másik időpontban")
        st.info("3. Használj másik letöltő szolgáltatást")
        st.info("4. Manuálisan töltsd le és töltsd fel a fájlokat")
        return False
    
    # Ha keresési találatlistát kaptunk, az első elem legyen az info
    if isinstance(info, dict) and info.get('entries'):
        first_entry = next((e for e in info.get('entries', []) if e), None)
        if first_entry:
            info = first_entry
            if first_entry.get('webpage_url'):
                url = first_entry['webpage_url']

    # Track info normalizálás (YouTube cím alapján)
    info_title = info.get('title') if isinstance(info, dict) else None
    info_channel = None
    if isinstance(info, dict):
        info_channel = info.get('uploader') or info.get('channel')
    if info_title:
        if "raw_title" not in track_info:
            track_info["raw_title"] = info_title
        current_title = track_info.get("title")
        if not current_title or _looks_like_url(current_title):
            track_info["title"] = info_title
            current_song_title = track_info.get("song_title")
            if not current_song_title or _looks_like_url(current_song_title):
                track_info["song_title"] = info_title
    if info_channel and not track_info.get("channel"):
        track_info["channel"] = info_channel
    if info_title and not track_info.get("artist"):
        parsed_artist, parsed_title = _parse_artist_title_from_youtube(info_title, info_channel)
        track_info["artist"] = parsed_artist
        if not track_info.get("song_title"):
            track_info["song_title"] = parsed_title
        if not track_info.get("title") or _looks_like_url(track_info.get("title")):
            track_info["title"] = parsed_title

    # Fájlnév meghatározása - YouTube ID alapján
    video_id = info.get('id', '')
    if not video_id:
        st.error("❌ Nem sikerült lekérni a videó ID-t")
        return False
    
    # Fájlnév YouTube ID alapján - először MP3-et próbáljuk
    audio_file = str(download_dir / f"{video_id}.mp3")
    
    # Ellenőrizzük, hogy a fájl létezik-e
    if not os.path.exists(audio_file):
        # Próbáljuk meg megtalálni a fájlt a könyvtárban
        import glob
        possible_files = glob.glob(str(download_dir / f"{video_id}.*"))
        if possible_files:
            audio_file = possible_files[0]  # A YouTube ID-vel kezdődő fájlt használjuk
            st.info(f"📁 Talált fájl: {os.path.basename(audio_file)}")
            
            # Ha nem MP3, konvertáljuk MP3-ba
            if not audio_file.endswith('.mp3'):
                try:
                    mp3_file = str(download_dir / f"{video_id}.mp3")
                    cmd = [
                        'ffmpeg', '-i', audio_file, 
                        '-acodec', 'libmp3lame', 
                        '-ab', '192k', 
                        '-ar', '44100', 
                        '-y', 
                        mp3_file
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0 and os.path.exists(mp3_file):
                        # Eredeti fájl törlése
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                        audio_file = mp3_file
                        st.success("✅ Fájl sikeresen konvertálva MP3-ba!")
                    else:
                        st.warning("⚠️ MP3 konvertálás sikertelen, eredeti fájl használata")
                except Exception as e:
                    st.warning(f"⚠️ MP3 konvertálás hiba: {str(e)}, eredeti fájl használata")
        else:
            st.error("❌ A letöltés sikertelen - fájl nem található")
            return False
    
    # Ellenőrizzük a fájl méretét
    if os.path.getsize(audio_file) == 0:
        st.error("❌ A letöltött fájl üres")
        return False
    
    st.success(f"✅ Sikeres letöltés: {track_info.get('title', 'Ismeretlen track')}")
    
    # 3 perces (vagy beállított) rész kivágása FFmpeg-gel
    try:
        import re
        
        # Ellenőrizzük, hogy a fájl létezik-e és nem üres
        if not os.path.exists(audio_file):
            st.error("❌ A letöltött fájl nem található!")
            return False
        
        if os.path.getsize(audio_file) == 0:
            st.error("❌ A letöltött fájl üres!")
            return False
        
        # Fájl létezik és nem üres, folytathatjuk a vágást
        # Biztonságos fájlnév létrehozása - "Előadó - Szám cím" formátum
        artist = track_info.get('artist', 'Unknown Artist')
        title = track_info.get('title', 'Unknown Title')
        
        # Biztonságos fájlnév létrehozása - rövidebb és egyszerűbb
        safe_artist = re.sub(r'[^\w\s-]', '', artist)[:20]  # Max 20 karakter
        safe_title = re.sub(r'[^\w\s-]', '', title)[:30]   # Max 30 karakter
        safe_artist = re.sub(r'[-\s]+', '_', safe_artist)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        
        # "Előadó_Szám" formátum (rövidebb)
        output_filename = f"{safe_artist}_{safe_title}.mp3"
        output_file = str(download_dir / output_filename)
        
        # FFmpeg paranccsal 2 perc kivágása - továbbfejlesztett verzió
        # Először ellenőrizzük a bemeneti fájl hosszát
        probe_cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
            '-of', 'csv=p=0', audio_file
        ]
        
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        
        if probe_result.returncode == 0 and probe_result.stdout.strip():
            try:
                duration = float(probe_result.stdout.strip())
                if duration < clip_seconds:
                    # Ha a fájl rövidebb mint a kívánt vágás, nem vágunk
                    st.info(f"⚠️ A fájl rövidebb mint {clip_seconds} mp ({duration:.1f}s), teljes fájl használata")
                else:
                    # FFmpeg paranccsal kivágás
                    cmd = [
                        'ffmpeg', '-i', audio_file, 
                        '-t', str(clip_seconds),  # vágás hossza másodpercben
                        '-acodec', 'libmp3lame',  # MP3 kódolás
                        '-ab', '192k',  # 192 kbps bitrate
                        '-ar', '44100',  # 44.1 kHz sample rate
                        '-y',  # Felülírás
                        output_file
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0 and os.path.exists(output_file):
                        # Ellenőrizzük a kimeneti fájl méretét
                        if os.path.getsize(output_file) > 0:
                            # Eredeti fájl törlése, csak a 2 perces marad
                            if os.path.exists(audio_file):
                                os.remove(audio_file)
                            audio_file = output_file
                            st.success(f"✅ {clip_seconds} mp rész sikeresen kivágva!")
                        else:
                            st.warning("⚠️ A kivágott fájl üres, teljes fájl használata")
                    else:
                        st.warning(f"⚠️ FFmpeg hiba: {result.stderr[:200]}..., teljes fájl használata")
            except ValueError:
                st.warning("⚠️ Nem sikerült meghatározni a fájl hosszát, teljes fájl használata")
        else:
            st.warning("⚠️ Nem sikerült elemezni a fájlt, teljes fájl használata")
            
    except subprocess.TimeoutExpired:
        st.warning("⚠️ FFmpeg időtúllépés, teljes fájl használata")
    except FileNotFoundError:
        st.warning("⚠️ FFmpeg nem található, teljes fájl használata")
    except Exception as e:
        st.warning(f"⚠️ FFmpeg hiba: {str(e)[:100]}..., teljes fájl használata")
    
    # Track info normalizálás (YouTube cím alapján) - már fent megtörtént

    # Quiz kérdés generálása
    question = generate_quiz_question(track_info, audio_file, category, custom_options)
    
    if require_review:
        return {
            "success": True,
            "question": question,
            "category": category,
            "audio_file": audio_file,
            "track_info": track_info,
        }
    
    # Kérdés hozzáadása a megfelelő kategóriához
    add_question_to_category(question, category)

    if return_metadata:
        return {
            "success": True,
            "question": question,
            "category": category,
            "audio_file": audio_file,
            "track_info": track_info,
        }
    return True

def generate_quiz_question(track_info, audio_file, category, custom_options=None):
    """Quiz kérdés generálása a track alapján"""
    try:
        # Track_info ellenőrzés
        if not isinstance(track_info, dict):
            track_info = {}
        
        # Biztonságos adatkinyerés
        title = track_info.get('song_title') or track_info.get('title', 'Ismeretlen cím')
        artist = track_info.get('artist') or track_info.get('channel', 'Ismeretlen előadó')
        
        # Kategória alapú kérdés
        if category == "komolyzene":
            question_text = "Ki a zeneszerző?"
        elif category == "sorozat_focimek":
            question_text = "Melyik sorozat főcímdala ez?"
        else:
            question_text = "Ki az előadó?"
        
        # Opciók használata
        if custom_options and len(custom_options) >= 4:
            # Egyedi opciók használata
            options = custom_options
            correct_answer = options[0]  # Első opció a helyes válasz
        else:
            # Alapértelmezett opciók
            if category == "sorozat_focimek":
                series_name = artist if artist and artist != "Ismeretlen előadó" else title
                correct_answer = series_name
            else:
                correct_answer = artist
            if category == "komolyzene":
                similar_options = ["Beethoven", "Mozart", "Bach"]
            elif category == "sorozat_focimek":
                similar_options = ["Game of Thrones", "Stranger Things", "Friends"]
            elif category == "magyar_zenekarok":
                similar_options = ["Kispál és a Borz", "Elefánt", "Quimby"]
            elif category == "nemzetkozi_zenekarok":
                similar_options = ["Imagine Dragons", "Bastille", "The Weeknd"]
            elif category == "one_hit_wonders":
                similar_options = ["Bastille", "Imagine Dragons", "The Chainsmokers"]
            else:
                similar_options = ["Előadó 1", "Előadó 2", "Előadó 3"]
            
            options = [
                correct_answer,
                similar_options[0],
                similar_options[1],
                "Szerkeszthető opció"
            ]
        
        # Kérdés objektum
        # Csak a fájlnevet tároljuk, nem a teljes elérési utat
        audio_filename = os.path.basename(audio_file) if audio_file else None
        explanation_text = f"{artist} - {title}" if artist or title else f"{correct_answer} - {category.replace('_', ' ').title()}"
        question = {
            'question': question_text,
            'options': options,
            'correct': 0,
            'explanation': explanation_text,
            'audio_file': audio_filename,
            'topic': category
        }
        if title:
            question['song_title'] = title
        return question
    except Exception as e:
        # Fallback kérdés
        audio_filename = os.path.basename(audio_file) if audio_file else None
        return {
            'question': 'Ki az előadó?',
            'options': ['Ismeretlen előadó', 'Előadó 1', 'Előadó 2', 'Szerkeszthető opció'],
            'correct': 0,
            'explanation': 'Ismeretlen dal',
            'audio_file': audio_filename,
            'topic': category
        }

def add_question_to_category(question, category):
    """Kérdés hozzáadása a megfelelő kategóriához"""
    try:
        # Importálás a megfelelő kategóriából
        if category == "magyar_zenekarok":
            from topics.magyar_zenekarok_uj import QUESTIONS as MAGYAR_ZENEKAROK_QUESTIONS_UJ
            MAGYAR_ZENEKAROK_QUESTIONS_UJ.append(question)
            # Fájlba mentés
            save_questions_to_file(MAGYAR_ZENEKAROK_QUESTIONS_UJ, "topics/magyar_zenekarok_uj.py", "QUESTIONS")
        elif category == "nemzetkozi_zenekarok":
            from topics.nemzetkozi_zenekarok_final_fixed_with_real_audio import QUESTIONS as NEMZETKOZI_ZENEKAROK_QUESTIONS
            NEMZETKOZI_ZENEKAROK_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(NEMZETKOZI_ZENEKAROK_QUESTIONS, "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py", "NEMZETKOZI_ZENEKAROK_QUESTIONS")
        elif category == "komolyzene":
            from topics.komolyzene_uj import QUESTIONS as KOMOLYZENE_QUESTIONS
            KOMOLYZENE_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(KOMOLYZENE_QUESTIONS, "topics/komolyzene_uj.py", "QUESTIONS")
        elif category == "one_hit_wonders":
            from topics.one_hit_wonders import QUESTIONS as ONE_HIT_WONDERS_QUESTIONS
            ONE_HIT_WONDERS_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(ONE_HIT_WONDERS_QUESTIONS, "topics/one_hit_wonders.py", "ONE_HIT_WONDERS_QUESTIONS")
        elif category == "sorozat_focimek":
            from topics.sorozat_focimek import QUESTIONS as SOROZAT_FOCIMEK_QUESTIONS
            SOROZAT_FOCIMEK_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(SOROZAT_FOCIMEK_QUESTIONS, "topics/sorozat_focimek.py", "QUESTIONS")
        
        # Sikeres hozzáadás
        pass
    except Exception as e:
        st.error(f"Hiba a kérdés hozzáadásakor: {e}")

def save_questions_to_file(questions_list, file_path, variable_name):
    """Kérdések mentése fájlba"""
    try:
        import os
        
        # Fájl tartalom generálása
        content = f"""# Auto-generated questions file
# Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{variable_name} = [
"""
        
        # Kérdések hozzáadása
        for i, question in enumerate(questions_list):
            content += "    {\n"
            question_text = str(question.get("question", "")).replace('"', '\\"')
            content += f'        "question": "{question_text}",\n'
            content += '        "options": [\n'
            for option in question["options"]:
                content += f'            "{option}",\n'
            content += '        ],\n'
            content += f'        "correct": {question["correct"]},\n'
            if "explanation" in question:
                explanation_text = str(question["explanation"]).replace('"', '\\"')
                content += f'        "explanation": "{explanation_text}",\n'
            if "audio_file" in question:
                audio_file_text = str(question["audio_file"]).replace('"', '\\"')
                content += f'        "audio_file": "{audio_file_text}",\n'
            if "song_title" in question:
                song_title_text = str(question["song_title"]).replace('"', '\\"')
                content += f'        "song_title": "{song_title_text}",\n'
            if "topic" in question:
                content += f'        "topic": "{question["topic"]}",\n'
            content += "    },\n"
        
        content += "]\n"
        normalized_path = str(file_path).replace("\\", "/")
        if normalized_path.endswith("topics/komolyzene_uj.py"):
            content += "\n# Export alias for compatibility\n"
            content += "KOMOLYZENE_QUESTIONS = QUESTIONS\n"
        if normalized_path.endswith("topics/sorozat_focimek.py"):
            content += "\n# Export alias for compatibility\n"
            content += "SOROZAT_FOCIMEK_QUESTIONS = QUESTIONS\n"
        
        # Fájlba írás
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        st.error(f"Hiba a fájl mentésekor: {e}")
        return False

if __name__ == "__main__":
    main() 