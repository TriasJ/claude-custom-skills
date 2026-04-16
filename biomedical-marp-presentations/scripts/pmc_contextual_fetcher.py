#!/usr/bin/env python3
"""
Enhanced PMC Contextual Image Fetcher

This script extends the PMC-figure-downloader methodology to intelligently
match figures to presentation subtopics based on contextual similarity between
figure descriptions (fig_desc) and subtopic content.

Usage:
    python pmc_contextual_fetcher.py --config subtopics.json --output ./images

Requirements:
    pip install requests polars scikit-learn --break-system-packages
"""

import json
import time
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
import argparse
from dataclasses import dataclass, asdict

try:
    import polars as pl
    POLARS_AVAILABLE = True
except ImportError:
    print("Warning: polars not available, using basic data structures")
    POLARS_AVAILABLE = False

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    print("Warning: scikit-learn not available, using simple keyword matching")
    SKLEARN_AVAILABLE = False


@dataclass
class SubtopicConfig:
    """Configuration for a presentation subtopic."""
    subtopic_name: str
    keywords: List[str]
    context_description: str
    pmc_query: str
    max_figures: int = 3


@dataclass
class FigureMatch:
    """A figure matched to a subtopic with relevance score."""
    subtopic_name: str
    pmcid: str
    fig_id: str
    fig_label: str
    fig_title: str
    fig_desc: str
    image_url: str
    relevance_score: float
    source_article_title: str = ""


