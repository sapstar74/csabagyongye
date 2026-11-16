"""A 9+1 játékok exportálása a webes felülethez (web/data/kilenc_plusz_egy.json).

Futtatás a repó gyökeréből:  python scripts/export_kilenc_plusz_egy.py

A forrás a kilenc_plusz_egy/ mappa, kategóriánként egy szövegfájl. Új vagy
módosított játék után újra kell futtatni, és a JSON-t is commitolni kell.

Kétféle játék van:
- 9+1: kilenc kérdés válaszai összefüggnek, a +1 kérdés válasza is ebbe az
  összefüggésbe illik (az összefüggést a játék csak a kiértékelés után írja ki);
- párok: tíz kérdés, az 1–6., 2–7., 3–8., 4–9. és 5–10. válasz párt alkot.

Sorformátum (a mezőket " | " választja el, az üres záró mezők elhagyhatók):

    # azonosító | összefüggés | magyarázat      9+1 játék fejléce
    # azonosító | téma                          páros játék fejléce
    = pár1; pár2; pár3; pár4; pár5              a páros játék megfejtései
    kérdés | válasz | elfogadott;… | kapcsolat | N
    ---                                         összetett szó: előtagok / utótagok határa
    + kérdés | válasz | elfogadott;… | kapcsolat     a +1 kérdés

"N" = nehéz kérdés (játékonként pontosan kettő). A "kapcsolat" a kiértékelés
után jelenik meg: összetett szónál maga az összetétel, rejtett listánál a
válaszban megbúvó listaelem. A „közös kezdőbetűk” játékokban az összefüggés a
három közös kezdőbetű (ékezet szerint is egyezniük kell).

A szkript ellenőrzi is a játékokat (kérdésszám, két nehéz kérdés, ismétlődő
válasz, összetételek, rejtett elemek, közös kezdőbetűk, az ételek hozzávalóinak átfedése), és
hibánál nem ír fájlt.
"""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "kilenc_plusz_egy"
OUT = ROOT / "web" / "data" / "kilenc_plusz_egy.json"

COMPOUND, PAIRS, HIDDEN, FOOD = "összetett szó", "párok", "rejtett lista", "híres étel összetevői"
PREFIX = "közös kezdőbetűk"
SOURCES = [
    ("osszetett_szo.txt", COMPOUND),
    ("muvek.txt", "mű címe, szereplői, helyszínei"),
    ("foldrajz.txt", "földrajzi egység"),
    ("szemelyisegek.txt", "híres személyiség"),
    ("etelek.txt", FOOD),
    ("parok.txt", PAIRS),
    ("rejtett_lista.txt", HIDDEN),
    ("kozos_kezdet.txt", PREFIX),
]


def normalize(text: str) -> str:
    """Kisbetű, ékezet, írásjel és névelő nélkül – ugyanez a szabály fut a web/app.js-ben (norm)."""
    text = unicodedata.normalize("NFD", str(text).strip().lower())
    text = "".join(c for c in text if not "̀" <= c <= "ͯ")
    words = re.sub(r"[^a-z0-9]+", " ", text).split()
    if len(words) > 1 and words[0] in ("a", "az"):
        words = words[1:]
    return "".join(words)


def _fields(line: str, n: int) -> list[str]:
    parts = [p.strip() for p in line.split("|")]
    return parts + [""] * (n - len(parts))


def _item(line: str) -> dict:
    q, answer, alts, link, hard = _fields(line, 5)[:5]
    item = {"q": q, "a": [answer] + [a.strip() for a in alts.split(";") if a.strip()]}
    if link:
        item["k"] = link
    if hard == "N":
        item["h"] = 1
    return item


