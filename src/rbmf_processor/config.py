"""Configuration management for RBMF Data Processor."""

import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Google Drive Configuration
    google_drive_folder_url: str = Field(
        default="https://drive.google.com/drive/folders/1h2SfH2gCGlRAmV9REkqe-5sacDQ6IghC",
        env="GOOGLE_DRIVE_FOLDER_URL"
    )
    
    # Application Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    data_dir: Path = Field(default=Path("/app/data"), env="DATA_DIR")
    log_dir: Path = Field(default=Path("/app/logs"), env="LOG_DIR")
    
    # Performance Configuration
    quiet_mode: bool = Field(default=False, env="QUIET_MODE")  # Reduce console output
    verbose_logging: bool = Field(default=True, env="VERBOSE_LOGGING")  # Detailed file logging
    
    # Processing Configuration
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    
    # Performance Configuration
    max_workers: Optional[int] = Field(default=None, env="MAX_WORKERS")  # None = auto-detect
    parallel_processing: bool = Field(default=True, env="PARALLEL_PROCESSING")
    memory_optimization: bool = Field(default=True, env="MEMORY_OPTIMIZATION")
    excel_chunk_size: int = Field(default=1000, env="EXCEL_CHUNK_SIZE")
    max_memory_usage: float = Field(default=0.8, env="MAX_MEMORY_USAGE")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()
