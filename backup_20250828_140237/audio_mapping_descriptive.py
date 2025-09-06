#!/usr/bin/env python3
"""
Audio fájl mapping - leíró fájlnevekkel
"""

import os
from pathlib import Path

# Audio fájlok és információk
AUDIO_INFO = {
    "track_5rk76Ugo6ZWsciJwvCQ4vH": {
        "artist": "Vivaldi",
        "title": "Four Seasons Spring Allegro",
        "filename": "track_5rk76Ugo6ZWsciJwvCQ4vH_Vivaldi_Four_Seasons_Spring_Allegro.mp3"
    },
    "track_7qXtc4JTbTugxB1sEktD8W": {
        "artist": "Vivaldi", 
        "title": "Violin Sonata A Major RV 31",
        "filename": "track_7qXtc4JTbTugxB1sEktD8W_Vivaldi_Violin_Sonata_A_Major_RV_31.mp3"
    },
    "track_5PUn21YNL2KNzReeCwOXqp": {
        "artist": "Mozart",
        "title": "Turkish March Piano Sonata", 
        "filename": "track_5PUn21YNL2KNzReeCwOXqp_Mozart_Turkish_March_Piano_Sonata.mp3"
    },
    "track_4BcSup56aUUtG55MkrsHDx": {
        "artist": "Ham Ko Ham",
        "title": "Ellopták a biciklim",
        "filename": "track_4BcSup56aUUtG55MkrsHDx_Ham_Ko_Ham_Ellopták_a_biciklim.mp3"
    },
    "track_0UjXKCLdx7UUETj8JGrD26": {
        "artist": "Maneskin",
        "title": "Beggin",
        "filename": "track_0UjXKCLdx7UUETj8JGrD26_Maneskin_Beggin.mp3"
    },
    "track_0Qe9CUxDFvQi64Tt2EmrM6": {
        "artist": "Tchaikovsky",
        "title": "Nutcracker Dance of the Sugar Plum Fairy",
        "filename": "track_0Qe9CUxDFvQi64Tt2EmrM6_Tchaikovsky_Nutcracker_Dance_of_the_Sugar_Plum_Fairy.mp3"
    },
    "track_5OJCtnMqWmeGzkTJE3mpYr": {
        "artist": "Tchaikovsky",
        "title": "Swan Lake",
        "filename": "track_5OJCtnMqWmeGzkTJE3mpYr_Tchaikovsky_Swan_Lake.mp3"
    },
    "track_62dD6AMgEvZq5OCHAZ7d9a": {
        "artist": "Tchaikovsky",
        "title": "Piano Concerto No 1",
        "filename": "track_62dD6AMgEvZq5OCHAZ7d9a_Tchaikovsky_Piano_Concerto_No_1.mp3"
    },
    "track_0C8ZW7ezQVs4URX5aX7Kqx": {
        "artist": "Selena Gomez",
        "title": "Love You Like A Love Song",
        "filename": "track_0C8ZW7ezQVs4URX5aX7Kqx_Selena_Gomez_Love_You_Like_A_Love_Song.mp3"
    },
}

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
    Leíró fájlneveket használ
    """
    available_files = get_available_audio_files()
    
    if not available_files:
        return None
    
    # Track ID alapú mapping
    if "/track/" in spotify_url:
        track_id = spotify_url.split('/track/')[1].split('?')[0]
        
        # Leíró fájlnév keresése
        if track_id in AUDIO_INFO:
            descriptive_filename = AUDIO_INFO[track_id]["filename"]
            if descriptive_filename in available_files:
                return descriptive_filename
        
        # Fallback: egyszerű track ID
        track_filename = f"track_{track_id}.mp3"
        if track_filename in available_files:
            return track_filename
    
    # Artist ID alapú mapping
    if "/artist/" in spotify_url:
        artist_id = spotify_url.split('/artist/')[1].split('?')[0]
        
        # Leíró fájlnév keresése
        if artist_id in AUDIO_INFO:
            descriptive_filename = AUDIO_INFO[artist_id]["filename"]
            if descriptive_filename in available_files:
                return descriptive_filename
        
        # Fallback: egyszerű track ID
        artist_filename = f"track_{artist_id}.mp3"
        if artist_filename in available_files:
            return artist_filename
    
    # Ha nincs megfelelő fájl, ne játsszon le semmit
    return None

def get_audio_info(spotify_url):
    """
    Visszaadja az audio fájl információit (előadó, cím)
    """
    if "/track/" in spotify_url:
        track_id = spotify_url.split('/track/')[1].split('?')[0]
        if track_id in AUDIO_INFO:
            return AUDIO_INFO[track_id]
    
    if "/artist/" in spotify_url:
        artist_id = spotify_url.split('/artist/')[1].split('?')[0]
        if artist_id in AUDIO_INFO:
            return AUDIO_INFO[artist_id]
    
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
        
        # Leíró fájlnév keresése
        if track_id in AUDIO_INFO:
            descriptive_filename = AUDIO_INFO[track_id]["filename"]
            if descriptive_filename in available_files:
                return descriptive_filename
        
        # Fallback: egyszerű track ID
        track_filename = f"track_{track_id}.mp3"
        if track_filename in available_files:
            return track_filename
    
    # Artist ID alapú mapping
    if "/artist/" in spotify_url:
        artist_id = spotify_url.split('/artist/')[1].split('?')[0]
        
        # Leíró fájlnév keresése
        if artist_id in AUDIO_INFO:
            descriptive_filename = AUDIO_INFO[artist_id]["filename"]
            if descriptive_filename in available_files:
                return descriptive_filename
        
        # Fallback: egyszerű track ID
        artist_filename = f"track_{artist_id}.mp3"
        if artist_filename in available_files:
            return artist_filename
    
    # Ha nincs megfelelő fájl, ne játsszon le semmit
    return None 