class PMCContextualFetcher:
    """Fetch figures from PMC matched to subtopic contexts."""
    
    def __init__(self, output_dir: str = './images'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BiomedicalMARPPresentations/1.0 (Educational Use)'
        })
        self.ns = {"": "https://jats.nlm.nih.gov/ns/archiving/1.3/"}
    
    def get_text_or_empty(self, element, xpath: str) -> str:
        """Extract text from XML element or return empty string."""
        node = element.find(xpath, namespaces=self.ns)
        if node is None:
            return ""
        text_content = ET.tostring(node, method="text", encoding="unicode")
        return text_content.strip()
    
    def search_pmc(self, query: str, max_results: int = 20) -> List[str]:
        """Search PMC and return PMCIDs."""
        print(f"  Searching PMC: {query}")
        
        url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {
            'db': 'pmc',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            pmcids = data.get('esearchresult', {}).get('idlist', [])
            print(f"    Found {len(pmcids)} articles")
            return [f"PMC{pmcid}" if not pmcid.startswith('PMC') else pmcid 
                    for pmcid in pmcids]
        except Exception as e:
            print(f"    Error searching PMC: {e}")
            return []
    
    def extract_article_figures(self, pmcid: str) -> List[Dict]:
        """Extract figures from a single PMC article."""
        print(f"    Extracting figures from {pmcid}")
        
        url = f"https://www.ncbi.nlm.nih.gov/pmc/oai/oai.cgi"
        params = {
            'verb': 'GetRecord',
            'identifier': f'oai:pubmedcentral.nih.gov:{pmcid.replace("PMC", "")}',
            'metadataPrefix': 'pmc'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            
            root = ET.fromstring(response.content)
            
            # Get article title
            article_title = self.get_text_or_empty(
                root, ".//article-title"
            )
            
            figures = []
            fig_elements = root.findall(".//fig", namespaces=self.ns)
            
            for fig in fig_elements:
                caption = self.get_text_or_empty(fig, ".//caption/p")
                title = self.get_text_or_empty(fig, ".//caption/title")
                label = self.get_text_or_empty(fig, ".//label")
                fig_id = fig.attrib.get("id", "")
                
                graphic = fig.find(".//graphic", namespaces=self.ns)
                if graphic is not None:
                    xlink_href = graphic.attrib.get(
                        "{http://www.w3.org/1999/xlink}href", ""
                    )
                    if xlink_href:
                        image_url = (
                            f"https://www.ncbi.nlm.nih.gov/pmc/articles/"
                            f"{pmcid}/bin/{xlink_href}.jpg"
                        )
                        
                        figures.append({
                            'pmcid': pmcid,
                            'fig_id': fig_id,
                            'fig_label': label,
                            'fig_title': title,
                            'fig_desc': caption,
                            'image_url': image_url,
                            'article_title': article_title
                        })
            
            print(f"      Found {len(figures)} figures")
            return figures
            
        except Exception as e:
            print(f"      Error extracting figures: {e}")
            return []
    
    def calculate_relevance_tfidf(
        self, 
        fig_desc: str, 
        subtopic_context: str
    ) -> float:
        """Calculate relevance using TF-IDF cosine similarity."""
        if not SKLEARN_AVAILABLE:
            return self.calculate_relevance_keywords(fig_desc, subtopic_context)
        
        try:
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([subtopic_context, fig_desc])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            return float(similarity[0][0])
        except:
            return self.calculate_relevance_keywords(fig_desc, subtopic_context)
    
    def calculate_relevance_keywords(
        self, 
        fig_desc: str, 
        subtopic_keywords: str
    ) -> float:
        """Fallback: Calculate relevance using keyword matching."""
        fig_desc_lower = fig_desc.lower()
        keywords = subtopic_keywords.lower().split()
        
        matches = sum(1 for kw in keywords if kw in fig_desc_lower)
        if not keywords:
            return 0.0
        
        return matches / len(keywords)
    
    def match_figures_to_subtopic(
        self,
        subtopic: SubtopicConfig,
        figures: List[Dict]
    ) -> List[FigureMatch]:
        """Match and rank figures by relevance to subtopic."""
        print(f"  Matching figures to: {subtopic.subtopic_name}")
        
        # Create full context for matching
        full_context = f"{subtopic.context_description} {' '.join(subtopic.keywords)}"
        
        matches = []
        for fig in figures:
            # Combine figure description and title for matching
            fig_content = f"{fig['fig_desc']} {fig['fig_title']}"
            
            if SKLEARN_AVAILABLE:
                score = self.calculate_relevance_tfidf(fig_content, full_context)
            else:
                score = self.calculate_relevance_keywords(fig_content, full_context)
            
            match = FigureMatch(
                subtopic_name=subtopic.subtopic_name,
                pmcid=fig['pmcid'],
                fig_id=fig['fig_id'],
                fig_label=fig['fig_label'],
                fig_title=fig['fig_title'],
                fig_desc=fig['fig_desc'],
                image_url=fig['image_url'],
                relevance_score=score,
                source_article_title=fig.get('article_title', '')
            )
            matches.append(match)
        
        # Sort by relevance and return top N
        matches.sort(key=lambda x: x.relevance_score, reverse=True)
        top_matches = matches[:subtopic.max_figures]
        
        print(f"    Selected {len(top_matches)} top figures")
        for i, match in enumerate(top_matches, 1):
            print(f"      {i}. Score: {match.relevance_score:.3f} - {match.fig_label}")
        
        return top_matches
    
    def download_figure(self, match: FigureMatch) -> Optional[Path]:
        """Download a figure image."""
        filename = f"{match.pmcid}_{match.fig_id}.jpg"
        filepath = self.output_dir / filename
        
        try:
            response = self.session.get(match.image_url, timeout=30)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filepath
        except Exception as e:
            print(f"      Error downloading {filename}: {e}")
            return None
    
    def process_subtopics(
        self,
        subtopics: List[SubtopicConfig]
    ) -> Dict[str, List[FigureMatch]]:
        """Process all subtopics and find matching figures."""
        all_matches = {}
        
        for i, subtopic in enumerate(subtopics, 1):
            print(f"\n[{i}/{len(subtopics)}] Processing: {subtopic.subtopic_name}")
            
            # Search PMC for relevant articles
            pmcids = self.search_pmc(subtopic.pmc_query, max_results=10)
            
            if not pmcids:
                print("  No articles found, skipping")
                continue
            
            # Extract figures from articles
            all_figures = []
            for pmcid in pmcids[:5]:  # Limit to first 5 articles
                time.sleep(0.3)  # Rate limiting
                figures = self.extract_article_figures(pmcid)
                all_figures.extend(figures)
            
            if not all_figures:
                print("  No figures found in articles")
                continue
            
            # Match figures to subtopic
            matches = self.match_figures_to_subtopic(subtopic, all_figures)
            all_matches[subtopic.subtopic_name] = matches
            
            # Download top figures
            print(f"  Downloading {len(matches)} figures")
            for match in matches:
                time.sleep(0.2)  # Rate limiting
                filepath = self.download_figure(match)
                if filepath:
                    print(f"    Downloaded: {filepath.name}")
        
        return all_matches
    
    def create_image_library(
        self,
        matches_by_subtopic: Dict[str, List[FigureMatch]]
    ) -> List[Dict]:
        """Create image library JSON from matched figures."""
        library = []
        
        for subtopic_name, matches in matches_by_subtopic.items():
            for match in matches:
                filename = f"{match.pmcid}_{match.fig_id}.jpg"
                filepath = self.output_dir / filename
                
                entry = {
                    'image_id': f"{match.pmcid}_{match.fig_id}",
                    'filename': filename,
                    'path': str(filepath.absolute()),
                    'source_document': f"{match.pmcid}.pdf",
                    'source_path': '',
                    'source_page': 0,
                    'document_title': match.source_article_title,
                    'caption': match.fig_desc,
                    'alt_text': match.fig_title,
                    'context_before': '',
                    'context_after': '',
                    'section': subtopic_name,
                    'image_type': 'figure',
                    'keywords': [],
                    'ocr_text': '',
                    'dimensions': '',
                    'extracted_date': time.strftime('%Y-%m-%dT%H:%M:%S'),
                    'relevance_score': match.relevance_score,
                    'subtopic': subtopic_name,
                    'markdown_embed': f"![{match.fig_label}]({filepath.absolute()})"
                }
                library.append(entry)
        
        return library


def load_subtopics_config(config_file: str) -> List[SubtopicConfig]:
    """Load subtopics configuration from JSON file."""
    with open(config_file, 'r') as f:
        data = json.load(f)
    
    subtopics = []
    for item in data:
        subtopic = SubtopicConfig(
            subtopic_name=item['subtopic_name'],
            keywords=item.get('keywords', []),
            context_description=item.get('context_description', ''),
            pmc_query=item.get('pmc_query', item['subtopic_name']),
            max_figures=item.get('max_figures', 3)
        )
        subtopics.append(subtopic)
    
    return subtopics


def create_example_config():
    """Create an example subtopics configuration file."""
    example = [
        {
            "subtopic_name": "TMS Coil Types",
            "keywords": ["figure-8 coil", "H-coil", "circular coil", "double-cone coil"],
            "context_description": "Overview of different TMS coil designs, their geometry, and physical characteristics",
            "pmc_query": "transcranial magnetic stimulation AND coil design",
            "max_figures": 3
        },
        {
            "subtopic_name": "Coil Penetration Depth",
            "keywords": ["penetration depth", "focality", "electric field", "depth"],
            "context_description": "Electric field penetration characteristics and depth-focality tradeoffs for different coil types",
            "pmc_query": "TMS AND (penetration depth OR focality)",
            "max_figures": 2
        }
    ]
    
    with open('subtopics_example.json', 'w') as f:
        json.dump(example, f, indent=2)
    
    print("Created example config: subtopics_example.json")


def main():
    parser = argparse.ArgumentParser(
        description='Fetch contextually relevant figures from PMC for presentation subtopics'
    )
    parser.add_argument('--config', required=True,
                       help='JSON config file with subtopics')
    parser.add_argument('--output', '-o', default='./images',
                       help='Output directory for images (default: ./images)')
    parser.add_argument('--create-library', action='store_true',
                       help='Create image_library.json file')
    parser.add_argument('--example-config', action='store_true',
                       help='Create example config file and exit')
    
    args = parser.parse_args()
    
    if args.example_config:
        create_example_config()
        return
    
    # Load configuration
    print("Loading subtopics configuration...")
    subtopics = load_subtopics_config(args.config)
    print(f"Loaded {len(subtopics)} subtopics\n")
    
    # Process subtopics
    fetcher = PMCContextualFetcher(args.output)
    matches = fetcher.process_subtopics(subtopics)
    
    # Create image library
    if args.create_library:
        library = fetcher.create_image_library(matches)
        library_path = Path(args.output) / 'image_library.json'
        
        with open(library_path, 'w') as f:
            json.dump(library, f, indent=2)
        
        print(f"\n✅ Created image library: {library_path}")
        print(f"   Total figures: {len(library)}")
        print(f"   Subtopics: {len(matches)}")
    
    # Print summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    for subtopic_name, figure_matches in matches.items():
        print(f"\n{subtopic_name}:")
        for match in figure_matches:
            print(f"  • {match.fig_label} (score: {match.relevance_score:.3f})")
            print(f"    {match.fig_title[:80]}")
    
    print(f"\n✅ Done! Downloaded {sum(len(m) for m in matches.values())} figures")
    print(f"   Output directory: {fetcher.output_dir}")


if __name__ == '__main__':
    main()
