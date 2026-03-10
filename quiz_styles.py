"""
Quiz CSS styles: theme overrides and base design system.
"""

import streamlit as st

_LIGHT_OVERRIDES = """
    /* Világos téma: minden felülírás – Streamlit, böngésző dark mode, prefers-color-scheme */
    html, body, html[data-theme="dark"], body[data-theme="dark"],
    [data-theme="dark"] html, [data-theme="dark"] body,
    body:has([data-quiz-theme="light"]), html:has([data-quiz-theme="light"]) {
        color-scheme: light !important;
        background-color: #ffffff !important;
    }
    @media (prefers-color-scheme: dark) {
        html, body, .stApp, [data-testid="stAppViewContainer"],
        section[data-testid="stAppViewContainer"], [data-theme="dark"] .stApp,
        [data-theme="dark"] [data-testid="stAppViewContainer"],
        body:has([data-quiz-theme="light"]) .stApp,
        body:has([data-quiz-theme="light"]) [data-testid="stAppViewContainer"],
        html:has([data-quiz-theme="light"]) .stApp,
        html:has([data-quiz-theme="light"]) [data-testid="stAppViewContainer"] {
            color-scheme: light !important;
            background-color: #ffffff !important;
        }
    }
    :root {
        --color-bg: #ffffff;
        --color-card: #ffffff;
        --color-border: #e7e5e4;
        --color-text: #1a1a1a;
        --color-muted: #44403c;
        --color-sidebar: #f5f5f4;
    }
    /* Világos téma: erős felülírás – magasabb specificitás a Streamlit dark mode ellen */
    html body .stApp, html body [data-testid="stAppViewContainer"],
    body .stApp, body [data-testid="stAppViewContainer"],
    .stApp, [data-testid="stAppViewContainer"], .main .block-container,
    section[data-testid="stAppViewContainer"], section.main,
    [data-theme="dark"] .stApp, [data-theme="dark"] [data-testid="stAppViewContainer"],
    div[data-testid="stAppViewContainer"], .stApp > div,
    body:has([data-quiz-theme="light"]) .stApp,
    body:has([data-quiz-theme="light"]) [data-testid="stAppViewContainer"],
    body:has([data-quiz-theme="light"]) .main .block-container,
    body:has([data-quiz-theme="light"]) section.main {
        background-color: #ffffff !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div,
    [data-theme="dark"] [data-testid="stSidebar"],
    body:has([data-quiz-theme="light"]) [data-testid="stSidebar"] {
        background-color: #f5f5f4 !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stRadio div,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div,
    body:has([data-quiz-theme="light"]) [data-testid="stSidebar"] .stMarkdown,
    body:has([data-quiz-theme="light"]) [data-testid="stSidebar"] label,
    body:has([data-quiz-theme="light"]) [data-testid="stSidebar"] .stRadio label, 
    body:has([data-quiz-theme="light"]) [data-testid="stSidebar"] .stRadio label * {
        color: #1a1a1a !important;
    }
    [data-testid="stSidebar"] .stRadio > div,
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        background-color: transparent !important;
    }
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label span,
    [data-testid="stSidebar"] .stRadio label *,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label * {
        color: #1a1a1a !important;
    }
    .main .block-container p, .main .block-container span, .main .block-container div,
    div[data-testid="stMarkdown"] p, .stMarkdown p, .stMarkdown span,
    h1, h2, h3, h4, .main-header, .question-text {
        color: #1a1a1a !important;
    }
"""

