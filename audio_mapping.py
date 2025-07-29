#!/usr/bin/env python3
"""
Audio fájl mapping - automatikus hozzárendelés a letöltött fájlok alapján
"""

import os
from pathlib import Path

def get_available_audio_files():
    """Visszaadja az összes elérhető audio fájlt"""
    audio_dir = Path(__file__).parent / "audio_files"
    if not audio_dir.exists():
        return []
    
    audio_files = []
    for file in audio_dir.glob("*.mp3"):
        audio_files.append(file.name)
    
    return sorted(audio_files)

def get_audio_filename(spotify_url, question_index=0):
    """
    Visszaadja az audio fájl nevét a Spotify URL alapján
    Automatikusan hozzárendeli a letöltött fájlokat
    """
    available_files = get_available_audio_files()
    
    if not available_files:
        return None
    
    # Track ID alapú mapping
    if "/track/" in spotify_url:
        track_id = spotify_url.split('/track/')[1].split('?')[0]
        track_filename = f"track_{track_id}.mp3"
        
        # Ha pontosan megtaláljuk a fájlt
        if track_filename in available_files:
            return track_filename
    
    # Artist ID alapú mapping
    if "/artist/" in spotify_url:
        artist_id = spotify_url.split('/artist/')[1].split('?')[0]
        artist_filename = f"track_{artist_id}.mp3"
        
        # Ha pontosan megtaláljuk a fájlt
        if artist_filename in available_files:
            return artist_filename
    
    # Ha nincs megfelelő fájl, ne játsszon le semmit
    return None

# Cache az elérhető fájlokhoz
_available_files_cache = None

def get_audio_filename_cached(spotify_url, question_index=0):
    """Cache-elt verzió a jobb teljesítményért"""
    global _available_files_cache
    
    if _available_files_cache is None:
        _available_files_cache = get_available_audio_files()
    
    available_files = _available_files_cache
    
    if not available_files:
        return None
    
    # Track ID alapú mapping
    if "/track/" in spotify_url:
        track_id = spotify_url.split('/track/')[1].split('?')[0]
        track_filename = f"track_{track_id}.mp3"
        
        # Ha pontosan megtaláljuk a fájlt
        if track_filename in available_files:
            return track_filename
    
    # Artist ID alapú mapping
    if "/artist/" in spotify_url:
        artist_id = spotify_url.split('/artist/')[1].split('?')[0]
        artist_filename = f"track_{artist_id}.mp3"
        
        # Ha pontosan megtaláljuk a fájlt
        if artist_filename in available_files:
            return artist_filename
    
    # Ha nincs megfelelő fájl, ne játsszon le semmit
    return None 