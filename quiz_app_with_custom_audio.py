#!/usr/bin/env python3
"""
🧠 PDF Alapú Quiz Alkalmazás - Saját Audio Lejátszóval
10 kérdéses feleletválasztós teszt a feltöltött PDF tartalom alapján
"""

import streamlit as st
import random
import time
from datetime import datetime
import os
from pathlib import Path
from topics.foldrajz import FOLDRAJZ_QUESTIONS
from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS as ZENEK_QUESTIONS
from topics.tudosok import TUDOSOK_QUESTIONS
from topics.mitologia_all_questions import MITOLOGIA_QUESTIONS_ALL
from topics.haboru_all_questions import HABORU_QUESTIONS_ALL
from topics.kiralyok import KIRALYOK_QUESTIONS
from topics.allatok_balanced import ALLATOK_QUESTIONS_BALANCED
from topics.dramak import DRAMAK_QUESTIONS
from topics.sport_logok import SPORT_LOGOK_QUESTIONS
from topics.zaszlok_all_questions import ZASZLOK_QUESTIONS_ALL
from topics.magyar_zenekarok import MAGYAR_ZENEKAROK_QUESTIONS
from topics.nemzetkozi_zenekarok import NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak_reversed import IDIOTA_SZAVAK_QUESTIONS
from custom_audio_player import show_custom_audio_player, replace_spotify_with_custom_player

