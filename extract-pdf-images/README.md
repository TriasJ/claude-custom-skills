# extract-pdf-images

A Claude Code skill that extracts images from PDF files with rich contextual metadata — captions, surrounding text, section titles, bounding boxes — and produces AI-agent-optimized JSON output.

## Features

- **Dual engine support**: MinerU (rich layout analysis) with PyMuPDF fallback
- **Rich context per image**: caption, figure label, section title, surrounding text, bounding box
- **Structured output**: `image_manifest.json` (nested) + `image_library.json` (flat, image_sourcer-compatible)
- **Optional AI analysis**: Claude Vision descriptions via `--analyze` flag
- **Cross-platform**: PowerShell + Bash wrappers, Python core

## Quick Start

```bash
# Basic extraction
python scripts/extract_images.py paper.pdf -o ./output

# With existing MinerU parse
python scripts/extract_images.py paper.pdf -o ./output --mineru-output ./mineru_parsed/paper

# PyMuPDF only (no MinerU required)
python scripts/extract_images.py paper.pdf -o ./output --engine pymupdf

# With Claude Vision analysis
python scripts/extract_images.py paper.pdf -o ./output --analyze
```

## Requirements

```bash
pip install -r scripts/requirements.txt
```

- **Pillow** >= 10.0 (image dimensions)
- **PyMuPDF** >= 1.24.0 (fallback extraction engine)
- **MinerU** (optional, preferred engine): `pip install magic-pdf[full]`
- **anthropic** (optional, for `--analyze`): `pip install anthropic`

## Output

```
output/
  image_manifest.json    # Full structured manifest
  image_library.json     # Flat list for image_sourcer.py
  images/
    paper_p1_001.png
    paper_p3_002.jpg
```

## Claude Code Skill

This is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill. Install by placing in `~/.claude/skills/extract-pdf-images/`.

Slash command: `/extract-pdf-images <pdf_path> [output_dir]`

## Documentation

- [Manifest Schema](references/manifest-schema.md) — JSON field reference
- [Integration Patterns](references/integration-patterns.md) — How other skills consume the output
- [Troubleshooting](references/troubleshooting.md) — Common issues and fixes

## License

MIT
