"""Az oldalak: témaválasztó → kvíz → eredmény."""

from __future__ import annotations

import random

import streamlit as st
import streamlit.components.v1 as components

from . import theme
from .catalog import GROUPS, TOPIC_BY_KEY, TOPICS, load_bank
from .answers import Verdict
from .engine import Feedback, Input, Mode, Session, build_session
from .visuals import cluster, esc, mark, pct, pearl_string, verdict

LETTERS = "12345678"


def _num(n: int) -> str:
    return f"{n:,}".replace(",", "\u202f")
S = st.session_state


@st.cache_resource(show_spinner="Kérdések betöltése…")
def _bank():
    return load_bank()


@st.cache_data(show_spinner=False, max_entries=500)
def _thumb(path: str, size: int = 160) -> str:
    """Kicsinyített kép data-URI-ként az áttekintő listához."""
    import base64
    import io

    from PIL import Image

    with Image.open(path) as im:
        im = im.convert("RGBA") if im.mode in ("P", "LA") else im
        im.thumbnail((size, size))
        buf = io.BytesIO()
        fmt = "PNG" if im.mode == "RGBA" else "JPEG"
        im.save(buf, fmt, quality=82)
    return f"data:image/{fmt.lower()};base64," + base64.b64encode(buf.getvalue()).decode()


def _go(view: str) -> None:
    S.view = view


def _start(topics: list[str], count: int, mode: Mode, inp: Input = Input.CHOICE,
           fb: Feedback = Feedback.NOW, only=None) -> None:
    S.session = build_session(_bank(), topics, count, mode, only=only, input=inp, feedback=fb)
    S.last = {"topics": topics, "count": count, "mode": mode, "input": inp, "feedback": fb}
    _go("quiz")


# ---------------------------------------------------------------------------
# Témaválasztó
# ---------------------------------------------------------------------------

def home() -> None:
    bank = _bank()
    total_q = sum(len(v) for v in bank.values())

    st.markdown(
        f'<div class="cg-mark">{mark(40)}<h1 class="cg-title">Csabagyöngye</h1></div>'
        f'<p class="cg-lede">Tematikus gyakorló kvíz: {len(bank)} témakör, '
        f'{_num(total_q)} kérdés. Válassz egyet vagy többet, és kezdd el.</p>',
        unsafe_allow_html=True,
    )

    # Kijelölés: témánként egy pill-csoport; a teljes kijelölés a csoportok uniója.
    prev = set(S.get("picked", []))
    picked: list[str] = []
    for g in GROUPS:
        keys = [t.key for t in TOPICS if t.group == g and t.key in bank]
        if not keys:
            continue
        st.markdown(f'<div class="cg-group">{g}</div>', unsafe_allow_html=True)
        sel = st.pills(
            g, keys, selection_mode="multi", default=[k for k in keys if k in prev],
            format_func=lambda k: f"{TOPIC_BY_KEY[k].name}  {len(bank[k])}",
            key=f"pills_{g}_{S.get('pick_rev', 0)}", label_visibility="collapsed",
        )
        picked.extend(sel or [])
    S.picked = picked

    c1, c2, _ = st.columns([1.3, 1, 3])
    if c1.button("Véletlen 4 téma", type="tertiary"):
        S.picked = random.sample(list(bank), 4)
        S.pick_rev = S.get("pick_rev", 0) + 1
        st.rerun()
    if picked and c2.button("Kijelölés törlése", type="tertiary"):
        S.picked = []
        S.pick_rev = S.get("pick_rev", 0) + 1
        st.rerun()

    st.markdown('<div class="cg-section">Hogyan játszol?</div>', unsafe_allow_html=True)
    mode = st.segmented_control(
        "Mód", list(Mode), default=S.get("mode", Mode.SERIES), format_func=lambda m: m.label,
        key="mode_ctl", label_visibility="collapsed",
    ) or Mode.SERIES
    S.mode = mode
    st.markdown(f'<p class="cg-hint">{mode.hint}</p>', unsafe_allow_html=True)

    available = sum(len(bank[k]) for k in picked)
    count = S.get("count", 10)
    if mode is Mode.SERIES:
        st.markdown('<div class="cg-group">Kérdések száma</div>', unsafe_allow_html=True)
        if available:
            c_num, c_all = st.columns([1, 2], vertical_alignment="center")
            every = c_all.checkbox(f"Az összes kérdés ({_num(available)})", value=S.get("all", False), key="all_ctl")
            S.all = every
            if every:
                count = available
                c_num.number_input("Kérdések száma", value=available, disabled=True, label_visibility="collapsed")
            else:
                count = int(c_num.number_input(
                    "Kérdések száma", min_value=1, max_value=available, value=max(1, min(count, available)),
                    step=1, label_visibility="collapsed",
                ))
                S.count = count
        else:
            st.markdown('<p class="cg-hint">Előbb válassz témát – utána beállíthatod, hány kérdést kérsz, akár az összeset.</p>',
                        unsafe_allow_html=True)

    st.markdown('<div class="cg-group">Válaszadás</div>', unsafe_allow_html=True)
    inp = st.segmented_control(
        "Válaszadás", list(Input), default=S.get("inp", Input.CHOICE), format_func=lambda m: m.label,
        key="inp_ctl", label_visibility="collapsed",
    ) or Input.CHOICE
    S.inp = inp
    st.markdown(f'<p class="cg-hint">{inp.hint}</p>', unsafe_allow_html=True)

    st.markdown('<div class="cg-group">Mikor derüljön ki, hogy jó-e a válasz?</div>', unsafe_allow_html=True)
    fbs = list(Feedback)
    fb = st.radio(
        "Visszajelzés", fbs, index=fbs.index(S.get("fb", Feedback.NOW)), format_func=lambda f: f.label,
        horizontal=True, key="fb_ctl", label_visibility="collapsed",
    )
    S.fb = fb
    hint = ("Minden válasz után látod a helyes választ és a magyarázatot." if fb is Feedback.NOW
            else "Menet közben nincs visszajelzés; a végén mindent átnézhetsz.")
    st.markdown(f'<p class="cg-hint">{hint}</p>', unsafe_allow_html=True)

    real = min(count, available)
    st.write("")
    if not picked:
        label = "Válassz legalább egy témát"
    elif mode is Mode.SUDDEN:
        label = "Indítás – az első hibáig"
    else:
        label = f"Indítás – {_num(real)} kérdés"
    if st.button(label, type="primary", disabled=not picked, width="stretch"):
        _start(picked, real if mode is Mode.SERIES else 10, mode, inp, fb)
        st.rerun()


