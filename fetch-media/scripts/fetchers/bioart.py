"""NIH BioArt Source fetcher implementation."""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path
import json
import re
import sys

sys.path.append(str(Path(__file__).parent.parent))
from models import MediaItem
from fetchers.base import BaseFetcher


class BioArtFetcher(BaseFetcher):
    """Fetcher for NIH BioArt Source.

    Requires a pre-built JSON index created by bioart_crawler.py.
    Searches the index and fetches files from the BioArt API.
    """

    BASE_URL = "https://bioart.niaid.nih.gov"
    INDEX_FILE = Path(__file__).parent.parent.parent / "bioart_index.json"

    async def search(
        self,
        query: str,
        file_types: Optional[List[str]] = None,
        limit: int = 20,
    ) -> List[MediaItem]:
        """Search for media on BioArt using the JSON index."""
        # Check if index exists
        if not self.INDEX_FILE.exists():
            raise FileNotFoundError(
                f"BioArt index not found at {self.INDEX_FILE}. "
                "Please run bioart_crawler.py to build the index."
            )

        # Load index
        with open(self.INDEX_FILE, "r", encoding="utf-8") as f:
            index = json.load(f)

        # Search index
        query_terms = query.lower().split()
        results = []

        for item_id, item in index.items():
            score = 0

            # Search in bioart_id (exact ID match)
            if query.lower() in item["bioart_id"].lower():
                score += 100

            # Search in title
            title_lower = item["title"].lower()
            for term in query_terms:
                if term in title_lower:
                    score += 10

            # Search in description
            description_lower = item.get("description", "").lower()
            for term in query_terms:
                if term in description_lower:
                    score += 7

            # Search in keywords
            keywords_lower = [k.lower() for k in item.get("keywords", [])]
            for term in query_terms:
                if term in keywords_lower:
                    score += 5

            # Bonus for items with files
            if item.get("has_files", False):
                score += 1

            if score > 0:
                results.append((score, item))

        # Sort by relevance
        results.sort(key=lambda x: x[0], reverse=True)

        # Convert to MediaItems (limit results)
        media_items = []
        for score, item in results[:limit]:
            try:
                media_item = await self._convert_to_media_item(item)
                if media_item:
                    media_items.append(media_item)
            except Exception:
                continue

        return media_items

    async def get_details(self, item_id: str) -> MediaItem:
        """Get detailed information about a specific BioArt item.

        Args:
            item_id: BioArt item ID (numeric, e.g., "631")
        """
        # Fetch fresh details from the website
        detail_url = f"{self.BASE_URL}/bioart/{item_id}"

        await self._rate_limit_wait()
        client = await self.get_client()
        response = await client.get(detail_url)
        response.raise_for_status()
        html = response.text

        # Extract file endpoints
        file_endpoints = self._extract_file_endpoints(html, item_id)

        # Parse HTML for metadata
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")

        # Extract title
        title_tag = soup.find("title")
        title = title_tag.text.strip() if title_tag else f"BioArt Item {item_id}"

        if title == "BioArt":
            title = f"BioArt Item {item_id}"

        # Extract license info
        license_text = "Unknown"
        if "Public Domain" in html:
            license_text = "Public Domain"
        elif "CC-BY" in html or "CC BY" in html:
            license_text = "CC-BY"

        # Determine download URL - prefer PNG format
        download_url = ""
        file_type = "png"

        if file_endpoints:
            # Try to find PNG format
            png_endpoint = None
            for endpoint in file_endpoints:
                # Fetch endpoint to check content-type
                # For now, just use first endpoint
                png_endpoint = endpoint
                break

            if png_endpoint:
                download_url = png_endpoint["full_url"]

        # Create attribution
        attribution = (
            f"NIAID Visual & Medical Arts, BioArt Source, {detail_url}"
        )

        return MediaItem(
            id=item_id,
            title=title,
            source="bioart",
            url=detail_url,
            download_url=download_url,
            file_type=file_type,
            description=f"NIH BioArt scientific illustration. ID: BIOART-{item_id.zfill(6)}",
            license=license_text,
            attribution=attribution,
            metadata={
                "detail_url": detail_url,
                "file_endpoints": file_endpoints,
                "bioart_id": f"BIOART-{item_id.zfill(6)}",
            },
        )

    async def _convert_to_media_item(self, item: Dict[str, Any]) -> Optional[MediaItem]:
        """Convert index item to MediaItem."""
        item_id = str(item["id"])

        # Get file endpoints
        file_endpoints = item.get("file_endpoints", [])

        # Determine download URL - prefer PNG format
        download_url = ""
        file_type = "png"

        if file_endpoints:
            download_url = file_endpoints[0]["url"]

        return MediaItem(
            id=item_id,
            title=item["title"],
            source="bioart",
            url=item["url"],
            download_url=download_url,
            file_type=file_type,
            description=item.get("description", ""),
            license=item.get("license", "Unknown"),
            attribution=f"NIAID Visual & Medical Arts, BioArt Source, {item['url']}",
            metadata={
                "file_endpoints": file_endpoints,
                "keywords": item.get("keywords", []),
                "bioart_id": item["bioart_id"],
            },
        )

    def _extract_file_endpoints(self, html: str, item_id: str) -> List[Dict[str, str]]:
        """Extract file endpoints from detail page HTML."""
        # Pattern: /api/bioarts/{id}/files/{file_id}
        file_pattern = re.compile(r"/api/bioarts/(\d+)/files/(\d+)")
        file_matches = file_pattern.findall(html)

        file_endpoints = []
        seen_files = set()

        for bioart_id, file_id in file_matches:
            if file_id not in seen_files:
                endpoint = f"/api/bioarts/{bioart_id}/files/{file_id}"
                full_url = f"{self.BASE_URL}{endpoint}"
                file_endpoints.append(
                    {
                        "file_id": file_id,
                        "endpoint": endpoint,
                        "full_url": full_url,
                    }
                )
                seen_files.add(file_id)

        return file_endpoints
