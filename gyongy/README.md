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
- Két mód: **Kérdéssor** (szabadon megadott számú kérdés, akár a kiválasztott témák összes kérdése) és **Hirtelen halál** (az első hibáig)
- Rádiógombbal állítható, mikor derüljön ki, jó-e a válasz: **rögtön a válasz után** (magyarázattal) vagy **csak a végén**
- A kérdések a választott témák között egyenletesen oszlanak el
- Hang- és képkérdések (zene, festmények, zászlók, logók) – a hiányzó fájlú kérdéseket kihagyja
- Két válaszadási mód: **Választás** (4 lehetőség) vagy **Beírás** (szabad szöveg). Beírásnál a kis- és nagybetű,
  a névelő és az ékezet nem számít, apró elgépelést elfogadunk (jelezve a pontos alakot), személynévnél elég a
  vezetéknév, a sorszámnak viszont stimmelnie kell (IV. László ≠ V. László; „4. László” jó). Ahol a válasz túl hosszú
  vagy állítás-kiválasztós a kérdés (kb. a kérdések 7%-a), ott automatikusan választani kell. A „Nem tudom” gombbal
  bármikor kérhetők a lehetőségek.
- Távoli képek is használhatók (`image_url` + kötelező `credit`, `credit_url`) – így készült a
  *20. századi építészek* témakör Wikimedia Commons-képekkel; a képek a böngészőbe töltődnek, a repóba nem kerülnek
- A zászlós témák országnevei magyarul jelennek meg (`countries.py`); beírásnál az angol alak is elfogadott
- Billentyűk: `1`–`4` a válaszokhoz, `Enter` a beküldéshez és a továbblépéshez
- Eredmény szőlőfürtként, témánkénti bontás, a hibás kérdések átnézése és újragyakorlása

## Felépítés

| Fájl | Szerep |
|---|---|
| `catalog.py` | témák neve és csoportja, kérdések egységesítése, médiafájlok megkeresése |
| `answers.py` | szabad szöveges válaszok ellenőrzése |
| `countries.py` | országnevek magyarul a zászlós témákhoz |
| `engine.py` | a kvízmenet logikája (Streamlit nélkül is tesztelhető) |
| `theme.py` | színek, betűk, CSS |
| `visuals.py` | gyöngysor és fürt SVG |
| `app.py` | a három nézet: témaválasztó, kvíz, eredmény |

Új témakör: vedd fel a `quiz_data.QUIZ_DATA_BY_TOPIC`-ba, majd a `catalog.TOPICS` listába egy névvel és csoporttal.
