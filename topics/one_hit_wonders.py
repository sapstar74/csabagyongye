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
    """Statikus One Hit Wonders kérdések - pontosan egyeznek az audio fájlokkal"""
    return [
        {
            "question": "Ki az előadó a 'Teenage Dirtbag' című dalban?",
            "options": ["Lady Gaga", "Wheatus", "Drake", "Bruno Mars"],
            "correct": 1,
            "explanation": "'Teenage Dirtbag' egy One Hit Wonder dal az előadótól: Wheatus",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 1
        },
        {
            "question": "Ki az előadó a 'Somebody That I Used To Know' című dalban?",
            "options": ["Katy Perry", "Gotye", "Justin Bieber", "Lady Gaga"],
            "correct": 1,
            "explanation": "'Somebody That I Used To Know' egy One Hit Wonder dal az előadótól: Gotye",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 2
        },
        {
            "question": "Ki az előadó a 'Tainted Love' című dalban?",
            "options": ["Ariana Grande", "Post Malone", "Soft Cell", "Billie Eilish"],
            "correct": 2,
            "explanation": "'Tainted Love' egy One Hit Wonder dal az előadótól: Soft Cell",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 4
        },
        {
            "question": "Ki az előadó a 'Return of the Mack' című dalban?",
            "options": ["Drake", "Mark Morrison", "The Weeknd", "One Direction"],
            "correct": 1,
            "explanation": "'Return of the Mack' egy One Hit Wonder dal az előadótól: Mark Morrison",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 5
        },
        {
            "question": "Ki az előadó a 'Bad Day' című dalban?",
            "options": ["Drake", "Ariana Grande", "Daniel Powter", "Rihanna"],
            "correct": 2,
            "explanation": "'Bad Day' egy One Hit Wonder dal az előadótól: Daniel Powter",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 8
        },
        {
            "question": "Ki az előadó a 'Stacy's Mom' című dalban?",
            "options": ["Katy Perry", "Fountains Of Wayne", "The Weeknd", "Lady Gaga"],
            "correct": 1,
            "explanation": "'Stacy's Mom' egy One Hit Wonder dal az előadótól: Fountains Of Wayne",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 9
        },
        {
            "question": "Ki az előadó a 'Bitch' című dalban?",
            "options": ["Taylor Swift", "Meredith Brooks", "Maroon 5", "Dua Lipa"],
            "correct": 1,
            "explanation": "'Bitch' egy One Hit Wonder dal az előadótól: Meredith Brooks",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 12
        },
        {
            "question": "Ki az előadó a 'Ice Ice Baby' című dalban?",
            "options": ["Ed Sheeran", "Rihanna", "Taylor Swift", "Vanilla Ice"],
            "correct": 3,
            "explanation": "'Ice Ice Baby' egy One Hit Wonder dal az előadótól: Vanilla Ice",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 14
        },
        {
            "question": "Ki az előadó a 'Video Killed The Radio Star' című dalban?",
            "options": ["The Buggles", "Depeche Mode", "New Order", "The Cure"],
            "correct": 0,
            "explanation": "'Video Killed The Radio Star' egy One Hit Wonder dal az előadótól: The Buggles",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 16
        },
        {
            "question": "Ki az előadó a 'Walking in Memphis' című dalban?",
            "options": ["Marc Cohn", "Bruce Springsteen", "Bob Dylan", "Tom Petty"],
            "correct": 0,
            "explanation": "'Walking in Memphis' egy One Hit Wonder dal az előadótól: Marc Cohn",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 17
        },
        {
            "question": "Ki az előadó a 'Saturday Night' című dalban?",
            "options": ["Whigfield", "Ace of Base", "Real McCoy", "La Bouche"],
            "correct": 0,
            "explanation": "'Saturday Night' egy One Hit Wonder dal az előadótól: Whigfield",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 18
        },
        {
            "question": "Ki az előadó a 'Who Let The Dogs Out' című dalban?",
            "options": ["Baha Men", "Village People", "Boney M", "ABBA"],
            "correct": 0,
            "explanation": "'Who Let The Dogs Out' egy One Hit Wonder dal az előadótól: Baha Men",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 19
        },
        {
            "question": "Ki az előadó a 'Shake It' című dalban?",
            "options": ["Metro Station", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'Shake It' egy One Hit Wonder dal az előadótól: Metro Station",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 20
        },
        {
            "question": "Ki az előadó az 'Informer' című dalban?",
            "options": ["Snow", "Shaggy", "Maxi Priest", "Mark Morrison"],
            "correct": 0,
            "explanation": "'Informer' egy One Hit Wonder dal az előadótól: Snow",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 21
        },
        {
            "question": "Ki az előadó a 'Jerk It Out' című dalban?",
            "options": ["Caesars", "The Strokes", "The Hives", "The Vines"],
            "correct": 0,
            "explanation": "'Jerk It Out' egy One Hit Wonder dal az előadótól: Caesars",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 22
        },
        {
            "question": "Ki az előadó a 'Heartbeats' című dalban?",
            "options": ["José González", "Iron & Wine", "Bon Iver", "Fleet Foxes"],
            "correct": 0,
            "explanation": "'Heartbeats' egy One Hit Wonder dal az előadótól: José González",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 23
        },
        {
            "question": "Ki az előadó a 'Rude' című dalban?",
            "options": ["MAGIC!", "Maroon 5", "OneRepublic", "Imagine Dragons"],
            "correct": 0,
            "explanation": "'Rude' egy One Hit Wonder dal az előadótól: MAGIC!",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 24
        },
        {
            "question": "Ki az előadó a 'Turn Me On' című dalban?",
            "options": ["Kevin Lyttle", "Sean Paul", "Shaggy", "Beenie Man"],
            "correct": 0,
            "explanation": "'Turn Me On' egy One Hit Wonder dal az előadótól: Kevin Lyttle",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 25
        },
        {
            "question": "Ki az előadó a 'Ring My Bell' című dalban?",
            "options": ["Anita Ward", "Donna Summer", "Gloria Gaynor", "Diana Ross"],
            "correct": 0,
            "explanation": "'Ring My Bell' egy One Hit Wonder dal az előadótól: Anita Ward",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 26
        },
        {
            "question": "Ki az előadó az 'It Just Won't Do' című dalban?",
            "options": ["Tim Deluxe", "Basement Jaxx", "Daft Punk", "The Chemical Brothers"],
            "correct": 0,
            "explanation": "'It Just Won't Do' egy One Hit Wonder dal az előadótól: Tim Deluxe",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 27
        },
        {
            "question": "Ki az előadó a 'Safety Dance' című dalban?",
            "options": ["Men Without Hats", "Depeche Mode", "New Order", "The Cure"],
            "correct": 0,
            "explanation": "'Safety Dance' egy One Hit Wonder dal az előadótól: Men Without Hats",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 28
        },
        {
            "question": "Ki az előadó az 'I Love It' című dalban?",
            "options": ["Icona Pop", "Robyn", "Tove Lo", "Zara Larsson"],
            "correct": 0,
            "explanation": "'I Love It' egy One Hit Wonder dal az előadótól: Icona Pop",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 29
        },
        {
            "question": "Ki az előadó a 'Hold You - Hold Yuh' című dalban?",
            "options": ["Gyptian", "Sean Paul", "Shaggy", "Beenie Man"],
            "correct": 0,
            "explanation": "'Hold You - Hold Yuh' egy One Hit Wonder dal az előadótól: Gyptian",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 30
        },
        {
            "question": "Ki az előadó a 'Macarena' című dalban?",
            "options": ["Los del Río", "Ricky Martin", "Enrique Iglesias", "Shakira"],
            "correct": 0,
            "explanation": "'Macarena' egy One Hit Wonder dal az előadótól: Los del Río",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 31
        },
        {
            "question": "Ki az előadó a 'Gangnam Style' című dalban?",
            "options": ["PSY", "Big Bang", "2NE1", "Wonder Girls"],
            "correct": 0,
            "explanation": "'Gangnam Style' egy One Hit Wonder dal az előadótól: PSY",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 32
        },
        {
            "question": "Ki az előadó a 'Harlem Shake' című dalban?",
            "options": ["Baauer", "Skrillex", "Deadmau5", "Daft Punk"],
            "correct": 0,
            "explanation": "'Harlem Shake' egy One Hit Wonder dal az előadótól: Baauer",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 33
        },
        {
            "question": "Ki az előadó a 'Call Me Maybe' című dalban?",
            "options": ["Drake", "Coldplay", "Katy Perry", "Carly Rae Jepsen"],
            "correct": 3,
            "explanation": "'Call Me Maybe' egy One Hit Wonder dal az előadótól: Carly Rae Jepsen",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 34
        },
        {
            "question": "Ki az előadó a 'Royals' című dalban?",
            "options": ["Lorde", "Lana Del Rey", "Florence + The Machine", "Halsey"],
            "correct": 0,
            "explanation": "'Royals' egy One Hit Wonder dal az előadótól: Lorde",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 35
        },
        {
            "question": "Ki az előadó a 'Pumped Up Kicks' című dalban?",
            "options": ["Foster the People", "MGMT", "Passion Pit", "Vampire Weekend"],
            "correct": 0,
            "explanation": "'Pumped Up Kicks' egy One Hit Wonder dal az előadótól: Foster the People",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 36
        },
        {
            "question": "Ki az előadó a 'Some Nights' című dalban?",
            "options": ["fun.", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'Some Nights' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 37
        },
        {
            "question": "Ki az előadó a 'We Are Young' című dalban?",
            "options": ["fun.", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'We Are Young' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 38
        },
        {
            "question": "Ki az előadó a 'Radioactive' című dalban?",
            "options": ["Imagine Dragons", "Mumford & Sons", "The Lumineers", "Of Monsters and Men"],
            "correct": 0,
            "explanation": "'Radioactive' egy One Hit Wonder dal az előadótól: Imagine Dragons",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 40
        },
        {
            "question": "Ki az előadó a 'Sail' című dalban?",
            "options": ["AWOLNATION", "Imagine Dragons", "Mumford & Sons", "The Lumineers"],
            "correct": 0,
            "explanation": "'Sail' egy One Hit Wonder dal az előadótól: AWOLNATION",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 41
        },
        {
            "question": "Ki az előadó a 'Thrift Shop' című dalban?",
            "options": ["Beyoncé", "Bruno Mars", "Macklemore & Ryan Lewis", "Rihanna"],
            "correct": 2,
            "explanation": "'Thrift Shop' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 42
        },
        {
            "question": "Ki az előadó a 'Can't Hold Us' című dalban?",
            "options": ["Macklemore & Ryan Lewis", "Billie Eilish", "Drake", "Post Malone"],
            "correct": 0,
            "explanation": "'Can't Hold Us' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 43
        },
        {
            "question": "Ki az előadó a 'Get Lucky' című dalban?",
            "options": ["Daft Punk", "Justice", "The Chemical Brothers", "Basement Jaxx"],
            "correct": 0,
            "explanation": "'Get Lucky' egy One Hit Wonder dal az előadótól: Daft Punk",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 44
        },
        {
            "question": "Ki az előadó a 'Blurred Lines' című dalban?",
            "options": ["Robin Thicke", "Pharrell Williams", "Bruno Mars", "Justin Timberlake"],
            "correct": 0,
            "explanation": "'Blurred Lines' egy One Hit Wonder dal az előadótól: Robin Thicke",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 45
        },
        {
            "question": "Ki az előadó az 'Uptown Funk' című dalban?",
            "options": ["Mark Ronson ft. Bruno Mars", "Bruno Mars", "Pharrell Williams", "Justin Timberlake"],
            "correct": 0,
            "explanation": "'Uptown Funk' egy One Hit Wonder dal az előadótól: Mark Ronson ft. Bruno Mars",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 46
        },
        {
            "question": "Ki az előadó a 'Blank Space' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Lady Gaga", "Rihanna"],
            "correct": 0,
            "explanation": "'Blank Space' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 48
        },
        {
            "question": "Ki az előadó a 'Shut Up and Dance' című dalban?",
            "options": ["WALK THE MOON", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'Shut Up and Dance' egy One Hit Wonder dal az előadótól: WALK THE MOON",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 49
        },
        {
            "question": "Ki az előadó a 'Cheerleader' című dalban?",
            "options": ["OMI", "Sean Paul", "Shaggy", "Beenie Man"],
            "correct": 0,
            "explanation": "'Cheerleader' egy One Hit Wonder dal az előadótól: OMI",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 50
        },
        {
            "question": "Ki az előadó a 'See You Again' című dalban?",
            "options": ["Wiz Khalifa ft. Charlie Puth", "Charlie Puth", "Wiz Khalifa", "Post Malone"],
            "correct": 0,
            "explanation": "'See You Again' egy One Hit Wonder dal az előadótól: Wiz Khalifa ft. Charlie Puth",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 51
        },
        {
            "question": "Ki az előadó a 'Fancy' című dalban?",
            "options": ["Iggy Azalea ft. Charli XCX", "Iggy Azalea", "Charli XCX", "Rita Ora"],
            "correct": 0,
            "explanation": "'Fancy' egy One Hit Wonder dal az előadótól: Iggy Azalea ft. Charli XCX",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 52
        },
        {
            "question": "Ki az előadó az 'All About That Bass' című dalban?",
            "options": ["Meghan Trainor", "Ariana Grande", "Demi Lovato", "Selena Gomez"],
            "correct": 0,
            "explanation": "'All About That Bass' egy One Hit Wonder dal az előadótól: Meghan Trainor",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 53
        },
        {
            "question": "Ki az előadó a 'Despacito' című dalban?",
            "options": ["Luis Fonsi ft. Daddy Yankee", "Enrique Iglesias", "Ricky Martin", "Shakira"],
            "correct": 0,
            "explanation": "'Despacito' egy One Hit Wonder dal az előadótól: Luis Fonsi ft. Daddy Yankee",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 54
        },
        {
            "question": "Ki az előadó a 'Shape of You' című dalban?",
            "options": ["Ed Sheeran", "James Blunt", "Robbie Williams", "Gary Barlow"],
            "correct": 0,
            "explanation": "'Shape of You' egy One Hit Wonder dal az előadótól: Ed Sheeran",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 55
        },
        {
            "question": "Ki az előadó a 'Havana' című dalban?",
            "options": ["Camila Cabello", "Fifth Harmony", "Little Mix", "Fifth Harmony"],
            "correct": 0,
            "explanation": "'Havana' egy One Hit Wonder dal az előadótól: Camila Cabello",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 56
        },
        {
            "question": "Ki az előadó a 'New Rules' című dalban?",
            "options": ["Dua Lipa", "Rita Ora", "Charli XCX", "Rita Ora"],
            "correct": 0,
            "explanation": "'New Rules' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 57
        },
        {
            "question": "Ki az előadó a 'Bad Guy' című dalban?",
            "options": ["Billie Eilish", "Lorde", "Lana Del Rey", "Halsey"],
            "correct": 0,
            "explanation": "'Bad Guy' egy One Hit Wonder dal az előadótól: Billie Eilish",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 58
        },
        {
            "question": "Ki az előadó az 'Old Town Road' című dalban?",
            "options": ["Lil Nas X", "Post Malone", "Travis Scott", "Migos"],
            "correct": 0,
            "explanation": "'Old Town Road' egy One Hit Wonder dal az előadótól: Lil Nas X",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 59
        },
        {
            "question": "Ki az előadó a 'Dance Monkey' című dalban?",
            "options": ["Tones and I", "Billie Eilish", "Lorde", "Halsey"],
            "correct": 0,
            "explanation": "'Dance Monkey' egy One Hit Wonder dal az előadótól: Tones and I",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 60
        },
        {
            "question": "Ki az előadó a 'Blinding Lights' című dalban?",
            "options": ["The Weeknd", "Post Malone", "Drake", "Travis Scott"],
            "correct": 0,
            "explanation": "'Blinding Lights' egy One Hit Wonder dal az előadótól: The Weeknd",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 61
        },
        {
            "question": "Ki az előadó a 'Levitating' című dalban?",
            "options": ["Dua Lipa", "Rita Ora", "Charli XCX", "Rita Ora"],
            "correct": 0,
            "explanation": "'Levitating' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 62
        },
        {
            "question": "Ki az előadó a 'Stay' című dalban?",
            "options": ["The Kid LAROI & Justin Bieber", "Justin Bieber", "The Kid LAROI", "Post Malone"],
            "correct": 0,
            "explanation": "'Stay' egy One Hit Wonder dal az előadótól: The Kid LAROI & Justin Bieber",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 63
        },
        {
            "question": "Ki az előadó az 'As It Was' című dalban?",
            "options": ["Harry Styles", "One Direction", "Niall Horan", "Liam Payne"],
            "correct": 0,
            "explanation": "'As It Was' egy One Hit Wonder dal az előadótól: Harry Styles",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 64
        },
        {
            "question": "Ki az előadó a 'Flowers' című dalban?",
            "options": ["Miley Cyrus", "Selena Gomez", "Demi Lovato", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Flowers' egy One Hit Wonder dal az előadótól: Miley Cyrus",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 65
        },
        {
            "question": "Ki az előadó a 'Cruel Summer' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Lady Gaga", "Rihanna"],
            "correct": 0,
            "explanation": "'Cruel Summer' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 67
        },
        {
            "question": "Ki az előadó a 'Last Night' című dalban?",
            "options": ["Morgan Wallen", "Luke Combs", "Florida Georgia Line", "Blake Shelton"],
            "correct": 0,
            "explanation": "'Last Night' egy One Hit Wonder dal az előadótól: Morgan Wallen",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 68
        },
        {
            "question": "Ki az előadó a 'Smooth Criminal' című dalban?",
            "options": ["Michael Jackson", "Alien Ant Farm", "The Weeknd", "Bruno Mars"],
            "correct": 1,
            "explanation": "'Smooth Criminal' egy One Hit Wonder dal az előadótól: Alien Ant Farm",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 69
        },
        {
            "question": "Ki az előadó a 'Lemon Tree' című dalban?",
            "options": ["Fools Garden", "The Cranberries", "The Cardigans", "The Corrs"],
            "correct": 0,
            "explanation": "'Lemon Tree' egy One Hit Wonder dal az előadótól: Fools Garden",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "original_index": 70
        },
        {
            "question": "Ki az előadó a 'Stolen Dance' című dalban?",
            "options": ["Milky Chance", "Of Monsters and Men", "Vance Joy", "Passenger"],
            "correct": 0,
            "explanation": "'Stolen Dance' egy One Hit Wonder dal az előadótól: Milky Chance",
            "topic": "one_hit_wonders",
            "preview_duration": 120,
            "original_index": 71
        },
        {
            "question": "Ki az előadó?",
            "audio_file": "audio_files/one_hit_wonders/Ylvis - Mr. Toot [Official music video HD].mp3",
            "options": ["Ylvis", "Bastille", "Imagine Dragons", "Szerkeszthető opció"],
            "correct": 0,
            "explanation": "Ylvis - One Hit Wonder előadó",
            "topic": "one_hit_wonders",
            "original_index": 72
        }
    ]

# Dinamikus kérdések exportálása
ONE_HIT_WONDERS_QUESTIONS = get_one_hit_wonders_questions_dynamic(60)

if __name__ == "__main__":
    print("🎵 One Hit Wonders Kérdések Tesztelése")
    print("=" * 40)
    
    questions = get_one_hit_wonders_questions_dynamic(5)
    print(f"Generált kérdések száma: {len(questions)}")
    
    for i, q in enumerate(questions[:3]):
        print(f"\n{i+1}. {q['question']}")
        print(f"   Válaszopciók: {q['options']}")
        print(f"   Helyes: {q['options'][q['correct']]}") 