_DARK_OVERRIDES = """
    html, body, body:has([data-quiz-theme="dark"]) { color-scheme: dark !important; }
    @media (prefers-color-scheme: dark) {
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            color-scheme: dark !important;
            background-color: #1a1a1a !important;
        }
    }
    body:has([data-quiz-theme="dark"]) .stApp,
    body:has([data-quiz-theme="dark"]) [data-testid="stAppViewContainer"],
    body:has([data-quiz-theme="dark"]) .main .block-container {
        background-color: #1a1a1a !important;
    }
    body:has([data-quiz-theme="dark"]) [data-testid="stSidebar"],
    body:has([data-quiz-theme="dark"]) [data-testid="stSidebar"] > div {
        background-color: #171717 !important;
    }
    :root {
        --color-bg: #1a1a1a;
        --color-card: #2d2d2d;
        --color-border: #404040;
        --color-text: #fafaf9;
        --color-muted: #a8a29e;
        --color-sidebar: #171717;
    }
    .stApp, [data-testid="stAppViewContainer"], .main .block-container {
        background-color: #1a1a1a !important;
    }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
        background-color: #171717 !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] .stRadio div,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div,
    [data-testid="stSidebar"] .stSelectbox label, [data-testid="stSidebar"] .stSelectbox span,
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] label,
    [data-testid="stSidebar"] div[data-testid="stSelectbox"] span {
        color: #fafaf9 !important;
    }
    [data-testid="stSidebar"] .stRadio label p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label p,
    [data-testid="stSidebar"] .stRadio label span,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label span,
    [data-testid="stSidebar"] .stRadio label *,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label * {
        color: #fafaf9 !important;
    }
    [data-testid="stSidebar"] .stRadio > div,
    [data-testid="stSidebar"] div[data-testid="stRadio"] > div {
        background-color: transparent !important;
    }
    .main-header, .question-text, .summary-box p, .summary-box strong,
    div[data-testid="stMarkdown"] p, .stMarkdown p {
        color: #fafaf9 !important;
    }
    .summary-box h3, .summary-box h4 { color: #94a3b8 !important; }
    .topic-button, .option-button { background: #ffffff !important; border-color: #404040 !important; color: #1a1a1a !important; }
    .topic-button:hover, .option-button:hover { background: #e7e5e4 !important; }
    /* Quiz beállítás csúszkák: értékek piros sötét módban is */
    div[data-testid="stSlider"] [data-testid="stThumbValue"],
    div[data-testid="stSlider"] span,
    div[data-testid="stSlider"] > div > div:last-child {
        color: #dc2626 !important;
    }
    /* Quiz válaszopciók: fehér háttér, sötét betű sötét módban is */
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button,
    #quiz-answer-options ~ div .stButton > button {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button p,
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button span,
    #quiz-answer-options ~ div .stButton > button p,
    #quiz-answer-options ~ div .stButton > button span {
        color: #1a1a1a !important;
    }
    /* Quiz Százalék, Mód, Streak: fekete felirat és érték sötét módban is (világos háttér) */
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"],
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] *,
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] * {
        color: #1a1a1a !important;
    }
    .score-display { background: #2d2d2d !important; color: #fafaf9 !important; border-color: #404040 !important; }
    h1, h2, h3, h4 { color: #fafaf9 !important; }
    /* Végleges Kérdésszám Beállítása sötét módban: világos háttér, sötét szöveg */
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h3,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h4,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h5,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] p,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] label,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] span,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"],
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"] *,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stSlider"] label,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * [data-testid="stCheckbox"] label {
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"] {
        background-color: #f5f5f4 !important;
        border-color: #d6d3d1 !important;
    }
    /* Végleges Kérdésszám Beállítása: gombok olvasható szöveg sötét módban */
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stButton"] > button {
        color: #1a1a1a !important;
        background-color: #f5f5f4 !important;
        border: 2px solid #d6d3d1 !important;
    }
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button p,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button span {
        color: #1a1a1a !important;
    }
"""


def get_theme_css(theme: str) -> str:
    """Return light or dark theme overrides based on theme name."""
    return _LIGHT_OVERRIDES if theme == "light" else _DARK_OVERRIDES


