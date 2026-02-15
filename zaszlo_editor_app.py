"""
🏳️ Zászló Szerkesztő és Kvíz Alkalmazás

Ez az alkalmazás:
1. Letölti a világ zászlóinak nagyfelbontású képeit a Github Flags forrásról
2. Egy szerkesztő felületet kínál, ahol négyzetes formában bizonyos részletek kivágást biztosítja
3. Ezekből a részletekből egy kvíz játékot készít
"""

import streamlit as st
import requests
from PIL import Image, ImageDraw
import json
import os
from pathlib import Path
import random
import base64
from io import BytesIO
import time
import streamlit.components.v1 as components

# Mappa struktúra
FLAGS_DIR = Path("zaszlo_kepek")
CROPS_DIR = Path("data") / "flags" / "crop"
DATA_DIR = Path("zaszlo_data")

# Mappák létrehozása
FLAGS_DIR.mkdir(exist_ok=True)
CROPS_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Konstansok
QUIZ_DATA_FILE = DATA_DIR / "quiz_data.json"
FLAGS_METADATA_FILE = DATA_DIR / "flags_metadata.json"

# Ország kódok listája (ISO 3166-1 alpha-2)
COUNTRY_CODES = [
    "AD", "AE", "AF", "AG", "AI", "AL", "AM", "AO", "AQ", "AR", "AS", "AT", "AU", "AW", "AX", "AZ",
    "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BL", "BM", "BN", "BO", "BQ", "BR", "BS",
    "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CI", "CK", "CL", "CM", "CN",
    "CO", "CR", "CU", "CV", "CW", "CX", "CY", "CZ", "DE", "DJ", "DK", "DM", "DO", "DZ", "EC", "EE",
    "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FM", "FO", "FR", "GA", "GB", "GD", "GE", "GF",
    "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ", "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM",
    "HN", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JM",
    "JO", "JP", "KE", "KG", "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC",
    "LI", "LK", "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MF", "MG", "MH", "MK",
    "ML", "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ", "NA",
    "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA", "PE", "PF", "PG",
    "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA", "RE", "RO", "RS", "RU", "RW",
    "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ", "SK", "SL", "SM", "SN", "SO", "SR", "SS",
    "ST", "SV", "SX", "SY", "SZ", "TC", "TD", "TF", "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO",
    "TR", "TT", "TV", "TW", "TZ", "UA", "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI",
    "VN", "VU", "WF", "WS", "YE", "YT", "ZA", "ZM", "ZW"
]

# Ország nevek magyarul (fontosabb országok)
COUNTRY_NAMES = {
    "HU": "Magyarország", "US": "Egyesült Államok", "GB": "Egyesült Királyság", "DE": "Németország",
    "FR": "Franciaország", "IT": "Olaszország", "ES": "Spanyolország", "RU": "Oroszország",
    "CN": "Kína", "JP": "Japán", "IN": "India", "BR": "Brazília", "AU": "Ausztrália",
    "CA": "Kanada", "MX": "Mexikó", "AR": "Argentína", "ZA": "Dél-afrikai Köztársaság",
    "EG": "Egyiptom", "TR": "Törökország", "IR": "Irán", "SA": "Szaúd-Arábia",
    "KR": "Dél-Korea", "TH": "Thaiföld", "ID": "Indonézia", "VN": "Vietnam",
    "PH": "Fülöp-szigetek", "MY": "Malajzia", "SG": "Szingapúr", "NZ": "Új-Zéland",
    "NO": "Norvégia", "SE": "Svédország", "DK": "Dánia", "FI": "Finnország",
    "PL": "Lengyelország", "NL": "Hollandia", "BE": "Belgium", "CH": "Svájc",
    "AT": "Ausztria", "CZ": "Csehország", "GR": "Görögország", "PT": "Portugália",
    "RO": "Románia", "BG": "Bulgária", "HR": "Horvátország", "RS": "Szerbia",
    "UA": "Ukrajna", "BY": "Fehéroroszország", "IL": "Izrael", "AE": "Egyesült Arab Emírségek"
}

def get_country_name(code):
    """Ország név lekérése kódból"""
    return COUNTRY_NAMES.get(code, code)

