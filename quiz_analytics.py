"""
📊 Quiz Analytics és Statisztika Modul
Quiz teljesítmény követése és elemzése
"""

import json
import os
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import pandas as pd
import streamlit as st

class QuizAnalytics:
    def __init__(self, data_file="quiz_analytics.json"):
        self.data_file = data_file
        self.analytics_data = self.load_analytics()
    
    def load_analytics(self):
        """Analytics adatok betöltése"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.get_default_analytics()
        return self.get_default_analytics()
    
    def get_default_analytics(self):
        """Alapértelmezett analytics struktúra"""
        return {
            "quiz_sessions": [],
            "topic_performance": {},
            "user_progress": {},
            "difficulty_analysis": {},
            "time_analysis": {},
            "total_quizzes": 0,
            "total_questions_answered": 0,
            "average_score": 0.0
        }
    
    def save_analytics(self):
        """Analytics adatok mentése"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.analytics_data, f, ensure_ascii=False, indent=2)
    
    def record_quiz_session(self, quiz_data):
        """Quiz session rögzítése"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "topics": quiz_data.get("topics", []),
            "total_questions": quiz_data.get("total_questions", 0),
            "correct_answers": quiz_data.get("correct_answers", 0),
            "score_percentage": quiz_data.get("score_percentage", 0),
            "duration_seconds": quiz_data.get("duration_seconds", 0),
            "question_details": quiz_data.get("question_details", [])
        }
        
        self.analytics_data["quiz_sessions"].append(session)
        self.update_statistics()
        self.save_analytics()
    
    def update_statistics(self):
        """Statisztikák frissítése"""
        sessions = self.analytics_data["quiz_sessions"]
        if not sessions:
            return
        
        # Alap statisztikák
        self.analytics_data["total_quizzes"] = len(sessions)
        self.analytics_data["total_questions_answered"] = sum(s["total_questions"] for s in sessions)
        self.analytics_data["average_score"] = sum(s["score_percentage"] for s in sessions) / len(sessions)
        
        # Témakör teljesítmény
        topic_performance = defaultdict(list)
        for session in sessions:
            for topic in session["topics"]:
                topic_performance[topic].append(session["score_percentage"])
        
        self.analytics_data["topic_performance"] = {
            topic: {
                "average_score": sum(scores) / len(scores),
                "total_quizzes": len(scores),
                "best_score": max(scores),
                "worst_score": min(scores)
            }
            for topic, scores in topic_performance.items()
        }
        
        # Idő elemzés
        time_analysis = defaultdict(list)
        for session in sessions:
            hour = datetime.fromisoformat(session["timestamp"]).hour
            time_analysis[hour].append(session["score_percentage"])
        
        self.analytics_data["time_analysis"] = {
            str(hour): {
                "average_score": sum(scores) / len(scores),
                "total_quizzes": len(scores)
            }
            for hour, scores in time_analysis.items()
        }
    
    def get_performance_summary(self):
        """Teljesítmény összefoglaló"""
        return {
            "total_quizzes": self.analytics_data["total_quizzes"],
            "total_questions": self.analytics_data["total_questions_answered"],
            "average_score": round(self.analytics_data["average_score"], 2),
            "best_topic": self.get_best_topic(),
            "worst_topic": self.get_worst_topic(),
            "recent_trend": self.get_recent_trend()
        }
    
    def get_best_topic(self):
        """Legjobb teljesítményű témakör"""
        topic_perf = self.analytics_data["topic_performance"]
        if not topic_perf:
            return None
        
        best_topic = max(topic_perf.items(), key=lambda x: x[1]["average_score"])
        return {
            "topic": best_topic[0],
            "average_score": round(best_topic[1]["average_score"], 2),
            "total_quizzes": best_topic[1]["total_quizzes"]
        }
    
    def get_worst_topic(self):
        """Legrosszabb teljesítményű témakör"""
        topic_perf = self.analytics_data["topic_performance"]
        if not topic_perf:
            return None
        
        worst_topic = min(topic_perf.items(), key=lambda x: x[1]["average_score"])
        return {
            "topic": worst_topic[0],
            "average_score": round(worst_topic[1]["average_score"], 2),
            "total_quizzes": worst_topic[1]["total_quizzes"]
        }
    
    def get_recent_trend(self):
        """Legutóbbi trend elemzése"""
        sessions = self.analytics_data["quiz_sessions"]
        if len(sessions) < 5:
            return "Nincs elég adat a trend elemzéshez"
        
        recent_scores = [s["score_percentage"] for s in sessions[-5:]]
        if len(recent_scores) < 2:
            return "Stabil"
        
        trend = recent_scores[-1] - recent_scores[0]
        if trend > 5:
            return "Javuló"
        elif trend < -5:
            return "Romló"
        else:
            return "Stabil"
    
    def get_topic_breakdown(self):
        """Témakörök lebontása"""
        return self.analytics_data["topic_performance"]
    
    def get_time_breakdown(self):
        """Idő szerinti lebontás"""
        return self.analytics_data["time_analysis"]
    
    def get_weekly_progress(self, weeks=4):
        """Heti progress"""
        sessions = self.analytics_data["quiz_sessions"]
        if not sessions:
            return {}
        
        # Csoportosítás hetente
        weekly_data = defaultdict(list)
        for session in sessions:
            date = datetime.fromisoformat(session["timestamp"]).date()
            week_start = date - timedelta(days=date.weekday())
            weekly_data[week_start.isoformat()].append(session["score_percentage"])
        
        # Heti átlagok
        weekly_averages = {}
        for week, scores in weekly_data.items():
            weekly_averages[week] = {
                "average_score": round(sum(scores) / len(scores), 2),
                "total_quizzes": len(scores)
            }
        
        return dict(list(weekly_averages.items())[-weeks:])

def show_analytics_dashboard():
    """Analytics dashboard megjelenítése"""
    analytics = QuizAnalytics()
    
    st.markdown("## 📊 Quiz Analytics Dashboard")
    
    # Összefoglaló statisztikák
    summary = analytics.get_performance_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Összes Quiz", summary["total_quizzes"])
    
    with col2:
        st.metric("Összes Kérdés", summary["total_questions"])
    
    with col3:
        st.metric("Átlagos Pontszám", f"{summary['average_score']}%")
    
    with col4:
        st.metric("Trend", summary["recent_trend"])
    
    # Témakör teljesítmény
    if summary["best_topic"]:
        st.markdown("### 🏆 Legjobb Témakörök")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Legjobb**: {summary['best_topic']['topic']}
            - Átlag: {summary['best_topic']['average_score']}%
            - Quizek: {summary['best_topic']['total_quizzes']}
            """)
        
        with col2:
            st.markdown(f"""
            **Legrosszabb**: {summary['worst_topic']['topic']}
            - Átlag: {summary['worst_topic']['average_score']}%
            - Quizek: {summary['worst_topic']['total_quizzes']}
            """)
    
    # Témakörök lebontása
    topic_breakdown = analytics.get_topic_breakdown()
    if topic_breakdown:
        st.markdown("### 📈 Témakör Teljesítmény")
        
        topic_data = []
        for topic, data in topic_breakdown.items():
            topic_data.append({
                "Témakör": topic,
                "Átlagos Pontszám": data["average_score"],
                "Quizek Száma": data["total_quizzes"],
                "Legjobb Pontszám": data["best_score"]
            })
        
        df = pd.DataFrame(topic_data)
        st.dataframe(df, use_container_width=True)
    
    # Heti progress
    weekly_progress = analytics.get_weekly_progress()
    if weekly_progress:
        st.markdown("### 📅 Heti Progress")
        
        week_data = []
        for week, data in weekly_progress.items():
            week_data.append({
                "Hét": week,
                "Átlagos Pontszám": data["average_score"],
                "Quizek Száma": data["total_quizzes"]
            })
        
        df_weekly = pd.DataFrame(week_data)
        st.dataframe(df_weekly, use_container_width=True)

if __name__ == "__main__":
    # Test the analytics
    analytics = QuizAnalytics()
    print("Analytics module loaded successfully!")
    print(f"Total quizzes: {analytics.analytics_data['total_quizzes']}") 