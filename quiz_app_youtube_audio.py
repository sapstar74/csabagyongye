import streamlit as st
import random
import json
import os
from topics.konnyuzene import POP_MUSIC_QUESTIONS
from topics.magyar_zenekarok import MAGYAR_ZENEKAROK_QUESTIONS

# Page config
st.set_page_config(
    page_title="Zenei Kvíz - YouTube Audio",
    page_icon="🎵",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .question-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .audio-player {
        margin: 1rem 0;
        padding: 1rem;
        background-color: #e8f4fd;
        border-radius: 8px;
    }
    .result-correct {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .result-incorrect {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def load_audio_mapping():
    """Load mapping from question index to audio file"""
    audio_dir = 'audio_files'
    audio_files = []
    
    if os.path.exists(audio_dir):
        # Get all mp3 files and sort by number
        files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
        
        # Filter and sort files that start with numbers
        numbered_files = []
        for file in files:
            try:
                # Check if file starts with a number
                if file[0].isdigit():
                    number = int(file.split('_')[0])
                    numbered_files.append((number, file))
            except (ValueError, IndexError):
                # Skip files that don't match the expected format
                continue
        
        # Sort by number and extract filenames
        numbered_files.sort(key=lambda x: x[0])
        audio_files = [file for _, file in numbered_files]
    
    return audio_files

def get_audio_file_for_question(question_index, audio_files):
    """Get audio file for a specific question index"""
    if question_index < len(audio_files):
        return os.path.join('audio_files', audio_files[question_index])
    return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎵 Zenei Kvíz - YouTube Audio</h1>', unsafe_allow_html=True)
    
    # Load audio mapping
    audio_files = load_audio_mapping()
    st.sidebar.success(f"📁 {len(audio_files)} audio fájl betöltve")
    
    # Initialize session state
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'show_result' not in st.session_state:
        st.session_state.show_result = False
    if 'selected_answer' not in st.session_state:
        st.session_state.selected_answer = None
    
    # Sidebar controls
    st.sidebar.title("🎮 Vezérlők")
    
    # Topic selection
    topic = st.sidebar.selectbox(
        "Válassz témát:",
        ["Könnyűzene", "Magyar zenekarok", "Véletlenszerű"]
    )
    
    # Get questions based on topic
    if topic == "Könnyűzene":
        questions = POP_MUSIC_QUESTIONS
    elif topic == "Magyar zenekarok":
        questions = MAGYAR_ZENEKAROK_QUESTIONS
    else:
        questions = POP_MUSIC_QUESTIONS + MAGYAR_ZENEKAROK_QUESTIONS
    
    st.sidebar.info(f"📊 {len(questions)} kérdés a témában")
    
    # New question button
    if st.sidebar.button("🔄 Új kérdés", type="primary"):
        st.session_state.current_question = random.choice(questions)
        st.session_state.show_result = False
        st.session_state.selected_answer = None
        st.rerun()
    
    # Reset score button
    if st.sidebar.button("🔄 Pontszám törlése"):
        st.session_state.score = 0
        st.session_state.total_questions = 0
        st.rerun()
    
    # Display current score
    st.sidebar.metric(
        "Pontszám", 
        f"{st.session_state.score}/{st.session_state.total_questions}"
    )
    
    # Main content
    if st.session_state.current_question is None:
        st.info("👆 Kattints az 'Új kérdés' gombra a játék indításához!")
        return
    
    question = st.session_state.current_question
    
    # Display question
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    st.subheader("🎵 " + question["question"])
    
    # Get audio file for this question
    question_index = questions.index(question)
    audio_file = get_audio_file_for_question(question_index, audio_files)
    
    if audio_file and os.path.exists(audio_file):
        # Display audio player
        st.markdown('<div class="audio-player">', unsafe_allow_html=True)
        st.audio(audio_file, format='audio/mp3')
        
        # Extract artist name from filename
        filename = os.path.basename(audio_file)
        artist_name = filename.split('_', 1)[1].replace('.mp3', '').replace('_', ' ')
        st.info(f"🎤 Előadó: {artist_name}")
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Audio fájl nem található")
    
    # Display options
    if not st.session_state.show_result:
        selected = st.radio(
            "Válassz választ:",
            question["options"],
            key=f"question_{question_index}"
        )
        
        if st.button("✅ Válasz beküldése", type="primary"):
            st.session_state.selected_answer = selected
            st.session_state.show_result = True
            st.session_state.total_questions += 1
            
            if selected == question["options"][question["correct"]]:
                st.session_state.score += 1
            
            st.rerun()
    
    # Show result
    if st.session_state.show_result:
        correct_answer = question["options"][question["correct"]]
        
        if st.session_state.selected_answer == correct_answer:
            st.markdown('<div class="result-correct">', unsafe_allow_html=True)
            st.success(f"✅ Helyes! A válasz: {correct_answer}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-incorrect">', unsafe_allow_html=True)
            st.error(f"❌ Helytelen! A helyes válasz: {correct_answer}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Show explanation
        st.info(f"💡 {question['explanation']}")
        
        # Next question button
        if st.button("➡️ Következő kérdés"):
            st.session_state.current_question = random.choice(questions)
            st.session_state.show_result = False
            st.session_state.selected_answer = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 