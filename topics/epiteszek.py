# 20. századi építészek – magyar és nemzetközi, 1900-tól
#
# A képek a Wikimedia Commonsról jönnek (szabad licenc), közvetlenül a
# böngészőbe töltve – a repóba nem kerülnek. Minden képnél ott a szerző
# és a licenc (credit), valamint a fájl Commons-oldala (credit_url).

import random
from urllib.parse import quote

_TOPIC = "építészek"

INT = [
    "Frank Lloyd Wright", "Antoni Gaudí", "Walter Gropius", "Ludwig Mies van der Rohe", "Le Corbusier",
    "Jørn Utzon", "Oscar Niemeyer", "Frank Gehry", "Richard Rogers", "Erich Mendelsohn", "Alvar Aalto",
    "Adolf Loos", "Otto Wagner", "Friedensreich Hundertwasser", "Zaha Hadid", "I. M. Pei", "Norman Foster",
    "Eero Saarinen", "Breuer Marcell", "Rudolf Steiner", "Kenzo Tange", "Moshe Safdie", "William F. Lamb",
    "Renzo Piano", "Philip Johnson", "Louis Kahn", "Tadao Ando", "Rem Koolhaas",
]
HU = [
    "Lechner Ödön", "Quittner Zsigmond", "Czigler Győző", "Sebestyén Artúr", "Márkus Géza", "Magyar Ede",
    "Makovecz Imre", "Szendrői Jenő", "Kós Károly", "Lajta Béla", "Medgyaszay István", "Molnár Farkas",
    "Hültl Dezső", "Csete György", "Málnai Béla", "Hauszmann Alajos", "Pecz Samu", "Baumgarten Sándor",
]
HU_PAIRS = [
    "Komor Marcell és Jakab Dezső", "Árkay Aladár és Árkay Bertalan", "Bálint Zoltán és Jámbor Lajos",
    "Kármán Aladár és Ullmann Gyula", "Vágó László és Vágó József",
]

# Személynév → beírásnál is elfogadott alakok
ACCEPT = {
    "I. M. Pei": ["Pei", "Ieoh Ming Pei"],
    "Ludwig Mies van der Rohe": ["Mies van der Rohe", "Mies"],
    "Breuer Marcell": ["Marcel Breuer", "Breuer"],
    "Friedensreich Hundertwasser": ["Hundertwasser"],
    "William F. Lamb": ["Lamb", "Shreve, Lamb & Harmon"],
    "Komor Marcell és Jakab Dezső": ["Komor és Jakab", "Komor Marcell, Jakab Dezső"],
    "Árkay Aladár és Árkay Bertalan": ["Árkay", "Árkay Aladár és Bertalan", "Árkayak"],
}

_rng = random.Random(1900)


def _opts(answer, pool, n=3):
    others = [p for p in pool if p != answer]
    opts = [answer] + _rng.sample(others, n)
    _rng.shuffle(opts)
    return opts, opts.index(answer)


def _img(file, building, year, place, architect, pool, author, license_, note=""):
    opts, c = _opts(architect, pool)
    expl = f"{building}, {place}, {year} – tervező: {architect}."
    if note:
        expl += " " + note
    return {
        "question": f"Ki tervezte ezt az épületet? {building}, {place}, {year}",
        "options": opts,
        "correct": c,
        "explanation": expl,
        "topic": _TOPIC,
        "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/" + quote(file) + "?width=900",
        "credit": f"Fotó: {author} · {license_} · Wikimedia Commons",
        "credit_url": "https://commons.wikimedia.org/wiki/File:" + quote(file),
        "accept": ACCEPT.get(architect, []),
    }


def _txt(question, answer, pool, explanation):
    opts, c = _opts(answer, pool)
    return {"question": question, "options": opts, "correct": c, "explanation": explanation,
            "topic": _TOPIC, "accept": ACCEPT.get(answer, [])}


