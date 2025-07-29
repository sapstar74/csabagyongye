#!/usr/bin/env python3
"""
Fixed international audio mapping - based on actual files
"""

# Nemzetközi zenekarok audio fájl mapping - valóságos fájlokkal
NEMZETKOZI_AUDIO_MAPPING = {
    0: "10_Adele.mp3",
    1: "1_Ariana_Grande.mp3",
    2: "2_Sabrina_Carpenter.mp3",
    3: "3_Olivia_Rodrigo.mp3",
    4: "4_Rihanna.mp3",
    5: "5_Dua_Lipa.mp3",
    6: "6_Camilla_Cabello.mp3",
    7: "7_Miley_Cyrus.mp3",
    8: "8_Lady_Gaga.mp3",
    9: "9_Billie_Eilish.mp3",
}

def get_nemzetkozi_audio_path(index):
    """
    Visszaadja a nemzetközi zenekarok audio fájljának teljes elérési útját az index alapján.
    """
    from pathlib import Path
    filename = NEMZETKOZI_AUDIO_MAPPING.get(index)
    if filename:
        audio_dir = Path(__file__).parent / "audio_files"
        audio_path = audio_dir / filename
        return audio_path
    return None

if __name__ == "__main__":
    # Példa használat
    print(f"Javított mapping bejegyzések száma: {len(NEMZETKOZI_AUDIO_MAPPING)}")
    print(f"Index 0: {get_nemzetkozi_audio_path(0)}")
    print(f"Index 1: {get_nemzetkozi_audio_path(1)}")
    print(f"Index 10: {get_nemzetkozi_audio_path(10)}")
