#!/usr/bin/env python3
"""
Komolyzenei kérdések audio fájlokkal - original_index mezőkkel
"""

KOMOLYZENE_QUESTIONS = [
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: IX. Új világ szimfónia',
        'audio_file': '1_Dvorak_New_World_Symphony.mp3',
        'original_index': 0,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: Humoresque',
        'audio_file': '2_Dvorak_Humoresque.mp3',
        'original_index': 1,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: 8. G-dúr szimfónia',
        'audio_file': '3_Dvorak_Symphony_8.mp3',
        'original_index': 2,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: V. Szimfónia - A sors szimfónia',
        'audio_file': '4_Beethoven_Symphony_5.mp3',
        'original_index': 3,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Holdvilág szonáta - Mondscheinsonate',
        'audio_file': '5_Beethoven_Moonlight_Sonata.mp3',
        'original_index': 4,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Ode to Joy - 9. szimfónia',
        'audio_file': '6_Beethoven_Ode_to_Joy.mp3',
        'original_index': 5,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: Diótörő - Tánc a cukorkák hercegnőjéről',
        'audio_file': '7_Tchaikovsky_Nutcracker.mp3',
        'original_index': 6,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: Hattyúk tava - Swan Lake',
        'audio_file': '8_Tchaikovsky_Swan_Lake.mp3',
        'original_index': 7,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: 1. Zongoraverseny',
        'audio_file': '9_Tchaikovsky_Piano_Concerto_1.mp3',
        'original_index': 8,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: Rinaldo',
        'audio_file': '10_Handel_Rinaldo.mp3',
        'original_index': 9,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: IV. B-dúr menüett',
        'audio_file': '11_Handel_Minuet_B_flat.mp3',
        'original_index': 10,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: Keyboard Suite in D minor',
        'audio_file': '12_Handel_Keyboard_Suite_D_minor.mp3',
        'original_index': 11,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Wagner', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Wagner: A Valkűrök bevonulása',
        'audio_file': '13_Wagner_Ride_of_Valkyries.mp3',
        'original_index': 12,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Wagner', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Wagner: Lohengrin - Here comes the Bride',
        'audio_file': '14_Wagner_Lohengrin_Wedding_March.mp3',
        'original_index': 13,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Schubert', 'Wagner', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Schubert: Ave Maria',
        'audio_file': '15_Schubert_Ave_Maria.mp3',
        'original_index': 14,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Wagner', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Ode to Joy - 9. szimfónia',
        'audio_file': '16_Beethoven_Ode_to_Joy_2.mp3',
        'original_index': 15,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Háry János',
        'audio_file': '17_Kodaly_Hary_Janos.mp3',
        'original_index': 16,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Kállai kettős',
        'audio_file': '18_Kodaly_Kallai_Kettos.mp3',
        'original_index': 17,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Adagio',
        'audio_file': '19_Kodaly_Adagio.mp3',
        'original_index': 18,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Kékszakállú herceg vára',
        'audio_file': '20_Bartok_Bluebeard_Castle.mp3',
        'original_index': 19,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Csodálatos mandarin',
        'audio_file': '21_Bartok_Miraculous_Mandarin.mp3',
        'original_index': 20,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Hacsaturján', 'Bartók', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Hacsaturján: Kartánc',
        'audio_file': '22_Khachaturian_Sabre_Dance.mp3',
        'original_index': 21,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Hacsaturján', 'Bartók', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Hacsaturján: Spartacus / Onedin',
        'audio_file': '23_Khachaturian_Spartacus.mp3',
        'original_index': 22,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Weiner Leó', 'Kodály', 'Bartók', 'Liszt'],
        'correct': 0,
        'explanation': 'Weiner Leó: Rókatánc',
        'audio_file': '24_Weiner_Fox_Dance.mp3',
        'original_index': 23,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Rimsky-Korsakov', 'Csajkovszkij', 'Mussorgsky', 'Bach'],
        'correct': 0,
        'explanation': 'Rimsky-Korsakov: Bumblebee',
        'audio_file': '25_Rimsky_Korsakov_Flight_of_Bumblebee.mp3',
        'original_index': 24,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Mussorgsky', 'Rimsky-Korsakov', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Mussorgsky: Éjszaka a hegyen',
        'audio_file': '26_Mussorgsky_Night_on_Bald_Mountain.mp3',
        'original_index': 25,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Schubert', 'Mozart', 'Beethoven', 'Bach'],
        'correct': 0,
        'explanation': 'Schubert: Pisztráng ötös',
        'audio_file': '27_Schubert_Trout_Quintet.mp3',
        'original_index': 26,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Prokofjev', 'Shostakovich', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Prokofjev: Péter és a farkas',
        'audio_file': '28_Prokofiev_Peter_and_Wolf.mp3',
        'original_index': 27,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Carl Orff', 'Bach', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Carl Orff: Carmina Burana',
        'audio_file': '29_Carl_Orff_Carmina_Burana.mp3',
        'original_index': 28,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Ravel', 'Debussy', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Ravel: Bolero',
        'audio_file': '30_Ravel_Bolero.mp3',
        'original_index': 29,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Brandenburgi versenyek - 3. verseny',
        'audio_file': '31_Bach_Brandenburg_Concerto_3.mp3',
        'original_index': 30,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Toccata és fúga d-moll',
        'audio_file': '32_Bach_Toccata_Fugue_D_minor.mp3',
        'original_index': 31,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Air on G-string',
        'audio_file': '33_Bach_Air_on_G_String.mp3',
        'original_index': 32,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Italian Concerto',
        'audio_file': '34_Bach_Italian_Concerto.mp3',
        'original_index': 33,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Jesu, Joy of Man',
        'audio_file': '35_Bach_Jesu_Joy.mp3',
        'original_index': 34,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Brandenburg Concerto No. 5',
        'audio_file': '36_Bach_Brandenburg_Concerto_5.mp3',
        'original_index': 35,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Vivace',
        'audio_file': '37_Bach_Concerto_Two_Violins.mp3',
        'original_index': 36,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: G-dúr menüett',
        'audio_file': '38_Bach_Minuet_G_major.mp3',
        'original_index': 37,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Charpentier', 'Handel', 'Bach', 'Vivaldi'],
        'correct': 0,
        'explanation': 'Charpentier: Te Deum Prelude',
        'audio_file': '39_Charpentier_Te_Deum_Prelude.mp3',
        'original_index': 38,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Delibes', 'Bizet', 'Gounod', 'Offenbach'],
        'correct': 0,
        'explanation': 'Delibes: Lakmé - Flower Duet',
        'audio_file': '41_Delibes_Lakme_Flower_Duet.mp3',
        'original_index': 39,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Offenbach', 'Bizet', 'Gounod', 'Delibes'],
        'correct': 0,
        'explanation': 'Offenbach: YouTube klasszikus',
        'audio_file': '40_Offenbach.mp3',
        'original_index': 40,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Vivaldi', 'Bach', 'Handel', 'Corelli'],
        'correct': 0,
        'explanation': 'Vivaldi: Négy évszak (YouTube)',
        'audio_file': '42_Vivaldi.mp3',
        'original_index': 41,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Mozart', 'Haydn', 'Beethoven', 'Schubert'],
        'correct': 0,
        'explanation': 'Mozart: YouTube klasszikus',
        'audio_file': '43_Mozart.mp3',
        'original_index': 42,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Rossini', 'Verdi', 'Donizetti', 'Bellini'],
        'correct': 0,
        'explanation': 'Rossini: YouTube klasszikus',
        'audio_file': '44_Rossini.mp3',
        'original_index': 43,
        'topic': 'komolyzene'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Delibes', 'Bizet', 'Gounod', 'Offenbach'],
        'correct': 0,
        'explanation': 'Delibes: YouTube klasszikus',
        'audio_file': '45_Delibes.mp3',
        'original_index': 44,
        'topic': 'komolyzene'
    },
]

if __name__ == "__main__":
    print(f"Komolyzenei kérdések száma: {len(KOMOLYZENE_QUESTIONS)}")
    print("Audio fájlokkal és original_index mezőkkel:")
    for i, q in enumerate(KOMOLYZENE_QUESTIONS):
        print(f"{i+1}. {q['explanation']} - {q['audio_file']} (index: {q.get('original_index', 'N/A')})")
