#!/usr/bin/env python3
"""
Image Sourcer for Biomedical MARP Presentations

Searches local JSON or CSV image libraries for relevant images based on keywords,
context, and metadata. Returns properly formatted MARP image markdown.

Usage:
    python image_sourcer.py <image_library_file> <search_query> [--max-results N]
    python image_sourcer.py images.json "TMS coil figure-8" --max-results 3
"""

import json
import csv
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
from difflib import SequenceMatcher


def load_image_library(filepath: str) -> List[Dict[str, Any]]:
    """Load image library from JSON or CSV file."""
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Image library not found: {filepath}")
    
    if path.suffix.lower() == '.json':
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    elif path.suffix.lower() == '.csv':
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}. Use .json or .csv")


def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""
    return text.lower().strip()


def calculate_relevance_score(image: Dict[str, Any], query_terms: List[str]) -> float:
    """
    Calculate relevance score for an image based on query terms.
    
    Scoring:
    - Exact keyword match: +10 points per term
    - Partial keyword match: +5 points per term
    - Title match: +8 points per term
    - Caption match: +6 points per term
    - Context match: +3 points per term
    - Document title match: +4 points per term
    """
    score = 0.0
    
    # Extract searchable fields
    keywords = [normalize_text(k) for k in image.get('keywords', [])]
    title = normalize_text(image.get('document_title', ''))
    caption = normalize_text(image.get('caption', ''))
    context = normalize_text(image.get('context_before', '') + ' ' + image.get('context_after', ''))
    ocr_text = normalize_text(image.get('ocr_text', ''))
    
    for term in query_terms:
        term_lower = normalize_text(term)
        
        # Exact keyword match
        if term_lower in keywords:
            score += 10
        
        # Partial keyword match
        elif any(term_lower in kw or kw in term_lower for kw in keywords):
            score += 5
        
        # Title matches
        if term_lower in title:
            score += 8
        
        # Caption matches
        if term_lower in caption:
            score += 6
        
        # Context matches
        if term_lower in context:
            score += 3
        
        # OCR text matches
        if term_lower in ocr_text:
            score += 4
    
    return score


def search_images(library: List[Dict[str, Any]], query: str, max_results: int = 5) -> List[Dict[str, Any]]:
    """Search image library and return top matches."""
    
    # Split query into terms
    query_terms = [term.strip() for term in query.split() if term.strip()]
    
    # Calculate scores for all images
    scored_images = []
    for image in library:
        score = calculate_relevance_score(image, query_terms)
        if score > 0:  # Only include images with some relevance
            scored_images.append((score, image))
    
    # Sort by score (descending) and return top results
    scored_images.sort(key=lambda x: x[0], reverse=True)
    
    return [img for score, img in scored_images[:max_results]]


def format_marp_image(image: Dict[str, Any], width: int = 600) -> str:
    """Format image data as MARP markdown."""
    
    path = image.get('path', '')
    caption = image.get('caption', '')
    document_title = image.get('document_title', '')
    
    # Build MARP image markdown
    marp_output = f"![w:{width}px]({path})\n\n"
    
    # Add caption if available
    if caption:
        marp_output += '<div style="font-size: 16px; text-align: center; color: #666; margin-top: 10px;">\n\n'
        marp_output += f'{caption}\n'
        if document_title:
            marp_output += f'*Source*: {document_title}\n'
        marp_output += '\n</div>'
    
    return marp_output


def main():
    parser = argparse.ArgumentParser(
        description='Search image library for biomedical presentation images'
    )
    parser.add_argument('library', help='Path to image library (JSON or CSV)')
    parser.add_argument('query', help='Search query (keywords)')
    parser.add_argument('--max-results', '-n', type=int, default=5,
                       help='Maximum number of results (default: 5)')
    parser.add_argument('--width', '-w', type=int, default=600,
                       help='Image width in pixels for MARP (default: 600)')
    parser.add_argument('--json', action='store_true',
                       help='Output results as JSON instead of MARP markdown')
    
    args = parser.parse_args()
    
    try:
        # Load library
        print(f"Loading image library from {args.library}...", file=sys.stderr)
        library = load_image_library(args.library)
        print(f"Loaded {len(library)} images", file=sys.stderr)
        
        # Search
        print(f"Searching for: {args.query}", file=sys.stderr)
        results = search_images(library, args.query, args.max_results)
        print(f"Found {len(results)} matching images", file=sys.stderr)
        
        if not results:
            print("\nNo matching images found.", file=sys.stderr)
            sys.exit(1)
        
        # Output results
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print("\n" + "="*80)
            print("MATCHING IMAGES")
            print("="*80 + "\n")
            
            for i, image in enumerate(results, 1):
                print(f"--- Result {i} ---")
                print(f"Image ID: {image.get('image_id', 'N/A')}")
                print(f"Filename: {image.get('filename', 'N/A')}")
                print(f"Source: {image.get('document_title', 'N/A')}")
                print(f"Keywords: {', '.join(image.get('keywords', []))}")
                print(f"\nMARP Markdown:\n")
                print(format_marp_image(image, args.width))
                print()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
