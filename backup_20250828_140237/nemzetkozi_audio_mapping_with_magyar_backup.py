#!/usr/bin/env python3
"""
Updated international audio mapping based on actual files in audio_files directory
"""

# Nemzetközi zenekarok audio fájl mapping - frissítve a tényleges mappa tartalom alapján
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
    19: "28_Lana_del_Rey.mp3",
    20: "29_Mabel.mp3",
    21: "2_Sabrina_Carpenter.mp3",
    22: "30_Kesha.mp3",
    23: "31_Christina_Aguilera.mp3",
    24: "31_Ed_Sheeran.mp3",
    25: "32_Nelly_Furtado.mp3",
    26: "32_Shawn_Mendes.mp3",
    27: "33_Kylie_Minogue.mp3",
    28: "34_Alanis_Morissette.mp3",
    29: "35_Adam_Levine.mp3",
    30: "36_Charlie_Puth.mp3",
    31: "37_Sean_Paul.mp3",
    32: "38_Ed_Sheeran.mp3",
    33: "39_James_Arthur.mp3",
    34: "3_Olivia_Rodrigo.mp3",
    35: "40_Sam_Smith.mp3",
    36: "41_Michael_Buble.mp3",
    37: "42_George_Ezra.mp3",
    38: "43_Keane.mp3",
    39: "44_Justin_Bieber.mp3",
    40: "45_Lukas_Graham.mp3",
    41: "46_James_Bay.mp3",
    42: "47_Pharrel_Williams.mp3",
    43: "48_FloRida.mp3",
    44: "49_Will.i.am.mp3",
    45: "4_Rihanna.mp3",
    46: "52_Harry_Styles.mp3",
    47: "53_Enrique_Iglesias.mp3",
    48: "54_John_Legend.mp3",
    49: "55_James_Blunt.mp3",
    50: "56_The_Weeknd.mp3",
    51: "57_Bruno_Mars.mp3",
    52: "58_Robbie_Williams.mp3",
    53: "59_One_Direction.mp3",
    54: "5_Dua_Lipa.mp3",
    55: "61_Imagine_Dragons.mp3",
    56: "61_Maneskin.mp3",
    57: "62_Bagossy_Brothers_Company.mp3",
    58: "62_My_Chemical_Romance.mp3",
    59: "62_One_Republic.mp3.mp3",
    60: "63_Elefánt.mp3",
    61: "64_The_Chainsmokers.mp3",
    62: "66_Taylor_Swift.mp3",
    63: "67_Train.mp3",
    64: "69_Bruno_Mars.mp3",
    65: "6_Camilla_Cabello.mp3",
    66: "71_Follow_the_flow.mp3",
    67: "72_4Street.mp3",
    68: "73_Bagossy_Brothers.mp3",
    69: "75_Lóci_játszik.mp3",
    70: "76_Galaxisok.mp3",
    71: "77_Parno_Graszt.mp3",
    72: "78_Palya_Bea.mp3",
    73: "79_Bohemian_Betyars.mp3",
    74: "7_Miley_Cyrus.mp3",
    75: "80_Aurevoir.mp3",
    76: "81_Dánielffy.mp3",
    77: "82_Ham_Ko_Ham.mp3",
    78: "83_Carbonfools.mp3",
    79: "84_Zagar.mp3",
    80: "85_Neo.mp3",
    81: "86_Soulwave.mp3",
    82: "88_Quimby.mp3",
    83: "89_Tankcsapda.mp3",
    84: "8_Lady_Gaga.mp3",
    85: "90_P._Mobil.mp3",
    86: "91_Republic.mp3",
    87: "92_Bonanza_Banzai.mp3",
    88: "93_Korai_Öröm.mp3",
    89: "9_Billie_Eilish.mp3",
    90: "temp_track_18TETrZMZTGax2T10xN4xY.mp3.mp3",
    91: "temp_track_2A7qdr3UNP9Pxjcxa5Jj53.mp3.mp3",
    92: "temp_track_2Sbb5o2R6zci4L0xEQhsvK.mp3.mp3",
    93: "temp_track_4HlS1s8sYBF5eVYbBkp6Be.mp3.mp3",
    94: "temp_track_4Nd5HJn4EExnLmHtClk4QV.mp3.mp3",
    95: "temp_track_5C40d7tzYgdyKFCjc1mEWg.mp3.mp3",
    96: "temp_track_6jZj45D2jdR6fMEb58TlSc.mp3.mp3",
    97: "temp_track_6srU3wlimYXpxBNoCabQGi.mp3.mp3",
    98: "temp_track_7K0WEkSBSMAHgyvOnWLJzo.mp3.mp3",
}

def get_nemzetkozi_audio_filename(index):
    """Visszaadja az audio fájl nevét az index alapján"""
    return NEMZETKOZI_AUDIO_MAPPING.get(index, None)

def get_nemzetkozi_audio_path(index):
    """Visszaadja az audio fájl teljes útvonalát az index alapján"""
    from pathlib import Path
    filename = get_nemzetkozi_audio_filename(index)
    if filename:
        audio_dir = Path(__file__).parent / "audio_files"
        return audio_dir / filename
    return None

# Debug: kiírjuk az összes elérhető fájlt
if __name__ == "__main__":
    print(f"Összes mapping bejegyzés: {len(NEMZETKOZI_AUDIO_MAPPING)}")
    print("Első 10 fájl:")
    for i in range(10):
        filename = NEMZETKOZI_AUDIO_MAPPING.get(i)
        if filename:
            print(f"  {i}: {filename}") 