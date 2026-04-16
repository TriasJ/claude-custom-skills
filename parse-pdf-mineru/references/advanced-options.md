# MinerU Advanced Options Reference

## Table of Contents
- [CLI Reference](#cli-reference)
- [Python API](#python-api)
- [Environment Variables](#environment-variables)
- [Backend Configuration](#backend-configuration)
- [Batch Processing](#batch-processing)

---

## CLI Reference

### Full Command Syntax
```bash
mineru [OPTIONS]
```

### All Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `-v, --version` | flag | - | Display version and exit |
| `-p, --path` | PATH | required | Input PDF file or directory |
| `-o, --output` | PATH | required | Output directory |
| `-m, --method` | choice | auto | Parsing method: `auto`, `txt`, `ocr` |
| `-b, --backend` | choice | hybrid-auto-engine | Processing backend |
| `-l, --lang` | choice | ch | Language for OCR optimization |
| `-u, --url` | TEXT | - | Server URL for http-client backends |
| `-s, --start` | INTEGER | 0 | Start page (0-indexed) |
| `-e, --end` | INTEGER | - | End page (0-indexed) |
| `-f, --formula` | BOOLEAN | true | Enable formula parsing |
| `-t, --table` | BOOLEAN | true | Enable table parsing |
| `-d, --device` | TEXT | - | Device: cpu, cuda, cuda:0, npu, mps |
| `--vram` | INTEGER | - | GPU memory limit in MB |
| `--source` | choice | huggingface | Model source: huggingface, modelscope, local |

### Parsing Methods
- **auto**: Automatically detect based on PDF content
- **txt**: Extract text directly (for text-based PDFs)
- **ocr**: Use OCR (for scanned/image PDFs)

### Supported Languages
| Code | Language |
|------|----------|
| `en` | English |
| `ch` | Chinese Simplified |
| `ch_server` | Chinese (Server) |
| `ch_lite` | Chinese (Lite) |
| `chinese_cht` | Chinese Traditional |
| `korean` | Korean |
| `japan` | Japanese |
| `arabic` | Arabic |
| `latin` | Latin-based languages |
| `th` | Thai |
| `ta` | Tamil |
| `te` | Telugu |
| `ka` | Georgian |
| `el` | Greek |
| `cyrillic` | Cyrillic languages |
| `devanagari` | Devanagari script |
| `east_slavic` | East Slavic languages |

---

## Python API

### Basic Usage
```python
from mineru.cli.common import do_parse, read_fn
from pathlib import Path

# Read PDF file
pdf_path = Path("./document.pdf")
pdf_bytes = read_fn(pdf_path)

# Parse with default settings
do_parse(
    output_dir="./output",
    pdf_file_names=["document"],
    pdf_bytes_list=[pdf_bytes]
)
```

### Full API Options
```python
do_parse(
    output_dir="./output",                    # Output directory
    pdf_file_names=["document"],              # List of file names
    pdf_bytes_list=[pdf_bytes],               # List of PDF byte contents
    p_lang_list=["en"],                       # Languages per document
    backend="hybrid-auto-engine",             # Processing backend
    parse_method="auto",                      # Parsing method
    formula_enable=True,                      # Enable formula extraction
    table_enable=True,                        # Enable table extraction
    server_url=None,                          # Server URL for http backends
    f_draw_layout_bbox=True,                  # Generate layout visualization
    f_draw_span_bbox=True,                    # Generate span visualization
    f_dump_md=True,                           # Generate Markdown output
    f_dump_middle_json=True,                  # Generate intermediate JSON
    f_dump_model_output=True,                 # Save model output
    f_dump_orig_pdf=True,                     # Save original PDF copy
    f_dump_content_list=True,                 # Generate content list JSON
    f_make_md_mode="MM_MD",                   # Markdown generation mode
    start_page_id=0,                          # Start page (0-indexed)
    end_page_id=None                          # End page (None = all)
)
```

### Output Files Generated
| Flag | File Generated |
|------|----------------|
| `f_dump_md=True` | `{name}.md` |
| `f_dump_content_list=True` | `{name}_content_list.json` |
| `f_dump_middle_json=True` | `{name}_middle.json` |
| `f_dump_model_output=True` | `{name}_model.json` |
| `f_draw_layout_bbox=True` | `{name}_layout.pdf` |
| `f_draw_span_bbox=True` | `{name}_span.pdf` |
| `f_dump_orig_pdf=True` | `{name}_origin.pdf` |

---

## Environment Variables

Configure MinerU behavior with environment variables:

```powershell
# Model source (huggingface, modelscope, local)
$env:MINERU_MODEL_SOURCE = "huggingface"

# Device mode for pipeline backend
$env:MINERU_DEVICE_MODE = "cuda:0"  # or cpu, npu, mps

# VRAM limit in MB
$env:MINERU_VIRTUAL_VRAM_SIZE = "4096"

# Batch size for inference
$env:MINERU_MIN_BATCH_INFERENCE_SIZE = "384"

# Mac MPS fallback
$env:PYTORCH_ENABLE_MPS_FALLBACK = "1"
```

---

## Backend Configuration

### Comparison Table

| Backend | Accuracy | Speed | Resources | Use Case |
|---------|----------|-------|-----------|----------|
| hybrid-auto-engine | Highest | Medium | High GPU | Best quality |
| vlm-auto-engine | High | Slow | Very High GPU | Complex layouts |
| pipeline | Good | Fast | Moderate | General use |
| hybrid-http-client | High | Variable | Low local | Remote server |
| vlm-http-client | High | Variable | Low local | Remote VLM |

### CPU-Only Configuration
```bash
mineru -p doc.pdf -o ./output -b pipeline -d cpu
```

### GPU with VRAM Limit
```bash
mineru -p doc.pdf -o ./output -b pipeline -d cuda:0 --vram 4096
```

---

## Batch Processing

### Process Directory of PDFs
```bash
mineru -p "./pdf_folder/" -o "./output"
```

### Python Batch Processing
```python
from mineru.cli.common import do_parse, read_fn
from pathlib import Path

pdf_dir = Path("./pdfs")
output_dir = "./output"

pdf_files = list(pdf_dir.glob("*.pdf"))
pdf_names = [f.stem for f in pdf_files]
pdf_bytes_list = [read_fn(f) for f in pdf_files]

do_parse(
    output_dir=output_dir,
    pdf_file_names=pdf_names,
    pdf_bytes_list=pdf_bytes_list,
    f_dump_md=True,
    f_dump_content_list=True
)
```

### Parallel Processing with Multiple GPUs
For multi-GPU setups, use the multi_gpu_v2 project from MinerU repository.
