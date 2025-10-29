"""Entry point for Rotato."""

import sys

from .core import DesktopBackgroundManager
from .platform import check_platform_support


def setup_autostart():
    """Setup automatic startup with Windows"""
    try:
        import winreg
        from pathlib import Path

        # Get path to current script
        script_path = str(Path(__file__).resolve())
        python_path = sys.executable

        # Create startup command
        startup_cmd = f'"{python_path}" -m rotato'

        # Add to Windows startup registry
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )

        winreg.SetValueEx(key, "Rotato", 0, winreg.REG_SZ, startup_cmd)

        winreg.CloseKey(key)
        print("Added Rotato to Windows startup")

    except Exception as e:
        print(f"Error setting up autostart: {e}")


def remove_autostart():
    """Remove from Windows startup"""
    try:
        import winreg

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE,
        )

        try:
            winreg.DeleteValue(key, "Rotato")
            print("Removed Rotato from Windows startup")
        except FileNotFoundError:
            print("Rotato was not in Windows startup")

        winreg.CloseKey(key)

    except Exception as e:
        print(f"Error removing autostart: {e}")


def main():
    """Main entry point"""
    # Check for command-line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--setup-autostart":
            setup_autostart()
            return
        elif command == "--remove-autostart":
            remove_autostart()
            return
        elif command == "--help":
            print("Rotato - Desktop Background Manager")
            print("\nUsage:")
            print("  rotato                    Run the application")
            print("  rotato --setup-autostart  Add to Windows startup")
            print("  rotato --remove-autostart Remove from Windows startup")
            print("  rotato --help            Show this help message")
            return
        else:
            print(f"Unknown command: {command}")
            print("Use --help for usage information")
            return

    # Check platform support
    if not check_platform_support():
        print("\nYou can help add support for your platform!")
        print("Visit: https://github.com/yourusername/rotato")
        sys.exit(1)

    # Run the application
    app = DesktopBackgroundManager()
    app.run()


if __name__ == "__main__":
    main()
