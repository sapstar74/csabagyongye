"""Témakörök és kérdések.

A kérdésadatbázis a repó meglévő `quiz_data.QUIZ_DATA_BY_TOPIC` szótára;
ez a modul csak egységes formára hozza, és megkeresi a hozzájuk tartozó
hang- és képfájlokat. Új kérdést továbbra is a `topics/` mappában kell
felvenni – az új felület automatikusan látja.
"""

from __future__ import annotations

import os
import unicodedata
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Optional

from .countries import COUNTRY_HU, EXTRA_ALIASES, FLAG_TOPICS

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Témakör-metaadatok
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class TopicMeta:
    key: str          # kulcs a QUIZ_DATA_BY_TOPIC-ban
    name: str         # megjelenített név
    group: str        # csoport a választóban


# A sorrend a választóban is ez lesz.
GROUPS = ["Zene", "Kép", "Történelem", "Tudomány és természet", "Kultúra", "Kalandorok", "Sport", "Nyelv és emberek"]

TOPICS: list[TopicMeta] = [
    TopicMeta("komolyzene", "Komolyzene", "Zene"),
    TopicMeta("magyar_zenekarok", "Magyar előadók", "Zene"),
    TopicMeta("nemzetkozi_zenekarok", "Nemzetközi előadók", "Zene"),
    TopicMeta("one_hit_wonders", "One hit wonders", "Zene"),
    TopicMeta("sorozat_focimek", "Sorozat-főcímek", "Zene"),
    TopicMeta("hip_hop", "Hip-hop", "Zene"),
    TopicMeta("rock_metal", "Rock és metal", "Zene"),
    TopicMeta("dj_producer", "DJ-k és producerek", "Zene"),
    TopicMeta("almombol_felebresztve", "Álmomból felébresztve", "Zene"),
    TopicMeta("festmények", "Festmények", "Kép"),
    TopicMeta("magyar_festmenyek", "Magyar festmények", "Kép"),
    TopicMeta("zászlók", "Zászlók", "Kép"),
    TopicMeta("zászlórészlet", "Zászlórészletek", "Kép"),
    TopicMeta("zászlórészlet_nehéz", "Zászlórészletek – nehéz (Afrika, arab, Óceánia)", "Kép"),
    TopicMeta("sport_logók", "Sportlogók", "Kép"),
    TopicMeta("magyar történelem", "Magyar történelem", "Történelem"),
    TopicMeta("világtörténelem", "Világtörténelem", "Történelem"),
    TopicMeta("politika", "Politika", "Történelem"),
    TopicMeta("vallás és egyháztörténet", "Vallás és egyháztörténet", "Történelem"),
    TopicMeta("természettudomány", "Természettudomány és földrajz", "Tudomány és természet"),
    TopicMeta("biológia", "Biológia", "Tudomány és természet"),
    TopicMeta("állatok", "Állatok", "Tudomány és természet"),
    TopicMeta("tudósok", "Tudósok", "Tudomány és természet"),
    TopicMeta("irodalom", "Irodalom és drámák", "Kultúra"),
    TopicMeta("regények", "Regények", "Kultúra"),
    TopicMeta("művészet", "Művészet", "Kultúra"),
    TopicMeta("mitológia", "Mitológia", "Kultúra"),
    TopicMeta("építészek", "20–21. századi építészek", "Kultúra"),
    TopicMeta("felfedezők", "Felfedezők és híres hajók", "Kalandorok"),
    TopicMeta("űrszondák", "Űrszondák", "Kalandorok"),
    TopicMeta("sport", "Sport", "Sport"),
    TopicMeta("labdarugo_palyafutas", "Labdarúgó-pályafutások", "Sport"),
    TopicMeta("híres magyarok", "Híres magyarok", "Nyelv és emberek"),
    TopicMeta("becenevek", "Becenevek", "Nyelv és emberek"),
    TopicMeta("idióta_szavak", "Idióta szavak", "Nyelv és emberek"),
]

TOPIC_BY_KEY = {t.key: t for t in TOPICS}


# ---------------------------------------------------------------------------
# Kérdés
# ---------------------------------------------------------------------------

@dataclass
class Question:
    uid: str                      # stabil azonosító: "<téma>#<index>"
    topic: str
    text: str
    options: list[str]
    correct: int
    explanation: str = ""
    audio: Optional[str] = None   # abszolút útvonal, ha van
    image: Optional[str] = None   # abszolút útvonal, ha van
    caption: str = ""             # pl. dal- vagy műcím, ha külön adott
    credit: str = ""              # kép forrása/licence (távoli képeknél kötelező)
    credit_url: str = ""
    aliases: dict[str, list[str]] = field(default_factory=dict)  # opció → beírásnál elfogadott más alakok
    extra: dict = field(default_factory=dict)

    @property
    def correct_text(self) -> str:
        return self.options[self.correct]

    @property
    def kind(self) -> str:
        if self.audio:
            return "audio"
        if self.image:
            return "image"
        return "text"


# ---------------------------------------------------------------------------
# Médiafájlok feloldása
# ---------------------------------------------------------------------------

