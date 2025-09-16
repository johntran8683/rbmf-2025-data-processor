"""Optimized RBMF transformer with performance improvements."""

import time
from pathlib import Path
from typing import Dict, List, Any, Optional
from loguru import logger

from .rbmf_transformer import RBMFTransformer
from .parallel_processor import ParallelProcessor, create_file_task, process_single_file_worker
from .memory_optimizer import MemoryOptimizer
from .excel_optimizer import ExcelOptimizer
from .config import settings

class OptimizedRBMFTransformer(RBMFTransformer):
    """Optimized RBMF transformer with performance improvements."""
    
    def __init__(self, data_dir: Path, include_steps: bool = False, target_folders: list = None, apply_filter: bool = False):
        """Initialize optimized transformer.
        
        Args:
            data_dir: Path to the data directory
            include_steps: Whether to include intermediate steps
            target_folders: List of target folders to process
            apply_filter: Whether to apply filtering to RBMF data
        """
        super().__init__(data_dir, include_steps, target_folders)
        self.apply_filter = apply_filter
        
        # Initialize performance components
        self.parallel_processor = ParallelProcessor(max_workers=settings.max_workers)
        self.memory_optimizer = MemoryOptimizer(max_memory_usage=settings.max_memory_usage)
        self.excel_optimizer = ExcelOptimizer()
        
        # Performance tracking
        self.processing_stats = {
            'total_files': 0,
            'processed_files': 0,
            'failed_files': 0,
            'start_time': None,
            'end_time': None
        }
    
    def process_folders_optimized(self) -> Dict[str, Any]:
        """Process all target folders with optimizations.
        
        Returns:
            Processing results and statistics
        """
        self.processing_stats['start_time'] = time.time()
        self.processing_stats['total_files'] = self._count_total_files()
        
        logger.info(f"Starting optimized processing of {len(self.target_folders)} folders")
        logger.info(f"Total files to process: {self.processing_stats['total_files']}")
        
        # Load shared resources once
        self.load_template_instructions()
        self.load_file_to_project_id_mapping()
        
        results = {
            'total_files': 0,
            'created_files': 0,
            'failed_files': 0,
            'mode': 'steps' if self.include_steps else 'final',
            'folder_results': {},
            'performance_stats': {}
        }
        
        for folder_name in self.target_folders:
            logger.info(f"Processing folder: {folder_name}")
            
            folder_result = self._process_folder_optimized(folder_name)
            results['folder_results'][folder_name] = folder_result
            
            # Update totals
            results['total_files'] += folder_result['files_processed']
            results['created_files'] += folder_result['files_created']
            results['failed_files'] += folder_result['files_failed']
            
            # Memory cleanup between folders
            if self.memory_optimizer.should_cleanup_memory():
                self.memory_optimizer.cleanup_memory()
        
        # Calculate performance stats
        self.processing_stats['end_time'] = time.time()
        results['performance_stats'] = self._calculate_performance_stats()
        
        logger.info(f"Optimized processing completed in {results['performance_stats']['total_time']:.2f}s")
        logger.info(f"Successfully processed: {results['created_files']}/{results['total_files']} files")
        
        return results
    
    def _process_folder_optimized(self, folder_name: str) -> Dict[str, Any]:
        """Process a single folder with optimizations.
        
        Args:
            folder_name: Name of folder to process
            
        Returns:
            Folder processing results
        """
        source_folder = self.data_dir / folder_name
        if self.include_steps:
            output_folder = self.output_dir / folder_name / "steps"
        elif self.apply_filter:
            output_folder = self.output_dir / folder_name / "final-filter"
        else:
            output_folder = self.output_dir / folder_name / "final"
        
        if not source_folder.exists():
            logger.warning(f"Source folder does not exist: {source_folder}")
            return {
                'files_processed': 0,
                'files_created': 0,
                'files_failed': 0,
                'file_results': []
            }
        
        # Create output directory
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Get all files to process
        files_to_process = list(source_folder.glob('*'))
        files_to_process = [f for f in files_to_process if f.is_file() and self._is_excel_file(f)]
        
        if not files_to_process:
            logger.warning(f"No Excel files found in {folder_name}")
            return {
                'files_processed': 0,
                'files_created': 0,
                'files_failed': 0,
                'file_results': []
            }
        
        # Create file tasks for parallel processing
        file_tasks = []
        for source_file in files_to_process:
            output_file = output_folder / source_file.name
            task = create_file_task(
                source_file=source_file,
                output_file=output_file,
                transformer_config={
                    'data_dir': str(self.data_dir),
                    'include_steps': self.include_steps,
                    'apply_filter': self.apply_filter
                }
            )
            file_tasks.append(task)
        
        # Process files in parallel or sequentially
        if settings.parallel_processing and len(file_tasks) > 1:
            logger.info(f"Processing {len(file_tasks)} files in parallel")
            file_results = self.parallel_processor.process_files_parallel(
                file_tasks=file_tasks,
                process_func=process_single_file_worker,
                chunk_size=1
            )
        else:
            logger.info(f"Processing {len(file_tasks)} files sequentially")
            file_results = []
            for task in file_tasks:
                result = process_single_file_worker(task)
                file_results.append(result)
        
        # Calculate folder statistics
        files_created = sum(1 for r in file_results if r.get('success', False))
        files_failed = len(file_results) - files_created
        
        return {
            'files_processed': len(file_results),
            'files_created': files_created,
            'files_failed': files_failed,
            'file_results': file_results
        }
    
    def _count_total_files(self) -> int:
        """Count total files to be processed.
        
        Returns:
            Total number of files
        """
        total = 0
        for folder_name in self.target_folders:
            source_folder = self.data_dir / folder_name
            if source_folder.exists():
                files = [f for f in source_folder.glob('*') if f.is_file() and self._is_excel_file(f)]
                total += len(files)
        return total
    
    def _calculate_performance_stats(self) -> Dict[str, Any]:
        """Calculate performance statistics.
        
        Returns:
            Performance statistics
        """
        total_time = self.processing_stats['end_time'] - self.processing_stats['start_time']
        files_per_second = self.processing_stats['processed_files'] / total_time if total_time > 0 else 0
        
        memory_info = self.memory_optimizer.check_memory_usage()
        
        return {
            'total_time': total_time,
            'files_per_second': files_per_second,
            'average_time_per_file': total_time / self.processing_stats['total_files'] if self.processing_stats['total_files'] > 0 else 0,
            'peak_memory_mb': memory_info['process_memory_mb'],
            'system_memory_usage': memory_info['system_memory_usage']
        }
