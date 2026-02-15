# Zászlók részlete – kérdések a data/flags/crop mappából
# A kérdés mindig: "Melyik ország zászlajából származik a részlet?"
# A válaszopciók a szomszédos országok közül kerülnek.
# A fájlnevek követik az ország kódját (pl. AD_crop_440_330.png = Andorra)

import random
from pathlib import Path
from typing import Optional

# Szomszédos országok (GeoDataSource country-borders alapján, ISO 3166-1)
COUNTRY_NEIGHBORS: dict[str, list[str]] = {
    "AD": ["FR", "ES"], "AE": ["OM", "SA"], "AF": ["CN", "IR", "PK", "TJ", "TM", "UZ"],
    "AL": ["GR", "ME", "MK", "RS"], "AM": ["AZ", "GE", "IR", "TR"], "AO": ["CG", "CD", "NA", "ZM"],
    "AR": ["BO", "BR", "CL", "PY", "UY"], "AT": ["CZ", "DE", "HU", "IT", "LI", "SK", "SI", "CH"],
    "AZ": ["AM", "GE", "IR", "RU", "TR"], "BA": ["HR", "ME", "RS"], "BD": ["IN", "MM"],
    "BE": ["FR", "DE", "LU", "NL"], "BF": ["BJ", "CI", "GH", "ML", "NE", "TG"],
    "BG": ["GR", "MK", "RO", "RS", "TR"], "BI": ["CD", "RW", "TZ"], "BJ": ["BF", "NE", "NG", "TG"],
    "BN": ["MY"], "BO": ["AR", "BR", "CL", "PY", "PE"], "BR": ["AR", "BO", "CO", "GF", "GY", "PY", "PE", "SR", "UY", "VE"],
    "BW": ["NA", "ZA", "ZM", "ZW"], "BY": ["LV", "LT", "PL", "RU", "UA"], "BZ": ["GT", "MX"],
    "CA": ["US"], "CD": ["AO", "BI", "CF", "CG", "RW", "SS", "TZ", "UG", "ZM"],
    "CF": ["CM", "TD", "CG", "CD", "SS", "SD"], "CG": ["AO", "CM", "CF", "CD", "GA"],
    "CH": ["AT", "FR", "DE", "IT", "LI"], "CI": ["BF", "GH", "GN", "LR", "ML"],
    "CL": ["AR", "BO", "PE"], "CM": ["CF", "TD", "CG", "GQ", "GA", "NG"],
    "CN": ["AF", "BT", "IN", "KZ", "KP", "KG", "LA", "MN", "MM", "NP", "PK", "RU", "TJ", "VN"],
    "CO": ["BR", "EC", "PA", "PE", "VE"], "CR": ["NI", "PA"], "CZ": ["AT", "DE", "PL", "SK"],
    "DE": ["AT", "BE", "CZ", "DK", "FR", "LU", "NL", "PL", "CH"], "DJ": ["ER", "ET", "SO"],
    "DZ": ["LY", "ML", "MR", "MA", "NE", "TN", "EH"], "DO": ["HT"], "EC": ["CO", "PE"],
    "EE": ["LV", "RU"], "EG": ["IL", "LY", "PS", "SD"], "ER": ["DJ", "ET", "SD"],
    "ES": ["AD", "FR", "MA", "PT"], "ET": ["DJ", "ER", "KE", "SO", "SS", "SD"],
    "FI": ["NO", "RU", "SE"], "FR": ["AD", "BE", "DE", "IT", "LU", "MC", "ES", "CH"],
    "GA": ["CM", "CG", "GQ"], "GB": ["IE"], "GE": ["AM", "AZ", "RU", "TR"],
    "GH": ["BF", "CI", "TG"], "GM": ["SN"], "GN": ["CI", "GW", "LR", "ML", "SN", "SL"],
    "GQ": ["CM", "GA"], "GR": ["AL", "BG", "MK", "TR"], "GT": ["BZ", "SV", "HN", "MX"],
    "GW": ["GN", "SN"], "HN": ["SV", "GT", "NI"], "HR": ["BA", "HU", "ME", "RS", "SI"],
    "HT": ["DO"], "HU": ["AT", "HR", "RO", "RS", "SK", "SI", "UA"],
    "ID": ["MY", "PG", "TL"], "IN": ["BD", "BT", "CN", "MM", "NP", "PK"],
    "IQ": ["IR", "JO", "KW", "SA", "SY", "TR"], "IR": ["AF", "AM", "AZ", "IQ", "PK", "TR", "TM"],
    "IL": ["EG", "JO", "LB", "PS", "SY"], "IT": ["AT", "FR", "SM", "SI", "CH", "VA"],
    "JO": ["IQ", "IL", "PS", "SA", "SY"], "KE": ["ET", "SO", "SS", "TZ", "UG"],
    "KG": ["CN", "KZ", "TJ", "UZ"], "KH": ["LA", "TH", "VN"], "KP": ["CN", "KR", "RU"],
    "KR": ["KP"], "KW": ["IQ", "SA"], "KZ": ["CN", "KG", "RU", "TM", "UZ"],
    "LA": ["CN", "KH", "MM", "TH", "VN"], "LB": ["IL", "SY"], "LR": ["CI", "GN", "SL"],
    "LS": ["ZA"], "LT": ["BY", "LV", "PL", "RU"], "LU": ["BE", "DE", "FR"],
    "LV": ["BY", "EE", "LT", "RU"], "LY": ["DZ", "TD", "EG", "NE", "SD", "TN"],
    "MA": ["DZ", "ES", "EH"], "MC": ["FR"], "MD": ["RO", "UA"], "ME": ["AL", "BA", "HR", "RS"],
    "ML": ["DZ", "BF", "CI", "GN", "MR", "NE", "SN"], "MM": ["BD", "CN", "IN", "LA", "TH"],
    "MN": ["CN", "RU"], "MR": ["DZ", "ML", "SN", "EH"], "MW": ["MZ", "TZ", "ZM"],
    "MX": ["BZ", "GT", "US"], "MZ": ["MW", "SZ", "ZA", "TZ", "ZM", "ZW"],
    "NA": ["AO", "BW", "ZA", "ZM"], "NE": ["DZ", "BJ", "BF", "TD", "LY", "ML", "NG"],
    "NG": ["BJ", "CM", "TD", "NE"], "NI": ["CR", "HN"], "NL": ["BE", "DE"],
    "NO": ["FI", "RU", "SE"], "NP": ["CN", "IN"], "OM": ["AE", "SA", "YE"],
    "PA": ["CO", "CR"], "PE": ["BO", "BR", "CL", "CO", "EC"], "PG": ["ID"],
    "PK": ["AF", "CN", "IN", "IR"], "PL": ["BY", "CZ", "DE", "LT", "RU", "SK", "UA"],
    "PS": ["EG", "IL", "JO"], "PT": ["ES"], "PY": ["AR", "BO", "BR"],
    "QA": ["SA"], "RO": ["BG", "HU", "MD", "RS", "UA"], "RS": ["AL", "BA", "BG", "HR", "HU", "ME", "MK", "RO"],
    "RU": ["AZ", "BY", "CN", "EE", "FI", "GE", "KZ", "KP", "LV", "LT", "MN", "NO", "PL", "UA"],
    "RW": ["BI", "CD", "TZ", "UG"], "SA": ["IQ", "JO", "KW", "OM", "QA", "AE", "YE"],
    "SD": ["CF", "TD", "EG", "ET", "ER", "LY", "SS"], "SE": ["FI", "NO"],
    "SI": ["AT", "HR", "HU", "IT"], "SK": ["AT", "CZ", "HU", "PL", "UA"],
    "SL": ["GN", "LR"], "SM": ["IT"], "SN": ["GM", "GN", "GW", "ML", "MR"],
    "SO": ["DJ", "ET", "KE"], "SS": ["CF", "CD", "ET", "KE", "SD", "UG"],
    "SR": ["BR", "GF", "GY"], "SZ": ["MZ", "ZA"], "SY": ["IQ", "IL", "JO", "LB", "TR"],
    "TD": ["CM", "CF", "LY", "NE", "NG", "SD"], "TG": ["BJ", "BF", "GH"],
    "TH": ["KH", "LA", "MY", "MM"], "TJ": ["AF", "CN", "KG", "UZ"], "TL": ["ID"],
    "TM": ["AF", "IR", "KZ", "UZ"], "TN": ["DZ", "LY"], "TR": ["AM", "AZ", "BG", "GE", "GR", "IR", "IQ", "SY"],
    "TZ": ["BI", "CD", "KE", "MW", "MZ", "RW", "UG", "ZM"], "UA": ["BY", "HU", "MD", "PL", "RO", "RU", "SK"],
    "UG": ["CD", "KE", "RW", "SS", "TZ"], "US": ["CA", "MX"], "UY": ["AR", "BR"],
    "UZ": ["AF", "KZ", "KG", "TJ", "TM"], "VE": ["BR", "CO", "GY"],
    "VN": ["KH", "CN", "LA"], "ZA": ["BW", "LS", "MZ", "NA", "SZ", "ZW"],
    "ZM": ["AO", "BW", "CD", "MW", "MZ", "NA", "TZ", "ZW"], "ZW": ["BW", "MZ", "ZA", "ZM"],
}

