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
from typing import Optional

from i18n import init_i18n, render_language_selector, t, translate_text
from quiz_data import QUIZ_DATA_BY_TOPIC
from quiz_utils import _normalize_answer_text, _is_text_answer_correct, get_client_ip
from quiz_styles import apply_styles
from quiz_sync import sync_with_github, sync_komolyzene_with_github, get_image_base64
from quiz_audio import (
    get_audio_file_for_question,
    get_all_audio_tracks,
    get_audio_tracks_by_category,
    _parse_artist_and_title,
    _parse_artist_title_from_youtube,
    _get_piece_title_for_question,
)
from quiz_youtube import (
    search_youtube_tracks,
    download_and_integrate_track,
    generate_quiz_question,
    add_question_to_category,
    save_questions_to_file,
)
from quiz_audio_management import show_audio_track_management_page
from quiz_spotify_page import show_spotify_playlist_main, show_spotify_playlist_tab

init_i18n()

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


def _topic_session_key(topic: str) -> str:
    """Biztonságos session_state/widget kulcs témakörökhöz (szóközök eltávolítása, Streamlit konfliktus elkerülésére)."""
    return topic.replace(" ", "_")


def _get_topic_question_count(topic: str, default: int = 0) -> int:
    """Kategória kérdésszáma – perzisztens tárolóból (nem törlődik kikapcsoláskor)."""
    counts = st.session_state.get("_topic_question_counts", {})
    if topic in counts:
        return counts[topic]
    key = f"final_{_topic_session_key(topic)}_questions"
    return st.session_state.get(key, default)


def _set_topic_question_count(topic: str, value: int) -> None:
    """Kategória kérdésszám mentése perzisztens tárolóba."""
    if "_topic_question_counts" not in st.session_state:
        st.session_state["_topic_question_counts"] = {}
    st.session_state["_topic_question_counts"][topic] = value


def _save_topic_count_before_deselect(topic_key: str) -> None:
    """Aktuális kérdésszám mentése kikapcsolás előtt (widget kulcs törlődik)."""
    key = f"final_{_topic_session_key(topic_key)}_questions"
    if key in st.session_state:
        _set_topic_question_count(topic_key, st.session_state[key])


# Page config
st.set_page_config(
    page_title=t("Csabagyöngye Tréning Center"),
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Theme init (Light/Dark) – query_params + session_state a deployolt környezetben való megmaradásért
# URL-ben: ?theme=light vagy ?theme=dark – így a session state elvesztése nem befolyásolja
_theme_from_url = st.query_params.get("theme")
if _theme_from_url is not None and isinstance(_theme_from_url, (list, tuple)):
    _theme_from_url = _theme_from_url[0] if _theme_from_url else None
if _theme_from_url in ("light", "dark"):
    st.session_state.theme = _theme_from_url
elif "theme" not in st.session_state:
    st.session_state.theme = "light"

_current_theme = st.session_state.get("theme", "light")
# Téma marker a legelső elem – a CSS :has() így biztosan működik
st.markdown(
    f'<div data-quiz-theme="{_current_theme}" style="position:absolute;width:0;height:0;overflow:hidden;pointer-events:none" aria-hidden="true"></div>',
    unsafe_allow_html=True,
)
apply_styles(_current_theme)

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
    st.session_state.pop('_show_answer_feedback', None)
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
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar könnyűzene",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi zenekarok",
        "sorozat_focimek": "📺 Sorozat főcímek",
        "festmények": "🎨 Festmények",
        "magyar_festmenyek": "🇭🇺 Magyar festmények",
        "regények": "📚 Regények",
        "tudósok": "🔬 Tudósok",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "zászlórészlet": "🏴 Zászlórészlet",
        "idióta_szavak": "🤪 Idióta szavak",
        "labdarugo_palyafutas": "⚽ Labdarúgó pályafutás",
        "vallás és egyháztörténet": "⛪ Vallás és egyháztörténet",
        "művészet": "🎨 Művészet",
        "természettudomány": "🔬 Természettudomány",
        "irodalom": "📖 Irodalom",
        "politika": "🏛️ Politika",
        "világtörténelem": "🌐 Világtörténelem",
        "magyar történelem": "🇭🇺 Magyar történelem",
        "híres magyarok": "🌟 Híres magyarok",
        "biológia": "🧬 Biológia",
        "sport": "🏅 Sport",
    }
    
    for topic_key in topics.keys():
        checkbox_key = f"topic_{topic_key}"
        if checkbox_key in st.session_state:
            del st.session_state[checkbox_key]