_AUDIO_ROOTS = ["audio_files", "audio_files_magyar_uj", "audio_files_one_hit_wonders"]
_IMAGE_ROOTS = {
    "festmények": ["festmény_képek"],
    "magyar_festmenyek": ["magyar_festmeny_kepek", "magyar_festmény_képek copy"],
}
_VISUAL_TOPICS = {"festmények", "magyar_festmenyek", "zászlók", "zászlórészlet", "zászlórészlet_nehéz", "sport_logók"}
_MEDIA_EXT ={".mp3", ".m4a", ".wav", ".ogg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def _nfc(s: str) -> str:
    # macOS-en a fájlnevek NFD-ben (szétbontott ékezettel) kerülnek a repóba.
    return unicodedata.normalize("NFC", s)


@lru_cache(maxsize=1)
def _media_index() -> dict[str, list[Path]]:
    """Fájlnév (NFC) → elérési utak, a repó összes médiamappájából."""
    index: dict[str, list[Path]] = {}
    roots = set(_AUDIO_ROOTS) | {"data"}
    for rs in _IMAGE_ROOTS.values():
        roots.update(rs)
    # A könyvtárneveket is normalizálva keressük (NFC/NFD kettőzés).
    wanted = {_nfc(r) for r in roots}
    for entry in ROOT.iterdir():
        if not entry.is_dir() or _nfc(entry.name) not in wanted:
            continue
        for dirpath, _, files in os.walk(entry):
            for f in files:
                if Path(f).suffix.lower() in _MEDIA_EXT:
                    index.setdefault(_nfc(f), []).append(Path(dirpath) / f)
    return index


def _resolve(raw: str, topic: str, prefer_dirs: list[str]) -> Optional[str]:
    if not raw:
        return None
    direct = ROOT / raw
    if direct.exists():
        return str(direct)
    for d in prefer_dirs:
        p = ROOT / d / raw
        if p.exists():
            return str(p)
    candidates = _media_index().get(_nfc(Path(raw).name), [])
    if not candidates:
        return None
    # Ha több azonos nevű fájl van, a téma saját mappája nyer.
    for c in candidates:
        if _nfc(c.parent.name) == _nfc(topic):
            return str(c)
    return str(candidates[0])


# ---------------------------------------------------------------------------
# Betöltés
# ---------------------------------------------------------------------------

def _normalize(topic: str, i: int, raw: dict) -> Optional[Question]:
    try:
        options = [str(o) for o in raw["options"]]
        correct = int(raw["correct"])
    except (KeyError, TypeError, ValueError):
        return None
    if len(options) < 2 or not 0 <= correct < len(options):
        return None

    audio = None
    if raw.get("audio_file"):
        audio = _resolve(raw["audio_file"], topic, [f"audio_files/{topic}", "audio_files"])

    image = None
    img_raw = raw.get("logo_path") or raw.get("image_file") or raw.get("image_url")
    if raw.get("image_url"):
        image = str(raw["image_url"])          # távoli kép: a böngésző tölti be
    elif img_raw:
        image = _resolve(img_raw, topic, _IMAGE_ROOTS.get(topic, []))

    # Hang- vagy képkérdés, aminek nincs meg a fájlja, nem játszható.
    if raw.get("audio_file") and not audio:
        return None
    if img_raw and not image:
        return None
    if topic in _VISUAL_TOPICS and not image:
        return None

    explanation = str(raw.get("explanation", "")).strip()
    aliases: dict[str, list[str]] = {}
    if raw.get("accept"):
        aliases[options[correct]] = [str(a) for a in raw["accept"]]
    if topic in FLAG_TOPICS:
        # angol országnevek → magyar; az angol alak beírásnál továbbra is jó
        en = options[correct]
        hu_opts = [COUNTRY_HU.get(o, o) for o in options]
        for o_en, o_hu in zip(options, hu_opts):
            aliases[o_hu] = ([o_en] if o_en != o_hu else []) + EXTRA_ALIASES.get(o_hu, [])
        options = hu_opts
        if en in explanation:
            explanation = explanation.replace(en, options[correct])

    return Question(
        uid=f"{topic}#{i}",
        topic=topic,
        text=str(raw.get("question", "")).strip(),
        options=options,
        correct=correct,
        explanation=explanation,
        aliases=aliases,
        audio=audio,
        image=image,
        caption=str(raw.get("song_title", "") or "").strip(),
        credit=str(raw.get("credit", "") or ""),
        credit_url=str(raw.get("credit_url", "") or ""),
    )


@lru_cache(maxsize=1)
def load_bank() -> dict[str, list[Question]]:
    """Az összes játszható kérdés témakörönként."""
    from quiz_data import QUIZ_DATA_BY_TOPIC  # a meglévő adatréteg

    bank: dict[str, list[Question]] = {}
    for meta in TOPICS:
        raw_list = QUIZ_DATA_BY_TOPIC.get(meta.key, [])
        qs = [q for i, r in enumerate(raw_list) if isinstance(r, dict) and (q := _normalize(meta.key, i, r))]
        if qs:
            bank[meta.key] = qs
    return bank
