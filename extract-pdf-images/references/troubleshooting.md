# Troubleshooting

Common issues and solutions when using `extract-pdf-images`.

## MinerU Not Installed

**Symptom:** `MinerU not found. Using PyMuPDF fallback.`

**Solutions:**
1. Install MinerU: `pip install magic-pdf[full]` (requires GPU for best results)
2. Or explicitly use PyMuPDF: `--engine pymupdf`
3. If MinerU is installed but not on PATH, activate its conda/venv environment first

**Note:** PyMuPDF fallback works well for image extraction but produces sparser context (no section titles from layout analysis, less reliable caption detection).

## Empty Extraction (0 images)

**Possible causes:**
1. **PDF has no embedded images** — Some PDFs render graphics as vector paths, not images. Try opening in a PDF viewer to confirm images exist.
2. **Page range excludes images** — Check `--start-page` and `--end-page` arguments.
3. **MinerU output path wrong** — Verify `--mineru-output` points to the correct directory containing `content_list.json`.
4. **Scanned PDF** — If the PDF is a scan, images may be full-page rasters. These will extract as one image per page.

**Debug steps:**
```bash
# Check with PyMuPDF directly
python -c "
import fitz
doc = fitz.open('paper.pdf')
for i, page in enumerate(doc):
    imgs = page.get_images(full=True)
    print(f'Page {i+1}: {len(imgs)} images')
"
```

## Missing Context (empty captions)

**Cause:** Caption detection relies on pattern matching for `Figure/Fig./Table/Exhibit` followed by a number. Uncommon labeling schemes may not match.

**Solutions:**
1. Use MinerU engine for better layout analysis
2. Use `--analyze` flag for Claude Vision to generate descriptions
3. Post-process: load `image_manifest.json` and manually add captions

## PyMuPDF Version Issues

**Symptom:** `ImportError: No module named 'fitz'` or `AttributeError: 'Page' object has no attribute 'get_images'`

**Solution:** Upgrade PyMuPDF:
```bash
pip install --upgrade PyMuPDF>=1.24.0
```

**Note:** The package name on PyPI is `PyMuPDF` but the import name is `fitz`.

## Vision Analysis Failures

**Symptom:** `Warning: No Anthropic API key found. Skipping vision analysis.`

**Solutions:**
1. Set environment variable: `export ANTHROPIC_API_KEY=sk-ant-...`
2. Or pass directly: `--api-key sk-ant-...`
3. Install the SDK: `pip install anthropic`

**Symptom:** Vision analysis fails for specific images

**Possible causes:**
- Image too large (>20MB) — rare for extracted images
- Unsupported format — convert to PNG/JPG
- API rate limits — the script processes images sequentially

## Manifest Not Valid JSON

This should not happen. If it does:
1. Check disk space
2. Verify write permissions to the output directory
3. Check for non-UTF-8 characters in the PDF text

## Large PDFs (100+ pages)

For large PDFs, extract in page ranges to manage memory:

```bash
python extract_images.py large.pdf -o ./out --start-page 0 --end-page 49
python extract_images.py large.pdf -o ./out2 --start-page 50 --end-page 99
```

Or use MinerU with page range:
```bash
mineru -p large.pdf -o ./mineru_out -s 0 -e 49
python extract_images.py large.pdf -o ./out --mineru-output ./mineru_out
```

## Integration Issues

### image_sourcer.py returns no matches

The `image_library.json` must be in the expected format. Verify:
```bash
python -c "
import json
with open('output/image_library.json') as f:
    lib = json.load(f)
print(f'{len(lib)} images')
print('Fields:', list(lib[0].keys()) if lib else 'empty')
"
```

Expected fields: `image_id`, `filename`, `path`, `caption`, `document_title`, `context_before`, `context_after`, `ocr_text`, `keywords`

### PowerPoint images not found

The `path` field in the manifest is relative to the output directory. When creating PPTX, either:
- Run from the output directory
- Use `absolute_path` instead of `path`
