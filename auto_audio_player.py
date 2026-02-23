"""
🎵 Automatikus Audio Lejátszó Komponens
Automatikusan elindítja az audio lejátszást a kérdések megjelenésekor
"""

import base64
import streamlit as st
import streamlit.components.v1 as components
import os
from pathlib import Path

def auto_audio_player(audio_file_path, audio_filename=None):
    """
    Automatikus audio lejátszó komponens

    Args:
        audio_file_path (str): Az audio fájl elérési útja
        audio_filename (str, optional): Az audio fájl neve megjelenítéshez
    """

    if not audio_file_path or not os.path.exists(audio_file_path):
        st.warning("⚠️ Audio fájl nem található")
        return

    # Audio fájlnév kinyerése, ha nincs megadva
    if audio_filename is None:
        audio_filename = os.path.basename(audio_file_path)

    # Audio fájlnév megjelenítése
    st.markdown(f"### 🎵 Hallgasd meg a zenét: **{audio_filename}**")

    # Base64 kódolás (data URI-hoz base64 kell, hex nem megfelelő)
    with open(audio_file_path, "rb") as f:
        audio_bytes = f.read()
    b64_audio = base64.b64encode(audio_bytes).decode()

    # HTML és JavaScript az automatikus lejátszáshoz
    html_code = f"""
    <div style="margin: 10px 0;">
        <audio id="autoAudio" controls autoplay style="width: 100%;">
            <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
            A böngésződ nem támogatja az audio lejátszást.
        </audio>
    </div>
    
    <script>
    (function() {{
        // Várunk, amíg az oldal betöltődik
        function initAutoPlay() {{
            const audioElement = document.getElementById('autoAudio');
            if (audioElement) {{
                // Automatikus lejátszás indítása
                audioElement.play().catch(function(error) {{
                    console.log('Automatikus lejátszás nem sikerült:', error);
                    // Felhasználói interakció szükséges lehet
                    console.log('Kérjük, kattints az audio lejátszás gombra');
                }});
                
                // Hangerő beállítása (50%)
                audioElement.volume = 0.5;
                
                // Eseménykezelők
                audioElement.addEventListener('play', function() {{
                    console.log('Audio lejátszás elindult');
                }});
                
                audioElement.addEventListener('error', function(e) {{
                    console.log('Audio lejátszási hiba:', e);
                }});
            }}
        }}
        
        // Több próbálkozás az automatikus lejátszáshoz
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initAutoPlay);
        }} else {{
            initAutoPlay();
        }}
        
        // Késleltetett próbálkozás is
        setTimeout(initAutoPlay, 500);
        setTimeout(initAutoPlay, 1000);
        setTimeout(initAutoPlay, 2000);
    }})();
    </script>
    """
    
    # Komponens megjelenítése
    components.html(html_code, height=100)

    # Fallback: Streamlit audio komponens
    st.markdown("**Vagy használd ezt a lejátszót:**")
    st.audio(audio_file_path, format="audio/mp3")

def auto_audio_player_simple(audio_file_path, audio_filename=None):
    """
    Egyszerű automatikus audio lejátszó Streamlit audio komponenssel
    
    Args:
        audio_file_path (str): Az audio fájl elérési útja
        audio_filename (str, optional): Az audio fájl neve megjelenítéshez
    """
    
    if not audio_file_path or not os.path.exists(audio_file_path):
        st.warning("⚠️ Audio fájl nem található")
        return
    
    # Audio fájlnév kinyerése, ha nincs megadva
    if audio_filename is None:
        audio_filename = os.path.basename(audio_file_path)
    
    # Audio fájlnév megjelenítése
    st.markdown(f"### 🎵 Hallgasd meg a zenét: **{audio_filename}**")

    # Path alapú lejátszás – memóriaoptimalizált (nem olvassuk be a teljes fájlt)
    st.audio(audio_file_path, format="audio/mp3")
    
    # JavaScript az automatikus lejátszáshoz
    st.markdown("""
    <script>
    // Várunk, amíg az oldal betöltődik
    document.addEventListener('DOMContentLoaded', function() {
        // Megkeressük az audio elemet
        const audioElement = document.querySelector('audio');
        if (audioElement) {
            // Automatikus lejátszás indítása
            audioElement.play().catch(function(error) {
                console.log('Automatikus lejátszás nem sikerült:', error);
            });
            
            // Hangerő beállítása (50%)
            audioElement.volume = 0.5;
        }
    });
    
    // Alternatív megoldások különböző időzítésekkel
    setTimeout(function() {
        const audioElement = document.querySelector('audio');
        if (audioElement) {
            audioElement.play().catch(function(error) {
                console.log('Automatikus lejátszás nem sikerült (1s):', error);
            });
            audioElement.volume = 0.5;
        }
    }, 1000);
    
    setTimeout(function() {
        const audioElement = document.querySelector('audio');
        if (audioElement) {
            audioElement.play().catch(function(error) {
                console.log('Automatikus lejátszás nem sikerült (2s):', error);
            });
            audioElement.volume = 0.5;
        }
    }, 2000);
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Test the component
    st.title("🎵 Automatikus Audio Lejátszó Teszt")
    
    # Teszt audio fájl
    test_audio_path = "audio_files/1_Ariana_Grande.mp3"
    
    if os.path.exists(test_audio_path):
        st.success("✅ Teszt audio fájl található")
        auto_audio_player_simple(test_audio_path, "Teszt zene")
    else:
        st.error("❌ Teszt audio fájl nem található")
        st.info("Kérjük, helyezz el egy audio fájlt az audio_files mappában") 