"""Google Drive downloader using gdown library."""

import gdown
from pathlib import Path
from typing import List, Optional
from loguru import logger

from .config import settings


class GDownClient:
    """Client for downloading Google Drive files using gdown."""
    
    def __init__(self):
        """Initialize the gdown client."""
        self.data_dir = settings.data_dir
    
    def download_folder(self, folder_url: str, output_dir: Path = None) -> List[Path]:
        """Download a Google Drive folder using gdown."""
        if output_dir is None:
            output_dir = self.data_dir / "gdown_download"
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Downloading folder from: {folder_url}")
        logger.info(f"Output directory: {output_dir}")
        
        try:
            # Download the folder
            gdown.download_folder(
                folder_url,
                output=str(output_dir),
                quiet=False,
                use_cookies=False
            )
            
            # Get list of downloaded files
            downloaded_files = list(output_dir.rglob('*'))
            downloaded_files = [f for f in downloaded_files if f.is_file()]
            
            logger.info(f"Downloaded {len(downloaded_files)} files successfully")
            return downloaded_files
            
        except Exception as e:
            logger.error(f"Error downloading folder: {e}")
            raise
    
    def download_file(self, file_url: str, output_path: Path = None) -> Path:
        """Download a single Google Drive file."""
        if output_path is None:
            output_path = self.data_dir / "gdown_download"
            output_path.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Downloading file from: {file_url}")
        
        try:
            gdown.download(
                file_url,
                output=str(output_path),
                quiet=False
            )
            
            logger.info(f"File downloaded to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            raise
