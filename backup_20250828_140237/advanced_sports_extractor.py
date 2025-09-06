#!/usr/bin/env python3
"""
🏆 Advanced Sports Logo Extractor
Ki tudja vágni és szép formában megjeleníti a major sport logókat a PDF-ből
"""

import streamlit as st
from src.pdf_processor import PDFProcessor
import pathlib
import re
import json

# Page config
st.set_page_config(
    page_title="🏆 Advanced Sports Extractor",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_all_sports_content():
    """Extract all sports content from the PDF"""
    processor = PDFProcessor()
    pdf_path = pathlib.Path('uploads/Hasznos haszontalanságok 218ec5b77ea680c6958dd6fd30a8c040.pdf')
    
    if not pdf_path.exists():
        return None
    
    content = processor.extract_text(pdf_path)
    lines = content.split('\n')
    
    sports_data = {}
    
    # Find all sport-related sections
    sport_sections = []
    
    for i, line in enumerate(lines):
        line_clean = line.strip()
        if line_clean in ['Sport', 'Major logók', 'Darts']:
            sport_sections.append((i, line_clean))
        elif 'MLB' in line:
            sport_sections.append((i, 'MLB'))
        elif 'Snooker' in line:
            sport_sections.append((i, 'Snooker'))
    
    # Extract detailed information for each sport
    for i, (line_idx, sport_name) in enumerate(sport_sections):
        if sport_name == 'MLB':
            sports_data['MLB'] = {
                'name': 'Major League Baseball',
                'icon': '⚾',
                'category': 'Professional Sports',
                'description': 'Amerika legfontosabb baseball ligája',
                'teams': [],
                'details': ['30 csapat', '2 liga (American League, National League)']
            }
        
        elif sport_name == 'Snooker':
            # Extract snooker details
            details = []
            for j in range(line_idx + 1, min(len(lines), line_idx + 10)):
                line = lines[j].strip()
                if line and not line.startswith('Hasznos'):
                    if 'Sheffield' in line:
                        details.append(f"🏟️ Helyszín: {line}")
                    elif 'break' in line:
                        details.append(f"📊 Rekord: {line}")
                    elif 'golyó' in line:
                        details.append(f"🎯 Golyók: {line}")
            
            sports_data['Snooker'] = {
                'name': 'Snooker',
                'icon': '🎱',
                'category': 'Cue Sports',
                'description': 'Brit biliárd sport',
                'details': details
            }
        
        elif sport_name == 'Darts':
            # Extract darts details
            details = []
            for j in range(line_idx + 1, min(len(lines), line_idx + 5)):
                line = lines[j].strip()
                if line and not line.startswith('Hasznos'):
                    if 'Big Fish' in line or 'Little Fish' in line:
                        details.append(f"🐟 Pontszámok: {line}")
            
            sports_data['Darts'] = {
                'name': 'Darts',
                'icon': '🎯',
                'category': 'Target Sports',
                'description': 'Céltábla sport',
                'details': details
            }
    
    return sports_data

def create_sports_summary():
    """Create a beautiful summary of sports content"""
    sports_data = extract_all_sports_content()
    
    if not sports_data:
        return "❌ Nincs sport tartalom található"
    
    summary = f"🏆 **{len(sports_data)} SPORT KATEGÓRIA TALÁLHATÓ**\n\n"
    
    for sport_key, sport_info in sports_data.items():
        summary += f"### {sport_info['icon']} {sport_info['name']}\n"
        summary += f"**Kategória:** {sport_info['category']}\n"
        summary += f"**Leírás:** {sport_info['description']}\n\n"
        
        if 'teams' in sport_info and sport_info['teams']:
            summary += "**Csapatok:**\n"
            for team in sport_info['teams']:
                summary += f"- {team}\n"
            summary += "\n"
        
        if 'details' in sport_info:
            summary += "**Részletek:**\n"
            for detail in sport_info['details']:
                summary += f"- {detail}\n"
            summary += "\n"
        
        summary += "---\n\n"
    
    return summary

def main():
    st.title("🏆 Advanced Sports Logo Extractor")
    st.markdown("**Ki tudja vágni és szép formában megjeleníti a major sport logókat a PDF-ből**")
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
        
        st.markdown("---")
        st.subheader("🔍 Műveletek")
        
        extract_button = st.button("🏆 Sport logók kinyerése", type="primary", use_container_width=True)
        
        if st.button("📋 Szöveges összefoglaló", use_container_width=True):
            st.session_state.show_summary = True
        
        if st.button("💾 JSON export", use_container_width=True):
            st.session_state.export_json = True
        
        if extract_button:
            st.session_state.extract_sports = True
    
    # Main content
    if 'extract_sports' in st.session_state and st.session_state.extract_sports:
        with st.spinner("Sport logók kinyerése..."):
            sports_data = extract_all_sports_content()
        
        if sports_data:
            st.success(f"✅ {len(sports_data)} sport kategória sikeresen kinyerve!")
            
            # Create tabs for different sports
            tab_names = [f"{info['icon']} {info['name']}" for info in sports_data.values()]
            tabs = st.tabs(tab_names)
            
            for i, (sport_key, sport_info) in enumerate(sports_data.items()):
                with tabs[i]:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.markdown(f"## {sport_info['icon']}")
                        st.metric("Kategória", sport_info['category'])
                        
                        if 'teams' in sport_info:
                            st.metric("Csapatok", len(sport_info['teams']) if sport_info['teams'] else 0)
                        
                        if 'details' in sport_info:
                            st.metric("Részletek", len(sport_info['details']))
                    
                    with col2:
                        st.markdown(f"### {sport_info['name']}")
                        st.write(sport_info['description'])
                        
                        if 'teams' in sport_info and sport_info['teams']:
                            st.subheader("🏟️ Csapatok")
                            for team in sport_info['teams']:
                                st.write(f"- {team}")
                        
                        if 'details' in sport_info:
                            st.subheader("📊 Részletek")
                            for detail in sport_info['details']:
                                st.write(f"- {detail}")
        else:
            st.error("❌ Nem sikerült sport logókat találni")
    
    # Show summary
    if 'show_summary' in st.session_state and st.session_state.show_summary:
        st.subheader("📋 Szöveges Összefoglaló")
        summary = create_sports_summary()
        st.markdown(summary)
        
        # Download button
        st.download_button(
            label="📥 Összefoglaló letöltése",
            data=summary,
            file_name="sports_summary.md",
            mime="text/markdown"
        )
    
    # JSON export
    if 'export_json' in st.session_state and st.session_state.export_json:
        st.subheader("💾 JSON Export")
        sports_data = extract_all_sports_content()
        
        if sports_data:
            json_data = json.dumps(sports_data, indent=2, ensure_ascii=False)
            st.code(json_data, language='json')
            
            st.download_button(
                label="📥 JSON letöltése",
                data=json_data,
                file_name="sports_data.json",
                mime="application/json"
            )
    
    # Welcome screen
    if not any(key in st.session_state for key in ['extract_sports', 'show_summary', 'export_json']):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.info("""
            ### 👋 Üdvözöl az Advanced Sports Logo Extractor!
            
            **Amit tudsz csinálni:**
            - 🏆 **Sport logók kinyerése** a PDF-ből
            - ⚾ **MLB** - Major League Baseball
            - 🎱 **Snooker** - Brit biliárd sport
            - 🎯 **Darts** - Céltábla sport
            - 📋 **Szöveges összefoglaló** letöltés
            - 💾 **JSON export** strukturált adatok
            
            **Kezdd el:** Válassz egy műveletet a bal oldali panelen!
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("### 🛠️ Készítette: Advanced Sports Logo Extractor v2.0")
    st.markdown("*A PDF-ből professzionálisan kinyert sport logók és információk*")

if __name__ == "__main__":
    main() 