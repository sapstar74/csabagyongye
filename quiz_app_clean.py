"""
🧠 PDF Alapú Quiz Alkalmazás
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
from topics.nemzetkozi_zenekarok_final_fixed import NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak_reversed import IDIOTA_SZAVAK_QUESTIONS
from custom_audio_player import audio_player_with_download
from youtube_audio_mapping import get_youtube_audio_filename_cached, get_youtube_audio_info

# Page config
st.set_page_config(
    page_title="Quiz App",
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
        color: #ffffff;
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
        background-color: transparent;
        border-radius: 10px;
        margin: 1rem 0;
        color: #ffffff;
    }
    .summary-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Quiz adatok témakörök szerint csoportosítva
QUIZ_DATA_BY_TOPIC = {
    "földrajz": FOLDRAJZ_QUESTIONS,
    "komolyzene": ZENEK_QUESTIONS,
    "magyar_zenekarok": MAGYAR_ZENEKAROK_QUESTIONS,
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
    st.session_state.selected_answer = None

def start_quiz():
    if not st.session_state.selected_topics:
        st.error("Kérlek válassz ki legalább egy témaköröt!")
        return
    
    all_questions = []
    
    # Zenei témakörök külön kezelése
    music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok"]
    other_topics = [t for t in st.session_state.selected_topics if t not in music_topics]
    
    # Zenei témakörök kezelése
    selected_music_topics = [t for t in st.session_state.selected_topics if t in music_topics]
    if selected_music_topics:
        music_total_questions = st.session_state.get('music_total_questions', 10)
        music_auto_distribute = st.session_state.get('music_auto_distribute', True)
        
        if music_auto_distribute:
            # Automatikus elosztás a zenei témakörök között
            questions_per_music_topic = music_total_questions // len(selected_music_topics)
            remaining_music_questions = music_total_questions % len(selected_music_topics)
            
            for i, topic in enumerate(selected_music_topics):
                if topic in QUIZ_DATA_BY_TOPIC:
                    topic_questions = QUIZ_DATA_BY_TOPIC[topic]
                    current_questions = questions_per_music_topic + (1 if i < remaining_music_questions else 0)
                    current_questions = min(current_questions, len(topic_questions))
                    
                    # Véletlenszerű kérdések kiválasztása, de megtartjuk az eredeti indexeket
                    selected_indices = random.sample(range(len(topic_questions)), current_questions)
                    for idx in selected_indices:
                        question = topic_questions[idx].copy()
                        question['original_index'] = idx  # Add original index for audio mapping
                        question['topic'] = topic  # Ensure topic is set
                        all_questions.append(question)
        else:
            # Manuális beállítás minden zenei témakörhöz
            for topic in selected_music_topics:
                if topic in QUIZ_DATA_BY_TOPIC:
                    topic_questions = QUIZ_DATA_BY_TOPIC[topic]
                    num_questions = st.session_state.topic_num_questions.get(topic, min(10, len(topic_questions)))
                    num_questions = min(num_questions, len(topic_questions))
                    
                    # Véletlenszerű kérdések kiválasztása, de megtartjuk az eredeti indexeket
                    selected_indices = random.sample(range(len(topic_questions)), num_questions)
                    for idx in selected_indices:
                        question = topic_questions[idx].copy()
                        question['original_index'] = idx  # Add original index for audio mapping
                        question['topic'] = topic  # Ensure topic is set
                        all_questions.append(question)
    
    # Egyéb témakörök - automatikus vagy manuális elosztás
    if other_topics:
        other_auto_distribute = st.session_state.get('other_auto_distribute', True)
        
        if other_auto_distribute:
            # Automatikus elosztás
            total_questions = st.session_state.get('total_questions', 10)
            questions_per_topic = total_questions // len(other_topics)
            remaining_questions = total_questions % len(other_topics)
            
            for i, topic in enumerate(other_topics):
                if topic in QUIZ_DATA_BY_TOPIC:
                    current_questions = questions_per_topic + (1 if i < remaining_questions else 0)
                    current_questions = min(current_questions, len(QUIZ_DATA_BY_TOPIC[topic]))
                    
                    selected_indices = random.sample(range(len(QUIZ_DATA_BY_TOPIC[topic])), current_questions)
                    for idx in selected_indices:
                        question = QUIZ_DATA_BY_TOPIC[topic][idx].copy()
                        question['original_index'] = idx  # Add original index for audio mapping
                        question['topic'] = topic  # Ensure topic is set
                        all_questions.append(question)
        else:
            # Manuális elosztás - minden témakör külön beállított kérdésszámmal
            for topic in other_topics:
                if topic in QUIZ_DATA_BY_TOPIC:
                    n = st.session_state.topic_num_questions.get(topic, min(10, len(QUIZ_DATA_BY_TOPIC[topic])))
                    selected_indices = random.sample(range(len(QUIZ_DATA_BY_TOPIC[topic])), min(n, len(QUIZ_DATA_BY_TOPIC[topic])))
                    for idx in selected_indices:
                        question = QUIZ_DATA_BY_TOPIC[topic][idx].copy()
                        question['original_index'] = idx  # Add original index for audio mapping
                        question['topic'] = topic  # Ensure topic is set
                        all_questions.append(question)
    
    if not all_questions:
        st.error("Nincsenek kérdések a kiválasztott témakörökben!")
        return
    
    random.shuffle(all_questions)
    st.session_state.quiz_questions = all_questions
    st.session_state.quiz_state = 'quiz'
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_start_time = datetime.now()
    st.session_state.selected_answer = None

def main():
    st.markdown('<h1 class="main-header">🎯 Quiz Alkalmazás</h1>', unsafe_allow_html=True)
    
    # Sidebar settings
    with st.sidebar:
        st.header("⚙️ Beállítások")
        
        # Time limit
        time_limit = st.slider("Időkorlát (perc):", 1, 60, 30)
        
        # Show explanations
        show_explanations = st.checkbox("Magyarázatok megjelenítése", value=True)
        
        # Auto-advance
        auto_advance = st.checkbox("Automatikus továbblépés", value=False)
        
        if st.button("🔄 Újraindítás"):
            reset_quiz()
    
    # Main content
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()
    elif st.session_state.quiz_state == 'results':
        show_results()

def show_topic_selection():
    st.markdown("## 📚 Válassz témaköröket")
    
    # Témakörök csoportosítása
    music_topics = {
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🇭🇺🎵 Magyar Zenekarok", 
        "nemzetkozi_zenekarok": "🌍🎵 Nemzetközi Zenekarok"
    }
    
    other_topics = {
        "földrajz": "🌍 Földrajz",
        "tudósok": "🔬 Tudósok", 
        "mitológia": "🏛️ Mitológia", 
        "háborúk": "⚔️ Háborúk",
        "magyar_királyok": "👑 Magyar Királyok",
        "állatok": "🦁 Állatok",
        "drámák": "🎭 Drámák",
        "sport_logók": "🏈 Sport Logók",
        "zászlók": "🏳️ Zászlók",
        "idióta_szavak": "🥋 Fekete Öves"
    }
    
    if 'topic_num_questions' not in st.session_state:
        st.session_state.topic_num_questions = {k: min(10, len(QUIZ_DATA_BY_TOPIC[k])) for k in QUIZ_DATA_BY_TOPIC}
    
    # Zenei témakörök
    st.markdown("### 🎵 Zenei Témakörök")
    
    music_col1, music_col2, music_col3 = st.columns(3)
    
    for i, (topic, display_name) in enumerate(music_topics.items()):
        col = music_col1 if i == 0 else music_col2 if i == 1 else music_col3
        with col:
            is_selected = topic in st.session_state.selected_topics
            if st.button(
                f"{display_name} ({len(QUIZ_DATA_BY_TOPIC[topic])} kérdés)",
                key=f"music_topic_{topic}",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                if topic in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic)
                else:
                    st.session_state.selected_topics.append(topic)
                st.rerun()
    
    # Zenei kérdésszám beállítása - csak ha vannak kiválasztott zenei témakörök
    music_selected = [topic for topic in music_topics.keys() if topic in st.session_state.selected_topics]
    if music_selected:
        st.markdown("### 🎵 Zenei kérdésszám beállítása")
        total_music_questions = sum(len(QUIZ_DATA_BY_TOPIC[topic]) for topic in music_topics.keys())
        
        music_questions = st.slider(
            "Zenei kérdések száma:",
            min_value=1,
            max_value=total_music_questions,
            value=st.session_state.get('music_total_questions', 10),
            key="music_total_questions_slider"
        )
        st.session_state.music_total_questions = music_questions
        
        # Automatikus elosztás a zenei témakörök között
        music_auto_distribute = st.checkbox(
            "Automatikus elosztás zenei témakörök között",
            value=st.session_state.get('music_auto_distribute', True),
            key="music_auto_distribute"
        )
        
        if music_auto_distribute and music_selected:
            questions_per_music_topic = music_questions // len(music_selected)
            remaining_music_questions = music_questions % len(music_selected)
            st.info(f"📊 Zenei kérdések elosztása: {questions_per_music_topic} kérdés/témakör + {remaining_music_questions} extra")
        
        # Manuális beállítás zenei témaköröknél (ha nincs automatikus elosztás)
        if not music_auto_distribute and music_selected:
            st.markdown("**Zenei kérdések száma témakörönként:**")
            for topic in music_selected:
                display_name = music_topics[topic]
                max_q = len(QUIZ_DATA_BY_TOPIC[topic])
                st.session_state.topic_num_questions[topic] = st.slider(
                    f"{display_name}:",
                    min_value=1,
                    max_value=max_q,
                    value=st.session_state.topic_num_questions.get(topic, min(10, max_q)),
                    key=f"music_slider_{topic}"
                )
    
    st.markdown("---")
    
    # Egyéb témakörök
    st.markdown("### 📚 Egyéb Témakörök")
    col1, col2 = st.columns(2)
    
    for i, (topic, display_name) in enumerate(other_topics.items()):
        is_selected = topic in st.session_state.selected_topics
        col = col1 if i % 2 == 0 else col2
        with col:
            if st.button(
                f"{display_name} ({len(QUIZ_DATA_BY_TOPIC[topic])} kérdés)",
                key=f"topic_{topic}",
                type="primary" if is_selected else "secondary",
                use_container_width=True
            ):
                if topic in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic)
                else:
                    st.session_state.selected_topics.append(topic)
                st.rerun()
    
    # Egyéb kérdésszám beállítása - csak ha vannak kiválasztott egyéb témakörök
    selected_other_topics = [topic for topic in st.session_state.selected_topics if topic in other_topics]
    if selected_other_topics:
        st.markdown("### 📚 Egyéb kérdésszám beállítása")
        
        # Automatikus elosztás beállítása
        other_auto_distribute = st.checkbox(
            "Automatikus elosztás egyéb témakörök között",
            value=st.session_state.get('other_auto_distribute', True),
            key="other_auto_distribute"
        )
        
        if other_auto_distribute:
            # Automatikus elosztás esetén összes kérdésszám beállítása
            total_other_questions = sum(len(QUIZ_DATA_BY_TOPIC[topic]) for topic in other_topics.keys())
            max_questions = sum(len(QUIZ_DATA_BY_TOPIC[topic]) for topic in selected_other_topics) if selected_other_topics else total_other_questions
            
            total_questions = st.slider(
                "Összes kérdés száma (egyéb témakörök):",
                min_value=1,
                max_value=max_questions,
                value=st.session_state.get('total_questions', 10),
                key="total_questions_slider"
            )
            st.session_state.total_questions = total_questions
            
            if selected_other_topics:
                questions_per_topic = total_questions // len(selected_other_topics)
                remaining_questions = total_questions % len(selected_other_topics)
                st.info(f"📊 Egyéb kérdések elosztása: {questions_per_topic} kérdés/témakör + {remaining_questions} extra")
                
                # Megjelenítjük, hogy hány kérdés lesz minden témakörből
                for topic in selected_other_topics:
                    display_name = other_topics[topic]
                    topic_index = selected_other_topics.index(topic)
                    current_questions = questions_per_topic + (1 if topic_index < remaining_questions else 0)
                    current_questions = min(current_questions, len(QUIZ_DATA_BY_TOPIC[topic]))
                    st.info(f"📊 {display_name}: {current_questions} kérdés")
        else:
            # Manuális beállítás esetén minden témakör külön
            st.markdown("**Kérdések száma témakörönként:**")
            
            total_manual_questions = 0
            for topic in selected_other_topics:
                display_name = other_topics[topic]
                max_q = len(QUIZ_DATA_BY_TOPIC[topic])
                
                st.session_state.topic_num_questions[topic] = st.slider(
                    f"{display_name}:",
                    min_value=1,
                    max_value=max_q,
                    value=st.session_state.topic_num_questions.get(topic, min(10, max_q)),
                    key=f"slider_{topic}"
                )
                total_manual_questions += st.session_state.topic_num_questions[topic]
            
            # Összes kérdésszám megjelenítése
            st.markdown(f"**📊 Összes kérdésszám (egyéb témakörök): {total_manual_questions}**")
            st.session_state.total_questions = total_manual_questions
    
    # Összes kérdésszám megjelenítése
    if st.session_state.selected_topics:
        st.markdown("---")
        
        # Kiszámítjuk az összes kérdésszámot
        total_selected_questions = 0
        
        # Zenei kérdések
        if music_selected:
            if st.session_state.get('music_auto_distribute', True):
                total_selected_questions += st.session_state.get('music_total_questions', 10)
            else:
                for topic in music_selected:
                    total_selected_questions += st.session_state.topic_num_questions.get(topic, 10)
        
        # Egyéb kérdések
        if selected_other_topics:
            if st.session_state.get('other_auto_distribute', True):
                total_selected_questions += st.session_state.get('total_questions', 10)
            else:
                for topic in selected_other_topics:
                    total_selected_questions += st.session_state.topic_num_questions.get(topic, 10)
        
        st.markdown(f"### 📊 **Összes kérdésszám: {total_selected_questions}**")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Quiz indítása", type="primary", use_container_width=True):
                start_quiz()
                st.rerun()

def show_quiz():
    if not st.session_state.quiz_questions:
        st.error("Nincsenek kérdések!")
        return
    
    current_q = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
    st.progress(progress)
    
    # Question counter
    current_question_num = st.session_state.current_question + 1
    total_questions = len(st.session_state.quiz_questions)
    st.markdown(f"**Kérdés {current_question_num} / {total_questions}**")
    
    # Navigation buttons with dynamic labels
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        prev_disabled = st.session_state.current_question == 0
        prev_label = f"⬅️ Előző ({current_question_num - 1}/{total_questions})" if not prev_disabled else "⬅️ Előző"
        if st.button(prev_label, disabled=prev_disabled):
            if st.session_state.current_question > 0:
                st.session_state.current_question -= 1
                st.session_state.selected_answer = None
                st.rerun()
    
    with col2:
        next_disabled = st.session_state.current_question == total_questions - 1
        next_label = f"➡️ Következő ({current_question_num + 1}/{total_questions})" if not next_disabled else "➡️ Következő"
        if st.button(next_label, disabled=next_disabled):
            if st.session_state.current_question < total_questions - 1:
                st.session_state.current_question += 1
                st.session_state.selected_answer = None
                st.rerun()
    
    with col3:
        if st.button("🏠 Vissza a menübe"):
            reset_quiz()
            st.rerun()
    
    with col4:
        if st.button("🏁 Quiz befejezése"):
            st.session_state.quiz_state = 'results'
            st.rerun()
    
    # Score display
    correct_answers = st.session_state.score
    incorrect_answers = st.session_state.current_question - correct_answers
    st.markdown(f'<div class="score-display">Pontszám: {correct_answers} / {st.session_state.current_question} (✅ {correct_answers} helyes, ❌ {incorrect_answers} hibás)</div>', 
                unsafe_allow_html=True)
    
    # Question
    st.markdown(f'<div class="question-text">{current_q["question"]}</div>', unsafe_allow_html=True)
    
    # Logo image if available (for sport logos and flags)
    if "logo_path" in current_q and current_q["logo_path"]:
        try:
            # Adjust path to be relative to the quiz app directory
            logo_path = current_q["logo_path"]
            
            # Handle different path formats
            if logo_path.startswith("data/flags/"):
                # Flag images - go up one level and into world_flags_project
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                logo_path = os.path.join(parent_dir, "world_flags_project", logo_path)
            elif logo_path.startswith("../"):
                # Get the current working directory and go up one level
                current_dir = os.path.dirname(os.path.abspath(__file__))
                parent_dir = os.path.dirname(current_dir)
                logo_path = os.path.join(parent_dir, logo_path[3:])
            
            # Check if file exists
            if os.path.exists(logo_path):
                # Center the logo using columns
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    st.image(logo_path, width=400, caption="Zászló")
            else:
                st.warning(f"⚠️ Zászló kép nem található: {logo_path}")
        except Exception as e:
            st.warning(f"⚠️ Hiba a zászló betöltésekor: {e}")
    
    # YouTube Audio if available - for music questions
    if "spotify_embed" in current_q and current_q["spotify_embed"]:
        # Get topic from current question
        topic = current_q.get("topic", "")
        
        # Use original index for audio mapping (if available)
        question_index = current_q.get("original_index", st.session_state.current_question)
        
        # Get YouTube audio filename using original question index and topic
        audio_filename = get_youtube_audio_filename_cached(question_index, topic)
        
        if audio_filename:
            # Get audio info for display
            audio_info = get_youtube_audio_info(audio_filename)
            
            # Display audio player with artist info
            st.markdown("### 🎵 Hallgasd meg a zenét:")
            if audio_info:
                st.info(f"🎤 **{audio_info['artist']}** - {audio_info['title']}")
            
            # Use custom audio player with the corresponding audio file
            audio_player_with_download(audio_filename)
        else:
            st.warning(f"⚠️ YouTube audio fájl nem található ehhez a kérdéshez. (Topic: {topic}, Original Index: {question_index})")

    # Check if this is a text input question (Fekete Öves / idióta szavak)
    if current_q.get("question_type") == "text_input":
        # Text input for Fekete Öves (text_input questions)
        user_answer = st.text_input(
            "Írd be a válaszod:",
            key=f"text_input_{st.session_state.current_question}",
            placeholder="Írd ide a válaszod..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⏭️ Kihagyás", key=f"skip_{st.session_state.current_question}"):
                # Skip this question
                st.session_state.answers.append({
                    'question': current_q["question"],
                    'user_answer': "Kihagyva",
                    'correct_answer': current_q["correct_answer"],
                    'is_correct': False,
                    'explanation': current_q.get("explanation", "")
                })
                
                if st.session_state.current_question + 1 < len(st.session_state.quiz_questions):
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.quiz_state = 'results'
                    st.rerun()
        
        with col2:
            if st.button("✅ Válasz beküldése", key=f"submit_{st.session_state.current_question}"):
                if user_answer.strip():
                    # Simple text similarity check (case insensitive)
                    user_lower = user_answer.lower().strip()
                    correct_lower = current_q["correct_answer"].lower().strip()
                    
                    # Check if the answer contains key words from the correct answer
                    correct_words = correct_lower.split()
                    user_words = user_lower.split()
                    
                    # Count matching words
                    matching_words = sum(1 for word in correct_words if any(user_word in word or word in user_word for user_word in user_words))
                    similarity = matching_words / len(correct_words) if correct_words else 0
                    
                    is_correct = similarity >= 0.3  # 30% similarity threshold
                    
                    if is_correct:
                        st.session_state.score += 1
                    
                    st.session_state.answers.append({
                        'question': current_q["question"],
                        'user_answer': user_answer,
                        'correct_answer': current_q["correct_answer"],
                        'is_correct': is_correct,
                        'explanation': current_q.get("explanation", "")
                    })
                    
                    if st.session_state.current_question + 1 < len(st.session_state.quiz_questions):
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        st.session_state.quiz_state = 'results'
                        st.rerun()
                else:
                    st.warning("Kérlek írj be egy választ!")
    
    else:
        # Multiple choice questions (existing logic)
        # Randomize options
        if 'current_options' not in st.session_state or st.session_state.current_question != st.session_state.get('last_question_index', -1):
            options = list(enumerate(current_q["options"]))
            random.shuffle(options)
            st.session_state.current_options = options
            st.session_state.last_question_index = st.session_state.current_question
            # Create mapping from new index to original index
            st.session_state.correct_answer_mapping = {new_idx: original_idx for new_idx, (original_idx, _) in enumerate(options)}
            # Create reverse mapping from original index to new index
            st.session_state.original_to_new_mapping = {original_idx: new_idx for new_idx, (original_idx, _) in enumerate(options)}
            # Reset selected answer for new question
            st.session_state.selected_answer = None
        
        # Options - direct answer selection
        for i, (original_idx, option_text) in enumerate(st.session_state.current_options):
            if st.button(
                option_text,
                key=f"option_{i}",
                use_container_width=True,
                type="primary" if st.session_state.selected_answer == i else "secondary"
            ):
                # Check answer using the reverse mapping
                # Get the correct answer index from the question data
                correct_original_idx = current_q["correct"]
                correct_new_idx = st.session_state.original_to_new_mapping[correct_original_idx]
                is_correct = i == correct_new_idx
                if is_correct:
                    st.session_state.score += 1
                
                # Store answer with original indices and current options
                st.session_state.answers.append({
                    'question': current_q["question"],
                    'user_answer': original_idx,
                    'user_selected_option': option_text,  # Store the actual selected option text
                    'correct_answer': correct_original_idx,
                    'is_correct': is_correct,
                    'explanation': current_q.get("explanation", ""),
                    'current_options': [opt[1] for opt in st.session_state.current_options],
                    'correct_new_idx': correct_new_idx
                })
                
                # Next question or finish
                if st.session_state.current_question + 1 < len(st.session_state.quiz_questions):
                    st.session_state.current_question += 1
                    st.session_state.selected_answer = None
                    st.rerun()
                else:
                    st.session_state.quiz_state = 'results'
                    st.rerun()

def show_results():
    st.markdown("## 🎉 Quiz befejezve!")
    
    total_questions = len(st.session_state.quiz_questions)
    correct_answers = st.session_state.score
    percentage = (correct_answers / total_questions) * 100
    
    # Final score
    st.markdown(f'<div class="score-display">Végső pontszám: {correct_answers} / {total_questions} ({percentage:.1f}%)</div>', 
                unsafe_allow_html=True)
    
    # Performance message
    if percentage >= 90:
        st.success("🏆 Kiváló teljesítmény!")
    elif percentage >= 80:
        st.success("🎯 Nagyon jó!")
    elif percentage >= 70:
        st.info("👍 Jó teljesítmény!")
    elif percentage >= 60:
        st.warning("⚠️ Átlagos teljesítmény")
    else:
        st.error("📚 Még gyakorolni kell!")
    
    # Detailed results
    st.markdown("## 📊 Részletes eredmények")
    
    for i, answer in enumerate(st.session_state.answers):
        # Add emoji to show if answer was correct
        status_emoji = "✅" if answer['is_correct'] else "❌"
        with st.expander(f"{status_emoji} Kérdés {i+1}: {answer['question'][:50]}..."):
            st.write(f"**Kérdés:** {answer['question']}")
            
            # Check if this was a text input question
            if isinstance(answer['user_answer'], str) and answer['user_answer'] != "Kihagyva":
                # Text input question
                st.write(f"**Te válaszod:** {answer['user_answer']}")
                st.write(f"**Helyes válasz:** {answer['correct_answer']}")
            elif answer['user_answer'] == "Kihagyva":
                # Skipped question
                st.write("**Te válaszod:** Kihagyva")
                st.write(f"**Helyes válasz:** {answer['correct_answer']}")
            else:
                # Multiple choice question - use stored current options
                if 'current_options' in answer and 'correct_new_idx' in answer and 'user_selected_option' in answer:
                    # Use the stored current options (shuffled order)
                    current_options = answer['current_options']
                    correct_new_idx = answer['correct_new_idx']
                    user_selected_option = answer['user_selected_option']
                    
                    # Show user's selected answer
                    st.write(f"**Te válaszod:** {user_selected_option}")
                    
                    # Show all options with correct/incorrect marks
                    for j, option in enumerate(current_options):
                        if j == correct_new_idx and option == user_selected_option:
                            st.write(f"✅ **{option}** (helyes válasz)")
                        elif j == correct_new_idx:
                            st.write(f"✅ **{option}** (helyes válasz)")
                        elif option == user_selected_option:
                            st.write(f"❌ **{option}** (te választottad)")
                        else:
                            st.write(f"• {option}")
                else:
                    # Fallback if stored options not available
                    st.write(f"**Te válaszod:** {answer['user_answer']}")
                    st.write(f"**Helyes válasz:** {answer['correct_answer']}")
            
            if answer.get("explanation"):
                st.info(f"**Magyarázat:** {answer['explanation']}")
    
    # Restart button
    if st.button("🔄 Új quiz", type="primary"):
        reset_quiz()
        st.rerun()

if __name__ == "__main__":
    main() 