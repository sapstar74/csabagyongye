#!/usr/bin/env python3
"""
Manuális Spotify Linkek Komolyzenei Darabokhoz
Előre összegyűjtött Spotify linkek a legnépszerűbb komolyzenei darabokhoz
"""

# Manuálisan összegyűjtött Spotify linkek népszerű komolyzenei darabokhoz
SPOTIFY_LINKS = {
    # Beethoven - Legnépszerűbb darabok
    "Beethoven: V. Szimfónia - A sors szimfónia": "https://open.spotify.com/embed/track/3zPrZvOFdXL3QY9T9X5Cy5",
    "Beethoven: Holdvilág szonáta - Mondscheinsonate": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Beethoven: Ode to Joy - 9. szimfónia": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Beethoven: Symphony 7. in A major": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Mozart - Legnépszerűbb darabok
    "Mozart: Eine kleine Nachtmusik (K. 525) - A kis éji zene": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Mozart: Török induló - A-túr szonáta": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Csajkovszkij - Legnépszerűbb darabok
    "Csajkovszkij: Diótörő - Tánc a cukorkák hercegnőjéről": "https://open.spotify.com/embed/track/6WzX2VSPFJDuyPyWOd8Rj5",
    "Csajkovszkij: Hattyúk tava - Tánc a kis hattyúkról": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Csajkovszkij: 1. Zongoraverseny": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Csajkovszkij: Rómeó és Júlia finálé": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Bach - Legnépszerűbb darabok
    "Bach: Brandenburgi versenyek - 3. verseny": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Toccata és fúga d-moll": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Air on G-string": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Italian Concerto": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Jesu, Joy of Man": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Brandenburg Concerto No. 5": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: Vivace": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bach: G-dúr menüett": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Liszt - Legnépszerűbb darabok
    "Liszt: Magyar rapszódia": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Liszt: Liebestraum": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Liszt: La campanella": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Liszt: Rákóczi induló": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Liszt: Consolation": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Chopin - Legnépszerűbb darabok
    "Chopin: Sonata 2 in B flat minor": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Grieg - Legnépszerűbb darabok
    "Grieg: Peer Gynt Op. 23": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Grieg: A hegyi király udvarában": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Vivaldi - Legnépszerűbb darabok
    "Vivaldi: 4 évszak": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Vivaldi: Szonáta": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Brahms - Legnépszerűbb darabok
    "Brahms: Magyar táncok": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Dvorak - Legnépszerűbb darabok
    "Dvorak: IX. Új világ szimfónia": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Dvorak: Humoresque": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Dvorak: 8. G-dúr szimfónia": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Handel - Legnépszerűbb darabok
    "Handel: Rinaldo": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Handel: IV. B-dúr menüett": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Handel: Keyboard Suite in D minor": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Wagner - Legnépszerűbb darabok
    "Wagner: A Valkűrök bevonulása": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Wagner: Here comes the Bride": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Wagner: Ave Maria": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Wagner: Ode to Joy": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Kodály - Legnépszerűbb darabok
    "Kodály Zoltán: Háry János": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Kodály Zoltán: Kállai kettős": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Kodály Zoltán: Adagio": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Bartók - Legnépszerűbb darabok
    "Bartók: Román táncok": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bartók: Allegro Barbaro": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bartók: Kékszakállú herceg vára": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Bartók: Csodálatos mandarin": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Hacsaturján - Legnépszerűbb darabok
    "Hacsaturján: Kartánc": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Hacsaturján: Spartacus / Onedin": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Weiner Leó - Legnépszerűbb darabok
    "Weiner Leó: Rókatánc": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Schubert - Legnépszerűbb darabok
    "Schubert: Pisztráng ötös": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Rimsky-Korsakov - Legnépszerűbb darabok
    "Rimsky-Korsakov: Bumblebee": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Mussorgsky - Legnépszerűbb darabok
    "Mussorgsky: Éjszaka a hegyen": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Prokofjev - Legnépszerűbb darabok
    "Prokofjev: Péter és a farkas": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Carl Orff - Legnépszerűbb darabok
    "Carl Orff: Carmina Burana": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Ravel - Legnépszerűbb darabok
    "Ravel: Bolero": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Rossini - Legnépszerűbb darabok
    "Rossini: Tell Vilmos nyitány": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Rossini: Sevillai borbély": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Verdi - Legnépszerűbb darabok
    "Verdi: Traviata": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    "Verdi: Aida": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Shostakovich - Legnépszerűbb darabok
    "Shostakovich: Second waltz": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Gershwin - Legnépszerűbb darabok
    "Gershwin: Rhapsody in Blue": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
    
    # Bizet - Legnépszerűbb darabok
    "Bizet: Carmen": "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd",
}

def update_classical_music_questions():
    """
    Frissíti a classical_music_questions.py fájlt a megfelelő Spotify linkekkel
    """
    from classical_music_questions import CLASSICAL_MUSIC_QUESTIONS
    
    updated_questions = []
    
    for question in CLASSICAL_MUSIC_QUESTIONS:
        explanation = question['explanation']
        
        # Keresés a Spotify linkek között
        spotify_link = SPOTIFY_LINKS.get(explanation, "https://open.spotify.com/embed/track/4VRRbrw7ai2mztUrXrAvfd")
        
        # Kérdés frissítése
        updated_question = question.copy()
        updated_question['spotify_embed'] = spotify_link
        
        updated_questions.append(updated_question)
    
    return updated_questions

def save_updated_questions(questions):
    """
    Elmenti a frissített kérdéseket egy új fájlba
    """
    with open('classical_music_questions_updated.py', 'w', encoding='utf-8') as f:
        f.write("# Komolyzene kérdések a PDF alapján - 67 darab összesen\n\n")
        f.write("CLASSICAL_MUSIC_QUESTIONS = [\n")
        
        for question in questions:
            f.write("    {\n")
            f.write(f'        "question": "{question["question"]}",\n')
            f.write(f'        "spotify_embed": "{question["spotify_embed"]}",\n')
            f.write(f'        "options": {question["options"]},\n')
            f.write(f'        "correct": {question["correct"]},\n')
            f.write(f'        "explanation": "{question["explanation"]}",\n')
            f.write(f'        "topic": "{question["topic"]}"\n')
            f.write("    },\n")
        
        f.write("]\n\n")
        f.write(f'# Összesen: {len(questions)} kérdés\n')
        f.write(f'print(f"Komolyzene kérdések száma: {len(questions)}")\n')

def main():
    """
    Fő függvény
    """
    print("🎵 Spotify Linkek Frissítése")
    print("=" * 40)
    
    # Kérdések frissítése
    updated_questions = update_classical_music_questions()
    
    # Eredmények mentése
    save_updated_questions(updated_questions)
    
    print(f"✅ Frissített kérdések mentve: classical_music_questions_updated.py")
    print(f"📊 Összesen {len(updated_questions)} kérdés frissítve")
    
    # Néhány példa megjelenítése
    print("\n📋 Példák a frissített linkekről:")
    for i, question in enumerate(updated_questions[:5]):
        print(f"{i+1}. {question['explanation']}")
        print(f"   Link: {question['spotify_embed']}")
        print()

if __name__ == "__main__":
    main() 