def get_flag_url(country_code, size="1000px"):
    """
    Zászló URL generálása flagcdn.com API-ból (megbízhatóbb)
    Támogatott méretek: w320, w640, w1280, w2560 (vagy 1000px -> w1280)
    """
    # Méret leképezés
    size_map = {
        "100px": "w320",
        "250px": "w640", 
        "1000px": "w1280"
    }
    
    # Ha a méret a map-ben van, használjuk, különben próbáljuk meg a flagcdn-et
    cdn_size = size_map.get(size, "w1280")
    
    # Speciális esetek kezelése
    if country_code.upper() == "UN":
        return f"https://flagcdn.com/{cdn_size}/un.png"
    elif country_code.upper() == "EU":
        return f"https://flagcdn.com/{cdn_size}/eu.png"
    elif country_code.upper() == "GB-WLS":
        return f"https://flagcdn.com/{cdn_size}/gb-wls.png"
    elif country_code.upper() == "XK":
        return f"https://flagcdn.com/{cdn_size}/xk.png"
    else:
        return f"https://flagcdn.com/{cdn_size}/{country_code.lower()}.png"

def download_flag(country_code, size="1000px", force=False):
    """
    Zászló letöltése és mentése
    """
    flag_path = FLAGS_DIR / f"{country_code.lower()}_{size}.png"
    
    # Ha már létezik és nem kényszerített letöltés
    if flag_path.exists() and not force:
        return flag_path
    
    url = get_flag_url(country_code, size)
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(flag_path, 'wb') as f:
            f.write(response.content)
        
        return flag_path
    except Exception as e:
        st.error(f"Hiba a zászló letöltésekor ({country_code}): {str(e)}")
        return None