# Országkód -> angol név (zaszlok_all_questions alapján)
COUNTRY_CODE_TO_NAME = {
    "AD": "Andorra", "AE": "United Arab Emirates", "AF": "Afghanistan", "AG": "Antigua and Barbuda",
    "AL": "Albania", "AM": "Armenia", "AO": "Angola", "AR": "Argentina", "AT": "Austria",
    "AU": "Australia", "AZ": "Azerbaijan", "BA": "Bosnia and Herzegovina", "BB": "Barbados",
    "BD": "Bangladesh", "BE": "Belgium", "BF": "Burkina Faso", "BG": "Bulgaria", "BH": "Bahrain",
    "BI": "Burundi", "BJ": "Benin", "BN": "Brunei", "BO": "Bolivia", "BR": "Brazil",
    "BS": "Bahamas", "BT": "Bhutan", "BW": "Botswana", "BY": "Belarus", "BZ": "Belize",
    "CA": "Canada", "CD": "DR Congo", "CF": "Central African Republic", "CG": "Republic of the Congo",
    "CH": "Switzerland", "CI": "Côte d'Ivoire (Ivory Coast)", "CL": "Chile", "CM": "Cameroon",
    "CN": "China", "CO": "Colombia", "CR": "Costa Rica", "CU": "Cuba", "CV": "Cape Verde",
    "CY": "Cyprus", "CZ": "Czechia", "DE": "Germany", "DJ": "Djibouti", "DK": "Denmark",
    "DM": "Dominica", "DO": "Dominican Republic", "DZ": "Algeria", "EC": "Ecuador",
    "EE": "Estonia", "EG": "Egypt", "ER": "Eritrea", "ES": "Spain", "ET": "Ethiopia",
    "FI": "Finland", "FJ": "Fiji", "FM": "Micronesia", "FR": "France", "GA": "Gabon",
    "GB": "United Kingdom", "GD": "Grenada", "GE": "Georgia", "GH": "Ghana", "GM": "Gambia",
    "GN": "Guinea", "GQ": "Equatorial Guinea", "GR": "Greece", "GT": "Guatemala",
    "GW": "Guinea-Bissau", "GY": "Guyana", "HN": "Honduras", "HR": "Croatia", "HT": "Haiti",
    "HU": "Hungary", "ID": "Indonesia", "IE": "Ireland", "IL": "Israel", "IN": "India",
    "IQ": "Iraq", "IR": "Iran", "IS": "Iceland", "IT": "Italy", "JM": "Jamaica",
    "JO": "Jordan", "JP": "Japan", "KE": "Kenya", "KG": "Kyrgyzstan", "KH": "Cambodia",
    "KI": "Kiribati", "KM": "Comoros", "KN": "Saint Kitts and Nevis", "KP": "North Korea",
    "KR": "South Korea", "KW": "Kuwait", "KZ": "Kazakhstan", "LA": "Laos", "LB": "Lebanon",
    "LC": "Saint Lucia", "LI": "Liechtenstein", "LK": "Sri Lanka", "LR": "Liberia",
    "LS": "Lesotho", "LT": "Lithuania", "LU": "Luxembourg", "LV": "Latvia", "LY": "Libya",
    "MA": "Morocco", "MC": "Monaco", "MD": "Moldova", "ME": "Montenegro", "MG": "Madagascar",
    "MH": "Marshall Islands", "MK": "North Macedonia", "ML": "Mali", "MM": "Myanmar",
    "MN": "Mongolia", "MR": "Mauritania", "MT": "Malta", "MU": "Mauritius", "MV": "Maldives",
    "MW": "Malawi", "MX": "Mexico", "MY": "Malaysia", "MZ": "Mozambique", "NA": "Namibia",
    "NE": "Niger", "NG": "Nigeria", "NI": "Nicaragua", "NL": "Netherlands", "NO": "Norway",
    "NP": "Nepal", "NR": "Nauru", "NZ": "New Zealand", "OM": "Oman", "PA": "Panama",
    "PE": "Peru", "PG": "Papua New Guinea", "PH": "Philippines", "PK": "Pakistan",
    "PL": "Poland", "PS": "Palestine", "PT": "Portugal", "PW": "Palau", "PY": "Paraguay",
    "QA": "Qatar", "RO": "Romania", "RS": "Serbia", "RU": "Russia", "RW": "Rwanda",
    "SA": "Saudi Arabia", "SB": "Solomon Islands", "SC": "Seychelles", "SD": "Sudan",
    "SE": "Sweden", "SG": "Singapore", "SI": "Slovenia", "SK": "Slovakia", "SL": "Sierra Leone",
    "SM": "San Marino", "SN": "Senegal", "SO": "Somalia", "SR": "Suriname", "SS": "South Sudan",
    "ST": "São Tomé and Príncipe", "SV": "El Salvador", "SY": "Syria", "SZ": "Eswatini (Swaziland)",
    "TD": "Chad", "TG": "Togo", "TH": "Thailand", "TJ": "Tajikistan", "TL": "Timor-Leste",
    "TM": "Turkmenistan", "TN": "Tunisia", "TO": "Tonga", "TR": "Turkey", "TT": "Trinidad and Tobago",
    "TV": "Tuvalu", "TW": "Taiwan", "TZ": "Tanzania", "UA": "Ukraine", "UG": "Uganda",
    "US": "United States", "UY": "Uruguay", "UZ": "Uzbekistan", "VC": "Saint Vincent and the Grenadines",
    "VE": "Venezuela", "VN": "Vietnam", "VU": "Vanuatu", "WS": "Samoa", "YE": "Yemen",
    "ZA": "South Africa", "ZM": "Zambia", "ZW": "Zimbabwe",
    # További területek (crop mappa szinkronizáláshoz)
    "PR": "Puerto Rico", "RE": "Réunion", "SH": "Saint Helena",
    "SJ": "Svalbard and Jan Mayen", "SX": "Sint Maarten",
    "TC": "Turks and Caicos Islands", "TF": "French Southern Territories",
    "TK": "Tokelau", "VA": "Vatican City", "VG": "British Virgin Islands",
    "VI": "U.S. Virgin Islands", "WF": "Wallis and Futuna", "YT": "Mayotte",
}

