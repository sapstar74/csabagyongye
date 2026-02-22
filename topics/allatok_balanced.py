# Kiegyensúlyozott állat kérdések a quiz alkalmazáshoz
# Különböző állatok a "Hasznos haszontalanságok" PDF-ből - EGYENSÚLYOS LISTA

_TOPIC = 'állatok'


def _q(question, correct, options, explanation, topic=_TOPIC):
    """Segédfüggvény: kompakt kérdés létrehozása."""
    return {"question": question, "options": options, "correct": correct, "explanation": explanation, "topic": topic}


ALLATOK_QUESTIONS_BALANCED = [
    _q('Mi az okapi rokonsági foka?', 0, ['Zsiráf rokona', 'Zebra rokona', 'Antilop rokona', 'Ló rokona'], 'Az okapi afrikai állat, amely a zsiráf rokona.'),
    _q('Hol él a tüskés ördög?', 3, ['Afrika', 'Ázsia', 'Dél-Amerika', 'Ausztrália'], 'A tüskés ördög egy ausztrál hüllő.'),
    _q('Mi a kacsafarkú szender?', 3, ['Madár', 'Emlős', 'Hüllő', 'Rovar lepke-szender'], 'A kacsafarkú szender egy rovar lepke-szender.'),
    _q('Milyen állat az axolotl?', 2, ['Hüllő', 'Hal', 'Kétéltű', 'Emlős'], 'Az axolotl egy kétéltű állat.'),
    _q('Mi a binturong másik neve?', 0, ['Pálmasodró cibetmacska', 'Himalájai macska', 'Erdei macska', 'Vaddisznó'], 'A binturong más néven pálmasodró cibetmacska.'),
    _q('Hol élt a tarpán?', 2, ['Afrika', 'Amerika', 'Eurázsia', 'Ausztrália'], 'A tarpán egy eurázsiai vadló volt.'),
    _q('Hol található a csillagorrú vakond?', 0, ['USA', 'Kanada', 'Mexikó', 'Grönland'], 'A csillagorrú vakond az USA-ban található.'),
    _q('Mi a quokka teljes neve?', 2, ['Rövid farkú oposszum', 'Kis válú medve', 'Kurtafarkú kenguru', 'Törpe antilop'], 'A quokka kurtafarkú kenguru.'),
    _q('Hol él a takin?', 3, ['Alpok', 'Andok', 'Kaukázus', 'Himalája'], 'A takin egy himalájai antilop.'),
    _q('Hol található az ocelot?', 3, ['Észak-Amerika', 'Afrika', 'Ázsia', 'Dél-Amerika'], 'Az ocelot Dél-Amerikában található.'),
    _q('Mi a fossa másik neve?', 0, ['Madagaszkári macska', 'Afrikai macska', 'Ázsiai macska', 'Európai macska'], 'A fossa Madagaszkár legnagyobb ragadozója, a macskafélék rokona.'),
    _q('Hol él a fossa?', 1, ['Afrika', 'Madagaszkár', 'Ázsia', 'Ausztrália'], 'A fossa Madagaszkáron él, a sziget legnagyobb ragadozója.'),
    _q('Hol él a saiga?', 0, ['Mongólia', 'Kína', 'Kazahsztán', 'Oroszország'], 'A saiga egy mongol antilop, a sivatagi területeken él.'),
    _q('Mi a kakapo?', 0, ['Papagáj', 'Kakadu', 'Ara', 'Lóri'], 'A kakapo egy papagájfaj, Új-Zéland endemikus madara.'),
    _q('Milyen állat a gila gyík?', 1, ['Kígyó', 'Gyík', 'Teknős', 'Krokodil'], 'A gila gyík egy mérgező gyíkfaj.'),
    _q('Mi a tardigrad?', 1, ['Rovar', 'Csillagállat', 'Tengeri állat', 'Férgecske'], 'A tardigrad egy csillagállat, rendkívül ellenálló mikroorganizmus.'),
    _q('Hol él a jerboa?', 0, ['Sivatagban', 'Erdőben', 'Hegyekben', 'Tengerparton'], 'A jerboa egy sivatagi rágcsáló, hosszú ugrólábakkal.'),
    _q('Mi a hoatzin?', 0, ['Dél-amerikai madár', 'Afrikai madár', 'Ázsiai madár', 'Európai madár'], 'A hoatzin egy dél-amerikai madár, egyedi megjelenéssel.'),
    _q('Mi a pangolin?', 0, ['Pikkelyes hangyász', 'Tüskés hangyász', 'Páncélos hangyász', 'Sima hangyász'], 'A pangolin egy pikkelyes hangyász, a pikkelyek védik.'),
    _q('Hol él a keelut?', 0, ['Délkelet-Ázsia', 'Észak-Ázsia', 'Nyugat-Ázsia', 'Közép-Ázsia'], 'A keelut egy délkelet-ázsiai kutya fajta.'),
    _q('Mi a takahe?', 0, ['Új-zélandi madár', 'Ausztrál madár', 'Fidzsi madár', 'Salamon madár'], 'A takahe egy új-zélandi madár, ritka faj.'),
    _q('Mi a tuatara?', 0, ['Új-zélandi hüllő', 'Ausztrál hüllő', 'Fidzsi hüllő', 'Salamon hüllő'], 'A tuatara egy új-zélandi hüllő, ősi faj.'),
    _q('Mi a solifuage?', 0, ['Pók', 'Skorpió', 'Atka', 'Rovar'], 'A solifuage egy pókfaj, a sivatagi területeken él.'),
    _q('Mi a colugo?', 0, ['Repülőmókus', 'Repülőnyúl', 'Repülőmacska', 'Repülőkutya'], 'A colugo egy repülőmókus, siklórepüléssel mozog.'),
    _q('Mi a weta?', 0, ['Új-zélandi rovar', 'Ausztrál rovar', 'Fidzsi rovar', 'Salamon rovar'], 'A weta egy új-zélandi rovar, nagy méretű.'),
    _q('Mi a markhor?', 0, ['Vadkecske', 'Vadjuh', 'Vadkutya', 'Vadmacska'], 'A markhor egy vadkecske, csavart szarvakkal.'),
    _q('Mi a zyzzyx?', 0, ['Tengeri csiga', 'Földi csiga', 'Édesvízi csiga', 'Szárazföldi csiga'], 'A zyzzyx egy tengeri csiga, az alfabetikus sorrendben az utolsó.'),
    _q('Melyik állat nem emlős?', 3, ['Okapi', 'Quokka', 'Takin', 'Kakapo'], 'A kakapo egy madár, a többi emlős.'),
    _q('Melyik állat nem hüllő?', 3, ['Tüskés ördög', 'Gila gyík', 'Tuatara', 'Tardigrad'], 'A tardigrad egy csillagállat, a többi hüllő.'),
    _q('Melyik állat nem madár?', 3, ['Kakapo', 'Takahe', 'Hoatzin', 'Jerboa'], 'A jerboa egy rágcsáló, a többi madár.'),
    _q('Melyik állat nem rovar?', 2, ['Kacsafarkú szender', 'Weta', 'Tardigrad', 'Solifuage'], 'A tardigrad egy csillagállat, a többi rovar.'),
    _q('Melyik állat nem kétéltű?', 3, ['Axolotl', 'Békák', 'Gőte', 'Tardigrad'], 'A tardigrad egy csillagállat, a többi kétéltű.'),
    _q('Melyik állat nem Ausztráliában él?', 2, ['Tüskés ördög', 'Quokka', 'Takin', 'Weta'], 'A takin a Himalájában él, a többi Ausztráliában.'),
    _q('Melyik állat nem Madagaszkáron él?', 2, ['Fossa', 'Lemúrok', 'Takin', 'Madagaszkári madarak'], 'A takin a Himalájában él, a többi Madagaszkáron.'),
    _q('Melyik állat nem Új-Zélandon él?', 3, ['Takahe', 'Tuatara', 'Weta', 'Takin'], 'A takin a Himalájában él, a többi Új-Zélandon.'),
    _q('Melyik állat nem Dél-Amerikában él?', 2, ['Ocelot', 'Hoatzin', 'Takin', 'Axolotl'], 'A takin a Himalájában él, a többi Dél-Amerikában.'),
    _q('Melyik állat nem Afrikában él?', 2, ['Okapi', 'Tüskés ördög', 'Takin', 'Fossa'], 'A takin a Himalájában él, a többi Afrikában.'),
    _q('Melyik állat nem ragadozó?', 2, ['Fossa', 'Ocelot', 'Takin', 'Markhor'], 'A takin növényevő antilop, a többi ragadozó.'),
    _q('Melyik állat nem növényevő?', 3, ['Okapi', 'Takin', 'Quokka', 'Fossa'], 'A fossa ragadozó, a többi növényevő.'),
    _q('Melyik állat nem magányos?', 2, ['Fossa', 'Ocelot', 'Takin', 'Jerboa'], 'A takin csordában él, a többi magányos.'),
    _q('Melyik állat nem éjszakai?', 3, ['Fossa', 'Ocelot', 'Jerboa', 'Takin'], 'A takin nappali aktív, a többi éjszakai.'),
    _q('Melyik állat nem veszélyeztetett?', 3, ['Kakapo', 'Takahe', 'Tuatara', 'Tardigrad'], 'A tardigrad nem veszélyeztetett, a többi igen.'),
    _q('Mi a zorilla másik neve?', 0, ['Csíkos görény', 'Fekete görény', 'Európai görény', 'Amerikai görény'], 'A zorilla más néven csíkos görény, Afrikában élő ragadozó.'),
    _q('Mi a burunduk?', 0, ['Sibériai csíkos mókus', 'Kínai mókus', 'Japán mókus', 'Mongol mókus'], 'A burunduk egy sibériai csíkos mókus, amely a tűlevelű erdőkben él és a föld alatt is mozog.'),
]