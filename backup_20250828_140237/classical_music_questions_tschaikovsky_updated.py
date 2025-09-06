#!/usr/bin/env python3
"""
Komolyzenei kérdések javított Spotify linkekkel
"""

CLASSICAL_MUSIC_QUESTIONS = [
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: IX. Új világ szimfónia',
        'spotify_embed': 'https://open.spotify.com/embed/track/6nqHzwOdGIaX57U6VU6kMO?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&hide_artist=1&hide_title=1',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Symphony No. 9 in E Minor, Op. 95, B. 178 "From the New World": IV. Allegro con fuoco',
        'spotify_found_artist': 'Antonín Dvořák'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: Humoresque',
        'spotify_embed': 'https://open.spotify.com/embed/track/5DNbuAAp64m3ULNsqTDTNF?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Humoresques, Op. 101: VII. Poco lento e grazioso - Remastered',
        'spotify_found_artist': 'Antonín Dvořák'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Dvorak', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Dvorak: 8. G-dúr szimfónia',
        'spotify_embed': 'https://open.spotify.com/embed/track/37RD6Is9M6zS5GeSOBAA27?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Symphony No. 8 in G Major, Op. 88, B. 163 (Arr. P. Breiner for Piano): III. Allegretto grazioso',
        'spotify_found_artist': 'Antonín Dvořák'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: V. Szimfónia - A sors szimfónia',
        'spotify_embed': 'https://open.spotify.com/embed/track/6CgJ9AhT2daf6j8KzRTrBf?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Symphony No. 5 in C Minor, Op. 67: I. Allegro con brio',
        'spotify_found_artist': 'Ludwig van Beethoven'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Holdvilág szonáta - Mondscheinsonate',
        'spotify_embed': 'https://open.spotify.com/embed/track/6OaCZQEFSvzf94rduujLkN?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Piano Sonata No. 14 in C-Sharp Minor, Op. 27 No. 2 "Moonlight": I. Adagio sostenuto',
        'spotify_found_artist': 'Ludwig van Beethoven'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Ode to Joy - 9. szimfónia',
        'spotify_embed': 'https://open.spotify.com/embed/track/4Nd5HJn4EExnLmHtClk4QV?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Ode to Joy',
        'spotify_found_artist': 'Ludwig van Beethoven'
    },

    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: Diótörő - Tánc a cukorkák hercegnőjéről',
        'spotify_embed': 'https://open.spotify.com/embed/track/0Qe9CUxDFvQi64Tt2EmrM6?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'The Nutcracker, Op. 71: Act II, No. 12d, Divertissement - Dance of the Sugar Plum Fairy',
        'spotify_found_artist': 'Pyotr Ilyich Tchaikovsky'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: Hattyúk tava - Swan Lake',
        'spotify_embed': 'https://open.spotify.com/embed/track/5OJCtnMqWmeGzkTJE3mpYr?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Swan Lake',
        'spotify_found_artist': 'Pyotr Ilyich Tchaikovsky'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 2,
        'explanation': 'Csajkovszkij: 1. Zongoraverseny',
        'spotify_embed': 'https://open.spotify.com/embed/track/62dD6AMgEvZq5OCHAZ7d9a?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Piano Concerto No. 1 in B-Flat Minor, Op. 23: I. Allegro non troppo e molto maestoso – Allegro con spirito - Live at Philharmonie, Berlin',
        'spotify_found_artist': 'Pyotr Ilyich Tchaikovsky'
    },

    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: Rinaldo',
        'spotify_embed': 'https://open.spotify.com/embed/track/2Sbb5o2R6zci4L0xEQhsvK?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Handel: Rinaldo, HWV 7, Act 2: "Lascia ch\'io pianga" (Almirena)',
        'spotify_found_artist': 'George Frideric Handel'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: IV. B-dúr menüett',
        'spotify_embed': 'https://open.spotify.com/embed/track/6jZj45D2jdR6fMEb58TlSc?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Suite in B-Flat Major, HWV 434: IV. Menuet',
        'spotify_found_artist': 'George Frideric Handel'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Handel', 'Bach', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Handel: Keyboard Suite in D minor',
        'spotify_embed': 'https://open.spotify.com/embed/track/6srU3wlimYXpxBNoCabQGi?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Keyboard Suite in D Minor, HWV 437: III. Sarabande (Arr. for Chamber Orchestra)',
        'spotify_found_artist': 'George Frideric Handel'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Wagner', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Wagner: A Valkűrök bevonulása',
        'spotify_embed': 'https://open.spotify.com/embed/track/2A7qdr3UNP9Pxjcxa5Jj53?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Ride of the Valkyries',
        'spotify_found_artist': 'Richard Wagner'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Wagner', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Wagner: Lohengrin - Here comes the Bride',
        'spotify_embed': 'https://open.spotify.com/embed/track/7K0WEkSBSMAHgyvOnWLJzo?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Lohengrin, WWV 75: Act III: Wedding March - "Treulich geführt"',
        'spotify_found_artist': 'Richard Wagner'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Schubert', 'Wagner', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Schubert: Ave Maria',
        'spotify_embed': 'https://open.spotify.com/embed/track/18TETrZMZTGax2T10xN4xY?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Ellens dritter Gesang (Ave Maria), D. 839',
        'spotify_found_artist': 'Franz Schubert'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Wagner', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Beethoven: Ode to Joy - 9. szimfónia',
        'spotify_embed': 'https://open.spotify.com/embed/track/4Nd5HJn4EExnLmHtClk4QV?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Symphony No. 9 in D Minor, Op. 125 "Choral": IV. Finale - Ode to Joy',
        'spotify_found_artist': 'Ludwig van Beethoven'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Háry János',
        'spotify_embed': 'https://open.spotify.com/embed/track/5C40d7tzYgdyKFCjc1mEWg?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Hary Janos: Adventure 1: Intermezzo',
        'spotify_found_artist': 'Zoltán Kodály'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Kállai kettős',
        'spotify_embed': 'https://open.spotify.com/embed/track/4HlS1s8sYBF5eVYbBkp6Be?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Kallai kettos (Kallo Double Dance): No. 1. Felulrol fuj az oszi szel',
        'spotify_found_artist': 'Zoltán Kodály'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Kodály', 'Bartók', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Kodály Zoltán: Adagio',
        'spotify_embed': 'https://open.spotify.com/embed/track/0uBi3Vc1DCiC8OeGbg6koG?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Adagio for Strings',
        'spotify_found_artist': 'Zoltán Kodály'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt Ferenc: Rákóczy induló - Hungarian Rhapsody No. 15',
        'spotify_embed': 'https://open.spotify.com/embed/track/4s2YEc66jLwMEH8WJUFh5C?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Rakoczy March from Hungarian Rhapsody No. 15 in A Minor, S. 244 / 15 - Horowitz Version',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Vivaldi', 'Bach', 'Handel', 'Mozart'],
        'correct': 0,
        'explanation': 'Vivaldi: 4 évszak',
        'spotify_embed': 'https://open.spotify.com/embed/track/5rk76Ugo6ZWsciJwvCQ4vH?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Spring (La Primavera) Op.8 No.1 E Major: Allegro',
        'spotify_found_artist': 'Antonio Vivaldi'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Vivaldi', 'Bach', 'Handel', 'Mozart'],
        'correct': 0,
        'explanation': 'Vivaldi: Szonáta',
        'spotify_embed': 'https://open.spotify.com/embed/track/7qXtc4JTbTugxB1sEktD8W?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Violin Sonata in A Major, RV 31: I. Allegro',
        'spotify_found_artist': 'Antonio Vivaldi'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Brahms', 'Beethoven', 'Mozart', 'Bach'],
        'correct': 0,
        'explanation': 'Brahms: Magyar táncok',
        'spotify_embed': 'https://open.spotify.com/embed/track/6DiWqtkdWwBzEQOhV98Cal?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'V. Magyar Tánc',
        'spotify_found_artist': 'Johannes Brahms'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt: Magyar rapszódia',
        'spotify_embed': 'https://open.spotify.com/embed/track/4MdtpUEhegl7xAdz7wjnIF?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Magyar Dalok & Rapszódiák, S. 242: No. 20 in G Minor. Romanian Rhapsody. Allegro vivace',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt: Liebestraum',
        'spotify_embed': 'https://open.spotify.com/embed/track/2u9VGZmVz7Rm01SfDgzcfA?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Liebestraum No. 3 in A-Flat Major, S. 541 / 3',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt: La campanella',
        'spotify_embed': 'https://open.spotify.com/embed/track/2Hnurh1BcigGbCGFOb4Uid?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'La campanella in G-Sharp Minor (From "Grandes études de Paganini", S. 141/3)',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt: Rákóczi induló',
        'spotify_embed': 'https://open.spotify.com/embed/track/2zIijzos3rNY6DkvX2ZYDX?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Hungarian Rhapsody No. 15 in A Minor, S. 244/15 "Rákóczi March"',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Liszt', 'Chopin', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Liszt: Consolation',
        'spotify_embed': 'https://open.spotify.com/embed/track/1L4NadMj3Jj7YgGaikyhfr?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Consolations, S. 172: No. 3 in D-Flat Major. Lento, placido',
        'spotify_found_artist': 'Franz Liszt'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Chopin', 'Liszt', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Chopin: Sonata 2 in B flat minor',
        'spotify_embed': 'https://open.spotify.com/embed/track/6JoT2QRzUZ8IpkamI6WkeN?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Chopin: Piano Sonata No. 2 in B-Flat Minor, Op. 35 "Funeral March": III. Marche funèbre. Lento',
        'spotify_found_artist': 'Frédéric Chopin'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Grieg', 'Dvorak', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Grieg: Peer Gynt Op. 23',
        'spotify_embed': 'https://open.spotify.com/embed/track/7JiIoKUNvoai56d5kYrVrx?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Grieg: Peer Gynt, Op. 23, Act 4: No. 13, Prelude. Morning Mood',
        'spotify_found_artist': 'Edvard Grieg'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Grieg', 'Dvorak', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Grieg: A hegyi király udvarában',
        'spotify_embed': 'https://open.spotify.com/embed/track/79JFQnUioUI1dH3uyubPNy?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': '19 Norwegian Folk Tunes, Op. 66: No. 3, En Konge hersked i Österland. Andante',
        'spotify_found_artist': 'Edvard Grieg'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Shostakovich', 'Prokofjev', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Shostakovich: Second waltz',
        'spotify_embed': 'https://open.spotify.com/embed/track/57KhrRvwNqwXNDdxfU3nqG?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'The Second Waltz, Op. 99a',
        'spotify_found_artist': 'Dmitri Shostakovich'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Gershwin', 'Jazz', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Gershwin: Rhapsody in Blue',
        'spotify_embed': 'https://open.spotify.com/embed/track/7oB0QBEnGRIJjvlDc8YnM6?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Rhapsody in Blue',
        'spotify_found_artist': 'George Gershwin'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bizet', 'Verdi', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Bizet: Carmen',
        'spotify_embed': 'https://open.spotify.com/embed/track/2pCLg7o60iAnNEbYDW9Lhy?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Carmen: Habanera',
        'spotify_found_artist': 'Georges Bizet'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Mozart', 'Beethoven', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Mozart: Eine kleine Nachtmusik (K. 525) - A kis éji zene',
        'spotify_embed': 'https://open.spotify.com/embed/track/2mRUmSG3XGjFloqgAT2UJN?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Eine kleine Nachtmusik K. 525: Allegro',
        'spotify_found_artist': 'Wolfgang Amadeus Mozart'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Mozart', 'Beethoven', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Mozart: Török induló - A-túr szonáta',
        'spotify_embed': 'https://open.spotify.com/embed/track/5PUn21YNL2KNzReeCwOXqp?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': '(alla turca) piano sonata n. 11 in A major, K. 331',
        'spotify_found_artist': 'Wolfgang Amadeus Mozart'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Rossini', 'Verdi', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Rossini: Tell Vilmos nyitány',
        'spotify_embed': 'https://open.spotify.com/embed/track/7c8hbMA6uohEg0Q8RVOHHS?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'William Tell Overture',
        'spotify_found_artist': 'Gioachino Rossini'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Rossini', 'Verdi', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Rossini: Sevillai borbély',
        'spotify_embed': 'https://open.spotify.com/embed/track/3PGPfeQTaZgHnmofWYBHSW?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'The Barber of Seville: Overture',
        'spotify_found_artist': 'Gioachino Rossini'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Verdi', 'Rossini', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Verdi: Traviata',
        'spotify_embed': 'https://open.spotify.com/embed/track/41ujv4mhxlqR8nlnieDpDp?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'La traviata, Act I: Libiamo ne\' lieti calici "Brindisi"',
        'spotify_found_artist': 'Giuseppe Verdi'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Verdi', 'Rossini', 'Mozart', 'Beethoven'],
        'correct': 0,
        'explanation': 'Verdi: Aida',
        'spotify_embed': 'https://open.spotify.com/embed/track/4MdA7J82XIaB65ZKcQhmY5?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Verdi: Aida, Act 2: Marcia trionfale',
        'spotify_found_artist': 'Giuseppe Verdi'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Román táncok',
        'spotify_embed': 'https://open.spotify.com/embed/track/0HhfVsdBuv62oyjNTtGolo?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Román népi táncok (Romanian Folk Dances), BB 76: No. 1. Jocul cu bata: Molto moderato',
        'spotify_found_artist': 'Béla Bartók'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Allegro Barbaro',
        'spotify_embed': 'https://open.spotify.com/embed/track/2PgaWTyAZGMGwmqfqlIwph?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Allegro Barbaro, Sz. 49',
        'spotify_found_artist': 'Béla Bartók'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Kékszakállú herceg vára',
        'spotify_embed': 'https://open.spotify.com/embed/track/7pH4osuBgzANxf5tXxRauf?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': "A Kekszakallu herceg vara (Bluebeard's Castle), Op. 11, BB 62: Nezd, hogy derul mar a varam (5. Ajto) (Look, my castle gleams and brightens (Door 5)) (Bluebeard, Judith)",
        'spotify_found_artist': 'Béla Bartók'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Bartók', 'Kodály', 'Liszt', 'Dvorak'],
        'correct': 0,
        'explanation': 'Bartók: Csodálatos mandarin',
        'spotify_embed': 'https://open.spotify.com/embed/track/03KcsheiygVoKSA4inC4WM?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'A csodálatos mandarin (the Miraculous Mandarin), Op. 19, BB 82: The girl begins a hesitant dance…',
        'spotify_found_artist': 'Béla Bartók'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Hacsaturján', 'Bartók', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Hacsaturján: Kartánc',
        'spotify_embed': 'https://open.spotify.com/embed/track/3MMxCtGgHiYrYzH2xvfFCD?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Gayane Suite No. 2: VI. Sabre Dance',
        'spotify_found_artist': 'Aram Khachaturian'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Hacsaturján', 'Bartók', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Hacsaturján: Spartacus / Onedin',
        'spotify_embed': 'https://open.spotify.com/embed/track/0Z973O9nqc2I6G0mGB4bM7?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Spartacus: Adagio of Spartacus and Phrygia',
        'spotify_found_artist': 'Aram Khachaturian'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Weiner Leó', 'Kodály', 'Bartók', 'Liszt'],
        'correct': 0,
        'explanation': 'Weiner Leó: Rókatánc',
        'spotify_embed': 'https://open.spotify.com/embed/track/63kr5smT8LmVevVOCKTEYP?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Divertimento No. 1, Op. 20 "Régi magyar táncok nyomán": II. Rókatánc',
        'spotify_found_artist': 'Leó Weiner'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Schubert', 'Mozart', 'Beethoven', 'Bach'],
        'correct': 0,
        'explanation': 'Schubert: Pisztráng ötös',
        'spotify_embed': 'https://open.spotify.com/embed/track/2GLToVCnkseCausHvzNrda?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Piano Quintet in A Major, D. 667 "The Trout": IV. Theme and Variations',
        'spotify_found_artist': 'Franz Schubert'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Rimsky-Korsakov', 'Csajkovszkij', 'Mussorgsky', 'Bach'],
        'correct': 0,
        'explanation': 'Rimsky-Korsakov: Bumblebee',
        'spotify_embed': 'https://open.spotify.com/embed/track/0nF5aQoLs2YtbWwClXvumL?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Flight of the Bumblebee',
        'spotify_found_artist': 'Nikolai Rimsky-Korsakov'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Mussorgsky', 'Rimsky-Korsakov', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Mussorgsky: Éjszaka a hegyen',
        'spotify_embed': 'https://open.spotify.com/embed/track/5rPqo5uyPn5MDoJkkiu8Nr?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Night on Bald Mountain',
        'spotify_found_artist': 'Modest Mussorgsky'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Prokofjev', 'Shostakovich', 'Csajkovszkij', 'Bach'],
        'correct': 0,
        'explanation': 'Prokofjev: Péter és a farkas',
        'spotify_embed': 'https://open.spotify.com/embed/track/29aSa4QJogizEK3Il132hD?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Péter és a farkas, gyermekeknek írt szimfonikus mese, Op. 67: II. Egyik reggel, jó korán...',
        'spotify_found_artist': 'Sergei Prokofiev'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Carl Orff', 'Bach', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Carl Orff: Carmina Burana',
        'spotify_embed': 'https://open.spotify.com/embed/track/6xez71zpAqQ6N5i8E1jHlD?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Carmina Burana: O Fortuna',
        'spotify_found_artist': 'Carl Orff'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Ravel', 'Debussy', 'Beethoven', 'Mozart'],
        'correct': 0,
        'explanation': 'Ravel: Bolero',
        'spotify_embed': 'https://open.spotify.com/embed/track/3KtsRijwp8KunCRYlOdWEi?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Boléro (Ravel)',
        'spotify_found_artist': 'London Symphony Orchestra'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Brandenburgi versenyek - 3. verseny',
        'spotify_embed': 'https://open.spotify.com/embed/track/4dl9qxvICalee6KBuuAmaJ?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Brandenburg Concerto No. 3 in G Major, BWV 1048: I. [ ]',
        'spotify_found_artist': 'Johann Sebastian Bach'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Toccata és fúga d-moll',
        'spotify_embed': 'https://open.spotify.com/embed/track/2oUllRIdt9vwj0FUdDcWlF?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'D-moll toccata és fúga',
        'spotify_found_artist': 'Rákász Gergely'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Air on G-string',
        'spotify_embed': 'https://open.spotify.com/embed/track/0mD1a7haZKdX9I0oPywrMb?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Air on a G String',
        'spotify_found_artist': 'Johann Sebastian Bach'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Italian Concerto',
        'spotify_embed': 'https://open.spotify.com/embed/track/19Ltkp5bHfTVdbotyPnp8s?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': 'Concerto In The Italian Style, BWV 971, "Italian Concerto": III. Presto',
        'spotify_found_artist': 'Janos Sebestyen'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Jesu, Joy of Man',
        'spotify_embed': 'https://open.spotify.com/embed/track/2Fyg7lcHiTth3mmeYfFCXm?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'medium',
        'spotify_found_track': "Bach Jesu Joy of Man's Desiring",
        'spotify_found_artist': 'Brodin Ray'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Brandenburg Concerto No. 5',
        'spotify_embed': 'https://open.spotify.com/embed/track/2hTOFrOwoYfpeQeKjvl1z3?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Bach, JS: Brandenburg Concerto No. 5 in D Major, BWV 1050: III. Allegro',
        'spotify_found_artist': 'Johann Sebastian Bach'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: Vivace',
        'spotify_embed': 'https://open.spotify.com/embed/track/1CvMYemOG863u8MTNkawbq?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Bach, JS: Concerto for Two Violins in D Minor, BWV 1043: I. Vivace',
        'spotify_found_artist': 'Johann Sebastian Bach'
    },
    {
        'question': 'Hallgasd meg ezt a zeneművet és válaszd ki a zeneszerzőjét:',
        'options': ['Beethoven', 'Mozart', 'Csajkovszkij', 'Bach'],
        'correct': 3,
        'explanation': 'Bach: G-dúr menüett',
        'spotify_embed': 'https://open.spotify.com/embed/track/4J9noekShoE7VBwjaG0zX8?theme=black?theme=black&size=small&hide_cover=1size=small?theme=black&size=small&hide_cover=1hide_cover=1?theme=black&size=small&hide_cover=1hide_artist=1?theme=black&size=small&hide_cover=1hide_title=1&',
        'spotify_confidence': 'high',
        'spotify_found_track': 'Menuett G Dur BWV.ANH. 114',
        'spotify_found_artist': 'Johann Sebastian Bach'
    },
]

if __name__ == "__main__":
    print(f"Komolyzenei kérdések száma: {len(CLASSICAL_MUSIC_QUESTIONS)}")
    print("Javított Spotify linkekkel:")
    for i, q in enumerate(CLASSICAL_MUSIC_QUESTIONS):
        if q['spotify_embed']:
            print(f"{i+1}. {q['explanation']} - {q['spotify_confidence']} confidence")
