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
    # Új festmény kérdések
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jacques-Louis David', 'Jean-Auguste-Dominique Ingres', 'Eugène Delacroix', 'Théodore Géricault'],
        'correct': 0,
        'explanation': 'Antoine Laurent Lavoisier and Marie Anne Lavoisier - Jacques-Louis David',
        'image_file': 'antoine-laurent-lavoisier-and-marie-anne-lavoisier---jacques-louis-david.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Frans Hals', 'Rembrandt', 'Jan Steen', 'Gerard van Honthorst'],
        'correct': 0,
        'explanation': 'Banquet of the Officers of the St George - Frans Hals (1616)',
        'image_file': 'banquet-of-the-officers-of-the-st-george---frans-hals-1616.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Vincent van Gogh', 'Paul Gauguin', 'Henri de Toulouse-Lautrec', 'Émile Bernard'],
        'correct': 0,
        'explanation': 'Bedroom in Arles - Vincent van Gogh (1889)',
        'image_file': 'bedroom-in-arles---vincent-van-gogh-1889.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Anthony van Dyck', 'Peter Paul Rubens', 'Frans Hals', 'Rembrandt'],
        'correct': 0,
        'explanation': 'Charles I at the Hunt - Anthony van Dyck (1635)',
        'image_file': 'charles-i-at-the-hunt---anthony-van-dyck-1635.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Oreste Cortazzo', 'Giovanni Boldini', 'Giacomo Favretto', 'Vincenzo Gemito'],
        'correct': 0,
        'explanation': 'Cortazzo - Oreste Cortazzo',
        'image_file': 'cortazzo---oreste-cortazzo.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['El Greco', 'Tintoretto', 'Titian', 'Veronese'],
        'correct': 0,
        'explanation': 'El Expolio - El Greco (1577)',
        'image_file': 'el-expolio---el-greco-1577.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Francisco Goya', 'Diego Velázquez', 'El Greco', 'Bartolomé Esteban Murillo'],
        'correct': 0,
        'explanation': 'El Tres de Mayo - Francisco Goya (1808)',
        'image_file': 'el-tres-de-mayothe---francisco-goya-1808.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Paolo Veronese', 'Tintoretto', 'Titian', 'Giorgione'],
        'correct': 0,
        'explanation': 'Feast in the House of Levi - Paolo Veronese (1573)',
        'image_file': 'feast-in-the-house-of-levi---paolo-veronese-1573.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jacopo Tintoretto', 'Titian', 'Veronese', 'Giorgione'],
        'correct': 0,
        'explanation': 'Finding of the Body of St Mark - Jacopo Tintoretto (1562)',
        'image_file': 'finding-of-the-body-of-st-markl---jacopo-tintoretto-1562.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jean-Auguste-Dominique Ingres', 'Jacques-Louis David', 'Théodore Géricault', 'Eugène Delacroix'],
        'correct': 0,
        'explanation': 'French Portrait de Madame Duvaucey - Jean-Auguste-Dominique Ingres (1807)',
        'image_file': 'french-portrait-de-madame-duvaucey---jean-auguste-dominique-ingres-1807.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Monet', 'Pierre-Auguste Renoir', 'Alfred Sisley', 'Camille Pissarro'],
        'correct': 0,
        'explanation': 'Le Pont d\'Argenteuil - Claude Monet',
        'image_file': 'le-pont-dargenteuil---claude-monet.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Sailesh Chatterjee', 'Raja Ravi Varma', 'Amrita Sher-Gil', 'Jamini Roy'],
        'correct': 0,
        'explanation': 'Lotus Serenity - Sailesh Chatterjee',
        'image_file': 'lotus-serenity----sailesh-chatterjee.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Daniel Volterra', 'Michelangelo', 'Raphael', 'Leonardo da Vinci'],
        'correct': 0,
        'explanation': 'Michelangelo Buonarroti - Daniel Volterra',
        'image_file': 'michelangelo-buonarroti---daniel-volterra.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jan Brueghel the Elder', 'Pieter Brueghel the Elder', 'Pieter Brueghel the Younger', 'Jan Brueghel the Younger'],
        'correct': 0,
        'explanation': 'Paradise with the Creation and Fall of Man - Jan Brueghel the Elder (1615)',
        'image_file': 'paradise-with-the-creation-and-fall-of-man---jan-brueghel-the-elder-1615.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Titian', 'Tintoretto', 'Veronese', 'Giorgione'],
        'correct': 0,
        'explanation': 'Portrait of Charles V Seated - Titian',
        'image_file': 'portrait-of-charles-v-seated---titian.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Piero della Francesca', 'Masaccio', 'Fra Angelico', 'Sandro Botticelli'],
        'correct': 0,
        'explanation': 'Portraits of the Duke and Duchess of Urbino - Piero della Francesca (1473)',
        'image_file': 'portraits-of-the-duke-and-duchess-of-urbino-federico-da-montefeltro-and-battista-sforza---piero-della-rancesca-1473.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Claude Lorrain', 'Nicolas Poussin', 'Gaspard Dughet', 'Salvator Rosa'],
        'correct': 0,
        'explanation': 'Seaport with the Embarkation of the Queen of Sheba - Claude Lorrain (1648)',
        'image_file': 'seaport-with-the-embarkation-of-the-queen-of-sheba---claude-lorrain-1648.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Rembrandt', 'Frans Hals', 'Jan Steen', 'Gerard van Honthorst'],
        'correct': 0,
        'explanation': 'Self Portrait - Rembrandt (1659)',
        'image_file': 'selfportrait---rembrandt-1659.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Vincent van Gogh', 'Paul Gauguin', 'Henri de Toulouse-Lautrec', 'Émile Bernard'],
        'correct': 0,
        'explanation': 'Sorrow - Vincent van Gogh (1882)',
        'image_file': 'sorrow---vincent-van-gogh-1882.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Johannes Vermeer', 'Pieter de Hooch', 'Gabriel Metsu', 'Gerard ter Borch'],
        'correct': 0,
        'explanation': 'The Art of Painting - Johannes Vermeer (1666)',
        'image_file': 'the-art-of-painting---johannes-vermeer-1666.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Caravaggio', 'Orazio Gentileschi', 'Artemisia Gentileschi', 'Carlo Saraceni'],
        'correct': 0,
        'explanation': 'The Calling of Saint Matthew - Caravaggio (1599)',
        'image_file': 'the-calling-of-saint-matthew---caravaggio-1599.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jan van Eyck', 'Rogier van der Weyden', 'Hans Memling', 'Dieric Bouts'],
        'correct': 0,
        'explanation': 'The Crucifixion - Jan van Eyck',
        'image_file': 'the-crucifiction ---jan-van-eyck.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Rembrandt', 'Frans Hals', 'Jan Steen', 'Gerard van Honthorst'],
        'correct': 0,
        'explanation': 'The Holy Family - Rembrandt (2023)',
        'image_file': 'the-holy-family-rembrandt---goldenartists-2023.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Leonardo da Vinci', 'Raphael', 'Sandro Botticelli', 'Piero della Francesca'],
        'correct': 0,
        'explanation': 'The Lady with an Ermine - Leonardo da Vinci (1490)',
        'image_file': 'the-lady-with-an-ermine-portrait-of-cecilia-gallerani---leonardo-da-vinci-1490.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Jacques-Louis David', 'Jean-Auguste-Dominique Ingres', 'Théodore Géricault', 'Eugène Delacroix'],
        'correct': 0,
        'explanation': 'The Oath of the Horatii - Jacques-Louis David (1784)',
        'image_file': 'the-oath-of-the-horatii---jacqueslouis-david-1784.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Peter Paul Rubens', 'Anthony van Dyck', 'Frans Hals', 'Rembrandt'],
        'correct': 0,
        'explanation': 'The Rape of the Daughters of Leucippus - Peter Paul Rubens (1618)',
        'image_file': 'the-rape-of-the-daughters-of-leucippus---peter-paul-rubens-1618.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Vincent van Gogh', 'Paul Gauguin', 'Henri de Toulouse-Lautrec', 'Émile Bernard'],
        'correct': 0,
        'explanation': 'Wheat Field with Cypresses - Vincent van Gogh (1899)',
        'image_file': 'wheat-field-with-cypresses---vincent-van-gogh-1899.jpg',
        'topic': 'festmények'
    },
    # További új festmény kérdések
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Paul Gauguin', 'Vincent van Gogh', 'Henri de Toulouse-Lautrec', 'Émile Bernard'],
        'correct': 0,
        'explanation': 'Two Tahitian Women - Paul Gauguin (1899)',
        'image_file': 'two-tahitian-women---paul-gaugin-1899.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Paul Klee', 'Wassily Kandinsky', 'Franz Marc', 'August Macke'],
        'correct': 0,
        'explanation': 'Villa R - Paul Klee (1919)',
        'image_file': 'villa-r---paul-klee-1919.jpg',
        'topic': 'festmények'
    },
    {
        'question': 'Nézd meg ezt a festményt és válaszd ki a festő nevét:',
        'options': ['Amedeo Modigliani', 'Pablo Picasso', 'Henri Matisse', 'Georges Braque'],
        'correct': 0,
        'explanation': 'Woman with Black Cravat - Amedeo Modigliani (1917)',
        'image_file': 'woman-with-black-cravat---amedeo-modigliani-1917.jpg',
        'topic': 'festmények'
    },
]

if __name__ == "__main__":
    print(f"Festmény kérdések száma: {len(FESTMENY_QUESTIONS)}")
    print("Első 5 kérdés:")
    for i, q in enumerate(FESTMENY_QUESTIONS[:5]):
        print(f"{i+1}. {q['explanation']}")
        print(f"   Fájl: {q['image_file']}")
