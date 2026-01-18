import streamlit as st
import random
import re

# Ország nevek leképezése (a kérdésekből kinyert országok)
COUNTRY_MAPPING = {
    "Srí Lanka": "LK", "Guatemala": "GT", "Wales": "GB-WLS", "Uganda": "UG",
    "Kiribati": "KI", "Dominika": "DM", "Mexikó": "MX", "Peru": "PE",
    "Ausztrália": "AU", "Moldova": "MD", "Montenegró": "ME", "Albánia": "AL",
    "Bhután": "BT", "Zimbabwe": "ZW", "Zambia": "ZM", "Egyiptom": "EG",
    "Kazahsztán": "KZ", "Andorra": "AD", "Botswana": "BW", "Szerbia": "RS",
    "Málta": "MT", "Horvátország": "HR", "Fidzsi-szigetek": "FJ",
    "Kanada": "CA", "Libanon": "LB", "Grenada": "GD", "ENSZ": "UN",
    "Ciprus": "CY", "Belize": "BZ", "Haiti": "HT", "Hongkong": "HK",
    "Makaó": "MO", "Olaszország": "IT", "Eritrea": "ER", "Egyenlítői-Guinea": "GQ",
    "Mozambik": "MZ", "USA": "US", "Kenya": "KE", "Eswatini": "SZ",
    "Angola": "AO", "Írország": "IE", "Kambodzsa": "KH", "Szaúd-Arábia": "SA",
    "Omán": "OM", "Barbados": "BB", "Portugália": "PT", "Lesotho": "LS",
    "San Marino": "SM", "Afganisztán": "AF", "India": "IN", "Gibraltár": "GI",
    "Észak-Macedónia": "MK", "Nauru": "NR", "Jordánia": "JO", "Malajzia": "MY",
    "Marshall-szigetek": "MH", "Európai Unió": "EU", "Kína": "CN", "Új-Zéland": "NZ",
    "Argentína": "AR", "Uruguay": "UY", "Mongólia": "MN", "Man-sziget": "IM",
    "Nepál": "NP", "Svájc": "CH", "Marokkó": "MA", "Tunézia": "TN",
    "Törökország": "TR", "Izrael": "IL", "Dél-Korea": "KR", "Vietnam": "VN",
    "Szomália": "SO", "Koszovó": "XK", "Paraguay": "PY", "Fülöp-szigetek": "PH",
    "Brazília": "BR", "Japán": "JP", "Líbia": "LY", "Hollandia": "NL",
    "Luxemburg": "LU", "Románia": "RO", "Csád": "TD", "Ukrajna": "UA",
    "Vatikán": "VA", "Jamaica": "JM", "Guyana": "GY", "Kuba": "CU",
    "Banglades": "BD", "Finnország": "FI", "Norvégia": "NO", "Svédország": "SE",
    "Dánia": "DK", "Ausztria": "AT", "Magyarország": "HU", "Elefántcsontpart": "CI",
    "Pápua Új-Guinea": "PG",
    # Új országok
    "Németország": "DE", "Franciaország": "FR", "Spanyolország": "ES", "Görögország": "GR",
    "Lengyelország": "PL", "Csehország": "CZ", "Szlovákia": "SK", "Szlovénia": "SI",
    "Bulgária": "BG", "Fehéroroszország": "BY", "Oroszország": "RU", "Litvánia": "LT",
    "Lettország": "LV", "Észtország": "EE", "Belgium": "BE", "Monaco": "MC",
    "Liechtenstein": "LI", "Izland": "IS", "Grúzia": "GE", "Örményország": "AM",
    "Azerbajdzsán": "AZ", "Bosznia-Hercegovina": "BA", "Thaiföld": "TH", "Indonézia": "ID",
    "Szingapúr": "SG", "Mianmar": "MM", "Laosz": "LA", "Pakisztán": "PK",
    "Irán": "IR", "Irak": "IQ", "Szíria": "SY", "Jemen": "YE",
    "Egyesült Arab Emírségek": "AE", "Katar": "QA", "Bahrein": "BH", "Kuvait": "KW",
    "Üzbegisztán": "UZ", "Türkmenisztán": "TM", "Tádzsikisztán": "TJ", "Kirgizisztán": "KG",
    "Dél-afrikai Köztársaság": "ZA", "Nigéria": "NG", "Ghána": "GH", "Szenegál": "SN",
    "Mali": "ML", "Burkina Faso": "BF", "Niger": "NE", "Szudán": "SD",
    "Etiópia": "ET", "Tanzánia": "TZ", "Ruanda": "RW", "Kongói Demokratikus Köztársaság": "CD",
    "Kongói Köztársaság": "CG", "Kamerun": "CM", "Gabon": "GA", "Közép-afrikai Köztársaság": "CF",
    "Togo": "TG", "Benin": "BJ", "Sierra Leone": "SL", "Libéria": "LR",
    "Guinea": "GN", "Guinea-Bissau": "GW", "Zöld-foki Köztársaság": "CV", "Mauritánia": "MR",
    "Algéria": "DZ", "Madagaszkár": "MG", "Mauritius": "MU", "Seychelle-szigetek": "SC",
    "Comore-szigetek": "KM", "Kolumbia": "CO", "Venezuela": "VE", "Ecuador": "EC",
    "Bolívia": "BO", "Chile": "CL", "Panama": "PA", "Costa Rica": "CR",
    "Nicaragua": "NI", "Honduras": "HN", "Salvador": "SV", "Dominikai Köztársaság": "DO",
    "Trinidad és Tobago": "TT", "Bahama-szigetek": "BS", "Tonga": "TO", "Szamoa": "WS",
    "Vanuatu": "VU", "Palau": "PW", "Mikronézia": "FM", "Salamon-szigetek": "SB"
}

def extract_country_from_question(question):
    """Kinyeri az ország nevét a kérdésből"""
    for country, code in COUNTRY_MAPPING.items():
        if country in question:
            return country, code
    return None, None

