# One Hit Wonders kérdések - Spotify playlist alapján
# Dinamikusan generált kérdések a Spotify API-ból

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_playlist_manager import get_one_hit_wonders_questions

def get_one_hit_wonders_questions_dynamic(count: int = 20):
    """Dinamikusan generált One Hit Wonders kérdések"""
    try:
        questions = get_one_hit_wonders_questions(count)
        if questions and len(questions) > 0:
            return questions
        else:
            print("Spotify API nem adott vissza kérdéseket, statikus kérdések használata")
            return get_static_one_hit_wonders_questions()
    except Exception as e:
        print(f"Hiba a One Hit Wonders kérdések generálásánál: {e}")
        # Fallback statikus kérdések
        return get_static_one_hit_wonders_questions()

def get_static_one_hit_wonders_questions():
    """Statikus One Hit Wonders kérdések fallback esetén"""
    return [
        {
            "question": "Ki az előadó a 'Teenage Dirtbag' című dalban?",
            "options": ["Wheatus", "Blink-182", "Sum 41", "Good Charlotte"],
            "correct": 0,
            "explanation": "'Teenage Dirtbag' egy One Hit Wonder dal az előadótól: Wheatus",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Somebody That I Used To Know' című dalban?",
            "options": ["Gotye", "Passenger", "James Blunt", "Ed Sheeran"],
            "correct": 0,
            "explanation": "'Somebody That I Used To Know' egy One Hit Wonder dal az előadótól: Gotye",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Little Talks' című dalban?",
            "options": ["Of Monsters and Men", "Mumford & Sons", "The Lumineers", "Imagine Dragons"],
            "correct": 0,
            "explanation": "'Little Talks' egy One Hit Wonder dal az előadótól: Of Monsters and Men",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Tainted Love' című dalban?",
            "options": ["Soft Cell", "Depeche Mode", "New Order", "The Cure"],
            "correct": 0,
            "explanation": "'Tainted Love' egy One Hit Wonder dal az előadótól: Soft Cell",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Return of the Mack' című dalban?",
            "options": ["Mark Morrison", "Maxi Priest", "Shabba Ranks", "Shaggy"],
            "correct": 0,
            "explanation": "'Return of the Mack' egy One Hit Wonder dal az előadótól: Mark Morrison",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Butterfly' című dalban?",
            "options": ["Crazy Town", "Limp Bizkit", "Korn", "Linkin Park"],
            "correct": 0,
            "explanation": "'Butterfly' egy One Hit Wonder dal az előadótól: Crazy Town",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Young Folks' című dalban?",
            "options": ["Peter Bjorn and John", "The Shins", "Death Cab for Cutie", "The Postal Service"],
            "correct": 0,
            "explanation": "'Young Folks' egy One Hit Wonder dal az előadótól: Peter Bjorn and John",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Bad Day' című dalban?",
            "options": ["Daniel Powter", "James Blunt", "Robbie Williams", "Gary Barlow"],
            "correct": 0,
            "explanation": "'Bad Day' egy One Hit Wonder dal az előadótól: Daniel Powter",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Stacy's Mom' című dalban?",
            "options": ["Fountains Of Wayne", "Weezer", "Blink-182", "Green Day"],
            "correct": 0,
            "explanation": "'Stacy's Mom' egy One Hit Wonder dal az előadótól: Fountains Of Wayne",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Cotton Eye Joe' című dalban?",
            "options": ["Rednex", "Village People", "Boney M", "ABBA"],
            "correct": 0,
            "explanation": "'Cotton Eye Joe' egy One Hit Wonder dal az előadótól: Rednex",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Two Princes' című dalban?",
            "options": ["Spin Doctors", "Blues Traveler", "Hootie & the Blowfish", "Counting Crows"],
            "correct": 0,
            "explanation": "'Two Princes' egy One Hit Wonder dal az előadótól: Spin Doctors",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Bitch' című dalban?",
            "options": ["Meredith Brooks", "Alanis Morissette", "Sheryl Crow", "Fiona Apple"],
            "correct": 0,
            "explanation": "'Bitch' egy One Hit Wonder dal az előadótól: Meredith Brooks",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'My Sharona' című dalban?",
            "options": ["The Knack", "The Cars", "The Police", "The Pretenders"],
            "correct": 0,
            "explanation": "'My Sharona' egy One Hit Wonder dal az előadótól: The Knack",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Ice Ice Baby' című dalban?",
            "options": ["Vanilla Ice", "MC Hammer", "Tone Loc", "Young MC"],
            "correct": 0,
            "explanation": "'Ice Ice Baby' egy One Hit Wonder dal az előadótól: Vanilla Ice",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Billionaire' című dalban?",
            "options": ["Travie McCoy", "Flo Rida", "Pitbull", "Sean Paul"],
            "correct": 0,
            "explanation": "'Billionaire' egy One Hit Wonder dal az előadótól: Travie McCoy",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Video Killed The Radio Star' című dalban?",
            "options": ["The Buggles", "The Cars", "The Police", "The Pretenders"],
            "correct": 0,
            "explanation": "'Video Killed The Radio Star' egy One Hit Wonder dal az előadótól: The Buggles",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Walking in Memphis' című dalban?",
            "options": ["Marc Cohn", "Bruce Hornsby", "Don Henley", "Jackson Browne"],
            "correct": 0,
            "explanation": "'Walking in Memphis' egy One Hit Wonder dal az előadótól: Marc Cohn",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Saturday Night' című dalban?",
            "options": ["Whigfield", "Corona", "Real McCoy", "La Bouche"],
            "correct": 0,
            "explanation": "'Saturday Night' egy One Hit Wonder dal az előadótól: Whigfield",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Who Let The Dogs Out' című dalban?",
            "options": ["Baha Men", "Vengaboys", "Aqua", "Eiffel 65"],
            "correct": 0,
            "explanation": "'Who Let The Dogs Out' egy One Hit Wonder dal az előadótól: Baha Men",
            "topic": "one_hit_wonders"
        },
        {
            "question": "Ki az előadó a 'Shake It' című dalban?",
            "options": ["Metro Station", "Cobra Starship", "The All-American Rejects", "Panic! At The Disco"],
            "correct": 0,
            "explanation": "'Shake It' egy One Hit Wonder dal az előadótól: Metro Station",
            "topic": "one_hit_wonders"
        }
    ]

# Dinamikus kérdések exportálása - fallback statikus kérdésekre
try:
    ONE_HIT_WONDERS_QUESTIONS = get_one_hit_wonders_questions_dynamic(20)
    if not ONE_HIT_WONDERS_QUESTIONS:
        ONE_HIT_WONDERS_QUESTIONS = get_static_one_hit_wonders_questions()
except Exception as e:
    print(f"Hiba a One Hit Wonders kérdések generálásánál: {e}")
    ONE_HIT_WONDERS_QUESTIONS = get_static_one_hit_wonders_questions()

if __name__ == "__main__":
    print("🎵 One Hit Wonders Kérdések Tesztelése")
    print("=" * 40)
    
    questions = get_one_hit_wonders_questions_dynamic(5)
    print(f"Generált kérdések száma: {len(questions)}")
    
    for i, q in enumerate(questions[:3]):
        print(f"\n{i+1}. {q['question']}")
        print(f"   Válaszopciók: {q['options']}")
        print(f"   Helyes: {q['options'][q['correct']]}") 