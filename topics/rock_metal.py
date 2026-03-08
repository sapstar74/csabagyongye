# Rock és Metal kérdések

_DEFAULT_QUESTION = "Ki az előadó?"
_TOPIC = "rock_metal"


def _q(audio_file, correct, options, explanation, question=_DEFAULT_QUESTION, **extra):
    return {
        "question": question,
        "options": options,
        "correct": correct,
        "explanation": explanation,
        "audio_file": audio_file,
        "topic": _TOPIC,
        **extra,
    }


QUESTIONS = [
    _q("01_Slipknot.mp3",        0, ["Slipknot", "Korn", "Disturbed", "Pantera"],           "Slipknot – Duality",                       song_title="Duality"),
    _q("02_Pantera.mp3",         0, ["Pantera", "Slayer", "Megadeth", "Sepultura"],          "Pantera – Walk",                           song_title="Walk"),
    _q("03_Megadeth.mp3",        0, ["Megadeth", "Metallica", "Slayer", "Anthrax"],          "Megadeth – Symphony of Destruction",       song_title="Symphony of Destruction"),
    _q("04_Disturbed.mp3",       0, ["Disturbed", "Slipknot", "Korn", "Machine Head"],       "Disturbed – Down with the Sickness",       song_title="Down with the Sickness"),
    _q("05_Metallica.mp3",       0, ["Metallica", "Megadeth", "Black Sabbath", "Iron Maiden"], "Metallica – Enter Sandman",              song_title="Enter Sandman"),
    _q("06_Alice_Cooper.mp3",    0, ["Alice Cooper", "Ozzy Osbourne", "W.A.S.P.", "Twisted Sister"], "Alice Cooper – School's Out",        song_title="School's Out"),
    _q("07_Black_Sabbath.mp3",   0, ["Black Sabbath", "Iron Maiden", "Judas Priest", "Metallica"], "Black Sabbath – Iron Man",            song_title="Iron Man"),
    _q("08_Iron_Maiden.mp3",     0, ["Iron Maiden", "Black Sabbath", "Judas Priest", "Helloween"], "Iron Maiden – The Trooper",           song_title="The Trooper"),
    _q("09_Judas_Priest.mp3",    0, ["Judas Priest", "Iron Maiden", "Black Sabbath", "Motörhead"], "Judas Priest – Breaking the Law",     song_title="Breaking the Law"),
    _q("10_Motorhead.mp3",       0, ["Motörhead", "Venom", "Judas Priest", "Slayer"],        "Motörhead – Ace of Spades",               song_title="Ace of Spades"),
    _q("11_Slayer.mp3",          0, ["Slayer", "Megadeth", "Pantera", "Venom"],              "Slayer – Raining Blood",                   song_title="Raining Blood"),
    _q("12_Venom.mp3",           0, ["Venom", "Mayhem", "Slayer", "Motörhead"],              "Venom – Black Metal",                      song_title="Black Metal"),
    _q("13_Ozzy_Osbourne.mp3",   0, ["Ozzy Osbourne", "Alice Cooper", "Black Sabbath", "W.A.S.P."], "Ozzy Osbourne – Crazy Train",       song_title="Crazy Train"),
    _q("14_Queensryche.mp3",     0, ["Queensrÿche", "Dream Theater", "Helloween", "Iron Maiden"], "Queensrÿche – Silent Lucidity",       song_title="Silent Lucidity"),
    _q("15_Dream_Theater.mp3",   0, ["Dream Theater", "Queensrÿche", "Tool", "Mastodon"],    "Dream Theater – Pull Me Under",            song_title="Pull Me Under"),
    _q("16_Manowar.mp3",         0, ["Manowar", "Helloween", "Iron Maiden", "Judas Priest"], "Manowar – Warriors of the World United",  song_title="Warriors of the World"),
    _q("17_Helloween.mp3",       0, ["Helloween", "Iron Maiden", "Manowar", "Queensrÿche"],  "Helloween – I Want Out",                  song_title="I Want Out"),
    _q("18_Anthrax.mp3",         0, ["Anthrax", "Megadeth", "Slayer", "Overkill"],           "Anthrax – I Am the Law",                  song_title="I Am the Law"),
    _q("19_Alice_in_Chains.mp3", 0, ["Alice in Chains", "Soundgarden", "Korn", "Faith No More"], "Alice in Chains – Would?",           song_title="Would?"),
    _q("20_Sepultura.mp3",       0, ["Sepultura", "Machine Head", "Pantera", "Slayer"],      "Sepultura – Roots Bloody Roots",          song_title="Roots Bloody Roots"),
    _q("21_Motley_Crue.mp3",     0, ["Mötley Crüe", "Scorpions", "Twisted Sister", "Skid Row"], "Mötley Crüe – Girls, Girls, Girls",   song_title="Girls, Girls, Girls"),
    _q("22_Scorpions.mp3",       0, ["Scorpions", "Mötley Crüe", "Judas Priest", "Skid Row"], "Scorpions – Rock You Like a Hurricane", song_title="Rock You Like a Hurricane"),
    _q("23_Tool.mp3",            0, ["Tool", "Korn", "Mastodon", "Alice in Chains"],         "Tool – Sober",                            song_title="Sober"),
    _q("24_Mayhem.mp3",          0, ["Mayhem", "Venom", "Cannibal Corpse", "Slayer"],        "Mayhem – Freezing Moon",                  song_title="Freezing Moon"),
    _q("25_Korn.mp3",            0, ["Korn", "Slipknot", "Disturbed", "Tool"],               "Korn – Freak on a Leash",                 song_title="Freak on a Leash"),
    _q("26_Cannibal_Corpse.mp3", 0, ["Cannibal Corpse", "Mayhem", "Slayer", "Venom"],        "Cannibal Corpse – Hammer Smashed Face",   song_title="Hammer Smashed Face"),
    _q("27_Faith_No_More.mp3",   0, ["Faith No More", "Alice in Chains", "Korn", "Pantera"], "Faith No More – Epic",                   song_title="Epic"),
    _q("28_Overkill.mp3",        0, ["Overkill", "Anthrax", "Megadeth", "Machine Head"],     "Overkill – Elimination",                  song_title="Elimination"),
    _q("29_Machine_Head.mp3",    0, ["Machine Head", "Sepultura", "Pantera", "Overkill"],    "Machine Head – Davidian",                 song_title="Davidian"),
    _q("30_Type_O_Negative.mp3", 0, ["Type O Negative", "Mayhem", "Black Sabbath", "Venom"], "Type O Negative – Black No. 1",          song_title="Black No. 1"),
    _q("31_WASP.mp3",            0, ["W.A.S.P.", "Alice Cooper", "Twisted Sister", "Mötley Crüe"], "W.A.S.P. – I Wanna Be Somebody",    song_title="I Wanna Be Somebody"),
    _q("32_Twisted_Sister.mp3",  0, ["Twisted Sister", "W.A.S.P.", "Mötley Crüe", "Skid Row"], "Twisted Sister – We're Not Gonna Take It", song_title="We're Not Gonna Take It"),
    _q("33_Mastodon.mp3",        0, ["Mastodon", "Tool", "Machine Head", "Alice in Chains"], "Mastodon – Blood and Thunder",            song_title="Blood and Thunder"),
    _q("34_Skid_Row.mp3",        0, ["Skid Row", "Mötley Crüe", "Twisted Sister", "Scorpions"], "Skid Row – 18 and Life",             song_title="18 and Life"),
]

ROCK_METAL_QUESTIONS = QUESTIONS