def show_answer_popup(question, user_answer, correct_answer, is_correct=True):
    """Tartós popup üzenet a válaszról és helyes válaszról"""
    music_topics = {"komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"}
    topic = question.get("topic") if isinstance(question, dict) else None
    # Magyar Zenekarok: ne jelenjen meg a "Darab címe" / "A szám címe" mező
    magyar_zenekarok_topics = {"magyar_zenekarok", "magyar_zenekarok_uj"}
    show_piece_title = (
        topic not in magyar_zenekarok_topics
        and (
            topic in music_topics
            or (isinstance(question, dict) and (question.get("audio_file") or question.get("spotify_embed")))
        )
    )
    piece_title = _get_piece_title_for_question(question) if show_piece_title else None
    if piece_title:
        piece_title = translate_text(piece_title)

    # Magyar Zenekarok: soha ne tároljuk a piece_title-t („A szám címe” mező)
    popup_data = {
        "user_answer": user_answer if user_answer else t("N/A"),
        "correct_answer": correct_answer if correct_answer else t("N/A"),
        "is_correct": is_correct,
    }
    if topic not in magyar_zenekarok_topics:
        popup_data["piece_title"] = piece_title
    st.session_state.answer_popup = popup_data

def render_answer_popup():
    """Popup megjelenítése, amíg a felhasználó be nem zárja. Hibás válasz esetén mindig figyelemfelhívó üzenet."""
    popup = st.session_state.get("answer_popup")
    if not popup:
        return

    is_correct = popup.get("is_correct", True)

    st.markdown(
        """
        <style>
        .answer-popup {
            padding: 16px 24px;
            border-radius: 12px;
            margin: 16px 0;
            font-size: 15px;
            font-family: 'Inter', sans-serif;
            animation: answerPopupFadeOut 0.4s ease 5s forwards;
        }
        .answer-popup.correct {
            background: #0f766e;
            color: #ffffff;
            border: 1px solid #0d9488;
        }
        .answer-popup.incorrect {
            background: #b91c1c;
            color: #ffffff;
            border: 1px solid #991b1b;
        }
        @keyframes answerPopupFadeOut {
            to { opacity: 0; visibility: hidden; pointer-events: none; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    piece_line = ""
    if "piece_title" in popup and popup.get("piece_title"):
        piece_value = popup["piece_title"] or t("N/A")
        piece_line = f"<br/><strong>{t('Darab címe:')}</strong> {piece_value}"

    user_answer_label = t("Válaszod:")
    correct_answer_label = t("Helyes válasz:")
    popup_class = "answer-popup incorrect" if not is_correct else "answer-popup correct"

    st.markdown(
        f"""
        <div class="{popup_class}">
            <strong>{user_answer_label}</strong> {popup["user_answer"]}
            &nbsp;|&nbsp;
            <strong>{correct_answer_label}</strong> {popup["correct_answer"]}
            {piece_line}
        </div>
        """,
        unsafe_allow_html=True,
    )
    # Egyszeri megjelenítés: a következő kérdésnél már nem jelenik meg (5 mp után CSS animációval eltűnik)
    st.session_state.pop("answer_popup", None)

def start_quiz():
    """Quiz indítása"""
    if not st.session_state.selected_topics:
        st.error(t("Kérlek válassz ki legalább egy témaköröt!"))
        return
    
    # Játékos név: opcionális, ha üres marad "Ismeretlen" lesz
    player_name = (
        st.session_state.get("player_name_input", "").strip()
        or st.session_state.get("selected_player", "").strip()
    )
    st.session_state.selected_player = player_name
    
    # Végleges kérdésszám használata - ha nincs beállítva, akkor 0 (a tényleges kérdések számától függ)
    final_question_count = st.session_state.get('final_question_count', 0)
    
    all_questions = []
    total_selected_questions = 0
    invalid_questions = 0
    
    # Minden témakör kezelése egyedi sliders alapján
    pending_counts = st.session_state.get('_pending_question_counts', {})
    for topic in st.session_state.selected_topics:
        if topic in QUIZ_DATA_BY_TOPIC:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic]
            default_count = min(3, len(topic_questions))
            # Először _pending_question_counts (gomb kattintáskor), majd perzisztens tároló
            questions_count = pending_counts.get(topic)
            if questions_count is None:
                questions_count = _get_topic_question_count(topic, default_count)
            # Ha nincs beállítva slider érték, használjuk az alapértelmezett értéket
            if questions_count == 0:
                questions_count = min(3, len(topic_questions))
            questions_count = min(questions_count, len(topic_questions))
            
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
    
    # Zenei kérdések csoportosítása: egymás után, a sor ~60%-ánál kezdődjenek
    _MUSIC_TOPICS = {"komolyzene", "magyar_zenekarok", "magyar_zenekarok_uj", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"}
    music_questions = [q for q in all_questions if q.get("topic") in _MUSIC_TOPICS]
    other_questions = [q for q in all_questions if q.get("topic") not in _MUSIC_TOPICS]
    
    if music_questions and other_questions:
        random.shuffle(music_questions)
        random.shuffle(other_questions)
        total = len(music_questions) + len(other_questions)
        insert_at = int(0.6 * total)  # ~60%-nál kezdődjenek a zenei kérdések
        insert_at = min(insert_at, len(other_questions))
        all_questions = other_questions[:insert_at] + music_questions + other_questions[insert_at:]
    else:
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
    st.session_state.pop('_pending_question_counts', None)  # Widget kulcsok ütközés elkerülése
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
        f'<h1 style="text-align: center; {font_style["title"]} color: #2c3e50; margin-bottom: 2rem; font-family: Inter, sans-serif;">{t("🎯 Csabagyöngye Tréning Center 😄")}</h1>',
        unsafe_allow_html=True,
    )
    
    # Sidebar navigáció
    with st.sidebar:
        st.markdown(t("## 🌓 Megjelenés"))
        theme_options = {"light": "☀️ Light", "dark": "🌙 Dark"}
        current_theme = st.session_state.get("theme", "light")
        new_theme = st.radio(
            t("Téma"),
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=list(theme_options.keys()).index(current_theme),
            key="theme_radio",
            label_visibility="collapsed",
        )
        if new_theme != current_theme:
            st.session_state.theme = new_theme
            # URL-be is mentjük – így a deployolt app (internet) is megőrzi a témát
            st.query_params["theme"] = new_theme
            st.rerun()
        st.markdown("---")
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

def show_artist_list_page():
    """Szerző szerinti lista önálló oldal"""
    st.markdown(
        f'<h2 style="text-align: center; color: #2c3e50; font-family: Inter, sans-serif;">{t("🎼 Szerző szerinti lista")}</h2>',
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


def show_github_sync_page():
    """GitHub szinkronizációs oldal megjelenítése"""
    st.markdown('<h2 style="text-align: center; color: #2c3e50; font-family: Inter, sans-serif;">🔄 GitHub Szinkronizálás</h2>', unsafe_allow_html=True)
    
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
    st.markdown('<div class="quiz-settings-section">', unsafe_allow_html=True)
    
    # Felhasználó kiválasztás
    st.markdown(t("### 👤 Játékos név megadása"))
    
    player_input = st.text_input(
        t("Add meg a neved (opcionális):"),
        value=st.session_state.get("selected_player", ""),
        key="player_name_input",
        placeholder=t("Üresen hagyható"),
    )
    player_name = player_input.strip()
    st.session_state.selected_player = player_name
    
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
        "komolyzene": "🎼 Komolyzene",
        "magyar_zenekarok": "🎵 Magyar könnyűzene",
        "nemzetkozi_zenekarok": "🌍 Nemzetközi zenekarok",
        "one_hit_wonders": "⭐ One Hit Wonders",
        "sorozat_focimek": "📺 Sorozat főcímek",
        "festmények": "🎨 Festmények",
        "magyar_festmenyek": "🇭🇺 Magyar festmények",
        "regények": "📚 Regények",
        "tudósok": "🔬 Tudósok, művészek, híres emberek",
        "mitológia": "🏛️ Mitológia",
        "állatok": "🐾 Állatok",
        "sport_logók": "🏆 Sport logók",
        "zászlók": "🏁 Zászlók",
        "zászlórészlet": "🏴 Zászlórészlet",
        "idióta_szavak": "🤪 Idióta szavak",
        "labdarugo_palyafutas": "⚽ Labdarúgó pályafutás",
        "vallás és egyháztörténet": "⛪ Vallás és egyháztörténet",
        "művészet": "🎨 Művészet",
        "természettudomány": "🔬 Természettudomány",
        "irodalom": "📖 Irodalom",
        "politika": "🏛️ Politika",
        "világtörténelem": "🌐 Világtörténelem",
        "magyar történelem": "🇭🇺 Magyar történelem",
        "híres magyarok": "🌟 Híres magyarok",
        "biológia": "🧬 Biológia",
        "sport": "🏅 Sport",
    }
    
    # Randomizáló funkció – minden kategória önállóan kap alapértelmezett kérdésszámot (min 3 / max)
    st.markdown(t("### 🎲 Randomizáló Funkció"))
    
    # Randomizáló gombok – kategóriánként önálló alapértelmezés (nem összesítő elosztás)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(t("🎯 Teljes kvíz létrehozása"), type="primary", use_container_width=True):
            # Összes témakör kiválasztása
            st.session_state.selected_topics = list(topics.keys())
            
            # Minden kategória önállóan kap alapértelmezett kérdésszámot (min 3, max)
            total_questions = 0
            for topic_key in topics.keys():
                max_questions = len(MAGYAR_AUDIO_MAPPING_UJ) if topic_key == "magyar_zenekarok" else len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                q = min(3, max_questions) if max_questions > 0 else 0
                st.session_state[f'final_{_topic_session_key(topic_key)}_questions'] = q
                _set_topic_question_count(topic_key, q)
                total_questions += q
            
            st.success(
                t(
                    "✅ Teljes kvíz létrehozva! {topic_count} témakör kiválasztva, összesen {question_count} kérdés. Kategóriánként önállóan állítható!",
                    topic_count=len(topics),
                    question_count=total_questions,
                )
            )
            st.rerun()
        
    with col2:
        if st.button(t("🎵 Random zenei témakörök kiválasztása"), type="secondary", use_container_width=True):
            # Zenei témakörök kiválasztása
            music_topics = ["komolyzene", "magyar_zenekarok", "nemzetkozi_zenekarok", "one_hit_wonders", "sorozat_focimek"]
            num_music_topics = random.randint(2, 3)  # 2-3 zenei témakör
            selected_music_topics = random.sample(music_topics, num_music_topics)
            
            # Meglévő nem-zenei témakörök megtartása
            existing_other_topics = [topic for topic in st.session_state.selected_topics if topic not in music_topics]
            
            # Témakörök kiválasztása (nem-zenei + új zenei)
            st.session_state.selected_topics = existing_other_topics + selected_music_topics
            
            # Minden új zenei kategória önállóan kap alapértelmezett kérdésszámot (min 3, max)
            total_music = 0
            for topic in selected_music_topics:
                max_q = len(MAGYAR_AUDIO_MAPPING_UJ) if topic == "magyar_zenekarok" else len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                q = min(3, max_q) if max_q > 0 else 0
                st.session_state[f'final_{_topic_session_key(topic)}_questions'] = q
                _set_topic_question_count(topic, q)
                total_music += q
            
            st.success(
                t(
                    "✅ {topic_count} zenei témakör kiválasztva + meglévő nem-zenei megtartva. Kategóriánként önállóan állítható!",
                    topic_count=num_music_topics,
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
            
            # Meglévő zenei témakörök megtartása
            existing_music_topics = [topic for topic in st.session_state.selected_topics if topic in music_topics]
            
            # Témakörök kiválasztása (zenei + új random)
            st.session_state.selected_topics = existing_music_topics + selected_random_topics
            
            # Minden új kategória önállóan kap alapértelmezett kérdésszámot (min 3, max)
            total_other = 0
            for topic in selected_random_topics:
                max_q = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                q = min(3, max_q) if max_q > 0 else 0
                st.session_state[f'final_{_topic_session_key(topic)}_questions'] = q
                _set_topic_question_count(topic, q)
                total_other += q
            
            st.success(
                t(
                    "✅ {topic_count} témakör kiválasztva (zene nélkül) + meglévő zenei megtartva. Kategóriánként önállóan állítható!",
                    topic_count=num_topics,
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
    
    selected_topics = st.session_state.selected_topics if 'selected_topics' in st.session_state else []

    # Minden kategória kérdésszáma önállóan állítható a témakör melletti sliderekkel

    with col1:
        st.markdown(t("### 🎵 Zenei témakörök"))
        for topic_key, topic_name in topics.items():
            if "zene" in topic_key or "zenekar" in topic_key or topic_key in {"one_hit_wonders", "sorozat_focimek"}:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{_topic_session_key(topic_key)}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        _save_topic_count_before_deselect(topic_key)
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(3, max_questions)
                    slider_val = _get_topic_question_count(topic_key, default_questions)
                    def _on_slider_change(tk=topic_key):
                        key = f"final_{_topic_session_key(tk)}_questions"
                        if key in st.session_state:
                            _set_topic_question_count(tk, st.session_state[key])
                        st.rerun()
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=slider_val,
                        key=f"final_{_topic_session_key(topic_key)}_questions",
                        on_change=_on_slider_change,
                    )
    
    with col2:
        st.markdown(t("### 📚 Egyéb témakörök"))
        other_topics_list = [item for item in topics.items() if "zene" not in item[0] and "zenekar" not in item[0] and item[0] not in {"one_hit_wonders", "sorozat_focimek"}]
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 0:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{_topic_session_key(topic_key)}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        _save_topic_count_before_deselect(topic_key)
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(3, max_questions)
                    slider_val = _get_topic_question_count(topic_key, default_questions)
                    def _on_slider_change(tk=topic_key):
                        key = f"final_{_topic_session_key(tk)}_questions"
                        if key in st.session_state:
                            _set_topic_question_count(tk, st.session_state[key])
                        st.rerun()
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=slider_val,
                        key=f"final_{_topic_session_key(topic_key)}_questions",
                        on_change=_on_slider_change,
                    )
    
    with col3:
        st.markdown("### &nbsp;")  # Üres cím a cím magasságához
        for i, (topic_key, topic_name) in enumerate(other_topics_list):
            if i % 2 == 1:
                # Kattintható gomb a checkbox helyett
                is_selected = topic_key in st.session_state.selected_topics
                button_style = "primary" if is_selected else "secondary"
                
                if st.button(t(topic_name), key=f"btn_{_topic_session_key(topic_key)}", type=button_style, use_container_width=True):
                    # Témakör hozzáadása/eltávolítása a listából
                    if topic_key in st.session_state.selected_topics:
                        _save_topic_count_before_deselect(topic_key)
                        st.session_state.selected_topics.remove(topic_key)
                    else:
                        st.session_state.selected_topics.append(topic_key)
                    st.rerun()
                
                # Egyedi slider közvetlenül a gomb alatt
                if topic_key in st.session_state.selected_topics:
                    max_questions = len(QUIZ_DATA_BY_TOPIC.get(topic_key, []))
                    default_questions = min(3, max_questions)
                    slider_val = _get_topic_question_count(topic_key, default_questions)
                    def _on_slider_change(tk=topic_key):
                        key = f"final_{_topic_session_key(tk)}_questions"
                        if key in st.session_state:
                            _set_topic_question_count(tk, st.session_state[key])
                        st.rerun()
                    final_topic_questions = st.slider(
                        t("{topic_name} kérdések száma", topic_name=t(topic_name)),
                        min_value=0,
                        max_value=max_questions,
                        value=slider_val,
                        key=f"final_{_topic_session_key(topic_key)}_questions",
                        on_change=_on_slider_change,
                    )
    
    # Minden kategória kérdésszáma a fenti sliderekkel önállóan állítható (nincs összesítő elosztás)
    if st.session_state.selected_topics:
        st.markdown('<div id="final-question-settings"></div>', unsafe_allow_html=True)
    

    # Quiz indítása
    if st.session_state.selected_topics:
        st.markdown(f'<h3 style="color:#1a1a1a;font-family:Inter,sans-serif;">{t("🎯 Végleges Kérdésszám Beállítása")}</h3>', unsafe_allow_html=True)
        
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
        
        # Automatikus elosztás már a témakör sliderek előtt lefutott (Streamlit widget key konfliktus elkerülésére)
        music_topics = [t for t in st.session_state.selected_topics if "zene" in t or "zenekar" in t or t in {"one_hit_wonders", "sorozat_focimek"}]
        other_topics = [t for t in st.session_state.selected_topics if t not in music_topics]
        # Végleges kérdésszám: MINDIG a kategóriánkénti csúszkák összege (minden kategória önállóan állítható)
        current_total = 0
        for topic in st.session_state.selected_topics:
            max_q = len(MAGYAR_AUDIO_MAPPING_UJ) if topic == "magyar_zenekarok" else len(QUIZ_DATA_BY_TOPIC.get(topic, []))
            if max_q == 0:
                continue
            q = _get_topic_question_count(topic, min(3, max_q))
            current_total += q
        if current_total == 0:
            for topic in st.session_state.selected_topics:
                max_available = len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                if max_available > 0:
                    current_total += min(3, max_available)
        final_question_count = current_total
        
        # Kiválasztott zenei és egyéb kérdésszámok (perzisztens tárolóból)
        def _get_topic_count(t, is_music):
            return _get_topic_question_count(t, 0)
        music_selected = sum(_get_topic_count(t, True) for t in music_topics)
        other_selected = sum(_get_topic_count(t, False) for t in other_topics)
        
        # Információk megjelenítése (inline stílus: mindig olvasható sötét szöveg)
        col1, col2, col3, col4 = st.columns(4)
        box_style = "padding:16px;border-radius:12px;margin:8px 0;font-size:1rem;background:#e0f2fe;color:#1a1a1a;border:1px solid #7dd3fc;"
        success_style = "padding:16px;border-radius:12px;margin:8px 0;font-size:1rem;background:#d1fae5;color:#1a1a1a;border:1px solid #34d399;"
        with col1:
            st.markdown(f'<div style="{box_style}"><strong>🎵 Zenei:</strong> {music_selected} / {music_questions}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div style="{box_style}"><strong>📚 Egyéb:</strong> {other_selected} / {other_questions}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="{box_style}"><strong>📊 Összes elérhető:</strong> {total_available_questions}</div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div style="{success_style}"><strong>🎯 Végleges:</strong> {final_question_count}</div>', unsafe_allow_html=True)
        
        # Frissítés gomb + Quiz indítás (Streamlit automatikusan frissít slider változásnál, de manuális frissítés is lehetséges)
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col1:
            if st.button(t("🔄 Frissítés"), key="refresh_final_count", use_container_width=True):
                st.rerun()
        with btn_col2:
            if st.button(t("🚀 Quiz indítása"), type="primary", use_container_width=True):
                # Kérdésszámok összegyűjtése: mindig a kategóriánkénti sliderekből (final_{topic}_questions)
                pending = {}
                for topic in st.session_state.selected_topics:
                    max_q = len(MAGYAR_AUDIO_MAPPING_UJ) if topic == "magyar_zenekarok" else len(QUIZ_DATA_BY_TOPIC.get(topic, []))
                    q = _get_topic_question_count(topic, min(3, max_q))
                    pending[topic] = min(q, max_q) if max_q > 0 else 0
                st.session_state['_pending_question_counts'] = pending
                st.session_state.final_question_count = final_question_count
                start_quiz()
    
    st.markdown('</div>', unsafe_allow_html=True)

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
        # Pontszám mező (akcentus szín – eredmények)
        score_label = t("🎯 PONTSZÁM")
        st.markdown(f"""
        <div style='text-align: center; padding: 16px; background: #ffffff; color: #1a1a1a; border-radius: 12px; border: 1px solid #e7e5e4; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); font-family: Inter, sans-serif;'>
            <div style='font-size: 14px; color: #44403c; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.02em;'>{score_label}</div>
            <div style='font-size: 28px; color: #1a1a1a; font-weight: 700; letter-spacing: -0.02em;'>{st.session_state.score}</div>
            <div style='font-size: 13px; color: #44403c; margin-top: 8px;'>{(st.session_state.score / len(st.session_state.quiz_questions) * 100):.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Kérdés sorszám mező (elsődleges szín)
        question_label = t("📝 KÉRDÉS")
        st.markdown(f"""
        <div style='text-align: center; padding: 16px; background: #ffffff; color: #1a1a1a; border-radius: 12px; border: 1px solid #e7e5e4; margin: 16px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.06); font-family: Inter, sans-serif;'>
            <div style='font-size: 14px; color: #44403c; font-weight: 600; margin-bottom: 8px; letter-spacing: 0.02em;'>{question_label}</div>
            <div style='font-size: 28px; color: #1a1a1a; font-weight: 700; letter-spacing: -0.02em;'>{st.session_state.current_question + 1}</div>
            <div style='font-size: 13px; color: #44403c; margin-top: 8px;'>/ {len(st.session_state.quiz_questions)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Egyéb metrikák megjelenítése (Százalék, Mód, Streak – fekete felirat és érték)
    st.markdown('<div id="quiz-metrics-row"></div>', unsafe_allow_html=True)
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
                f"<div style='text-align: center; font-size: 14px; color: #78716c; margin-top: -10px; font-family: Inter, sans-serif;'>{lives_text}</div>",
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
            f"<div style='text-align: center; font-size: 16px; color: {'#b91c1c' if time_remaining < 10 else '#b45309' if time_remaining < 30 else '#0f766e'}; font-family: Inter, sans-serif; font-weight: 500;'>{timer_text}</div>",
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
    # Magyar Zenekarok: mindig 4 válaszopció (soha szöveges bevitel)
    magyar_zenekarok_topics = {"magyar_zenekarok", "magyar_zenekarok_uj"}
    question_type = question.get("question_type", "multiple_choice")
    if topic in magyar_zenekarok_topics and question.get("options"):
        question_type = "multiple_choice"
    
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
        difficulty = st.session_state.mode_manager.current_difficulty
        # Többválasztós: visszajelzés (zöld/piros), 2 mp után automatikus továbblépés
        if question_type != "text_input" and st.session_state.get('_show_answer_feedback') and 'options' in locals():
            st.markdown('<div id="quiz-answer-options">', unsafe_allow_html=True)
            sel = selected_answer
            col1, col2 = st.columns(2)
            with col1:
                for i in range(0, min(2, len(options))):
                    opt = display_options[i]
                    if i == sel:
                        bg = "#22c55e" if is_correct else "#dc2626"
                        st.markdown(f'<div style="background:{bg};color:white;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
                    elif not is_correct and i == new_correct_index:
                        st.markdown(f'<div style="background:#22c55e;color:white;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="background:#f5f5f4;color:#1a1a1a;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
            with col2:
                for i in range(2, min(4, len(options))):
                    opt = display_options[i]
                    if i == sel:
                        bg = "#22c55e" if is_correct else "#dc2626"
                        st.markdown(f'<div style="background:{bg};color:white;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
                    elif not is_correct and i == new_correct_index:
                        st.markdown(f'<div style="background:#22c55e;color:white;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div style="background:#f5f5f4;color:#1a1a1a;padding:20px;border-radius:12px;margin:10px 0;font-size:1.1rem;">{opt}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            time.sleep(2)
            st.session_state.pop('_show_answer_feedback', None)
            if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                st.session_state.current_question += 1
                st.session_state.question_start_time = datetime.now()
            else:
                st.session_state.quiz_state = 'results'
            st.rerun()
        elif question_type == "text_input":
            pass
        elif difficulty == DifficultyLevel.EASY and new_correct_index < len(options):
            # Helyes válasz gomb (Könnyű módban, ha nincs feedback megjelenítés)
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
        
        # Magyar Zenekarok: mindig a 4 válaszopció gombok (soha szöveges bevitel)
        magyar_zenekarok_topics = {"magyar_zenekarok", "magyar_zenekarok_uj"}
        force_options_for_magyar = topic in magyar_zenekarok_topics and 'options' in locals() and 'new_correct_index' in locals()

        # Idióta szavak kérdések vagy nehéz mód (kivéve mitológia): szöveges bevitel
        if question_type == "text_input" and not force_options_for_magyar:
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
                    
                    # Válasz mentése (popup nélkül)
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
                    
                    # 2 mp várakozás, majd továbblépés
                    time.sleep(2)
                    if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                        st.session_state.current_question += 1
                        st.session_state.question_start_time = datetime.now()
                    else:
                        st.session_state.quiz_state = 'results'
                    st.rerun()
                else:
                    st.warning(t("Kérlek, írj be egy választ!"))
        elif (difficulty == DifficultyLevel.HARD and question.get("topic") != "mitológia"
              and topic not in ("magyar_zenekarok", "magyar_zenekarok_uj")
              and 'options' in locals() and 'new_correct_index' in locals()):
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

                        # Válasz mentése (popup nélkül)
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
                        
                        # 2 mp várakozás, majd továbblépés
                        time.sleep(2)
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

                        # Válasz mentése (popup nélkül)
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
                        
                        # 2 mp várakozás, majd továbblépés
                        time.sleep(2)
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
            /* Válaszopció gombok: fehér háttér, sötét szöveg – Streamlit DOM: marker után jönnek a gombok */
            [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button,
            [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button,
            #quiz-answer-options ~ div .stButton > button,
            #quiz-answer-options ~ div div[data-testid="stButton"] > button {{
                background-color: #ffffff !important;
                background: #ffffff !important;
                color: #1a1a1a !important;
                border: 2px solid #d6d3d1 !important;
                font-size: 24px !important;
                padding: 20px !important;
                height: auto !important;
                min-height: 60px !important;
                line-height: 1.5 !important;
            }}
            [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button:hover,
            #quiz-answer-options ~ div .stButton > button:hover {{
                background-color: #f5f5f4 !important;
                background: #f5f5f4 !important;
                color: #1a1a1a !important;
            }}
            [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button p,
            [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button span,
            #quiz-answer-options ~ div .stButton > button p,
            #quiz-answer-options ~ div .stButton > button span {{
                color: #1a1a1a !important;
            }}

            </style>
            """, unsafe_allow_html=True)
            

                

                

            
            # Válaszlehetőségek elrendezése (fehér háttér, sötét szöveg)
            st.markdown('<div id="quiz-answer-options"></div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                for i in range(0, min(2, len(options))):
                    option = display_options[i]
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               type="secondary", use_container_width=True, help=t("Válaszlehetőség")):
                        handle_answer(i, new_correct_index, options, question, display_options)
            with col2:
                for i in range(2, min(4, len(options))):
                    option = display_options[i]
                    if st.button(option, key=f"option_{st.session_state.current_question}_{i}", 
                               type="secondary", use_container_width=True, help=t("Válaszlehetőség")):
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
    
    # Válasz mentése (popup nélkül)
    display_options = display_options or options
    st.session_state.question_answers[st.session_state.current_question] = selected_index
    st.session_state.answers.append({
        'question': question.get("question", t("Ismeretlen kérdés")),
        'selected': selected_index,
        'correct': correct_index,
        'options': options,
        'is_correct': is_correct,
        'time_taken': (datetime.now() - st.session_state.question_start_time).total_seconds()
    })
    
    # Visszajelzés megjelenítése (zöld/piros gomb), majd Következő gombbal lépünk
    st.session_state['_show_answer_feedback'] = True
    st.rerun()

def handle_time_up():
    """Idő lejárt kezelése"""
    question = st.session_state.quiz_questions[st.session_state.current_question]
    
    # Ellenőrizzük, hogy van-e options_data
    if st.session_state.current_question not in st.session_state.question_options:
        # Ha nincs options_data, automatikusan rossz válasz
        opts = question.get("options", [])
        corr = question.get("correct", 0)
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
        correct_index = options_data['correct_index']
        options = options_data.get('options', [])
        display_options = options_data.get('display_options', options)
        # Automatikusan rossz válasz (popup nélkül)
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
                        <h3 style="color: #2c3e50; margin-bottom: 20px; font-size: 12px;">📋 Letöltési és integrálási folyamat</h3>
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
        # Magyar Zenekarok: nincs "Szám címe" mező
        if category != "magyar_zenekarok":
            approved_title = st.text_input("Szám címe:", value=fallback_title)
        else:
            approved_title = ""
        
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

if __name__ == "__main__":
    main() 