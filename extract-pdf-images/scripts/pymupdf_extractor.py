"""PyMuPDF-based fallback image extractor.

Used when MinerU is not installed. Extracts embedded images from PDFs
with basic contextual metadata (bounding boxes, nearby text, caption detection).
"""

import re
import os
from pathlib import Path
from typing import List, Optional, Tuple

try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None

from models import (
    ExtractedImage,
    ImageLocation,
    ImageContext,
    ImageClassification,
)

# Pattern for detecting figure captions
CAPTION_PATTERN = re.compile(
    r"^(fig(?:ure)?|exhibit|table|plate|scheme|chart|image|photo)[\s.:]+(\d+[a-z]?)",
    re.IGNORECASE,
)


def check_pymupdf_available() -> bool:
    """Check if PyMuPDF is installed and importable."""
    return fitz is not None


def _find_caption_in_blocks(
    blocks: List, img_bbox: fitz.Rect, page_height: float
) -> Tuple[str, str]:
    """Find caption text near an image by proximity.

    Searches text blocks below (and slightly above) the image bbox
    for caption-like patterns.

    Returns (caption, figure_label).
    """
    caption = ""
    figure_label = ""
    best_distance = float("inf")

    for block in blocks:
        if block[6] != 0:  # Not a text block
            continue

        block_text = block[4].strip()
        if not block_text:
            continue

        # Block bbox: (x0, y0, x1, y1)
        block_y0 = block[1]
        block_y1 = block[3]

        # Check if block is below the image (within 100pt)
        distance_below = block_y0 - img_bbox.y1
        # Check if block is above the image (within 50pt)
        distance_above = img_bbox.y0 - block_y1

        if 0 <= distance_below <= 100:
            distance = distance_below
        elif 0 <= distance_above <= 50:
            distance = distance_above + 200  # Penalize above-image captions
        else:
            continue

        match = CAPTION_PATTERN.match(block_text)
        if match and distance < best_distance:
            best_distance = distance
            caption = block_text[:500]  # Limit length
            figure_label = match.group(0)

    return caption, figure_label


def _get_surrounding_text(
    blocks: List, img_bbox: fitz.Rect, max_chars: int = 300
) -> Tuple[str, str]:
    """Get text blocks immediately before and after the image."""
    text_blocks = [
        (b[1], b[4].strip()) for b in blocks if b[6] == 0 and b[4].strip()
    ]
    text_blocks.sort(key=lambda x: x[0])  # Sort by y-position

    text_before = ""
    text_after = ""

    for y_pos, text in text_blocks:
        if y_pos < img_bbox.y0:
            text_before = text[:max_chars]
        elif y_pos > img_bbox.y1 and not text_after:
            text_after = text[:max_chars]
            break

    return text_before, text_after


def extract_images_pymupdf(
    pdf_path: str,
    output_dir: str,
    start_page: int = 0,
    end_page: Optional[int] = None,
) -> List[ExtractedImage]:
    """Extract images from a PDF using PyMuPDF.

    Args:
        pdf_path: Path to the input PDF file.
        output_dir: Directory to save extracted images.
        start_page: First page to process (0-indexed).
        end_page: Last page to process (0-indexed, inclusive). None = all pages.

    Returns:
        List of ExtractedImage objects with metadata.
    """
    if not check_pymupdf_available():
        raise ImportError(
            "PyMuPDF (fitz) is not installed. Install with: pip install PyMuPDF"
        )

    doc = fitz.open(pdf_path)
    images_dir = Path(output_dir) / "images"
    images_dir.mkdir(parents=True, exist_ok=True)

    pdf_stem = Path(pdf_path).stem
    extracted: List[ExtractedImage] = []
    image_counter = 0

    if end_page is None:
        end_page = doc.page_count - 1
    end_page = min(end_page, doc.page_count - 1)

    for page_idx in range(start_page, end_page + 1):
        page = doc[page_idx]
        page_width = page.rect.width
        page_height = page.rect.height
        blocks = page.get_text("blocks")

        image_list = page.get_images(full=True)

        for img_index, img_info in enumerate(image_list):
            xref = img_info[0]

            try:
                base_image = doc.extract_image(xref)
            except Exception:
                continue

            if not base_image:
                continue

            img_bytes = base_image["image"]
            img_ext = base_image.get("ext", "png")
            if img_ext == "jpeg":
                img_ext = "jpg"

            # Skip tiny images (likely decorative)
            img_width = base_image.get("width", 0)
            img_height = base_image.get("height", 0)
            is_decorative = img_width < 50 or img_height < 50

            # Get bounding box on the page
            try:
                rects = page.get_image_rects(xref)
                if rects:
                    img_rect = rects[0]
                else:
                    img_rect = fitz.Rect(0, 0, img_width, img_height)
            except Exception:
                img_rect = fitz.Rect(0, 0, img_width, img_height)

            # Generate filename and save
            image_counter += 1
            filename = f"{pdf_stem}_p{page_idx + 1}_{image_counter:03d}.{img_ext}"
            img_path = images_dir / filename
            img_path.write_bytes(img_bytes)

            # Build context
            caption, figure_label = _find_caption_in_blocks(
                blocks, img_rect, page_height
            )
            text_before, text_after = _get_surrounding_text(blocks, img_rect)

            bbox = [img_rect.x0, img_rect.y0, img_rect.x1, img_rect.y1]
            bbox_norm = None
            if page_width > 0 and page_height > 0:
                bbox_norm = [
                    round(img_rect.x0 / page_width, 4),
                    round(img_rect.y0 / page_height, 4),
                    round(img_rect.x1 / page_width, 4),
                    round(img_rect.y1 / page_height, 4),
                ]

            # Classify by caption keywords
            image_type = "unknown"
            caption_lower = caption.lower()
            if any(w in caption_lower for w in ("chart", "graph", "plot")):
                image_type = "chart"
            elif any(w in caption_lower for w in ("diagram", "schematic", "schema")):
                image_type = "diagram"
            elif any(w in caption_lower for w in ("photo", "micrograph", "photograph")):
                image_type = "photo"
            elif any(w in caption_lower for w in ("table",)):
                image_type = "table"
            elif figure_label:
                image_type = "figure"

            keywords = []
            if figure_label:
                keywords.append(figure_label.lower())

            extracted_image = ExtractedImage(
                image_id=f"{pdf_stem}_{image_counter:03d}",
                filename=filename,
                path=f"images/{filename}",
                absolute_path=str(img_path.resolve()),
                format=img_ext,
                width=img_width,
                height=img_height,
                file_size=len(img_bytes),
                location=ImageLocation(
                    page_number=page_idx + 1,
                    page_index=page_idx,
                    bbox=bbox,
                    bbox_normalized=bbox_norm,
                ),
                context=ImageContext(
                    caption=caption,
                    figure_label=figure_label,
                    section_title="",  # PyMuPDF doesn't have layout analysis for sections
                    text_before=text_before,
                    text_after=text_after,
                ),
                classification=ImageClassification(
                    image_type=image_type,
                    keywords=keywords,
                    is_decorative=is_decorative,
                    has_text_overlay=False,
                ),
            )
            extracted.append(extracted_image)

    doc.close()
    return extracted
