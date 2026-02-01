#!/usr/bin/env python3
"""
Komolyzenei audio fájlok mapping-je
"""

# Komolyzenei audio fájlok mapping-je - frissítve a valóságos fájlok alapján
KOMOLYZENE_AUDIO_MAPPING = {
    # Dvorak
    0: "1. Dvorak - New World Symphony.mp3",
    1: "2. Dvorak - Humoresque.mp3",
    2: "3. Dvorak - Symphony 8.mp3",

    # Beethoven
    3: "4. Beethoven - Symphony 5.mp3",
    4: "5. Beethoven - Moonlight Sonata.mp3",
    5: "6. Beethoven - Ode to Joy.mp3",
    15: "16. Beethoven - Ode to Joy 2.mp3",

    # Csajkovszkij
    6: "7. Tchaikovsky - Nutcracker.mp3",
    7: "8. Tchaikovsky - Swan Lake.mp3",
    8: "9. Tchaikovsky - Piano Concerto 1.mp3",

    # Handel
    9: "10. Handel - Rinaldo.mp3",
    10: "11. Handel - Minuet B flat.mp3",
    11: "12. Handel - Keyboard Suite D minor.mp3",

    # Wagner
    12: "13. Wagner - Ride of Valkyries.mp3",
    13: "14. Wagner - Lohengrin Wedding March.mp3",

    # Schubert
    14: "15. Schubert - Ave Maria.mp3",
    26: "27. Schubert - Trout Quintet.mp3",

    # Kodály
    16: "17. Kodaly - Hary Janos.mp3",
    17: "18. Kodaly - Kallai Kettos.mp3",
    18: "19. Kodaly - Adagio.mp3",

    # Bartók
    19: "20. Bartok - Bluebeard Castle.mp3",
    20: "21. Bartok - Miraculous Mandarin.mp3",

    # Hacsaturján
    21: "22. Khachaturian - Sabre Dance.mp3",
    22: "23. Khachaturian - Spartacus.mp3",

    # Weiner Leó
    23: "24. Weiner - Fox Dance.mp3",

    # Rimsky-Korsakov
    24: "25. Rimsky Korsakov - Flight of Bumblebee.mp3",

    # Mussorgsky
    25: "26. Mussorgsky - Night on Bald Mountain.mp3",

    # Prokofjev
    27: "28. Prokofiev - Peter and Wolf.mp3",

    # Carl Orff
    28: "29. Carl Orff - Carmina Burana.mp3",

    # Ravel
    29: "30. Ravel - Bolero.mp3",

    # Bach
    30: "31. Bach - Brandenburg Concerto 3.mp3",
    31: "32. Bach - Toccata Fugue D minor.mp3",
    32: "33. Bach - Air on G String.mp3",
    33: "34. Bach - Italian Concerto.mp3",
    34: "35. Bach - Jesu Joy.mp3",
    35: "36. Bach - Brandenburg Concerto 5.mp3",
    36: "37. Bach - Concerto Two Violins.mp3",
    37: "38. Bach - Minuet G major.mp3",

    # Új komolyzenei kérdések
    38: "39. Charpentier - Te Deum Prelude.mp3",
    39: "40. Delibes - Lakme Flower Duet.mp3",
    40: "41. Offenbach - Offenbach.mp3",
    41: "42. Vivaldi - Four Seasons.mp3",
    42: "43. Mozart - Mozart.mp3",
    43: "44. Rossini - Rossini.mp3",
    44: "45. Delibes - Sylvia - Pizzicato.mp3",
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
    """Komolyzenei audio fájl teljes útvonalának lekérése"""
    from pathlib import Path
    filename = get_komolyzene_audio_filename(index)
    if filename:
        audio_dir = Path(__file__).parent / "audio_files/komolyzene"
        audio_path = audio_dir / filename
        if audio_path.exists():
            return audio_path
        return audio_path
    return None

if __name__ == "__main__":
    print(f"Komolyzenei audio mapping: {len(KOMOLYZENE_AUDIO_MAPPING)} fájl")
    print("Elérhető komolyzenei fájlok:")
    for index, filename in KOMOLYZENE_AUDIO_MAPPING.items():
        print(f"{index}: {filename}") 