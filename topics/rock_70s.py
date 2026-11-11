# „Klasszikus rock” (korábban: 70s Rock) – zenei kategória; súlypontja a 70-es évek, de 1964–1988 közötti dalok (és egy 2003-as retró rock: Jet) is vannak benne.
#
# Az audio útvonalak az audio_files mappához képest értendők.
#   * A már meglévő felvételeket (one_hit_wonders/, nemzetkozi_zenekarok/, rock_metal/) újrahasznosítjuk.
#   * Az új számok helye: audio_files/rock_70s/<fájlnév>. Amíg egy mp3 nincs meg, a kérdése
#     automatikusan kimarad (ROCK_70S_QUESTIONS csak a lejátszható kérdéseket tartalmazza).
#
# Hiányzó fájlok listája:   python3 -m topics.rock_70s

from pathlib import Path

_TOPIC = "rock_70s"
_DEFAULT_QUESTION = "Ki az előadó?"
_AUDIO_ROOT = Path(__file__).resolve().parent.parent / "audio_files"


def _q(audio_subpath, artist, distractors, song, year):
    """Egy kérdés. A helyes válasz helye a dalcímtől függően fix, de kérdésenként változó."""
    pos = sum(map(ord, song)) % (len(distractors) + 1)
    options = list(distractors)
    options.insert(pos, artist)
    return {
        "question": _DEFAULT_QUESTION,
        "options": options,
        "correct": pos,
        "explanation": f"{artist} – {song} ({year})",
        "song_title": song,
        "audio_file": audio_subpath,
        "topic": _TOPIC,
    }


def _new(n, slug):
    return f"rock_70s/{n:02d}_{slug}.mp3"


