#!/usr/bin/env python3
"""
Convert quiz_temakorok_v2.docx to topic Python files.
Extracts questions from the docx and creates 9 topic files.
"""
import zipfile
import xml.etree.ElementTree as ET
import re
import os

DOCX_PATH = '/Users/zsigagabor/Downloads/quiz_temakorok_v2.docx'
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'topics')

TOPIC_SECTIONS = [
    ("1.  VALLÁS ÉS EGYHÁZTÖRTÉNET", "vallás és egyháztörténet", "VALLAS_EGYHAZTORTENET_QUESTIONS"),
    ("2.  MŰVÉSZET – KÉPZŐ, ZENE, FILM, SZÍNHÁZ, MAGYAR KULTÚRA", "művészet", "MUVESZET_QUESTIONS"),
    ("3.  TERMÉSZETTUDOMÁNY – TECHNIKA, FELFEDEZÉSEK", "természettudomány", "TERMESZETTUDOMANY_QUESTIONS"),
    ("4.  IRODALOM", "irodalom", "IRODALOM_QUESTIONS"),
    ("5.  POLITIKA", "politika", "POLITIKA_QUESTIONS"),
    ("6.  VILÁGTÖRTÉNELEM", "világtörténelem", "VILAGTORTENELM_QUESTIONS"),
    ("7.  MAGYAR TÖRTÉNELEM", "magyar történelem", "MAGYAR_TORTENELM_QUESTIONS"),
    ("8.  BIOLÓGIA", "biológia", "BIOLOGIA_QUESTIONS"),
    ("9.  SPORT", "sport", "SPORT_QUESTIONS"),
]

# Színkód a helyes válaszok jelölésére a docx-ben (piros)
CORRECT_ANSWER_COLOR = 'C00000'

def extract_paragraphs_with_formatting(path):
    """Extract paragraphs with text and whether they have the 'correct answer' color."""
    with zipfile.ZipFile(path, 'r') as z:
        xml_content = z.read('word/document.xml')
    root = ET.fromstring(xml_content)
    ns = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    result = []
    for p in root.iter(f'{{{ns}}}p'):
        texts = []
        has_correct_color = False
        for r in p.findall(f'.//{{{ns}}}r'):
            rPr = r.find(f'{{{ns}}}rPr')
            color_val = None
            if rPr is not None:
                color_elem = rPr.find(f'{{{ns}}}color')
                if color_elem is not None:
                    color_val = color_elem.get(f'{{{ns}}}val', '')
            if color_val and color_val.upper() == CORRECT_ANSWER_COLOR.upper():
                has_correct_color = True
            t = r.find(f'{{{ns}}}t')
            if t is not None and t.text:
                texts.append(t.text)
        if texts:
            result.append((''.join(texts), has_correct_color))
    return result

def extract_text_from_docx(path):
    """Extract all paragraph text from docx (backward compat)."""
    return [p[0] for p in extract_paragraphs_with_formatting(path)]

def parse_questions(paragraphs_with_format, start_idx, end_idx):
    """Parse questions from paragraphs. paragraphs_with_format: list of (text, has_correct_color)."""
    questions = []
    i = start_idx
    while i < end_idx:
        line, _ = paragraphs_with_format[i]
        # Check for question number (e.g. "1.", "2.", "61.")
        num_match = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
        if num_match and not line.strip().startswith(('A)', 'B)', 'C)', 'D)')):
            question_text = num_match.group(2).strip()
            options = []
            correct = 0  # Default
            i += 1
            while i < end_idx:
                opt_line, has_correct = paragraphs_with_format[i]
                if re.match(r'^[A-D]\)', opt_line.strip()):
                    opt_text = re.sub(r'^[A-D]\)\s*', '', opt_line.strip()).strip()
                    options.append(opt_text)
                    if has_correct:
                        correct = len(options) - 1
                    i += 1
                    if len(options) == 4:
                        break
                elif re.match(r'^\d+\.\s+', opt_line.strip()) and not opt_line.strip().startswith(('A)', 'B)', 'C)', 'D)')):
                    break
                else:
                    i += 1
            if len(options) == 4 and question_text:
                questions.append({
                    "question": question_text,
                    "options": options,
                    "correct": correct,
                    "explanation": f"Helyes válasz: {options[correct]}",
                    "topic": ""
                })
            continue
        i += 1
    return questions

