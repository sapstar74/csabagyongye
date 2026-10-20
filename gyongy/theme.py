"""Megjelenés.

Az alapötlet a névadó szőlőfajta: halvány, sárgászöld bogyók („gyöngyök”)
a venyige mély zöldjén. A haladást is gyöngysor mutatja, az eredményt
pedig egy fürt, amelynek minden szeme egy kérdés.
"""

import streamlit as st

PALETTE = {
    "ink": "#1E3328",      # venyige – szöveg, elsődleges gomb
    "paper": "#F4F6EF",    # háttér
    "surface": "#FFFFFF",
    "pearl": "#D7E39A",    # érett bogyó – helyes válasz
    "pearl_deep": "#9DB23A",
    "wrong": "#B23A31",
    "wrong_soft": "#F3DCD8",
    "line": "#D3DAC8",
    "muted": "#5E6B60",
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=Atkinson+Hyperlegible+Next:wght@400;600&display=swap');

:root {
  --ink: %(ink)s; --paper: %(paper)s; --surface: %(surface)s;
  --pearl: %(pearl)s; --pearl-deep: %(pearl_deep)s;
  --wrong: %(wrong)s; --wrong-soft: %(wrong_soft)s;
  --line: %(line)s; --muted: %(muted)s;
  --display: 'Bricolage Grotesque', system-ui, sans-serif;
  --body: 'Atkinson Hyperlegible Next', 'Atkinson Hyperlegible', system-ui, sans-serif;
}

/* ---- keret -------------------------------------------------------- */
.stApp { background: var(--paper); color: var(--ink); }
.stApp, .stApp p, .stApp label, .stApp li, .stApp button { font-family: var(--body); }
header[data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"],
[data-testid="stToolbar"], footer { display: none !important; }
.block-container { max-width: 780px; padding: 2.5rem 1rem 4rem; }
.stApp h1, .stApp h2, .stApp h3 { font-family: var(--display); color: var(--ink); letter-spacing: -0.01em; }

/* ---- fejléc ------------------------------------------------------- */
.cg-mark { display: flex; align-items: center; gap: .9rem; margin-bottom: .4rem; }
.cg-mark svg { flex: none; }
.cg-title { font-family: var(--display); font-weight: 800; font-size: clamp(2.4rem, 7vw, 3.6rem);
  line-height: 1; margin: 0; letter-spacing: -0.03em; color: var(--ink); }
.cg-lede { font-size: 1.1rem; color: var(--muted); margin: .6rem 0 2rem; max-width: 34em; }

.cg-group { font-family: var(--display); font-weight: 700; font-size: 1.05rem; margin: 1.4rem 0 .35rem; }
.cg-section { font-family: var(--display); font-weight: 700; font-size: 1.35rem; margin: 2.2rem 0 .6rem;
  padding-top: 1.4rem; border-top: 1px solid var(--line); }
.cg-hint { color: var(--muted); font-size: .95rem; margin: .2rem 0 0; }

/* ---- pills / segmented ------------------------------------------- */
[data-testid="stPills"] button, [data-testid="stButtonGroup"] button {
  border-radius: 999px !important; border: 1px solid var(--line) !important;
  background: var(--surface) !important; color: var(--ink) !important; font-size: .95rem !important; }
[data-testid="stPills"] button[aria-pressed="true"], [data-testid="stButtonGroup"] button[aria-pressed="true"],
[data-testid="stButtonGroup"] button[aria-checked="true"] {
  background: var(--ink) !important; color: var(--paper) !important; border-color: var(--ink) !important; }
[data-testid="stPills"] button[aria-pressed="true"] *, [data-testid="stButtonGroup"] button[aria-pressed="true"] *,
[data-testid="stButtonGroup"] button[aria-checked="true"] * { color: var(--paper) !important; }

/* ---- gombok ------------------------------------------------------- */
.stButton > button { border-radius: 12px; font-weight: 600; border: 1px solid var(--line);
  background: var(--surface); color: var(--ink); min-height: 2.75rem; }
.stButton > button:hover { border-color: var(--ink); color: var(--ink); }
.stButton > button:focus-visible { outline: 3px solid var(--pearl-deep); outline-offset: 2px; }
.stButton > button[kind="primary"] { background: var(--ink); color: var(--paper); border-color: var(--ink);
  min-height: 3.2rem; font-size: 1.05rem; }
.stButton > button[kind="primary"]:hover { background: #2C4A3A; color: var(--paper); }
.stButton > button[kind="primary"]:disabled { background: var(--line); border-color: var(--line); color: var(--muted); }
.stButton > button[kind="tertiary"] { border: none; background: none; color: var(--muted); padding: 0; min-height: 0; }
.stButton > button[kind="tertiary"]:hover { color: var(--ink); text-decoration: underline; }

/* válaszgombok – a billentyűparancs (1–4) bal oldali jelvényként jelenik meg */
[class*="st-key-ans_"] .stButton > button { width: 100%%; min-height: 4.2rem; padding: .7rem 1rem;
  font-size: 1.05rem; font-weight: 600; border-width: 1.5px; justify-content: flex-start; }
[class*="st-key-ans_"] .stButton > button > div, [class*="st-key-ans_"] .stButton > button span[data-has-shortcut] {
  justify-content: flex-start; width: 100%%; gap: .8rem; }
[class*="st-key-ans_"] .stButton > button p { text-align: left; font-weight: 600; }
[class*="st-key-ans_"] .stButton > button kbd { order: -1; flex: none; width: 1.7rem; height: 1.7rem; border-radius: 50%%;
  display: grid; place-items: center; font-family: var(--display); font-size: .9rem; color: var(--ink);
  border: 1.5px solid var(--line); background: none; margin: 0; padding: 0; opacity: 1; }
[class*="st-key-ans_"] .stButton > button:hover { background: #FBFCF6; }
[class*="st-key-ans_"] .stButton > button:hover kbd { border-color: var(--ink); }

/* ---- kvíz --------------------------------------------------------- */
.st-key-topbar [data-testid="stHorizontalBlock"] { flex-wrap: nowrap; }
.st-key-topbar [data-testid="stColumn"] { min-width: 0; width: auto; flex: 1 1 0; }
.cg-topbar { display: flex; justify-content: space-between; align-items: baseline; color: var(--muted);
  font-size: .95rem; }
.cg-topbar b { color: var(--ink); font-family: var(--display); font-size: 1.15rem; }
.cg-string { display: flex; flex-wrap: wrap; gap: 6px; margin: .6rem 0 1.8rem; }
.cg-p { width: 14px; height: 14px; border-radius: 50%%; border: 1.5px solid var(--line); background: transparent; }
.cg-p.ok { background: radial-gradient(circle at 35%% 30%%, #FBFDE9 0 18%%, var(--pearl) 45%%, var(--pearl-deep) 100%%);
  border-color: var(--pearl-deep); }
.cg-p.bad { background: var(--wrong); border-color: var(--wrong); }
.cg-p.done { background: var(--muted); border-color: var(--muted); }
.cg-p.now { border-color: var(--ink); box-shadow: 0 0 0 3px rgba(30,51,40,.15); }
.cg-topic { font-size: .95rem; color: var(--muted); margin-bottom: .2rem; }
.cg-q { font-family: var(--display); font-weight: 700; font-size: clamp(1.4rem, 4.4vw, 2.05rem);
  line-height: 1.18; margin: 0 0 1.2rem; letter-spacing: -0.015em; }
.cg-q.long { font-size: clamp(1.15rem, 3.2vw, 1.5rem); line-height: 1.3; letter-spacing: 0; }
.cg-caption { color: var(--muted); margin: -.6rem 0 1rem; }

[data-testid="stImage"] img { max-height: 380px; width: auto !important; object-fit: contain;
  border-radius: 10px; background: var(--surface); padding: 8px; border: 1px solid var(--line); }
[data-testid="stAudio"] { margin-bottom: 1rem; }

/* haladásjelző sok kérdésnél */
[data-testid="stProgress"] [role="progressbar"] > div > div { background-color: var(--line) !important; }
[data-testid="stProgress"] [role="progressbar"] > div > div > div { background-color: var(--pearl-deep) !important; }

/* számbevitel */
[data-testid="stNumberInput"] [data-baseweb="input"] { border-radius: 12px !important; border: 1.5px solid var(--line) !important;
  background: var(--surface) !important; }
[data-testid="stNumberInput"] [data-baseweb="input"] > div, [data-testid="stNumberInput"] input,
[data-testid="stNumberInput"] button { background: var(--surface) !important; }
[data-testid="stNumberInput"] input { font-family: var(--display); font-weight: 700; font-size: 1.1rem; color: var(--ink); }
[data-testid="stNumberInput"] [data-baseweb="input"]:focus-within { border-color: var(--ink) !important; }
[data-testid="stNumberInput"] [data-testid="InputInstructions"] { display: none; }

/* rádiógombok */
[data-testid="stRadio"] label p { font-size: 1rem; }
[data-testid="stRadio"] [role="radiogroup"] { gap: .4rem 1.4rem; }

/* szabad szöveges válasz */
[data-testid="stForm"] { padding: 0; }
[data-testid="stTextInput"] input { font-family: var(--body); font-size: 1.15rem; font-weight: 600; color: var(--ink);
  min-height: 3.4rem; padding: .6rem 1rem; }
[data-testid="stTextInput"] [data-baseweb="input"] { border-radius: 12px !important; border: 1.5px solid var(--line) !important;
  background: var(--surface) !important; }
[data-testid="stTextInput"] [data-baseweb="input"] > div, [data-testid="stTextInput"] input { background: var(--surface) !important; }
[data-testid="stTextInput"] [data-baseweb="input"]:focus-within { border-color: var(--ink) !important;
  box-shadow: 0 0 0 3px rgba(30,51,40,.12); }
[data-testid="stTextInput"] [data-testid="InputInstructions"] { display: none; }
.stFormSubmitButton > button { border-radius: 12px; font-weight: 600; min-height: 3.2rem; font-size: 1.05rem; }
.stFormSubmitButton > button[kind="primaryFormSubmit"], .stFormSubmitButton > button[kind="primary"] {
  background: var(--ink); color: var(--paper); border: 1px solid var(--ink); }
.stFormSubmitButton > button:hover { background: #2C4A3A; color: var(--paper); }
.cg-typed .lbl { flex: none; font-family: var(--display); font-size: .85rem; color: var(--muted);
  border: 1.5px solid var(--line); border-radius: 99px; padding: .1rem .6rem; }
.cg-typed.ok .lbl { background: var(--pearl-deep); border-color: var(--pearl-deep); color: #fff; }
.cg-typed.bad .lbl { background: var(--wrong); border-color: var(--wrong); color: #fff; }
.cg-mc-note { margin: -.4rem 0 .8rem; }

/* visszajelzés utáni, már nem kattintható válaszok */
.cg-opts { display: grid; gap: .75rem; margin-bottom: .2rem; }
.st-key-answers, .st-key-answers [data-testid="stHorizontalBlock"] { gap: .75rem !important; }
.cg-opts.two { grid-template-columns: 1fr 1fr; }
.cg-opt { display: flex; gap: .8rem; align-items: center; border: 1.5px solid var(--line); border-radius: 12px;
  padding: .7rem 1rem; background: var(--surface); font-weight: 600; min-height: 4.2rem; font-size: 1.05rem; }
.cg-opt .k { flex: none; width: 1.7rem; height: 1.7rem; border-radius: 50%%; display: grid; place-items: center;
  font-family: var(--display); font-size: .9rem; border: 1.5px solid var(--line); }
.cg-opt.ok { border-color: var(--pearl-deep); background: #F1F6DA; }
.cg-opt.ok .k { background: var(--pearl-deep); border-color: var(--pearl-deep); color: #fff; }
.cg-opt.bad { border-color: var(--wrong); background: var(--wrong-soft); }
.cg-opt.bad .k { background: var(--wrong); border-color: var(--wrong); color: #fff; }
.cg-opt.dim { opacity: .55; }
.cg-verdict { font-family: var(--display); font-weight: 800; font-size: 1.3rem; margin: 1rem 0 .3rem; }
.cg-verdict.ok { color: #56691A; } .cg-verdict.bad { color: var(--wrong); }
.cg-expl { color: var(--ink); background: var(--surface); border-left: 3px solid var(--pearl-deep);
  padding: .7rem 1rem; border-radius: 0 10px 10px 0; margin-bottom: 1.2rem; }
.cg-expl.bad { border-left-color: var(--wrong); }

/* ---- eredmény ----------------------------------------------------- */
.cg-result { display: grid; grid-template-columns: auto 1fr; gap: 2rem; align-items: center; margin: 1rem 0 1.5rem; }
.cg-score { font-family: var(--display); font-weight: 800; font-size: clamp(3.4rem, 12vw, 5.2rem); line-height: .9;
  letter-spacing: -0.04em; }
.cg-score small { font-size: .38em; color: var(--muted); font-weight: 700; letter-spacing: 0; }
.cg-word { font-family: var(--display); font-weight: 700; font-size: 1.5rem; margin: .4rem 0 .2rem; }
.cg-row { display: grid; grid-template-columns: minmax(8rem, 14rem) 1fr 3.5rem; gap: .8rem; align-items: center;
  padding: .45rem 0; border-bottom: 1px solid var(--line); font-size: .98rem; }
.cg-bar { height: 8px; border-radius: 99px; background: var(--line); overflow: hidden; }
.cg-bar i { display: block; height: 100%%; background: var(--pearl-deep); }
.cg-row span:last-child { text-align: right; font-variant-numeric: tabular-nums; color: var(--muted); }
.cg-miss { padding: .9rem 0; border-bottom: 1px solid var(--line); display: flex; gap: 1rem; align-items: flex-start; }
.cg-miss img { flex: none; width: 80px; height: 80px; object-fit: contain; background: var(--surface);
  border: 1px solid var(--line); border-radius: 8px; padding: 4px; }
.cg-miss p { margin: .15rem 0; }
.cg-miss .q { font-weight: 600; }
.cg-miss .you { color: var(--wrong); } .cg-miss .right { color: #56691A; }
.cg-miss .ex { color: var(--muted); font-size: .95rem; }

@media (max-width: 640px) {
  .block-container { padding-top: 1.2rem; }
  [class*="st-key-ans_"] .stButton > button, .cg-opt { min-height: 3.4rem; }
}
@media (max-width: 560px) {
  .cg-result { grid-template-columns: 1fr; gap: 1rem; }
  .cg-row { grid-template-columns: 1fr 4rem 3rem; }
  .cg-opts.two { grid-template-columns: 1fr; }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } }
""" % PALETTE


def apply() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)