_ALL = [
    # --- Már meglévő felvételek ---
    _q("nemzetkozi_zenekarok/115_Lynyrd_Skynyrd_Sweet_Home_Alabama.mp3", "Lynyrd Skynyrd", ["The Allman Brothers Band", "Creedence Clearwater Revival", "ZZ Top"], "Sweet Home Alabama", 1974),
    _q("nemzetkozi_zenekarok/118_Boston_More_Than_a_Feeling.mp3", "Boston", ["Foreigner", "Journey", "Kansas"], "More Than a Feeling", 1976),
    _q("nemzetkozi_zenekarok/117_T_Rex_20th_Century_Boy.mp3", "T. Rex", ["Slade", "Sweet", "David Bowie"], "20th Century Boy", 1973),
    _q("nemzetkozi_zenekarok/105_Jefferson_Airplane.mp3", "Jefferson Airplane", ["The Doors", "Grateful Dead", "Big Brother and the Holding Company"], "Somebody to Love", 1967),
    _q("nemzetkozi_zenekarok/Blue Swede - Hooked On A Feeling.mp3", "Blue Swede", ["Stealers Wheel", "Norman Greenbaum", "Redbone"], "Hooked on a Feeling", 1974),
    _q("nemzetkozi_zenekarok/70. The Rolling Stones - Paint It Black Official Lyric Video.mp3", "The Rolling Stones", ["The Kinks", "The Who", "The Animals"], "Paint It Black", 1966),
    _q("one_hit_wonders/66. RamJam - Black Betty.mp3", "Ram Jam", ["Steppenwolf", "Thin Lizzy", "Foghat"], "Black Betty", 1977),
    _q("one_hit_wonders/Wild Cherry - Play That Funky Music.mp3", "Wild Cherry", ["The Knack", "Average White Band", "KC and the Sunshine Band"], "Play That Funky Music", 1976),
    _q("one_hit_wonders/Journey - Dont Stop Believin.mp3", "Journey", ["Foreigner", "REO Speedwagon", "Boston"], "Don't Stop Believin'", 1981),
    _q("one_hit_wonders/The Proclaimers - 500 Miles.mp3", "The Proclaimers", ["The Waterboys", "Big Country", "Dexys Midnight Runners"], "I'm Gonna Be (500 Miles)", 1988),
    _q("rock_metal/06_Alice_Cooper.mp3", "Alice Cooper", ["Kiss", "Iggy Pop", "Ozzy Osbourne"], "School's Out", 1972),
    _q("rock_metal/07_Black_Sabbath.mp3", "Black Sabbath", ["Deep Purple", "Led Zeppelin", "Uriah Heep"], "Iron Man", 1970),
    _q("rock_metal/32_Twisted_Sister.mp3", "Twisted Sister", ["Kiss", "Quiet Riot", "Mötley Crüe"], "We're Not Gonna Take It", 1984),
    _q("nemzetkozi_zenekarok/69. The Beatles - For No One.mp3", "The Beatles", ["The Kinks", "The Zombies", "The Hollies"], "For No One", 1966),
    _q("nemzetkozi_zenekarok/112_Aphrodites_Child_End_of_the_World.mp3", "Aphrodite's Child", ["Procol Harum", "The Moody Blues", "King Crimson"], "End of the World", 1968),
    _q("nemzetkozi_zenekarok/68. Queen - 39.mp3", "Queen", ["Electric Light Orchestra", "10cc", "Supertramp"], "'39", 1975),
    _q("one_hit_wonders/Smokie - Living Next Door to Alice.mp3", "Smokie", ["Racey", "Mud", "The Rubettes"], "Living Next Door to Alice", 1976),
    _q("one_hit_wonders/Suzi Quatro - Stumblin In.mp3", "Suzi Quatro", ["Bonnie Tyler", "Pat Benatar", "Joan Jett"], "Stumblin' In", 1978),
    _q("rock_metal/09_Judas_Priest.mp3", "Judas Priest", ["Iron Maiden", "Saxon", "Motörhead"], "Breaking the Law", 1980),
    _q("rock_metal/10_Motorhead.mp3", "Motörhead", ["Saxon", "Judas Priest", "AC/DC"], "Ace of Spades", 1980),
    _q("rock_metal/13_Ozzy_Osbourne.mp3", "Ozzy Osbourne", ["Alice Cooper", "Rainbow", "Dio"], "Crazy Train", 1980),
    _q("rock_metal/08_Iron_Maiden.mp3", "Iron Maiden", ["Judas Priest", "Saxon", "Def Leppard"], "The Trooper", 1983),

    # --- Új felvételek: audio_files/rock_70s/ ---
    _q(_new(1, "ACDC_TNT"), "AC/DC", ["Rose Tattoo", "Thin Lizzy", "Aerosmith"], "T.N.T.", 1975),
    _q(_new(2, "ACDC_Highway_to_Hell"), "AC/DC", ["Aerosmith", "Kiss", "Cheap Trick"], "Highway to Hell", 1979),
    _q(_new(3, "Iggy_Pop_The_Passenger"), "Iggy Pop", ["Lou Reed", "David Bowie", "The Stooges"], "The Passenger", 1977),
    _q(_new(4, "CCR_Bad_Moon_Rising"), "Creedence Clearwater Revival", ["Lynyrd Skynyrd", "The Byrds", "Steppenwolf"], "Bad Moon Rising", 1969),
    _q(_new(5, "Pink_Floyd_Another_Brick_in_the_Wall"), "Pink Floyd", ["Supertramp", "Genesis", "Yes"], "Another Brick in the Wall, Part 2", 1979),
    _q(_new(6, "Pink_Floyd_Money"), "Pink Floyd", ["Jethro Tull", "King Crimson", "Electric Light Orchestra"], "Money", 1973),
    _q(_new(7, "Led_Zeppelin_Whole_Lotta_Love"), "Led Zeppelin", ["Deep Purple", "Cream", "Black Sabbath"], "Whole Lotta Love", 1969),
    _q(_new(8, "Led_Zeppelin_Stairway_to_Heaven"), "Led Zeppelin", ["Pink Floyd", "Jethro Tull", "Deep Purple"], "Stairway to Heaven", 1971),
    _q(_new(9, "Jethro_Tull_Aqualung"), "Jethro Tull", ["Procol Harum", "Uriah Heep", "Genesis"], "Aqualung", 1971),
    _q(_new(10, "Aerosmith_Dream_On"), "Aerosmith", ["Boston", "Kansas", "Journey"], "Dream On", 1973),
    _q(_new(11, "Aerosmith_Walk_This_Way"), "Aerosmith", ["The Rolling Stones", "Cheap Trick", "AC/DC"], "Walk This Way", 1975),
    _q(_new(12, "The_Who_Who_Are_You"), "The Who", ["The Kinks", "The Rolling Stones", "Thin Lizzy"], "Who Are You", 1978),
    _q(_new(13, "The_Who_Baba_ORiley"), "The Who", ["Led Zeppelin", "Pink Floyd", "The Kinks"], "Baba O'Riley", 1971),
    _q(_new(14, "Ramones_Blitzkrieg_Bop"), "Ramones", ["The Stooges", "Sex Pistols", "The Clash"], "Blitzkrieg Bop", 1976),
    _q(_new(15, "Kiss_Rock_and_Roll_All_Nite"), "Kiss", ["Alice Cooper", "Aerosmith", "Twisted Sister"], "Rock and Roll All Nite", 1975),
    _q(_new(16, "Kiss_I_Was_Made_for_Lovin_You"), "Kiss", ["Cheap Trick", "Foreigner", "Aerosmith"], "I Was Made for Lovin' You", 1979),
    _q(_new(17, "Foreigner_Cold_as_Ice"), "Foreigner", ["Journey", "Boston", "Styx"], "Cold as Ice", 1977),
    _q(_new(18, "Eagles_Hotel_California"), "Eagles", ["Fleetwood Mac", "The Doobie Brothers", "Kansas"], "Hotel California", 1977),
    _q(_new(19, "Eagles_Take_It_Easy"), "Eagles", ["Creedence Clearwater Revival", "Lynyrd Skynyrd", "The Allman Brothers Band"], "Take It Easy", 1972),
    _q(_new(20, "Stealers_Wheel_Stuck_in_the_Middle_with_You"), "Stealers Wheel", ["Steve Miller Band", "Badfinger", "Blue Swede"], "Stuck in the Middle with You", 1972),
    _q(_new(21, "ELO_Mr_Blue_Sky"), "Electric Light Orchestra", ["Supertramp", "10cc", "Wings"], "Mr. Blue Sky", 1977),
    _q(_new(22, "Norman_Greenbaum_Spirit_in_the_Sky"), "Norman Greenbaum", ["Steppenwolf", "Ram Jam", "Canned Heat"], "Spirit in the Sky", 1969),
    _q(_new(23, "Black_Sabbath_Paranoid"), "Black Sabbath", ["Deep Purple", "Led Zeppelin", "Blue Öyster Cult"], "Paranoid", 1970),
    _q(_new(24, "T_Rex_Get_It_On"), "T. Rex", ["Slade", "Sweet", "Mott the Hoople"], "Get It On", 1971),
    _q(_new(25, "Thin_Lizzy_The_Boys_Are_Back_in_Town"), "Thin Lizzy", ["Bob Seger", "Bad Company", "AC/DC"], "The Boys Are Back in Town", 1976),
    _q(_new(26, "The_Knack_My_Sharona"), "The Knack", ["Cheap Trick", "The Cars", "Blondie"], "My Sharona", 1979),
    _q(_new(27, "Supertramp_Give_a_Little_Bit"), "Supertramp", ["Electric Light Orchestra", "Kansas", "Wings"], "Give a Little Bit", 1977),
    _q(_new(28, "Steve_Miller_Band_The_Joker"), "Steve Miller Band", ["Eagles", "The Doobie Brothers", "Stealers Wheel"], "The Joker", 1973),
    _q(_new(29, "Steve_Miller_Band_Abracadabra"), "Steve Miller Band", ["The Knack", "Foreigner", "Chicago"], "Abracadabra", 1982),
    _q(_new(30, "The_Kinks_You_Really_Got_Me"), "The Kinks", ["The Who", "The Rolling Stones", "The Animals"], "You Really Got Me", 1964),
    _q(_new(31, "Lou_Reed_Walk_on_the_Wild_Side"), "Lou Reed", ["Iggy Pop", "David Bowie", "Bob Dylan"], "Walk on the Wild Side", 1972),
    _q(_new(32, "Chicago_Hard_to_Say_Im_Sorry"), "Chicago", ["Foreigner", "Journey", "Toto"], "Hard to Say I'm Sorry", 1982),
    _q(_new(33, "Chicago_25_or_6_to_4"), "Chicago", ["Blood, Sweat & Tears", "Steppenwolf", "Santana"], "25 or 6 to 4", 1970),
    _q(_new(34, "Neil_Young_Cinnamon_Girl"), "Neil Young", ["Bob Dylan", "Creedence Clearwater Revival", "Bob Seger"], "Cinnamon Girl", 1969),
    _q(_new(35, "Neil_Young_Down_by_the_River"), "Neil Young", ["Bob Dylan", "The Allman Brothers Band", "Lynyrd Skynyrd"], "Down by the River", 1969),
    _q(_new(36, "Peter_Frampton_Baby_I_Love_Your_Way"), "Peter Frampton", ["Supertramp", "Bob Seger", "Kansas"], "Baby, I Love Your Way", 1975),
    _q(_new(37, "Kansas_Dust_in_the_Wind"), "Kansas", ["Boston", "Supertramp", "Eagles"], "Dust in the Wind", 1977),
    _q(_new(38, "Steppenwolf_Born_to_Be_Wild"), "Steppenwolf", ["Creedence Clearwater Revival", "Deep Purple", "The Doors"], "Born to Be Wild", 1968),
    _q(_new(39, "Jimi_Hendrix_Purple_Haze"), "Jimi Hendrix", ["Cream", "Stevie Ray Vaughan", "Santana"], "Purple Haze", 1967),
    _q(_new(40, "Jimi_Hendrix_All_Along_the_Watchtower"), "Jimi Hendrix", ["Cream", "The Doors", "Steppenwolf"], "All Along the Watchtower", 1968),
    _q(_new(41, "Procol_Harum_A_Whiter_Shade_of_Pale"), "Procol Harum", ["The Moody Blues", "The Doors", "Jethro Tull"], "A Whiter Shade of Pale", 1967),
    _q(_new(42, "Cream_Sunshine_of_Your_Love"), "Cream", ["Jimi Hendrix", "Led Zeppelin", "Steppenwolf"], "Sunshine of Your Love", 1967),
    _q(_new(43, "Fleetwood_Mac_Go_Your_Own_Way"), "Fleetwood Mac", ["Eagles", "Heart", "Supertramp"], "Go Your Own Way", 1977),
    _q(_new(44, "Fleetwood_Mac_Dreams"), "Fleetwood Mac", ["Joni Mitchell", "Eagles", "Heart"], "Dreams", 1977),
    _q(_new(45, "The_Doors_Light_My_Fire"), "The Doors", ["Jefferson Airplane", "Procol Harum", "The Animals"], "Light My Fire", 1967),
    _q(_new(46, "The_Doors_Riders_on_the_Storm"), "The Doors", ["Pink Floyd", "Procol Harum", "Jefferson Airplane"], "Riders on the Storm", 1971),
    _q(_new(47, "Bob_Dylan_Like_a_Rolling_Stone"), "Bob Dylan", ["Neil Young", "Lou Reed", "Bruce Springsteen"], "Like a Rolling Stone", 1965),
    _q(_new(48, "Bob_Dylan_Knockin_on_Heavens_Door"), "Bob Dylan", ["Neil Young", "Bob Seger", "Lou Reed"], "Knockin' on Heaven's Door", 1973),
    _q(_new(49, "ZZ_Top_La_Grange"), "ZZ Top", ["Lynyrd Skynyrd", "Stevie Ray Vaughan", "Canned Heat"], "La Grange", 1973),
    _q(_new(50, "Rolling_Stones_Brown_Sugar"), "The Rolling Stones", ["Faces", "Aerosmith", "The Who"], "Brown Sugar", 1971),
    _q(_new(51, "Cheap_Trick_I_Want_You_to_Want_Me"), "Cheap Trick", ["The Knack", "Kiss", "Thin Lizzy"], "I Want You to Want Me", 1978),
    _q(_new(52, "Stevie_Ray_Vaughan_Pride_and_Joy"), "Stevie Ray Vaughan", ["ZZ Top", "Jimi Hendrix", "Eric Clapton"], "Pride and Joy", 1983),
    _q(_new(53, "The_Police_Roxanne"), "The Police", ["The Clash", "Dire Straits", "The Cars"], "Roxanne", 1978),
    _q(_new(54, "The_Police_Message_in_a_Bottle"), "The Police", ["Dire Straits", "The Knack", "The Cars"], "Message in a Bottle", 1979),
    _q(_new(55, "Bob_Seger_Old_Time_Rock_and_Roll"), "Bob Seger", ["Bruce Springsteen", "Thin Lizzy", "Tom Petty"], "Old Time Rock and Roll", 1978),
    _q(_new(56, "Joni_Mitchell_Big_Yellow_Taxi"), "Joni Mitchell", ["Carole King", "Joan Baez", "Fleetwood Mac"], "Big Yellow Taxi", 1970),
    _q(_new(57, "Jet_Are_You_Gonna_Be_My_Girl"), "Jet", ["The Vines", "The Hives", "Wolfmother"], "Are You Gonna Be My Girl", 2003),
    _q(_new(58, "John_Denver_Take_Me_Home_Country_Roads"), "John Denver", ["Glen Campbell", "James Taylor", "Kenny Rogers"], "Take Me Home, Country Roads", 1971),
]

# Csak a lejátszható kérdések (meglévő mp3) kerülnek a kvízbe.
ROCK_70S_QUESTIONS = [q for q in _ALL if (_AUDIO_ROOT / q["audio_file"]).is_file()]
QUESTIONS = ROCK_70S_QUESTIONS


def missing_audio():
    return [q for q in _ALL if not (_AUDIO_ROOT / q["audio_file"]).is_file()]


if __name__ == "__main__":
    miss = missing_audio()
    print(f"Összesen {len(_ALL)} kérdés, lejátszható {len(ROCK_70S_QUESTIONS)}, hiányzó mp3: {len(miss)}\n")
    for q in miss:
        print(f"audio_files/{q['audio_file']}   ←  {q['explanation']}")
