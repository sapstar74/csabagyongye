"""
Quiz questions I/O: load_questions_from_file, find_matching_question, _make_safe_filename.
"""

import os
import re

import streamlit as st


def _make_safe_filename(artist: str, title: str) -> str:
    """Biztonságos fájlnév generálása az előadó és cím alapján"""
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
        except Exception:
            pass

        # 2. Ha az import nem sikerült, regex-szel próbáljuk
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        questions = []
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
                options = re.findall(r'"([^"]+)"', options_str)

                if len(options) >= 4:
                    question_data = {
                        "question": question_text,
                        "options": options,
                        "correct": correct
                    }
                    audio_match = re.search(r'"audio_file":\s*"([^"]+)"', content)
                    if audio_match:
                        question_data['audio_file'] = audio_match.group(1)
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

    for q in questions:
        if 'audio_file' in q:
            audio_file = q['audio_file'].lower()
            audio_file_no_ext = os.path.splitext(audio_file)[0]
            track_name_no_ext = os.path.splitext(track_name)[0]

            if audio_file_no_ext == track_name_no_ext:
                return q

            if '_' in track_name_no_ext and track_name_no_ext.split('_')[0].isdigit():
                track_name_without_number = '_'.join(track_name_no_ext.split('_')[1:])
                if audio_file_no_ext.endswith(track_name_without_number):
                    return q

    for q in questions:
        if track_name_lower in q['question'].lower() or q['question'].lower() in track_name_lower:
            return q

    track_words = [word.strip() for word in track_name_lower.replace('-', ' ').replace('_', ' ').split() if len(word.strip()) > 2]

    for q in questions:
        question_lower = q['question'].lower()
        matching_words = sum(1 for word in track_words if word in question_lower)
        if matching_words >= 2:
            return q

    if '-' in track_name_lower:
        artist_name = track_name_lower.split('-')[0].strip()
        for q in questions:
            if artist_name in q['question'].lower():
                return q

    return None
