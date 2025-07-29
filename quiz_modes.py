"""
🎮 Quiz Módok és Nehézségi Szintek
Különböző játékmódok és nehézségi szintek implementálása
"""

import random
import time
from datetime import datetime, timedelta
from enum import Enum
import streamlit as st

class QuizMode(Enum):
    """Quiz módok enum"""
    NORMAL = "normal"
    TIMED = "timed"
    SURVIVAL = "survival"
    PRACTICE = "practice"
    CHALLENGE = "challenge"

class DifficultyLevel(Enum):
    """Nehézségi szintek enum"""
    EASY = "easy"      # Könnyű - feleletválasztós + megoldás
    MEDIUM = "medium"  # Közepes - feleletválasztós
    HARD = "hard"      # Nehéz - szabad szöveges bevitel

class QuizModeManager:
    """Quiz módok kezelő osztály"""
    
    def __init__(self):
        self.current_mode = QuizMode.NORMAL
        self.current_difficulty = DifficultyLevel.MEDIUM
        self.time_limit = None
        self.lives = None
        self.streak = 0
        self.max_streak = 0
        self.show_solution = False  # Megoldás megjelenítése (Könnyű mód)
        self.text_input_mode = False  # Szöveges bevitel (Nehéz mód)
    
    def set_mode(self, mode: QuizMode, **kwargs):
        """Quiz mód beállítása"""
        self.current_mode = mode
        
        if mode == QuizMode.TIMED:
            self.time_limit = kwargs.get('time_limit', 30)  # másodpercek
        elif mode == QuizMode.SURVIVAL:
            self.lives = kwargs.get('lives', 3)
        elif mode == QuizMode.CHALLENGE:
            self.time_limit = kwargs.get('time_limit', 20)
            self.lives = kwargs.get('lives', 1)
    
    def set_difficulty(self, difficulty: DifficultyLevel):
        """Nehézségi szint beállítása"""
        self.current_difficulty = difficulty
        
        # Nehézségi szint specifikus beállítások
        if difficulty == DifficultyLevel.EASY:
            self.show_solution = True
            self.text_input_mode = False
        elif difficulty == DifficultyLevel.MEDIUM:
            self.show_solution = False
            self.text_input_mode = False
        elif difficulty == DifficultyLevel.HARD:
            self.show_solution = False
            self.text_input_mode = True
    
    def get_mode_config(self):
        """Aktuális mód konfigurációja"""
        config = {
            "mode": self.current_mode.value,
            "difficulty": self.current_difficulty.value,
            "time_limit": self.time_limit,
            "lives": self.lives,
            "streak": self.streak,
            "max_streak": self.max_streak,
            "show_solution": self.show_solution,
            "text_input_mode": self.text_input_mode
        }
        return config
    
    def update_streak(self, correct: bool):
        """Streak frissítése"""
        if correct:
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
        else:
            self.streak = 0
        
        return self.streak
    
    def lose_life(self):
        """Élet elvesztése (Survival mód)"""
        if self.lives is not None:
            self.lives -= 1
            return self.lives > 0
        return True
    
    def get_remaining_time(self, start_time):
        """Hátralévő idő (Timed mód)"""
        if self.time_limit is None:
            return None
        
        elapsed = (datetime.now() - start_time).total_seconds()
        remaining = self.time_limit - elapsed
        return max(0, remaining)
    
    def is_time_up(self, start_time):
        """Idő lejárt? (Timed mód)"""
        if self.time_limit is None:
            return False
        
        return self.get_remaining_time(start_time) <= 0

