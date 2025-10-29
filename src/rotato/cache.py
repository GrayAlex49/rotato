"""Image caching for Rotato."""

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Optional

from PIL import Image, ImageStat


@dataclass
class ImageInfo:
    """Cached information about an image"""

    path: str
    width: int
    height: int
    aspect_ratio: float
    brightness: float  # 0-255, average brightness
    file_size: int
    last_modified: float


class ImageCache:
    """Manages cached image metadata"""

    def __init__(self, cache_file: str = "image_cache.json"):
        self.cache_file = Path(cache_file)
        self.cache: Dict[str, ImageInfo] = {}
        self.load_cache()

    def load_cache(self):
        """Load cache from JSON file"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                self.cache = {path: ImageInfo(**info) for path, info in cache_data.items()}
            except Exception as e:
                print(f"Error loading cache: {e}")
                self.cache = {}

    def save_cache(self):
        """Save cache to JSON file"""
        try:
            cache_data = {path: asdict(info) for path, info in self.cache.items()}
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, indent=2)
        except Exception as e:
            print(f"Error saving cache: {e}")

    def get_image_info(self, image_path: str) -> Optional[ImageInfo]:
        """Get cached image info or analyze and cache new image"""
        path = str(Path(image_path).resolve())

        if not Path(path).exists():
            return None

        # Check if we have fresh cached data
        file_stat = os.stat(path)
        if path in self.cache:
            cached = self.cache[path]
            if cached.last_modified == file_stat.st_mtime:
                return cached

        # Analyze image and cache result
        try:
            with Image.open(path) as img:
                # Calculate average brightness
                if img.mode == "RGBA":
                    # Convert to RGB for brightness calculation
                    rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1])
                    stat = ImageStat.Stat(rgb_img)
                else:
                    stat = ImageStat.Stat(img.convert("RGB"))

                brightness = sum(stat.mean) / len(stat.mean)

                info = ImageInfo(
                    path=path,
                    width=img.width,
                    height=img.height,
                    aspect_ratio=img.width / img.height,
                    brightness=brightness,
                    file_size=file_stat.st_size,
                    last_modified=file_stat.st_mtime,
                )

                self.cache[path] = info
                return info
        except Exception as e:
            print(f"Error analyzing image {path}: {e}")
            return None
