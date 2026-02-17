from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Optional

import requests
import streamlit as st

LANG_OPTIONS = {
    "hu": "🇭🇺 Magyar",
    "en": "🇬🇧 English",
}

_EN_TRANSLATIONS = {
    "Nyelv": "Language",
    "Csabagyöngye Tréning Center": "Csabagyöngye Training Center",
    "🎯 Csabagyöngye Tréning Center 😄": "🎯 Csabagyöngye Training Center 😄",
    "## 🧭 Navigáció": "## 🧭 Navigation",
    "Válassz oldalt:": "Choose a page:",
    "🎯 Quiz": "🎯 Quiz",
    "🎵 Spotify Playlist": "🎵 Spotify Playlist",
    "📊 Analytics": "📊 Analytics",
    "⚙️ Beállítások": "⚙️ Settings",
    "🎵 Audio hozzáadása": "🎵 Add Audio",
    "🔄 GitHub Szinkronizálás": "🔄 GitHub Sync",
    "🎵 Audio Track Kezelés": "🎵 Audio Track Management",
    "🎼 Előadók szerinti lista": "🎼 Artist List",
    "## 🔤 Betűméret": "## 🔤 Font size",
    "Válassz betűméretet:": "Choose font size:",
    "📝 Normál": "📝 Normal",
    "🔍 Nagy": "🔍 Large",
    "🗑️ Cache törlése": "🗑️ Clear cache",
    "Cache törölve!": "Cache cleared!",
    "🔄 GitHub szinkronizálás indítása...": "🔄 Starting GitHub sync...",
    "### 📥 1. Legfrissebb változások letöltése...": "### 📥 1. Download latest changes...",
    "❌ Git pull hiba: {error}": "❌ Git pull error: {error}",
    "✅ Git pull sikeres!": "✅ Git pull successful!",
    "### 🎵 2. Új audiofájlok keresése...": "### 🎵 2. Searching for new audio files...",
    "📊 {count} audiofájl található": "📊 {count} audio files found",
    "**📁 Kategóriánkénti eloszlás:**": "**📁 Distribution by category:**",
    "- {directory}: {count} track": "- {directory}: {count} tracks",
    "### 📝 3. Új kérdés fájlok keresése...": "### 📝 3. Searching for new question files...",
    "📊 {count} kérdés fájl található": "📊 {count} question files found",
    "### 📋 4. Új tartalmak összefoglalása...": "### 📋 4. Summary of new content...",
    "**🎵 Új audiofájlok:**": "**🎵 New audio files:**",
    "- {filename}": "- {filename}",
    "**📝 Kérdés fájlok:**": "**📝 Question files:**",
    "### 🔄 5. Alkalmazás újraindítása...": "### 🔄 5. Restart application...",
    "⚠️ A szinkronizálás után javasolt az alkalmazás újraindítása a legfrissebb tartalmak betöltéséhez.": "⚠️ After syncing, it is recommended to restart the app to load the latest content.",
    "🔄 Alkalmazás újraindítása": "🔄 Restart application",
    "✅ GitHub szinkronizálás sikeresen befejezve!": "✅ GitHub sync completed successfully!",
    "❌ Szinkronizálási hiba: {error}": "❌ Sync error: {error}",
    "❌ Git repo nem található, szinkronizálás nem lehetséges.": "❌ Git repo not found, sync not possible.",
    "🔄 Komolyzene Git sync indítása...": "🔄 Starting classical music Git sync...",
    "⚠️ Nincsenek komolyzene fájlok a szinkronhoz.": "⚠️ No classical music files to sync.",
    "❌ Git add hiba: {error}": "❌ Git add error: {error}",
    "❌ Git diff hiba: {error}": "❌ Git diff error: {error}",
    "ℹ️ Nincs komolyzene változás a szinkronhoz.": "ℹ️ No classical music changes to sync.",
    "❌ Git commit hiba: {error}": "❌ Git commit error: {error}",
    "❌ Git push hiba: {error}": "❌ Git push error: {error}",
    "✅ Komolyzene Git sync sikeres!": "✅ Classical music Git sync successful!",
    "❌ Komolyzene sync hiba: {error}": "❌ Classical music sync error: {error}",
    "Hiba a kép betöltése során: {error}": "Error loading image: {error}",
    "🎼 Szerző szerinti lista": "🎼 Artist List",
    "📭 Nincs elérhető zenei kategória.": "📭 No music category available.",
    "### 🎵 Zenei kategória választás": "### 🎵 Music category selection",
    "📭 Nincsenek track-ek ebben a kategóriában.": "📭 No tracks in this category.",
    "### {category}": "### {category}",
    "📊 **{track_count} track**, **{artist_count} előadó**": "📊 **{track_count} tracks**, **{artist_count} artists**",
    "{artist} ({count})": "{artist} ({count})",
    "{title} ({filename})": "{title} ({filename})",
    "▶️ Lejátszás": "▶️ Play",
    "⏹ Stop": "⏹ Stop",
    "🔧 Audio módosítás": "🔧 Audio editing",
    "A feltöltött fájl felülírja az eredeti tracket (név változatlan).": "The uploaded file overwrites the original track (name unchanged).",
    "Új MP3 feltöltése": "Upload new MP3",
    "Igen, felülírom az eredeti fájlt": "Yes, overwrite the original file",
    "💾 Csere mentése": "💾 Save replacement",
    "⚠️ Előbb válassz ki egy MP3 fájlt!": "⚠️ Please choose an MP3 file first!",
    "⚠️ Jelöld be a megerősítést a felülíráshoz!": "⚠️ Please check the confirmation to overwrite!",
    "✅ Audio cserélve és GitHub-ra feltöltve.": "✅ Audio replaced and uploaded to GitHub.",
    "⚠️ Git szinkronizáció sikertelen: {error}": "⚠️ Git sync failed: {error}",
    "✅ Audio cserélve, de Git sync nem futott le.": "✅ Audio replaced, but Git sync did not run.",
    "❌ Audio csere hiba: {error}": "❌ Audio replacement error: {error}",
    "Hiba a keresési funkció betöltésekor: {error}": "Error loading search feature: {error}",
    "A keresési funkció nem érhető el. Ellenőrizd a search_functionality.py fájlt.": "Search feature is not available. Check the search_functionality.py file.",
    "### 👤 Játékos Kiválasztás": "### 👤 Player Selection",
    "Válassz játékost:": "Choose a player:",
    "Vendég": "Guest",
    "normál": "normal",
    "időzített": "timed",
    "túlélés": "survival",
    "gyakorlás": "practice",
    "kihívás": "challenge",
    "könnyű": "easy",
    "közepes": "medium",
    "nehéz": "hard",
    "🌍 Földrajz": "🌍 Geography",
    "🎼 Komolyzene": "🎼 Classical music",
    "🎵 Magyar könnyűzene": "🎵 Hungarian pop",
    "🌍 Nemzetközi zenekarok": "🌍 International bands",
    "⭐ One Hit Wonders": "⭐ One Hit Wonders",
    "📺 Sorozat főcímek": "📺 TV show themes",
    "🎨 Festmények": "🎨 Paintings",
    "🇭🇺 Magyar festmények": "🇭🇺 Hungarian paintings",
    "📚 Regények": "📚 Novels",
    "⚔️ Háborúk": "⚔️ Wars",
    "👑 Magyar királyok": "👑 Hungarian kings",
    "🔬 Tudósok, művészek, híres emberek": "🔬 Scientists, artists, famous people",
    "🏛️ Mitológia": "🏛️ Mythology",
    "🐾 Állatok": "🐾 Animals",
    "🎭 Drámák": "🎭 Dramas",
    "🏆 Sport logók": "🏆 Sports logos",
    "🏁 Zászlók": "🏁 Flags",
    "🔍 Zászlók részlete": "🔍 Flag details",
    "Melyik ország zászlajából származik a részlet?": "Which country's flag does this detail come from?",
    "Melyik szigetcsoport legészakibb tagja a Stromboli vulkán szigete?": "Which island group's northernmost member is Stromboli volcanic island?",
    "Lipari-szigetek": "Lipari Islands",
    "Egadi-szigetek": "Egadi Islands",
    "Kikládok": "Cyclades",
    "Dodekanészosz": "Dodecanese",
    "A Stromboli a Lipari-szigetek (Eolie-szigetek) legészakibb tagja, Szicília északi partjánál.": "Stromboli is the northernmost member of the Lipari Islands (Aeolian Islands), off the northern coast of Sicily.",
    "Ez {country} zászlójának egy részlete.": "This is a detail of {country}'s flag.",
    "Középkori vallási mozgalom tagjai, akik bűneik vezekléséül testüket naponta ostorozták – hogy hívják őket?": "Members of a medieval religious movement who flagellated themselves daily to atone for their sins – what are they called?",
    "Flagellánsok": "Flagellants",
    "Aszkéták": "Ascetics",
    "Koldulórendek": "Mendicant orders",
    "Pénitensek": "Penitents",
    "A flagellánsok középkori mozgalom tagjai voltak, akik önkéntes testi önfenyítéssel (ostorozással) kívánták bűneiket vezekelni. A szó a latin 'flagello' (ostoroz) szóból ered. A mozgalom a 14. századi pestisjárvány idején érte el legnagyobb felfutását.": "The flagellants were members of a medieval movement who sought to atone for their sins through voluntary self-flagellation. The word derives from the Latin 'flagello' (to whip). The movement reached its peak during the 14th-century plague.",
    "🤪 Idióta szavak": "🤪 Silly words",
    "⚽ Labdarúgó pályafutás": "⚽ Football career",
    "🎵 Magyar": "🎵 Hungarian",
    "🌍 Nemzetközi": "🌍 International",
    "### 🎲 Randomizáló Funkció": "### 🎲 Randomizer",
    "Randomizáláshoz használandó kérdésszám": "Question count for randomization",
    "Zenei randomizáláshoz használandó kérdésszám": "Question count for music randomization",
    "🎯 Teljes kvíz létrehozása": "🎯 Create full quiz",
    "✅ Teljes kvíz létrehozva! {topic_count} témakör kiválasztva, összesen {question_count} kérdés!": "✅ Full quiz created! {topic_count} topics selected, {question_count} questions total!",
    "🎵 Random zenei témakörök kiválasztása": "🎵 Select random music topics",
    "✅ {topic_count} zenei témakör kiválasztva + meglévő nem-zenei témakörök megtartva, {question_count} kérdés elosztva!": "✅ {topic_count} music topics selected + existing non-music topics kept, {question_count} questions distributed!",
    "🎲 Random témakörök kiválasztása (zene nélkül)": "🎲 Select random topics (no music)",
    "✅ {topic_count} témakör kiválasztva (zene nélkül) + meglévő zenei témakörök megtartva, {question_count} kérdés elosztva!": "✅ {topic_count} topics selected (no music) + existing music topics kept, {question_count} questions distributed!",
    "### 🎵 Zenei témakörök": "### 🎵 Music topics",
    "### 📚 Egyéb témakörök": "### 📚 Other topics",
    "{topic_name} kérdések száma": "{topic_name} question count",
    "### ⚙️ Kérdésszámok beállítása": "### ⚙️ Question count settings",
    "#### 🎵 Zenei kérdések beállításai": "#### 🎵 Music question settings",
    "Összes zenei kérdés száma": "Total music questions",
    "Automatikus elosztás a zenei témakörök között": "Auto-distribute among music topics",
    "##### Manuális elosztás:": "##### Manual distribution:",
    "#### 📚 Egyéb témakörök kérdésszámai": "#### 📚 Other topic question counts",
    "Összes egyéb kérdés száma": "Total other questions",
    "Automatikus elosztás az egyéb témakörök között": "Auto-distribute among other topics",
    "### 🎯 Végleges Kérdésszám Beállítása": "### 🎯 Final Question Count",
    "🎵 Zenei kérdések: {count}": "🎵 Music questions: {count}",
    "📚 Egyéb kérdések: {count}": "📚 Other questions: {count}",
    "📊 Összes elérhető: {count}": "📊 Total available: {count}",
    "🎯 Végleges kérdésszám: {count}": "🎯 Final question count: {count}",
    "🚀 Quiz indítása": "🚀 Start quiz",
    "Érvénytelen kérdés kihagyva: {question}": "Invalid question skipped: {question}",
    "Ismeretlen": "Unknown",
    "⬅️ Előző": "⬅️ Previous",
    "Következő ➡️": "Next ➡️",
    "Haladás: {current}/{total}": "Progress: {current}/{total}",
    "🎯 PONTSZÁM": "🎯 SCORE",
    "📝 KÉRDÉS": "📝 QUESTION",
    "Százalék": "Percentage",
    "Streak": "Streak",
    "Mód": "Mode",
    "Életek: {count}": "Lives: {count}",
    "⏱️ Hátralévő idő: {seconds} másodperc": "⏱️ Time remaining: {seconds} seconds",
    "Ismeretlen kérdés": "Unknown question",
    "Audio fájl lejátszási hiba: {error}": "Audio playback error: {error}",
    "Audio fájl nem található": "Audio file not found",
    "Logó fájl nem található: {path}": "Logo file not found: {path}",
    "❌ Kép bezárása": "❌ Close image",
    "💡 Tipp: A modal automatikusan bezáródik 30 másodperc múlva!": "💡 Tip: The modal closes automatically after 30 seconds!",
    "🔍 Kép nagyítása": "🔍 Zoom image",
    "Festmény kép nem található: {path}": "Painting image not found: {path}",
    "Hibás kérdés adatok: {error}. Kérdés: {question}": "Invalid question data: {error}. Question: {question}",
    "Hibás kérdés adatok - automatikus folytatás": "Invalid question data - auto continue",
    "### 💬 Írd be a válaszod:": "### 💬 Type your answer:",
    "Válasz:": "Answer:",
    "✅ Válasz beküldése": "✅ Submit answer",
    "Kérlek, írj be egy választ!": "Please enter an answer!",
    "Válaszlehetőség": "Answer option",
    "😊 Jó napom van!": "😊 I'm feeling lucky!",
    "🔄 Kvíz újraindítása": "🔄 Restart quiz",
    "N/A": "N/A",
    "Darab címe:": "Piece title:",
    "Válaszod:": "Your answer:",
    "Helyes válasz:": "Correct answer:",
    "Kérlek válassz ki legalább egy témaköröt!": "Please select at least one topic!",
    "Nem található érvényes kérdés a kiválasztott témakörökben!": "No valid questions found in the selected topics!",
    "{count} érvénytelen kérdés kihagyva (hiányzó adatok)": "{count} invalid questions skipped (missing data)",
    "Kiválasztott kérdések: {selected} / {limit}": "Selected questions: {selected} / {limit}",
    "Kiválasztott kérdések: {selected}": "Selected questions: {selected}",
    "{count} érvénytelen kérdés kihagyva": "{count} invalid questions skipped",
    "🏆 Quiz Eredmények": "🏆 Quiz Results",
    "Analytics rögzítés sikertelen: {error}": "Analytics recording failed: {error}",
    "📊 Alap Pontszám": "📊 Base Score",
    "⏱️ Idő": "⏱️ Time",
    "{minutes} perc {seconds} mp": "{minutes} min {seconds} sec",
    "🏆 Végső Pontszám": "🏆 Final Score",
    "Szorzó: {multiplier}x": "Multiplier: {multiplier}x",
    "🏅 Kiváló": "🏅 Excellent",
    "🥈 Jó": "🥈 Good",
    "🥉 Közepes": "🥉 Average",
    "📝 Megfelelő": "📝 Satisfactory",
    "❌ Elégtelen": "❌ Insufficient",
    "📈 Értékelés": "📈 Rating",
    "### 📋 Részletes Pontszámítás": "### 📋 Detailed Score Breakdown",
    "🔥 Maximális streak": "🔥 Max streak",
    "{count} kérdés": "{count} questions",
    "⏱️ Átlagos válaszidő": "⏱️ Average response time",
    "{seconds} másodperc": "{seconds} seconds",
    "🎮 Mód": "🎮 Mode",
    "🎯 Nehézség": "🎯 Difficulty",
    "### 👤 Játékos: {player}": "### 👤 Player: {player}",
    "### 👤 Játékos név megadása": "### 👤 Enter player name",
    "Add meg a neved:": "Enter your name:",
    "A játékos név megadása kötelező.": "Player name is required.",
    "Add meg a neved a quiz indításához.": "Enter your name to start the quiz.",
    "📊 Összes Quiz": "📊 Total Quizzes",
    "🎯 Átlagos Pontszám": "🎯 Average Score",
    "🏆 Legjobb Pontszám": "🏆 Best Score",
    "📝 Összes Kérdés": "📝 Total Questions",
    "### 📋 Kérdésenkénti eredmények": "### 📋 Question-by-question results",
    "Kérdés:": "Question:",
    "Válaszod:": "Your answer:",
    "Helyes válasz:": "Correct answer:",
    "Válaszidő:": "Answer time:",
    "Idő lejárt": "Time's up",
    "{status} Kérdés {index}": "{status} Question {index}",
    "🔄 Új quiz indítása": "🔄 Start new quiz",
    "## ⚙️ Beállítások": "## ⚙️ Settings",
    "### 🎯 Quiz Beállítások": "### 🎯 Quiz Settings",
    "#### Alapértelmezett beállítások": "#### Default settings",
    "Alapértelmezett zenei kérdések": "Default music questions",
    "Alapértelmezett egyéb kérdések": "Default other questions",
    "#### Időzítő beállítások": "#### Timer settings",
    "Alapértelmezett időkorlát (másodperc)": "Default time limit (seconds)",
    "Kihívás mód időkorlát (másodperc)": "Challenge mode time limit (seconds)",
    "### 🎵 Audio Beállítások": "### 🎵 Audio Settings",
    "Automatikus audio lejátszás": "Auto-play audio",
    "Audio fájlnév megjelenítése": "Show audio filename",
    "Alapértelmezett hangerő": "Default volume",
    "Audio minőség": "Audio quality",
    "Alacsony": "Low",
    "Közepes": "Medium",
    "Magas": "High",
    "### 📊 Analytics Beállítások": "### 📊 Analytics Settings",
    "Teljesítmény követése": "Track performance",
    "Részletes eredmények mentése": "Save detailed results",
    "Analytics adatok megőrzése (nap)": "Analytics data retention (days)",
    "Analytics exportálása": "Export analytics",
    "💾 Beállítások mentése": "💾 Save settings",
    "Beállítások mentve!": "Settings saved!",
    "## 🎵 Audio Hozzáadása": "## 🎵 Add Audio",
    "Válassz hozzáadási módszert:": "Choose an add method:",
    "🎵 A) YouTube Keresés": "🎵 A) YouTube Search",
    "🎵 B) Spotify Playlist": "🎵 B) Spotify Playlist",
    "📥 C) Tömeges YouTube linkek": "📥 C) Bulk YouTube links",
    "### 📥 Tömeges feltöltés yt-link alapján": "### 📥 Bulk upload via YouTube links",
    "Minden link ugyanabba a kategóriába kerül. 1 sor = 1 link.": "All links go into the same category. 1 line = 1 link.",
    "Kategória (kötelező):": "Category (required):",
    "— Válassz kategóriát —": "— Select a category —",
    "YouTube linkek": "YouTube links",
    "https://www.youtube.com/watch?v=...\nhttps://youtu.be/...": "https://www.youtube.com/watch?v=...\nhttps://youtu.be/...",
    "Cookies.txt (opcionális, 403 tiltás ellen)": "Cookies.txt (optional, against 403 blocks)",
    "Netscape formátumú cookie fájl. Bejelentkezett böngészőből exportálható.": "Netscape-format cookie file. Can be exported from a logged-in browser.",
    "🚀 Tömeges integrálás": "🚀 Bulk integrate",
    "⚠️ Válassz kötelező kategóriát!": "⚠️ Please select a required category!",
    "⚠️ Adj meg legalább egy érvényes YouTube linket!": "⚠️ Provide at least one valid YouTube link!",
    "🔄 Feldolgozás: {current}/{total}": "🔄 Processing: {current}/{total}",
    "✅ Tömeges integráció kész, GitHub szinkronizálva.": "✅ Bulk integration done, GitHub synced.",
    "✅ Tömeges integráció kész, cache frissítve.": "✅ Bulk integration done, cache refreshed.",
    "⚠️ Sikertelen linkek: {count}": "⚠️ Failed links: {count}",
    "✅ Feldolgozva: {count} link": "✅ Processed: {count} links",
    "🎵 Track újra lejátszása": "🎵 Replay track",
    "Nincs elérhető audio ehhez a kérdéshez.": "No audio available for this question.",
    "### 📋 Módok": "### 📋 Modes",
    "**Jellemzők:**": "**Features:**",
    "Hagyományos quiz mód": "Traditional quiz mode",
    "Nincs időkorlát": "No time limit",
    "Nincs életrendszer": "No life system",
    "Részletes eredmények": "Detailed results",
    "Időkorlátozott quiz": "Timed quiz",
    "30 másodperc/kérdés": "30 seconds/question",
    "Gyors válaszok": "Quick answers",
    "Idő nyomás": "Time pressure",
    "Túlélési mód": "Survival mode",
    "3 élet": "3 lives",
    "Hibák után élet elvesztése": "Lose a life after mistakes",
    "Hosszú sorozatok": "Long streaks",
    "Gyakorló mód": "Practice mode",
    "Azonnali visszajelzés": "Instant feedback",
    "Magyarázatok": "Explanations",
    "Nincs pontszám": "No score",
    "Kihívás mód": "Challenge mode",
    "1 élet": "1 life",
    "20 másodperc/kérdés": "20 seconds/question",
    "Legmagasabb pontszámok": "Highest scores",
    "### 🎯 Nehézségi Szint": "### 🎯 Difficulty Level",
    "Könnyű - feleletválasztós + megoldás": "Easy - multiple choice + solution",
    "Feleletválasztós kérdések": "Multiple choice questions",
    "Megoldás megjelenítése": "Show solution",
    "Segítség a jobb alsó sarokban": "Help in the bottom right corner",
    "Közepes - feleletválasztós": "Medium - multiple choice",
    "Nincs megoldás": "No solution",
    "Hagyományos quiz": "Traditional quiz",
    "Nehéz - szabad szöveges bevitel": "Hard - free text input",
    "Szöveges bevitel": "Text input",
    "Pontos válasz szükséges": "Exact answer required",
    "Legnehezebb mód": "Hardest mode",
    "Pontszám szorzó:": "Score multiplier:",
    "Nehézség": "Difficulty",
    "Életek": "Lives",
    "⏱️ Hátralévő idő: {minutes:02d}:{seconds:02d}": "⏱️ Time remaining: {minutes:02d}:{seconds:02d}",
    "## 📊 Quiz Analytics Dashboard": "## 📊 Quiz Analytics Dashboard",
    "### 📅 Időszakos Szűrés": "### 📅 Time Period Filter",
    "Időszak:": "Period:",
    "Összes időszak": "All time",
    "Utolsó 7 nap": "Last 7 days",
    "Utolsó 30 nap": "Last 30 days",
    "Utolsó 3 hónap": "Last 3 months",
    "Egyéni": "Custom",
    "Kezdő dátum:": "Start date:",
    "Befejező dátum:": "End date:",
    "Szűrés játékos szerint:": "Filter by player:",
    "Összes játékos": "All players",
    "Összes Quiz": "Total quizzes",
    "Összes Kérdés": "Total questions",
    "Átlagos Pontszám": "Average score",
    "Trend": "Trend",
    "### 🏆 Legjobb Témakörök": "### 🏆 Best Topics",
    "**Legjobb**:": "**Best**:",
    "**Legrosszabb**:": "**Worst**:",
    "- Átlag:": "- Average:",
    "- Quizek:": "- Quizzes:",
    "### 👥 Játékos Teljesítmény": "### 👥 Player Performance",
    "#### 📊 Részletes statisztikák: {player}": "#### 📊 Detailed stats: {player}",
    "#### 📈 Quiz Előzmények": "#### 📈 Quiz History",
    "### 📈 Témakör Teljesítmény": "### 📈 Topic Performance",
    "### 🎯 Játékos Témakör Teljesítmény": "### 🎯 Player Topic Performance",
    "### 📅 Heti Progress": "### 📅 Weekly Progress",
    "### 🏆 Játékosok Összehasonlítása": "### 🏆 Player Comparison",
    "#### ⚔️ {player1} vs {player2}": "#### ⚔️ {player1} vs {player2}",
    "#### 📊 Összehasonlítás Grafikon": "#### 📊 Comparison Chart",
    "#### 🏅 Top 3 Játékos": "#### 🏅 Top 3 Players",
    "#### 📊 Játékosok Teljesítmény Grafikon": "#### 📊 Player Performance Chart",
    "### 🔄 GitHub Szinkronizáció": "### 🔄 GitHub Sync",
    "GitHub állapot ellenőrzése...": "Checking GitHub status...",
    "⚠️ **Lokális változások vannak:**": "⚠️ **Local changes detected:**",
    "💾 Lokális változások mentése": "💾 Save local changes",
    "✅ Lokális változások mentve!": "✅ Local changes saved!",
    "🗑️ Lokális változások eldobása": "🗑️ Discard local changes",
    "✅ Lokális változások eldobva!": "✅ Local changes discarded!",
    "📥 **Új változások érkeztek a GitHub-ról:**": "📥 **New changes available from GitHub:**",
    "📥 Változások letöltése": "📥 Download changes",
    "✅ Változások letöltve!": "✅ Changes downloaded!",
    "⏭️ Kihagyás": "⏭️ Skip",
    "ℹ️ Változások kihagyva. Folytathatod a munkát.": "ℹ️ Changes skipped. You can continue working.",
    "✅ **Minden szinkronizálva!** Nincs új változás.": "✅ **Everything synced!** No new changes.",
    "🔄 Frissítés ellenőrzése": "🔄 Check for updates",
    "✅ Cache törölve! Az oldal újratöltődik...": "✅ Cache cleared! The page will reload...",
    "### 📁 Kategória választás": "### 📁 Category selection",
    "### 🔄 Komolyzene Git sync": "### 🔄 Classical music Git sync",
    "Teljes szinkron: git pull + komolyzene fájlok commit/push.": "Full sync: git pull + classical music files commit/push.",
    "🔄 Teljes komolyzene Git sync": "🔄 Full classical music Git sync",
    "🔄 Kérdésfájl változott, cache frissítése...": "🔄 Question file changed, refreshing cache...",
    "🔄 Kényszerített frissítés...": "🔄 Forced refresh...",
    "🔄 Új adatok betöltése...": "🔄 Loading new data...",
    "❌ Nincs kérdésfájl!": "❌ No question file!",
    "### ✏️ Szerkesztés": "### ✏️ Edit",
    "**Válassz egy sort a szerkesztéshez:**": "**Select a row to edit:**",
    "⚠️ A kérdéslista megváltozott. Cache frissítés szükséges.": "⚠️ The question list changed. Cache refresh required.",
    "⚠️ Hibás kérdésindex. Kérlek frissítsd a cache-t.": "⚠️ Invalid question index. Please refresh the cache.",
    "**Válaszopciók:**": "**Answer options:**",
    "💾 Mentés": "💾 Save",
    "✅ Kérdés sikeresen mentve!": "✅ Question saved successfully!",
    "✅ Változások GitHub-ra feltöltve!": "✅ Changes uploaded to GitHub!",
    "🔄 Oldal frissítése...": "🔄 Refreshing page...",
    "❌ Hiba a fájl mentésekor!": "❌ Error saving file!",
    "### 🗑️ Törlés": "### 🗑️ Delete",
    "⚠️ Ez a művelet visszavonhatatlan: a kérdés és az audio fájl is törlődik.": "⚠️ This action is irreversible: the question and audio file will be deleted.",
    "🗑️ Track + kérdés törlése és GitHub sync": "🗑️ Delete track + question and GitHub sync",
    "⚠️ A törléshez jelöld be a megerősítést.": "⚠️ Check the confirmation to delete.",
    "❌ Nincs kérdésfájl, törlés nem lehetséges.": "❌ No question file, delete not possible.",
    "⚠️ Audio fájl nem található, csak a kérdés törölve.": "⚠️ Audio file not found, only the question was deleted.",
    "✅ Törlés GitHub-ra szinkronizálva!": "✅ Deletion synced to GitHub!",
    "**Válassz a fenti opciók közül a szerkesztéshez.**": "**Choose one of the above options to edit.**",
    "### 💾 Összes változás mentése": "### 💾 Save all changes",
    "🚀 Összes változás mentése és Git Push": "🚀 Save all changes and Git Push",
    "✅ Kérdések sikeresen mentve!": "✅ Questions saved successfully!",
    "✅ Összes változás GitHub-ra feltöltve!": "✅ All changes uploaded to GitHub!",
    "🔄 GitHub Szinkronizálás Indítása": "🔄 Start GitHub Sync",
    "### 📊 Jelenlegi állapot": "### 📊 Current status",
    "🎵 Audiofájlok": "🎵 Audio files",
    "📝 Kérdés fájlok": "📝 Question files",
    "### 📊 Kategóriánkénti eloszlás": "### 📊 Distribution by category",
    "### 📅 Utolsó szinkronizálás": "### 📅 Last sync",
    "Az utolsó szinkronizálás időpontja: **Még nem történt szinkronizálás**": "Last sync time: **No sync yet**",
    "🔄 Frissítés": "🔄 Refresh",
    "🎵 Spotify Playlist Feldolgozás": "🎵 Spotify Playlist Processing",
    "🔐 Spotify OAuth Beállítás (Nyilvános playlistekhez)": "🔐 Spotify OAuth Settings (for public playlists)",
    "**A nyilvános Spotify playlistek eléréséhez OAuth autentikáció szükséges.**": "**OAuth authentication is required to access public Spotify playlists.**",
    "🔗 OAuth URL Generálása": "🔗 Generate OAuth URL",
    "1. Kattints a linkre és engedélyezd a hozzáférést": "1. Click the link and authorize access",
    "2. Másold ki az authorization code-ot az URL-ből": "2. Copy the authorization code from the URL",
    "3. Illeszd be az authorization code-ot alább": "3. Paste the authorization code below",
    "🔑 OAuth Token Beállítása": "🔑 Set OAuth Token",
    "OAuth token beállítása...": "Setting OAuth token...",
    "✅ OAuth token sikeresen beállítva!": "✅ OAuth token set successfully!",
    "Most már elérheted a nyilvános Spotify playlisteket!": "You can now access public Spotify playlists!",
    "❌ OAuth token beállítása sikertelen!": "❌ Failed to set OAuth token!",
    "⚠️ Kérlek add meg az authorization code-ot!": "⚠️ Please provide the authorization code!",
    "⚠️ OAuth token lejárt, újra kell autentikálni!": "⚠️ OAuth token expired, please re-authenticate!",
    "ℹ️ Nincs aktív OAuth token": "ℹ️ No active OAuth token",
    "📥 Playlist Betöltése": "📥 Load playlist",
    "Playlist betöltése...": "Loading playlist...",
    "❌ Nem sikerült betölteni a playlist-et": "❌ Failed to load the playlist",
    "⚠️ Kérlek add meg a playlist URL-jét!": "⚠️ Please provide the playlist URL!",
    "✅ YouTube találat!": "✅ YouTube match!",
    "ℹ️ YouTube keresés folyamatban...": "ℹ️ YouTube search in progress...",
    "❌ MP3 letöltés sikertelen": "❌ MP3 download failed",
    "ℹ️ YouTube keresés szükséges a letöltéshez": "ℹ️ YouTube search required for download",
    "📊 Részletes Táblázat": "📊 Detailed Table",
    "❌ Spotify playlist funkció nem elérhető": "❌ Spotify playlist feature not available",
    "A spotify_playlist_integration.py fájl szükséges": "The spotify_playlist_integration.py file is required",
    "### 🎵 Spotify Playlist Feldolgozás": "### 🎵 Spotify Playlist Processing",
    "### 📋 Playlist Feldolgozás": "### 📋 Playlist Processing",
    "🎵 Playlist Feldolgozása": "🎵 Process Playlist",
    "❌ Nincs aktív OAuth token!": "❌ No active OAuth token!",
    "🔐 Kérlek állítsd be az OAuth tokent a fenti expanderben!": "🔐 Please set the OAuth token in the expander above!",
    "❌ Az OAuth token lejárt!": "❌ OAuth token expired!",
    "🔄 Kérlek generálj új tokent!": "🔄 Please generate a new token!",
    "Playlist feldolgozása...": "Processing playlist...",
    "⚠️ Nincsenek trackek a playlistben!": "⚠️ No tracks in the playlist!",
    "🔍 Lehetséges okok:": "🔍 Possible reasons:",
    "• Privát playlist": "• Private playlist",
    "• Érvénytelen playlist URL": "• Invalid playlist URL",
    "• Spotify API hiba": "• Spotify API error",
    "🔐 Ellenőrizd az OAuth tokent vagy próbálj másik playlistet!": "🔐 Check the OAuth token or try another playlist!",
    "### 📊 Debug Információk": "### 📊 Debug Information",
    "🧪 API Teszt": "🧪 API Test",
    "❌ OAuth Token lejárt!": "❌ OAuth Token expired!",
    "⚠️ Nincs OAuth token": "⚠️ No OAuth token",
    "### 🔍 Session State": "### 🔍 Session State",
    "✅ Token mentve session state-ben": "✅ Token saved in session state",
    "⚠️ Token nincs mentve session state-ben": "⚠️ Token not saved in session state",
    "Összes track": "Total tracks",
    "🎬 YouTube": "🎬 YouTube",
    "Találati arány": "Match rate",
    "### 🎵 Playlist Elemek": "### 🎵 Playlist Items",
    "### 📁 Helyi Audio Fájlok": "### 📁 Local Audio Files",
    "📝 Metaadatok szerkesztése": "📝 Edit metadata",
    "Cím": "Title",
    "Előadó": "Artist",
    "Album": "Album",
    "Év": "Year",
    "💾 Metaadatok mentése": "💾 Save metadata",
    "✅ Metaadatok mentve!": "✅ Metadata saved!",
    "### 🔗 YouTube Linkek Feldolgozása": "### 🔗 YouTube Link Processing",
    "🔍 Metaadatok lekérése": "🔍 Fetch metadata",
    "🔍 Metaadatok lekérése...": "🔍 Fetching metadata...",
    "✅ Metaadatok lekérve!": "✅ Metadata fetched!",
    "⬇️ Audio letöltés": "⬇️ Download audio",
    "⬇️ Audio letöltés...": "⬇️ Downloading audio...",
    "✅ Audio letöltve!": "✅ Audio downloaded!",
    "📋 Példa metaadatok": "📋 Example metadata",
    "### 🎵 YouTube Keresés": "### 🎵 YouTube Search",
    "#### 🔍 YouTube Keresés": "#### 🔍 YouTube Search",
    "🔍 Keresés indítása": "🔍 Start search",
    "YouTube keresés folyamatban...": "YouTube search in progress...",
    "❌ Nem találtam megfelelő találatokat": "❌ No suitable results found",
    "⚠️ Kérlek add meg a keresési kifejezést!": "⚠️ Please enter a search query!",
    "#### 📋 Keresési eredmények": "#### 📋 Search results",
    "📷 Nincs kép": "📷 No image",
    "**Válasz opciók:**": "**Answer options:**",
    "1. helyes válasz:": "1. correct answer:",
    "2. opció:": "2. option:",
    "3. opció:": "3. option:",
    "4. opció:": "4. option:",
    "🔄 Integráció indult...": "🔄 Integration started...",
    "✅ Letöltés kész. A mentés előtt még szerkesztheted a kérdést lent.": "✅ Download complete. You can edit the question below before saving.",
    "✅ Letöltés és integrálás befejezve.": "✅ Download and integration complete.",
    "❌ Integráció nem adott vissza eredményt.": "❌ Integration returned no result.",
    "### ✏️ Mentés előtti szerkesztés": "### ✏️ Edit before saving",
    "Kérdés szövege:": "Question text:",
    "Magyarázat:": "Explanation:",
    "### 🌐 IP használat": "### 🌐 IP usage",
    "IP cím": "IP address",
    "Játékos": "Player",
    "Használatok": "Sessions",
    "Utoljára": "Last seen",
    "Nincs IP adat.": "No IP data.",
    "Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:": "Listen to this piece and choose its composer:",
    "Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét!": "Listen to this piece and choose its composer!",
    "Ki a zeneszerző?": "Who is the composer?",
    "Csajkovszkij": "Tchaikovsky",
    "Hacsaturján": "Khachaturian",
    "Prokofjev": "Prokofiev",
    "Erkel Ferenc": "Ferenc Erkel",
    "Weiner Leó": "Leó Weiner",
    "Dohnány Ernő": "Ernő Dohnányi",
    "Bartók Béla": "Béla Bartók",
}

