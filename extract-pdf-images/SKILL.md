---
name: extract-pdf-images
description: Extract images from PDF files with rich contextual metadata including captions, surrounding text, section titles, and bounding boxes. Produces AI-agent-optimized JSON manifest for downstream consumption. Use when extracting images from PDFs, building image libraries from documents, or preparing figures for presentations, DOCX generation, or image-generation workflows.
---

<objective>
Extract all images from a PDF file and produce a structured `image_manifest.json` with rich metadata per image: caption, figure label, section title, surrounding text, bounding box, dimensions, classification, and optional AI vision analysis. Also produces `image_library.json` compatible with `biomedical-marp-presentations/scripts/image_sourcer.py`.

Two extraction engines are supported:
- **MinerU** (preferred): Leverages MinerU's layout analysis for rich contextual metadata. Requires MinerU installed.
- **PyMuPDF** (fallback): Direct image extraction with basic context. Works without MinerU.
</objective>

<quick_start>
Extract images from a PDF:

PowerShell:
```powershell
$skill = "$env:USERPROFILE\.claude\skills\extract-pdf-images\scripts"
& "$skill\extract_images.ps1" -PdfPath "paper.pdf" -OutputDir "./extracted"
```

Bash:
```bash
skill="$HOME/.claude/skills/extract-pdf-images/scripts"
bash "$skill/extract_images.sh" paper.pdf -o ./extracted
```

Python directly:
```bash
python extract_images.py paper.pdf -o ./extracted
```

With existing MinerU output:
```bash
python extract_images.py paper.pdf -o ./extracted --mineru-output ./mineru_parsed/paper
```

With Claude Vision analysis:
```bash
python extract_images.py paper.pdf -o ./extracted --analyze
```
</quick_start>

<workflow>
Follow these steps to extract images from a PDF:

1. **Identify the PDF** and choose an output directory
2. **Check engine availability**: MinerU preferred, PyMuPDF fallback
   - [ ] MinerU installed? (`mineru --help`)
   - [ ] Or existing MinerU output available? (from `parse-pdf-mineru` skill)
   - [ ] PyMuPDF installed? (`python -c "import fitz"`)
3. **Run extraction**:
   ```bash
   python extract_images.py <pdf> -o <output> [--engine auto|mineru|pymupdf]
   ```
4. **Review outputs**:
   - [ ] `image_manifest.json` exists and is valid JSON
   - [ ] `image_library.json` exists (flat format for image_sourcer)
   - [ ] `images/` directory contains extracted image files
5. **Optional enrichment**:
   - Add `--analyze` for Claude Vision descriptions (requires ANTHROPIC_API_KEY)
   - Post-process manifest to add custom keywords or fix captions

Output directory structure:
```
output/
  image_manifest.json    # Full structured manifest
  image_library.json     # Flat list for image_sourcer.py
  images/
    paper_p1_001.png
    paper_p3_002.jpg
    ...
```
</workflow>

<output_format>
The extraction produces two JSON files:

**`image_manifest.json`** — Full structured manifest with nested metadata per image. Contains `version`, `source_pdf`, `extraction` info, `summary` stats, and `images[]` array with location, context, classification, and integration fields.

**`image_library.json`** — Flat list with fields matching `image_sourcer.py`: `image_id`, `filename`, `path`, `caption`, `document_title`, `keywords`, `context_before`, `context_after`, `ocr_text`.

See `references/manifest-schema.md` for complete field documentation with examples.
</output_format>

<engine_options>
**Auto-detection** (default `--engine auto`):
1. If `--mineru-output` is provided, uses MinerU path
2. If `mineru` CLI is on PATH, runs MinerU then extracts
3. Otherwise falls back to PyMuPDF

**MinerU engine** (`--engine mineru`):
- Requires MinerU installed (`pip install magic-pdf[full]`)
- Parses `content_list.json` for sequential element stream
- Rich context: section titles, accurate captions, layout-aware text blocks
- Uses `middle.json` for precise bounding boxes and page dimensions
- Best results with `--mineru-output` pointing to existing parse

**PyMuPDF engine** (`--engine pymupdf`):
- Requires PyMuPDF (`pip install PyMuPDF>=1.24.0`)
- Direct extraction via `page.get_images()` + `doc.extract_image()`
- Basic context: proximity-based caption detection, nearby text blocks
- No section title detection (no layout analysis)
- Faster than MinerU, no GPU required

**When to use which:**
- Use MinerU when: you need accurate captions, section titles, or have already parsed with `parse-pdf-mineru`
- Use PyMuPDF when: MinerU is not installed, you need speed, or you only need the images themselves
</engine_options>

<integration>
The manifest is designed for consumption by other skills:

- **PowerPoint/PPTX**: Load manifest, filter images, use `path` with `add_picture()`
- **MARP presentations**: Use pre-computed `integration.marp_embed` strings
- **DOCX generation**: Iterate images with `context.caption` for figure captions
- **biomedical-marp-presentations**: `image_library.json` is directly loadable by `image_sourcer.py`
- **image-generation**: Use `context.caption` + `vision_analysis.description` as reference prompts
- **fetch-media**: `to_media_item_dict()` format is compatible with MediaItem patterns

See `references/integration-patterns.md` for code examples.

Auto-discovery: other skills can find extracted images at:
- Windows: `$env:TEMP\extract-pdf-images\{pdf-stem}\image_manifest.json`
- Unix: `/tmp/extract-pdf-images/{pdf-stem}/image_manifest.json`
</integration>

<cli_reference>
```
python extract_images.py <pdf_path> -o <output_dir> [options]

Required:
  pdf_path                  Path to input PDF file
  -o, --output DIR          Output directory for images and manifest

Optional:
  --mineru-output DIR       Path to existing MinerU output (skip re-running)
  --engine {auto,mineru,pymupdf}  Extraction engine (default: auto)
  --analyze                 Run Claude Vision analysis on images
  --api-key KEY             Anthropic API key (or set ANTHROPIC_API_KEY)
  --start-page N            Start page, 0-indexed (default: 0)
  --end-page N              End page, 0-indexed, inclusive
```
</cli_reference>

<success_criteria>
Extraction is successful when:
1. `image_manifest.json` exists and is valid JSON
2. `images/` directory contains files matching manifest entries
3. Each image entry has: `image_id`, `filename`, `path`, `format`, `dimensions`
4. Images with captions have non-empty `context.caption`
5. Page numbers are correct (1-indexed)

Verify:
```bash
python -c "
import json
with open('output/image_manifest.json') as f:
    m = json.load(f)
print(f'Images: {m[\"summary\"][\"total_images\"]}')
print(f'With captions: {m[\"summary\"][\"has_captions\"]}')
for img in m['images'][:3]:
    print(f'  {img[\"filename\"]} p{img[\"location\"][\"page_number\"]} - {img[\"context\"][\"caption\"][:60]}')
"
```
</success_criteria>

<reference_guides>
- `references/manifest-schema.md` — Complete JSON schema with field descriptions and examples
- `references/integration-patterns.md` — Code examples for consuming manifest in other skills
- `references/troubleshooting.md` — Common issues and solutions
</reference_guides>