# ---------------------------------------------------------------------------
# Kvíz
# ---------------------------------------------------------------------------

def _states(s: Session) -> list[str]:
    out = []
    for i, it in enumerate(s.items):
        if i == s.cursor and not it.answered:
            out.append("now")
        elif not it.answered:
            out.append("")
        elif not s.instant:
            out.append("done")
        else:
            out.append("ok" if it.is_correct else "bad")
    return out


def _two_col(opts: list[str]) -> bool:
    return len(opts) == 4 and all(len(o) < 34 for o in opts)


def _typed_input(s: Session) -> None:
    """Beviteli mező; Enterrel is beküldhető."""
    with st.form(key=f"type_{s.cursor}", border=False, enter_to_submit=True):
        text = st.text_input("Válaszod", key=f"t_{s.cursor}", placeholder="Írd be a választ…",
                             label_visibility="collapsed", autocomplete="off")
        sent = st.form_submit_button("Ellenőrzés", type="primary", width="stretch")
    if sent:
        if text.strip():
            s.answer_text(text)
            if not s.instant:
                s.advance()
            st.rerun()
        else:
            st.markdown('<p class="cg-hint">Írj be valamit, vagy kérd a lehetőségeket.</p>', unsafe_allow_html=True)
    # a beviteli mező kapjon fókuszt, hogy rögtön lehessen gépelni
    components.html(
        f"<script>/* {s.cursor} */const d=window.parent.document;"
        "setTimeout(()=>{const i=d.querySelector('[data-testid=\"stTextInput\"] input');if(i)i.focus();},150);</script>",
        height=0,
    )
    if st.button("Nem tudom – mutasd a lehetőségeket", type="tertiary", key=f"hint_{s.cursor}"):
        s.current.hinted = True
        st.rerun()


