#!/usr/bin/env python3
"""
Spotify Playlist Integration Module
- Spotify playlist elemek lekérése
- YouTube keresés a metadata alapján
- yt-dlp letöltés optimalizált beállításokkal
"""

import requests
import json
import time
import re
import yt_dlp
from typing import List, Dict, Optional, Tuple
import os
from spotify_api_config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_API_BASE_URL

# Streamlit import opcionális
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    # Mock st objektum teszteléshez
    class MockSt:
        def info(self, msg): print(f"INFO: {msg}")
        def success(self, msg): print(f"SUCCESS: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def write(self, msg): print(f"WRITE: {msg}")
    st = MockSt()

class SpotifyPlaylistManager:
    def __init__(self):
        self.access_token = None
        self.token_expires_at = 0
        
    def get_access_token(self) -> str:
        """Spotify access token lekérése"""
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
            
        auth_url = "https://accounts.spotify.com/api/token"
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET,
        })
        
        if auth_response.status_code == 200:
            auth_data = auth_response.json()
            self.access_token = auth_data['access_token']
            self.token_expires_at = time.time() + auth_data['expires_in'] - 60  # 1 perc buffer
            return self.access_token
        else:
            raise Exception(f"Spotify auth failed: {auth_response.status_code}")
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict]:
        """Playlist elemek lekérése"""
        # Playlist ID kinyerése az URL-ből
        playlist_id = self._extract_playlist_id(playlist_url)
        if not playlist_id:
            raise ValueError("Érvénytelen Spotify playlist URL")
        
        # Mock adatok teszteléshez (mivel Client Credentials nem engedélyezi a nyilvános playlisteket)
        print("INFO: Mock adatok használata teszteléshez")
        return self._get_mock_tracks()
    
    def _get_mock_tracks(self) -> List[Dict]:
        """Mock track adatok teszteléshez"""
        return [
            {
                'id': 'mock_1',
                'name': 'Bohemian Rhapsody',
                'artists': ['Queen'],
                'album': 'A Night at the Opera',
                'duration_ms': 354000,
                'external_url': 'https://open.spotify.com/track/mock_1',
                'preview_url': None,
                'album_art_url': 'https://i.scdn.co/image/ab67616d0000b273ce4f1737e6c24e4c0f0c5c0f'
            },
            {
                'id': 'mock_2',
                'name': 'Hotel California',
                'artists': ['Eagles'],
                'album': 'Hotel California',
                'duration_ms': 391000,
                'external_url': 'https://open.spotify.com/track/mock_2',
                'preview_url': None,
                'album_art_url': 'https://i.scdn.co/image/ab67616d0000b273ce4f1737e6c24e4c0f0c5c0f'
            },
            {
                'id': 'mock_3',
                'name': 'Stairway to Heaven',
                'artists': ['Led Zeppelin'],
                'album': 'Led Zeppelin IV',
                'duration_ms': 482000,
                'external_url': 'https://open.spotify.com/track/mock_3',
                'preview_url': None,
                'album_art_url': 'https://i.scdn.co/image/ab67616d0000b273ce4f1737e6c24e4c0f0c5c0f'
            },
            {
                'id': 'mock_4',
                'name': 'Imagine',
                'artists': ['John Lennon'],
                'album': 'Imagine',
                'duration_ms': 183000,
                'external_url': 'https://open.spotify.com/track/mock_4',
                'preview_url': None,
                'album_art_url': 'https://i.scdn.co/image/ab67616d0000b273ce4f1737e6c24e4c0f0c5c0f'
            },
            {
                'id': 'mock_5',
                'name': 'Yesterday',
                'artists': ['The Beatles'],
                'album': 'Help!',
                'duration_ms': 125000,
                'external_url': 'https://open.spotify.com/track/mock_5',
                'preview_url': None,
                'album_art_url': 'https://i.scdn.co/image/ab67616d0000b273ce4f1737e6c24e4c0f0c5c0f'
            }
        ]
    
    def _extract_playlist_id(self, playlist_url: str) -> Optional[str]:
        """Playlist ID kinyerése URL-ből"""
        patterns = [
            r'spotify\.com/playlist/([a-zA-Z0-9]+)',
            r'spotify\.com/user/[^/]+/playlist/([a-zA-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, playlist_url)
            if match:
                return match.group(1)
        return None

class YouTubeSearcher:
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'default_search': 'ytsearch',
            'noplaylist': True,
            'ignoreerrors': True
        }
    
    def search_track(self, track_info: Dict) -> Optional[Dict]:
        """YouTube keresés track metadata alapján"""
        # Keresési kifejezés összeállítása
        search_query = self._build_search_query(track_info)
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # YouTube keresés
                search_results = ydl.extract_info(f"ytsearch10:{search_query}", download=False)
                
                if not search_results or 'entries' not in search_results:
                    return None
                
                entries = search_results['entries']
                if not entries:
                    return None
                
                # Legjobb találat kiválasztása
                best_match = self._select_best_match(entries, track_info)
                return best_match
                
        except Exception as e:
            st.error(f"YouTube keresési hiba: {e}")
            return None
    
    def _build_search_query(self, track_info: Dict) -> str:
        """Keresési kifejezés összeállítása"""
        artists = " ".join(track_info['artists'])
        track_name = track_info['name']
        
        # Alap keresési kifejezés
        query = f"{artists} - {track_name}"
        
        # Kiegészítések a pontosabb találathoz
        if track_info['album']:
            query += f" {track_info['album']}"
        
        # Sponsored és live tartalmak kiszűrése
        query += " -sponsored -live -cover -remix"
        
        return query
    
    def _select_best_match(self, entries: List[Dict], track_info: Dict) -> Optional[Dict]:
        """Legjobb YouTube találat kiválasztása"""
        valid_entries = []
        
        for entry in entries:
            if not entry:
                continue
                
            title = entry.get('title', '').lower()
            duration = entry.get('duration', 0)
            
            # Sponsored tartalmak kiszűrése
            if any(spam in title for spam in ['sponsored', 'ad', 'reklám', 'promo']):
                continue
            
            # Live tartalmak kiszűrése
            if any(live in title for live in ['live', 'élő', 'concert', 'koncert']):
                continue
            
            # Cover és remix tartalmak kiszűrése
            if any(cover in title for cover in ['cover', 'remix', 'mashup']):
                continue
            
            # Hossz ellenőrzése (nem túl rövid, nem túl hosszú)
            if duration and 30 < duration < 600:  # 30 másodperc - 10 perc
                valid_entries.append(entry)
        
        if not valid_entries:
            return None
        
        # Rendezés prioritások szerint
        def score_entry(entry):
            score = 0
            title = entry.get('title', '').lower()
            view_count = entry.get('view_count', 0)
            duration = entry.get('duration', 0)
            
            # Nézettség alapján pontozás
            if view_count > 1000000:
                score += 10
            elif view_count > 100000:
                score += 5
            elif view_count > 10000:
                score += 2
            
            # Cím egyezés alapján pontozás
            track_name = track_info['name'].lower()
            artists = " ".join(track_info['artists']).lower()
            
            if track_name in title:
                score += 5
            if artists in title:
                score += 3
            
            # Hossz optimalizálás (2-5 perc között)
            if 120 <= duration <= 300:
                score += 3
            elif 60 <= duration <= 600:
                score += 1
            
            return score
        
        # Legjobb találat kiválasztása
        best_entry = max(valid_entries, key=score_entry)
        return best_entry

