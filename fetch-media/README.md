# Fetch-Media Skill

Search and download open-access images, scientific illustrations, and media from multiple sources with proper attribution.

## Features

- **Multiple Sources**: Wikimedia Commons, NIH BioArt, Unsplash
- **Flexible Modes**: Get URLs only or download files
- **Auto Source Selection**: Searches all sources or specify one
- **Proper Attribution**: Automatic citation generation
- **File Type Filtering**: Filter by SVG, PNG, JPG, etc.
- **Expandable Architecture**: Easy to add new sources

## Quick Start

### 1. Install Dependencies

```bash
cd ~/.claude/skills/fetch-media
pip3 install -r scripts/requirements.txt
```

### 2. Basic Usage

```bash
# Search and get URLs (fastest)
python3 scripts/search_media.py --query "virus microscopy" --mode url --limit 5

# Download files
python3 scripts/search_media.py --query "cell division" --mode download --limit 3
```

### 3. Using the Slash Command

From Claude Code:
```
/fetch-media virus electron microscopy
```

## Sources

### Wikimedia Commons
- **Type**: General media repository
- **Content**: 100M+ files
- **Setup**: None required ✓

### NIH BioArt
- **Type**: Scientific illustrations
- **Content**: Professional medical/biological artwork
- **Setup**: Requires building search index (one-time)

```bash
# Build index (takes ~15 minutes)
python3 scripts/bioart_crawler.py --mode full
```

### Unsplash
- **Type**: Professional photography
- **Content**: High-quality photos
- **Setup**: Requires API key

```bash
# Configure API key
cp .env.example .env
# Edit .env and add UNSPLASH_API_KEY
```

## Examples

### Search All Sources
```bash
python3 scripts/search_media.py --query "microscopy" --limit 10
```

### Specific Source
```bash
python3 scripts/search_media.py \
  --source wikimedia \
  --query "DNA structure" \
  --file-types svg
```

### Download to Custom Directory (Persistent Storage)
```bash
# Save to permanent location instead of temp
python3 scripts/search_media.py \
  --query "bacteria" \
  --mode download \
  --output ~/presentation/images
```

**Note**: By default, files download to `/tmp/fetch-media` and rely on system cleanup. Use `--output` to save files permanently.

### Pretty Output
```bash
python3 scripts/search_media.py \
  --query "cell" \
  --format pretty
```

## Testing

Run the test suite to verify all sources work:

```bash
cd ~/.claude/skills/fetch-media
python3 scripts/test_fetchers.py
```

Expected output:
- ✓ WIKIMEDIA: PASSED (always)
- ✓ BIOART: PASSED (if index exists)
- ✓ UNSPLASH: PASSED (if API key configured)

## Directory Structure

```
~/.claude/skills/fetch-media/
├── SKILL.md                          # Main skill file
├── README.md                         # This file
├── .env.example                      # API key template
├── scripts/
│   ├── search_media.py               # Main CLI script
│   ├── bioart_crawler.py             # BioArt index builder
│   ├── test_fetchers.py              # Test suite
│   ├── requirements.txt              # Python dependencies
│   ├── models.py                     # Data models
│   └── fetchers/
│       ├── base.py                   # Base fetcher class
│       ├── wikimedia.py              # Wikimedia Commons
│       ├── bioart.py                 # NIH BioArt
│       └── unsplash.py               # Unsplash
├── references/
│   ├── api-setup.md                  # API configuration guide
│   ├── sources.md                    # Source documentation
│   └── examples.md                   # Usage examples
└── bioart_index.json                 # BioArt search index (generated)
```

## Configuration

### Environment Variables

Create `.env` file:
```bash
# Unsplash API key (required for Unsplash)
UNSPLASH_API_KEY=your_key_here

# Optional: Override default download directory
# DOWNLOAD_DIR=/path/to/downloads
```

### BioArt Index

The BioArt source requires a local search index:

```bash
# First time: Full build (~15 minutes)
python3 scripts/bioart_crawler.py --mode full

# Updates: Incremental (only new items)
python3 scripts/bioart_crawler.py --mode incremental

# Search the index directly
python3 scripts/bioart_crawler.py --mode search --search "virus"
```

## Output Format

### JSON (default)
```json
{
  "query": "virus",
  "mode": "url",
  "results": [
    {
      "id": "File:Virus.jpg",
      "title": "Electron microscopy of virus",
      "source": "wikimedia",
      "url": "https://commons.wikimedia.org/...",
      "download_url": "https://upload.wikimedia.org/...",
      "file_type": "jpg",
      "license": "CC-BY 4.0",
      "attribution": "John Doe, via Wikimedia Commons, ..."
    }
  ],
  "citations": [
    "John Doe, via Wikimedia Commons, ..."
  ],
  "warnings": [],
  "stats": {
    "total_found": 1,
    "sources_searched": ["wikimedia"],
    "sources_failed": []
  }
}
```

### Pretty Format
```
======================================================================
Search Results for: virus
======================================================================

Found 1 results
Sources searched: wikimedia

1. Electron microscopy of virus
   Source: wikimedia
   URL: https://commons.wikimedia.org/wiki/File:Virus.jpg
   Attribution: John Doe, via Wikimedia Commons, ...
```

## Adding New Sources

To add a new media source:

1. Create fetcher in `scripts/fetchers/new_source.py`:
```python
from .base import BaseFetcher

class NewSourceFetcher(BaseFetcher):
    async def search(self, query, file_types=None, limit=20):
        # Implement search
        pass

    async def get_details(self, item_id):
        # Implement details
        pass
```

2. Register in `scripts/search_media.py`:
```python
FETCHERS = {
    'wikimedia': WikimediaFetcher,
    'bioart': BioArtFetcher,
    'unsplash': UnsplashFetcher,
    'newsource': NewSourceFetcher  # Add here
}
```

3. Test and document

See `scripts/fetchers/base.py` for the complete interface.

## Troubleshooting

### "BioArt index not found"
**Solution**: Build the index:
```bash
python3 scripts/bioart_crawler.py --mode full
```

### "Unsplash API key not found"
**Solution**: Configure API key:
```bash
cp .env.example .env
# Edit .env and add UNSPLASH_API_KEY
```

### "No module named 'httpx'"
**Solution**: Install dependencies:
```bash
pip3 install -r scripts/requirements.txt
```

### Rate Limiting
If you hit rate limits, wait and retry. The fetchers respect rate limits automatically (1-2 seconds between requests).

## Documentation

- **API Setup**: [references/api-setup.md](references/api-setup.md)
- **Source Details**: [references/sources.md](references/sources.md)
- **Usage Examples**: [references/examples.md](references/examples.md)

## License & Attribution

This skill helps you find and use openly-licensed media:
- **Wikimedia Commons**: Various licenses (CC0, CC-BY, CC-BY-SA, Public Domain)
- **NIH BioArt**: Public Domain and CC-BY
- **Unsplash**: Unsplash License (free to use, attribution appreciated)

**Always use the attribution text provided in results** when publishing or presenting media.

## Support

For issues or questions:
1. Check the [references/](references/) documentation
2. Run tests: `python3 scripts/test_fetchers.py`
3. Review error messages for specific guidance

## Version

**Version**: 1.0.0
**Last Updated**: 2025-01-19
