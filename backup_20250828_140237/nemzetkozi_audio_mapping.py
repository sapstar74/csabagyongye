#!/usr/bin/env python3
"""
Clean international audio mapping - magyar zenekarok nélkül
"""

# Nemzetközi zenekarok audio fájl mapping - tisztítva magyar zenekarok nélkül
NEMZETKOZI_AUDIO_MAPPING = {
    0: "10_Adele.mp3",
    1: "11_Zaz.mp3",
    2: "12_Ellie_Goulding.mp3",
    3: "13_Emelie_Sande.mp3",
    4: "14_Katy_Perry.mp3",
    5: "15_Lilly_Allen.mp3",
    6: "16_Jessie_J..mp3",
    7: "17_Pink.mp3",
    8: "18_Sia.mp3",
    9: "19_Zara_Larsson.mp3",
    10: "1_Ariana_Grande.mp3",
    11: "20_Beyonce.mp3",
    12: "21_Norah_Jones.mp3",
    13: "22_Janis_Joplin.mp3",
    14: "23_Anne-Marie.mp3",
    15: "24_Bebe_Rexha.mp3",
    16: "25_Taylor_Swift.mp3",
    17: "26_Selena_Gomez.mp3",
    18: "28_21_Pilots.mp3",
    19: "29_Lana_del_Rey.mp3",
    20: "2_Ariana_Grande.mp3",
    21: "30_Mabel.mp3",
    22: "31_Sabrina_Carpenter.mp3",
    23: "32_Kesha.mp3",
    24: "33_Christina_Aguilera.mp3",
    25: "34_Megan_Trainor.mp3",
    26: "35_Dua_Lipa.mp3",
    27: "36_Bruno_Mars.mp3",
    28: "37_Justin_Bieber.mp3",
    29: "38_Lana_del_Rey.mp3",
    30: "39_Ed_Sheeran.mp3",
    31: "3_Ariana_Grande.mp3",
    32: "40_Imagine_Dragons.mp3",
    33: "41_One_Republic.mp3",
    34: "42_The_Chainsmokers.mp3",
    35: "43_Coldplay.mp3",
    36: "44_Maroon_5.mp3",
    37: "45_One_Direction.mp3",
    38: "46_Shawn_Mendes.mp3",
    39: "47_The_Weeknd.mp3",
    40: "48_Post_Malone.mp3",
    41: "49_Khalid.mp3",
    42: "4_Ariana_Grande.mp3",
    43: "50_Billie_Eilish.mp3",
    44: "51_Halsey.mp3",
    45: "52_Camila_Cabello.mp3",
    46: "53_Dua_Lipa.mp3",
    47: "54_Ava_Max.mp3",
    48: "55_Doja_Cat.mp3",
    49: "56_Olivia_Rodrigo.mp3",
    50: "57_Lil_Nas_X.mp3",
    51: "58_Doja_Cat.mp3",
    52: "59_The_Kid_Laroi.mp3",
    53: "5_Ariana_Grande.mp3",
    54: "60_Glass_Animals.mp3",
    55: "61_Måneskin.mp3",
    56: "62_Imagine_Dragons.mp3",
    57: "63_The_Weeknd.mp3",
    58: "64_Ed_Sheeran.mp3",
    59: "65_Justin_Bieber.mp3",
    60: "66_Dua_Lipa.mp3",
    61: "67_Olivia_Rodrigo.mp3",
    62: "68_Lil_Nas_X.mp3",
    63: "69_Doja_Cat.mp3",
    64: "6_Ariana_Grande.mp3",
    65: "70_The_Kid_Laroi.mp3",
    66: "71_Glass_Animals.mp3",
    67: "72_Måneskin.mp3",
    68: "73_Imagine_Dragons.mp3",
    69: "74_The_Weeknd.mp3",
    70: "75_Ed_Sheeran.mp3",
    71: "76_Justin_Bieber.mp3",
    72: "77_Dua_Lipa.mp3",
    73: "78_Olivia_Rodrigo.mp3",
    74: "79_Lil_Nas_X.mp3",
    75: "7_Ariana_Grande.mp3",
    76: "80_Doja_Cat.mp3",
    77: "81_The_Kid_Laroi.mp3",
    78: "82_Glass_Animals.mp3",
    79: "83_Måneskin.mp3",
    80: "84_Imagine_Dragons.mp3",
    81: "85_The_Weeknd.mp3",
    82: "86_Ed_Sheeran.mp3",
    83: "87_Justin_Bieber.mp3",
    84: "88_Dua_Lipa.mp3",
    85: "89_Olivia_Rodrigo.mp3",
    86: "8_Ariana_Grande.mp3",
    87: "90_Lil_Nas_X.mp3",
    88: "91_Doja_Cat.mp3",
    89: "92_The_Kid_Laroi.mp3",
    90: "93_Glass_Animals.mp3",
    91: "94_Måneskin.mp3",
    92: "95_Imagine_Dragons.mp3",
    93: "96_The_Weeknd.mp3",
    94: "97_Ed_Sheeran.mp3",
    95: "98_Justin_Bieber.mp3",
    96: "99_Dua_Lipa.mp3",
    97: "9_Ariana_Grande.mp3",
    98: "audio_file_placeholder.mp3"
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
    print(f"Tisztított mapping bejegyzések száma: {len(NEMZETKOZI_AUDIO_MAPPING)}")
    print(f"Index 0: {get_nemzetkozi_audio_path(0)}")
    print(f"Index 1: {get_nemzetkozi_audio_path(1)}")
    print(f"Index 10: {get_nemzetkozi_audio_path(10)}")
    print(f"Index 99: {get_nemzetkozi_audio_path(99)}") # Nem létező index 