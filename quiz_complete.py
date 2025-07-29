import streamlit as st
import random

# Page config
st.set_page_config(
    page_title="Quiz Alkalmazás - Teljes Adatbázis",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state inicializálása
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'selected_topics' not in st.session_state:
    st.session_state.selected_topics = []

# Témakörök és logók - teljes lista
TOPICS_WITH_LOGOS = {
    "földrajz": {
        "name": "🌍 Földrajz",
        "description": "Országok, városok, természeti adottságok",
        "logo": "🌍",
        "color": "#4CAF50"
    },
    "komolyzene": {
        "name": "🎼 Komolyzene",
        "description": "Zeneművek, zeneszerzők, Spotify hallgatás",
        "logo": "🎼",
        "color": "#9C27B0"
    },
    "tudósok": {
        "name": "🔬 Tudósok",
        "description": "Híres tudósok és felfedezések",
        "logo": "🔬",
        "color": "#FF9800"
    },
    "mitológia": {
        "name": "🏛️ Mitológia",
        "description": "Görög, római és északi istenek, hősök",
        "logo": "🏛️",
        "color": "#795548"
    },
    "állatok": {
        "name": "🦁 Különleges Állatok",
        "description": "Ritka és egzotikus állatok",
        "logo": "🦁",
        "color": "#FF5722"
    },
    "sport_logók": {
        "name": "🏆 Sport Logók",
        "description": "NFL, NBA, MLB, NHL csapatok",
        "logo": "🏆",
        "color": "#2196F3"
    },
    "hegységek": {
        "name": "🏔️ Hegységek & Csúcsok",
        "description": "Világ legmagasabb hegyei",
        "logo": "🏔️",
        "color": "#607D8B"
    },
    "us_államok": {
        "name": "🇺🇸 US Államok",
        "description": "Amerikai államok címerei",
        "logo": "🇺🇸",
        "color": "#3F51B5"
    },
    "világzászlók": {
        "name": "🏳️ Világzászlók",
        "description": "Országok zászlainak felismerése",
        "logo": "🏳️",
        "color": "#E91E63"
    },
    "magyar_királyok": {
        "name": "👑 Magyar Királyok",
        "description": "Magyar királyok évszámokkal",
        "logo": "👑",
        "color": "#FFC107"
    },
    "háborúk": {
        "name": "⚔️ Háborúk", 
        "description": "Történelmi konfliktusok és csaták",
        "logo": "⚔️",
        "color": "#F44336"
    },
    "drámák": {
        "name": "🎭 Drámák",
        "description": "Shakespeare és Csehov drámák",
        "logo": "🎭",
        "color": "#673AB7"
    }
}

# Teljes kérdésadatbázis - eredeti kérdések
questions = {
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
        }
    ],
    
    "háborúk": [
        {
            "question": "Melyik háború zajlott 1914-1918 között? (Antant vs. Központi hatalmak)",
            "options": ["I. világháború", "II. világháború", "Koreai háború", "Vietnámi háború"],
            "correct": 0,
            "explanation": "I. világháború (1914-1918): Antant vs. Központi hatalmak"
        },
        {
            "question": "Melyik háború zajlott 1337-1453 között? (Anglia vs Franciaország)",
            "options": ["Százéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Százéves háború (1337-1453): Anglia vs Franciaország"
        },
        {
            "question": "Melyik háború zajlott 1618-1648 között? (Katolikus Habsburgok vs Protestáns államok)",
            "options": ["Harmincéves háború", "Világháború", "Polgárháború", "Függetlenségi háború"],
            "correct": 0,
            "explanation": "Harmincéves háború (1618-1648): Katolikus Habsburgok vs Protestáns államok"
        },
        {
            "question": "Melyik háború zajlott 1939-1945 között? (Tengelyhatalmak vs Szövetségesek)",
            "options": ["II. világháború", "I. világháború", "Hidegháború", "Vietnámi háború"],
            "correct": 0,
            "explanation": "II. világháború (1939-1945): Tengelyhatalmak vs Szövetségesek"
        },
        {
            "question": "Melyik háború zajlott 1950-1953 között? (Észak-Korea vs Dél-Korea)",
            "options": ["Koreai háború", "Vietnámi háború", "Hidegháború", "Golfi háború"],
            "correct": 0,
            "explanation": "Koreai háború (1950-1953): Észak-Korea vs Dél-Korea"
        }
    ],
    
    "drámák": [
        {
            "question": "Ki írta a Romeo és Júliát?",
            "options": ["Shakespeare", "Goethe", "Dante", "Homerosz"],
            "correct": 0,
            "explanation": "A Romeo és Júliát William Shakespeare írta."
        },
        {
            "question": "Melyik évben íródott a Romeo és Júlia?",
            "options": ["1595", "1596", "1597", "1598"],
            "correct": 1,
            "explanation": "A Romeo és Júlia 1596-ban íródott."
        },
        {
            "question": "Hol játszódik a Romeo és Júlia cselekménye?",
            "options": ["London", "Verona", "Róma", "Velence"],
            "correct": 1,
            "explanation": "A Romeo és Júlia cselekménye Veronában játszódik."
        },
        {
            "question": "Ki a főhős a Romeo és Júliában?",
            "options": ["Romeo", "Júlia", "Mindkettő", "Senki"],
            "correct": 2,
            "explanation": "A Romeo és Júlia főhősei Romeo és Júlia."
        }
    ],
    
    "komolyzene": [
        {
            "question": "Ki írta a Hatodik szimfóniát?",
            "options": ["Beethoven", "Mozart", "Bach", "Tchaikovsky"],
            "correct": 3,
            "explanation": "A Hatodik szimfóniát Tchaikovsky írta."
        },
        {
            "question": "Melyik évben íródott a Hatodik szimfónia?",
            "options": ["1891", "1892", "1893", "1894"],
            "correct": 2,
            "explanation": "A Hatodik szimfónia 1893-ban íródott."
        },
        {
            "question": "Mi a Hatodik szimfónia alcíme?",
            "options": ["Patetikus", "Tragikus", "Melankolikus", "Szenvedélyes"],
            "correct": 0,
            "explanation": "A Hatodik szimfónia alcíme 'Patetikus'."
        },
        {
            "question": "Melyik zeneszerző írta a 9. szimfóniát?",
            "options": ["Beethoven", "Mozart", "Bach", "Tchaikovsky"],
            "correct": 0,
            "explanation": "A 9. szimfóniát Beethoven írta."
        }
    ],
    
    "mitológia": [
        {
            "question": "Ki a görög mitológia főistene?",
            "options": ["Zeusz", "Poseidón", "Hadész", "Apollón"],
            "correct": 0,
            "explanation": "Zeusz a görög mitológia főistene."
        },
        {
            "question": "Ki a háború istennője a görög mitológiában?",
            "options": ["Aphrodité", "Athéné", "Artemisz", "Héra"],
            "correct": 1,
            "explanation": "Athéné a háború istennője a görög mitológiában."
        }
    ],
    
    "állatok": [
        {
            "question": "Melyik a legnagyobb szárazföldi emlős?",
            "options": ["Elefánt", "Zsiráf", "Oroszlán", "Tigris"],
            "correct": 0,
            "explanation": "Az elefánt a legnagyobb szárazföldi emlős."
        },
        {
            "question": "Melyik állat tud repülni?",
            "options": ["Denevér", "Kenguru", "Krokodil", "Kígyó"],
            "correct": 0,
            "explanation": "A denevér az egyetlen repülő emlős."
        }
    ],
    
    "sport_logók": [
        {
            "question": "Melyik NFL csapat logója?",
            "options": ["Dallas Cowboys", "New York Giants", "Green Bay Packers", "Chicago Bears"],
            "correct": 0,
            "explanation": "A Dallas Cowboys egy NFL csapat."
        },
        {
            "question": "Melyik NBA csapat logója?",
            "options": ["Los Angeles Lakers", "Boston Celtics", "Chicago Bulls", "Miami Heat"],
            "correct": 0,
            "explanation": "A Los Angeles Lakers egy NBA csapat."
        }
    ],
    
    "hegységek": [
        {
            "question": "Melyik a világ legmagasabb hegye?",
            "options": ["K2", "Mount Everest", "Kangchenjunga", "Lhotse"],
            "correct": 1,
            "explanation": "A Mount Everest 8848 méter magas."
        },
        {
            "question": "Melyik kontinensen található a Kilimandzsáró?",
            "options": ["Ázsia", "Afrika", "Dél-Amerika", "Európa"],
            "correct": 1,
            "explanation": "A Kilimandzsáró Afrikában található."
        }
    ],
    
    "us_államok": [
        {
            "question": "Melyik az USA legnagyobb állama?",
            "options": ["Texas", "Alaszka", "Kalifornia", "Montana"],
            "correct": 1,
            "explanation": "Alaszka az USA legnagyobb állama."
        },
        {
            "question": "Melyik az USA fővárosa?",
            "options": ["New York", "Washington D.C.", "Los Angeles", "Chicago"],
            "correct": 1,
            "explanation": "Washington D.C. az USA fővárosa."
        }
    ],
    
    "világzászlók": [
        {
            "question": "Melyik ország zászlaja?",
            "options": ["Japán", "Kína", "Dél-Korea", "Vietnam"],
            "correct": 0,
            "explanation": "A piros kör fehér háttéren Japán zászlaja."
        },
        {
            "question": "Melyik ország zászlaja?",
            "options": ["Németország", "Belgium", "Olaszország", "Hollandia"],
            "correct": 0,
            "explanation": "A fekete-piros-arany sávok Németország zászlaja."
        }
    ],
    
    "magyar_királyok": [
        {
            "question": "Ki volt Magyarország első királya?",
            "options": ["Szent István", "Szent László", "Kálmán", "Béla"],
            "correct": 0,
            "explanation": "Szent István volt Magyarország első királya."
        },
        {
            "question": "Mikor koronázták meg Szent Istvánt?",
            "options": ["1000", "1001", "1002", "1003"],
            "correct": 0,
            "explanation": "Szent Istvánt 1000-ben koronázták meg."
        }
    ]
}

