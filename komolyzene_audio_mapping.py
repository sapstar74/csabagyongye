#!/usr/bin/env python3
"""
Komolyzenei audio fájlok mapping-je
"""

# Komolyzenei audio fájlok mapping-je
KOMOLYZENE_AUDIO_MAPPING = {
    # Dvorak
    0: "1_Dvorak_New_World_Symphony.mp3",
    1: "2_Dvorak_Humoresque.mp3", 
    2: "3_Dvorak_Symphony_8.mp3",
    
    # Beethoven
    3: "4_Beethoven_Symphony_5.mp3",
    4: "5_Beethoven_Moonlight_Sonata.mp3",
    5: "6_Beethoven_Ode_to_Joy.mp3",
    15: "16_Beethoven_Ode_to_Joy_2.mp3",
    
    # Csajkovszkij
    6: "7_Tchaikovsky_Nutcracker.mp3",
    7: "8_Tchaikovsky_Swan_Lake.mp3", 
    8: "9_Tchaikovsky_Piano_Concerto_1.mp3",
    
    # Handel
    9: "10_Handel_Rinaldo.mp3",
    10: "11_Handel_Minuet_B_flat.mp3",
    11: "12_Handel_Keyboard_Suite_D_minor.mp3",
    
    # Wagner
    12: "13_Wagner_Ride_of_Valkyries.mp3",
    13: "14_Wagner_Lohengrin_Wedding_March.mp3",
    
    # Schubert
    14: "15_Schubert_Ave_Maria.mp3",
    26: "27_Schubert_Trout_Quintet.mp3",
    
    # Kodály
    16: "17_Kodaly_Hary_Janos.mp3",
    17: "18_Kodaly_Kallai_Kettos.mp3",
    18: "19_Kodaly_Adagio.mp3",
    
    # Bartók
    19: "20_Bartok_Bluebeard_Castle.mp3",
    20: "21_Bartok_Miraculous_Mandarin.mp3",
    
    # Hacsaturján
    21: "22_Khachaturian_Sabre_Dance.mp3",
    22: "23_Khachaturian_Spartacus.mp3",
    
    # Weiner Leó
    23: "24_Weiner_Fox_Dance.mp3",
    
    # Rimsky-Korsakov
    24: "25_Rimsky_Korsakov_Flight_of_Bumblebee.mp3",
    
    # Mussorgsky
    25: "26_Mussorgsky_Night_on_Bald_Mountain.mp3",
    
    # Prokofjev
    27: "28_Prokofiev_Peter_and_Wolf.mp3",
    
    # Carl Orff
    28: "29_Carl_Orff_Carmina_Burana.mp3",
    
    # Ravel
    29: "30_Ravel_Bolero.mp3",
    
    # Bach
    30: "31_Bach_Brandenburg_Concerto_3.mp3",
    31: "32_Bach_Toccata_Fugue_D_minor.mp3",
    32: "33_Bach_Air_on_G_String.mp3",
    33: "34_Bach_Italian_Concerto.mp3",
    34: "35_Bach_Jesu_Joy.mp3",
    35: "36_Bach_Brandenburg_Concerto_5.mp3",
    36: "37_Bach_Concerto_Two_Violins.mp3",
    37: "38_Bach_Minuet_G_major.mp3",
    
    # Új komolyzenei kérdések
    38: "39_Charpentier_Te_Deum_Prelude.mp3",
    39: "41_Delibes_Lakme_Flower_Duet.mp3",  # Delibes (40-es kérdés)
    40: "40_Offenbach.mp3",  # Offenbach (41-es kérdés)
    41: "42_Vivaldi.mp3",
    42: "43_Mozart.mp3",
    43: "44_Rossini.mp3",
    44: "45_Delibes.mp3",
}

# Komolyzenei zeneszerzők listája
KOMOLYZENE_COMPOSERS = [
    "Dvorak", "Beethoven", "Csajkovszkij", "Handel", "Wagner", 
    "Schubert", "Kodály", "Bartók", "Hacsaturján", "Weiner Leó",
    "Rimsky-Korsakov", "Mussorgsky", "Prokofjev", "Carl Orff", 
    "Ravel", "Bach", "Charpentier", "Delibes", "Offenbach", "Vivaldi", "Mozart", "Rossini"
]

def get_komolyzene_audio_filename(index):
    """Komolyzenei audio fájl nevének lekérése index alapján"""
    return KOMOLYZENE_AUDIO_MAPPING.get(index, None)

def get_komolyzene_audio_path(index):
    """Komolyzenei audio fájl teljes útvonalának lekérése (új mappa)"""
    from pathlib import Path
    filename = get_komolyzene_audio_filename(index)
    if filename:
        # Próbáljuk meg az új mappát először
        audio_dir = Path(__file__).parent / "audio_files_komolyzene_uj"
        audio_path = audio_dir / filename
        if audio_path.exists():
            return audio_path
        # Ha nem található, próbáljuk meg a régi mappát
        audio_dir = Path(__file__).parent / "audio_files_komolyzene"
        return audio_dir / filename
    return None

if __name__ == "__main__":
    print(f"Komolyzenei audio mapping: {len(KOMOLYZENE_AUDIO_MAPPING)} fájl")
    print("Elérhető komolyzenei fájlok:")
    for index, filename in KOMOLYZENE_AUDIO_MAPPING.items():
        print(f"{index}: {filename}") 