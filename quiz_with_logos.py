import streamlit as st
import random
import base64
from PIL import Image
import io

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

# Teljes kérdésadatbázis - alap kérdések
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
        }
    ],
    
    "háborúk": [
        {
            "question": "Mikor kezdődött az első világháború?",
            "options": ["1914", "1915", "1916", "1917"],
            "correct": 0,
            "explanation": "Az első világháború 1914-ben kezdődött."
        },
        {
            "question": "Mikor fejeződött be a második világháború Európában?",
            "options": ["1944", "1945", "1946", "1947"],
            "correct": 1,
            "explanation": "A második világháború Európában 1945-ben fejeződött be."
        },
        {
            "question": "Melyik évben kezdődött a hidegháború?",
            "options": ["1945", "1947", "1949", "1951"],
            "correct": 1,
            "explanation": "A hidegháború 1947-ben kezdődött."
        },
        {
            "question": "Mikor volt a vietnámi háború?",
            "options": ["1955-1975", "1960-1970", "1965-1975", "1970-1980"],
            "correct": 0,
            "explanation": "A vietnámi háború 1955-1975 között zajlott."
        },
        {
            "question": "Melyik évben volt a koreai háború?",
            "options": ["1950-1953", "1951-1954", "1952-1955", "1953-1956"],
            "correct": 0,
            "explanation": "A koreai háború 1950-1953 között zajlott."
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
    
    "tudósok": [
        {
            "question": "Ki fedezte fel a gravitációt?",
            "options": ["Einstein", "Newton", "Galilei", "Kepler"],
            "correct": 1,
            "explanation": "Isaac Newton fedezte fel a gravitációt."
        },
        {
            "question": "Ki írta az E=mc² képletet?",
            "options": ["Einstein", "Newton", "Planck", "Bohr"],
            "correct": 0,
            "explanation": "Albert Einstein írta az E=mc² képletet."
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
        max_value=50,
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