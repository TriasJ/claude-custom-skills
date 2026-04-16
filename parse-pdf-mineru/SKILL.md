---
name: parse-pdf-mineru
description: Extract text, images, tables, and formulas from PDFs using MinerU. Creates comprehensive markdown documents with layout preservation. Use when parsing PDFs, extracting structured content, converting documents to markdown, or when user mentions PDF extraction, document parsing, or text extraction from PDFs.
---

<objective>
MinerU is a high-quality PDF to Markdown/JSON converter that extracts:
- Text with layout preservation
- Images to a dedicated folder
- Tables with structure intact
- Mathematical formulas and equations

This skill enables comprehensive PDF parsing that produces clean markdown documents suitable for further processing, analysis, or display.
</objective>

<quick_start>
Parse a PDF to markdown with all features:

```bash
mineru -p "path/to/document.pdf" -o "./output"
```

This creates in the output folder:
- `document.md` - Markdown with full content
- `document_content_list.json` - Structured content list
- `images/` - Extracted images

Parse specific pages only:
```bash
mineru -p "document.pdf" -o "./output" -s 0 -e 10
```

Parse with English language optimization:
```bash
mineru -p "document.pdf" -o "./output" -l en
```
</quick_start>

<workflow>
1. **Identify the PDF**: Get the full path to the PDF file
2. **Create output directory**: Choose or create a directory for outputs
3. **Run MinerU**: Execute the parsing command with appropriate options
4. **Review outputs**: Check the generated markdown and images
5. **Post-process if needed**: Edit markdown or organize images as required

For batch processing multiple PDFs:
```bash
mineru -p "./pdf_folder/" -o "./output"
```
</workflow>

<output_formats>
MinerU generates multiple output files:

| File | Description |
|------|-------------|
| `{filename}.md` | Main markdown output with text, tables, formulas |
| `{filename}_content_list.json` | Structured content as JSON array |
| `{filename}_middle.json` | Intermediate processing data |
| `images/` | Directory containing all extracted images |

Images in markdown are referenced as: `![image](images/image_name.png)`
</output_formats>

<options>
Common CLI options:

| Option | Description | Example |
|--------|-------------|---------|
| `-p, --path` | Input PDF path or directory | `-p doc.pdf` |
| `-o, --output` | Output directory | `-o ./results` |
| `-s, --start` | Start page (0-indexed) | `-s 0` |
| `-e, --end` | End page (0-indexed) | `-e 10` |
| `-l, --lang` | Language for OCR | `-l en` |
| `-m, --method` | Parsing method: auto, txt, ocr | `-m auto` |
| `-f, --formula` | Enable formula parsing | `-f true` |
| `-t, --table` | Enable table parsing | `-t true` |
| `-b, --backend` | Processing backend | `-b pipeline` |

Supported languages: `en`, `ch`, `korean`, `japan`, `arabic`, `latin`, and more.
</options>

<backends>
MinerU supports multiple processing backends:

- **hybrid-auto-engine** (default): Best accuracy, uses local GPU/CPU
- **pipeline**: General purpose, most compatible
- **vlm-auto-engine**: High accuracy with vision language models
- **hybrid-http-client**: Remote processing, minimal local resources
- **vlm-http-client**: Remote VLM processing

For CPU-only systems, use the pipeline backend:
```bash
mineru -p "doc.pdf" -o "./output" -b pipeline -d cpu
```
</backends>

<advanced_features>
For advanced usage including Python API, batch processing, and server deployment, see:
- `references/advanced-options.md` - Full CLI and Python API documentation
- `references/troubleshooting.md` - Common issues and solutions

Python API example:
```python
from mineru.cli.common import do_parse, read_fn
from pathlib import Path

pdf_bytes = read_fn(Path("document.pdf"))
do_parse(
    output_dir="./output",
    pdf_file_names=["document"],
    pdf_bytes_list=[pdf_bytes],
    f_dump_md=True,
    f_dump_content_list=True
)
```
</advanced_features>

<success_criteria>
Successful PDF parsing is confirmed when:
1. Output directory contains `{filename}.md` file
2. Markdown file contains extracted text with proper formatting
3. Images folder contains extracted images (if PDF had images)
4. Tables are rendered as markdown tables
5. Formulas appear as LaTeX (if formula parsing enabled)

Verify with:
```bash
dir ./output
type ./output/document.md | head -50
```
</success_criteria>
