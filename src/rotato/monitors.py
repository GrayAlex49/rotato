"""Monitor detection and management."""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MonitorInfo:
    """Information about a monitor"""

    handle: int
    width: int
    height: int
    x: int
    y: int
    is_primary: bool
    name: str

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height


class MonitorManager:
    """Manages monitor detection and information"""

    def __init__(self):
        self.monitors: List[MonitorInfo] = []
        self.detect_monitors()

    def detect_monitors(self):
        """Detect all connected monitors - platform-specific implementation"""
        from .platform import get_platform_detector

        detector = get_platform_detector()
        self.monitors = detector.detect_monitors()

        print(f"Detected {len(self.monitors)} monitors")
        for i, monitor in enumerate(self.monitors):
            primary = "(Primary)" if monitor.is_primary else ""
            print(f"  Monitor {i+1}: {monitor.width}x{monitor.height} {primary}")

    def get_monitor_by_name(self, name: str) -> Optional[MonitorInfo]:
        """Get monitor by device name"""
        for monitor in self.monitors:
            if monitor.name == name:
                return monitor
        return None
