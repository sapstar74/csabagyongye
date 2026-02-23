"""
Quiz sync: sync_with_github, sync_komolyzene_with_github, get_image_base64.
"""

import base64
import glob
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import streamlit as st

from i18n import t
from quiz_audio import get_all_audio_tracks


def sync_with_github():
    """GitHub-ról szinkronizálja az audiofájlokat és kérdéseket"""
    try:
        st.info(t("🔄 GitHub szinkronizálás indítása..."))

        st.markdown(t("### 📥 1. Legfrissebb változások letöltése..."))
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )

        if pull_result.returncode != 0:
            st.error(t("❌ Git pull hiba: {error}", error=pull_result.stderr))
            return False

        st.success(t("✅ Git pull sikeres!"))

        st.markdown(t("### 🎵 2. Új audiofájlok keresése..."))
        all_tracks = get_all_audio_tracks()
        audio_files = [track["audio_path"] for track in all_tracks]

        st.info(t("📊 {count} audiofájl található", count=len(audio_files)))

        category_stats = {}
        for track in all_tracks:
            directory = track["directory"]
            if directory not in category_stats:
                category_stats[directory] = 0
            category_stats[directory] += 1

        st.markdown(t("**📁 Kategóriánkénti eloszlás:**"))
        for directory, count in category_stats.items():
            st.markdown(t("- {directory}: {count} track", directory=directory, count=count))

        st.markdown(t("### 📝 3. Új kérdés fájlok keresése..."))
        question_files = []
        topics_patterns = [
            "topics/*.py",
            "topics/*_questions.py",
            "topics/*_complete.py"
        ]
        for pattern in topics_patterns:
            files = glob.glob(pattern)
            question_files.extend(files)

        st.info(t("📊 {count} kérdés fájl található", count=len(question_files)))

        st.markdown(t("### 📋 4. Új tartalmak összefoglalása..."))
        if audio_files:
            st.markdown(t("**🎵 Új audiofájlok:**"))
            for file in audio_files:
                st.markdown(t("- {filename}", filename=os.path.basename(file)))
        if question_files:
            st.markdown(t("**📝 Kérdés fájlok:**"))
            for file in question_files:
                st.markdown(t("- {filename}", filename=os.path.basename(file)))

        st.markdown(t("### 🔄 5. Alkalmazás újraindítása..."))
        st.warning(t("⚠️ A szinkronizálás után javasolt az alkalmazás újraindítása a legfrissebb tartalmak betöltéséhez."))

        if st.button(t("🔄 Alkalmazás újraindítása"), type="primary"):
            st.rerun()

        st.success(t("✅ GitHub szinkronizálás sikeresen befejezve!"))
        return True

    except Exception as e:
        st.error(t("❌ Szinkronizálási hiba: {error}", error=e))
        return False