def parse(path: Path, kind: str) -> list[dict]:
    games: list[dict] = []
    game: dict | None = None
    for no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            if line.startswith("#"):
                gid, title, note = _fields(line[1:], 3)[:3]
                game = {"id": gid, "type": kind, "items": []}
                if kind == PAIRS:
                    game["theme"] = title
                else:
                    game["link"] = title
                    if note:
                        game["note"] = note
                games.append(game)
            elif line.startswith("="):
                game["pairs"] = [p.strip() for p in line[1:].split(";") if p.strip()]
            elif line == "---":
                game["prefixes"] = len(game["items"])
            elif line.startswith("+"):
                game["closer"] = _item(line[1:])
            else:
                game["items"].append(_item(line))
        except TypeError:
            sys.exit(f"{path.name}:{no}: játékfejléc (# …) előtt álló sor")
    for g in games:
        if kind == COMPOUND:
            n = g.pop("prefixes", 5)
            words = [it.get("k", "") for it in g["items"]]
            g["note"] = f"Előtag ({n}): " + ", ".join(words[:n]) + f"; utótag ({9 - n}): " + ", ".join(words[n:]) + "."
            g["_prefixes"] = n
    return games


def validate(games: list[dict]) -> list[str]:
    errors: list[str] = []

    def err(game: dict, msg: str) -> None:
        errors.append(f"{game['id']}: {msg}")

    ids = [g["id"] for g in games]
    for gid in sorted({i for i in ids if ids.count(i) > 1}):
        errors.append(f"{gid}: az azonosító többször szerepel")
    food_seen: dict[str, str] = {}
    for g in games:
        pairs = g["type"] == PAIRS
        want = 10 if pairs else 9
        if len(g["items"]) != want:
            err(g, f"{len(g['items'])} kérdés van {want} helyett")
        if sum(1 for it in g["items"] if it.get("h")) != 2:
            err(g, "pontosan két nehéz (N) kérdés kell")
        everything = g["items"] + ([] if pairs else [g.get("closer") or {"q": "", "a": [""]}])
        for it in everything:
            if not it["q"].endswith("?"):
                err(g, f"nem kérdőjelre végződik: {it['q']!r}")
            if not normalize(it["a"][0]):
                err(g, f"hiányzó válasz: {it['q']!r}")
        answers = [normalize(it["a"][0]) for it in everything]
        if len(set(answers)) != len(answers):
            err(g, "ugyanaz a válasz többször szerepel")
        if pairs:
            if len(g.get("pairs", [])) != 5 or not g.get("theme"):
                err(g, "öt pár (= …) és téma kell")
            continue
        if "closer" not in g:
            err(g, "hiányzik a +1 kérdés (+ …)")
            continue
        key = normalize(g["link"])
        if g["type"] == COMPOUND:
            n = g["_prefixes"]
            for i, it in enumerate(g["items"]):
                answer = normalize(it["a"][0])
                expected = answer + key if i < n else key + answer
                if normalize(it.get("k", "")) != expected:
                    err(g, f"az összetétel nem stimmel: {it.get('k')!r}")
            for a in g["closer"]["a"]:
                if key not in normalize(a):
                    err(g, f"a +1 válaszban nincs benne a kulcsszó: {a!r}")
        if g["type"] == HIDDEN:
            for it in g["items"] + [g["closer"]]:
                if normalize(it.get("k", "")) not in normalize(it["a"][0]) or not it.get("k"):
                    err(g, f"a rejtett elem nincs benne a válaszban: {it['a'][0]!r}")
        if g["type"] == PREFIX:
            start = g["link"].lower()
            if len(start) != 3:
                err(g, "az összefüggés három betű legyen")
            for it in g["items"] + [g["closer"]]:
                if not it["a"][0].lower().startswith(start):
                    err(g, f"nem {g['link']} betűkkel kezdődik: {it['a'][0]!r}")
        if g["type"] == FOOD:
            for it in g["items"] + [g["closer"]]:
                a = normalize(it["a"][0])
                if a in food_seen:
                    err(g, f"hozzávaló-átfedés ({it['a'][0]}) ezzel: {food_seen[a]}")
                food_seen[a] = g["id"]
    return errors


def main() -> None:
    games: list[dict] = []
    for name, kind in SOURCES:
        games += parse(SRC / name, kind)
    errors = validate(games)
    if errors:
        sys.exit("Hibás játékok:\n" + "\n".join(errors))
    for g in games:
        g.pop("_prefixes", None)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"games": games}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    counts = ", ".join(f"{kind}: {sum(1 for g in games if g['type'] == kind)}" for _, kind in SOURCES)
    print(f"{len(games)} játék ({counts}) -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