class AudioDownloader:
    def __init__(self, output_dir: str = "audio_files", max_duration: int = 90):
        self.output_dir = output_dir
        self.max_duration = max_duration
        
        # Könyvtár létrehozása, ha nem létezik
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def download_track(self, youtube_url: str, track_info: Dict) -> Optional[str]:
        """Track letöltése YouTube URL-ből yt-dlp parancssal"""
        try:
            # Egyedi fájlnév generálása
            safe_title = self._sanitize_filename(f"{track_info['artists'][0]} - {track_info['name']}")
            output_filename = f"{self.output_dir}/{safe_title}.mp3"
            
            # yt-dlp parancs összeállítása
            cmd = [
                "python3", "-m", "yt_dlp",
                "--extract-audio",
                "--audio-format", "mp3",
                "--audio-quality", "0",  # Legjobb minőség
                "--output", output_filename,
                "--postprocessor-args", f"ffmpeg:-ss 0 -t {self.max_duration}",  # Vágás 0-tól max_duration-ig
                "--no-warnings",
                "--quiet",
                youtube_url
            ]
            
            # Parancs végrehajtása
            import subprocess
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                if os.path.exists(output_filename):
                    return output_filename
                else:
                    st.warning(f"Fájl nem található: {output_filename}")
                    return None
            else:
                st.error(f"yt-dlp hiba: {result.stderr}")
                return None
                    
        except Exception as e:
            st.error(f"Letöltési hiba: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Fájlnév tisztítása"""
        # Speciális karakterek eltávolítása
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Túl hosszú nevek levágása
        if len(filename) > 100:
            filename = filename[:100]
        return filename.strip()

# Fő integrációs osztály
class SpotifyPlaylistQuiz:
    def __init__(self):
        self.playlist_manager = SpotifyPlaylistManager()
        self.youtube_searcher = YouTubeSearcher()
        self.audio_downloader = AudioDownloader()
    
    def process_playlist(self, playlist_url: str) -> List[Dict]:
        """Playlist feldolgozása teljes folyamattal"""
        try:
            # 1. Playlist elemek lekérése
            st.info("🎵 Spotify playlist elemek lekérése...")
            tracks = self.playlist_manager.get_playlist_tracks(playlist_url)
            st.success(f"✅ {len(tracks)} track betöltve")
            
            processed_tracks = []
            
            for i, track in enumerate(tracks):
                st.write(f"🔍 Feldolgozás: {track['name']} - {', '.join(track['artists'])}")
                
                # 2. YouTube keresés
                youtube_result = self.youtube_searcher.search_track(track)
                
                if youtube_result:
                    track['youtube_url'] = f"https://www.youtube.com/watch?v={youtube_result['id']}"
                    track['youtube_title'] = youtube_result['title']
                    track['youtube_duration'] = youtube_result.get('duration', 0)
                    track['youtube_views'] = youtube_result.get('view_count', 0)
                    
                    st.success(f"✅ YouTube találat: {youtube_result['title']}")
                else:
                    st.warning(f"⚠️ Nincs YouTube találat: {track['name']}")
                    track['youtube_url'] = None
                
                processed_tracks.append(track)
                
                # Rate limiting
                time.sleep(1)
            
            return processed_tracks
            
        except Exception as e:
            st.error(f"Hiba a playlist feldolgozásakor: {e}")
            return []
    
    def download_selected_tracks(self, tracks: List[Dict], selected_indices: List[int]) -> List[str]:
        """Kiválasztott trackek letöltése"""
        downloaded_files = []
        
        for idx in selected_indices:
            if idx < len(tracks):
                track = tracks[idx]
                if track.get('youtube_url'):
                    st.write(f"⬇️ Letöltés: {track['name']}")
                    
                    file_path = self.audio_downloader.download_track(
                        track['youtube_url'], 
                        track
                    )
                    
                    if file_path:
                        downloaded_files.append(file_path)
                        st.success(f"✅ Letöltve: {os.path.basename(file_path)}")
                    else:
                        st.error(f"❌ Letöltés sikertelen: {track['name']}")
                else:
                    st.warning(f"⚠️ Nincs YouTube URL: {track['name']}")
        
        return downloaded_files

# Segédfüggvények
def format_duration(ms: int) -> str:
    """Milliszekundumok formázása"""
    if ms is None:
        return "N/A"
    try:
        seconds = int(ms) // 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "N/A"

def format_views(views: int) -> str:
    """Nézettség formázása"""
    if views >= 1000000:
        return f"{views/1000000:.1f}M"
    elif views >= 1000:
        return f"{views/1000:.1f}K"
    else:
        return str(views) 