TRANSLATIONS = {
    "hu": {key: key for key in _EN_TRANSLATIONS},
    "en": _EN_TRANSLATIONS,
}

_TRANSLATION_INITIALIZED = False
_AUTO_TRANSLATIONS_LOADED = False
_AUTO_TRANSLATIONS: dict[str, str] = {}
_AUTO_TRANSLATIONS_PATH = Path(__file__).with_name("i18n_auto_translations.json")
_HUNGARIAN_CHARS = re.compile(r"[áéíóöőúüűÁÉÍÓÖŐÚÜŰ]")
_HUNGARIAN_HINTS = {
    "mi ", "melyik", "milyen", "ki ", "hol ", "mikor ", "mely ", "mennyi", "hány",
    "melyik ország", "főváros", "zászló", "festmény", "kérdés", "válasz", "igaz",
    "hamis", "mely", "kinek", "hogy", "hogyan", "mit", "melyik", "mely",
}


def get_language() -> str:
    lang = st.session_state.get("language")
    if lang not in LANG_OPTIONS:
        lang = "hu"
        st.session_state["language"] = lang
    return lang


def set_language(lang: str) -> None:
    if lang in LANG_OPTIONS:
        st.session_state["language"] = lang
    else:
        st.session_state["language"] = "hu"


def t(text: str, **kwargs) -> str:
    lang = get_language()
    template = TRANSLATIONS.get(lang, {}).get(text, text)
    if kwargs:
        try:
            return template.format(**kwargs)
        except (KeyError, ValueError):
            return template
    return template


