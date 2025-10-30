#!/usr/bin/env python3
"""
Monitor Detection Helper Script
Run this on Windows to detect your monitor device names for config.yaml
"""

import sys


def detect_monitors():
    """Detect monitors and display their information"""
    try:
        # Import Windows-specific modules
        import win32api
        import win32con

        print("=" * 60)
        print("ROTATO - Monitor Detection")
        print("=" * 60)
        print()

        monitors = []

        def enum_callback(hmonitor, hdc, rect, data):
            monitor_info = win32api.GetMonitorInfo(hmonitor)
            device_name = monitor_info["Device"]

            # Get monitor dimensions
            left, top, right, bottom = rect
            width = right - left
            height = bottom - top
            is_primary = monitor_info["Flags"] & win32con.MONITORINFOF_PRIMARY != 0
            aspect_ratio = width / height

            monitor = {
                "device_name": device_name,
                "width": width,
                "height": height,
                "x": left,
                "y": top,
                "is_primary": is_primary,
                "aspect_ratio": aspect_ratio,
            }

            monitors.append(monitor)
            return True

        # Detect monitors
        win32api.EnumDisplayMonitors(None, None, enum_callback, None)

        print(f"Detected {len(monitors)} monitor(s):\n")

        for i, monitor in enumerate(monitors, 1):
            primary_text = " (PRIMARY)" if monitor["is_primary"] else ""
            print(f"Monitor {i}{primary_text}:")
            print(f"  Device Name: {monitor['device_name']}")
            print(f"  Resolution:  {monitor['width']}x{monitor['height']}")
            print(f"  Aspect Ratio: {monitor['aspect_ratio']:.2f}")
            print(f"  Position:    X={monitor['x']}, Y={monitor['y']}")

            # Identify common aspect ratios
            ar = monitor["aspect_ratio"]
            if 2.3 <= ar <= 2.5:
                ar_name = "21:9 Ultrawide"
            elif 1.7 <= ar <= 1.85:
                ar_name = "16:9 Standard"
            elif 1.55 <= ar <= 1.65:
                ar_name = "16:10"
            elif 0.5 <= ar <= 0.65:
                ar_name = "9:16 Vertical"
            elif 1.3 <= ar <= 1.4:
                ar_name = "4:3 Classic"
            else:
                ar_name = "Custom"

            print(f"  Type:        {ar_name}")
            print()

        # Print configuration example
        print("=" * 60)
        print("CONFIGURATION FOR config.yaml")
        print("=" * 60)
        print()
        print("Copy and paste this into your config.yaml:\n")
        print("monitors:")

        for i, monitor in enumerate(monitors, 1):
            ar = monitor["aspect_ratio"]
            device_name_escaped = monitor["device_name"].replace("\\", "\\\\")

            print(f"  # Monitor {i}: {monitor['width']}x{monitor['height']}")
            print(f"  - monitor_name: {device_name_escaped}")
            print(f"    image_sources:")
            print(f"      - E:\\wallpapers")
            print(f"    recursive: true")
            print(f"    rotation_interval_minutes: 10")
            print(f"    filters:")
            print(f"      min_width: {monitor['width']}")
            print(f"      min_height: {monitor['height']}")
            print(f"      aspect_ratios: [{ar:.2f}]")
            print(f"      aspect_ratio_tolerance: 0.15")
            print(f"      brightness_range: [40, 220]")
            print(f"      max_file_size_mb: 30")
            print()

        print("=" * 60)
        print("NEXT STEPS:")
        print("=" * 60)
        print("1. Copy the configuration above")
        print("2. Edit your config.yaml file")
        print("3. Replace the 'monitors:' section with the configuration above")
        print("4. Adjust the image_sources paths as needed")
        print("5. Run Rotato and enjoy your custom wallpapers!")
        print()

    except ImportError:
        print("ERROR: This script requires pywin32 to be installed.")
        print("Install it with: pip install pywin32")
        print()
        print("Or install Rotato with all dependencies: pip install -e .")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: Failed to detect monitors: {e}")
        print()
        print("Make sure you're running this on Windows.")
        sys.exit(1)


if __name__ == "__main__":
    detect_monitors()
