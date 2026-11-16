"""A GitHub Pages oldal összeállítása a _site/ mappába.

Futtatás a repó gyökeréből (ffmpeg kell hozzá):

    python scripts/export_web.py
    python scripts/build_site.py            # -> _site/

Mit csinál:
- bemásolja a web/ mappát, a felület ikonjait és a kérdésekhez tartozó képeket;
- a kérdésekhez tartozó hangfájlokat legfeljebb 90 másodpercre vágja és
  96 kbps-os AAC (.m4a) formátumra kódolja, mert az eredetiek együtt nem
  férnek bele a GitHub Pages 1 GB-os korlátjába;
- a questions.json-ban az új hangfájlokra mutató útvonalakat írja;
- a gyökérbe átirányítást tesz a /web/ oldalra.

A repóban lévő eredeti fájlok nem változnak. A kódolt hangok a --cache
mappában megmaradnak (a forrásfájl tartalmának hash-e a kulcs), így a
következő futás csak az új vagy megváltozott dalokat kódolja újra.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parent.parent
CLIP_SECONDS = 90
BITRATE = "96k"
LIMIT_BYTES = 1_000_000_000  # GitHub Pages: a közzétett oldal legfeljebb 1 GB


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:20]


def _encode(src: Path, cached: Path) -> None:
    if cached.exists():
        return
    tmp = cached.with_name(cached.stem + ".tmp.m4a")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(src), "-map", "0:a:0", "-t", str(CLIP_SECONDS),
         "-ac", "2", "-c:a", "aac", "-b:a", BITRATE, "-movflags", "+faststart", str(tmp)],
        check=True, stdin=subprocess.DEVNULL,
    )
    tmp.replace(cached)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(ROOT / "_site"))
    ap.add_argument("--cache", default=str(ROOT / ".cache" / "audio"))
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    out, cache = Path(args.out), Path(args.cache)
    if out.exists():
        shutil.rmtree(out)
    cache.mkdir(parents=True, exist_ok=True)

    shutil.copytree(ROOT / "web", out / "web", ignore=shutil.ignore_patterns("README.md"))
    for icon in ("icon-192.png", "icon-512.png"):
        (out / "static").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "static" / icon, out / "static" / icon)

    data_path = out / "web" / "data" / "questions.json"
    data = json.loads(data_path.read_text(encoding="utf-8"))
    audio_jobs: dict[str, tuple[Path, Path]] = {}
    images: set[str] = set()
    for q in data["questions"]:
        a = q.get("a")
        if a and not a.startswith(("http://", "https://")):
            rel = Path(unquote(a))
            new_rel = rel.with_suffix(".m4a")
            audio_jobs[a] = (ROOT / rel, out / new_rel)
            q["a"] = quote(new_rel.as_posix())
        i = q.get("i")
        if i and not i.startswith(("http://", "https://")):
            images.add(unquote(i))

    missing = [str(src) for src, _ in audio_jobs.values() if not src.exists()] + [p for p in images if not (ROOT / p).exists()]
    if missing:
        sys.exit("Hiányzó médiafájlok:\n" + "\n".join(missing[:20]))

    for rel in sorted(images):
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, dst)

    # Ugyanaz a dal több kérdésnél is szerepelhet: minden egyedi tartalmat egyszer kódolunk.
    targets: dict[Path, tuple[Path, list[Path]]] = {}
    for src, dst in audio_jobs.values():
        cached = cache / f"{_sha(src)}-{CLIP_SECONDS}s-{BITRATE}.m4a"
        targets.setdefault(cached, (src, []))[1].append(dst)
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        for n, _ in enumerate(pool.map(lambda item: _encode(item[1][0], item[0]), targets.items()), 1):
            if n % 100 == 0:
                print(f"  {n}/{len(targets)} hangfájl kész", flush=True)
    canonical: dict[str, str] = {}  # minden példány az első fájlra mutat
    for cached, (_, dsts) in targets.items():
        first = sorted(set(dsts))[0]
        first.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(cached, first)
        for dst in dsts:
            canonical[quote(dst.relative_to(out).as_posix())] = quote(first.relative_to(out).as_posix())
    for q in data["questions"]:
        if q.get("a") in canonical:
            q["a"] = canonical[q["a"]]

    data_path.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    (out / "index.html").write_text(
        '<!doctype html><html lang="hu"><head><meta charset="utf-8"><title>Csabagyöngye</title>'
        '<meta http-equiv="refresh" content="0; url=web/"><link rel="canonical" href="web/"></head>'
        '<body><a href="web/">Csabagyöngye</a></body></html>\n', encoding="utf-8")
    (out / ".nojekyll").write_text("", encoding="utf-8")

    total = sum(p.stat().st_size for p in out.rglob("*") if p.is_file())
    print(f"{len(audio_jobs)} hangfájl, {len(images)} kép, összesen {total / 1e9:.2f} GB -> {out}")
    if total > LIMIT_BYTES:
        sys.exit(f"Túl nagy a GitHub Pages-hez: {total / 1e9:.2f} GB > 1 GB")


if __name__ == "__main__":
    main()
