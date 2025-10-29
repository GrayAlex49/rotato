"""Wallpaper management."""

from pathlib import Path
from typing import Dict, Optional

from .monitors import MonitorInfo


class WallpaperManager:
    """Manages setting wallpapers on different monitors"""

    def __init__(self):
        self.current_wallpapers: Dict[str, str] = {}  # monitor_name -> image_path

    def set_wallpaper(self, monitor: MonitorInfo, image_path: str):
        """Set wallpaper for specific monitor - platform-specific implementation"""
        from .platform import get_platform_wallpaper_setter

        setter = get_platform_wallpaper_setter()

        try:
            # Convert to absolute path
            abs_path = str(Path(image_path).resolve())

            # Set wallpaper using platform-specific implementation
            result = setter.set_wallpaper(monitor, abs_path)

            if result:
                self.current_wallpapers[monitor.name] = abs_path
                print(f"Set wallpaper for {monitor.name}: {Path(image_path).name}")
            else:
                print(f"Failed to set wallpaper: {image_path}")

        except Exception as e:
            print(f"Error setting wallpaper: {e}")

    def get_current_wallpaper(self, monitor_name: str) -> Optional[str]:
        """Get current wallpaper path for monitor"""
        return self.current_wallpapers.get(monitor_name)
