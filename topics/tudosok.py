# Tudósok kérdések a quiz alkalmazáshoz
# Híres tudósok és feltalálók életműveivel

_TOPIC = 'tudósok'


def _q(question, correct, options, explanation, topic=_TOPIC):
    """Segédfüggvény: kompakt kérdés létrehozása."""
    return {"question": question, "options": options, "correct": correct, "explanation": explanation, "topic": topic}


TUDOSOK_QUESTIONS = [
    _q('Ki alapította a Vöröskeresztet?', 1, ['Albert Schweitzer', 'Jean-Henri Dunant', 'Kármán Tódor', 'Jedlik Ányos'], 'Jean-Henri Dunant alapította a Vöröskeresztet.'),
    _q('Melyik magyar tudós volt bencés szerzetes?', 2, ['Kármán Tódor', 'Csonka János', 'Jedlik Ányos', 'Bolyai János'], 'Jedlik Ányos bencés szerzetes volt.'),
    _q('Ki dolgozta ki a Cauchy-eloszlást?', 3, ['Gauss', 'Euler', 'Newton', 'Cauchy'], 'Augustin-Louis Cauchy francia matematikus dolgozta ki.'),
    _q('Ki oldotta meg a königsbergi hidak problémáját?', 2, ['Newton', 'Leibniz', 'Euler', 'Gauss'], 'Leonhard Euler oldotta meg, megalapítva a gráfelméletet.'),
    _q('Ki volt Konrad Lorenz?', 0, ['Etológus', 'Fizikus', 'Kémikus', 'Matematikus'], 'Konrad Lorenz osztrák etológus (állatviselkedés-kutató) volt.'),
    _q('Kármán Tódor melyik tudományterületen alkotott?', 3, ['Biológia', 'Kémia', 'Geológia', 'Aerodinamika'], 'Kármán Tódor magyar származású aerodinamikus volt.'),
    _q('Ki volt Albert Schweitzer?', 2, ['Fizikus', 'Kémikus', 'Orvos és filozófus', 'Matematikus'], 'Albert Schweitzer német-francia orvos és filozófus volt.'),
    _q('Csonka János mivel foglalkozott?', 3, ['Csillagászat', 'Botanika', 'Geológia', 'Gépészet'], 'Csonka János magyar gépészmérnök és feltaláló volt.'),
    _q('Mi a fotoszintézis lényege?', 3, ['Oxigén felhasználás', 'Fehérje termelés', 'Zsír égetés', 'Szénhidrátkészítés'], 'A fotoszintézis során a növények szénhidrátot készítenek fényenergiából.'),
    _q('Mi a ganglion az orvostudományban?', 2, ['Izom', 'Csont', 'Idegdúc', 'Véredény'], 'A ganglion idegdúc, idegsejtek csoportosulása.'),
    _q('Ki volt Bakunyin Mihail?', 0, ['Orosz anarchista író', 'Szovjet politikus', 'Orosz költő', 'Szovjet tudós'], 'Bakunyin Mihail (1814-1876) orosz anarchista író és filozófus volt.'),
    _q('Ki volt Bondarcsuk Szergej?', 0, ['Szovjet rendező', 'Orosz író', 'Szovjet színész', 'Orosz zeneszerző'], 'Bondarcsuk Szergej (1920-1994) szovjet filmrendező és színész volt.'),
    _q('Ki tervezte Dzsószer fáraó piramisát?', 0, ['Imhotep', 'Hemiunu', 'Sznofru', 'Kheopsz'], 'Dzsószer fáraó piramisát Imhotep tervezte. Imhotep (kb. 2650-2600 Kr.e.) ókori egyiptomi építész, orvos, írnok és tanácsadó volt, aki a világ első kőpiramisát, a lépcsős piramist tervezte Szakkarában. Később istenként is tisztelték.'),
    _q('Miért kapott Nobel-díjat Lénárd Fülöp?', 0, ['A katódsugarak vizsgálatáért', 'A holográfia feltalálásáért', 'A C-vitamin azonosításáért', 'Az izotópos nyomjelzés módszeréért'], 'Lénárd Fülöp a katódsugarak vizsgálatáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Lénárd Fülöp?', 0, ['Fizika', 'Kémia', 'Orvostudomány/élettan', 'Irodalom'], 'Lénárd Fülöp fizikai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Bárány Róbert?', 0, ['A belső fül és az egyensúlyérzék kutatásáért', 'A karbokationok vizsgálatáért', 'A játékelmélet kidolgozásáért', 'Az attoszekundumos fényimpulzusokért'], 'Bárány Róbert a belső fül és az egyensúlyérzék kutatásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Bárány Róbert?', 0, ['Orvostudomány/élettan', 'Fizika', 'Kémia', 'Irodalom'], 'Bárány Róbert orvostudományi Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Zsigmondy Richárd?', 0, ['A kolloidok vizsgálatáért és az ultramikroszkópért', 'A holográfia feltalálásáért', 'A hallás mechanizmusának leírásáért', 'Az mRNS-technológia fejlesztéséért'], 'Zsigmondy Richárd a kolloidok vizsgálatáért és az ultramikroszkóp fejlesztéséért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Zsigmondy Richárd?', 0, ['Kémia', 'Fizika', 'Orvostudomány/élettan', 'Irodalom'], 'Zsigmondy Richárd kémiai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Szent-Györgyi Albert?', 0, ['A C-vitamin azonosításáért és a biológiai oxidáció vizsgálatáért', 'Az attoszekundumos fényimpulzusokért', 'A játékelmélet kidolgozásáért', 'A kolloidok vizsgálatáért'], 'Szent-Györgyi Albert a C-vitamin azonosításáért és a biológiai oxidációs folyamatok kutatásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Szent-Györgyi Albert?', 0, ['Orvostudomány/élettan', 'Fizika', 'Kémia', 'Irodalom'], 'Szent-Györgyi Albert orvostudományi Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Hevesy György?', 0, ['Az izotópos nyomjelzés módszeréért', 'A holográfia feltalálásáért', 'Az egyensúlyérzék kutatásáért', 'A Sorstalanság megírásáért'], 'Hevesy György az izotópos nyomjelzés módszeréért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Hevesy György?', 0, ['Kémia', 'Fizika', 'Orvostudomány/élettan', 'Irodalom'], 'Hevesy György kémiai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Békésy György?', 0, ['A hallás mechanizmusának és a csiga működésének vizsgálatáért', 'A karbokationok kutatásáért', 'A kolloidok vizsgálatáért', 'Az mRNS-technológia fejlesztéséért'], 'Békésy György a hallás mechanizmusának vizsgálatáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Békésy György?', 0, ['Orvostudomány/élettan', 'Fizika', 'Kémia', 'Irodalom'], 'Békésy György orvostudományi Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Wigner Jenő?', 0, ['Az atommag és az elemi részecskék elméletéért, szimmetriaelvekért', 'A C-vitamin azonosításáért', 'A játékelmélet kidolgozásáért', 'A holográfia feltalálásáért'], 'Wigner Jenő az atommag és az elemi részecskék elméletéhez adott alapvető hozzájárulásaiért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Wigner Jenő?', 0, ['Fizika', 'Kémia', 'Orvostudomány/élettan', 'Irodalom'], 'Wigner Jenő fizikai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Gábor Dénes?', 0, ['A holográfia feltalálásáért', 'A kolloidok vizsgálatáért', 'Az mRNS-technológia fejlesztéséért', 'Az attoszekundumos fényimpulzusokért'], 'Gábor Dénes a holográfia feltalálásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Gábor Dénes?', 0, ['Fizika', 'Kémia', 'Orvostudomány/élettan', 'Irodalom'], 'Gábor Dénes fizikai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Polányi János?', 0, ['A kémiai elemi reakciók dinamikájának kutatásáért', 'A karbokationok vizsgálatáért', 'A C-vitamin azonosításáért', 'A játékelmélet kidolgozásáért'], 'Polányi János a kémiai reakciók dinamikájának kutatásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Polányi János?', 0, ['Kémia', 'Fizika', 'Orvostudomány/élettan', 'Irodalom'], 'Polányi János kémiai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Harsányi János?', 0, ['A hiányos információjú játékelmélet kidolgozásáért', 'A holográfia feltalálásáért', 'Az attoszekundumos fényimpulzusokért', 'A kolloidok vizsgálatáért'], 'Harsányi János a hiányos információjú játékelmélet kidolgozásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Harsányi János?', 0, ['Közgazdaságtan', 'Fizika', 'Kémia', 'Irodalom'], 'Harsányi János közgazdasági Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Oláh György?', 0, ['A karbokationok és szupererős savak kutatásáért', 'A játékelmélet kidolgozásáért', 'A C-vitamin azonosításáért', 'Az egyensúlyérzék vizsgálatáért'], 'Oláh György a karbokationok kémiájának kutatásáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Oláh György?', 0, ['Kémia', 'Fizika', 'Orvostudomány/élettan', 'Irodalom'], 'Oláh György kémiai Nobel-díjat kapott.'),
    _q('Melyik művéért kapott Nobel-díjat Kertész Imre?', 0, ['Sorstalanság', 'Egri csillagok', 'Az ember tragédiája', 'A Pál utcai fiúk'], 'Kertész Imre a Sorstalanság című regényéért kapott irodalmi Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Kertész Imre?', 0, ['Irodalom', 'Fizika', 'Kémia', 'Orvostudomány/élettan'], 'Kertész Imre irodalmi Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Herskó Ferenc?', 0, ['Az ubikvitin-mediált fehérjelebontás felfedezéséért', 'A holográfia feltalálásáért', 'A C-vitamin azonosításáért', 'A játékelmélet kidolgozásáért'], 'Herskó Ferenc az ubikvitin-mediált fehérjelebontás felfedezéséért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Herskó Ferenc?', 0, ['Kémia', 'Fizika', 'Orvostudomány/élettan', 'Irodalom'], 'Herskó Ferenc kémiai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Krausz Ferenc?', 0, ['Az attoszekundumos fényimpulzusok előállításáért és méréséért', 'A kolloidok vizsgálatáért', 'A karbokationok kutatásáért', 'A C-vitamin azonosításáért'], 'Krausz Ferenc az attoszekundumos fényimpulzusokkal kapcsolatos munkájáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Krausz Ferenc?', 0, ['Fizika', 'Kémia', 'Orvostudomány/élettan', 'Irodalom'], 'Krausz Ferenc fizikai Nobel-díjat kapott.'),
    _q('Miért kapott Nobel-díjat Karikó Katalin?', 0, ['A nukleozid-módosított mRNS technológiáért', 'A holográfia feltalálásáért', 'A játékelmélet kidolgozásáért', 'Az atommag elméletéért'], 'Karikó Katalin a nukleozid-módosított mRNS technológiájáért kapott Nobel-díjat.'),
    _q('Melyik Nobel-díj kategóriában kapott díjat Karikó Katalin?', 0, ['Orvostudomány/élettan', 'Fizika', 'Kémia', 'Irodalom'], 'Karikó Katalin orvostudományi Nobel-díjat kapott.'),
]