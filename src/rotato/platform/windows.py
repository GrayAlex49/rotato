"""Windows-specific implementations for monitor detection and wallpaper setting."""

from typing import List

try:
    import win32api
    import win32con
    import win32gui

    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    print("Warning: pywin32 not available. Windows features will not work.")

from ..monitors import MonitorInfo


class WindowsMonitorDetector:
    """Windows-specific monitor detection"""

    def detect_monitors(self) -> List[MonitorInfo]:
        """Detect all connected monitors using Windows API"""
        if not WINDOWS_AVAILABLE:
            raise RuntimeError("Windows API not available")

        monitors: List[MonitorInfo] = []

        try:
            enum_result = win32api.EnumDisplayMonitors(None, None)
        except Exception as e:
            print(f"Error detecting monitors: {e}")
            return monitors

        for hmonitor, _hdc, rect in enum_result:
            monitor_info = win32api.GetMonitorInfo(hmonitor)
            device_name = monitor_info["Device"]

            left, top, right, bottom = rect
            width = right - left
            height = bottom - top
            is_primary = monitor_info["Flags"] & win32con.MONITORINFOF_PRIMARY != 0

            monitors.append(
                MonitorInfo(
                    handle=hmonitor,
                    width=width,
                    height=height,
                    x=left,
                    y=top,
                    is_primary=is_primary,
                    name=device_name,
                )
            )

        return monitors


class WindowsWallpaperSetter:
    """Windows-specific wallpaper setting"""

    def set_wallpaper(self, monitor: MonitorInfo, image_path: str) -> bool:
        """Set wallpaper using Windows API"""
        if not WINDOWS_AVAILABLE:
            raise RuntimeError("Windows API not available")

        try:
            # On Windows, we set the wallpaper globally
            # For true per-monitor wallpapers, we'd need a more complex solution
            result = win32gui.SystemParametersInfo(
                win32con.SPI_SETDESKWALLPAPER,
                0,
                image_path,
                win32con.SPIF_UPDATEINIFILE | win32con.SPIF_SENDCHANGE,
            )
            return bool(result)
        except Exception as e:
            print(f"Error setting wallpaper via Windows API: {e}")
            return False
