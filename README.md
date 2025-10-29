# Rotato 🖼️

A lightweight, intelligent wallpaper rotation manager for Windows with multi-monitor support, advanced filtering, and system tray integration.

## Features

- **🖥️ Multi-Monitor Support**: Independent wallpaper rotation for each monitor
- **🎨 Smart Filtering**: Filter images by resolution, aspect ratio, brightness, and file size
- **⚡ Fast**: Intelligent image caching for quick startup and filtering
- **⌨️ Hotkeys**: Global keyboard shortcuts for instant control
- **🔄 Flexible Rotation**: Per-monitor rotation intervals
- **📁 Recursive Scanning**: Automatically discover images in nested folders
- **🎯 System Tray**: Convenient system tray icon for quick access
- **🔧 YAML Configuration**: Easy-to-edit configuration file
- **🚀 Auto-Start**: Optional Windows startup integration

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows (Linux support planned)

### Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is the fastest Python package manager:

```bash
# Install uv (if not already installed)
pip install uv

# Clone the repository
git clone https://github.com/yourusername/rotato.git
cd rotato

# Install in development mode
uv pip install -e .

# Or install with development dependencies
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/rotato.git
cd rotato

# Install in development mode
pip install -e .
```

## Quick Start

1. **Configure your image sources**: Edit `config.yaml` (created on first run)

2. **Run Rotato**:
   ```bash
   rotato
   # or
   python -m rotato
   ```

3. **Set up auto-start** (optional):
   ```bash
   rotato --setup-autostart
   ```

## Configuration

Rotato uses a YAML configuration file (`config.yaml`) for settings. On first run, a default configuration will be created.

### Example Configuration

```yaml
global:
  rotation_interval_minutes: 10
  cache_file: image_cache.json
  max_recursion_depth: 10
  supported_formats:
    - .jpg
    - .jpeg
    - .png
    - .webp
  hotkeys:
    trigger_rotation: ctrl+alt+w
    open_current_image: ctrl+alt+o

monitors:
  - monitor_name: auto  # 'auto' applies to all monitors
    image_sources:
      - C:/Users/YourName/Pictures/Wallpapers
      - D:/Photos
    recursive: true
    rotation_interval_minutes: 10
    filters:
      min_width: 1920
      min_height: 1080
      aspect_ratios: [1.78, 0.56]  # 16:9 and 9:16
      aspect_ratio_tolerance: 0.1
      brightness_range: [50, 200]  # Avoid too dark or bright images
      max_file_size_mb: 10
```

### Filter Options

- **min_width/max_width**: Minimum/maximum image width in pixels
- **min_height/max_height**: Minimum/maximum image height in pixels
- **aspect_ratios**: List of acceptable aspect ratios (e.g., 1.78 for 16:9, 0.56 for 9:16)
- **aspect_ratio_tolerance**: Tolerance for aspect ratio matching (default: 0.1)
- **brightness_range**: [min, max] average brightness (0-255)
- **max_file_size_mb**: Maximum file size in megabytes

### Common Aspect Ratios

- 16:9 = 1.78 (most common widescreen)
- 21:9 = 2.33 (ultrawide)
- 16:10 = 1.6 (some laptops)
- 9:16 = 0.56 (vertical/portrait)
- 4:3 = 1.33 (older displays)

## Usage

### Command Line

```bash
# Run Rotato
rotato

# Set up Windows auto-start
rotato --setup-autostart

# Remove from Windows auto-start
rotato --remove-autostart

# Show help
rotato --help
```

### Hotkeys

Default hotkeys (configurable in `config.yaml`):

- **Ctrl+Alt+W**: Trigger immediate wallpaper rotation
- **Ctrl+Alt+O**: Open current wallpaper in File Explorer

### System Tray

Right-click the system tray icon for quick access to:

- Rotate Now
- Open Current Image
- Reload Config
- Exit

## Development

### Project Structure

```
rotato/
├── src/rotato/          # Main package
│   ├── cache.py         # Image caching
│   ├── config.py        # Configuration management
│   ├── core.py          # Main application logic
│   ├── images.py        # Image discovery & filtering
│   ├── monitors.py      # Monitor detection
│   ├── wallpaper.py     # Wallpaper management
│   └── platform/        # Platform-specific implementations
│       ├── windows.py   # Windows APIs
│       └── linux.py     # Linux (future)
├── tests/               # Unit tests
├── scripts/             # Utility scripts
└── pyproject.toml       # Project configuration
```

### Running Tests

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=rotato --cov-report=html
```

### Code Quality

```bash
# Format and lint with ruff
ruff check src/
ruff format src/

# Type checking with mypy
mypy src/
```

## Roadmap

- [ ] Linux support (GNOME, KDE, XFCE)
- [ ] macOS support
- [ ] GUI configuration tool
- [ ] Image effects (blur, darken, etc.)
- [ ] Per-monitor configuration profiles
- [ ] Integration with online wallpaper sources
- [ ] Scheduled wallpaper themes (time of day)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with ❤️ using modern Python tools
- Uses [Pillow](https://python-pillow.org/) for image processing
- Uses [pywin32](https://github.com/mhammond/pywin32) for Windows integration
- Uses [pystray](https://github.com/moses-palmer/pystray) for system tray
- Package management by [uv](https://github.com/astral-sh/uv)

## Support

Having issues? Please [open an issue](https://github.com/yourusername/rotato/issues) on GitHub.
