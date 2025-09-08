#!/usr/bin/env python3
"""
Spotify Audio Downloader
Letölti az audio tartalmakat a Spotify linkekből
"""

import os
import requests
import json
import time
from pathlib import Path
from urllib.parse import urlparse, parse_qs
import yt_dlp

class SpotifyAudioDownloader:
    def __init__(self):
        self.audio_dir = Path(__file__).parent / "audio_files"
        self.audio_dir.mkdir(exist_ok=True)
        
    def extract_track_id(self, spotify_url):
        """Kinyeri a track ID-t a Spotify URL-ből"""
        if '/track/' in spotify_url:
            return spotify_url.split('/track/')[1].split('?')[0]
        elif '/artist/' in spotify_url:
            return spotify_url.split('/artist/')[1].split('?')[0]
        return None
    
    def get_track_info(self, track_id):
        """Lekéri a track információit a Spotify API-ból"""
        try:
            search_query = f"spotify track {track_id}"
            return {"track_id": track_id, "search_query": search_query}
        except Exception as e:
            print(f"Hiba a track info lekérésekor: {e}")
            return None
    
    def download_from_youtube(self, search_query, output_filename):
        try:
            base_filename = output_filename.replace('.mp3', '')
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': str(self.audio_dir / f"{base_filename}.%(ext)s"),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'quiet': True,
                'no_warnings': True,
                # 403 Forbidden hiba javítása - teljesen új megközelítés
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache',
                    'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                    'Sec-Ch-Ua-Mobile': '?0',
                    'Sec-Ch-Ua-Platform': '"Windows"',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Upgrade-Insecure-Requests': '1',
                },
                'extractor_retries': 10,
                'fragment_retries': 10,
                'retries': 10,
                # Cookie és referer beállítások
                'cookiefile': None,
                'referer': 'https://www.youtube.com/',
                # Proxy és timeout beállítások
                'socket_timeout': 120,
                'retry_sleep_functions': {'http': lambda n: min(1.5 ** n, 60)},
                # Teljesen új extractor beállítások
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls', 'translated_subs'],
                        'player_skip': ['configs', 'webpage'],
                        'player_client': ['android', 'web'],
                    }
                },
                # További beállítások
                'no_check_certificate': True,
                'prefer_insecure': True,
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                # Rate limiting
                'sleep_interval': 1,
                'max_sleep_interval': 5,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"ytsearch:{search_query}"])
            return True
        except Exception as e:
            print(f"Hiba a YouTube letöltéskor: {e}")
            return False
    
    def download_spotify_track(self, spotify_url, output_filename=None):
        track_id = self.extract_track_id(spotify_url)
        if not track_id:
            print(f"Érvénytelen Spotify URL: {spotify_url}")
            return False
        if not output_filename:
            output_filename = f"track_{track_id}.mp3"
        track_info = self.get_track_info(track_id)
        if not track_info:
            return False
        print(f"Letöltés: {track_info['search_query']}")
        return self.download_from_youtube(track_info['search_query'], output_filename)
    
    def batch_download_questions(self, questions, max_downloads=None):
        downloaded_files = []
        if max_downloads is None:
            max_downloads = len(questions)
        for i, question in enumerate(questions[:max_downloads]):
            if 'spotify_embed' not in question or not question['spotify_embed']:
                continue
            spotify_url = question['spotify_embed']
            explanation = question.get('explanation', f'track_{i}')
            track_id = self.extract_track_id(spotify_url)
            if track_id:
                output_filename = f"track_{track_id}.mp3"
            else:
                output_filename = f"audio_{i}.mp3"
            print(f"Letöltés {i+1}/{min(max_downloads, len(questions))}: {explanation}")
            if self.download_spotify_track(spotify_url, output_filename):
                downloaded_files.append({
                    'question_index': i,
                    'filename': output_filename,
                    'explanation': explanation
                })
                print(f"✅ Sikeres: {output_filename}")
            else:
                print(f"❌ Sikertelen: {explanation}")
            time.sleep(2)
        return downloaded_files

def main():
    downloader = SpotifyAudioDownloader()
    from topics.magyar_zenekarok import MAGYAR_ZENEKAROK_QUESTIONS
    from topics.nemzetkozi_zenekarok import NEMZETKOZI_ZENEKAROK_QUESTIONS
    from classical_music_questions_tschaikovsky_updated import CLASSICAL_MUSIC_QUESTIONS
    all_questions = (
        MAGYAR_ZENEKAROK_QUESTIONS +
        NEMZETKOZI_ZENEKAROK_QUESTIONS +
        CLASSICAL_MUSIC_QUESTIONS
    )
    print("🎵 Spotify Audio Downloader")
    print(f"Talált kérdések: {len(all_questions)}")
    downloaded = downloader.batch_download_questions(all_questions)
    print(f"\n✅ Sikeresen letöltve: {len(downloaded)} fájl")
    for file_info in downloaded:
        print(f"  - {file_info['filename']}: {file_info['explanation']}")

if __name__ == "__main__":
    main() 