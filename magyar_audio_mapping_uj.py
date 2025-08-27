#!/usr/bin/env python3
"""
Magyar zenekarok (új) audio mapping - az audio_files/magyar_zenekarok mappa alapján (automatikusan generálva)
"""

import os
from pathlib import Path

# Dinamikusan generáljuk a mappinget a tényleges fájlok alapján
AUDIO_DIR = Path(__file__).parent / "audio_files/magyar_zenekarok"
files = sorted([f for f in os.listdir(AUDIO_DIR) if f.endswith('.mp3')])
MAGYAR_AUDIO_MAPPING_UJ = {i: fname for i, fname in enumerate(files)}

def get_magyar_audio_uj_path(index):
    """Visszaadja az audio fájl elérési útját az index alapján"""
    fname = MAGYAR_AUDIO_MAPPING_UJ.get(index)
    if fname:
        # ÚJ: próbáljuk az új mappából
        path = AUDIO_DIR / fname
        if path.exists():
            return str(path)
        # Fallback: régi mappa
        old_audio_dir = Path(__file__).parent / "audio_files_magyar_uj"
        old_path = old_audio_dir / fname
        if old_path.exists():
            return str(old_path)
    return None

if __name__ == "__main__":
    print(f"Új magyar mapping bejegyzések száma: {len(MAGYAR_AUDIO_MAPPING_UJ)}")
    for i, fname in MAGYAR_AUDIO_MAPPING_UJ.items():
        print(f"{i}: {fname}") 