#!/usr/bin/env python3
"""
Script a preview_duration mező hozzáadásához a One Hit Wonders kérdésekhez
"""

import re

def add_preview_duration_to_questions():
    """Hozzáadja a preview_duration mezőt az összes kérdéshez"""
    
    # Fájl beolvasása
    with open('topics/one_hit_wonders.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Regex pattern a "topic": "one_hit_wonders" sorokhoz
    pattern = r'("topic": "one_hit_wonders")\s*'
    replacement = r'\1,\n            "preview_duration": 90'
    
    # Csere végrehajtása
    updated_content = re.sub(pattern, replacement, content)
    
    # Fájl visszaírása
    with open('topics/one_hit_wonders.py', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("✅ preview_duration mező hozzáadva az összes One Hit Wonders kérdéshez!")

if __name__ == "__main__":
    add_preview_duration_to_questions() 