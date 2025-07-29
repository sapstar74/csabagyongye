import streamlit as st
import random

# Importáljuk a valódi kérdésfájlokat
try:
    from topics.haboru_all_questions import HABORU_QUESTIONS_ALL
    from topics.kiralyok import KIRALYOK_QUESTIONS
    from topics.foldrajz import FOLDRAJZ_QUESTIONS
    from topics.mitologia_all_questions import MITOLOGIA_QUESTIONS_ALL
    from topics.allatok_all_questions import ALLATOK_QUESTIONS_ALL
    from topics.sport_logok import SPORT_LOGOK_QUESTIONS
    from topics.zaszlok_all_questions import ZASZLOK_QUESTIONS_ALL
    from topics.dramak import DRAMAK_QUESTIONS
    from topics.tudosok import TUDOSOK_QUESTIONS
    from topics.zenek import ZENEK_QUESTIONS
except ImportError as e:
    st.error(f"Hiba a kérdésfájlok betöltésekor: {e}")
    st.stop()

st.set_page_config(
    page_title="🧠 Teljes Quiz App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Valódi kérdésbank a külön fájlokból ---
QUIZ_DATA_BY_TOPIC = {
    "földrajz": FOLDRAJZ_QUESTIONS,
    "komolyzene": ZENEK_QUESTIONS,
    "tudósok": TUDOSOK_QUESTIONS,
    "mitológia": MITOLOGIA_QUESTIONS_ALL,
    "állatok": ALLATOK_QUESTIONS_ALL,
    "sport_logók": SPORT_LOGOK_QUESTIONS,
    "világzászlók": ZASZLOK_QUESTIONS_ALL,
    "magyar_királyok": KIRALYOK_QUESTIONS,
    "háborúk": HABORU_QUESTIONS_ALL,
    "drámák": DRAMAK_QUESTIONS
}

# --- Témakörök és logók - szép szelekciós képernyő ---
TOPICS_WITH_LOGOS = {
    "földrajz": {
        "name": "🌍 Földrajz",
        "description": "Országok, városok, természeti adottságok",
        "logo": "🌍",
        "color": "#4CAF50",
        "questions": len(QUIZ_DATA_BY_TOPIC["földrajz"])
    },
    "komolyzene": {
        "name": "🎼 Komolyzene",
        "description": "Zeneművek, zeneszerzők, Spotify hallgatás",
        "logo": "🎼",
        "color": "#9C27B0",
        "questions": len(QUIZ_DATA_BY_TOPIC["komolyzene"])
    },
    "tudósok": {
        "name": "🔬 Tudósok",
        "description": "Híres tudósok és felfedezések",
        "logo": "🔬",
        "color": "#FF9800",
        "questions": len(QUIZ_DATA_BY_TOPIC["tudósok"])
    },
    "mitológia": {
        "name": "🏛️ Mitológia",
        "description": "Görög, római és északi istenek, hősök",
        "logo": "🏛️",
        "color": "#795548",
        "questions": len(QUIZ_DATA_BY_TOPIC["mitológia"])
    },
    "állatok": {
        "name": "🦁 Különleges Állatok",
        "description": "Ritka és egzotikus állatok",
        "logo": "🦁",
        "color": "#FF5722",
        "questions": len(QUIZ_DATA_BY_TOPIC["állatok"])
    },
    "sport_logók": {
        "name": "🏆 Sport Logók",
        "description": "NFL, NBA, MLB, NHL csapatok",
        "logo": "🏆",
        "color": "#2196F3",
        "questions": len(QUIZ_DATA_BY_TOPIC["sport_logók"])
    },
    "világzászlók": {
        "name": "🏳️ Világzászlók",
        "description": "Országok zászlainak felismerése",
        "logo": "🏳️",
        "color": "#E91E63",
        "questions": len(QUIZ_DATA_BY_TOPIC["világzászlók"])
    },
    "magyar_királyok": {
        "name": "👑 Magyar Királyok",
        "description": "Magyar királyok évszámokkal",
        "logo": "👑",
        "color": "#FFC107",
        "questions": len(QUIZ_DATA_BY_TOPIC["magyar_királyok"])
    },
    "háborúk": {
        "name": "⚔️ Háborúk", 
        "description": "Történelmi konfliktusok és csaták",
        "logo": "⚔️",
        "color": "#F44336",
        "questions": len(QUIZ_DATA_BY_TOPIC["háborúk"])
    },
    "drámák": {
        "name": "🎭 Drámák",
        "description": "Shakespeare és Csehov drámák",
        "logo": "🎭",
        "color": "#673AB7",
        "questions": len(QUIZ_DATA_BY_TOPIC["drámák"])
    }
}

# --- Session state inicializálás ---
if 'selected_topics' not in st.session_state:
    st.session_state.selected_topics = []
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []

# --- Fő tartalom ---
st.title("🧠 Teljes Quiz App")
st.markdown("---")

# Statisztikák megjelenítése
st.sidebar.header("📊 Kérdésbank Statisztikák")
total_questions = sum(len(questions) for questions in QUIZ_DATA_BY_TOPIC.values())
st.sidebar.metric("📝 Összes kérdés", total_questions)
st.sidebar.metric("🎯 Témakörök", len(QUIZ_DATA_BY_TOPIC))

for topic, questions in QUIZ_DATA_BY_TOPIC.items():
    topic_name = TOPICS_WITH_LOGOS[topic]["name"]
    st.sidebar.metric(topic_name, len(questions))

if not st.session_state.quiz_started:
    # --- Szép szelekciós képernyő ---
    st.header("🎯 Válassz témaköröket a kvízhez!")
    
    # Kérdések száma beállítása
    col1, col2 = st.columns([2, 1])
    with col2:
        st.subheader("⚙️ Beállítások")
        num_questions = st.slider("📝 Kérdések száma:", 5, 50, 15)
    
    with col1:
        st.subheader("📚 Elérhető témakörök")
    
    # Témakörök megjelenítése checkboxokkal
    selected_topics = []
    
    # 3 oszlopos elrendezés
    cols = st.columns(3)
    if 'selected_topics_temp' not in st.session_state:
        st.session_state.selected_topics_temp = []
    for i, (topic_key, topic_info) in enumerate(TOPICS_WITH_LOGOS.items()):
        col_idx = i % 3
        selected = topic_key in st.session_state.selected_topics_temp
        with cols[col_idx]:
            # Teljes téglalap kattintható
            button_text = f"{topic_info['logo']} {topic_info['name']}\n{topic_info['description']}\n📊 {topic_info['questions']} kérdés"
            if st.button(
                button_text,
                key=f"btn_{topic_key}",
                help=f"{topic_info['description']} - {topic_info['questions']} kérdés",
                use_container_width=True,
                type="secondary" if not selected else "primary"
            ):
                if selected:
                    st.session_state.selected_topics_temp.remove(topic_key)
                else:
                    st.session_state.selected_topics_temp.append(topic_key)
                st.rerun()
    
    # Kvíz indítása gomb
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Kvíz indítása", type="primary", use_container_width=True):
            if st.session_state.selected_topics_temp:
                st.session_state.selected_topics = st.session_state.selected_topics_temp.copy()
                # Kérdések összegyűjtése
                questions = []
                for topic in st.session_state.selected_topics:
                    questions.extend(QUIZ_DATA_BY_TOPIC[topic])
                random.shuffle(questions)
                st.session_state.questions = questions[:num_questions]
                st.session_state.quiz_started = True
                st.session_state.current_question = 0
                st.session_state.score = 0
                st.session_state.answers = []
                st.session_state.selected_topics_temp = []
                st.rerun()
            else:
                st.warning("⚠️ Válassz legalább egy témakört!")
        
        # Reset gomb
        if st.button("🔄 Alaphelyzet", use_container_width=True):
            st.session_state.selected_topics = []
            st.session_state.selected_topics_temp = []
            st.session_state.quiz_started = False
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun()

else:
    # --- Kvíz képernyő ---
    qn = st.session_state.current_question
    questions = st.session_state.questions
    
    if qn < len(questions):
        q = questions[qn]
        
        # Progress bar
        progress = (qn + 1) / len(questions)
        st.progress(progress)
        st.write(f"**{qn+1} / {len(questions)}** kérdés")
        
        st.header(f"❓ {q['question']}")
        # --- Zenei embed ---
        if 'spotify' in q:
            st.markdown(f'<iframe src="{q["spotify"]}" width="100%" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>', unsafe_allow_html=True)
        if 'youtube' in q:
            st.markdown(f'<iframe width="100%" height="315" src="{q["youtube"]}" frameborder="0" allowfullscreen></iframe>', unsafe_allow_html=True)
        
        options = q["options"]
        answer = st.radio("Válaszlehetőségek:", options, key=f"q{qn}")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✅ Válasz beküldése", key=f"submit{qn}", type="primary"):
                correct = options[q["correct"]]
                st.session_state.answers.append(answer)
                if answer == correct:
                    st.session_state.score += 1
                    st.success("🎉 Helyes válasz!")
                else:
                    st.error(f"❌ Helytelen! A helyes válasz: **{correct}**")
                    if "explanation" in q:
                        st.info(f"💡 **Magyarázat:** {q['explanation']}")
                # --- Összefoglaló ---
                helyes = st.session_state.score
                rossz = len(st.session_state.answers) - helyes
                st.info(f"**Eddigi eredmény:** {helyes} helyes, {rossz} helytelen válasz")
                st.session_state.current_question += 1
                st.rerun()
        
        with col2:
            if st.button("🔄 Következő kérdés", key=f"next{qn}"):
                st.session_state.current_question += 1
                st.rerun()
    else:
        # Kvíz vége
        st.success("🎊 **Kvíz vége!**")
        st.balloons()
        
        score_percent = (st.session_state.score / len(questions)) * 100
        st.metric("📊 Pontszám", f"{st.session_state.score} / {len(questions)} ({score_percent:.1f}%)")
        
        if score_percent >= 80:
            st.success("🏆 Kiváló teljesítmény!")
        elif score_percent >= 60:
            st.info("👍 Jó teljesítmény!")
        else:
            st.warning("📚 Még van mit tanulni!")
        
        # --- Részletes értékelés ---
        st.markdown("---")
        st.subheader("📋 Részletes értékelés")
        for idx, (q, user_ans) in enumerate(zip(st.session_state.questions, st.session_state.answers)):
            correct_ans = q["options"][q["correct"]]
            helyes = (user_ans == correct_ans)
            color = "#d4edda" if helyes else "#f8d7da"
            border = "#28a745" if helyes else "#dc3545"
            st.markdown(f"""
            <div style='border:2px solid {border}; border-radius:10px; background:{color}; padding:12px; margin-bottom:10px;'>
                <b>{idx+1}. {q['question']}</b><br>
                <span style='color: {'green' if helyes else 'red'}; font-weight:bold;'>
                    {'✔️' if helyes else '❌'} Válaszod: {user_ans}
                </span><br>
                <span style='color:#333;'>Helyes válasz: <b>{correct_ans}</b></span><br>
                {('<span style="color:#888;">💡 ' + q['explanation'] + '</span>') if 'explanation' in q else ''}
            </div>
            """, unsafe_allow_html=True)
        if st.button("🔄 Új kvíz", type="primary"):
            st.session_state.quiz_started = False
            st.session_state.questions = []
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.answers = []
            st.rerun() 