"""SVG- és HTML-elemek: gyöngysor (haladás) és fürt (eredmény)."""

from __future__ import annotations

import html

from .theme import PALETTE as P


def pearl_string(states: list[str]) -> str:
    """states elemei: 'ok', 'bad', 'done', 'now', '' (még hátravan)."""
    labels = {"ok": "helyes", "bad": "hibás", "done": "megválaszolva", "now": "aktuális", "": "hátravan"}
    dots = "".join(f'<span class="cg-p {s}" title="{i + 1}. kérdés: {labels[s]}"></span>' for i, s in enumerate(states))
    return f'<div class="cg-string" role="img" aria-label="Haladás">{dots}</div>'


def _defs(uid: str) -> str:
    return f"""<defs>
  <radialGradient id="ok{uid}" cx="35%" cy="30%" r="75%">
    <stop offset="0" stop-color="#FBFDE9"/><stop offset=".35" stop-color="{P['pearl']}"/>
    <stop offset="1" stop-color="{P['pearl_deep']}"/></radialGradient>
  <radialGradient id="bad{uid}" cx="35%" cy="30%" r="75%">
    <stop offset="0" stop-color="#E9928A"/><stop offset=".4" stop-color="{P['wrong']}"/>
    <stop offset="1" stop-color="#7E2620"/></radialGradient>
</defs>"""


def cluster(results: list[bool], width: int = 220, uid: str = "r") -> str:
    """Szőlőfürt: soronként fogyó bogyók, felül szárral és levéllel."""
    n = max(len(results), 1)
    w = 1
    while w * (w + 1) // 2 < n:
        w += 1
    rows, left = [], n
    for k in range(w, 0, -1):
        take = min(k, left)
        if take:
            rows.append(take)
        left -= take
    r = min(15.0, (width - 20) / (2 * w + 0.4 * (w - 1)) )
    dx, dy = 2 * r * 1.06, 2 * r * 0.9
    top = 46
    h = top + len(rows) * dy + r + 6
    cx0 = width / 2
    circles, i = [], 0
    for row_i, cnt in enumerate(rows):
        y = top + row_i * dy + r
        x_start = cx0 - (cnt - 1) * dx / 2
        for j in range(cnt):
            ok = results[i] if i < len(results) else None
            fill = f"url(#ok{uid})" if ok else f"url(#bad{uid})" if ok is False else "none"
            stroke = P["pearl_deep"] if ok else P["wrong"] if ok is False else P["line"]
            circles.append(f'<circle cx="{x_start + j * dx:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
            i += 1
    # szár és levél
    stem = (f'<path d="M{cx0:.1f} {top - 4} C {cx0 - 2:.1f} 26, {cx0 + 6:.1f} 16, {cx0 + 2:.1f} 4" '
            f'fill="none" stroke="{P["ink"]}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M{cx0 + 3:.1f} 18 C {cx0 + 24:.1f} 2, {cx0 + 50:.1f} 8, {cx0 + 58:.1f} 22 '
            f'C {cx0 + 40:.1f} 34, {cx0 + 18:.1f} 32, {cx0 + 3:.1f} 18 Z" fill="{P["ink"]}" opacity=".9"/>')
    good = sum(1 for x in results if x)
    return (f'<svg width="{width}" height="{h:.0f}" viewBox="0 0 {width} {h:.0f}" role="img" '
            f'aria-label="{good} helyes, {len(results) - good} hibás válasz">{_defs(uid)}{stem}{"".join(circles)}</svg>')


def mark(size: int = 44) -> str:
    """Kis logó: hat szemből álló fürt."""
    return cluster([True] * 6, width=size + 16, uid="m").replace('stroke-width="3"', 'stroke-width="2.5"')


def esc(s: str) -> str:
    return html.escape(s or "")


def pct(a: int, b: int) -> int:
    return 0 if b == 0 else round(100 * a / b)


def verdict(p: int) -> tuple[str, str]:
    if p >= 90:
        return "Tiszta gyöngy.", "Szinte hibátlan menet."
    if p >= 70:
        return "Szép termés.", "Néhány szem még savanyú – nézd meg lent, melyek."
    if p >= 40:
        return "Érik még.", "A hibás válaszokat egy kattintással újragyakorolhatod."
    return "Ez most savanyú volt.", "Próbáld újra Gyakorlás módban, ott magyarázatot is kapsz."


__all__ = ["pearl_string", "cluster", "mark", "esc", "pct", "verdict"]
