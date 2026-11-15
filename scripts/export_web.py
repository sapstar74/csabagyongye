"""A kérdésbank exportálása a webes felülethez (web/data/questions.json).

Futtatás a repó gyökeréből:  python scripts/export_web.py

A `gyongy.catalog` egységesített kérdéseit írja ki; a helyi médiafájlokra a
repó gyökeréhez viszonyított, URL-kódolt útvonallal hivatkozik. Új vagy
módosított kérdés után újra kell futtatni.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from gyongy.catalog import GROUPS, TOPICS, load_bank  # noqa: E402


def _media(path: str | None) -> str | None:
    if not path:
        return None
    if path.startswith(("http://", "https://")):
        return path
    return quote(Path(path).relative_to(ROOT).as_posix())


def main() -> None:
    bank = load_bank()
    topics, questions = [], []
    for meta in TOPICS:
        qs = bank.get(meta.key)
        if not qs:
            continue
        topics.append({"key": meta.key, "name": meta.name, "group": meta.group, "count": len(qs)})
        for q in qs:
            item = {"id": q.uid, "t": q.topic, "q": q.text, "o": q.options, "c": q.correct, "e": q.explanation}
            if q.audio:
                item["a"] = _media(q.audio)
            if q.image:
                item["i"] = _media(q.image)
            if q.caption:
                item["cap"] = q.caption
            if q.credit:
                item["cr"] = q.credit
            if q.credit_url:
                item["cru"] = q.credit_url
            questions.append(item)
    out = ROOT / "web" / "data" / "questions.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"groups": GROUPS, "topics": topics, "questions": questions}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{len(questions)} kérdés, {len(topics)} témakör -> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
