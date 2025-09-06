#!/usr/bin/env python3
"""
Spotify API teszt a megadott authorization code-dal
"""

import requests
import json
import time
from urllib.parse import quote

# Spotify API beállítások
CLIENT_ID = "b288da1cbde34062aba6724de8531c46"
CLIENT_SECRET = "bd3b3835e63744149f580ebb919cbdd3"
REDIRECT_URI = "http://127.0.0.1:8509/callback"

# Megadott authorization code
AUTH_CODE = None

# Spotify API endpoints
TOKEN_URL = "https://accounts.spotify.com/api/token"
SEARCH_URL = "https://api.spotify.com/v1/search"

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

def search_all_classical_pieces(access_token):
    """
    Keres minden komolyzenei darabhoz Spotify linket
    """
    from classical_music_questions import CLASSICAL_MUSIC_QUESTIONS
    
    results = []
    
    for i, question in enumerate(CLASSICAL_MUSIC_QUESTIONS):
        explanation = question['explanation']
        if ': ' in explanation:
            composer, piece = explanation.split(': ', 1)
            
            print(f"\n{i+1}/{len(CLASSICAL_MUSIC_QUESTIONS)}: {composer} - {piece}")
            
            result = search_spotify_track(access_token, composer, piece)
            
            if result:
                print(f"✅ Találat: {result['artist_name']} - {result['track_name']}")
                print(f"   Link: {result['embed_url']}")
                
                results.append({
                    'question_index': i,
                    'composer': composer,
                    'piece': piece,
                    'spotify_embed': result['embed_url'],
                    'found_track': result['track_name'],
                    'found_artist': result['artist_name'],
                    'confidence': result['confidence']
                })
            else:
                print(f"❌ Nincs találat")
                results.append({
                    'question_index': i,
                    'composer': composer,
                    'piece': piece,
                    'spotify_embed': None,
                    'found_track': None,
                    'found_artist': None,
                    'confidence': 'none'
                })
            
            time.sleep(1)  # Késleltetés a rate limiting elkerülése érdekében
    
    return results

def main():
    """
    Fő függvény
    """
    print("🎵 Spotify API Teszt Authorization Code-dal")
    print("=" * 50)
    
    # 1. Authorization code bekérése
    global AUTH_CODE
    AUTH_CODE = input("Add meg az authorization code-ot (amit a Spotify OAuth flow-ból kapsz): ").strip()
    if not AUTH_CODE:
        print("❌ Nincs megadva authorization code!")
        return
    
    # 2. Access token beszerzése
    print("1. Access token beszerzése...")
    access_token = get_access_token(AUTH_CODE)
    
    if not access_token:
        print("❌ Nem sikerült access tokent beszerezni!")
        return
    
    print("✅ Access token sikeresen beszerezve!")
    
    # 3. Teszt keresés
    print("\n2. Teszt keresés...")
    test_result = search_spotify_track(access_token, "Beethoven", "Symphony 5")
    
    if test_result:
        print(f"✅ Teszt sikeres: {test_result['artist_name']} - {test_result['track_name']}")
        print(f"   Link: {test_result['embed_url']}")
    else:
        print("❌ Teszt sikertelen")
        return
    
    # 4. Minden komolyzenei darab keresése
    print("\n3. Minden komolyzenei darab keresése...")
    results = search_all_classical_pieces(access_token)
    
    # 5. Eredmények mentése
    with open('spotify_search_results_final.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 50)
    print(f"Keresés befejezve!")
    print(f"Találatok: {len([r for r in results if r['spotify_embed']])}/{len(results)}")
    print(f"Eredmények mentve: spotify_search_results_final.json")
    
    return results

if __name__ == "__main__":
    main() 