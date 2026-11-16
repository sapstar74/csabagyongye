# Csabagyöngye – webes felület

Önálló, Streamlit nélküli felület ugyanarra a kérdésbázisra. A régi alkalmazások
(`streamlit_app.py`, `gyongy_app.py`) érintetlenek.

## Indítás

A repó gyökeréből:

```bash
python scripts/export_web.py     # kérdésbank → web/data/questions.json
python -m http.server 8000       # majd a böngészőben: http://localhost:8000/web/
```

A szervert a repó **gyökeréből** kell indítani, mert a képek és hangok a gyökérhez
képest vannak megadva (`audio_files/…`, `data/flags/…`). Fájlként megnyitva
(`file://`) nem működik.

Új vagy módosított kérdés után futtasd újra az exportot, és a `questions.json`-t
is commitold.

## Közzététel (GitHub Pages)

A `.github/workflows/pages.yml` a `main` ág minden érintett változása után
újraépíti és közzéteszi az oldalt: `https://sapstar74.github.io/csabagyongye/`.

- Egyszeri beállítás: a repó **Settings → Pages → Build and deployment → Source**
  mezőjében a **GitHub Actions** legyen kiválasztva.
- Az összeállítás (`scripts/build_site.py`) a hangokat 90 másodpercre vágja és
  96 kbps-os AAC-re kódolja, így az oldal kb. 0,8 GB, a Pages 1 GB-os korlátja alatt.
  A repó eredeti fájljai nem változnak. 1 GB felett az összeállítás hibával leáll.
- Az oldal **nyilvános**: bárki megnyithatja, akinek megvan a linkje.
- Helyben kipróbálni: `python scripts/build_site.py`, majd
  `python -m http.server 8000 -d _site` és `http://localhost:8000/`.

Telefonon a böngésző menüjéből („Hozzáadás a kezdőképernyőhöz”) appként is kitehető.

## Mit tud

- Egy játékmód: a kiválasztott témákból sorsolt, csúszkán beállított számú kérdés (5–50),
  a témák között egyenletesen elosztva
- Minden válasz után visszajelzés és magyarázat; 2 másodperc múlva magától jön a következő
  kérdés (`ADVANCE_MS` az `app.js` elején). A „Várj, elolvasom” gomb vagy a zene tekerése megállítja
- Szöveges, képes és zenés kérdések; a hang a válasz után is szól, csúszkával tekerhető
- Szőlőfürt: a helyes válasz gyöngyszem, a hibás mazsola. 10 kérdésig lefelé keskenyedő
  fürt, fölötte négy szem széles, gördülő füzér; az eredményoldalon a teljes fürt
- Eredmény: pontszám, a hibák áttekintése, a hibás kérdések újrajátszása
- Három paletta (fekete, zöld, borvörös), minden képernyőn váltható; a paletta, a
  kiválasztott témák és a kérdésszám a böngészőben megmarad
- Billentyűk: `1`–`4` vagy `A`–`D` a válaszhoz, `Enter` a következő kérdéshez

A beírós válaszadás és a „Hirtelen halál” mód ebben a felületben nincs benne.

## Felépítés

| Fájl | Szerep |
|---|---|
| `index.html`, `style.css`, `app.js` | a teljes felület, build lépés nélkül |
| `data/questions.json` | az exportált kérdésbank (generált fájl) |
| `fonts/` | Archivo és Inter betűk helyben (SIL OFL 1.1) |
| `../scripts/export_web.py` | export a `gyongy.catalog` egységesített kérdéseiből |
| `../scripts/build_site.py` | a közzétehető oldal összeállítása `_site/`-ba |
| `manifest.webmanifest` | telefonos telepíthetőség (kezdőképernyő) |
