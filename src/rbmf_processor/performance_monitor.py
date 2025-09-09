"""Performance monitoring and reporting for RBMF processing."""

import time
import psutil
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger
from datetime import datetime
import json

class PerformanceMonitor:
    """Monitors and reports performance metrics."""
    
    def __init__(self):
        """Initialize performance monitor."""
        self.metrics = {
            'start_time': None,
            'end_time': None,
            'file_metrics': [],
            'system_metrics': [],
            'memory_usage': [],
            'cpu_usage': []
        }
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start performance monitoring."""
        self.metrics['start_time'] = time.time()
        logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring."""
        self.metrics['end_time'] = time.time()
        logger.info("Performance monitoring stopped")
    
    def record_file_processing(self, file_name: str, start_time: float, 
                             end_time: float, success: bool, file_size: int = 0):
        """Record file processing metrics.
        
        Args:
            file_name: Name of processed file
            start_time: Processing start time
            end_time: Processing end time
            success: Whether processing was successful
            file_size: Size of file in bytes
        """
        processing_time = end_time - start_time
        
        self.metrics['file_metrics'].append({
            'file_name': file_name,
            'processing_time': processing_time,
            'success': success,
            'file_size_mb': file_size / 1024 / 1024,
            'throughput_mb_per_sec': (file_size / 1024 / 1024) / processing_time if processing_time > 0 else 0
        })
    
    def record_system_metrics(self):
        """Record current system metrics."""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        
        self.metrics['system_metrics'].append({
            'timestamp': time.time(),
            'cpu_percent': cpu_percent,
            'memory_percent': memory.percent,
            'memory_available_gb': memory.available / 1024 / 1024 / 1024,
            'memory_used_gb': memory.used / 1024 / 1024 / 1024
        })
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report.
        
        Returns:
            Performance report dictionary
        """
        if not self.metrics['file_metrics']:
            return {'error': 'No file metrics recorded'}
        
        # Calculate file processing statistics
        successful_files = [f for f in self.metrics['file_metrics'] if f['success']]
        failed_files = [f for f in self.metrics['file_metrics'] if not f['success']]
        
        if successful_files:
            processing_times = [f['processing_time'] for f in successful_files]
            file_sizes = [f['file_size_mb'] for f in successful_files]
            throughputs = [f['throughput_mb_per_sec'] for f in successful_files]
            
            file_stats = {
                'total_files': len(self.metrics['file_metrics']),
                'successful_files': len(successful_files),
                'failed_files': len(failed_files),
                'success_rate': len(successful_files) / len(self.metrics['file_metrics']) * 100,
                'total_processing_time': sum(processing_times),
                'average_processing_time': sum(processing_times) / len(processing_times),
                'min_processing_time': min(processing_times),
                'max_processing_time': max(processing_times),
                'total_file_size_mb': sum(file_sizes),
                'average_file_size_mb': sum(file_sizes) / len(file_sizes),
                'average_throughput_mb_per_sec': sum(throughputs) / len(throughputs),
                'files_per_second': len(successful_files) / self.metrics['total_processing_time'] if self.metrics['total_processing_time'] > 0 else 0
            }
        else:
            file_stats = {
                'total_files': len(self.metrics['file_metrics']),
                'successful_files': 0,
                'failed_files': len(failed_files),
                'success_rate': 0
            }
        
        # Calculate system metrics
        if self.metrics['system_metrics']:
            cpu_values = [m['cpu_percent'] for m in self.metrics['system_metrics']]
            memory_values = [m['memory_percent'] for m in self.metrics['system_metrics']]
            
            system_stats = {
                'average_cpu_percent': sum(cpu_values) / len(cpu_values),
                'max_cpu_percent': max(cpu_values),
                'average_memory_percent': sum(memory_values) / len(memory_values),
                'max_memory_percent': max(memory_values),
                'peak_memory_used_gb': max([m['memory_used_gb'] for m in self.metrics['system_metrics']])
            }
        else:
            system_stats = {}
        
        # Overall timing
        total_time = self.metrics['end_time'] - self.metrics['start_time'] if self.metrics['end_time'] else 0
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_execution_time': total_time,
            'file_statistics': file_stats,
            'system_statistics': system_stats,
            'performance_summary': self._generate_performance_summary(file_stats, system_stats, total_time)
        }
        
        return report
    
    def _generate_performance_summary(self, file_stats: Dict, system_stats: Dict, total_time: float) -> Dict[str, str]:
        """Generate human-readable performance summary.
        
        Args:
            file_stats: File processing statistics
            system_stats: System statistics
            total_time: Total execution time
            
        Returns:
            Performance summary
        """
        summary = {}
        
        # Processing efficiency
        if file_stats.get('files_per_second', 0) > 0:
            summary['processing_speed'] = f"{file_stats['files_per_second']:.2f} files/second"
        else:
            summary['processing_speed'] = "Unable to calculate"
        
        # Success rate
        summary['success_rate'] = f"{file_stats.get('success_rate', 0):.1f}%"
        
        # Average processing time
        if file_stats.get('average_processing_time', 0) > 0:
            summary['avg_file_time'] = f"{file_stats['average_processing_time']:.2f} seconds/file"
        else:
            summary['avg_file_time'] = "Unable to calculate"
        
        # System resource usage
        if system_stats:
            summary['avg_cpu_usage'] = f"{system_stats.get('average_cpu_percent', 0):.1f}%"
            summary['avg_memory_usage'] = f"{system_stats.get('average_memory_percent', 0):.1f}%"
            summary['peak_memory'] = f"{system_stats.get('peak_memory_used_gb', 0):.2f} GB"
        
        # Performance recommendations
        recommendations = []
        
        if file_stats.get('success_rate', 0) < 90:
            recommendations.append("Consider investigating failed files")
        
        if system_stats and system_stats.get('average_cpu_percent', 0) < 50:
            recommendations.append("Consider increasing parallel processing")
        
        if system_stats and system_stats.get('average_memory_percent', 0) > 80:
            recommendations.append("Consider reducing memory usage or increasing system memory")
        
        if file_stats.get('average_processing_time', 0) > 30:
            recommendations.append("Consider optimizing file processing or using faster storage")
        
        summary['recommendations'] = recommendations
        
        return summary
    
    def save_report(self, output_path: Path):
        """Save performance report to file.
        
        Args:
            output_path: Path to save report
        """
        report = self.generate_performance_report()
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Performance report saved to: {output_path}")
    
    def print_summary(self):
        """Print performance summary to console."""
        report = self.generate_performance_report()
        summary = report.get('performance_summary', {})
        
        print("\n" + "="*60)
        print("PERFORMANCE SUMMARY")
        print("="*60)
        
        for key, value in summary.items():
            if key != 'recommendations':
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        if summary.get('recommendations'):
            print("\nRecommendations:")
            for rec in summary['recommendations']:
                print(f"  • {rec}")
        
        print("="*60)
