#!/usr/bin/env python3
"""
Spotify OAuth 2.0 Autentikáció
"""

import requests
import json
import time
from urllib.parse import quote

# Spotify API beállítások
CLIENT_ID = "b288da1cbde34062aba6724de8531c46"
CLIENT_SECRET = "bd3b3835e63744149f580ebb919cbdd3"
REDIRECT_URI = "http://127.0.0.1:8509/callback"

# Spotify API endpoints
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

def get_authorization_url():
    """
    Generálja az autorizációs URL-t
    """
    scopes = [
        "user-read-private",
        "user-read-email",
        "playlist-read-private",
        "playlist-read-collaborative"
    ]
    
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(scopes),
        'show_dialog': 'true'
    }
    
    auth_url = f"{AUTH_URL}?client_id={params['client_id']}&response_type={params['response_type']}&redirect_uri={quote(params['redirect_uri'])}&scope={quote(params['scope'])}&show_dialog={params['show_dialog']}"
    
    return auth_url

def get_access_token(authorization_code):
    """
    Megszerzi az access tokent az authorization code alapján
    """
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    try:
        response = requests.post(TOKEN_URL, data=data, headers=headers)
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            print(f"Hiba a token beszerzésekor: {response.status_code}")
            print(f"Válasz: {response.text}")
            return None
            
    except Exception as e:
        print(f"Hiba: {e}")
        return None

def search_spotify_track(access_token, composer, piece_name):
    """
    Keres egy zeneművet a Spotify API-n keresztül
    """
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    params = {
        'q': f"{composer} {piece_name}",
        'type': 'track',
        'limit': 5,
        'market': 'HU'
    }
    
    try:
        response = requests.get(SEARCH_URL, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            
            if tracks:
                track = tracks[0]
                track_id = track['id']
                track_name = track['name']
                artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown"
                
                embed_url = f"https://open.spotify.com/embed/track/{track_id}"
                
                return {
                    'embed_url': embed_url,
                    'track_name': track_name,
                    'artist_name': artist_name,
                    'confidence': 'high' if composer.lower() in artist_name.lower() else 'medium'
                }
        
        return None
        
    except Exception as e:
        print(f"Hiba a keresés során: {e}")
        return None

def main():
    """
    Fő függvény - OAuth folyamat
    """
    print("🎵 Spotify OAuth 2.0 Autentikáció")
    print("=" * 40)
    
    # 1. Autorizációs URL generálása
    auth_url = get_authorization_url()
    print(f"1. Nyisd meg ezt a linket a böngészőben:")
    print(f"   {auth_url}")
    print()
    
    # 2. Felhasználó beírja az authorization code-ot
    auth_code = input("2. Add meg az authorization code-ot: ").strip()
    
    if not auth_code:
        print("❌ Nincs megadva authorization code!")
        return
    
    # 3. Access token beszerzése
    print("3. Access token beszerzése...")
    access_token = get_access_token(auth_code)
    
    if not access_token:
        print("❌ Nem sikerült access tokent beszerezni!")
        return
    
    print("✅ Access token sikeresen beszerezve!")
    
    # 4. Teszt keresés
    print("4. Teszt keresés...")
    test_result = search_spotify_track(access_token, "Beethoven", "Symphony 5")
    
    if test_result:
        print(f"✅ Teszt sikeres: {test_result['artist_name']} - {test_result['track_name']}")
        print(f"   Link: {test_result['embed_url']}")
    else:
        print("❌ Teszt sikertelen")
    
    return access_token

if __name__ == "__main__":
    main() 