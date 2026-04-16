"""Media fetchers for different sources."""

from .wikimedia import WikimediaFetcher
from .bioart import BioArtFetcher
from .unsplash import UnsplashFetcher

__all__ = ['WikimediaFetcher', 'BioArtFetcher', 'UnsplashFetcher']