# Fő oldal
st.title("🧠 Quiz Alkalmazás - Teljes Adatbázis")

# Sidebar beállítások
with st.sidebar:
    st.markdown("## ⚙️ Beállítások")
    st.markdown("---")
    
    # Kérdések száma
    st.markdown("### 📊 Kérdések száma")
    num_questions = st.slider(
        "Válaszd ki a kérdések számát:",
        min_value=1,
        max_value=100,
        value=10,
        step=1
    )
    
    # Quiz indítása
    st.markdown("---")
    st.markdown("### 🚀 Quiz indítása")
    
    if st.button("🎯 Indítsd el a Quiz-t!", type="primary", use_container_width=True):
        if not st.session_state.selected_topics:
            st.error("❌ Kérlek válassz ki legalább egy témakört!")
        else:
            # Quiz indítása
            st.session_state.quiz_started = True
            st.session_state.current_question = 0
            st.session_state.score = 0
            
            # Kérdések összegyűjtése
            all_questions = []
            for topic in st.session_state.selected_topics:
                all_questions.extend(questions[topic])
            
            # Véletlenszerű kiválasztás
            if len(all_questions) < num_questions:
                st.warning(f"⚠️ Csak {len(all_questions)} kérdés áll rendelkezésre.")
                st.session_state.quiz_questions = all_questions
            else:
                st.session_state.quiz_questions = random.sample(all_questions, num_questions)
            
            st.rerun()
    
    # Debug info
    st.markdown("---")
    st.markdown("### 🔍 Debug")
    st.write(f"**Kiválasztott témák:** {st.session_state.selected_topics}")
    st.write(f"**Kérdések száma:** {num_questions}")

