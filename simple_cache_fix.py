import streamlit as st
import os
import subprocess

def simple_audio_track_management(selected_category):
    """Egyszerű audio track kezelés cache rendszerrel"""
    
    # Cache key
    cache_key = f"simple_audio_data_{selected_category}"
    
    # Cache törlése gomb
    if st.button("🗑️ Cache törlése"):
        if cache_key in st.session_state:
            del st.session_state[cache_key]
        st.rerun()
    
    # Cache ellenőrzése
    if cache_key in st.session_state:
        table_data = st.session_state[cache_key]
        st.info(f"📊 Cache betöltve: {len(table_data)} sor")
        return table_data
    
    # Új adatok betöltése
    st.info("🔄 Új adatok betöltése...")
    
    # Kérdések betöltése
    questions = load_questions_from_file(selected_category)
    st.info(f"📚 Kérdések betöltve: {len(questions)} kérdés")
    
    # Track cache létrehozása
    category_info = get_audio_tracks_by_category(selected_category)
    tracks = category_info['tracks']
    track_cache = {}
    for track in tracks:
        track_name_no_ext = os.path.splitext(track['name'])[0]
        track_cache[track_name_no_ext] = track
    
    st.info(f"🎵 Track cache létrehozva: {len(track_cache)} track")
    
    # Egyszerű táblázat létrehozás
    table_data = []
    st.info(f"🔄 Táblázat létrehozása {len(questions)} kérdésből...")
    
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
            question_audio_no_ext = os.path.splitext(question_audio_file)[0]
            matching_track = track_cache.get(question_audio_no_ext)
        
        # Song title meghatározása
        song_title = "Ismeretlen szám"
        if matching_track and 'name' in matching_track:
            song_title = matching_track['name']
        elif 'audio_file' in question:
            audio_file = question['audio_file']
            filename = os.path.basename(audio_file)
            filename_no_ext = os.path.splitext(filename)[0]
            song_title = filename_no_ext
        
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
        
        # Progress jelzés minden 10. kérdésnél
        if (i + 1) % 10 == 0:
            st.info(f"📊 Feldolgozott kérdések: {i + 1}/{len(questions)}")
    
    # Cache mentése
    st.session_state[cache_key] = table_data
    st.info(f"💾 Cache mentve: {len(table_data)} sor")
    st.success(f"✅ Táblázat létrehozva: {len(table_data)} sor")
    
    return table_data
