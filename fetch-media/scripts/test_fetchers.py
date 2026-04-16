#!/usr/bin/env python3
"""Test script to validate all media fetchers."""

import asyncio
import sys
from pathlib import Path
import tempfile
import os

# Add to path
sys.path.insert(0, str(Path(__file__).parent))

from fetchers.wikimedia import WikimediaFetcher
from fetchers.bioart import BioArtFetcher
from fetchers.unsplash import UnsplashFetcher

# Try to load environment variables
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        load_dotenv(env_file)
except ImportError:
    pass


async def test_wikimedia():
    """Test Wikimedia Commons fetcher."""
    print("\n" + "=" * 70)
    print("Testing Wikimedia Commons Fetcher")
    print("=" * 70)

    config = {"rate_limit": 1.0}
    fetcher = WikimediaFetcher(config)

    try:
        # Test 1: Search
        print("\n[TEST 1] Searching for 'virus electron microscopy'...")
        results = await fetcher.search("virus electron microscopy", limit=3)

        if not results:
            print("✗ No results found")
            return False

        print(f"✓ Found {len(results)} results")

        # Display first result
        item = results[0]
        print(f"\n[RESULT] First result:")
        print(f"  Title: {item.title}")
        print(f"  ID: {item.id}")
        print(f"  Format: {item.file_type}")
        print(f"  License: {item.license}")
        print(f"  URL: {item.url}")

        # Test 2: Get Details
        print(f"\n[TEST 2] Getting details for: {item.id}")
        details = await fetcher.get_details(item.id)
        print(f"✓ Retrieved details")
        print(f"  Attribution: {details.attribution[:80]}...")

        # Test 3: Download (to temp)
        print(f"\n[TEST 3] Testing download...")
        temp_dir = Path(tempfile.gettempdir()) / "fetch-media-test"
        temp_dir.mkdir(exist_ok=True)

        result = await fetcher.download(item, temp_dir)

        if result.success:
            print(f"✓ Download successful")
            print(f"  Path: {result.local_path}")
            print(f"  Size: {result.file_size:,} bytes")

            # Verify file exists
            if Path(result.local_path).exists():
                print(f"✓ File verified on disk")
            else:
                print(f"✗ File not found!")
                return False
        else:
            print(f"✗ Download failed: {result.error}")
            return False

        print("\n✓ Wikimedia tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Wikimedia test error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await fetcher.close()


async def test_bioart():
    """Test BioArt fetcher."""
    print("\n" + "=" * 70)
    print("Testing BioArt Fetcher")
    print("=" * 70)

    # Check if index exists
    index_file = Path(__file__).parent.parent / "bioart_index.json"
    if not index_file.exists():
        print("\n⚠️  BioArt index not found")
        print("   Run: python3 bioart_crawler.py --mode full")
        print("   Skipping BioArt tests")
        return True  # Not a failure, just skip

    config = {"rate_limit": 1.0}
    fetcher = BioArtFetcher(config)

    try:
        # Test 1: Search
        print("\n[TEST 1] Searching for 'virus'...")
        results = await fetcher.search("virus", limit=3)

        if not results:
            print("✗ No results found")
            return False

        print(f"✓ Found {len(results)} results")

        # Display first result
        item = results[0]
        print(f"\n[RESULT] First result:")
        print(f"  Title: {item.title}")
        print(f"  ID: {item.id}")
        print(f"  URL: {item.url}")

        # Test 2: Get Details
        print(f"\n[TEST 2] Getting details for item ID 560...")
        details = await fetcher.get_details("560")
        print(f"✓ Retrieved details")
        print(f"  Title: {details.title}")
        print(f"  Files: {len(details.metadata.get('file_endpoints', []))}")

        # Test 3: Download
        if details.download_url:
            print(f"\n[TEST 3] Testing download...")
            temp_dir = Path(tempfile.gettempdir()) / "fetch-media-test"
            temp_dir.mkdir(exist_ok=True)

            result = await fetcher.download(details, temp_dir)

            if result.success:
                print(f"✓ Download successful")
                print(f"  Path: {result.local_path}")
            else:
                print(f"✗ Download failed: {result.error}")
                return False
        else:
            print(f"\n[TEST 3] No download URL available (skipped)")

        print("\n✓ BioArt tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ BioArt test error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await fetcher.close()


async def test_unsplash():
    """Test Unsplash fetcher."""
    print("\n" + "=" * 70)
    print("Testing Unsplash Fetcher")
    print("=" * 70)

    # Check for API key
    api_key = os.getenv("UNSPLASH_API_KEY")
    if not api_key:
        print("\n⚠️  Unsplash API key not found")
        print("   Set UNSPLASH_API_KEY in .env file")
        print("   Skipping Unsplash tests")
        return True  # Not a failure, just skip

    config = {"rate_limit": 1.0, "api_key": api_key}
    fetcher = UnsplashFetcher(config)

    try:
        # Test 1: Search
        print("\n[TEST 1] Searching for 'laboratory'...")
        results = await fetcher.search("laboratory", limit=3)

        if not results:
            print("✗ No results found")
            return False

        print(f"✓ Found {len(results)} results")

        # Display first result
        item = results[0]
        print(f"\n[RESULT] First result:")
        print(f"  Title: {item.title}")
        print(f"  ID: {item.id}")
        print(f"  Author: {item.author}")
        print(f"  License: {item.license}")

        # Test 2: Get Details
        print(f"\n[TEST 2] Getting details for: {item.id}")
        details = await fetcher.get_details(item.id)
        print(f"✓ Retrieved details")
        print(f"  Attribution: {details.attribution}")

        # Test 3: Download
        print(f"\n[TEST 3] Testing download...")
        temp_dir = Path(tempfile.gettempdir()) / "fetch-media-test"
        temp_dir.mkdir(exist_ok=True)

        result = await fetcher.download(item, temp_dir)

        if result.success:
            print(f"✓ Download successful")
            print(f"  Path: {result.local_path}")
            print(f"  Size: {result.file_size:,} bytes")
        else:
            print(f"✗ Download failed: {result.error}")
            return False

        print("\n✓ Unsplash tests passed!")
        return True

    except Exception as e:
        print(f"\n✗ Unsplash test error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        await fetcher.close()


async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("FETCH-MEDIA SKILL TEST SUITE")
    print("=" * 70)

    results = {
        "wikimedia": await test_wikimedia(),
        "bioart": await test_bioart(),
        "unsplash": await test_unsplash(),
    }

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)

    for source, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{source.upper()}: {status}")

    all_passed = all(results.values())
    print("\n" + "=" * 70)
    if all_passed:
        print("✓ ALL TESTS PASSED")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 70)

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
