import streamlit as st
import random

# Page config - force sidebar to be expanded
st.set_page_config(
    page_title="Quiz Alkalmazás - Látható Sidebar",
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

# Egyszerűsített kérdésadatbázis
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
        }
    ],
    "irodalom": [
        {
            "question": "Ki írta a Romeo és Júliát?",
            "options": ["Shakespeare", "Goethe", "Dante", "Homerosz"],
            "correct": 0,
            "explanation": "A Romeo és Júliát William Shakespeare írta."
        }
    ]
}

# Fő oldal címe
st.title("🧠 Quiz Alkalmazás - Látható Sidebar")

# Sidebar - nagyobb és láthatóbb
st.sidebar.markdown("## ⚙️ BEÁLLÍTÁSOK")
st.sidebar.markdown("---")

# Témakörök kiválasztása - nagyobb betűmérettel
st.sidebar.markdown("### 📚 TÉMAKÖRÖK KIVÁLASZTÁSA")
st.sidebar.markdown("Válaszd ki a témaköröket:")

available_topics = list(questions.keys())
selected_topics = st.sidebar.multiselect(
    "Témakörök:",
    available_topics,
    default=available_topics[:2],
    help="Válaszd ki a témaköröket, amelyekből kérdéseket szeretnél"
)

# Kérdések száma
st.sidebar.markdown("### 📊 KÉRDÉSEK SZÁMA")
num_questions = st.sidebar.slider(
    "Kérdések száma:",
    min_value=1,
    max_value=20,
    value=5,
    step=1,
    help="Válaszd ki, hogy hány kérdést szeretnél"
)

# Quiz indítása gomb - nagyobb és színesebb
st.sidebar.markdown("---")
st.sidebar.markdown("### 🚀 QUIZ INDÍTÁSA")

if st.sidebar.button("🎯 INDÍTSD EL A QUIZ-T!", type="primary", use_container_width=True):
    if not selected_topics:
        st.sidebar.error("❌ Kérlek válassz ki legalább egy témakört!")
    else:
        # Összes kérdés összegyűjtése
        all_questions = []
        for topic in selected_topics:
            all_questions.extend(questions[topic])
        
        # Véletlenszerű kiválasztás
        if len(all_questions) < num_questions:
            st.sidebar.warning(f"⚠️ Csak {len(all_questions)} kérdés áll rendelkezésre.")
            quiz_questions = all_questions
        else:
            quiz_questions = random.sample(all_questions, num_questions)
        
        # Quiz indítása
        st.session_state.quiz_started = True
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.quiz_questions = quiz_questions
        st.rerun()

# Debug információk
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 DEBUG INFO")
st.sidebar.write(f"**Quiz indítva:** {st.session_state.quiz_started}")
st.sidebar.write(f"**Kiválasztott témák:** {selected_topics}")
st.sidebar.write(f"**Kérdések száma:** {num_questions}")

# Fő tartalom
if not st.session_state.quiz_started:
    st.markdown("""
    ## Üdvözöllek a Quiz Alkalmazásban! 🎯
    
    ### Hogyan működik:
    1. **Válaszd ki a témaköröket** a bal oldali menüben ⬅️
    2. **Állítsd be a kérdések számát** (1-20 között)
    3. **Indítsd el a quiz-t** a gombra kattintva
    4. **Válaszolj a kérdésekre**
    
    ### Elérhető témakörök:
    - 🌍 **Földrajz**: Országok, városok, természeti adottságok
    - ⚔️ **Háborúk**: Történelmi konfliktusok és csaták
    - 📚 **Irodalom**: Könyvek, szerzők, művek
    """)
    
    # Statisztikák
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Összes kérdés", sum(len(q) for q in questions.values()))
    with col2:
        st.metric("Témakörök", len(questions))
    with col3:
        st.metric("Kiválasztott témák", len(selected_topics))

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
            st.rerun() 