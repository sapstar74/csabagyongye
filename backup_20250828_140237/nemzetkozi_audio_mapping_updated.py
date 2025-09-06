#!/usr/bin/env python3
"""
Updated international audio mapping based on actual files in audio_files/nemzetkozi_zenekarok directory
"""

# Nemzetközi zenekarok audio fájl mapping - frissítve a tényleges mappa tartalom alapján
NEMZETKOZI_AUDIO_MAPPING = {
    0: "1_Ariana_Grande.mp3",
    1: "2_Sabrina_Carpenter.mp3",
    2: "3_Olivia_Rodrigo.mp3",
    3: "5_Dua_Lipa.mp3",
    4: "6_Camilla_Cabello.mp3",
    5: "7_Miley_Cyrus.mp3",
    6: "8_Lady_Gaga.mp3",
    7: "9_Billie_Eilish.mp3",
    8: "10_Adele.mp3",
    9: "11_Zaz.mp3",
    10: "13_Emelie_Sande.mp3",
    11: "15_Lilly_Allen.mp3",
    12: "16_Jessie_J..mp3",
    13: "17_Pink.mp3",
    14: "18_Sia.mp3",
    15: "19_Zara_Larsson.mp3",
    16: "20_Beyonce.mp3",
    17: "21_Norah_Jones.mp3",
    18: "22_Janis_Joplin.mp3",
    19: "23_Anne-Marie.mp3",
    20: "24_Bebe_Rexha.mp3",
    21: "25_Taylor_Swift.mp3",
    22: "26_Selena_Gomez.mp3",
    23: "27_Meghan_Trainor.mp3",
    24: "28_21_Pilots.mp3",
    25: "29_Mabel.mp3",
    26: "30_Kesha.mp3",
    27: "31_Christina_Aguilera.mp3",
    28: "31_Ed_Sheeran.mp3",
    29: "32_Shawn_Mendes.mp3",
    30: "34_Alanis_Morissette.mp3",
    31: "35_Adam_Levine.mp3",
    32: "36_Charlie_Puth.mp3",
    33: "37_Sean_Paul.mp3",
    34: "38_Ed_Sheeran.mp3",
    35: "39_James_Arthur.mp3",
    36: "40_Sam_Smith.mp3",
    37: "41_Michael_Buble.mp3",
    38: "42_George_Ezra.mp3",
    39: "43_Keane.mp3",
    40: "44_Justin_Bieber.mp3",
    41: "45_Lukas_Graham.mp3",
    42: "47_Pharrel_Williams.mp3",
    43: "49_Will.i.am.mp3",
    44: "50_Pharrel_Williams.mp3",
    45: "51_Jason_Mraz.mp3",
    46: "52_Harry_Styles.mp3",
    47: "53_Enrique_Iglesias.mp3",
    48: "54_John_Legend.mp3",
    49: "55_James_Blunt.mp3",
    50: "56_The_Weeknd.mp3",
    51: "57_Bruno_Mars.mp3",
    52: "59_One_Direction.mp3",
    53: "60_Maroon_5.mp3",
    54: "61_Imagine_Dragons.mp3",
    55: "62_Bagossy_Brothers_Company.mp3",
    56: "62_My_Chemical_Romance.mp3",
    57: "62_One_Republic.mp3",
    58: "62_One_Republic.mp3.mp3",
    59: "63_Elefánt.mp3",
    60: "63_Maneskin.mp3",
    61: "63_The_Chainsmokers.mp3",
    62: "64_Beatrice.mp3",
    63: "65_Nelly_Furtado.mp3",
    64: "66_Kylie_Minogue.mp3",
    65: "67_Train.mp3",
    66: "69_Bruno_Mars.mp3",
    67: "70_Lady_Gaga.mp3",
    68: "71_Follow_the_flow.mp3",
    69: "71_Maneskin.mp3",
    70: "72_4Street.mp3",
    71: "72_Sam_Smith.mp3",
    72: "73_Bagossy_Brothers.mp3",
    73: "74_Csaknekedkislány.mp3",
    74: "75_Lóci_játszik.mp3",
    75: "76_Galaxisok.mp3",
    76: "77_Parno_Graszt.mp3",
    77: "78_Palya_Bea.mp3",
    78: "79_Bohemian_Betyars.mp3",
    79: "80_Aurevoir.mp3",
    80: "81_Dánielffy.mp3",
    81: "82_Ham_Ko_Ham.mp3",
    82: "83_Carbonfools.mp3",
    83: "84_Zagar.mp3",
    84: "85_Neo.mp3",
    85: "86_Soulwave.mp3",
    86: "88_Quimby.mp3",
    87: "89_Tankcsapda.mp3",
    88: "90_P._Mobil.mp3",
    89: "92_Bonanza_Banzai.mp3",
    90: "93_Korai_Öröm.mp3",
    91: "95_Pearl_Jam.mp3",
    92: "96_Temple_of_the_Dog.mp3",
    93: "97_The_Cranberries.mp3",
    94: "Audioslave - Like a Stone.mp3",
    95: "Queen - '39 (Official Lyric Video).mp3",
    96: "Stakka Bo - Here We Go.mp3",
    97: "The Beatles - For No One.mp3",
    98: "The Rolling Stones - Paint It, Black (Official Lyric Video).mp3",
}

def get_nemzetkozi_audio_filename(index):
    """Visszaadja az audio fájl nevét az index alapján"""
    return NEMZETKOZI_AUDIO_MAPPING.get(index, None)

def get_nemzetkozi_audio_path(index):
    """Visszaadja az audio fájl teljes útvonalát az index alapján"""
    from pathlib import Path
    filename = get_nemzetkozi_audio_filename(index)
    if filename:
        # ÚJ: próbáljuk az új mappából
        audio_dir = Path(__file__).parent / "audio_files/nemzetkozi_zenekarok"
        audio_path = audio_dir / filename
        if audio_path.exists():
            return audio_path
        # Fallback: régi mappa
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