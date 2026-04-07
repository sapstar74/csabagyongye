# Hip-hop / Rap kérdések

_DEFAULT_QUESTION = "Ki az előadó?"
_TOPIC = "hip_hop"


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
    _q("01_Run_DMC.mp3",              0, ["Run-D.M.C.", "Beastie Boys", "LL Cool J", "Public Enemy"],         "Run-D.M.C. – Walk This Way",                          song_title="Walk This Way"),
    _q("02_2Pac.mp3",                 0, ["2Pac", "The Notorious B.I.G.", "Snoop Dogg", "Ice Cube"],          "2Pac – California Love",                               song_title="California Love"),
    _q("03_Public_Enemy.mp3",         0, ["Public Enemy", "N.W.A", "Run-D.M.C.", "Ice Cube"],                 "Public Enemy – Fight the Power",                       song_title="Fight the Power"),
    _q("04_Jay_Z.mp3",                0, ["Jay-Z", "Kanye West", "Drake", "50 Cent"],                         "Jay-Z – 99 Problems",                                  song_title="99 Problems"),
    _q("05_NWA.mp3",                  0, ["N.W.A", "Public Enemy", "Ice Cube", "Cypress Hill"],               "N.W.A – Straight Outta Compton",                       song_title="Straight Outta Compton"),
    _q("06_Grandmaster_Flash.mp3",    0, ["Grandmaster Flash & the Furious Five", "The Sugarhill Gang", "Kurtis Blow", "Afrika Bambaataa"], "Grandmaster Flash – The Message", song_title="The Message"),
    _q("07_Notorious_BIG.mp3",        0, ["The Notorious B.I.G.", "2Pac", "Jay-Z", "Snoop Dogg"],             "The Notorious B.I.G. – Hypnotize",                     song_title="Hypnotize"),
    _q("08_LL_Cool_J.mp3",            0, ["LL Cool J", "Run-D.M.C.", "Beastie Boys", "Ice Cube"],             "LL Cool J – Mama Said Knock You Out",                  song_title="Mama Said Knock You Out"),
    _q("09_De_La_Soul.mp3",           0, ["De La Soul", "The Fugees", "OutKast", "Arrested Development"],     "De La Soul – Ring Ring Ring",                           song_title="Ring Ring Ring"),
    _q("10_OutKast.mp3",              0, ["OutKast", "De La Soul", "Kanye West", "Jay-Z"],                    "OutKast – Hey Ya!",                                     song_title="Hey Ya!"),
    _q("11_Eminem.mp3",               0, ["Eminem", "Jay-Z", "Dr. Dre", "50 Cent"],                           "Eminem – Lose Yourself",                               song_title="Lose Yourself"),
    _q("12_Beastie_Boys.mp3",         0, ["Beastie Boys", "Run-D.M.C.", "LL Cool J", "Public Enemy"],         "Beastie Boys – (You Gotta) Fight for Your Right",      song_title="Fight for Your Right"),
    _q("13_Afrika_Bambaataa.mp3",     0, ["Afrika Bambaataa", "Grandmaster Flash", "Kurtis Blow", "The Sugarhill Gang"], "Afrika Bambaataa – Planet Rock",            song_title="Planet Rock"),
    _q("14_Dr_Dre.mp3",               0, ["Dr. Dre", "Snoop Dogg", "Ice Cube", "Eminem"],                     "Dr. Dre – Still D.R.E.",                               song_title="Still D.R.E."),
    _q("15_Kanye_West.mp3",           0, ["Kanye West", "Jay-Z", "Drake", "Eminem"],                          "Kanye West – Gold Digger",                             song_title="Gold Digger"),
    _q("16_Wu_Tang_Clan.mp3",         0, ["Wu-Tang Clan", "N.W.A", "Cypress Hill", "Public Enemy"],           "Wu-Tang Clan – C.R.E.A.M.",                            song_title="C.R.E.A.M."),
    _q("17_Ice_Cube.mp3",             0, ["Ice Cube", "N.W.A", "Snoop Dogg", "2Pac"],                         "Ice Cube – It Was a Good Day",                         song_title="It Was a Good Day"),
    _q("18_Snoop_Dogg.mp3",           0, ["Snoop Dogg", "Dr. Dre", "Ice Cube", "2Pac"],                       "Snoop Dogg – Gin and Juice",                           song_title="Gin and Juice"),
    _q("19_Kurtis_Blow.mp3",          0, ["Kurtis Blow", "The Sugarhill Gang", "Grandmaster Flash", "Afrika Bambaataa"], "Kurtis Blow – The Breaks",                  song_title="The Breaks"),
    _q("20_Lauryn_Hill.mp3",          0, ["Lauryn Hill", "Missy Elliott", "Salt-N-Pepa", "Eve"],              "Lauryn Hill – Doo Wop (That Thing)",                   song_title="Doo Wop (That Thing)"),
    _q("21_Missy_Elliott.mp3",        0, ["Missy Elliott", "Lauryn Hill", "Nicki Minaj", "Cardi B"],          "Missy Elliott – Work It",                              song_title="Work It"),
    _q("22_Salt_N_Pepa.mp3",          0, ["Salt-N-Pepa", "Missy Elliott", "Lauryn Hill", "Eve"],              "Salt-N-Pepa – Push It",                                song_title="Push It"),
    _q("23_Cardi_B.mp3",              0, ["Cardi B", "Nicki Minaj", "Missy Elliott", "Eve"],                  "Cardi B – Bodak Yellow",                               song_title="Bodak Yellow"),
    _q("24_Nicki_Minaj.mp3",          0, ["Nicki Minaj", "Cardi B", "Missy Elliott", "Lauryn Hill"],          "Nicki Minaj – Super Bass",                             song_title="Super Bass"),
    _q("25_Busta_Rhymes.mp3",         0, ["Busta Rhymes", "The Fugees", "Wu-Tang Clan", "Cypress Hill"],      "Busta Rhymes – Put Your Hands Where My Eyes Could See", song_title="Put Your Hands…"),
    _q("26_The_Fugees.mp3",           0, ["The Fugees", "De La Soul", "Arrested Development", "Lauryn Hill"], "The Fugees – Killing Me Softly",                       song_title="Killing Me Softly"),
    _q("27_Sugarhill_Gang.mp3",       0, ["The Sugarhill Gang", "Grandmaster Flash", "Kurtis Blow", "Afrika Bambaataa"], "The Sugarhill Gang – Rapper's Delight",      song_title="Rapper's Delight"),
    _q("28_Cypress_Hill.mp3",         0, ["Cypress Hill", "N.W.A", "Wu-Tang Clan", "Ice Cube"],               "Cypress Hill – Insane in the Brain",                   song_title="Insane in the Brain"),
    _q("29_Naughty_By_Nature.mp3",    0, ["Naughty By Nature", "The Sugarhill Gang", "De La Soul", "Busta Rhymes"], "Naughty By Nature – Hip Hop Hooray",             song_title="Hip Hop Hooray"),
    _q("30_50_Cent.mp3",              0, ["50 Cent", "Eminem", "Jay-Z", "Dr. Dre"],                           "50 Cent – In Da Club",                                 song_title="In Da Club"),
    _q("31_Drake.mp3",                0, ["Drake", "Kanye West", "Jay-Z", "50 Cent"],                         "Drake – Hotline Bling",                                song_title="Hotline Bling"),
    _q("32_DJ_Jazzy_Jeff.mp3",        0, ["DJ Jazzy Jeff & the Fresh Prince", "Run-D.M.C.", "Beastie Boys", "Naughty By Nature"], "DJ Jazzy Jeff & the Fresh Prince – Summertime", song_title="Summertime"),
    _q("33_Arrested_Development.mp3", 0, ["Arrested Development", "De La Soul", "The Fugees", "OutKast"],     "Arrested Development – Tennessee",                     song_title="Tennessee"),
    _q("34_Kool_Keith.mp3",           0, ["Kool Keith", "Afrika Bambaataa", "Grandmaster Flash", "Kurtis Blow"], "Kool Keith (Ultramagnetic MCs) – Ego Trippin'",      song_title="Ego Trippin'"),
    _q("35_Eve.mp3",                  0, ["Eve", "Missy Elliott", "Lauryn Hill", "Salt-N-Pepa"],              "Eve – Let Me Blow Ya Mind",                            song_title="Let Me Blow Ya Mind"),
    _q("36_Bad_Bunny.mp3",            0, ["Bad Bunny", "J Balvin", "Ozuna", "Maluma"],                        "Bad Bunny – Dakiti (ft. Jhay Cortez)",                   song_title="Dakiti"),
]

HIP_HOP_QUESTIONS = QUESTIONS
