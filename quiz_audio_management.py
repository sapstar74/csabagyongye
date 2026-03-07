"""
Quiz audio management: show_audio_track_management_page.
"""

import os
import shutil
import subprocess
import time

import pandas as pd
import streamlit as st

from quiz_audio import get_audio_tracks_by_category
from quiz_questions_io import load_questions_from_file
from quiz_sync import show_github_sync_dialog, sync_komolyzene_with_github
from quiz_youtube import save_questions_to_file


def show_audio_track_management_page():
    """Audio track kezelési oldal megjelenítése"""
    st.markdown('<h2 style="text-align: center; color: #2c3e50; font-family: Inter, sans-serif;">🎵 Audio Track Kezelés</h2>', unsafe_allow_html=True)

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

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🗑️ Cache törlése", type="secondary", use_container_width=True):
            cache_keys_to_delete = [key for key in st.session_state.keys() if key.startswith("audio_track_data_") or key.startswith("duration_")]
            for key in cache_keys_to_delete:
                del st.session_state[key]
            st.success("✅ Cache törölve! Az oldal újratöltődik...")
            st.rerun()

    tracks_by_category = get_audio_tracks_by_category()
    st.markdown("### 📁 Kategória választás")
    category_options = {key: info["title"] for key, info in tracks_by_category.items()}

    cols = st.columns(3)
    selected_category = None
    current_selected = st.session_state.get('selected_category', list(category_options.keys())[0])

    for i, (key, title) in enumerate(category_options.items()):
        col_index = i % 3
        with cols[col_index]:
            is_selected = key == current_selected
            button_type = "primary" if is_selected else "secondary"
            if st.button(f"📂 {title}", key=f"cat_{key}", use_container_width=True, type=button_type):
                selected_category = key
                st.session_state.selected_category = key
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

            cache_key = f"simple_audio_data_{selected_category}"
            question_file_path = category_info['tracks'][0]['question_file'] if category_info['tracks'] else None
            question_file_mtime = None
            if question_file_path and os.path.exists(question_file_path):
                question_file_mtime = os.path.getmtime(question_file_path)
            cache_meta_key = f"{cache_key}_meta"

            if st.button("🗑️ Cache törlése"):
                if cache_key in st.session_state:
                    del st.session_state[cache_key]
                if cache_meta_key in st.session_state:
                    del st.session_state[cache_meta_key]
                st.rerun()

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

                question_file_path = category_info['tracks'][0]['question_file'] if category_info['tracks'] else None
                if question_file_path:
                    questions = load_questions_from_file(question_file_path)
                    st.info(f"📚 Kérdések betöltve: {len(questions)} kérdés")
                else:
                    questions = []
                    st.info("❌ Nincs kérdésfájl!")

                track_cache = {}
                for track in category_info['tracks']:
                    track_cache[track['name']] = track
                st.info(f"🎵 Track cache létrehozva: {len(track_cache)} track")

                table_data = []
                st.info(f"🔄 Táblázat létrehozása {len(questions)} kérdésből...")
                progress_bar = st.progress(0)
                progress_text = st.empty()

                for i, question in enumerate(questions):
                    question_text = question['question']
                    artist = question['options'][question['correct']] if question['correct'] < len(question['options']) else "Ismeretlen"
                    correct_answer = question['options'][question['correct']] if question['correct'] < len(question['options']) else "N/A"
                    options = question['options'] + [""] * (4 - len(question['options']))

                    matching_track = None
                    if 'audio_file' in question:
                        question_audio_filename = os.path.basename(question['audio_file'])
                        question_audio_no_ext = os.path.splitext(question_audio_filename)[0]
                        matching_track = track_cache.get(question_audio_no_ext)

                    song_title = "Ismeretlen szám"
                    if 'song_title' in question and question['song_title']:
                        song_title = question['song_title']
                    elif matching_track and 'name' in matching_track:
                        track_name = matching_track['name']
                        if '. ' in track_name and ' - ' in track_name:
                            parts = track_name.split(' - ', 1)
                            if len(parts) == 2:
                                song_title = parts[1].strip()
                                artist_part = parts[0].strip()
                                if '. ' in artist_part:
                                    artist_name = artist_part.split('. ', 1)[1].strip()
                                    if song_title.lower() == artist_name.lower():
                                        song_title = artist_name
                            else:
                                song_title = track_name
                        elif '_' in track_name and any(part.isdigit() for part in track_name.split('_')):
                            parts = track_name.split('_')
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
                            except Exception:
                                duration_str = "N/A"
                                st.session_state[duration_cache_key] = duration_str

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
                    progress = (i + 1) / len(questions)
                    progress_bar.progress(progress)
                    progress_text.text(f"Feldolgozás: {int(progress * 100)}% ({i + 1}/{len(questions)})")

                st.session_state[cache_key] = table_data
                st.session_state[cache_meta_key] = {"questions_mtime": question_file_mtime}
                st.info(f"💾 Cache mentve: {len(table_data)} sor")
                st.success(f"✅ Táblázat létrehozva: {len(table_data)} sor")

            if table_data:
                df = pd.DataFrame(table_data)
                row_numbers = []
                filenames = []
                for row in table_data:
                    if row['matching_track'] and 'audio_path' in row['matching_track']:
                        audio_path = row['matching_track']['audio_path']
                        filename = os.path.basename(audio_path)
                        filename_no_ext = os.path.splitext(filename)[0]
                        filenames.append(filename)
                        if '_' in filename_no_ext and filename_no_ext.split('_')[0].isdigit():
                            row_numbers.append(filename_no_ext.split('_')[0])
                        else:
                            row_numbers.append("N/A")
                    else:
                        filenames.append("N/A")
                        row_numbers.append("N/A")

                # Magyar Zenekarok: nincs "Szám címe" oszlop
                if selected_category == "magyar_zenekarok":
                    display_cols = ["Előadó", "Opció1", "Opció2", "Opció3", "Opció4"]
                    column_config = {
                        "Sorszám": st.column_config.TextColumn("Sorszám", width="small"),
                        "Fájlnév": st.column_config.TextColumn("Fájlnév", width="medium"),
                        "Előadó": st.column_config.TextColumn("Előadó", width="medium"),
                        "Opció1": st.column_config.TextColumn("Opció1", width="medium"),
                        "Opció2": st.column_config.TextColumn("Opció2", width="medium"),
                        "Opció3": st.column_config.TextColumn("Opció3", width="medium"),
                        "Opció4": st.column_config.TextColumn("Opció4", width="medium")
                    }
                    row_options = [f"{i+1}. {row['Előadó']}" for i, row in enumerate(table_data)]
                else:
                    display_cols = ["Előadó", "Szám címe", "Opció1", "Opció2", "Opció3", "Opció4"]
                    column_config = {
                        "Sorszám": st.column_config.TextColumn("Sorszám", width="small"),
                        "Fájlnév": st.column_config.TextColumn("Fájlnév", width="medium"),
                        "Előadó": st.column_config.TextColumn("Előadó", width="medium"),
                        "Szám címe": st.column_config.TextColumn("Szám címe", width="large"),
                        "Opció1": st.column_config.TextColumn("Opció1", width="medium"),
                        "Opció2": st.column_config.TextColumn("Opció2", width="medium"),
                        "Opció3": st.column_config.TextColumn("Opció3", width="medium"),
                        "Opció4": st.column_config.TextColumn("Opció4", width="medium")
                    }
                    row_options = [f"{i+1}. {row['Előadó']} - {row['Szám címe']}" for i, row in enumerate(table_data)]

                display_df = df[display_cols].copy()
                display_df.insert(0, "Sorszám", row_numbers)
                display_df.insert(1, "Fájlnév", filenames)

                def style_dataframe(df):
                    css = """
                    <style>
                    .dataframe { font-size: 12px !important; }
                    .dataframe th { font-size: 12px !important; font-weight: bold !important; }
                    .dataframe td { font-size: 12px !important; }
                    </style>
                    """
                    st.markdown(css, unsafe_allow_html=True)
                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                        column_config=column_config
                    )
                style_dataframe(display_df)

                selected_row_index = st.selectbox(
                    "Válassz egy sort:",
                    options=row_options,
                    key="audio_row_selector"
                )

                if selected_row_index:
                    selected_index = int(selected_row_index.split('.')[0]) - 1
                    selected_data = table_data[selected_index]
                    play_label = selected_data['Előadó'] if selected_category == "magyar_zenekarok" else f"{selected_data['Előadó']} - {selected_data['Szám címe']}"
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(f"🎵 Play {play_label}", type="primary", use_container_width=True):
                            if selected_data['matching_track'] and 'audio_path' in selected_data['matching_track']:
                                audio_path = selected_data['matching_track']['audio_path']
                                st.audio(audio_path, format='audio/mp3')
                                st.success(f"✅ Lejátszás: {play_label}")
                            else:
                                st.warning(f"⚠️ Nincs audio fájl: {play_label}")

                st.markdown("### ✏️ Szerkesztés")
                if 'modified_questions' not in st.session_state:
                    st.session_state.modified_questions = set()
                if st.session_state.modified_questions:
                    st.info(f"📝 **{len(st.session_state.modified_questions)} kérdés módosítva** - Ne felejtsd el menteni a változásokat!")

                if edit_mode == "✏️ Szerkesztés":
                    st.markdown("**Válassz egy sort a szerkesztéshez:**")
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

                    for i, row in enumerate(table_data):
                        is_modified = row['question_index'] in st.session_state.modified_questions
                        expander_title = f"📝 {i+1}. {row['Előadó']}" if selected_category == "magyar_zenekarok" else f"📝 {i+1}. {row['Előadó']} - {row['Szám címe']}"
                        if is_modified:
                            expander_title += " ✏️ (módosítva)"

                        with st.expander(expander_title, expanded=False):
                            question_index = row['question_index']
                            if question_index < 0 or question_index >= len(questions):
                                st.warning("⚠️ Hibás kérdésindex. Kérlek frissítsd a cache-t.")
                                continue
                            current_question = questions[question_index]

                            question_text = st.text_input("Kérdés:", value=current_question['question'], key=f"question_edit_{i}")
                            # Magyar Zenekarok: nincs "Szám címe" mező
                            if selected_category == "magyar_zenekarok":
                                song_title = ""
                            else:
                                current_song_title = row['Szám címe']
                                song_title = st.text_input("Szám címe:", value=current_song_title, key=f"song_title_edit_{i}")

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

                            correct_answer = st.selectbox(
                                "Helyes válasz:",
                                options=options,
                                index=current_question['correct'] if current_question['correct'] < len(options) else 0,
                                key=f"correct_edit_{i}"
                            )

                            col1, col2, col3 = st.columns([1, 1, 1])
                            with col2:
                                if st.button("💾 Mentés", key=f"save_edit_{i}", type="primary"):
                                    try:
                                        updated_question = {
                                            "question": question_text,
                                            "options": options,
                                            "correct": options.index(correct_answer) if correct_answer in options else 0,
                                            "song_title": song_title
                                        }
                                        if 'audio_file' in current_question:
                                            updated_question['audio_file'] = current_question['audio_file']
                                        if 'explanation' in current_question:
                                            updated_question['explanation'] = current_question['explanation']
                                        if 'topic' in current_question:
                                            updated_question['topic'] = current_question['topic']

                                        questions[question_index] = updated_question
                                        st.session_state.modified_questions.add(question_index)

                                        if save_questions_to_file(questions, question_file_path, "QUESTIONS"):
                                            st.success("✅ Kérdés sikeresen mentve!")
                                            if 'audio_file' in current_question and (song_title != current_song_title or not os.path.basename(current_question['audio_file']).startswith(f"{i+1:02d}.")):
                                                try:
                                                    artist = current_question['options'][current_question['correct']] if current_question['correct'] < len(current_question['options']) else "Unknown_Artist"
                                                    old_audio_file = current_question['audio_file']
                                                    old_audio_path = None
                                                    old_audio_filename = os.path.basename(old_audio_file)
                                                    old_audio_name = os.path.splitext(old_audio_filename)[0]
                                                    for track in category_info['tracks']:
                                                        if track['name'] == old_audio_name:
                                                            old_audio_path = track['audio_path']
                                                            break
                                                    if old_audio_path and os.path.exists(old_audio_path):
                                                        clean_song_title = song_title
                                                        if '_' in clean_song_title and any(part.isdigit() for part in clean_song_title.split('_')):
                                                            parts = clean_song_title.split('_')
                                                            for j in range(len(parts)-1, -1, -1):
                                                                if not parts[j].isdigit() and parts[j].lower() not in [artist.lower().replace(' ', '_'), 'unknown_artist']:
                                                                    clean_song_title = '_'.join(parts[j:])
                                                                    break
                                                        safe_song_title = "".join(c for c in clean_song_title if c.isalnum() or c in (' ', '-')).rstrip().replace('  ', ' ')
                                                        artist_safe = "".join(c for c in artist if c.isalnum() or c in (' ', '-')).rstrip().replace('  ', ' ')
                                                        new_filename = f"{i+1:02d}. {artist_safe} - {safe_song_title}.mp3"
                                                        new_audio_path = os.path.join(os.path.dirname(old_audio_path), new_filename)
                                                        shutil.move(old_audio_path, new_audio_path)
                                                        updated_question['audio_file'] = new_filename
                                                        questions[question_index] = updated_question
                                                        save_questions_to_file(questions, question_file_path, "QUESTIONS")
                                                        st.success(f"✅ Audio fájl átnevezve: {new_filename}")
                                                except Exception as e:
                                                    st.warning(f"⚠️ Fájl átnevezése sikertelen: {str(e)}")

                                            cache_keys_to_delete = [key for key in st.session_state.keys() if key.startswith("audio_track_data_") or key.startswith("duration_") or key.startswith("track_cache_") or key == "modified_questions"]
                                            for key in cache_keys_to_delete:
                                                if key in st.session_state:
                                                    del st.session_state[key]
                                            st.session_state['force_refresh'] = True
                                            try:
                                                subprocess.run(['git', 'add', question_file_path], check=True)
                                                subprocess.run(['git', 'commit', '-m', f'Update question for {row["Előadó"]} - {row["Szám címe"]}'], check=True)
                                                subprocess.run(['git', 'push'], check=True)
                                                st.success("✅ Változások GitHub-ra feltöltve!")
                                                time.sleep(0.5)
                                                st.rerun()
                                            except subprocess.CalledProcessError as e:
                                                st.error(f"❌ Git hiba: {e}")
                                        else:
                                            st.error("❌ Hiba a fájl mentésekor!")
                                    except Exception as e:
                                        st.error(f"❌ Hiba a mentés során: {e}")

                            st.markdown("---")
                            st.markdown("### ▶️ Lejátszás")
                            _audio_path_play = None
                            if row.get('matching_track') and row['matching_track'].get('audio_path'):
                                _audio_path_play = row['matching_track']['audio_path']
                            elif 'audio_file' in current_question and current_question['audio_file']:
                                _candidate = os.path.join(
                                    os.path.dirname(question_file_path or ""),
                                    "..", "audio_files", selected_category,
                                    os.path.basename(current_question['audio_file'])
                                )
                                if os.path.exists(_candidate):
                                    _audio_path_play = _candidate
                            if _audio_path_play and os.path.exists(_audio_path_play):
                                st.audio(_audio_path_play, format='audio/mp3')
                            else:
                                st.caption("⚠️ Nincs elérhető audio fájl ehhez a trackhez.")

                            st.markdown("---")
                            st.markdown("### 🗑️ Törlés")
                            st.warning("⚠️ Ez a művelet visszavonhatatlan: a kérdés és az audio fájl is törlődik.")
                            confirm_delete = st.checkbox("Igen, törlöm ezt a tracket és a kérdést", key=f"confirm_delete_{i}")

                            if st.button("🗑️ Track + kérdés törlése és GitHub sync", key=f"delete_track_{i}", type="secondary"):
                                if not confirm_delete:
                                    st.warning("⚠️ A törléshez jelöld be a megerősítést.")
                                else:
                                    try:
                                        if not question_file_path:
                                            st.error("❌ Nincs kérdésfájl, törlés nem lehetséges.")
                                        else:
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

                                            updated_questions = [q for idx, q in enumerate(questions) if idx != question_index]
                                            if save_questions_to_file(updated_questions, question_file_path, "QUESTIONS"):
                                                if audio_path and os.path.exists(audio_path):
                                                    os.remove(audio_path)
                                                    st.success(f"✅ Audio fájl törölve: {os.path.basename(audio_path)}")
                                                else:
                                                    st.warning("⚠️ Audio fájl nem található, csak a kérdés törölve.")
                                                try:
                                                    subprocess.run(['git', 'add', '-A', question_file_path], check=True)
                                                    if audio_path:
                                                        subprocess.run(['git', 'add', '-A', audio_path], check=True)
                                                    subprocess.run(['git', 'commit', '-m', f'Delete track {row["Előadó"]} - {row["Szám címe"]}'], check=True)
                                                    subprocess.run(['git', 'push'], check=True)
                                                    st.success("✅ Törlés GitHub-ra szinkronizálva!")
                                                except subprocess.CalledProcessError as e:
                                                    st.error(f"❌ Git hiba: {e}")
                                                cache_keys_to_delete = [key for key in st.session_state.keys() if key.startswith("audio_track_data_") or key.startswith("duration_") or key.startswith("track_cache_") or key == "modified_questions"]
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
                    st.markdown("**Válassz a fenti opciók közül a szerkesztéshez.**")

                if edit_mode == "✏️ Szerkesztés" and st.session_state.modified_questions:
                    st.markdown("---")
                    st.markdown("### 💾 Összes változás mentése")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button("🚀 Összes változás mentése és Git Push", type="primary", use_container_width=True):
                            try:
                                if save_questions_to_file(questions, question_file_path, "QUESTIONS"):
                                    st.success("✅ Kérdések sikeresen mentve!")
                                    try:
                                        subprocess.run(['git', 'add', question_file_path], check=True)
                                        subprocess.run(['git', 'commit', '-m', f'Update multiple questions in {selected_category}'], check=True)
                                        subprocess.run(['git', 'push'], check=True)
                                        st.success("✅ Összes változás GitHub-ra feltöltve!")
                                        st.session_state.modified_questions.clear()
                                        st.rerun()
                                    except subprocess.CalledProcessError as e:
                                        st.error(f"❌ Git hiba: {e}")
                                else:
                                    st.error("❌ Hiba a fájl mentésekor!")
                            except Exception as e:
                                st.error(f"❌ Hiba a mentés során: {e}")