# Page config
st.set_page_config(
    page_title="Quiz App - Saját Audio Lejátszóval",
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
    .audio-player-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
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
    st.session_state.use_custom_audio = True  # Alapértelmezetten saját audio lejátszó

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
        st.error("Kérlek válassz ki legalább egy témakört!")
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
                    
                    # Véletlenszerű kérdések kiválasztása
                    selected_questions = random.sample(topic_questions, current_questions)
                    
                    # Saját audio lejátszó alkalmazása, ha be van kapcsolva
                    if st.session_state.use_custom_audio:
                        selected_questions = [replace_spotify_with_custom_player(q) for q in selected_questions]
                    
                    all_questions.extend(selected_questions)
        else:
            # Manuális beállítás minden zenei témakörhöz
            for topic in selected_music_topics:
                if topic in QUIZ_DATA_BY_TOPIC:
                    topic_questions = QUIZ_DATA_BY_TOPIC[topic]
                    num_questions = st.session_state.topic_num_questions.get(topic, min(10, len(topic_questions)))
                    num_questions = min(num_questions, len(topic_questions))
                    
                    selected_questions = random.sample(topic_questions, num_questions)
                    
                    # Saját audio lejátszó alkalmazása
                    if st.session_state.use_custom_audio:
                        selected_questions = [replace_spotify_with_custom_player(q) for q in selected_questions]
                    
                    all_questions.extend(selected_questions)
    
    # Egyéb témakörök kezelése
    for topic in other_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            num_questions = st.session_state.topic_num_questions.get(topic, min(10, len(topic_questions)))
            num_questions = min(num_questions, len(topic_questions))
            
            selected_questions = random.sample(topic_questions, num_questions)
            all_questions.extend(selected_questions)
    
    # Véletlenszerű sorrendbe rendezés
    random.shuffle(all_questions)
    
    st.session_state.quiz_questions = all_questions
    st.session_state.quiz_state = 'quiz'
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_start_time = datetime.now()

def show_topic_selection():
    st.markdown('<div class="main-header">🎯 Quiz Alkalmazás</div>', unsafe_allow_html=True)
    
    # Audio lejátszó beállítások
    st.sidebar.markdown("### 🎵 Audio Lejátszó Beállítások")
    st.session_state.use_custom_audio = st.sidebar.checkbox(
        "Saját Audio Lejátszó Használata", 
        value=st.session_state.use_custom_audio,
        help="Ha be van kapcsolva, saját audio lejátszót használ a Spotify embed helyett"
    )
    
    if st.session_state.use_custom_audio:
        st.sidebar.success("✅ Saját audio lejátszó aktív")
        st.sidebar.info("A zenei kérdésekben saját audio lejátszó jelenik meg letöltési lehetőséggel.")
    else:
        st.sidebar.warning("⚠️ Spotify embed aktív")
        st.sidebar.info("A zenei kérdésekben Spotify embed jelenik meg.")
    
    st.markdown("### 📚 Válassz témaköröket:")
    
    # Témakörök megjelenítése
    col1, col2, col3 = st.columns(3)
    
    topics_list = list(QUIZ_DATA_BY_TOPIC.keys())
    topics_per_col = len(topics_list) // 3 + 1
    
    for i, topic in enumerate(topics_list):
        col = col1 if i < topics_per_col else (col2 if i < 2 * topics_per_col else col3)
        
        with col:
            if st.button(
                f"📖 {topic.title()} ({len(QUIZ_DATA_BY_TOPIC[topic])} kérdés)",
                key=f"topic_{topic}",
                help=f"Kattints a {topic} témakör kiválasztásához"
            ):
                if topic in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic)
                else:
                    st.session_state.selected_topics.append(topic)
    
    # Kiválasztott témakörök megjelenítése
    if st.session_state.selected_topics:
        st.markdown("### ✅ Kiválasztott témakörök:")
        for topic in st.session_state.selected_topics:
            st.success(f"📖 {topic.title()} ({len(QUIZ_DATA_BY_TOPIC[topic])} kérdés)")
        
        # Zenei témakörök speciális beállításai
        music_topics = [t for t in st.session_state.selected_topics if t in ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok"]]
        
        if music_topics:
            st.markdown("### 🎵 Zenei Témakörök Beállításai")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.session_state.music_auto_distribute = st.checkbox(
                    "Automatikus elosztás",
                    value=st.session_state.get('music_auto_distribute', True),
                    help="Automatikusan elosztja a kérdéseket a zenei témakörök között"
                )
            
            with col2:
                if st.session_state.music_auto_distribute:
                    st.session_state.music_total_questions = st.number_input(
                        "Összes zenei kérdés száma",
                        min_value=1,
                        max_value=30,
                        value=st.session_state.get('music_total_questions', 10)
                    )
                else:
                    st.markdown("**Manuális beállítás:**")
                    for topic in music_topics:
                        max_questions = len(QUIZ_DATA_BY_TOPIC[topic])
                        st.session_state.topic_num_questions[topic] = st.number_input(
                            f"{topic.title()} kérdések száma",
                            min_value=1,
                            max_value=max_questions,
                            value=min(10, max_questions)
                        )
        
        # Kvíz indítása
        if st.button("🚀 Kvíz Indítása", type="primary", use_container_width=True):
            start_quiz()
            st.rerun()
    else:
        st.info("👆 Válassz ki legalább egy témakört a kvíz indításához!")

def show_quiz():
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        show_results()
        return
    
    current_q = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
    st.progress(progress)
    st.markdown(f"**Kérdés {st.session_state.current_question + 1} / {len(st.session_state.quiz_questions)}**")
    
    # Kérdés megjelenítése
    st.markdown(f"<div class='question-text'>{current_q['question']}</div>", unsafe_allow_html=True)
    
    # Logó megjelenítése, ha van
    if 'logo_path' in current_q and current_q['logo_path']:
        logo_path = Path(current_q['logo_path'])
        if logo_path.exists():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image(str(logo_path), width=300, caption="")
        else:
            st.warning(f"⚠️ Logó nem található: {current_q['logo_path']}")
    
    # Audio lejátszó megjelenítése
    if st.session_state.use_custom_audio:
        # Saját audio lejátszó
        show_custom_audio_player(current_q)
    else:
        # Spotify embed
        if "spotify_embed" in current_q and current_q["spotify_embed"]:
            st.markdown("### 🎵 Spotify Lejátszó")
            st.components.v1.iframe(current_q["spotify_embed"], height=80)
    
    # Válaszlehetőségek
    selected_answer = st.radio(
        "Válassz egyet:",
        options=current_q['options'],
        key=f"question_{st.session_state.current_question}"
    )
    
    # Válasz beküldése
    if st.button("✅ Válasz Beküldése", type="primary"):
        answer_index = current_q['options'].index(selected_answer)
        st.session_state.answers.append(answer_index)
        
        if answer_index == current_q['correct']:
            st.session_state.score += 1
        
        st.session_state.current_question += 1
        st.rerun()

def show_results():
    st.markdown('<div class="main-header">🏆 Kvíz Eredmények</div>', unsafe_allow_html=True)
    
    total_questions = len(st.session_state.quiz_questions)
    correct_answers = st.session_state.score
    percentage = (correct_answers / total_questions) * 100
    
    # Eredmény megjelenítése
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Helyes válaszok", correct_answers)
    
    with col2:
        st.metric("Helytelen válaszok", total_questions - correct_answers)
    
    with col3:
        st.metric("Sikeresség", f"{percentage:.1f}%")
    
    # Részletes eredmények
    st.markdown("### 📊 Részletes Eredmények")
    
    for i, (question, answer) in enumerate(zip(st.session_state.quiz_questions, st.session_state.answers)):
        is_correct = answer == question['correct']
        
        if is_correct:
            st.success(f"✅ Kérdés {i+1}: Helyes")
        else:
            correct_answer = question['options'][question['correct']]
            st.error(f"❌ Kérdés {i+1}: Helytelen (helyes: {correct_answer})")
        
        if 'explanation' in question:
            st.info(f"💡 {question['explanation']}")
    
    # Új kvíz indítása
    if st.button("🔄 Új Kvíz", type="primary"):
        reset_quiz()
        st.rerun()

def main():
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()

if __name__ == "__main__":
    main() 