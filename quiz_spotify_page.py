"""
Quiz Spotify page: show_spotify_playlist_main, show_spotify_playlist_tab.
"""

import os
import time

import streamlit as st


def show_spotify_playlist_main():
    """Spotify playlist fő képernyő"""

    try:
        from spotify_playlist_integration import SpotifyPlaylistQuiz, format_duration, format_views

        # Spotify Playlist Quiz inicializálása
        if 'spotify_quiz' not in st.session_state:
            st.session_state.spotify_quiz = SpotifyPlaylistQuiz()

        # OAuth token visszaállítása session state-ből
        if 'oauth_token' in st.session_state and 'oauth_token_expires' in st.session_state:
            if time.time() < st.session_state.oauth_token_expires:
                st.session_state.spotify_quiz.restore_oauth_token(
                    st.session_state.oauth_token,
                    st.session_state.oauth_token_expires
                )

        # CSS stílus a rejtett st.button-ok elrejtéséhez
        st.markdown("""
        <style>
        /* Rejtett st.button-ok elrejtése */
        .stButton > button {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            background: transparent !important;
        }

        /* Rejtett st.button-ok teljes elrejtése */
        div[data-testid="stButton"] {
            display: none !important;
        }

        /* Rejtett st.button-ok konténer elrejtése */
        .stButton {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        st.header("🎵 Spotify Playlist Feldolgozás")

        # OAuth beállítás szekció
        with st.expander("🔐 Spotify OAuth Beállítás (Nyilvános playlistekhez)", expanded=False):
            st.markdown("**A nyilvános Spotify playlistek eléréséhez OAuth autentikáció szükséges.**")

            # OAuth URL generálás
            if st.button("🔗 OAuth URL Generálása"):
                auth_url = st.session_state.spotify_quiz.get_oauth_authorization_url()
                st.markdown(f"**Nyisd meg ezt a linket a böngészőben:**")
                st.code(auth_url)
                st.info("1. Kattints a linkre és engedélyezd a hozzáférést")
                st.info("2. Másold ki az authorization code-ot az URL-ből")
                st.info("3. Illeszd be az authorization code-ot alább")

            # Authorization code bevitel
            auth_code = st.text_input(
                "Authorization Code:",
                placeholder="Például: AQAA...",
                help="Illeszd be az authorization code-ot a Spotify OAuth flow-ból"
            )

            if st.button("🔑 OAuth Token Beállítása"):
                if auth_code:
                    with st.spinner("OAuth token beállítása..."):
                        success = st.session_state.spotify_quiz.set_oauth_access_token(auth_code)
                        if success:
                            st.success("✅ OAuth token sikeresen beállítva!")
                            st.info("Most már elérheted a nyilvános Spotify playlisteket!")
                        else:
                            st.error("❌ OAuth token beállítása sikertelen!")
                else:
                    st.warning("⚠️ Kérlek add meg az authorization code-ot!")

            # OAuth állapot megjelenítése
            if hasattr(st.session_state.spotify_quiz.playlist_manager, 'oauth_access_token') and st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                if time.time() < token_expires:
                    remaining_time = int(token_expires - time.time())
                    st.success(f"✅ OAuth token aktív (Hátralévő idő: {remaining_time} másodperc)")
                else:
                    st.warning("⚠️ OAuth token lejárt, újra kell autentikálni!")
            else:
                st.info("ℹ️ Nincs aktív OAuth token")

        # Spotify playlist URL beviteli mező
        playlist_url = st.text_input(
            "Spotify Playlist URL:",
            placeholder="https://open.spotify.com/playlist/...",
            help="Add meg a Spotify playlist URL-jét"
        )

        # Playlist betöltés gomb
        if st.button("📥 Playlist Betöltése", type="primary"):
            if playlist_url:
                with st.spinner("Playlist betöltése..."):
                    try:
                        # Spotify playlist betöltése
                        tracks = st.session_state.spotify_quiz.get_playlist_tracks(playlist_url)
                        if tracks:
                            st.session_state.playlist_tracks = tracks
                            st.success(f"✅ {len(tracks)} track betöltve!")
                            st.rerun()
                        else:
                            st.error("❌ Nem sikerült betölteni a playlist-et")
                    except Exception as e:
                        st.error(f"❌ Hiba a playlist betöltésekor: {e}")
            else:
                st.warning("⚠️ Kérlek add meg a playlist URL-jét!")

        # Playlist elemek megjelenítése
        if hasattr(st.session_state, 'playlist_tracks') and st.session_state.playlist_tracks:
            st.subheader(f"📋 Playlist Elemek ({len(st.session_state.playlist_tracks)} track)")

            # Statisztikák
            downloaded_count = sum(1 for track in st.session_state.playlist_tracks if track.get('downloaded', False))
            youtube_ready_count = sum(1 for track in st.session_state.playlist_tracks if track.get('youtube_url'))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Összesen", len(st.session_state.playlist_tracks))
            with col2:
                st.metric("✅ Letöltve", downloaded_count)
            with col3:
                st.metric("📺 YouTube kész", youtube_ready_count)

            # Grid layout a trackekhez
            cols_per_row = 3
            for i in range(0, len(st.session_state.playlist_tracks), cols_per_row):
                row_tracks = st.session_state.playlist_tracks[i:i + cols_per_row]
                cols = st.columns(cols_per_row)

                for j, track in enumerate(row_tracks):
                    with cols[j]:
                        # Track azonosító
                        track_id = track.get('id', f"track_{i}_{j}")

                        # Album Art Work megjelenítése kattinthatóként
                        if track.get('album_art_url'):
                            # Album art megjelenítése
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="{track['album_art_url']}"
                                     alt="Album Art"
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Placeholder kép megjelenítése
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="https://picsum.photos/150/150?random={i}_{j}"
                                     alt="No Image"
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)

                        # Kattintható gomb a letöltéshez
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button(
                                f"🎵 {track['name']}",
                                key=f"download_{track_id}",
                                help=f"Kattints a letöltéshez: {track['name']}",
                                use_container_width=True
                            ):
                                # YouTube keresés csak kattintás után
                                if not track.get('youtube_url'):
                                    with st.spinner(f"YouTube keresés: {track['name']}..."):
                                        youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                        if youtube_result:
                                            track['youtube_url'] = youtube_result.get('url')
                                            track['youtube_title'] = youtube_result.get('title')
                                            track['youtube_views'] = youtube_result.get('views')
                                            track['youtube_duration'] = youtube_result.get('duration')
                                            track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')
                                            track['youtube_found'] = True
                                            st.success("✅ YouTube találat!")
                                            st.rerun()
                                        else:
                                            st.info("ℹ️ YouTube keresés folyamatban...")
                                            st.rerun()
                                            return

                                # MP3 letöltés YouTube URL-rel
                                if track.get('youtube_url'):
                                    with st.spinner(f"MP3 letöltés: {track['name']}..."):
                                        try:
                                            audio_path = st.session_state.spotify_quiz.audio_downloader.download_track(
                                                track['youtube_url'],
                                                track
                                            )
                                            if audio_path:
                                                track['downloaded'] = True
                                                track['audio_path'] = audio_path
                                                st.success(f"✅ MP3 letöltve: {os.path.basename(audio_path)}")
                                                with open(audio_path, "rb") as audio_file:
                                                    st.audio(audio_file.read(), format="audio/mp3")
                                                st.rerun()
                                            else:
                                                st.error("❌ MP3 letöltés sikertelen")
                                        except Exception as e:
                                            st.error(f"❌ Letöltési hiba: {e}")
                                else:
                                    st.info("ℹ️ YouTube keresés szükséges a letöltéshez")

                        # Track információk
                        st.markdown(f"**{track['name']}**")
                        st.markdown(f"*{', '.join(track['artists'])}*")
                        st.markdown(f"⏱️ {format_duration(track['duration_ms'])}")

                        # Linkek
                        if track.get('external_url'):
                            st.markdown(f"[🎵 Spotify]({track['external_url']})")
                        if track.get('youtube_url'):
                            st.markdown(f"[📺 YouTube]({track['youtube_url']})")

                        # Letöltési állapot megjelenítése
                        if track.get('downloaded', False):
                            st.markdown(
                                f"<div style='color: #0f766e; font-weight: 600; font-family: Inter, sans-serif;'>✅ Letöltve</div>",
                                unsafe_allow_html=True
                            )

                        st.markdown("---")

            # Részletes táblázat is elérhető
            with st.expander("📊 Részletes Táblázat"):
                table_data = []
                for i, track in enumerate(st.session_state.playlist_tracks):
                    row = {
                        "Sorszám": i + 1,
                        "Cím": track['name'],
                        "Előadó": ", ".join(track['artists']),
                        "Album": track['album'],
                        "Hossz": format_duration(track['duration_ms']),
                        "YouTube": "✅" if track.get('youtube_url') else "❌"
                    }

                    if track.get('youtube_url'):
                        row["YouTube Cím"] = track.get('youtube_title', 'N/A')
                        row["YouTube Hossz"] = format_duration(track.get('youtube_duration', 0) * 1000) if track.get('youtube_duration') else 'N/A'
                        row["Nézettség"] = format_views(track.get('youtube_views', 0)) if track.get('youtube_views') else 'N/A'

                    table_data.append(row)

                st.dataframe(
                    table_data,
                    use_container_width=True,
                    hide_index=True
                )

    except ImportError:
        st.error("❌ Spotify playlist funkció nem elérhető")
        st.info("A spotify_playlist_integration.py fájl szükséges")
        st.code("pip install yt-dlp")


def show_spotify_playlist_tab():
    """Spotify playlist tab megjelenítése"""
    st.markdown("### 🎵 Spotify Playlist Feldolgozás")

    try:
        from spotify_playlist_integration import SpotifyPlaylistQuiz, format_duration, format_views

        # Spotify Playlist Quiz inicializálása
        if 'spotify_quiz' not in st.session_state:
            st.session_state.spotify_quiz = SpotifyPlaylistQuiz()

        # OAuth beállítás szekció
        with st.expander("🔐 Spotify OAuth Beállítás (Nyilvános playlistekhez)", expanded=False):
            st.markdown("**A nyilvános Spotify playlistek eléréséhez OAuth autentikáció szükséges.**")

            # OAuth URL generálás
            if st.button("🔗 OAuth URL Generálása", key="oauth_url_audio"):
                auth_url = st.session_state.spotify_quiz.get_oauth_authorization_url()
                st.markdown(f"**Nyisd meg ezt a linket a böngészőben:**")
                st.code(auth_url)
                st.info("1. Kattints a linkre és engedélyezd a hozzáférést")
                st.info("2. Másold ki az authorization code-ot az URL-ből")
                st.info("3. Illeszd be az authorization code-ot alább")

            # Authorization code bevitel
            auth_code = st.text_input(
                "Authorization Code:",
                placeholder="Például: AQAA...",
                help="Illeszd be az authorization code-ot a Spotify OAuth flow-ból",
                key="auth_code_audio"
            )

            if st.button("🔑 OAuth Token Beállítása", key="oauth_token_audio"):
                if auth_code:
                    with st.spinner("OAuth token beállítása..."):
                        success = st.session_state.spotify_quiz.set_oauth_access_token(auth_code)
                        if success:
                            st.success("✅ OAuth token sikeresen beállítva!")
                            st.info("Most már elérheted a nyilvános Spotify playlisteket!")
                            st.session_state.oauth_token = st.session_state.spotify_quiz.playlist_manager.oauth_access_token
                            st.session_state.oauth_token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                            st.rerun()
                        else:
                            st.error("❌ OAuth token beállítása sikertelen!")
                else:
                    st.warning("⚠️ Kérlek add meg az authorization code-ot!")

            # OAuth állapot megjelenítése
            if hasattr(st.session_state.spotify_quiz.playlist_manager, 'oauth_access_token') and st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                if time.time() < token_expires:
                    remaining_time = int(token_expires - time.time())
                    st.success(f"✅ OAuth token aktív (Hátralévő idő: {remaining_time} másodperc)")
                    st.session_state.oauth_token = st.session_state.spotify_quiz.playlist_manager.oauth_access_token
                    st.session_state.oauth_token_expires = st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at
                else:
                    st.warning("⚠️ OAuth token lejárt, újra kell autentikálni!")
            else:
                st.info("ℹ️ Nincs aktív OAuth token")

        # Fő tartalom
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### 📋 Playlist Feldolgozás")

            # Playlist URL input
            playlist_url = st.text_input(
                "Spotify Playlist URL",
                value="https://open.spotify.com/playlist/37i9dQZEVXbMDoHDwVN2tF",
                placeholder="https://open.spotify.com/playlist/...",
                help="Illeszd be a Spotify playlist URL-jét (alapértelmezett: Global Top 50)"
            )

            # Playlist feldolgozása
            if st.button("🎵 Playlist Feldolgozása", key="process_playlist"):
                if 'spotify_quiz' not in st.session_state:
                    st.session_state.spotify_quiz = SpotifyPlaylistQuiz()

                # OAuth token ellenőrzése
                if not hasattr(st.session_state.spotify_quiz, 'playlist_manager') or \
                   not st.session_state.spotify_quiz.playlist_manager.oauth_access_token:
                    st.error("❌ Nincs aktív OAuth token!")
                    st.info("🔐 Kérlek állítsd be az OAuth tokent a fenti expanderben!")
                    return

                # Token lejárat ellenőrzése
                if time.time() >= st.session_state.spotify_quiz.playlist_manager.oauth_token_expires_at:
                    st.error("❌ Az OAuth token lejárt!")
                    st.info("🔄 Kérlek generálj új tokent!")
                    return

                with st.spinner("Playlist feldolgozása..."):
                    try:
                        tracks = st.session_state.spotify_quiz.get_playlist_tracks_only(playlist_url)

                        if tracks:
                            st.session_state.spotify_playlist_tracks = tracks
                            st.success(f"✅ {len(tracks)} track betöltve!")
                            st.rerun()
                        else:
                            st.warning("⚠️ Nincsenek trackek a playlistben!")
                            st.info("🔍 Lehetséges okok:")
                            st.info("• Privát playlist")
                            st.info("• Érvénytelen playlist URL")
                            st.info("• Spotify API hiba")
                    except Exception as e:
                        st.error(f"❌ Hiba a playlist feldolgozásakor: {e}")
                        st.info("🔐 Ellenőrizd az OAuth tokent vagy próbálj másik playlistet!")

        with col2:
            st.markdown("### 📊 Debug Információk")

            # Debug információk
            if 'spotify_quiz' in st.session_state and hasattr(st.session_state.spotify_quiz, 'playlist_manager'):
                manager = st.session_state.spotify_quiz.playlist_manager
                if manager.oauth_access_token:
                    token_expires = manager.oauth_token_expires_at
                    time_left = token_expires - time.time()
                    if time_left > 0:
                        st.success(f"🔐 OAuth Token aktív ({time_left:.0f}s hátra)")

                        # API teszt gomb
                        if st.button("🧪 API Teszt", key="api_test"):
                            import requests
                            headers = {
                                'Authorization': f'Bearer {manager.oauth_access_token}',
                                'Content-Type': 'application/json'
                            }

                            test_url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF"
                            response = requests.get(test_url, headers=headers)

                            if response.status_code == 200:
                                data = response.json()
                                st.success(f"✅ API működik!")
                                st.info(f"Playlist: {data.get('name')}")
                                st.info(f"Tracks: {len(data.get('tracks', {}).get('items', []))}")
                            else:
                                st.error(f"❌ API hiba: {response.status_code}")
                                st.error(f"Response: {response.text}")
                    else:
                        st.error("❌ OAuth Token lejárt!")
                else:
                    st.warning("⚠️ Nincs OAuth token")

            # Session state debug
            st.markdown("### 🔍 Session State")
            if 'oauth_token' in st.session_state:
                st.info("✅ Token mentve session state-ben")
            else:
                st.warning("⚠️ Token nincs mentve session state-ben")

            if hasattr(st.session_state, 'spotify_playlist_tracks') and st.session_state.spotify_playlist_tracks:
                total_tracks = len(st.session_state.spotify_playlist_tracks)
                youtube_tracks = len([t for t in st.session_state.spotify_playlist_tracks if t.get('youtube_url')])

                st.metric("Összes track", total_tracks)
                st.metric("🎬 YouTube", youtube_tracks)
                st.metric("Találati arány", f"{youtube_tracks/total_tracks*100:.1f}%")

        # Playlist megjelenítése (ha van)
        if hasattr(st.session_state, 'spotify_playlist_tracks') and st.session_state.spotify_playlist_tracks:
            st.markdown("---")
            st.markdown("### 🎵 Playlist Elemek")

            # Grid layout a trackekhez
            cols_per_row = 3
            for i in range(0, len(st.session_state.spotify_playlist_tracks), cols_per_row):
                row_tracks = st.session_state.spotify_playlist_tracks[i:i + cols_per_row]
                cols = st.columns(cols_per_row)

                for j, track in enumerate(row_tracks):
                    with cols[j]:
                        track_id = track.get('id', f"track_{i}_{j}")

                        # Kép megjelenítése
                        image_url = None
                        if track.get('youtube_thumbnail_url'):
                            image_url = track['youtube_thumbnail_url']
                        elif track.get('album_art_url'):
                            image_url = track['album_art_url']

                        if image_url:
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0;">
                                <img src="{image_url}"
                                     alt="Track Image"
                                     style="width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px;">
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="text-align: center; margin: 10px 0; width: 150px; height: 150px; border: 2px solid #ddd; border-radius: 8px; display: flex; align-items: center; justify-content: center; background-color: #f0f0f0;">
                                <span style="color: #78716c; font-size: 12px;">Nincs kép</span>
                            </div>
                            """, unsafe_allow_html=True)

                        # Kattintható gomb a letöltéshez
                        col1, col2, col3 = st.columns([1, 2, 1])
                        with col2:
                            if st.button(
                                f"🎵 {track['name']}",
                                key=f"download_{track_id}_audio",
                                help=f"Kattints a letöltéshez: {track['name']}",
                                use_container_width=True
                            ):
                                if not track.get('youtube_url'):
                                    with st.spinner(f"YouTube keresés: {track['name']}..."):
                                        youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                        if youtube_result:
                                            track['youtube_url'] = youtube_result.get('url')
                                            track['youtube_title'] = youtube_result.get('title')
                                            track['youtube_views'] = youtube_result.get('views')
                                            track['youtube_duration'] = youtube_result.get('duration')
                                            track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')
                                            track['youtube_found'] = True
                                            st.success("✅ YouTube találat!")
                                            st.rerun()
                                        else:
                                            st.info("ℹ️ YouTube keresés folyamatban...")
                                            st.rerun()
                                            return

                                if track.get('youtube_url'):
                                    with st.spinner(f"MP3 letöltés: {track['name']}..."):
                                        try:
                                            audio_path = st.session_state.spotify_quiz.audio_downloader.download_track(
                                                track['youtube_url'],
                                                track
                                            )
                                            if audio_path:
                                                track['downloaded'] = True
                                                track['audio_path'] = audio_path
                                                st.success(f"✅ MP3 letöltve: {os.path.basename(audio_path)}")
                                                with open(audio_path, "rb") as audio_file:
                                                    st.audio(audio_file.read(), format="audio/mp3")
                                                st.rerun()
                                            else:
                                                st.error("❌ MP3 letöltés sikertelen")
                                        except Exception as e:
                                            st.error(f"❌ Letöltési hiba: {e}")
                                else:
                                    st.info("ℹ️ YouTube keresés szükséges a letöltéshez")

                        # Track információk
                        st.markdown(f"**{track['name']}**")
                        st.markdown(f"*{', '.join(track['artists'])}*")
                        st.markdown(f"💿 {track['album']}")

                        if not track.get('youtube_url'):
                            if st.button(f"🔍 YouTube Keresés", key=f"youtube_search_{i}_{j}"):
                                with st.spinner(f"YouTube keresés: {track['name']}..."):
                                    youtube_result = st.session_state.spotify_quiz.search_youtube_for_track(track)
                                    if youtube_result:
                                        track['youtube_url'] = youtube_result.get('url')
                                        track['youtube_title'] = youtube_result.get('title')
                                        track['youtube_views'] = youtube_result.get('views')
                                        track['youtube_duration'] = youtube_result.get('duration')
                                        track['youtube_thumbnail_url'] = youtube_result.get('thumbnail_url')
                                        track['youtube_found'] = True
                                        st.success("✅ YouTube találat!")
                                        st.rerun()
                                    else:
                                        st.info("ℹ️ YouTube keresés folyamatban...")
                                        st.rerun()
                                        return
                        else:
                            if st.button(f"💾 Letöltés", key=f"download_{i}_{j}"):
                                with st.spinner(f"Letöltés: {track['name']}..."):
                                    downloaded_file = st.session_state.spotify_quiz.download_selected_tracks([track], [0])
                                    if downloaded_file:
                                        track['downloaded'] = True
                                        st.success(f"✅ Letöltve: {downloaded_file[0]}")
                                    else:
                                        st.error("❌ Letöltési hiba!")

                        # YouTube információk megjelenítése
                        if track.get('youtube_url'):
                            st.write(f"🎬 [YouTube]({track['youtube_url']})")
                            if track.get('youtube_views'):
                                st.write(f"👁️ {format_views(track['youtube_views'])} nézettség")
                            if track.get('youtube_duration'):
                                st.write(f"⏱️ {format_duration(track['youtube_duration'] * 1000)}")

                        st.divider()
        else:
            st.info("ℹ️ Nincsenek trackek betöltve. Feldolgozz egy playlistet!")

    except ImportError:
        st.error("❌ Spotify playlist funkció nem elérhető")
        st.info("A spotify_playlist_integration.py fájl szükséges")
        st.code("pip install yt-dlp")
