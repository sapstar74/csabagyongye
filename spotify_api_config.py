#!/usr/bin/env python3
"""
Spotify API konfiguráció
"""

# Spotify API credentials
# Kérlek add meg a saját Client ID és Client Secret értékeidet
# Ezeket a Spotify Developer Dashboard-on találod: https://developer.spotify.com/dashboard

SPOTIFY_CLIENT_ID = "4d1cd07e3eb14487b6bc714c9d94cf89"
SPOTIFY_CLIENT_SECRET = "6aa54bf8edad42b5b925b7dd3becab90"

# API beállítások
SPOTIFY_API_BASE_URL = "https://api.spotify.com/v1"
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/api/token"

# Keresési beállítások
DEFAULT_MARKET = "HU"  # Magyarország
SEARCH_LIMIT = 5  # Találatok száma keresésenként
RATE_LIMIT_DELAY = 1  # Másodpercek a kérések között

# Magyar zenekarok listája
MAGYAR_ZENEKAROK = [
    "Kispál", "HS7", "Óriás", "Kiscsillag", "Vad Fruttik",
    "Tereskova", "Anna and the Barbies", "Honeybeast", "Konyha",
    "Follow the flow", "Elefánt", "4Street", "Bagossy Brothers",
    "Csaknekedkislány", "Lóci játszik", "Galaxisok", "Parno Graszt",
    "Palya Bea", "Bohemian Betyars", "Aurevoir", "Dánielffy",
    "Ham Ko Ham", "Carbonfools", "Zagar", "Neo", "Soulwave", "Neon",
    # További ismert magyar zenekarok
    "Quimby", "Tankcsapda", "P. Mobil", "Republic", "Bonanza Banzai", "Korai Öröm",
    "Kispál és a Borz", "Bea Palya", "Bagossy Brothers Company", "Follow the Flow"
]

# Név leképezések a valódi Spotify nevekre
NAME_MAPPINGS = {
    "Kispál": "Kispál és a Borz",
    "Palya Bea": "Bea Palya",
    "Bagossy Brothers": "Bagossy Brothers Company",
    "Follow the flow": "Follow the Flow"
}

# Ismert magyar zenekarok és valódi Spotify ID-jai
KNOWN_HUNGARIAN_ARTISTS = {
    "Kispál és a Borz": "4iJbqBq2WnU5k3IXfk6FCP",
    # További ismert ID-k ide kerülnek majd
}

def validate_credentials():
    """Ellenőrzi, hogy a credentials be vannak-e állítva"""
    if (SPOTIFY_CLIENT_ID == "YOUR_CLIENT_ID_HERE" or 
        SPOTIFY_CLIENT_SECRET == "YOUR_CLIENT_SECRET_HERE"):
        return False
    return True

def print_setup_instructions():
    """Kiírja a beállítási utasításokat"""
    print("🎵 Spotify API beállítási utasítások:")
    print("=" * 50)
    print("1. Menj a Spotify Developer Dashboard-ra:")
    print("   https://developer.spotify.com/dashboard")
    print()
    print("2. Jelentkezz be a Spotify fiókoddal")
    print()
    print("3. Kattints a 'Create App' gombra")
    print()
    print("4. Töltsd ki az adatokat:")
    print("   - App name: Magyar Zenekarok Quiz")
    print("   - App description: Quiz app magyar zenekarok Spotify linkjeivel")
    print("   - Redirect URI: http://localhost:8888/callback")
    print("   - Website: http://localhost:8888")
    print()
    print("5. Az alkalmazás létrehozása után másold ki:")
    print("   - Client ID")
    print("   - Client Secret")
    print()
    print("6. Írd be ezeket a spotify_api_config.py fájlba:")
    print("   SPOTIFY_CLIENT_ID = 'a_sajat_client_id_d'")
    print("   SPOTIFY_CLIENT_SECRET = 'a_sajat_client_secret_d'")
    print()
    print("7. Futtasd újra a keresési scriptet!")
    print("=" * 50)

if __name__ == "__main__":
    if not validate_credentials():
        print_setup_instructions()
    else:
        print("✅ Spotify API credentials be vannak állítva!")
        print(f"Client ID: {SPOTIFY_CLIENT_ID[:10]}...")
        print(f"Client Secret: {SPOTIFY_CLIENT_SECRET[:10]}...") 