def load_quiz_data():
    """Kvíz adatok betöltése"""
    if QUIZ_DATA_FILE.exists():
        with open(QUIZ_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_quiz_data(quiz_data):
    """Kvíz adatok mentése"""
    with open(QUIZ_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(quiz_data, f, ensure_ascii=False, indent=2)

def crop_image_square(image_path, x, y, size):
    """
    Négyzetes kivágás készítése egy képből
    """
    try:
        img = Image.open(image_path)
        width, height = img.size
        
        # Koordináták normalizálása és korlátozása
        x = max(0, min(x, width - size))
        y = max(0, min(y, height - size))
        
        # Négyzetes kivágás
        crop = img.crop((x, y, x + size, y + size))
        
        return crop
    except Exception as e:
        st.error(f"Hiba a kép kivágásakor: {str(e)}")
        return None

def image_to_base64(image):
    """Kép konvertálása base64 string-gé"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def init_session_state():
    """Session state inicializálása"""
    if 'current_mode' not in st.session_state:
        st.session_state.current_mode = "download"
    if 'selected_country' not in st.session_state:
        st.session_state.selected_country = "HU"
    if 'quiz_data' not in st.session_state:
        st.session_state.quiz_data = load_quiz_data()
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_question_index' not in st.session_state:
        st.session_state.quiz_question_index = 0
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

def show_download_section():
    """Zászlók letöltése"""
    st.header("📥 Zászlók Letöltése")
    
    st.info("""
    Ez a szekció letölti a világ zászlóinak nagyfelbontású képeit a 
    [flagcdn.com](https://flagcdn.com) API-ból (megbízható és gyors forrás).
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        download_mode = st.radio(
            "Letöltési mód:",
            ["Egy ország", "Több ország", "Minden ország"]
        )
        
        if download_mode == "Egy ország":
            selected_country = st.selectbox(
                "Válassz országot:",
                options=COUNTRY_CODES,
                format_func=lambda x: f"{x} - {get_country_name(x)}",
                index=COUNTRY_CODES.index("HU") if "HU" in COUNTRY_CODES else 0
            )
            countries_to_download = [selected_country]
        elif download_mode == "Több ország":
            selected_countries = st.multiselect(
                "Válassz országokat:",
                options=COUNTRY_CODES,
                format_func=lambda x: f"{x} - {get_country_name(x)}",
                default=["HU", "US", "GB", "DE", "FR"]
            )
            countries_to_download = selected_countries
        else:
            countries_to_download = COUNTRY_CODES
    
    with col2:
        size_option = st.selectbox(
            "Kép méret:",
            options=["1000px (w1280)", "250px (w640)", "100px (w320)"],
            index=0,
            help="A zászlók flagcdn.com-ról töltődnek le (w320, w640, w1280 méretekben)"
        )
        
        force_download = st.checkbox("Már letöltött képek újra letöltése", value=False)
    
    if st.button("🚀 Letöltés Indítása", type="primary"):
        if not countries_to_download:
            st.warning("Válassz legalább egy országot!")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        downloaded = 0
        failed = 0
        
        total = len(countries_to_download)
        
        for i, country_code in enumerate(countries_to_download):
            status_text.text(f"Letöltés: {country_code} ({i+1}/{total})")
            progress_bar.progress((i + 1) / total)
            
            # Méret normalizálása (eltávolítjuk a zárójeleket)
            actual_size = size_option.split()[0] if "(" in size_option else size_option
            result = download_flag(country_code, actual_size, force_download)
            if result:
                downloaded += 1
            else:
                failed += 1
            
            # Kis késleltetés a GitHub API rate limiting miatt
            time.sleep(0.1)
        
        status_text.empty()
        progress_bar.empty()
        
        st.success(f"✅ Letöltés kész! Sikeres: {downloaded}, Sikertelen: {failed}")
        
        # Letöltött zászlók listázása
        actual_size = size_option.split()[0] if "(" in size_option else size_option
        existing_flags = list(FLAGS_DIR.glob(f"*_{actual_size}.png"))
        st.info(f"📁 Jelenleg {len(existing_flags)} zászló van letöltve ({actual_size} méretben)")

def show_editor_section():
    """Zászló szerkesztő - részletek kivágása"""
    st.header("✂️ Zászló Szerkesztő - Részletek Kivágása")
    
    # Letöltött zászlók listája
    flag_files = sorted(list(FLAGS_DIR.glob("*_1000px.png")))
    
    if not flag_files:
        st.warning("⚠️ Nincsenek letöltött zászlók! Először tölts le néhány zászlót a 'Zászlók Letöltése' szekcióból.")
        return
    
    # Zászló választása
    flag_options = {f.name: f for f in flag_files}
    selected_flag_name = st.selectbox(
        "Válassz zászlót:",
        options=list(flag_options.keys()),
        format_func=lambda x: x.replace("_1000px.png", "").upper()
    )
    
    selected_flag_path = flag_options[selected_flag_name]
    country_code = selected_flag_name.replace("_1000px.png", "").upper()
    
    # Zászló betöltése és megjelenítése
    try:
        flag_image = Image.open(selected_flag_path)
        width, height = flag_image.size
        
        st.info(f"Zászló mérete: {width}x{height} px")
        
        # Kivágási beállítások
        st.subheader("⚙️ Kivágási Beállítások")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            crop_size = st.slider("Kivágás mérete (px):", 50, min(500, width, height), 200, 10)
        
        with col2:
            max_x = max(0, width - crop_size)
            crop_x = st.slider("X pozíció:", 0, max_x, min(100, max_x), 10, key="crop_x")
        
        with col3:
            max_y = max(0, height - crop_size)
            crop_y = st.slider("Y pozíció:", 0, max_y, min(100, max_y), 10, key="crop_y")
        
        # Koordináta információk
        st.caption(f"💡 Tipp: A középső pozíció X={width//2}, Y={height//2} körül van")
        
        # Vizualizáció a teljes képen
        st.subheader("📐 Zászló Kivágási Terület")
        
        # Kép megjelenítése koordinátákkal
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Session state inicializálása kattintás koordinátákhoz
            click_x_key = f"click_x_{country_code}"
            click_y_key = f"click_y_{country_code}"
            drag_coords_key = f"drag_coords_{country_code}"
            
            if click_x_key not in st.session_state:
                st.session_state[click_x_key] = crop_x
            if click_y_key not in st.session_state:
                st.session_state[click_y_key] = crop_y
            if drag_coords_key not in st.session_state:
                st.session_state[drag_coords_key] = None
            
            # Ha van drag koordináta, használjuk
            if st.session_state[drag_coords_key] is not None:
                drag_x, drag_y = st.session_state[drag_coords_key]
                st.session_state[click_x_key] = drag_x
                st.session_state[click_y_key] = drag_y
                st.session_state[drag_coords_key] = None
                st.rerun()
            
            # Ha van kattintás koordináta, használjuk
            if st.session_state[click_x_key] != crop_x or st.session_state[click_y_key] != crop_y:
                crop_x = st.session_state[click_x_key]
                crop_y = st.session_state[click_y_key]
                # Frissítjük a slider-eket is
                max_x = max(0, width - crop_size)
                max_y = max(0, height - crop_size)
            
            # Kép átméretezése megjelenítéshez (max 800px széles)
            display_width = min(800, width)
            display_ratio = display_width / width
            display_height = int(height * display_ratio)
            
            # Kivágási terület koordinátái a megjelenített mérethez
            disp_crop_x = int(crop_x * display_ratio)
            disp_crop_y = int(crop_y * display_ratio)
            disp_crop_size = int(crop_size * display_ratio)
            
            # Kép másolata (NÉLKÜL a négyzet rajzolásával, mert JavaScript-tel rajzoljuk)
            display_img = flag_image.copy().resize((display_width, display_height), Image.Resampling.LANCZOS)
            
            # Kép base64 kódolása interaktív használathoz
            buffered = BytesIO()
            display_img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            
            # Interaktív kép drag-and-drop-pal
            unique_id = f"flag_editor_{country_code}_{hash(selected_flag_path) % 10000}"
            
            # Frissítés gomb - először ezt jelenítjük meg
            update_clicked = st.button("🔄 Koordináták frissítése (kattintás/húzás után)", 
                                      key=f"update-coords-{unique_id}", 
                                      help="Kattints ide, miután a képen kattintottál vagy húztad a négyzetet")
            
            # Ha a frissítés gombra kattintottak, olvassuk be a localStorage-ból
            if update_clicked:
                # JavaScript-ben a localStorage-ba mentjük a koordinátákat
                # Itt egy HTML/JS megoldással olvassuk be és frissítjük a slider-eket
                st.markdown(f"""
                <script>
                (function() {{
                    const storedX = localStorage.getItem('crop_x_coord_{unique_id}');
                    const storedY = localStorage.getItem('crop_y_coord_{unique_id}');
                    if (storedX && storedY) {{
                        // Koordináták átadása Streamlit-nek query paraméterekkel
                        const url = new URL(window.location);
                        url.searchParams.set('crop_x_{unique_id}', storedX);
                        url.searchParams.set('crop_y_{unique_id}', storedY);
                        window.location.href = url.toString();
                    }}
                }})();
                </script>
                """, unsafe_allow_html=True)
                
                # URL paraméterekből olvassuk be
                query_params = st.query_params
                x_param = f'crop_x_{unique_id}'
                y_param = f'crop_y_{unique_id}'
                if x_param in query_params and y_param in query_params:
                    try:
                        new_x = int(query_params[x_param])
                        new_y = int(query_params[y_param])
                        st.session_state[click_x_key] = new_x
                        st.session_state[click_y_key] = new_y
                        # URL paraméterek törlése
                        del st.query_params[x_param]
                        del st.query_params[y_param]
                        st.rerun()
                    except:
                        pass
            
            st.markdown(f"""
            <div id="flag-container-{unique_id}" style="position: relative; display: inline-block; border: 2px solid #ddd;">
                <img id="flag-img-{unique_id}" 
                     src="data:image/png;base64,{img_base64}" 
                     style="display: block; max-width: 100%; cursor: crosshair;">
                <div id="crop-box-{unique_id}" 
                     style="position: absolute; 
                            border: 3px solid red; 
                            background: rgba(255, 0, 0, 0.1);
                            width: {disp_crop_size}px; 
                            height: {disp_crop_size}px; 
                            left: {disp_crop_x}px; 
                            top: {disp_crop_y}px; 
                            cursor: move;
                            box-sizing: border-box;
                            z-index: 10;">
                    <div style="position: absolute; 
                                left: 50%; 
                                top: 50%; 
                                transform: translate(-50%, -50%); 
                                width: 12px; 
                                height: 12px; 
                                background: red; 
                                border: 2px solid white;
                                border-radius: 50%; 
                                pointer-events: none;"></div>
                </div>
            </div>
            <script>
            (function() {{
                const img = document.getElementById('flag-img-{unique_id}');
                const cropBox = document.getElementById('crop-box-{unique_id}');
                
                let isDragging = false;
                let dragOffset = {{x: 0, y: 0}};
                let currentX = {crop_x};
                let currentY = {crop_y};
                
                const displayRatio = {display_ratio};
                const origWidth = {width};
                const origHeight = {height};
                const cropSize = {crop_size};
                
                function getImageCoords(e) {{
                    const rect = img.getBoundingClientRect();
                    const x = e.clientX - rect.left;
                    const y = e.clientY - rect.top;
                    const scaleX = origWidth / rect.width;
                    const scaleY = origHeight / rect.height;
                    return {{
                        origX: x * scaleX,
                        origY: y * scaleY
                    }};
                }}
                
                function updateCropBox(origX, origY) {{
                    const maxX = origWidth - cropSize;
                    const maxY = origHeight - cropSize;
                    const finalX = Math.max(0, Math.min(origX, maxX));
                    const finalY = Math.max(0, Math.min(origY, maxY));
                    
                    currentX = Math.round(finalX);
                    currentY = Math.round(finalY);
                    
                    const dispX = finalX * displayRatio;
                    const dispY = finalY * displayRatio;
                    
                    cropBox.style.left = dispX + 'px';
                    cropBox.style.top = dispY + 'px';
                    
                    // Koordináták mentése localStorage-ba
                    localStorage.setItem('crop_x_coord_{unique_id}', currentX);
                    localStorage.setItem('crop_y_coord_{unique_id}', currentY);
                }}
                
                // Kép kattintás - négyzet középpontja a kattintás helyére
                img.addEventListener('click', function(e) {{
                    if (!isDragging) {{
                        const coords = getImageCoords(e);
                        updateCropBox(coords.origX - cropSize / 2, coords.origY - cropSize / 2);
                    }}
                }});
                
                // Drag kezdés
                cropBox.addEventListener('mousedown', function(e) {{
                    isDragging = true;
                    const rect = cropBox.getBoundingClientRect();
                    dragOffset.x = e.clientX - rect.left;
                    dragOffset.y = e.clientY - rect.top;
                    e.preventDefault();
                    e.stopPropagation();
                }});
                
                // Drag mozgatás
                document.addEventListener('mousemove', function(e) {{
                    if (isDragging) {{
                        const coords = getImageCoords(e);
                        const imgRect = img.getBoundingClientRect();
                        const scaleX = origWidth / imgRect.width;
                        const scaleY = origHeight / imgRect.height;
                        updateCropBox(coords.origX - dragOffset.x * scaleX, 
                                     coords.origY - dragOffset.y * scaleY);
                    }}
                }});
                
                // Drag vége
                document.addEventListener('mouseup', function(e) {{
                    if (isDragging) {{
                        isDragging = false;
                    }}
                }});
            }})();
            </script>
            """, unsafe_allow_html=True)
            
            st.caption(f"💡 **Kattints a képre**, hogy a négyzet középpontja oda kerüljön! **Vagy húzd a vörös négyzetet** egérrel, majd kattints a 'Koordináták frissítése' gombra!")
            st.caption(f"Kivágási terület: X={crop_x}, Y={crop_y}, Méret={crop_size}px")
            
            # Gyors pozíció beállítás gombok
            st.markdown("**Gyors pozíció beállítás:**")
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            with col_btn1:
                if st.button("↖️ Bal felső", key=f"pos_tl_{country_code}"):
                    st.session_state[click_x_key] = 0
                    st.session_state[click_y_key] = 0
                    st.rerun()
            with col_btn2:
                if st.button("↗️ Jobb felső", key=f"pos_tr_{country_code}"):
                    st.session_state[click_x_key] = max_x
                    st.session_state[click_y_key] = 0
                    st.rerun()
            with col_btn3:
                if st.button("↙️ Bal alsó", key=f"pos_bl_{country_code}"):
                    st.session_state[click_x_key] = 0
                    st.session_state[click_y_key] = max_y
                    st.rerun()
            with col_btn4:
                if st.button("↘️ Jobb alsó", key=f"pos_br_{country_code}"):
                    st.session_state[click_x_key] = max_x
                    st.session_state[click_y_key] = max_y
                    st.rerun()
            
            col_center, col_reset = st.columns([1, 1])
            with col_center:
                if st.button("🎯 Középre", key=f"pos_center_{country_code}"):
                    st.session_state[click_x_key] = max_x // 2
                    st.session_state[click_y_key] = max_y // 2
                    st.rerun()
            with col_reset:
                if st.button("🔄 Visszaállítás", key=f"pos_reset_{country_code}"):
                    st.session_state[click_x_key] = min(100, max_x)
                    st.session_state[click_y_key] = min(100, max_y)
                    st.rerun()
        
        with col2:
            # Kivágás előnézete
            preview_crop = crop_image_square(selected_flag_path, crop_x, crop_y, crop_size)
            
            if preview_crop:
                st.subheader("🔍 Előnézet")
                st.image(preview_crop, caption=f"Négyzetes kivágás ({crop_size}x{crop_size}px)", width=300)
                
                # Kivágás mentése
                st.subheader("💾 Mentés")
                crop_name = st.text_input(
                    "Részlet neve:",
                    value=f"{country_code}_crop_{crop_x}_{crop_y}",
                    key="crop_name_input"
                )
                
                crop_description = st.text_area(
                    "Leírás (opcionális):",
                    value="",
                    height=100,
                    placeholder="Pl: bal felső sarok, középső rész, stb..."
                )
                
                if st.button("💾 Kivágás Mentése", type="primary", use_container_width=True):
                    # Kivágás mentése
                    crop_filename = f"{crop_name}.png"
                    crop_path = CROPS_DIR / crop_filename
                    preview_crop.save(crop_path)
                    
                    # Adatok mentése
                    crop_data = {
                        "country_code": country_code,
                        "country_name": get_country_name(country_code),
                        "crop_name": crop_name,
                        "crop_path": str(crop_path),
                        "crop_size": crop_size,
                        "crop_x": crop_x,
                        "crop_y": crop_y,
                        "description": crop_description,
                        "original_flag": selected_flag_name,
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    # Kvíz adatok frissítése
                    quiz_data = load_quiz_data()
                    quiz_data.append(crop_data)
                    save_quiz_data(quiz_data)
                    st.session_state.quiz_data = quiz_data
                    
                    st.success(f"✅ Kivágás mentve: {crop_filename}")
                    st.balloons()
        
        # Mentett részletek listája
        st.subheader("📋 Mentett Részletek")
        quiz_data = load_quiz_data()
        
        country_crops = [c for c in quiz_data if c.get("country_code") == country_code]
        
        if country_crops:
            st.write(f"**{len(country_crops)} mentett részlet:**")
            cols = st.columns(3)
            for idx, crop in enumerate(country_crops):
                with cols[idx % 3]:
                    if os.path.exists(crop["crop_path"]):
                        crop_img = Image.open(crop["crop_path"])
                        st.image(crop_img, caption=crop.get("crop_name", "Névtelen"), width=150)
                        if crop.get("description"):
                            st.caption(crop["description"])
                        
                        # Törlés gomb
                        if st.button("🗑️ Törlés", key=f"delete_{idx}_{country_code}", use_container_width=True):
                            if os.path.exists(crop["crop_path"]):
                                os.remove(crop["crop_path"])
                            quiz_data.remove(crop)
                            save_quiz_data(quiz_data)
                            st.session_state.quiz_data = quiz_data
                            st.success("✅ Részlet törölve!")
                            st.rerun()
                    else:
                        st.warning("Kép nem található")
        else:
            st.info("Még nincsenek mentett részletek ennél az országnál.")
    
    except Exception as e:
        st.error(f"Hiba a zászló betöltésekor: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

def show_quiz_section():
    """Kvíz játék a kivágott részletekből"""
    st.header("🎮 Zászló Részletek Kvíz")
    
    quiz_data = load_quiz_data()
    
    if not quiz_data:
        st.warning("⚠️ Nincsenek kivágott részletek! Először készíts néhány kivágást a 'Zászló Szerkesztő' szekcióból.")
        return
    
    # Kvíz beállítások
    if not st.session_state.quiz_started:
        st.subheader("Kvíz Beállítások")
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_questions = min(20, len(quiz_data))
            min_questions = min(5, max_questions) if max_questions > 0 else 1
            
            # Ha nincs elég kérdés, ne jelenítsük meg a slider-t
            if max_questions < min_questions:
                num_questions = len(quiz_data)
                st.info(f"Elérhető kérdések száma: {num_questions}")
            else:
                num_questions = st.slider(
                    "Kérdések száma:",
                    min_value=min_questions,
                    max_value=max_questions,
                    value=min(10, max_questions) if max_questions > 0 else 1,
                    step=1
                )
        
        with col2:
            st.metric("Elérhető részletek", len(quiz_data))
        
        if st.button("🎮 Kvíz Indítása", type="primary"):
            # Véletlenszerű kérdések kiválasztása
            selected_crops = random.sample(quiz_data, min(num_questions, len(quiz_data)))
            st.session_state.quiz_questions = selected_crops
            st.session_state.quiz_started = True
            st.session_state.quiz_question_index = 0
            st.session_state.quiz_score = 0
            st.session_state.quiz_answers = {}
            st.rerun()
    
    else:
        # Kvíz futása
        questions = st.session_state.quiz_questions
        current_idx = st.session_state.quiz_question_index
        
        if current_idx >= len(questions):
            # Eredmények
            score = st.session_state.quiz_score
            total = len(questions)
            percentage = int((score / total) * 100)
            
            st.success("🎉 Kvíz befejezve!")
            st.metric("Pontszám", f"{score} / {total}", f"{percentage}%")
            
            # Színkódolt értékelés
            if percentage >= 80:
                st.balloons()
                st.success("Kiváló! 🌟")
            elif percentage >= 60:
                st.info("Jó teljesítmény! 👍")
            else:
                st.warning("Gyakorolj még! 💪")
            
            if st.button("🔄 Új Kvíz", type="primary"):
                st.session_state.quiz_started = False
                st.session_state.quiz_question_index = 0
                st.session_state.quiz_score = 0
                st.rerun()
        else:
            # Kérdés megjelenítése
            current_question = questions[current_idx]
            
            # Progress bar
            progress = (current_idx + 1) / len(questions)
            st.progress(progress)
            st.caption(f"Kérdés {current_idx + 1} / {len(questions)}")
            
            # Kép megjelenítése
            crop_path = current_question.get("crop_path")
            if os.path.exists(crop_path):
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    crop_img = Image.open(crop_path)
                    st.image(crop_img, caption="Melyik ország zászlajának részlete ez?", width=400)
            else:
                st.error("Kép nem található!")
            
            # Válaszlehetőségek
            correct_answer = current_question.get("country_name", current_question.get("country_code"))
            
            # Helyes válasz + 3 véletlen válasz
            all_countries = list(set([q.get("country_name", q.get("country_code")) for q in quiz_data]))
            wrong_answers = random.sample([c for c in all_countries if c != correct_answer], min(3, len(all_countries) - 1))
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            
            # Válasz bekérése
            selected = st.radio(
                "Válassz országot:",
                options=options,
                key=f"answer_{current_idx}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ Válasz Beküldése", type="primary"):
                    is_correct = selected == correct_answer
                    st.session_state.quiz_answers[current_idx] = {
                        "selected": selected,
                        "correct": correct_answer,
                        "is_correct": is_correct
                    }
                    
                    if is_correct:
                        st.session_state.quiz_score += 1
                        st.success(f"✅ Helyes! Ez valóban {correct_answer} zászlajának része!")
                    else:
                        st.error(f"❌ Helytelen. A helyes válasz: {correct_answer}")
                    
                    time.sleep(1.5)
                    st.session_state.quiz_question_index += 1
                    st.rerun()
            
            with col2:
                if st.button("⏭️ Kihagyás"):
                    st.session_state.quiz_question_index += 1
                    st.rerun()
            
            # Statisztika
            st.caption(f"Jelenlegi pontszám: {st.session_state.quiz_score} / {current_idx}")

def main():
    """Fő alkalmazás"""
    st.set_page_config(
        page_title="🏳️ Zászló Szerkesztő és Kvíz",
        page_icon="🏳️",
        layout="wide"
    )
    
    st.title("🏳️ Zászló Szerkesztő és Kvíz Alkalmazás")
    
    st.markdown("""
    Ez az alkalmazás három fő funkciót kínál:
    1. **Zászlók letöltése** - Nagyfelbontású zászlóképek letöltése GitHub-ról
    2. **Részletek kivágása** - Négyzetes formában részletek kivágása és mentése
    3. **Kvíz játék** - Kvíz játék a kivágott részletekből
    """)
    
    init_session_state()
    
    # Főmenü
    tab1, tab2, tab3 = st.tabs(["📥 Zászlók Letöltése", "✂️ Szerkesztő", "🎮 Kvíz"])
    
    with tab1:
        show_download_section()
    
    with tab2:
        show_editor_section()
    
    with tab3:
        show_quiz_section()

if __name__ == "__main__":
    main()

