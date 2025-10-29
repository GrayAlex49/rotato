"""Main application logic for Rotato."""

import random
import sys
import threading
from pathlib import Path
from typing import Dict, List

try:
    import keyboard

    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: keyboard module not available. Hotkeys will not work.")

try:
    import pystray
    from PIL import Image as PILImage
    from pystray import MenuItem as item

    TRAY_AVAILABLE = True
except ImportError:
    TRAY_AVAILABLE = False
    print("Warning: pystray not available. System tray icon will not work.")

from .cache import ImageCache
from .config import ConfigManager, MonitorConfig
from .images import ImageManager
from .monitors import MonitorManager
from .wallpaper import WallpaperManager


class DesktopBackgroundManager:
    """Main application class"""

    def __init__(self, config_path: str = "config.yaml"):
        # Load configuration
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()

        # Initialize components
        cache_file = self.config["global"]["cache_file"]
        self.image_cache = ImageCache(cache_file)

        supported_formats = self.config["global"]["supported_formats"]
        max_depth = self.config["global"]["max_recursion_depth"]
        self.image_manager = ImageManager(self.image_cache, supported_formats, max_depth)

        self.monitor_manager = MonitorManager()
        self.wallpaper_manager = WallpaperManager()

        # Runtime state
        self.monitor_images: Dict[str, List[str]] = {}  # monitor_name -> filtered images
        self.rotation_timers: Dict[str, threading.Timer] = {}
        self.is_running = False

        # System tray
        self.tray_icon = None

        # Setup
        self.setup_hotkeys()
        self.discover_and_filter_images()

    def setup_hotkeys(self):
        """Setup global hotkeys"""
        if not KEYBOARD_AVAILABLE:
            print("Skipping hotkey setup (keyboard module not available)")
            return

        hotkeys = self.config["global"]["hotkeys"]

        try:
            keyboard.add_hotkey(hotkeys["trigger_rotation"], self.trigger_rotation)
            keyboard.add_hotkey(hotkeys["open_current_image"], self.open_current_image)
            print(f"Hotkeys registered: {hotkeys}")
        except Exception as e:
            print(f"Error setting up hotkeys: {e}")

    def discover_and_filter_images(self):
        """Discover and filter images for all monitors"""
        print("Discovering and filtering images...")

        monitor_configs = self.config["monitors"]

        for monitor_config_data in monitor_configs:
            monitor_config = MonitorConfig(**monitor_config_data)

            # Find matching monitor(s)
            if monitor_config.monitor_name == "auto":
                target_monitors = self.monitor_manager.monitors
            else:
                monitor = self.monitor_manager.get_monitor_by_name(
                    monitor_config.monitor_name
                )
                target_monitors = [monitor] if monitor else []

            for monitor in target_monitors:
                # Discover images
                images = self.image_manager.discover_images(
                    monitor_config.image_sources, monitor_config.recursive
                )

                # Filter images
                filtered_images = self.image_manager.filter_images(
                    images, monitor_config.filters, monitor
                )

                self.monitor_images[monitor.name] = filtered_images
                print(f"Monitor {monitor.name}: {len(filtered_images)} suitable images found")

        # Save cache
        self.image_cache.save_cache()

    def start_rotation(self):
        """Start wallpaper rotation for all monitors"""
        self.is_running = True

        # Set initial wallpapers and start timers
        for monitor in self.monitor_manager.monitors:
            self.rotate_wallpaper(monitor.name)

    def stop_rotation(self):
        """Stop wallpaper rotation"""
        self.is_running = False

        # Cancel all timers
        for timer in self.rotation_timers.values():
            if timer.is_alive():
                timer.cancel()
        self.rotation_timers.clear()

    def rotate_wallpaper(self, monitor_name: str):
        """Rotate wallpaper for specific monitor"""
        if not self.is_running:
            return

        images = self.monitor_images.get(monitor_name, [])
        if not images:
            print(f"No images available for monitor {monitor_name}")
            return

        # Select random image
        image_path = random.choice(images)

        # Get monitor
        monitor = None
        for m in self.monitor_manager.monitors:
            if m.name == monitor_name:
                monitor = m
                break

        if monitor:
            self.wallpaper_manager.set_wallpaper(monitor, image_path)

        # Schedule next rotation
        self.schedule_next_rotation(monitor_name)

    def schedule_next_rotation(self, monitor_name: str):
        """Schedule next wallpaper rotation"""
        if not self.is_running:
            return

        # Find interval for this monitor
        interval_minutes = self.config["global"]["rotation_interval_minutes"]

        # Check for monitor-specific interval
        for monitor_config_data in self.config["monitors"]:
            monitor_config = MonitorConfig(**monitor_config_data)
            if (
                monitor_config.monitor_name == monitor_name
                or monitor_config.monitor_name == "auto"
            ):
                interval_minutes = monitor_config.rotation_interval_minutes
                break

        # Cancel existing timer
        if monitor_name in self.rotation_timers:
            self.rotation_timers[monitor_name].cancel()

        # Schedule new timer
        timer = threading.Timer(
            interval_minutes * 60, lambda: self.rotate_wallpaper(monitor_name)
        )
        timer.start()
        self.rotation_timers[monitor_name] = timer

    def trigger_rotation(self):
        """Manually trigger wallpaper rotation for all monitors"""
        print("Triggering manual rotation...")
        for monitor in self.monitor_manager.monitors:
            self.rotate_wallpaper(monitor.name)

    def open_current_image(self):
        """Open current wallpaper image in Explorer"""
        import subprocess

        # For simplicity, get the first monitor's current wallpaper
        if self.monitor_manager.monitors:
            monitor_name = self.monitor_manager.monitors[0].name
            current_path = self.wallpaper_manager.get_current_wallpaper(monitor_name)

            if current_path and Path(current_path).exists():
                # Open file in Explorer and select it
                subprocess.run(["explorer", "/select,", current_path])
                print(f"Opened in Explorer: {Path(current_path).name}")
            else:
                print("No current wallpaper found")

    def create_tray_icon(self):
        """Create system tray icon"""
        if not TRAY_AVAILABLE:
            print("Skipping tray icon creation (pystray not available)")
            return

        try:
            # Create a simple icon (you can replace with a proper .ico file)
            icon_image = PILImage.new("RGB", (64, 64), color="blue")

            menu = pystray.Menu(
                item("Rotate Now", self.trigger_rotation),
                item("Open Current Image", self.open_current_image),
                item("Reload Config", self.reload_config),
                pystray.Menu.SEPARATOR,
                item("Exit", self.quit_application),
            )

            self.tray_icon = pystray.Icon(
                "rotato", icon_image, "Rotato - Desktop Background Manager", menu
            )

        except Exception as e:
            print(f"Error creating tray icon: {e}")

    def reload_config(self):
        """Reload configuration and restart rotation"""
        print("Reloading configuration...")
        self.stop_rotation()

        # Reload config
        self.config = self.config_manager.load_config()

        # Re-discover images
        self.discover_and_filter_images()

        # Restart rotation
        self.start_rotation()

    def quit_application(self):
        """Quit the application"""
        print("Shutting down...")
        self.stop_rotation()

        if self.tray_icon:
            self.tray_icon.stop()

        sys.exit(0)

    def run(self):
        """Run the application"""
        print("Starting Rotato - Desktop Background Manager...")

        # Create and run tray icon
        self.create_tray_icon()

        # Start rotation
        self.start_rotation()

        # Run tray icon (this blocks)
        if self.tray_icon:
            self.tray_icon.run()
        else:
            # Fallback: just keep running
            import time

            try:
                print("Running without tray icon. Press Ctrl+C to quit.")
                while self.is_running:
                    time.sleep(1)
            except KeyboardInterrupt:
                self.quit_application()