def quiz() -> None:
    s: Session = S.session
    if s.finished:
        _go("result")
        st.rerun()
    it = s.current
    q = it.question

    bar = st.container(key="topbar")
    left, right = bar.columns([1, 1], vertical_alignment="center")
    if left.button("‹ Kilépés", type="tertiary", key="quit"):
        _go("result" if s.answered_items else "home")
        st.rerun()
    if s.mode is Mode.SUDDEN and not s.instant:
        status = f"<b>{s.cursor + 1}</b>.&nbsp;kérdés"
    elif not s.instant:
        status = f"<b>{s.cursor + 1}</b>&nbsp;/ {s.total}"
    elif s.mode is Mode.SUDDEN:
        status = f"sorozat:&nbsp;<b>{s.score}</b>"
    else:
        status = f"<b>{s.score}</b>&nbsp;helyes / {len(s.answered_items)}"
    right.markdown(f'<div class="cg-topbar" style="justify-content:flex-end">{status}</div>', unsafe_allow_html=True)

    if s.mode is not Mode.SUDDEN:
        if s.total <= 60:
            st.markdown(pearl_string(_states(s)), unsafe_allow_html=True)
        else:
            st.progress(s.cursor / s.total)
    elif s.instant:
        st.markdown(pearl_string(["ok"] * min(s.score, 60) + ["now"]), unsafe_allow_html=True)
    else:
        st.markdown(pearl_string(["done"] * min(s.cursor, 60) + ["now"]), unsafe_allow_html=True)

    st.markdown(
        f'<div class="cg-topic">{esc(TOPIC_BY_KEY[q.topic].name)}</div>'
        f'<h2 class="cg-q{" long" if len(q.text) > 120 else ""}">{esc(q.text)}</h2>',
        unsafe_allow_html=True,
    )
    if q.audio:
        st.audio(q.audio, autoplay=not it.answered)
    if q.image:
        st.image(q.image)

    if not it.answered and s.typing_now():
        _typed_input(s)
        return

    if not it.answered:
        if s.input is Input.TYPE and not it.hinted:
            st.markdown('<p class="cg-hint cg-mc-note">Ennél a kérdésnél a lehetőségek közül válassz.</p>', unsafe_allow_html=True)
        opts = it.options
        # Soronként rakjuk ki, így keskeny kijelzőn is 1-2-3-4 a sorrend.
        per_row = 2 if _two_col(opts) else 1
        box = st.container(key="answers")
        slots = []
        for r in range(0, len(opts), per_row):
            slots.extend(box.columns(per_row, gap="small") if per_row > 1 else [box.container()])
        for i, o in enumerate(opts):
            with slots[i]:
                with st.container(key=f"ans_{i}"):
                    if st.button(o, key=f"a_{s.cursor}_{i}", width="stretch", shortcut=LETTERS[i] if i < 9 else None):
                        s.answer(i)
                        if not s.instant:
                            s.advance()
                        st.rerun()
        return

    # --- visszajelzés (gyakorlás / hirtelen halál) ---
    good = it.is_correct
    right = esc(it.question.correct_text)
    if it.typed is not None:
        cls = "ok" if good else "bad"
        st.markdown(f'<div class="cg-opt cg-typed {cls}"><span class="lbl">Te</span>{esc(it.typed)}</div>', unsafe_allow_html=True)
        if it.verdict is Verdict.EXACT:
            word = "Helyes."
        elif it.verdict is Verdict.CLOSE:
            word = f"Elfogadva. A pontos alak: {right}."
        else:
            word = f"Nem, a helyes válasz: {right}."
    else:
        rows = []
        for i, o in enumerate(it.options):
            cls = "ok" if i == it.correct_pos else "bad" if i == it.picked else "dim"
            rows.append(f'<div class="cg-opt {cls}"><span class="k">{LETTERS[i]}</span>{esc(o)}</div>')
        two = " two" if _two_col(it.options) else ""
        st.markdown(f'<div class="cg-opts{two}">{"".join(rows)}</div>', unsafe_allow_html=True)
        word = "Helyes." if good else f"Nem, a helyes válasz: {right}."
    st.markdown(f'<div class="cg-verdict {"ok" if good else "bad"}">{word}</div>', unsafe_allow_html=True)
    if q.explanation:
        st.markdown(f'<div class="cg-expl {"" if good else "bad"}">{esc(q.explanation)}</div>', unsafe_allow_html=True)

    last = s.cursor == s.total - 1 or (s.mode is Mode.SUDDEN and not good)
    if st.button("Eredmény" if last else "Következő kérdés", type="primary", width="stretch", key=f"next_{s.cursor}", shortcut="Enter"):
        s.advance()
        st.rerun()


# ---------------------------------------------------------------------------
# Eredmény
# ---------------------------------------------------------------------------

