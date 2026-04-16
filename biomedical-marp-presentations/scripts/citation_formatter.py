#!/usr/bin/env python3
"""
Citation Formatter for Biomedical Presentations

Fetches citation information from PubMed and formats it for use in
biomedical presentations (numbered or author-year formats).

Usage:
    # Format single PMID
    python citation_formatter.py 20439832
    
    # Format multiple PMIDs
    python citation_formatter.py 20439832 19114986 18326821
    
    # Use author-year format
    python citation_formatter.py 20439832 --format author-year
    
    # Output as JSON
    python citation_formatter.py 20439832 --json

Requirements:
    pip install requests --break-system-packages
"""

import sys
import json
import argparse
import requests
from typing import List, Dict, Optional
from datetime import datetime


class PubMedCitationFormatter:
    """Format citations from PubMed data."""
    
    def __init__(self):
        self.eutils_base = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
        self.session = requests.Session()
    
    def fetch_pubmed_data(self, pmid: str) -> Optional[Dict]:
        """Fetch article data from PubMed."""
        url = f"{self.eutils_base}esummary.fcgi"
        params = {
            'db': 'pubmed',
            'id': pmid,
            'retmode': 'json'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            result = data.get('result', {}).get(pmid, {})
            if 'error' in result:
                print(f"Error fetching PMID {pmid}: {result['error']}", file=sys.stderr)
                return None
            
            return result
        
        except Exception as e:
            print(f"Error fetching PMID {pmid}: {e}", file=sys.stderr)
            return None
    
    def parse_authors(self, pubmed_data: Dict, max_authors: int = 3) -> tuple:
        """
        Parse author list from PubMed data.
        Returns (author_list_string, et_al_needed)
        """
        authors = pubmed_data.get('authors', [])
        
        if not authors:
            return "Unknown Authors", False
        
        author_names = []
        for author in authors[:max_authors]:
            name = author.get('name', '')
            author_names.append(name)
        
        et_al = len(authors) > max_authors
        
        return author_names, et_al
    
    def format_numbered(self, pmid: str, pubmed_data: Dict) -> str:
        """Format citation in numbered style for MARP presentations."""
        
        authors, et_al = self.parse_authors(pubmed_data)
        
        # Get first author's last name
        first_author = authors[0] if authors else "Unknown"
        author_str = f"{first_author}"
        if len(authors) > 1 or et_al:
            author_str += " et al"
        
        title = pubmed_data.get('title', 'Unknown Title')
        journal = pubmed_data.get('fulljournalname', 'Unknown Journal')
        
        # Get publication date
        pub_date = pubmed_data.get('pubdate', '')
        year = pub_date.split()[0] if pub_date else 'Year Unknown'
        
        # Get volume and issue
        volume = pubmed_data.get('volume', '')
        issue = pubmed_data.get('issue', '')
        pages = pubmed_data.get('pages', '')
        
        # Build citation
        citation = f"{author_str}. {title}. {journal}. {year}"
        
        if volume:
            citation += f";{volume}"
            if issue:
                citation += f"({issue})"
            if pages:
                citation += f":{pages}"
        
        citation += f". PMID: {pmid}"
        
        # Add DOI if available
        doi = pubmed_data.get('elocationid', '')
        if doi and doi.startswith('doi:'):
            doi = doi.replace('doi:', '').strip()
        if doi:
            citation += f" doi:{doi}"
        
        return citation
    
    def format_author_year(self, pmid: str, pubmed_data: Dict) -> str:
        """Format citation in author-year style."""
        
        authors, et_al = self.parse_authors(pubmed_data)
        
        # Build author string
        if len(authors) == 1:
            author_str = authors[0]
        elif len(authors) == 2:
            author_str = f"{authors[0]} & {authors[1]}"
        else:
            author_str = f"{authors[0]} et al"
        
        title = pubmed_data.get('title', 'Unknown Title')
        journal = pubmed_data.get('fulljournalname', 'Unknown Journal')
        
        # Get year
        pub_date = pubmed_data.get('pubdate', '')
        year = pub_date.split()[0] if pub_date else 'Year Unknown'
        
        # Get volume and pages
        volume = pubmed_data.get('volume', '')
        pages = pubmed_data.get('pages', '')
        
        # Build citation
        citation = f"{author_str} ({year}). {title}. {journal}"
        
        if volume:
            citation += f", {volume}"
            if pages:
                citation += f", {pages}"
        
        citation += f". PMID: {pmid}"
        
        return citation
    
    def format_short(self, pmid: str, pubmed_data: Dict) -> str:
        """Format short citation for inline use (Author et al. Journal. Year)."""
        
        authors, et_al = self.parse_authors(pubmed_data, max_authors=1)
        first_author = authors[0] if authors else "Unknown"
        
        # Get abbreviated journal name
        journal = pubmed_data.get('source', pubmed_data.get('fulljournalname', 'Unknown'))
        
        # Get year
        pub_date = pubmed_data.get('pubdate', '')
        year = pub_date.split()[0] if pub_date else 'Unknown'
        
        citation = f"{first_author} et al. {journal}. {year}"
        
        return citation
    
    def format_marp_footer(self, citations: List[tuple]) -> str:
        """Format multiple citations for MARP footer."""
        
        footer_parts = []
        for pmid, data in citations:
            short_cite = self.format_short(pmid, data)
            footer_parts.append(short_cite)
        
        return ' | '.join(footer_parts)
    
    def create_citation_dict(self, pmid: str, pubmed_data: Dict) -> Dict:
        """Create a dictionary with all citation formats."""
        
        return {
            'pmid': pmid,
            'numbered': self.format_numbered(pmid, pubmed_data),
            'author_year': self.format_author_year(pmid, pubmed_data),
            'short': self.format_short(pmid, pubmed_data),
            'title': pubmed_data.get('title', ''),
            'journal': pubmed_data.get('fulljournalname', ''),
            'year': pubmed_data.get('pubdate', '').split()[0] if pubmed_data.get('pubdate') else '',
            'doi': pubmed_data.get('elocationid', '').replace('doi:', '').strip() if pubmed_data.get('elocationid') else ''
        }


def main():
    parser = argparse.ArgumentParser(
        description='Format PubMed citations for biomedical presentations'
    )
    parser.add_argument('pmids', nargs='+', help='PubMed IDs (PMIDs)')
    parser.add_argument('--format', '-f', 
                       choices=['numbered', 'author-year', 'short', 'all'],
                       default='numbered',
                       help='Citation format (default: numbered)')
    parser.add_argument('--json', action='store_true',
                       help='Output as JSON')
    parser.add_argument('--footer', action='store_true',
                       help='Format for MARP footer (short citations)')
    
    args = parser.parse_args()
    
    formatter = PubMedCitationFormatter()
    results = []
    
    print("Fetching citations from PubMed...", file=sys.stderr)
    
    for pmid in args.pmids:
        # Clean PMID
        pmid = pmid.strip().replace('PMID:', '').replace('pmid:', '')
        
        # Fetch data
        pubmed_data = formatter.fetch_pubmed_data(pmid)
        
        if not pubmed_data:
            continue
        
        results.append((pmid, pubmed_data))
    
    if not results:
        print("No valid citations found.", file=sys.stderr)
        sys.exit(1)
    
    # Output
    if args.json:
        output = [formatter.create_citation_dict(pmid, data) for pmid, data in results]
        print(json.dumps(output, indent=2))
    
    elif args.footer:
        print("\nMARP Footer Citation:")
        print("="*80)
        print(f"footer: '{formatter.format_marp_footer(results)}'")
    
    else:
        print("\nFormatted Citations:")
        print("="*80)
        
        for i, (pmid, data) in enumerate(results, 1):
            if args.format == 'all':
                cite_dict = formatter.create_citation_dict(pmid, data)
                print(f"\n{i}. PMID: {pmid}")
                print(f"\nNumbered Style:")
                print(cite_dict['numbered'])
                print(f"\nAuthor-Year Style:")
                print(cite_dict['author_year'])
                print(f"\nShort Style:")
                print(cite_dict['short'])
                print("-"*80)
            else:
                if args.format == 'numbered':
                    citation = formatter.format_numbered(pmid, data)
                elif args.format == 'author-year':
                    citation = formatter.format_author_year(pmid, data)
                else:  # short
                    citation = formatter.format_short(pmid, data)
                
                print(f"{i}. {citation}\n")


if __name__ == '__main__':
    main()
