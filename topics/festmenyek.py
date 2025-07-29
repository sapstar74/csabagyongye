#!/usr/bin/env python3
"""
Festmény kérdések a quiz alkalmazáshoz
Népszerű festmények és festők
"""

FESTMENY_QUESTIONS = [
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pablo Picasso', 'Marc Chagall', 'John Constable', 'Leonardo da Vinci'],
        'correct': 3,
        'explanation': 'Mona Lisa - Leonardo da Vinci (1503-1519)',
        'image_file': 'mona-lisa---Leonardo-Da-Vinci-1519.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Vincent van Gogh', 'Leonardo da Vinci', 'Raphael', 'Sandro Botticelli'],
        'correct': 0,
        'explanation': 'The Starry Night - Vincent van Gogh (1889)',
        'image_file': 'the-starry-night---vincent-van-gogh-1889.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Andy Warhol', 'Edvard Munch', 'Claude Monet', 'Johannes Vermeer'],
        'correct': 1,
        'explanation': 'The Scream - Edvard Munch (1893)',
        'image_file': 'the-scream---edvard-munch-1893.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Monet', "Georgia O'Keeffe", 'Frida Kahlo', 'Salvador Dalí'],
        'correct': 3,
        'explanation': 'The Persistence of Memory - Salvador Dalí (1931)',
        'image_file': 'the-persistence-of-memory---salvador-dal-1931.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pierre-Auguste Renoir', 'Raphael', 'Johannes Vermeer', 'Sandro Botticelli'],
        'correct': 2,
        'explanation': 'Girl with a Pearl Earring - Johannes Vermeer (1665)',
        'image_file': 'girl-with-a-pearl-earring---johannes-vermeer-1665.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Eugène Delacroix', 'Sandro Botticelli', 'Wassily Kandinsky', 'Édouard Manet'],
        'correct': 1,
        'explanation': 'The Birth of Venus - Sandro Botticelli (1485)',
        'image_file': 'the-birth-of-venus---sandro-botticelli-1485.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pablo Picasso', 'Hieronymus Bosch', 'Vincent van Gogh', 'Frida Kahlo'],
        'correct': 0,
        'explanation': 'Guernica - Pablo Picasso (1937)',
        'image_file': 'guernica---pablo-picasso-1937.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Rembrandt', 'Marc Chagall', 'Hieronymus Bosch', 'Georges Seurat'],
        'correct': 0,
        'explanation': 'The Night Watch - Rembrandt (1642)',
        'image_file': 'the-night-watch---rembrandt-1642.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Gustav Klimt', 'Claude Monet', 'Edvard Munch', 'John Constable'],
        'correct': 1,
        'explanation': 'Water Lilies - Claude Monet (1916)',
        'image_file': 'water-lilies---claude-monet-1916.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Grant Wood', 'Jackson Pollock', 'Gustav Klimt', 'Rembrandt'],
        'correct': 2,
        'explanation': 'The Kiss - Gustav Klimt (1908)',
        'image_file': 'the-kiss---gustav-klimt-1908.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pierre-Auguste Renoir', 'John Constable', 'Vincent van Gogh', 'René Magritte'],
        'correct': 2,
        'explanation': 'Self-Portrait with Bandaged Ear - Vincent van Gogh (1889)',
        'image_file': 'self-portrait-with-bandaged-ear---vincent-van-gogh-1889.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pablo Picasso', 'Raphael', 'Hieronymus Bosch', 'Leonardo da Vinci'],
        'correct': 3,
        'explanation': 'The Last Supper - Leonardo da Vinci (1495-1498)',
        'image_file': 'the-last-supper---Leonardo-da-Vinci-1495.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Rembrandt', 'Jackson Pollock', 'Hieronymus Bosch', 'René Magritte'],
        'correct': 2,
        'explanation': 'The Garden of Earthly Delights - Hieronymus Bosch (1503-1515)',
        'image_file': 'the-garden-of-earthly-delights---hierno1515.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jackson Pollock', 'Marc Chagall', 'Pablo Picasso', 'Raphael'],
        'correct': 2,
        'explanation': "Les Demoiselles d'Avignon - Pablo Picasso (1907)",
        'image_file': 'les-demoiselles-davignon---pablo-picasso-1907.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Edvard Munch', 'Jan van Eyck', 'Sandro Botticelli', 'Eugène Delacroix'],
        'correct': 1,
        'explanation': 'The Arnolfini Portrait - Jan van Eyck (1434)',
        'image_file': 'the-arnolfini-portrait---jan-van-eyck-1434.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Michelangelo', 'Pablo Picasso', 'Pierre-Auguste Renoir', 'Raphael'],
        'correct': 0,
        'explanation': 'The Creation of Adam - Michelangelo (1512)',
        'image_file': 'the-creation-of-adam---michelangelo-1512.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Monet', 'Michelangelo', 'Raphael', 'Auguste Rodin'],
        'correct': 2,
        'explanation': 'The School of Athens - Raphael (1509-1511)',
        'image_file': 'the-school-of-athens---raphael-1511.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Monet', 'Edgar Degas', 'Edvard Munch', 'Pierre-Auguste Renoir'],
        'correct': 0,
        'explanation': 'Impression, Sunrise - Claude Monet (1872)',
        'image_file': 'impression-sunrise---claude-monet-1872.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Edvard Munch', 'Katsushika Hokusai', 'Paul Cézanne', 'René Magritte'],
        'correct': 3,
        'explanation': 'The Son of Man - René Magritte (1964)',
        'image_file': 'the-son-of-man---ren-magritte-1964.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Johannes Vermeer', 'Grant Wood', 'Andy Warhol', 'Jan van Eyck'],
        'correct': 1,
        'explanation': 'American Gothic - Grant Wood (1930)',
        'image_file': 'american-gothic---grant-wood-1930.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Frida Kahlo', 'Katsushika Hokusai', 'Rembrandt', 'Wassily Kandinsky'],
        'correct': 1,
        'explanation': 'The Great Wave off Kanagawa - Katsushika Hokusai (1831)',
        'image_file': 'the-great-wave-off-kanagawa---katsushika-hokusai-1831.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Edgar Degas', 'Johannes Vermeer', 'Auguste Rodin', 'Pablo Picasso'],
        'correct': 2,
        'explanation': 'The Thinker - Auguste Rodin (1904)',
        'image_file': 'the-thinker---auguste-rodin-1904.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Andy Warhol', 'Henri Matisse', 'Leonardo da Vinci', 'René Magritte'],
        'correct': 1,
        'explanation': 'The Dance - Henri Matisse (1910)',
        'image_file': 'the-dance---henri-matisse-1910.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Leonardo da Vinci', 'Georges Seurat', 'Wassily Kandinsky', 'Edvard Munch'],
        'correct': 2,
        'explanation': 'Composition VII - Wassily Kandinsky (1913)',
        'image_file': 'composition-vii---wassily-kandinsky-1913.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Monet', 'Henri Matisse', 'Raphael', 'Frida Kahlo'],
        'correct': 3,
        'explanation': 'The Two Fridas - Frida Kahlo (1939)',
        'image_file': 'the-two-fridas---frida-kahlo-1939.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Auguste Rodin', 'Jackson Pollock', 'Andy Warhol', 'Vincent van Gogh'],
        'correct': 2,
        'explanation': "Campbell's Soup Cans - Andy Warhol (1962)",
        'image_file': 'campbells-soup-cans---andy-warhol-1962.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Johannes Vermeer', 'John Constable', 'Jackson Pollock', 'Pierre-Auguste Renoir'],
        'correct': 2,
        'explanation': 'Number 1 (Lavender Mist) - Jackson Pollock (1950)',
        'image_file': 'number-1-lavender-mist---jackson-pollock-1950.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pablo Picasso', 'Auguste Rodin', 'Paul Cézanne', 'Leonardo da Vinci'],
        'correct': 2,
        'explanation': 'The Card Players - Paul Cézanne (1892)',
        'image_file': 'the-card-players---paul-czanne-1892.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Édouard Manet', 'Marc Chagall', 'Hieronymus Bosch', 'Michelangelo'],
        'correct': 0,
        'explanation': 'The Luncheon on the Grass - Édouard Manet (1863)',
        'image_file': 'the-luncheon-on-the-grass---douard-manet-1863.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Pierre-Auguste Renoir', 'John Constable', 'Jackson Pollock', 'Johannes Vermeer'],
        'correct': 1,
        'explanation': 'The Hay Wain - John Constable (1821)',
        'image_file': 'the-hay-wain---john-constable-1821.jpg',
        'topic': 'festmények'
    },
]

if __name__ == "__main__":
    print(f"Festmény kérdések száma: {len(FESTMENY_QUESTIONS)}")
    print("Első 5 kérdés:")
    for i, q in enumerate(FESTMENY_QUESTIONS[:5]):
        print(f"{i+1}. {q['explanation']}")
        print(f"   Fájl: {q['image_file']}")
