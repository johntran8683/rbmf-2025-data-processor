"""Data processing utilities for RBMF files."""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
from loguru import logger

from .config import settings


class DataProcessor:
    """Processor for RBMF data files."""
    
    def __init__(self):
        """Initialize the data processor."""
        self.supported_formats = {'.xlsx', '.xls', '.csv', '.json'}
    
    def process_file(self, file_path: Path) -> Dict[str, Any]:
        """Process a single file and return metadata."""
        logger.info(f"Processing file: {file_path}")
        
        file_info = {
            'file_path': str(file_path),
            'file_name': file_path.name,
            'file_size': file_path.stat().st_size,
            'file_extension': file_path.suffix.lower(),
            'processed': False,
            'error': None,
            'data_summary': {}
        }
        
        try:
            # Detect file type by content if no extension
            file_type = self._detect_file_type(file_path)
            
            if file_type == 'excel':
                file_info['data_summary'] = self._process_excel_file(file_path)
            elif file_type == 'csv':
                file_info['data_summary'] = self._process_csv_file(file_path)
            elif file_type == 'json':
                file_info['data_summary'] = self._process_json_file(file_path)
            else:
                logger.warning(f"Unsupported file format: {file_path.suffix}")
                file_info['error'] = f"Unsupported format: {file_path.suffix}"
                return file_info
            
            file_info['processed'] = True
            logger.info(f"Successfully processed: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Error processing {file_path.name}: {e}")
            file_info['error'] = str(e)
        
        return file_info
    
    def _detect_file_type(self, file_path: Path) -> str:
        """Detect file type by content and extension."""
        # First check by extension
        if file_path.suffix.lower() in {'.xlsx', '.xls'}:
            return 'excel'
        elif file_path.suffix.lower() == '.csv':
            return 'csv'
        elif file_path.suffix.lower() == '.json':
            return 'json'
        
        # If no extension, try to detect by content
        try:
            import magic
            mime_type = magic.from_file(str(file_path), mime=True)
            
            if mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                           'application/vnd.ms-excel']:
                return 'excel'
            elif mime_type == 'text/csv':
                return 'csv'
            elif mime_type == 'application/json':
                return 'json'
        except ImportError:
            # Fallback: try to read as Excel first
            try:
                pd.read_excel(file_path, nrows=1)
                return 'excel'
            except:
                try:
                    pd.read_csv(file_path, nrows=1)
                    return 'csv'
                except:
                    try:
                        import json
                        with open(file_path, 'r') as f:
                            json.load(f)
                        return 'json'
                    except:
                        pass
        
        return 'unknown'
    
    def _process_excel_file(self, file_path: Path) -> Dict[str, Any]:
        """Process Excel file and return summary."""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            sheets_info = {}
            
            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                sheets_info[sheet_name] = {
                    'rows': len(df),
                    'columns': len(df.columns),
                    'column_names': df.columns.tolist(),
                    'data_types': df.dtypes.to_dict(),
                    'null_counts': df.isnull().sum().to_dict()
                }
            
            return {
                'file_type': 'excel',
                'sheets': sheets_info,
                'total_sheets': len(excel_file.sheet_names)
            }
            
        except Exception as e:
            logger.error(f"Error processing Excel file {file_path}: {e}")
            raise
    
    def _process_csv_file(self, file_path: Path) -> Dict[str, Any]:
        """Process CSV file and return summary."""
        try:
            # Try to detect encoding
            encodings = ['utf-8', 'latin-1', 'cp1252']
            df = None
            
            for encoding in encodings:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            
            if df is None:
                raise ValueError("Could not decode CSV file with any supported encoding")
            
            return {
                'file_type': 'csv',
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': df.columns.tolist(),
                'data_types': df.dtypes.to_dict(),
                'null_counts': df.isnull().sum().to_dict()
            }
            
        except Exception as e:
            logger.error(f"Error processing CSV file {file_path}: {e}")
            raise
    
    def _process_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Process JSON file and return summary."""
        try:
            import json
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, list):
                return {
                    'file_type': 'json',
                    'data_type': 'array',
                    'length': len(data),
                    'sample_keys': list(data[0].keys()) if data and isinstance(data[0], dict) else None
                }
            elif isinstance(data, dict):
                return {
                    'file_type': 'json',
                    'data_type': 'object',
                    'keys': list(data.keys()),
                    'key_count': len(data)
                }
            else:
                return {
                    'file_type': 'json',
                    'data_type': type(data).__name__,
                    'value': str(data)[:100]  # First 100 characters
                }
                
        except Exception as e:
            logger.error(f"Error processing JSON file {file_path}: {e}")
            raise
    
    def process_directory(self, directory_path: Path) -> List[Dict[str, Any]]:
        """Process all supported files in a directory."""
        logger.info(f"Processing directory: {directory_path}")
        
        if not directory_path.exists():
            logger.error(f"Directory does not exist: {directory_path}")
            return []
        
        results = []
        
        # Find all files (including those without extensions)
        for file_path in directory_path.rglob('*'):
            if file_path.is_file():
                # Skip certain files
                if file_path.name in ['gdown_download_summary.json', 'processing_report.json']:
                    continue
                result = self.process_file(file_path)
                results.append(result)
        
        logger.info(f"Processed {len(results)} files from {directory_path}")
        return results
    
    def generate_summary_report(self, processing_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary report from processing results."""
        total_files = len(processing_results)
        successful_files = sum(1 for result in processing_results if result['processed'])
        failed_files = total_files - successful_files
        
        # Group by file type
        file_types = {}
        for result in processing_results:
            file_ext = result['file_extension']
            if file_ext not in file_types:
                file_types[file_ext] = {'count': 0, 'successful': 0, 'failed': 0}
            
            file_types[file_ext]['count'] += 1
            if result['processed']:
                file_types[file_ext]['successful'] += 1
            else:
                file_types[file_ext]['failed'] += 1
        
        return {
            'total_files': total_files,
            'successful_files': successful_files,
            'failed_files': failed_files,
            'success_rate': (successful_files / total_files * 100) if total_files > 0 else 0,
            'file_types': file_types,
            'processing_results': processing_results
        }
