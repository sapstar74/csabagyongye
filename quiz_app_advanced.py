"""
🧠 PDF Alapú Quiz Alkalmazás - Fejlett Verzió
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
from custom_audio_player import audio_player_with_download
from youtube_audio_mapping import get_youtube_audio_filename_cached, get_youtube_audio_info
from magyar_audio_mapping_uj import MAGYAR_AUDIO_MAPPING_UJ, get_magyar_audio_uj_path
from nemzetkozi_audio_mapping_complete import get_nemzetkozi_audio_path
from quiz_analytics import QuizAnalytics
from quiz_modes import QuizModeManager, QuizMode, DifficultyLevel, QuizModeUI, QuizScoring
from auto_audio_player import auto_audio_player_simple

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
    page_title="Quiz App - Fejlett Verzió",
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
    if topic == "magyar_zenekarok":
        if "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_path = get_magyar_audio_uj_path(index)
                if audio_path and os.path.exists(audio_path):
                    return str(audio_path)
            except Exception as e:
                pass
        return None
    elif topic == "nemzetkozi_zenekarok":
        # Nemzetközi zenekarok - audio_file vagy original_index alapú
        if "audio_file" in question and question["audio_file"]:
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
            audio_dir = Path(__file__).parent / "audio_files_komolyzene"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
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
    
    # Végleges kérdésszám használata
    final_question_count = st.session_state.get('final_question_count', 40)
    
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
            questions_count = min(questions_count, len(topic_questions))
            print(f"[DEBUG] {topic} kiválasztott kérdésszám: {questions_count}")
            
            if questions_count > 0:
                total_selected_questions += questions_count
                # Véletlenszerű kérdések kiválasztása
                selected_indices = random.sample(range(len(topic_questions)), questions_count)
                for idx in selected_indices:
                    question = topic_questions[idx].copy()
                    # Ellenőrizzük, hogy a kérdés rendelkezik-e a szükséges mezőkkel
                    if "options" not in question or "correct" not in question:
                        invalid_questions += 1
                        debug_invalid.append((topic, idx, question))
                        continue
                    question['topic'] = topic
                    # --- Magyar zenekarok: opciók és helyes válasz igazítása ---
                    if topic == "magyar_zenekarok":
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
    if len(all_questions) > final_question_count:
        all_questions = all_questions[:final_question_count]
    
    # Debug információ
    st.info(f"Kiválasztott kérdések: {len(all_questions)} / {final_question_count} (összesen: {total_selected_questions})")
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
    
    st.markdown('<h1 class="main-header">🎯 Quiz Alkalmazás - Fejlett Verzió</h1>', unsafe_allow_html=True)
    
    # Sidebar navigáció
    with st.sidebar:
        st.markdown("## 🧭 Navigáció")
        page = st.selectbox(
            "Válassz oldalt:",
            ["Quiz", "Keresés", "Analytics", "Beállítások"],
            format_func=lambda x: {
                "Quiz": "🎯 Quiz",
                "Keresés": "🔍 Keresés",
                "Analytics": "📊 Analytics", 
                "Beállítások": "⚙️ Beállítások"
            }[x]
        )
    
    if page == "Quiz":
        show_quiz_page()
    elif page == "Keresés":
        show_search_page()
    elif page == "Analytics":
        show_analytics_page()
    elif page == "Beállítások":
        show_settings_page()

def show_quiz_page():
    """Quiz oldal megjelenítése"""
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()
    elif st.session_state.quiz_state == 'results':
        show_results()

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
    st.markdown("## 📚 Témakörök és Mód Kiválasztása")
    
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
    
    # Randomizáló funkció
    st.markdown("### 🎲 Randomizáló Funkció")
    
    # Kérdésszám beállítás csúszkával
    col1, col2 = st.columns(2)
    with col1:
        random_question_count = st.slider("Randomizáláshoz használandó kérdésszám", 10, 100, 40, key="random_question_count")
    
    with col2:
        random_music_question_count = st.slider("Zenei randomizáláshoz használandó kérdésszám", 5, 50, 20, key="random_music_question_count")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🎲 Random témakörök kiválasztása (zene nélkül)", type="secondary", use_container_width=True):
            # Legalább 5 témakör kiválasztása (zenei témakörök nélkül)
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok"]
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
            
            # Checkbox állapotok frissítése
            for topic_key in topics.keys():
                checkbox_key = f"topic_{topic_key}"
                if topic_key in selected_random_topics or topic_key in existing_music_topics:
                    st.session_state[checkbox_key] = True
                elif topic_key not in music_topics:  # Csak nem-zenei témakörök törlése
                    st.session_state[checkbox_key] = False
            
            # Kérdésszámok beállítása
            for i, topic in enumerate(selected_random_topics):
                topic_questions = questions_per_topic + (1 if i < remaining_questions else 0)
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
        if st.button("🎵 Random zenei témakörök kiválasztása", type="secondary", use_container_width=True):
            # Zenei témakörök kiválasztása
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok"]
            num_music_topics = random.randint(2, 3)  # 2-3 zenei témakör
            selected_music_topics = random.sample(music_topics, num_music_topics)
            
            # Kérdések elosztása a zenei témakörök között
            questions_per_music_topic = random_music_question_count // num_music_topics
            remaining_music_questions = random_music_question_count % num_music_topics
            
            # Meglévő nem-zenei témakörök megtartása
            existing_other_topics = [topic for topic in st.session_state.selected_topics if topic not in music_topics]
            
            # Témakörök kiválasztása (nem-zenei + új zenei)
            st.session_state.selected_topics = existing_other_topics + selected_music_topics
            
            # Checkbox állapotok frissítése
            for topic_key in topics.keys():
                checkbox_key = f"topic_{topic_key}"
                if topic_key in selected_music_topics or topic_key in existing_other_topics:
                    st.session_state[checkbox_key] = True
                elif topic_key in music_topics:  # Csak zenei témakörök törlése
                    st.session_state[checkbox_key] = False
            
            # Kérdésszámok beállítása
            for i, topic in enumerate(selected_music_topics):
                topic_questions = questions_per_music_topic + (1 if i < remaining_music_questions else 0)
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
        if st.button("🔄 Reset kiválasztás", type="secondary", use_container_width=True):
            st.session_state.selected_topics = []
            # Checkbox állapotok törlése
            for topic_key in topics.keys():
                checkbox_key = f"topic_{topic_key}"
                st.session_state[checkbox_key] = False
            st.rerun()
    
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
        st.markdown("### 🎵 Zenei témakörök")
        for topic_key, topic_name in topics.items():
            if "zene" in topic_key or "zenekar" in topic_key:
                # Checkbox állapot kezelése
                checkbox_key = f"topic_{topic_key}"
                # Alapértelmezetten nincs bejelölve, csak ha már kiválasztva van
                default_checked = topic_key in st.session_state.selected_topics
                is_checked = st.checkbox(topic_name, key=checkbox_key, value=default_checked)
                
                # Témakör hozzáadása/eltávolítása a listából
                if is_checked and topic_key not in st.session_state.selected_topics:
                    st.session_state.selected_topics.append(topic_key)
                elif not is_checked and topic_key in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 20 zenei témaköröknél (növelve 10-ről)
                    default_questions = min(20, max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
                    final_topic_questions = st.slider(
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        key=f"final_{topic_key}_questions"
                    )
    
    with col2:
        st.markdown("### 📚 Egyéb témakörök")
        other_topics_list = [t for t in topics.items() if "zene" not in t[0] and "zenekar" not in t[0]]
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 0:
                # Checkbox állapot kezelése
                checkbox_key = f"topic_{topic_key}"
                # Alapértelmezetten nincs bejelölve
                is_checked = st.checkbox(topic_name, key=checkbox_key)
                
                # Témakör hozzáadása/eltávolítása a listából
                if is_checked and topic_key not in st.session_state.selected_topics:
                    st.session_state.selected_topics.append(topic_key)
                elif not is_checked and topic_key in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 20 egyéb témaköröknél
                    default_questions = min(20, max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
                    final_topic_questions = st.slider(
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        key=f"final_{topic_key}_questions"
                    )
    
    with col3:
        st.markdown("### 📚 Egyéb témakörök (folyt.)")
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 1:
                # Checkbox állapot kezelése
                checkbox_key = f"topic_{topic_key}"
                # Alapértelmezetten nincs bejelölve
                is_checked = st.checkbox(topic_name, key=checkbox_key)
                
                # Témakör hozzáadása/eltávolítása a listából
                if is_checked and topic_key not in st.session_state.selected_topics:
                    st.session_state.selected_topics.append(topic_key)
                elif not is_checked and topic_key in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    # Alapértelmezett érték: 20 egyéb témaköröknél
                    default_questions = min(20, max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
                    final_topic_questions = st.slider(
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        key=f"final_{topic_key}_questions"
                    )
    
    # Kérdésszámok beállítása
    if st.session_state.selected_topics:
        st.markdown("### ⚙️ Kérdésszámok beállítása")
        
        music_topics = [t for t in st.session_state.selected_topics if "zene" in t or "zenekar" in t]
        other_topics = [t for t in st.session_state.selected_topics if "zene" not in t and "zenekar" not in t]
        
        if music_topics:
            st.markdown("#### 🎵 Zenei kérdések beállításai")
            # Összes zenei kérdés számának kiszámítása
            total_music_questions = sum(len(QUIZ_DATA_BY_TOPIC.get(topic, [])) for topic in music_topics)
            
            # Jelenlegi zenei kérdések összege az egyedi sliders alapján
            current_music_total = sum(st.session_state.get(f'final_{topic}_questions', 0) for topic in music_topics)
            
            col1, col2 = st.columns(2)
            with col1:
                music_total_questions = st.slider("Összes zenei kérdés száma", 1, total_music_questions, current_music_total, key="music_total_questions")
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
                other_total_questions = st.slider("Összes egyéb kérdés száma", 1, 200, key="other_total_questions")
            
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
            # Végleges kérdésszám beállítása - csak akkor, ha még nincs beállítva
            if 'final_question_count' not in st.session_state:
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
    if "options" not in question or "correct" not in question:
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
    if topic == "nemzetkozi_zenekarok" or topic == "magyar_zenekarok":
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
    
    # Válaszlehetőségek randomizálása - robusztus hibakezeléssel
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
        is_correct = selected_answer == new_correct_index
        # --- Helyes válasz gomb (Könnyű módban) ---
        difficulty = st.session_state.mode_manager.current_difficulty
        if difficulty == DifficultyLevel.EASY and new_correct_index < len(options):
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
        
        # Idióta szavak kérdések vagy nehéz mód: szöveges bevitel
        if question_type == "text_input" or difficulty == DifficultyLevel.HARD:
            # Szöveges bevitel mód
            st.markdown("### 💬 Írd be a válaszod:")
            
            # Idióta szavak kérdéseknél a correct_answer mezőt használjuk
            if question_type == "text_input":
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
                            st.rerun()
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
                            st.rerun()
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
            
            /* Válasz visszajelzés stílusok */
            .correct-answer {
                background-color: #28a745 !important;
                color: white !important;
                border: 3px solid #28a745 !important;
            }
            
            .incorrect-answer {
                background-color: #dc3545 !important;
                color: white !important;
                border: 3px solid #dc3545 !important;
            }
            

            </style>
            """, unsafe_allow_html=True)
            
            # Válasz állapot ellenőrzése
            answer_state = getattr(st.session_state, 'answer_state', None)
            show_answer_feedback = False
            if answer_state and (time.time() - answer_state['timestamp']) < 2.0:
                show_answer_feedback = True
            
            # Válaszlehetőségek elrendezése
            col1, col2 = st.columns(2)
            
            # Első sor: 2 válaszlehetőség
            with col1:
                for i in range(0, min(2, len(options))):
                    option = options[i]
                    
                    # CSS osztály meghatározása válasz állapot alapján
                    button_class = ""
                    if show_answer_feedback:
                        if i == answer_state['selected_index']:
                            if answer_state['is_correct']:
                                button_class = "correct-answer"
                            else:
                                button_class = "incorrect-answer"
                        elif i == answer_state['correct_index']:
                            button_class = "correct-answer"
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help="Válaszlehetőség"):
                        if selected_answer is None:
                            handle_answer(i, new_correct_index, options, question)
                            st.rerun()
            
            with col2:
                for i in range(2, min(4, len(options))):
                    option = options[i]
                    
                    # CSS osztály meghatározása válasz állapot alapján
                    button_class = ""
                    if show_answer_feedback:
                        if i == answer_state['selected_index']:
                            if answer_state['is_correct']:
                                button_class = "correct-answer"
                            else:
                                button_class = "incorrect-answer"
                        elif i == answer_state['correct_index']:
                            button_class = "correct-answer"
                    
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               use_container_width=True, help="Válaszlehetőség"):
                        if selected_answer is None:
                            handle_answer(i, new_correct_index, options, question)
                            st.rerun()
            
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
            
            # Automatikus következő kérdésre lépés 2 másodperc után
            if show_answer_feedback:
                if st.session_state.quiz_state != 'results':
                    st.session_state.current_question += 1
                    st.session_state.question_start_time = datetime.now()
                    st.session_state.answer_state = None
                    st.rerun()
                else:
                    # Ha ez az utolsó kérdés, akkor töröljük a válasz állapotot
                    st.session_state.answer_state = None
            
            # Automatikus válasz beküldés (opcionális)
            if st.button("😊 Jó napom van!", key=f"auto_answer_{st.session_state.current_question}", use_container_width=True):
                # Véletlenszerű válasz kiválasztása
                random_answer = random.randint(0, len(options) - 1)
                handle_answer(random_answer, new_correct_index, options, question)
                st.rerun()
    
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
    
    # Válasz állapot beállítása 2 másodpercre
    st.session_state.answer_state = {
        'selected_index': selected_index,
        'correct_index': correct_index,
        'is_correct': is_correct,
        'timestamp': time.time()
    }
    
    # Ne hívjuk meg a st.rerun()-t itt, hagyjuk, hogy a show_quiz() kezelje a következő kérdést

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
        "topics": st.session_state.selected_topics,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "score_percentage": percentage,
        "duration_seconds": duration_seconds,
        "question_details": st.session_state.answers
    }
    st.session_state.analytics.record_quiz_session(quiz_data)
    
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
    
    # Részletes eredmények
    st.markdown("### 📋 Kérdésenkénti eredmények")
    
    for i, answer in enumerate(st.session_state.answers):
        is_correct = answer['is_correct']
        status = "✅" if is_correct else "❌"
        
        st.markdown(f"""
        <div class="summary-box">
            <h4>{status} Kérdés {i+1}</h4>
            <p><strong>Kérdés:</strong> {answer['question']}</p>
            <p><strong>Válaszod:</strong> {answer['options'][answer['selected']] if answer['selected'] >= 0 else 'Idő lejárt'}</p>
            <p><strong>Helyes válasz:</strong> {answer['options'][answer['correct']]}</p>
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
        default_music_questions = st.number_input("Alapértelmezett zenei kérdések", 1, 20, 10)
        default_other_questions = st.number_input("Alapértelmezett egyéb kérdések", 1, 20, 10)
    
    with col2:
        st.markdown("#### Időzítő beállítások")
        default_timed_limit = st.number_input("Alapértelmezett időkorlát (másodperc)", 10, 60, 30)
        default_challenge_limit = st.number_input("Kihívás mód időkorlát (másodperc)", 10, 30, 20)
    
    st.markdown("### 🎵 Audio Beállítások")
    
    col1, col2 = st.columns(2)
    
    with col1:
        auto_play_audio = st.checkbox("Automatikus audio lejátszás", False)
        show_audio_filename = st.checkbox("Audio fájlnév megjelenítése", True)
    
    with col2:
        audio_volume = st.slider("Alapértelmezett hangerő", 0, 100, 50)
        audio_quality = st.selectbox("Audio minőség", ["Alacsony", "Közepes", "Magas"], index=1)
    
    st.markdown("### 📊 Analytics Beállítások")
    
    col1, col2 = st.columns(2)
    
    with col1:
        track_performance = st.checkbox("Teljesítmény követése", True)
        save_detailed_results = st.checkbox("Részletes eredmények mentése", True)
    
    with col2:
        analytics_retention_days = st.number_input("Analytics adatok megőrzése (nap)", 30, 365, 90)
        export_analytics = st.checkbox("Analytics exportálása", False)
    
    # Beállítások mentése
    if st.button("💾 Beállítások mentése", type="primary"):
        st.success("Beállítások mentve!")

if __name__ == "__main__":
    main() 