def get_flag_url(country_code):
    """Visszaadja a zászló kép URL-jét"""
    if country_code == "UN":
        return "https://flagcdn.com/w320/un.png"
    elif country_code == "EU":
        return "https://flagcdn.com/w320/eu.png"
    elif country_code == "GB-WLS":
        return "https://flagcdn.com/w320/gb-wls.png"
    elif country_code == "XK":
        return "https://flagcdn.com/w320/xk.png"
    else:
        return f"https://flagcdn.com/w320/{country_code.lower()}.png"

def generate_explanation(q_data, is_correct, selected_answer):
    """Generál magyarázatot a válaszhoz"""
    country, code = extract_country_from_question(q_data["q"])
    
    if is_correct:
        explanation = f"✅ **Helyes válasz!**\n\n"
        explanation += f"A **{q_data['a']}** valóban látható "
        if country:
            explanation += f"**{country}** zászlaján. "
        explanation += f"Ez a zászló egyik jellegzetes eleme."
    else:
        explanation = f"❌ **Helytelen válasz.**\n\n"
        explanation += f"A helyes válasz: **{q_data['a']}**\n\n"
        if country:
            explanation += f"**{country}** zászlaján a **{q_data['a']}** látható, nem a választott **{selected_answer}**."
        else:
            explanation += f"A zászlón a **{q_data['a']}** látható."
    
    return explanation, country, code

