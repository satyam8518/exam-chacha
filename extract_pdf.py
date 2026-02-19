import json
from pathlib import Path
from PyPDF2 import PdfReader

# Input PDF (from user's attachment)
pdf_path = Path(r"C:\Users\pc\Downloads\Polity class - 6.pdf")
output_json = Path(__file__).resolve().parent / "ba_polity_v6.json"

text_blocks = []
reader = PdfReader(str(pdf_path))
for page in reader.pages:
    text = page.extract_text() or ""
    # normalize bullets and split into paragraphs
    text = text.replace('\r', '\n')
    parts = [p.strip() for p in text.split('\n\n') if p.strip()]
    if not parts:
        # fallback: split by single newline
        parts = [p.strip() for p in text.split('\n') if p.strip()]
    text_blocks.extend(parts)

# Heuristic: group continuous lines that start with bullet '•' or contain short length into slides
slides = []
for block in text_blocks:
    if block.startswith('•'):
        # split bullets inside block
        bullets = [b.strip() for b in block.split('•') if b.strip()]
        for b in bullets:
            slides.append('• ' + b)
    else:
        # treat as a slide paragraph
        slides.append(block)

# Build JSON structure similar to existing files
subject = {
    "subjectId": "ba_sub_polity_v6",
    "subjectTitle": "भारतीय राजव्यवस्था (Class-6)",
    "topics": [
        {
            "title": "राजव्यवस्था और संविधान: Class-6",
            "slides": slides,
            "questions": []
        }
    ]
}

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(subject, f, ensure_ascii=False, indent=2)

print(f"Wrote {output_json}")