# Fő tartalom
if not st.session_state.quiz_started:
    st.markdown("""
    ## Üdvözöllek a Teljes Quiz Alkalmazásban! 🎯
    
    ### Válaszd ki a témaköröket:
    """)
    
    # Témakörök kiválasztása checkbox-kal
    st.markdown("### 📚 Témakörök kiválasztása")
    
    # Reset gomb
    if st.button("🔄 Összes kiválasztás törlése"):
        st.session_state.selected_topics = []
        st.rerun()
    
    # Témakörök megjelenítése - 3 oszlopban
    cols = st.columns(3)
    
    for i, (topic_key, topic_info) in enumerate(TOPICS_WITH_LOGOS.items()):
        col = cols[i % 3]
        
        with col:
            # Témakör kártya
            st.markdown(f"""
            <div style="
                border: 2px solid {topic_info['color']}; 
                border-radius: 10px; 
                padding: 15px; 
                margin: 10px 0;
                background-color: {'#f0f8ff' if topic_key in st.session_state.selected_topics else '#ffffff'};
            ">
                <h4 style="color: {topic_info['color']}; margin: 0;">
                    {topic_info['logo']} {topic_info['name']}
                </h4>
                <p style="color: #666; margin: 8px 0; font-size: 0.9em;">
                    {topic_info['description']}
                </p>
                <p style="color: #888; font-size: 0.8em; margin: 0;">
                    {len(questions.get(topic_key, []))} kérdés
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Checkbox
            if st.checkbox(
                f"Válaszd ki: {topic_info['name']}", 
                key=f"checkbox_{topic_key}",
                value=topic_key in st.session_state.selected_topics
            ):
                if topic_key not in st.session_state.selected_topics:
                    st.session_state.selected_topics.append(topic_key)
            else:
                if topic_key in st.session_state.selected_topics:
                    st.session_state.selected_topics.remove(topic_key)
    
    # Kiválasztott témák megjelenítése
    if st.session_state.selected_topics:
        st.markdown("---")
        st.markdown("### ✅ Kiválasztott témakörök:")
        
        for topic in st.session_state.selected_topics:
            topic_info = TOPICS_WITH_LOGOS[topic]
            st.markdown(f"- {topic_info['logo']} **{topic_info['name']}** ({len(questions.get(topic, []))} kérdés)")
        
        total_questions = sum(len(questions.get(topic, [])) for topic in st.session_state.selected_topics)
        st.markdown(f"**Összesen:** {total_questions} kérdés")
    
    # Statisztikák
    st.markdown("---")
    st.markdown("### 📈 Statisztikák")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Összes kérdés", sum(len(q) for q in questions.values()))
    with col2:
        st.metric("Témakörök", len(questions))
    with col3:
        st.metric("Kiválasztott", len(st.session_state.selected_topics))
    with col4:
        st.metric("Elérhető", sum(len(questions.get(topic, [])) for topic in st.session_state.selected_topics))

else:
    # Quiz megjelenítése
    if st.session_state.current_question < len(st.session_state.quiz_questions):
        question = st.session_state.quiz_questions[st.session_state.current_question]
        
        # Progress
        progress = (st.session_state.current_question + 1) / len(st.session_state.quiz_questions)
        st.progress(progress)
        st.caption(f"Kérdés {st.session_state.current_question + 1} / {len(st.session_state.quiz_questions)}")
        
        # Kérdés
        st.subheader(f"❓ {question['question']}")
        
        # Válaszlehetőségek
        for i, option in enumerate(question['options']):
            if st.button(f"{chr(65+i)}. {option}", key=f"q{st.session_state.current_question}_opt{i}", use_container_width=True):
                if i == question['correct']:
                    st.success("✅ Helyes válasz!")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Helytelen! A helyes válasz: {chr(65+question['correct'])}. {question['options'][question['correct']]}")
                
                # Magyarázat
                st.info(f"💡 **Magyarázat:** {question['explanation']}")
                
                # Következő kérdés
                st.session_state.current_question += 1
                if st.session_state.current_question < len(st.session_state.quiz_questions):
                    st.rerun()
                else:
                    st.rerun()
    else:
        # Eredmények
        st.success("🏆 Quiz befejezve!")
        score = st.session_state.score
        total = len(st.session_state.quiz_questions)
        percentage = (score / total) * 100
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Helyes válaszok", f"{score}/{total}")
        with col2:
            st.metric("Százalék", f"{percentage:.1f}%")
        with col3:
            if percentage >= 90:
                grade = "A+"
                emoji = "🌟"
            elif percentage >= 80:
                grade = "A"
                emoji = "⭐"
            elif percentage >= 70:
                grade = "B"
                emoji = "👍"
            elif percentage >= 60:
                grade = "C"
                emoji = "😊"
            elif percentage >= 50:
                grade = "D"
                emoji = "😐"
            else:
                grade = "F"
                emoji = "😔"
            st.metric("Osztályzat", f"{grade} {emoji}")
        
        # Új quiz gomb
        if st.button("🔄 Új Quiz", type="primary"):
            st.session_state.quiz_started = False
            st.session_state.selected_topics = []
            st.rerun() 