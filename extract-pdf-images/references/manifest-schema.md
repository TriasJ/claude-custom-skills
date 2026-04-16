# Image Manifest Schema Reference

The `image_manifest.json` file is the primary output of `extract-pdf-images`. It contains structured metadata for every image extracted from a PDF, optimized for AI agent consumption.

## Top-Level Structure

```json
{
  "version": "1.0",
  "source_pdf": "/absolute/path/to/document.pdf",
  "source_pdf_pages": 42,
  "extraction": {
    "engine": "mineru",
    "timestamp": "2025-01-15T10:30:00+00:00",
    "output_directory": "/absolute/path/to/output"
  },
  "summary": {
    "total_images": 12,
    "pages_with_images": 8,
    "formats": ["png", "jpg"],
    "has_captions": 10,
    "has_vision_analysis": 0
  },
  "images": [ ... ]
}
```

## Per-Image Fields

Each entry in `images[]`:

```json
{
  "image_id": "paper_001",
  "filename": "paper_p1_001.png",
  "path": "images/paper_p1_001.png",
  "absolute_path": "/full/path/to/images/paper_p1_001.png",
  "format": "png",
  "dimensions": { "width": 800, "height": 600 },
  "file_size": 45230,

  "location": {
    "page_number": 1,
    "page_index": 0,
    "bbox": [72.0, 150.0, 540.0, 450.0],
    "bbox_normalized": [0.1, 0.1944, 0.75, 0.5833]
  },

  "context": {
    "caption": "Figure 1. Overview of the proposed architecture.",
    "figure_label": "Figure 1",
    "section_title": "Methods",
    "text_before": "We propose a novel architecture for...",
    "text_after": "As shown in Figure 1, the system consists of..."
  },

  "classification": {
    "image_type": "figure",
    "keywords": ["figure 1", "architecture", "proposed", "novel"],
    "is_decorative": false,
    "has_text_overlay": false
  },

  "vision_analysis": null,

  "integration": {
    "pptx_path": "images/paper_p1_001.png",
    "marp_embed": "![w:600px](images/paper_p1_001.png)"
  }
}
```

## Field Reference

### location

| Field | Type | Description |
|-------|------|-------------|
| `page_number` | int | 1-indexed page number |
| `page_index` | int | 0-indexed page index |
| `bbox` | float[4] | `[x0, y0, x1, y1]` in PDF points (72 pts/inch) |
| `bbox_normalized` | float[4] | `[x0, y0, x1, y1]` normalized to 0.0-1.0 relative to page dimensions |

### context

| Field | Type | Description |
|-------|------|-------------|
| `caption` | string | Full caption text (up to 500 chars) |
| `figure_label` | string | Extracted label like "Figure 3" or "Fig. 2a" |
| `section_title` | string | Nearest heading/title above the image |
| `text_before` | string | 1-2 text blocks before image (up to 300 chars) |
| `text_after` | string | 1-2 text blocks after image (up to 300 chars) |

### classification

| Field | Type | Description |
|-------|------|-------------|
| `image_type` | string | One of: `figure`, `chart`, `diagram`, `photo`, `table`, `decorative`, `unknown` |
| `keywords` | string[] | Extracted keywords from caption (max 10) |
| `is_decorative` | bool | True if image is < 50x50 pixels |
| `has_text_overlay` | bool | True if vision analysis detects text |

### vision_analysis (optional, requires --analyze flag)

| Field | Type | Description |
|-------|------|-------------|
| `description` | string | AI-generated 1-2 sentence description |
| `detected_text` | string | Text detected in the image |
| `model_used` | string | Model used for analysis |
| `timestamp` | string | ISO 8601 timestamp of analysis |

### integration

Pre-computed paths for downstream skills:

| Field | Type | Description |
|-------|------|-------------|
| `pptx_path` | string | Relative path for PowerPoint `add_picture()` |
| `marp_embed` | string | Ready-to-use MARP markdown image embed |

## Companion File: image_library.json

A flat list of images with fields matching `image_sourcer.py` expectations:

```json
[
  {
    "image_id": "paper_001",
    "filename": "paper_p1_001.png",
    "path": "images/paper_p1_001.png",
    "absolute_path": "/full/path/to/images/paper_p1_001.png",
    "file_type": "png",
    "width": 800,
    "height": 600,
    "file_size": 45230,
    "caption": "Figure 1. Overview of the proposed architecture.",
    "document_title": "Methods",
    "context_before": "We propose a novel...",
    "context_after": "As shown in Figure 1...",
    "ocr_text": "",
    "keywords": ["figure 1", "architecture"],
    "source": "pdf_extraction"
  }
]
```

This file is directly loadable by `biomedical-marp-presentations/scripts/image_sourcer.py`.
