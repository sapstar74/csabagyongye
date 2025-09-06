#!/usr/bin/env python3
"""
Script az original_index mező hozzáadásához a nemzetközi zenekarok kérdésekhez
"""

from topics.nemzetkozi_zenekarok_final_fixed import NEMZETKOZI_ZENEKAROK_QUESTIONS

def add_original_index_to_nemzetkozi():
    """Hozzáadja az original_index mezőt minden nemzetközi zenekarok kérdéshez"""
    
    updated_questions = []
    
    for i, question in enumerate(NEMZETKOZI_ZENEKAROK_QUESTIONS):
        # Új kérdés az original_index mezővel
        updated_question = question.copy()
        updated_question['original_index'] = i
        
        updated_questions.append(updated_question)
        
        print(f"Kérdés {i+1}: original_index: {i}")
    
    return updated_questions

def generate_updated_file():
    """Generálja az frissített fájlt az original_index mezőkkel"""
    
    updated_questions = add_original_index_to_nemzetkozi()
    
    # Generálja a fájl tartalmát
    file_content = '''#!/usr/bin/env python3
"""
Nemzetközi zenekarok kérdések - javított válaszokkal és original_index mezőkkel
"""

NEMZETKOZI_ZENEKAROK_QUESTIONS = [
'''
    
    for i, question in enumerate(updated_questions):
        file_content += '    {\n'
        file_content += f'        "question": "{question["question"]}",\n'
        
        if 'audio_file' in question:
            file_content += f'        "audio_file": "{question["audio_file"]}",\n'
        elif 'spotify_embed' in question:
            file_content += f'        "spotify_embed": "{question["spotify_embed"]}",\n'
        
        file_content += f'        "original_index": {question["original_index"]},\n'
        file_content += f'        "options": {question["options"]},\n'
        file_content += f'        "correct": "{question["correct"]}",\n'
        file_content += f'        "explanation": "{question["explanation"]}",\n'
        file_content += f'        "topic": "{question["topic"]}",\n'
        
        if i < len(updated_questions) - 1:
            file_content += '    },\n'
        else:
            file_content += '    }\n'
    
    file_content += ']\n'
    
    # Írja ki a fájlt
    with open('topics/nemzetkozi_zenekarok_final_fixed_with_index.py', 'w', encoding='utf-8') as f:
        f.write(file_content)
    
    print(f"\n✅ Frissített fájl generálva: topics/nemzetkozi_zenekarok_final_fixed_with_index.py")
    print(f"📊 Összesen {len(updated_questions)} kérdés frissítve original_index mezővel")

if __name__ == "__main__":
    generate_updated_file() 