_BASE_CSS_TEMPLATE = """
<style>
    /* Theme-specific color-scheme and background: __THEME_OVERRIDES__ contains them */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* === SZÍNPALETTA === */
    :root {
        /* Elsődleges márkaszín (grafitszürke/mélykék) */
        --brand-primary: #2c3e50;
        /* Akcentus (eredmények, kiemelések) */
        --brand-accent: #0d9488;
        /* Neutrális árnyalatok */
        --neutral-50: #fafaf9;
        --neutral-100: #f5f5f4;
        --neutral-200: #e7e5e4;
        --neutral-300: #d6d3d1;
        --neutral-400: #a8a29e;
        --neutral-500: #78716c;
        --neutral-600: #57534e;
        --neutral-700: #44403c;
        --neutral-800: #292524;
        /* Sémaváltozók */
        --color-bg: var(--neutral-50);
        --color-card: #ffffff;
        --color-border: var(--neutral-200);
        --color-text: var(--neutral-800);
        --color-muted: var(--neutral-500);
        --color-success: #0f766e;
        --color-error: #b91c1c;
        /* Komponens: 8–12px radius, diszkrét árnyékok */
        --radius-sm: 8px;
        --radius-md: 10px;
        --radius-lg: 12px;
        --shadow-sm: 0 1px 3px rgba(44, 62, 80, 0.06);
        --shadow-md: 0 4px 12px rgba(44, 62, 80, 0.08);
        --shadow-lg: 0 8px 24px rgba(44, 62, 80, 0.1);
        /* 8px spacing grid */
        --space-1: 8px;
        --space-2: 16px;
        --space-3: 24px;
        --space-4: 32px;
        --space-5: 40px;
    }
    
    /* === TIPOGRAFIA: Inter, max 2 betűcsalád === */
    .main-header, .question-text, .summary-box, .topic-button, .option-button,
    div[data-testid="stMarkdown"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        line-height: 1.2;
        text-align: center;
        color: var(--brand-primary);
        margin-bottom: var(--space-3);
        padding-bottom: var(--space-2);
        border-bottom: 1px solid var(--color-border);
    }
    .question-text {
        font-size: 1.25rem;
        font-weight: 500;
        line-height: 1.6;
        margin-bottom: var(--space-3);
        color: var(--color-text);
        letter-spacing: -0.01em;
    }
    
    /* === KOMPONENSEK: egységes radius, árnyékok === */
    .topic-button {
        background: var(--color-card);
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        padding: var(--space-2) var(--space-3);
        margin: var(--space-1);
        text-align: center;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
    }
    .topic-button:hover {
        background: var(--neutral-100);
        border-color: var(--brand-accent);
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .topic-button.selected {
        background: #f5f5f4 !important;
        color: #1a1a1a !important;
        border-color: var(--brand-accent);
        box-shadow: var(--shadow-md);
    }
    .quiz-container {
        background: var(--color-card);
        border-radius: var(--radius-lg);
        padding: var(--space-4);
        box-shadow: var(--shadow-sm);
        margin: var(--space-3) 0;
        border: 1px solid var(--color-border);
    }
    div[data-testid="stMarkdown"] table {
        font-size: 0.9375rem;
        margin: var(--space-2) 0;
        border-collapse: collapse;
        border-radius: var(--radius-sm);
        overflow: hidden;
    }
    div[data-testid="stMarkdown"] table th, div[data-testid="stMarkdown"] table td {
        padding: var(--space-1) var(--space-2);
        border: 1px solid var(--color-border);
    }
    .option-button {
        width: 100%;
        text-align: left;
        padding: var(--space-2) var(--space-3);
        margin: var(--space-1) 0;
        border: 1px solid var(--color-border);
        border-radius: var(--radius-lg);
        background: var(--color-card);
        transition: all 0.2s ease;
    }
    /* Minden gomb: fehér háttér, vastag keret, árnyék */
    .stButton > button,
    div[data-testid="stButton"] > button {
        height: 48px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        margin-bottom: var(--space-2) !important;
        border-radius: var(--radius-lg) !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease !important;
        border: 2px solid #d6d3d1 !important;
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    .stButton > button:hover,
    div[data-testid="stButton"] > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12) !important;
        background-color: #f5f5f4 !important;
        color: #1a1a1a !important;
    }
    .stButton > button p, .stButton > button span,
    div[data-testid="stButton"] > button p, div[data-testid="stButton"] > button span {
        color: #1a1a1a !important;
    }
    /* Quiz válaszopciók: fehér háttér, sötét betű mindig */
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button,
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] div[data-testid="stButton"] > button,
    #quiz-answer-options ~ div .stButton > button,
    #quiz-answer-options ~ div div[data-testid="stButton"] > button {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
        border-color: #d6d3d1 !important;
    }
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button:hover,
    #quiz-answer-options ~ div .stButton > button:hover {
        background-color: #f5f5f4 !important;
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button p,
    [data-testid="stMarkdown"]:has(#quiz-answer-options) ~ [data-testid="stHorizontalBlock"] .stButton > button span,
    #quiz-answer-options ~ div .stButton > button p,
    #quiz-answer-options ~ div .stButton > button span {
        color: #1a1a1a !important;
    }
    /* Quiz Százalék, Mód, Streak metrikák: fekete felirat és érték */
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"],
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] label,
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] div,
    [data-testid="stMarkdown"]:has(#quiz-metrics-row) ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] span,
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] label,
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] div,
    #quiz-metrics-row ~ [data-testid="stHorizontalBlock"] [data-testid="metric-container"] span {
        color: #1a1a1a !important;
    }
    /* Végleges Kérdésszám, Témakörök, Mód, Nehézség: olvasható szöveg (világos háttér, sötét szöveg) */
    .quiz-settings-section .stButton > button,
    .quiz-settings-section div[data-testid="stButton"] > button {
        background-color: #f5f5f4 !important;
        color: #1a1a1a !important;
        border: 2px solid #d6d3d1 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
    }
    .quiz-settings-section .stButton > button p,
    .quiz-settings-section .stButton > button span,
    .quiz-settings-section div[data-testid="stButton"] > button p,
    .quiz-settings-section div[data-testid="stButton"] > button span {
        color: #1a1a1a !important;
    }
    /* Quiz beállítás csúszkák: értékek (min/max/aktuális) piros színű (láthatóság) */
    div[data-testid="stSlider"] [data-testid="stThumbValue"],
    div[data-testid="stSlider"] [data-testid="stThumbValue"] *,
    div[data-testid="stSlider"] > div > div:last-child,
    div[data-testid="stSlider"] > div > div:last-child *,
    div[data-testid="stSlider"] span {
        color: #dc2626 !important;
    }
    /* Mód és Nehézség st.radio (sidebar): kiválasztott opció – szürke háttér, fekete betű */
    [data-testid="stSidebar"] .stRadio label:has(input:checked),
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) {
        background-color: #9ca3af !important;
        color: #000000 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    [data-testid="stSidebar"] .stRadio label:has(input:checked) *,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label:has(input:checked) * {
        color: #000000 !important;
    }
    /* Legördülő menük, selectbox, radio: világos háttér, sötét szöveg – nem fekete */
    .stSelectbox > div, .stSelectbox div[data-baseweb="select"],
    div[data-testid="stSelectbox"] > div,
    [data-baseweb="select"] {
        background-color: #f5f5f4 !important;
        color: #1a1a1a !important;
    }
    .stSelectbox > div > div, .stSelectbox input,
    div[data-testid="stSelectbox"] input,
    [data-baseweb="select"] input {
        background-color: #f5f5f4 !important;
        color: #1a1a1a !important;
    }
    .stSelectbox label, div[data-testid="stSelectbox"] label {
        color: #1a1a1a !important;
    }
    .stRadio > div, div[data-testid="stRadio"] > div {
        background-color: transparent !important;
    }
    .stRadio label, div[data-testid="stRadio"] label {
        color: #1a1a1a !important;
    }
    /* Játékos név megadása és egyéb szövegmezők: fehér háttér */
    .stTextInput > div > div,
    .stTextInput input,
    div[data-testid="stTextInput"] > div > div,
    div[data-testid="stTextInput"] input,
    div[data-baseweb="base-input"],
    div[data-baseweb="base-input"] input {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    .stTextInput input, div[data-testid="stTextInput"] input {
        border: 2px solid #e7e5e4 !important;
    }
    .stTextInput label, div[data-testid="stTextInput"] label {
        color: #1a1a1a !important;
    }
    .topic-column {
        min-height: 400px;
        display: flex;
        flex-direction: column;
    }
    .topic-column > div {
        flex: 1;
    }
    .option-button:hover {
        background: var(--neutral-100);
        border-color: var(--brand-accent);
        box-shadow: var(--shadow-sm);
    }
    .option-button.selected {
        background: #f5f5f4 !important;
        color: #1a1a1a !important;
        border-color: var(--brand-accent);
    }
    .option-button.correct {
        background: var(--color-success);
        color: white;
        border-color: transparent;
    }
    .option-button.incorrect {
        background: var(--color-error);
        color: white;
        border-color: transparent;
    }
    .score-display {
        font-size: 1rem;
        font-weight: 500;
        text-align: center;
        padding: var(--space-2) var(--space-3);
        background: var(--neutral-100);
        border-radius: var(--radius-lg);
        margin: var(--space-2) 0;
        color: var(--color-text);
        border: 1px solid var(--color-border);
    }
    .summary-box {
        background: var(--neutral-100);
        border-radius: var(--radius-lg);
        padding: var(--space-3);
        margin: var(--space-2) 0;
        border-left: 4px solid var(--brand-accent);
        color: var(--color-text);
        box-shadow: var(--shadow-sm);
    }
    .summary-box h3, .summary-box h4 {
        color: var(--brand-primary);
        margin-bottom: var(--space-1);
        font-size: 1rem;
        font-weight: 600;
    }
    .summary-box p {
        color: var(--color-muted);
        margin: var(--space-1) 0;
        font-size: 0.9375rem;
        line-height: 1.6;
    }
    .summary-box strong {
        color: var(--brand-primary);
        font-weight: 600;
    }
    .mode-info {
        background: #f5f5f4;
        color: #1a1a1a;
        border: 1px solid #e7e5e4;
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-lg);
        margin: var(--space-2) 0;
        box-shadow: var(--shadow-sm);
    }
    .timer-warning {
        background: #fef3c7;
        color: var(--neutral-700);
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-md);
        text-align: center;
        font-weight: 600;
    }
    .timer-danger {
        background: var(--color-error);
        color: white;
        padding: var(--space-1) var(--space-2);
        border-radius: var(--radius-md);
        text-align: center;
        font-weight: 600;
    }
    .image-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: var(--space-3) 0;
        padding: var(--space-3);
        background: var(--neutral-100);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--color-border);
    }
    .image-container img {
        max-width: 100%;
        height: auto;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        transition: transform 0.2s ease;
    }
    .image-container img:hover {
        transform: scale(1.01);
    }
    .image-modal {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0,0,0,0.9);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
        cursor: pointer;
        backdrop-filter: blur(8px);
    }
    .modal-buttons {
        position: fixed;
        top: var(--space-3);
        left: 50%;
        transform: translateX(-50%);
        z-index: 1001;
        background: var(--color-card);
        padding: var(--space-2) var(--space-3);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-md);
        border: 1px solid var(--color-border);
    }
    .image-modal img {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
    }
    .image-caption {
        text-align: center;
        font-style: italic;
        color: var(--color-muted);
        margin-top: var(--space-1);
        font-size: 0.875rem;
    }
    div[data-testid="stAlert"] {
        border-radius: var(--radius-lg) !important;
        border: 1px solid var(--neutral-300) !important;
        box-shadow: var(--shadow-sm) !important;
    }
    /* Végleges Kérdésszám Beállítása blokk: olvasható szöveg (címek, info/success, slider címkék, checkbox) */
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h3,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h4,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] h5,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] p,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] label,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stMarkdown"] span,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"],
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"] *,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stSlider"] label,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stCheckbox"] label,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * [data-testid="stCheckbox"] label {
        color: #1a1a1a !important;
    }
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ [data-testid="stHorizontalBlock"] [data-testid="stAlert"] {
        background-color: #f5f5f4 !important;
        border-color: #d6d3d1 !important;
    }
    /* Végleges Kérdésszám Beállítása: gombok olvasható szöveg (világos háttér, sötét betű) */
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stButton"] > button {
        color: #1a1a1a !important;
        background-color: #f5f5f4 !important;
        border: 2px solid #d6d3d1 !important;
    }
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button p,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * .stButton > button span,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stButton"] > button p,
    [data-testid="stMarkdown"]:has(#final-question-settings) ~ * div[data-testid="stButton"] > button span {
        color: #1a1a1a !important;
    }
    /* Kérdésszám csúszkák: piros gomb (thumb) */
    div[data-testid="stSlider"] [role="slider"] {
        background-color: #dc2626 !important;
        border: 2px solid #991b1b !important;
    }
    /* Thumb felirat (érték buborék) */
    div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
        background-color: #dc2626 !important;
        color: #ffffff !important;
        border-color: #dc2626 !important;
    }
    div[data-testid="stSlider"] [data-testid="stSliderThumbValue"] * {
        color: #ffffff !important;
    }
    /* Címsor hierarchia */
    h1, h2, h3, h4 {
        font-family: 'Inter', sans-serif !important;
        color: var(--brand-primary) !important;
        font-weight: 600 !important;
        letter-spacing: -0.02em !important;
    }
    h1 { font-size: 1.75rem !important; line-height: 1.3 !important; }
    h2 { font-size: 1.375rem !important; line-height: 1.4 !important; }
    h3 { font-size: 1.125rem !important; line-height: 1.5 !important; }
    __THEME_OVERRIDES__
</style>
"""


def apply_styles(theme: str) -> None:
    """Apply full CSS with theme overrides via st.markdown."""
    theme_css = get_theme_css(theme)
    full_css = _BASE_CSS_TEMPLATE.replace("__THEME_OVERRIDES__", theme_css)
    st.markdown(full_css, unsafe_allow_html=True)
