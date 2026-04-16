#!/usr/bin/env python3
"""
Enhanced Open-i Biomedical Image Retrieval Service

Advanced image search using NCBI Open-i API with filtering by:
- Image modality (CT, MRI, X-ray, microscopy, etc.)
- Clinical specialty
- Image type (diagnostic, illustration, chart)
- Collection (PMC, clinical images, etc.)

Based on Open-i API documentation: https://openi.nlm.nih.gov/services

Usage:
    python openi_advanced_search.py --query "brain MRI glioblastoma" --modality MRI --max-results 10
    python openi_advanced_search.py --query "TMS coil" --image-type illustration --output ./images

Requirements:
    pip install requests --break-system-packages
"""

import json
import time
import requests
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from urllib.parse import quote


@dataclass
class OpenIImage:
    """Structured representation of an Open-i image result."""
    uid: str
    title: str
    caption: str
    abstract: str
    image_url: str
    thumbnail_url: str
    pmcid: str
    article_title: str
    journal: str
    year: str
    authors: str
    image_type: str
    modality: str
    collection: str
    mesh_terms: List[str]


class OpenIAdvancedSearch:
    """Advanced Open-i biomedical image search with filtering."""
    
    # Open-i API endpoints
    BASE_URL = "https://openi.nlm.nih.gov/api/search"
    
    # Image modalities supported by Open-i
    MODALITIES = {
        'ct': 'CT Scan',
        'mri': 'MRI',
        'xray': 'X-Ray',
        'ultrasound': 'Ultrasound',
        'pet': 'PET Scan',
        'microscopy': 'Microscopy',
        'photograph': 'Clinical Photograph',
        'illustration': 'Illustration/Diagram',
        'graph': 'Graph/Chart'
    }
    
    # Clinical specialties
    SPECIALTIES = {
        'cardiology': 'Cardiology',
        'neurology': 'Neurology',
        'oncology': 'Oncology',
        'psychiatry': 'Psychiatry',
        'radiology': 'Radiology',
        'surgery': 'Surgery',
        'pathology': 'Pathology',
        'dermatology': 'Dermatology'
    }
    
    # Collections
    COLLECTIONS = {
        'pmc': 'PubMed Central',
        'clinical': 'Clinical Images',
        'medpix': 'MedPix',
        'indiana': 'Indiana Network'
    }
    
    def __init__(self, output_dir: str = './openi_images'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BiomedicalMARPPresentations/1.0 (Educational Use)'
        })
    
    def build_query(
        self,
        query: str,
        modality: Optional[str] = None,
        specialty: Optional[str] = None,
        image_type: Optional[str] = None,
        collection: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None
    ) -> str:
        """Build advanced Open-i query string with filters."""
        
        query_parts = [query]
        
        # Add modality filter
        if modality and modality.lower() in self.MODALITIES:
            query_parts.append(f'modality:"{modality}"')
        
        # Add specialty filter
        if specialty and specialty.lower() in self.SPECIALTIES:
            query_parts.append(f'specialty:"{specialty}"')
        
        # Add image type filter
        if image_type:
            query_parts.append(f'imgType:"{image_type}"')
        
        # Add collection filter
        if collection and collection.lower() in self.COLLECTIONS:
            query_parts.append(f'collection:"{collection}"')
        
        # Add date range
        if year_from or year_to:
            year_from = year_from or 1900
            year_to = year_to or 2100
            query_parts.append(f'pubYear:[{year_from} TO {year_to}]')
        
        return ' AND '.join(query_parts)
    
    def search(
        self,
        query: str,
        max_results: int = 20,
        modality: Optional[str] = None,
        specialty: Optional[str] = None,
        image_type: Optional[str] = None,
        collection: Optional[str] = None,
        year_from: Optional[int] = None,
        year_to: Optional[int] = None,
        sort_by: str = 'relevance'
    ) -> List[OpenIImage]:
        """
        Search Open-i with advanced filters.
        
        Args:
            query: Search query string
            max_results: Maximum number of results (default: 20)
            modality: Image modality (ct, mri, xray, etc.)
            specialty: Clinical specialty
            image_type: Type of image (diagnostic, illustration, etc.)
            collection: Source collection (pmc, clinical, etc.)
            year_from: Start year for date range
            year_to: End year for date range
            sort_by: Sort order ('relevance' or 'date')
        
        Returns:
            List of OpenIImage objects
        """
        
        # Build query with filters
        full_query = self.build_query(
            query, modality, specialty, image_type, 
            collection, year_from, year_to
        )
        
        print(f"Searching Open-i: {full_query}")
        print(f"  Filters applied:")
        if modality:
            print(f"    Modality: {self.MODALITIES.get(modality.lower(), modality)}")
        if specialty:
            print(f"    Specialty: {self.SPECIALTIES.get(specialty.lower(), specialty)}")
        if image_type:
            print(f"    Image Type: {image_type}")
        if collection:
            print(f"    Collection: {self.COLLECTIONS.get(collection.lower(), collection)}")
        
        params = {
            'query': full_query,
            'rows': min(max_results, 100),  # API limit
            'start': 0,
            'sort': sort_by
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            images = self._parse_results(data)
            
            print(f"  Found {len(images)} images\n")
            return images[:max_results]
            
        except requests.exceptions.RequestException as e:
            print(f"  Error searching Open-i: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"  Error parsing response: {e}")
            return []
    
    def _parse_results(self, data: Dict) -> List[OpenIImage]:
        """Parse Open-i API response into structured objects."""
        images = []
        
        # Handle different response formats
        docs = data.get('list', [])
        if not docs:
            docs = data.get('response', {}).get('docs', [])
        
        for doc in docs:
            try:
                image = OpenIImage(
                    uid=doc.get('id', doc.get('uid', '')),
                    title=doc.get('title', doc.get('imgCaption', '')),
                    caption=doc.get('imgCaption', doc.get('caption', '')),
                    abstract=doc.get('abstract', '')[:500],  # Truncate
                    image_url=doc.get('imgLarge', doc.get('image_url', '')),
                    thumbnail_url=doc.get('imgThumb', doc.get('thumbnail', '')),
                    pmcid=doc.get('pmcid', ''),
                    article_title=doc.get('articleTitle', doc.get('article', '')),
                    journal=doc.get('journal', ''),
                    year=str(doc.get('year', doc.get('pubYear', ''))),
                    authors=doc.get('authors', ''),
                    image_type=doc.get('imgType', ''),
                    modality=doc.get('modality', ''),
                    collection=doc.get('collection', ''),
                    mesh_terms=doc.get('meshTerms', [])
                )
                images.append(image)
            except Exception as e:
                print(f"    Warning: Skipping malformed result: {e}")
                continue
        
        return images
    
    def download_image(self, image: OpenIImage, use_thumbnail: bool = False) -> Optional[Path]:
        """Download image to output directory."""
        
        url = image.thumbnail_url if use_thumbnail else image.image_url
        if not url:
            print(f"    No URL for image: {image.uid}")
            return None
        
        # Create safe filename
        safe_id = image.uid.replace('/', '_').replace(':', '_')
        ext = '.jpg'  # Open-i typically serves JPG
        filename = f"openi_{safe_id}{ext}"
        filepath = self.output_dir / filename
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
            
        except Exception as e:
            print(f"    Error downloading {filename}: {e}")
            return None
    
    def download_batch(
        self,
        images: List[OpenIImage],
        use_thumbnail: bool = False,
        delay: float = 0.5
    ) -> List[Path]:
        """Download multiple images with rate limiting."""
        
        print(f"Downloading {len(images)} images...")
        filepaths = []
        
        for i, image in enumerate(images, 1):
            print(f"  [{i}/{len(images)}] {image.title[:60]}...")
            
            filepath = self.download_image(image, use_thumbnail)
            if filepath:
                filepaths.append(filepath)
                print(f"    Saved: {filepath.name}")
            
            time.sleep(delay)  # Rate limiting
        
        print(f"\n✅ Downloaded {len(filepaths)}/{len(images)} images")
        return filepaths
    
    def create_image_library(self, images: List[OpenIImage]) -> List[Dict]:
        """Create image library JSON compatible with the skill."""
        
        library = []
        for image in images:
            safe_id = image.uid.replace('/', '_').replace(':', '_')
            filename = f"openi_{safe_id}.jpg"
            filepath = self.output_dir / filename
            
            entry = {
                'image_id': image.uid,
                'filename': filename,
                'path': str(filepath.absolute()),
                'source_document': f"{image.pmcid}.pdf" if image.pmcid else '',
                'source_path': '',
                'source_page': 0,
                'document_title': image.article_title,
                'caption': image.caption,
                'alt_text': image.title,
                'context_before': image.abstract[:200],
                'context_after': '',
                'section': '',
                'image_type': image.image_type or 'figure',
                'keywords': image.mesh_terms,
                'ocr_text': '',
                'dimensions': '',
                'extracted_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
                'modality': image.modality,
                'specialty': '',
                'collection': image.collection,
                'journal': image.journal,
                'year': image.year,
                'markdown_embed': f"![{image.title}]({filepath.absolute()})"
            }
            library.append(entry)
        
        return library
    
    def export_metadata(self, images: List[OpenIImage], format: str = 'json') -> str:
        """Export search results metadata."""
        
        metadata_file = self.output_dir / f'openi_metadata.{format}'
        
        if format == 'json':
            with open(metadata_file, 'w') as f:
                json.dump([asdict(img) for img in images], f, indent=2)
        elif format == 'csv':
            import csv
            with open(metadata_file, 'w', newline='') as f:
                if images:
                    writer = csv.DictWriter(f, fieldnames=asdict(images[0]).keys())
                    writer.writeheader()
                    for img in images:
                        writer.writerow(asdict(img))
        
        return str(metadata_file)


def print_results_summary(images: List[OpenIImage]):
    """Print formatted summary of search results."""
    
    print("\n" + "="*80)
    print("SEARCH RESULTS")
    print("="*80 + "\n")
    
    for i, img in enumerate(images, 1):
        print(f"{i}. {img.title}")
        print(f"   Article: {img.article_title}")
        print(f"   Journal: {img.journal} ({img.year})")
        if img.modality:
            print(f"   Modality: {img.modality}")
        if img.image_type:
            print(f"   Type: {img.image_type}")
        print(f"   PMCID: {img.pmcid}")
        print(f"   Caption: {img.caption[:100]}...")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Advanced Open-i biomedical image search with filters'
    )
    
    # Search parameters
    parser.add_argument('--query', '-q', required=True,
                       help='Search query')
    parser.add_argument('--max-results', '-n', type=int, default=20,
                       help='Maximum results (default: 20)')
    
    # Filters
    parser.add_argument('--modality', '-m',
                       choices=list(OpenIAdvancedSearch.MODALITIES.keys()),
                       help='Image modality filter')
    parser.add_argument('--specialty', '-s',
                       choices=list(OpenIAdvancedSearch.SPECIALTIES.keys()),
                       help='Clinical specialty filter')
    parser.add_argument('--image-type', '-t',
                       help='Image type (diagnostic, illustration, etc.)')
    parser.add_argument('--collection', '-c',
                       choices=list(OpenIAdvancedSearch.COLLECTIONS.keys()),
                       help='Collection filter')
    parser.add_argument('--year-from', type=int,
                       help='Start year for date range')
    parser.add_argument('--year-to', type=int,
                       help='End year for date range')
    
    # Output options
    parser.add_argument('--output', '-o', default='./openi_images',
                       help='Output directory (default: ./openi_images)')
    parser.add_argument('--download', action='store_true',
                       help='Download images')
    parser.add_argument('--thumbnail', action='store_true',
                       help='Download thumbnails instead of full images')
    parser.add_argument('--create-library', action='store_true',
                       help='Create image_library.json file')
    parser.add_argument('--export-metadata', choices=['json', 'csv'],
                       help='Export metadata in specified format')
    parser.add_argument('--sort', choices=['relevance', 'date'], default='relevance',
                       help='Sort results by relevance or date')
    
    # List options
    parser.add_argument('--list-modalities', action='store_true',
                       help='List available modalities and exit')
    parser.add_argument('--list-specialties', action='store_true',
                       help='List available specialties and exit')
    
    args = parser.parse_args()
    
    # Handle list commands
    if args.list_modalities:
        print("\nAvailable Modalities:")
        for key, name in OpenIAdvancedSearch.MODALITIES.items():
            print(f"  {key:15} - {name}")
        return
    
    if args.list_specialties:
        print("\nAvailable Specialties:")
        for key, name in OpenIAdvancedSearch.SPECIALTIES.items():
            print(f"  {key:15} - {name}")
        return
    
    # Perform search
    searcher = OpenIAdvancedSearch(args.output)
    
    images = searcher.search(
        query=args.query,
        max_results=args.max_results,
        modality=args.modality,
        specialty=args.specialty,
        image_type=args.image_type,
        collection=args.collection,
        year_from=args.year_from,
        year_to=args.year_to,
        sort_by=args.sort
    )
    
    if not images:
        print("No images found.")
        return
    
    # Print results
    print_results_summary(images)
    
    # Download images
    if args.download:
        searcher.download_batch(images, use_thumbnail=args.thumbnail)
    
    # Create library
    if args.create_library:
        library = searcher.create_image_library(images)
        library_path = Path(args.output) / 'image_library.json'
        
        with open(library_path, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n✅ Created image library: {library_path}")
        print(f"   Total images: {len(library)}")
    
    # Export metadata
    if args.export_metadata:
        metadata_path = searcher.export_metadata(images, args.export_metadata)
        print(f"\n✅ Exported metadata: {metadata_path}")


if __name__ == '__main__':
    main()
