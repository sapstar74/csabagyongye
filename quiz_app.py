"""
🧠 PDF Alapú Quiz Alkalmazás
10 kérdéses feleletválasztós teszt a feltöltött PDF tartalom alapján
"""

import streamlit as st
import random
import time
from datetime import datetime
import os
from pathlib import Path
from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS
from topics.haboru import HABORU_QUESTIONS

# Page config
st.set_page_config(
    page_title="🧠 PDF Quiz Alkalmazás",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Quiz adatok témakörök szerint csoportosítva
QUIZ_DATA_BY_TOPIC = {
    "földrajz": [
        {
            "question": "Mi a legmagasabb csúcs a Mátrában?",
            "options": ["Kékes", "Dobogó-kő", "Csóványos", "Szilvási-kő"],
            "correct": 0,
            "explanation": "A Kékes 1014 méter magasságával a Mátra legmagasabb csúcsa."
        },
        {
            "question": "Melyik ország fővárosa Taskent?",
            "options": ["Kazahsztán", "Üzbegisztán", "Kirgizisztán", "Tádzsikisztán"],
            "correct": 1,
            "explanation": "Taskent Üzbegisztán fővárosa."
        },
        {
            "question": "Melyik a világ leghosszabb folyója?",
            "options": ["Amazonas", "Nílus", "Jangce", "Mississippi"],
            "correct": 1,
            "explanation": "A Nílus 6650 km hosszával a világ leghosszabb folyója."
        },
        {
            "question": "Mi Bhután fővárosa?",
            "options": ["Thimphu", "Katmandu", "Dhaka", "Vientiane"],
            "correct": 0,
            "explanation": "Bhután fővárosa Thimphu, pénzneme a ngultrum."
        },
        {
            "question": "Melyik hegység csúcsa a Börzsöny legmagasabb pontja?",
            "options": ["Nagy-Kopasz", "Pilis", "Dobogó-kő", "Csóványos"],
            "correct": 3,
            "explanation": "A Csóványos (938 m) a Börzsöny hegység legmagasabb csúcsa."
        },
        {
            "question": "Melyik kontinensen található a Kilimandzsáró?",
            "options": ["Ázsia", "Dél-Amerika", "Afrika", "Ausztrália"],
            "correct": 2,
            "explanation": "A Kilimandzsáró (5895 m) Afrika legmagasabb hegycsúcsa."
        },
        {
            "question": "Mi Costa Rica pénzneme?",
            "options": ["Peso", "Dollár", "Quetzal", "Colón"],
            "correct": 3,
            "explanation": "Costa Rica pénzneme a Costa Rica-i colón."
        },
        {
            "question": "Melyik az Európa leghosszabb folyója?",
            "options": ["Volga", "Duna", "Rajna", "Dnyeper"],
            "correct": 0,
            "explanation": "A Volga 3530 km hosszával Európa leghosszabb folyója."
        },
        {
            "question": "Mi a Pilis hegység legmagasabb csúcsa?",
            "options": ["Nagy-Kopasz", "Dobogó-kő", "Szánkó-hegy", "Pilis"],
            "correct": 3,
            "explanation": "A Pilis (757 m) a Pilis hegység névadó és legmagasabb csúcsa."
        },
        {
            "question": "Melyik ország pénzneme a manat?",
            "options": ["Grúzia", "Örményország", "Azerbajdzsán", "Kazahsztán"],
            "correct": 2,
            "explanation": "Azerbajdzsán pénzneme a manat, fővárosa Baku."
        },
        {
            "question": "Mi Üzbegisztán fővárosa?",
            "options": ["Taskent", "Biskek", "Dusanbe", "Tbiliszi"],
            "correct": 0,
            "explanation": "Üzbegisztán fővárosa Taskent, pénzneme a som."
        },
        {
            "question": "Mi Kirgizisztán fővárosa?",
            "options": ["Taskent", "Biskek", "Asztana", "Jereván"],
            "correct": 1,
            "explanation": "Kirgizisztán fővárosa Biskek, pénzneme a som."
        },
        {
            "question": "Mi Tádzsikisztán fővárosa?",
            "options": ["Biskek", "Dusanbe", "Taskent", "Baku"],
            "correct": 1,
            "explanation": "Tádzsikisztán fővárosa Dusanbe, pénzneme a somoni."
        },
        {
            "question": "Mi Grúzia fővárosa?",
            "options": ["Baku", "Jereván", "Tbiliszi", "Asztana"],
            "correct": 2,
            "explanation": "Grúzia fővárosa Tbiliszi, pénzneme a lari."
        },
        {
            "question": "Mi Örményország fővárosa?",
            "options": ["Tbiliszi", "Jereván", "Baku", "Biskek"],
            "correct": 1,
            "explanation": "Örményország fővárosa Jereván, pénzneme a dram."
        },
        {
            "question": "Mi Kazahsztán fővárosa?",
            "options": ["Almati", "Asztana", "Taskent", "Biskek"],
            "correct": 1,
            "explanation": "Kazahsztán fővárosa Asztana (ma Nur-Sultan), pénzneme a tenge."
        },
        {
            "question": "Mi Laosz fővárosa?",
            "options": ["Vientiane", "Phnom Penh", "Bangkok", "Hanoi"],
            "correct": 0,
            "explanation": "Laosz fővárosa Vientiane, pénzneme a kip."
        },
        {
            "question": "Mi Brunei fővárosa?",
            "options": ["Bandar Seri Begawan", "Kuala Lumpur", "Jakarta", "Manila"],
            "correct": 0,
            "explanation": "Brunei fővárosa Bandar Seri Begawan, pénzneme a dollár."
        },
        {
            "question": "Mi Costa Rica fővárosa?",
            "options": ["Guatemala City", "San José", "Managua", "Tegucigalpa"],
            "correct": 1,
            "explanation": "Costa Rica fővárosa San José, pénzneme a colón."
        },
        {
            "question": "Mi Honduras fővárosa?",
            "options": ["San José", "Managua", "Tegucigalpa", "Panamaváros"],
            "correct": 2,
            "explanation": "Honduras fővárosa Tegucigalpa, pénzneme a lempira."
        },
        {
            "question": "Mi Nicaragua fővárosa?",
            "options": ["Tegucigalpa", "Managua", "San José", "Belmopan"],
            "correct": 1,
            "explanation": "Nicaragua fővárosa Managua, pénzneme a córdoba."
        },
        {
            "question": "Mi Belize fővárosa?",
            "options": ["Belize City", "Belmopan", "San Salvador", "Guatemala City"],
            "correct": 1,
            "explanation": "Belize fővárosa Belmopan, pénzneme a belize-i dollár."
        },
        {
            "question": "Mi Fidzsi-szigetek fővárosa?",
            "options": ["Suva", "Nuku'alofa", "Apia", "Port Vila"],
            "correct": 0,
            "explanation": "Fidzsi-szigetek fővárosa Suva, pénzneme a fidzsi dollár."
        },
        {
            "question": "Mi Ausztrália fővárosa?",
            "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "correct": 2,
            "explanation": "Ausztrália fővárosa Canberra, nem Sydney vagy Melbourne."
        },
        {
            "question": "Mi Új-Zéland fővárosa?",
            "options": ["Auckland", "Wellington", "Christchurch", "Hamilton"],
            "correct": 1,
            "explanation": "Új-Zéland fővárosa Wellington, a legnagyobb város Auckland."
        },
        {
            "question": "Mi Pápua Új-Guinea fővárosa?",
            "options": ["Port Moresby", "Lae", "Mount Hagen", "Madang"],
            "correct": 0,
            "explanation": "Pápua Új-Guinea fővárosa Port Moresby, pénzneme a kina."
        },
        {
            "question": "Mi Samoa fővárosa?",
            "options": ["Apia", "Fagamalo", "Salelologa", "Asau"],
            "correct": 0,
            "explanation": "Samoa fővárosa Apia, pénzneme a tala."
        },
        {
            "question": "Mi Tonga fővárosa?",
            "options": ["Nuku'alofa", "Neiafu", "Pangai", "Hihifo"],
            "correct": 0,
            "explanation": "Tonga fővárosa Nuku'alofa, pénzneme a pa'anga."
        },
        {
            "question": "Mi Vanuatu fővárosa?",
            "options": ["Port Vila", "Luganville", "Isangel", "Lakatoro"],
            "correct": 0,
            "explanation": "Vanuatu fővárosa Port Vila, pénzneme a vatu."
        },
        {
            "question": "Mi a Salamon-szigetek fővárosa?",
            "options": ["Gizo", "Auki", "Honiara", "Munda"],
            "correct": 2,
            "explanation": "A Salamon-szigetek fővárosa Honiara, pénzneme a dollár."
        },
        {
            "question": "Mi Palau fővárosa?",
            "options": ["Koror", "Ngerulmud", "Airai", "Melekeok"],
            "correct": 1,
            "explanation": "Palau fővárosa Ngerulmud, pénzneme az amerikai dollár."
        },
        {
            "question": "Mi a Mikronéziai Szövetségi Államok fővárosa?",
            "options": ["Kolonia", "Weno", "Palikir", "Tofol"],
            "correct": 2,
            "explanation": "A Mikronéziai Szövetségi Államok fővárosa Palikir."
        },
        {
            "question": "Mi a Marshall-szigetek fővárosa?",
            "options": ["Majuro", "Ebeye", "Arno", "Kwajalein"],
            "correct": 0,
            "explanation": "A Marshall-szigetek fővárosa Majuro, pénzneme az amerikai dollár."
        }
    ],
    "komolyzene": CLASSICAL_MUSIC_QUESTIONS,
    "tudósok": [
        {
            "question": "Ki alapította a Vöröskeresztet?",
            "options": ["Albert Schweitzer", "Jean-Henri Dunant", "Kármán Tódor", "Jedlik Ányos"],
            "correct": 1,
            "explanation": "Jean-Henri Dunant alapította a Vöröskeresztet."
        },
        {
            "question": "Melyik magyar tudós volt bencés szerzetes?",
            "options": ["Kármán Tódor", "Csonka János", "Jedlik Ányos", "Bolyai János"],
            "correct": 2,
            "explanation": "Jedlik Ányos bencés szerzetes volt."
        },
        {
            "question": "Ki dolgozta ki a Cauchy-eloszlást?",
            "options": ["Gauss", "Euler", "Newton", "Cauchy"],
            "correct": 3,
            "explanation": "Augustin-Louis Cauchy francia matematikus dolgozta ki."
        },
        {
            "question": "Ki oldotta meg a königsbergi hidak problémáját?",
            "options": ["Newton", "Leibniz", "Euler", "Gauss"],
            "correct": 2,
            "explanation": "Leonhard Euler oldotta meg, megalapítva a gráfelméletet."
        },
        {
            "question": "Ki volt Konrad Lorenz?",
            "options": ["Etológus", "Fizikus", "Kémikus", "Matematikus"],
            "correct": 0,
            "explanation": "Konrad Lorenz osztrák etológus (állatviselkedés-kutató) volt."
        },
        {
            "question": "Kármán Tódor melyik tudományterületen alkotott?",
            "options": ["Biológia", "Kémia", "Geológia", "Aerodinamika"],
            "correct": 3,
            "explanation": "Kármán Tódor magyar származású aerodinamikus volt."
        },
        {
            "question": "Ki volt Albert Schweitzer?",
            "options": ["Fizikus", "Kémikus", "Orvos és filozófus", "Matematikus"],
            "correct": 2,
            "explanation": "Albert Schweitzer német-francia orvos és filozófus volt."
        },
        {
            "question": "Csonka János mivel foglalkozott?",
            "options": ["Csillagászat", "Botanika", "Geológia", "Gépészet"],
            "correct": 3,
            "explanation": "Csonka János magyar gépészmérnök és feltaláló volt."
        },
        {
            "question": "Mi a fotoszintézis lényege?",
            "options": ["Oxigén felhasználás", "Fehérje termelés", "Zsír égetés", "Szénhidrátkészítés"],
            "correct": 3,
            "explanation": "A fotoszintézis során a növények szénhidrátot készítenek fényenergiából."
        },
        {
            "question": "Mi a ganglion az orvostudományban?",
            "options": ["Izom", "Csont", "Idegdúc", "Véredény"],
            "correct": 2,
            "explanation": "A ganglion idegdúc, idegsejtek csoportosulása."
        }
    ],
    "mitológia": [
        # Görög mitológia
        {
            "question": "Ki a görög mitológiában a nap, jóslás, költészet és zene istene? (Apollón - a legszebb isten, aranyhajú, lantjával gyógyítja a lelket)",
            "options": ["Arész", "Apollón", "Hermész", "Héphaisztosz"],
            "correct": 1,
            "explanation": "Apollón a nap, jóslás, költészet és zene istene, a legszebb isten."
        },
        {
            "question": "Ki volt Orpheusz felesége? (Eurüdiké - akit a kígyócsípés után elvesztett, és az alvilágból próbált visszahozni)",
            "options": ["Eurüdiké", "Artemisz", "Aphrodité", "Thetisz"],
            "correct": 0,
            "explanation": "Eurüdiké volt Orpheusz felesége, akit a kígyócsípés után elvesztett."
        },
        {
            "question": "Ki a háború és vérontás istene a görög mitológiában? (Arész - a kegyetlen, vérszomjas isten, aki a csatákban élvezettel harcol)",
            "options": ["Apollón", "Héphaisztosz", "Hermész", "Arész"],
            "correct": 3,
            "explanation": "Arész a háború és vérontás istene, a kegyetlen, vérszomjas isten."
        },
        {
            "question": "Ki Akhilleusz anyja? (Thetisz - tengeri istennő, aki fiát a Stüx folyóba mártotta, hogy halhatatlanná tegye)",
            "options": ["Héra", "Aphrodité", "Thetisz", "Artemisz"],
            "correct": 2,
            "explanation": "Thetisz tengeri istennő Akhilleusz anyja, aki fiát a Stüx folyóba mártotta."
        },
        {
            "question": "Ki a tűz, kovácsmesterség és technológia istene? (Héphaisztosz - a sánta isten, aki fegyvereket és tárgyakat kovácsolt az isteneknek)",
            "options": ["Apollón", "Arész", "Héphaisztosz", "Hermész"],
            "correct": 2,
            "explanation": "Héphaisztosz a sánta isten, aki fegyvereket és tárgyakat kovácsolt."
        },
        {
            "question": "Ki az alvilág révésze? (Kharón - aki a halottak lelkét viszi át a Stüx folyón, pénzért)",
            "options": ["Hadész", "Orpheusz", "Hermész", "Kharón"],
            "correct": 3,
            "explanation": "Kharón az alvilág révésze, aki a halottak lelkét viszi át a Stüx folyón."
        },
        {
            "question": "Ki a vadászat, erdők és szűziesség istennője? (Artemisz - a vadász istennő, ikerhúga Apollónnak, mindig lándzsával és íjjal)",
            "options": ["Héra", "Aphrodité", "Artemisz", "Athéné"],
            "correct": 2,
            "explanation": "Artemisz a vadászat, erdők és szűziesség istennője, ikerhúga Apollónnak."
        },
        {
            "question": "Ki a szerelem, vágy és szépség istennője? (Aphrodité - aki a tenger habjaiból született, a legszebb istennő)",
            "options": ["Héra", "Artemisz", "Athéné", "Aphrodité"],
            "correct": 3,
            "explanation": "Aphrodité a szerelem, vágy és szépség istennője, aki a tenger habjaiból született."
        },
        {
            "question": "Mi okozta a trójai háborút? (Aphrodité aranyalmája - amit Párisznak adott, hogy a legszebb nőt megkapja)",
            "options": ["Héra bosszúja", "Zeus haragja", "Athéné bosszúja", "Aphrodité aranyalmája"],
            "correct": 3,
            "explanation": "Aphrodité aranyalmája okozta a trójai háborút, amit Párisznak adott."
        },
        {
            "question": "Ki lett Athén védőistennője? (Athéné - a bölcsesség istennője, aki az olajfáért versenyzett Poszeidónnal)",
            "options": ["Aphrodité", "Artemisz", "Athéné", "Héra"],
            "correct": 2,
            "explanation": "Athéné lett Athén védőistennője, a bölcsesség istennője."
        },
        {
            "question": "Ki a görög mitológiában a tenger istene? (Poszeidón - aki tridentjével földrengéseket és viharokat okoz)",
            "options": ["Zeus", "Poszeidón", "Hadész", "Apollón"],
            "correct": 1,
            "explanation": "Poszeidón a tenger istene, aki tridentjével földrengéseket okoz."
        },
        {
            "question": "Ki a görög mitológiában a menny istene? (Zeus - az istenek királya, aki villámokkal uralkodik)",
            "options": ["Apollón", "Zeus", "Arész", "Hermész"],
            "correct": 1,
            "explanation": "Zeus a menny istene, az istenek királya, aki villámokkal uralkodik."
        },
        {
            "question": "Ki a görög mitológiában az alvilág istene? (Hadész - aki a halottak lelkeit uralja, láthatatlan sisakot visel)",
            "options": ["Zeus", "Poszeidón", "Hadész", "Apollón"],
            "correct": 2,
            "explanation": "Hadész az alvilág istene, aki a halottak lelkeit uralja."
        },
        {
            "question": "Ki a görög mitológiában a házasság és család istennője? (Héra - Zeus felesége, aki féltékeny volt a férje szeretőire)",
            "options": ["Aphrodité", "Héra", "Athéné", "Artemisz"],
            "correct": 1,
            "explanation": "Héra a házasság és család istennője, Zeus felesége."
        },
        {
            "question": "Ki a görög mitológiában a kereskedelem és utazás istene? (Hermész - aki szárnyas cipőt és botot visel, az istenek hírnöke)",
            "options": ["Apollón", "Arész", "Hermész", "Héphaisztosz"],
            "correct": 2,
            "explanation": "Hermész a kereskedelem és utazás istene, az istenek hírnöke."
        },
        # Római mitológia
        {
            "question": "Ki a római mitológiában a háború istene? (Mars - a római hadsereg védőistene, aki a mezők és termékenység istene is)",
            "options": ["Jupiter", "Mars", "Neptunusz", "Pluto"],
            "correct": 1,
            "explanation": "Mars a római mitológiában a háború istene, a hadsereg védőistene."
        },
        {
            "question": "Ki a római mitológiában a menny istene? (Jupiter - az istenek királya, aki villámokkal uralkodik, Zeus római megfelelője)",
            "options": ["Mars", "Jupiter", "Neptunusz", "Apollo"],
            "correct": 1,
            "explanation": "Jupiter a római mitológiában a menny istene, Zeus megfelelője."
        },
        {
            "question": "Ki a római mitológiában a tenger istene? (Neptunusz - aki tridentjével uralja a tengereket, Poszeidón megfelelője)",
            "options": ["Jupiter", "Mars", "Neptunusz", "Pluto"],
            "correct": 2,
            "explanation": "Neptunusz a római mitológiában a tenger istene, Poszeidón megfelelője."
        },
        {
            "question": "Ki a római mitológiában a szerelem istennője? (Venus - a szépség és szerelem istennője, Aphrodité megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 2,
            "explanation": "Venus a római mitológiában a szerelem istennője, Aphrodité megfelelője."
        },
        {
            "question": "Ki a római mitológiában a bölcsesség istennője? (Minerva - a bölcsesség és háború istennője, Athéné megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 1,
            "explanation": "Minerva a római mitológiában a bölcsesség istennője, Athéné megfelelője."
        },
        {
            "question": "Ki a római mitológiában a házasság istennője? (Juno - Jupiter felesége, a nők és házasság védőistennője)",
            "options": ["Venus", "Minerva", "Juno", "Diana"],
            "correct": 2,
            "explanation": "Juno a római mitológiában a házasság istennője, Jupiter felesége."
        },
        {
            "question": "Ki a római mitológiában a vadászat istennője? (Diana - a vadászat és szűziesség istennője, Artemisz megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 3,
            "explanation": "Diana a római mitológiában a vadászat istennője, Artemisz megfelelője."
        },
        {
            "question": "Ki a római mitológiában a tűz istene? (Vulcanus - a kovácsmesterség istene, Héphaisztosz megfelelője)",
            "options": ["Mars", "Apollo", "Mercurius", "Vulcanus"],
            "correct": 3,
            "explanation": "Vulcanus a római mitológiában a tűz istene, Héphaisztosz megfelelője."
        },
        {
            "question": "Ki a római mitológiában a kereskedelem istene? (Mercurius - az istenek hírnöke, Hermész megfelelője)",
            "options": ["Apollo", "Mars", "Mercurius", "Vulcanus"],
            "correct": 2,
            "explanation": "Mercurius a római mitológiában a kereskedelem istene, Hermész megfelelője."
        },
        {
            "question": "Ki a római mitológiában a nap istene? (Apollo - a nap, költészet és zene istene, görög eredetű)",
            "options": ["Jupiter", "Mars", "Apollo", "Neptunusz"],
            "correct": 2,
            "explanation": "Apollo a római mitológiában a nap istene, görög eredetű."
        },
        # Északi mitológia
        {
            "question": "Ki az északi mitológiában a menny istene? (Odin - az istenek atyja, aki egy szemét feláldozta a bölcsességért)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 1,
            "explanation": "Odin az északi mitológiában a menny istene, az istenek atyja."
        },
        {
            "question": "Ki az északi mitológiában a mennydörgés istene? (Thor - aki Mjölnir kalapácsával harcol, Odin fia)",
            "options": ["Odin", "Thor", "Loki", "Freyr"],
            "correct": 1,
            "explanation": "Thor az északi mitológiában a mennydörgés istene, Odin fia."
        },
        {
            "question": "Ki az északi mitológiában a csalárdság istene? (Loki - a trükkös isten, aki gyakran bajt okoz az isteneknek)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 2,
            "explanation": "Loki az északi mitológiában a csalárdság istene, a trükkös isten."
        },
        {
            "question": "Ki az északi mitológiában a szerelem istennője? (Freya - a szerelem és szépség istennője, aki a Valkürök vezetője)",
            "options": ["Frigg", "Freya", "Sif", "Hel"],
            "correct": 1,
            "explanation": "Freya az északi mitológiában a szerelem istennője, a Valkürök vezetője."
        },
        {
            "question": "Ki az északi mitológiában a termékenység istene? (Freyr - a termékenység és béke istene, Freya testvére)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 3,
            "explanation": "Freyr az északi mitológiában a termékenység istene, Freya testvére."
        },
        {
            "question": "Ki az északi mitológiában a házasság istennője? (Frigg - Odin felesége, a házasság és anyaság istennője)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 1,
            "explanation": "Frigg az északi mitológiában a házasság istennője, Odin felesége."
        },
        {
            "question": "Ki az északi mitológiában a termékenység istennője? (Sif - Thor felesége, aranyhajú istennő)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 2,
            "explanation": "Sif az északi mitológiában a termékenység istennője, Thor felesége."
        },
        {
            "question": "Ki az északi mitológiában a halál istennője? (Hel - a halottak istennője, Loki lánya, aki az alvilágban uralkodik)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 3,
            "explanation": "Hel az északi mitológiában a halál istennője, Loki lánya."
        },
        {
            "question": "Mi az északi mitológiában a világfa neve? (Yggdrasil - a három világot összekötő óriási kőrisfa)",
            "options": ["Bifröst", "Yggdrasil", "Valhalla", "Asgard"],
            "correct": 1,
            "explanation": "Yggdrasil az északi mitológiában a világfa, a három világot összeköti."
        },
        {
            "question": "Mi az északi mitológiában a mennyország neve? (Asgard - az istenek otthona, ahol Odin uralkodik)",
            "options": ["Valhalla", "Asgard", "Midgard", "Helheim"],
            "correct": 1,
            "explanation": "Asgard az északi mitológiában a mennyország, az istenek otthona."
        },
        {
            "question": "Mi az északi mitológiában a harcosok mennyországának neve? (Valhalla - ahol a hősi halott harcosok élnek)",
            "options": ["Asgard", "Valhalla", "Midgard", "Helheim"],
            "correct": 1,
            "explanation": "Valhalla az északi mitológiában a harcosok mennyországa."
        },
        {
            "question": "Mi az északi mitológiában a szivárvány híd neve? (Bifröst - a híd, ami Asgardot köti össze Midgarddal)",
            "options": ["Yggdrasil", "Bifröst", "Valhalla", "Asgard"],
            "correct": 1,
            "explanation": "Bifröst az északi mitológiában a szivárvány híd, ami Asgardot köti össze Midgarddal."
        },
        {
            "question": "Mi az északi mitológiában a föld neve? (Midgard - az emberek világa, a középső világ)",
            "options": ["Asgard", "Valhalla", "Midgard", "Helheim"],
            "correct": 2,
            "explanation": "Midgard az északi mitológiában a föld, az emberek világa."
        },
        {
            "question": "Mi az északi mitológiában az alvilág neve? (Helheim - a halottak világa, ahol Hel uralkodik)",
            "options": ["Valhalla", "Asgard", "Midgard", "Helheim"],
            "correct": 3,
            "explanation": "Helheim az északi mitológiában az alvilág, a halottak világa."
        },
        {
            "question": "Mi az északi mitológiában Thor kalapácsának neve? (Mjölnir - a varázslatos kalapács, ami mindig visszatér Thorhoz)",
            "options": ["Gungnir", "Mjölnir", "Skofnung", "Tyrfing"],
            "correct": 1,
            "explanation": "Mjölnir az északi mitológiában Thor varázslatos kalapácsa."
        },
        {
            "question": "Mi az északi mitológiában Odin lándzsájának neve? (Gungnir - a varázslatos lándzsa, ami soha nem téveszti el a célját)",
            "options": ["Mjölnir", "Gungnir", "Skofnung", "Tyrfing"],
            "correct": 1,
            "explanation": "Gungnir az északi mitológiában Odin varázslatos lándzsája."
        },
        {
            "question": "Ki az északi mitológiában a háború istene? (Tyr - a háború és igazság istene, aki egy kezét feláldozta)",
            "options": ["Thor", "Odin", "Tyr", "Freyr"],
            "correct": 2,
            "explanation": "Tyr az északi mitológiában a háború istene, aki egy kezét feláldozta."
        },
        {
            "question": "Ki az északi mitológiában a tenger istene? (Njord - a tenger és halászat istene, Freyr és Freya apja)",
            "options": ["Thor", "Odin", "Njord", "Freyr"],
            "correct": 2,
            "explanation": "Njord az északi mitológiában a tenger istene, Freyr és Freya apja."
        },
        {
            "question": "Ki az északi mitológiában a bölcsesség istennője? (Saga - a bölcsesség és történetek istennője, Odin társa)",
            "options": ["Freya", "Frigg", "Saga", "Hel"],
            "correct": 2,
            "explanation": "Saga az északi mitológiában a bölcsesség istennője, Odin társa."
        },
        {
            "question": "Mi az északi mitológiában a végítélet napjának neve? (Ragnarök - a világ vége, amikor az istenek és óriások harcolnak)",
            "options": ["Yggdrasil", "Bifröst", "Ragnarök", "Valhalla"],
            "correct": 2,
            "explanation": "Ragnarök az északi mitológiában a végítélet napja, a világ vége."
        },
        {
            "question": "Ki az északi mitológiában a termékenység óriása? (Ymir - az első lény, akiből a világ teremtődött)",
            "options": ["Thor", "Odin", "Loki", "Ymir"],
            "correct": 3,
            "explanation": "Ymir az északi mitológiában a termékenység óriása, az első lény."
        },
        {
            "question": "Ki az északi mitológiában a tűz óriása? (Surtr - a tűz óriása, aki Ragnarökön felégeti a világot)",
            "options": ["Ymir", "Surtr", "Loki", "Hel"],
            "correct": 1,
            "explanation": "Surtr az északi mitológiában a tűz óriása, aki Ragnarökön felégeti a világot."
        },
        {
            "question": "Ki az északi mitológiában a jég óriása? (Hrímthurs - a jég óriásai, akik az északi sarkon élnek)",
            "options": ["Ymir", "Surtr", "Hrímthurs", "Hel"],
            "correct": 2,
            "explanation": "Hrímthurs az északi mitológiában a jég óriásai, akik az északi sarkon élnek."
        },
        {
            "question": "Mi az északi mitológiában a Valkürök szerepe? (A harcosok kiválasztása - a női lények, akik a hősi halottakat Valhallába viszik)",
            "options": ["Az istenek szolgálói", "A harcosok kiválasztása", "A halottak őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Valkürök az északi mitológiában a harcosok kiválasztói, a hősi halottakat Valhallába viszik."
        },
        {
            "question": "Mi az északi mitológiában a Nornok szerepe? (A sors istennői - három nő, akik az emberek sorsát szőrik)",
            "options": ["A harcosok vezetői", "A sors istennői", "A termékenység őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Nornok az északi mitológiában a sors istennői, akik az emberek sorsát szőrik."
        },
        {
            "question": "Mi az északi mitológiában a Dísir szerepe? (A család védőistennői - női lények, akik a családokat védik)",
            "options": ["A harcosok segítői", "A család védőistennői", "A termékenység őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Dísir az északi mitológiában a család védőistennői, akik a családokat védik."
        }
    ],
    "drámák": [
        # Shakespeare drámák
        {
            "question": "Melyik drámában szerepel egy dán herceg, aki bosszút áll apja haláláért? (Hamlet, Ophelia, Polonius, Gertrude)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 0,
            "explanation": "Hamlet - a dán herceg, aki bosszút áll apja haláláért, miután apja szelleme elmondja, hogy bátyja mérgezte meg."
        },
        {
            "question": "Melyik drámában szerepel egy skót tábornok, aki király akar lenni? (Macbeth, Lady Macbeth, Banquo, Macduff)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 1,
            "explanation": "Macbeth - a skót tábornok, aki a három boszorkány jóslata miatt meggyilkolja a királyt, hogy király legyen."
        },
        {
            "question": "Melyik drámában szerepel egy mór tábornok, aki féltékeny feleségére? (Othello, Desdemona, Iago, Cassio)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 2,
            "explanation": "Othello - a mór tábornok, aki Iago manipulálására féltékeny lesz és megfojtja feleségét, Desdemonát."
        },
        {
            "question": "Melyik drámában szerepel egy király, aki három lányának osztja országát? (King Lear, Goneril, Regan, Cordelia)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 3,
            "explanation": "King Lear - a király, aki három lányának osztja országát, de csak a legkisebb, Cordelia mondja meg az igazat."
        },
        {
            "question": "Melyik drámában szerepel két szerelmes, akik családjuk ellenségeskedése miatt nem lehetnek együtt? (Romeo, Júlia, Mercutio, Tybalt)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 0,
            "explanation": "Romeo és Júlia - a két szerelmes, akik a Capulet és Montague családok ellenségeskedése miatt nem lehetnek együtt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában menekül az erdőbe? (Rosalind, Orlando, Celia, Jacques)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 2,
            "explanation": "Ahogy tetszik - Rosalind, aki férfi ruhában menekül az erdőbe, miután elűzték a udvarból."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában szolgál egy hercegnél? (Viola, Orsino, Olivia, Sebastian)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 3,
            "explanation": "Vízkereszt - Viola, aki férfi ruhában szolgál Orsino hercegnél, miután hajótörést szenvedett."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában védi barátját a bíróságon? (Portia, Bassanio, Antonio, Shylock)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 1,
            "explanation": "Szeget szeggel - Portia, aki férfi ruhában védi Bassanio barátját a bíróságon."
        },
        {
            "question": "Melyik drámában szerepel egy király, aki három boszorkánytól kap jóslatot? (Macbeth, Lady Macbeth, Banquo, Macduff)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 1,
            "explanation": "Macbeth - a király, aki a három boszorkánytól kap jóslatot, hogy király lesz."
        },
        {
            "question": "Melyik drámában szerepel egy herceg, aki 'Lenni vagy nem lenni' monológot mond? (Hamlet, Ophelia, Polonius, Gertrude)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 0,
            "explanation": "Hamlet - a herceg, aki a híres 'Lenni vagy nem lenni' monológot mondja a halálról és a cselekvésről."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki álomba hullatja magát, hogy meghaljon? (Júlia, Romeo, Mercutio, Tybalt)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 0,
            "explanation": "Romeo és Júlia - Júlia álomba hullatja magát, hogy meghaljon, de Romeo nem tudja és megmérgezi magát."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki három ládikából választ? (Portia, Bassanio, Antonio, Shylock)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 1,
            "explanation": "Szeget szeggel - Portia, aki három ládikából választ: arany, ezüst, ólom, és csak az ólomban van a kép."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki ikerhúga után kutat? (Viola, Sebastian, Orsino, Olivia)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 3,
            "explanation": "Vízkereszt - Viola, aki ikerhúga, Sebastian után kutat, miután hajótörést szenvedett."
        },
        {
            "question": "Melyik drámában szerepel egy férfi, aki 'A világ egy színház' monológot mond? (Jacques, Rosalind, Orlando, Celia)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 2,
            "explanation": "Ahogy tetszik - Jacques, aki a híres 'A világ egy színház' monológot mondja."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki 'Minden világos' monológot mond? (Cordelia, King Lear, Goneril, Regan)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 3,
            "explanation": "King Lear - Cordelia, aki a 'Minden világos' monológot mondja apjának."
        },
        # Csehov drámák
        {
            "question": "Melyik drámában szerepel egy család, aki a cseresznyéskert eladását tervezi? (Ranevszkaja, Lopahin, Trofimov, Várya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - a Ranevszkaja család, aki a cseresznyéskert eladását tervezi, mert nincs pénzük."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal író, aki szerelmes egy nőbe? (Treplev, Nina Zarecsnaja, Trigorin, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Treplev, aki szerelmes Nina Zarecsnajába, de Nina Trigorin íróba szerelmes."
        },
        {
            "question": "Melyik drámában szerepel három nővér, akik Moszkvába akarnak költözni? (Olga, Mása, Irina, Versinyin)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Olga, Mása és Irina, akik Moszkvába akarnak költözni, de soha nem jutnak el oda."
        },
        {
            "question": "Melyik drámában szerepel egy férfi, aki szerelmes sógorába? (Ványa bácsi, Jelena, Asztrov, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Ványa bácsi, aki szerelmes Jelena sógorába, de Jelena nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal színésznő, aki szerelmes egy íróba? (Nina Zarecsnaja, Trigorin, Treplev, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Nina Zarecsnaja, aki szerelmes Trigorin íróba, de Trigorin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy orvosba? (Mása, Versinyin, Olga, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Mása, aki szerelmes Versinyin orvosba, de Versinyin feleségével él."
        },
        {
            "question": "Melyik drámában szerepel egy üzletember, aki szerelmes egy nőbe? (Lopahin, Várya, Ranevszkaja, Trofimov)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Lopahin, aki szerelmes Váryába, de Várya nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy lány, aki szerelmes egy orvosba? (Szonya, Asztrov, Ványa bácsi, Jelena)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Szonya, aki szerelmes Asztrov orvosba, de Asztrov nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy báróba? (Irina, Tusenbach, Mása, Olga)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Irina, aki szerelmes Tusenbach báróba, de Tusenbach meghal a párbajban."
        },
        {
            "question": "Melyik drámában szerepel egy színésznő, aki szerelmes egy íróba? (Arkagyina, Trigorin, Nina Zarecsnaja, Treplev)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Arkagyina, aki szerelmes Trigorin íróba, de Trigorin Nina Zarecsnajába szerelmes."
        },
        {
            "question": "Melyik drámában szerepel egy diák, aki szerelmes egy lányba? (Trofimov, Anja, Ranevszkaja, Lopahin)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Trofimov, aki szerelmes Anjába, de Anja nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy orvos, aki szerelmes egy nőbe? (Asztrov, Jelena, Ványa bácsi, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Asztrov, aki szerelmes Jelena sógorába, de Jelena nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy katonatiszt, aki szerelmes egy nőbe? (Versinyin, Mása, Olga, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Versinyin, aki szerelmes Mása nővérébe, de Mása férjével él."
        },
        {
            "question": "Melyik drámában szerepel egy író, aki szerelmes egy fiatal nőbe? (Trigorin, Nina Zarecsnaja, Arkagyina, Treplev)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Trigorin, aki szerelmes Nina Zarecsnajába, de Nina nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy lány, aki szerelmes egy üzletemberbe? (Várya, Lopahin, Ranevszkaja, Trofimov)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Várya, aki szerelmes Lopahinba, de Lopahin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy orvosba? (Jelena, Asztrov, Ványa bácsi, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Jelena, aki szerelmes Asztrov orvosba, de Asztrov nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy tanárba? (Olga, Kuligin, Mása, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Olga, aki szerelmes Kuliginba, de Kuligin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal nő, aki szerelmes egy íróba? (Nina Zarecsnaja, Treplev, Trigorin, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Nina Zarecsnaja, aki szerelmes Treplevba, de Treplev nem szereti őt."
        }
    ],
    "állatok": [
        {
            "question": "Mi az okapi rokonsági foka?",
            "options": ["Zsiráf rokona", "Zebra rokona", "Antilop rokona", "Ló rokona"],
            "correct": 0,
            "explanation": "Az okapi afrikai állat, amely a zsiráf rokona."
        },
        {
            "question": "Hol él a tüskés ördög?",
            "options": ["Afrika", "Ázsia", "Dél-Amerika", "Ausztrália"],
            "correct": 3,
            "explanation": "A tüskés ördög egy ausztrál hüllő."
        },
        {
            "question": "Mi a kacsafarkú szender?",
            "options": ["Madár", "Emlős", "Hüllő", "Rovar lepke-szender"],
            "correct": 3,
            "explanation": "A kacsafarkú szender egy rovar lepke-szender."
        },
        {
            "question": "Milyen állat az axolotl?",
            "options": ["Hüllő", "Hal", "Kétéltű", "Emlős"],
            "correct": 2,
            "explanation": "Az axolotl egy kétéltű állat."
        },
        {
            "question": "Mi a binturong másik neve?",
            "options": ["Pálmasodró cibetmacska", "Himalájai macska", "Erdei macska", "Vaddisznó"],
            "correct": 0,
            "explanation": "A binturong más néven pálmasodró cibetmacska."
        },
        {
            "question": "Hol élt a tarpán?",
            "options": ["Afrika", "Amerika", "Eurázsia", "Ausztrália"],
            "correct": 2,
            "explanation": "A tarpán egy eurázsiai vadló volt."
        },
        {
            "question": "Hol található a csillagorrú vakond?",
            "options": ["USA", "Kanada", "Mexikó", "Grönland"],
            "correct": 0,
            "explanation": "A csillagorrú vakond az USA-ban található."
        },
        {
            "question": "Mi a quokka teljes neve?",
            "options": ["Rövid farkú oposszum", "Kis válú medve", "Kurtafarkú kenguru", "Törpe antilop"],
            "correct": 2,
            "explanation": "A quokka kurtafarkú kenguru."
        },
        {
            "question": "Hol él a takin?",
            "options": ["Alpok", "Andok", "Kaukázus", "Himalája"],
            "correct": 3,
            "explanation": "A takin egy himalájai antilop."
        },
        {
            "question": "Hol található az ocelot?",
            "options": ["Észak-Amerika", "Afrika", "Ázsia", "Dél-Amerika"],
            "correct": 3,
            "explanation": "Az ocelot Dél-Amerikában található."
        }
    ],
    "us_államok": [
"""
🧠 PDF Alapú Quiz Alkalmazás
10 kérdéses feleletválasztós teszt a feltöltött PDF tartalom alapján
"""

import streamlit as st
import random
import time
from datetime import datetime
import os
from pathlib import Path
from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS

# Page config
st.set_page_config(
    page_title="🧠 PDF Quiz Alkalmazás",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Quiz adatok témakörök szerint csoportosítva
QUIZ_DATA_BY_TOPIC = {
    "földrajz": [
        {
            "question": "Mi a legmagasabb csúcs a Mátrában?",
            "options": ["Kékes", "Dobogó-kő", "Csóványos", "Szilvási-kő"],
            "correct": 0,
            "explanation": "A Kékes 1014 méter magasságával a Mátra legmagasabb csúcsa."
        },
        {
            "question": "Melyik ország fővárosa Taskent?",
            "options": ["Kazahsztán", "Üzbegisztán", "Kirgizisztán", "Tádzsikisztán"],
            "correct": 1,
            "explanation": "Taskent Üzbegisztán fővárosa."
        },
        {
            "question": "Melyik a világ leghosszabb folyója?",
            "options": ["Amazonas", "Nílus", "Jangce", "Mississippi"],
            "correct": 1,
            "explanation": "A Nílus 6650 km hosszával a világ leghosszabb folyója."
        },
        {
            "question": "Mi Bhután fővárosa?",
            "options": ["Thimphu", "Katmandu", "Dhaka", "Vientiane"],
            "correct": 0,
            "explanation": "Bhután fővárosa Thimphu, pénzneme a ngultrum."
        },
        {
            "question": "Melyik hegység csúcsa a Börzsöny legmagasabb pontja?",
            "options": ["Nagy-Kopasz", "Pilis", "Dobogó-kő", "Csóványos"],
            "correct": 3,
            "explanation": "A Csóványos (938 m) a Börzsöny hegység legmagasabb csúcsa."
        },
        {
            "question": "Melyik kontinensen található a Kilimandzsáró?",
            "options": ["Ázsia", "Dél-Amerika", "Afrika", "Ausztrália"],
            "correct": 2,
            "explanation": "A Kilimandzsáró (5895 m) Afrika legmagasabb hegycsúcsa."
        },
        {
            "question": "Mi Costa Rica pénzneme?",
            "options": ["Peso", "Dollár", "Quetzal", "Colón"],
            "correct": 3,
            "explanation": "Costa Rica pénzneme a Costa Rica-i colón."
        },
        {
            "question": "Melyik az Európa leghosszabb folyója?",
            "options": ["Volga", "Duna", "Rajna", "Dnyeper"],
            "correct": 0,
            "explanation": "A Volga 3530 km hosszával Európa leghosszabb folyója."
        },
        {
            "question": "Mi a Pilis hegység legmagasabb csúcsa?",
            "options": ["Nagy-Kopasz", "Dobogó-kő", "Szánkó-hegy", "Pilis"],
            "correct": 3,
            "explanation": "A Pilis (757 m) a Pilis hegység névadó és legmagasabb csúcsa."
        },
        {
            "question": "Melyik ország pénzneme a manat?",
            "options": ["Grúzia", "Örményország", "Azerbajdzsán", "Kazahsztán"],
            "correct": 2,
            "explanation": "Azerbajdzsán pénzneme a manat, fővárosa Baku."
        },
        {
            "question": "Mi Üzbegisztán fővárosa?",
            "options": ["Taskent", "Biskek", "Dusanbe", "Tbiliszi"],
            "correct": 0,
            "explanation": "Üzbegisztán fővárosa Taskent, pénzneme a som."
        },
        {
            "question": "Mi Kirgizisztán fővárosa?",
            "options": ["Taskent", "Biskek", "Asztana", "Jereván"],
            "correct": 1,
            "explanation": "Kirgizisztán fővárosa Biskek, pénzneme a som."
        },
        {
            "question": "Mi Tádzsikisztán fővárosa?",
            "options": ["Biskek", "Dusanbe", "Taskent", "Baku"],
            "correct": 1,
            "explanation": "Tádzsikisztán fővárosa Dusanbe, pénzneme a somoni."
        },
        {
            "question": "Mi Grúzia fővárosa?",
            "options": ["Baku", "Jereván", "Tbiliszi", "Asztana"],
            "correct": 2,
            "explanation": "Grúzia fővárosa Tbiliszi, pénzneme a lari."
        },
        {
            "question": "Mi Örményország fővárosa?",
            "options": ["Tbiliszi", "Jereván", "Baku", "Biskek"],
            "correct": 1,
            "explanation": "Örményország fővárosa Jereván, pénzneme a dram."
        },
        {
            "question": "Mi Kazahsztán fővárosa?",
            "options": ["Almati", "Asztana", "Taskent", "Biskek"],
            "correct": 1,
            "explanation": "Kazahsztán fővárosa Asztana (ma Nur-Sultan), pénzneme a tenge."
        },
        {
            "question": "Mi Laosz fővárosa?",
            "options": ["Vientiane", "Phnom Penh", "Bangkok", "Hanoi"],
            "correct": 0,
            "explanation": "Laosz fővárosa Vientiane, pénzneme a kip."
        },
        {
            "question": "Mi Brunei fővárosa?",
            "options": ["Bandar Seri Begawan", "Kuala Lumpur", "Jakarta", "Manila"],
            "correct": 0,
            "explanation": "Brunei fővárosa Bandar Seri Begawan, pénzneme a dollár."
        },
        {
            "question": "Mi Costa Rica fővárosa?",
            "options": ["Guatemala City", "San José", "Managua", "Tegucigalpa"],
            "correct": 1,
            "explanation": "Costa Rica fővárosa San José, pénzneme a colón."
        },
        {
            "question": "Mi Honduras fővárosa?",
            "options": ["San José", "Managua", "Tegucigalpa", "Panamaváros"],
            "correct": 2,
            "explanation": "Honduras fővárosa Tegucigalpa, pénzneme a lempira."
        },
        {
            "question": "Mi Nicaragua fővárosa?",
            "options": ["Tegucigalpa", "Managua", "San José", "Belmopan"],
            "correct": 1,
            "explanation": "Nicaragua fővárosa Managua, pénzneme a córdoba."
        },
        {
            "question": "Mi Belize fővárosa?",
            "options": ["Belize City", "Belmopan", "San Salvador", "Guatemala City"],
            "correct": 1,
            "explanation": "Belize fővárosa Belmopan, pénzneme a belize-i dollár."
        },
        {
            "question": "Mi Fidzsi-szigetek fővárosa?",
            "options": ["Suva", "Nuku'alofa", "Apia", "Port Vila"],
            "correct": 0,
            "explanation": "Fidzsi-szigetek fővárosa Suva, pénzneme a fidzsi dollár."
        },
        {
            "question": "Mi Ausztrália fővárosa?",
            "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
            "correct": 2,
            "explanation": "Ausztrália fővárosa Canberra, nem Sydney vagy Melbourne."
        },
        {
            "question": "Mi Új-Zéland fővárosa?",
            "options": ["Auckland", "Wellington", "Christchurch", "Hamilton"],
            "correct": 1,
            "explanation": "Új-Zéland fővárosa Wellington, a legnagyobb város Auckland."
        },
        {
            "question": "Mi Pápua Új-Guinea fővárosa?",
            "options": ["Port Moresby", "Lae", "Mount Hagen", "Madang"],
            "correct": 0,
            "explanation": "Pápua Új-Guinea fővárosa Port Moresby, pénzneme a kina."
        },
        {
            "question": "Mi Samoa fővárosa?",
            "options": ["Apia", "Fagamalo", "Salelologa", "Asau"],
            "correct": 0,
            "explanation": "Samoa fővárosa Apia, pénzneme a tala."
        },
        {
            "question": "Mi Tonga fővárosa?",
            "options": ["Nuku'alofa", "Neiafu", "Pangai", "Hihifo"],
            "correct": 0,
            "explanation": "Tonga fővárosa Nuku'alofa, pénzneme a pa'anga."
        },
        {
            "question": "Mi Vanuatu fővárosa?",
            "options": ["Port Vila", "Luganville", "Isangel", "Lakatoro"],
            "correct": 0,
            "explanation": "Vanuatu fővárosa Port Vila, pénzneme a vatu."
        },
        {
            "question": "Mi a Salamon-szigetek fővárosa?",
            "options": ["Gizo", "Auki", "Honiara", "Munda"],
            "correct": 2,
            "explanation": "A Salamon-szigetek fővárosa Honiara, pénzneme a dollár."
        },
        {
            "question": "Mi Palau fővárosa?",
            "options": ["Koror", "Ngerulmud", "Airai", "Melekeok"],
            "correct": 1,
            "explanation": "Palau fővárosa Ngerulmud, pénzneme az amerikai dollár."
        },
        {
            "question": "Mi a Mikronéziai Szövetségi Államok fővárosa?",
            "options": ["Kolonia", "Weno", "Palikir", "Tofol"],
            "correct": 2,
            "explanation": "A Mikronéziai Szövetségi Államok fővárosa Palikir."
        },
        {
            "question": "Mi a Marshall-szigetek fővárosa?",
            "options": ["Majuro", "Ebeye", "Arno", "Kwajalein"],
            "correct": 0,
            "explanation": "A Marshall-szigetek fővárosa Majuro, pénzneme az amerikai dollár."
        }
    ],
    "komolyzene": CLASSICAL_MUSIC_QUESTIONS,
    "tudósok": [
        {
            "question": "Ki alapította a Vöröskeresztet?",
            "options": ["Albert Schweitzer", "Jean-Henri Dunant", "Kármán Tódor", "Jedlik Ányos"],
            "correct": 1,
            "explanation": "Jean-Henri Dunant alapította a Vöröskeresztet."
        },
        {
            "question": "Melyik magyar tudós volt bencés szerzetes?",
            "options": ["Kármán Tódor", "Csonka János", "Jedlik Ányos", "Bolyai János"],
            "correct": 2,
            "explanation": "Jedlik Ányos bencés szerzetes volt."
        },
        {
            "question": "Ki dolgozta ki a Cauchy-eloszlást?",
            "options": ["Gauss", "Euler", "Newton", "Cauchy"],
            "correct": 3,
            "explanation": "Augustin-Louis Cauchy francia matematikus dolgozta ki."
        },
        {
            "question": "Ki oldotta meg a königsbergi hidak problémáját?",
            "options": ["Newton", "Leibniz", "Euler", "Gauss"],
            "correct": 2,
            "explanation": "Leonhard Euler oldotta meg, megalapítva a gráfelméletet."
        },
        {
            "question": "Ki volt Konrad Lorenz?",
            "options": ["Etológus", "Fizikus", "Kémikus", "Matematikus"],
            "correct": 0,
            "explanation": "Konrad Lorenz osztrák etológus (állatviselkedés-kutató) volt."
        },
        {
            "question": "Kármán Tódor melyik tudományterületen alkotott?",
            "options": ["Biológia", "Kémia", "Geológia", "Aerodinamika"],
            "correct": 3,
            "explanation": "Kármán Tódor magyar származású aerodinamikus volt."
        },
        {
            "question": "Ki volt Albert Schweitzer?",
            "options": ["Fizikus", "Kémikus", "Orvos és filozófus", "Matematikus"],
            "correct": 2,
            "explanation": "Albert Schweitzer német-francia orvos és filozófus volt."
        },
        {
            "question": "Csonka János mivel foglalkozott?",
            "options": ["Csillagászat", "Botanika", "Geológia", "Gépészet"],
            "correct": 3,
            "explanation": "Csonka János magyar gépészmérnök és feltaláló volt."
        },
        {
            "question": "Mi a fotoszintézis lényege?",
            "options": ["Oxigén felhasználás", "Fehérje termelés", "Zsír égetés", "Szénhidrátkészítés"],
            "correct": 3,
            "explanation": "A fotoszintézis során a növények szénhidrátot készítenek fényenergiából."
        },
        {
            "question": "Mi a ganglion az orvostudományban?",
            "options": ["Izom", "Csont", "Idegdúc", "Véredény"],
            "correct": 2,
            "explanation": "A ganglion idegdúc, idegsejtek csoportosulása."
        }
    ],
    "mitológia": [
        # Görög mitológia
        {
            "question": "Ki a görög mitológiában a nap, jóslás, költészet és zene istene? (Apollón - a legszebb isten, aranyhajú, lantjával gyógyítja a lelket)",
            "options": ["Arész", "Apollón", "Hermész", "Héphaisztosz"],
            "correct": 1,
            "explanation": "Apollón a nap, jóslás, költészet és zene istene, a legszebb isten."
        },
        {
            "question": "Ki volt Orpheusz felesége? (Eurüdiké - akit a kígyócsípés után elvesztett, és az alvilágból próbált visszahozni)",
            "options": ["Eurüdiké", "Artemisz", "Aphrodité", "Thetisz"],
            "correct": 0,
            "explanation": "Eurüdiké volt Orpheusz felesége, akit a kígyócsípés után elvesztett."
        },
        {
            "question": "Ki a háború és vérontás istene a görög mitológiában? (Arész - a kegyetlen, vérszomjas isten, aki a csatákban élvezettel harcol)",
            "options": ["Apollón", "Héphaisztosz", "Hermész", "Arész"],
            "correct": 3,
            "explanation": "Arész a háború és vérontás istene, a kegyetlen, vérszomjas isten."
        },
        {
            "question": "Ki Akhilleusz anyja? (Thetisz - tengeri istennő, aki fiát a Stüx folyóba mártotta, hogy halhatatlanná tegye)",
            "options": ["Héra", "Aphrodité", "Thetisz", "Artemisz"],
            "correct": 2,
            "explanation": "Thetisz tengeri istennő Akhilleusz anyja, aki fiát a Stüx folyóba mártotta."
        },
        {
            "question": "Ki a tűz, kovácsmesterség és technológia istene? (Héphaisztosz - a sánta isten, aki fegyvereket és tárgyakat kovácsolt az isteneknek)",
            "options": ["Apollón", "Arész", "Héphaisztosz", "Hermész"],
            "correct": 2,
            "explanation": "Héphaisztosz a sánta isten, aki fegyvereket és tárgyakat kovácsolt."
        },
        {
            "question": "Ki az alvilág révésze? (Kharón - aki a halottak lelkét viszi át a Stüx folyón, pénzért)",
            "options": ["Hadész", "Orpheusz", "Hermész", "Kharón"],
            "correct": 3,
            "explanation": "Kharón az alvilág révésze, aki a halottak lelkét viszi át a Stüx folyón."
        },
        {
            "question": "Ki a vadászat, erdők és szűziesség istennője? (Artemisz - a vadász istennő, ikerhúga Apollónnak, mindig lándzsával és íjjal)",
            "options": ["Héra", "Aphrodité", "Artemisz", "Athéné"],
            "correct": 2,
            "explanation": "Artemisz a vadászat, erdők és szűziesség istennője, ikerhúga Apollónnak."
        },
        {
            "question": "Ki a szerelem, vágy és szépség istennője? (Aphrodité - aki a tenger habjaiból született, a legszebb istennő)",
            "options": ["Héra", "Artemisz", "Athéné", "Aphrodité"],
            "correct": 3,
            "explanation": "Aphrodité a szerelem, vágy és szépség istennője, aki a tenger habjaiból született."
        },
        {
            "question": "Mi okozta a trójai háborút? (Aphrodité aranyalmája - amit Párisznak adott, hogy a legszebb nőt megkapja)",
            "options": ["Héra bosszúja", "Zeus haragja", "Athéné bosszúja", "Aphrodité aranyalmája"],
            "correct": 3,
            "explanation": "Aphrodité aranyalmája okozta a trójai háborút, amit Párisznak adott."
        },
        {
            "question": "Ki lett Athén védőistennője? (Athéné - a bölcsesség istennője, aki az olajfáért versenyzett Poszeidónnal)",
            "options": ["Aphrodité", "Artemisz", "Athéné", "Héra"],
            "correct": 2,
            "explanation": "Athéné lett Athén védőistennője, a bölcsesség istennője."
        },
        {
            "question": "Ki a görög mitológiában a tenger istene? (Poszeidón - aki tridentjével földrengéseket és viharokat okoz)",
            "options": ["Zeus", "Poszeidón", "Hadész", "Apollón"],
            "correct": 1,
            "explanation": "Poszeidón a tenger istene, aki tridentjével földrengéseket okoz."
        },
        {
            "question": "Ki a görög mitológiában a menny istene? (Zeus - az istenek királya, aki villámokkal uralkodik)",
            "options": ["Apollón", "Zeus", "Arész", "Hermész"],
            "correct": 1,
            "explanation": "Zeus a menny istene, az istenek királya, aki villámokkal uralkodik."
        },
        {
            "question": "Ki a görög mitológiában az alvilág istene? (Hadész - aki a halottak lelkeit uralja, láthatatlan sisakot visel)",
            "options": ["Zeus", "Poszeidón", "Hadész", "Apollón"],
            "correct": 2,
            "explanation": "Hadész az alvilág istene, aki a halottak lelkeit uralja."
        },
        {
            "question": "Ki a görög mitológiában a házasság és család istennője? (Héra - Zeus felesége, aki féltékeny volt a férje szeretőire)",
            "options": ["Aphrodité", "Héra", "Athéné", "Artemisz"],
            "correct": 1,
            "explanation": "Héra a házasság és család istennője, Zeus felesége."
        },
        {
            "question": "Ki a görög mitológiában a kereskedelem és utazás istene? (Hermész - aki szárnyas cipőt és botot visel, az istenek hírnöke)",
            "options": ["Apollón", "Arész", "Hermész", "Héphaisztosz"],
            "correct": 2,
            "explanation": "Hermész a kereskedelem és utazás istene, az istenek hírnöke."
        },
        # Római mitológia
        {
            "question": "Ki a római mitológiában a háború istene? (Mars - a római hadsereg védőistene, aki a mezők és termékenység istene is)",
            "options": ["Jupiter", "Mars", "Neptunusz", "Pluto"],
            "correct": 1,
            "explanation": "Mars a római mitológiában a háború istene, a hadsereg védőistene."
        },
        {
            "question": "Ki a római mitológiában a menny istene? (Jupiter - az istenek királya, aki villámokkal uralkodik, Zeus római megfelelője)",
            "options": ["Mars", "Jupiter", "Neptunusz", "Apollo"],
            "correct": 1,
            "explanation": "Jupiter a római mitológiában a menny istene, Zeus megfelelője."
        },
        {
            "question": "Ki a római mitológiában a tenger istene? (Neptunusz - aki tridentjével uralja a tengereket, Poszeidón megfelelője)",
            "options": ["Jupiter", "Mars", "Neptunusz", "Pluto"],
            "correct": 2,
            "explanation": "Neptunusz a római mitológiában a tenger istene, Poszeidón megfelelője."
        },
        {
            "question": "Ki a római mitológiában a szerelem istennője? (Venus - a szépség és szerelem istennője, Aphrodité megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 2,
            "explanation": "Venus a római mitológiában a szerelem istennője, Aphrodité megfelelője."
        },
        {
            "question": "Ki a római mitológiában a bölcsesség istennője? (Minerva - a bölcsesség és háború istennője, Athéné megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 1,
            "explanation": "Minerva a római mitológiában a bölcsesség istennője, Athéné megfelelője."
        },
        {
            "question": "Ki a római mitológiában a házasság istennője? (Juno - Jupiter felesége, a nők és házasság védőistennője)",
            "options": ["Venus", "Minerva", "Juno", "Diana"],
            "correct": 2,
            "explanation": "Juno a római mitológiában a házasság istennője, Jupiter felesége."
        },
        {
            "question": "Ki a római mitológiában a vadászat istennője? (Diana - a vadászat és szűziesség istennője, Artemisz megfelelője)",
            "options": ["Juno", "Minerva", "Venus", "Diana"],
            "correct": 3,
            "explanation": "Diana a római mitológiában a vadászat istennője, Artemisz megfelelője."
        },
        {
            "question": "Ki a római mitológiában a tűz istene? (Vulcanus - a kovácsmesterség istene, Héphaisztosz megfelelője)",
            "options": ["Mars", "Apollo", "Mercurius", "Vulcanus"],
            "correct": 3,
            "explanation": "Vulcanus a római mitológiában a tűz istene, Héphaisztosz megfelelője."
        },
        {
            "question": "Ki a római mitológiában a kereskedelem istene? (Mercurius - az istenek hírnöke, Hermész megfelelője)",
            "options": ["Apollo", "Mars", "Mercurius", "Vulcanus"],
            "correct": 2,
            "explanation": "Mercurius a római mitológiában a kereskedelem istene, Hermész megfelelője."
        },
        {
            "question": "Ki a római mitológiában a nap istene? (Apollo - a nap, költészet és zene istene, görög eredetű)",
            "options": ["Jupiter", "Mars", "Apollo", "Neptunusz"],
            "correct": 2,
            "explanation": "Apollo a római mitológiában a nap istene, görög eredetű."
        },
        # Északi mitológia
        {
            "question": "Ki az északi mitológiában a menny istene? (Odin - az istenek atyja, aki egy szemét feláldozta a bölcsességért)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 1,
            "explanation": "Odin az északi mitológiában a menny istene, az istenek atyja."
        },
        {
            "question": "Ki az északi mitológiában a mennydörgés istene? (Thor - aki Mjölnir kalapácsával harcol, Odin fia)",
            "options": ["Odin", "Thor", "Loki", "Freyr"],
            "correct": 1,
            "explanation": "Thor az északi mitológiában a mennydörgés istene, Odin fia."
        },
        {
            "question": "Ki az északi mitológiában a csalárdság istene? (Loki - a trükkös isten, aki gyakran bajt okoz az isteneknek)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 2,
            "explanation": "Loki az északi mitológiában a csalárdság istene, a trükkös isten."
        },
        {
            "question": "Ki az északi mitológiában a szerelem istennője? (Freya - a szerelem és szépség istennője, aki a Valkürök vezetője)",
            "options": ["Frigg", "Freya", "Sif", "Hel"],
            "correct": 1,
            "explanation": "Freya az északi mitológiában a szerelem istennője, a Valkürök vezetője."
        },
        {
            "question": "Ki az északi mitológiában a termékenység istene? (Freyr - a termékenység és béke istene, Freya testvére)",
            "options": ["Thor", "Odin", "Loki", "Freyr"],
            "correct": 3,
            "explanation": "Freyr az északi mitológiában a termékenység istene, Freya testvére."
        },
        {
            "question": "Ki az északi mitológiában a házasság istennője? (Frigg - Odin felesége, a házasság és anyaság istennője)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 1,
            "explanation": "Frigg az északi mitológiában a házasság istennője, Odin felesége."
        },
        {
            "question": "Ki az északi mitológiában a termékenység istennője? (Sif - Thor felesége, aranyhajú istennő)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 2,
            "explanation": "Sif az északi mitológiában a termékenység istennője, Thor felesége."
        },
        {
            "question": "Ki az északi mitológiában a halál istennője? (Hel - a halottak istennője, Loki lánya, aki az alvilágban uralkodik)",
            "options": ["Freya", "Frigg", "Sif", "Hel"],
            "correct": 3,
            "explanation": "Hel az északi mitológiában a halál istennője, Loki lánya."
        },
        {
            "question": "Mi az északi mitológiában a világfa neve? (Yggdrasil - a három világot összekötő óriási kőrisfa)",
            "options": ["Bifröst", "Yggdrasil", "Valhalla", "Asgard"],
            "correct": 1,
            "explanation": "Yggdrasil az északi mitológiában a világfa, a három világot összeköti."
        },
        {
            "question": "Mi az északi mitológiában a mennyország neve? (Asgard - az istenek otthona, ahol Odin uralkodik)",
            "options": ["Valhalla", "Asgard", "Midgard", "Helheim"],
            "correct": 1,
            "explanation": "Asgard az északi mitológiában a mennyország, az istenek otthona."
        },
        {
            "question": "Mi az északi mitológiában a harcosok mennyországának neve? (Valhalla - ahol a hősi halott harcosok élnek)",
            "options": ["Asgard", "Valhalla", "Midgard", "Helheim"],
            "correct": 1,
            "explanation": "Valhalla az északi mitológiában a harcosok mennyországa."
        },
        {
            "question": "Mi az északi mitológiában a szivárvány híd neve? (Bifröst - a híd, ami Asgardot köti össze Midgarddal)",
            "options": ["Yggdrasil", "Bifröst", "Valhalla", "Asgard"],
            "correct": 1,
            "explanation": "Bifröst az északi mitológiában a szivárvány híd, ami Asgardot köti össze Midgarddal."
        },
        {
            "question": "Mi az északi mitológiában a föld neve? (Midgard - az emberek világa, a középső világ)",
            "options": ["Asgard", "Valhalla", "Midgard", "Helheim"],
            "correct": 2,
            "explanation": "Midgard az északi mitológiában a föld, az emberek világa."
        },
        {
            "question": "Mi az északi mitológiában az alvilág neve? (Helheim - a halottak világa, ahol Hel uralkodik)",
            "options": ["Valhalla", "Asgard", "Midgard", "Helheim"],
            "correct": 3,
            "explanation": "Helheim az északi mitológiában az alvilág, a halottak világa."
        },
        {
            "question": "Mi az északi mitológiában Thor kalapácsának neve? (Mjölnir - a varázslatos kalapács, ami mindig visszatér Thorhoz)",
            "options": ["Gungnir", "Mjölnir", "Skofnung", "Tyrfing"],
            "correct": 1,
            "explanation": "Mjölnir az északi mitológiában Thor varázslatos kalapácsa."
        },
        {
            "question": "Mi az északi mitológiában Odin lándzsájának neve? (Gungnir - a varázslatos lándzsa, ami soha nem téveszti el a célját)",
            "options": ["Mjölnir", "Gungnir", "Skofnung", "Tyrfing"],
            "correct": 1,
            "explanation": "Gungnir az északi mitológiában Odin varázslatos lándzsája."
        },
        {
            "question": "Ki az északi mitológiában a háború istene? (Tyr - a háború és igazság istene, aki egy kezét feláldozta)",
            "options": ["Thor", "Odin", "Tyr", "Freyr"],
            "correct": 2,
            "explanation": "Tyr az északi mitológiában a háború istene, aki egy kezét feláldozta."
        },
        {
            "question": "Ki az északi mitológiában a tenger istene? (Njord - a tenger és halászat istene, Freyr és Freya apja)",
            "options": ["Thor", "Odin", "Njord", "Freyr"],
            "correct": 2,
            "explanation": "Njord az északi mitológiában a tenger istene, Freyr és Freya apja."
        },
        {
            "question": "Ki az északi mitológiában a bölcsesség istennője? (Saga - a bölcsesség és történetek istennője, Odin társa)",
            "options": ["Freya", "Frigg", "Saga", "Hel"],
            "correct": 2,
            "explanation": "Saga az északi mitológiában a bölcsesség istennője, Odin társa."
        },
        {
            "question": "Mi az északi mitológiában a végítélet napjának neve? (Ragnarök - a világ vége, amikor az istenek és óriások harcolnak)",
            "options": ["Yggdrasil", "Bifröst", "Ragnarök", "Valhalla"],
            "correct": 2,
            "explanation": "Ragnarök az északi mitológiában a végítélet napja, a világ vége."
        },
        {
            "question": "Ki az északi mitológiában a termékenység óriása? (Ymir - az első lény, akiből a világ teremtődött)",
            "options": ["Thor", "Odin", "Loki", "Ymir"],
            "correct": 3,
            "explanation": "Ymir az északi mitológiában a termékenység óriása, az első lény."
        },
        {
            "question": "Ki az északi mitológiában a tűz óriása? (Surtr - a tűz óriása, aki Ragnarökön felégeti a világot)",
            "options": ["Ymir", "Surtr", "Loki", "Hel"],
            "correct": 1,
            "explanation": "Surtr az északi mitológiában a tűz óriása, aki Ragnarökön felégeti a világot."
        },
        {
            "question": "Ki az északi mitológiában a jég óriása? (Hrímthurs - a jég óriásai, akik az északi sarkon élnek)",
            "options": ["Ymir", "Surtr", "Hrímthurs", "Hel"],
            "correct": 2,
            "explanation": "Hrímthurs az északi mitológiában a jég óriásai, akik az északi sarkon élnek."
        },
        {
            "question": "Mi az északi mitológiában a Valkürök szerepe? (A harcosok kiválasztása - a női lények, akik a hősi halottakat Valhallába viszik)",
            "options": ["Az istenek szolgálói", "A harcosok kiválasztása", "A halottak őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Valkürök az északi mitológiában a harcosok kiválasztói, a hősi halottakat Valhallába viszik."
        },
        {
            "question": "Mi az északi mitológiában a Nornok szerepe? (A sors istennői - három nő, akik az emberek sorsát szőrik)",
            "options": ["A harcosok vezetői", "A sors istennői", "A termékenység őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Nornok az északi mitológiában a sors istennői, akik az emberek sorsát szőrik."
        },
        {
            "question": "Mi az északi mitológiában a Dísir szerepe? (A család védőistennői - női lények, akik a családokat védik)",
            "options": ["A harcosok segítői", "A család védőistennői", "A termékenység őrei", "A bölcsesség őrei"],
            "correct": 1,
            "explanation": "A Dísir az északi mitológiában a család védőistennői, akik a családokat védik."
        }
    ],
    "drámák": [
        # Shakespeare drámák
        {
            "question": "Melyik drámában szerepel egy dán herceg, aki bosszút áll apja haláláért? (Hamlet, Ophelia, Polonius, Gertrude)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 0,
            "explanation": "Hamlet - a dán herceg, aki bosszút áll apja haláláért, miután apja szelleme elmondja, hogy bátyja mérgezte meg."
        },
        {
            "question": "Melyik drámában szerepel egy skót tábornok, aki király akar lenni? (Macbeth, Lady Macbeth, Banquo, Macduff)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 1,
            "explanation": "Macbeth - a skót tábornok, aki a három boszorkány jóslata miatt meggyilkolja a királyt, hogy király legyen."
        },
        {
            "question": "Melyik drámában szerepel egy mór tábornok, aki féltékeny feleségére? (Othello, Desdemona, Iago, Cassio)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 2,
            "explanation": "Othello - a mór tábornok, aki Iago manipulálására féltékeny lesz és megfojtja feleségét, Desdemonát."
        },
        {
            "question": "Melyik drámában szerepel egy király, aki három lányának osztja országát? (King Lear, Goneril, Regan, Cordelia)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 3,
            "explanation": "King Lear - a király, aki három lányának osztja országát, de csak a legkisebb, Cordelia mondja meg az igazat."
        },
        {
            "question": "Melyik drámában szerepel két szerelmes, akik családjuk ellenségeskedése miatt nem lehetnek együtt? (Romeo, Júlia, Mercutio, Tybalt)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 0,
            "explanation": "Romeo és Júlia - a két szerelmes, akik a Capulet és Montague családok ellenségeskedése miatt nem lehetnek együtt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában menekül az erdőbe? (Rosalind, Orlando, Celia, Jacques)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 2,
            "explanation": "Ahogy tetszik - Rosalind, aki férfi ruhában menekül az erdőbe, miután elűzték a udvarból."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában szolgál egy hercegnél? (Viola, Orsino, Olivia, Sebastian)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 3,
            "explanation": "Vízkereszt - Viola, aki férfi ruhában szolgál Orsino hercegnél, miután hajótörést szenvedett."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki férfi ruhában védi barátját a bíróságon? (Portia, Bassanio, Antonio, Shylock)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 1,
            "explanation": "Szeget szeggel - Portia, aki férfi ruhában védi Bassanio barátját a bíróságon."
        },
        {
            "question": "Melyik drámában szerepel egy király, aki három boszorkánytól kap jóslatot? (Macbeth, Lady Macbeth, Banquo, Macduff)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 1,
            "explanation": "Macbeth - a király, aki a három boszorkánytól kap jóslatot, hogy király lesz."
        },
        {
            "question": "Melyik drámában szerepel egy herceg, aki 'Lenni vagy nem lenni' monológot mond? (Hamlet, Ophelia, Polonius, Gertrude)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 0,
            "explanation": "Hamlet - a herceg, aki a híres 'Lenni vagy nem lenni' monológot mondja a halálról és a cselekvésről."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki álomba hullatja magát, hogy meghaljon? (Júlia, Romeo, Mercutio, Tybalt)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 0,
            "explanation": "Romeo és Júlia - Júlia álomba hullatja magát, hogy meghaljon, de Romeo nem tudja és megmérgezi magát."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki három ládikából választ? (Portia, Bassanio, Antonio, Shylock)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 1,
            "explanation": "Szeget szeggel - Portia, aki három ládikából választ: arany, ezüst, ólom, és csak az ólomban van a kép."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki ikerhúga után kutat? (Viola, Sebastian, Orsino, Olivia)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 3,
            "explanation": "Vízkereszt - Viola, aki ikerhúga, Sebastian után kutat, miután hajótörést szenvedett."
        },
        {
            "question": "Melyik drámában szerepel egy férfi, aki 'A világ egy színház' monológot mond? (Jacques, Rosalind, Orlando, Celia)",
            "options": ["Romeo és Júlia", "Szeget szeggel", "Ahogy tetszik", "Vízkereszt"],
            "correct": 2,
            "explanation": "Ahogy tetszik - Jacques, aki a híres 'A világ egy színház' monológot mondja."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki 'Minden világos' monológot mond? (Cordelia, King Lear, Goneril, Regan)",
            "options": ["Hamlet", "Macbeth", "Othello", "King Lear"],
            "correct": 3,
            "explanation": "King Lear - Cordelia, aki a 'Minden világos' monológot mondja apjának."
        },
        # Csehov drámák
        {
            "question": "Melyik drámában szerepel egy család, aki a cseresznyéskert eladását tervezi? (Ranevszkaja, Lopahin, Trofimov, Várya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - a Ranevszkaja család, aki a cseresznyéskert eladását tervezi, mert nincs pénzük."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal író, aki szerelmes egy nőbe? (Treplev, Nina Zarecsnaja, Trigorin, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Treplev, aki szerelmes Nina Zarecsnajába, de Nina Trigorin íróba szerelmes."
        },
        {
            "question": "Melyik drámában szerepel három nővér, akik Moszkvába akarnak költözni? (Olga, Mása, Irina, Versinyin)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Olga, Mása és Irina, akik Moszkvába akarnak költözni, de soha nem jutnak el oda."
        },
        {
            "question": "Melyik drámában szerepel egy férfi, aki szerelmes sógorába? (Ványa bácsi, Jelena, Asztrov, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Ványa bácsi, aki szerelmes Jelena sógorába, de Jelena nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal színésznő, aki szerelmes egy íróba? (Nina Zarecsnaja, Trigorin, Treplev, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Nina Zarecsnaja, aki szerelmes Trigorin íróba, de Trigorin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy orvosba? (Mása, Versinyin, Olga, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Mása, aki szerelmes Versinyin orvosba, de Versinyin feleségével él."
        },
        {
            "question": "Melyik drámában szerepel egy üzletember, aki szerelmes egy nőbe? (Lopahin, Várya, Ranevszkaja, Trofimov)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Lopahin, aki szerelmes Váryába, de Várya nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy lány, aki szerelmes egy orvosba? (Szonya, Asztrov, Ványa bácsi, Jelena)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Szonya, aki szerelmes Asztrov orvosba, de Asztrov nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy báróba? (Irina, Tusenbach, Mása, Olga)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Irina, aki szerelmes Tusenbach báróba, de Tusenbach meghal a párbajban."
        },
        {
            "question": "Melyik drámában szerepel egy színésznő, aki szerelmes egy íróba? (Arkagyina, Trigorin, Nina Zarecsnaja, Treplev)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Arkagyina, aki szerelmes Trigorin íróba, de Trigorin Nina Zarecsnajába szerelmes."
        },
        {
            "question": "Melyik drámában szerepel egy diák, aki szerelmes egy lányba? (Trofimov, Anja, Ranevszkaja, Lopahin)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Trofimov, aki szerelmes Anjába, de Anja nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy orvos, aki szerelmes egy nőbe? (Asztrov, Jelena, Ványa bácsi, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Asztrov, aki szerelmes Jelena sógorába, de Jelena nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy katonatiszt, aki szerelmes egy nőbe? (Versinyin, Mása, Olga, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Versinyin, aki szerelmes Mása nővérébe, de Mása férjével él."
        },
        {
            "question": "Melyik drámában szerepel egy író, aki szerelmes egy fiatal nőbe? (Trigorin, Nina Zarecsnaja, Arkagyina, Treplev)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Trigorin, aki szerelmes Nina Zarecsnajába, de Nina nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy lány, aki szerelmes egy üzletemberbe? (Várya, Lopahin, Ranevszkaja, Trofimov)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 0,
            "explanation": "A cseresznyéskert - Várya, aki szerelmes Lopahinba, de Lopahin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy orvosba? (Jelena, Asztrov, Ványa bácsi, Szonya)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 1,
            "explanation": "Ványa bácsi - Jelena, aki szerelmes Asztrov orvosba, de Asztrov nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy nő, aki szerelmes egy tanárba? (Olga, Kuligin, Mása, Irina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 2,
            "explanation": "Három nővér - Olga, aki szerelmes Kuliginba, de Kuligin nem szereti őt."
        },
        {
            "question": "Melyik drámában szerepel egy fiatal nő, aki szerelmes egy íróba? (Nina Zarecsnaja, Treplev, Trigorin, Arkagyina)",
            "options": ["A cseresznyéskert", "Ványa bácsi", "Három nővér", "A sirály"],
            "correct": 3,
            "explanation": "A sirály - Nina Zarecsnaja, aki szerelmes Treplevba, de Treplev nem szereti őt."
        }
    ],
    "állatok": [
        {
            "question": "Mi az okapi rokonsági foka?",
            "options": ["Zsiráf rokona", "Zebra rokona", "Antilop rokona", "Ló rokona"],
            "correct": 0,
            "explanation": "Az okapi afrikai állat, amely a zsiráf rokona."
        },
        {
            "question": "Hol él a tüskés ördög?",
            "options": ["Afrika", "Ázsia", "Dél-Amerika", "Ausztrália"],
            "correct": 3,
            "explanation": "A tüskés ördög egy ausztrál hüllő."
        },
        {
            "question": "Mi a kacsafarkú szender?",
            "options": ["Madár", "Emlős", "Hüllő", "Rovar lepke-szender"],
            "correct": 3,
            "explanation": "A kacsafarkú szender egy rovar lepke-szender."
        },
        {
            "question": "Milyen állat az axolotl?",
            "options": ["Hüllő", "Hal", "Kétéltű", "Emlős"],
            "correct": 2,
            "explanation": "Az axolotl egy kétéltű állat."
        },
        {
            "question": "Mi a binturong másik neve?",
            "options": ["Pálmasodró cibetmacska", "Himalájai macska", "Erdei macska", "Vaddisznó"],
            "correct": 0,
            "explanation": "A binturong más néven pálmasodró cibetmacska."
        },
        {
            "question": "Hol élt a tarpán?",
            "options": ["Afrika", "Amerika", "Eurázsia", "Ausztrália"],
            "correct": 2,
            "explanation": "A tarpán egy eurázsiai vadló volt."
        },
        {
            "question": "Hol található a csillagorrú vakond?",
            "options": ["USA", "Kanada", "Mexikó", "Grönland"],
            "correct": 0,
            "explanation": "A csillagorrú vakond az USA-ban található."
        },
        {
            "question": "Mi a quokka teljes neve?",
            "options": ["Rövid farkú oposszum", "Kis válú medve", "Kurtafarkú kenguru", "Törpe antilop"],
            "correct": 2,
            "explanation": "A quokka kurtafarkú kenguru."
        },
        {
            "question": "Hol él a takin?",
            "options": ["Alpok", "Andok", "Kaukázus", "Himalája"],
            "correct": 3,
            "explanation": "A takin egy himalájai antilop."
        },
        {
            "question": "Hol található az ocelot?",
            "options": ["Észak-Amerika", "Afrika", "Ázsia", "Dél-Amerika"],
            "correct": 3,
            "explanation": "Az ocelot Dél-Amerikában található."
        }
    ],
    "us_államok": [
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/AL.png",
            "options": ["Alabama", "Alaska", "Arizona", "Arkansas"],
            "correct": 0,
            "explanation": "Ez Alabama állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/AK.png",
            "options": ["Alabama", "Alaska", "Arizona", "Arkansas"],
            "correct": 1,
            "explanation": "Ez Alaska állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/AZ.png",
            "options": ["Alabama", "Alaska", "Arizona", "Arkansas"],
            "correct": 2,
            "explanation": "Ez Arizona állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/AR.png",
            "options": ["Alabama", "Alaska", "Arizona", "Arkansas"],
            "correct": 3,
            "explanation": "Ez Arkansas állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/CA.png",
            "options": ["California", "Colorado", "Connecticut", "Delaware"],
            "correct": 0,
            "explanation": "Ez California állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/CO.png",
            "options": ["California", "Colorado", "Connecticut", "Delaware"],
            "correct": 1,
            "explanation": "Ez Colorado állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/CT.png",
            "options": ["California", "Colorado", "Connecticut", "Delaware"],
            "correct": 2,
            "explanation": "Ez Connecticut állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/DE.png",
            "options": ["California", "Colorado", "Connecticut", "Delaware"],
            "correct": 3,
            "explanation": "Ez Delaware állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/FL.png",
            "options": ["Florida", "Georgia", "Hawaii", "Idaho"],
            "correct": 0,
            "explanation": "Ez Florida állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/GA.png",
            "options": ["Florida", "Georgia", "Hawaii", "Idaho"],
            "correct": 1,
            "explanation": "Ez Georgia állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/HI.png",
            "options": ["Florida", "Georgia", "Hawaii", "Idaho"],
            "correct": 2,
            "explanation": "Ez Hawaii állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/ID.png",
            "options": ["Florida", "Georgia", "Hawaii", "Idaho"],
            "correct": 3,
            "explanation": "Ez Idaho állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/IL.png",
            "options": ["Illinois", "Indiana", "Iowa", "Kansas"],
            "correct": 0,
            "explanation": "Ez Illinois állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/IN.png",
            "options": ["Illinois", "Indiana", "Iowa", "Kansas"],
            "correct": 1,
            "explanation": "Ez Indiana állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/IA.png",
            "options": ["Illinois", "Indiana", "Iowa", "Kansas"],
            "correct": 2,
            "explanation": "Ez Iowa állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/KS.png",
            "options": ["Illinois", "Indiana", "Iowa", "Kansas"],
            "correct": 3,
            "explanation": "Ez Kansas állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/KY.png",
            "options": ["Kentucky", "Louisiana", "Maine", "Maryland"],
            "correct": 0,
            "explanation": "Ez Kentucky állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/LA.png",
            "options": ["Kentucky", "Louisiana", "Maine", "Maryland"],
            "correct": 1,
            "explanation": "Ez Louisiana állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/ME.png",
            "options": ["Kentucky", "Louisiana", "Maine", "Maryland"],
            "correct": 2,
            "explanation": "Ez Maine állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MD.png",
            "options": ["Kentucky", "Louisiana", "Maine", "Maryland"],
            "correct": 3,
            "explanation": "Ez Maryland állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MA.png",
            "options": ["Massachusetts", "Michigan", "Minnesota", "Mississippi"],
            "correct": 0,
            "explanation": "Ez Massachusetts állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MI.png",
            "options": ["Massachusetts", "Michigan", "Minnesota", "Mississippi"],
            "correct": 1,
            "explanation": "Ez Michigan állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MN.png",
            "options": ["Massachusetts", "Michigan", "Minnesota", "Mississippi"],
            "correct": 2,
            "explanation": "Ez Minnesota állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MS.png",
            "options": ["Massachusetts", "Michigan", "Minnesota", "Mississippi"],
            "correct": 3,
            "explanation": "Ez Mississippi állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MO.png",
            "options": ["Missouri", "Montana", "Nebraska", "Nevada"],
            "correct": 0,
            "explanation": "Ez Missouri állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/MT.png",
            "options": ["Missouri", "Montana", "Nebraska", "Nevada"],
            "correct": 1,
            "explanation": "Ez Montana állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NE.png",
            "options": ["Missouri", "Montana", "Nebraska", "Nevada"],
            "correct": 2,
            "explanation": "Ez Nebraska állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NV.png",
            "options": ["Missouri", "Montana", "Nebraska", "Nevada"],
            "correct": 3,
            "explanation": "Ez Nevada állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NH.png",
            "options": ["New Hampshire", "New Jersey", "New Mexico", "New York"],
            "correct": 0,
            "explanation": "Ez New Hampshire állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NJ.png",
            "options": ["New Hampshire", "New Jersey", "New Mexico", "New York"],
            "correct": 1,
            "explanation": "Ez New Jersey állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NM.png",
            "options": ["New Hampshire", "New Jersey", "New Mexico", "New York"],
            "correct": 2,
            "explanation": "Ez New Mexico állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NY.png",
            "options": ["New Hampshire", "New Jersey", "New Mexico", "New York"],
            "correct": 3,
            "explanation": "Ez New York állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/NC.png",
            "options": ["North Carolina", "North Dakota", "Ohio", "Oklahoma"],
            "correct": 0,
            "explanation": "Ez North Carolina állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/ND.png",
            "options": ["North Carolina", "North Dakota", "Ohio", "Oklahoma"],
            "correct": 1,
            "explanation": "Ez North Dakota állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/OH.png",
            "options": ["North Carolina", "North Dakota", "Ohio", "Oklahoma"],
            "correct": 2,
            "explanation": "Ez Ohio állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/OK.png",
            "options": ["North Carolina", "North Dakota", "Ohio", "Oklahoma"],
            "correct": 3,
            "explanation": "Ez Oklahoma állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/OR.png",
            "options": ["Oregon", "Pennsylvania", "Rhode Island", "South Carolina"],
            "correct": 0,
            "explanation": "Ez Oregon állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/PA.png",
            "options": ["Oregon", "Pennsylvania", "Rhode Island", "South Carolina"],
            "correct": 1,
            "explanation": "Ez Pennsylvania állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/RI.png",
            "options": ["Oregon", "Pennsylvania", "Rhode Island", "South Carolina"],
            "correct": 2,
            "explanation": "Ez Rhode Island állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/SC.png",
            "options": ["Oregon", "Pennsylvania", "Rhode Island", "South Carolina"],
            "correct": 3,
            "explanation": "Ez South Carolina állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/SD.png",
            "options": ["South Dakota", "Tennessee", "Texas", "Utah"],
            "correct": 0,
            "explanation": "Ez South Dakota állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/TN.png",
            "options": ["South Dakota", "Tennessee", "Texas", "Utah"],
            "correct": 1,
            "explanation": "Ez Tennessee állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/TX.png",
            "options": ["South Dakota", "Tennessee", "Texas", "Utah"],
            "correct": 2,
            "explanation": "Ez Texas állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/UT.png",
            "options": ["South Dakota", "Tennessee", "Texas", "Utah"],
            "correct": 3,
            "explanation": "Ez Utah állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/VA.png",
            "options": ["Virginia", "Vermont", "Washington", "Wisconsin"],
            "correct": 0,
            "explanation": "Ez Virginia állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/VT.png",
            "options": ["Virginia", "Vermont", "Washington", "Wisconsin"],
            "correct": 1,
            "explanation": "Ez Vermont állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/WA.png",
            "options": ["Virginia", "Vermont", "Washington", "Wisconsin"],
            "correct": 2,
            "explanation": "Ez Washington állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/WI.png",
            "options": ["Virginia", "Vermont", "Washington", "Wisconsin"],
            "correct": 3,
            "explanation": "Ez Wisconsin állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/WV.png",
            "options": ["West Virginia", "Wyoming", "District of Columbia", "Puerto Rico"],
            "correct": 0,
            "explanation": "Ez West Virginia állam címere."
        },
        {
            "question": "Ez a címere melyik amerikai államhoz tartozik?",
            "logo_path": "../us_state_seals/WY.png",
            "options": ["West Virginia", "Wyoming", "District of Columbia", "Puerto Rico"],
            "correct": 1,
            "explanation": "Ez Wyoming állam címere."
        }
    ],
    "magyar_királyok": [
        {
            "question": "Ki volt Magyarország első királya (1000-1038)?",
            "options": ["Szent István", "Szent László", "Kálmán", "II. András"],
            "correct": 0,
            "explanation": "Szent István (1000-1038) volt Magyarország első királya, aki keresztény hitre térítette az országot."
        },
        {
            "question": "Melyik király uralkodott 1077-1095 között és szentté avatták?",
            "options": ["Szent István", "Szent László", "Kálmán", "II. Béla"],
            "correct": 1,
            "explanation": "Szent László (1077-1095) volt a király, aki törvénykezéssel és hadjáratokkal erősítette meg az országot."
        },
        {
            "question": "Ki volt a 'Könyves' király (1095-1116)?",
            "options": ["Szent László", "Kálmán", "II. István", "II. Géza"],
            "correct": 1,
            "explanation": "Kálmán (1095-1116) volt a 'Könyves' király, aki törvénykezéssel és diplomáciával tette híressé nevét."
        },
        {
            "question": "Melyik király uralkodott 1131-1141 között és 'Vak' néven ismert?",
            "options": ["II. István", "II. Géza", "II. Béla", "III. István"],
            "correct": 2,
            "explanation": "II. Béla (1131-1141) volt a 'Vak' király, aki a bizánci császár fogságában megvakult."
        },
        {
            "question": "Ki volt a 'Kálmán fia' király (1141-1162)?",
            "options": ["II. Géza", "III. István", "II. László", "III. Béla"],
            "correct": 0,
            "explanation": "II. Géza (1141-1162) volt a 'Kálmán fia' király, aki békés uralkodást folytatott."
        },
        {
            "question": "Melyik király uralkodott 1162-1172 között és 'Kálmán unokája' volt?",
            "options": ["III. István", "II. László", "III. Béla", "II. Imre"],
            "correct": 0,
            "explanation": "III. István (1162-1172) volt a 'Kálmán unokája' király, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Ki volt a 'Szent' király (1172-1196)?",
            "options": ["II. László", "III. Béla", "II. Imre", "III. László"],
            "correct": 1,
            "explanation": "III. Béla (1172-1196) volt a 'Szent' király, aki törvénykezéssel és építkezéssel tette híressé nevét."
        },
        {
            "question": "Melyik király uralkodott 1196-1204 között és 'Jeruzsálemi' néven ismert?",
            "options": ["II. Imre", "III. László", "II. András", "IV. Béla"],
            "correct": 0,
            "explanation": "II. Imre (1196-1204) volt a 'Jeruzsálemi' király, aki keresztes hadjáratot vezetett."
        },
        {
            "question": "Ki volt a 'Jeruzsálemi' király fia (1204-1205)?",
            "options": ["III. László", "II. András", "IV. Béla", "III. István"],
            "correct": 0,
            "explanation": "III. László (1204-1205) volt II. Imre fia, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Melyik király uralkodott 1205-1235 között és 'Jeruzsálemi' néven ismert?",
            "options": ["II. András", "IV. Béla", "III. István", "V. István"],
            "correct": 0,
            "explanation": "II. András (1205-1235) volt a 'Jeruzsálemi' király, aki Aranybullát adott ki."
        },
        {
            "question": "Ki volt a 'Kun' király (1235-1270)?",
            "options": ["IV. Béla", "III. István", "V. István", "IV. László"],
            "correct": 0,
            "explanation": "IV. Béla (1235-1270) volt a 'Kun' király, aki a tatárjárás után újjáépítette az országot."
        },
        {
            "question": "Melyik király uralkodott 1270-1272 között és 'Kun' néven ismert?",
            "options": ["III. István", "V. István", "IV. László", "III. András"],
            "correct": 1,
            "explanation": "V. István (1270-1272) volt a 'Kun' király, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Ki volt a 'Kun' király fia (1272-1290)?",
            "options": ["IV. László", "III. András", "V. László", "I. Károly"],
            "correct": 0,
            "explanation": "IV. László (1272-1290) volt a 'Kun' király, aki a kunokkal szövetséget kötött."
        },
        {
            "question": "Melyik király uralkodott 1290-1301 között és 'Veneciai' néven ismert?",
            "options": ["III. András", "V. László", "I. Károly", "I. Lajos"],
            "correct": 0,
            "explanation": "III. András (1290-1301) volt a 'Veneciai' király, az Árpád-ház utolsó tagja."
        },
        {
            "question": "Ki volt az első Anjou király (1301-1342)?",
            "options": ["I. Károly", "I. Lajos", "Mária", "II. Károly"],
            "correct": 0,
            "explanation": "I. Károly (1301-1342) volt az első Anjou király, aki megerősítette a királyi hatalmat."
        },
        {
            "question": "Melyik király uralkodott 1342-1382 között és 'Nagy' néven ismert?",
            "options": ["I. Lajos", "Mária", "II. Károly", "Zsigmond"],
            "correct": 0,
            "explanation": "I. Lajos (1342-1382) volt a 'Nagy' király, aki Dalmáciát és Nápolyt is meghódította."
        },
        {
            "question": "Ki volt a 'Nagy' király lánya (1382-1385, 1386-1395)?",
            "options": ["Mária", "II. Károly", "Zsigmond", "I. Albert"],
            "correct": 0,
            "explanation": "Mária (1382-1385, 1386-1395) volt I. Lajos lánya, aki Luxemburgi Zsigmonddal házasodott."
        },
        {
            "question": "Melyik király uralkodott 1385-1386 között és 'Kis' néven ismert?",
            "options": ["II. Károly", "Zsigmond", "I. Albert", "I. Ulászló"],
            "correct": 0,
            "explanation": "II. Károly (1385-1386) volt a 'Kis' király, aki rövid uralkodás után meggyilkolták."
        },
        {
            "question": "Ki volt a 'Luxemburgi' király (1387-1437)?",
            "options": ["Zsigmond", "I. Albert", "I. Ulászló", "II. Ulászló"],
            "correct": 0,
            "explanation": "Zsigmond (1387-1437) volt a 'Luxemburgi' király, aki német-római császár is volt."
        },
        {
            "question": "Melyik király uralkodott 1437-1439 között és 'Német' néven ismert?",
            "options": ["I. Albert", "I. Ulászló", "II. Ulászló", "I. Mátyás"],
            "correct": 0,
            "explanation": "I. Albert (1437-1439) volt a 'Német' király, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Ki volt a 'Lengyel' király (1440-1444)?",
            "options": ["I. Ulászló", "II. Ulászló", "I. Mátyás", "II. Lajos"],
            "correct": 0,
            "explanation": "I. Ulászló (1440-1444) volt a 'Lengyel' király, aki a várnai csatában esett el."
        },
        {
            "question": "Melyik király uralkodott 1444-1490 között és 'Hunyadi' néven ismert?",
            "options": ["I. Mátyás", "II. Lajos", "II. Ulászló", "I. Ferdinánd"],
            "correct": 0,
            "explanation": "I. Mátyás (1444-1490) volt a 'Hunyadi' király, aki reneszánsz udvart tartott."
        },
        {
            "question": "Ki volt a 'Jagelló' király (1490-1516)?",
            "options": ["II. Ulászló", "II. Lajos", "I. Ferdinánd", "I. János"],
            "correct": 0,
            "explanation": "II. Ulászló (1490-1516) volt a 'Jagelló' király, aki a Jagelló-házból származott."
        },
        {
            "question": "Melyik király uralkodott 1516-1526 között és 'Jagelló' néven ismert?",
            "options": ["II. Lajos", "I. Ferdinánd", "I. János", "I. Miksa"],
            "correct": 0,
            "explanation": "II. Lajos (1516-1526) volt a 'Jagelló' király, aki a mohácsi csatában esett el."
        },
        {
            "question": "Ki volt a 'Habsburg' király (1526-1564)?",
            "options": ["I. Ferdinánd", "I. János", "I. Miksa", "II. Rudolf"],
            "correct": 0,
            "explanation": "I. Ferdinánd (1526-1564) volt a 'Habsburg' király, aki a Habsburg-ház alapítója Magyarországon."
        },
        {
            "question": "Melyik király uralkodott 1540-1570 között és 'Szapolyai' néven ismert?",
            "options": ["I. János", "I. Miksa", "II. Rudolf", "I. Mátyás"],
            "correct": 0,
            "explanation": "I. János (1540-1570) volt a 'Szapolyai' király, aki Erdély fejedelme is volt."
        },
        {
            "question": "Ki volt a 'Habsburg' király fia (1564-1576)?",
            "options": ["I. Miksa", "II. Rudolf", "I. Mátyás", "II. Ferdinánd"],
            "correct": 0,
            "explanation": "I. Miksa (1564-1576) volt I. Ferdinánd fia, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Melyik király uralkodott 1576-1608 között és 'Habsburg' néven ismert?",
            "options": ["II. Rudolf", "I. Mátyás", "II. Ferdinánd", "III. Ferdinánd"],
            "correct": 0,
            "explanation": "II. Rudolf (1576-1608) volt a 'Habsburg' király, aki Prágában élt."
        },
        {
            "question": "Ki volt a 'Habsburg' király testvére (1608-1619)?",
            "options": ["I. Mátyás", "II. Ferdinánd", "III. Ferdinánd", "II. Rudolf"],
            "correct": 0,
            "explanation": "I. Mátyás (1608-1619) volt II. Rudolf testvére, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Melyik király uralkodott 1619-1637 között és 'Habsburg' néven ismert?",
            "options": ["II. Ferdinánd", "III. Ferdinánd", "I. Lipót", "I. József"],
            "correct": 0,
            "explanation": "II. Ferdinánd (1619-1637) volt a 'Habsburg' király, aki a harmincéves háborúban uralkodott."
        },
        {
            "question": "Ki volt a 'Habsburg' király fia (1637-1657)?",
            "options": ["III. Ferdinánd", "I. Lipót", "I. József", "I. Károly"],
            "correct": 0,
            "explanation": "III. Ferdinánd (1637-1657) volt II. Ferdinánd fia, aki a harmincéves háború után uralkodott."
        },
        {
            "question": "Melyik király uralkodott 1657-1705 között és 'Habsburg' néven ismert?",
            "options": ["I. Lipót", "I. József", "I. Károly", "Mária Terézia"],
            "correct": 0,
            "explanation": "I. Lipót (1657-1705) volt a 'Habsburg' király, aki a török elleni háborúkban uralkodott."
        },
        {
            "question": "Ki volt a 'Habsburg' király fia (1705-1711)?",
            "options": ["I. József", "I. Károly", "Mária Terézia", "II. József"],
            "correct": 0,
            "explanation": "I. József (1705-1711) volt I. Lipót fia, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Melyik király uralkodott 1711-1740 között és 'Habsburg' néven ismert?",
            "options": ["I. Károly", "Mária Terézia", "II. József", "I. Ferenc"],
            "correct": 0,
            "explanation": "I. Károly (1711-1740) volt a 'Habsburg' király, aki a pragmatikus szankciót hirdette ki."
        },
        {
            "question": "Ki volt a 'Habsburg' király lánya (1740-1780)?",
            "options": ["Mária Terézia", "II. József", "I. Ferenc", "II. Lipót"],
            "correct": 0,
            "explanation": "Mária Terézia (1740-1780) volt a 'Habsburg' királynő, aki reformokat vezetett be."
        },
        {
            "question": "Melyik király uralkodott 1780-1790 között és 'Habsburg' néven ismert?",
            "options": ["II. József", "I. Ferenc", "II. Lipót", "I. Ferenc József"],
            "correct": 0,
            "explanation": "II. József (1780-1790) volt a 'Habsburg' király, aki felvilágosult abszolutizmust vezetett be."
        },
        {
            "question": "Ki volt a 'Habsburg' király testvére (1790-1792)?",
            "options": ["I. Ferenc", "II. Lipót", "I. Ferenc József", "II. Ferenc József"],
            "correct": 0,
            "explanation": "I. Ferenc (1790-1792) volt II. József testvére, aki rövid uralkodás után meghalt."
        },
        {
            "question": "Melyik király uralkodott 1792-1835 között és 'Habsburg' néven ismert?",
            "options": ["II. Lipót", "I. Ferenc József", "II. Ferenc József", "I. Károly"],
            "correct": 0,
            "explanation": "II. Lipót (1792-1835) volt a 'Habsburg' király, aki a napóleoni háborúkban uralkodott."
        },
        {
            "question": "Ki volt a 'Habsburg' király fia (1835-1848)?",
            "options": ["I. Ferenc József", "II. Ferenc József", "I. Károly", "IV. Károly"],
            "correct": 0,
            "explanation": "I. Ferenc József (1835-1848) volt II. Lipót fia, aki a reformkorban uralkodott."
        },
        {
            "question": "Melyik király uralkodott 1848-1916 között és 'Habsburg' néven ismert?",
            "options": ["I. Ferenc József", "II. Ferenc József", "I. Károly", "IV. Károly"],
            "correct": 0,
            "explanation": "I. Ferenc József (1848-1916) volt a 'Habsburg' király, aki 68 évig uralkodott."
        },
        {
            "question": "Ki volt a 'Habsburg' király unokája (1916-1918)?",
            "options": ["II. Ferenc József", "I. Károly", "IV. Károly", "II. Károly"],
            "correct": 0,
            "explanation": "II. Ferenc József (1916-1918) volt I. Ferenc József unokája, az utolsó magyar király."
        }
    ],
    "háborúk": HABORU_QUESTIONS,
        {
            "question": "Melyik háború zajlott 1454-1466 között? (Porosz Konföderáció, Lengyel Királyság vs Teuton Lovagrend)",
            "options": ["Tizenhárom éves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Tizenhárom éves háború (1454-1466): Porosz Konföderáció, Lengyel Királyság vs Teuton Lovagrend"
        },
        {
            "question": "Melyik háború zajlott 1618-1648 között? (Katolikus Habsburgok, Spanyolország vs Protestáns államok, Franciaország, Svédország)",
            "options": ["Harmincéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Harmincéves háború (1618-1648): Katolikus Habsburgok, Spanyolország vs Protestáns államok, Franciaország, Svédország"
        },
        {
            "question": "Melyik háború zajlott 1701-1714 között? (Franciaország, Spanyolország vs Ausztria, Nagy-Britannia, Hollandia)",
            "options": ["Spanyol örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Spanyol örökösödési háború (1701-1714): Franciaország, Spanyolország vs Ausztria, Nagy-Britannia, Hollandia"
        },
        {
            "question": "Melyik háború zajlott 1740-1748 között? (Ausztria vs Poroszország, Franciaország, Spanyolország)",
            "options": ["Osztrák örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Osztrák örökösödési háború (1740-1748): Ausztria vs Poroszország, Franciaország, Spanyolország"
        },
        {
            "question": "Melyik háború zajlott 1756-1763 között? (Nagy-Britannia, Poroszország vs Franciaország, Ausztria, Oroszország)",
            "options": ["Hétéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Hétéves háború (1756-1763): Nagy-Britannia, Poroszország vs Franciaország, Ausztria, Oroszország"
        },
        {
            "question": "Melyik háború zajlott 1803-1815 között? (Napóleoni Franciaország vs Európai szövetséges hatalmak)",
            "options": ["Napóleoni háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Napóleoni háborúk (1803-1815): Napóleoni Franciaország vs Európai szövetséges hatalmak"
        },
        {
            "question": "Melyik háború zajlott 1808-1809 között? (Svédország vs Orosz Birodalom)",
            "options": ["Finn háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Finn háború (1808-1809): Svédország vs Orosz Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1821-1829 között? (Görög felkelők vs Oszmán Birodalom)",
            "options": ["Görög függetlenségi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Görög függetlenségi háború (1821-1829): Görög felkelők vs Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1853-1856 között? (Oroszország vs Oszmán Birodalom, Egyesült Királyság, Franciaország, Szardínia)",
            "options": ["Krími háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Krími háború (1853-1856): Oroszország vs Oszmán Birodalom, Egyesült Királyság, Franciaország, Szardínia"
        },
        {
            "question": "Melyik háború zajlott 1912-1913 között? (Balkán Liga vs Oszmán Birodalom)",
            "options": ["Első Balkán-háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Első Balkán-háború (1912-1913): Balkán Liga vs Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1913 között? (Bulgária vs volt szövetségesei)",
            "options": ["Második Balkán-háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Második Balkán-háború (1913): Bulgária vs volt szövetségesei"
        },
        {
            "question": "Melyik háború zajlott 1914-1918 között? (Központi hatalmak vs Antant)",
            "options": ["Első világháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Első világháború (1914-1918): Központi hatalmak vs Antant"
        },
        {
            "question": "Melyik háború zajlott 1936-1939 között? (Köztársaságiak vs Franco tábornok nemzeti erői)",
            "options": ["Spanyol polgárháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Spanyol polgárháború (1936-1939): Köztársaságiak vs Franco tábornok nemzeti erői"
        },
        {
            "question": "Melyik háború zajlott 1939-1945 között? (Tengelyhatalmak vs Szövetségesek)",
            "options": ["Második világháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Második világháború (1939-1945): Tengelyhatalmak vs Szövetségesek"
        },
        {
            "question": "Melyik háború zajlott 1337-1453 között? (Angol Királyság vs. Francia Királyság)",
            "options": ["Százéves háború (első szakasz)", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Százéves háború (első szakasz) (1337-1453): Angol Királyság vs. Francia Királyság"
        },
        {
            "question": "Melyik háború zajlott 1341-1364 között? (Montfort-ház vs. Blois-ház)",
            "options": ["Bretagne-i örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Bretagne-i örökösödési háború (1341-1364): Montfort-ház vs. Blois-ház"
        },
        {
            "question": "Melyik háború zajlott 1375-1378 között? (Pápai Állam vs. Firenze, Milánó, Siena)",
            "options": ["Nyolc Szent háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Nyolc Szent háborúja (1375-1378): Pápai Állam vs. Firenze, Milánó, Siena"
        },
        {
            "question": "Melyik háború zajlott 1332-1357 között? (Skót Királyság vs. Angol Királyság)",
            "options": ["Második skót függetlenségi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Második skót függetlenségi háború (1332-1357): Skót Királyság vs. Angol Királyság"
        },
        {
            "question": "Melyik háború zajlott 14. sz. második fele között? (Bolgár Birodalmak vs. Oszmán Birodalom)",
            "options": ["Bolgár–török háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Bolgár–török háborúk (14. sz. második fele): Bolgár Birodalmak vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 14. század között? (Bizánci Birodalom vs. Oszmán Birodalom)",
            "options": ["Bizánci–török háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Bizánci–török háborúk (14. század): Bizánci Birodalom vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1356-1375 között? (Kasztíliai Királyság vs. Aragóniai Királyság)",
            "options": ["Két Péter háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Két Péter háborúja (1356-1375): Kasztíliai Királyság vs. Aragóniai Királyság"
        },
        {
            "question": "Melyik háború zajlott 1381 között? (Angol parasztság vs. Angol Királyság)",
            "options": ["Angol parasztlázadás", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Angol parasztlázadás (1381): Angol parasztság vs. Angol Királyság"
        },
        {
            "question": "Melyik háború zajlott 1396 között? (Keresztes hadsereg vs. Oszmán Birodalom)",
            "options": ["Nikápolyi csata", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Nikápolyi csata (1396): Keresztes hadsereg vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1419-1434/36 között? (Husziták vs. Német-római Birodalom)",
            "options": ["Huszita háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Huszita háborúk (1419-1434/36): Husziták vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1455-1485/87 között? (Lancaster-ház vs. York-ház)",
            "options": ["Rózsák háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Rózsák háborúja (1455-1485/87): Lancaster-ház vs. York-ház"
        },
        {
            "question": "Melyik háború zajlott 1454-1466 között? (Lengyel Királyság & Porosz Konföderáció vs. Német Lovagrend)",
            "options": ["Tizenhárom éves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Tizenhárom éves háború (1454-1466): Lengyel Királyság & Porosz Konföderáció vs. Német Lovagrend"
        },
        {
            "question": "Melyik háború zajlott 15. század között? (Magyar Királyság vs. Oszmán Birodalom)",
            "options": ["Oszmán–magyar háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Oszmán–magyar háborúk (15. század): Magyar Királyság vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1463-1479 között? (Velencei Köztársaság vs. Oszmán Birodalom)",
            "options": ["Oszmán–velencei háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Oszmán–velencei háború (1463-1479): Velencei Köztársaság vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1474-1477 között? (Burgundiai Állam vs. Ósvájci Konföderáció)",
            "options": ["Burgundiai háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Burgundiai háborúk (1474-1477): Burgundiai Állam vs. Ósvájci Konföderáció"
        },
        {
            "question": "Melyik háború zajlott 1482-1492 között? (Kasztíliai Királyság és Aragóniai Királyság vs. Granadai Emirátus)",
            "options": ["Granadai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Granadai háború (1482-1492): Kasztíliai Királyság és Aragóniai Királyság vs. Granadai Emirátus"
        },
        {
            "question": "Melyik háború zajlott 1494-1498 között? (Franciaország vs. Velencei Liga)",
            "options": ["Itáliai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Itáliai háború (1494-1498): Franciaország vs. Velencei Liga"
        },
        {
            "question": "Melyik háború zajlott 1475-1479 között? (I. Izabella támogatói vs. Johanna la Beltraneja támogatói)",
            "options": ["Kasztíliai örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Kasztíliai örökösödési háború (1475-1479): I. Izabella támogatói vs. Johanna la Beltraneja támogatói"
        },
        {
            "question": "Melyik háború zajlott 1508-1516 között? (Változó szövetségek: Pápai Állam, Franciaország, Német-római Birodalom)",
            "options": ["Cambrai-i Liga háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Cambrai-i Liga háborúja (1508-1516): Változó szövetségek: Pápai Állam, Franciaország, Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1521-1526 között? (Franciaország & Velence vs. Német-római Birodalom)",
            "options": ["Itáliai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Itáliai háború (1521-1526): Franciaország & Velence vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1526-1530 között? (Franciaország, Pápai Állam, Velence vs. Német-római Birodalom)",
            "options": ["Cognaci Liga háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Cognaci Liga háborúja (1526-1530): Franciaország, Pápai Állam, Velence vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1536-1538 között? (Franciaország & Oszmán Birodalom vs. Német-római Birodalom)",
            "options": ["Itáliai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Itáliai háború (1536-1538): Franciaország & Oszmán Birodalom vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1542-1546 között? (Franciaország & Oszmán Birodalom vs. Német-római Birodalom)",
            "options": ["Itáliai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Itáliai háború (1542-1546): Franciaország & Oszmán Birodalom vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1551-1559 között? (Franciaország & Oszmán Birodalom vs. Német-római Birodalom)",
            "options": ["Itáliai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Itáliai háború (1551-1559): Franciaország & Oszmán Birodalom vs. Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1524-1525 között? (Paraszti seregek vs. Sváb Liga)",
            "options": ["Német parasztháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Német parasztháború (1524-1525): Paraszti seregek vs. Sváb Liga"
        },
        {
            "question": "Melyik háború zajlott 1546-1547, 1552 között? (Schmalkaldeni Szövetség vs. V. Károly)",
            "options": ["Schmalkaldeni háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Schmalkaldeni háború (1546-1547, 1552): Schmalkaldeni Szövetség vs. V. Károly"
        },
        {
            "question": "Melyik háború zajlott 1562-1598 között? (Hugenották vs. Francia katolikusok)",
            "options": ["Francia vallásháborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Francia vallásháborúk (1562-1598): Hugenották vs. Francia katolikusok"
        },
        {
            "question": "Melyik háború zajlott 1566/68-1648 között? (Holland lázadók vs. Spanyol Birodalom)",
            "options": ["Nyolcvanéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Nyolcvanéves háború (1566/68-1648): Holland lázadók vs. Spanyol Birodalom"
        },
        {
            "question": "Melyik háború zajlott 16. század között? (Habsburg Monarchia vs. Oszmán Birodalom)",
            "options": ["Oszmán–Habsburg háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Oszmán–Habsburg háborúk (16. század): Habsburg Monarchia vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1571 között? (Szent Liga vs. Oszmán Birodalom)",
            "options": ["Lepantói csata", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Lepantói csata (1571): Szent Liga vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1558-1583 között? (Orosz Cárság vs. Livóniai Konföderáció)",
            "options": ["Livóniai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Livóniai háború (1558-1583): Orosz Cárság vs. Livóniai Konföderáció"
        },
        {
            "question": "Melyik háború zajlott 1618-1648 között? (Protestáns Unió vs. Katolikus Liga)",
            "options": ["Harmincéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Harmincéves háború (1618-1648): Protestáns Unió vs. Katolikus Liga"
        },
        {
            "question": "Melyik háború zajlott 1611-1613 között? (Dánia-Norvégia vs. Svédország)",
            "options": ["Kalmari háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Kalmari háború (1611-1613): Dánia-Norvégia vs. Svédország"
        },
        {
            "question": "Melyik háború zajlott 1620-1621 között? (Lengyel-Litván Unió & Kozákok vs. Oszmán Birodalom)",
            "options": ["Lengyel–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Lengyel–török háború (1620-1621): Lengyel-Litván Unió & Kozákok vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1639-1653 között? (Angol királypártiak vs. Angol parlamentaristák)",
            "options": ["A három királyság háborúi", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "A három királyság háborúi (1639-1653): Angol királypártiak vs. Angol parlamentaristák"
        },
        {
            "question": "Melyik háború zajlott 1654-1667 között? (Orosz Cárság & Kozák Hetmanátus vs. Lengyel-Litván Unió)",
            "options": ["Orosz–lengyel háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–lengyel háború (1654-1667): Orosz Cárság & Kozák Hetmanátus vs. Lengyel-Litván Unió"
        },
        {
            "question": "Melyik háború zajlott 1655-1660 között? (Svédország vs. Dánia-Norvégia, Lengyel-Litván Unió)",
            "options": ["Második északi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Második északi háború (1655-1660): Svédország vs. Dánia-Norvégia, Lengyel-Litván Unió"
        },
        {
            "question": "Melyik háború zajlott 1939-1945 között? (Szövetségesek vs. Tengelyhatalmak)",
            "options": ["I. világháború", "II. világháború", "Hidegháború", "Koreai háború"],
            "correct": 1,
            "explanation": "II. világháború (1939-1945): Szövetségesek vs. Tengelyhatalmak (Németország, Olaszország, Japán)"
        },
        {
            "question": "Melyik háború zajlott 1950-1953 között? (Észak-Korea vs. Dél-Korea)",
            "options": ["Vietnámi háború", "Koreai háború", "Hidegháború", "Afganisztáni háború"],
            "correct": 1,
            "explanation": "Koreai háború (1950-1953): Észak-Korea (Kína, Szovjetunió támogatásával) vs. Dél-Korea (USA, ENSZ támogatásával)"
        },
        {
            "question": "Melyik háború zajlott 1955-1975 között? (Észak-Vietnam vs. Dél-Vietnam)",
            "options": ["Koreai háború", "Vietnámi háború", "Hidegháború", "Afganisztáni háború"],
            "correct": 1,
            "explanation": "Vietnámi háború (1955-1975): Észak-Vietnam (Szovjetunió, Kína támogatásával) vs. Dél-Vietnam (USA támogatásával)"
        },
        {
            "question": "Melyik háború zajlott 1947-1991 között? (USA vs. Szovjetunió)",
            "options": ["Hidegháború", "Koreai háború", "Vietnámi háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Hidegháború (1947-1991): USA és szövetségesei vs. Szovjetunió és szövetségesei (ideológiai konfliktus)"
        },
        {
            "question": "Melyik háború zajlott 1979-1989 között? (Szovjetunió vs. Afganisztáni mudzsahidok)",
            "options": ["Afganisztáni háború", "Irak-irani háború", "Öbölháború", "Jugoszláv háború"],
            "correct": 0,
            "explanation": "Afganisztáni háború (1979-1989): Szovjetunió vs. Afganisztáni mudzsahidok (USA, Pakisztán támogatásával)"
        },
        {
            "question": "Melyik háború zajlott 1980-1988 között? (Irak vs. Irán)",
            "options": ["Irak-irani háború", "Öbölháború", "Jugoszláv háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Irak-irani háború (1980-1988): Irak vs. Irán (két iszlám ország közötti konfliktus)"
        },
        {
            "question": "Melyik háború zajlott 1990-1991 között? (ENSZ koalíció vs. Irak)",
            "options": ["Öbölháború", "Jugoszláv háború", "Irak-irani háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Öbölháború (1990-1991): ENSZ koalíció (USA vezetésével) vs. Irak (Kuvait megszállása miatt)"
        },
        {
            "question": "Melyik háború zajlott 1991-2001 között? (Jugoszlávia felbomlása)",
            "options": ["Jugoszláv háború", "Afganisztáni háború", "Irak-irani háború", "Öbölháború"],
            "correct": 0,
            "explanation": "Jugoszláv háború (1991-2001): Jugoszlávia felbomlása, különböző etnikai csoportok közötti konfliktusok"
        },
        {
            "question": "Melyik háború zajlott 2001-2021 között? (USA vs. Taliban)",
            "options": ["Afganisztáni háború", "Irak háború", "Szíriai háború", "Jemeni háború"],
            "correct": 0,
            "explanation": "Afganisztáni háború (2001-2021): USA és szövetségesei vs. Taliban és al-Kaida (9/11 terrortámadás után)"
        },
        {
            "question": "Melyik háború zajlott 2003-2011 között? (USA vs. Irak)",
            "options": ["Irak háború", "Afganisztáni háború", "Szíriai háború", "Jemeni háború"],
            "correct": 0,
            "explanation": "Irak háború (2003-2011): USA és szövetségesei vs. Irak (Saddam Huszein eltávolítása miatt)"
        },
        {
            "question": "Melyik háború zajlott 2011-2023 között? (Szíriai kormány vs. lázadók)",
            "options": ["Szíriai háború", "Jemeni háború", "Irak háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Szíriai háború (2011-2023): Szíriai kormány vs. különböző lázadó csoportok (arab tavasz következménye)"
        },
        {
            "question": "Melyik háború zajlott 2014-2023 között? (Jemeni kormány vs. Huti lázadók)",
            "options": ["Jemeni háború", "Szíriai háború", "Irak háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Jemeni háború (2014-2023): Jemeni kormány vs. Huti lázadók (Szaúd-Arábia és Irán proxy háborúja)"
        },
        {
            "question": "Melyik háború zajlott 2022-2023 között? (Oroszország vs. Ukrajna)",
            "options": ["Orosz-ukrán háború", "Jemeni háború", "Szíriai háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Orosz-ukrán háború (2022-2023): Oroszország vs. Ukrajna (Oroszország inváziója Ukrajnába)"
        },
        {
            "question": "Melyik háború zajlott 1917-1922 között? (Vörösök vs. Fehérek)",
            "options": ["Orosz polgárháború", "I. világháború", "II. világháború", "Hidegháború"],
            "correct": 0,
            "explanation": "Orosz polgárháború (1917-1922): Vörösök (bolsevikok) vs. Fehérek (ellenforradalmárok)"
        },
        {
            "question": "Melyik háború zajlott 1936-1939 között? (Köztársaságiak vs. Nacionalisták)",
            "options": ["Spanyol polgárháború", "II. világháború", "I. világháború", "Hidegháború"],
            "correct": 0,
            "explanation": "Spanyol polgárháború (1936-1939): Köztársaságiak vs. Nacionalisták (Franco vezetésével)"
        },
        {
            "question": "Melyik háború zajlott 1948-1949 között? (Izrael vs. Arab Liga)",
            "options": ["Arab-izraeli háború", "Koreai háború", "Vietnámi háború", "Hidegháború"],
            "correct": 0,
            "explanation": "Arab-izraeli háború (1948-1949): Izrael vs. Arab Liga (Egyiptom, Jordánia, Szíria, Libanon, Irak)"
        },
        {
            "question": "Melyik háború zajlott 1967-ben? (Izrael vs. Arab Liga)",
            "options": ["Hatnapos háború", "Arab-izraeli háború", "Koreai háború", "Vietnámi háború"],
            "correct": 0,
            "explanation": "Hatnapos háború (1967): Izrael vs. Arab Liga (Egyiptom, Jordánia, Szíria) - Izrael gyors győzelme"
        },
        {
            "question": "Melyik háború zajlott 1973-ban? (Izrael vs. Egyiptom és Szíria)",
            "options": ["Jom Kippur háború", "Hatnapos háború", "Arab-izraeli háború", "Vietnámi háború"],
            "correct": 0,
            "explanation": "Jom Kippur háború (1973): Izrael vs. Egyiptom és Szíria (arab országok meglepetésszerű támadása)"
        },
        {
            "question": "Melyik háború zajlott 1982-ben? (Izrael vs. Libanon)",
            "options": ["Libanoni háború", "Jom Kippur háború", "Hatnapos háború", "Arab-izraeli háború"],
            "correct": 0,
            "explanation": "Libanoni háború (1982): Izrael vs. Libanon (PLO kiűzése Libanonból)"
        },
        {
            "question": "Melyik háború zajlott 1999-ben? (NATO vs. Jugoszlávia)",
            "options": ["Koszovói háború", "Jugoszláv háború", "Öbölháború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Koszovói háború (1999): NATO vs. Jugoszlávia (Koszovó albánok védelmében)"
        },
        {
            "question": "Melyik háború zajlott 2008-ban? (Oroszország vs. Grúzia)",
            "options": ["Orosz-grúz háború", "Orosz-ukrán háború", "Jugoszláv háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Orosz-grúz háború (2008): Oroszország vs. Grúzia (Dél-Oszétia és Abházia miatt)"
        },
        {
            "question": "Melyik háború zajlott 2014-ben? (Oroszország vs. Ukrajna)",
            "options": ["Orosz-ukrán háború kezdete", "Szíriai háború", "Jemeni háború", "Irak háború"],
            "correct": 0,
            "explanation": "Orosz-ukrán háború kezdete (2014): Oroszország vs. Ukrajna (Krím annektálása és kelet-ukrán konfliktus)"
        },
        {
            "question": "Melyik háború zajlott 1941-1945 között? (Szovjetunió vs. Németország)",
            "options": ["Nagy Honvédő Háború", "II. világháború", "I. világháború", "Hidegháború"],
            "correct": 0,
            "explanation": "Nagy Honvédő Háború (1941-1945): Szovjetunió vs. Németország (a II. világháború keleti frontja)"
        },
        {
            "question": "Melyik háború zajlott 1939-1940 között? (Szovjetunió vs. Finnország)",
            "options": ["Téli háború", "II. világháború", "I. világháború", "Hidegháború"],
            "correct": 0,
            "explanation": "Téli háború (1939-1940): Szovjetunió vs. Finnország (Finnország területi veszteségei)"
        },
        {
            "question": "Melyik háború zajlott 1941-1944 között? (Szovjetunió vs. Finnország)",
            "options": ["Folyamatos háború", "Téli háború", "Nagy Honvédő Háború", "II. világháború"],
            "correct": 0,
            "explanation": "Folyamatos háború (1941-1944): Szovjetunió vs. Finnország (a II. világháború részeként)"
        },
        {
            "question": "Melyik háború zajlott 1954-1962 között? (Franciaország vs. Algériai Front)",
            "options": ["Algériai háború", "Vietnámi háború", "Koreai háború", "Hidegháború"],
            "correct": 0,
            "explanation": "Algériai háború (1954-1962): Franciaország vs. Algériai Nemzeti Felszabadítási Front (Algéria függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1962-ben? (Kína vs. India)",
            "options": ["Indokínai háború", "Algériai háború", "Vietnámi háború", "Koreai háború"],
            "correct": 0,
            "explanation": "Indokínai háború (1962): Kína vs. India (határviták miatt)"
        },
        {
            "question": "Melyik háború zajlott 1965-ben? (India vs. Pakisztán)",
            "options": ["Indo-pakisztáni háború", "Indokínai háború", "Vietnámi háború", "Koreai háború"],
            "correct": 0,
            "explanation": "Indo-pakisztáni háború (1965): India vs. Pakisztán (Kasmír miatt)"
        },
        {
            "question": "Melyik háború zajlott 1971-ben? (India vs. Pakisztán)",
            "options": ["Bangladesi függetlenségi háború", "Indo-pakisztáni háború", "Vietnámi háború", "Koreai háború"],
            "correct": 0,
            "explanation": "Bangladesi függetlenségi háború (1971): India vs. Pakisztán (Banglades függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1979-ben? (Kína vs. Vietnam)",
            "options": ["Kínai-vietnámi háború", "Vietnámi háború", "Koreai háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Kínai-vietnámi háború (1979): Kína vs. Vietnam (határviták és politikai konfliktusok)"
        },
        {
            "question": "Melyik háború zajlott 1982-ben? (Nagy-Britannia vs. Argentína)",
            "options": ["Falkland-szigeteki háború", "Libanoni háború", "Jom Kippur háború", "Arab-izraeli háború"],
            "correct": 0,
            "explanation": "Falkland-szigeteki háború (1982): Nagy-Britannia vs. Argentína (Falkland-szigetek birtoklása)"
        },
        {
            "question": "Melyik háború zajlott 1994-1996 között? (Oroszország vs. Csecsenföld)",
            "options": ["Csecsen háború", "Jugoszláv háború", "Afganisztáni háború", "Irak háború"],
            "correct": 0,
            "explanation": "Csecsen háború (1994-1996): Oroszország vs. Csecsenföld (Csecsenföld függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1999-2009 között?",
            "options": ["Második csecsen háború", "Csecsen háború", "Jugoszláv háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Második csecsen háború (1999-2009): Oroszország vs. Csecsenföld (terrorizmus elleni háború)"
        },
        {
            "question": "Melyik háború zajlott 2006-ban?",
            "options": ["Libanoni háború", "Szíriai háború", "Jemeni háború", "Irak háború"],
            "correct": 0,
            "explanation": "Libanoni háború (2006): Izrael vs. Libanon (Hezbollah elleni hadművelet)"
        },
        {
            "question": "Melyik háború zajlott 2008-2009 között?",
            "options": ["Gázai háború", "Libanoni háború", "Szíriai háború", "Jemeni háború"],
            "correct": 0,
            "explanation": "Gázai háború (2008-2009): Izrael vs. Palesztina (Gázai övezet elleni hadművelet)"
        },
        {
            "question": "Melyik háború zajlott 2012-ben?",
            "options": ["Mali háború", "Szíriai háború", "Jemeni háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Mali háború (2012): Franciaország vs. Iszlám milíciák (Mali területi integritása)"
        },
        {
            "question": "Melyik háború zajlott 2014-2017 között?",
            "options": ["Irak háború", "Szíriai háború", "Jemeni háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Irak háború (2014-2017): Irak és koalíció vs. ISIL (Iszlám Állam elleni háború)"
        },
        {
            "question": "Melyik háború zajlott 2015-2023 között?",
            "options": ["Jemeni háború", "Szíriai háború", "Irak háború", "Afganisztáni háború"],
            "correct": 0,
            "explanation": "Jemeni háború (2015-2023): Jemeni kormány vs. Huti lázadók (Szaúd-Arábia és Irán proxy háborúja)"
        },
        {
            "question": "Melyik háború zajlott 2020-ban? (Örményország vs. Azerbajdzsán)",
            "options": ["Örmény-azeri háború", "Orosz-ukrán háború", "Jemeni háború", "Szíriai háború"],
            "correct": 0,
            "explanation": "Örmény-azeri háború (2020): Örményország vs. Azerbajdzsán (Heves-Karabah régió miatt)"
        },
        {
            "question": "Melyik háború zajlott 2023-ban? (Izrael vs. Hamas)",
            "options": ["Izrael-Hamas háború", "Orosz-ukrán háború", "Jemeni háború", "Szíriai háború"],
            "correct": 0,
            "explanation": "Izrael-Hamas háború (2023): Izrael vs. Hamas (Gázai övezet elleni hadművelet)"
        },
        {
            "question": "Melyik háború zajlott 1812-ben?",
            "options": ["Napóleoni háború", "Amerikai függetlenségi háború", "Hétéves háború", "Spanyol örökösödési háború"],
            "correct": 0,
            "explanation": "Napóleoni háború (1812): Franciaország vs. Oroszország (Napóleon oroszországi hadjárata)"
        },
        {
            "question": "Melyik háború zajlott 1775-1783 között?",
            "options": ["Amerikai függetlenségi háború", "Hétéves háború", "Spanyol örökösödési háború", "Napóleoni háború"],
            "correct": 0,
            "explanation": "Amerikai függetlenségi háború (1775-1783): Amerikai kolóniák vs. Nagy-Britannia (USA függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1756-1763 között?",
            "options": ["Hétéves háború", "Spanyol örökösödési háború", "Napóleoni háború", "Amerikai függetlenségi háború"],
            "correct": 0,
            "explanation": "Hétéves háború (1756-1763): Nagy-Britannia, Poroszország vs. Franciaország, Ausztria, Oroszország"
        },
        {
            "question": "Melyik háború zajlott 1701-1714 között?",
            "options": ["Spanyol örökösödési háború", "Hétéves háború", "Napóleoni háború", "Amerikai függetlenségi háború"],
            "correct": 0,
            "explanation": "Spanyol örökösödési háború (1701-1714): Habsburgok vs. Bourbonok (Spanyol trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1618-1648 között?",
            "options": ["Harmincéves háború", "Spanyol örökösödési háború", "Hétéves háború", "Napóleoni háború"],
            "correct": 0,
            "explanation": "Harmincéves háború (1618-1648): Protestánsok vs. Katolikusok (Német-római Birodalom)"
        },
        {
            "question": "Melyik háború zajlott 1455-1485 között?",
            "options": ["Rózsák háborúja", "Harmincéves háború", "Spanyol örökösödési háború", "Hétéves háború"],
            "correct": 0,
            "explanation": "Rózsák háborúja (1455-1485): Lancaster vs. York (Angol trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1337-1453 között?",
            "options": ["Százéves háború", "Rózsák háborúja", "Harmincéves háború", "Spanyol örökösödési háború"],
            "correct": 0,
            "explanation": "Százéves háború (1337-1453): Anglia vs. Franciaország (francia trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1096-1291 között?",
            "options": ["Keresztes háborúk", "Százéves háború", "Rózsák háborúja", "Harmincéves háború"],
            "correct": 0,
            "explanation": "Keresztes háborúk (1096-1291): Európai keresztények vs. Muszlimok (Szentföld visszafoglalása)"
        },
        {
            "question": "Melyik háború zajlott 431-404 i.e. között?",
            "options": ["Peloponnészoszi háború", "Keresztes háborúk", "Százéves háború", "Rózsák háborúja"],
            "correct": 0,
            "explanation": "Peloponnészoszi háború (431-404 i.e.): Athén vs. Spárta (görög városállamok közötti konfliktus)"
        },
        {
            "question": "Melyik háború zajlott 264-146 i.e. között?",
            "options": ["Pun háborúk", "Peloponnészoszi háború", "Keresztes háborúk", "Százéves háború"],
            "correct": 0,
            "explanation": "Pun háborúk (264-146 i.e.): Róma vs. Karthágó (Földközi-tenger dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1861-1865 között?",
            "options": ["Amerikai polgárháború", "Pun háborúk", "Peloponnészoszi háború", "Keresztes háborúk"],
            "correct": 0,
            "explanation": "Amerikai polgárháború (1861-1865): Északi Unió vs. Déli Konföderáció (rabszolgaság kérdése)"
        },
        {
            "question": "Melyik háború zajlott 1803-1815 között?",
            "options": ["Napóleoni háborúk", "Amerikai polgárháború", "Pun háborúk", "Peloponnészoszi háború"],
            "correct": 0,
            "explanation": "Napóleoni háborúk (1803-1815): Franciaország vs. Európai koalíció (Napóleon dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1853-1856 között?",
            "options": ["Krím háború", "Napóleoni háborúk", "Amerikai polgárháború", "Pun háborúk"],
            "correct": 0,
            "explanation": "Krím háború (1853-1856): Oroszország vs. Oszmán Birodalom, Nagy-Britannia, Franciaország"
        },
        {
            "question": "Melyik háború zajlott 1870-1871 között?",
            "options": ["Porosz-francia háború", "Krím háború", "Napóleoni háborúk", "Amerikai polgárháború"],
            "correct": 0,
            "explanation": "Porosz-francia háború (1870-1871): Poroszország vs. Franciaország (Német egység)"
        },
        {
            "question": "Melyik háború zajlott 1899-1902 között?",
            "options": ["Búr háború", "Porosz-francia háború", "Krím háború", "Napóleoni háborúk"],
            "correct": 0,
            "explanation": "Búr háború (1899-1902): Nagy-Britannia vs. Búr köztársaságok (Dél-Afrika dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1904-1905 között?",
            "options": ["Orosz-japán háború", "Búr háború", "Porosz-francia háború", "Krím háború"],
            "correct": 0,
            "explanation": "Orosz-japán háború (1904-1905): Oroszország vs. Japán (Mandzsúria és Korea dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1912-1913 között?",
            "options": ["Balkáni háborúk", "Orosz-japán háború", "Búr háború", "Porosz-francia háború"],
            "correct": 0,
            "explanation": "Balkáni háborúk (1912-1913): Balkáni Liga vs. Oszmán Birodalom (Balkán függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1939-1940 között?",
            "options": ["Téli háború", "Balkáni háborúk", "Orosz-japán háború", "Búr háború"],
            "correct": 0,
            "explanation": "Téli háború (1939-1940): Szovjetunió vs. Finnország (Finnország területi veszteségei)"
        },
        {
            "question": "Melyik háború zajlott 1941-1944 között?",
            "options": ["Folyamatos háború", "Téli háború", "Balkáni háborúk", "Orosz-japán háború"],
            "correct": 0,
            "explanation": "Folyamatos háború (1941-1944): Szovjetunió vs. Finnország (a II. világháború részeként)"
        },
        {
            "question": "Melyik háború zajlott 1948-1949 között?",
            "options": ["Arab-izraeli háború", "Folyamatos háború", "Téli háború", "Balkáni háborúk"],
            "correct": 0,
            "explanation": "Arab-izraeli háború (1948-1949): Izrael vs. Arab Liga (Egyiptom, Jordánia, Szíria, Libanon, Irak)"
        },
        {
            "question": "Melyik háború zajlott 1956-ban?",
            "options": ["Szuézi válság", "Arab-izraeli háború", "Folyamatos háború", "Téli háború"],
            "correct": 0,
            "explanation": "Szuézi válság (1956): Izrael, Nagy-Britannia, Franciaország vs. Egyiptom (Szuézi-csatorna)"
        },
        {
            "question": "Melyik háború zajlott 1962-ben?",
            "options": ["Indokínai háború", "Szuézi válság", "Arab-izraeli háború", "Folyamatos háború"],
            "correct": 0,
            "explanation": "Indokínai háború (1962): Kína vs. India (határviták miatt)"
        },
        {
            "question": "Melyik háború zajlott 1965-ben?",
            "options": ["Indo-pakisztáni háború", "Indokínai háború", "Szuézi válság", "Arab-izraeli háború"],
            "correct": 0,
            "explanation": "Indo-pakisztáni háború (1965): India vs. Pakisztán (Kasmír miatt)"
        },
        {
            "question": "Melyik háború zajlott 1971-ben?",
            "options": ["Bangladesi függetlenségi háború", "Indo-pakisztáni háború", "Indokínai háború", "Szuézi válság"],
            "correct": 0,
            "explanation": "Bangladesi függetlenségi háború (1971): India vs. Pakisztán (Banglades függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1979-ben?",
            "options": ["Kínai-vietnámi háború", "Bangladesi függetlenségi háború", "Indo-pakisztáni háború", "Indokínai háború"],
            "correct": 0,
            "explanation": "Kínai-vietnámi háború (1979): Kína vs. Vietnam (határviták és politikai konfliktusok)"
        },
        {
            "question": "Melyik háború zajlott 1982-ben?",
            "options": ["Falkland-szigeteki háború", "Kínai-vietnámi háború", "Bangladesi függetlenségi háború", "Indo-pakisztáni háború"],
            "correct": 0,
            "explanation": "Falkland-szigeteki háború (1982): Nagy-Britannia vs. Argentína (Falkland-szigetek birtoklása)"
        },
        {
            "question": "Melyik háború zajlott 1994-1996 között?",
            "options": ["Csecsen háború", "Falkland-szigeteki háború", "Kínai-vietnámi háború", "Bangladesi függetlenségi háború"],
            "correct": 0,
            "explanation": "Csecsen háború (1994-1996): Oroszország vs. Csecsenföld (Csecsenföld függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 2020-ban?",
            "options": ["Örmény-azeri háború", "Jemeni háború", "Irak háború", "Mali háború"],
            "correct": 0,
            "explanation": "Örmény-azeri háború (2020): Örményország vs. Azerbajdzsán (Heves-Karabah régió miatt)"
        },
        {
            "question": "Melyik háború zajlott 2023-ban?",
            "options": ["Izrael-Hamas háború", "Örmény-azeri háború", "Jemeni háború", "Irak háború"],
            "correct": 0,
            "explanation": "Izrael-Hamas háború (2023): Izrael vs. Hamas (Gázai övezet elleni hadművelet)"
        },
        {
            "question": "Melyik háború zajlott 1202-1204 között? (Keresztesek vs. Bizánci Birodalom)",
            "options": ["IV. keresztes háború", "III. keresztes háború", "V. keresztes háború", "VI. keresztes háború"],
            "correct": 0,
            "explanation": "IV. keresztes háború (1202-1204): Keresztesek vs. Bizánci Birodalom (Konstantinápoly kifosztása)"
        },
        {
            "question": "Melyik háború zajlott 1217-1221 között? (Magyar Királyság vs. Oszmán Birodalom)",
            "options": ["V. keresztes háború", "IV. keresztes háború", "VI. keresztes háború", "VII. keresztes háború"],
            "correct": 0,
            "explanation": "V. keresztes háború (1217-1221): Magyar Királyság vs. Oszmán Birodalom (II. András hadjárata)"
        },
        {
            "question": "Melyik háború zajlott 1228-1229 között? (Német-római Birodalom vs. Egyiptom)",
            "options": ["VI. keresztes háború", "V. keresztes háború", "VII. keresztes háború", "VIII. keresztes háború"],
            "correct": 0,
            "explanation": "VI. keresztes háború (1228-1229): Német-római Birodalom vs. Egyiptom (II. Frigyes diplomáciai győzelme)"
        },
        {
            "question": "Melyik háború zajlott 1337-1453 között? (Anglia vs. Franciaország)",
            "options": ["Százéves háború", "Rózsák háborúja", "Harmincéves háború", "Spanyol örökösödési háború"],
            "correct": 0,
            "explanation": "Százéves háború (1337-1453): Anglia vs. Franciaország (francia trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1389-ben? (Szerb Birodalom vs. Oszmán Birodalom)",
            "options": ["Kosovói csata", "Marathóni csata", "Thermopülai csata", "Hastings csata"],
            "correct": 0,
            "explanation": "Kosovói csata (1389): Szerb Birodalom vs. Oszmán Birodalom (Lázár herceg halála)"
        },
        {
            "question": "Melyik háború zajlott 1396-ban? (Európai keresztesek vs. Oszmán Birodalom)",
            "options": ["Nikápolyi csata", "Kosovói csata", "Marathóni csata", "Thermopülai csata"],
            "correct": 0,
            "explanation": "Nikápolyi csata (1396): Európai keresztesek vs. Oszmán Birodalom (Sigismund veresége)"
        },
        {
            "question": "Melyik háború zajlott 1455-1485 között? (Lancaster vs. York)",
            "options": ["Rózsák háborúja", "Százéves háború", "Harmincéves háború", "Spanyol örökösödési háború"],
            "correct": 0,
            "explanation": "Rózsák háborúja (1455-1485): Lancaster vs. York (Angol trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1453-ban? (Oszmán Birodalom vs. Bizánci Birodalom)",
            "options": ["Konstantinápoly ostroma", "Nikápolyi csata", "Kosovói csata", "Marathóni csata"],
            "correct": 0,
            "explanation": "Konstantinápoly ostroma (1453): Oszmán Birodalom vs. Bizánci Birodalom (Bizánc bukása)"
        },
        {
            "question": "Melyik háború zajlott 1494-1498 között? (Franciaország vs. Itáliai városállamok)",
            "options": ["I. itáliai háború", "Rózsák háborúja", "Százéves háború", "Harmincéves háború"],
            "correct": 0,
            "explanation": "I. itáliai háború (1494-1498): Franciaország vs. Itáliai városállamok (VIII. Károly hadjárata)"
        },
        {
            "question": "Melyik háború zajlott 1526-ban? (Magyar Királyság vs. Oszmán Birodalom)",
            "options": ["Mohácsi csata", "Konstantinápoly ostroma", "Nikápolyi csata", "Kosovói csata"],
            "correct": 0,
            "explanation": "Mohácsi csata (1526): Magyar Királyság vs. Oszmán Birodalom (II. Lajos halála)"
        },
        {
            "question": "Melyik háború zajlott 1556-1609 között? (Spanyolország vs. Hollandia)",
            "options": ["Nyolcvanéves háború", "I. itáliai háború", "Rózsák háborúja", "Százéves háború"],
            "correct": 0,
            "explanation": "Nyolcvanéves háború (1556-1609): Spanyolország vs. Hollandia (Hollandia függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1588-ban? (Anglia vs. Spanyolország)",
            "options": ["Spanyol Armada", "Nyolcvanéves háború", "I. itáliai háború", "Rózsák háborúja"],
            "correct": 0,
            "explanation": "Spanyol Armada (1588): Anglia vs. Spanyolország (I. Erzsébet győzelme)"
        },
        {
            "question": "Melyik háború zajlott 1618-1648 között? (Protestánsok vs. Katolikusok)",
            "options": ["Harmincéves háború", "Nyolcvanéves háború", "I. itáliai háború", "Rózsák háborúja"],
            "correct": 0,
            "explanation": "Harmincéves háború (1618-1648): Protestánsok vs. Katolikusok (Német-római Birodalom)"
        },
        {
            "question": "Melyik háború zajlott 1683-ban? (Oszmán Birodalom vs. Európai koalíció)",
            "options": ["Bécs ostroma", "Harmincéves háború", "Nyolcvanéves háború", "I. itáliai háború"],
            "correct": 0,
            "explanation": "Bécs ostroma (1683): Oszmán Birodalom vs. Európai koalíció (Sobieski győzelme)"
        },
        {
            "question": "Melyik háború zajlott 1701-1714 között? (Habsburgok vs. Bourbonok)",
            "options": ["Spanyol örökösödési háború", "Harmincéves háború", "Nyolcvanéves háború", "I. itáliai háború"],
            "correct": 0,
            "explanation": "Spanyol örökösödési háború (1701-1714): Habsburgok vs. Bourbonok (Spanyol trón öröklése)"
        },
        {
            "question": "Melyik háború zajlott 1756-1763 között? (Nagy-Britannia, Poroszország vs. Franciaország, Ausztria, Oroszország)",
            "options": ["Hétéves háború", "Spanyol örökösödési háború", "Harmincéves háború", "Nyolcvanéves háború"],
            "correct": 0,
            "explanation": "Hétéves háború (1756-1763): Nagy-Britannia, Poroszország vs. Franciaország, Ausztria, Oroszország"
        },
        {
            "question": "Melyik háború zajlott 1775-1783 között? (Amerikai kolóniák vs. Nagy-Britannia)",
            "options": ["Amerikai függetlenségi háború", "Hétéves háború", "Spanyol örökösödési háború", "Harmincéves háború"],
            "correct": 0,
            "explanation": "Amerikai függetlenségi háború (1775-1783): Amerikai kolóniák vs. Nagy-Britannia (USA függetlensége)"
        },
        {
            "question": "Melyik háború zajlott 1789-1799 között? (Francia forradalmárok vs. Európai monarchiák)",
            "options": ["Francia forradalom", "Amerikai függetlenségi háború", "Hétéves háború", "Spanyol örökösödési háború"],
            "correct": 0,
            "explanation": "Francia forradalom (1789-1799): Francia forradalmárok vs. Európai monarchiák (abszolutizmus bukása)"
        },
        {
            "question": "Melyik háború zajlott 1803-1815 között? (Franciaország vs. Európai koalíció)",
            "options": ["Napóleoni háborúk", "Francia forradalom", "Amerikai függetlenségi háború", "Hétéves háború"],
            "correct": 0,
            "explanation": "Napóleoni háborúk (1803-1815): Franciaország vs. Európai koalíció (Napóleon dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1812-ben? (Franciaország vs. Oroszország)",
            "options": ["Napóleon oroszországi hadjárata", "Napóleoni háborúk", "Francia forradalom", "Amerikai függetlenségi háború"],
            "correct": 0,
            "explanation": "Napóleon oroszországi hadjárata (1812): Franciaország vs. Oroszország (Napóleon veresége)"
        },
        {
            "question": "Melyik háború zajlott 1815-ben? (Európai koalíció vs. Franciaország)",
            "options": ["Waterloo csata", "Napóleon oroszországi hadjárata", "Napóleoni háborúk", "Francia forradalom"],
            "correct": 0,
            "explanation": "Waterloo csata (1815): Európai koalíció vs. Franciaország (Napóleon végleges veresége)"
        },
        {
            "question": "Melyik háború zajlott 1853-1856 között? (Oroszország vs. Oszmán Birodalom, Nagy-Britannia, Franciaország)",
            "options": ["Krím háború", "Waterloo csata", "Napóleon oroszországi hadjárata", "Napóleoni háborúk"],
            "correct": 0,
            "explanation": "Krím háború (1853-1856): Oroszország vs. Oszmán Birodalom, Nagy-Britannia, Franciaország"
        },
        {
            "question": "Melyik háború zajlott 1861-1865 között? (Északi Unió vs. Déli Konföderáció)",
            "options": ["Amerikai polgárháború", "Krím háború", "Waterloo csata", "Napóleon oroszországi hadjárata"],
            "correct": 0,
            "explanation": "Amerikai polgárháború (1861-1865): Északi Unió vs. Déli Konföderáció (rabszolgaság kérdése)"
        },
        {
            "question": "Melyik háború zajlott 1870-1871 között? (Poroszország vs. Franciaország)",
            "options": ["Porosz-francia háború", "Amerikai polgárháború", "Krím háború", "Waterloo csata"],
            "correct": 0,
            "explanation": "Porosz-francia háború (1870-1871): Poroszország vs. Franciaország (Német egység)"
        },
        {
            "question": "Melyik háború zajlott 1899-1902 között? (Nagy-Britannia vs. Búr köztársaságok)",
            "options": ["Búr háború", "Porosz-francia háború", "Amerikai polgárháború", "Krím háború"],
            "correct": 0,
            "explanation": "Búr háború (1899-1902): Nagy-Britannia vs. Búr köztársaságok (Dél-Afrika dominanciája)"
        },
        {
            "question": "Melyik háború zajlott 1672-1678 között? (Franciaország vs. Holland Köztársaság, Spanyolország, Német-római Birodalom)",
            "options": ["Francia–holland háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Francia–holland háború (1672-1678): Franciaország vs. Holland Köztársaság, Spanyolország, Német-római Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1683-1699 között? (Szent Liga (Német-római Birodalom, Lengyelország, Velence, Oroszország) vs. Oszmán Birodalom)",
            "options": ["Nagy török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Nagy török háború (1683-1699): Szent Liga (Német-római Birodalom, Lengyelország, Velence, Oroszország) vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1688-1697 között? (Franciaország vs. Augsburgi Liga (Anglia, Hollandia, Német-római Birodalom))",
            "options": ["Augsburgi Liga háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Augsburgi Liga háborúja (1688-1697): Franciaország vs. Augsburgi Liga (Anglia, Hollandia, Német-római Birodalom)"
        },
        {
            "question": "Melyik háború zajlott 1667-1668 között? (Franciaország vs. Spanyolország)",
            "options": ["Devolúciós háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Devolúciós háború (1667-1668): Franciaország vs. Spanyolország"
        },
        {
            "question": "Melyik háború zajlott 1652-1654 között? (Angol Commonwealth vs. Holland Köztársaság)",
            "options": ["Első angol-holland háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Első angol-holland háború (1652-1654): Angol Commonwealth vs. Holland Köztársaság"
        },
        {
            "question": "Melyik háború zajlott 1665-1667 között? (Anglia vs. Holland Köztársaság)",
            "options": ["Második angol-holland háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Második angol-holland háború (1665-1667): Anglia vs. Holland Köztársaság"
        },
        {
            "question": "Melyik háború zajlott 1672-1674 között? (Anglia, Franciaország vs. Holland Köztársaság)",
            "options": ["Harmadik angol-holland háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Harmadik angol-holland háború (1672-1674): Anglia, Franciaország vs. Holland Köztársaság"
        },
        {
            "question": "Melyik háború zajlott 1676-1681 között? (Lengyel-Litván Unió vs. Oszmán Birodalom)",
            "options": ["Lengyel–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Lengyel–török háború (1676-1681): Lengyel-Litván Unió vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1700-1721 között? (Svédország vs. Oroszország, Dánia-Norvégia, Szász-Lengyelország)",
            "options": ["Nagy északi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Nagy északi háború (1700-1721): Svédország vs. Oroszország, Dánia-Norvégia, Szász-Lengyelország"
        },
        {
            "question": "Melyik háború zajlott 1733-1735 között? (Leszczyński Stanisław támogatói (Franciaország) vs. II. Ágost támogatói (Oroszország, Ausztria))",
            "options": ["Lengyel örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Lengyel örökösödési háború (1733-1735): Leszczyński Stanisław támogatói (Franciaország) vs. II. Ágost támogatói (Oroszország, Ausztria)"
        },
        {
            "question": "Melyik háború zajlott 1735-1739 között? (Orosz Birodalom vs. Oszmán Birodalom)",
            "options": ["Orosz–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–török háború (1735-1739): Orosz Birodalom vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1739-1748 között? (Nagy-Britannia vs. Spanyolország (Osztrák örökösödési háború része))",
            "options": ["Jenkins füle háborúja", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Jenkins füle háborúja (1739-1748): Nagy-Britannia vs. Spanyolország (Osztrák örökösödési háború része)"
        },
        {
            "question": "Melyik háború zajlott 1768-1774 között? (Orosz Birodalom vs. Oszmán Birodalom)",
            "options": ["Orosz–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–török háború (1768-1774): Orosz Birodalom vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1778-1779 között? (Poroszország, Szászország vs. Habsburg Monarchia)",
            "options": ["Bajor örökösödési háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Bajor örökösödési háború (1778-1779): Poroszország, Szászország vs. Habsburg Monarchia"
        },
        {
            "question": "Melyik háború zajlott 1788-1790 között? (Orosz Birodalom vs. Svédország)",
            "options": ["Orosz–svéd háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–svéd háború (1788-1790): Orosz Birodalom vs. Svédország"
        },
        {
            "question": "Melyik háború zajlott 1787-1792 között? (Orosz Birodalom, Ausztria vs. Oszmán Birodalom)",
            "options": ["Orosz–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–török háború (1787-1792): Orosz Birodalom, Ausztria vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1792-1797 között? (Francia Köztársaság vs. Első koalíció (Ausztria, Poroszország, Nagy-Britannia))",
            "options": ["Első koalíciós háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Első koalíciós háború (1792-1797): Francia Köztársaság vs. Első koalíció (Ausztria, Poroszország, Nagy-Britannia)"
        },
        {
            "question": "Melyik háború zajlott 1848-1849 között? (Szardínia-Piemont vs. Osztrák Birodalom)",
            "options": ["Szardíniai–osztrák háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Szardíniai–osztrák háború (1848-1849): Szardínia-Piemont vs. Osztrák Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1859 között? (Franciaország, Szardínia-Piemont vs. Osztrák Birodalom)",
            "options": ["Francia–osztrák háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Francia–osztrák háború (1859): Franciaország, Szardínia-Piemont vs. Osztrák Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1864 között? (Poroszország & Ausztria vs. Dánia)",
            "options": ["Dán–porosz háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Dán–porosz háború (1864): Poroszország & Ausztria vs. Dánia"
        },
        {
            "question": "Melyik háború zajlott 1866 között? (Poroszország & Olaszország vs. Osztrák Birodalom)",
            "options": ["Porosz–osztrák háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Porosz–osztrák háború (1866): Poroszország & Olaszország vs. Osztrák Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1870-1871 között? (Poroszország & Északnémet Szövetség vs. Franciaország)",
            "options": ["Porosz–francia háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Porosz–francia háború (1870-1871): Poroszország & Északnémet Szövetség vs. Franciaország"
        },
        {
            "question": "Melyik háború zajlott 1877-1878 között? (Orosz Birodalom vs. Oszmán Birodalom)",
            "options": ["Orosz–török háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz–török háború (1877-1878): Orosz Birodalom vs. Oszmán Birodalom"
        },
        {
            "question": "Melyik háború zajlott 1918-1921 között? (Vörös Hadsereg vs. Fehér Hadsereg)",
            "options": ["Orosz polgárháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Orosz polgárháború (1918-1921): Vörös Hadsereg vs. Fehér Hadsereg"
        },
        {
            "question": "Melyik háború zajlott 1919-1921 között? (Ír Köztársasági Hadsereg (IRA) vs. Brit erők)",
            "options": ["Ír függetlenségi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Ír függetlenségi háború (1919-1921): Ír Köztársasági Hadsereg (IRA) vs. Brit erők"
        },
        {
            "question": "Melyik háború zajlott 1919-1921 között? (Lengyelország vs. Szovjet-Oroszország)",
            "options": ["Lengyel–szovjet háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Lengyel–szovjet háború (1919-1921): Lengyelország vs. Szovjet-Oroszország"
        },
        {
            "question": "Melyik háború zajlott 1946-1949 között? (Görög Kormányhadsereg vs. Kommunista gerillák)",
            "options": ["Görög polgárháború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Görög polgárháború (1946-1949): Görög Kormányhadsereg vs. Kommunista gerillák"
        },
        {
            "question": "Melyik háború zajlott 1991-2001 között? (Jugoszlávia utódállamai (Szlovénia, Horvátország, Bosznia, Szerbia, Montenegró))",
            "options": ["Délszláv háborúk", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Délszláv háborúk (1991-2001): Jugoszlávia utódállamai (Szlovénia, Horvátország, Bosznia, Szerbia, Montenegró)"
        },
        {
            "question": "Melyik háború zajlott 1991 között? (Szlovén Területvédelem vs. Jugoszláv Néphadsereg)",
            "options": ["Szlovén függetlenségi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Szlovén függetlenségi háború (1991): Szlovén Területvédelem vs. Jugoszláv Néphadsereg"
        },
        {
            "question": "Melyik háború zajlott 1991-1995 között? (Horvátország vs. Jugoszláv Néphadsereg, Szerb milíciák)",
            "options": ["Horvát függetlenségi háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Horvát függetlenségi háború (1991-1995): Horvátország vs. Jugoszláv Néphadsereg, Szerb milíciák"
        },
        {
            "question": "Melyik háború zajlott 1992-1995 között? (Boszniai kormányerők vs. Boszniai szerbek, Boszniai horvátok)",
            "options": ["Boszniai háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Boszniai háború (1992-1995): Boszniai kormányerők vs. Boszniai szerbek, Boszniai horvátok"
        },
        {
            "question": "Melyik háború zajlott 1998-1999 között? (Koszovói Felszabadítási Hadsereg vs. Szerbia)",
            "options": ["Koszovói háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Koszovói háború (1998-1999): Koszovói Felszabadítási Hadsereg vs. Szerbia"
        }
    ],
    "világzászlók": [
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ad_Andorra.png",
            "options": ["Andorra", "Albania", "Austria", "Armenia"],
            "correct": 0,
            "explanation": "Ez Andorra zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ae_United_Arab_Emirates.png",
            "options": ["Saudi Arabia", "United Arab Emirates", "Qatar", "Kuwait"],
            "correct": 1,
            "explanation": "Ez az Egyesült Arab Emírségek zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/af_Afghanistan.png",
            "options": ["Pakistan", "Afghanistan", "Iran", "Iraq"],
            "correct": 1,
            "explanation": "Ez Afganisztán zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ar_Argentina.png",
            "options": ["Argentina", "Brazil", "Chile", "Uruguay"],
            "correct": 0,
            "explanation": "Ez Argentína zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/at_Austria.png",
            "options": ["Austria", "Hungary", "Slovakia", "Czechia"],
            "correct": 0,
            "explanation": "Ez Ausztria zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/au_Australia.png",
            "options": ["New Zealand", "Australia", "Fiji", "Papua New Guinea"],
            "correct": 1,
            "explanation": "Ez Ausztrália zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/az_Azerbaijan.png",
            "options": ["Georgia", "Azerbaijan", "Armenia", "Turkey"],
            "correct": 1,
            "explanation": "Ez Azerbajdzsán zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ba_Bosnia_and_Herzegovina.png",
            "options": ["Croatia", "Serbia", "Bosnia and Herzegovina", "Montenegro"],
            "correct": 2,
            "explanation": "Ez Bosznia-Hercegovina zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/be_Belgium.png",
            "options": ["Netherlands", "Belgium", "Luxembourg", "France"],
            "correct": 1,
            "explanation": "Ez Belgium zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/br_Brazil.png",
            "options": ["Argentina", "Brazil", "Chile", "Peru"],
            "correct": 1,
            "explanation": "Ez Brazília zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ca_Canada.png",
            "options": ["Canada", "United States", "Mexico", "Greenland"],
            "correct": 0,
            "explanation": "Ez Kanada zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ch_Switzerland.png",
            "options": ["Austria", "Switzerland", "Liechtenstein", "Germany"],
            "correct": 1,
            "explanation": "Ez Svájc zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/cn_China.png",
            "options": ["Japan", "China", "South Korea", "North Korea"],
            "correct": 1,
            "explanation": "Ez Kína zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/cz_Czechia.png",
            "options": ["Slovakia", "Czechia", "Poland", "Hungary"],
            "correct": 1,
            "explanation": "Ez Csehország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/de_Germany.png",
            "options": ["Germany", "Austria", "Belgium", "Netherlands"],
            "correct": 0,
            "explanation": "Ez Németország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/dk_Denmark.png",
            "options": ["Norway", "Denmark", "Sweden", "Finland"],
            "correct": 1,
            "explanation": "Ez Dánia zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/eg_Egypt.png",
            "options": ["Egypt", "Libya", "Sudan", "Ethiopia"],
            "correct": 0,
            "explanation": "Ez Egyiptom zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/es_Spain.png",
            "options": ["Portugal", "Spain", "France", "Italy"],
            "correct": 1,
            "explanation": "Ez Spanyolország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/fi_Finland.png",
            "options": ["Norway", "Sweden", "Finland", "Denmark"],
            "correct": 2,
            "explanation": "Ez Finnország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/fr_France.png",
            "options": ["Belgium", "France", "Netherlands", "Luxembourg"],
            "correct": 1,
            "explanation": "Ez Franciaország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/gb_United_Kingdom.png",
            "options": ["Ireland", "United Kingdom", "Scotland", "Wales"],
            "correct": 1,
            "explanation": "Ez az Egyesült Királyság zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/gr_Greece.png",
            "options": ["Greece", "Cyprus", "Turkey", "Bulgaria"],
            "correct": 0,
            "explanation": "Ez Görögország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/hu_Hungary.png",
            "options": ["Austria", "Hungary", "Slovakia", "Romania"],
            "correct": 1,
            "explanation": "Ez Magyarország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/in_India.png",
            "options": ["Pakistan", "India", "Bangladesh", "Sri Lanka"],
            "correct": 1,
            "explanation": "Ez India zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ie_Ireland.png",
            "options": ["Ireland", "United Kingdom", "Scotland", "Wales"],
            "correct": 0,
            "explanation": "Ez Írország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/it_Italy.png",
            "options": ["Spain", "France", "Italy", "Greece"],
            "correct": 2,
            "explanation": "Ez Olaszország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/jp_Japan.png",
            "options": ["China", "Japan", "South Korea", "North Korea"],
            "correct": 1,
            "explanation": "Ez Japán zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/mx_Mexico.png",
            "options": ["Mexico", "United States", "Canada", "Guatemala"],
            "correct": 0,
            "explanation": "Ez Mexikó zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/nl_Netherlands.png",
            "options": ["Belgium", "Netherlands", "Luxembourg", "Germany"],
            "correct": 1,
            "explanation": "Ez Hollandia zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/no_Norway.png",
            "options": ["Norway", "Sweden", "Denmark", "Finland"],
            "correct": 0,
            "explanation": "Ez Norvégia zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/pl_Poland.png",
            "options": ["Poland", "Czechia", "Slovakia", "Hungary"],
            "correct": 0,
            "explanation": "Ez Lengyelország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/pt_Portugal.png",
            "options": ["Spain", "Portugal", "France", "Italy"],
            "correct": 1,
            "explanation": "Ez Portugália zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ru_Russia.png",
            "options": ["Ukraine", "Russia", "Belarus", "Poland"],
            "correct": 1,
            "explanation": "Ez Oroszország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/se_Sweden.png",
            "options": ["Norway", "Sweden", "Denmark", "Finland"],
            "correct": 1,
            "explanation": "Ez Svédország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/tr_Turkey.png",
            "options": ["Greece", "Turkey", "Bulgaria", "Romania"],
            "correct": 1,
            "explanation": "Ez Törökország zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/ua_Ukraine.png",
            "options": ["Ukraine", "Russia", "Belarus", "Poland"],
            "correct": 0,
            "explanation": "Ez Ukrajna zászlaja."
        },
        {
            "question": "Ez a zászló melyik országhoz tartozik?",
            "logo_path": "../world_flags_project/data/flags/us_United_States.png",
            "options": ["Canada", "United States", "Mexico", "Cuba"],
            "correct": 1,
            "explanation": "Ez az Egyesült Államok zászlaja."
        }
    ],
    "sport_logók": [
        # NFL TEAMS (32 teams)
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/ARI_Cardinals.png",
            "options": ["Arizona Cardinals", "Atlanta Falcons", "New Orleans Saints", "Tampa Bay Buccaneers"],
            "correct": 0,
            "explanation": "Ez az Arizona Cardinals (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/ATL_Falcons.png",
            "options": ["Carolina Panthers", "Atlanta Falcons", "New Orleans Saints", "Tampa Bay Buccaneers"],
            "correct": 1,
            "explanation": "Ez az Atlanta Falcons (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/BAL_Ravens.png",
            "options": ["Baltimore Ravens", "Pittsburgh Steelers", "Cleveland Browns", "Cincinnati Bengals"],
            "correct": 0,
            "explanation": "Ez a Baltimore Ravens (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/BUF_Bills.png",
            "options": ["Buffalo Bills", "New England Patriots", "Miami Dolphins", "New York Jets"],
            "correct": 0,
            "explanation": "Ez a Buffalo Bills (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/CAR_Panthers.png",
            "options": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
            "correct": 1,
            "explanation": "Ez a Carolina Panthers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/CHI_Bears.png",
            "options": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
            "correct": 0,
            "explanation": "Ez a Chicago Bears (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/CIN_Bengals.png",
            "options": ["Pittsburgh Steelers", "Cleveland Browns", "Cincinnati Bengals", "Baltimore Ravens"],
            "correct": 2,
            "explanation": "Ez a Cincinnati Bengals (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/CLE_Browns.png",
            "options": ["Pittsburgh Steelers", "Cleveland Browns", "Cincinnati Bengals", "Baltimore Ravens"],
            "correct": 1,
            "explanation": "Ez a Cleveland Browns (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/DAL_Cowboys.png",
            "options": ["Dallas Cowboys", "Houston Texans", "New York Giants", "Washington Commanders"],
            "correct": 0,
            "explanation": "Ez a Dallas Cowboys (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/DEN_Broncos.png",
            "options": ["Denver Broncos", "Kansas City Chiefs", "Las Vegas Raiders", "Los Angeles Chargers"],
            "correct": 0,
            "explanation": "Ez a Denver Broncos (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/DET_Lions.png",
            "options": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
            "correct": 1,
            "explanation": "Ez a Detroit Lions (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/GB_Packers.png",
            "options": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
            "correct": 2,
            "explanation": "Ez a Green Bay Packers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/HOU_Texans.png",
            "options": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
            "correct": 0,
            "explanation": "Ez a Houston Texans (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/IND_Colts.png",
            "options": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
            "correct": 1,
            "explanation": "Ez az Indianapolis Colts (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/JAX_Jaguars.png",
            "options": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
            "correct": 2,
            "explanation": "Ez a Jacksonville Jaguars (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/KC_Chiefs.png",
            "options": ["Kansas City Chiefs", "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers"],
            "correct": 0,
            "explanation": "Ez a Kansas City Chiefs (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/LA_Rams.png",
            "options": ["Los Angeles Rams", "Arizona Cardinals", "San Francisco 49ers", "Seattle Seahawks"],
            "correct": 0,
            "explanation": "Ez a Los Angeles Rams (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/LAC_Chargers.png",
            "options": ["Kansas City Chiefs", "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers"],
            "correct": 3,
            "explanation": "Ez a Los Angeles Chargers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/LV_Raiders.png",
            "options": ["Kansas City Chiefs", "Denver Broncos", "Las Vegas Raiders", "Los Angeles Chargers"],
            "correct": 2,
            "explanation": "Ez a Las Vegas Raiders (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/MIA_Dolphins.png",
            "options": ["Buffalo Bills", "New England Patriots", "Miami Dolphins", "New York Jets"],
            "correct": 2,
            "explanation": "Ez a Miami Dolphins (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/MIN_Vikings.png",
            "options": ["Chicago Bears", "Detroit Lions", "Green Bay Packers", "Minnesota Vikings"],
            "correct": 3,
            "explanation": "Ez a Minnesota Vikings (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/NE_Patriots.png",
            "options": ["Buffalo Bills", "New England Patriots", "Miami Dolphins", "New York Jets"],
            "correct": 1,
            "explanation": "Ez a New England Patriots (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/NO_Saints.png",
            "options": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
            "correct": 2,
            "explanation": "Ez a New Orleans Saints (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/NYG_Giants.png",
            "options": ["New York Giants", "Philadelphia Eagles", "Dallas Cowboys", "Washington Commanders"],
            "correct": 0,
            "explanation": "Ez a New York Giants (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/NYJ_Jets.png",
            "options": ["Buffalo Bills", "New England Patriots", "Miami Dolphins", "New York Jets"],
            "correct": 3,
            "explanation": "Ez a New York Jets (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/PHI_Eagles.png",
            "options": ["New York Giants", "Philadelphia Eagles", "Dallas Cowboys", "Washington Commanders"],
            "correct": 1,
            "explanation": "Ez a Philadelphia Eagles (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/PIT_Steelers.png",
            "options": ["Pittsburgh Steelers", "Cleveland Browns", "Cincinnati Bengals", "Baltimore Ravens"],
            "correct": 0,
            "explanation": "Ez a Pittsburgh Steelers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/SEA_Seahawks.png",
            "options": ["Los Angeles Rams", "Arizona Cardinals", "San Francisco 49ers", "Seattle Seahawks"],
            "correct": 3,
            "explanation": "Ez a Seattle Seahawks (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/SF_49ers.png",
            "options": ["Los Angeles Rams", "Arizona Cardinals", "San Francisco 49ers", "Seattle Seahawks"],
            "correct": 2,
            "explanation": "Ez a San Francisco 49ers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/TB_Buccaneers.png",
            "options": ["Atlanta Falcons", "Carolina Panthers", "New Orleans Saints", "Tampa Bay Buccaneers"],
            "correct": 3,
            "explanation": "Ez a Tampa Bay Buccaneers (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/TEN_Titans.png",
            "options": ["Houston Texans", "Indianapolis Colts", "Jacksonville Jaguars", "Tennessee Titans"],
            "correct": 3,
            "explanation": "Ez a Tennessee Titans (NFL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nfl_logos_flat/WAS_Commanders.png",
            "options": ["New York Giants", "Philadelphia Eagles", "Dallas Cowboys", "Washington Commanders"],
            "correct": 3,
            "explanation": "Ez a Washington Commanders (NFL) logója."
        },
        # NBA TEAMS (30 teams)
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612737_ATL_Hawks.png",
            "options": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic"],
            "correct": 0,
            "explanation": "Ez az Atlanta Hawks (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612738_BOS_Celtics.png",
            "options": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers"],
            "correct": 0,
            "explanation": "Ez a Boston Celtics (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612751_BKN_Nets.png",
            "options": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers"],
            "correct": 1,
            "explanation": "Ez a Brooklyn Nets (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612766_CHA_Hornets.png",
            "options": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic"],
            "correct": 1,
            "explanation": "Ez a Charlotte Hornets (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612741_CHI_Bulls.png",
            "options": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers"],
            "correct": 0,
            "explanation": "Ez a Chicago Bulls (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612739_CLE_Cavaliers.png",
            "options": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers"],
            "correct": 1,
            "explanation": "Ez a Cleveland Cavaliers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612742_DAL_Mavericks.png",
            "options": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans"],
            "correct": 0,
            "explanation": "Ez a Dallas Mavericks (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612743_DEN_Nuggets.png",
            "options": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers"],
            "correct": 0,
            "explanation": "Ez a Denver Nuggets (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612765_DET_Pistons.png",
            "options": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers"],
            "correct": 2,
            "explanation": "Ez a Detroit Pistons (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612744_GSW_Warriors.png",
            "options": ["Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns"],
            "correct": 0,
            "explanation": "Ez a Golden State Warriors (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612745_HOU_Rockets.png",
            "options": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans"],
            "correct": 1,
            "explanation": "Ez a Houston Rockets (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612754_IND_Pacers.png",
            "options": ["Chicago Bulls", "Cleveland Cavaliers", "Detroit Pistons", "Indiana Pacers"],
            "correct": 3,
            "explanation": "Ez az Indiana Pacers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612746_LAC_Clippers.png",
            "options": ["Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns"],
            "correct": 1,
            "explanation": "Ez a Los Angeles Clippers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612747_LAL_Lakers.png",
            "options": ["Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns"],
            "correct": 2,
            "explanation": "Ez a Los Angeles Lakers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612763_MEM_Grizzlies.png",
            "options": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans"],
            "correct": 2,
            "explanation": "Ez a Memphis Grizzlies (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612748_MIA_Heat.png",
            "options": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic"],
            "correct": 2,
            "explanation": "Ez a Miami Heat (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612749_MIL_Bucks.png",
            "options": ["Chicago Bulls", "Cleveland Cavaliers", "Milwaukee Bucks", "Indiana Pacers"],
            "correct": 2,
            "explanation": "Ez a Milwaukee Bucks (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612750_MIN_Timberwolves.png",
            "options": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers"],
            "correct": 1,
            "explanation": "Ez a Minnesota Timberwolves (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612740_NOP_Pelicans.png",
            "options": ["Dallas Mavericks", "Houston Rockets", "Memphis Grizzlies", "New Orleans Pelicans"],
            "correct": 3,
            "explanation": "Ez a New Orleans Pelicans (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612752_NYK_Knicks.png",
            "options": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers"],
            "correct": 2,
            "explanation": "Ez a New York Knicks (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612760_OKC_Thunder.png",
            "options": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers"],
            "correct": 2,
            "explanation": "Ez az Oklahoma City Thunder (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612753_ORL_Magic.png",
            "options": ["Atlanta Hawks", "Charlotte Hornets", "Miami Heat", "Orlando Magic"],
            "correct": 3,
            "explanation": "Ez az Orlando Magic (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612755_PHI_76ers.png",
            "options": ["Boston Celtics", "Brooklyn Nets", "New York Knicks", "Philadelphia 76ers"],
            "correct": 3,
            "explanation": "Ez a Philadelphia 76ers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612756_PHX_Suns.png",
            "options": ["Golden State Warriors", "Los Angeles Clippers", "Los Angeles Lakers", "Phoenix Suns"],
            "correct": 3,
            "explanation": "Ez a Phoenix Suns (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612757_POR_Trail Blazers.png",
            "options": ["Denver Nuggets", "Minnesota Timberwolves", "Oklahoma City Thunder", "Portland Trail Blazers"],
            "correct": 3,
            "explanation": "Ez a Portland Trail Blazers (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612758_SAC_Kings.png",
            "options": ["Golden State Warriors", "Los Angeles Clippers", "Sacramento Kings", "Phoenix Suns"],
            "correct": 2,
            "explanation": "Ez a Sacramento Kings (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612759_SAS_Spurs.png",
            "options": ["Dallas Mavericks", "Houston Rockets", "San Antonio Spurs", "New Orleans Pelicans"],
            "correct": 2,
            "explanation": "Ez a San Antonio Spurs (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612761_TOR_Raptors.png",
            "options": ["Boston Celtics", "Brooklyn Nets", "Toronto Raptors", "Philadelphia 76ers"],
            "correct": 2,
            "explanation": "Ez a Toronto Raptors (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612762_UTA_Jazz.png",
            "options": ["Denver Nuggets", "Minnesota Timberwolves", "Utah Jazz", "Portland Trail Blazers"],
            "correct": 2,
            "explanation": "Ez a Utah Jazz (NBA) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nba_logos_fixed/1610612764_WAS_Wizards.png",
            "options": ["Atlanta Hawks", "Charlotte Hornets", "Washington Wizards", "Orlando Magic"],
            "correct": 2,
            "explanation": "Ez a Washington Wizards (NBA) logója."
        },
        # MLB TEAMS (30 teams)
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/108_Angels.png",
            "options": ["Los Angeles Angels", "Oakland Athletics", "Seattle Mariners", "Texas Rangers"],
            "correct": 0,
            "explanation": "Ez a Los Angeles Angels (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/109_Diamondbacks.png",
            "options": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres"],
            "correct": 0,
            "explanation": "Ez az Arizona Diamondbacks (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/110_Orioles.png",
            "options": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays"],
            "correct": 0,
            "explanation": "Ez a Baltimore Orioles (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/111_Red Sox.png",
            "options": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays"],
            "correct": 1,
            "explanation": "Ez a Boston Red Sox (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/112_Cubs.png",
            "options": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates"],
            "correct": 0,
            "explanation": "Ez a Chicago Cubs (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/113_Reds.png",
            "options": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates"],
            "correct": 1,
            "explanation": "Ez a Cincinnati Reds (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/114_Guardians.png",
            "options": ["Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
            "correct": 0,
            "explanation": "Ez a Cleveland Guardians (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/115_Rockies.png",
            "options": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres"],
            "correct": 1,
            "explanation": "Ez a Colorado Rockies (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/116_Tigers.png",
            "options": ["Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
            "correct": 1,
            "explanation": "Ez a Detroit Tigers (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/117_Astros.png",
            "options": ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners"],
            "correct": 0,
            "explanation": "Ez a Houston Astros (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/118_Royals.png",
            "options": ["Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
            "correct": 2,
            "explanation": "Ez a Kansas City Royals (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/119_Dodgers.png",
            "options": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres"],
            "correct": 2,
            "explanation": "Ez a Los Angeles Dodgers (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/120_Nationals.png",
            "options": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Washington Nationals"],
            "correct": 3,
            "explanation": "Ez a Washington Nationals (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/121_Mets.png",
            "options": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies"],
            "correct": 2,
            "explanation": "Ez a New York Mets (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/133_Athletics.png",
            "options": ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners"],
            "correct": 2,
            "explanation": "Ez az Oakland Athletics (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/134_Pirates.png",
            "options": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates"],
            "correct": 3,
            "explanation": "Ez a Pittsburgh Pirates (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/135_Padres.png",
            "options": ["Arizona Diamondbacks", "Colorado Rockies", "Los Angeles Dodgers", "San Diego Padres"],
            "correct": 3,
            "explanation": "Ez a San Diego Padres (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/136_Mariners.png",
            "options": ["Houston Astros", "Los Angeles Angels", "Oakland Athletics", "Seattle Mariners"],
            "correct": 3,
            "explanation": "Ez a Seattle Mariners (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/137_Giants.png",
            "options": ["Arizona Diamondbacks", "Los Angeles Dodgers", "San Francisco Giants", "San Diego Padres"],
            "correct": 2,
            "explanation": "Ez a San Francisco Giants (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/138_Cardinals.png",
            "options": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "St. Louis Cardinals"],
            "correct": 3,
            "explanation": "Ez a St. Louis Cardinals (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/139_Rays.png",
            "options": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays"],
            "correct": 3,
            "explanation": "Ez a Tampa Bay Rays (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/140_Rangers.png",
            "options": ["Houston Astros", "Los Angeles Angels", "Seattle Mariners", "Texas Rangers"],
            "correct": 3,
            "explanation": "Ez a Texas Rangers (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/141_Blue Jays.png",
            "options": ["Baltimore Orioles", "Boston Red Sox", "Toronto Blue Jays", "Tampa Bay Rays"],
            "correct": 2,
            "explanation": "Ez a Toronto Blue Jays (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/142_Twins.png",
            "options": ["Cleveland Guardians", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
            "correct": 3,
            "explanation": "Ez a Minnesota Twins (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/143_Phillies.png",
            "options": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies"],
            "correct": 3,
            "explanation": "Ez a Philadelphia Phillies (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/144_Braves.png",
            "options": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies"],
            "correct": 0,
            "explanation": "Ez az Atlanta Braves (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/145_White Sox.png",
            "options": ["Chicago White Sox", "Detroit Tigers", "Kansas City Royals", "Minnesota Twins"],
            "correct": 0,
            "explanation": "Ez a Chicago White Sox (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/146_Marlins.png",
            "options": ["Atlanta Braves", "Miami Marlins", "New York Mets", "Philadelphia Phillies"],
            "correct": 1,
            "explanation": "Ez a Miami Marlins (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/147_Yankees.png",
            "options": ["Baltimore Orioles", "Boston Red Sox", "New York Yankees", "Tampa Bay Rays"],
            "correct": 2,
            "explanation": "Ez a New York Yankees (MLB) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../mlb_logos_flat/158_Brewers.png",
            "options": ["Chicago Cubs", "Cincinnati Reds", "Milwaukee Brewers", "Pittsburgh Pirates"],
            "correct": 2,
            "explanation": "Ez a Milwaukee Brewers (MLB) logója."
        },
        # NHL TEAMS (32 teams)
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/1_NJD_New_Jersey_Devils.png",
            "options": ["New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers"],
            "correct": 0,
            "explanation": "Ez a New Jersey Devils (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/2_NYI_New_York_Islanders.png",
            "options": ["New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers"],
            "correct": 1,
            "explanation": "Ez a New York Islanders (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/3_NYR_New_York_Rangers.png",
            "options": ["New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers"],
            "correct": 2,
            "explanation": "Ez a New York Rangers (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/4_PHI_Philadelphia_Flyers.png",
            "options": ["New Jersey Devils", "New York Islanders", "New York Rangers", "Philadelphia Flyers"],
            "correct": 3,
            "explanation": "Ez a Philadelphia Flyers (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/5_PIT_Pittsburgh_Penguins.png",
            "options": ["Pittsburgh Penguins", "Boston Bruins", "Buffalo Sabres", "Montreal Canadiens"],
            "correct": 0,
            "explanation": "Ez a Pittsburgh Penguins (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/6_BOS_Boston_Bruins.png",
            "options": ["Pittsburgh Penguins", "Boston Bruins", "Buffalo Sabres", "Montreal Canadiens"],
            "correct": 1,
            "explanation": "Ez a Boston Bruins (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/7_BUF_Buffalo_Sabres.png",
            "options": ["Pittsburgh Penguins", "Boston Bruins", "Buffalo Sabres", "Montreal Canadiens"],
            "correct": 2,
            "explanation": "Ez a Buffalo Sabres (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/8_MTL_Montréal_Canadiens.png",
            "options": ["Pittsburgh Penguins", "Boston Bruins", "Buffalo Sabres", "Montreal Canadiens"],
            "correct": 3,
            "explanation": "Ez a Montreal Canadiens (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/9_OTT_Ottawa_Senators.png",
            "options": ["Ottawa Senators", "Toronto Maple Leafs", "Carolina Hurricanes", "Florida Panthers"],
            "correct": 0,
            "explanation": "Ez az Ottawa Senators (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/10_TOR_Toronto_Maple_Leafs.png",
            "options": ["Ottawa Senators", "Toronto Maple Leafs", "Carolina Hurricanes", "Florida Panthers"],
            "correct": 1,
            "explanation": "Ez a Toronto Maple Leafs (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/12_CAR_Carolina_Hurricanes.png",
            "options": ["Ottawa Senators", "Toronto Maple Leafs", "Carolina Hurricanes", "Florida Panthers"],
            "correct": 2,
            "explanation": "Ez a Carolina Hurricanes (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/13_FLA_Florida_Panthers.png",
            "options": ["Ottawa Senators", "Toronto Maple Leafs", "Carolina Hurricanes", "Florida Panthers"],
            "correct": 3,
            "explanation": "Ez a Florida Panthers (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/14_TBL_Tampa_Bay_Lightning.png",
            "options": ["Tampa Bay Lightning", "Washington Capitals", "Chicago Blackhawks", "Detroit Red Wings"],
            "correct": 0,
            "explanation": "Ez a Tampa Bay Lightning (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/15_WSH_Washington_Capitals.png",
            "options": ["Tampa Bay Lightning", "Washington Capitals", "Chicago Blackhawks", "Detroit Red Wings"],
            "correct": 1,
            "explanation": "Ez a Washington Capitals (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/16_CHI_Chicago_Blackhawks.png",
            "options": ["Tampa Bay Lightning", "Washington Capitals", "Chicago Blackhawks", "Detroit Red Wings"],
            "correct": 2,
            "explanation": "Ez a Chicago Blackhawks (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/17_DET_Detroit_Red_Wings.png",
            "options": ["Tampa Bay Lightning", "Washington Capitals", "Chicago Blackhawks", "Detroit Red Wings"],
            "correct": 3,
            "explanation": "Ez a Detroit Red Wings (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/18_NSH_Nashville_Predators.png",
            "options": ["Nashville Predators", "St. Louis Blues", "Calgary Flames", "Colorado Avalanche"],
            "correct": 0,
            "explanation": "Ez a Nashville Predators (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/19_STL_St._Louis_Blues.png",
            "options": ["Nashville Predators", "St. Louis Blues", "Calgary Flames", "Colorado Avalanche"],
            "correct": 1,
            "explanation": "Ez a St. Louis Blues (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/20_CGY_Calgary_Flames.png",
            "options": ["Nashville Predators", "St. Louis Blues", "Calgary Flames", "Colorado Avalanche"],
            "correct": 2,
            "explanation": "Ez a Calgary Flames (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/21_COL_Colorado_Avalanche.png",
            "options": ["Nashville Predators", "St. Louis Blues", "Calgary Flames", "Colorado Avalanche"],
            "correct": 3,
            "explanation": "Ez a Colorado Avalanche (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/22_EDM_Edmonton_Oilers.png",
            "options": ["Edmonton Oilers", "Vancouver Canucks", "Anaheim Ducks", "Dallas Stars"],
            "correct": 0,
            "explanation": "Ez az Edmonton Oilers (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/23_VAN_Vancouver_Canucks.png",
            "options": ["Edmonton Oilers", "Vancouver Canucks", "Anaheim Ducks", "Dallas Stars"],
            "correct": 1,
            "explanation": "Ez a Vancouver Canucks (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/24_ANA_Anaheim_Ducks.png",
            "options": ["Edmonton Oilers", "Vancouver Canucks", "Anaheim Ducks", "Dallas Stars"],
            "correct": 2,
            "explanation": "Ez az Anaheim Ducks (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/25_DAL_Dallas_Stars.png",
            "options": ["Edmonton Oilers", "Vancouver Canucks", "Anaheim Ducks", "Dallas Stars"],
            "correct": 3,
            "explanation": "Ez a Dallas Stars (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/26_LAK_Los_Angeles_Kings.png",
            "options": ["Los Angeles Kings", "San Jose Sharks", "Columbus Blue Jackets", "Minnesota Wild"],
            "correct": 0,
            "explanation": "Ez a Los Angeles Kings (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/28_SJS_San_Jose_Sharks.png",
            "options": ["Los Angeles Kings", "San Jose Sharks", "Columbus Blue Jackets", "Minnesota Wild"],
            "correct": 1,
            "explanation": "Ez a San Jose Sharks (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/29_CBJ_Columbus_Blue_Jackets.png",
            "options": ["Los Angeles Kings", "San Jose Sharks", "Columbus Blue Jackets", "Minnesota Wild"],
            "correct": 2,
            "explanation": "Ez a Columbus Blue Jackets (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/30_MIN_Minnesota_Wild.png",
            "options": ["Los Angeles Kings", "San Jose Sharks", "Columbus Blue Jackets", "Minnesota Wild"],
            "correct": 3,
            "explanation": "Ez a Minnesota Wild (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/52_WPG_Winnipeg_Jets.png",
            "options": ["Winnipeg Jets", "Arizona Coyotes", "Vegas Golden Knights", "Seattle Kraken"],
            "correct": 0,
            "explanation": "Ez a Winnipeg Jets (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/53_ARI_Arizona_Coyotes.png",
            "options": ["Winnipeg Jets", "Arizona Coyotes", "Vegas Golden Knights", "Seattle Kraken"],
            "correct": 1,
            "explanation": "Ez az Arizona Coyotes (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/54_VGK_Vegas_Golden_Knights.png",
            "options": ["Winnipeg Jets", "Arizona Coyotes", "Vegas Golden Knights", "Seattle Kraken"],
            "correct": 2,
            "explanation": "Ez a Vegas Golden Knights (NHL) logója."
        },
        {
            "question": "Ez a logó melyik csapathoz tartozik?",
            "logo_path": "../nhl_logos_new/55_SEA_Seattle_Kraken.png",
            "options": ["Winnipeg Jets", "Arizona Coyotes", "Vegas Golden Knights", "Seattle Kraken"],
            "correct": 3,
            "explanation": "Ez a Seattle Kraken (NHL) logója."
        }
    ],
    "hegységek": [
        {
            "question": "Mi a világ legmagasabb hegycsúcsa?",
            "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"],
            "correct": 1,
            "explanation": "A Mount Everest (8849 m) a világ legmagasabb hegycsúcsa a Himalájában."
        },
        {
            "question": "Melyik kontinens legmagasabb csúcsa a Mount McKinley (Denali)?",
            "options": ["Ázsia", "Európa", "Afrika", "Észak-Amerika"],
            "correct": 3,
            "explanation": "A Denali (6190 m) Észak-Amerika legmagasabb csúcsa Alaszkában."
        },
        {
            "question": "Mi Afrika legmagasabb hegycsúcsa?",
            "options": ["Mount Kenya", "Kilimandzsáró", "Mount Stanley", "Ras Dashen"],
            "correct": 1,
            "explanation": "A Kilimandzsáró (5895 m) Afrika legmagasabb csúcsa Tanzániában."
        },
        {
            "question": "Melyik hegységben található a Mont Blanc?",
            "options": ["Pireneusok", "Alpok", "Kárpátok", "Appeninek"],
            "correct": 1,
            "explanation": "A Mont Blanc (4809 m) az Alpok legmagasabb csúcsa."
        },
        {
            "question": "Mi Dél-Amerika legmagasabb hegycsúcsa?",
            "options": ["Aconcagua", "Ojos del Salado", "Bonete", "Tres Cruces"],
            "correct": 0,
            "explanation": "Az Aconcagua (6961 m) Dél-Amerika legmagasabb csúcsa Argentínában."
        },
        {
            "question": "Melyik hegységben található a K2?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A K2 (8611 m) a Karakorum hegységben található, a világ második legmagasabb csúcsa."
        },
        {
            "question": "Mi Európa legmagasabb hegycsúcsa?",
            "options": ["Mont Blanc", "Mount Elbrus", "Dykh-Tau", "Mount Blanc de Courmayeur"],
            "correct": 1,
            "explanation": "A Mount Elbrus (5642 m) Európa legmagasabb csúcsa a Kaukázusban."
        },
        {
            "question": "Melyik hegységben található az Annapurna?",
            "options": ["Karakorum", "Himalája", "Hindu Kush", "Kun Lun"],
            "correct": 1,
            "explanation": "Az Annapurna (8091 m) a Himalájában található, Nepálban."
        },
        {
            "question": "Mi Ausztrália legmagasabb hegycsúcsa?",
            "options": ["Mount Townsend", "Mount Twynam", "Mount Kosciuszko", "Mount Bogong"],
            "correct": 2,
            "explanation": "A Mount Kosciuszko (2228 m) Ausztrália legmagasabb csúcsa."
        },
        {
            "question": "Melyik országban található a Matterhorn?",
            "options": ["Ausztria", "Svájc-Olaszország", "Franciaország", "Németország"],
            "correct": 1,
            "explanation": "A Matterhorn (4478 m) a svájci-olasz határon található az Alpokban."
        },
        {
            "question": "Mi a világ harmadik legmagasabb hegycsúcsa?",
            "options": ["K2", "Kangchenjunga", "Lhotse", "Makalu"],
            "correct": 1,
            "explanation": "A Kangchenjunga (8586 m) a világ harmadik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Broad Peak?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Broad Peak (8051 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ negyedik legmagasabb hegycsúcsa?",
            "options": ["Lhotse", "Makalu", "Cho Oyu", "Dhaulagiri"],
            "correct": 0,
            "explanation": "A Lhotse (8516 m) a világ negyedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Gasherbrum I?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Gasherbrum I (8080 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ ötödik legmagasabb hegycsúcsa?",
            "options": ["Makalu", "Cho Oyu", "Dhaulagiri", "Manaslu"],
            "correct": 0,
            "explanation": "A Makalu (8485 m) a világ ötödik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Gasherbrum II?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Gasherbrum II (8035 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ hatodik legmagasabb hegycsúcsa?",
            "options": ["Cho Oyu", "Dhaulagiri", "Manaslu", "Nanga Parbat"],
            "correct": 0,
            "explanation": "A Cho Oyu (8188 m) a világ hatodik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Shishapangma?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 0,
            "explanation": "A Shishapangma (8027 m) a Himalájában található."
        },
        {
            "question": "Mi a világ hetedik legmagasabb hegycsúcsa?",
            "options": ["Dhaulagiri", "Manaslu", "Nanga Parbat", "Annapurna"],
            "correct": 0,
            "explanation": "A Dhaulagiri (8167 m) a világ hetedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Nanga Parbat?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Nanga Parbat (8126 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ nyolcadik legmagasabb hegycsúcsa?",
            "options": ["Manaslu", "Nanga Parbat", "Annapurna", "Broad Peak"],
            "correct": 0,
            "explanation": "A Manaslu (8163 m) a világ nyolcadik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Hidden Peak?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Hidden Peak (Gasherbrum I, 8080 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ kilencedik legmagasabb hegycsúcsa?",
            "options": ["Nanga Parbat", "Annapurna", "Broad Peak", "Gasherbrum I"],
            "correct": 0,
            "explanation": "A Nanga Parbat (8126 m) a világ kilencedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Gyachung Kang?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 0,
            "explanation": "A Gyachung Kang (7952 m) a Himalájában található."
        },
        {
            "question": "Mi a világ tizedik legmagasabb hegycsúcsa?",
            "options": ["Annapurna", "Broad Peak", "Gasherbrum I", "Shishapangma"],
            "correct": 0,
            "explanation": "Az Annapurna (8091 m) a világ tizedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Distaghil Sar?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Distaghil Sar (7885 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenegyedik legmagasabb hegycsúcsa?",
            "options": ["Broad Peak", "Gasherbrum I", "Shishapangma", "Gyachung Kang"],
            "correct": 0,
            "explanation": "A Broad Peak (8051 m) a világ tizenegyedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Kunyang Chhish?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Kunyang Chhish (7852 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenkettedik legmagasabb hegycsúcsa?",
            "options": ["Gasherbrum I", "Shishapangma", "Gyachung Kang", "Distaghil Sar"],
            "correct": 0,
            "explanation": "A Gasherbrum I (8080 m) a világ tizenkettedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Masherbrum?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Masherbrum (7821 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenharmadik legmagasabb hegycsúcsa?",
            "options": ["Shishapangma", "Gyachung Kang", "Distaghil Sar", "Kunyang Chhish"],
            "correct": 0,
            "explanation": "A Shishapangma (8027 m) a világ tizenharmadik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Batura Sar?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Batura Sar (7795 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizennegyedik legmagasabb hegycsúcsa?",
            "options": ["Gyachung Kang", "Distaghil Sar", "Kunyang Chhish", "Masherbrum"],
            "correct": 0,
            "explanation": "A Gyachung Kang (7952 m) a világ tizennegyedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Rakaposhi?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Rakaposhi (7788 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenötödik legmagasabb hegycsúcsa?",
            "options": ["Distaghil Sar", "Kunyang Chhish", "Masherbrum", "Batura Sar"],
            "correct": 0,
            "explanation": "A Distaghil Sar (7885 m) a világ tizenötödik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Kanjut Sar?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Kanjut Sar (7760 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenhatodik legmagasabb hegycsúcsa?",
            "options": ["Kunyang Chhish", "Masherbrum", "Batura Sar", "Rakaposhi"],
            "correct": 0,
            "explanation": "A Kunyang Chhish (7852 m) a világ tizenhatodik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Saltoro Kangri?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Saltoro Kangri (7742 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenhetedik legmagasabb hegycsúcsa?",
            "options": ["Masherbrum", "Batura Sar", "Rakaposhi", "Kanjut Sar"],
            "correct": 0,
            "explanation": "A Masherbrum (7821 m) a világ tizenhetedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Chogolisa?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Chogolisa (7665 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizennyolcadik legmagasabb hegycsúcsa?",
            "options": ["Batura Sar", "Rakaposhi", "Kanjut Sar", "Saltoro Kangri"],
            "correct": 0,
            "explanation": "A Batura Sar (7795 m) a világ tizennyolcadik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Saser Kangri?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Saser Kangri (7672 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ tizenkilencedik legmagasabb hegycsúcsa?",
            "options": ["Rakaposhi", "Kanjut Sar", "Saltoro Kangri", "Chogolisa"],
            "correct": 0,
            "explanation": "A Rakaposhi (7788 m) a világ tizenkilencedik legmagasabb csúcsa."
        },
        {
            "question": "Melyik hegységben található a Mamostong Kangri?",
            "options": ["Himalája", "Karakorum", "Hindu Kush", "Pamír"],
            "correct": 1,
            "explanation": "A Mamostong Kangri (7516 m) a Karakorum hegységben található."
        },
        {
            "question": "Mi a világ huszadik legmagasabb hegycsúcsa?",
            "options": ["Kanjut Sar", "Saltoro Kangri", "Chogolisa", "Saser Kangri"],
            "correct": 0,
            "explanation": "A Kanjut Sar (7760 m) a világ huszadik legmagasabb csúcsa."
        }
    ]
}
}

def shuffle_options(question):
    """Megkeveri a válaszlehetőségeket és frissíti a helyes válasz indexét"""
    if 'options' not in question or 'correct' not in question:
        return question
    
    # Eredeti adatok mentése
    original_options = question['options'].copy()
    original_correct = question['correct']
    correct_answer = original_options[original_correct]
    
    # Válaszlehetőségek keverése
    shuffled_options = original_options.copy()
    random.shuffle(shuffled_options)
    
    # Helyes válasz új indexének megtalálása
    new_correct_index = shuffled_options.index(correct_answer)
    
    # Kérdés frissítése - új objektum létrehozása, nem módosítjuk az eredetit
    question_copy = question.copy()
    question_copy['options'] = shuffled_options
    question_copy['correct'] = new_correct_index
    
    return question_copy

def get_selected_questions(topic_question_counts):
    """Kiválasztott témakörökből témakörönként megadott számú kérdéseket választ"""
    all_questions = []
    
    for topic, num_questions in topic_question_counts.items():
        if topic in QUIZ_DATA_BY_TOPIC and num_questions > 0:
            topic_questions = QUIZ_DATA_BY_TOPIC[topic].copy()
            
            # Témakör kérdéseinek véletlenszerű keverése
            random.shuffle(topic_questions)
            
            # Ha kevesebb kérdés van, mint amennyit kérnek, adjuk vissza az összeset
            if len(topic_questions) <= num_questions:
                selected_questions = topic_questions
            else:
                # Véletlenszerű kiválasztás
                selected_questions = random.sample(topic_questions, num_questions)
            
            # Témakör hozzáadása minden kérdéshez és válaszlehetőségek keverése
            shuffled_questions = []
            for q in selected_questions:
                q["topic"] = topic
                shuffled_q = shuffle_options(q)  # Válaszlehetőségek keverése
                shuffled_questions.append(shuffled_q)
            
            all_questions.extend(shuffled_questions)
    
    # Teljes kérdéslista véletlenszerű keverése
    random.shuffle(all_questions)
    
    return all_questions

def reset_quiz(selected_questions):
    """Quiz újraindítása a kiválasztott kérdésekkel"""
    st.session_state.selected_questions = selected_questions
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.answers = []
    st.session_state.quiz_completed = False
    st.session_state.start_time = time.time()
    st.session_state.total_questions = len(st.session_state.selected_questions)

def main():
    # Kvíz állapot kezelése
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    
    # Ha a kvíz fut, akkor csak azt jelenítjük meg
    if st.session_state.quiz_started and 'selected_questions' in st.session_state and len(st.session_state.selected_questions) > 0:
        if st.session_state.quiz_completed:
            # Eredmények megjelenítése
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.success("🎉 Quiz Befejezve!")
                
                score_percentage = (st.session_state.score / st.session_state.total_questions) * 100
                
                st.metric("Végső Pontszám", f"{st.session_state.score}/{st.session_state.total_questions} ({score_percentage:.0f}%)")
                
                total_time = time.time() - st.session_state.start_time
                st.metric("Teljes idő", f"{total_time:.0f} másodperc")
                
                # Értékelés
                if score_percentage >= 80:
                    st.balloons()
                    st.success("🌟 Kiváló! Nagyszerű tudás!")
                elif score_percentage >= 60:
                    st.info("👍 Jó! Szép munka!")
                else:
                    st.warning("📚 Érdemes tanulni még!")
            
            # Új kvíz gomb
            if st.button("🔄 Új Kvíz", type="primary"):
                st.session_state.quiz_started = False
                st.session_state.selected_questions = []
                st.session_state.quiz_completed = False
                st.rerun()
            
            # Részletes eredmények
            st.markdown("---")
            st.header("📝 Részletes Eredmények")
            
            # Témakörök szerinti csoportosítás
            results_by_topic = {}
            for i, (question, answer) in enumerate(zip(st.session_state.selected_questions, st.session_state.answers)):
                topic = question.get("topic", "egyéb")
                if topic not in results_by_topic:
                    results_by_topic[topic] = []
                results_by_topic[topic].append((i, question, answer))
            
            for topic, topic_results in results_by_topic.items():
                topic_icon = {"földrajz": "🌍", "komolyzene": "🎼", "tudósok": "🔬", "mitológia": "🏛️", "állatok": "🦁", "sport_logók": "🏆", "hegységek": "🏔️", "us_államok": "🇺🇸", "világzászlók": "🏳️", "magyar_királyok": "👑", "háborúk": "⚔️", "drámák": "🎭"}.get(topic, "📋")
                if topic == "sport_logók":
                    topic_name = "Sport Logók"
                elif topic == "hegységek":
                    topic_name = "Hegységek & Csúcsok"
                elif topic == "us_államok":
                    topic_name = "US Államok"
                elif topic == "világzászlók":
                    topic_name = "Világzászlók"
                elif topic == "magyar_királyok":
                    topic_name = "Magyar Királyok"
                elif topic == "háborúk":
                    topic_name = "Háborúk"
                elif topic == "drámák":
                    topic_name = "Drámák"
                else:
                    topic_name = topic.title()
                
                with st.expander(f"{topic_icon} {topic_name} - {len(topic_results)} kérdés"):
                    for i, question, answer in topic_results:
                        is_correct = answer == question["correct"]
                        
                        st.markdown(f"**{i+1}. {question['question']}** {'✅' if is_correct else '❌'}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write(f"**Válaszod:** {question['options'][answer]}")
                        with col2:
                            st.write(f"**Helyes válasz:** {question['options'][question['correct']]}")
                        
                        st.info(f"💡 {question['explanation']}")
                        st.markdown("---")
        
        else:
            # Quiz folyamatban
            current_q = st.session_state.selected_questions[st.session_state.current_question]
            topic_icon = {"földrajz": "🌍", "komolyzene": "🎼", "tudósok": "🔬", "mitológia": "🏛️", "állatok": "🦁", "sport_logók": "🏆", "hegységek": "🏔️", "us_államok": "🇺🇸", "világzászlók": "🏳️", "magyar_királyok": "👑", "háborúk": "⚔️", "drámák": "🎭"}.get(current_q.get("topic", ""), "📋")
            
            # Progress és info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Kérdés", f"{st.session_state.current_question + 1}/{st.session_state.total_questions}")
            with col2:
                answered = len(st.session_state.answers)
                st.metric("Pontszám", f"{st.session_state.score}/{answered}")
            with col3:
                if st.session_state.current_question > 0:
                    elapsed = time.time() - st.session_state.start_time
                    st.metric("Eltelt idő", f"{elapsed:.0f}s")
            
            # Kérdés megjelenítése
            st.markdown(f"### {topic_icon} Kérdés {st.session_state.current_question + 1}")
            
            # Logó megjelenítése, ha van
            if 'logo_path' in current_q:
                logo_path = Path(current_q['logo_path'])
                if logo_path.exists():
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.image(str(logo_path), width=300, caption="")
                else:
                    st.warning(f"⚠️ Logó nem található: {current_q['logo_path']}")
            
            # Spotify embed megjelenítése, ha van
            if 'spotify_embed' in current_q:
                st.markdown("### 🎵 Hallgasd meg a zeneművet:")
                # A track ID kinyerése az URL-ből
                track_id = current_q['spotify_embed'].split('/track/')[1].split('?')[0]
                # Spotify embed teljes méretben, de minimális - csak lejátszó vezérlők
                play_button_url = f"https://open.spotify.com/embed/track/{track_id}?theme=black&size=small&hide_cover=1&hide_artist=1&hide_title=1&hide_metadata=1&hide_playlist=1"
                
                # CSS stílus a baloldal 50%-ának elrejtéséhez
                css_code = """
                <style>
                .spotify-embed-container {
                    position: relative;
                    width: 100%;
                    height: 80px;
                    margin: 0 auto;
                    overflow: hidden;
                    border-radius: 8px;
                }
                .spotify-embed-overlay-left {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: #764ba2;
                    z-index: 9999;
                    border-radius: 8px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    font-size: 18px;
                    text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
                    pointer-events: none;
                }
                .spotify-embed-container iframe {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    border-radius: 8px;
                    z-index: 1;
                }
                </style>
                """
                st.markdown(css_code, unsafe_allow_html=True)
                
                # Spotify embed konténer baloldali átfedő képpel
                html_code = f"""
                <div class="spotify-embed-container">
                    <iframe src="{play_button_url}" 
                            frameborder="0" 
                            allowtransparency="true" 
                            allow="encrypted-media">
                    </iframe>
                    <div class="spotify-embed-overlay-left">
                        🎵
                    </div>
                </div>
                """
                st.components.v1.html(html_code, height=80)
                st.markdown("---")
            
            # Kérdés szövege
            st.markdown(f"**{current_q['question']}**")
            
            # Válaszlehetőségek - már keverve vannak a get_selected_questions-ban
            selected_answer = st.radio(
                "Válassz egyet:",
                options=current_q['options'],
                key=f"question_{st.session_state.current_question}"
            )
            
            # Válasz beküldése
            if st.button("✅ Válasz Beküldése", type="primary"):
                # Válasz mentése - a kevert opciókban a helyes válasz már frissítve van
                answer_index = current_q['options'].index(selected_answer)
                st.session_state.answers.append(answer_index)
                
                # Pontszám frissítése
                if answer_index == current_q['correct']:
                    st.session_state.score += 1
                
                # Következő kérdés vagy kvíz befejezése
                st.session_state.current_question += 1
                
                if st.session_state.current_question >= len(st.session_state.selected_questions):
                    st.session_state.quiz_completed = True
                
                st.rerun()
        
        return
    
    # Témakör kiválasztó oldal (csak akkor jelenik meg, ha nincs aktív kvíz)
    topic_question_counts = {}
    total_questions = 0
    
    # Témakörök definíciói
    topics = [
        {"key": "földrajz", "icon": "🌍", "name": "Földrajz", "max_questions": len(QUIZ_DATA_BY_TOPIC["földrajz"])},
        {"key": "komolyzene", "icon": "🎼", "name": "Komolyzene", "max_questions": 10},
        {"key": "tudósok", "icon": "🔬", "name": "Tudósok", "max_questions": len(QUIZ_DATA_BY_TOPIC["tudósok"])},
        {"key": "mitológia", "icon": "🏛️", "name": "Mitológia", "max_questions": len(QUIZ_DATA_BY_TOPIC["mitológia"])},
        {"key": "állatok", "icon": "🦁", "name": "Különleges Állatok", "max_questions": len(QUIZ_DATA_BY_TOPIC["állatok"])},
        {"key": "sport_logók", "icon": "🏆", "name": "Sport Logók", "max_questions": 10},
        {"key": "hegységek", "icon": "🏔️", "name": "Hegységek & Csúcsok", "max_questions": len(QUIZ_DATA_BY_TOPIC["hegységek"])},
        {"key": "us_államok", "icon": "🇺🇸", "name": "US Államok", "max_questions": len(QUIZ_DATA_BY_TOPIC["us_államok"])},
        {"key": "világzászlók", "icon": "🏳️", "name": "Világzászlók", "max_questions": len(QUIZ_DATA_BY_TOPIC["világzászlók"])},
        {"key": "magyar_királyok", "icon": "👑", "name": "Magyar Királyok", "max_questions": len(QUIZ_DATA_BY_TOPIC["magyar_királyok"])},
        {"key": "háborúk", "icon": "⚔️", "name": "Háborúk", "max_questions": len(QUIZ_DATA_BY_TOPIC["háborúk"])},
        {"key": "drámák", "icon": "🎭", "name": "Drámák", "max_questions": len(QUIZ_DATA_BY_TOPIC["drámák"])}
    ]
    
    # Témakörök kiválasztása
    st.title("🧠 Advanced PDF Quiz Alkalmazás")
    st.markdown("**Válaszd ki a kívánt témaköröket:**")
    
    # Három oszlopos elrendezés a témaköröknek
    col1, col2, col3 = st.columns(3)
    
    for i, topic in enumerate(topics):
        col = col1 if i % 3 == 0 else col2 if i % 3 == 1 else col3
        
        with col:
            # Checkbox + logó + név formátum
            if st.checkbox(f"{topic['icon']} {topic['name']}", key=f"enable_{topic['key']}"):
                if topic['max_questions'] > 0:
                    questions = st.slider(
                        f"{topic['name']} kérdések:", 
                        min_value=0, 
                        max_value=topic['max_questions'], 
                        value=3 if topic['key'] in ['földrajz', 'komolyzene', 'sport_logók', 'hegységek', 'us_államok', 'világzászlók', 'magyar_királyok', 'háborúk', 'drámák'] else 2,
                        key=f"{topic['key']}_count"
                    )
                else:
                    st.warning("Nincs elérhető kérdés ebben a témakörben.")
                    questions = 0
                topic_question_counts[topic['key']] = questions
                total_questions += questions
            else:
                topic_question_counts[topic['key']] = 0
    
    # Összesítő információ
    if total_questions > 0:
        st.markdown("---")
        col_summary1, col_summary2, col_summary3 = st.columns([1, 2, 1])
        with col_summary2:
            st.subheader("📊 Összesítő")
            st.metric("Összes kérdés", total_questions)
            
            if total_questions > 10:
                st.warning("⚠️ Maximum 10 kérdés ajánlott!")
            
            # Kvíz indítás gomb
            if st.button("🚀 Kvíz Indítása", type="primary", key="start_quiz"):
                # Kérdések kiválasztása és kvíz inicializálása
                selected_questions = get_selected_questions(topic_question_counts)
                st.session_state.selected_questions = selected_questions
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.quiz_completed = False
                st.session_state.start_time = time.time()
                st.session_state.total_questions = len(selected_questions)
                st.session_state.quiz_started = True
                st.rerun()
    else:
        st.markdown("---")
        st.info("ℹ️ Válassz ki legalább egy témakört a kvíz indításához!")
        
        # Kezdő képernyő információ
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.info("""
            ### 👋 Üdvözöl az Advanced Quiz!
            
            **Új funkciók:**
            - 🎯 **Témakörönkénti beállítás**: Minden témakörre külön kérdésszám
            - 🔢 **Rugalmas kérdésszám**: 0-10 kérdés témakörönként
            - 📊 **Valós idejű összesítő**: Lásd az összes kérdés számát
            - 🎨 **Színes kategóriák**: Minden téma más ikonnal
            
            **Elérhető témakörök:**
            - 🌍 **Földrajz** (34 kérdés): Országok, fővárosok, hegyek, folyók + PDF adatok
            - 🎼 **Komolyzene** (67 kérdés): Zeneművek hallgatása Spotify-ban, zeneszerzők felismerése
            - 🔬 **Tudósok** (10 kérdés): Híres tudósok és felfedezések
            - 🏛️ **Mitológia** (60 kérdés): Görög, római és északi istenek, hősök és világok
            - 🦁 **Különleges Állatok** (10 kérdés): Ritka és egzotikus állatok
            - 🏆 **Sport Logók** (124 kérdés): NFL, NBA, MLB, NHL - összes csapat
            - 🏔️ **Hegységek & Csúcsok** (50 kérdés): Világ legmagasabb hegyei
            - 🇺🇸 **US Államok** (50 kérdés): Amerikai államok címerei felismerése
            - 🏳️ **Világzászlók** (40 kérdés): Országok zászlainak felismerése
            - 👑 **Magyar Királyok** (50 kérdés): Magyar királyok évszámokkal és leírásokkal
            - ⚔️ **Háborúk** (100 kérdés): Történelmi háborúk időpontokkal és szembenálló felekkel
            - 🎭 **Drámák** (30 kérdés): Shakespeare és Csehov drámák történetekkel és szereplőkkel
            
            **Használat:**
            1. Engedélyezd a kívánt témakörö(ke)t
            2. Állítsd be témakörönként a kérdések számát  
            3. Indítsd el a quiz-t!
            """)

if __name__ == "__main__":
    main() 