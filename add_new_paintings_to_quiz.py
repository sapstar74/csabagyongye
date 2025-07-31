#!/usr/bin/env python3
"""
Új festmények hozzáadása a quiz alkalmazáshoz
Automatikusan azonosítja az új képeket és létrehozza a kérdéseket
"""

import os
import re
from pathlib import Path

def extract_painting_info(filename):
    """Képfájl nevéből kinyeri a festmény és festő információit"""
    # Eltávolítjuk a .jpg kiterjesztést
    name = filename.replace('.jpg', '')
    
    # Különböző formátumok kezelése
    patterns = [
        # "festmény-neve---festő-neve-év.jpg" formátum
        r'^(.+?)---(.+?)-(\d{4})$',
        # "festmény-neve---festő-neve.jpg" formátum (év nélkül)
        r'^(.+?)---(.+?)$',
        # "festmény-neve-festő-neve-év.jpg" formátum
        r'^(.+?)-(.+?)-(\d{4})$',
        # "festmény-neve-festő-neve.jpg" formátum
        r'^(.+?)-(.+?)$'
    ]
    
    for pattern in patterns:
        match = re.match(pattern, name)
        if match:
            if len(match.groups()) == 3:
                painting_name, artist_name, year = match.groups()
                return painting_name.replace('-', ' ').title(), artist_name.replace('-', ' ').title(), year
            else:
                painting_name, artist_name = match.groups()
                return painting_name.replace('-', ' ').title(), artist_name.replace('-', ' ').title(), None
    
    # Ha nem találunk mintát, visszaadjuk a fájlnevet
    return name.replace('-', ' ').title(), "Ismeretlen festő", None

def get_existing_quiz_images():
    """Lekéri a jelenlegi quiz-ben használt képeket"""
    quiz_file = "topics/festmenyek.py"
    existing_images = set()
    
    if os.path.exists(quiz_file):
        with open(quiz_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Keresünk image_file sorokat
            matches = re.findall(r"'image_file':\s*'([^']+)'", content)
            existing_images.update(matches)
    
    return existing_images

def get_all_image_files():
    """Lekéri az összes képfájlt a festmény_képek mappából"""
    image_dir = Path("festmény_képek")
    image_files = []
    
    if image_dir.exists():
        for file in image_dir.glob("*.jpg"):
            image_files.append(file.name)
    
    return image_files

def create_quiz_question(painting_name, artist_name, year, filename):
    """Létrehoz egy quiz kérdést egy festményhez"""
    
    # Téves válaszok generálása (ezeket később manuálisan kell finomítani)
    false_artists = [
        "Claude Monet", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci",
        "Rembrandt", "Johannes Vermeer", "Sandro Botticelli", "Edvard Munch",
        "Salvador Dalí", "Gustav Klimt", "Pierre-Auguste Renoir", "Édouard Manet",
        "Raphael", "Michelangelo", "Caravaggio", "Titian", "El Greco",
        "Francisco Goya", "Paul Cézanne", "Henri Matisse", "Wassily Kandinsky",
        "Frida Kahlo", "Andy Warhol", "Jackson Pollock", "René Magritte"
    ]
    
    # Eltávolítjuk a helyes választ a téves válaszokból
    false_artists = [a for a in false_artists if a != artist_name]
    
    # 3 véletlenszerű téves választ választunk
    import random
    selected_false = random.sample(false_artists, 3)
    
    # Válaszlehetőségek összeállítása (helyes válasz + 3 téves)
    options = selected_false + [artist_name]
    random.shuffle(options)
    
    # Helyes válasz indexének meghatározása
    correct_index = options.index(artist_name)
    
    # Magyarázat összeállítása
    explanation = f"{painting_name}"
    if year:
        explanation += f" - {artist_name} ({year})"
    else:
        explanation += f" - {artist_name}"
    
    return {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': options,
        'correct': correct_index,
        'explanation': explanation,
        'image_file': filename,
        'topic': 'festmények'
    }

def main():
    """Fő függvény az új festmények hozzáadásához"""
    
    print("🎨 Új festmények keresése...")
    
    # Meglévő képek lekérése
    existing_images = get_existing_quiz_images()
    print(f"Jelenlegi quiz képek: {len(existing_images)}")
    
    # Összes képfájl lekérése
    all_images = get_all_image_files()
    print(f"Összes képfájl: {len(all_images)}")
    
    # Új képek azonosítása
    new_images = [img for img in all_images if img not in existing_images]
    print(f"Új képek: {len(new_images)}")
    
    if not new_images:
        print("✅ Nincs új kép hozzáadandó!")
        return
    
    print("\n🆕 Új képek:")
    new_questions = []
    
    for filename in new_images:
        painting_name, artist_name, year = extract_painting_info(filename)
        print(f"  - {filename}")
        print(f"    Festmény: {painting_name}")
        print(f"    Festő: {artist_name}")
        if year:
            print(f"    Év: {year}")
        print()
        
        # Quiz kérdés létrehozása
        question = create_quiz_question(painting_name, artist_name, year, filename)
        new_questions.append(question)
    
    # Új kérdések hozzáadása a meglévő fájlhoz
    if new_questions:
        quiz_file = "topics/festmenyek.py"
        
        if os.path.exists(quiz_file):
            with open(quiz_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Megkeressük a lista végét
            # Keresünk az utolsó kérdés után
            last_question_pattern = r'(\s+},\s*)\n\s*\]\s*$'
            match = re.search(last_question_pattern, content, re.MULTILINE | re.DOTALL)
            
            if match:
                # Új kérdések beszúrása
                new_content = content[:match.start(1)]
                
                for question in new_questions:
                    new_content += f"""    {{
        'question': '{question['question']}',
        'options': {question['options']},
        'correct': {question['correct']},
        'explanation': '{question['explanation']}',
        'image_file': '{question['image_file']}',
        'topic': '{question['topic']}'
    }},
"""
                
                new_content += content[match.start(1):]
                
                # Fájl mentése
                with open(quiz_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                print(f"✅ {len(new_questions)} új kérdés hozzáadva a quiz-hez!")
                print(f"📁 Fájl frissítve: {quiz_file}")
            else:
                print("❌ Nem sikerült megtalálni a lista végét a fájlban!")
        else:
            print("❌ A quiz fájl nem található!")
    
    # Összesítés
    print(f"\n📊 Összesítés:")
    print(f"  - Eredeti kérdések: {len(existing_images)}")
    print(f"  - Új kérdések: {len(new_questions)}")
    print(f"  - Összes kérdés: {len(existing_images) + len(new_questions)}")

if __name__ == "__main__":
    main() 