# --- 1. A NAGY ADATBÁZIS (100+ Kérdés) ---
questions_db = [
    # --- ÁLLATOK ---
    {"q": "Milyen állat tart kardot Srí Lanka zászlaján?", "o": ["Oroszlán", "Tigris", "Elefánt", "Sárkány"], "a": "Oroszlán"},
    {"q": "Milyen madár látható Guatemala zászlaján?", "o": ["Quetzal", "Papagáj", "Kolibri", "Tukán"], "a": "Quetzal"},
    {"q": "Milyen mitikus lény szerepel Wales zászlaján?", "o": ["Vörös sárkány", "Griff", "Főnix", "Egyszarvú"], "a": "Vörös sárkány"},
    {"q": "Milyen állat látható Uganda zászlajának közepén?", "o": ["Koronás daru", "Flamingó", "Strucc", "Páva"], "a": "Koronás daru"},
    {"q": "Milyen állat szerepel Kiribati zászlaján a felkelő nap felett?", "o": ["Fregattmadár", "Sirály", "Albatrosz", "Sas"], "a": "Fregattmadár"},
    {"q": "Milyen állat látható Dominika zászlajának közepén?", "o": ["Sisserou papagáj", "Tukán", "Ara papagáj", "Zöld küllő"], "a": "Sisserou papagáj"},
    {"q": "Milyen állat látható Mexikó címerében a zászló közepén?", "o": ["Sas", "Sólyom", "Keselyű", "Kondor"], "a": "Sas"},
    {"q": "Mit eszik a sas Mexikó zászlaján?", "o": ["Kígyót", "Halat", "Egeret", "Kaktuszt"], "a": "Kígyót"},
    {"q": "Milyen állat található Pápua Új-Guinea zászlaján?", "o": ["Paradicsommadár", "Kivi", "Kazuár", "Kakadu"], "a": "Paradicsommadár"},
    {"q": "Milyen állat látható Peru állami zászlajának címerében?", "o": ["Vikunya", "Láma", "Alpaka", "Guanakó"], "a": "Vikunya"},
    {"q": "Milyen két állat tartja a címert Ausztrália (nem hivatalos) címeres ábrázolásain?", "o": ["Kenguru és Emu", "Koala és Kenguru", "Dingo és Emu", "Krokodil és Kenguru"], "a": "Kenguru és Emu"},
    {"q": "Milyen állat szerepel Moldova zászlajának közepén?", "o": ["Sas", "Oroszlán", "Medve", "Bölény"], "a": "Sas"},
    {"q": "Milyen állat látható Montenegró zászlaján?", "o": ["Kétfejű sas", "Arany oroszlán", "Fekete párduc", "Fehér ló"], "a": "Kétfejű sas"},
    {"q": "Milyen állat van Albánia zászlaján?", "o": ["Fekete kétfejű sas", "Vörös oroszlán", "Fekete farkas", "Arany sólyom"], "a": "Fekete kétfejű sas"},
    {"q": "Milyen állat látható Bhután zászlaján?", "o": ["Sárkány", "Tigris", "Hópárduc", "Jak"], "a": "Sárkány"},
    {"q": "Milyen állatot ábrázol Zimbabwe zászlajának madara (szobor)?", "o": ["Zimbabwei madár", "Sas", "Héja", "Gólya"], "a": "Zimbabwei madár"},
    {"q": "Milyen állat látható Zambia zászlajának jobb sarkában?", "o": ["Lármás rétisas", "Héja", "Keselyű", "Sólyom"], "a": "Lármás rétisas"},
    {"q": "Milyen állat szerepel Egyiptom zászlaján?", "o": ["Szalah-ad-Dín sasa", "Szfinx", "Kobra", "Teve"], "a": "Szalah-ad-Dín sasa"},
    {"q": "Milyen állat van Kazahsztán zászlaján a nap alatt?", "o": ["Sztyeppei sas", "Sólyom", "Hópárduc", "Ló"], "a": "Sztyeppei sas"},
    {"q": "Milyen állat látható Andorra zászlajának címerében (a katalán negyedben)?", "o": ["Két tehén", "Egy ló", "Egy kecske", "Egy juh"], "a": "Két tehén"},
    {"q": "Milyen állat tartja a címert Botswana címerében (nem mindig a zászlón, de kapcsolódó)?", "o": ["Zebrák", "Elefántok", "Oroszlánok", "Zsiráfok"], "a": "Zebrák"},
    {"q": "Milyen állat látható Szerbia zászlaján?", "o": ["Fehér kétfejű sas", "Fekete sas", "Arany oroszlán", "Medve"], "a": "Fehér kétfejű sas"},
    {"q": "Milyen mitikus állat szerepel Málta címerében (a György-kereszt mellett néha ábrázolva)?", "o": ["Sárkány (Szent György)", "Griff", "Egyszarvú", "Hydra"], "a": "Sárkány (Szent György)"},
    {"q": "Milyen állat van Horvátország címerének egyik kis pajzsán?", "o": ["Nyest és Kecske", "Farkas és Medve", "Oroszlán és Sas", "Róka és Nyúl"], "a": "Nyest és Kecske"},
    {"q": "Milyen állat található a Fidzsi-szigetek zászlajának címerében?", "o": ["Oroszlán és Galamb", "Cápa és Teknős", "Papagáj és Hal", "Krokodil"], "a": "Oroszlán és Galamb"},
    
    # --- NÖVÉNYEK ---
    {"q": "Milyen növény levele van Kanada zászlaján?", "o": ["Juhar", "Tölgy", "Nyír", "Fenyő"], "a": "Juhar"},
    {"q": "Milyen fa látható Libanon zászlaján?", "o": ["Cédrus", "Olajfa", "Pálma", "Fenyő"], "a": "Cédrus"},
    {"q": "Milyen fűszertermés látható Grenada zászlaján?", "o": ["Szerecsendió", "Fahéj", "Kakaó", "Vanília"], "a": "Szerecsendió"},
    {"q": "Milyen növény koszorúja öleli körül az ENSZ zászlaját?", "o": ["Olajág", "Babér", "Búza", "Tölgy"], "a": "Olajág"},
    {"q": "Milyen növény látható Ciprus zászlaján a térkép alatt?", "o": ["Olajág", "Babér", "Szőlő", "Pálmaág"], "a": "Olajág"},
    {"q": "Milyen fa szerepel Belize zászlajának címerében?", "o": ["Mahagónifa", "Pálmafa", "Banyánfa", "Kaucsukfa"], "a": "Mahagónifa"},
    {"q": "Milyen növény szerepel a Fidzsi-szigetek zászlajának címerében?", "o": ["Cukornád és Banán", "Kókusz és Ananász", "Kávé és Tea", "Rizs és Búza"], "a": "Cukornád és Banán"},
    {"q": "Milyen fa látható Haiti zászlajának címerében?", "o": ["Királypálma", "Kókuszpálma", "Banánfa", "Mangófa"], "a": "Királypálma"},
    {"q": "Milyen virág látható Hongkong zászlaján?", "o": ["Bauhinia (Orchidea fa)", "Lótusz", "Rózsa", "Cseresznyevirág"], "a": "Bauhinia (Orchidea fa)"},
    {"q": "Milyen növény szerepel Makaó zászlaján?", "o": ["Lótusz", "Jázmin", "Liliom", "Orchidea"], "a": "Lótusz"},
    {"q": "Milyen növények ölelik körül a címert Olaszország tengerészeti zászlaján?", "o": ["Babér és Tölgy", "Olaj és Szőlő", "Búza és Kukorica", "Rózsa és Liliom"], "a": "Babér és Tölgy"},
    {"q": "Milyen növény látható Eritrea zászlajának emblémájában?", "o": ["Olajág koszorú", "Pálmaág", "Akácia", "Baobab"], "a": "Olajág koszorú"},
    {"q": "Milyen fa szerepel Egyenlítői-Guinea zászlaján?", "o": ["Selyemgyapotfa", "Majomkenyérfa", "Ébenfa", "Mahagóni"], "a": "Selyemgyapotfa"},
    
    # --- TÁRGYAK ÉS FEGYVEREK ---
    {"q": "Milyen modern fegyver látható Mozambik zászlaján?", "o": ["AK-47 gépkarabély", "M16 puska", "RPG", "Pisztoly"], "a": "AK-47 gépkarabély"},
    {"q": "Milyen szerszám látható Mozambik zászlaján a puska mellett?", "o": ["Kapa", "Sarló", "Kalapács", "Ásó"], "a": "Kapa"},
    {"q": "Milyen tárgyat tart a sas az USA címerében a nyilak mellett?", "o": ["Olajágat", "Kardot", "Mérleget", "Könyvet"], "a": "Olajágat"},
    {"q": "Milyen fegyverek vannak Kenya zászlaján?", "o": ["Két lándzsa és egy maszáj pajzs", "Kard és pajzs", "Íj és nyíl", "Puska és bajonett"], "a": "Két lándzsa és egy maszáj pajzs"},
    {"q": "Milyen fegyverek vannak Eswatini (Szváziföld) zászlaján?", "o": ["Lándzsák és pajzs", "Kardok", "Buzogány", "Fejsze"], "a": "Lándzsák és pajzs"},
    {"q": "Milyen tárgy látható Angola zászlaján a csillag mellett?", "o": ["Bozótvágó kés és fogaskerék", "Sarló és kalapács", "Puska", "Könyv"], "a": "Bozótvágó kés és fogaskerék"},
    {"q": "Milyen hangszer látható Írország címeres zászlaján (elnöki zászló)?", "o": ["Hárfa", "Duda", "Hegedű", "Lant"], "a": "Hárfa"},
    {"q": "Milyen épület látható Kambodzsa zászlaján?", "o": ["Angkor Wat templom", "Taj Mahal", "Nagy Fal", "Királyi Palota"], "a": "Angkor Wat templom"},
    {"q": "Milyen tárgy van Szaúd-Arábia zászlaján az írás alatt?", "o": ["Kard", "Tőr", "Puska", "Íj"], "a": "Kard"},
    {"q": "Milyen tárgy van Omán zászlajának címerében?", "o": ["Kandzsár tőr és két kard", "Puska", "Lándzsa", "Íj"], "a": "Kandzsár tőr és két kard"},
    {"q": "Milyen tárgyat tartanak az emberek Belize zászlaján?", "o": ["Fejszét és evezőt/fűrészt", "Puskát", "Hálót", "Gyümölcsöt"], "a": "Fejszét és evezőt/fűrészt"},
    {"q": "Milyen tárgy látható Barbados zászlajának közepén?", "o": ["Szigony", "Horgony", "Kard", "Nyíl"], "a": "Szigony"},
    {"q": "Milyen tárgy van Portugália zászlaján a címerpajzs mögött?", "o": ["Armilláris gömb (csillagászati eszköz)", "Földgömb", "Kormánykerék", "Iránytű"], "a": "Armilláris gömb (csillagászati eszköz)"},
    {"q": "Milyen fejfedő látható Lesotho zászlaján?", "o": ["Mokorotlo (szalmakalap)", "Turbán", "Korona", "Sisak"], "a": "Mokorotlo (szalmakalap)"},
    {"q": "Milyen épület látható San Marino zászlajának címerében?", "o": ["Három torony", "Egy vár", "Egy templom", "Egy híd"], "a": "Három torony"},
    {"q": "Milyen építmény látható Afganisztán (bizonyos verzióinak) zászlaján?", "o": ["Mecset", "Palota", "Erőd", "Minaret"], "a": "Mecset"},
    {"q": "Milyen tárgy látható India zászlajának közepén?", "o": ["Ashoka Csakra (küllős kerék)", "Lótusz", "Nap", "Csillag"], "a": "Ashoka Csakra (küllős kerék)"},
    {"q": "Milyen tárgy látható Gibraltár zászlaján?", "o": ["Vár és kulcs", "Hajó", "Oroszlán", "Horgony"], "a": "Vár és kulcs"},
    {"q": "Milyen hajó látható az USA egyes történelmi zászlóin?", "o": ["Nem jellemző, inkább kígyó", "Vitorlás", "Gőzhajó", "Kenú"], "a": "Nem jellemző, inkább kígyó"},
    
    # --- CSILLAGOK, NAPOK ÉS SZIMBÓLUMOK ---
    {"q": "Hány ágú a csillag (Nap) Észak-Macedónia zászlaján?", "o": ["8", "16", "12", "10"], "a": "8"},
    {"q": "Hány ágú a csillag Nauru zászlaján?", "o": ["12", "5", "6", "10"], "a": "12"},
    {"q": "Hány ágú a csillag Jordánia zászlaján?", "o": ["7", "5", "6", "8"], "a": "7"},
    {"q": "Hány ágú a csillag Malajzia zászlaján?", "o": ["14", "12", "10", "16"], "a": "14"},
    {"q": "Hány ágú a csillag a Marshall-szigetek zászlaján?", "o": ["24", "12", "20", "50"], "a": "24"},
    {"q": "Hány csillag van az Európai Unió zászlaján?", "o": ["12", "15", "27", "28"], "a": "12"},
    {"q": "Hány csillag van Kína zászlaján?", "o": ["5", "1", "4", "6"], "a": "5"},
    {"q": "Hány csillag van Új-Zéland zászlaján?", "o": ["4", "5", "6", "7"], "a": "4"},
    {"q": "Milyen színűek a csillagok Új-Zéland zászlaján?", "o": ["Vörös, fehér szegéllyel", "Fehér", "Sárga", "Kék"], "a": "Vörös, fehér szegéllyel"},
    {"q": "Hány csillag van Ausztrália zászlaján?", "o": ["6", "5", "7", "4"], "a": "6"},
    {"q": "Milyen színű a nap Argentína zászlaján?", "o": ["Arany/Sárga", "Vörös", "Fehér", "Narancs"], "a": "Arany/Sárga"},
    {"q": "Van-e arc a napban Argentína zászlaján?", "o": ["Igen", "Nem", "Csak a régieken", "Csak a haditengerészetin"], "a": "Igen"},
    {"q": "Van-e arc a napban Uruguay zászlaján?", "o": ["Igen", "Nem", "Néha", "Soha"], "a": "Igen"},
    {"q": "Milyen szimbólum van Mongólia zászlajának bal oldalán?", "o": ["Szojombo", "Sárkány", "Jurta", "Lófej"], "a": "Szojombo"},
    {"q": "Milyen szimbólum van a Man-sziget zászlaján?", "o": ["Triszkellion (három páncélos láb)", "Kelta kereszt", "Oroszlán", "Hárfa"], "a": "Triszkellion (három páncélos láb)"},
    {"q": "Milyen alakzat látható Nepál zászlaján (a formája)?", "o": ["Két egymásba csúszó háromszög", "Négyzet", "Téglalap", "Kör"], "a": "Két egymásba csúszó háromszög"},
    {"q": "Milyen szimbólumok vannak Nepál zászlaján?", "o": ["Nap és Hold", "Csillag és Sarló", "Hegy és Folyó", "Kard és Pajzs"], "a": "Nap és Hold"},
    {"q": "Milyen kereszt látható Svájc zászlaján?", "o": ["Görög kereszt (egyenlő szárú)", "Latin kereszt", "András-kereszt", "Máltai kereszt"], "a": "Görög kereszt (egyenlő szárú)"},
    {"q": "Milyen színű a kereszt Skandinávia legtöbb zászlaján?", "o": ["Változó, de a forma azonos", "Mindig fehér", "Mindig sárga", "Mindig kék"], "a": "Változó, de a forma azonos"},
    {"q": "Milyen színű a csillag Marokkó zászlaján?", "o": ["Zöld", "Vörös", "Fekete", "Sárga"], "a": "Zöld"},
    {"q": "Milyen szimbólum van Tunézia zászlaján?", "o": ["Vörös félhold és csillag", "Zöld csillag", "Fekete sas", "Kék sávok"], "a": "Vörös félhold és csillag"},
    {"q": "Milyen színű a félhold Törökország zászlaján?", "o": ["Fehér", "Sárga", "Vörös", "Fekete"], "a": "Fehér"},
    {"q": "Milyen szimbólum van Izrael zászlaján?", "o": ["Dávid-csillag", "Menóra", "Oroszlán", "Olajág"], "a": "Dávid-csillag"},
    {"q": "Milyen színű a Dávid-csillag Izrael zászlaján?", "o": ["Kék", "Arany", "Fekete", "Fehér"], "a": "Kék"},
    {"q": "Milyen szimbólum látható Dél-Korea zászlajának közepén?", "o": ["Jing-jang (Taegeuk)", "Nap", "Lótusz", "Sárkány"], "a": "Jing-jang (Taegeuk)"},
    {"q": "Hány trigram (fekete vonalkázás) van Dél-Korea zászlaján?", "o": ["4", "8", "2", "6"], "a": "4"},
    {"q": "Milyen szimbólum van Vietnam zászlaján?", "o": ["Nagy sárga csillag", "Sarló és kalapács", "Nap", "Sárkány"], "a": "Nagy sárga csillag"},
    {"q": "Milyen szimbólum van Szomália zászlaján?", "o": ["Nagy fehér csillag", "Félhold", "Lándzsa", "Teve"], "a": "Nagy fehér csillag"},
    {"q": "Milyen színű a csillag Pakisztán zászlaján?", "o": ["Fehér", "Zöld", "Sárga", "Kék"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Törökország zászlaján?", "o": ["Fehér", "Vörös", "Sárga", "Zöld"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Algéria zászlaján?", "o": ["Fehér", "Zöld", "Vörös", "Sárga"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Azerbajdzsán zászlaján?", "o": ["Fehér", "Vörös", "Kék", "Zöld"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Makaó zászlaján?", "o": ["Arany/Sárga", "Fehér", "Vörös", "Zöld"], "a": "Arany/Sárga"},
    {"q": "Milyen színű a csillag Észak-Korea zászlaján?", "o": ["Vörös", "Fehér", "Kék", "Arany"], "a": "Vörös"},
    {"q": "Milyen színű a csillag Szíria zászlaján?", "o": ["Zöld", "Vörös", "Fehér", "Fekete"], "a": "Zöld"},
    {"q": "Milyen színű a csillag Irak zászlaján?", "o": ["Zöld", "Vörös", "Fehér", "Fekete"], "a": "Zöld"},
    {"q": "Milyen színű a csillag Libanon zászlaján?", "o": ["Zöld", "Vörös", "Fehér", "Fekete"], "a": "Zöld"},
    
    # --- BRIT NEMZETKÖZÖSSÉG ZÁSZLÓK ---
    {"q": "Melyik elem látható a legtöbb brit nemzetközösségi ország zászlaján?", "o": ["Union Jack (brit zászló)", "Korona", "Oroszlán", "Horgony"], "a": "Union Jack (brit zászló)"},
    {"q": "Melyik ország zászlaján van Union Jack és négy csillag?", "o": ["Új-Zéland", "Ausztrália", "Kanada", "Dél-afrikai Köztársaság"], "a": "Új-Zéland"},
    {"q": "Melyik ország zászlaján van Union Jack és hat fehér csillag?", "o": ["Ausztrália", "Új-Zéland", "Kanada", "Fidzsi"], "a": "Ausztrália"},
    {"q": "Melyik ország zászlaján van Union Jack és egy nagy csillag?", "o": ["Ausztrália", "Új-Zéland", "Kanada", "Jamaica"], "a": "Ausztrália"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van juharlevél?", "o": ["Kanada", "Ausztrália", "Új-Zéland", "India"], "a": "Kanada"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van kenguru és emu?", "o": ["Ausztrália", "Új-Zéland", "Fidzsi", "Pápua Új-Guinea"], "a": "Ausztrália"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van Ashoka Csakra (küllős kerék)?", "o": ["India", "Pakisztán", "Banglades", "Srí Lanka"], "a": "India"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van zöld háttér és sárga csillag?", "o": ["Pakisztán", "Banglades", "India", "Srí Lanka"], "a": "Pakisztán"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van zöld háttér és piros kör?", "o": ["Banglades", "Pakisztán", "India", "Srí Lanka"], "a": "Banglades"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van oroszlán és kard?", "o": ["Srí Lanka", "India", "Pakisztán", "Banglades"], "a": "Srí Lanka"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van fekete, piros, zöld és sárga sávok?", "o": ["Uganda", "Kenya", "Ghána", "Nigéria"], "a": "Uganda"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van fekete, piros, zöld sávok és maszáj pajzs?", "o": ["Kenya", "Uganda", "Tanzánia", "Ghána"], "a": "Kenya"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van piros, fehér, kék sávok és juharlevél?", "o": ["Kanada", "Ausztrália", "Új-Zéland", "Fidzsi"], "a": "Kanada"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van kék háttér és Union Jack a bal felső sarokban?", "o": ["Ausztrália", "Új-Zéland", "Fidzsi", "Tuvalu"], "a": "Ausztrália"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van kék háttér, Union Jack és négy vörös csillag?", "o": ["Új-Zéland", "Ausztrália", "Fidzsi", "Pápua Új-Guinea"], "a": "Új-Zéland"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van kék háttér, Union Jack és Fidzsi címer?", "o": ["Fidzsi", "Ausztrália", "Új-Zéland", "Tuvalu"], "a": "Fidzsi"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van zöld, fehér, narancs sávok és Ashoka Csakra?", "o": ["India", "Pakisztán", "Banglades", "Srí Lanka"], "a": "India"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van piros, fehér, zöld sávok és fekete oroszlán?", "o": ["Srí Lanka", "India", "Pakisztán", "Banglades"], "a": "Srí Lanka"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van zöld háttér és fehér félhold és csillag?", "o": ["Pakisztán", "Banglades", "India", "Srí Lanka"], "a": "Pakisztán"},
    {"q": "Melyik brit nemzetközösségi ország zászlaján van zöld háttér és piros kör (nem középen)?", "o": ["Banglades", "Pakisztán", "India", "Srí Lanka"], "a": "Banglades"},
    
    # --- GEOGRÁFIA ÉS EGYÉB ---
    {"q": "Melyik ország zászlaján látható az ország térképe?", "o": ["Ciprus", "Málta", "Izland", "Kuba"], "a": "Ciprus"},
    {"q": "Melyik másik ország (vagy terület) zászlaján van még térkép Cipruson kívül?", "o": ["Koszovó", "Albánia", "Macedónia", "Szerbia"], "a": "Koszovó"},
    {"q": "Mi a furcsaság Paraguay zászlaján?", "o": ["A két oldala különböző címerrel rendelkezik", "Négyzet alakú", "Átlátszó", "Nincs rajta szín"], "a": "A két oldala különböző címerrel rendelkezik"},
    {"q": "Milyen színű a háromszög a Fülöp-szigetek zászlaján?", "o": ["Fehér", "Sárga", "Kék", "Vörös"], "a": "Fehér"},
    {"q": "Mi történik a Fülöp-szigetek zászlajával háború esetén?", "o": ["Fordítva vonják fel (a vörös sáv kerül felülre)", "Levágják a szélét", "Fekete szalagot tesznek rá", "Másik zászlót használnak"], "a": "Fordítva vonják fel (a vörös sáv kerül felülre)"},
    {"q": "Milyen felirat olvasható Brazília zászlaján?", "o": ["Ordem e Progresso", "Libertad", "Dios y Patria", "Union"], "a": "Ordem e Progresso"},
    {"q": "Milyen színű az égbolt Brazília zászlajának gömbjében?", "o": ["Kék", "Fekete", "Zöld", "Sárga"], "a": "Kék"},
    {"q": "Mit jelképez a 27 csillag Brazília zászlaján?", "o": ["Az államokat", "A gyarmatokat", "A győzelmeket", "A szenteket"], "a": "Az államokat"},
    {"q": "Milyen színű a kör Japán zászlaján?", "o": ["Bíborvörös", "Narancs", "Sárga", "Fekete"], "a": "Bíborvörös"},
    {"q": "Milyen színű a sávok nélküli Líbiai zászló (1977-2011 között)?", "o": ["Teljesen zöld", "Teljesen fekete", "Teljesen vörös", "Teljesen fehér"], "a": "Teljesen zöld"},
    {"q": "Milyen szín dominál Szaúd-Arábia zászlaján?", "o": ["Zöld", "Fekete", "Fehér", "Vörös"], "a": "Zöld"},
    {"q": "Mi a különbség Hollandia és Luxemburg zászlaja között?", "o": ["A kék szín árnyalata (Luxemburgé világosabb)", "A sorrend", "A piros árnyalata", "Nincs különbség"], "a": "A kék szín árnyalata (Luxemburgé világosabb)"},
    {"q": "Mi a különbség Románia és Csád zászlaja között?", "o": ["A kék szín árnyalata (Csádé sötétebb)", "A címer", "A sorrend", "A piros színe"], "a": "A kék szín árnyalata (Csádé sötétebb)"},
    {"q": "Milyen színű a felső sáv Ukrajna zászlaján?", "o": ["Kék", "Sárga", "Fehér", "Vörös"], "a": "Kék"},
    {"q": "Mit jelképez a sárga szín Ukrajna zászlaján?", "o": ["Búzamezőket", "A napot", "Az aranyat", "A homokot"], "a": "Búzamezőket"},
    {"q": "Melyik ország zászlaja az egyetlen, ami nem téglalap alakú?", "o": ["Nepál", "Svájc", "Vatikán", "Belgium"], "a": "Nepál"},
    {"q": "Melyik két ország zászlaja négyzet alakú hivatalosan?", "o": ["Svájc és Vatikán", "Svájc és Monaco", "Vatikán és San Marino", "Nepál és India"], "a": "Svájc és Vatikán"},
    {"q": "Milyen tárgyak vannak a Vatikán zászlaján?", "o": ["Két kulcs és a pápai tiara", "Kereszt és Biblia", "Kehely és Ostya", "Galamb"], "a": "Két kulcs és a pápai tiara"},
    {"q": "Milyen színű a két kulcs a Vatikán zászlaján?", "o": ["Arany és Ezüst", "Két arany", "Két ezüst", "Fekete és Fehér"], "a": "Arany és Ezüst"},
    {"q": "Milyen színű az átlós kereszt Jamaica zászlaján?", "o": ["Arany/Sárga", "Fehér", "Vörös", "Zöld"], "a": "Arany/Sárga"},
    {"q": "Milyen színek nincsenek Jamaica zászlaján (az egyetlen a világon)?", "o": ["Piros, fehér vagy kék", "Zöld vagy sárga", "Fekete", "Lila"], "a": "Piros, fehér vagy kék"},
    {"q": "Milyen színű a háromszög Guyana zászlajának bal szélén?", "o": ["Vörös (fekete szegéllyel)", "Zöld", "Sárga", "Fehér"], "a": "Vörös (fekete szegéllyel)"},
    {"q": "Milyen színű csillag van Kuba zászlaján?", "o": ["Fehér", "Vörös", "Sárga", "Kék"], "a": "Fehér"},
    {"q": "Milyen színű a háromszög Kuba zászlaján?", "o": ["Vörös", "Kék", "Fehér", "Fekete"], "a": "Vörös"},
    {"q": "Milyen színű a sávok nélküli alap Banglades zászlaján?", "o": ["Zöld", "Vörös", "Fehér", "Narancs"], "a": "Zöld"},
    {"q": "Miért nem pontosan középen van a piros kör Banglades zászlaján?", "o": ["Hogy lobogáskor középen látszódjon", "Mert így szebb", "Hiba volt a tervezéskor", "Vallási okokból"], "a": "Hogy lobogáskor középen látszódjon"},
    {"q": "Milyen színű a kereszt Finnország zászlaján?", "o": ["Kék", "Sárga", "Vörös", "Fekete"], "a": "Kék"},
    {"q": "Milyen színű a kereszt Norvégia zászlaján?", "o": ["Kék (fehér szegéllyel)", "Sárga", "Vörös", "Fehér"], "a": "Kék (fehér szegéllyel)"},
    {"q": "Milyen színű a kereszt Svédország zászlaján?", "o": ["Sárga", "Kék", "Vörös", "Fehér"], "a": "Sárga"},
    {"q": "Milyen színű a kereszt Dánia zászlaján?", "o": ["Fehér", "Sárga", "Kék", "Fekete"], "a": "Fehér"},
    {"q": "Melyik a világ legrégebbi, ma is használt nemzeti zászlaja?", "o": ["Dánia (Dannebrog)", "Japán", "Ausztria", "Hollandia"], "a": "Dánia (Dannebrog)"},
    {"q": "Milyen madár van Pápua Új-Guinea zászlaján?", "o": ["Raggi-paradicsommadár", "Kivi", "Sárgarigó", "Héja"], "a": "Raggi-paradicsommadár"},
    
    # --- EURÓPAI ORSZÁGOK (hiányzó országok) ---
    {"q": "Hány sáv van Görögország zászlaján?", "o": ["9 (5 kék, 4 fehér)", "7 (4 kék, 3 fehér)", "5 (3 kék, 2 fehér)", "11 (6 kék, 5 fehér)"], "a": "9 (5 kék, 4 fehér)"},
    {"q": "Milyen kereszt látható Görögország zászlaján?", "o": ["Görög kereszt (bal felső sarokban)", "Latin kereszt", "András-kereszt", "Máltai kereszt"], "a": "Görög kereszt (bal felső sarokban)"},
    {"q": "Milyen színű a kereszt Izland zászlaján?", "o": ["Piros (fehér szegéllyel)", "Kék", "Fehér", "Sárga"], "a": "Piros (fehér szegéllyel)"},
    {"q": "Milyen színű a félhold Azerbajdzsán zászlaján?", "o": ["Fehér", "Zöld", "Vörös", "Kék"], "a": "Fehér"},
    {"q": "Hány csillag van Bosznia-Hercegovina zászlaján?", "o": ["9 (félkörben)", "5", "7", "12"], "a": "9 (félkörben)"},
    {"q": "Hány csillag van Koszovó zászlaján?", "o": ["6 (félkörben)", "5", "7", "12"], "a": "6 (félkörben)"},
    
    # --- ÁZSIAI ORSZÁGOK (hiányzó országok) ---
    {"q": "Milyen színű a félhold Malajzia zászlaján?", "o": ["Sárga", "Fehér", "Vörös", "Kék"], "a": "Sárga"},
    {"q": "Hány csillag van Szingapúr zászlaján?", "o": ["5", "4", "6", "7"], "a": "5"},
    {"q": "Hány csillag van Fülöp-szigetek zászlaján?", "o": ["3", "5", "4", "6"], "a": "3"},
    {"q": "Milyen színű a csillag Mianmar zászlaján?", "o": ["Fehér", "Sárga", "Vörös", "Kék"], "a": "Fehér"},
    {"q": "Milyen színű a félhold Pakisztán zászlaján?", "o": ["Fehér", "Zöld", "Vörös", "Kék"], "a": "Fehér"},
    {"q": "Hány csillag van Szíria zászlaján?", "o": ["2", "3", "5", "7"], "a": "2"},
    {"q": "Hány csillag van Üzbegisztán zászlaján?", "o": ["12", "5", "7", "9"], "a": "12"},
    {"q": "Hány csillag van Tádzsikisztán zászlaján?", "o": ["7", "5", "9", "12"], "a": "7"},
    
    # --- AFRIKAI ORSZÁGOK (hiányzó országok) ---
    {"q": "Milyen színű a csillag Ghána zászlaján?", "o": ["Fekete", "Fehér", "Sárga", "Kék"], "a": "Fekete"},
    {"q": "Milyen színű a csillag Szenegál zászlaján?", "o": ["Zöld", "Fehér", "Sárga", "Kék"], "a": "Zöld"},
    {"q": "Milyen színű a csillag Burkina Faso zászlaján?", "o": ["Sárga", "Fehér", "Zöld", "Kék"], "a": "Sárga"},
    {"q": "Milyen színű a csillag Etiópia zászlaján?", "o": ["Kék", "Fehér", "Sárga", "Zöld"], "a": "Kék"},
    {"q": "Milyen színű a csillag Ruanda zászlaján?", "o": ["Sárga", "Fehér", "Kék", "Zöld"], "a": "Sárga"},
    {"q": "Milyen színű a csillag Kongói Demokratikus Köztársaság zászlaján?", "o": ["Sárga", "Fehér", "Kék", "Zöld"], "a": "Sárga"},
    {"q": "Milyen színű a csillag Kamerun zászlaján?", "o": ["Sárga", "Fehér", "Kék", "Zöld"], "a": "Sárga"},
    {"q": "Milyen színű a csillag Közép-afrikai Köztársaság zászlaján?", "o": ["Sárga", "Fehér", "Kék", "Zöld"], "a": "Sárga"},
    {"q": "Milyen színű a csillag Togo zászlaján?", "o": ["Fehér", "Sárga", "Kék", "Zöld"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Libéria zászlaján?", "o": ["Fehér", "Kék", "Sárga", "Zöld"], "a": "Fehér"},
    {"q": "Milyen színű a csillag Guinea-Bissau zászlaján?", "o": ["Fekete", "Fehér", "Sárga", "Kék"], "a": "Fekete"},
    {"q": "Hány csillag van Zöld-foki Köztársaság zászlaján?", "o": ["10 (körben)", "5", "7", "12"], "a": "10 (körben)"},
    {"q": "Milyen színű a félhold Mauritánia zászlaján?", "o": ["Sárga", "Fehér", "Zöld", "Kék"], "a": "Sárga"},
    {"q": "Milyen színű a félhold Algéria zászlaján?", "o": ["Piros", "Fehér", "Zöld", "Kék"], "a": "Piros"},
    {"q": "Milyen színű a félhold Líbia zászlaján?", "o": ["Piros", "Fehér", "Zöld", "Kék"], "a": "Piros"},
    {"q": "Hány csillag van Comore-szigetek zászlaján?", "o": ["4", "5", "6", "7"], "a": "4"},
    
    # --- AMERIKAI ORSZÁGOK (hiányzó országok) ---
    {"q": "Hány csillag van Venezuela zászlaján?", "o": ["8", "5", "7", "12"], "a": "8"},
    {"q": "Milyen színű a csillag Chile zászlaján?", "o": ["Fehér", "Kék", "Sárga", "Piros"], "a": "Fehér"},
    {"q": "Hány csillag van Panama zászlaján?", "o": ["2", "3", "5", "7"], "a": "2"},
    {"q": "Hány csillag van Honduras zászlaján?", "o": ["5", "4", "6", "7"], "a": "5"},
    
    # --- ÓCEÁNIAI ORSZÁGOK (hiányzó országok) ---
    {"q": "Milyen színű a csillag Tonga zászlaján?", "o": ["Piros", "Fehér", "Kék", "Sárga"], "a": "Piros"},
    {"q": "Hány csillag van Szamoa zászlaján?", "o": ["5", "4", "6", "7"], "a": "5"},
    {"q": "Milyen színű a csillag Vanuatu zászlaján?", "o": ["Sárga", "Fehér", "Kék", "Zöld"], "a": "Sárga"},
    {"q": "Hány csillag van Mikronézia zászlaján?", "o": ["4", "5", "6", "7"], "a": "4"},
    {"q": "Hány csillag van Salamon-szigetek zászlaján?", "o": ["5", "4", "6", "7"], "a": "5"}
]

# Session state inicializálása
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = []
if 'question_index' not in st.session_state:
    st.session_state.question_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'num_questions' not in st.session_state:
    st.session_state.num_questions = 10
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'incorrect_answers' not in st.session_state:
    st.session_state.incorrect_answers = 0
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False

# Főoldal
st.title("🏳️ Zászló Mester PRO - 100+ Kérdés")

if not st.session_state.quiz_started:
    # Beállítások képernyő
    st.markdown(f"**Összesen {len(questions_db)} kérdés van az adatbázisban.**")
    
    st.markdown("### Hány kérdést szeretnél kapni?")
    num_questions = st.slider(
        "Kérdések száma:",
        min_value=5,
        max_value=len(questions_db),
        value=10,
        step=1
    )
    
    if st.button("🎮 JÁTÉK INDÍTÁSA", type="primary", use_container_width=True):
        st.session_state.num_questions = num_questions
        # Kérdések előkészítése - válaszopciók véletlenszerűen keverve
        prepared_questions = []
        for q in random.sample(questions_db, num_questions):
            # Válaszopciók véletlenszerűen keverve
            options = q["o"].copy()
            random.shuffle(options)
            prepared_questions.append({
                "q": q["q"],
                "o": options,
                "a": q["a"]  # A helyes válasz megmarad, de az opciók keverve vannak
            })
        st.session_state.current_questions = prepared_questions
        st.session_state.question_index = 0
        st.session_state.score = 0
        st.session_state.correct_answers = 0
        st.session_state.incorrect_answers = 0
        st.session_state.show_answer = False
        st.session_state.quiz_started = True
        st.rerun()
else:
    # Kvíz képernyő
    if st.session_state.question_index >= len(st.session_state.current_questions):
        # Eredmények képernyő
        percent = int((st.session_state.score / st.session_state.num_questions) * 100)
        color = "🟢" if percent >= 80 else "🟠" if percent >= 50 else "🔴"
        
        st.title("🎉 Játék Vége!")
        st.markdown(f"### {color} Pontszámod: {st.session_state.score} / {st.session_state.num_questions}")
        st.markdown(f"### {percent}%")
        
        if st.button("🔙 Vissza a menübe", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.correct_answers = 0
            st.session_state.incorrect_answers = 0
            st.session_state.show_answer = False
            st.rerun()
    else:
        # Kérdés képernyő
        q_data = st.session_state.current_questions[st.session_state.question_index]
        
        # Számlálók megjelenítése
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("✅ Helyes válaszok", st.session_state.correct_answers)
        with col2:
            st.metric("❌ Hibás válaszok", st.session_state.incorrect_answers)
        with col3:
            st.metric("📊 Pontszám", f"{st.session_state.score}/{st.session_state.num_questions}")
        
        # Progress
        progress = (st.session_state.question_index + 1) / st.session_state.num_questions
        st.progress(progress)
        st.markdown(f"**Kérdés: {st.session_state.question_index + 1} / {st.session_state.num_questions}**")
        
        # Kérdés - NAGYON LÁTHATÓ
        st.markdown("---")
        st.markdown(f"### ❓ {q_data['q']}")
        st.markdown("---")
        
        if not st.session_state.show_answer:
            # Válaszlehetőségek (csak ha még nem mutattuk meg a választ)
            selected = st.radio(
                "Válassz egyet:",
                options=q_data["o"],
                key=f"question_{st.session_state.question_index}"
            )
            
            # Válasz beküldése
            if st.button("✅ Válasz Beküldése", type="primary", use_container_width=True):
                is_correct = selected == q_data["a"]
                
                if is_correct:
                    st.session_state.score += 1
                    st.session_state.correct_answers += 1
                else:
                    st.session_state.incorrect_answers += 1
                
                st.session_state.show_answer = True
                st.session_state.last_answer_correct = is_correct
                st.session_state.last_selected = selected
                st.rerun()
        else:
            # Válasz megjelenítése
            is_correct = st.session_state.get('last_answer_correct', False)
            selected = st.session_state.get('last_selected', '')
            
            # Magyarázat generálása
            explanation, country_name, code = generate_explanation(q_data, is_correct, selected)
            
            # Eredmény megjelenítése
            st.markdown("---")
            if is_correct:
                st.success(explanation)
            else:
                st.error(explanation)
            
            # Zászló megjelenítése a válasz után (csak itt jelenik meg)
            if code:
                flag_url = get_flag_url(code)
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    try:
                        st.image(flag_url, width=300, caption=f"{country_name} zászlaja" if country_name else "Zászló")
                    except:
                        st.info(f"🌍 {country_name} zászlaja" if country_name else "🌍 Zászló")
            
            # Következő kérdés gomb
            if st.button("➡️ Következő kérdés", use_container_width=True, type="primary"):
                st.session_state.question_index += 1
                st.session_state.show_answer = False
                st.rerun()

