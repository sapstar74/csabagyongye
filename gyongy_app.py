"""Csabagyöngye – az új felület belépési pontja.

Futtatás helyben:      streamlit run gyongy_app.py
Streamlit Cloudon:     a „Main file path” legyen gyongy_app.py

A régi felület (streamlit_app.py) változatlanul megmarad, mindkettő
ugyanazt a kérdésbázist (quiz_data.py + topics/) használja.
"""

import streamlit as st

st.set_page_config(page_title="Csabagyöngye", page_icon="🍇", layout="centered", initial_sidebar_state="collapsed")

from gyongy.app import main  # noqa: E402

main()
