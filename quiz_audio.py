"""
Quiz audio: get_audio_file_for_question, get_all_audio_tracks, get_audio_tracks_by_category,
_parse_artist_and_title, _parse_artist_title_from_youtube, _get_piece_title_for_question.
"""

import os
import re
import glob
from pathlib import Path
from typing import Optional

from magyar_audio_mapping_uj import MAGYAR_AUDIO_MAPPING_UJ, get_magyar_audio_uj_path
from nemzetkozi_audio_mapping_updated import get_nemzetkozi_audio_path
from youtube_audio_mapping import get_youtube_audio_filename_cached

_PROJECT_ROOT = Path(__file__).parent


def get_audio_file_for_question(question, topic):
    """Visszaadja az audio fájl elérési útját a kérdéshez"""
    if topic == "magyar_zenekarok" or topic == "magyar_zenekarok_uj":
        if "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_path = get_magyar_audio_uj_path(index)
                if audio_path and os.path.exists(audio_path):
                    return str(audio_path)
            except Exception:
                pass
        elif "audio_file" in question and question["audio_file"]:
            audio_dir = _PROJECT_ROOT / "audio_files/magyar_zenekarok"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            audio_dir = _PROJECT_ROOT / "audio_files_magyar_uj"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
        return None
    elif topic == "nemzetkozi_zenekarok":
        if "audio_file" in question and question["audio_file"]:
            audio_dir = _PROJECT_ROOT / "audio_files/nemzetkozi_zenekarok"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            audio_dir = _PROJECT_ROOT / "audio_files"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
        elif "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_path = get_nemzetkozi_audio_path(index)
                if audio_path and audio_path.exists():
                    return str(audio_path)
            except Exception:
                pass
        elif "spotify_embed" in question and "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_path = get_nemzetkozi_audio_path(index)
                if audio_path and audio_path.exists():
                    return str(audio_path)
            except Exception:
                pass
    elif topic == "hip_hop":
        if "audio_file" in question and question["audio_file"]:
            audio_dir = _PROJECT_ROOT / "audio_files/hip_hop"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
    elif topic == "sorozat_focimek":
        if "audio_file" in question and question["audio_file"]:
            audio_dir = _PROJECT_ROOT / "audio_files/sorozat_focimek"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
            audio_dir = _PROJECT_ROOT / "audio_files"
            audio_path = audio_dir / question["audio_file"]
            if audio_path.exists():
                return str(audio_path)
    elif topic == "komolyzene":
        audio_dirs = [_PROJECT_ROOT / "audio_files/komolyzene"]
        audio_file = question.get("audio_file")
        if "original_index" in question:
            from komolyzene_audio_mapping import get_komolyzene_audio_path
            try:
                index = int(question["original_index"])
                audio_path = get_komolyzene_audio_path(index)
                if audio_path and audio_path.exists():
                    return str(audio_path)
            except Exception:
                pass
        if audio_file:
            for audio_dir in audio_dirs:
                audio_path = audio_dir / audio_file
                if audio_path.exists():
                    return str(audio_path)
            try:
                match = re.match(r"^\s*(\d+)", audio_file)
                if match:
                    num = match.group(1)
                    for audio_dir in audio_dirs:
                        if not audio_dir.exists():
                            continue
                        for candidate in audio_dir.glob(f"{num}*"):
                            if not candidate.is_file() or candidate.suffix.lower() != ".mp3":
                                continue
                            if re.match(fr"^{num}(\D|$)", candidate.name):
                                return str(candidate)
            except Exception:
                pass
        try:
            composer_candidates = []
            explanation = question.get("explanation")
            if explanation and ":" in explanation:
                composer_candidates.append(explanation.split(":", 1)[0])
            if "options" in question and "correct" in question:
                options = question.get("options") or []
                correct_index = question.get("correct")
                if isinstance(correct_index, int) and 0 <= correct_index < len(options):
                    composer_candidates.append(options[correct_index])
            if audio_file:
                base = os.path.splitext(os.path.basename(audio_file))[0]
                base = base.replace("Unknown Artist", "").replace("Unknown_Artist", "")
                composer_candidates.append(base)

            def _normalize_text(value: str) -> str:
                cleaned = value.lower().replace("_", " ")
                cleaned = re.sub(r"[^\w\s]", " ", cleaned, flags=re.UNICODE)
                return re.sub(r"\s+", " ", cleaned).strip()

            normalized_candidates = [_normalize_text(c) for c in composer_candidates if c]
            if normalized_candidates:
                matches = []
                for audio_dir in audio_dirs:
                    if not audio_dir.exists():
                        continue
                    for candidate in audio_dir.glob("*.mp3"):
                        candidate_norm = _normalize_text(candidate.stem)
                        if any(c and c in candidate_norm for c in normalized_candidates):
                            matches.append(candidate)
                if len(matches) == 1:
                    return str(matches[0])
                if audio_file:
                    match = re.match(r"^\s*(\d+)", audio_file)
                    if match:
                        num = match.group(1)
                        num_matches = [m for m in matches if re.match(fr"^{num}(\D|$)", m.name)]
                        if len(num_matches) == 1:
                            return str(num_matches[0])
        except Exception:
            pass
    elif topic == "one_hit_wonders":
        if "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_dir = _PROJECT_ROOT / "audio_files"
                for filename in os.listdir(audio_dir):
                    if filename.endswith('.mp3') and filename.startswith(f"{index:02d}_"):
                        audio_path = audio_dir / filename
                        if audio_path.exists():
                            return str(audio_path)
            except Exception:
                pass
        try:
            question_text = question.get("question", "")
            match = re.search(r"'([^']+)'", question_text)
            if match:
                song_title = match.group(1)
                audio_dir = _PROJECT_ROOT / "audio_files/one_hit_wonders"
                if audio_dir.exists():
                    for filename in os.listdir(audio_dir):
                        normalized_song_title = song_title.lower().replace(' ', '_')
                        normalized_filename = filename.lower()
                        if filename.endswith('.mp3') and (song_title.lower() in normalized_filename or normalized_song_title in normalized_filename):
                            audio_path = audio_dir / filename
                            if audio_path.exists():
                                return str(audio_path)
        except Exception:
            pass
        if "spotify_preview_url" in question and question["spotify_preview_url"]:
            return question["spotify_preview_url"]
        return None
    else:
        if "original_index" in question:
            try:
                index = int(question["original_index"])
                audio_filename = get_youtube_audio_filename_cached(index, topic)
                if audio_filename:
                    audio_dir = _PROJECT_ROOT / "audio_files"
                    audio_path = audio_dir / audio_filename
                    if audio_path.exists():
                        return str(audio_path)
            except Exception:
                pass
    return None


