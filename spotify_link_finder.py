#!/usr/bin/env python3
"""
Spotify Link Finder for Classical Music Questions
Keresi a megfelelő Spotify track linkeket a komolyzenei darabokhoz
"""

import requests
import json
import time
from urllib.parse import quote

def search_spotify_track(composer, piece_name):
    """
    Keres egy zeneművet a Spotify-n a zeneszerző és a darab neve alapján
    """
    # Spotify Web API endpoint (nem igényel API kulcsot)
    search_url = "https://api.spotify.com/v1/search"
    
    # Keresési kifejezés összeállítása
    query = f"{composer} {piece_name}"
    
    # URL paraméterek
    params = {
        'q': query,
        'type': 'track',
        'limit': 5,  # Top 5 találat
        'market': 'HU'
    }
    
    try:
        # Kérés küldése
        response = requests.get(search_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('tracks', {}).get('items', [])
            
            if tracks:
                # Visszaadjuk az első (legjobb) találatot
                track = tracks[0]
                track_id = track['id']
                track_name = track['name']
                artist_name = track['artists'][0]['name'] if track['artists'] else "Unknown"
                
                # Spotify embed URL generálása
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

def get_classical_music_pieces():
    """
    Visszaadja a komolyzenei darabok listáját a classical_music_questions.py-ból
    """
    from classical_music_questions import CLASSICAL_MUSIC_QUESTIONS
    
    pieces = []
    for question in CLASSICAL_MUSIC_QUESTIONS:
        explanation = question['explanation']
        # Az explanation formátuma: "Zeneszerző: Darab neve"
        if ': ' in explanation:
            composer, piece = explanation.split(': ', 1)
            pieces.append({
                'composer': composer.strip(),
                'piece': piece.strip(),
                'question_index': CLASSICAL_MUSIC_QUESTIONS.index(question)
            })
    
    return pieces

def main():
    """
    Fő függvény: keres minden darabhoz Spotify linket
    """
    print("🎵 Spotify Link Finder - Komolyzenei Darabok")
    print("=" * 50)
    
    pieces = get_classical_music_pieces()
    results = []
    
    for i, piece in enumerate(pieces):
        print(f"\n{i+1}/{len(pieces)}: {piece['composer']} - {piece['piece']}")
        
        # Spotify keresés
        result = search_spotify_track(piece['composer'], piece['piece'])
        
        if result:
            print(f"✅ Találat: {result['artist_name']} - {result['track_name']}")
            print(f"   Link: {result['embed_url']}")
            
            results.append({
                'question_index': piece['question_index'],
                'composer': piece['composer'],
                'piece': piece['piece'],
                'spotify_embed': result['embed_url'],
                'found_track': result['track_name'],
                'found_artist': result['artist_name'],
                'confidence': result['confidence']
            })
        else:
            print(f"❌ Nincs találat")
            results.append({
                'question_index': piece['question_index'],
                'composer': piece['composer'],
                'piece': piece['piece'],
                'spotify_embed': None,
                'found_track': None,
                'found_artist': None,
                'confidence': 'none'
            })
        
        # Késleltetés a rate limiting elkerülése érdekében
        time.sleep(1)
    
    # Eredmények mentése
    with open('spotify_search_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n" + "=" * 50)
    print(f"Keresés befejezve!")
    print(f"Találatok: {len([r for r in results if r['spotify_embed']])}/{len(results)}")
    print(f"Eredmények mentve: spotify_search_results.json")
    
    return results

if __name__ == "__main__":
    main() 