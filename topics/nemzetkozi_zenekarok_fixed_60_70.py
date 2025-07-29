#!/usr/bin/env python3
"""
Fixed international questions with corrected answer indices for questions 60-70
"""

NEMZETKOZI_ZENEKAROK_QUESTIONS = [
    # ... existing questions 0-59 remain the same ...
    # Questions 60-70 are fixed with correct answer indices
    
    # Question 60: Keane (already correct)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/4NgfOZCL9Ml67xzM0xzIvC",
        "options": ['Janis Joplin', 'Anne-Marie', 'Bebe Rexha', 'Taylor Swift'],
        "correct": 3,
        "explanation": "Taylor Swift - Amerikai énekesnő, 1989-ben született",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 61: Justin Bieber (already correct)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/track/0V3wPSX9ygBnCm8psDIegu",
        "options": ['Justin Bieber', 'Lukas Graham', 'James Bay', 'Pharrel Williams'],
        "correct": 0,
        "explanation": "Justin Bieber - Kanadai énekes, 1994-ben született",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 62: Lukas Graham (already correct)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/25u4wHJWxCA9vO0CzxAbK7",
        "options": ['Lukas Graham', 'James Bay', 'Pharrel Williams', 'Jason Mraz'],
        "correct": 0,
        "explanation": "Lukas Graham - Dán zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 63: Maroon 5 (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/04gDigrS5kc9YWfZHwBETP",
        "options": ['Maroon 5', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Maroon 5 - Amerikai pop rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 64: Maneskin (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/0UjXKCLdx7UUETj8JGrD26",
        "options": ['Maneskin', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Maneskin - Olasz rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 65: My Chemical Romance (already fixed)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/7FBcuc1gsnv6Y1nwFtNRCb",
        "options": ['My Chemical Romance', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "My Chemical Romance - Amerikai rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 66: Kings of Leon (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/2qk9voo8llSGYcZ6xrBzKx",
        "options": ['Kings of Leon', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Kings of Leon - Amerikai rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 67: The Chainsmokers (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/track/0V3wPSX9ygBnCm8psDIegu",
        "options": ['The Chainsmokers', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "The Chainsmokers - Amerikai DJ duó",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 68: Muse (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/12Chz98pHFMPJEknJQMWvI",
        "options": ['Muse', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Muse - Brit rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 69: Milky Chance (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/track/0V3wPSX9ygBnCm8psDIegu",
        "options": ['Milky Chance', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Milky Chance - Német indie folk zenekar",
        "topic": "nemzetkozi_zenekarok"
    },
    # Question 70: Train (FIXED: was 3, now 0)
    {
        "question": "Ki az előadó?",
        "spotify_embed": "https://open.spotify.com/embed/artist/3FUY2gzHeIiaesXtOAdB7A",
        "options": ['Train', 'Imagine Dragons', 'One Direction', 'One Republic'],
        "correct": 0,
        "explanation": "Train - Amerikai pop rock zenekar",
        "topic": "nemzetkozi_zenekarok"
    }
]

print(f"Nemzetközi zenekarok kérdések száma: {len(NEMZETKOZI_ZENEKAROK_QUESTIONS)}") 