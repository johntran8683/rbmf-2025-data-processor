"""Tests for configuration module."""

import pytest
from pathlib import Path
from src.rbmf_processor.config import Settings


def test_settings_default_values():
    """Test that settings have correct default values."""
    settings = Settings()
    
    assert settings.google_drive_folder_id == "1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC"
    assert settings.google_credentials_file == "credentials.json"
    assert settings.google_token_file == "token.json"
    assert settings.log_level == "INFO"
    assert settings.batch_size == 10
    assert settings.max_retries == 3


def test_settings_directory_creation():
    """Test that directories are created when settings are initialized."""
    settings = Settings()
    
    assert settings.data_dir.exists()
    assert settings.log_dir.exists()


def test_settings_custom_values():
    """Test that custom values can be set."""
    custom_settings = Settings(
        google_drive_folder_id="custom_folder_id",
        log_level="DEBUG",
        batch_size=20
    )
    
    assert custom_settings.google_drive_folder_id == "custom_folder_id"
    assert custom_settings.log_level == "DEBUG"
    assert custom_settings.batch_size == 20