class QuizModeUI:
    """Quiz módok UI komponensei"""
    
    @staticmethod
    def show_mode_selection():
        """Mód kiválasztás megjelenítése"""
        st.markdown("## 🎮 Quiz Mód Kiválasztása")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📋 Módok")
            
            mode_options = {
                "normál": {
                    "description": "Hagyományos quiz mód",
                    "icon": "📝",
                    "features": ["Nincs időkorlát", "Nincs életrendszer", "Részletes eredmények"]
                },
                "időzített": {
                    "description": "Időkorlátozott quiz",
                    "icon": "⏱️",
                    "features": ["30 másodperc/kérdés", "Gyors válaszok", "Idő nyomás"]
                },
                "túlélés": {
                    "description": "Túlélési mód",
                    "icon": "💀",
                    "features": ["3 élet", "Hibák után élet elvesztése", "Hosszú sorozatok"]
                },
                "gyakorlás": {
                    "description": "Gyakorló mód",
                    "icon": "📚",
                    "features": ["Azonnali visszajelzés", "Magyarázatok", "Nincs pontszám"]
                },
                "kihívás": {
                    "description": "Kihívás mód",
                    "icon": "🏆",
                    "features": ["1 élet", "20 másodperc/kérdés", "Legmagasabb pontszámok"]
                }
            }
            
            selected_mode = st.selectbox(
                "Válassz módot:",
                list(mode_options.keys()),
                format_func=lambda x: f"{mode_options[x]['icon']} {x}"
            )
            
            # Mód leírása
            if selected_mode in mode_options:
                mode_info = mode_options[selected_mode]
                st.markdown(f"**{mode_info['description']}**")
                st.markdown("**Jellemzők:**")
                for feature in mode_info['features']:
                    st.markdown(f"• {feature}")
        
        with col2:
            st.markdown("### 🎯 Nehézségi Szint")
            
            difficulty_options = {
                "könnyű": {
                    "description": "Könnyű - feleletválasztós + megoldás",
                    "icon": "🟢",
                    "multiplier": 0.5,
                    "features": ["Feleletválasztós kérdések", "Megoldás megjelenítése", "Segítség a jobb alsó sarokban"]
                },
                "közepes": {
                    "description": "Közepes - feleletválasztós",
                    "icon": "🟡",
                    "multiplier": 1.0,
                    "features": ["Feleletválasztós kérdések", "Nincs megoldás", "Hagyományos quiz"]
                },
                "nehéz": {
                    "description": "Nehéz - szabad szöveges bevitel",
                    "icon": "🔴",
                    "multiplier": 1.5,
                    "features": ["Szöveges bevitel", "Pontos válasz szükséges", "Legnehezebb mód"]
                }
            }
            
            selected_difficulty = st.selectbox(
                "Válassz nehézségi szintet:",
                list(difficulty_options.keys()),
                format_func=lambda x: f"{difficulty_options[x]['icon']} {x}"
            )
            
            # Nehézség leírása
            if selected_difficulty in difficulty_options:
                difficulty_info = difficulty_options[selected_difficulty]
                st.markdown(f"**{difficulty_info['description']}**")
                st.markdown("**Jellemzők:**")
                for feature in difficulty_info['features']:
                    st.markdown(f"• {feature}")
                st.markdown(f"**Pontszám szorzó:** {difficulty_info['multiplier']}x")
        
        # Visszaadjuk a kiválasztott értékeket
        return selected_mode, selected_difficulty
        return selected_mode, selected_difficulty
    
    @staticmethod
    def show_mode_info(mode_manager: QuizModeManager):
        """Aktuális mód információk megjelenítése"""
        config = mode_manager.get_mode_config()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            mode_name = config["mode"].title()
            st.metric("Mód", mode_name)
        
        with col2:
            difficulty_name = config["difficulty"].title()
            st.metric("Nehézség", difficulty_name)
        
        with col3:
            if config["lives"] is not None:
                st.metric("Életek", config["lives"])
            else:
                st.metric("Életek", "∞")
        
        with col4:
            st.metric("Streak", config["streak"])
    
    @staticmethod
    def show_timer(start_time, time_limit):
        """Időzítő megjelenítése"""
        if time_limit is None:
            return
        
        remaining = time_limit - (datetime.now() - start_time).total_seconds()
        remaining = max(0, remaining)
        
        # Progress bar
        progress = remaining / time_limit
        st.progress(progress)
        
        # Idő kijelzése
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        st.markdown(f"**⏱️ Hátralévő idő: {minutes:02d}:{seconds:02d}**")
        
        return remaining <= 0

class QuizScoring:
    """Pontszámítás különböző módokhoz"""
    
    @staticmethod
    def calculate_score(mode: QuizMode, difficulty: DifficultyLevel, 
                       correct_answers: int, total_questions: int, 
                       time_taken: float, streak: int, lives_remaining: int = None):
        """Pontszám kiszámítása"""
        
        # Alap pontszám - elkerüljük a nullával való osztást
        if total_questions == 0:
            base_score = 0
        else:
            base_score = (correct_answers / total_questions) * 100
        
        # Nehézségi szorzó
        difficulty_multipliers = {
            DifficultyLevel.EASY: 0.5,
            DifficultyLevel.MEDIUM: 1.0,
            DifficultyLevel.HARD: 1.5
        }
        
        multiplier = difficulty_multipliers.get(difficulty, 1.0)
        
        # Mód-specifikus bónuszok
        mode_bonus = 0
        
        if mode == QuizMode.TIMED:
            # Idő bónusz (gyorsabb = több pont)
            time_bonus = max(0, (30 - time_taken) * 2)
            mode_bonus += time_bonus
        
        elif mode == QuizMode.SURVIVAL:
            # Élet bónusz
            if lives_remaining is not None:
                life_bonus = lives_remaining * 10
                mode_bonus += life_bonus
        
        elif mode == QuizMode.CHALLENGE:
            # Kihívás bónusz (idő + élet)
            time_bonus = max(0, (20 - time_taken) * 3)
            life_bonus = (lives_remaining or 0) * 20
            mode_bonus += time_bonus + life_bonus
        
        # Streak bónusz
        streak_bonus = streak * 2
        
        # Végső pontszám
        final_score = (base_score + mode_bonus + streak_bonus) * multiplier
        
        return {
            "base_score": round(base_score, 2),
            "difficulty_multiplier": multiplier,
            "mode_bonus": round(mode_bonus, 2),
            "streak_bonus": round(streak_bonus, 2),
            "final_score": round(final_score, 2)
        }

if __name__ == "__main__":
    # Test the quiz modes
    manager = QuizModeManager()
    manager.set_mode(QuizMode.TIMED, time_limit=30)
    manager.set_difficulty(DifficultyLevel.HARD)
    
    print("Quiz modes module loaded successfully!")
    print(f"Current mode: {manager.current_mode.value}")
    print(f"Current difficulty: {manager.current_difficulty.value}") 