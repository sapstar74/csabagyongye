#!/usr/bin/env python3
"""
Magyar zenekarok keresése Spotify Web API-val
"""

import requests
import json
import time
import base64
from urllib.parse import quote

# Import konfiguráció
try:
    from spotify_api_config import (
        SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_API_BASE_URL, 
        SPOTIFY_AUTH_URL, DEFAULT_MARKET, SEARCH_LIMIT, RATE_LIMIT_DELAY,
        MAGYAR_ZENEKAROK, NAME_MAPPINGS, KNOWN_HUNGARIAN_ARTISTS,
        validate_credentials, print_setup_instructions
    )
except ImportError:
    print("❌ spotify_api_config.py fájl nem található!")
    print("Kérlek futtasd le: python spotify_api_config.py")
    exit(1)

class SpotifyAPI:
    def __init__(self):
        self.client_id = SPOTIFY_CLIENT_ID
        self.client_secret = SPOTIFY_CLIENT_SECRET
        self.access_token = None
        self.base_url = SPOTIFY_API_BASE_URL
    
    def get_access_token(self):
        """Spotify access token beszerzése"""
        if self.access_token:
            return self.access_token
        
        # Client credentials flow
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {"grant_type": "client_credentials"}
        
        try:
            response = requests.post(SPOTIFY_AUTH_URL, headers=headers, data=data)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data["access_token"]
            return self.access_token
        except Exception as e:
            print(f"❌ Hiba az access token beszerzésekor: {e}")
            return None
    
    def search_artist(self, artist_name, market=DEFAULT_MARKET):
        """Zenekar keresése Spotify-on"""
        if not self.access_token:
            self.get_access_token()
        
        if not self.access_token:
            return None
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        # Keresési paraméterek
        params = {
            "q": f"{artist_name}",
            "type": "artist",
            "market": market,
            "limit": SEARCH_LIMIT
        }
        
        try:
            response = requests.get(f"{self.base_url}/search", headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data["artists"]["items"]:
                # Visszaadjuk az első találatot
                artist = data["artists"]["items"][0]
                return {
                    "id": artist["id"],
                    "name": artist["name"],
                    "popularity": artist["popularity"],
                    "followers": artist["followers"]["total"],
                    "spotify_url": f"https://open.spotify.com/artist/{artist['id']}"
                }
            
            return None
            
        except Exception as e:
            print(f"❌ Hiba a keresés során ({artist_name}): {e}")
            return None

def search_hungarian_artists():
    """Magyar zenekarok keresése"""
    
    # Ellenőrizzük a credentials-eket
    if not validate_credentials():
        print("❌ Spotify API credentials nincsenek beállítva!")
        print_setup_instructions()
        return
    
    # Spotify API inicializálása
    spotify = SpotifyAPI()
    
    results = {}
    success_count = 0
    fallback_count = 0
    
    print("🎵 Magyar zenekarok keresése Spotify API-val...")
    print(f"🔍 {len(MAGYAR_ZENEKAROK)} zenekar keresése...")
    
    for i, zenekar in enumerate(MAGYAR_ZENEKAROK, 1):
        print(f"[{i}/{len(MAGYAR_ZENEKAROK)}] Keresés: {zenekar}")
        
        # Try original name first
        artist_data = spotify.search_artist(zenekar)
        
        # If not found, try mapped name
        if not artist_data and zenekar in NAME_MAPPINGS:
            mapped_name = NAME_MAPPINGS[zenekar]
            print(f"  🔄 Próbálom: {mapped_name}")
            artist_data = spotify.search_artist(mapped_name)
        
        if artist_data:
            print(f"✅ {zenekar}: {artist_data['spotify_url']} (Popularity: {artist_data['popularity']})")
            results[zenekar] = artist_data['spotify_url']
            success_count += 1
        else:
            # Fallback link
            fallback_link = "https://open.spotify.com/artist/0YqQvRjqNXAv2K5FqS9cdO"
            print(f"❌ {zenekar}: Fallback link")
            results[zenekar] = fallback_link
            fallback_count += 1
        
        time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
    
    # Eredmények mentése
    with open('magyar_zenekarok_spotify_api_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    # Python fájl generálása
    python_code = "# Magyar zenekarok Spotify linkjei (API keresés)\n"
    python_code += "MAGYAR_ZENEKAROK_SPOTIFY_API_LINKS = {\n"
    
    for zenekar, link in results.items():
        python_code += f'    "{zenekar}": "{link}",\n'
    
    python_code += "}\n"
    
    with open('magyar_zenekarok_spotify_api_links.py', 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"\n📁 Eredmények mentve: magyar_zenekarok_spotify_api_results.json")
    print(f"✅ {success_count} valódi link találva")
    print(f"❌ {fallback_count} fallback link")
    print(f"📁 Python fájl létrehozva: magyar_zenekarok_spotify_api_links.py")
    print("🎉 Keresés befejezve!")
    
    print("\n📊 Összefoglaló:")
    for zenekar, link in results.items():
        status = "✅" if "0YqQvRjqNXAv2K5FqS9cdO" not in link else "❌"
        print(f"{status} {zenekar}: {link}")

def manual_spotify_search():
    """Manuális Spotify keresés ismert ID-kkel"""
    
    print("🔍 Manuális Spotify keresés ismert magyar zenekarokkal...")
    
    results = {}
    success_count = 0
    
    for artist_name, artist_id in KNOWN_HUNGARIAN_ARTISTS.items():
        if artist_id != "0YqQvRjqNXAv2K5FqS9cdO":
            spotify_url = f"https://open.spotify.com/artist/{artist_id}"
            print(f"✅ {artist_name}: {spotify_url}")
            results[artist_name] = spotify_url
            success_count += 1
        else:
            fallback_url = "https://open.spotify.com/artist/0YqQvRjqNXAv2K5FqS9cdO"
            print(f"❌ {artist_name}: Fallback link")
            results[artist_name] = fallback_url
    
    print(f"\n✅ {success_count} valódi Spotify link találva")
    return results

if __name__ == "__main__":
    print("🎵 Magyar zenekarok Spotify keresése")
    print("1. Spotify API keresés (credentials szükséges)")
    print("2. Manuális keresés ismert ID-kkel")
    print("3. Spotify API beállítási utasítások")
    
    choice = input("\nVálassz opciót (1-3): ").strip()
    
    if choice == "1":
        search_hungarian_artists()
    elif choice == "2":
        results = manual_spotify_search()
        
        # Eredmények mentése
        with open('magyar_zenekarok_manual_results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print("📁 Eredmények mentve: magyar_zenekarok_manual_results.json")
    elif choice == "3":
        print_setup_instructions()
    else:
        print("❌ Érvénytelen választás!") 