QUESTION_HU = "Melyik ország zászlajából származik a részlet?"
QUESTION_EN = "Which country's flag does this detail come from?"
EXPLANATION_TEMPLATE_HU = "Ez {country} zászlójának egy részlete."
EXPLANATION_TEMPLATE_EN = "This is a detail of {country}'s flag."


def _get_crop_dir():
    """Visszaadja a crop mappa abszolút útvonalát."""
    base = Path(__file__).parent.parent
    return base / "data" / "flags" / "crop"


def _parse_country_code_from_filename(filename: str) -> Optional[str]:
    """
    Fájlnévből országkód kinyerése.
    Formátumok: AD_crop_440_330.png, tg_1000px_crop_001_....jpg, AD.png
    """
    name = Path(filename).stem.upper()
    if "_crop" in name:
        return name.split("_")[0][:2]
    if len(name) >= 2 and name[:2].isalpha():
        return name[:2]
    return None


def _load_crop_questions() -> list[dict]:
    """Dinamikusan betölti a kérdéseket a crop mappából."""
    questions = []
    seen_filenames = set()

    crop_dir = _get_crop_dir()
    if crop_dir.exists():
        for f in list(crop_dir.glob("*.png")) + list(crop_dir.glob("*.jpg")):
            if f.name in seen_filenames:
                continue
            seen_filenames.add(f.name)
            code = _parse_country_code_from_filename(f.name)
            if not code or code not in COUNTRY_CODE_TO_NAME:
                continue
            country_name = COUNTRY_CODE_TO_NAME[code]
            # Szomszédos országok nevei (csak azok, amik a listában vannak)
            neighbor_codes = COUNTRY_NEIGHBORS.get(code.upper(), [])
            neighbor_names = [
                COUNTRY_CODE_TO_NAME[nc] for nc in neighbor_codes
                if nc in COUNTRY_CODE_TO_NAME and COUNTRY_CODE_TO_NAME[nc] != country_name
            ]
            # Ha kevesebb mint 3 szomszéd, kiegészítjük véletlennel
            if len(neighbor_names) >= 3:
                wrong = random.sample(neighbor_names, 3)
            else:
                other_countries = [
                    c for cc, c in COUNTRY_CODE_TO_NAME.items()
                    if cc != code and c != country_name and c not in neighbor_names
                ]
                wrong = list(neighbor_names) + random.sample(other_countries, 3 - len(neighbor_names))
            options = [country_name] + wrong
            random.shuffle(options)
            correct = options.index(country_name)

            # Relatív útvonal a quizhez (data/flags/crop/)
            rel = f.relative_to(Path(__file__).parent.parent)
            logo_path = str(rel).replace("\\", "/")

            questions.append({
                "question": QUESTION_HU,
                "logo_path": logo_path,
                "options": options,
                "correct": correct,
                "explanation": EXPLANATION_TEMPLATE_HU.format(country=country_name),
                "topic": "zaszlok_reszletek",
                "_country_name": country_name,
            })

    return questions


# Betöltés indításkor
ZASZLOK_RESZLETEK_QUESTIONS = _load_crop_questions()
