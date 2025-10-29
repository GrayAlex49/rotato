"""Platform-specific implementations."""

import platform
import sys


def get_platform_detector():
    """Get platform-specific monitor detector"""
    system = platform.system()

    if system == "Windows":
        from .windows import WindowsMonitorDetector

        return WindowsMonitorDetector()
    elif system == "Linux":
        # Future Linux support
        raise NotImplementedError("Linux support not yet implemented")
    else:
        raise NotImplementedError(f"Platform {system} not supported")


def get_platform_wallpaper_setter():
    """Get platform-specific wallpaper setter"""
    system = platform.system()

    if system == "Windows":
        from .windows import WindowsWallpaperSetter

        return WindowsWallpaperSetter()
    elif system == "Linux":
        # Future Linux support
        raise NotImplementedError("Linux support not yet implemented")
    else:
        raise NotImplementedError(f"Platform {system} not supported")


def check_platform_support():
    """Check if current platform is supported"""
    system = platform.system()
    if system not in ["Windows"]:
        print(f"Warning: Platform {system} is not fully supported yet.")
        print("Currently supported platforms: Windows")
        return False
    return True
