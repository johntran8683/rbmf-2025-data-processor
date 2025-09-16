"""Parallel processing utilities for RBMF data transformation."""

import multiprocessing as mp
from pathlib import Path
from typing import List, Dict, Any, Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from loguru import logger
import time

class ParallelProcessor:
    """Handles parallel processing of RBMF files."""
    
    def __init__(self, max_workers: int = None):
        """Initialize parallel processor.
        
        Args:
            max_workers: Maximum number of worker processes. 
                        If None, uses CPU count - 1.
        """
        self.max_workers = max_workers or max(1, mp.cpu_count() - 1)
        logger.info(f"Initialized parallel processor with {self.max_workers} workers")
    
    def process_files_parallel(self, 
                             file_tasks: List[Dict[str, Any]], 
                             process_func: Callable,
                             chunk_size: int = 1) -> List[Dict[str, Any]]:
        """Process files in parallel.
        
        Args:
            file_tasks: List of file processing tasks
            process_func: Function to process each file
            chunk_size: Number of files per worker (for memory optimization)
            
        Returns:
            List of processing results
        """
        results = []
        start_time = time.time()
        
        logger.info(f"Starting parallel processing of {len(file_tasks)} files with {self.max_workers} workers")
        
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(process_func, task): task 
                for task in file_tasks
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result.get('success', False):
                        logger.info(f"✅ Completed: {task.get('file_name', 'Unknown')}")
                    else:
                        logger.error(f"❌ Failed: {task.get('file_name', 'Unknown')} - {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    logger.error(f"❌ Exception processing {task.get('file_name', 'Unknown')}: {e}")
                    results.append({
                        'file_name': task.get('file_name', 'Unknown'),
                        'success': False,
                        'error': str(e)
                    })
        
        elapsed_time = time.time() - start_time
        successful = sum(1 for r in results if r.get('success', False))
        
        logger.info(f"Parallel processing completed in {elapsed_time:.2f}s")
        logger.info(f"Successfully processed: {successful}/{len(file_tasks)} files")
        logger.info(f"Average time per file: {elapsed_time/len(file_tasks):.2f}s")
        
        return results

def create_file_task(source_file: Path, output_file: Path, transformer_config: Dict[str, Any]) -> Dict[str, Any]:
    """Create a file processing task for parallel execution.
    
    Args:
        source_file: Path to source file
        output_file: Path to output file
        transformer_config: Configuration for transformer
        
    Returns:
        Task dictionary
    """
    return {
        'source_file': str(source_file),
        'output_file': str(output_file),
        'file_name': source_file.name,
        'config': transformer_config
    }

def process_single_file_worker(task: Dict[str, Any]) -> Dict[str, Any]:
    """Worker function for processing a single file.
    
    This function runs in a separate process and needs to be importable.
    
    Args:
        task: File processing task
        
    Returns:
        Processing result
    """
    try:
        from .rbmf_transformer import RBMFTransformer
        
        source_file = Path(task['source_file'])
        output_file = Path(task['output_file'])
        config = task['config']
        
        # Create transformer instance
        transformer = RBMFTransformer(
            data_dir=Path(config['data_dir']),
            include_steps=config['include_steps'],
            target_folders=None
        )
        
        # Load required data
        transformer.load_template_instructions()
        transformer.load_file_to_project_id_mapping()
        
        # Process file
        apply_filter = config.get('apply_filter', False)
        success = transformer.create_output_file(source_file, output_file, apply_filter=apply_filter)
        
        return {
            'file_name': task['file_name'],
            'success': success,
            'output_file': str(output_file) if success else None,
            'error': None if success else "Failed to create output file"
        }
        
    except Exception as e:
        return {
            'file_name': task['file_name'],
            'success': False,
            'output_file': None,
            'error': str(e)
        }