def sync_komolyzene_with_github(question_file_path: Optional[str] = None) -> bool:
    """Teljes komolyzene Git sync (pull + add/commit/push)"""
    try:
        repo_root = Path(__file__).parent
        if not (repo_root / ".git").exists():
            st.error(t("❌ Git repo nem található, szinkronizálás nem lehetséges."))
            return False

        st.info(t("🔄 Komolyzene Git sync indítása..."))

        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'main'],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if pull_result.returncode != 0:
            st.error(t("❌ Git pull hiba: {error}", error=pull_result.stderr or pull_result.stdout))
            return False
        st.success(t("✅ Git pull sikeres!"))

        sync_paths = []
        if question_file_path:
            sync_paths.append(question_file_path)
        else:
            sync_paths.append("topics/komolyzene_uj.py")

        candidate_dirs = ["audio_files/komolyzene"]
        for path in candidate_dirs:
            if (repo_root / path).exists():
                sync_paths.append(path)

        existing_paths = [p for p in dict.fromkeys(sync_paths) if (repo_root / p).exists()]
        if not existing_paths:
            st.warning(t("⚠️ Nincsenek komolyzene fájlok a szinkronhoz."))
            return False

        add_result = subprocess.run(
            ['git', 'add', '-A', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if add_result.returncode != 0:
            st.error(t("❌ Git add hiba: {error}", error=add_result.stderr or add_result.stdout))
            return False

        diff_result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if diff_result.returncode != 0:
            st.error(t("❌ Git diff hiba: {error}", error=diff_result.stderr or diff_result.stdout))
            return False

        if not diff_result.stdout.strip():
            st.info(t("ℹ️ Nincs komolyzene változás a szinkronhoz."))
            return True

        commit_msg = f"Komolyzene sync - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_msg, '--', *existing_paths],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if commit_result.returncode != 0:
            st.error(t("❌ Git commit hiba: {error}", error=commit_result.stderr or commit_result.stdout))
            return False

        push_result = subprocess.run(
            ['git', 'push'],
            capture_output=True,
            text=True,
            cwd=str(repo_root)
        )
        if push_result.returncode != 0:
            st.error(t("❌ Git push hiba: {error}", error=push_result.stderr or push_result.stdout))
            return False

        st.success(t("✅ Komolyzene Git sync sikeres!"))
        return True
    except Exception as e:
        st.error(t("❌ Komolyzene sync hiba: {error}", error=e))
        return False


@st.cache_data(ttl=3600, show_spinner=False)
def get_image_base64(image_path):
    """Kép konvertálása base64 formátumra"""
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        return encoded_string
    except Exception as e:
        st.error(t("Hiba a kép betöltése során: {error}", error=e))
        return ""


_REPO_ROOT = Path(__file__).parent


def check_github_sync_status():
    """GitHub szinkronizáció állapotának ellenőrzése"""
    try:
        cwd = str(_REPO_ROOT)
        result = subprocess.run(['git', 'status', '--porcelain'],
                                capture_output=True, text=True, cwd=cwd)

        if result.returncode != 0:
            return {"error": "Git status hiba", "details": result.stderr}

        local_changes = result.stdout.strip()

        fetch_result = subprocess.run(['git', 'fetch', 'origin'],
                                      capture_output=True, text=True, cwd=cwd)

        if fetch_result.returncode != 0:
            return {"error": "Git fetch hiba", "details": fetch_result.stderr}

        diff_result = subprocess.run(['git', 'diff', 'HEAD', 'origin/main', '--name-only'],
                                     capture_output=True, text=True, cwd=cwd)

        if diff_result.returncode != 0:
            return {"error": "Git diff hiba", "details": diff_result.stderr}

        remote_changes = diff_result.stdout.strip()

        return {
            "local_changes": local_changes,
            "remote_changes": remote_changes,
            "has_local_changes": bool(local_changes),
            "has_remote_changes": bool(remote_changes)
        }

    except Exception as e:
        return {"error": "Szinkronizáció ellenőrzés hiba", "details": str(e)}


def show_github_sync_dialog():
    """GitHub szinkronizáció dialógus megjelenítése"""
    st.markdown("### 🔄 GitHub Szinkronizáció")

    with st.spinner("GitHub állapot ellenőrzése..."):
        sync_status = check_github_sync_status()

    if "error" in sync_status:
        st.error(f"❌ Hiba a szinkronizáció ellenőrzése során: {sync_status['error']}")
        if sync_status.get('details'):
            st.code(sync_status['details'])
        return False

    if sync_status["has_local_changes"]:
        st.warning("⚠️ **Lokális változások vannak:**")
        st.code(sync_status["local_changes"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lokális változások mentése", type="primary"):
                try:
                    subprocess.run(['git', 'add', '.'], cwd=str(_REPO_ROOT))
                    subprocess.run(['git', 'commit', '-m', 'Auto-save before sync'], cwd=str(_REPO_ROOT))
                    subprocess.run(['git', 'push'], cwd=str(_REPO_ROOT))
                    st.success("✅ Lokális változások mentve!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba a mentés során: {e}")

        with col2:
            if st.button("🗑️ Lokális változások eldobása", type="secondary"):
                try:
                    subprocess.run(['git', 'reset', '--hard', 'HEAD'], cwd=str(_REPO_ROOT))
                    st.success("✅ Lokális változások eldobva!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba az eldobás során: {e}")

        st.markdown("---")

    if sync_status["has_remote_changes"]:
        st.info("📥 **Új változások érkeztek a GitHub-ról:**")
        st.code(sync_status["remote_changes"])

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Változások letöltése", type="primary"):
                try:
                    subprocess.run(['git', 'pull', 'origin', 'main'], cwd=str(_REPO_ROOT))
                    st.success("✅ Változások letöltve!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Hiba a letöltés során: {e}")

        with col2:
            if st.button("⏭️ Kihagyás", type="secondary"):
                st.info("ℹ️ Változások kihagyva. Folytathatod a munkát.")

        st.markdown("---")

    if not sync_status["has_local_changes"] and not sync_status["has_remote_changes"]:
        st.success("✅ **Minden szinkronizálva!** Nincs új változás.")

        if st.button("🔄 Frissítés ellenőrzése", type="secondary"):
            st.rerun()

    return True
