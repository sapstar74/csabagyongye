# Csabagyöngye – webes felület

Önálló, Streamlit nélküli felület ugyanarra a kérdésbázisra. A régi alkalmazások
(`streamlit_app.py`, `gyongy_app.py`) érintetlenek.

## Indítás

A repó gyökeréből:

```bash
python scripts/export_web.py     # kérdésbank → web/data/questions.json
python scripts/export_kilenc_plusz_egy.py   # 9+1 játékok → web/data/kilenc_plusz_egy.json
python -m http.server 8000       # majd a böngészőben: http://localhost:8000/web/
```

A szervert a repó **gyökeréből** kell indítani, mert a képek és hangok a gyökérhez
képest vannak megadva (`audio_files/…`, `data/flags/…`). Fájlként megnyitva
(`file://`) nem működik.

Új vagy módosított kérdés után futtasd újra az exportot, és a `questions.json`-t
is commitold. Ugyanez igaz a 9+1 játékokra és a `kilenc_plusz_egy.json`-ra.

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

- Kérdéssor: a kiválasztott témákból sorsolt, csúszkán beállított számú kérdés (5–50),
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

- **3. blokk – szabad szöveges válasszal** (jelölőnégyzet a 9+1 kártya alatt, a böngészőben megmarad): a kérdéssorban
  válaszlehetőségek helyett beírós válasz. Csak a rövid (legfeljebb 40 karakteres) válaszú
  kérdések jönnek; az állításos, tagadó („Melyik NEM…”) és kakukktojásos kérdések kimaradnak.
  Az összevetés a 9+1 szabályát követi (kis- és nagybetű, ékezet, írásjel, névelő nem számít),
  emellett elfogadja a „/” jellel elválasztott alakokat, a zárójel és a „ft.” utáni rész
  nélküli alakot, és 5 betűtől egy, 10 betűtől két elgépelést (számot tartalmazó válasznál
  soha). Hibás válasznál nincs automatikus továbblépés, és a „Mégis jó volt” gombbal a
  játékos elfogadtathatja a válaszát

A kérdéssorban „Hirtelen halál” mód ebben a felületben nincs.

## 9+1

Külön játék a témaválasztó tetején, saját kártyával (a témák kijelölésétől független).

- Tíz beírós kérdés egy oldalon; a kiértékelésig bármelyik válasz javítható
- **9+1**: kilenc kérdés válaszai összefüggnek, a +1 kérdésre az a válasz jó, amelyik ebbe az
  összefüggésbe illik. Az összefüggést a játék csak a kiértékelés után írja ki
- **Párok**: tíz kérdés, az 1–6., 2–7., 3–8., 4–9. és 5–10. válasz együtt egy ismert nevet,
  címet vagy kifejezést ad ki
- Nyolc kategória (összetett szó, művek, földrajz, személyiségek, ételek, párok, rejtett lista,
  közös kezdőbetűk);
  a játék véletlenszerűen jön, kategóriát nem lehet választani, és játék közben nem is látszik
- A válaszoknál a kis- és nagybetű, az ékezet, az írásjel és a névelő nem számít; elgépelést
  nem fogad el, csak a forrásban felsorolt alakokat
- A már játszott játékok nem jönnek újra, amíg van új; a félbehagyott játék megmarad
  (mindkettő a böngészőben tárolódik)
- Üres válasznál az első koppintásra csak figyelmeztet, a második értékel ki

Új játék: a `kilenc_plusz_egy/` megfelelő fájljába kell beírni (a formátum leírása a
`scripts/export_kilenc_plusz_egy.py` elején), majd az exportot újra futtatni. Az export
ellenőriz is: kérdésszám, két nehéz kérdés, összetételek, rejtett elemek, ételek átfedése.

## Felépítés

| Fájl | Szerep |
|---|---|
| `index.html`, `style.css`, `app.js` | a teljes felület, build lépés nélkül |
| `data/questions.json` | az exportált kérdésbank (generált fájl) |
| `data/kilenc_plusz_egy.json` | az exportált 9+1 játékok (generált fájl) |
| `fonts/` | Archivo és Inter betűk helyben (SIL OFL 1.1) |
| `../scripts/export_web.py` | export a `gyongy.catalog` egységesített kérdéseiből |
| `../kilenc_plusz_egy/` | a 9+1 játékok forrása, kategóriánként egy szövegfájl |
| `../scripts/export_kilenc_plusz_egy.py` | a 9+1 játékok ellenőrzése és exportja |
| `../scripts/build_site.py` | a közzétehető oldal összeállítása `_site/`-ba |
| `manifest.webmanifest` | telefonos telepíthetőség (kezdőképernyő) |