def find_section_boundaries(paragraphs_with_format):
    """Find start and end indices for each topic section. paragraphs_with_format: list of (text, bool)."""
    paragraphs = [p[0] for p in paragraphs_with_format]
    boundaries = []
    for idx, section_header in enumerate(TOPIC_SECTIONS):
        header_text = section_header[0]
        start = None
        for i, p in enumerate(paragraphs):
            if header_text in p:
                start = i + 2  # Skip header and "X kérdés" line
                break
        if start is None:
            continue
        # Find end = start of next section
        end = len(paragraphs)
        if idx + 1 < len(TOPIC_SECTIONS):
            next_header = TOPIC_SECTIONS[idx + 1][0]
            for i in range(start, len(paragraphs)):
                if next_header in paragraphs[i]:
                    end = i
                    break
        boundaries.append((start, end))
    return boundaries

def escape_for_python(s):
    """Escape string for Python string literal."""
    return s.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')

def generate_python_file(topic_id, var_name, questions, topic_label):
    """Generate Python file content for a topic."""
    lines = [
        f"# {topic_label} kvíz kérdések",
        f"# {len(questions)} kérdés a quiz_temakorok_v2.docx alapján",
        "",
        f"{var_name} = ["
    ]
    for q in questions:
        q["topic"] = topic_label
        opt_str = ",\n        ".join([f'"{escape_for_python(opt)}"' for opt in q["options"]])
        lines.append(f'    {{')
        lines.append(f'        "question": "{escape_for_python(q["question"])}",')
        lines.append(f'        "options": [{opt_str}],')
        lines.append(f'        "correct": {q["correct"]},')
        lines.append(f'        "explanation": "{escape_for_python(q["explanation"])}",')
        lines.append(f'        "topic": "{topic_label}"')
        lines.append(f'    }},')
    lines[-1] = lines[-1].rstrip(',')  # Remove trailing comma from last item
    lines.append("]")
    return "\n".join(lines)

def main():
    paragraphs_with_format = extract_paragraphs_with_formatting(DOCX_PATH)
    boundaries = find_section_boundaries(paragraphs_with_format)
    
    file_mapping = [
        ("vallas_egyhaztortenet.py", "VALLAS_EGYHAZTORTENET_QUESTIONS", "vallás és egyháztörténet"),
        ("muveszet.py", "MUVESZET_QUESTIONS", "művészet"),
        ("termeszettudomany.py", "TERMESZETTUDOMANY_QUESTIONS", "természettudomány"),
        ("irodalom.py", "IRODALOM_QUESTIONS", "irodalom"),
        ("politika.py", "POLITIKA_QUESTIONS", "politika"),
        ("vilagtortenelm.py", "VILAGTORTENELM_QUESTIONS", "világtörténelem"),
        ("magyar_tortenelm.py", "MAGYAR_TORTENELM_QUESTIONS", "magyar történelem"),
        ("biologia.py", "BIOLOGIA_QUESTIONS", "biológia"),
        ("sport.py", "SPORT_QUESTIONS", "sport"),
    ]
    
    for (filename, var_name, topic_label), (start, end) in zip(file_mapping, boundaries):
        questions = parse_questions(paragraphs_with_format, start, end)
        # Deduplicate by question text
        seen = set()
        unique_questions = []
        for q in questions:
            key = q["question"][:100]
            if key not in seen:
                seen.add(key)
                unique_questions.append(q)
        
        content = generate_python_file(topic_label, var_name, unique_questions, topic_label)
        out_path = os.path.join(OUTPUT_DIR, filename)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Created {filename} with {len(unique_questions)} questions")

if __name__ == "__main__":
    main()
