#!/usr/bin/env python3
"""
Spotify Playlist Manager - One Hit Wonders és egyéb playlistek kezelése
"""

import requests
import json
import random
import time
from typing import List, Dict, Optional
from spotify_api_config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_AUTH_URL

class SpotifyPlaylistManager:
    def __init__(self):
        self.access_token = None
        self.base_url = "https://api.spotify.com/v1"
        
    def get_access_token(self) -> bool:
        """Spotify access token beszerzése"""
        try:
            auth_response = requests.post(SPOTIFY_AUTH_URL, {
                'grant_type': 'client_credentials',
                'client_id': SPOTIFY_CLIENT_ID,
                'client_secret': SPOTIFY_CLIENT_SECRET,
            })
            
            if auth_response.status_code == 200:
                auth_data = auth_response.json()
                self.access_token = auth_data['access_token']
                return True
            else:
                print(f"Hiba az access token beszerzésénél: {auth_response.status_code}")
                return False
                
        except Exception as e:
            print(f"Hiba az access token beszerzésénél: {e}")
            return False
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """Playlist dalainak lekérése"""
        if not self.access_token:
            if not self.get_access_token():
                return []
        
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        
        tracks = []
        offset = 0
        limit = 100
        
        while True:
            url = f"{self.base_url}/playlists/{playlist_id}/tracks"
            params = {
                'offset': offset,
                'limit': limit,
                'market': 'HU'
            }
            
            try:
                response = requests.get(url, headers=headers, params=params)
                
                if response.status_code == 200:
                    data = response.json()
                    items = data.get('items', [])
                    
                    if not items:
                        break
                    
                    for item in items:
                        track = item.get('track')
                        if track and track.get('preview_url'):
                            track_info = {
                                'id': track['id'],
                                'name': track['name'],
                                'artist': track['artists'][0]['name'] if track['artists'] else 'Unknown',
                                'preview_url': track['preview_url'],
                                'external_url': track['external_urls']['spotify'],
                                'album': track['album']['name'] if track['album'] else 'Unknown'
                            }
                            tracks.append(track_info)
                    
                    offset += limit
                    
                    # Ha nincs több dal, kilépünk
                    if len(items) < limit:
                        break
                        
                else:
                    print(f"Hiba a playlist lekérdezésénél: {response.status_code}")
                    break
                    
            except Exception as e:
                print(f"Hiba a playlist lekérdezésénél: {e}")
                break
        
        return tracks
    
    def get_random_tracks_from_playlist(self, playlist_id: str, count: int = 10) -> List[Dict]:
        """Random dalok kiválasztása playlistből"""
        tracks = self.get_playlist_tracks(playlist_id)
        
        if not tracks:
            return []
        
        # Random kiválasztás, de maximum a rendelkezésre álló dalok számát
        count = min(count, len(tracks))
        return random.sample(tracks, count)
    
    def get_extended_preview_url(self, preview_url: str, duration: int = 90) -> str:
        """90 másodperces preview URL generálása (ha lehetséges)"""
        if not preview_url:
            return preview_url
        
        # A Spotify preview URL-ek alapértelmezetten 30 másodpercesek
        # Sajnos a Spotify API nem támogatja a hosszabb preview-okat
        # De visszaadjuk az eredeti URL-t, és a frontend kezeli majd
        return preview_url
    
    def generate_question_options(self, correct_artist: str, all_tracks: List[Dict]) -> List[str]:
        """Válaszopciók generálása a helyes előadóval együtt"""
        options = [correct_artist]
        
        # Más előadók kiválasztása random
        other_artists = [track['artist'] for track in all_tracks if track['artist'] != correct_artist]
        
        if len(other_artists) >= 3:
            # 3 random másik előadó
            random_artists = random.sample(other_artists, 3)
            options.extend(random_artists)
        else:
            # Ha nincs elég másik előadó, ismert One Hit Wonders előadókat adunk hozzá
            famous_one_hit_wonders = [
                "Vanilla Ice", "Gotye", "Soft Cell", "Mark Morrison", 
                "Crazy Town", "Rednex", "Spin Doctors", "The Knack",
                "Whigfield", "Baha Men", "Snow", "Caesars"
            ]
            
            for artist in famous_one_hit_wonders:
                if artist not in options and len(options) < 4:
                    options.append(artist)
        
        # Random sorrendbe rendezés
        random.shuffle(options)
        return options

# One Hit Wonders playlist ID
ONE_HIT_WONDERS_PLAYLIST_ID = "37i9dQZF1DX0Ew6u9sRtTY"

def get_one_hit_wonders_questions(count: int = 20) -> List[Dict]:
    """One Hit Wonders kérdések generálása"""
    manager = SpotifyPlaylistManager()
    
    # Random dalok lekérése a playlistből
    random_tracks = manager.get_random_tracks_from_playlist(ONE_HIT_WONDERS_PLAYLIST_ID, count * 2)
    
    if not random_tracks:
        print("Nem sikerült dalokat lekérni a Spotify playlistből")
        return []
    
    # Összes dal lekérése a válaszopciók generálásához
    all_tracks = manager.get_playlist_tracks(ONE_HIT_WONDERS_PLAYLIST_ID)
    
    questions = []
    
    for i, track in enumerate(random_tracks[:count]):
        # Válaszopciók generálása
        options = manager.generate_question_options(track['artist'], all_tracks)
        
        # Helyes válasz indexének meghatározása
        correct_index = options.index(track['artist'])
        
        question = {
            "question": f"Ki az előadó a '{track['name']}' című dalban?",
            "spotify_track_id": track['id'],
            "spotify_preview_url": self.get_extended_preview_url(track['preview_url'], 90),
            "spotify_external_url": track['external_url'],
            "options": options,
            "correct": correct_index,
            "explanation": f"'{track['name']}' egy One Hit Wonder dal az előadótól: {track['artist']}",
            "topic": "one_hit_wonders",
            "album": track['album'],
            "preview_duration": 90  # 90 másodperces preview
        }
        
        questions.append(question)
    
    return questions

def test_spotify_integration():
    """Tesztelés a Spotify integrációhoz"""
    print("🎵 Spotify One Hit Wonders Integráció Tesztelése")
    print("=" * 50)
    
    manager = SpotifyPlaylistManager()
    
    # Access token tesztelése
    if manager.get_access_token():
        print("✅ Access token sikeresen beszerezve")
        
        # Playlist tesztelése
        tracks = manager.get_playlist_tracks(ONE_HIT_WONDERS_PLAYLIST_ID)
        print(f"✅ Playlist dalok lekérdezve: {len(tracks)} dal")
        
        if tracks:
            print("\n📋 Első 5 dal:")
            for i, track in enumerate(tracks[:5]):
                print(f"  {i+1}. {track['artist']} - {track['name']}")
            
            # Kérdés generálás tesztelése
            questions = get_one_hit_wonders_questions(3)
            print(f"\n❓ Generált kérdések: {len(questions)}")
            
            for i, q in enumerate(questions):
                print(f"\n  Kérdés {i+1}: {q['question']}")
                print(f"  Válaszopciók: {q['options']}")
                print(f"  Helyes válasz: {q['options'][q['correct']]}")
        
    else:
        print("❌ Access token beszerzése sikertelen")
        print("Ellenőrizd a Spotify API credentials beállításokat!")

if __name__ == "__main__":
    test_spotify_integration() 