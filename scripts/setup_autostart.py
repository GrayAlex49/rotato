#!/usr/bin/env python3
"""Setup script for Windows autostart."""

import sys


def main():
    """Setup autostart"""
    from rotato.__main__ import setup_autostart

    print("Setting up Rotato to start with Windows...")
    setup_autostart()


if __name__ == "__main__":
    main()
