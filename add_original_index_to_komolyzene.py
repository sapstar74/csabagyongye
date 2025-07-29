#!/usr/bin/env python3
"""
Script a komolyzene kérdések original_index mezőinek hozzáadásához
"""

from topics.komolyzene_uj import KOMOLYZENE_QUESTIONS

def add_original_index_to_komolyzene():
    """Hozzáadja az original_index mezőt a komolyzene kérdésekhez"""
    
    # Komolyzene audio mapping alapján az indexek
    komolyzene_indices = {
        '1_Dvorak_New_World_Symphony.mp3': 0,
        '2_Dvorak_Humoresque.mp3': 1,
        '3_Dvorak_Symphony_8.mp3': 2,
        '4_Beethoven_Symphony_5.mp3': 3,
        '5_Beethoven_Moonlight_Sonata.mp3': 4,
        '6_Beethoven_Ode_to_Joy.mp3': 5,
        '7_Tchaikovsky_Nutcracker.mp3': 6,
        '8_Tchaikovsky_Swan_Lake.mp3': 7,
        '9_Tchaikovsky_Piano_Concerto_1.mp3': 8,
        '10_Handel_Rinaldo.mp3': 9,
        '11_Handel_Minuet_B_flat.mp3': 10,
        '12_Handel_Keyboard_Suite_D_minor.mp3': 11,
        '13_Wagner_Ride_of_Valkyries.mp3': 12,
        '14_Wagner_Lohengrin_Wedding_March.mp3': 13,
        '15_Schubert_Ave_Maria.mp3': 14,
        '16_Beethoven_Ode_to_Joy_2.mp3': 15,
        '17_Kodaly_Hary_Janos.mp3': 16,
        '18_Kodaly_Kallai_Kettos.mp3': 17,
        '19_Kodaly_Adagio.mp3': 18,
        '20_Bartok_Bluebeard_Castle.mp3': 19,
        '21_Bartok_Miraculous_Mandarin.mp3': 20,
        '22_Khachaturian_Sabre_Dance.mp3': 21,
        '23_Khachaturian_Spartacus.mp3': 22,
        '24_Weiner_Fox_Dance.mp3': 23,
        '25_Rimsky_Korsakov_Flight_of_Bumblebee.mp3': 24,
        '26_Mussorgsky_Night_on_Bald_Mountain.mp3': 25,
        '27_Schubert_Trout_Quintet.mp3': 26,
        '28_Prokofiev_Peter_and_Wolf.mp3': 27,
        '29_Carl_Orff_Carmina_Burana.mp3': 28,
        '30_Ravel_Bolero.mp3': 29,
        '31_Bach_Brandenburg_Concerto_3.mp3': 30,
        '32_Bach_Toccata_Fugue_D_minor.mp3': 31,
        '33_Bach_Air_on_G_String.mp3': 32,
        '34_Bach_Italian_Concerto.mp3': 33,
        '35_Bach_Jesu_Joy.mp3': 34,
        '36_Bach_Brandenburg_Concerto_5.mp3': 35,
        '37_Bach_Concerto_Two_Violins.mp3': 36,
        '38_Bach_Minuet_G_major.mp3': 37,
    }
    
    updated_questions = []
    
    for i, question in enumerate(KOMOLYZENE_QUESTIONS):
        audio_file = question.get('audio_file', '')
        original_index = komolyzene_indices.get(audio_file, i)
        
        # Új kérdés az original_index mezővel
        updated_question = question.copy()
        updated_question['original_index'] = original_index
        
        updated_questions.append(updated_question)
        
        print(f"Kérdés {i+1}: {audio_file} -> original_index: {original_index}")
    
    return updated_questions

def save_updated_komolyzene_questions(questions):
    """Mentés az új komolyzene kérdéseket"""
    
    content = '''#!/usr/bin/env python3
"""
Komolyzenei kérdések audio fájlokkal - original_index mezőkkel
"""

KOMOLYZENE_QUESTIONS = [
'''
    
    for question in questions:
        content += f'''    {{
        'question': '{question['question']}',
        'options': {question['options']},
        'correct': {question['correct']},
        'explanation': '{question['explanation']}',
        'audio_file': '{question['audio_file']}',
        'topic': '{question['topic']}',
        'original_index': {question['original_index']}
    }},
'''
    
    content += ''']

if __name__ == "__main__":
    print(f"Komolyzene kérdések száma: {len(KOMOLYZENE_QUESTIONS)}")
    print("Első kérdés:", KOMOLYZENE_QUESTIONS[0]['question'])
    print("Audio fájl:", KOMOLYZENE_QUESTIONS[0]['audio_file'])
    print("Original index:", KOMOLYZENE_QUESTIONS[0]['original_index'])
'''
    
    with open('topics/komolyzene_uj_fixed.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Frissített komolyzene kérdések mentve: topics/komolyzene_uj_fixed.py")
    print(f"📊 Összesen {len(questions)} kérdés frissítve")

if __name__ == "__main__":
    print("🔧 Komolyzene kérdések original_index mezőinek hozzáadása...")
    
    updated_questions = add_original_index_to_komolyzene()
    save_updated_komolyzene_questions(updated_questions)
    
    print("\n✅ Kész! A komolyzene kérdések most már tartalmaznak original_index mezőket.") 