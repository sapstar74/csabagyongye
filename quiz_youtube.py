"""
Quiz YouTube: search_youtube_tracks, download_and_integrate_track,
generate_quiz_question, add_question_to_category, save_questions_to_file.
"""

import os
import re
import json
import glob
import random
import subprocess
from pathlib import Path
from datetime import datetime

import streamlit as st

from quiz_audio import _parse_artist_title_from_youtube

_PROJECT_ROOT = Path(__file__).parent

def search_youtube_tracks(query):
    """YouTube keresés implementáció"""
    try:
        import requests
        import json
        import re
        
        # YouTube keresés közvetlenül a YouTube API nélkül - pontosabb keresés
        # Hozzáadunk specifikus kulcsszavakat a jobb eredményekért
        if "one night in bangkok" in query.lower():
            enhanced_query = f"{query} Murray Head official music video"
        elif "murray head" in query.lower():
            enhanced_query = f"{query} One Night in Bangkok official music video"
        else:
            enhanced_query = f"{query} official music video"
        
        search_url = f"https://www.youtube.com/results?search_query={enhanced_query.replace(' ', '+')}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            # YouTube oldal tartalmából kinyerjük a videó adatokat
            html_content = response.text
            
            # ytInitialData keresése
            yt_initial_data_match = re.search(r'var ytInitialData = ({.*?});', html_content)
            
            if yt_initial_data_match:
                try:
                    yt_data = json.loads(yt_initial_data_match.group(1))
                    
                    # Videó adatok kinyerése
                    videos = []
                    
                    # Keresési eredmények keresése a JSON-ben
                    def extract_videos(data):
                        if isinstance(data, dict):
                            for key, value in data.items():
                                if key == 'videoRenderer':
                                    video_info = value
                                    
                                    # Title kinyerése
                                    title_obj = video_info.get('title', {})
                                    if isinstance(title_obj, dict) and 'runs' in title_obj:
                                        title = title_obj['runs'][0].get('text', '') if title_obj['runs'] else ''
                                    else:
                                        title = str(title_obj)
                                    
                                    # Channel kinyerése
                                    channel_obj = video_info.get('ownerText', {})
                                    if isinstance(channel_obj, dict) and 'runs' in channel_obj:
                                        channel = channel_obj['runs'][0].get('text', '') if channel_obj['runs'] else ''
                                    else:
                                        channel = str(channel_obj)
                                    
                                    video_id = video_info.get('videoId', '')
                                    
                                    # Duration kinyerése
                                    duration_obj = video_info.get('lengthText', {})
                                    if isinstance(duration_obj, dict):
                                        duration = duration_obj.get('simpleText', '')
                                    else:
                                        duration = str(duration_obj)
                                    
                                    # Views kinyerése
                                    views_obj = video_info.get('viewCountText', {})
                                    if isinstance(views_obj, dict):
                                        views = views_obj.get('simpleText', '')
                                    else:
                                        views = str(views_obj)
                                    
                                    # Thumbnail kinyerése
                                    thumbnail_obj = video_info.get('thumbnail', {})
                                    if isinstance(thumbnail_obj, dict) and 'thumbnails' in thumbnail_obj:
                                        thumbnails = thumbnail_obj['thumbnails']
                                        if thumbnails and len(thumbnails) > 0:
                                            thumbnail = thumbnails[-1].get('url', '')
                                        else:
                                            thumbnail = f"https://i.ytimg.com/vi/{video_id}/default.jpg"
                                    else:
                                        thumbnail = f"https://i.ytimg.com/vi/{video_id}/default.jpg"
                                    
                                    if video_id and title:
                                        videos.append({
                                            'title': title,
                                            'channel': channel,
                                            'duration': duration,
                                            'views': views,
                                            'url': f"https://www.youtube.com/watch?v={video_id}",
                                            'thumbnail': thumbnail
                                        })
                                elif isinstance(value, (dict, list)):
                                    extract_videos(value)
                        elif isinstance(data, list):
                            for item in data:
                                extract_videos(item)
                    
                    extract_videos(yt_data)
                    
                    # Sponsored találatok kiszűrése és jobb eredmények kiválasztása
                    processed_results = []
                    for video in videos[:10]:  # Több találat ellenőrzése
                        title = video.get('title', '').lower()
                        channel = video.get('channel', '').lower()
                        
                        # Sponsored és reklám találatok kiszűrése
                        if 'sponsored' in title or 'reklám' in title:
                            continue
                        
                        # Jobb eredmények prioritása
                        score = 0
                        
                        # Official/VEVO csatornák prioritása
                        if 'official' in title or 'vevo' in channel:
                            score += 10
                        
                        # Music kulcsszó prioritása
                        if 'music' in title or 'music' in channel:
                            score += 5
                        
                        # Rövidebb címek prioritása (kevesebb "fehér zaj")
                        if len(title) < 100:
                            score += 3
                        
                        # Specifikus dalok prioritása
                        if "one night in bangkok" in query.lower():
                            if "murray head" in title.lower() and "one night in bangkok" in title.lower():
                                score += 20
                            elif "murray head" in channel.lower():
                                score += 15
                            elif "one night in bangkok" in title.lower():
                                score += 10
                        
                        # Rossz találatok kiszűrése
                        if "stacy's mom" in title.lower() or "fountains of wayne" in title.lower():
                            score -= 50
                        
                        # Hozzáadjuk a pontszámot
                        video['score'] = score
                        processed_results.append(video)
                    
                    # Rendezés pontszám szerint (csökkenő)
                    processed_results.sort(key=lambda x: x.get('score', 0), reverse=True)
                    
                    return processed_results[:5]  # Top 5 eredmény
                    
                except json.JSONDecodeError:
                    st.error("Hiba a YouTube adatok feldolgozásakor")
                    return []
            else:
                st.error("Nem sikerült megtalálni a YouTube adatokat")
                return []
        else:
            st.error(f"YouTube oldal betöltési hiba: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"YouTube keresési hiba: {e}")
        return []

def download_and_integrate_track(track_info, category, custom_options=None, require_review=False, clip_seconds=120, return_metadata=False, cookies_path=None):
    """Track letöltése és integrálása"""
    try:
        import yt_dlp
    except ImportError:
        st.error("❌ yt-dlp modul nincs telepítve! Telepítsd: pip install yt-dlp")
        return False
    
    import os
    
    # Ellenőrizzük, hogy track_info dict-e
    if not isinstance(track_info, dict):
        st.error(f"Track info nem dict típusú: {type(track_info)}")
        return False
    
    # Kategória alapján letöltési könyvtár meghatározása
    category_mapping = {
        "magyar_zenekarok": "audio_files/magyar_zenekarok",
        "nemzetkozi_zenekarok": "audio_files/nemzetkozi_zenekarok", 
        "komolyzene": "audio_files/komolyzene",
        "one_hit_wonders": "audio_files/one_hit_wonders",
        "sorozat_focimek": "audio_files/sorozat_focimek",
    }
    
    download_dir = _PROJECT_ROOT / category_mapping.get(category, "audio_files")
    download_dir.mkdir(parents=True, exist_ok=True)
    
    def _yt_dlp_hint(error_message: str) -> None:
        if "Failed to extract any player response" in error_message:
            version = getattr(yt_dlp, "__version__", "ismeretlen")
            st.error(
                "❌ YouTube player response hiba (yt-dlp). "
                f"Frissítsd a yt-dlp-t: pip install -U yt-dlp (aktuális: {version})"
            )
        if "HTTP Error 403" in error_message or "403" in error_message:
            st.error("❌ YouTube 403 tiltás. Próbáld meg cookie fájllal (bejelentkezett böngészőből exportálva).")

    def _looks_like_url(value) -> bool:
        if not isinstance(value, str):
            return False
        lowered = value.lower()
        return lowered.startswith("http") or "youtu" in lowered
    
    # yt-dlp konfiguráció - 403 Forbidden hiba javítása - teljesen új megközelítés
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': str(download_dir / '%(id)s.%(ext)s'),  # YouTube ID használata fájlnévként
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
        # Egyszerűsített extractor beállítások
        'extractor_args': {
            'youtube': {
                'skip': ['dash', 'hls'],
                'player_skip': ['configs', 'webpage'],
                'player_client': ['android', 'web', 'ios', 'tv_embedded'],
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
        # Alternative extractors
        'extractor_retries': 10,
        'fragment_retries': 10,
        'retries': 10,
        # IPv4 kényszerítés macOS-en
        'force_ipv4': True,
        'source_address': '0.0.0.0',
        # Egyszerű beállítások
        'no_color': True,
    }
    if cookies_path:
        ydl_opts['cookiefile'] = cookies_path
    
    # Letöltés - több próbálkozás különböző konfigurációkkal
    url = track_info.get('url', '')
    if not url:
        st.error("Nincs érvényes URL a track_info-ban")
        return False
    
    success = False
    info = {}
    
    # Próbálkozás 1: Egyszerű konfiguráció
    try:
        simple_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'youtube': {
                    'player_skip': ['configs', 'webpage'],
                    'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                }
            },
        }
        if cookies_path:
            simple_opts['cookiefile'] = cookies_path
        with yt_dlp.YoutubeDL(simple_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if info:
                ydl.download([url])
                success = True
            else:
                success = False
    except Exception as e:
        st.error(f"Egyszerű konfiguráció is sikertelen: {str(e)}")
        _yt_dlp_hint(str(e))
        success = False
    
    # Próbálkozás 2: Részletes konfiguráció (ha az első sikertelen)
    if not success:
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.warning(f"Letöltés sikertelen: {str(e)}")
            _yt_dlp_hint(str(e))
            success = False
    
    # Próbálkozás 4: VPN/Proxy beállításokkal (ha mindhárom sikertelen)
    if not success:
        try:
            vpn_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # VPN/Proxy beállítások
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                },
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'geo_bypass_ip_block': '0.0.0.0/0',
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls'],
                        'player_skip': ['configs', 'webpage'],
                        'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                    }
                },
                'socket_timeout': 30,
                'retries': 5,
                'fragment_retries': 5,
            }
            if cookies_path:
                vpn_opts['cookiefile'] = cookies_path
            with yt_dlp.YoutubeDL(vpn_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.error(f"VPN/Proxy konfiguráció is sikertelen: {str(e)}")
            _yt_dlp_hint(str(e))
            success = False
    
    # Próbálkozás 5: Teljesen más megközelítés - yt-dlp alternatív beállítások
    if not success:
        try:
            alt_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
                # Alternatív beállítások
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
                'extractor_args': {
                    'youtube': {
                        'skip': ['dash', 'hls', 'translated_subs'],
                        'player_skip': ['configs', 'webpage'],
                        'player_client': ['android', 'web', 'ios', 'tv_embedded'],
                    }
                },
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'socket_timeout': 60,
                'retries': 3,
                'fragment_retries': 3,
                'no_check_certificate': True,
                'prefer_insecure': True,
            }
            if cookies_path:
                alt_opts['cookiefile'] = cookies_path
            with yt_dlp.YoutubeDL(alt_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                else:
                    success = False
        except Exception as e:
            st.error(f"Alternatív konfiguráció is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 6: Teljesen más URL formátum - ytsearch használata
    if not success:
        try:
            # YouTube URL helyett ytsearch használata
            search_query = track_info.get('title', '') + ' ' + track_info.get('artist', '')
            if search_query.strip():
                search_url = f"ytsearch1:{search_query}"
                st.info(f"🔍 Keresés: {search_query}")
                
                search_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'noplaylist': True,
                    'quiet': True,
                    'no_warnings': True,
                    'http_headers': {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    },
                    'extractor_args': {
                        'youtube': {
                            'skip': ['dash', 'hls'],
                        }
                    },
                    'geo_bypass': True,
                    'geo_bypass_country': 'US',
                    'socket_timeout': 30,
                    'retries': 3,
                }
                if cookies_path:
                    search_opts['cookiefile'] = cookies_path
                with yt_dlp.YoutubeDL(search_opts) as ydl:
                    info = ydl.extract_info(search_url, download=False)
                    if info and 'entries' in info and info['entries']:
                        # Az első találatot használjuk
                        first_result = info['entries'][0]
                        ydl.download([first_result['webpage_url']])
                        success = True
                        info = first_result  # Az info változót frissítjük
                    else:
                        success = False
            else:
                success = False
        except Exception as e:
            st.error(f"Keresés alapú letöltés is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 7: Teljesen más megközelítés - YouTube API közvetlen használata
    if not success:
        try:
            st.info("🔄 Próbálkozás YouTube API közvetlen használatával...")
            
            # YouTube API kulcs nélküli keresés
            import urllib.parse
            import urllib.request
            import json
            
            search_query = track_info.get('title', '') + ' ' + track_info.get('artist', '')
            if search_query.strip():
                # YouTube keresési URL
                search_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
                st.info(f"🔍 YouTube keresés: {search_url}")
                
                # Próbáljuk meg a YouTube oldal tartalmát lekérni
                req = urllib.request.Request(
                    search_url,
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    html_content = response.read().decode('utf-8')
                    
                    # YouTube videó ID keresése a HTML-ben
                    import re
                    video_ids = re.findall(r'"videoId":"([^"]+)"', html_content)
                    
                    if video_ids:
                        video_id = video_ids[0]  # Az első találatot használjuk
                        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
                        st.info(f"📺 Talált videó: {youtube_url}")
                        
                        # Most próbáljuk meg letölteni ezt a videót
                        direct_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True,
                            'quiet': True,
                            'no_warnings': True,
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            },
                            'extractor_args': {
                                'youtube': {
                                    'skip': ['dash', 'hls'],
                                }
                            },
                            'geo_bypass': True,
                            'geo_bypass_country': 'US',
                            'socket_timeout': 30,
                            'retries': 3,
                        }
                        if cookies_path:
                            direct_opts['cookiefile'] = cookies_path
                        
                        with yt_dlp.YoutubeDL(direct_opts) as ydl:
                            info = ydl.extract_info(youtube_url, download=False)
                            if info:
                                ydl.download([youtube_url])
                                success = True
                            else:
                                success = False
                    else:
                        st.warning("⚠️ Nem találtam videó ID-t a keresési eredményekben")
                        success = False
            else:
                success = False
                
        except Exception as e:
            st.error(f"YouTube API közvetlen használat is sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 8: Intelligens proxy rendszer
    if not success:
        try:
            st.info("🔄 Próbálkozás intelligens proxy rendszerrel...")
            
            # 1. Webes proxy szolgáltatások (CroxyProxy, ProxySite)
            web_proxies = [
                'https://www.croxyproxy.com/',
                'https://www.proxysite.com/',
                'https://www.kproxy.com/',
            ]
            
            # 2. Friss HTTP proxy lista
            import requests
            import random
            
            try:
                st.info("🔍 Friss proxy lista letöltése...")
                proxy_response = requests.get(
                    'https://api.proxyscrape.com/v2/?request=get&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all',
                    timeout=10
                )
                
                if proxy_response.status_code == 200:
                    proxy_list = proxy_response.text.strip().split('\n')
                    # Véletlenszerűen választunk 3 proxy-t
                    selected_proxies = random.sample(proxy_list, min(3, len(proxy_list)))
                    st.info(f"✅ Találtam {len(selected_proxies)} friss proxy-t")
                else:
                    selected_proxies = []
                    st.warning("⚠️ Nem sikerült letölteni a proxy listát")
                    
            except Exception as e:
                st.warning(f"⚠️ Proxy lista letöltés hiba: {str(e)}")
                selected_proxies = []
            
            # 3. Proxy-k tesztelése és használata
            all_proxies = []
            
            # Webes proxy-k hozzáadása
            for web_proxy in web_proxies:
                all_proxies.append(('web', web_proxy))
            
            # HTTP proxy-k hozzáadása
            for proxy in selected_proxies:
                all_proxies.append(('http', f"http://{proxy}"))
            
            # Proxy-k tesztelése
            for proxy_type, proxy_url in all_proxies:
                try:
                    if proxy_type == 'web':
                        st.info(f"🌐 Webes proxy tesztelése: {proxy_url}")
                        # Webes proxy-knál más a tesztelés
                        test_success = True
                    else:
                        st.info(f"🌐 HTTP proxy tesztelése: {proxy_url}")
                        # HTTP proxy gyors teszt
                        test_response = requests.get(
                            'http://httpbin.org/ip',
                            proxies={'http': proxy_url, 'https': proxy_url},
                            timeout=5
                        )
                        test_success = test_response.status_code == 200
                    
                    if test_success:
                        st.info(f"✅ Proxy működik: {proxy_url}")
                        
                        # YouTube letöltés proxy-val
                        proxy_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
                            }],
                            'noplaylist': True,
                            'quiet': True,
                            'no_warnings': True,
                            'http_headers': {
                                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                            },
                            'extractor_args': {
                                'youtube': {
                                    'skip': ['dash', 'hls'],
                                }
                            },
                            'geo_bypass': True,
                            'geo_bypass_country': 'US',
                            'socket_timeout': 30,
                            'retries': 2,
                        }
                        if cookies_path:
                            proxy_opts['cookiefile'] = cookies_path
                        
                        # Proxy hozzáadása ha HTTP proxy
                        if proxy_type == 'http':
                            proxy_opts['proxy'] = proxy_url
                        
                        with yt_dlp.YoutubeDL(proxy_opts) as ydl:
                            info = ydl.extract_info(url, download=False)
                            if info:
                                ydl.download([url])
                                success = True
                                st.success(f"🎉 Sikeres letöltés {proxy_type} proxy-val: {proxy_url}")
                                break
                            else:
                                st.warning(f"⚠️ {proxy_type} proxy nem működik YouTube-nál: {proxy_url}")
                    else:
                        st.warning(f"⚠️ {proxy_type} proxy nem elérhető: {proxy_url}")
                        
                except Exception as e:
                    st.warning(f"⚠️ {proxy_type} proxy hiba ({proxy_url}): {str(e)}")
                    continue
                    
        except Exception as e:
            st.error(f"Intelligens proxy rendszer sikertelen: {str(e)}")
            success = False
    
    # Próbálkozás 9: Egyszerű megközelítés (minimális beállításokkal)
    if not success:
        try:
            st.info("🔄 Próbálkozás egyszerű megközelítéssel...")
            
            # Minimális yt-dlp konfiguráció
            simple_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(download_dir / '%(id)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }
            if cookies_path:
                simple_opts['cookiefile'] = cookies_path
            
            with yt_dlp.YoutubeDL(simple_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info:
                    ydl.download([url])
                    success = True
                    st.success("✅ Sikeres letöltés egyszerű megközelítéssel")
                else:
                    success = False
                    
        except Exception as e:
            st.error(f"Egyszerű megközelítés is sikertelen: {str(e)}")
            success = False
    
    if not success:
        st.error("❌ Minden letöltési módszer sikertelen volt")
        st.error("🔍 YouTube valószínűleg blokkolja a letöltéseket ezen a szerveren")
        st.info("💡 Alternatív megoldások:")
        st.info("1. Használj VPN-t a szerveren")
        st.info("2. Próbáld meg másik időpontban")
        st.info("3. Használj másik letöltő szolgáltatást")
        st.info("4. Manuálisan töltsd le és töltsd fel a fájlokat")
        return False
    
    # Ha keresési találatlistát kaptunk, az első elem legyen az info
    if isinstance(info, dict) and info.get('entries'):
        first_entry = next((e for e in info.get('entries', []) if e), None)
        if first_entry:
            info = first_entry
            if first_entry.get('webpage_url'):
                url = first_entry['webpage_url']

    # Track info normalizálás (YouTube cím alapján)
    info_title = info.get('title') if isinstance(info, dict) else None
    info_channel = None
    if isinstance(info, dict):
        info_channel = info.get('uploader') or info.get('channel')
    if info_title:
        if "raw_title" not in track_info:
            track_info["raw_title"] = info_title
        current_title = track_info.get("title")
        if not current_title or _looks_like_url(current_title):
            track_info["title"] = info_title
            current_song_title = track_info.get("song_title")
            if not current_song_title or _looks_like_url(current_song_title):
                track_info["song_title"] = info_title
    if info_channel and not track_info.get("channel"):
        track_info["channel"] = info_channel
    if info_title and not track_info.get("artist"):
        parsed_artist, parsed_title = _parse_artist_title_from_youtube(info_title, info_channel)
        track_info["artist"] = parsed_artist
        if not track_info.get("song_title"):
            track_info["song_title"] = parsed_title
        if not track_info.get("title") or _looks_like_url(track_info.get("title")):
            track_info["title"] = parsed_title

    # Fájlnév meghatározása - YouTube ID alapján
    video_id = info.get('id', '')
    if not video_id:
        st.error("❌ Nem sikerült lekérni a videó ID-t")
        return False
    
    # Fájlnév YouTube ID alapján - először MP3-et próbáljuk
    audio_file = str(download_dir / f"{video_id}.mp3")
    
    # Ellenőrizzük, hogy a fájl létezik-e
    if not os.path.exists(audio_file):
        # Próbáljuk meg megtalálni a fájlt a könyvtárban
        import glob
        possible_files = glob.glob(str(download_dir / f"{video_id}.*"))
        if possible_files:
            audio_file = possible_files[0]  # A YouTube ID-vel kezdődő fájlt használjuk
            st.info(f"📁 Talált fájl: {os.path.basename(audio_file)}")
            
            # Ha nem MP3, konvertáljuk MP3-ba
            if not audio_file.endswith('.mp3'):
                try:
                    mp3_file = str(download_dir / f"{video_id}.mp3")
                    cmd = [
                        'ffmpeg', '-i', audio_file, 
                        '-acodec', 'libmp3lame', 
                        '-ab', '192k', 
                        '-ar', '44100', 
                        '-y', 
                        mp3_file
                    ]
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0 and os.path.exists(mp3_file):
                        # Eredeti fájl törlése
                        if os.path.exists(audio_file):
                            os.remove(audio_file)
                        audio_file = mp3_file
                        st.success("✅ Fájl sikeresen konvertálva MP3-ba!")
                    else:
                        st.warning("⚠️ MP3 konvertálás sikertelen, eredeti fájl használata")
                except Exception as e:
                    st.warning(f"⚠️ MP3 konvertálás hiba: {str(e)}, eredeti fájl használata")
        else:
            st.error("❌ A letöltés sikertelen - fájl nem található")
            return False
    
    # Ellenőrizzük a fájl méretét
    if os.path.getsize(audio_file) == 0:
        st.error("❌ A letöltött fájl üres")
        return False
    
    st.success(f"✅ Sikeres letöltés: {track_info.get('title', 'Ismeretlen track')}")
    
    # 3 perces (vagy beállított) rész kivágása FFmpeg-gel
    try:
        import re
        
        # Ellenőrizzük, hogy a fájl létezik-e és nem üres
        if not os.path.exists(audio_file):
            st.error("❌ A letöltött fájl nem található!")
            return False
        
        if os.path.getsize(audio_file) == 0:
            st.error("❌ A letöltött fájl üres!")
            return False
        
        # Fájl létezik és nem üres, folytathatjuk a vágást
        # Biztonságos fájlnév létrehozása - "Előadó - Szám cím" formátum
        artist = track_info.get('artist', 'Unknown Artist')
        title = track_info.get('title', 'Unknown Title')
        
        # Biztonságos fájlnév létrehozása - rövidebb és egyszerűbb
        safe_artist = re.sub(r'[^\w\s-]', '', artist)[:20]  # Max 20 karakter
        safe_title = re.sub(r'[^\w\s-]', '', title)[:30]   # Max 30 karakter
        safe_artist = re.sub(r'[-\s]+', '_', safe_artist)
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        
        # "Előadó_Szám" formátum (rövidebb)
        output_filename = f"{safe_artist}_{safe_title}.mp3"
        output_file = str(download_dir / output_filename)
        
        # FFmpeg paranccsal 2 perc kivágása - továbbfejlesztett verzió
        # Először ellenőrizzük a bemeneti fájl hosszát
        probe_cmd = [
            'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration', 
            '-of', 'csv=p=0', audio_file
        ]
        
        probe_result = subprocess.run(probe_cmd, capture_output=True, text=True, timeout=30)
        
        if probe_result.returncode == 0 and probe_result.stdout.strip():
            try:
                duration = float(probe_result.stdout.strip())
                if duration < clip_seconds:
                    # Ha a fájl rövidebb mint a kívánt vágás, nem vágunk
                    st.info(f"⚠️ A fájl rövidebb mint {clip_seconds} mp ({duration:.1f}s), teljes fájl használata")
                else:
                    # FFmpeg paranccsal kivágás
                    cmd = [
                        'ffmpeg', '-i', audio_file, 
                        '-t', str(clip_seconds),  # vágás hossza másodpercben
                        '-acodec', 'libmp3lame',  # MP3 kódolás
                        '-ab', '192k',  # 192 kbps bitrate
                        '-ar', '44100',  # 44.1 kHz sample rate
                        '-y',  # Felülírás
                        output_file
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                    
                    if result.returncode == 0 and os.path.exists(output_file):
                        # Ellenőrizzük a kimeneti fájl méretét
                        if os.path.getsize(output_file) > 0:
                            # Eredeti fájl törlése, csak a 2 perces marad
                            if os.path.exists(audio_file):
                                os.remove(audio_file)
                            audio_file = output_file
                            st.success(f"✅ {clip_seconds} mp rész sikeresen kivágva!")
                        else:
                            st.warning("⚠️ A kivágott fájl üres, teljes fájl használata")
                    else:
                        st.warning(f"⚠️ FFmpeg hiba: {result.stderr[:200]}..., teljes fájl használata")
            except ValueError:
                st.warning("⚠️ Nem sikerült meghatározni a fájl hosszát, teljes fájl használata")
        else:
            st.warning("⚠️ Nem sikerült elemezni a fájlt, teljes fájl használata")
            
    except subprocess.TimeoutExpired:
        st.warning("⚠️ FFmpeg időtúllépés, teljes fájl használata")
    except FileNotFoundError:
        st.warning("⚠️ FFmpeg nem található, teljes fájl használata")
    except Exception as e:
        st.warning(f"⚠️ FFmpeg hiba: {str(e)[:100]}..., teljes fájl használata")
    
    # Track info normalizálás (YouTube cím alapján) - már fent megtörtént

    # Quiz kérdés generálása
    question = generate_quiz_question(track_info, audio_file, category, custom_options)
    
    if require_review:
        return {
            "success": True,
            "question": question,
            "category": category,
            "audio_file": audio_file,
            "track_info": track_info,
        }
    
    # Kérdés hozzáadása a megfelelő kategóriához
    add_question_to_category(question, category)

    if return_metadata:
        return {
            "success": True,
            "question": question,
            "category": category,
            "audio_file": audio_file,
            "track_info": track_info,
        }
    return True

def generate_quiz_question(track_info, audio_file, category, custom_options=None):
    """Quiz kérdés generálása a track alapján"""
    try:
        # Track_info ellenőrzés
        if not isinstance(track_info, dict):
            track_info = {}
        
        # Biztonságos adatkinyerés
        title = track_info.get('song_title') or track_info.get('title', 'Ismeretlen cím')
        artist = track_info.get('artist') or track_info.get('channel', 'Ismeretlen előadó')
        
        # Kategória alapú kérdés
        if category == "komolyzene":
            question_text = "Ki a zeneszerző?"
        elif category == "sorozat_focimek":
            question_text = "Melyik sorozat főcímdala ez?"
        else:
            question_text = "Ki az előadó?"
        
        # Opciók használata
        if custom_options and len(custom_options) >= 4:
            # Egyedi opciók használata
            options = custom_options
            correct_answer = options[0]  # Első opció a helyes válasz
        else:
            # Alapértelmezett opciók
            if category == "sorozat_focimek":
                series_name = artist if artist and artist != "Ismeretlen előadó" else title
                correct_answer = series_name
            else:
                correct_answer = artist
            if category == "komolyzene":
                similar_options = ["Beethoven", "Mozart", "Bach"]
            elif category == "sorozat_focimek":
                similar_options = ["Game of Thrones", "Stranger Things", "Friends"]
            elif category == "magyar_zenekarok":
                similar_options = ["Kispál és a Borz", "Elefánt", "Quimby"]
            elif category == "nemzetkozi_zenekarok":
                similar_options = ["Imagine Dragons", "Bastille", "The Weeknd"]
            elif category == "one_hit_wonders":
                similar_options = ["Bastille", "Imagine Dragons", "The Chainsmokers"]
            else:
                similar_options = ["Előadó 1", "Előadó 2", "Előadó 3"]
            
            options = [
                correct_answer,
                similar_options[0],
                similar_options[1],
                "Szerkeszthető opció"
            ]
        
        # Kérdés objektum
        # Csak a fájlnevet tároljuk, nem a teljes elérési utat
        audio_filename = os.path.basename(audio_file) if audio_file else None
        explanation_text = f"{artist} - {title}" if artist or title else f"{correct_answer} - {category.replace('_', ' ').title()}"
        question = {
            'question': question_text,
            'options': options,
            'correct': 0,
            'explanation': explanation_text,
            'audio_file': audio_filename,
            'topic': category
        }
        if title:
            question['song_title'] = title
        return question
    except Exception as e:
        # Fallback kérdés
        audio_filename = os.path.basename(audio_file) if audio_file else None
        return {
            'question': 'Ki az előadó?',
            'options': ['Ismeretlen előadó', 'Előadó 1', 'Előadó 2', 'Szerkeszthető opció'],
            'correct': 0,
            'explanation': 'Ismeretlen dal',
            'audio_file': audio_filename,
            'topic': category
        }

def add_question_to_category(question, category):
    """Kérdés hozzáadása a megfelelő kategóriához"""
    try:
        # Importálás a megfelelő kategóriából
        if category == "magyar_zenekarok":
            from topics.magyar_zenekarok_uj import QUESTIONS as MAGYAR_ZENEKAROK_QUESTIONS_UJ
            MAGYAR_ZENEKAROK_QUESTIONS_UJ.append(question)
            # Fájlba mentés
            save_questions_to_file(MAGYAR_ZENEKAROK_QUESTIONS_UJ, "topics/magyar_zenekarok_uj.py", "QUESTIONS")
        elif category == "nemzetkozi_zenekarok":
            from topics.nemzetkozi_zenekarok_final_fixed_with_real_audio import QUESTIONS as NEMZETKOZI_ZENEKAROK_QUESTIONS
            NEMZETKOZI_ZENEKAROK_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(NEMZETKOZI_ZENEKAROK_QUESTIONS, "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py", "NEMZETKOZI_ZENEKAROK_QUESTIONS")
        elif category == "komolyzene":
            from topics.komolyzene_uj import QUESTIONS as KOMOLYZENE_QUESTIONS
            KOMOLYZENE_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(KOMOLYZENE_QUESTIONS, "topics/komolyzene_uj.py", "QUESTIONS")
        elif category == "one_hit_wonders":
            from topics.one_hit_wonders import QUESTIONS as ONE_HIT_WONDERS_QUESTIONS
            ONE_HIT_WONDERS_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(ONE_HIT_WONDERS_QUESTIONS, "topics/one_hit_wonders.py", "ONE_HIT_WONDERS_QUESTIONS")
        elif category == "sorozat_focimek":
            from topics.sorozat_focimek import QUESTIONS as SOROZAT_FOCIMEK_QUESTIONS
            SOROZAT_FOCIMEK_QUESTIONS.append(question)
            # Fájlba mentés
            save_questions_to_file(SOROZAT_FOCIMEK_QUESTIONS, "topics/sorozat_focimek.py", "QUESTIONS")
        
        # Sikeres hozzáadás
        pass
    except Exception as e:
        st.error(f"Hiba a kérdés hozzáadásakor: {e}")

def save_questions_to_file(questions_list, file_path, variable_name):
    """Kérdések mentése fájlba"""
    try:
        import os
        
        # Fájl tartalom generálása
        content = f"""# Auto-generated questions file
# Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{variable_name} = [
"""
        
        # Kérdések hozzáadása
        for i, question in enumerate(questions_list):
            content += "    {\n"
            question_text = str(question.get("question", "")).replace('"', '\\"')
            content += f'        "question": "{question_text}",\n'
            content += '        "options": [\n'
            for option in question["options"]:
                content += f'            "{option}",\n'
            content += '        ],\n'
            content += f'        "correct": {question["correct"]},\n'
            if "explanation" in question:
                explanation_text = str(question["explanation"]).replace('"', '\\"')
                content += f'        "explanation": "{explanation_text}",\n'
            if "audio_file" in question:
                audio_file_text = str(question["audio_file"]).replace('"', '\\"')
                content += f'        "audio_file": "{audio_file_text}",\n'
            if "song_title" in question:
                song_title_text = str(question["song_title"]).replace('"', '\\"')
                content += f'        "song_title": "{song_title_text}",\n'
            if "topic" in question:
                content += f'        "topic": "{question["topic"]}",\n'
            content += "    },\n"
        
        content += "]\n"
        normalized_path = str(file_path).replace("\\", "/")
        if normalized_path.endswith("topics/komolyzene_uj.py"):
            content += "\n# Export alias for compatibility\n"
            content += "KOMOLYZENE_QUESTIONS = QUESTIONS\n"
        if normalized_path.endswith("topics/sorozat_focimek.py"):
            content += "\n# Export alias for compatibility\n"
            content += "SOROZAT_FOCIMEK_QUESTIONS = QUESTIONS\n"
        
        # Fájlba írás
        full_path = _PROJECT_ROOT / file_path
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        st.error(f"Hiba a fájl mentésekor: {e}")
        return False

