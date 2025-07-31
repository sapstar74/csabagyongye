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
    """Statikus One Hit Wonders kérdések fallback esetén - 60 kérdés"""
    return [
        {
            "question": "Ki az előadó a 'Teenage Dirtbag' című dalban?",
            "options": ["Wheatus", "Blink-182", "Sum 41", "Good Charlotte"],
            "correct": 0,
            "explanation": "'Teenage Dirtbag' egy One Hit Wonder dal az előadótól: Wheatus",
            "topic": "one_hit_wonders",
            "preview_duration": 90,
            "preview_duration": 90
        },
        {
            "question": "Ki az előadó a 'Somebody That I Used To Know' című dalban?",
            "options": ["Gotye", "Passenger", "James Blunt", "Ed Sheeran"],
            "correct": 0,
            "explanation": "'Somebody That I Used To Know' egy One Hit Wonder dal az előadótól: Gotye",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Little Talks' című dalban?",
            "options": ["Of Monsters and Men", "Mumford & Sons", "The Lumineers", "Imagine Dragons"],
            "correct": 0,
            "explanation": "'Little Talks' egy One Hit Wonder dal az előadótól: Of Monsters and Men",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Tainted Love' című dalban?",
            "options": ["Soft Cell", "Depeche Mode", "New Order", "The Cure"],
            "correct": 0,
            "explanation": "'Tainted Love' egy One Hit Wonder dal az előadótól: Soft Cell",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Return of the Mack' című dalban?",
            "options": ["Mark Morrison", "Maxi Priest", "Shabba Ranks", "Shaggy"],
            "correct": 0,
            "explanation": "'Return of the Mack' egy One Hit Wonder dal az előadótól: Mark Morrison",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Butterfly' című dalban?",
            "options": ["Crazy Town", "Limp Bizkit", "Korn", "Linkin Park"],
            "correct": 0,
            "explanation": "'Butterfly' egy One Hit Wonder dal az előadótól: Crazy Town",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Young Folks' című dalban?",
            "options": ["Peter Bjorn and John", "The Shins", "Death Cab for Cutie", "The Postal Service"],
            "correct": 0,
            "explanation": "'Young Folks' egy One Hit Wonder dal az előadótól: Peter Bjorn and John",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Bad Day' című dalban?",
            "options": ["Daniel Powter", "James Blunt", "Robbie Williams", "Gary Barlow"],
            "correct": 0,
            "explanation": "'Bad Day' egy One Hit Wonder dal az előadótól: Daniel Powter",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Stacy's Mom' című dalban?",
            "options": ["Fountains Of Wayne", "Weezer", "Blink-182", "Green Day"],
            "correct": 0,
            "explanation": "'Stacy's Mom' egy One Hit Wonder dal az előadótól: Fountains Of Wayne",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Cotton Eye Joe' című dalban?",
            "options": ["Rednex", "Village People", "Boney M", "ABBA"],
            "correct": 0,
            "explanation": "'Cotton Eye Joe' egy One Hit Wonder dal az előadótól: Rednex",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Two Princes' című dalban?",
            "options": ["Spin Doctors", "Blues Traveler", "Hootie & the Blowfish", "Counting Crows"],
            "correct": 0,
            "explanation": "'Two Princes' egy One Hit Wonder dal az előadótól: Spin Doctors",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Bitch' című dalban?",
            "options": ["Meredith Brooks", "Alanis Morissette", "Sheryl Crow", "Fiona Apple"],
            "correct": 0,
            "explanation": "'Bitch' egy One Hit Wonder dal az előadótól: Meredith Brooks",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'My Sharona' című dalban?",
            "options": ["The Knack", "The Cars", "The Police", "The Pretenders"],
            "correct": 0,
            "explanation": "'My Sharona' egy One Hit Wonder dal az előadótól: The Knack",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Ice Ice Baby' című dalban?",
            "options": ["Vanilla Ice", "MC Hammer", "Tone Loc", "Young MC"],
            "correct": 0,
            "explanation": "'Ice Ice Baby' egy One Hit Wonder dal az előadótól: Vanilla Ice",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Billionaire' című dalban?",
            "options": ["Travie McCoy", "Flo Rida", "Pitbull", "Sean Paul"],
            "correct": 0,
            "explanation": "'Billionaire' egy One Hit Wonder dal az előadótól: Travie McCoy",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Video Killed The Radio Star' című dalban?",
            "options": ["The Buggles", "The Cars", "The Police", "The Pretenders"],
            "correct": 0,
            "explanation": "'Video Killed The Radio Star' egy One Hit Wonder dal az előadótól: The Buggles",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Walking in Memphis' című dalban?",
            "options": ["Marc Cohn", "Bruce Hornsby", "Don Henley", "Jackson Browne"],
            "correct": 0,
            "explanation": "'Walking in Memphis' egy One Hit Wonder dal az előadótól: Marc Cohn",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Saturday Night' című dalban?",
            "options": ["Whigfield", "Corona", "Real McCoy", "La Bouche"],
            "correct": 0,
            "explanation": "'Saturday Night' egy One Hit Wonder dal az előadótól: Whigfield",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Who Let The Dogs Out' című dalban?",
            "options": ["Baha Men", "Vengaboys", "Aqua", "Eiffel 65"],
            "correct": 0,
            "explanation": "'Who Let The Dogs Out' egy One Hit Wonder dal az előadótól: Baha Men",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shake It' című dalban?",
            "options": ["Metro Station", "Cobra Starship", "The All-American Rejects", "Panic! At The Disco"],
            "correct": 0,
            "explanation": "'Shake It' egy One Hit Wonder dal az előadótól: Metro Station",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Informer' című dalban?",
            "options": ["Snow", "Vanilla Ice", "MC Hammer", "Tone Loc"],
            "correct": 0,
            "explanation": "'Informer' egy One Hit Wonder dal az előadótól: Snow",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Jerk It Out' című dalban?",
            "options": ["Caesars", "The Strokes", "The Hives", "The Vines"],
            "correct": 0,
            "explanation": "'Jerk It Out' egy One Hit Wonder dal az előadótól: Caesars",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Heartbeats' című dalban?",
            "options": ["José González", "Iron & Wine", "Bon Iver", "Fleet Foxes"],
            "correct": 0,
            "explanation": "'Heartbeats' egy One Hit Wonder dal az előadótól: José González",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Rude' című dalban?",
            "options": ["MAGIC!", "Passenger", "James Blunt", "Ed Sheeran"],
            "correct": 0,
            "explanation": "'Rude' egy One Hit Wonder dal az előadótól: MAGIC!",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Turn Me On' című dalban?",
            "options": ["Kevin Lyttle", "Sean Paul", "Shaggy", "Beenie Man"],
            "correct": 0,
            "explanation": "'Turn Me On' egy One Hit Wonder dal az előadótól: Kevin Lyttle",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Ring My Bell' című dalban?",
            "options": ["Anita Ward", "Gloria Gaynor", "Donna Summer", "Diana Ross"],
            "correct": 0,
            "explanation": "'Ring My Bell' egy One Hit Wonder dal az előadótól: Anita Ward",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'It Just Won't Do' című dalban?",
            "options": ["Tim Deluxe", "Fatboy Slim", "The Chemical Brothers", "Prodigy"],
            "correct": 0,
            "explanation": "'It Just Won't Do' egy One Hit Wonder dal az előadótól: Tim Deluxe",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Safety Dance' című dalban?",
            "options": ["Men Without Hats", "Devo", "Talking Heads", "The B-52's"],
            "correct": 0,
            "explanation": "'Safety Dance' egy One Hit Wonder dal az előadótól: Men Without Hats",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'I Love It' című dalban?",
            "options": ["Icona Pop", "Tove Lo", "Ellie Goulding", "Lorde"],
            "correct": 0,
            "explanation": "'I Love It' egy One Hit Wonder dal az előadótól: Icona Pop",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Hold You - Hold Yuh' című dalban?",
            "options": ["Gyptian", "Sean Paul", "Shaggy", "Beenie Man"],
            "correct": 0,
            "explanation": "'Hold You - Hold Yuh' egy One Hit Wonder dal az előadótól: Gyptian",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Macarena' című dalban?",
            "options": ["Los del Río", "Ricky Martin", "Enrique Iglesias", "Shakira"],
            "correct": 0,
            "explanation": "'Macarena' egy One Hit Wonder dal az előadótól: Los del Río",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Gangnam Style' című dalban?",
            "options": ["PSY", "Big Bang", "2NE1", "Wonder Girls"],
            "correct": 0,
            "explanation": "'Gangnam Style' egy One Hit Wonder dal az előadótól: PSY",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Harlem Shake' című dalban?",
            "options": ["Baauer", "Skrillex", "Deadmau5", "Daft Punk"],
            "correct": 0,
            "explanation": "'Harlem Shake' egy One Hit Wonder dal az előadótól: Baauer",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Call Me Maybe' című dalban?",
            "options": ["Carly Rae Jepsen", "Katy Perry", "Taylor Swift", "Selena Gomez"],
            "correct": 0,
            "explanation": "'Call Me Maybe' egy One Hit Wonder dal az előadótól: Carly Rae Jepsen",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Royals' című dalban?",
            "options": ["Lorde", "Lana Del Rey", "Halsey", "Billie Eilish"],
            "correct": 0,
            "explanation": "'Royals' egy One Hit Wonder dal az előadótól: Lorde",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Pumped Up Kicks' című dalban?",
            "options": ["Foster the People", "MGMT", "Vampire Weekend", "The Strokes"],
            "correct": 0,
            "explanation": "'Pumped Up Kicks' egy One Hit Wonder dal az előadótól: Foster the People",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Some Nights' című dalban?",
            "options": ["fun.", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'Some Nights' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'We Are Young' című dalban?",
            "options": ["fun.", "Panic! At The Disco", "Fall Out Boy", "My Chemical Romance"],
            "correct": 0,
            "explanation": "'We Are Young' egy One Hit Wonder dal az előadótól: fun.",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Ho Hey' című dalban?",
            "options": ["The Lumineers", "Mumford & Sons", "Of Monsters and Men", "The Avett Brothers"],
            "correct": 0,
            "explanation": "'Ho Hey' egy One Hit Wonder dal az előadótól: The Lumineers",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Radioactive' című dalban?",
            "options": ["Imagine Dragons", "Mumford & Sons", "Of Monsters and Men", "The Lumineers"],
            "correct": 0,
            "explanation": "'Radioactive' egy One Hit Wonder dal az előadótól: Imagine Dragons",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Sail' című dalban?",
            "options": ["AWOLNATION", "Imagine Dragons", "Mumford & Sons", "Of Monsters and Men"],
            "correct": 0,
            "explanation": "'Sail' egy One Hit Wonder dal az előadótól: AWOLNATION",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Thrift Shop' című dalban?",
            "options": ["Macklemore & Ryan Lewis", "Eminem", "Kendrick Lamar", "Drake"],
            "correct": 0,
            "explanation": "'Thrift Shop' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Can't Hold Us' című dalban?",
            "options": ["Macklemore & Ryan Lewis", "Eminem", "Kendrick Lamar", "Drake"],
            "correct": 0,
            "explanation": "'Can't Hold Us' egy One Hit Wonder dal az előadótól: Macklemore & Ryan Lewis",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Get Lucky' című dalban?",
            "options": ["Daft Punk", "Justice", "The Chemical Brothers", "Prodigy"],
            "correct": 0,
            "explanation": "'Get Lucky' egy One Hit Wonder dal az előadótól: Daft Punk",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Blurred Lines' című dalban?",
            "options": ["Robin Thicke", "Justin Timberlake", "Usher", "Chris Brown"],
            "correct": 0,
            "explanation": "'Blurred Lines' egy One Hit Wonder dal az előadótól: Robin Thicke",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Uptown Funk' című dalban?",
            "options": ["Mark Ronson ft. Bruno Mars", "Bruno Mars", "Pharrell Williams", "Justin Timberlake"],
            "correct": 0,
            "explanation": "'Uptown Funk' egy One Hit Wonder dal az előadótól: Mark Ronson ft. Bruno Mars",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shake It Off' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Shake It Off' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Blank Space' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Blank Space' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shut Up and Dance' című dalban?",
            "options": ["WALK THE MOON", "The 1975", "Panic! At The Disco", "Fall Out Boy"],
            "correct": 0,
            "explanation": "'Shut Up and Dance' egy One Hit Wonder dal az előadótól: WALK THE MOON",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Cheerleader' című dalban?",
            "options": ["OMI", "Jason Derulo", "Pitbull", "Flo Rida"],
            "correct": 0,
            "explanation": "'Cheerleader' egy One Hit Wonder dal az előadótól: OMI",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'See You Again' című dalban?",
            "options": ["Wiz Khalifa ft. Charlie Puth", "Eminem", "Kendrick Lamar", "Drake"],
            "correct": 0,
            "explanation": "'See You Again' egy One Hit Wonder dal az előadótól: Wiz Khalifa ft. Charlie Puth",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Fancy' című dalban?",
            "options": ["Iggy Azalea ft. Charli XCX", "Nicki Minaj", "Cardi B", "Megan Thee Stallion"],
            "correct": 0,
            "explanation": "'Fancy' egy One Hit Wonder dal az előadótól: Iggy Azalea ft. Charli XCX",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'All About That Bass' című dalban?",
            "options": ["Meghan Trainor", "Ariana Grande", "Selena Gomez", "Demi Lovato"],
            "correct": 0,
            "explanation": "'All About That Bass' egy One Hit Wonder dal az előadótól: Meghan Trainor",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Uptown Funk' című dalban?",
            "options": ["Mark Ronson ft. Bruno Mars", "Bruno Mars", "Pharrell Williams", "Justin Timberlake"],
            "correct": 0,
            "explanation": "'Uptown Funk' egy One Hit Wonder dal az előadótól: Mark Ronson ft. Bruno Mars",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shake It Off' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Shake It Off' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Blank Space' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Blank Space' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shut Up and Dance' című dalban?",
            "options": ["WALK THE MOON", "The 1975", "Panic! At The Disco", "Fall Out Boy"],
            "correct": 0,
            "explanation": "'Shut Up and Dance' egy One Hit Wonder dal az előadótól: WALK THE MOON",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Cheerleader' című dalban?",
            "options": ["OMI", "Jason Derulo", "Pitbull", "Flo Rida"],
            "correct": 0,
            "explanation": "'Cheerleader' egy One Hit Wonder dal az előadótól: OMI",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'See You Again' című dalban?",
            "options": ["Wiz Khalifa ft. Charlie Puth", "Eminem", "Kendrick Lamar", "Drake"],
            "correct": 0,
            "explanation": "'See You Again' egy One Hit Wonder dal az előadótól: Wiz Khalifa ft. Charlie Puth",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Fancy' című dalban?",
            "options": ["Iggy Azalea ft. Charli XCX", "Nicki Minaj", "Cardi B", "Megan Thee Stallion"],
            "correct": 0,
            "explanation": "'Fancy' egy One Hit Wonder dal az előadótól: Iggy Azalea ft. Charli XCX",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'All About That Bass' című dalban?",
            "options": ["Meghan Trainor", "Ariana Grande", "Selena Gomez", "Demi Lovato"],
            "correct": 0,
            "explanation": "'All About That Bass' egy One Hit Wonder dal az előadótól: Meghan Trainor",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Despacito' című dalban?",
            "options": ["Luis Fonsi ft. Daddy Yankee", "Shakira", "Ricky Martin", "Enrique Iglesias"],
            "correct": 0,
            "explanation": "'Despacito' egy One Hit Wonder dal az előadótól: Luis Fonsi ft. Daddy Yankee",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Shape of You' című dalban?",
            "options": ["Ed Sheeran", "James Blunt", "Passenger", "Sam Smith"],
            "correct": 0,
            "explanation": "'Shape of You' egy One Hit Wonder dal az előadótól: Ed Sheeran",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Havana' című dalban?",
            "options": ["Camila Cabello", "Selena Gomez", "Ariana Grande", "Demi Lovato"],
            "correct": 0,
            "explanation": "'Havana' egy One Hit Wonder dal az előadótól: Camila Cabello",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'New Rules' című dalban?",
            "options": ["Dua Lipa", "Ariana Grande", "Selena Gomez", "Demi Lovato"],
            "correct": 0,
            "explanation": "'New Rules' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Bad Guy' című dalban?",
            "options": ["Billie Eilish", "Lorde", "Lana Del Rey", "Halsey"],
            "correct": 0,
            "explanation": "'Bad Guy' egy One Hit Wonder dal az előadótól: Billie Eilish",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Old Town Road' című dalban?",
            "options": ["Lil Nas X", "Post Malone", "Travis Scott", "Lil Baby"],
            "correct": 0,
            "explanation": "'Old Town Road' egy One Hit Wonder dal az előadótól: Lil Nas X",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Dance Monkey' című dalban?",
            "options": ["Tones and I", "Billie Eilish", "Lorde", "Lana Del Rey"],
            "correct": 0,
            "explanation": "'Dance Monkey' egy One Hit Wonder dal az előadótól: Tones and I",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Blinding Lights' című dalban?",
            "options": ["The Weeknd", "Post Malone", "Drake", "Travis Scott"],
            "correct": 0,
            "explanation": "'Blinding Lights' egy One Hit Wonder dal az előadótól: The Weeknd",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Levitating' című dalban?",
            "options": ["Dua Lipa", "Ariana Grande", "Selena Gomez", "Demi Lovato"],
            "correct": 0,
            "explanation": "'Levitating' egy One Hit Wonder dal az előadótól: Dua Lipa",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Stay' című dalban?",
            "options": ["The Kid LAROI & Justin Bieber", "Justin Bieber", "Post Malone", "Drake"],
            "correct": 0,
            "explanation": "'Stay' egy One Hit Wonder dal az előadótól: The Kid LAROI & Justin Bieber",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'As It Was' című dalban?",
            "options": ["Harry Styles", "One Direction", "Niall Horan", "Liam Payne"],
            "correct": 0,
            "explanation": "'As It Was' egy One Hit Wonder dal az előadótól: Harry Styles",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Flowers' című dalban?",
            "options": ["Miley Cyrus", "Selena Gomez", "Demi Lovato", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Flowers' egy One Hit Wonder dal az előadótól: Miley Cyrus",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Vampire' című dalban?",
            "options": ["Olivia Rodrigo", "Billie Eilish", "Lorde", "Lana Del Rey"],
            "correct": 0,
            "explanation": "'Vampire' egy One Hit Wonder dal az előadótól: Olivia Rodrigo",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Cruel Summer' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Cruel Summer' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Last Night' című dalban?",
            "options": ["Morgan Wallen", "Luke Combs", "Florida Georgia Line", "Dan + Shay"],
            "correct": 0,
            "explanation": "'Last Night' egy One Hit Wonder dal az előadótól: Morgan Wallen",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Vampire' című dalban?",
            "options": ["Olivia Rodrigo", "Billie Eilish", "Lorde", "Lana Del Rey"],
            "correct": 0,
            "explanation": "'Vampire' egy One Hit Wonder dal az előadótól: Olivia Rodrigo",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Cruel Summer' című dalban?",
            "options": ["Taylor Swift", "Katy Perry", "Selena Gomez", "Ariana Grande"],
            "correct": 0,
            "explanation": "'Cruel Summer' egy One Hit Wonder dal az előadótól: Taylor Swift",
            "topic": "one_hit_wonders",
            "preview_duration": 90},
        {
            "question": "Ki az előadó a 'Last Night' című dalban?",
            "options": ["Morgan Wallen", "Luke Combs", "Florida Georgia Line", "Dan + Shay"],
            "correct": 0,
            "explanation": "'Last Night' egy One Hit Wonder dal az előadótól: Morgan Wallen",
            "topic": "one_hit_wonders",
            "preview_duration": 90}
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