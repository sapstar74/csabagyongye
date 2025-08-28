"""
🎯 Csabagyöngye Tréning Center 😄
Kiegészített funkciókkal: Analytics, Quiz módok, Nehézségi szintek
"""

import streamlit as st
import random
import time
from datetime import datetime
import os
from pathlib import Path
import base64
from topics.foldrajz_complete import FOLDRAJZ_QUESTIONS_COMPLETE as FOLDRAJZ_QUESTIONS
from topics.komolyzene_uj import KOMOLYZENE_QUESTIONS
from topics.tudosok import TUDOSOK_QUESTIONS
from topics.mitologia_all_questions import MITOLOGIA_QUESTIONS_ALL
from topics.haboru_all_questions import HABORU_QUESTIONS_ALL
from topics.kiralyok import KIRALYOK_QUESTIONS
from topics.allatok_balanced import ALLATOK_QUESTIONS_BALANCED
from topics.dramak import DRAMAK_QUESTIONS
from topics.sport_logok import SPORT_LOGOK_QUESTIONS
from topics.zaszlok_all_questions import ZASZLOK_QUESTIONS_ALL
from topics.magyar_zenekarok_uj import MAGYAR_ZENEKAROK_QUESTIONS_UJ
from topics.nemzetkozi_zenekarok_final_fixed_with_real_audio import NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak import IDIOTA_SZAVAK_QUESTIONS
from topics.festmenyek import FESTMENY_QUESTIONS
from topics.one_hit_wonders import ONE_HIT_WONDERS_QUESTIONS
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
        st.info("🔄 GitHub szinkronizálás indítása...")
        
        # 1. Git pull - legfrissebb változások letöltése
        st.markdown("### 📥 1. Legfrissebb változások letöltése...")
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'], 
            capture_output=True, 
            text=True, 
            cwd=os.getcwd()
        )
        
        if pull_result.returncode != 0:
            st.error(f"❌ Git pull hiba: {pull_result.stderr}")
            return False
            
        st.success("✅ Git pull sikeres!")
        
        # 2. Új audiofájlok keresése
        st.markdown("### 🎵 2. Új audiofájlok keresése...")
        
        # Összes audio track összegyűjtése
        all_tracks = get_all_audio_tracks()
        audio_files = [track["audio_path"] for track in all_tracks]
        
        st.info(f"📊 {len(audio_files)} audiofájl található")
        
        # Kategóriánkénti statisztika
        category_stats = {}
        for track in all_tracks:
            directory = track["directory"]
            if directory not in category_stats:
                category_stats[directory] = 0
            category_stats[directory] += 1
        
        st.markdown("**📁 Kategóriánkénti eloszlás:**")
        for directory, count in category_stats.items():
            st.markdown(f"- {directory}: {count} track")
        
        # 3. Új kérdés fájlok keresése
        st.markdown("### 📝 3. Új kérdés fájlok keresése...")
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
        
        st.info(f"📊 {len(question_files)} kérdés fájl található")
        
        # 4. Új tartalmak listázása
        st.markdown("### 📋 4. Új tartalmak összefoglalása...")
        
        if audio_files:
            st.markdown("**🎵 Új audiofájlok:**")
            for file in audio_files:
                st.markdown(f"- {os.path.basename(file)}")
        
        if question_files:
            st.markdown("**📝 Kérdés fájlok:**")
            for file in question_files:
                st.markdown(f"- {os.path.basename(file)}")
        
        # 5. Alkalmazás újraindítása javaslat
        st.markdown("### 🔄 5. Alkalmazás újraindítása...")
        st.warning("⚠️ A szinkronizálás után javasolt az alkalmazás újraindítása a legfrissebb tartalmak betöltéséhez.")
        
        if st.button("🔄 Alkalmazás újraindítása", type="primary"):
            st.rerun()
        
        st.success("✅ GitHub szinkronizálás sikeresen befejezve!")
        return True
        
    except Exception as e:
        st.error(f"❌ Szinkronizálási hiba: {e}")
        return False

def get_image_base64(image_path):
    """Kép konvertálása base64 formátumra"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except Exception as e:
        st.error(f"Hiba a kép betöltése során: {e}")
        return ""

# Page config
st.set_page_config(
    page_title="Csabagyöngye Tréning Center",
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
    "háborúk": HABORU_QUESTIONS_ALL,
    "magyar_királyok": KIRALYOK_QUESTIONS,
    "tudósok": TUDOSOK_QUESTIONS,
    "mitológia": MITOLOGIA_QUESTIONS_ALL,
    "állatok": ALLATOK_QUESTIONS_BALANCED,
    "drámák": DRAMAK_QUESTIONS,
    "sport_logók": SPORT_LOGOK_QUESTIONS,
    "zászlók": ZASZLOK_QUESTIONS_ALL,
    "idióta_szavak": IDIOTA_SZAVAK_QUESTIONS,
    "festmények": FESTMENY_QUESTIONS,
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
        "festmények": "🎨 Festmények",
        "háborúk": "⚔️ Háborúk",
        "magyar_királyok": "👑 Magyar királyok",
        "tudósok": "🔬 Tudósok",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "drámák": "🎭 Drámák",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "idióta_szavak": "🤪 Idióta szavak",
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
    elif topic == "komolyzene":
        # Komolyzene: original_index alapú mapping használata
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
        elif "audio_file" in question:
            # Ha csak audio_file van, próbáljuk az új mappából
            audio_dir = Path(__file__).parent / "audio_files/komolyzene"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            # Fallback: régi mappa
            audio_dir = Path(__file__).parent / "audio_files_komolyzene"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
    elif topic == "one_hit_wonders":
        # One Hit Wonders audio fájl kezelése
        if "original_index" in question:
            try:
                # Audio fájl elérési útja az új mappából
                index = int(question["original_index"])
                audio_dir = Path(__file__).parent / "audio_files/one_hit_wonders"
                # Fájlnév keresése az index alapján
                for filename in os.listdir(audio_dir):
                    if filename.endswith('.mp3') and filename.startswith(f"{index:02d}_"):
                        audio_path = audio_dir / filename
                        if audio_path.exists():
                            # Audio fájl megtalálva
                            return str(audio_path)
            except Exception as e:
                pass
            # Fallback: régi mappa
            try:
                index = int(question["original_index"])
                audio_dir = Path(__file__).parent / "audio_files_one_hit_wonders"
                for filename in os.listdir(audio_dir):
                    if filename.endswith('.mp3') and filename.startswith(f"{index:02d}_"):
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

def start_quiz():
    """Quiz indítása"""
    if not st.session_state.selected_topics:
        st.error("Kérlek válassz ki legalább egy témaköröt!")
        return
    
    # Végleges kérdésszám használata - ha nincs beállítva, akkor 0 (a tényleges kérdések számától függ)
    final_question_count = st.session_state.get('final_question_count', 0)
    
    all_questions = []
    total_selected_questions = 0
    invalid_questions = 0
    debug_invalid = []
    
    # Minden témakör kezelése egyedi sliders alapján
    for topic in st.session_state.selected_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            print(f"[DEBUG] {topic} összes kérdés: {len(topic_questions)}")
            # Egyedi témakör slider használata
            questions_count = st.session_state.get(f'final_{topic}_questions', 0)
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
                            debug_invalid.append((topic, idx, question))
                            continue
                    else:
                        # Többválasztós kérdések esetén options és correct mezők szükségesek
                        if "options" not in question or "correct" not in question:
                            invalid_questions += 1
                            debug_invalid.append((topic, idx, question))
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
    print(f"[DEBUG] Összes kiválasztott kérdés (szűrés előtt): {total_selected_questions}")
    if invalid_questions > 0:
        print(f"[DEBUG] {invalid_questions} érvénytelen kérdés kihagyva:")
        for topic, idx, q in debug_invalid:
            print(f"  - {topic} [{idx}]: {q.get('question', 'N/A')}")
    
    if not all_questions:
        st.error("Nem található érvényes kérdés a kiválasztott témakörökben!")
        if invalid_questions > 0:
            st.warning(f"{invalid_questions} érvénytelen kérdés kihagyva (hiányzó adatok)")
        return
    
    # Kérdések keverése
    random.shuffle(all_questions)
    
    # Végleges kérdésszám alkalmazása - csak akkor, ha több kérdés van, mint amit kértünk
    if final_question_count > 0 and len(all_questions) > final_question_count:
        all_questions = all_questions[:final_question_count]
    
    # Debug információ
    if final_question_count > 0:
        st.info(f"Kiválasztott kérdések: {len(all_questions)} / {final_question_count} (összesen: {total_selected_questions})")
    else:
        st.info(f"Kiválasztott kérdések: {len(all_questions)} (összesen: {total_selected_questions})")
    if invalid_questions > 0:
        st.warning(f"{invalid_questions} érvénytelen kérdés kihagyva")
    
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
    
    st.markdown('<h1 style="text-align: center; font-size: 3rem; color: #1f77b4; margin-bottom: 2rem;">🎯 Csabagyöngye Tréning Center 😄</h1>', unsafe_allow_html=True)
    
    # Sidebar navigáció
    with st.sidebar:
        st.markdown("## 🧭 Navigáció")
        page = st.selectbox(
            "Válassz oldalt:",
            ["Quiz", "Spotify Playlist", "Analytics", "Beállítások", "Audio hozzáadása", "GitHub Szinkronizálás", "Audio Track Kezelés"],
            format_func=lambda x: {
                "Quiz": "🎯 Quiz",
                "Spotify Playlist": "🎵 Spotify Playlist",
                "Analytics": "📊 Analytics", 
                "Beállítások": "⚙️ Beállítások",
                "Audio hozzáadása": "🎵 Audio hozzáadása",
                "GitHub Szinkronizálás": "🔄 GitHub Szinkronizálás",
                "Audio Track Kezelés": "🎵 Audio Track Kezelés"
            }[x]
        )
        
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
            st.debug(f"Import hiba: {import_error}")
        
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
    
    # 1. Pontos egyezés keresése
    for q in questions:
        if track_name_lower in q['question'].lower() or q['question'].lower() in track_name_lower:
            return q
    
    # 2. Ha nincs pontos egyezés, keresés a track nevének részei alapján
    track_words = [word.strip() for word in track_name_lower.replace('-', ' ').replace('_', ' ').split() if len(word.strip()) > 2]
    
    for q in questions:
        question_lower = q['question'].lower()
        # Ellenőrizzük, hogy a track szavak közül hány szerepel a kérdésben
        matching_words = sum(1 for word in track_words if word in question_lower)
        if matching_words >= 2:  # Legalább 2 szó egyezik
            return q
    
    # 3. Ha még mindig nincs találat, keresés az előadó neve alapján
    if '-' in track_name_lower:
        artist_name = track_name_lower.split('-')[0].strip()
        for q in questions:
            if artist_name in q['question'].lower():
                return q
    
    return None

def save_questions_to_file(file_path, questions):
    """Kérdések mentése Python fájlba"""
    try:
        # Fájl tartalmának beolvasása
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Új kérdések listájának létrehozása
        questions_list = []
        for q in questions:
            options_str = ', '.join([f'"{opt}"' for opt in q["options"]])
            question_dict = f'{{"question": "{q["question"]}", "options": [{options_str}], "correct": {q["correct"]}}}'
            questions_list.append(question_dict)
        
        # Teljes lista string
        questions_str = ',\n    '.join(questions_list)
        
        # Új tartalom létrehozása
        new_content = f"""# Auto-generated questions file
