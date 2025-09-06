"""
🧠 PDF Alapú Quiz Alkalmazás - Leíró Audio Fájlnevekkel
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
from topics.magyar_zenekarok import MAGYAR_ZENEKAROK_QUESTIONS
from topics.nemzetkozi_zenekarok import NEMZETKOZI_ZENEKAROK_QUESTIONS
from topics.idiota_szavak_reversed import IDIOTA_SZAVAK_QUESTIONS
from custom_audio_player import audio_player_with_download
from audio_mapping_descriptive import get_audio_filename, get_audio_info

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
    .audio-info {
        background-color: #e3f2fd;
        border-radius: 8px;
        padding: 0.5rem;
        margin: 0.5rem 0;
        font-size: 0.9rem;
        color: #1976d2;
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
                    
                    # Véletlenszerű kérdések kiválasztása
                    selected_questions = random.sample(topic_questions, current_questions)
                    all_questions.extend(selected_questions)
        else:
            # Manuális beállítás minden zenei témakörhöz
            for topic in selected_music_topics:
                if topic in QUIZ_DATA_BY_TOPIC:
                    topic_questions = QUIZ_DATA_BY_TOPIC[topic]
                    topic_question_count = st.session_state.get(f'{topic}_questions', 5)
                    topic_question_count = min(topic_question_count, len(topic_questions))
                    
                    # Véletlenszerű kérdések kiválasztása
                    selected_questions = random.sample(topic_questions, topic_question_count)
                    all_questions.extend(selected_questions)
    
    # Egyéb témakörök kezelése
    for topic in other_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            topic_question_count = st.session_state.get(f'{topic}_questions', 5)
            topic_question_count = min(topic_question_count, len(topic_questions))
            
            # Véletlenszerű kérdések kiválasztása
            selected_questions = random.sample(topic_questions, topic_question_count)
            all_questions.extend(selected_questions)
    
    if not all_questions:
        st.error("Nincs elérhető kérdés a kiválasztott témakörökből!")
        return
    
    # Véletlenszerű sorrendbe rendezés
    random.shuffle(all_questions)
    
    st.session_state.quiz_questions = all_questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_state = 'quiz'
    st.session_state.quiz_start_time = datetime.now()

def main():
    st.markdown('<h1 class="main-header">🎯 Quiz Alkalmazás</h1>', unsafe_allow_html=True)
    
    if st.session_state.quiz_state == 'selection':
        show_topic_selection()
    elif st.session_state.quiz_state == 'quiz':
        show_quiz()
    elif st.session_state.quiz_state == 'results':
        show_results()

def show_topic_selection():
    st.markdown("### 📚 Témakörök kiválasztása")
    
    # Témakörök megjelenítése
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🏛️ Történelmi témakörök**")
        if st.button("🏛️ Háborúk", key="háborúk"):
            if "háborúk" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("háborúk")
            st.rerun()
        
        if st.button("👑 Magyar királyok", key="magyar_királyok"):
            if "magyar_királyok" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("magyar_királyok")
            st.rerun()
        
        if st.button("🧠 Tudósok", key="tudósok"):
            if "tudósok" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("tudósok")
            st.rerun()
        
        if st.button("🏛️ Mitológia", key="mitológia"):
            if "mitológia" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("mitológia")
            st.rerun()
    
    with col2:
        st.markdown("**🎵 Zenei témakörök**")
        if st.button("🎼 Komolyzene", key="komolyzene"):
            if "komolyzene" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("komolyzene")
            st.rerun()
        
        if st.button("🇭🇺 Magyar zenekarok", key="magyar_zenekarok"):
            if "magyar_zenekarok" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("magyar_zenekarok")
            st.rerun()
        
        if st.button("🌍 Nemzetközi zenekarok", key="nemzetkozi_zenekarok"):
            if "nemzetkozi_zenekarok" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("nemzetkozi_zenekarok")
            st.rerun()
    
    with col3:
        st.markdown("**🎯 Egyéb témakörök**")
        if st.button("🗺️ Földrajz", key="földrajz"):
            if "földrajz" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("földrajz")
            st.rerun()
        
        if st.button("🐾 Állatok", key="állatok"):
            if "állatok" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("állatok")
            st.rerun()
        
        if st.button("🎭 Drámák", key="drámák"):
            if "drámák" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("drámák")
            st.rerun()
        
        if st.button("🏆 Sport logók", key="sport_logók"):
            if "sport_logók" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("sport_logók")
            st.rerun()
        
        if st.button("🏁 Zászlók", key="zászlók"):
            if "zászlók" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("zászlók")
            st.rerun()
        
        if st.button("🤪 Idióta szavak", key="idióta_szavak"):
            if "idióta_szavak" not in st.session_state.selected_topics:
                st.session_state.selected_topics.append("idióta_szavak")
            st.rerun()
    
    # Kiválasztott témakörök megjelenítése
    if st.session_state.selected_topics:
        st.markdown("### ✅ Kiválasztott témakörök:")
        for topic in st.session_state.selected_topics:
            st.write(f"• {topic}")
        
        # Kérdések számának beállítása
        st.markdown("### ⚙️ Beállítások")
        
        # Zenei témakörök külön kezelése
        music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok"]
        selected_music_topics = [t for t in st.session_state.selected_topics if t in music_topics]
        
        if selected_music_topics:
            st.markdown("**🎵 Zenei kérdések beállítása**")
            music_auto_distribute = st.checkbox("Automatikus elosztás a zenei témakörök között", value=True, key="music_auto_distribute")
            
            if music_auto_distribute:
                music_total_questions = st.slider("Összes zenei kérdés száma", 1, 30, 10, key="music_total_questions")
            else:
                for topic in selected_music_topics:
                    topic_questions = QUIZ_DATA_BY_TOPIC.get(topic, [])
                    max_questions = len(topic_questions)
                    if max_questions > 0:
                        st.slider(f"{topic} kérdések száma", 1, max_questions, min(5, max_questions), key=f"{topic}_questions")
        
        # Egyéb témakörök beállítása
        other_topics = [t for t in st.session_state.selected_topics if t not in music_topics]
        if other_topics:
            st.markdown("**📚 Egyéb kérdések beállítása**")
            for topic in other_topics:
                topic_questions = QUIZ_DATA_BY_TOPIC.get(topic, [])
                max_questions = len(topic_questions)
                if max_questions > 0:
                    st.slider(f"{topic} kérdések száma", 1, max_questions, min(5, max_questions), key=f"{topic}_questions")
        
        # Quiz indítása
        if st.button("🚀 Quiz indítása", type="primary"):
            start_quiz()

def show_quiz():
    if st.session_state.current_question >= len(st.session_state.quiz_questions):
        st.session_state.quiz_state = 'results'
        st.rerun()
        return
    
    current_q = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Progress bar
    progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
    st.progress(progress)
    
    # Kérdés száma és pontszám
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"### 📝 Kérdés {st.session_state.current_question + 1}/{len(st.session_state.quiz_questions)}")
    with col2:
        st.markdown(f"### 🎯 Pontszám: {st.session_state.score}")
    with col3:
        if st.session_state.quiz_start_time:
            elapsed = datetime.now() - st.session_state.quiz_start_time
            st.markdown(f"### ⏱️ Idő: {elapsed.seconds // 60}:{elapsed.seconds % 60:02d}")
    
    # Kérdés megjelenítése
    st.markdown(f'<div class="quiz-container"><div class="question-text">{current_q["question"]}</div></div>', unsafe_allow_html=True)
    
    # Audio lejátszás (ha van)
    if "spotify_embed" in current_q and current_q["spotify_embed"]:
        audio_filename = get_audio_filename(current_q["spotify_embed"], st.session_state.current_question)
        audio_info = get_audio_info(current_q["spotify_embed"])
        
        if audio_filename:
            audio_path = f"audio_files/{audio_filename}"
            if os.path.exists(audio_path):
                # Audio információ megjelenítése
                if audio_info:
                    st.markdown(f"""
                    <div class="audio-info">
                        🎵 <strong>{audio_info['artist']}</strong> - {audio_info['title']}
                    </div>
                    """, unsafe_allow_html=True)
                
                # Audio lejátszó
                audio_player_with_download(audio_path)
            else:
                st.warning(f"Audio fájl nem található: {audio_filename}")
    
    # Válaszlehetőségek
    if "options" in current_q:
        options = current_q["options"]
        random.shuffle(options)
        
        selected_answer = None
        for i, option in enumerate(options):
            if st.button(option, key=f"option_{i}", use_container_width=True):
                selected_answer = option
                break
        
        if selected_answer:
            st.session_state.selected_answer = selected_answer
            
            # Válasz ellenőrzése
            correct_answer = current_q["correct_answer"]
            is_correct = selected_answer == correct_answer
            
            if is_correct:
                st.session_state.score += 1
                st.success(f"✅ Helyes! A válasz: {correct_answer}")
            else:
                st.error(f"❌ Helytelen! A helyes válasz: {correct_answer}")
            
            # Válasz mentése
            st.session_state.answers.append({
                "question": current_q["question"],
                "user_answer": selected_answer,
                "correct_answer": correct_answer,
                "is_correct": is_correct
            })
            
            # Következő kérdés
            time.sleep(2)
            st.session_state.current_question += 1
            st.session_state.selected_answer = None
            st.rerun()

def show_results():
    st.markdown('<h1 class="main-header">🏆 Quiz Eredmények</h1>', unsafe_allow_html=True)
    
    # Végső pontszám
    total_questions = len(st.session_state.quiz_questions)
    score_percentage = (st.session_state.score / total_questions) * 100
    
    st.markdown(f"""
    <div class="summary-box">
        <h2>📊 Végső Eredmény</h2>
        <p><strong>Pontszám:</strong> {st.session_state.score}/{total_questions}</p>
        <p><strong>Százalék:</strong> {score_percentage:.1f}%</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Idő
    if st.session_state.quiz_start_time:
        total_time = datetime.now() - st.session_state.quiz_start_time
        st.markdown(f"<p><strong>⏱️ Teljes idő:</strong> {total_time.seconds // 60} perc {total_time.seconds % 60} másodperc</p>", unsafe_allow_html=True)
    
    # Részletes eredmények
    st.markdown("### 📝 Részletes eredmények")
    for i, answer in enumerate(st.session_state.answers):
        status = "✅" if answer["is_correct"] else "❌"
        st.markdown(f"""
        <div class="summary-box">
            <p><strong>{i+1}. kérdés:</strong> {answer["question"]}</p>
            <p><strong>Te válaszod:</strong> {answer["user_answer"]}</p>
            <p><strong>Helyes válasz:</strong> {answer["correct_answer"]}</p>
            <p><strong>Eredmény:</strong> {status}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Új quiz indítása
    if st.button("🔄 Új Quiz", type="primary"):
        reset_quiz()
        st.rerun()

if __name__ == "__main__":
    main() 