"""
🧠 PDF Alapú Quiz Alkalmazás - Új magyar zenei kérdésekkel
10 kérdéses feleletválasztós teszt a feltöltött PDF tartalom alapján
"""

import streamlit as st
import random
import time
from datetime import datetime
import os
from pathlib import Path
from topics.foldrajz_complete import FOLDRAJZ_QUESTIONS_COMPLETE as FOLDRAJZ_QUESTIONS
from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS as ZENEK_QUESTIONS
from topics.tudosok import TUDOSOK_QUESTIONS
from topics.mitologia_all_questions import MITOLOGIA_QUESTIONS_ALL
from topics.haboru_all_questions import HABORU_QUESTIONS_ALL
from topics.kiralyok import KIRALYOK_QUESTIONS
from topics.allatok_balanced import ALLATOK_QUESTIONS_BALANCED
from topics.dramak import DRAMAK_QUESTIONS
from topics.sport_logok import SPORT_LOGOK_QUESTIONS
from topics.zaszlok_all_questions import ZASZLOK_QUESTIONS_ALL
from topics.magyar_zenekarok_correct import MAGYAR_ZENEKAROK_QUESTIONS
from topics.magyar_zenekarok_uj import MAGYAR_ZENEKAROK_QUESTIONS_UJ
from topics.nemzetkozi_zenekarok_final_fixed import NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak_reversed import IDIOTA_SZAVAK_QUESTIONS
from custom_audio_player import audio_player_with_download
from youtube_audio_mapping import get_youtube_audio_filename_cached, get_youtube_audio_info
from magyar_audio_mapping_uj import get_magyar_uj_audio_path, get_magyar_uj_audio_info
from auto_audio_player import auto_audio_player_simple

