# Integration Patterns

How other skills consume images extracted by `extract-pdf-images`.

## Loading the Manifest

```python
import json
from pathlib import Path

# Load full manifest
with open("output/image_manifest.json") as f:
    manifest = json.load(f)

images = manifest["images"]
print(f"Found {manifest['summary']['total_images']} images")
```

```python
# Load flat library (image_sourcer-compatible)
with open("output/image_library.json") as f:
    library = json.load(f)
```

## PowerPoint / PPTX Creation

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation()

for img in images:
    if img["classification"]["is_decorative"]:
        continue

    slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank

    # Add image using relative path from manifest
    slide.shapes.add_picture(
        img["path"],
        Inches(1), Inches(1.5),
        width=Inches(6)
    )

    # Add caption
    if img["context"]["caption"]:
        txBox = slide.shapes.add_textbox(Inches(1), Inches(6), Inches(6), Inches(1))
        txBox.text_frame.text = img["context"]["caption"]

prs.save("figures.pptx")
```

## MARP Presentations

```python
# Use pre-computed MARP embed strings
for img in images:
    if img["classification"]["image_type"] in ("figure", "chart", "diagram"):
        print(f"---\n")
        print(f"## {img['context']['section_title']}\n")
        print(img["integration"]["marp_embed"])
        if img["context"]["caption"]:
            print(f"\n*{img['context']['caption']}*")
```

## Biomedical MARP Presentations (image_sourcer.py)

The `image_library.json` output is directly compatible with `image_sourcer.py`:

```bash
python image_sourcer.py output/image_library.json "TMS coil placement" --max-results 3
```

The flat library format provides all fields expected by the scoring algorithm:
- `keywords` for exact/partial keyword matching
- `document_title` (mapped from section_title) for title matching
- `caption` for caption matching
- `context_before` / `context_after` for context matching
- `ocr_text` for OCR text matching (populated when --analyze is used)

## DOCX Generation

```python
from docx import Document
from docx.shared import Inches

doc = Document()

for img in images:
    if img["context"]["section_title"]:
        doc.add_heading(img["context"]["section_title"], level=2)

    doc.add_picture(img["path"], width=Inches(5))

    if img["context"]["caption"]:
        p = doc.add_paragraph(img["context"]["caption"])
        p.style = "Caption"

doc.save("figures.docx")
```

## Image Generation (reference-based)

Pass extracted images + context as references to image generation skills:

```python
# Use caption as prompt context for Gemini/DALL-E
for img in images:
    prompt = f"Based on: {img['context']['caption']}"
    if img.get("vision_analysis") and img["vision_analysis"].get("description"):
        prompt += f"\nDescription: {img['vision_analysis']['description']}"
    # Pass to image generation API...
```

## Auto-Discovery via Temp Directory

Other skills can find extracted images via the temp directory convention:

```python
import os, glob, platform
from pathlib import Path

def find_extracted_images(pdf_stem: str):
    """Find previously extracted images for a PDF."""
    if platform.system() == "Windows":
        base = Path(os.environ.get("TEMP", ""))
    else:
        base = Path("/tmp")

    manifest = base / "extract-pdf-images" / pdf_stem / "image_manifest.json"
    if manifest.exists():
        import json
        with open(manifest) as f:
            return json.load(f)
    return None
```

## Filtering Images

Common filtering patterns:

```python
# Only figures (skip decorative)
figures = [img for img in images if not img["classification"]["is_decorative"]]

# Only from specific section
methods_figs = [img for img in images if "methods" in img["context"]["section_title"].lower()]

# Only charts and diagrams
visuals = [img for img in images if img["classification"]["image_type"] in ("chart", "diagram")]

# Images with captions
captioned = [img for img in images if img["context"]["caption"]]

# By page range
page_range = [img for img in images if 5 <= img["location"]["page_number"] <= 10]

# By keyword
keyword_match = [img for img in images if any("neural" in kw for kw in img["classification"]["keywords"])]
```
