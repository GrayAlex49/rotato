"""Tests for configuration management."""

import tempfile
from pathlib import Path

import pytest

from rotato.config import ConfigManager, FilterConfig, MonitorConfig


def test_filter_config_defaults():
    """Test FilterConfig default values"""
    config = FilterConfig()
    assert config.min_width is None
    assert config.aspect_ratio_tolerance == 0.1


def test_monitor_config_creation():
    """Test MonitorConfig creation"""
    config = MonitorConfig(
        monitor_name="test",
        image_sources=["/path/to/images"],
        recursive=True,
        rotation_interval_minutes=5,
    )
    assert config.monitor_name == "test"
    assert config.rotation_interval_minutes == 5
    assert config.filters is not None


def test_config_manager_creates_default():
    """Test that ConfigManager creates default config if none exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.yaml"
        manager = ConfigManager(str(config_path))

        assert not config_path.exists()  # File doesn't exist yet

        config = manager.load_config()

        assert config_path.exists()  # File was created
        assert "global" in config
        assert "monitors" in config


def test_config_manager_load_save():
    """Test config loading and saving"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "test_config.yaml"
        manager = ConfigManager(str(config_path))

        # Create custom config
        custom_config = {
            "global": {"rotation_interval_minutes": 20},
            "monitors": [{"monitor_name": "test", "image_sources": ["/test"]}],
        }

        # Save and reload
        manager.save_config(custom_config)
        loaded_config = manager.load_config()

        assert loaded_config["global"]["rotation_interval_minutes"] == 20
        assert loaded_config["monitors"][0]["monitor_name"] == "test"
