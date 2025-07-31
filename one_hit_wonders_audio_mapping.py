# One Hit Wonders Audio Mapping
import os
from pathlib import Path

AUDIO_DIR = Path(__file__).parent / "audio_files_one_hit_wonders"

# Dinamikusan generált mapping a letöltött fájlok alapján
ONE_HIT_WONDERS_AUDIO_MAPPING = {}

def load_audio_mapping():
    """Audio mapping betöltése a letöltött fájlok alapján"""
    global ONE_HIT_WONDERS_AUDIO_MAPPING
    
    if not AUDIO_DIR.exists():
        return {}
    
    files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')])
    
    for i, filename in enumerate(files, 1):
        ONE_HIT_WONDERS_AUDIO_MAPPING[i] = filename
    
    return ONE_HIT_WONDERS_AUDIO_MAPPING

def get_one_hit_wonders_audio_path(index):
    """One Hit Wonders audio fájl elérési útja"""
    if not ONE_HIT_WONDERS_AUDIO_MAPPING:
        load_audio_mapping()
    
    if index in ONE_HIT_WONDERS_AUDIO_MAPPING:
        return AUDIO_DIR / ONE_HIT_WONDERS_AUDIO_MAPPING[index]
    return None

# Mapping betöltése importáláskor
load_audio_mapping() 