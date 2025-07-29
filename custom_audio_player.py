#!/usr/bin/env python3
"""
Saját audio lejátszó komponens a Spotify embed helyett
"""

import streamlit as st
import os
from pathlib import Path
import base64

def get_audio_file_path(audio_filename):
    """Visszaadja az audio fájl teljes elérési útját"""
    audio_dir = Path(__file__).parent / "audio_files"
    return audio_dir / audio_filename

def audio_player_with_download(audio_filename):
    """
    Saját audio lejátszó komponens letöltési lehetőség nélkül, cím és metaadatok nélkül
    Args:
        audio_filename: Az audio fájl neve (pl. "track_1.mp3")
    """
    audio_path = get_audio_file_path(audio_filename)
    if not audio_path.exists():
        st.warning(f"⚠️ Audio fájl nem található.")
        return
    with open(audio_path, "rb") as audio_file:
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")

def show_custom_audio_player(audio_filename):
    """
    Csak az audio lejátszót jeleníti meg, semmilyen cím vagy tag nélkül.
    """
    audio_player_with_download(audio_filename)

# Példa használat
if __name__ == "__main__":
    st.title("Saját Audio Lejátszó Teszt")
    
    # Teszt audio lejátszó
    test_audio_filename = 'test_track.mp3'
    
    show_custom_audio_player(test_audio_filename) 