def translate_text(text: str) -> str:
    if not isinstance(text, str):
        return text
    if get_language() == "hu":
        return text
    translated = TRANSLATIONS["en"].get(text)
    if translated:
        return translated
    # Partial replacements for dynamic strings
    translated = text
    for key in sorted(TRANSLATIONS["en"], key=len, reverse=True):
        if key in translated:
            translated = translated.replace(key, TRANSLATIONS["en"][key])
    if translated != text:
        return translated
    return _auto_translate_text(text)


def _load_auto_translations() -> None:
    global _AUTO_TRANSLATIONS_LOADED
    if _AUTO_TRANSLATIONS_LOADED:
        return
    _AUTO_TRANSLATIONS_LOADED = True
    if _AUTO_TRANSLATIONS_PATH.exists():
        try:
            with _AUTO_TRANSLATIONS_PATH.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                _AUTO_TRANSLATIONS.update(
                    {str(k): str(v) for k, v in data.items() if isinstance(k, str) and isinstance(v, str)}
                )
        except Exception:
            pass


def _save_auto_translations() -> None:
    try:
        with _AUTO_TRANSLATIONS_PATH.open("w", encoding="utf-8") as handle:
            json.dump(_AUTO_TRANSLATIONS, handle, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _should_auto_translate(text: str) -> bool:
    if not text or len(text.strip()) < 2:
        return False
    stripped = text.strip()
    if stripped.startswith("http://") or stripped.startswith("https://"):
        return False
    if "<" in text and ">" in text:
        return False
    if "```" in text:
        return False
    if _HUNGARIAN_CHARS.search(text):
        return True
    lowered = text.lower()
    return any(hint in lowered for hint in _HUNGARIAN_HINTS)


def _google_translate_hu_to_en(text: str) -> Optional[str]:
    try:
        response = requests.get(
            "https://translate.googleapis.com/translate_a/single",
            params={
                "client": "gtx",
                "sl": "hu",
                "tl": "en",
                "dt": "t",
                "q": text,
            },
            timeout=10,
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if not data or not isinstance(data, list) or not data[0]:
            return None
        parts = [segment[0] for segment in data[0] if segment and isinstance(segment, list)]
        translated = "".join(parts).strip()
        return translated or None
    except Exception:
        return None


def _auto_translate_text(text: str) -> str:
    if get_language() != "en":
        return text
    _load_auto_translations()
    cached = _AUTO_TRANSLATIONS.get(text)
    if cached:
        return cached
    if not _should_auto_translate(text):
        return text
    translated = _google_translate_hu_to_en(text)
    if translated:
        _AUTO_TRANSLATIONS[text] = translated
        _save_auto_translations()
        return translated
    return text


def init_i18n() -> None:
    global _TRANSLATION_INITIALIZED
    if _TRANSLATION_INITIALIZED:
        return
    _TRANSLATION_INITIALIZED = True

    def wrap_text_fn(fn, text_arg_index=0, text_kw_keys=None):
        text_kw_keys = text_kw_keys or []

        def wrapper(*args, **kwargs):
            args = list(args)
            if len(args) > text_arg_index and isinstance(args[text_arg_index], str):
                args[text_arg_index] = translate_text(args[text_arg_index])
            for key in text_kw_keys:
                if key in kwargs and isinstance(kwargs[key], str):
                    kwargs[key] = translate_text(kwargs[key])
            return fn(*args, **kwargs)

        return wrapper

    def wrap_tabs(fn):
        def wrapper(tabs, *args, **kwargs):
            if isinstance(tabs, (list, tuple)):
                tabs = [translate_text(item) if isinstance(item, str) else item for item in tabs]
            return fn(tabs, *args, **kwargs)

        return wrapper

    st.title = wrap_text_fn(st.title)
    st.header = wrap_text_fn(st.header)
    st.subheader = wrap_text_fn(st.subheader)
    st.caption = wrap_text_fn(st.caption)
    st.markdown = wrap_text_fn(st.markdown)
    st.write = wrap_text_fn(st.write)
    st.info = wrap_text_fn(st.info)
    st.warning = wrap_text_fn(st.warning)
    st.error = wrap_text_fn(st.error)
    st.success = wrap_text_fn(st.success)
    st.code = wrap_text_fn(st.code)
    st.button = wrap_text_fn(st.button, text_kw_keys=["help"])
    st.checkbox = wrap_text_fn(st.checkbox, text_kw_keys=["help"])
    st.radio = wrap_text_fn(st.radio, text_kw_keys=["help"])
    st.selectbox = wrap_text_fn(st.selectbox, text_kw_keys=["help"])
    st.slider = wrap_text_fn(st.slider, text_kw_keys=["help"])
    st.text_input = wrap_text_fn(st.text_input, text_kw_keys=["placeholder", "help"])
    st.text_area = wrap_text_fn(st.text_area, text_kw_keys=["placeholder", "help"])
    st.file_uploader = wrap_text_fn(st.file_uploader, text_kw_keys=["help"])
    st.expander = wrap_text_fn(st.expander)
    st.metric = wrap_text_fn(st.metric, text_kw_keys=["label"])
    st.progress = wrap_text_fn(st.progress, text_kw_keys=["text"])
    st.spinner = wrap_text_fn(st.spinner)
    st.tabs = wrap_tabs(st.tabs)


def render_language_selector(label: Optional[str] = None) -> str:
    label_text = label or t("Nyelv")
    current = get_language()
    options = list(LANG_OPTIONS.keys())
    index = options.index(current) if current in options else 0
    selected = st.selectbox(
        label_text,
        options=options,
        index=index,
        format_func=lambda key: LANG_OPTIONS[key],
    )
    if selected != current:
        st.session_state["language"] = selected
        st.rerun()
    return selected
