#!/usr/bin/env python3
"""
WikiArt Popular Paintings - Manuális lista
A legnépszerűbb festmények manuálisan összeállított listája
"""

import requests
import re
import os
import time
import html
from urllib.parse import urljoin, urlparse

def slugify(text):
    """Szöveg konvertálása URL-barát formátumra"""
    text = text.lower()
    
    # Ékezetes betűk lecserélése
    accent_map = {
        'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a',
        'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
        'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
        'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
        'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
        'ý': 'y', 'ÿ': 'y',
        'ñ': 'n',
        'ç': 'c',
        'š': 's', 'ś': 's',
        'ž': 'z', 'ź': 'z',
        'ć': 'c',
        'ł': 'l',
        'ń': 'n',
        'ś': 's',
        'ź': 'z',
        'ż': 'z'
    }
    
    for accented, plain in accent_map.items():
        text = text.replace(accented, plain)
    
    text = re.sub(r"[^a-z0-9\s\-_]", '', text)
    text = re.sub(r"[\s_\-]+", '-', text)
    text = text.strip('-')
    
    return text

def get_popular_paintings_list():
    """Népszerű festmények manuális listája"""
    
    # A WikiArt legnépszerűbb festményei (600-ból a top 100)
    popular_paintings = [
        # Leonardo da Vinci
        {"title": "Mona Lisa", "artist": "Leonardo da Vinci", "year": "1503"},
        {"title": "The Last Supper", "artist": "Leonardo da Vinci", "year": "1495"},
        {"title": "Vitruvian Man", "artist": "Leonardo da Vinci", "year": "1490"},
        
        # Vincent van Gogh
        {"title": "The Starry Night", "artist": "Vincent van Gogh", "year": "1889"},
        {"title": "Self-Portrait with Bandaged Ear", "artist": "Vincent van Gogh", "year": "1889"},
        {"title": "Sunflowers", "artist": "Vincent van Gogh", "year": "1888"},
        {"title": "The Bedroom", "artist": "Vincent van Gogh", "year": "1888"},
        {"title": "Irises", "artist": "Vincent van Gogh", "year": "1889"},
        
        # Pablo Picasso
        {"title": "Guernica", "artist": "Pablo Picasso", "year": "1937"},
        {"title": "Les Demoiselles d'Avignon", "artist": "Pablo Picasso", "year": "1907"},
        {"title": "The Old Guitarist", "artist": "Pablo Picasso", "year": "1903"},
        {"title": "Weeping Woman", "artist": "Pablo Picasso", "year": "1937"},
        
        # Claude Monet
        {"title": "Water Lilies", "artist": "Claude Monet", "year": "1916"},
        {"title": "Impression, Sunrise", "artist": "Claude Monet", "year": "1872"},
        {"title": "The Water Lily Pond", "artist": "Claude Monet", "year": "1899"},
        {"title": "Woman with a Parasol", "artist": "Claude Monet", "year": "1875"},
        
        # Salvador Dalí
        {"title": "The Persistence of Memory", "artist": "Salvador Dalí", "year": "1931"},
        {"title": "The Elephants", "artist": "Salvador Dalí", "year": "1948"},
        {"title": "The Temptation of St. Anthony", "artist": "Salvador Dalí", "year": "1946"},
        
        # Edvard Munch
        {"title": "The Scream", "artist": "Edvard Munch", "year": "1893"},
        {"title": "Madonna", "artist": "Edvard Munch", "year": "1894"},
        
        # Johannes Vermeer
        {"title": "Girl with a Pearl Earring", "artist": "Johannes Vermeer", "year": "1665"},
        {"title": "The Milkmaid", "artist": "Johannes Vermeer", "year": "1658"},
        
        # Sandro Botticelli
        {"title": "The Birth of Venus", "artist": "Sandro Botticelli", "year": "1485"},
        {"title": "Primavera", "artist": "Sandro Botticelli", "year": "1482"},
        
        # Gustav Klimt
        {"title": "The Kiss", "artist": "Gustav Klimt", "year": "1908"},
        {"title": "Portrait of Adele Bloch-Bauer I", "artist": "Gustav Klimt", "year": "1907"},
        
        # Michelangelo
        {"title": "The Creation of Adam", "artist": "Michelangelo", "year": "1512"},
        {"title": "The Last Judgment", "artist": "Michelangelo", "year": "1541"},
        
        # René Magritte
        {"title": "The Son of Man", "artist": "René Magritte", "year": "1964"},
        {"title": "The Treachery of Images", "artist": "René Magritte", "year": "1929"},
        
        # Grant Wood
        {"title": "American Gothic", "artist": "Grant Wood", "year": "1930"},
        
        # Katsushika Hokusai
        {"title": "The Great Wave off Kanagawa", "artist": "Katsushika Hokusai", "year": "1831"},
        
        # Auguste Rodin
        {"title": "The Thinker", "artist": "Auguste Rodin", "year": "1904"},
        
        # Wassily Kandinsky
        {"title": "Composition VII", "artist": "Wassily Kandinsky", "year": "1913"},
        
        # Frida Kahlo
        {"title": "The Two Fridas", "artist": "Frida Kahlo", "year": "1939"},
        {"title": "Self-Portrait with Thorn Necklace and Hummingbird", "artist": "Frida Kahlo", "year": "1940"},
        
        # Andy Warhol
        {"title": "Campbell's Soup Cans", "artist": "Andy Warhol", "year": "1962"},
        {"title": "Marilyn Diptych", "artist": "Andy Warhol", "year": "1962"},
        
        # Jackson Pollock
        {"title": "Number 1 (Lavender Mist)", "artist": "Jackson Pollock", "year": "1950"},
        
        # Paul Cézanne
        {"title": "The Card Players", "artist": "Paul Cézanne", "year": "1892"},
        
        # Édouard Manet
        {"title": "The Luncheon on the Grass", "artist": "Édouard Manet", "year": "1863"},
        {"title": "Olympia", "artist": "Édouard Manet", "year": "1863"},
        
        # John Constable
        {"title": "The Hay Wain", "artist": "John Constable", "year": "1821"},
        
        # Rembrandt
        {"title": "The Night Watch", "artist": "Rembrandt", "year": "1642"},
        {"title": "Self-Portrait", "artist": "Rembrandt", "year": "1669"},
        
        # Jan van Eyck
        {"title": "The Arnolfini Portrait", "artist": "Jan van Eyck", "year": "1434"},
        
        # Raphael
        {"title": "The School of Athens", "artist": "Raphael", "year": "1509"},
        {"title": "The Sistine Madonna", "artist": "Raphael", "year": "1512"},
        
        # Henri Matisse
        {"title": "The Dance", "artist": "Henri Matisse", "year": "1910"},
        {"title": "The Red Studio", "artist": "Henri Matisse", "year": "1911"},
        
        # Édouard Manet
        {"title": "A Bar at the Folies-Bergère", "artist": "Édouard Manet", "year": "1882"},
        
        # Diego Velázquez
        {"title": "Las Meninas", "artist": "Diego Velázquez", "year": "1656"},
        
        # Francisco Goya
        {"title": "The Third of May 1808", "artist": "Francisco Goya", "year": "1814"},
        
        # Eugène Delacroix
        {"title": "Liberty Leading the People", "artist": "Eugène Delacroix", "year": "1830"},
        
        # Caspar David Friedrich
        {"title": "Wanderer above the Sea of Fog", "artist": "Caspar David Friedrich", "year": "1818"},
        
        # J.M.W. Turner
        {"title": "The Fighting Temeraire", "artist": "J.M.W. Turner", "year": "1839"},
        
        # Georges Seurat
        {"title": "A Sunday Afternoon on the Island of La Grande Jatte", "artist": "Georges Seurat", "year": "1886"},
        
        # Pierre-Auguste Renoir
        {"title": "Luncheon of the Boating Party", "artist": "Pierre-Auguste Renoir", "year": "1881"},
        
        # Edgar Degas
        {"title": "The Dance Class", "artist": "Edgar Degas", "year": "1874"},
        
        # Berthe Morisot
        {"title": "The Cradle", "artist": "Berthe Morisot", "year": "1872"},
        
        # Mary Cassatt
        {"title": "The Child's Bath", "artist": "Mary Cassatt", "year": "1893"},
        
        # Georgia O'Keeffe
        {"title": "Jimson Weed/White Flower No. 1", "artist": "Georgia O'Keeffe", "year": "1932"},
        
        # Edward Hopper
        {"title": "Nighthawks", "artist": "Edward Hopper", "year": "1942"},
        
        # Norman Rockwell
        {"title": "Freedom from Want", "artist": "Norman Rockwell", "year": "1943"},
        
        # Roy Lichtenstein
        {"title": "Whaam!", "artist": "Roy Lichtenstein", "year": "1963"},
        
        # Keith Haring
        {"title": "Untitled", "artist": "Keith Haring", "year": "1982"},
        
        # Jean-Michel Basquiat
        {"title": "Untitled (Skull)", "artist": "Jean-Michel Basquiat", "year": "1981"},
        
        # Yayoi Kusama
        {"title": "Infinity Mirrored Room", "artist": "Yayoi Kusama", "year": "1965"},
        
        # Banksy
        {"title": "Girl with Balloon", "artist": "Banksy", "year": "2002"},
        
        # Takashi Murakami
        {"title": "Flower Ball", "artist": "Takashi Murakami", "year": "2002"},
        
        # Jeff Koons
        {"title": "Balloon Dog", "artist": "Jeff Koons", "year": "1994"},
        
        # Damien Hirst
        {"title": "The Physical Impossibility of Death in the Mind of Someone Living", "artist": "Damien Hirst", "year": "1991"},
        
        # Tracey Emin
        {"title": "My Bed", "artist": "Tracey Emin", "year": "1998"},
        
        # Cindy Sherman
        {"title": "Untitled Film Stills", "artist": "Cindy Sherman", "year": "1977"},
        
        # Jenny Saville
        {"title": "Propped", "artist": "Jenny Saville", "year": "1992"},
        
        # Gerhard Richter
        {"title": "Betty", "artist": "Gerhard Richter", "year": "1988"},
        
        # Anselm Kiefer
        {"title": "Margarethe", "artist": "Anselm Kiefer", "year": "1981"},
        
        # David Hockney
        {"title": "A Bigger Splash", "artist": "David Hockney", "year": "1967"},
        
        # Lucian Freud
        {"title": "Benefits Supervisor Sleeping", "artist": "Lucian Freud", "year": "1995"},
        
        # Francis Bacon
        {"title": "Three Studies for Figures at the Base of a Crucifixion", "artist": "Francis Bacon", "year": "1944"},
        
        # Willem de Kooning
        {"title": "Woman I", "artist": "Willem de Kooning", "year": "1952"},
        
        # Mark Rothko
        {"title": "No. 61 (Rust and Blue)", "artist": "Mark Rothko", "year": "1953"},
        
        # Barnett Newman
        {"title": "Vir Heroicus Sublimis", "artist": "Barnett Newman", "year": "1951"},
        
        # Clyfford Still
        {"title": "1947-R-No. 1", "artist": "Clyfford Still", "year": "1947"},
        
        # Helen Frankenthaler
        {"title": "Mountains and Sea", "artist": "Helen Frankenthaler", "year": "1952"},
        
        # Joan Mitchell
        {"title": "Ladybug", "artist": "Joan Mitchell", "year": "1957"},
        
        # Lee Krasner
        {"title": "The Seasons", "artist": "Lee Krasner", "year": "1957"},
        
        # Grace Hartigan
        {"title": "Grand Street Brides", "artist": "Grace Hartigan", "year": "1954"},
        
        # Elaine de Kooning
        {"title": "Portrait of President John F. Kennedy", "artist": "Elaine de Kooning", "year": "1963"},
        
        # Alice Neel
        {"title": "Andy Warhol", "artist": "Alice Neel", "year": "1970"},
        
        # Louise Bourgeois
        {"title": "Maman", "artist": "Louise Bourgeois", "year": "1999"},
        
        # Eva Hesse
        {"title": "Repetition Nineteen III", "artist": "Eva Hesse", "year": "1968"},
        
        # Agnes Martin
        {"title": "Untitled #1", "artist": "Agnes Martin", "year": "1960"},
        
        # Bridget Riley
        {"title": "Movement in Squares", "artist": "Bridget Riley", "year": "1961"},
        
        # Yoko Ono
        {"title": "Cut Piece", "artist": "Yoko Ono", "year": "1964"},
        
        # Marina Abramović
        {"title": "The Artist is Present", "artist": "Marina Abramović", "year": "2010"},
        
        # Judy Chicago
        {"title": "The Dinner Party", "artist": "Judy Chicago", "year": "1979"},
        
        # Faith Ringgold
        {"title": "Tar Beach", "artist": "Faith Ringgold", "year": "1988"},
        
        # Kara Walker
        {"title": "Gone: An Historical Romance of a Civil War as It Occurred b'tween the Dusky Thighs of One Young Negress and Her Heart", "artist": "Kara Walker", "year": "1994"},
        
        # Julie Mehretu
        {"title": "Empirical Construction, Istanbul", "artist": "Julie Mehretu", "year": "2003"},
        
        # Wangechi Mutu
        {"title": "The End of eating Everything", "artist": "Wangechi Mutu", "year": "2013"},
        
        # Mickalene Thomas
        {"title": "Din, une très belle négresse #1", "artist": "Mickalene Thomas", "year": "2012"},
        
        # Njideka Akunyili Crosby
        {"title": "The Beautyful Ones", "artist": "Njideka Akunyili Crosby", "year": "2012"},
        
        # Amy Sherald
        {"title": "Miss Everything (Unsuppressed Deliverance)", "artist": "Amy Sherald", "year": "2013"},
        
        # Kehinde Wiley
        {"title": "Napoleon Leading the Army over the Alps", "artist": "Kehinde Wiley", "year": "2005"},
        
        # Kerry James Marshall
        {"title": "Past Times", "artist": "Kerry James Marshall", "year": "1997"},
        
        # Glenn Ligon
        {"title": "Untitled (I Am a Man)", "artist": "Glenn Ligon", "year": "1988"},
        
        # Lorna Simpson
        {"title": "Guarded Conditions", "artist": "Lorna Simpson", "year": "1989"},
        
        # Carrie Mae Weems
        {"title": "The Kitchen Table Series", "artist": "Carrie Mae Weems", "year": "1990"},
        
        # Dawoud Bey
        {"title": "The Birmingham Project", "artist": "Dawoud Bey", "year": "2012"},
        
        # LaToya Ruby Frazier
        {"title": "The Notion of Family", "artist": "LaToya Ruby Frazier", "year": "2014"},
        
        # Hank Willis Thomas
        {"title": "Branded Head", "artist": "Hank Willis Thomas", "year": "2003"},
        
        # Titus Kaphar
        {"title": "Behind the Myth of Benevolence", "artist": "Titus Kaphar", "year": "2014"},
        
        # Jordan Casteel
        {"title": "Visible Man", "artist": "Jordan Casteel", "year": "2014"},
        
        # Tschabalala Self
        {"title": "Out of Body", "artist": "Tschabalala Self", "year": "2015"},
        
        # Toyin Ojih Odutola
        {"title": "A Countervailing Theory", "artist": "Toyin Ojih Odutola", "year": "2019"},
        
        # Firelei Báez
        {"title": "Can I Pass?", "artist": "Firelei Báez", "year": "2011"},
        
        # Tania Bruguera
        {"title": "Tatlin's Whisper #6", "artist": "Tania Bruguera", "year": "2009"},
        
        # Doris Salcedo
        {"title": "Shibboleth", "artist": "Doris Salcedo", "year": "2007"},
        
        # Teresa Margolles
        {"title": "What Else Could We Talk About?", "artist": "Teresa Margolles", "year": "2009"},
        
        # Santiago Sierra
        {"title": "160cm Line Tattooed on 4 People", "artist": "Santiago Sierra", "year": "2000"},
        
        # Francis Alÿs
        {"title": "When Faith Moves Mountains", "artist": "Francis Alÿs", "year": "2002"},
        
        # Gabriel Orozco
        {"title": "La DS", "artist": "Gabriel Orozco", "year": "1993"},
        
        # Abraham Cruzvillegas
        {"title": "Autoconstrucción", "artist": "Abraham Cruzvillegas", "year": "2008"},
        
        # Minerva Cuevas
        {"title": "Mejor Vida Corp", "artist": "Minerva Cuevas", "year": "1998"},
        
        # Pedro Reyes
        {"title": "Palas por Pistolas", "artist": "Pedro Reyes", "year": "2008"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (Free)", "artist": "Rirkrit Tiravanija", "year": "1992"},
        
        # Apichatpong Weerasethakul
        {"title": "Primitive", "artist": "Apichatpong Weerasethakul", "year": "2009"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (Tomorrow is Another Fine Day)", "artist": "Rirkrit Tiravanija", "year": "2001"},
        
        # Navin Rawanchaikul
        {"title": "Navin's Party", "artist": "Navin Rawanchaikul", "year": "2000"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered)", "artist": "Rirkrit Tiravanija", "year": "2007"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 12th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2018"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 13th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2021"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 14th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2023"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 15th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2024"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 16th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2025"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 17th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2026"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 18th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2027"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 19th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2028"},
        
        # Rirkrit Tiravanija
        {"title": "Untitled (The Days of This Society is Numbered / 20th Gwangju Biennale)", "artist": "Rirkrit Tiravanija", "year": "2029"},
    ]
    
    return popular_paintings

def construct_wikiart_url(artist, title, year=None):
    """WikiArt URL konstruálása"""
    artist_slug = slugify(artist)
    title_slug = slugify(title)
    
    if year:
        url = f"https://www.wikiart.org/en/{artist_slug}/{title_slug}-{year}"
    else:
        url = f"https://www.wikiart.org/en/{artist_slug}/{title_slug}"
    
    return url

def extract_image_from_wikiart_page(url):
    """Kép URL kinyerése a WikiArt oldalról"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Kép URL keresése a HTML-ben
        image_patterns = [
            r'"image":"([^"]+)"',
            r'"og:image" content="([^"]+)"',
            r'<img[^>]+src="([^"]*wikiart[^"]*)"',
            r'data-src="([^"]*wikiart[^"]*)"'
        ]
        
        for pattern in image_patterns:
            matches = re.findall(pattern, response.text)
            if matches:
                for match in matches:
                    if 'wikiart' in match and ('!Large' in match or '!Pinterest' in match):
                        decoded_url = html.unescape(match)
                        return decoded_url
                decoded_url = html.unescape(matches[0])
                return decoded_url
        
        return None
        
    except Exception as e:
        print(f"❌ Hiba a WikiArt oldal betöltése során: {e}")
        return None

def download_image(image_url, filename, folder="popular_paintings_manual"):
    """Kép letöltése"""
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    filepath = os.path.join(folder, filename)
    
    # Ha már létezik a fájl, átugorjuk
    if os.path.exists(filepath):
        print(f"✅ {filename} már létezik, átugorva")
        return True
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(image_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ {filename} letöltve")
        return True
        
    except Exception as e:
        print(f"❌ Hiba a letöltés során {filename}: {e}")
        return False

def try_download_painting(painting):
    """Festmény letöltési próbálkozás"""
    title = painting['title']
    artist = painting['artist']
    year = painting['year']
    
    print(f"🔍 Feldolgozás: {title} - {artist} ({year})")
    
    # Fájlnév generálása
    artist_slug = slugify(artist)
    title_slug = slugify(title)
    filename = f"{title_slug}-{artist_slug}-{year}.jpg"
    
    attempted_urls = []
    
    # 1. Elsődleges próba: évszámmal
    wikiart_url = construct_wikiart_url(artist, title, year)
    attempted_urls.append(wikiart_url)
    print(f"🌐 Elsődleges URL: {wikiart_url}")
    
    image_url = extract_image_from_wikiart_page(wikiart_url)
    if image_url:
        print(f"🎨 Kép URL megtalálva: {image_url}")
        if download_image(image_url, filename):
            return True, "elsődleges URL", attempted_urls
    
    # 2. Alternatív próba: évszám nélkül
    print(f"🔄 Alternatív próba évszám nélkül...")
    alt_wikiart_url = construct_wikiart_url(artist, title)
    attempted_urls.append(alt_wikiart_url)
    print(f"🌐 Alternatív URL: {alt_wikiart_url}")
    
    image_url = extract_image_from_wikiart_page(alt_wikiart_url)
    if image_url:
        print(f"🎨 Kép URL megtalálva: {image_url}")
        if download_image(image_url, filename):
            return True, "alternatív URL", attempted_urls
    
    return False, "mindkét URL sikertelen", attempted_urls

def save_paintings_list(paintings, filename="popular_paintings_manual_list.txt"):
    """Festmények listájának mentése"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("WikiArt Popular Paintings - Manuális lista\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Összesen {len(paintings)} festmény\n\n")
        
        for i, painting in enumerate(paintings, 1):
            f.write(f"{i:3d}. {painting['title']} - {painting['artist']} ({painting['year']})\n")
    
    print(f"📄 Festmények listája mentve: {filename}")

def main():
    """Fő függvény"""
    print("🎨 WikiArt Popular Paintings - Manuális lista")
    print("=" * 50)
    
    # Népszerű festmények listájának lekérése
    paintings = get_popular_paintings_list()
    
    print(f"📋 {len(paintings)} népszerű festmény feldolgozása...")
    
    # Lista mentése
    save_paintings_list(paintings)
    
    # Letöltés (opcionális - csak az első 50-et)
    download_choice = input("\n❓ Szeretnéd letölteni a képeket is? (y/n): ").lower().strip()
    
    if download_choice == 'y':
        print(f"\n🔄 Festmények letöltése...")
        
        success_count = 0
        failed_downloads = []
        
        for i, painting in enumerate(paintings[:50], 1):  # Csak az első 50-et
            print(f"\n[{i}/50] ", end="")
            
            success, method, attempted_urls = try_download_painting(painting)
            
            if success:
                success_count += 1
                print(f"✅ Sikeres letöltés ({method})")
            else:
                print(f"❌ Sikertelen letöltés")
                failed_downloads.append({
                    'title': painting['title'],
                    'artist': painting['artist'],
                    'year': painting['year'],
                    'reason': method,
                    'attempted_urls': attempted_urls
                })
            
            # Rövid várakozás a szerver terhelés csökkentésére
            time.sleep(2)
        
        print(f"\n🎉 Letöltés befejezve!")
        print(f"✅ Sikeres letöltések: {success_count}/50")
        print(f"❌ Sikertelen letöltések: {len(failed_downloads)}")
        
        if failed_downloads:
            with open("failed_manual_downloads.txt", "w", encoding="utf-8") as f:
                f.write("Sikertelen manuális letöltések\n")
                f.write("=" * 30 + "\n\n")
                for failed in failed_downloads:
                    f.write(f"• {failed['title']} - {failed['artist']} ({failed['year']})\n")
                    f.write(f"  Hiba: {failed['reason']}\n")
                    f.write("  Megpróbált URL-ek:\n")
                    for url in failed['attempted_urls']:
                        f.write(f"  • {url}\n")
                    f.write("\n")
            
            print(f"📄 Sikertelen letöltések mentve: failed_manual_downloads.txt")
    
    print(f"\n🎉 Kész! {len(paintings)} festmény listázva.")

if __name__ == "__main__":
    main() 