def _cluster_marks(answered) -> list[bool]:
    """Sok kérdésnél a fürt arányosan kicsinyítve (legfeljebb 120 szem)."""
    marks = [it.is_correct for it in answered]
    if len(marks) <= 120:
        return marks
    ok = round(120 * sum(marks) / len(marks))
    return [True] * ok + [False] * (120 - ok)


REVIEW_LIMIT = 100


def result() -> None:
    s: Session = S.session
    answered = s.answered_items
    n, good = len(answered), s.score
    p = pct(good, n)
    head, sub = verdict(p)

    if s.mode is Mode.SUDDEN:
        big = f'{good}<small> helyes egymás után</small>'
        head = "Hosszú fürt." if good >= 10 else "Szép kezdet." if good >= 3 else "Az első szemek lehullottak."
        sub = "A menet az első hibáig tartott." if s.mistakes() else "Elfogytak a kérdések – hibátlan!"
    else:
        big = f'{good}<small> / {n}</small>'

    if s.input is Input.TYPE:
        typed = [it for it in answered if it.typed is not None]
        hinted = sum(1 for it in answered if it.hinted)
        extra = f"{len(typed)} választ írtál be"
        if hinted:
            extra += f", {hinted} kérdésnél a lehetőségek közül választottál"
        sub = f"{sub} {extra}."

    st.markdown(
        f'<div class="cg-result"><div>{cluster(_cluster_marks(answered), 220)}</div>'
        f'<div><div class="cg-score">{big}</div><div class="cg-word">{head}</div>'
        f'<p class="cg-hint">{sub}</p></div></div>',
        unsafe_allow_html=True,
    )

    misses = s.mistakes()
    c1, c2 = st.columns(2)
    last = S.get("last", {})
    if c1.button("Új menet ugyanezekkel", type="primary", width="stretch"):
        _start(last["topics"], last["count"], last["mode"], last.get("input", Input.CHOICE),
               last.get("feedback", Feedback.NOW))
        st.rerun()
    if misses and c2.button(f"Hibák újragyakorlása ({len(misses)})", width="stretch"):
        S.session = build_session(_bank(), [], 0, Mode.SERIES, only=misses, input=s.input, feedback=Feedback.NOW)
        _go("quiz")
        st.rerun()
    if st.button("‹ Vissza a témákhoz", type="tertiary"):
        _go("home")
        st.rerun()

    topics = s.by_topic()
    if len(topics) > 1:
        st.markdown('<div class="cg-section">Témánként</div>', unsafe_allow_html=True)
        rows = "".join(
            f'<div class="cg-row"><span>{esc(TOPIC_BY_KEY[t].name)}</span>'
            f'<div class="cg-bar"><i style="width:{pct(a, b)}%"></i></div><span>{a}/{b}</span></div>'
            for t, (a, b) in sorted(topics.items(), key=lambda kv: -pct(*kv[1]))
        )
        st.markdown(rows, unsafe_allow_html=True)

    if misses:
        st.markdown('<div class="cg-section">Ezeket érdemes átnézni</div>', unsafe_allow_html=True)
        out = []
        wrong = [it for it in answered if not it.is_correct]
        if len(wrong) > REVIEW_LIMIT:
            st.markdown(f'<p class="cg-hint">Az első {REVIEW_LIMIT} hibás válasz látszik a {_num(len(wrong))}-ból; '
                        'a „Hibák újragyakorlása” mindet tartalmazza.</p>', unsafe_allow_html=True)
        for it in wrong[:REVIEW_LIMIT]:
            q = it.question
            ex = f'<p class="ex">{esc(q.explanation)}</p>' if q.explanation else ""
            thumb = f'<img src="{_thumb(q.image)}" alt="">' if q.image else ""
            out.append(
                f'<div class="cg-miss">{thumb}<div><p class="q">{esc(q.text)}</p>'
                f'<p class="you">Te: {esc(it.your_answer) or "–"}</p>'
                f'<p class="right">Helyes: {esc(q.correct_text)}</p>{ex}</div></div>'
            )
        st.markdown("".join(out), unsafe_allow_html=True)


# ---------------------------------------------------------------------------

def main() -> None:
    theme.apply()
    S.setdefault("view", "home")
    view = S.view
    if view in ("quiz", "result") and "session" not in S:
        view = "home"
    {"home": home, "quiz": quiz, "result": result}[view]()
