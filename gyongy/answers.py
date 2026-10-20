"""Szabad szöveges válaszok ellenőrzése.

Elvek:
- a kis- és nagybetű, az írásjelek, a névelő (a, az, the …) nem számít;
- ékezethiba vagy apró elgépelés elfogadható, de jelezzük a pontos alakot;
- a sorszám nem lehet hibás: „IV. László” ≠ „V. László”, „4. László” = „IV. László”;
- személynévnél elég a vezetéknév („Beethoven”), zárójeles alternatíva is jó;
- ha a beírt szöveg egy másik, hibás opcióval egyezik, az hibás – akkor is,
  ha hasonlít a helyesre.
"""

from __future__ import annotations

import re
import unicodedata
from difflib import SequenceMatcher
from enum import Enum
from typing import Iterable

from .catalog import Question

ARTICLES = {"a", "az", "the", "le", "la", "les", "der", "die", "das", "el", "il"}
PARTICLES = {"van", "von", "de", "da", "di", "du", "der", "del", "la", "le", "y", "of"}
# Gyakori magyar utónevek: ha egy név ezzel végződik, magyar sorrendű (vezetéknév elöl).
HU_GIVEN = set("""
ádám ákos albert alajos aladár andor andrás antal árpád artúr attila balázs bálint béla bence benedek bertalan
csaba dániel dávid dénes dezső domokos ede elek endre erik ernő ervin ferenc frigyes gábor gellért géza gyula győző
gusztáv györgy henrik ignác imre istván jakab jános jenő józsef kálmán károly kristóf lajos lászló levente lőrinc
marcell márk márton mátyás mihály miklós mór nándor norbert ödön oszkár pál péter rezső richárd róbert sámuel
sándor szabolcs tamás tibor tivadar vilmos viktor vince zoltán zsigmond zsolt farkas
anna mária erzsébet katalin éva ilona margit zsuzsanna júlia ágnes judit irén klára magda piroska rozália terézia
""".split())
_ROMAN = ["", "i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x", "xi", "xii", "xiii", "xiv", "xv",
          "xvi", "xvii", "xviii", "xix", "xx"]
_ROMAN_SET = set(_ROMAN[1:])


class Verdict(str, Enum):
    EXACT = "exact"      # pontosan egyezik (normalizálás után)
    CLOSE = "close"      # elfogadva, de nem pontos alak
    WRONG = "wrong"


def _fold(s: str) -> str:
    """Ékezetek nélkül: ö→o, ő→o, é→e …"""
    return "".join(c for c in unicodedata.normalize("NFD", s) if not unicodedata.combining(c))


def normalize(s: str) -> str:
    s = unicodedata.normalize("NFC", s or "").lower().strip()
    # „4.” → „iv” (sorszámnév), hogy a római és arab alak egyezzen
    s = re.sub(r"\b(\d{1,2})\.(?=\s|$)", lambda m: _ROMAN[int(m.group(1))] if 0 < int(m.group(1)) < len(_ROMAN) else m.group(1), s)
    s = re.sub(r"[\"'’`„”“«»().,;:!?¿¡\-–—/]", " ", s)
    words = s.split()
    while words and words[0] in ARTICLES and len(words) > 1:
        words = words[1:]
    return " ".join(words)


def _numerals(s: str) -> set[str]:
    return {w for w in s.split() if w in _ROMAN_SET or w.isdigit()}


def _person_like(answer: str) -> bool:
    words = answer.split()
    if len(words) < 2:
        return False
    return all(w[0].isupper() or w.lower() in PARTICLES for w in words if w)


def variants(answer: str) -> list[str]:
    """A helyes válasz elfogadható alakjai (normalizálva)."""
    out: list[str] = []
    raw = [answer]
    # „Côte d'Ivoire (Ivory Coast)” → mindkét rész
    m = re.match(r"^(.*?)\s*\((.+)\)\s*$", answer)
    if m:
        raw += [m.group(1), m.group(2)]
    for part in list(raw):
        if "/" in part:
            raw += [p.strip() for p in part.split("/")]
    for r in raw:
        n = normalize(r)
        if n and n not in out:
            out.append(n)
        # vezetéknév, ha személynévnek látszik és nincs benne sorszám
        if _person_like(r) and not _numerals(n) and " és " not in r:
            words = r.split()
            # magyar névsorrend: „Lechner Ödön” → „Lechner”; egyébként „Ludwig van Beethoven” → „Beethoven”
            fam = words[0] if words[-1].lower() in HU_GIVEN else words[-1]
            fam = normalize(fam)
            if len(fam) >= 4 and fam not in out:
                out.append(fam)
    return out


def _close(a: str, b: str) -> bool:
    fa, fb = _fold(a), _fold(b)
    if fa == fb:
        return True
    n = max(len(fa), len(fb))
    if n < 5:
        return False
    ratio = SequenceMatcher(None, fa, fb).ratio()
    return ratio >= (0.86 if n < 10 else 0.82)


def check(user: str, answer: str, distractors: Iterable[str] = (), accept: Iterable[str] = ()) -> Verdict:
    u = normalize(user)
    if not u:
        return Verdict.WRONG
    distractors = list(distractors)
    vs = variants(answer)
    for alt in accept:
        vs += [v for v in variants(alt) if v not in vs]
    if u in vs:
        return Verdict.EXACT
    # pontos egyezés egy hibás opcióval → hibás
    for d in distractors:
        if u in variants(d):
            return Verdict.WRONG
    for v in vs:
        if _numerals(v) != _numerals(u):
            continue
        if _close(u, v):
            # ha egy hibás opcióhoz legalább ennyire közel van, nem döntünk a javára
            if any(_close(u, dv) and SequenceMatcher(None, _fold(u), _fold(dv)).ratio()
                   >= SequenceMatcher(None, _fold(u), _fold(v)).ratio()
                   for d in distractors for dv in variants(d)):
                continue
            return Verdict.CLOSE
    return Verdict.WRONG


_NOT_TYPEABLE = re.compile(r"alábbi|felsorolt|melyik állítás|melyik igaz|melyik hamis|nem igaz|\bigaz\b|\bhamis\b", re.I)


def typeable(q: Question) -> bool:
    """Beírható-e értelmesen a válasz (rövid név, cím, szám), vagy választani kell."""
    a = q.correct_text
    if len(a) > 32 or len(a.split()) > 5 or " vs " in a:
        return False
    if _NOT_TYPEABLE.search(q.text):
        return False
    return True