# Page config
st.set_page_config(
    page_title="Quiz App - Új magyar zenekkel",
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
        color: #333333;
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
        color: #333333;
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
</style>
""", unsafe_allow_html=True)

# Quiz adatok témakörök szerint csoportosítva
QUIZ_DATA_BY_TOPIC = {
    "földrajz": FOLDRAJZ_QUESTIONS,
    "komolyzene": ZENEK_QUESTIONS,
    "magyar_zenekarok": MAGYAR_ZENEKAROK_QUESTIONS + MAGYAR_ZENEKAROK_QUESTIONS_UJ,  # Összevont magyar kérdések
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
}

# Initialize session state
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = 'selection'
    st.session_state.selected_topics = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = []
    st.session_state.quiz_start_time = None

def reset_quiz():
    st.session_state.quiz_state = 'selection'
    st.session_state.selected_topics = []
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_questions = []
    st.session_state.quiz_start_time = None
    st.session_state.question_answers = {}
    st.session_state.question_options = {}

def get_audio_file_for_question(question, topic):
    """Visszaadja az audio fájl elérési útját a kérdéshez"""
    if topic == "magyar_zenekarok":
        # Magyar kérdések - ellenőrizzük, hogy új vagy régi kérdés
        if "audio_file" in question:
            # Új magyar kérdések - audio_files_magyar_uj könyvtárból
            audio_path = get_magyar_uj_audio_path(question["audio_file"].replace(".mp3", ""))
            if audio_path and os.path.exists(audio_path):
                return audio_path
        elif "original_index" in question:
            # Régi magyar kérdések - youtube_audio_mapping használata
            audio_filename = get_youtube_audio_filename_cached(question["original_index"], "magyar_zenekarok")
            if audio_filename:
                audio_dir = Path(__file__).parent / "audio_files"
                audio_path = audio_dir / audio_filename
                if audio_path.exists():
                    return str(audio_path)
    else:
        # Egyéb témakörök - youtube_audio_mapping használata
        if "original_index" in question:
            audio_filename = get_youtube_audio_filename_cached(question["original_index"], topic)
            if audio_filename:
                audio_dir = Path(__file__).parent / "audio_files"
                audio_path = audio_dir / audio_filename
                if audio_path.exists():
                    return str(audio_path)
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
    
    # Minden témakör kezelése egyedi sliders alapján
    for topic in st.session_state.selected_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            
            # Egyedi témakör slider használata
            questions_count = st.session_state.get(f'final_{topic}_questions', 0)
            questions_count = min(questions_count, len(topic_questions))
            
            if questions_count > 0:
                total_selected_questions += questions_count
                # Véletlenszerű kérdések kiválasztása
            selected_indices = random.sample(range(len(topic_questions)), questions_count)
            for idx in selected_indices:
                question = topic_questions[idx].copy()
                    
                    # Ellenőrizzük, hogy a kérdés rendelkezik-e a szükséges mezőkkel
                    if "options" not in question or "correct" not in question:
                        invalid_questions += 1
                        continue
                    
                question['original_index'] = idx
                question['topic'] = topic
                all_questions.append(question)
    
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
    st.markdown('<h1 class="main-header">🎯 Quiz Alkalmazás - Új magyar zenekkel</h1>', unsafe_allow_html=True)
    
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()
    elif st.session_state.quiz_state == 'results':
        show_results()

def show_topic_selection():
    st.markdown("## 📚 Témakörök kiválasztása")
    
    # Témakörök definiálása
    topics = {
        "földrajz": "🌍 Földrajz",
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar zenekarok (67 kérdés - régi + új)",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi zenekarok",
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
                if st.checkbox(topic_name, key=f"topic_{topic_key}"):
                    if topic_key not in st.session_state.selected_topics:
                        st.session_state.selected_topics.append(topic_key)
                else:
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(fair_distribution.get(topic_key, 0), max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
                    final_topic_questions = st.slider(
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    with col2:
        st.markdown("### 📚 Egyéb témakörök")
        other_topics_list = [t for t in topics.items() if "zene" not in t[0] and "zenekar" not in t[0]]
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 0:
                if st.checkbox(topic_name, key=f"topic_{topic_key}"):
                    if topic_key not in st.session_state.selected_topics:
                        st.session_state.selected_topics.append(topic_key)
                else:
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(fair_distribution.get(topic_key, 0), max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
                    final_topic_questions = st.slider(
                        f"{topic_name} kérdések száma",
                        min_value=0,
                        max_value=max_questions,
                        value=st.session_state.get(f"final_{topic_key}_questions", default_questions),
                        key=f"final_{topic_key}_questions"
                    )
    
    with col3:
        st.markdown("### 📚 Egyéb témakörök (folyt.)")
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 1:
                if st.checkbox(topic_name, key=f"topic_{topic_key}"):
                    if topic_key not in st.session_state.selected_topics:
                        st.session_state.selected_topics.append(topic_key)
                else:
                    if topic_key in st.session_state.selected_topics:
                        st.session_state.selected_topics.remove(topic_key)
                
                # Egyedi slider közvetlenül a checkbox alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(fair_distribution.get(topic_key, 0), max_questions)
                    st.session_state.setdefault(f"final_{topic_key}_questions", default_questions)
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
    
    # Zenei kérdések beállításai
    music_topics = [t for t in st.session_state.selected_topics if "zene" in t or "zenekar" in t]
    if music_topics:
            st.markdown("#### 🎵 Zenei kérdések beállításai")
            
            # Összes zenei kérdés számának kiszámítása
            total_music_questions = sum(len(QUIZ_DATA_BY_TOPIC.get(topic, [])) for topic in music_topics)
        
        col1, col2 = st.columns(2)
        with col1:
                music_total_questions = st.slider("Összes zenei kérdés száma", 1, total_music_questions, 20, key="music_total_questions")
        
        with col2:
            music_auto_distribute = st.checkbox("Automatikus elosztás a zenei témakörök között", True, key="music_auto_distribute")
        
        if not music_auto_distribute:
                st.markdown("##### Manuális elosztás:")
            for topic in music_topics:
                topic_name = topics.get(topic, topic)
                max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    default_questions = min(20 // len(music_topics), max_questions)
                    questions_count = st.slider(f"{topic_name} kérdések száma", 0, max_questions, default_questions, key=f"{topic}_questions")
    
    # Egyéb témakörök kérdésszámai
    other_topics = [t for t in st.session_state.selected_topics if "zene" not in t and "zenekar" not in t]
    if other_topics:
            st.markdown("#### 📚 Egyéb témakörök kérdésszámai")
            
            # Automatikus elosztás egyéb témakörök között
            col1, col2 = st.columns(2)
            with col1:
                other_total_questions = st.slider("Összes egyéb kérdés száma", 1, 200, 40, key="other_total_questions")
            
            with col2:
                other_auto_distribute = st.checkbox("Automatikus elosztás az egyéb témakörök között", True, key="other_auto_distribute")
            
            if not other_auto_distribute:
                st.markdown("##### Manuális elosztás:")
        cols = st.columns(3)
        for i, topic in enumerate(other_topics):
            topic_name = topics.get(topic, topic)
            max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    default_questions = min(40 // len(other_topics), max_questions)
            with cols[i % 3]:
                        questions_count = st.slider(f"{topic_name} kérdések száma", 0, max_questions, default_questions, key=f"{topic}_questions")
        

    
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
        
        # Végleges kérdésszám csúszka - automatikusan frissül az egyedi sliders változásakor
        final_question_count = st.slider(
            f"Végleges kérdésszám (max: {total_available_questions})",
            min_value=1,
            max_value=total_available_questions,
            key="final_question_count"
        )
        
        # Információk megjelenítése
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.info(f"🎵 Zenei kérdések: {music_questions}")
        with col2:
            st.info(f"📚 Egyéb kérdések: {other_questions}")
        with col3:
            st.info(f"📊 Összes elérhető: {total_available_questions}")
        with col4:
            st.success(f"🎯 Kiválasztott: {current_total}")
        
        # Quiz indítás gomb
    if st.button("🚀 Quiz indítása", type="primary", use_container_width=True):
        start_quiz()

def show_quiz():
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        st.session_state.quiz_state = 'results'
        st.rerun()
    
    question = st.session_state.quiz_questions[st.session_state.current_question]
    topic = question.get('topic', 'unknown')
    
    st.markdown('<div class="quiz-container">', unsafe_allow_html=True)
    
    # Kérdés száma és pontszám
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        st.markdown(f'<div class="score-display">Kérdés: {st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-display">Pontszám: {st.session_state.score}</div>', unsafe_allow_html=True)
    with col3:
        if st.button("🏁 Quiz befejezése", type="secondary"):
            st.session_state.quiz_state = 'results'
            st.rerun()
    
    # Kérdés szövege - jobb formázással
    st.markdown(f"""
    <div style="
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        color: #333;
        line-height: 1.5;
    ">
        {question["question"]}
    </div>
    """, unsafe_allow_html=True)
    
    # Logó vagy audio megjelenítése - csak zenei kérdéseknél audio
    if "logo_path" in question:
        # Logó kérdés - logó megjelenítése
        logo_path = question["logo_path"]
        if os.path.exists(logo_path):
            st.image(logo_path, width=300)
        else:
            st.warning(f"Logó fájl nem található: {logo_path}")
    elif topic in ["magyar_zenekarok", "nemzetkozi_zenekarok", "komolyzene"]:
        # Csak zenei kérdéseknél audio megjelenítése
        audio_file = get_audio_file_for_question(question, topic)
        if audio_file:
            auto_audio_player_simple(audio_file)
    else:
            st.info("Audio fájl nem található ehhez a kérdéshez.")
    
    # Session state inicializálása
    if 'question_answers' not in st.session_state:
        st.session_state.question_answers = {}
    if 'question_options' not in st.session_state:
        st.session_state.question_options = {}
    
    # Válaszlehetőségek randomizálása - hibakezeléssel
    if st.session_state.current_question not in st.session_state.question_options:
        # Ellenőrizzük, hogy a kérdés rendelkezik a szükséges mezőkkel
        if "options" not in question:
            st.error(f"Hibás kérdés struktúra: hiányzó 'options' mező. Kérdés: {question.get('question', 'Ismeretlen')}")
            st.button("Következő kérdés", on_click=lambda: setattr(st.session_state, 'current_question', st.session_state.current_question + 1))
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        if "correct" not in question:
            st.error(f"Hibás kérdés struktúra: hiányzó 'correct' mező. Kérdés: {question.get('question', 'Ismeretlen')}")
            st.button("Következő kérdés", on_click=lambda: setattr(st.session_state, 'current_question', st.session_state.current_question + 1))
            st.markdown('</div>', unsafe_allow_html=True)
            return
        
        try:
        options = question["options"].copy()
        correct_answer = options[question["correct"]]
        random.shuffle(options)
        new_correct_index = options.index(correct_answer)
        st.session_state.question_options[st.session_state.current_question] = {
            'options': options,
            'correct_index': new_correct_index
        }
        except (KeyError, IndexError, ValueError) as e:
            st.error(f"Hibás kérdés adatok: {e}. Kérdés: {question.get('question', 'Ismeretlen')}")
            st.button("Következő kérdés", on_click=lambda: setattr(st.session_state, 'current_question', st.session_state.current_question + 1))
            st.markdown('</div>', unsafe_allow_html=True)
            return
    
    options_data = st.session_state.question_options[st.session_state.current_question]
    options = options_data['options']
    new_correct_index = options_data['correct_index']
    
    # Válasz megjelenítése
    selected_answer = st.session_state.question_answers.get(st.session_state.current_question)
    
    # Ha már válaszoltunk, mutassuk meg az eredményt
    if selected_answer is not None:
        is_correct = selected_answer == new_correct_index
        if is_correct:
            st.success("✅ Helyes válasz!")
        else:
            st.error(f"❌ Helytelen! A helyes válasz: {options[new_correct_index]}")
        
        # Következő kérdés gomb
        if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
            if st.button("➡️ Következő kérdés", type="primary", use_container_width=True):
            st.session_state.current_question += 1
            st.rerun()
        else:
            if st.button("🏁 Quiz befejezése", type="primary", use_container_width=True):
            st.session_state.quiz_state = 'results'
            st.rerun()
    else:
        # Válaszlehetőségek megjelenítése
    for i, option in enumerate(options):
        if st.button(option, key=f"option_{st.session_state.current_question}_{i}", use_container_width=True):
            if selected_answer is None:
                    # Válasz kezelése
                    is_correct = i == new_correct_index
                    if is_correct:
                        st.session_state.score += 1
                    
                    # Válasz mentése
                st.session_state.question_answers[st.session_state.current_question] = i
                st.session_state.answers.append({
                    'question': question["question"],
                    'selected': i,
                    'correct': new_correct_index,
                        'options': options,
                        'is_correct': is_correct
                })
                    
                    # Automatikusan folytatjuk a következő kérdéssel
                    if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_state = 'results'
                st.rerun()
    
        # Automatikus válasz beküldés (opcionális)
        if st.button("🤖 Automatikus válasz", key=f"auto_answer_{st.session_state.current_question}", use_container_width=True):
            # Véletlenszerű válasz kiválasztása
            random_answer = random.randint(0, len(options) - 1)
            is_correct = random_answer == new_correct_index
            if is_correct:
                st.session_state.score += 1
            
            # Válasz mentése
            st.session_state.question_answers[st.session_state.current_question] = random_answer
            st.session_state.answers.append({
                'question': question["question"],
                'selected': random_answer,
                'correct': new_correct_index,
                'options': options,
                'is_correct': is_correct
            })
            
            # Automatikusan folytatjuk a következő kérdéssel
            if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                st.session_state.current_question += 1
                st.rerun()
            else:
            st.session_state.quiz_state = 'results'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_results():
    st.markdown('<h1 class="main-header">🏆 Quiz eredmények</h1>', unsafe_allow_html=True)
    
    # Eredmények számítása
    total_questions = len(st.session_state.quiz_questions)
    correct_answers = st.session_state.score
    percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
    
    # Idő számítása
    if st.session_state.quiz_start_time:
        end_time = datetime.now()
        duration = end_time - st.session_state.quiz_start_time
        minutes = duration.seconds // 60
        seconds = duration.seconds % 60
    else:
        minutes, seconds = 0, 0
    
    # Eredmények megjelenítése
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="summary-box">
            <h3>📊 Pontszám</h3>
            <p><strong>{correct_answers}/{total_questions}</strong></p>
            <p><strong>{percentage:.1f}%</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="summary-box">
            <h3>⏱️ Idő</h3>
            <p><strong>{minutes} perc {seconds} másodperc</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Értékelés
        if percentage >= 90:
            grade = "🏅 Kiváló"
        elif percentage >= 80:
            grade = "🥈 Jó"
        elif percentage >= 70:
            grade = "🥉 Közepes"
        elif percentage >= 60:
            grade = "📝 Megfelelő"
        else:
            grade = "❌ Elégtelen"
        
        st.markdown(f"""
        <div class="summary-box">
            <h3>📈 Értékelés</h3>
            <p><strong>{grade}</strong></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Részletes eredmények
    st.markdown("### 📋 Részletes eredmények")
    
    for i, answer in enumerate(st.session_state.answers):
        is_correct = answer['selected'] == answer['correct']
        status = "✅" if is_correct else "❌"
        
        st.markdown(f"""
        <div class="summary-box">
            <h4>{status} Kérdés {i+1}</h4>
            <p><strong>Kérdés:</strong> {answer['question']}</p>
            <p><strong>Válaszod:</strong> {answer['options'][answer['selected']]}</p>
            <p><strong>Helyes válasz:</strong> {answer['options'][answer['correct']]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Új quiz indítása
    if st.button("🔄 Új quiz indítása", type="primary", use_container_width=True):
        reset_quiz()
        st.rerun()

if __name__ == "__main__":
    # Print the total number of Hungarian music questions
    total_magyar_questions = len(MAGYAR_ZENEKAROK_QUESTIONS) + len(MAGYAR_ZENEKAROK_QUESTIONS_UJ)
    print(f"Összes magyar zenekarok kérdések száma: {total_magyar_questions} (régi: {len(MAGYAR_ZENEKAROK_QUESTIONS)}, új: {len(MAGYAR_ZENEKAROK_QUESTIONS_UJ)})")
    main() 