"""Memory optimization utilities for RBMF processing."""

import gc
import psutil
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
from loguru import logger
import pandas as pd
import openpyxl
from functools import lru_cache

class MemoryOptimizer:
    """Handles memory optimization for large-scale processing."""
    
    def __init__(self, max_memory_usage: float = 0.8):
        """Initialize memory optimizer.
        
        Args:
            max_memory_usage: Maximum memory usage ratio (0.0 to 1.0)
        """
        self.max_memory_usage = max_memory_usage
        self.template_cache = {}
        
    def check_memory_usage(self) -> Dict[str, float]:
        """Check current memory usage.
        
        Returns:
            Dictionary with memory usage information
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        system_memory = psutil.virtual_memory()
        
        return {
            'process_memory_mb': memory_info.rss / 1024 / 1024,
            'system_memory_usage': system_memory.percent / 100,
            'available_memory_mb': system_memory.available / 1024 / 1024
        }
    
    def should_cleanup_memory(self) -> bool:
        """Check if memory cleanup is needed.
        
        Returns:
            True if memory cleanup is recommended
        """
        memory_info = self.check_memory_usage()
        return memory_info['system_memory_usage'] > self.max_memory_usage
    
    def cleanup_memory(self):
        """Perform memory cleanup."""
        logger.info("Performing memory cleanup...")
        gc.collect()
        logger.info(f"Memory after cleanup: {self.check_memory_usage()}")
    
    @lru_cache(maxsize=1)
    def get_cached_template_workbook(self, template_path: str):
        """Get cached template workbook to avoid reloading.
        
        Args:
            template_path: Path to template file
            
        Returns:
            Cached openpyxl workbook
        """
        logger.debug(f"Loading template workbook: {template_path}")
        return openpyxl.load_workbook(template_path)
    
    def optimize_dataframe_memory(self, df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame memory usage.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Memory-optimized DataFrame
        """
        original_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        
        # Optimize data types
        for col in df.columns:
            col_type = df[col].dtype
            
            if col_type != 'object':
                c_min = df[col].min()
                c_max = df[col].max()
                
                if str(col_type)[:3] == 'int':
                    if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)
                else:
                    if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                        df[col] = df[col].astype(np.float16)
                    elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                        df[col] = df[col].astype(np.float32)
                    else:
                        df[col] = df[col].astype(np.float64)
            else:
                # Convert object columns to category if they have few unique values
                if df[col].nunique() / len(df) < 0.5:
                    df[col] = df[col].astype('category')
        
        optimized_memory = df.memory_usage(deep=True).sum() / 1024 / 1024
        reduction = (original_memory - optimized_memory) / original_memory * 100
        
        logger.debug(f"Memory optimization: {original_memory:.2f}MB -> {optimized_memory:.2f}MB ({reduction:.1f}% reduction)")
        
        return df

def stream_excel_sheet(file_path: Path, sheet_name: str, chunk_size: int = 1000):
    """Stream Excel sheet data in chunks to reduce memory usage.
    
    Args:
        file_path: Path to Excel file
        sheet_name: Name of sheet to stream
        chunk_size: Number of rows per chunk
        
    Yields:
        DataFrame chunks
    """
    try:
        excel_file = pd.ExcelFile(file_path)
        total_rows = len(pd.read_excel(file_path, sheet_name=sheet_name, nrows=0))
        
        for start_row in range(0, total_rows, chunk_size):
            chunk = pd.read_excel(
                file_path, 
                sheet_name=sheet_name, 
                skiprows=start_row,
                nrows=chunk_size
            )
            
            if chunk.empty:
                break
                
            yield chunk
            
    except Exception as e:
        logger.error(f"Error streaming Excel sheet {sheet_name} from {file_path}: {e}")
        raise
