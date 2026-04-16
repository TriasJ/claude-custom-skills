#!/usr/bin/env python3
"""
Extract images from PDF files with rich contextual metadata.

Produces an image_manifest.json optimized for AI agent consumption,
with captions, surrounding text, section titles, bounding boxes, and
optional Claude Vision analysis.

Engines:
  - mineru (default): Uses MinerU's content_list.json + middle.json for rich context
  - pymupdf: Fallback using PyMuPDF for direct image extraction

Usage:
    python extract_images.py <pdf_path> -o <output_dir>
    python extract_images.py paper.pdf -o ./extracted --engine auto
    python extract_images.py paper.pdf -o ./extracted --mineru-output ./mineru_out
    python extract_images.py paper.pdf -o ./extracted --analyze
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Add script directory to path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

from models import (
    ExtractionResult,
    ExtractedImage,
    ImageClassification,
    ImageContext,
    ImageLocation,
    VisionAnalysis,
)

CAPTION_PATTERN = re.compile(
    r"(fig(?:ure)?|exhibit|table|plate|scheme|chart)[\s.:]+(\d+[a-z]?)",
    re.IGNORECASE,
)


def get_temp_dir(pdf_stem: str) -> Path:
    """Get the cross-skill temp directory for this PDF."""
    if platform.system() == "Windows":
        base = Path(os.environ.get("TEMP", os.environ.get("TMP", "/tmp")))
    else:
        base = Path("/tmp")
    return base / "extract-pdf-images" / pdf_stem


def check_mineru_available() -> bool:
    """Check if MinerU CLI is on PATH."""
    return shutil.which("mineru") is not None


def run_mineru(pdf_path: str, output_dir: str, start_page: int = 0,
               end_page: Optional[int] = None) -> Path:
    """Run MinerU on the PDF and return the output directory."""
    cmd = ["mineru", "-p", pdf_path, "-o", output_dir]
    if start_page > 0:
        cmd.extend(["-s", str(start_page)])
    if end_page is not None:
        cmd.extend(["-e", str(end_page)])

    print(f"Running MinerU: {' '.join(cmd)}", file=sys.stderr)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"MinerU stderr: {result.stderr}", file=sys.stderr)
        raise RuntimeError(f"MinerU failed with exit code {result.returncode}")

    # MinerU creates a subdirectory named after the PDF
    pdf_stem = Path(pdf_path).stem
    mineru_out = Path(output_dir) / pdf_stem
    if not mineru_out.exists():
        # Sometimes output is directly in output_dir
        mineru_out = Path(output_dir)
    return mineru_out


def find_mineru_output(mineru_dir: Path) -> Tuple[Optional[Path], Optional[Path], Optional[Path]]:
    """Locate MinerU output files in the given directory.

    Returns (content_list_path, middle_json_path, images_dir).
    """
    content_list = None
    middle_json = None
    images_dir = None

    # Search for content_list.json (may have PDF stem prefix)
    for f in mineru_dir.rglob("*content_list.json"):
        content_list = f
        break

    for f in mineru_dir.rglob("*middle.json"):
        middle_json = f
        break

    # Images directory
    for d in mineru_dir.rglob("images"):
        if d.is_dir():
            images_dir = d
            break

    return content_list, middle_json, images_dir


def extract_from_mineru(
    pdf_path: str,
    mineru_dir: Path,
    output_dir: str,
) -> List[ExtractedImage]:
    """Extract images using MinerU's parsed output for rich context.

    Parses content_list.json as a sequential stream, matching images
    to captions, surrounding text, and section titles.
    """
    content_list_path, middle_json_path, mineru_images_dir = find_mineru_output(mineru_dir)

    if content_list_path is None:
        raise FileNotFoundError(
            f"content_list.json not found in {mineru_dir}. "
            "Run MinerU first or check --mineru-output path."
        )

    with open(content_list_path, "r", encoding="utf-8") as f:
        content_list = json.load(f)

    # Load middle.json for bbox data if available
    middle_data = {}
    if middle_json_path and middle_json_path.exists():
        with open(middle_json_path, "r", encoding="utf-8") as f:
            middle_data = json.load(f)

    # Get page dimensions from middle.json
    page_dims = {}
    if isinstance(middle_data, dict):
        for page_info in middle_data.get("pdf_info", []):
            page_idx = page_info.get("page_idx", 0)
            page_dims[page_idx] = {
                "width": page_info.get("page_size", [0, 0])[0] if isinstance(page_info.get("page_size"), list) else 0,
                "height": page_info.get("page_size", [0, 0])[1] if isinstance(page_info.get("page_size"), list) else 0,
            }

    images_out = Path(output_dir) / "images"
    images_out.mkdir(parents=True, exist_ok=True)
    pdf_stem = Path(pdf_path).stem

    extracted: List[ExtractedImage] = []
    image_counter = 0

    # Build sequential element list with indices for context lookup
    elements = []
    if isinstance(content_list, list):
        elements = content_list
    elif isinstance(content_list, dict) and "content_list" in content_list:
        elements = content_list["content_list"]

    # Track current section title
    current_section = ""

    for idx, elem in enumerate(elements):
        elem_type = elem.get("type", "")

        # Track section titles
        if elem_type in ("title", "heading"):
            current_section = elem.get("text", "").strip()
            continue

        if elem_type != "image":
            continue

        image_counter += 1
        page_idx = elem.get("page_idx", 0)
        img_path_str = elem.get("img_path", "")

        # Resolve image source path
        src_path = None
        if img_path_str:
            # Try relative to content_list.json directory
            candidate = content_list_path.parent / img_path_str
            if candidate.exists():
                src_path = candidate
            elif mineru_images_dir:
                # Try in images directory
                candidate = mineru_images_dir / Path(img_path_str).name
                if candidate.exists():
                    src_path = candidate

        if src_path is None and mineru_images_dir:
            # Fallback: look for any image matching page index
            for f in sorted(mineru_images_dir.iterdir()):
                if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".bmp", ".tiff"):
                    src_path = f
                    break

        if src_path is None:
            continue

        # Copy image to output
        ext = src_path.suffix.lstrip(".").lower()
        if ext == "jpeg":
            ext = "jpg"
        filename = f"{pdf_stem}_p{page_idx + 1}_{image_counter:03d}.{ext}"
        dest_path = images_out / filename
        shutil.copy2(src_path, dest_path)

        # Get dimensions
        width, height, file_size = _get_image_info(dest_path)

        # Context assembly: scan backward/forward for caption and text
        caption, figure_label = _find_caption_in_elements(elements, idx)
        text_before = _get_adjacent_text(elements, idx, direction="before")
        text_after = _get_adjacent_text(elements, idx, direction="after")

        # Bbox from element or middle.json
        bbox = elem.get("bbox", None)
        bbox_norm = None
        if bbox and page_idx in page_dims:
            pw = page_dims[page_idx]["width"]
            ph = page_dims[page_idx]["height"]
            if pw > 0 and ph > 0:
                bbox_norm = [
                    round(bbox[0] / pw, 4),
                    round(bbox[1] / ph, 4),
                    round(bbox[2] / pw, 4),
                    round(bbox[3] / ph, 4),
                ]

        # Classification
        image_type, keywords = _classify_image(caption, figure_label, elem)

        extracted_image = ExtractedImage(
            image_id=f"{pdf_stem}_{image_counter:03d}",
            filename=filename,
            path=f"images/{filename}",
            absolute_path=str(dest_path.resolve()),
            format=ext,
            width=width,
            height=height,
            file_size=file_size,
            location=ImageLocation(
                page_number=page_idx + 1,
                page_index=page_idx,
                bbox=bbox,
                bbox_normalized=bbox_norm,
            ),
            context=ImageContext(
                caption=caption,
                figure_label=figure_label,
                section_title=current_section,
                text_before=text_before,
                text_after=text_after,
            ),
            classification=ImageClassification(
                image_type=image_type,
                keywords=keywords,
                is_decorative=(width < 50 or height < 50),
                has_text_overlay=False,
            ),
        )
        extracted.append(extracted_image)

    return extracted


def _find_caption_in_elements(
    elements: List[Dict], image_idx: int, search_range: int = 3
) -> Tuple[str, str]:
    """Scan elements near an image for caption patterns."""
    caption = ""
    figure_label = ""

    # Search forward first (captions usually follow images)
    for offset in range(1, search_range + 1):
        idx = image_idx + offset
        if idx >= len(elements):
            break
        elem = elements[idx]
        if elem.get("type") == "image":
            break
        text = elem.get("text", "").strip()
        if not text:
            continue
        match = CAPTION_PATTERN.search(text)
        if match:
            caption = text[:500]
            figure_label = match.group(0)
            return caption, figure_label

    # Search backward
    for offset in range(1, search_range + 1):
        idx = image_idx - offset
        if idx < 0:
            break
        elem = elements[idx]
        if elem.get("type") == "image":
            break
        text = elem.get("text", "").strip()
        if not text:
            continue
        match = CAPTION_PATTERN.search(text)
        if match:
            caption = text[:500]
            figure_label = match.group(0)
            return caption, figure_label

    return caption, figure_label


def _get_adjacent_text(
    elements: List[Dict], image_idx: int, direction: str = "before",
    max_blocks: int = 2, max_chars: int = 300
) -> str:
    """Get text from elements adjacent to the image."""
    texts = []
    step = -1 if direction == "before" else 1
    start = image_idx + step

    count = 0
    idx = start
    while 0 <= idx < len(elements) and count < max_blocks:
        elem = elements[idx]
        if elem.get("type") == "image":
            break
        text = elem.get("text", "").strip()
        if text:
            texts.append(text)
            count += 1
        idx += step

    if direction == "before":
        texts.reverse()

    combined = " ".join(texts)
    return combined[:max_chars]


def _classify_image(
    caption: str, figure_label: str, elem: Dict
) -> Tuple[str, List[str]]:
    """Classify image type from caption and element metadata."""
    image_type = "unknown"
    keywords = []
    caption_lower = caption.lower()

    if any(w in caption_lower for w in ("chart", "graph", "plot")):
        image_type = "chart"
    elif any(w in caption_lower for w in ("diagram", "schematic", "schema", "flowchart")):
        image_type = "diagram"
    elif any(w in caption_lower for w in ("photo", "micrograph", "photograph", "microscopy")):
        image_type = "photo"
    elif any(w in caption_lower for w in ("table",)):
        image_type = "table"
    elif figure_label:
        image_type = "figure"

    if figure_label:
        keywords.append(figure_label.lower())

    # Extract keywords from caption
    for word in re.findall(r"\b[A-Za-z]{4,}\b", caption_lower):
        if word not in ("figure", "table", "image", "shows", "this", "that", "with", "from"):
            if word not in keywords:
                keywords.append(word)
                if len(keywords) >= 10:
                    break

    return image_type, keywords


def _get_image_info(path: Path) -> Tuple[int, int, int]:
    """Get image dimensions and file size. Uses Pillow if available."""
    file_size = path.stat().st_size
    width, height = 0, 0

    try:
        from PIL import Image
        with Image.open(path) as img:
            width, height = img.size
    except ImportError:
        pass
    except Exception:
        pass

    return width, height, file_size


def analyze_with_vision(
    images: List[ExtractedImage], api_key: Optional[str] = None
) -> List[ExtractedImage]:
    """Optionally analyze images with Claude Vision for descriptions.

    Requires ANTHROPIC_API_KEY environment variable or --api-key flag.
    """
    key = api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        print("Warning: No Anthropic API key found. Skipping vision analysis.", file=sys.stderr)
        return images

    try:
        import anthropic
    except ImportError:
        print("Warning: anthropic package not installed. Skipping vision analysis.", file=sys.stderr)
        return images

    client = anthropic.Anthropic(api_key=key)

    for img in images:
        if img.classification.is_decorative:
            continue

        img_path = Path(img.absolute_path)
        if not img_path.exists():
            continue

        try:
            import base64
            img_data = base64.standard_b64encode(img_path.read_bytes()).decode("utf-8")
            media_type = f"image/{img.format}"
            if img.format == "jpg":
                media_type = "image/jpeg"

            response = client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": img_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": (
                                "Briefly describe this image in 1-2 sentences. "
                                "If it contains text, list the key text. "
                                "Respond with JSON: {\"description\": \"...\", \"detected_text\": \"...\"}"
                            ),
                        },
                    ],
                }],
            )

            text = response.content[0].text
            try:
                parsed = json.loads(text)
            except json.JSONDecodeError:
                parsed = {"description": text, "detected_text": ""}

            img.vision_analysis = VisionAnalysis(
                description=parsed.get("description", ""),
                detected_text=parsed.get("detected_text", ""),
                model_used="claude-sonnet-4-5-20250929",
                timestamp=datetime.now(timezone.utc).isoformat(),
            )
            print(f"  Analyzed: {img.filename}", file=sys.stderr)

        except Exception as e:
            print(f"  Vision analysis failed for {img.filename}: {e}", file=sys.stderr)

    return images


def get_pdf_page_count(pdf_path: str) -> int:
    """Get total page count of a PDF."""
    try:
        import fitz
        doc = fitz.open(pdf_path)
        count = doc.page_count
        doc.close()
        return count
    except ImportError:
        pass

    try:
        from PIL import Image
        # Can't get page count from Pillow
        pass
    except ImportError:
        pass

    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Extract images from PDFs with rich contextual metadata."
    )
    parser.add_argument("pdf_path", help="Path to the input PDF file")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument(
        "--mineru-output",
        help="Path to existing MinerU output directory (skip re-running MinerU)",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "mineru", "pymupdf"],
        default="auto",
        help="Extraction engine (default: auto-detect)",
    )
    parser.add_argument("--analyze", action="store_true", help="Run Claude Vision analysis")
    parser.add_argument("--api-key", help="Anthropic API key for vision analysis")
    parser.add_argument("--start-page", type=int, default=0, help="Start page (0-indexed)")
    parser.add_argument("--end-page", type=int, default=None, help="End page (0-indexed, inclusive)")

    args = parser.parse_args()

    pdf_path = os.path.abspath(args.pdf_path)
    if not os.path.isfile(pdf_path):
        print(f"Error: PDF not found: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    output_dir = os.path.abspath(args.output)
    os.makedirs(output_dir, exist_ok=True)

    pdf_stem = Path(pdf_path).stem
    timestamp = datetime.now(timezone.utc).isoformat()

    # Engine selection
    engine = args.engine
    if engine == "auto":
        if args.mineru_output:
            engine = "mineru"
        elif check_mineru_available():
            engine = "mineru"
        else:
            engine = "pymupdf"
            print("MinerU not found. Using PyMuPDF fallback.", file=sys.stderr)

    print(f"Engine: {engine}", file=sys.stderr)
    print(f"PDF: {pdf_path}", file=sys.stderr)
    print(f"Output: {output_dir}", file=sys.stderr)

    # Extract images
    images: List[ExtractedImage] = []

    if engine == "mineru":
        if args.mineru_output:
            mineru_dir = Path(args.mineru_output)
        else:
            # Run MinerU, output to temp then copy
            temp_dir = get_temp_dir(pdf_stem)
            mineru_dir = run_mineru(pdf_path, str(temp_dir), args.start_page, args.end_page)

        images = extract_from_mineru(pdf_path, mineru_dir, output_dir)

    elif engine == "pymupdf":
        from pymupdf_extractor import extract_images_pymupdf
        images = extract_images_pymupdf(
            pdf_path, output_dir, args.start_page, args.end_page
        )

    print(f"Extracted {len(images)} images", file=sys.stderr)

    # Enrich with Pillow dimensions (if not already set)
    for img in images:
        if img.width == 0 or img.height == 0:
            abs_path = Path(img.absolute_path)
            if abs_path.exists():
                img.width, img.height, img.file_size = _get_image_info(abs_path)

    # Optional vision analysis
    if args.analyze:
        print("Running Claude Vision analysis...", file=sys.stderr)
        images = analyze_with_vision(images, args.api_key)

    # Get page count
    page_count = get_pdf_page_count(pdf_path)

    # Build result
    result = ExtractionResult(
        version="1.0",
        source_pdf=pdf_path,
        source_pdf_pages=page_count,
        engine=engine,
        extraction_timestamp=timestamp,
        output_directory=output_dir,
        images=images,
    )

    # Write manifest
    manifest_path = Path(output_dir) / "image_manifest.json"
    manifest = result.to_manifest()
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Also write image_sourcer-compatible flat list
    flat_path = Path(output_dir) / "image_library.json"
    flat_list = [img.to_media_item_dict() for img in images]
    with open(flat_path, "w", encoding="utf-8") as f:
        json.dump(flat_list, f, indent=2, ensure_ascii=False)

    # Summary
    summary = result.summary
    print(f"\nExtraction complete:", file=sys.stderr)
    print(f"  Total images: {summary['total_images']}", file=sys.stderr)
    print(f"  Pages with images: {summary['pages_with_images']}", file=sys.stderr)
    print(f"  With captions: {summary['has_captions']}", file=sys.stderr)
    print(f"  Formats: {', '.join(summary['formats']) if summary['formats'] else 'none'}", file=sys.stderr)
    print(f"  Manifest: {manifest_path}", file=sys.stderr)
    print(f"  Library:  {flat_path}", file=sys.stderr)

    # Print manifest path to stdout for scripting
    print(str(manifest_path))


if __name__ == "__main__":
    main()
