"""
Csabagyöngye – Streamlit Cloud
Ez a fájl a Streamlit Cloud-on futó fő alkalmazás
"""

import streamlit as st

st.set_page_config(
    page_title="Csabagyöngye",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Import és futtatás a quiz_app_advanced.py-ból
from quiz_app_advanced import main

if __name__ == "__main__":
    main() 