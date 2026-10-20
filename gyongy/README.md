# Csabagyöngye – új felület

Önálló, újraírt kvízfelület ugyanarra a kérdésbázisra (`quiz_data.py` + `topics/`).
A régi alkalmazás (`streamlit_app.py`) érintetlen, a kettő párhuzamosan futtatható.

## Indítás

```bash
pip install -r requirements.txt
streamlit run gyongy_app.py
```

Streamlit Cloudon az app beállításaiban a **Main file path** legyen `gyongy_app.py`.

## Mit tud

- Témaválasztó csoportosítva (Zene, Kép, Történelem …), témánkénti kérdésszámmal
- Három mód: **Gyakorlás** (azonnali visszajelzés + magyarázat), **Teszt** (kiértékelés a végén), **Hirtelen halál** (az első hibáig)
- A kérdések a választott témák között egyenletesen oszlanak el
- Hang- és képkérdések (zene, festmények, zászlók, logók) – a hiányzó fájlú kérdéseket kihagyja
- Billentyűk: `1`–`4` a válaszokhoz, `Enter` a továbblépéshez
- Eredmény szőlőfürtként, témánkénti bontás, a hibás kérdések átnézése és újragyakorlása

## Felépítés

| Fájl | Szerep |
|---|---|
| `catalog.py` | témák neve és csoportja, kérdések egységesítése, médiafájlok megkeresése |
| `engine.py` | a kvízmenet logikája (Streamlit nélkül is tesztelhető) |
| `theme.py` | színek, betűk, CSS |
| `visuals.py` | gyöngysor és fürt SVG |
| `app.py` | a három nézet: témaválasztó, kvíz, eredmény |

Új témakör: vedd fel a `quiz_data.QUIZ_DATA_BY_TOPIC`-ba, majd a `catalog.TOPICS` listába egy névvel és csoporttal.
