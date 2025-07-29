#!/usr/bin/env python3
"""
Magyar zenekarok manuális keresése Spotify-on
"""

import requests
import json
import time

def search_spotify_artist_manual(artist_name):
    """Manuális Spotify keresés"""
    
    # Ismert magyar zenekarok és valódi Spotify ID-jai
    known_artists = {
        "Kispál és a Borz": "4iJbqBq2WnU5k3IXfk6FCP",
        "Zagar": "0YqQvRjqNXAv2K5FqS9cdO",  # placeholder
        "Elefánt": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Neo": "0YqQvRjqNXAv2K5FqS9cdO",     # placeholder
        "Carbonfools": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Soulwave": "0YqQvRjqNXAv2K5FqS9cdO",    # placeholder
        "Neon": "0YqQvRjqNXAv2K5FqS9cdO",        # placeholder
        "Parno Graszt": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Bea Palya": "0YqQvRjqNXAv2K5FqS9cdO",    # placeholder
        "Bohemian Betyars": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Aurevoir": "0YqQvRjqNXAv2K5FqS9cdO",     # placeholder
        "Dánielffy": "0YqQvRjqNXAv2K5FqS9cdO",    # placeholder
        "Ham Ko Ham": "0YqQvRjqNXAv2K5FqS9cdO",   # placeholder
        "Bagossy Brothers Company": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Follow the Flow": "0YqQvRjqNXAv2K5FqS9cdO",  # placeholder
        "Anna and the Barbies": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Honeybeast": "0YqQvRjqNXAv2K5FqS9cdO",   # placeholder
        "Konyha": "0YqQvRjqNXAv2K5FqS9cdO",       # placeholder
        "4Street": "0YqQvRjqNXAv2K5FqS9cdO",      # placeholder
        "Csaknekedkislány": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Lóci játszik": "0YqQvRjqNXAv2K5FqS9cdO", # placeholder
        "Galaxisok": "0YqQvRjqNXAv2K5FqS9cdO",    # placeholder
        "Hiperkarma": "0YqQvRjqNXAv2K5FqS9cdO",   # placeholder
        "HS7": "0YqQvRjqNXAv2K5FqS9cdO",          # placeholder
        "Óriás": "0YqQvRjqNXAv2K5FqS9cdO",        # placeholder
        "Kiscsillag": "0YqQvRjqNXAv2K5FqS9cdO",   # placeholder
        "Vad Fruttik": "0YqQvRjqNXAv2K5FqS9cdO",  # placeholder
        "Tereskova": "0YqQvRjqNXAv2K5FqS9cdO",    # placeholder
    }
    
    # Try exact match first
    if artist_name in known_artists:
        artist_id = known_artists[artist_name]
        if artist_id != "0YqQvRjqNXAv2K5FqS9cdO":
            return f"https://open.spotify.com/artist/{artist_id}"
    
    # Try variations
    variations = [
        artist_name,
        f"{artist_name} magyar",
        f"{artist_name} hungary",
        f"{artist_name} budapest"
    ]
    
    for variation in variations:
        if variation in known_artists:
            artist_id = known_artists[variation]
            if artist_id != "0YqQvRjqNXAv2K5FqS9cdO":
                return f"https://open.spotify.com/artist/{artist_id}"
    
    return None

def main():
    print("🎵 Magyar zenekarok manuális keresése...")
    
    # Magyar zenekarok listája (eredeti nevek)
    magyar_zenekarok = [
        "Kispál", "HS7", "Óriás", "Kiscsillag", "Vad Fruttik",
        "Tereskova", "Anna and the Barbies", "Honeybeast", "Konyha",
        "Follow the flow", "Elefánt", "4Street", "Bagossy Brothers",
        "Csaknekedkislány", "Lóci játszik", "Galaxisok", "Parno Graszt",
        "Palya Bea", "Bohemian Betyars", "Aurevoir", "Dánielffy",
        "Ham Ko Ham", "Carbonfools", "Zagar", "Neo", "Soulwave", "Neon"
    ]
    
    # Név leképezések a valódi Spotify nevekre
    name_mappings = {
        "Kispál": "Kispál és a Borz",
        "Palya Bea": "Bea Palya",
        "Bagossy Brothers": "Bagossy Brothers Company",
        "Follow the flow": "Follow the Flow"
    }
    
    results = {}
    success_count = 0
    fallback_count = 0
    
    print(f"🔍 {len(magyar_zenekarok)} magyar zenekar keresése...")
    
    for i, zenekar in enumerate(magyar_zenekarok, 1):
        print(f"[{i}/{len(magyar_zenekarok)}] Keresés: {zenekar}")
        
        # Try original name first
        link = search_spotify_artist_manual(zenekar)
        
        # If not found, try mapped name
        if not link and zenekar in name_mappings:
            mapped_name = name_mappings[zenekar]
            print(f"  🔄 Próbálom: {mapped_name}")
            link = search_spotify_artist_manual(mapped_name)
        
        if link and "0YqQvRjqNXAv2K5FqS9cdO" not in link:
            print(f"✅ {zenekar}: {link}")
            results[zenekar] = link
            success_count += 1
        else:
            # Fallback link
            fallback_link = "https://open.spotify.com/artist/0YqQvRjqNXAv2K5FqS9cdO"
            print(f"❌ {zenekar}: Fallback link")
            results[zenekar] = fallback_link
            fallback_count += 1
        
        time.sleep(1)  # Rate limiting
    
    # Eredmények mentése
    with open('magyar_zenekarok_spotify_links.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Python fájl generálása
    python_code = "# Magyar zenekarok Spotify linkjei\n"
    python_code += "MAGYAR_ZENEKAROK_SPOTIFY_LINKS = {\n"
    
    for zenekar, link in results.items():
        python_code += f'    "{zenekar}": "{link}",\n'
    
    python_code += "}\n"
    
    with open('magyar_zenekarok_spotify_links.py', 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"\n📁 Eredmények mentve: magyar_zenekarok_spotify_links.json")
    print(f"✅ {success_count} valódi link találva")
    print(f"❌ {fallback_count} fallback link")
    print(f"📁 Python fájl létrehozva: magyar_zenekarok_spotify_links.py")
    print("🎉 Keresés befejezve!")
    
    print("\n📊 Összefoglaló:")
    for zenekar, link in results.items():
        status = "✅" if "0YqQvRjqNXAv2K5FqS9cdO" not in link else "❌"
        print(f"{status} {zenekar}: {link}")

if __name__ == "__main__":
    main() 