def get_all_audio_tracks():
    """Összes audio track összegyűjtése"""
    all_tracks = []
    audio_dirs = [
        "audio_files",
        "audio_files/sorozat_focimek",
        "magyar_audio",
        "nemzetkozi_audio",
        "komolyzene_audio",
        "one_hit_wonders_audio"
    ]
    audio_extensions = ["*.mp3", "*.wav", "*.m4a", "*.flac", "*.ogg"]

    for audio_dir in audio_dirs:
        if os.path.exists(audio_dir):
            for ext in audio_extensions:
                audio_files = glob.glob(f"{audio_dir}/{ext}")
                for audio_file in audio_files:
                    track_name = os.path.splitext(os.path.basename(audio_file))[0]
                    if not any(track["name"] == track_name for track in all_tracks):
                        all_tracks.append({
                            "name": track_name,
                            "audio_path": audio_file,
                            "directory": audio_dir
                        })
    return all_tracks


def get_audio_tracks_by_category():
    """Audio track-ek kategóriánként összegyűjtése"""
    categories = {
        "magyar_zenekarok": {
            "title": "🎵 Magyar Zenekarok",
            "audio_dirs": ["audio_files/magyar_zenekarok", "audio_files"],
            "question_file": "topics/magyar_zenekarok_uj.py"
        },
        "nemzetkozi_zenekarok": {
            "title": "🌍 Nemzetközi Zenekarok",
            "audio_dirs": ["audio_files/nemzetkozi_zenekarok", "audio_files"],
            "question_file": "topics/nemzetkozi_zenekarok_final_fixed_with_real_audio.py"
        },
        "komolyzene": {
            "title": "🎼 Komolyzene",
            "audio_dirs": ["audio_files/komolyzene", "audio_files"],
            "question_file": "topics/komolyzene_uj.py"
        },
        "one_hit_wonders": {
            "title": "⭐ One Hit Wonders",
            "audio_dirs": ["audio_files/one_hit_wonders", "audio_files"],
            "question_file": "topics/one_hit_wonders.py"
        },
        "sorozat_focimek": {
            "title": "📺 Sorozat főcímek",
            "audio_dirs": ["audio_files/sorozat_focimek", "audio_files"],
            "question_file": "topics/sorozat_focimek.py"
        },
        "hip_hop": {
            "title": "🎤 Hip-hop / Rap",
            "audio_dirs": ["audio_files/hip_hop"],
            "question_file": "topics/hip_hop.py"
        }
    }

    tracks_by_category = {}
    for category_key, category_info in categories.items():
        tracks = []
        for audio_dir in category_info["audio_dirs"]:
            if os.path.exists(audio_dir):
                for ext in ["*.mp3", "*.wav", "*.m4a"]:
                    audio_files = glob.glob(f"{audio_dir}/{ext}")
                    for audio_file in audio_files:
                        track_name = os.path.splitext(os.path.basename(audio_file))[0]
                        if not any(track["name"] == track_name for track in tracks):
                            tracks.append({
                                "name": track_name,
                                "audio_path": audio_file,
                                "question_file": category_info["question_file"]
                            })
        tracks_by_category[category_key] = {
            "title": category_info["title"],
            "tracks": tracks
        }
    return tracks_by_category


