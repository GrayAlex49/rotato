"""Image discovery and filtering."""

from pathlib import Path
from typing import List

from .cache import ImageCache
from .config import FilterConfig
from .monitors import MonitorInfo


class ImageManager:
    """Manages image discovery and filtering"""

    def __init__(
        self, cache: ImageCache, supported_formats: List[str], max_depth: int = 10
    ):
        self.cache = cache
        self.supported_formats = [fmt.lower() for fmt in supported_formats]
        self.max_depth = max_depth

    def discover_images(self, sources: List[str], recursive: bool = True) -> List[str]:
        """Discover all images from given sources"""
        images = []

        for source in sources:
            source_path = Path(source)

            if source_path.is_file() and self._is_supported_format(source_path):
                images.append(str(source_path))
            elif source_path.is_dir():
                if recursive:
                    images.extend(self._scan_directory_recursive(source_path, 0))
                else:
                    images.extend(self._scan_directory(source_path))

        return images

    def _scan_directory(self, directory: Path) -> List[str]:
        """Scan single directory for images"""
        images = []
        try:
            for file_path in directory.iterdir():
                if file_path.is_file() and self._is_supported_format(file_path):
                    images.append(str(file_path))
        except PermissionError:
            print(f"Permission denied accessing {directory}")
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")

        return images

    def _scan_directory_recursive(self, directory: Path, depth: int) -> List[str]:
        """Recursively scan directory for images"""
        if depth >= self.max_depth:
            return []

        images = []
        try:
            for item in directory.iterdir():
                if item.is_file() and self._is_supported_format(item):
                    images.append(str(item))
                elif item.is_dir() and not item.is_symlink():
                    images.extend(self._scan_directory_recursive(item, depth + 1))
        except PermissionError:
            print(f"Permission denied accessing {directory}")
        except Exception as e:
            print(f"Error scanning directory {directory}: {e}")

        return images

    def _is_supported_format(self, file_path: Path) -> bool:
        """Check if file format is supported"""
        return file_path.suffix.lower() in self.supported_formats

    def filter_images(
        self, image_paths: List[str], filters: FilterConfig, monitor: MonitorInfo
    ) -> List[str]:
        """Filter images based on criteria"""
        filtered = []

        for path in image_paths:
            info = self.cache.get_image_info(path)
            if not info:
                continue

            # Size filters
            if filters.min_width and info.width < filters.min_width:
                continue
            if filters.max_width and info.width > filters.max_width:
                continue
            if filters.min_height and info.height < filters.min_height:
                continue
            if filters.max_height and info.height > filters.max_height:
                continue

            # Aspect ratio filter
            if filters.aspect_ratios:
                aspect_match = False
                for target_ratio in filters.aspect_ratios:
                    if (
                        abs(info.aspect_ratio - target_ratio)
                        <= filters.aspect_ratio_tolerance
                    ):
                        aspect_match = True
                        break
                if not aspect_match:
                    continue

            # Brightness filter
            if filters.brightness_range:
                min_bright, max_bright = filters.brightness_range
                if not (min_bright <= info.brightness <= max_bright):
                    continue

            # File size filter
            if filters.max_file_size_mb:
                max_bytes = filters.max_file_size_mb * 1024 * 1024
                if info.file_size > max_bytes:
                    continue

            # Check if image resolution is suitable (don't upscale)
            if info.width < monitor.width and info.height < monitor.height:
                continue  # Image too small, would need upscaling

            filtered.append(path)

        return filtered
