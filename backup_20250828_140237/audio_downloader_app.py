#!/usr/bin/env python3
"""
🎵 Audio Letöltő Alkalmazás
Streamlit alkalmazás a Spotify linkekből való audio letöltéshez
"""

import streamlit as st
import os
from pathlib import Path
import time
from spotify_audio_downloader import SpotifyAudioDownloader

def main():
    st.set_page_config(
        page_title="Audio Letöltő",
        page_icon="🎵",
        layout="wide"
    )
    
    st.title("🎵 Audio Letöltő Alkalmazás")
    st.markdown("Ez az alkalmazás letölti az audio tartalmakat a Spotify linkekből.")
    
    # Audio könyvtár létrehozása
    audio_dir = Path(__file__).parent / "audio_files"
    audio_dir.mkdir(exist_ok=True)
    
    # Sidebar beállítások
    st.sidebar.markdown("### ⚙️ Beállítások")
    
    # Kérdések betöltése
    st.sidebar.markdown("### 📚 Kérdések Betöltése")
    
    if st.sidebar.button("🔄 Kérdések Betöltése"):
        try:
            from topics.magyar_zenekarok import MAGYAR_ZENEKAROK_QUESTIONS
            from topics.nemzetkozi_zenekarok import NEMZETKOZI_ZENEKAROK_QUESTIONS
            from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS
            
            all_questions = (
                MAGYAR_ZENEKAROK_QUESTIONS + 
                NEMZETKOZI_ZENEKAROK_QUESTIONS + 
                CLASSICAL_MUSIC_QUESTIONS
            )
            
            st.session_state.all_questions = all_questions
            st.session_state.spotify_links = []
            
            for i, q in enumerate(all_questions):
                if 'spotify_embed' in q and q['spotify_embed']:
                    st.session_state.spotify_links.append({
                        'index': i,
                        'question': q['question'],
                        'explanation': q.get('explanation', ''),
                        'spotify_url': q['spotify_embed'],
                        'downloaded': False
                    })
            
            st.sidebar.success(f"✅ {len(st.session_state.spotify_links)} Spotify link találva!")
            
        except Exception as e:
            st.sidebar.error(f"❌ Hiba a kérdések betöltésekor: {e}")
    
    # Fő tartalom
    if 'spotify_links' in st.session_state:
        st.markdown(f"### 📋 Talált Spotify Linkek: {len(st.session_state.spotify_links)}")
        
        # Letöltési beállítások
        col1, col2 = st.columns(2)
        
        with col1:
            max_downloads = st.number_input(
                "Maximális letöltések száma",
                min_value=1,
                max_value=len(st.session_state.spotify_links),
                value=min(10, len(st.session_state.spotify_links))
            )
        
        with col2:
            delay_seconds = st.number_input(
                "Várakozás letöltések között (másodperc)",
                min_value=1,
                max_value=10,
                value=2
            )
        
        # Letöltés indítása
        if st.button("🚀 Letöltés Indítása", type="primary"):
            downloader = SpotifyAudioDownloader()
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            downloaded_count = 0
            
            for i, link_info in enumerate(st.session_state.spotify_links[:max_downloads]):
                status_text.text(f"Letöltés {i+1}/{max_downloads}: {link_info['explanation']}")
                
                # Fájlnév generálása
                track_id = downloader.extract_track_id(link_info['spotify_url'])
                if track_id:
                    output_filename = f"track_{track_id}.mp3"
                else:
                    output_filename = f"audio_{i}.mp3"
                
                # Letöltés
                if downloader.download_spotify_track(link_info['spotify_url'], output_filename):
                    link_info['downloaded'] = True
                    link_info['filename'] = output_filename
                    downloaded_count += 1
                    st.success(f"✅ {output_filename}: {link_info['explanation']}")
                else:
                    st.error(f"❌ Sikertelen: {link_info['explanation']}")
                
                progress_bar.progress((i + 1) / max_downloads)
                
                # Várakozás
                time.sleep(delay_seconds)
            
            status_text.text(f"✅ Letöltés befejezve! {downloaded_count}/{max_downloads} sikeres.")
            
            if downloaded_count > 0:
                st.balloons()
        
        # Letöltött fájlok listázása
        st.markdown("### 📁 Letöltött Fájlok")
        
        audio_files = list(audio_dir.glob("*.mp3"))
        if audio_files:
            for audio_file in audio_files:
                file_size = audio_file.stat().st_size / 1024  # KB
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"🎵 {audio_file.name}")
                
                with col2:
                    st.write(f"{file_size:.1f} KB")
                
                with col3:
                    # Letöltési gomb
                    with open(audio_file, "rb") as f:
                        st.download_button(
                            label="📥",
                            data=f.read(),
                            file_name=audio_file.name,
                            mime="audio/mpeg"
                        )
        else:
            st.info("📁 Még nincsenek letöltött audio fájlok.")
    
    else:
        st.info("👆 Kattints a 'Kérdések Betöltése' gombra a bal oldali menüben!")
    
    # Használati útmutató
    with st.expander("📖 Használati Útmutató"):
        st.markdown("""
        ### 🎯 Hogyan használd:
        
        1. **Kérdések Betöltése**: Kattints a bal oldali menüben
        2. **Letöltési Beállítások**: Állítsd be a maximális letöltések számát
        3. **Letöltés Indítása**: Kattints a nagy kék gombra
        4. **Várakozás**: A letöltés automatikusan folytatódik
        5. **Fájlok**: A letöltött fájlok megjelennek a listában
        
        ### ⚠️ Fontos:
        - A letöltés időbe telik, kérlek várj türelmesen
        - Csak olyan tartalmakat tölts le, amikhez jogod van
        - A fájlok az `audio_files` könyvtárba kerülnek
        
        ### 🔧 Technikai Részletek:
        - A letöltés YouTube keresésen keresztül történik
        - MP3 formátumban mentődnek a fájlok
        - Automatikus minőség optimalizálás
        """)

if __name__ == "__main__":
    main() 