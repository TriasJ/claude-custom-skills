"""Data models for PDF image extraction manifest."""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class ImageLocation:
    """Where the image appears in the PDF."""

    page_number: int  # 1-indexed page number
    page_index: int  # 0-indexed page index
    bbox: Optional[List[float]] = None  # [x0, y0, x1, y1] in PDF points
    bbox_normalized: Optional[List[float]] = None  # [x0, y0, x1, y1] normalized 0-1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_number": self.page_number,
            "page_index": self.page_index,
            "bbox": self.bbox,
            "bbox_normalized": self.bbox_normalized,
        }


@dataclass
class ImageContext:
    """Contextual metadata extracted from surrounding PDF content."""

    caption: str = ""
    figure_label: str = ""  # e.g. "Figure 3", "Fig. 2a"
    section_title: str = ""
    text_before: str = ""  # 1-2 blocks of text preceding the image
    text_after: str = ""  # 1-2 blocks of text following the image

    def to_dict(self) -> Dict[str, Any]:
        return {
            "caption": self.caption,
            "figure_label": self.figure_label,
            "section_title": self.section_title,
            "text_before": self.text_before,
            "text_after": self.text_after,
        }


@dataclass
class ImageClassification:
    """Classification metadata for the image."""

    image_type: str = "unknown"  # figure, chart, photo, diagram, table, decorative
    keywords: List[str] = field(default_factory=list)
    is_decorative: bool = False
    has_text_overlay: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "image_type": self.image_type,
            "keywords": self.keywords,
            "is_decorative": self.is_decorative,
            "has_text_overlay": self.has_text_overlay,
        }


@dataclass
class VisionAnalysis:
    """Optional AI vision analysis results."""

    description: str = ""
    detected_text: str = ""
    model_used: str = ""
    timestamp: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "detected_text": self.detected_text,
            "model_used": self.model_used,
            "timestamp": self.timestamp,
        }


@dataclass
class ExtractedImage:
    """A single image extracted from a PDF with full metadata."""

    image_id: str
    filename: str
    path: str  # Relative path from output directory
    absolute_path: str
    format: str  # png, jpg, etc.
    width: int = 0
    height: int = 0
    file_size: int = 0
    location: ImageLocation = field(default_factory=lambda: ImageLocation(1, 0))
    context: ImageContext = field(default_factory=ImageContext)
    classification: ImageClassification = field(default_factory=ImageClassification)
    vision_analysis: Optional[VisionAnalysis] = None

    def to_dict(self) -> Dict[str, Any]:
        """Full manifest dict with all metadata."""
        result = {
            "image_id": self.image_id,
            "filename": self.filename,
            "path": self.path,
            "absolute_path": self.absolute_path,
            "format": self.format,
            "dimensions": {"width": self.width, "height": self.height},
            "file_size": self.file_size,
            "location": self.location.to_dict(),
            "context": self.context.to_dict(),
            "classification": self.classification.to_dict(),
            "vision_analysis": (
                self.vision_analysis.to_dict() if self.vision_analysis else None
            ),
            "integration": {
                "pptx_path": self.path,
                "marp_embed": f"![w:600px]({self.path})",
            },
        }
        return result

    def to_media_item_dict(self) -> Dict[str, Any]:
        """Compatibility dict matching fetch-media MediaItem + image_sourcer fields."""
        return {
            "image_id": self.image_id,
            "filename": self.filename,
            "path": self.path,
            "absolute_path": self.absolute_path,
            "file_type": self.format,
            "width": self.width,
            "height": self.height,
            "file_size": self.file_size,
            "caption": self.context.caption,
            "document_title": self.context.section_title,
            "context_before": self.context.text_before,
            "context_after": self.context.text_after,
            "ocr_text": (
                self.vision_analysis.detected_text
                if self.vision_analysis
                else ""
            ),
            "keywords": self.classification.keywords,
            "source": "pdf_extraction",
        }


@dataclass
class ExtractionResult:
    """Complete result of a PDF image extraction run."""

    version: str = "1.0"
    source_pdf: str = ""
    source_pdf_pages: int = 0
    engine: str = ""  # "mineru" or "pymupdf"
    extraction_timestamp: str = ""
    output_directory: str = ""
    images: List[ExtractedImage] = field(default_factory=list)

    @property
    def summary(self) -> Dict[str, Any]:
        return {
            "total_images": len(self.images),
            "pages_with_images": len(
                set(img.location.page_number for img in self.images)
            ),
            "formats": list(set(img.format for img in self.images)),
            "has_captions": sum(1 for img in self.images if img.context.caption),
            "has_vision_analysis": sum(
                1 for img in self.images if img.vision_analysis
            ),
        }

    def to_manifest(self) -> Dict[str, Any]:
        """Generate the full image_manifest.json structure."""
        return {
            "version": self.version,
            "source_pdf": self.source_pdf,
            "source_pdf_pages": self.source_pdf_pages,
            "extraction": {
                "engine": self.engine,
                "timestamp": self.extraction_timestamp,
                "output_directory": self.output_directory,
            },
            "summary": self.summary,
            "images": [img.to_dict() for img in self.images],
        }
