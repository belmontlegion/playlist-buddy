"""Image caching and processing utilities."""

import os
import hashlib
from pathlib import Path
from typing import Optional
from PIL import Image, ImageFilter
import requests


class ImageCache:
    """Cache for thumbnails and artwork."""
    
    def __init__(self, cache_dir: Optional[Path] = None):
        """
        Initialize image cache.
        
        Args:
            cache_dir: Directory for cached images. Defaults to user cache dir.
        """
        if cache_dir is None:
            cache_dir = Path.home() / '.playlist_buddy' / 'cache' / 'images'
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_path(self, url: str, grayscale: bool = False) -> Path:
        """
        Get cache file path for a URL.
        
        Args:
            url: Image URL
            grayscale: Whether to use grayscale version
            
        Returns:
            Path to cached file
        """
        # Create hash of URL for filename
        url_hash = hashlib.md5(url.encode()).hexdigest()
        suffix = '_gray' if grayscale else ''
        return self.cache_dir / f"{url_hash}{suffix}.jpg"
    
    def get_image(self, url: str, grayscale: bool = False) -> Optional[Path]:
        """
        Get cached image or download if not cached.
        
        Args:
            url: Image URL
            grayscale: Whether to return grayscale version
            
        Returns:
            Path to cached image file or None on failure
        """
        cache_path = self._get_cache_path(url, grayscale)
        
        # Return if already cached
        if cache_path.exists():
            return cache_path
        
        # Download and cache
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Save original
            original_path = self._get_cache_path(url, False)
            with open(original_path, 'wb') as f:
                f.write(response.content)
            
            # Create grayscale version if requested
            if grayscale:
                img = Image.open(original_path)
                gray_img = img.convert('L')
                gray_img.save(cache_path, 'JPEG')
                return cache_path
            else:
                return original_path
                
        except Exception as e:
            print(f"Failed to download image from {url}: {e}")
            return None
    
    def create_grayscale(self, source_path: Path) -> Optional[Path]:
        """
        Create grayscale version of an image.
        
        Args:
            source_path: Path to source image
            
        Returns:
            Path to grayscale image or None on failure
        """
        try:
            img = Image.open(source_path)
            gray_img = img.convert('L')
            
            # Use same hash-based naming
            file_hash = hashlib.md5(str(source_path).encode()).hexdigest()
            gray_path = self.cache_dir / f"{file_hash}_gray.jpg"
            
            gray_img.save(gray_path, 'JPEG')
            return gray_path
            
        except Exception as e:
            print(f"Failed to create grayscale image: {e}")
            return None
    
    def clear_cache(self):
        """Clear all cached images."""
        for file in self.cache_dir.glob('*'):
            if file.is_file():
                file.unlink()
    
    def get_cache_size(self) -> int:
        """
        Get total size of cached images in bytes.
        
        Returns:
            Total cache size in bytes
        """
        total_size = 0
        for file in self.cache_dir.glob('*'):
            if file.is_file():
                total_size += file.stat().st_size
        return total_size