def _parse_artist_and_title(track_name: str):
    """Egyszerű előadó és cím kinyerés track névből"""
    name = track_name.strip()
    if ". " in name:
        name = name.split(". ", 1)[1]
    if " - " in name:
        artist, title = name.split(" - ", 1)
        return artist.strip(), title.strip()
    if "_" in name:
        parts = [p for p in name.split("_") if p]
        if parts and parts[0].isdigit():
            parts = parts[1:]
        if len(parts) >= 2:
            return parts[0].replace("_", " ").strip(), " ".join(parts[1:]).replace("_", " ").strip()
    return "Ismeretlen", name


def _parse_artist_title_from_youtube(youtube_title: str, channel: Optional[str] = None):
    """YouTube cím alapján előadó és cím kinyerése"""
    if not youtube_title:
        return channel or "Ismeretlen", "Ismeretlen cím"

    title = str(youtube_title).strip()
    title = re.sub(r"\s*\[[^\]]*\]\s*", " ", title)
    title = re.sub(r"\s*\([^)]*\)\s*", " ", title)
    title = re.sub(r"\s+", " ", title).strip()

    for sep in [" - ", " – ", " — ", " | "]:
        if sep in title:
            artist, song = title.split(sep, 1)
            return artist.strip() or (channel or "Ismeretlen"), song.strip() or title

    if channel:
        return channel.strip(), title
    return "Ismeretlen", title


def _get_piece_title_for_question(question: dict) -> Optional[str]:
    """Darab címének becsült kinyerése a kérdésből"""
    if not isinstance(question, dict):
        return None
    song_title = question.get("song_title")
    if song_title:
        return str(song_title).strip().strip('"')
    explanation = question.get("explanation")
    if explanation:
        explanation = str(explanation).strip()
        if ":" in explanation:
            title = explanation.split(":", 1)[1].strip()
            if title:
                return title
        if " - " in explanation:
            title = explanation.split(" - ", 1)[1].strip()
            if title:
                return title
    audio_file = question.get("audio_file")
    if audio_file:
        filename = os.path.splitext(os.path.basename(str(audio_file)))[0]
        _, title = _parse_artist_and_title(filename)
        if title and title != "Ismeretlen":
            return title.strip()
        cleaned = filename
        if ". " in cleaned:
            cleaned = cleaned.split(". ", 1)[1]
        cleaned = cleaned.replace("_", " ").strip()
        return cleaned or None
    return None
