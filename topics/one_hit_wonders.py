# One Hit Wonders kérdések - Spotify playlist alapján
# Dinamikusan generált kérdések a Spotify API-ból

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_playlist_manager import get_one_hit_wonders_questions
from one_hit_wonders_audio_mapping import get_one_hit_wonders_audio_path

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
    """Statikus One Hit Wonders kérdések - minden elérhető audio fájlhoz kérdés"""
    return [
        {
            "question": "Ki az előadó a 'Teenage Dirtbag' című dalban?",
            "options": ["BTS", "Justin Bieber", "One Direction", "Wheatus"],
            "correct": 3,
            "explanation": "'Teenage Dirtbag' egy One Hit Wonder dal az előadótól: Wheatus",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 1
        },
        {
            "question": "Ki az előadó a 'Somebody That I Used To Know' című dalban?",
            "options": ["Justin Bieber", "Gotye", "Maroon 5", "Taylor Swift"],
            "correct": 1,
            "explanation": "'Somebody That I Used To Know' egy One Hit Wonder dal az előadótól: Gotye",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 2
        },
        {
            "question": "Ki az előadó a 'Tainted Love' című dalban?",
            "options": ["Katy Perry", "Soft Cell", "One Direction", "Rihanna"],
            "correct": 1,
            "explanation": "'Tainted Love' egy One Hit Wonder dal az előadótól: Soft Cell",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 4
        },
        {
            "question": "Ki az előadó a 'Return of the Mack' című dalban?",
            "options": ["Adele", "Billie Eilish", "Beyoncé", "Mark Morrison"],
            "correct": 3,
            "explanation": "'Return of the Mack' egy One Hit Wonder dal az előadótól: Mark Morrison",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 5
        },
        {
            "question": "Ki az előadó a 'Bad Day' című dalban?",
            "options": ["Daniel Powter", "Post Malone", "Ed Sheeran", "The Weeknd"],
            "correct": 0,
            "explanation": "'Bad Day' egy One Hit Wonder dal az előadótól: Daniel Powter",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 8
        },
        {
            "question": "Ki az előadó a 'Stacy's Mom' című dalban?",
            "options": ["BTS", "Post Malone", "Justin Bieber", "Fountains Of Wayne"],
            "correct": 3,
            "explanation": "'Stacy's Mom' egy One Hit Wonder dal az előadótól: Fountains Of Wayne",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 9
        },
        {
            "question": "Ki az előadó a 'Bitch' című dalban?",
            "options": ["Justin Bieber", "The Weeknd", "Maroon 5", "Meredith Brooks"],
            "correct": 3,
            "explanation": "'Bitch' egy One Hit Wonder dal az előadótól: Meredith Brooks",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 12
        },
        {
            "question": "Ki az előadó a 'Ice Ice Baby' című dalban?",
            "options": ["Adele", "Maroon 5", "Justin Bieber", "Vanilla Ice"],
            "correct": 3,
            "explanation": "'Ice Ice Baby' egy One Hit Wonder dal az előadótól: Vanilla Ice",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 14
        },
        {
            "question": "Ki az előadó a 'Video Killed The Radio Star' című dalban?",
            "options": ["BTS", "The Buggles", "Post Malone", "One Direction"],
            "correct": 1,
            "explanation": "'Video Killed The Radio Star' egy One Hit Wonder dal az előadótól: The Buggles",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 16
        },
        {
            "question": "Ki az előadó a 'Walking in Memphis' című dalban?",
            "options": ["Rihanna", "Adele", "Justin Bieber", "Marc Cohn"],
            "correct": 3,
            "explanation": "'Walking in Memphis' egy One Hit Wonder dal az előadótól: Marc Cohn",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 17
        },
        {
            "question": "Ki az előadó a 'Saturday Night' című dalban?",
            "options": ["Taylor Swift", "Post Malone", "Whigfield", "Maroon 5"],
            "correct": 2,
            "explanation": "'Saturday Night' egy One Hit Wonder dal az előadótól: Whigfield",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 18
        },
        {
            "question": "Ki az előadó a 'Who Let The Dogs Out' című dalban?",
            "options": ["Baha Men", "Rihanna", "Adele", "The Weeknd"],
            "correct": 0,
            "explanation": "'Who Let The Dogs Out' egy One Hit Wonder dal az előadótól: Baha Men",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 19
        },
        {
            "question": "Ki az előadó a 'Shake It' című dalban?",
            "options": ["Ed Sheeran", "Bruno Mars", "Metro Station", "The Weeknd"],
            "correct": 2,
            "explanation": "'Shake It' egy One Hit Wonder dal az előadótól: Metro Station",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 20
        },
        {
            "question": "Ki az előadó a 'Informer' című dalban?",
            "options": ["Snow", "One Direction", "Dua Lipa", "Maroon 5"],
            "correct": 0,
            "explanation": "'Informer' egy One Hit Wonder dal az előadótól: Snow",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 21
        },
        {
            "question": "Ki az előadó a 'Jerk It Out' című dalban?",
            "options": ["Ed Sheeran", "Caesars", "Billie Eilish", "Taylor Swift"],
            "correct": 1,
            "explanation": "'Jerk It Out' egy One Hit Wonder dal az előadótól: Caesars",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 22
        },
        {
            "question": "Ki az előadó a 'Heartbeats' című dalban?",
            "options": ["José González", "BTS", "Maroon 5", "Billie Eilish"],
            "correct": 0,
            "explanation": "'Heartbeats' egy One Hit Wonder dal az előadótól: José González",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 23
        },
        {
            "question": "Ki az előadó a 'Rude' című dalban?",
            "options": ["Adele", "Imagine Dragons", "MAGIC!", "Rihanna"],
            "correct": 2,
            "explanation": "'Rude' egy One Hit Wonder dal az előadótól: MAGIC!",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 24
        },
        {
            "question": "Ki az előadó a 'Turn Me On' című dalban?",
            "options": ["Billie Eilish", "Dua Lipa", "Kevin Lyttle", "One Direction"],
            "correct": 2,
            "explanation": "'Turn Me On' egy One Hit Wonder dal az előadótól: Kevin Lyttle",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 25
        },
        {
            "question": "Ki az előadó a 'Ring My Bell' című dalban?",
            "options": ["Taylor Swift", "Adele", "Dua Lipa", "Anita Ward"],
            "correct": 3,
            "explanation": "'Ring My Bell' egy One Hit Wonder dal az előadótól: Anita Ward",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 26
        },
        {
            "question": "Ki az előadó a 'It Just Won't Do' című dalban?",
            "options": ["Tim Deluxe", "Maroon 5", "Coldplay", "Taylor Swift"],
            "correct": 0,
            "explanation": "'It Just Won't Do' egy One Hit Wonder dal az előadótól: Tim Deluxe",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 27
        },
        {
            "question": "Ki az előadó a 'Safety Dance' című dalban?",
            "options": ["Men Without Hats", "Beyoncé", "BTS", "Justin Bieber"],
            "correct": 0,
            "explanation": "'Safety Dance' egy One Hit Wonder dal az előadótól: Men Without Hats",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 28
        },
        {
            "question": "Ki az előadó a 'I Love It' című dalban?",
            "options": ["The Weeknd", "BTS", "Katy Perry", "Icona Pop"],
            "correct": 3,
            "explanation": "'I Love It' egy One Hit Wonder dal az előadótól: Icona Pop",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 29
        },
        {
            "question": "Ki az előadó a 'Hold You - Hold Yuh' című dalban?",
            "options": ["One Direction", "Dua Lipa", "Imagine Dragons", "Gyptian"],
            "correct": 3,
            "explanation": "'Hold You - Hold Yuh' egy One Hit Wonder dal az előadótól: Gyptian",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 30
        },
        {
            "question": "Ki az előadó a 'Macarena' című dalban?",
            "options": ["Imagine Dragons", "Coldplay", "Ed Sheeran", "Los del Río"],
            "correct": 3,
            "explanation": "'Macarena' egy One Hit Wonder dal az előadótól: Los del Río",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 31
        },
        {
            "question": "Ki az előadó a 'Gangnam Style' című dalban?",
            "options": ["PSY", "Taylor Swift", "Beyoncé", "One Direction"],
            "correct": 0,
            "explanation": "'Gangnam Style' egy One Hit Wonder dal az előadótól: PSY",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 32
        },
        {
            "question": "Ki az előadó a 'Harlem Shake' című dalban?",
            "options": ["Bruno Mars", "BTS", "Baauer", "Post Malone"],
            "correct": 2,
            "explanation": "'Harlem Shake' egy One Hit Wonder dal az előadótól: Baauer",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 33
        },
        {
            "question": "Ki az előadó a 'Call Me Maybe' című dalban?",
            "options": ["Lady Gaga", "Billie Eilish", "Carly Rae Jepsen", "Taylor Swift"],
            "correct": 2,
            "explanation": "'Call Me Maybe' egy One Hit Wonder dal az előadótól: Carly Rae Jepsen",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 34
        },
        {
            "question": "Ki az előadó a 'Royals' című dalban?",
            "options": ["Lorde", "Taylor Swift", "Coldplay", "One Direction"],
            "correct": 0,
            "explanation": "'Royals' egy One Hit Wonder dal az előadótól: Lorde",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 35
        },
        {
            "question": "Ki az előadó a 'Pumped Up Kicks' című dalban?",
            "options": ["The Weeknd", "One Direction", "Foster the People", "Rihanna"],
            "correct": 2,
            "explanation": "'Pumped Up Kicks' egy One Hit Wonder dal az előadótól: Foster the People",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 36
        },
        {
            "question": "Ki az előadó a 'Some Nights' című dalban?",
            "options": ["Lady Gaga", "fun.", "Adele", "Rihanna"],
            "correct": 1,
            "explanation": "'Some Nights' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 37
        },
        {
            "question": "Ki az előadó a 'We Are Young' című dalban?",
            "options": ["fun.", "Imagine Dragons", "Taylor Swift", "Katy Perry"],
            "correct": 0,
            "explanation": "'We Are Young' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 38
        },
        {
            "question": "Ki az előadó a 'Radioactive' című dalban?",
            "options": ["Taylor Swift", "Imagine Dragons", "Drake", "Billie Eilish"],
            "correct": 1,
            "explanation": "'Radioactive' egy One Hit Wonder dal az előadótól: Imagine Dragons",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 40
        },
        {
            "question": "Ki az előadó a 'Sail' című dalban?",
            "options": ["Adele", "AWOLNATION", "Maroon 5", "Katy Perry"],
            "correct": 1,
            "explanation": "'Sail' egy One Hit Wonder dal az előadótól: AWOLNATION",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 41
        },
        {
            "question": "Ki az előadó a 'Thrift Shop' című dalban?",
            "options": ["Taylor Swift", "One Direction", "Ariana Grande", "Macklemore & Ryan Lewis"],
            "correct": 3,
            "explanation": "'Thrift Shop' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 42
        },
        {
            "question": "Ki az előadó a 'Can't Hold Us' című dalban?",
            "options": ["Imagine Dragons", "Maroon 5", "Beyoncé", "Macklemore & Ryan Lewis"],
            "correct": 3,
            "explanation": "'Can't Hold Us' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 43
        },
        {
            "question": "Ki az előadó a 'Get Lucky' című dalban?",
            "options": ["Drake", "Katy Perry", "Daft Punk", "Billie Eilish"],
            "correct": 2,
            "explanation": "'Get Lucky' egy One Hit Wonder dal az előadótól: Daft Punk",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 44
        },
        {
            "question": "Ki az előadó a 'Blurred Lines' című dalban?",
            "options": ["Ariana Grande", "Lady Gaga", "One Direction", "Robin Thicke"],
            "correct": 3,
            "explanation": "'Blurred Lines' egy One Hit Wonder dal az előadótól: Robin Thicke",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 45
        },
        {
            "question": "Ki az előadó a 'Uptown Funk' című dalban?",
            "options": ["Coldplay", "Beyoncé", "Mark Ronson ft  Bruno Mars", "Ed Sheeran"],
            "correct": 2,
            "explanation": "'Uptown Funk' egy One Hit Wonder dal az előadótól: Mark Ronson ft  Bruno Mars",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 46
        },
        {
            "question": "Ki az előadó a 'Blank Space' című dalban?",
            "options": ["Taylor Swift", "Post Malone", "Ed Sheeran", "Dua Lipa"],
            "correct": 0,
            "explanation": "'Blank Space' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 48
        },
        {
            "question": "Ki az előadó a 'Shut Up and Dance' című dalban?",
            "options": ["Rihanna", "WALK THE MOON", "Dua Lipa", "Drake"],
            "correct": 1,
            "explanation": "'Shut Up and Dance' egy One Hit Wonder dal az előadótól: WALK THE MOON",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 49
        },
        {
            "question": "Ki az előadó a 'Cheerleader' című dalban?",
            "options": ["Lady Gaga", "Coldplay", "Imagine Dragons", "OMI"],
            "correct": 3,
            "explanation": "'Cheerleader' egy One Hit Wonder dal az előadótól: OMI",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 50
        },
        {
            "question": "Ki az előadó a 'See You Again' című dalban?",
            "options": ["The Weeknd", "Wiz Khalifa ft  Charlie Puth", "Lady Gaga", "Taylor Swift"],
            "correct": 1,
            "explanation": "'See You Again' egy One Hit Wonder dal az előadótól: Wiz Khalifa ft  Charlie Puth",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 51
        },
        {
            "question": "Ki az előadó a 'Fancy' című dalban?",
            "options": ["Iggy Azalea ft  Charli XCX", "Rihanna", "BTS", "Post Malone"],
            "correct": 0,
            "explanation": "'Fancy' egy One Hit Wonder dal az előadótól: Iggy Azalea ft  Charli XCX",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 52
        },
        {
            "question": "Ki az előadó a 'All About That Bass' című dalban?",
            "options": ["Meghan Trainor", "One Direction", "Post Malone", "Bruno Mars"],
            "correct": 0,
            "explanation": "'All About That Bass' egy One Hit Wonder dal az előadótól: Meghan Trainor",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 53
        },
        {
            "question": "Ki az előadó a 'Despacito' című dalban?",
            "options": ["BTS", "Billie Eilish", "Justin Bieber", "Luis Fonsi ft  Daddy Yankee"],
            "correct": 3,
            "explanation": "'Despacito' egy One Hit Wonder dal az előadótól: Luis Fonsi ft  Daddy Yankee",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 54
        },
        {
            "question": "Ki az előadó a 'Shape of You' című dalban?",
            "options": ["One Direction", "Ed Sheeran", "The Weeknd", "Coldplay"],
            "correct": 1,
            "explanation": "'Shape of You' egy One Hit Wonder dal az előadótól: Ed Sheeran",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 55
        },
        {
            "question": "Ki az előadó a 'Havana' című dalban?",
            "options": ["Dua Lipa", "Coldplay", "Camila Cabello", "Billie Eilish"],
            "correct": 2,
            "explanation": "'Havana' egy One Hit Wonder dal az előadótól: Camila Cabello",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 56
        },
        {
            "question": "Ki az előadó a 'New Rules' című dalban?",
            "options": ["Ariana Grande", "Dua Lipa", "Post Malone", "Rihanna"],
            "correct": 1,
            "explanation": "'New Rules' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 57
        },
        {
            "question": "Ki az előadó a 'Bad Guy' című dalban?",
            "options": ["Maroon 5", "Billie Eilish", "Rihanna", "Dua Lipa"],
            "correct": 1,
            "explanation": "'Bad Guy' egy One Hit Wonder dal az előadótól: Billie Eilish",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 58
        },
        {
            "question": "Ki az előadó a 'Old Town Road' című dalban?",
            "options": ["Billie Eilish", "Rihanna", "Lil Nas X", "Adele"],
            "correct": 2,
            "explanation": "'Old Town Road' egy One Hit Wonder dal az előadótól: Lil Nas X",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 59
        },
        {
            "question": "Ki az előadó a 'Dance Monkey' című dalban?",
            "options": ["Drake", "Ariana Grande", "Tones and I", "BTS"],
            "correct": 2,
            "explanation": "'Dance Monkey' egy One Hit Wonder dal az előadótól: Tones and I",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 60
        },
        {
            "question": "Ki az előadó a 'Blinding Lights' című dalban?",
            "options": ["Bruno Mars", "Coldplay", "The Weeknd", "Dua Lipa"],
            "correct": 2,
            "explanation": "'Blinding Lights' egy One Hit Wonder dal az előadótól: The Weeknd",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 61
        },
        {
            "question": "Ki az előadó a 'Levitating' című dalban?",
            "options": ["Imagine Dragons", "Beyoncé", "Dua Lipa", "Ariana Grande"],
            "correct": 2,
            "explanation": "'Levitating' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 62
        },
        {
            "question": "Ki az előadó a 'Stay' című dalban?",
            "options": ["Maroon 5", "Drake", "Taylor Swift", "The Kid LAROI & Justin Bieber"],
            "correct": 3,
            "explanation": "'Stay' egy One Hit Wonder dal az előadótól: The Kid LAROI & Justin Bieber",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 63
        },
        {
            "question": "Ki az előadó a 'As It Was' című dalban?",
            "options": ["Justin Bieber", "Harry Styles", "Taylor Swift", "Lady Gaga"],
            "correct": 1,
            "explanation": "'As It Was' egy One Hit Wonder dal az előadótól: Harry Styles",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 64
        },
        {
            "question": "Ki az előadó a 'Flowers' című dalban?",
            "options": ["Miley Cyrus", "Post Malone", "Dua Lipa", "Ed Sheeran"],
            "correct": 0,
            "explanation": "'Flowers' egy One Hit Wonder dal az előadótól: Miley Cyrus",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 65
        },
        {
            "question": "Ki az előadó a 'Cruel Summer' című dalban?",
            "options": ["Ed Sheeran", "Beyoncé", "Taylor Swift", "One Direction"],
            "correct": 2,
            "explanation": "'Cruel Summer' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 67
        },
        {
            "question": "Ki az előadó a 'Last Night' című dalban?",
            "options": ["Adele", "Imagine Dragons", "Rihanna", "Morgan Wallen"],
            "correct": 3,
            "explanation": "'Last Night' egy One Hit Wonder dal az előadótól: Morgan Wallen",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 68
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

# Csak azok a kérdések, amelyekhez van audio fájl
ONE_HIT_WONDERS_QUESTIONS = [q for q in ONE_HIT_WONDERS_QUESTIONS if 'original_index' in q]

if __name__ == "__main__":
    print("🎵 One Hit Wonders Kérdések Tesztelése")
    print("=" * 40)
    
    questions = get_one_hit_wonders_questions_dynamic(5)
    print(f"Generált kérdések száma: {len(questions)}")
    
    for i, q in enumerate(questions[:3]):
        print(f"\n{i+1}. {q['question']}")
        print(f"   Válaszopciók: {q['options']}")
        print(f"   Helyes: {q['options'][q['correct']]}") 