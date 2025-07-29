#!/usr/bin/env python3
"""
Complete international audio mapping - all actual international files
"""

# Nemzetközi zenekarok audio fájl mapping - összes valóságos nemzetközi fájllal
NEMZETKOZI_AUDIO_MAPPING = {
    1: "1_Ariana_Grande.mp3",
    2: "2_Sabrina_Carpenter.mp3",
    3: "3_Olivia_Rodrigo.mp3",
    4: "4_Rihanna.mp3",
    5: "5_Dua_Lipa.mp3",
    6: "6_Camilla_Cabello.mp3",
    7: "7_Miley_Cyrus.mp3",
    8: "8_Lady_Gaga.mp3",
    9: "9_Billie_Eilish.mp3",
    10: "10_Adele.mp3",
    11: "11_Zaz.mp3",
    12: "12_Ellie_Goulding.mp3",
    13: "13_Emelie_Sande.mp3",
    14: "14_Katy_Perry.mp3",
    15: "15_Lilly_Allen.mp3",
    16: "16_Jessie_J..mp3",
    17: "17_Pink.mp3",
    18: "18_Sia.mp3",
    19: "19_Zara_Larsson.mp3",
    20: "20_Beyonce.mp3",
    21: "21_Norah_Jones.mp3",
    22: "22_Janis_Joplin.mp3",
    23: "23_Anne-Marie.mp3",
    24: "24_Bebe_Rexha.mp3",
    25: "25_Taylor_Swift.mp3",
    26: "26_Selena_Gomez.mp3",
    27: "27_Meghan_Trainor.mp3",
    28: "28_Lana_del_Rey.mp3",
    29: "29_Mabel.mp3",
    30: "30_Kesha.mp3",
    31: "31_Christina_Aguilera.mp3",
    32: "31_Ed_Sheeran.mp3",
    33: "32_Shawn_Mendes.mp3",
    34: "34_Alanis_Morissette.mp3",
    35: "35_Adam_Levine.mp3",
    36: "36_Charlie_Puth.mp3",
    37: "37_Sean_Paul.mp3",
    38: "38_Ed_Sheeran.mp3",
    39: "39_James_Arthur.mp3",
    40: "40_Sam_Smith.mp3",
    41: "41_Michael_Buble.mp3",
    42: "42_George_Ezra.mp3",
    43: "43_Keane.mp3",
    44: "44_Justin_Bieber.mp3",
    45: "45_Lukas_Graham.mp3",
    46: "46_James_Bay.mp3",
    47: "47_Pharrel_Williams.mp3",
    48: "48_FloRida.mp3",
    49: "49_Will.i.am.mp3",
    50: "50_Pharell_Williams.mp3",
    51: "51_Jason_Mraz.mp3",
    52: "52_Harry_Styles.mp3",
    53: "53_Enrique_Iglesias.mp3",
    54: "54_John_Legend.mp3",
    55: "55_James_Blunt.mp3",
    56: "56_The_Weeknd.mp3",
    57: "57_Bruno_Mars.mp3",
    58: "58_Robbie_Williams.mp3",
    59: "59_One_Direction.mp3",
    60: "60_Maroon_5.mp3",
    61: "61_Imagine_Dragons.mp3",
    62: "62_My_Chemical_Romance.mp3",
    63: "63_The_Chainsmokers.mp3",
    64: "64_Taylor_Swift.mp3",
    65: "65_Nelly_Furtado.mp3",
    66: "66_Kylie_Minogue.mp3",
    67: "67_Train.mp3",
    69: "69_Bruno_Mars.mp3",
    70: "70_Lady_Gaga.mp3",
    71: "71_Maneskin.mp3",
    72: "72_Sam_Smith.mp3",
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
    print(f"Teljes mapping bejegyzések száma: {len(NEMZETKOZI_AUDIO_MAPPING)}")
    print(f"Index 0: {get_nemzetkozi_audio_path(0)}")
    print(f"Index 1: {get_nemzetkozi_audio_path(1)}")
    print(f"Index 10: {get_nemzetkozi_audio_path(10)}")
