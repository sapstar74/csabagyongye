# DJ / Producer kérdések

_DEFAULT_QUESTION = "Ki az előadó / DJ?"
_TOPIC = "dj_producer"


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
    _q("01_David_Guetta.mp3",        0, ["David Guetta", "Martin Garrix", "Tiësto", "Calvin Harris"],              "David Guetta – Titanium ft. Sia",                    song_title="Titanium"),
    _q("02_Martin_Garrix.mp3",        0, ["Martin Garrix", "Hardwell", "Afrojack", "W&W"],                         "Martin Garrix – Animals",                            song_title="Animals"),
    _q("03_Armin_van_Buuren.mp3",     0, ["Armin van Buuren", "Above & Beyond", "Paul van Dyk", "Tiësto"],         "Armin van Buuren – Blah Blah Blah",                  song_title="Blah Blah Blah"),
    _q("04_Tiesto.mp3",               0, ["Tiësto", "David Guetta", "Skrillex", "Diplo"],                          "Tiësto – Red Lights",                                song_title="Red Lights"),
    _q("05_Calvin_Harris.mp3",        0, ["Calvin Harris", "The Chainsmokers", "Marshmello", "David Guetta"],      "Calvin Harris – Summer",                             song_title="Summer"),
    _q("06_Skrillex.mp3",             0, ["Skrillex", "Deadmau5", "Diplo", "Steve Aoki"],                          "Skrillex – Bangarang",                               song_title="Bangarang"),
    _q("07_Charlotte_de_Witte.mp3",   0, ["Charlotte de Witte", "Amelie Lens", "Miss Monique", "Adam Beyer"],      "Charlotte de Witte – Doppler",                       song_title="Doppler"),
    _q("08_Dimitri_Vegas.mp3",        0, ["Dimitri Vegas & Like Mike", "W&W", "Hardwell", "Afrojack"],             "Dimitri Vegas & Like Mike – Tremor ft. Martin Garrix", song_title="Tremor"),
    _q("09_Alok.mp3",                 0, ["Alok", "Vintage Culture", "Dom Dolla", "Fred again"],                   "Alok – Never Let Me Go",                             song_title="Never Let Me Go"),
    _q("10_Peggy_Gou.mp3",            0, ["Peggy Gou", "Keinemusik", "Black Coffee", "Solomun"],                   "Peggy Gou – (It Goes Like) Nanana",                  song_title="Nanana"),
    _q("11_Anyma.mp3",                0, ["Anyma", "Tale of Us", "Solomun", "Fred again"],                         "Anyma – Explore Your Future",                        song_title="Explore Your Future"),
    _q("12_Vintage_Culture.mp3",      0, ["Vintage Culture", "Alok", "Dom Dolla", "James Hype"],                   "Vintage Culture – Spaceman",                         song_title="Spaceman"),
    _q("13_Hardwell.mp3",             0, ["Hardwell", "W&W", "Afrojack", "Dimitri Vegas & Like Mike"],             "Hardwell – Dare You",                                song_title="Dare You"),
    _q("14_Swedish_House_Mafia.mp3",  0, ["Swedish House Mafia", "The Chainsmokers", "Avicii", "Calvin Harris"],   "Swedish House Mafia – Don't You Worry Child",        song_title="Don't You Worry Child"),
    _q("15_Fred_again.mp3",           0, ["Fred again", "Anyma", "James Hype", "Dom Dolla"],                       "Fred again.. – Delilah (Pull Me Out of This)",       song_title="Delilah"),
    _q("16_Dom_Dolla.mp3",            0, ["Dom Dolla", "Vintage Culture", "James Hype", "Gordo"],                  "Dom Dolla – Eat Your Man",                           song_title="Eat Your Man"),
    _q("17_Black_Coffee.mp3",         0, ["Black Coffee", "Solomun", "Carl Cox", "Richie Hawtin"],                 "Black Coffee – We Dance Again",                      song_title="We Dance Again"),
    _q("18_Carl_Cox.mp3",             0, ["Carl Cox", "Richie Hawtin", "Solomun", "Black Coffee"],                 "Carl Cox – I Want You (Forever)",                    song_title="I Want You"),
    _q("19_John_Summit.mp3",          0, ["John Summit", "Dom Dolla", "James Hype", "Michael Bibi"],               "John Summit – La Danza",                             song_title="La Danza"),
    _q("20_Diplo.mp3",                0, ["Diplo", "Skrillex", "Steve Aoki", "David Guetta"],                      "Diplo – Revolution ft. Faustix & Imanos",            song_title="Revolution"),
    _q("21_Avicii.mp3",               0, ["Avicii", "Swedish House Mafia", "Calvin Harris", "Martin Garrix"],      "Avicii – Wake Me Up",                                song_title="Wake Me Up"),
    _q("22_Keinemusik.mp3",           0, ["Keinemusik", "Peggy Gou", "Black Coffee", "Solomun"],                   "Keinemusik – Momma's Boy",                           song_title="Momma's Boy"),
    _q("23_DJ_Snake.mp3",             0, ["DJ Snake", "Diplo", "Skrillex", "Steve Aoki"],                          "DJ Snake – Turn Down for What",                      song_title="Turn Down for What"),
    _q("24_Deadmau5.mp3",             0, ["Deadmau5", "Skrillex", "Eric Prydz", "Richie Hawtin"],                  "Deadmau5 – Strobe",                                  song_title="Strobe"),
    _q("25_Marshmello.mp3",           0, ["Marshmello", "The Chainsmokers", "Alan Walker", "Avicii"],              "Marshmello – Alone",                                 song_title="Alone"),
    _q("26_The_Chainsmokers.mp3",     0, ["The Chainsmokers", "Marshmello", "Calvin Harris", "Swedish House Mafia"], "The Chainsmokers – Closer ft. Halsey",             song_title="Closer"),
    _q("27_Eric_Prydz.mp3",           0, ["Eric Prydz", "Deadmau5", "Richie Hawtin", "Adam Beyer"],                "Eric Prydz – Pjanoo",                                song_title="Pjanoo"),
    _q("28_Amelie_Lens.mp3",          0, ["Amelie Lens", "Charlotte de Witte", "Miss Monique", "Adam Beyer"],      "Amelie Lens – Exhale",                               song_title="Exhale"),
    _q("29_Adam_Beyer.mp3",           0, ["Adam Beyer", "Richie Hawtin", "Carl Cox", "Amelie Lens"],               "Adam Beyer – Your Mind Is a Box",                    song_title="Your Mind Is a Box"),
    _q("30_Afrojack.mp3",             0, ["Afrojack", "Hardwell", "W&W", "Martin Garrix"],                         "Afrojack – Take Over Control",                       song_title="Take Over Control"),
    _q("31_Don_Diablo.mp3",           0, ["Don Diablo", "Oliver Heldens", "Lost Frequencies", "Alan Walker"],      "Don Diablo – Tonight",                               song_title="Tonight"),
    _q("32_Steve_Aoki.mp3",           0, ["Steve Aoki", "Diplo", "Skrillex", "DJ Snake"],                          "Steve Aoki – Turbulence ft. Weezer",                 song_title="Turbulence"),
    _q("33_CamelPhat.mp3",            0, ["CamelPhat", "Dom Dolla", "Michael Bibi", "James Hype"],                 "CamelPhat – Cola",                                   song_title="Cola"),
    _q("34_Alan_Walker.mp3",          0, ["Alan Walker", "Marshmello", "Lost Frequencies", "Avicii"],              "Alan Walker – Faded",                                song_title="Faded"),
    _q("35_Oliver_Heldens.mp3",       0, ["Oliver Heldens", "Don Diablo", "Lost Frequencies", "James Hype"],       "Oliver Heldens – Gecko (Overdrive)",                 song_title="Gecko"),
    _q("36_Richie_Hawtin.mp3",        0, ["Richie Hawtin", "Carl Cox", "Adam Beyer", "Deadmau5"],                  "Richie Hawtin – Close Combined",                     song_title="Close Combined"),
    _q("37_Above_and_Beyond.mp3",     0, ["Above & Beyond", "Armin van Buuren", "Paul van Dyk", "Kaskade"],        "Above & Beyond – Sun & Moon",                        song_title="Sun and Moon"),
    _q("38_Miss_Monique.mp3",         0, ["Miss Monique", "Charlotte de Witte", "Amelie Lens", "Tale of Us"],      "Miss Monique – Mind Travel",                         song_title="Mind Travel"),
    _q("39_Tale_of_Us.mp3",           0, ["Tale of Us", "Anyma", "Solomun", "Black Coffee"],                       "Tale of Us – Astral",                                song_title="Astral"),
    _q("40_Solomun.mp3",              0, ["Solomun", "Black Coffee", "Carl Cox", "Tale of Us"],                    "Solomun – Nobody Is Not Loved",                      song_title="Nobody Is Not Loved"),
    _q("41_Kaskade.mp3",              0, ["Kaskade", "Above & Beyond", "Paul van Dyk", "Armin van Buuren"],        "Kaskade – I Remember",                               song_title="I Remember"),
    _q("42_Lost_Frequencies.mp3",     0, ["Lost Frequencies", "Don Diablo", "Oliver Heldens", "Alan Walker"],      "Lost Frequencies – Are You With Me",                 song_title="Are You With Me"),
    _q("43_W&W.mp3",                  0, ["W&W", "Hardwell", "Afrojack", "Dimitri Vegas & Like Mike"],             "W&W – Bigfoot",                                      song_title="Bigfoot"),
    _q("44_Michael_Bibi.mp3",         0, ["Michael Bibi", "James Hype", "Dom Dolla", "CamelPhat"],                 "Michael Bibi – Clap Your Hands",                     song_title="Clap Your Hands"),
    _q("45_James_Hype.mp3",           0, ["James Hype", "Dom Dolla", "Michael Bibi", "Fred again"],                "James Hype – Ferrari",                               song_title="Ferrari"),
    _q("46_Boris_Brejcha.mp3",        0, ["Boris Brejcha", "Reinier Zonneveld", "Richie Hawtin", "Deadmau5"],      "Boris Brejcha – Purple Noise",                       song_title="Purple Noise"),
    _q("47_Reinier_Zonneveld.mp3",    0, ["Reinier Zonneveld", "Boris Brejcha", "Richie Hawtin", "Adam Beyer"],    "Reinier Zonneveld – How Long",                       song_title="How Long"),
    _q("48_Gordo.mp3",                0, ["Gordo", "Dom Dolla", "James Hype", "Michael Bibi"],                     "Gordo – Buff Riff",                                  song_title="Buff Riff"),
    _q("49_Paul_van_Dyk.mp3",         0, ["Paul van Dyk", "Armin van Buuren", "Above & Beyond", "Kaskade"],        "Paul van Dyk – For an Angel",                        song_title="For an Angel"),
]

DJ_PRODUCER_QUESTIONS = QUESTIONS