EPITESZEK_QUESTIONS = [
    # --- nemzetközi, képpel ------------------------------------------------
    _img("Fallingwater3.jpg", "Fallingwater (Vízesésház)", 1939, "Pennsylvania", "Frank Lloyd Wright", INT,
         "lachrimae72", "CC0", "A ház egy vízesés fölé épült, a természet és az építészet egységének jelképe."),
    _img("Solomon_R._Guggenheim_Museum_(48059131351).jpg", "Solomon R. Guggenheim Múzeum", 1959, "New York",
         "Frank Lloyd Wright", INT, "Ajay Suresh", "CC BY 2.0", "A kiállítótér egyetlen, felfelé táguló spirálrámpa."),
    _img("Casa_Milà,_general_view.jpg", "Casa Milà (La Pedrera)", 1912, "Barcelona", "Antoni Gaudí", INT,
         "Thomas Ledl", "CC BY-SA 4.0"),
    _img("Dessau_Bauhaus-Gebäude_asv2024-06_img1.jpg", "A Bauhaus dessaui épülete", 1926, "Dessau", "Walter Gropius", INT,
         "A. Savin", "FAL", "Gropius alapította a Bauhaus iskolát is."),
    _img("Vila_Tugendhat_exterior_Dvorak2.JPG", "Villa Tugendhat", 1930, "Brno", "Ludwig Mies van der Rohe", INT,
         "Petr1987", "CC BY-SA 4.0"),
    _img("Seagram_Building_(35098307116).jpg", "Seagram Building", 1958, "New York", "Ludwig Mies van der Rohe", INT,
         "Ken Ohyama", "CC BY-SA 2.0", "A belsőépítészetben Philip Johnson működött közre."),
    _img("Sydney_Australia._(21339175489).jpg", "Sydney-i Operaház", 1973, "Sydney", "Jørn Utzon", INT,
         "Bernard Spragg", "CC0"),
    _img("Catedral_Metropolitana_de_Brasilia.jpg", "Brazíliavárosi katedrális", 1970, "Brazíliaváros", "Oscar Niemeyer", INT,
         "Tissiana de A. de Souza", "CC BY-SA 4.0"),
    _img("Museo_Guggenheim,_Bilbao_(31273245344).jpg", "Guggenheim Múzeum", 1997, "Bilbao", "Frank Gehry", INT,
         "Naotake Murayama", "CC BY 2.0"),
    _img("Lloyds_building_taken_2011.jpg", "Lloyd's-székház", 1986, "London", "Richard Rogers", INT,
         "Stephen Richards", "CC BY-SA 2.0", "A gépészet és a lépcsők az épület külsejére kerültek."),
    _img("Potsdam_Telegrafenberg_asv2023-09_img4.jpg", "Einstein-torony", 1921, "Potsdam", "Erich Mendelsohn", INT,
         "A. Savin", "FAL"),
    _img("Finlandia_Hall-7141.jpg", "Finlandia-csarnok", 1971, "Helsinki", "Alvar Aalto", INT,
         "Matthias Süßen", "CC BY-SA 3.0"),
    _img("Looshaus_Michaelerplatz.JPG", "Looshaus a Michaelerplatzon", 1911, "Bécs", "Adolf Loos", INT,
         "Thomas Ledl", "CC BY-SA 4.0", "Díszítetlen homlokzata miatt a kortársak „szemöldök nélküli háznak” csúfolták."),
    _img("P.S.K._Vienna_August_2006_030.jpg", "Osztrák Postatakarékpénztár", 1906, "Bécs", "Otto Wagner", INT,
         "Gryffindor", "CC BY 2.5"),
    _img("Wien_-_Hundertwasserhaus_(03).JPG", "Hundertwasser-ház", 1985, "Bécs", "Friedensreich Hundertwasser", INT,
         "C. Stadler/Bwag", "CC BY-SA 4.0", "A kivitelezési terveket Joseph Krawina építész készítette."),
    _img("Baden-Württemberg_Weil_am_Rhein_Vitra_Fire_station_01.jpg", "Vitra tűzoltóállomás", 1993, "Weil am Rhein",
         "Zaha Hadid", INT, "Calips", "CC BY-SA 3.0", "Hadid első megvalósult épülete."),
    _img("HK_Bank_of_China_Tower_2008_(2).jpg", "Bank of China Tower", 1990, "Hongkong", "I. M. Pei", INT,
         "WiNG", "CC BY-SA 4.0"),
    _img("Berlin_reichstag_west_panorama_2.jpg", "A Reichstag üvegkupolája (az épület 1999-es átépítése)", 1999, "Berlin",
         "Norman Foster", INT, "Matthew Field", "GFDL 1.2", "Az eredeti épületet Paul Wallot tervezte 1894-ben."),
    _img("St_Louis_night_expblend_cropped.jpg", "Gateway Arch", 1965, "St. Louis", "Eero Saarinen", INT,
         "Daniel Schwen", "CC BY-SA 3.0"),
    _img("MET_Breuer_(48377070386).jpg", "Whitney Múzeum (Breuer-épület)", 1966, "New York", "Breuer Marcell", INT,
         "Ajay Suresh", "CC BY 2.0", "Breuer Marcell Pécsen született, a Bauhausban tanult és tanított."),
    _img("Goetheanum_Dornach2.jpg", "Második Goetheanum", 1928, "Dornach", "Rudolf Steiner", INT,
         "Wladyslaw", "CC BY-SA 3.0"),
    _img("Kokuritsu_Yoyogi_Kyōgijō_1.jpg", "Yoyogi Nemzeti Sportcsarnok", 1964, "Tokió", "Kenzo Tange", INT,
         "Arne Müseler", "CC BY-SA 3.0 de", "Az 1964-es tokiói olimpiára épült."),
    _img("Habitat_67_2019_dllu_01.jpg", "Habitat 67", 1967, "Montréal", "Moshe Safdie", INT,
         "Dllu", "CC BY-SA 4.0"),
    _img("Empire_State_Building_(aerial_view).jpg", "Empire State Building", 1931, "New York", "William F. Lamb", INT,
         "Sam Valadi", "közkincs", "A Shreve, Lamb & Harmon iroda terve; a vezető tervező William F. Lamb volt."),

    # --- magyar, képpel ----------------------------------------------------
    _img("View_of_Hungarian_State_Treasury_building_(03).jpg", "Postatakarékpénztár", 1901, "Budapest", "Lechner Ödön", HU,
         "Vasyatka1", "CC BY-SA 4.0", "Ma a Magyar Államkincstár épülete."),
    _img("Gresham_Palace_-_Stierch_01.jpg", "Gresham-palota", 1906, "Budapest", "Quittner Zsigmond", HU,
         "Sarah Stierch", "CC BY 4.0", "Quittner Zsigmond tervét a Vágó fivérek közreműködésével valósították meg."),
    _img("Budapest_Széchenyi_Baths_R01.jpg", "Széchenyi gyógyfürdő", 1913, "Budapest", "Czigler Győző", HU,
         "Marc Ryckaert", "CC BY 3.0", "Czigler halála után Schmahl Henrik és Dvorák Ede fejezte be."),
    _img("Budapest_Gellértbad_1.JPG", "Gellért gyógyfürdő", 1918, "Budapest", "Sebestyén Artúr", HU,
         "Zairon", "CC BY-SA 3.0", "Sebestyén Artúr Hegedűs Ármin és Sterk Izidor társaságában tervezte."),
    _img("Cifra_Palota.jpg", "Cifrapalota", 1902, "Kecskemét", "Márkus Géza", HU,
         "Bali22", "közkincs"),
    _img("Reök_Palace.jpg", "Reök-palota", 1907, "Szeged", "Magyar Ede", HU,
         "Kalyob", "CC BY-SA 3.0"),
    _img("Hagymaház.JPG", "Hagymaház", 1998, "Makó", "Makovecz Imre", HU,
         "Burrows", "közkincs"),
    _img("Szentlélek_templom,_Makoveczpaks.jpg", "Szentlélek-templom", 1991, "Paks", "Makovecz Imre", HU,
         "Osbi", "közkincs"),
    _img("Hotel_Budapest_Korszallo_-_Exterior_(4).jpg", "Hotel Budapest (Körszálló)", 1967, "Budapest", "Szendrői Jenő", HU,
         "Illustratedjc", "CC BY-SA 4.0"),
    _img("Palatul_Culturii_(Targu_Mures).jpg", "Kultúrpalota", 1913, "Marosvásárhely", "Komor Marcell és Jakab Dezső",
         HU_PAIRS, "Rsocol", "CC BY-SA 3.0"),
    _img("Varosmajor_Church.JPG", "Városmajori Jézus Szíve-templom", 1933, "Budapest", "Árkay Aladár és Árkay Bertalan",
         HU_PAIRS, "MOs810", "CC BY-SA 4.0", "Apa és fia közös műve; Árkay Aladár halála után Bertalan fejezte be."),

    # --- szöveges kérdések ---------------------------------------------------
    _txt("Melyik építész nevéhez fűződik a „kevesebb több” (less is more) jelmondat?", "Ludwig Mies van der Rohe", INT,
         "Ludwig Mies van der Rohe, a Bauhaus utolsó igazgatója."),
    _txt("Ki alapította 1919-ben Weimarban a Bauhaus iskolát?", "Walter Gropius", INT,
         "Walter Gropius alapította; az iskola 1925-ben Dessauba, 1932-ben Berlinbe költözött."),
    _txt("Melyik építész valódi neve Charles-Édouard Jeanneret?", "Le Corbusier", INT,
         "Le Corbusier svájci születésű francia építész, a modern építészet egyik atyja."),
    _txt("Ki tervezte az indiai Chandigarh város fő középületeit és városrendezési tervét?", "Le Corbusier", INT,
         "Le Corbusier az 1950-es években dolgozott Chandigarh-on."),
    _txt("Melyik építész tervezte Brazíliaváros legfontosabb középületeit?", "Oscar Niemeyer", INT,
         "Oscar Niemeyer; a város alaprajzát Lúcio Costa készítette."),
    _txt("Ki kapta 1979-ben elsőként a Pritzker-díjat, az építészet „Nobel-díját”?", "Philip Johnson", INT,
         "Philip Johnson, a New Canaan-i Üvegház tervezője."),
    _txt("Ki volt az első nő, aki megkapta a Pritzker-díjat (2004)?", "Zaha Hadid", INT,
         "Zaha Hadid iraki születésű brit építész."),
    _txt("Melyik építészt gázolta el egy villamos Barcelonában 1926-ban?", "Antoni Gaudí", INT,
         "Gaudít ruházata miatt csavargónak nézték, és csak napokkal később azonosították."),
    _txt("Ki dolgozta ki a „Modulor” nevű, az emberi test arányain alapuló méretrendszert?", "Le Corbusier", INT,
         "Le Corbusier 1948-ban tette közzé a Modulort."),
    _txt("Melyik Pécsen született építész lett a Bauhaus tanára, majd az Egyesült Államokban dolgozott?", "Breuer Marcell",
         INT, "Breuer Marcell (Marcel Breuer) – a csővázas Vaszilij-szék is az ő terve."),
    _txt("Kit tartanak a magyaros szecessziós formanyelv megteremtőjének?", "Lechner Ödön", HU,
         "Lechner Ödön – „a magyar formanyelv” megalkotója, a Zsolnay-kerámia építészeti használatának úttörője."),
    _txt("Melyik építész nevéhez fűződik a magyar organikus építészet?", "Makovecz Imre", HU,
         "Makovecz Imre; legismertebb művei a paksi templom, a makói Hagymaház és a piliscsabai Stephaneum."),
    _txt("Melyik építész házát hívják Varjúvárnak az erdélyi Sztánán?", "Kós Károly", HU,
         "Kós Károly 1910-ben építette Sztánán saját házát, a Varjúvárat."),
    _txt("Ki tervezte a Fővárosi Állatkert madárházát és több pavilonját 1909–1912 között?", "Kós Károly", HU,
         "Kós Károly és Zrumeczky Dezső tervezte az állatkert népies stílusú épületeit."),
    _txt("Melyik Bauhausban tanult magyar építész vezette a CIAM magyar csoportját?", "Molnár Farkas", HU,
         "Molnár Farkas a magyar modernizmus egyik vezéralakja volt."),
    _txt("Ki tervezte a veszprémi Petőfi Színházat (1908), Magyarország egyik első vasbeton színházát?",
         "Medgyaszay István", HU, "Medgyaszay István a vasbeton és a népi formakincs ötvözésének úttörője."),
]
