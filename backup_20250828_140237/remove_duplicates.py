#!/usr/bin/env python3
"""
Duplikátum háborús kérdések eltávolítása a kvízből
"""

import json
import re
from collections import defaultdict

def remove_duplicate_wars(quiz_file_path):
    """Eltávolítja a duplikátum háborús kérdéseket"""
    
    # Fájl beolvasása
    with open(quiz_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Háborúk szekció keresése
    war_section_start = content.find('"háborúk": [')
    if war_section_start == -1:
        print("Háborúk szekció nem található!")
        return False
    
    # Háborúk szekció vége keresése
    bracket_count = 0
    war_section_end = war_section_start + len('"háborúk": [')
    
    while war_section_end < len(content):
        if content[war_section_end] == '[':
            bracket_count += 1
        elif content[war_section_end] == ']':
            if bracket_count == 0:
                break
            bracket_count -= 1
        war_section_end += 1
    
    if war_section_end >= len(content):
        print("Háborúk szekció vége nem található!")
        return False
    
    # Háborúk szekció kinyerése
    wars_section = content[war_section_start:war_section_end+1]
    
    # Kérdések kinyerése reguláris kifejezéssel
    question_pattern = r'\{\s*"question":\s*"([^"]+)"[^}]*"explanation":\s*"([^"]+)"[^}]*\}'
    questions = re.findall(question_pattern, wars_section, re.DOTALL)
    
    print(f"Összesen {len(questions)} háborús kérdés található")
    
    # Duplikátumok keresése
    seen_questions = {}
    unique_questions = []
    duplicates_removed = 0
    
    for i, (question, explanation) in enumerate(questions):
        # Kérdés normalizálása (whitespace eltávolítása)
        normalized_question = ' '.join(question.split())
        
        if normalized_question not in seen_questions:
            seen_questions[normalized_question] = True
            unique_questions.append((question, explanation))
        else:
            duplicates_removed += 1
            print(f"Duplikátum eltávolítva: {normalized_question[:80]}...")
    
    print(f"Eltávolított duplikátumok: {duplicates_removed}")
    print(f"Megmaradt egyedi kérdések: {len(unique_questions)}")
    
    # Új háborúk szekció építése
    # Először ki kell nyerni a teljes kérdés blokkokat
    full_question_pattern = r'(\{\s*"question":\s*"[^"]+"\s*,\s*"options":\s*\[[^\]]+\]\s*,\s*"correct":\s*\d+\s*,\s*"explanation":\s*"[^"]+"\s*\})'
    full_questions = re.findall(full_question_pattern, wars_section, re.DOTALL)
    
    # Duplikátumok eltávolítása a teljes kérdések közül
    seen_full_questions = {}
    unique_full_questions = []
    
    for full_question in full_questions:
        # Kérdés szöveg kinyerése
        question_match = re.search(r'"question":\s*"([^"]+)"', full_question)
        if question_match:
            question_text = question_match.group(1)
            normalized_question = ' '.join(question_text.split())
            
            if normalized_question not in seen_full_questions:
                seen_full_questions[normalized_question] = True
                unique_full_questions.append(full_question)
    
    # Új háborúk szekció összeállítása
    new_wars_section = '"háborúk": [\n        ' + ',\n        '.join(unique_full_questions) + '\n    ]'
    
    # Fájl frissítése
    new_content = content[:war_section_start] + new_wars_section + content[war_section_end+1:]
    
    # Mentés
    with open(quiz_file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True, duplicates_removed, len(unique_full_questions)

def main():
    """Fő függvény"""
    quiz_path = "quiz_app.py"
    
    print("Duplikátum háborús kérdések eltávolítása...")
    
    result = remove_duplicate_wars(quiz_path)
    if result and len(result) == 3:
        success, removed, remaining = result
        if success:
            print(f"✅ Sikeresen eltávolítottam {removed} duplikátumot!")
            print(f"📊 Megmaradt háborús kérdések: {remaining}")
        else:
            print("❌ Hiba történt a duplikátumok eltávolításakor!")
    else:
        print("❌ Nem sikerült a duplikátumokat eltávolítani!")

if __name__ == "__main__":
    main() 