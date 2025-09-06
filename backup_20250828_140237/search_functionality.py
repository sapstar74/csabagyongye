# Search functionality for quiz app

import streamlit as st

def display_search_interface():
    """Display search interface"""
    st.header("🔍 Keresés")
    
    # Search input
    search_term = st.text_input("Keresési kifejezés:", placeholder="Írd be a keresendő szöveget...")
    
    if search_term:
        st.info(f"Keresési eredmények a következőre: '{search_term}'")
        st.write("A keresési funkció fejlesztés alatt áll.")
    else:
        st.info("Írj be egy keresési kifejezést a kereséshez.")
    
    # Search filters
    st.subheader("Szűrők")
    col1, col2 = st.columns(2)
    
    with col1:
        search_topics = st.multiselect(
            "Témakörök:",
            ["Festmények", "Magyar könnyűzene", "Nemzetközi zenekarok", "Vegyes"],
            default=["Festmények", "Magyar könnyűzene", "Nemzetközi zenekarok", "Vegyes"]
        )
    
    with col2:
        search_difficulty = st.selectbox(
            "Nehézség:",
            ["Minden", "Könnyű", "Közepes", "Nehéz"]
        )
    
    # Search results placeholder
    if search_term and search_topics:
        st.subheader("Keresési eredmények")
        st.write("A keresési eredmények itt jelennek meg...") 