#!/usr/bin/env python3
"""
Spotify Playlist Integration Module
- OAuth alapú Spotify playlist elérés
- YouTube keresés és letöltés
"""

import requests
import time
import re
import yt_dlp
from typing import List, Dict, Optional
import os
from spotify_api_config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from urllib.parse import quote

# Streamlit import opcionális
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False
    class MockSt:
        def info(self, msg): print(f"INFO: {msg}")
        def success(self, msg): print(f"SUCCESS: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
    st = MockSt()

class SpotifyPlaylistManager:
    def __init__(self):
        self.oauth_access_token = None
        self.oauth_token_expires_at = 0
        self.redirect_uri = "http://127.0.0.1:8501/callback"
    
    def set_oauth_token_manual(self, token: str, expires_in: int = 3600):
        """Manuális OAuth token beállítás teszteléshez"""
        self.oauth_access_token = token
        self.oauth_token_expires_at = time.time() + expires_in - 60
        if STREAMLIT_AVAILABLE:
            st.success(f"✅ OAuth token manuálisan beállítva: {token[:20]}...")
        else:
            print(f"✅ OAuth token manuálisan beállítva: {token[:20]}...")
    
    def restore_oauth_token(self, token: str, expires_at: float):
        """OAuth token visszaállítása session state-ből"""
        self.oauth_access_token = token
        self.oauth_token_expires_at = expires_at
        if STREAMLIT_AVAILABLE:
            st.success(f"✅ OAuth token visszaállítva: {token[:20]}...")
        else:
            print(f"✅ OAuth token visszaállítva: {token[:20]}...")
    
    def get_oauth_authorization_url(self) -> str:
        """OAuth autorizációs URL generálása"""
        scopes = [
            "user-read-private",
            "user-read-email",
            "playlist-read-private",
            "playlist-read-collaborative"
        ]
        
        params = {
            'client_id': SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(scopes),
            'show_dialog': 'true'
        }
        
        auth_url = f"https://accounts.spotify.com/authorize?client_id={params['client_id']}&response_type={params['response_type']}&redirect_uri={quote(params['redirect_uri'])}&scope={quote(params['scope'])}&show_dialog={params['show_dialog']}"
        return auth_url
    
    def get_oauth_access_token(self, authorization_code: str) -> Optional[str]:
        """OAuth access token beszerzése"""
        if STREAMLIT_AVAILABLE:
            st.info(f"🔑 OAuth token kérése... Code: {authorization_code[:10]}...")
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'client_id': SPOTIFY_CLIENT_ID,
            'client_secret': SPOTIFY_CLIENT_SECRET
        }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        try:
            if STREAMLIT_AVAILABLE:
                st.info("📡 Spotify API hívás...")
            
            response = requests.post("https://accounts.spotify.com/api/token", data=data, headers=headers)
            
            if STREAMLIT_AVAILABLE:
                st.info(f"📊 Response status: {response.status_code}")
            
            if response.status_code == 200:
                token_data = response.json()
                self.oauth_access_token = token_data.get('access_token')
                self.oauth_token_expires_at = time.time() + token_data.get('expires_in', 3600) - 60
                
                if STREAMLIT_AVAILABLE:
                    st.success(f"✅ OAuth token sikeres: {self.oauth_access_token[:20]}...")
                    st.info(f"⏰ Lejárat: {self.oauth_token_expires_at - time.time():.0f}s múlva")
                
                return self.oauth_access_token
            else:
                if STREAMLIT_AVAILABLE:
                    st.error(f"❌ OAuth token hiba: {response.status_code}")
                    st.error(f"📄 Response: {response.text}")
                else:
                    print(f"OAuth token hiba: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ OAuth token hiba: {e}")
            else:
                print(f"OAuth token hiba: {e}")
            return None
    
    def get_playlist_tracks(self, playlist_url: str) -> List[Dict]:
        """Playlist trackek lekérése OAuth token-nel"""
        if not self.oauth_access_token or time.time() >= self.oauth_token_expires_at:
            if STREAMLIT_AVAILABLE:
                st.error("❌ OAuth token szükséges nyilvános playlistekhez!")
                st.info("🔐 Kérlek állítsd be az OAuth tokent a fenti expanderben!")
            else:
                print("ERROR: OAuth token szükséges nyilvános playlistekhez!")
            return []
        
        playlist_id = self._extract_playlist_id(playlist_url)
        if not playlist_id:
            if STREAMLIT_AVAILABLE:
                st.error("❌ Érvénytelen Spotify playlist URL!")
            else:
                print("ERROR: Érvénytelen Spotify playlist URL!")
            return []
        
        headers = {
            'Authorization': f'Bearer {self.oauth_access_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            playlist_url_api = f"https://api.spotify.com/v1/playlists/{playlist_id}"
            
            if STREAMLIT_AVAILABLE:
                st.info(f"🎵 Playlist lekérdezés: {playlist_id}")
                st.info(f"🔗 API URL: {playlist_url_api}")
                st.info(f"🔑 Token: {self.oauth_access_token[:20]}...")
            
            response = requests.get(playlist_url_api, headers=headers)
            
            if STREAMLIT_AVAILABLE:
                st.info(f"📊 Response status: {response.status_code}")
            
            if response.status_code != 200:
                if STREAMLIT_AVAILABLE:
                    st.error(f"❌ Hiba a playlist lekérdezésénél: {response.status_code}")
                    st.error(f"📄 Response: {response.text}")
                else:
                    print(f"ERROR: Hiba a playlist lekérdezésénél: {response.status_code}")
                return []
            
            playlist_data = response.json()
            tracks = []
            
            for item in playlist_data.get('tracks', {}).get('items', []):
                track_data = item.get('track')
                if not track_data:
                    continue
                
                album_images = track_data.get('album', {}).get('images', [])
                album_art_url = album_images[0].get('url') if album_images else None
                
                track = {
                    'id': track_data.get('id'),
                    'name': track_data.get('name'),
                    'artists': [artist.get('name') for artist in track_data.get('artists', [])],
                    'album': track_data.get('album', {}).get('name'),
                    'duration_ms': track_data.get('duration_ms'),
                    'external_url': track_data.get('external_urls', {}).get('spotify'),
                    'preview_url': track_data.get('preview_url'),
                    'album_art_url': album_art_url
                }
                tracks.append(track)
            
            if STREAMLIT_AVAILABLE:
                st.success(f"✅ {len(tracks)} track betöltve a playlistből!")
            
            return tracks
            
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ Hiba a playlist lekérdezésénél: {e}")
            else:
                print(f"ERROR: Hiba a playlist lekérdezésénél: {e}")
            return []
    
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
        search_query = self._build_search_query(track_info)
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch10:{search_query}", download=False)
                
                if not search_results or 'entries' not in search_results:
                    return None
                
                entries = search_results['entries']
                if not entries:
                    return None
                
                best_match = self._select_best_match(entries, track_info)
                
                if best_match:
                    video_id = best_match.get('id')
                    if video_id:
                        thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                        best_match['thumbnail_url'] = thumbnail_url
                
                return best_match
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"YouTube keresési hiba: {e}")
            else:
                print(f"YouTube keresési hiba: {e}")
            return None
    
    def _build_search_query(self, track_info: Dict) -> str:
        """Keresési kifejezés összeállítása"""
        artists = " ".join(track_info['artists'])
        track_name = track_info['name']
        query = f"{artists} - {track_name}"
        
        if track_info['album']:
            query += f" {track_info['album']}"
        
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
            
            if any(spam in title for spam in ['sponsored', 'ad', 'reklám', 'promo']):
                continue
            
            if duration > 600:  # 10 perc felett
                continue
                
            valid_entries.append(entry)
        
        if not valid_entries:
            return None
        
        # Legjobb találat kiválasztása (legrövidebb, legtöbb nézettség)
        def score_entry(entry):
            title = entry.get('title', '').lower()
            duration = entry.get('duration', 0)
            view_count = entry.get('view_count', 0)
            
            # Alap pontszám
            score = 0
            
            # Cím egyezés
            track_name = track_info['name'].lower()
            artists = " ".join(track_info['artists']).lower()
            
            if track_name in title:
                score += 10
            if any(artist.lower() in title for artist in track_info['artists']):
                score += 5
            
            # Időtartam (rövidebb = jobb)
            if duration > 0:
                score += max(0, 10 - duration // 30)
            
            # Nézettség (több = jobb)
            if view_count > 0:
                score += min(5, view_count // 1000000)
            
            return score
        
        best_entry = max(valid_entries, key=score_entry)
        return best_entry


class AudioDownloader:
    def __init__(self, output_dir: str = None, max_duration: int = 90):
        self.output_dir = output_dir or os.path.expanduser("~/Downloads")
        self.max_duration = max_duration
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def download_track(self, youtube_url: str, track_info: Dict) -> Optional[str]:
        """Track letöltése YouTube URL-ből"""
        try:
            # Fájlnév generálása
            artists = " ".join(track_info['artists'])
            track_name = track_info['name']
            filename = f"{artists} - {track_name}.mp3"
            filename = self._sanitize_filename(filename)
            
            output_path = os.path.join(self.output_dir, filename)
            
            # yt-dlp beállítások
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_path,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
            
            if os.path.exists(output_path):
                return output_path
            else:
                return None
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"Letöltési hiba: {e}")
            else:
                print(f"Letöltési hiba: {e}")
            return None
    
    def _sanitize_filename(self, filename: str) -> str:
        """Fájlnév tisztítása"""
        # Speciális karakterek eltávolítása
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')
        
        # Hossz korlátozása
        if len(filename) > 200:
            filename = filename[:200]
        
        return filename


class SpotifyPlaylistQuiz:
    def __init__(self):
        self.playlist_manager = SpotifyPlaylistManager()
        self.youtube_searcher = YouTubeSearcher()
        self.audio_downloader = AudioDownloader()
    
    def restore_oauth_token(self, token: str, expires_at: float):
        """OAuth token visszaállítása session state-ből"""
        self.playlist_manager.restore_oauth_token(token, expires_at)
    
    def get_oauth_authorization_url(self) -> str:
        """OAuth autorizációs URL generálása"""
        return self.playlist_manager.get_oauth_authorization_url()
    
    def set_oauth_access_token(self, authorization_code: str) -> bool:
        """OAuth access token beállítása"""
        try:
            if STREAMLIT_AVAILABLE:
                st.info(f"🔑 OAuth token beállítása... Code: {authorization_code[:10]}...")
            
            token = self.playlist_manager.get_oauth_access_token(authorization_code)
            
            if token:
                if STREAMLIT_AVAILABLE:
                    st.success(f"✅ OAuth token sikeresen beállítva: {token[:20]}...")
                return True
            else:
                if STREAMLIT_AVAILABLE:
                    st.error("❌ OAuth token beállítása sikertelen!")
                return False
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"❌ OAuth token hiba: {e}")
            else:
                print(f"ERROR: OAuth token hiba: {e}")
            return False
    
    def get_playlist_tracks_only(self, playlist_url: str) -> List[Dict]:
        """Csak Spotify adatok lekérése, YouTube keresés nélkül"""
        try:
            if STREAMLIT_AVAILABLE:
                st.info("🎵 Spotify playlist elemek lekérése...")
            
            tracks = self.playlist_manager.get_playlist_tracks(playlist_url)
            
            if STREAMLIT_AVAILABLE:
                st.success(f"✅ {len(tracks)} track betöltve Spotify adatokkal")
            
            return tracks
            
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"Hiba a playlist betöltésekor: {e}")
            else:
                print(f"ERROR: Hiba a playlist betöltésekor: {e}")
            return []
    
    def search_youtube_for_track(self, track: Dict) -> Optional[Dict]:
        """YouTube keresés egy konkrét trackhez"""
        try:
            if STREAMLIT_AVAILABLE:
                st.info(f"🔍 YouTube keresés: {track['name']} - {', '.join(track['artists'])}")
            
            youtube_result = self.youtube_searcher.search_track(track)
            
            if youtube_result:
                result = {
                    'url': f"https://www.youtube.com/watch?v={youtube_result['id']}",
                    'title': youtube_result['title'],
                    'views': youtube_result.get('view_count', 0),
                    'duration': youtube_result.get('duration', 0),
                    'thumbnail_url': youtube_result.get('thumbnail_url')
                }
                
                if STREAMLIT_AVAILABLE:
                    st.success(f"✅ YouTube találat: {youtube_result['title']}")
                
                return result
            else:
                if STREAMLIT_AVAILABLE:
                    st.warning(f"⚠️ Nincs YouTube találat: {track['name']}")
                
                return None
                
        except Exception as e:
            if STREAMLIT_AVAILABLE:
                st.error(f"Hiba a YouTube kereséskor: {e}")
            else:
                print(f"ERROR: Hiba a YouTube kereséskor: {e}")
            return None
    
    def download_selected_tracks(self, tracks: List[Dict], selected_indices: List[int]) -> List[str]:
        """Kiválasztott trackek letöltése"""
        downloaded_files = []
        
        for idx in selected_indices:
            if idx < len(tracks):
                track = tracks[idx]
                if track.get('youtube_url'):
                    with st.spinner(f"Letöltés: {track['name']}..."):
                        downloaded_file = self.audio_downloader.download_track(track['youtube_url'], track)
                        if downloaded_file:
                            downloaded_files.append(downloaded_file)
                            st.success(f"✅ Letöltve: {os.path.basename(downloaded_file)}")
                        else:
                            st.error(f"❌ Letöltési hiba: {track['name']}")
        
        return downloaded_files


def format_duration(ms: int) -> str:
    """Időtartam formázása"""
    if not ms:
        return "0:00"
    
    seconds = ms // 1000
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes}:{seconds:02d}"


def format_views(views: int) -> str:
    """Nézettség formázása"""
    if not views:
        return "0"
    
    if views >= 1000000:
        return f"{views // 1000000}M"
    elif views >= 1000:
        return f"{views // 1000}K"
    else:
        return str(views) 