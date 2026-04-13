# „Álmomból felébresztve” – zenei playlist a PDF alapján; audio útvonalak az audio_files mappához képest.

_TOPIC = "almombol_felebresztve"
_DEFAULT_QUESTION = "Ki az előadó?"


def _q(audio_subpath, correct, options, explanation, question=_DEFAULT_QUESTION):
    """audio_subpath: pl. one_hit_wonders/fájl.mp3 – az audio_files mappához képest."""
    return {
        "question": question,
        "options": options,
        "correct": correct,
        "explanation": explanation,
        "audio_file": audio_subpath,
        "topic": _TOPIC,
    }


QUESTIONS = [
    _q("nemzetkozi_zenekarok/114_Green_Day_Basket_Case.mp3", 0, ["Green Day", "Blink-182", "Sum 41", "Good Charlotte"], "Green Day – Basket Case"),
    _q("nemzetkozi_zenekarok/107_Green_Day.mp3", 0, ["Green Day", "Blink-182", "Sum 41", "The Offspring"], "Green Day – Boulevard of Broken Dreams"),
    _q("one_hit_wonders/Journey - Dont Stop Believin.mp3", 0, ["Journey", "Foreigner", "Boston", "REO Speedwagon"], "Journey – Don't Stop Believin'"),
    _q("nemzetkozi_zenekarok/115_Lynyrd_Skynyrd_Sweet_Home_Alabama.mp3", 0, ["Lynyrd Skynyrd", "ZZ Top", "The Allman Brothers Band", "Creedence Clearwater Revival"], "Lynyrd Skynyrd – Sweet Home Alabama"),
    _q("nemzetkozi_zenekarok/116_Goo_Goo_Dolls_Iris.mp3", 0, ["Goo Goo Dolls", "Third Eye Blind", "Matchbox Twenty", "Counting Crows"], "Goo Goo Dolls – Iris"),
    _q("nemzetkozi_zenekarok/105_Jefferson_Airplane.mp3", 0, ["Jefferson Airplane", "The Doors", "Janis Joplin", "Grateful Dead"], "Jefferson Airplane – Somebody to Love"),
    _q("one_hit_wonders/49_WALK THE MOON_Shut Up and Dance.mp3", 0, ["WALK THE MOON", "Imagine Dragons", "OneRepublic", "Fun."], "WALK THE MOON – Shut Up and Dance"),
    _q("one_hit_wonders/Big Mountain - Baby I Love Your Way.mp3", 0, ["Big Mountain", "UB40", "Inner Circle", "Shaggy"], "Big Mountain – Baby, I Love Your Way"),
    _q("one_hit_wonders/Plain White Ts - Hey There Delilah.mp3", 0, ["Plain White T's", "The Fray", "Augustana", "Secondhand Serenade"], "Plain White T's – Hey There Delilah"),
    _q("one_hit_wonders/Taco - Puttin on the Ritz.mp3", 0, ["Taco", "Falco", "Peter Schilling", "Nena"], "Taco – Puttin' on the Ritz"),
    _q("one_hit_wonders/Jimmy Cliff - I Can See Clearly Now.mp3", 0, ["Jimmy Cliff", "Johnny Nash", "Bob Marley", "Toots and the Maytals"], "Jimmy Cliff – I Can See Clearly Now"),
    _q("one_hit_wonders/37_fun._Some Nights.mp3", 0, ["fun.", "Imagine Dragons", "Foster the People", "Walk the Moon"], "fun. – Some Nights"),
    _q("one_hit_wonders/38_fun._We Are Young.mp3", 0, ["fun.", "The Lumineers", "Of Monsters and Men", "Passion Pit"], "fun. – We Are Young"),
    _q("one_hit_wonders/01_Wheatus_Teenage Dirtbag.mp3", 0, ["Wheatus", "Bowling for Soup", "Sum 41", "Good Charlotte"], "Wheatus – Teenage Dirtbag"),
    _q("one_hit_wonders/Inner Circle - Bad Boys.mp3", 0, ["Inner Circle", "Shaggy", "Sean Paul", "Bob Marley"], "Inner Circle – Bad Boys"),
    _q("one_hit_wonders/66. RamJam - Black Betty.mp3", 0, ["Ram Jam", "Led Zeppelin", "CCR", "Steppenwolf"], "Ram Jam – Black Betty"),
    _q("one_hit_wonders/Billy Paul - Me And Mrs. Jones.mp3", 0, ["Billy Paul", "Barry White", "Marvin Gaye", "Bill Withers"], "Billy Paul – Me and Mrs. Jones"),
    _q("one_hit_wonders/Marc Cohn - Walking in Memphis.mp3", 0, ["Marc Cohn", "Bruce Springsteen", "Billy Joel", "Elton John"], "Marc Cohn – Walking in Memphis"),
    _q("nemzetkozi_zenekarok/117_T_Rex_20th_Century_Boy.mp3", 0, ["T. Rex", "Slade", "Sweet", "Mott the Hoople"], "T. Rex – 20th Century Boy"),
    _q("one_hit_wonders/Carl Douglas - Kung Fu Fighting.mp3", 0, ["Carl Douglas", "Boney M.", "Village People", "KC and the Sunshine Band"], "Carl Douglas – Kung Fu Fighting"),
    _q("one_hit_wonders/London Beat - Ive Been Thinking About You.mp3", 0, ["London Beat", "Swing Out Sister", "Lisa Stansfield", "Soul II Soul"], "London Beat – I've Been Thinking About You"),
    _q("one_hit_wonders/70_Fools Garden_Lemon Tree.mp3", 0, ["Fools Garden", "The Cranberries", "Sixpence None the Richer", "Savage Garden"], "Fools Garden – Lemon Tree"),
    _q("one_hit_wonders/Technotronic - Pump Up the Jam.mp3", 0, ["Technotronic", "Black Box", "C+C Music Factory", "Snap!"], "Technotronic – Pump Up the Jam"),
    _q("one_hit_wonders/The Proclaimers - 500 Miles.mp3", 0, ["The Proclaimers", "Dexys Midnight Runners", "The Waterboys", "Simple Minds"], "The Proclaimers – I'm Gonna Be (500 Miles)"),
    _q("one_hit_wonders/Sir Mix-A-Lot - Baby Got Back.mp3", 0, ["Sir Mix-A-Lot", "Vanilla Ice", "MC Hammer", "Tone Lōc"], "Sir Mix-A-Lot – Baby Got Back"),
    _q("one_hit_wonders/New Radicals - You Get What You Give.mp3", 0, ["New Radicals", "Counting Crows", "Third Eye Blind", "Semisonic"], "New Radicals – You Get What You Give"),
    _q("one_hit_wonders/Bow Wow Wow - I Want Candy.mp3", 0, ["Bow Wow Wow", "The B-52's", "Devo", "Talking Heads"], "Bow Wow Wow – I Want Candy"),
    _q("one_hit_wonders/16_The Buggles_Video Killed The Radio Star.mp3", 0, ["The Buggles", "Gary Numan", "Kraftwerk", "Human League"], "The Buggles – Video Killed the Radio Star"),
    _q("one_hit_wonders/Cascada - Everytime We Touch.mp3", 0, ["Cascada", "ATB", "Scooter", "Groove Coverage"], "Cascada – Everytime We Touch"),
    _q("one_hit_wonders/08_Daniel Powter_Bad Day.mp3", 0, ["Daniel Powter", "James Blunt", "Jason Mraz", "John Mayer"], "Daniel Powter – Bad Day"),
    _q("one_hit_wonders/Cheryl Lynn - Got to Be Real.mp3", 0, ["Cheryl Lynn", "Chaka Khan", "Donna Summer", "Gloria Gaynor"], "Cheryl Lynn – Got to Be Real"),
    _q("one_hit_wonders/45_Robin Thicke_Blurred Lines.mp3", 0, ["Robin Thicke", "Pharrell Williams", "Justin Timberlake", "Bruno Mars"], "Robin Thicke – Blurred Lines"),
    _q("one_hit_wonders/59_Lil Nas X_Old Town Road.mp3", 0, ["Lil Nas X", "Post Malone", "Travis Scott", "Drake"], "Lil Nas X – Old Town Road"),
    _q("one_hit_wonders/54_Luis Fonsi ft. Daddy Yankee_Despacito.mp3", 0, ["Luis Fonsi", "Daddy Yankee", "Maluma", "J Balvin"], "Luis Fonsi ft. Daddy Yankee – Despacito"),
    _q("one_hit_wonders/Dexys Midnight Runners - Come On Eileen.mp3", 0, ["Dexys Midnight Runners", "The Pogues", "The Smiths", "The Cure"], "Dexys Midnight Runners – Come On Eileen"),
    _q("one_hit_wonders/28_Men Without Hats_Safety Dance.mp3", 0, ["Men Without Hats", "A Flock of Seagulls", "Soft Cell", "Tears for Fears"], "Men Without Hats – The Safety Dance"),
    _q("one_hit_wonders/Van McCoy - The Hustle.mp3", 0, ["Van McCoy", "KC and the Sunshine Band", "Chic", "Earth, Wind & Fire"], "Van McCoy – The Hustle"),
    _q("one_hit_wonders/23_José González_Heartbeats.mp3", 0, ["José González", "Iron & Wine", "Bon Iver", "Sufjan Stevens"], "José González – Heartbeats"),
    _q("one_hit_wonders/26_Anita Ward_Ring My Bell.mp3", 0, ["Anita Ward", "Gloria Gaynor", "Donna Summer", "Sister Sledge"], "Anita Ward – Ring My Bell"),
    _q("nemzetkozi_zenekarok/118_Boston_More_Than_a_Feeling.mp3", 0, ["Boston", "Journey", "REO Speedwagon", "Styx"], "Boston – More Than a Feeling"),
    _q("one_hit_wonders/24_MAGIC!_Rude.mp3", 0, ["MAGIC!", "Maroon 5", "Train", "Jason Mraz"], "MAGIC! – Rude"),
    _q("one_hit_wonders/50_OMI_Cheerleader.mp3", 0, ["OMI", "Sean Paul", "Shaggy", "Major Lazer"], "OMI – Cheerleader"),
    _q("one_hit_wonders/09_Murray Head_One Night in Bangkok.mp3", 0, ["Murray Head", "ABBA", "Elton John", "Andrew Lloyd Webber"], "Murray Head – One Night in Bangkok"),
    _q("one_hit_wonders/Tom Cochrane - Life Is a Highway.mp3", 0, ["Tom Cochrane", "John Mellencamp", "Bryan Adams", "Bob Seger"], "Tom Cochrane – Life Is a Highway"),
    _q("one_hit_wonders/Terry Jacks - Seasons in the Sun.mp3", 0, ["Terry Jacks", "Cat Stevens", "Rod Stewart", "Elton John"], "Terry Jacks – Seasons in the Sun"),
    _q("one_hit_wonders/John Denver - Take Me Home Country Roads.mp3", 0, ["John Denver", "Willie Nelson", "Glen Campbell", "Kenny Rogers"], "John Denver – Take Me Home, Country Roads"),
    _q("one_hit_wonders/Michael Sembello - Maniac.mp3", 0, ["Michael Sembello", "Kenny Loggins", "Irene Cara", "Donna Summer"], "Michael Sembello – Maniac"),
    _q("nemzetkozi_zenekarok/119_Smash_Mouth_Walking_on_the_Sun.mp3", 0, ["Smash Mouth", "Third Eye Blind", "Sugar Ray", "Barenaked Ladies"], "Smash Mouth – Walking on the Sun"),
    _q("one_hit_wonders/22_Caesars_Jerk It Out.mp3", 0, ["Caesars", "The Hives", "The Vines", "Jet"], "Caesars – Jerk It Out"),
    _q("one_hit_wonders/Wild Cherry - Play That Funky Music.mp3", 0, ["Wild Cherry", "Kool & the Gang", "Earth, Wind & Fire", "Commodores"], "Wild Cherry – Play That Funky Music"),
    _q("one_hit_wonders/Deep Blue Something - Breakfast at Tiffanys.mp3", 0, ["Deep Blue Something", "Toad the Wet Sprocket", "Gin Blossoms", "Dishwalla"], "Deep Blue Something – Breakfast at Tiffany's"),
    _q("one_hit_wonders/36_Foster the People_Pumped Up Kicks.mp3", 0, ["Foster the People", "MGMT", "Two Door Cinema Club", "Passion Pit"], "Foster the People – Pumped Up Kicks"),
    _q("nemzetkozi_zenekarok/120_Counting_Crows_Mr_Jones.mp3", 0, ["Counting Crows", "Gin Blossoms", "Matchbox Twenty", "Third Eye Blind"], "Counting Crows – Mr. Jones"),
    _q("nemzetkozi_zenekarok/121_Counting_Crows_Big_Yellow_Taxi.mp3", 0, ["Counting Crows", "Joni Mitchell", "Sheryl Crow", "Alanis Morissette"], "Counting Crows – Big Yellow Taxi"),
    _q("one_hit_wonders/Goodboys - Bongo Cha Cha Cha.mp3", 0, ["Goodboys", "Vize", "Felix Jaehn", "Topic"], "Goodboys – Bongo Cha Cha Cha"),
    _q("one_hit_wonders/Louis Prima - Just a Gigolo.mp3", 0, ["Louis Prima", "Dean Martin", "Frank Sinatra", "Bobby Darin"], "Louis Prima – Just a Gigolo"),
]

ALMOMBOL_FELEBRESZTVE_QUESTIONS = QUESTIONS
