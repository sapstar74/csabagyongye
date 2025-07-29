#!/usr/bin/env python3
"""
Script az original_index mező hozzáadásához a magyar zenekarok kérdésekhez
"""

def add_original_index_to_magyar_questions():
    """Hozzáadja az original_index mezőt minden magyar zenekarok kérdéshez"""
    
    # Magyar zenekarok kérdések az original_index mezőkkel
    MAGYAR_ZENEKAROK_QUESTIONS_WITH_INDEX = [
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/1UIPahyz7pEKaU6RQvU3FC",
            "original_index": 0,
            "options": ['Follow the flow', 'Elefánt', '4Street', 'Bagossy Brothers'],
            "correct": 0,
            "explanation": "Follow the flow magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/5XXDBFhkTp168rjq9IjAE3",
            "original_index": 1,
            "options": ['Elefánt', 'Follow the flow', '4Street', 'Bagossy Brothers'],
            "correct": 0,
            "explanation": "Elefánt magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/3W75Q3HN7adHVSjjRJX1ap",
            "original_index": 2,
            "options": ['4Street', 'Follow the flow', 'Elefánt', 'Bagossy Brothers'],
            "correct": 0,
            "explanation": "4Street magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/1vpC76RZf9ndFkOEB7agn9",
            "original_index": 3,
            "options": ['Bagossy Brothers', 'Follow the flow', 'Elefánt', '4Street'],
            "correct": 0,
            "explanation": "Bagossy Brothers magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/1SN71xW3yOVbPgsGFBMXTZ",
            "original_index": 4,
            "options": ['Csaknekedkislány', 'Lóci játszik', 'Galaxisok', 'Parno Graszt'],
            "correct": 0,
            "explanation": "Csaknekedkislány magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/1M7KsIoOlY1CK4h0bFkjIf",
            "original_index": 5,
            "options": ['Lóci játszik', 'Csaknekedkislány', 'Galaxisok', 'Parno Graszt'],
            "correct": 0,
            "explanation": "Lóci játszik magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/0oTbG6PYGGhT0vRYqByYEL",
            "original_index": 6,
            "options": ['Galaxisok', 'Csaknekedkislány', 'Lóci játszik', 'Parno Graszt'],
            "correct": 0,
            "explanation": "Galaxisok magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/5hBCfYFEDK8otrksMYuzoL",
            "original_index": 7,
            "options": ['Parno Graszt', 'Palya Bea', 'Bohemian Betyars', 'Aurevoir'],
            "correct": 0,
            "explanation": "Parno Graszt magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/7KRmqRSdAGjiSDns2qsdQ8",
            "original_index": 8,
            "options": ['Palya Bea', 'Parno Graszt', 'Bohemian Betyars', 'Aurevoir'],
            "correct": 0,
            "explanation": "Palya Bea magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/2ezYPSKWBfnFTobN9puCow",
            "original_index": 9,
            "options": ['Bohemian Betyars', 'Parno Graszt', 'Palya Bea', 'Aurevoir'],
            "correct": 0,
            "explanation": "Bohemian Betyars magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/51BZWZTWqI7GjrgHw3Wvuw",
            "original_index": 10,
            "options": ['Aurevoir', 'Parno Graszt', 'Palya Bea', 'Bohemian Betyars'],
            "correct": 0,
            "explanation": "Aurevoir magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/4imSxhDqtkiuKUamV1AL2l",
            "original_index": 11,
            "options": ['Dánielffy', 'Aurevoir', 'Ham Ko Ham', 'Carbonfools'],
            "correct": 0,
            "explanation": "Dánielffy magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/4BcSup56aUUtG55MkrsHDx",
            "original_index": 12,
            "options": ['Ham Ko Ham', 'Dánielffy', 'Aurevoir', 'Carbonfools'],
            "correct": 0,
            "explanation": "Ham Ko Ham magyar roma/népzene zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/4hQQE3GUQeBAOFwTJ5aede",
            "original_index": 13,
            "options": ['Carbonfools', 'Zagar', 'Neo', 'Soulwave'],
            "correct": 0,
            "explanation": "Carbonfools magyar elektronikus zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/3zhmiYvMt6ScobjEnbVB4I",
            "original_index": 14,
            "options": ['Zagar', 'Carbonfools', 'Neo', 'Soulwave'],
            "correct": 0,
            "explanation": "Zagar magyar elektronikus zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/54N9jnigs5yhiMGY7rVu1K",
            "original_index": 15,
            "options": ['Neo', 'Carbonfools', 'Zagar', 'Soulwave'],
            "correct": 0,
            "explanation": "Neo magyar elektronikus zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/6K7CJm6E0mB6TpJPiR46oZ",
            "original_index": 16,
            "options": ['Soulwave', 'Carbonfools', 'Zagar', 'Neo'],
            "correct": 0,
            "explanation": "Soulwave magyar elektronikus zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/0VJ7t5tdQqXfw5CSLBRngi",
            "original_index": 17,
            "options": ['Quimby', 'Tankcsapda', 'P. Mobil', 'Republic'],
            "correct": 0,
            "explanation": "Quimby magyar alternatív zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/2jB5Vy4QBIB71DoEIGqEn5",
            "original_index": 18,
            "options": ['Tankcsapda', 'Quimby', 'P. Mobil', 'Republic'],
            "correct": 0,
            "explanation": "Tankcsapda magyar rock zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/2KZ3SgUuMLSxlRiz7MllMu",
            "original_index": 19,
            "options": ['P. Mobil', 'Quimby', 'Tankcsapda', 'Republic'],
            "correct": 0,
            "explanation": "P. Mobil magyar rock zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/0VJ7t5tdQqXfw5CSLBRngi",
            "original_index": 20,
            "options": ['Republic', 'Quimby', 'Tankcsapda', 'P. Mobil'],
            "correct": 0,
            "explanation": "Republic magyar rock zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/2jB5Vy4QBIB71DoEIGqEn5",
            "original_index": 21,
            "options": ['Bonanza Banzai', 'Quimby', 'Tankcsapda', 'P. Mobil'],
            "correct": 0,
            "explanation": "Bonanza Banzai magyar rock zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/0VJ7t5tdQqXfw5CSLBRngi",
            "original_index": 22,
            "options": ['Korai Öröm', 'Quimby', 'Tankcsapda', 'P. Mobil'],
            "correct": 0,
            "explanation": "Korai Öröm magyar rock zenekar",
            "topic": "magyar_zenekarok"
        },
        {
            "question": "Ki az előadó?",
            "spotify_embed": "https://open.spotify.com/embed/artist/0VJ7t5tdQqXfw5CSLBRngi",
            "original_index": 23,
            "options": ['Beatrice', 'Óriás', 'HS7', 'Hiperkarma'],
            "correct": 0,
            "explanation": "Nagy Feró a Beatrice frontembere",
            "topic": "magyar_zenekarok"
        },
    ]
    
    return MAGYAR_ZENEKAROK_QUESTIONS_WITH_INDEX

if __name__ == "__main__":
    questions = add_original_index_to_magyar_questions()
    print(f"Magyar zenekarok kérdések száma: {len(questions)}")
    
    # Ellenőrizzük a Lóci játszik kérdést
    for i, question in enumerate(questions):
        if "Lóci játszik" in question.get("explanation", ""):
            print(f"Lóci játszik kérdés: index {i}, original_index: {question.get('original_index')}")
            break 