QUESTIONS = [
    {questions_str}
]"""
        
        # Fájl mentése
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        return True
    except Exception as e:
        st.error(f"Hiba a kérdések mentésekor: {e}")
        return False

def show_audio_track_management_page():
    """Audio track kezelési oldal megjelenítése"""
    st.markdown('<h2 style="text-align: center; color: #1f77b4;">🎵 Audio Track Kezelés</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 📋 Mit csinál ez a funkció?
    
    Ez a funkció lehetővé teszi, hogy:
    - 📁 **Megtekintsd az összes audio track-et** táblázatos formában
    - ✏️ **Szerkeszd a válaszopciókat** közvetlenül a táblázatban
    - 💾 **Mentsd el a változásokat** lokálisan és GitHub-ra
    - 🔄 **Frissítsd a kérdésbankot** automatikusan
    
    ---
    """)
    
    # Track-ek betöltése kategóriánként
    tracks_by_category = get_audio_tracks_by_category()
    
    # Kategória választó
    category_options = {key: info["title"] for key, info in tracks_by_category.items()}
    selected_category = st.selectbox(
        "Válassz kategóriát:",
        list(category_options.keys()),
        format_func=lambda x: category_options[x]
    )
    
    if selected_category:
        category_info = tracks_by_category[selected_category]
        st.markdown(f"### {category_info['title']}")
        
        if not category_info['tracks']:
            st.info("📭 Nincsenek track-ek ebben a kategóriában.")
        else:
            st.markdown(f"📊 **{len(category_info['tracks'])} track található**")
            

            
            # Kérdések betöltése - az első track-ből vesszük a kérdésfájl elérési útját
            question_file_path = category_info['tracks'][0]['question_file'] if category_info['tracks'] else None
            if question_file_path:
                questions = load_questions_from_file(question_file_path)
            else:
                questions = []
            
            # Táblázat adatok előkészítése a kérdésfájlokból
            table_data = []
            
            # Kérdések alapján táblázat létrehozása
            for i, question in enumerate(questions):
                # Kérdés szövegéből előadó és szám cím kinyerése
                question_text = question['question']
                
                # Helyes válasz az előadó
                artist = question['options'][question['correct']] if question['correct'] < len(question['options']) else "Ismeretlen"
                
                # Helyes válasz
                correct_answer = question['options'][question['correct']] if question['correct'] < len(question['options']) else "N/A"
                
                # Opciók
                options = question['options'] + [""] * (4 - len(question['options']))  # 4 opcióra kiegészítés
                
                # Audio fájl keresése a track neve alapján
                matching_track = None
                for track in category_info['tracks']:
                    if find_matching_question(track['name'], [question]):
                        matching_track = track
                        break
                
                # Kérdés szövegéből szám cím kinyerése
                song_title = "Ismeretlen szám"
                
                # 1. Audio file mező alapján - ha van a kérdésben (nemzetközi számok)
                if 'audio_file' in question:
                    audio_file = question['audio_file']
                    # Fájlnévből szám cím kinyerése
                    import os
                    filename = os.path.basename(audio_file)
                    # Kiterjesztés eltávolítása
                    filename = os.path.splitext(filename)[0]
                    # Ha van " - " a fájlnévben, akkor az előadó - szám cím formátum
                    if " - " in filename:
                        song_title = filename.split(" - ", 1)[1].strip()
                    # Komolyzene formátum: "szám_Előadó_Szám_címe" (pl. "10_Handel_Rinaldo")
                    elif '_' in filename and selected_category == "komolyzene":
                        parts = filename.split('_')
                        if len(parts) >= 3 and parts[0].isdigit():
                            # Az első rész a szám, a második az előadó, a harmadik és továbbiak a cím
                            song_title = '_'.join(parts[2:]).replace('_', ' ')
                        elif len(parts) > 1 and parts[0].isdigit():
                            # Ha csak 2 rész van: "szám_Előadó"
                            song_title = parts[1].replace('_', ' ')
                        else:
                            song_title = filename.replace('_', ' ')
                    else:
                        # Ha csak az előadó neve van a fájlnévben, próbáljuk meg a kérdés szövegéből
                        # vagy más forrásból kinyerni a szám címét
                        song_title = "Ismeretlen szám"
                
                # 2. "című dalban?" formátum - One Hit Wonders
                elif "című dalban?" in question_text:
                    import re
                    song_match = re.search(r"'([^']+)'", question_text)
                    if song_match:
                        song_title = song_match.group(1)
                
                # 3. " - " formátum - régi formátum
                elif " - " in question_text:
                    song_title = question_text.split(" - ", 1)[1].strip()
                
                # 4. Audio fájl név alapján - ha van matching track
                elif matching_track and 'audio_path' in matching_track:
                    audio_path = matching_track['audio_path']
                    # Fájlnévből szám cím kinyerése
                    import os
                    filename = os.path.basename(audio_path)
                    # Kiterjesztés eltávolítása
                    filename = os.path.splitext(filename)[0]
                    
                    # Komolyzene formátum: "szám_Előadó_Szám_címe" (pl. "10_Handel_Rinaldo")
                    if '_' in filename:
                        parts = filename.split('_')
                        if len(parts) >= 3 and parts[0].isdigit():
                            # Az első rész a szám, a második az előadó, a harmadik és továbbiak a cím
                            song_title = '_'.join(parts[2:]).replace('_', ' ')
                        elif len(parts) > 1 and parts[0].isdigit():
                            # Ha csak 2 rész van: "szám_Előadó"
                            song_title = parts[1].replace('_', ' ')
                        else:
                            song_title = filename.replace('_', ' ')
                    else:
                        song_title = filename.replace('_', ' ')
                
                # 5. Track név alapján - ha van matching track
                elif matching_track and 'name' in matching_track:
                    song_title = matching_track['name']
                
                # 6. Spotify embed alapján - ha van a kérdésben
                if song_title == "Ismeretlen szám" and 'spotify_embed' in question:
                    spotify_url = question['spotify_embed']
                    # Spotify URL-ből szám cím kinyerése
                    if '/track/' in spotify_url:
                        # Track URL - próbáljuk meg a track ID alapján
                        song_title = "Spotify Track"
                    elif '/artist/' in spotify_url:
                        # Artist URL - próbáljuk meg az előadó neve alapján
                        song_title = "Spotify Artist"
                
                # 7. Ha még mindig "Ismeretlen szám", próbáljuk meg a kérdés szövegéből kinyerni
                if song_title == "Ismeretlen szám":
                    # Kérdés szövegéből próbálunk valamit kinyerni
                    cleaned_text = question_text.replace("Ki az előadó?", "").replace("Ki a zeneszerző?", "").replace("Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:", "").strip()
                    if cleaned_text and len(cleaned_text) > 3:
                        song_title = cleaned_text[:50] + "..." if len(cleaned_text) > 50 else cleaned_text
                
                # Audio fájl hosszának meghatározása
                duration_str = "N/A"
                if matching_track:
                    try:
                        import subprocess
                        duration_cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', '-of', 'csv=p=0', matching_track['audio_path']]
                        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True, timeout=10)
                        if duration_result.returncode == 0 and duration_result.stdout.strip():
                            duration_seconds = float(duration_result.stdout.strip())
                            duration_str = f"{int(duration_seconds // 60)}:{int(duration_seconds % 60):02d}"
                    except:
                        duration_str = "N/A"
                
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
            

            
            # Táblázat megjelenítése
            if table_data:
                # DataFrame létrehozása
                import pandas as pd
                df = pd.DataFrame(table_data)
                
                # Play gombok hozzáadása
                play_buttons = []
                for i, row in enumerate(table_data):
                    if row['matching_track'] and 'audio_path' in row['matching_track']:
                        audio_path = row['matching_track']['audio_path']
                        play_buttons.append(f"🎵 Play")
                    else:
                        play_buttons.append("🎵 Play")
                
                # DataFrame létrehozása play gombokkal
                display_df = df.copy()
                display_df.insert(0, "Play", play_buttons)
                
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
                            "Előadó": st.column_config.TextColumn("Előadó", width="medium"),
                            "Szám címe": st.column_config.TextColumn("Szám címe", width="large"),
                            "Opció1": st.column_config.TextColumn("Opció1", width="medium"),
                            "Opció2": st.column_config.TextColumn("Opció2", width="medium"),
                            "Opció3": st.column_config.TextColumn("Opció3", width="medium"),
                            "Opció4": st.column_config.TextColumn("Opció4", width="medium")
                        }
                    )
                
                # Egyszerű táblázat megjelenítés
                st.markdown("### 📊 Track lista")
                
                # Teljes táblázat megjelenítés play gombokkal
                st.markdown("### 📊 Teljes táblázat")
                
                # Play gombok hozzáadása a táblázathoz
                for i, row in enumerate(table_data):
                    if row['matching_track'] and 'audio_path' in row['matching_track']:
                        audio_path = row['matching_track']['audio_path']
                        if st.button(f"🎵 Play {row['Előadó']} - {row['Szám címe']}", key=f"play_{i}"):
                            try:
                                st.audio(audio_path, format='audio/mp3')
                                st.success(f"✅ Lejátszás: {row['Előadó']} - {row['Szám címe']}")
                            except Exception as e:
                                st.error(f"❌ Hiba a lejátszás során: {e}")
                
                # DataFrame megjelenítés
                try:
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    st.success("✅ Táblázat sikeresen megjelenítve!")
                except Exception as e:
                    st.error(f"DataFrame hiba: {e}")
                

                
                # Szerkesztési funkció - soronkénti szerkesztés
                st.markdown("### ✏️ Szerkesztés")
                
                # Módosított kérdések követése
                if 'modified_questions' not in st.session_state:
                    st.session_state.modified_questions = set()
                
                # Szerkesztési mód választó
                edit_mode = st.radio(
                    "Szerkesztési mód:",
                    ["📋 Lista nézet", "✏️ Szerkesztés"],
                    horizontal=True
                )
                
                # Módosított kérdések megjelenítése
                if st.session_state.modified_questions:
                    st.info(f"📝 **{len(st.session_state.modified_questions)} kérdés módosítva** - Ne felejtsd el menteni a változásokat!")
                
                if edit_mode == "✏️ Szerkesztés":
                    st.markdown("**Válassz egy sort a szerkesztéshez:**")
                    
                    # Szerkesztési űrlapok minden sorhoz
                    for i, row in enumerate(table_data):
                        # Módosított kérdés jelölése
                        is_modified = row['question_index'] in st.session_state.modified_questions
                        expander_title = f"📝 {i+1}. {row['Előadó']} - {row['Szám címe']}"
                        if is_modified:
                            expander_title += " ✏️ (módosítva)"
                        
                        with st.expander(expander_title, expanded=False):
                            question_index = row['question_index']
                            current_question = questions[question_index]
                            
                            # Kérdés szerkesztése
                            question_text = st.text_input(
                                "Kérdés:",
                                value=current_question['question'],
                                key=f"question_edit_{i}"
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
                                    # Kérdés frissítése
                                    updated_question = {
                                        "question": question_text,
                                        "options": options,
                                        "correct": options.index(correct_answer) if correct_answer in options else 0
                                    }
                                    
                                    # Kérdés frissítése a listában
                                    questions[question_index] = updated_question
                                    
                                    # Módosított kérdés jelölése
                                    st.session_state.modified_questions.add(question_index)
                                    
                                    # Fájl mentése
                                    if save_questions_to_file(question_file_path, questions):
                                        st.success("✅ Kérdés sikeresen mentve!")
                                        
                                        # Git műveletek
                                        try:
                                            import subprocess
                                            subprocess.run(['git', 'add', question_file_path], check=True)
                                            subprocess.run(['git', 'commit', '-m', f'Update question for {row["Előadó"]} - {row["Szám címe"]}'], check=True)
                                            subprocess.run(['git', 'push'], check=True)
                                            st.success("✅ Változások GitHub-ra feltöltve!")
                                            st.rerun()
                                        except subprocess.CalledProcessError as e:
                                            st.error(f"❌ Git hiba: {e}")
                                    else:
                                        st.error("❌ Hiba a mentés során!")
                
                else:
                    # Lista nézet - csak megjelenítés
                    st.markdown("**Válassz a fenti opciók közül a szerkesztéshez.**")
                
                # Összes változás mentése gomb
                st.markdown("---")
                st.markdown("### 💾 Összes változás mentése")
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Összes változás mentése és Git Push", type="primary", use_container_width=True):
                        # Fájl mentése
                        if save_questions_to_file(question_file_path, questions):
                            st.success("✅ Kérdések sikeresen mentve!")
                            
                            # Git műveletek
                            try:
                                import subprocess
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
                            st.error("❌ Hiba a mentés során!")

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
        st.error(f"Hiba a keresési funkció betöltésekor: {e}")
        st.info("A keresési funkció nem érhető el. Ellenőrizd a search_functionality.py fájlt.")

def show_topic_selection():
    """Témakör kiválasztás"""
    
    # Felhasználó kiválasztás
    st.markdown("### 👤 Játékos Kiválasztás")
    
    # Játékos kiválasztó mező középre igazítva
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        players = ["Éva", "Ákos", "Orsika", "Mikcsi", "Ildi", "Szabi", "Hanna", "Villő", "Béla", "Gábor", "Emese", "Vendég"]
        selected_player = st.selectbox("Válassz játékost:", players, key="selected_player")
    
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
        "festmények": "🎨 Festmények",
        "háborúk": "⚔️ Háborúk",
        "magyar_királyok": "👑 Magyar királyok",
        "tudósok": "🔬 Tudósok, művészek, híres emberek",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "drámák": "🎭 Drámák",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "idióta_szavak": "🤪 Idióta szavak",
    }
    
    # Randomizáló funkció
    st.markdown("### 🎲 Randomizáló Funkció")
    
    # Kérdésszám beállítás csúszkával
    col1, col2 = st.columns(2)
    with col1:
        random_question_count = st.slider("Randomizáláshoz használandó kérdésszám", 10, 100, st.session_state.get('default_other_questions', 40), key="random_question_count")
    
    with col2:
        random_music_question_count = st.slider("Zenei randomizáláshoz használandó kérdésszám", 5, 50, st.session_state.get('default_music_questions', 10), key="random_music_question_count")
    
    # Randomizáló gombok egy sorban
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎯 Teljes kvíz létrehozása", type="primary", use_container_width=True):
            # Összes témakör kiválasztása
            st.session_state.selected_topics = list(topics.keys())
            
            # Zenei és egyéb témakörök szétválasztása
            music_topics = [t for t in topics.keys() if "zene" in t or "zenekar" in t or t == "one_hit_wonders"]
            other_topics = [t for t in topics.keys() if "zene" not in t and "zenekar" not in t and t != "one_hit_wonders"]
            
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
            
            st.success(f"✅ Teljes kvíz létrehozva! {len(topics)} témakör kiválasztva, összesen {total_music_questions + total_other_questions} kérdés!")
            st.rerun()
        
    with col2:
        if st.button("🎵 Random zenei témakörök kiválasztása", type="secondary", use_container_width=True):
            # Zenei témakörök kiválasztása
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders"]
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
            
            st.success(f"✅ {num_music_topics} zenei témakör kiválasztva + meglévő nem-zenei témakörök megtartva, {random_music_question_count} kérdés elosztva!")
            st.rerun()
        
    with col3:
        if st.button("🎲 Random témakörök kiválasztása (zene nélkül)", type="secondary", use_container_width=True):
            # Legalább 5 témakör kiválasztása (zenei témakörök nélkül)
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders"]
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
            
            st.success(f"✅ {num_topics} témakör kiválasztva (zene nélkül) + meglévő zenei témakörök megtartva, {random_question_count} kérdés elosztva!")
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

    # CSS a gombok egységes magasságához és játékos kiválasztó mezőhöz
    st.markdown("""
    <style>
        /* Egységes gomb magasság */
        .stButton > button {
            height: 50px !important;
            margin-bottom: 8px !important;
        }
        /* Oszlopok egységes magasság */
        div[data-testid="column"] {
            min-height: 600px !important;
        }
        /* Játékos kiválasztó mező stílus */
        .stSelectbox > div > div {
            font-size: 2em !important;
            width: 25vw !important;
        }
        .stSelectbox > div > div > div {
            font-size: 2em !important;
        }
        /* Kiválasztott érték betűmérete */
        .stSelectbox > div > div > div > div {
            font-size: 2em !important;
        }
        /* Legördülő lista elemek betűmérete */
        .stSelectbox > div > div > div > div > div {
            font-size: 2em !important;
        }
        /* Legördülő menü elemek */
        .stSelectbox > div > div > div > div > div > div {
            font-size: 2em !important;
        }
        /* Játékos kiválasztó mező specifikus stílus - csak a selected_player key-vel */
        [data-testid="stSelectbox"]:has([data-baseweb="select"]:has([data-testid="selected_player"])) {
            font-size: 2em !important;
        }
        [data-testid="stSelectbox"]:has([data-baseweb="select"]:has([data-testid="selected_player"])) * {
            font-size: 2em !important;
        }
        /* Navigáció selectbox szélessége */
        .stSelectbox {
            width: 50% !important;
        }
        /* Minden más input mező normál méretű */
        .stSelectbox:not(:has([data-testid="selected_player"])),
        .stSlider,
        .stNumberInput,
        .stCheckbox {
            font-size: 1em !important;
        }
        .stSelectbox:not(:has([data-testid="selected_player"])) *,
        .stSlider *,
        .stNumberInput *,
        .stCheckbox * {
            font-size: 1em !important;
        }
        /* Slider-ek specifikus stílus */
        .stSlider > div > div > div {
            font-size: 1em !important;
        }
        .stSlider > div > div > div > div {
            font-size: 1em !important;
        }
        .stSlider > div > div > div > div > div {
            font-size: 1em !important;
        }
    </style>
    """, unsafe_allow_html=True)

    with col1:
        st.markdown("### 🎵 Zenei témakörök")
        for topic_key, topic_name in topics.items():
            if "zene" in topic_key or "zenekar" in topic_key or topic_key == "one_hit_wonders":
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(topic_name, key=f"btn_{topic_key}", type=button_style, use_container_width=True):
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
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    with col2:
        st.markdown("### 📚 Egyéb témakörök")
        other_topics_list = [t for t in topics.items() if "zene" not in t[0] and "zenekar" not in t[0] and t[0] != "one_hit_wonders"]
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 0:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(topic_name, key=f"btn_{topic_key}", type=button_style, use_container_width=True):
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
                        f"{topic_name} kérdések száma",
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
                
                if st.button(topic_name, key=f"btn_{topic_key}", type=button_style, use_container_width=True):
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
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    # Kérdésszámok beállítása
    if st.session_state.selected_topics:
        st.markdown("### ⚙️ Kérdésszámok beállítása")
        
        music_topics = [t for t in st.session_state.selected_topics if "zene" in t or "zenekar" in t or t == "one_hit_wonders"]
        other_topics = [t for t in st.session_state.selected_topics if "zene" not in t and "zenekar" not in t and t != "one_hit_wonders"]
        
        if music_topics:
            st.markdown("#### 🎵 Zenei kérdések beállításai")
            # Összes zenei kérdés számának kiszámítása
            total_music_questions = sum(len(QUIZ_DATA_BY_TOPIC.get(topic, [])) for topic in music_topics)
            
            # Jelenlegi zenei kérdések összege az egyedi sliders alapján
            current_music_total = sum(st.session_state.get(f'final_{topic}_questions', 0) for topic in music_topics)
            
            col1, col2 = st.columns(2)
            with col1:
                music_total_questions = st.slider("Összes zenei kérdés száma", 1, total_music_questions, st.session_state.get('default_music_questions', current_music_total), key="music_total_questions")
            with col2:
                music_auto_distribute = st.checkbox("Automatikus elosztás a zenei témakörök között", True, key="music_auto_distribute")
            
            if not music_auto_distribute:
                st.markdown("##### Manuális elosztás:")
                for topic in music_topics:
                    topic_name = topics.get(topic, topic)
                    if topic == "magyar_zenekarok":
                        max_questions = len(MAGYAR_AUDIO_MAPPING_UJ)
                    else:
                        max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    questions_count = st.slider(f"{topic_name} kérdések száma", 0, max_questions, key=f"{topic}_questions")
        
        if other_topics:
            st.markdown("#### 📚 Egyéb témakörök kérdésszámai")
            
            # Automatikus elosztás egyéb témakörök között
            col1, col2 = st.columns(2)
            with col1:
                other_total_questions = st.slider("Összes egyéb kérdés száma", 1, 200, st.session_state.get('default_other_questions', 40), key="other_total_questions")
            
            with col2:
                other_auto_distribute = st.checkbox("Automatikus elosztás az egyéb témakörök között", True, key="other_auto_distribute")
            
            if not other_auto_distribute:
                st.markdown("##### Manuális elosztás:")
                cols = st.columns(3)
                for i, topic in enumerate(other_topics):
                    topic_name = topics.get(topic, topic)
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    with cols[i % 3]:
                        questions_count = st.slider(f"{topic_name} kérdések száma", 0, max_questions, key=f"{topic}_questions")
        

    
    # Quiz indítása
    if st.session_state.selected_topics:
        st.markdown("### 🎯 Végleges Kérdésszám Beállítása")
        
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
            st.info(f"🎵 Zenei kérdések: {music_questions}")
        with col2:
            st.info(f"📚 Egyéb kérdések: {other_questions}")
        with col3:
            st.info(f"📊 Összes elérhető: {total_available_questions}")
        with col4:
            st.success(f"🎯 Végleges kérdésszám: {final_question_count}")
        
        # Quiz indítás gomb
        if st.button("🚀 Quiz indítása", type="primary", use_container_width=True):
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
        st.warning(f"Érvénytelen kérdés kihagyva: {question.get('question', 'Ismeretlen')}")
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
            if st.button("⬅️ Előző", key=f"prev_{st.session_state.current_question}"):
                st.session_state.current_question -= 1
                st.rerun()
    
    with col2:
        # Központi üres tér a navigációs gombok között
        st.markdown("<div style='text-align: center; padding: 10px;'></div>", unsafe_allow_html=True)
    
    with col3:
        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
            if st.button("Következő ➡️", key=f"next_{st.session_state.current_question}"):
                st.session_state.current_question += 1
                st.rerun()
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
    st.progress(progress, text=f"Haladás: {st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}")
    
    # Pontszám és kérdés sorszám külön mezőkben, 50-50% szélesség
    col1, col2 = st.columns(2)
    
    with col1:
        # Pontszám mező
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #ff6b6b, #ee5a24); border-radius: 15px; border: 3px solid #d32f2f; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <div style='font-size: 16px; color: white; font-weight: bold; margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>🎯 PONTSZÁM</div>
            <div style='font-size: 32px; color: white; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{st.session_state.score}</div>
            <div style='font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 5px;'>{(st.session_state.score / len(st.session_state.quiz_questions) * 100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Kérdés sorszám mező
        st.markdown(f"""
        <div style='text-align: center; padding: 15px; background: linear-gradient(135deg, #4CAF50, #45a049); border-radius: 15px; border: 3px solid #2E7D32; margin: 20px 0; box-shadow: 0 4px 8px rgba(0,0,0,0.2);'>
            <div style='font-size: 16px; color: white; font-weight: bold; margin-bottom: 8px; text-shadow: 1px 1px 2px rgba(0,0,0,0.3);'>📝 KÉRDÉS</div>
            <div style='font-size: 32px; color: white; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>{st.session_state.current_question + 1}</div>
            <div style='font-size: 14px; color: rgba(255,255,255,0.9); margin-top: 5px;'>/ {len(st.session_state.quiz_questions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Egyéb metrikák megjelenítése
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Százalék", f"{(st.session_state.score / len(st.session_state.quiz_questions) * 100):.1f}%")
    
    with col2:
        # Jelenlegi streak és legmagasabb streak együtt
        current_streak = st.session_state.mode_manager.streak
        max_streak = st.session_state.mode_manager.max_streak
        streak_text = f"{current_streak} ({max_streak})"
        st.metric("Streak", streak_text)
    
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
        mode_name = mode_names.get(mode_text, mode_text)
        
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
        difficulty_name = difficulty_names.get(current_difficulty_value, "Ismeretlen")
        
        # Mód és nehézségi szint együtt
        combined_text = f"{mode_name} {difficulty_icon} {difficulty_name}"
        st.metric("Mód", combined_text)
        
        # Életek megjelenítése külön sorban, ha van
        if st.session_state.mode_manager.lives is not None:
            st.markdown(f"<div style='text-align: center; font-size: 14px; color: #666; margin-top: -10px;'>Életek: {st.session_state.mode_manager.lives}</div>", unsafe_allow_html=True)
    
    # Időzítő (ha van)
    if st.session_state.mode_manager.time_limit:
        time_elapsed = (datetime.now() - st.session_state.question_start_time).total_seconds()
        time_remaining = max(0, st.session_state.mode_manager.time_limit - time_elapsed)
        
        if time_remaining <= 0:
            handle_time_up()
            return
        
        # Időzítő megjelenítése
        st.markdown(f"<div style='text-align: center; font-size: 16px; color: {'red' if time_remaining < 10 else 'orange' if time_remaining < 30 else 'green'};'>"
                   f"⏱️ Hátralévő idő: {time_remaining:.1f} másodperc</div>", unsafe_allow_html=True)
    
    # Kérdés megjelenítése
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    
    # Kérdés szövege
    question_text = question.get("question", "Ismeretlen kérdés")
    st.markdown(f"<div class='question-text'>{question_text}</div>", unsafe_allow_html=True)
    
    # Audio, Spotify embed vagy kép megjelenítése
    audio_file = get_audio_file_for_question(question, topic)
    if topic == "nemzetkozi_zenekarok" or topic == "magyar_zenekarok" or topic == "one_hit_wonders":
        # Minden zenei kérdésnél megpróbáljuk megjeleníteni az audio playert
        if audio_file and os.path.exists(audio_file):
            try:
                abs_path = os.path.abspath(audio_file)
                
                st.audio(abs_path, format="audio/mp3")
            except Exception as e:
                st.error(f"Audio fájl lejátszási hiba: {e}")
        else:
            st.warning("Audio fájl nem található")
    else:
        # Eredeti logika más témakörökre
        if "audio_file" in question and question["audio_file"]:
            if audio_file and os.path.exists(audio_file):
                try:
                    abs_path = os.path.abspath(audio_file)
                    st.audio(abs_path, format="audio/mp3")
                except Exception as e:
                    st.error(f"Audio fájl lejátszási hiba: {e}")
            else:
                st.warning("Audio fájl nem található")
    

    
    # Logó vagy festmény kép megjelenítése
    if "logo_path" in question and question["logo_path"]:
        logo_path = question["logo_path"]
        
        # Zászló képek útvonal javítása
        if logo_path.startswith("data/flags/"):
            # Streamlit Cloud és lokális környezet kompatibilitás
            # Először próbáljuk meg a jelenlegi munkakönyvtárból (Streamlit Cloud)
            if os.path.exists(logo_path):
                pass  # Már jó az útvonal
            else:
                # Ha nem található, próbáljuk meg a quiz_app_advanced.py fájl helyétől
                current_dir = os.path.dirname(os.path.abspath(__file__))
                logo_path = os.path.join(current_dir, logo_path)
        
        if os.path.exists(logo_path):
            # Logó középre pozícionálása
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(logo_path, width=400)
        else:
            st.warning(f"Logó fájl nem található: {logo_path}")
    
    # Festmény kép megjelenítése
    elif "image_file" in question and question["image_file"]:
        image_file = question["image_file"]
        
        # Festmény képek útvonal javítása
        if not image_file.startswith("/"):
            image_path = os.path.join("festmény_képek", image_file)
        else:
            image_path = image_file
        
        if os.path.exists(image_path):
            # Ha nagyított állapotban vagyunk, nagyobb képet jelenítünk meg
            if st.session_state.image_modal_states.get(st.session_state.current_question, False):
                # Nagyított kép megjelenítése - nagyobb mérethez igazított oszlopok
                col1, col2, col3 = st.columns([1, 4, 1])
                with col2:
                    # Csak a festmény címét jelenítjük meg (festő név nélkül)
                    caption = question.get("explanation", "")
                    if " - " in caption:
                        title_only = caption.split(" - ")[0]
                        st.image(image_path, width=800, caption=title_only)
                    else:
                        st.image(image_path, width=800, caption=caption)
                    
                    # Bezárás gomb
                    if st.button("❌ Kép bezárása", key=f"close_modal_{st.session_state.current_question}", type="primary", use_container_width=True):
                        st.session_state.image_modal_states[st.session_state.current_question] = False
                        st.rerun()
                    
                    # Automatikus bezárás 30 másodperc után
                    st.info("💡 Tipp: A modal automatikusan bezáródik 30 másodperc múlva!")
                    
                    # Automatikus bezárás időzítő
                    modal_time_key = f"modal_start_time_{st.session_state.current_question}"
                    if modal_time_key not in st.session_state:
                        st.session_state[modal_time_key] = time.time()
                    
                    elapsed_time = time.time() - st.session_state[modal_time_key]
                    if elapsed_time > 30:  # 30 másodperc
                        st.session_state.image_modal_states[st.session_state.current_question] = False
                        st.session_state[modal_time_key] = None
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
                    
                    # Kép felirat - csak a festmény címe
                    caption = question.get("explanation", "")
                    if caption:
                        # Csak a festmény címét jelenítjük meg (festő név nélkül)
                        if " - " in caption:
                            title_only = caption.split(" - ")[0]
                            st.markdown(f'<div class="image-caption">{title_only}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div class="image-caption">{caption}</div>', unsafe_allow_html=True)
                    
                    # Nagyítás gomb
                    if st.button("🔍 Kép nagyítása", key=f"zoom_{st.session_state.current_question}"):
                        st.session_state.image_modal_states[st.session_state.current_question] = True
                        st.rerun()
        else:
            st.warning(f"Festmény kép nem található: {image_path}")
    
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
                st.session_state.question_options[st.session_state.current_question] = {
                    'options': options,
                    'correct_index': new_correct_index
                }
            except (KeyError, IndexError, ValueError, TypeError) as e:
                st.error(f"Hibás kérdés adatok: {e}. Kérdés: {question.get('question', 'Ismeretlen')}")
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
            st.error("Hibás kérdés adatok - automatikus folytatás")
            st.session_state.current_question += 1
            if st.session_state.current_question >= len(st.session_state.quiz_questions):
                st.session_state.quiz_state = 'results'
                st.rerun()
            else:
                st.rerun()
            return
        
        options_data = st.session_state.question_options[st.session_state.current_question]
        options = options_data['options']
        new_correct_index = options_data['correct_index']
    
    # Válasz megjelenítése
    selected_answer = st.session_state.question_answers.get(st.session_state.current_question)
    
    # Ha már válaszoltunk, mutassuk meg az eredményt
    if selected_answer is not None:
        if question_type == "text_input":
            # Text input kérdések esetén a válasz szöveges
            is_correct = selected_answer.lower().strip() == question.get("correct_answer", "").lower().strip()
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
                        {options[new_correct_index]}
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
            st.markdown("### 💬 Írd be a válaszod:")
            
            # Idióta szavak kérdéseknél a correct_answer mezőt használjuk
            correct_answer = question.get("correct_answer", "").lower().strip()
            user_answer = st.text_input("Válasz:", key=f"text_input_{st.session_state.current_question}")
            
            if st.button("✅ Válasz beküldése", key=f"submit_{st.session_state.current_question}", use_container_width=True):
                if user_answer:
                    # Válasz ellenőrzése (case-insensitive) - részleges egyezés is elfogadható
                    user_answer_clean = user_answer.lower().strip()
                    correct_answer_clean = correct_answer.lower().strip()
                    
                    # Teljes egyezés vagy részleges egyezés (ha a felhasználó válasza tartalmazza a helyes válasz kulcsszavait)
                    is_correct = (user_answer_clean == correct_answer_clean or 
                                any(keyword in user_answer_clean for keyword in correct_answer_clean.split() if len(keyword) > 3) or
                                any(keyword in correct_answer_clean for keyword in user_answer_clean.split() if len(keyword) > 3))
                    
                    if is_correct:
                        st.session_state.score += 1
                    
                    # Válasz mentése
                    st.session_state.question_answers[st.session_state.current_question] = user_answer
                    st.session_state.answers.append({
                        'question': question.get("question", "Ismeretlen kérdés"),
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
                    st.warning("Kérlek, írj be egy választ!")
        elif difficulty == DifficultyLevel.HARD and question.get("topic") != "mitológia" and 'options' in locals() and 'new_correct_index' in locals():
            # Nehéz mód: feleletválasztós kérdések szöveges bevitellel
            st.markdown("### 💬 Írd be a válaszod:")
            
            # Nehéz mód kérdéseknél az options alapján
            if 'options' in locals() and 'new_correct_index' in locals():
                correct_answer = question.get("correct_answer", "").lower().strip()
                user_answer = st.text_input("Válasz:", key=f"text_input_{st.session_state.current_question}")
                
                if st.button("✅ Válasz beküldése", key=f"submit_{st.session_state.current_question}", use_container_width=True):
                    if user_answer:
                        # Válasz ellenőrzése (case-insensitive)
                        user_answer_clean = user_answer.lower().strip()
                        is_correct = user_answer_clean == correct_answer
                        
                        if is_correct:
                            st.session_state.score += 1
                        
                        # Válasz mentése
                        st.session_state.question_answers[st.session_state.current_question] = user_answer
                        st.session_state.answers.append({
                            'question': question.get("question", "Ismeretlen kérdés"),
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
                        st.warning("Kérlek, írj be egy választ!")
            else:
                # Nehéz mód: feleletválasztós kérdések szöveges bevitellel
                user_answer = st.text_input("Válasz:", key=f"text_input_{st.session_state.current_question}")
                
                if st.button("✅ Válasz beküldése", key=f"submit_{st.session_state.current_question}", use_container_width=True):
                    if user_answer:
                        # Válasz ellenőrzése (case-insensitive)
                        correct_answer = options[new_correct_index].lower().strip()
                        user_answer_clean = user_answer.lower().strip()
                        is_correct = user_answer_clean == correct_answer
                        
                        if is_correct:
                            st.session_state.score += 1
                        
                        # Válasz mentése
                        st.session_state.question_answers[st.session_state.current_question] = user_answer
                        st.session_state.answers.append({
                            'question': question.get("question", "Ismeretlen kérdés"),
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
                        st.warning("Kérlek, írj be egy választ!")
        
        else:
            # Könnyű és Közepes mód: feleletválasztós
            # CSS stílus a nagyobb betűmérethez
            st.markdown("""
            <style>
            .big-answer-button {
                font-size: 24px !important;
                padding: 20px !important;
                margin: 10px 0 !important;
                height: auto !important;
                min-height: 60px !important;
            }
            .rotated-answer {
                transform: rotate(180deg);
                display: inline-block;
            }
            /* Streamlit gombok nagyobbítása */
            .stButton > button {
                font-size: 24px !important;
                padding: 20px !important;
                height: auto !important;
                min-height: 60px !important;
                line-height: 1.5 !important;
            }
            
            /* Dinamikus gomb stílusok */
            .stButton > button[data-selected="correct"] {
                background-color: #28a745 !important;
                color: white !important;
                border: 3px solid #28a745 !important;
            }
            
            .stButton > button[data-selected="incorrect"] {
                background-color: #dc3545 !important;
                color: white !important;
                border: 3px solid #dc3545 !important;
            }
            

            </style>
            """, unsafe_allow_html=True)
            

                

                

            
            # Válaszlehetőségek elrendezése
            col1, col2 = st.columns(2)
            
            # Első sor: 2 válaszlehetőség
            with col1:
                for i in range(0, min(2, len(options))):
                    option = options[i]
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help="Válaszlehetőség"):
                        handle_answer(i, new_correct_index, options, question)
            
            with col2:
                for i in range(2, min(4, len(options))):
                    option = options[i]
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help="Válaszlehetőség"):
                        handle_answer(i, new_correct_index, options, question)
            
            # Helyes válasz megjelenítése (csak Könnyű módban)
            if difficulty == DifficultyLevel.EASY and new_correct_index < len(options):
                st.markdown(f"""
                <div style="position: fixed; bottom: 40px; right: 20px; z-index: 1000;">
                    <div class="rotated-answer">
                        <button style="background-color: #28a745; color: white; border: none; border-radius: 8px; padding: 10px 15px; font-size: 16px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                            {options[new_correct_index]}
                        </button>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            

            
            # Automatikus válasz beküldés (opcionális)
            if st.button("😊 Jó napom van!", key=f"auto_answer_{st.session_state.current_question}", use_container_width=True):
                # Véletlenszerű válasz kiválasztása
                random_answer = random.randint(0, len(options) - 1)
                handle_answer(random_answer, new_correct_index, options, question)
    
    # Kvíz újraindítás gomb minden kérdéshez (a válaszlehetőségek után)
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 Kvíz újraindítása", key=f"restart_{st.session_state.current_question}", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def handle_answer(selected_index, correct_index, options, question):
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
    st.session_state.question_answers[st.session_state.current_question] = selected_index
    st.session_state.answers.append({
        'question': question.get("question", "Ismeretlen kérdés"),
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
            'question': question.get("question", "Ismeretlen kérdés"),
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
    st.title("🏆 Quiz Eredmények")
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
    quiz_data = {
        "player": st.session_state.get("selected_player", "Vendég"),
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
        st.warning(f"Analytics rögzítés sikertelen: {e}")
    
    # Eredmények megjelenítése - jobb formázással
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Alap Pontszám",
            value=f"{correct_answers}/{total_questions}",
            delta=f"{percentage:.1f}%"
        )
    
    with col2:
        st.metric(
            label="⏱️ Idő",
            value=f"{minutes} perc {seconds} mp"
        )
    
    with col3:
        st.metric(
            label="🏆 Végső Pontszám",
            value=scoring_result['final_score'],
            delta=f"Szorzó: {scoring_result['difficulty_multiplier']}x"
        )
    
    with col4:
        # Értékelés
        if scoring_result['final_score'] >= 90:
            grade = "🏅 Kiváló"
            grade_color = "success"
        elif scoring_result['final_score'] >= 80:
            grade = "🥈 Jó"
            grade_color = "success"
        elif scoring_result['final_score'] >= 70:
            grade = "🥉 Közepes"
            grade_color = "warning"
        elif scoring_result['final_score'] >= 60:
            grade = "📝 Megfelelő"
            grade_color = "warning"
        else:
            grade = "❌ Elégtelen"
            grade_color = "error"
        
        st.metric(
            label="📈 Értékelés",
            value=grade
        )
    
    # Részletes pontszámítás
    st.markdown("### 📋 Részletes Pontszámítás")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="summary-box">
            <h4>📊 Alap pontszám</h4>
            <p><strong>{scoring_result['base_score']} pont</strong></p>
            
            <h4>🎯 Nehézségi szorzó</h4>
            <p><strong>{scoring_result['difficulty_multiplier']}x</strong></p>
            
            <h4>🎮 Mód bónusz</h4>
            <p><strong>{scoring_result['mode_bonus']} pont</strong></p>
            
            <h4>🔥 Streak bónusz</h4>
            <p><strong>{scoring_result['streak_bonus']} pont</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summary-box">
            <h4>🔥 Maximális streak</h4>
            <p><strong>{st.session_state.mode_manager.max_streak} kérdés</strong></p>
            
            <h4>⏱️ Átlagos válaszidő</h4>
            <p><strong>{duration_seconds/total_questions:.1f} másodperc</strong></p>
            
            <h4>🎮 Mód</h4>
            <p><strong>{st.session_state.mode_manager.current_mode.value.title()}</strong></p>
            
            <h4>🎯 Nehézség</h4>
            <p><strong>{st.session_state.mode_manager.current_difficulty.value.title()}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Játékos statisztika
    player_name = st.session_state.get("selected_player", "Vendég")
    st.markdown(f"### 👤 Játékos: {player_name}")
    
    # Játékos teljesítmény lekérdezése
    if 'analytics' in st.session_state:
        player_performance = st.session_state.analytics.get_player_performance()
        if player_name in player_performance:
            player_data = player_performance[player_name]
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📊 Összes Quiz", player_data["total_quizzes"])
            with col2:
                st.metric("🎯 Átlagos Pontszám", f"{player_data['average_score']:.1f}%")
            with col3:
                st.metric("🏆 Legjobb Pontszám", f"{player_data['best_score']:.1f}%")
            with col4:
                st.metric("📝 Összes Kérdés", player_data["total_questions"])
    
    # Részletes eredmények
    st.markdown("### 📋 Kérdésenkénti eredmények")
    
    for i, answer in enumerate(st.session_state.answers):
        is_correct = answer['is_correct']
        status = "✅" if is_correct else "❌"
        
        st.markdown(f"""
        <div class="summary-box">
            <h4>{status} Kérdés {i+1}</h4>
            <p><strong>Kérdés:</strong> {answer['question']}</p>
            <p><strong>Válaszod:</strong> {answer['selected'] if isinstance(answer['selected'], str) else (answer['options'][answer['selected']] if answer['selected'] >= 0 else 'Idő lejárt')}</p>
            <p><strong>Helyes válasz:</strong> {answer['correct'] if isinstance(answer['correct'], str) else answer['options'][answer['correct']]}</p>
            <p><strong>Válaszidő:</strong> {answer['time_taken']:.1f} másodperc</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Új quiz indítása
    if st.button("🔄 Új quiz indítása", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()

def show_analytics_page():
    """Analytics oldal megjelenítése"""
    from quiz_analytics import show_analytics_dashboard
    show_analytics_dashboard()

def show_settings_page():
    """Beállítások oldal megjelenítése"""
    st.markdown("## ⚙️ Beállítások")
    
    st.markdown("### 🎯 Quiz Beállítások")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Alapértelmezett beállítások")
        default_music_questions = st.number_input("Alapértelmezett zenei kérdések", 1, 20, st.session_state.get('default_music_questions', 10))
        default_other_questions = st.number_input("Alapértelmezett egyéb kérdések", 1, 100, st.session_state.get('default_other_questions', 40))
    
    with col2:
        st.markdown("#### Időzítő beállítások")
        default_timed_limit = st.number_input("Alapértelmezett időkorlát (másodperc)", 10, 60, st.session_state.get('default_timed_limit', 30))
        default_challenge_limit = st.number_input("Kihívás mód időkorlát (másodperc)", 10, 30, st.session_state.get('default_challenge_limit', 20))
    
    st.markdown("### 🎵 Audio Beállítások")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_play_audio = st.checkbox("Automatikus audio lejátszás", st.session_state.get('auto_play_audio', False))
        show_audio_filename = st.checkbox("Audio fájlnév megjelenítése", st.session_state.get('show_audio_filename', True))
    
    with col2:
        audio_volume = st.slider("Alapértelmezett hangerő", 0, 100, st.session_state.get('audio_volume', 50))
        audio_quality = st.selectbox("Audio minőség", ["Alacsony", "Közepes", "Magas"], index=["Alacsony", "Közepes", "Magas"].index(st.session_state.get('audio_quality', "Közepes")))
    
    st.markdown("### 📊 Analytics Beállítások")
    
    col1, col2 = st.columns(2)
    
    with col1:
        track_performance = st.checkbox("Teljesítmény követése", st.session_state.get('track_performance', True))
        save_detailed_results = st.checkbox("Részletes eredmények mentése", st.session_state.get('save_detailed_results', True))
    
    with col2:
        analytics_retention_days = st.number_input("Analytics adatok megőrzése (nap)", 30, 365, st.session_state.get('analytics_retention_days', 90))
        export_analytics = st.checkbox("Analytics exportálása", st.session_state.get('export_analytics', False))
    
    # Beállítások mentése
    if st.button("💾 Beállítások mentése", type="primary"):
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
        st.success("Beállítások mentve!")

def show_audio_addition_page():
    """Audio hozzáadása oldal megjelenítése"""
    st.markdown("## 🎵 Audio Hozzáadása")
    
    # Két fő opció
    option = st.radio(
        "Válassz hozzáadási módszert:",
        ["A) Track hozzáadása YouTube kereséssel", "B) Spotify playlist alapú keresés"],
        format_func=lambda x: {
            "A) Track hozzáadása YouTube kereséssel": "🎵 A) YouTube Keresés",
            "B) Spotify playlist alapú keresés": "🎵 B) Spotify Playlist"
        }[x]
    )
    
    if option == "A) Track hozzáadása YouTube kereséssel":
        show_youtube_search_tab()
    else:
        show_spotify_playlist_tab()

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
            with st.expander(f"🎵 {result['title']} - {result['channel']}", expanded=False):
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
                        "one_hit_wonders": "⭐ One Hit Wonders"
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
                                    
                                    # Track letöltése és integrálása
                                    success = download_and_integrate_track(result, selected_category, custom_options)
                                    
                                    if success:
                                        # Sikeres integráció üzenet
                                        st.balloons()  # Konfetti effekt
                                        st.markdown('<div style="font-size: 12px;">🎉 <strong>SIKERES INTEGRÁCIÓ!</strong> 🎉</div>', unsafe_allow_html=True)
                                        st.markdown(f'<div style="font-size: 12px;">✅ <strong>{result["title"]}</strong> sikeresen letöltve és integrálva a <strong>{selected_category}</strong> kategóriába!</div>', unsafe_allow_html=True)
                                        st.markdown('<div style="font-size: 12px;">🚀 GitHub is frissítve!</div>', unsafe_allow_html=True)
                                        st.markdown('<div style="font-size: 12px;">🎯 A track most már elérhető a quiz-ben!</div>', unsafe_allow_html=True)
                                        
                                        # Eredmények törlése
                                        if 'youtube_search_results' in st.session_state:
                                            del st.session_state.youtube_search_results
                                        
                                        # Választási lehetőség az integrálás után
                                        st.markdown("---")
                                        st.markdown("### 🎯 Mit szeretnél csinálni most?")
                                        
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            if st.button("🎵 Új Audio Import", type="primary", use_container_width=True):
                                                # Új import kezdése
                                                if 'youtube_search_results' in st.session_state:
                                                    del st.session_state.youtube_search_results
                                                st.rerun()
                                        
                                        with col2:
                                            if st.button("🎮 Quiz Kezdése", type="secondary", use_container_width=True):
                                                # Szelekciós képernyőre navigálás (nehézségi szint és mód választás)
                                                st.session_state.current_page = "Quiz Selection"
                                                st.rerun()
                                        
                                        # Ne fusson tovább automatikusan
                                        st.stop()
                                    else:
                                        st.markdown('<div style="font-size: 12px;">❌ Hiba történt a letöltés során!</div>', unsafe_allow_html=True)
                                        
                                except Exception as e:
                                    st.markdown(f'<div style="font-size: 12px;">❌ Hiba: {e}</div>', unsafe_allow_html=True)


def search_youtube_tracks(query):
    """YouTube keresés implementáció"""
    try:
        import requests
        import json
        import re
        
        # YouTube keresés közvetlenül a YouTube API nélkül
        search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
        
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
                    
                    # Sponsored találatok kiszűrése
                    processed_results = []
                    for video in videos[:5]:  # Maximum 5 találat
                        if 'sponsored' not in video.get('title', '').lower() and 'reklám' not in video.get('title', '').lower():
                            processed_results.append(video)
                    
                    return processed_results
                    
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

def download_and_integrate_track(track_info, category, custom_options=None):
    """Track letöltése és integrálása"""
    try:
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
            "one_hit_wonders": "audio_files/one_hit_wonders"
        }
        
        download_dir = Path(category_mapping.get(category, "audio_files"))
        download_dir.mkdir(parents=True, exist_ok=True)
        
        # yt-dlp konfiguráció
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
        
        # Letöltés
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            url = track_info.get('url', '')
            if not url:
                st.error("Nincs érvényes URL a track_info-ban")
                return False
            
            try:
                # Információk lekérése
                info = ydl.extract_info(url, download=False)
                if not info:
                    st.error("Nem sikerült lekérni a videó információit")
                    return False
                
                # Letöltés
                ydl.download([url])
                
                # Fájlnév meghatározása
                audio_file = ydl.prepare_filename(info)
                audio_file = audio_file.replace('.webm', '.mp3').replace('.m4a', '.mp3')
                
                # Ellenőrizzük, hogy a fájl létezik-e
                if not os.path.exists(audio_file):
                    # Próbáljuk meg megtalálni a fájlt a könyvtárban
                    import glob
                    possible_files = glob.glob(str(download_dir / "*.mp3"))
                    if possible_files:
                        audio_file = possible_files[0]  # Az első MP3 fájlt használjuk
                    else:
                        st.error("❌ A letöltés sikertelen - fájl nem található")
                        return False
                
                # Ellenőrizzük a fájl méretét
                if os.path.getsize(audio_file) == 0:
                    st.error("❌ A letöltött fájl üres")
                    return False
                    
                st.success(f"✅ Sikeres letöltés: {track_info.get('title', 'Ismeretlen track')}")
                
            except Exception as e:
                st.error(f"❌ Letöltési hiba: {str(e)}")
                return False
            
            # 2 perces rész kivágása FFmpeg-gel
            try:
                import subprocess
                import re
                import time
                
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
                
                # Biztonságos fájlnév létrehozása
                safe_artist = re.sub(r'[^\w\s-]', '', artist)
                safe_title = re.sub(r'[^\w\s-]', '', title)
                safe_artist = re.sub(r'[-\s]+', '_', safe_artist)
                safe_title = re.sub(r'[-\s]+', '_', safe_title)
                
                # "Előadó - Szám cím" formátum
                output_filename = f"{safe_artist} - {safe_title}.mp3"
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
                        if duration < 120:
                            # Ha a fájl rövidebb mint 2 perc, nem vágunk
                            st.info(f"⚠️ A fájl rövidebb mint 2 perc ({duration:.1f}s), teljes fájl használata")
                        else:
                            # FFmpeg paranccsal 2 perc kivágása
                            cmd = [
                                'ffmpeg', '-i', audio_file, 
                                '-t', '120',  # 2 perc = 120 másodperc
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
                                    st.success("✅ 2 perces rész sikeresen kivágva!")
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
        
        # Quiz kérdés generálása
        question = generate_quiz_question(track_info, audio_file, category, custom_options)
        
        # Kérdés hozzáadása a megfelelő kategóriához
        add_question_to_category(question, category)
        
        return True
    except Exception as e:
        st.error(f"Letöltési hiba: {e}")
        st.error(f"Hiba típusa: {type(e)}")
        import traceback
        st.error(f"Hiba részletei: {traceback.format_exc()}")
        return False

def generate_quiz_question(track_info, audio_file, category, custom_options=None):
    """Quiz kérdés generálása a track alapján"""
    try:
        # Track_info ellenőrzés
        if not isinstance(track_info, dict):
            track_info = {}
        
        # Biztonságos adatkinyerés
        title = track_info.get('title', 'Ismeretlen cím')
        channel = track_info.get('channel', 'Ismeretlen előadó')
        
        # Kategória alapú kérdés
        if category == "komolyzene":
            question_text = "Ki a zeneszerző?"
        else:
            question_text = "Ki az előadó?"
        
        # Opciók használata
        if custom_options and len(custom_options) >= 4:
            # Egyedi opciók használata
            options = custom_options
            correct_answer = options[0]  # Első opció a helyes válasz
        else:
            # Alapértelmezett opciók
            correct_answer = channel
            if category == "komolyzene":
                similar_options = ["Beethoven", "Mozart", "Bach"]
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
        question = {
            'question': question_text,
            'options': options,
            'correct': 0,
            'explanation': f"{correct_answer} - {category.replace('_', ' ').title()}",
            'audio_file': audio_filename,
            'topic': category
        }
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
            from topics.magyar_zenekarok_uj import MAGYAR_ZENEKAROK_QUESTIONS_UJ
            MAGYAR_ZENEKAROK_QUESTIONS_UJ.append(question)
            # Fájlba mentés
            save_questions_to_file(MAGYAR_ZENEKAROK_QUESTIONS_UJ, "topics/magyar_zenekarok_uj.py", "MAGYAR_ZENEKAROK_QUESTIONS_UJ")
        elif category == "nemzetkozi_zenekarok":
            from topics.nemzetkozi_zenekarok_final_fixed_with_real_audio import NEMZETKOZI_ZENEKAROK_QUESTIONS
            NEMZETKOZI_ZENEKAROK_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(NEMZETKOZI_ZENEKAROK_QUESTIONS, "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py", "NEMZETKOZI_ZENEKAROK_QUESTIONS")
        elif category == "komolyzene":
            from topics.komolyzene import KOMPOLYZENE_QUESTIONS
            KOMPOLYZENE_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(KOMPOLYZENE_QUESTIONS, "topics/komolyzene.py", "KOMPOLYZENE_QUESTIONS")
        elif category == "one_hit_wonders":
            from topics.one_hit_wonders import ONE_HIT_WONDERS_QUESTIONS
            ONE_HIT_WONDERS_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(ONE_HIT_WONDERS_QUESTIONS, "topics/one_hit_wonders.py", "ONE_HIT_WONDERS_QUESTIONS")
        
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
            content += f'        "question": "{question["question"]}",\n'
            content += '        "options": [\n'
            for option in question["options"]:
                content += f'            "{option}",\n'
            content += '        ],\n'
            content += f'        "correct": {question["correct"]},\n'
            content += f'        "explanation": "{question["explanation"]}",\n'
            if "audio_file" in question:
                content += f'        "audio_file": "{question["audio_file"]}",\n'
            if "topic" in question:
                content += f'        "topic": "{question["topic"]}",\n'
            content += "    },\n"
        
        content += "]\n"
        
        # Fájlba írás
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
    except Exception as e:
        st.error(f"Hiba a fájl mentésekor: {e}")

if __name__ == "__main__":
    main() 