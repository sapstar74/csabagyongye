#!/usr/bin/env python3
"""
🏆 Sports Logo Extractor
Ki tudja vágni a major sport logókat a PDF-ből
"""

import streamlit as st
from src.pdf_processor import PDFProcessor
import pathlib
import re

# Page config
st.set_page_config(
    page_title="🏆 Sports Logo Extractor",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_sports_logos():
    """Extract sports logos from the PDF"""
    processor = PDFProcessor()
    pdf_path = pathlib.Path('uploads/Hasznos haszontalanságok 218ec5b77ea680c6958dd6fd30a8c040.pdf')
    
    if not pdf_path.exists():
        return None
    
    content = processor.extract_text(pdf_path)
    lines = content.split('\n')
    
    # Find the Major logók section
    major_index = -1
    for i, line in enumerate(lines):
        if 'Major logók' in line:
            major_index = i
            break
    
    if major_index == -1:
        return None
    
    # Extract sport sections
    sports_data = {}
    
    # Find MLB section (right after Major logók)
    mlb_start = -1
    for i in range(major_index, min(len(lines), major_index + 20)):
        if 'MLB' in lines[i]:
            mlb_start = i
            break
    
    if mlb_start >= 0:
        # MLB teams would be on the next lines
        sports_data['MLB'] = {
            'name': 'Major League Baseball',
            'icon': '⚾',
            'description': 'Amerika legfontosabb baseball ligája',
            'teams': []
        }
    
    # Find Snooker section
    snooker_start = -1
    for i in range(major_index, min(len(lines), major_index + 50)):
        if 'Snooker' in lines[i]:
            snooker_start = i
            break
    
    if snooker_start >= 0:
        sports_data['Snooker'] = {
            'name': 'Snooker',
            'icon': '🎱',
            'description': 'Brit biliárd sport',
            'details': []
        }
        
        # Extract snooker details
        for i in range(snooker_start + 1, min(len(lines), snooker_start + 10)):
            line = lines[i].strip()
            if line and not line.startswith('Hasznos'):
                if 'Sheffield' in line or 'Crucible' in line:
                    sports_data['Snooker']['details'].append(f"🏟️ Helyszín: {line}")
                elif 'break' in line:
                    sports_data['Snooker']['details'].append(f"📊 Rekord: {line}")
                elif 'golyó' in line:
                    sports_data['Snooker']['details'].append(f"🎯 Golyók: {line}")
    
    # Find Darts section
    darts_start = -1
    for i in range(major_index, min(len(lines), major_index + 50)):
        if 'Darts' in lines[i]:
            darts_start = i
            break
    
    if darts_start >= 0:
        sports_data['Darts'] = {
            'name': 'Darts',
            'icon': '🎯',
            'description': 'Céltábla sport',
            'details': []
        }
        
        # Extract darts details
        for i in range(darts_start + 1, min(len(lines), darts_start + 5)):
            line = lines[i].strip()
            if line and not line.startswith('Hasznos'):
                if 'Big Fish' in line or 'Little Fish' in line:
                    sports_data['Darts']['details'].append(f"🐟 Pontszámok: {line}")
    
    return sports_data

def main():
    st.title("🏆 Sports Logo Extractor")
    st.markdown("**Ki tudja vágni a major sport logókat a PDF-ből**")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Beállítások")
        
        # Check if PDF exists
        pdf_path = pathlib.Path('uploads/Hasznos haszontalanságok 218ec5b77ea680c6958dd6fd30a8c040.pdf')
        if pdf_path.exists():
            st.success("✅ PDF betöltve")
            st.metric("Fájl méret", f"{pdf_path.stat().st_size / (1024*1024):.1f} MB")
        else:
            st.error("❌ PDF nem található")
            st.info("Kérlek tölts fel egy PDF-et a főalkalmazásban!")
            return
        
        if st.button("🔍 Sport logók keresése", type="primary"):
            st.session_state.extract_sports = True
    
    # Main content
    if 'extract_sports' in st.session_state and st.session_state.extract_sports:
        with st.spinner("Sport logók keresése..."):
            sports_data = extract_sports_logos()
        
        if sports_data:
            st.success(f"✅ {len(sports_data)} sport kategória találva!")
            
            # Display found sports
            for sport_key, sport_info in sports_data.items():
                st.header(f"{sport_info['icon']} {sport_info['name']}")
                st.write(f"**Leírás:** {sport_info['description']}")
                
                if 'teams' in sport_info:
                    st.subheader("🏟️ Csapatok")
                    if sport_info['teams']:
                        for team in sport_info['teams']:
                            st.write(f"- {team}")
                    else:
                        st.info("Csapat adatok még nem kerültek feldolgozásra")
                
                if 'details' in sport_info:
                    st.subheader("📊 Részletek")
                    for detail in sport_info['details']:
                        st.write(f"- {detail}")
                
                st.markdown("---")
        else:
            st.error("❌ Nem sikerült megtalálni a sport logókat")
    
    else:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### 👋 Üdvözöl a Sports Logo Extractor!
            
            **Amit tudsz csinálni:**
            - 🏆 **Sport logók keresése** a PDF-ben
            - ⚾ **MLB** információk
            - 🎱 **Snooker** részletek
            - 🎯 **Darts** adatok
            - 📊 **Statisztikák** és rekordok
            
            **Kezdd el:** Kattints a "Sport logók keresése" gombra!
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🛠️ Készítette: Sports Logo Extractor v1.0")
    st.markdown("*A PDF-ből kiválogalt sport logók és információk*")

if __name__ == "__main__":
    main() 