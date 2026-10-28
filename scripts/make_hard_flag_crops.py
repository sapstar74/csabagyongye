"""A nehéz zászlórészlet-blokk képeinek előállítása.

Forrás:  zaszlo_kepek/<kód>_1000px.png
Cél:     data/flags/crop_nehez/<kód>_nehez.png
Doboz:   topics/zaszlok_reszletek_nehez.CROPS

Futtatás a repó gyökeréből:  python scripts/make_hard_flag_crops.py [--sheet kontaktlap.png]
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from topics.zaszlok_reszletek import COUNTRY_CODE_TO_NAME  # noqa: E402
from topics.zaszlok_reszletek_nehez import CROPS, CROP_SUBDIR  # noqa: E402

SRC = ROOT / "zaszlo_kepek"
DST = ROOT / CROP_SUBDIR
MAX_SIDE = 480


def crop_one(code: str, box: tuple) -> Image.Image:
    im = Image.open(SRC / f"{code.lower()}_1000px.png").convert("RGB")
    w, h = im.size
    x0, y0, x1, y1 = box
    out = im.crop((round(x0 * w), round(y0 * h), round(x1 * w), round(y1 * h)))
    out.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", help="kontaktlap mentése ellenőrzéshez")
    args = ap.parse_args()

    DST.mkdir(parents=True, exist_ok=True)
    seen = set()
    tiles = []
    for item in CROPS:
        code = item["code"]
        assert code not in seen, f"duplikált kód: {code}"
        seen.add(code)
        for c in [code, *item["wrong"]]:
            assert c in COUNTRY_CODE_TO_NAME, f"ismeretlen kód: {c}"
        assert len(set(item["wrong"])) == 3 and code not in item["wrong"], code
        img = crop_one(code, item["box"])
        img.save(DST / f"{code.lower()}_nehez.png", optimize=True)
        tiles.append((code, item["wrong"], img))
    print(f"{len(tiles)} kivágás → {DST.relative_to(ROOT)}")

    if args.sheet:
        T, cols = 220, 6
        rows = (len(tiles) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * T, rows * (T + 28)), "white")
        d = ImageDraw.Draw(sheet)
        for i, (code, wrong, img) in enumerate(tiles):
            t = img.copy()
            t.thumbnail((T - 10, T - 10))
            x, y = (i % cols) * T, (i // cols) * (T + 28)
            sheet.paste(t, (x + 5, y + 5))
            d.text((x + 5, y + T), f"{code}  vs {' '.join(wrong)}", fill="black")
        sheet.save(args.sheet)


if __name__ == "__main__":
    main()
