"""Linux-specific implementations (placeholder for future development)."""

from typing import List

from ..monitors import MonitorInfo


class LinuxMonitorDetector:
    """Linux-specific monitor detection (to be implemented)"""

    def detect_monitors(self) -> List[MonitorInfo]:
        """Detect all connected monitors using Linux APIs"""
        # TODO: Implement using xrandr or other Linux APIs
        raise NotImplementedError("Linux monitor detection not yet implemented")


class LinuxWallpaperSetter:
    """Linux-specific wallpaper setting (to be implemented)"""

    def set_wallpaper(self, monitor: MonitorInfo, image_path: str) -> bool:
        """Set wallpaper using Linux APIs"""
        # TODO: Implement for various Linux desktop environments:
        # - GNOME: gsettings
        # - KDE: plasma-apply-wallpaperimage
        # - XFCE: xfconf-query
        # - Others: feh, nitrogen, etc.
        raise NotImplementedError("Linux wallpaper setting not yet implemented")
