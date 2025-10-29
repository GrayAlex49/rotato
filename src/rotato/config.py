"""Configuration management for Rotato."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import yaml


@dataclass
class FilterConfig:
    """Image filtering configuration"""

    min_width: Optional[int] = None
    max_width: Optional[int] = None
    min_height: Optional[int] = None
    max_height: Optional[int] = None
    aspect_ratios: Optional[List[float]] = None  # List of acceptable aspect ratios
    aspect_ratio_tolerance: float = 0.1  # Tolerance for aspect ratio matching
    brightness_range: Optional[Tuple[float, float]] = None  # (min, max) brightness 0-255
    max_file_size_mb: Optional[float] = None


@dataclass
class MonitorConfig:
    """Configuration for a specific monitor"""

    monitor_name: str
    image_sources: List[str]  # Paths to folders or individual images
    recursive: bool = True
    filters: FilterConfig = None
    rotation_interval_minutes: int = 10

    def __post_init__(self):
        if self.filters is None:
            self.filters = FilterConfig()
        elif isinstance(self.filters, dict):
            # Convert dict to FilterConfig if loaded from YAML
            self.filters = FilterConfig(**self.filters)


class ConfigManager:
    """Manages YAML configuration file"""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = Path(config_path)
        self.default_config = {
            "global": {
                "rotation_interval_minutes": 10,
                "cache_file": "image_cache.json",
                "max_recursion_depth": 10,
                "supported_formats": [".jpg", ".jpeg", ".png", ".webp"],
                "hotkeys": {
                    "trigger_rotation": "ctrl+alt+w",
                    "open_current_image": "ctrl+alt+o",
                },
            },
            "monitors": [
                {
                    "monitor_name": "auto",  # 'auto' means any monitor
                    "image_sources": ["C:/Users/Public/Pictures"],
                    "recursive": True,
                    "rotation_interval_minutes": 10,
                    "filters": {
                        "min_width": 1920,
                        "min_height": 1080,
                        "aspect_ratios": [1.78, 0.56],  # 16:9 and 9:16
                        "aspect_ratio_tolerance": 0.1,
                        "brightness_range": [50, 200],
                    },
                }
            ],
        }

    def load_config(self) -> Dict:
        """Load configuration from YAML file"""
        if not self.config_path.exists():
            self.save_config(self.default_config)
            return self.default_config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return self.default_config

    def save_config(self, config: Dict):
        """Save configuration to YAML file"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
