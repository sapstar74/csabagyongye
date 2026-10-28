# Zászlórészletek – nehéz blokk
# Könnyen összetéveszthető afrikai, arab és ritka óceániai zászlók részletei.
#
# Az eredeti "zászlórészlet" témakör (topics/zaszlok_reszletek.py, data/flags/crop/)
# változatlan; ez külön témakör, saját képekkel a data/flags/crop_nehez/ mappában.
#
# Elv: minden kivágáson rajta van az a részlet, ami alapján a válasz egyértelmű
# (sorrend, csillag megléte/hiánya, szín árnyalata), de a három zavaró opció a
# kinézetre leginkább hasonló zászló – nem a földrajzi szomszéd.
#
# A képeket a scripts/make_hard_flag_crops.py állítja elő a zaszlo_kepek/*_1000px.png
# forrásokból a lenti CROPS dobozai alapján. Új tétel: vedd fel ide, futtasd a scriptet.

import random
from pathlib import Path

from topics.zaszlok_reszletek import COUNTRY_CODE_TO_NAME

QUESTION_HU = "Melyik ország zászlajából származik a részlet? (nehéz)"
CROP_SUBDIR = "data/flags/crop_nehez"

# kód, kivágás (x0, y0, x1, y1 a zászló szélességének/magasságának arányában),
# három hasonmás zavaró opció, régió, árulkodó jel
CROPS: list[dict] = [
    # --- Afrika: pánafrikai trikolórok ---------------------------------------
    {"code": "ML", "box": (0.14, 0.25, 0.60, 0.75), "wrong": ["GN", "SN", "CM"], "region": "Afrika",
     "tip": "Zöld a bal oldalon, a sárga sáv közepe üres – Szenegálnál ott zöld csillag lenne, Guineánál balra piros áll."},
    {"code": "GN", "box": (0.12, 0.25, 0.60, 0.75), "wrong": ["ML", "CM", "SN"], "region": "Afrika",
     "tip": "Piros balra, sárga jobbra, a piros sáv közepén nincs csillag – Kamerunnál a piros középső sávban sárga csillag van, Malinál fordított a sorrend."},
    {"code": "SN", "box": (0.30, 0.18, 0.76, 0.64), "wrong": ["ML", "CM", "GN"], "region": "Afrika",
     "tip": "Zöld csillag a sárga sávon – Kamerun csillaga sárga a piros sávon."},
    {"code": "CM", "box": (0.22, 0.28, 0.66, 0.72), "wrong": ["SN", "GN", "ML"], "region": "Afrika",
     "tip": "Sárga csillag a piros középső sávon, balra zöld – Szenegálnál a csillag zöld a sárgán."},
    {"code": "GH", "box": (0.25, 0.08, 0.75, 0.55), "wrong": ["GW", "ST", "TG"], "region": "Afrika",
     "tip": "Vízszintes piros sáv a sárga fölött, rajta fekete csillag – São Tomén felül zöld van, Bissau-Guineában a piros függőleges."},
    {"code": "GW", "box": (0.06, 0.10, 0.60, 0.80), "wrong": ["GH", "ST", "BJ"], "region": "Afrika",
     "tip": "Függőleges piros sáv fekete csillaggal, mellette sárga a zöld fölött – Beninnél a függőleges sáv zöld, alul piros."},
    {"code": "ST", "box": (0.38, 0.20, 0.88, 0.82), "wrong": ["GH", "GW", "TG"], "region": "Afrika",
     "tip": "Két fekete csillag a sárga sávon, felül és alul zöld – Ghánán egy csillag van, felül piros."},
    {"code": "TG", "box": (0.10, 0.06, 0.62, 0.62), "wrong": ["GH", "GW", "ST"], "region": "Afrika",
     "tip": "Piros négyzet fehér csillaggal, mellette zöld–sárga csíkok – a többi hasonmásnál a csillag fekete."},
    {"code": "BJ", "box": (0.20, 0.20, 0.70, 0.80), "wrong": ["MG", "GW", "TG"], "region": "Afrika",
     "tip": "Függőleges zöld sáv, mellette sárga a piros fölött – Madagaszkárnál fehér a függőleges sáv, és piros van felül."},
    {"code": "CI", "box": (0.12, 0.20, 0.60, 0.80), "wrong": ["IE", "NE", "IN"], "region": "Afrika",
     "tip": "Narancs balra, fehér jobbra – Írországnál a narancs a jobb oldalon van."},
    {"code": "NE", "box": (0.10, 0.00, 0.60, 0.56), "wrong": ["IN", "CI", "IE"], "region": "Afrika",
     "tip": "Narancs korong a fehér sávban – Indiánál ott kék kerék van."},
    {"code": "NG", "box": (0.20, 0.15, 0.80, 0.85), "wrong": ["NF", "CI", "IE"], "region": "Afrika",
     "tip": "Zöld–fehér–zöld, a fehér sáv üres – a Norfolk-szigeteknél ott fenyő áll."},
    {"code": "CG", "box": (0.20, 0.15, 0.78, 0.85), "wrong": ["CD", "TZ", "NA"], "region": "Afrika",
     "tip": "Sárga átló zöld és piros között, szegély nélkül – Tanzániánál és a KDK-nál szegélyezett sáv fut."},
    {"code": "CD", "box": (0.38, 0.20, 0.88, 0.80), "wrong": ["CG", "TZ", "NA"], "region": "Afrika",
     "tip": "Sárga szegélyű piros átló világoskék mezőn – Namíbiánál a szegély fehér."},
    {"code": "TZ", "box": (0.28, 0.22, 0.76, 0.78), "wrong": ["CD", "NA", "TT"], "region": "Afrika",
     "tip": "Sárga szegélyű fekete átló zöld és kék között – Trinidad és Tobagónál fehér szegélyű fekete sáv fut pirosban."},
    {"code": "NA", "box": (0.30, 0.30, 0.82, 0.88), "wrong": ["TZ", "CD", "TT"], "region": "Afrika",
     "tip": "Fehér szegélyű piros átló kék és zöld között – Tanzániánál sárga szegélyű fekete."},
    {"code": "ET", "box": (0.00, 0.04, 0.52, 0.62), "wrong": ["GH", "LT", "BO"], "region": "Afrika",
     "tip": "Zöld felül, sárga középen és a kék korong széle – Litvániánál sárga van felül."},
    {"code": "GA", "box": (0.20, 0.12, 0.80, 0.88), "wrong": ["SL", "RW", "ET"], "region": "Afrika",
     "tip": "Zöld–sárga–kék fentről lefelé – Sierra Leonénál a középső sáv fehér, Ruandánál fordított a sorrend."},
    {"code": "SL", "box": (0.20, 0.12, 0.80, 0.88), "wrong": ["GA", "RW", "ET"], "region": "Afrika",
     "tip": "Zöld–fehér–kék – Gabonnál a középső sáv sárga."},
    {"code": "RW", "box": (0.08, 0.30, 0.60, 0.96), "wrong": ["GA", "SL", "LT"], "region": "Afrika",
     "tip": "Kék felül, alatta keskeny sárga, alul zöld – Litvániánál nincs kék, Gabonnál a kék alul van."},
    {"code": "BF", "box": (0.25, 0.22, 0.75, 0.78), "wrong": ["CM", "GH", "SN"], "region": "Afrika",
     "tip": "Vízszintes piros a zöld fölött, a határon sárga csillag – a többi hasonmás csíkjai függőlegesek vagy hármasak."},
    {"code": "MR", "box": (0.32, 0.00, 0.76, 0.56), "wrong": ["DZ", "KM", "TN"], "region": "Afrika",
     "tip": "Zöld mező, arany félhold és csillag, felül piros csík – Algériánál a félhold piros."},

    # --- Arab világ ---------------------------------------------------------
    {"code": "JO", "box": (0.00, 0.18, 0.50, 0.82), "wrong": ["PS", "EH", "SD"], "region": "Arab világ",
     "tip": "Fehér hétágú csillag a piros háromszögben – Palesztina háromszöge üres."},
    {"code": "PS", "box": (0.04, 0.20, 0.62, 0.80), "wrong": ["JO", "EH", "SD"], "region": "Arab világ",
     "tip": "Piros háromszög csillag nélkül, a fehér sáv is üres – Jordániánál csillag, Nyugat-Szaharánál piros félhold lenne."},
    {"code": "SD", "box": (0.12, 0.00, 0.60, 0.52), "wrong": ["PS", "JO", "EH"], "region": "Arab világ",
     "tip": "Zöld háromszög, felül piros sáv – a hasonmásoknál a háromszög piros, felül fekete."},
    {"code": "EH", "box": (0.28, 0.24, 0.76, 0.76), "wrong": ["PS", "JO", "SD"], "region": "Arab világ",
     "tip": "Piros félhold és csillag a fehér sáv közepén."},
    {"code": "AE", "box": (0.10, 0.00, 0.62, 0.62), "wrong": ["KW", "OM", "PS"], "region": "Arab világ",
     "tip": "Egyenes szélű függőleges piros sáv, mellette zöld a fehér fölött – Kuvaitnál fekete trapéz, Ománnál fehér a felső sáv."},
    {"code": "KW", "box": (0.04, 0.00, 0.56, 0.62), "wrong": ["AE", "PS", "JO"], "region": "Arab világ",
     "tip": "Ferde szélű fekete trapéz a rúdnál – az Emírségeknél egyenes piros sáv."},
    {"code": "OM", "box": (0.12, 0.15, 0.70, 0.85), "wrong": ["AE", "KW", "BH"], "region": "Arab világ",
     "tip": "Piros függőleges sáv, mellette fehér–piros–zöld – az Emírségeknél zöld–fehér–fekete."},
    {"code": "EG", "box": (0.25, 0.18, 0.75, 0.68), "wrong": ["IQ", "YE", "SD"], "region": "Arab világ",
     "tip": "Arany sas a fehér sávban – Iraknál zöld írás, Jemennél üres."},
    {"code": "IQ", "box": (0.30, 0.18, 0.86, 0.68), "wrong": ["EG", "YE", "SA"], "region": "Arab világ",
     "tip": "Zöld kúfi írás a fehér sávban – Szaúd-Arábiánál fehér írás zöld mezőn."},
    {"code": "QA", "box": (0.14, 0.08, 0.60, 0.62), "wrong": ["BH", "OM", "AE"], "region": "Arab világ",
     "tip": "Fűrészfogas fehér szél gesztenyebarna mezőn – Bahrein élénkpiros, és csak öt foga van."},
    {"code": "BH", "box": (0.10, 0.08, 0.56, 0.62), "wrong": ["QA", "OM", "TN"], "region": "Arab világ",
     "tip": "Széles fogak élénkpiros mezőn – Katar sötét gesztenyebarna, sűrűbb fogakkal."},
    {"code": "DZ", "box": (0.30, 0.18, 0.76, 0.82), "wrong": ["TN", "TR", "MR"], "region": "Arab világ",
     "tip": "Piros félhold a zöld–fehér határon – Tunéziánál fehér korongban, piros mezőn."},
    {"code": "TN", "box": (0.30, 0.22, 0.76, 0.78), "wrong": ["TR", "DZ", "MA"], "region": "Arab világ",
     "tip": "Fehér korong, benne piros félhold – Törökországnál a félhold maga fehér."},
    {"code": "MA", "box": (0.25, 0.18, 0.72, 0.66), "wrong": ["TN", "DZ", "TR"], "region": "Arab világ",
     "tip": "Zöld körvonalas ötágú csillag piros mezőn."},
    {"code": "SA", "box": (0.15, 0.55, 0.78, 0.96), "wrong": ["IQ", "DZ", "MR"], "region": "Arab világ",
     "tip": "Fehér kard zöld mezőn."},
    {"code": "LY", "box": (0.28, 0.12, 0.76, 0.82), "wrong": ["TR", "TN", "DZ"], "region": "Arab világ",
     "tip": "Fehér félhold és csillag fekete sávban, felül piros."},

    # --- Óceánia (ritkák) ---------------------------------------------------
    {"code": "TV", "box": (0.55, 0.30, 0.97, 0.97), "wrong": ["FJ", "CK", "NU"], "region": "Óceánia",
     "tip": "Sárga csillagok világoskék mezőn – a Cook-szigetek csillagai fehérek, sötétkéken."},
    {"code": "FJ", "box": (0.55, 0.00, 0.98, 0.60), "wrong": ["TV", "CK", "NU"], "region": "Óceánia",
     "tip": "Címerpajzs teteje világoskék mezőn – Tuvalunál csillagok lennének."},
    {"code": "CK", "box": (0.55, 0.05, 0.97, 0.62), "wrong": ["FM", "TV", "NR"], "region": "Óceánia",
     "tip": "Fehér csillagok körben, sötétkék mezőn – Mikronéziánál világoskék a mező."},
    {"code": "FM", "box": (0.22, 0.05, 0.76, 0.62), "wrong": ["SO", "CK", "TV"], "region": "Óceánia",
     "tip": "Több kisebb fehér csillag világoskéken – Szomáliánál egyetlen nagy csillag van."},
    {"code": "NU", "box": (0.10, 0.00, 0.66, 0.66), "wrong": ["TV", "CK", "FJ"], "region": "Óceánia",
     "tip": "Sárga csillagok a Union Jackben és sárga mező – egyedül Niue ilyen."},
    {"code": "NR", "box": (0.00, 0.30, 0.52, 0.88), "wrong": ["MH", "FM", "SB"], "region": "Óceánia",
     "tip": "Keskeny sárga vízszintes csík, alatta fehér tizenkétágú csillag sötétkéken."},
    {"code": "MH", "box": (0.20, 0.35, 0.82, 0.92), "wrong": ["NR", "SB", "FM"], "region": "Óceánia",
     "tip": "Narancs és fehér, szélesedő átlós sugár kéken."},
    {"code": "SB", "box": (0.30, 0.25, 0.82, 0.82), "wrong": ["TZ", "MH", "CG"], "region": "Óceánia",
     "tip": "Keskeny sárga átló, felette kék, alatta zöld – Tanzániánál a sárga egy fekete sávot szegélyez."},
    {"code": "PW", "box": (0.15, 0.20, 0.60, 0.78), "wrong": ["BD", "JP", "LA"], "region": "Óceánia",
     "tip": "Sárga korong világoskék mezőn, kissé a rúd felé tolva."},
    {"code": "KI", "box": (0.00, 0.42, 0.60, 1.00), "wrong": ["PF", "TK", "TV"], "region": "Óceánia",
     "tip": "Kék–fehér hullámok, felettük a lemenő nap sugarai."},
    {"code": "PF", "box": (0.30, 0.18, 0.76, 0.82), "wrong": ["KI", "TK", "WF"], "region": "Óceánia",
     "tip": "Piros–fehér–piros sávok, középen a kenus, napos jelvény széle."},
    {"code": "TK", "box": (0.20, 0.20, 0.78, 0.88), "wrong": ["KI", "PF", "FM"], "region": "Óceánia",
     "tip": "Sárga kenu vitorlája sötétkék mezőn, fehér csillagokkal."},
    {"code": "WF", "box": (0.55, 0.30, 0.96, 0.86), "wrong": ["TO", "CH", "GE"], "region": "Óceánia",
     "tip": "Fehér négyzet piros X-szel, piros mezőn."},
    {"code": "TO", "box": (0.00, 0.00, 0.52, 0.62), "wrong": ["GE", "CH", "WF"], "region": "Óceánia",
     "tip": "Fehér négyzet piros kereszttel, körülötte piros mező – Grúziánál a mező fehér."},
    {"code": "WS", "box": (0.00, 0.00, 0.60, 0.62), "wrong": ["TW", "CL", "CK"], "region": "Óceánia",
     "tip": "Kék sarok több fehér csillaggal (Dél Keresztje), piros mező – Tajvannál nap, Chilénél egy csillag."},
    {"code": "VU", "box": (0.30, 0.18, 0.88, 0.82), "wrong": ["ZA", "GY", "SB"], "region": "Óceánia",
     "tip": "Fekete szegélyű sárga sáv piros és zöld között – a Dél-afrikai Köztársaságnál fehér szegély és zöld Y."},
    {"code": "PG", "box": (0.20, 0.15, 0.78, 0.78), "wrong": ["TT", "VU", "SB"], "region": "Óceánia",
     "tip": "Fekete–piros átlós határ, fehér csillagok és a paradicsommadár részlete."},
    {"code": "NF", "box": (0.25, 0.08, 0.75, 0.92), "wrong": ["LB", "NG", "CI"], "region": "Óceánia",
     "tip": "Fenyő a fehér sávban, két oldalt zöld – Libanonnál a cédrus vízszintes piros sávok között áll."},
    {"code": "NC", "box": (0.20, 0.00, 0.78, 0.62), "wrong": ["PW", "KI", "PF"], "region": "Óceánia",
     "tip": "Kék–piros–zöld sávok és sárga korong – a kanak zászló."},
]


def _load() -> list[dict]:
    questions = []
    base = Path(__file__).parent.parent
    for item in CROPS:
        code = item["code"]
        rel = f"{CROP_SUBDIR}/{code.lower()}_nehez.png"
        if not (base / rel).exists():
            continue
        name = COUNTRY_CODE_TO_NAME[code]
        options = [name] + [COUNTRY_CODE_TO_NAME[w] for w in item["wrong"]]
        random.shuffle(options)
        questions.append({
            "question": QUESTION_HU,
            "logo_path": rel,
            "options": options,
            "correct": options.index(name),
            "explanation": f"Ez {name} zászlójának egy részlete. {item['tip']}",
            "topic": "zászlórészlet_nehéz",
            "region": item["region"],
            "_country_name": name,
        })
    return questions


ZASZLOK_RESZLETEK_NEHEZ_QUESTIONS = _load()
