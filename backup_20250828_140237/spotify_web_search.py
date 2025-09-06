#!/usr/bin/env python3
"""
Spotify Web API keresés komolyzenei darabokhoz
Megpróbálja megtalálni a megfelelő Spotify linkeket
"""

import requests
import json
import time
from urllib.parse import quote

def search_spotify_web(composer, piece_name):
    """
    Keres a Spotify Web API-n keresztül
    """
    # Spotify Web API endpoint
    search_url = "https://api.spotify.com/v1/search"
    
    # Keresési kifejezés
    query = f"{composer} {piece_name}"
    
    # Headers (néha működik API kulcs nélkül is)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Paraméterek
    params = {
        'q': query,
        'type': 'track',
        'limit': 5,
        'market': 'HU'
    }
    
    try:
        response = requests.get(search_url, params=params, headers=headers)
        print(f"Status: {response.status_code}")
        
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
        print(f"Hiba: {e}")
        return None

def get_classical_pieces():
    """
    Visszaadja a komolyzenei darabok listáját
    """
    from classical_music_questions import CLASSICAL_MUSIC_QUESTIONS
    
    pieces = []
    for question in CLASSICAL_MUSIC_QUESTIONS:
        explanation = question['explanation']
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
    Fő függvény
    """
    print("🎵 Spotify Web API Keresés")
    print("=" * 40)
    
    pieces = get_classical_pieces()
    results = []
    
    for i, piece in enumerate(pieces[:10]):  # Csak az első 10-et teszteljük
        print(f"\n{i+1}/10: {piece['composer']} - {piece['piece']}")
        
        result = search_spotify_web(piece['composer'], piece['piece'])
        
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
        
        time.sleep(2)  # Késleltetés
    
    print(f"\n" + "=" * 40)
    print(f"Keresés befejezve!")
    print(f"Találatok: {len([r for r in results if r['spotify_embed']])}/{len(results)}")
    
    return results

if __name__ == "__main__":
    main() 