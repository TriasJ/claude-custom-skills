#!/usr/bin/env python3
"""
PMC Image Fetcher for Biomedical Presentations

Fetches figures and images from PubMed Central (PMC) articles and NCBI Open-I
using their public APIs. Inspired by PMC-figure-downloader.

Usage:
    # Search PMC for articles and download figures
    python pmc_image_fetcher.py --search "transcranial magnetic stimulation" --max-articles 5 --output ./images
    
    # Fetch specific PMC article figures
    python pmc_image_fetcher.py --pmcid PMC1234567 --output ./images
    
    # Search NCBI Open-I directly
    python pmc_image_fetcher.py --openi "brain fMRI depression" --max-results 10 --output ./images

Requirements:
    pip install requests --break-system-packages
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import quote


class PMCImageFetcher:
    """Fetch images from PubMed Central and NCBI Open-I."""
    
    def __init__(self, output_dir: str = './images'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BiomedicalMARPPresentations/1.0 (Educational Use)'
        })
        
        # API endpoints
        self.eutils_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.openi_base = 'https://openi.nlm.nih.gov/api/search'
        self.pmc_image_base = 'https://www.ncbi.nlm.nih.gov/pmc/articles/'
    
    def search_pmc(self, query: str, max_results: int = 10) -> List[str]:
        """Search PMC and return PMCIDs."""
        print(f"Searching PMC for: {query}")
        
        url = f"{self.eutils_base}esearch.fcgi"
        params = {
            'db': 'pmc',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        pmcids = data.get('esearchresult', {}).get('idlist', [])
        
        print(f"Found {len(pmcids)} articles")
        return [f"PMC{pmcid}" if not pmcid.startswith('PMC') else pmcid for pmcid in pmcids]
    
    def get_pmc_metadata(self, pmcid: str) -> Dict:
        """Get article metadata from PMC."""
        print(f"Fetching metadata for {pmcid}")
        
        # Convert PMCID to numeric ID
        numeric_id = pmcid.replace('PMC', '')
        
        url = f"{self.eutils_base}esummary.fcgi"
        params = {
            'db': 'pmc',
            'id': numeric_id,
            'retmode': 'json'
        }
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        result = data.get('result', {}).get(numeric_id, {})
        
        return {
            'pmcid': pmcid,
            'title': result.get('title', ''),
            'authors': result.get('authors', []),
            'journal': result.get('fulljournalname', ''),
            'pubdate': result.get('pubdate', '')
        }
    
    def fetch_pmc_figures(self, pmcid: str) -> List[Dict]:
        """
        Fetch figure information from a PMC article.
        Note: This is a simplified version. Full implementation would parse
        the article XML/HTML to extract figure URLs and captions.
        """
        print(f"Fetching figures from {pmcid}")
        
        # Get article metadata
        metadata = self.get_pmc_metadata(pmcid)
        
        # In a full implementation, we would:
        # 1. Fetch the article XML from PMC FTP or OA service
        # 2. Parse the XML to extract figure elements
        # 3. Get figure URLs, captions, and labels
        
        # For now, return a structure showing what would be available
        return [{
            'pmcid': pmcid,
            'metadata': metadata,
            'note': 'Full figure extraction requires XML parsing - see PMC OA Service'
        }]
    
    def search_openi(self, query: str, max_results: int = 10) -> List[Dict]:
        """Search NCBI Open-I for medical images."""
        print(f"Searching NCBI Open-I for: {query}")
        
        params = {
            'query': query,
            'rows': max_results
        }
        
        try:
            response = self.session.get(self.openi_base, params=params)
            response.raise_for_status()
            
            data = response.json()
            images = []
            
            for item in data.get('list', []):
                image_info = {
                    'id': item.get('imgLarge', '').split('/')[-1],
                    'title': item.get('imgCaption', ''),
                    'url': item.get('imgLarge', ''),
                    'thumbnail_url': item.get('imgThumb', ''),
                    'pmcid': item.get('pmcid', ''),
                    'abstract': item.get('abstract', ''),
                    'article_title': item.get('articleTitle', ''),
                    'journal': item.get('journal', ''),
                    'year': item.get('year', '')
                }
                images.append(image_info)
            
            print(f"Found {len(images)} images from Open-I")
            return images
        
        except Exception as e:
            print(f"Error searching Open-I: {e}")
            return []
    
    def download_image(self, url: str, filename: str) -> Optional[Path]:
        """Download an image from URL."""
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            filepath = self.output_dir / filename
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Downloaded: {filename}")
            return filepath
        
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            return None
    
    def create_image_library_entry(self, image_info: Dict, filepath: Path) -> Dict:
        """Create an entry for the image library JSON."""
        return {
            'image_id': image_info.get('id', ''),
            'filename': filepath.name,
            'path': str(filepath.absolute()),
            'source_document': f"{image_info.get('pmcid', 'N/A')}.pdf",
            'source_path': '',
            'source_page': 0,
            'document_title': image_info.get('article_title', ''),
            'caption': image_info.get('title', ''),
            'alt_text': '',
            'context_before': image_info.get('abstract', '')[:200],
            'context_after': '',
            'section': 'Figure',
            'image_type': 'figure',
            'keywords': [],
            'ocr_text': '',
            'dimensions': '',
            'extracted_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'markdown_embed': f"![{image_info.get('title', '')}]({filepath.absolute()})"
        }


def main():
    parser = argparse.ArgumentParser(
        description='Fetch biomedical images from PMC and NCBI Open-I'
    )
    
    # Search options
    parser.add_argument('--search', help='Search PMC for articles')
    parser.add_argument('--pmcid', help='Specific PMC article ID (e.g., PMC1234567)')
    parser.add_argument('--openi', help='Search NCBI Open-I for images')
    
    # Output options
    parser.add_argument('--output', '-o', default='./images',
                       help='Output directory for images (default: ./images)')
    parser.add_argument('--max-articles', type=int, default=5,
                       help='Maximum articles to process (default: 5)')
    parser.add_argument('--max-results', type=int, default=10,
                       help='Maximum images from Open-I (default: 10)')
    parser.add_argument('--create-library', action='store_true',
                       help='Create image_library.json file')
    
    args = parser.parse_args()
    
    if not any([args.search, args.pmcid, args.openi]):
        parser.error('Must specify --search, --pmcid, or --openi')
    
    fetcher = PMCImageFetcher(args.output)
    library_entries = []
    
    try:
        # Search and download from PMC
        if args.search:
            pmcids = fetcher.search_pmc(args.search, args.max_articles)
            for pmcid in pmcids:
                time.sleep(0.5)  # Rate limiting
                figures = fetcher.fetch_pmc_figures(pmcid)
                print(f"\nArticle {pmcid}:")
                print(json.dumps(figures, indent=2))
        
        # Fetch specific PMC article
        if args.pmcid:
            figures = fetcher.fetch_pmc_figures(args.pmcid)
            print(json.dumps(figures, indent=2))
        
        # Search Open-I
        if args.openi:
            images = fetcher.search_openi(args.openi, args.max_results)
            
            print(f"\nDownloading {len(images)} images...")
            for i, img in enumerate(images, 1):
                if img['url']:
                    filename = f"openi_{img.get('id', i)}.jpg"
                    filepath = fetcher.download_image(img['url'], filename)
                    
                    if filepath and args.create_library:
                        entry = fetcher.create_image_library_entry(img, filepath)
                        library_entries.append(entry)
                    
                    time.sleep(0.5)  # Rate limiting
        
        # Create image library JSON
        if args.create_library and library_entries:
            library_path = Path(args.output) / 'image_library.json'
            with open(library_path, 'w', encoding='utf-8') as f:
                json.dump(library_entries, f, indent=2)
            print(f"\nCreated image library: {library_path}")
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    print("\nDone!")


if __name__ == '__main__':
    main()
