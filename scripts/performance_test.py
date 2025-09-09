#!/usr/bin/env python3
"""Performance testing script for RBMF processor."""

import sys
import time
from pathlib import Path
from loguru import logger

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from rbmf_processor.optimized_transformer import OptimizedRBMFTransformer
from rbmf_processor.performance_monitor import PerformanceMonitor

def run_performance_test():
    """Run performance test with different configurations."""
    
    # Test configurations
    test_configs = [
        {
            'name': 'Sequential Processing',
            'parallel_processing': False,
            'max_workers': 1
        },
        {
            'name': 'Parallel Processing (2 workers)',
            'parallel_processing': True,
            'max_workers': 2
        },
        {
            'name': 'Parallel Processing (4 workers)',
            'parallel_processing': True,
            'max_workers': 4
        },
        {
            'name': 'Parallel Processing (Auto)',
            'parallel_processing': True,
            'max_workers': None
        }
    ]
    
    data_dir = Path("data")
    results = {}
    
    for config in test_configs:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing: {config['name']}")
        logger.info(f"{'='*60}")
        
        # Set configuration
        import os
        os.environ['PARALLEL_PROCESSING'] = str(config['parallel_processing'])
        if config['max_workers']:
            os.environ['MAX_WORKERS'] = str(config['max_workers'])
        
        # Initialize transformer
        transformer = OptimizedRBMFTransformer(
            data_dir=data_dir,
            include_steps=False,  # Use final mode for speed
            target_folders=["test"]  # Test with test folder first
        )
        
        # Initialize performance monitor
        monitor = PerformanceMonitor()
        
        try:
            # Run processing
            start_time = time.time()
            result = transformer.process_folders_optimized()
            end_time = time.time()
            
            # Record performance
            monitor.stop_monitoring()
            performance_report = monitor.generate_performance_report()
            
            # Store results
            results[config['name']] = {
                'config': config,
                'result': result,
                'performance': performance_report,
                'execution_time': end_time - start_time
            }
            
            # Print summary
            monitor.print_summary()
            
        except Exception as e:
            logger.error(f"Error in {config['name']}: {e}")
            results[config['name']] = {
                'config': config,
                'error': str(e),
                'execution_time': 0
            }
    
    # Generate comparison report
    generate_comparison_report(results)
    
    return results

def generate_comparison_report(results: dict):
    """Generate performance comparison report.
    
    Args:
        results: Dictionary of test results
    """
    logger.info(f"\n{'='*80}")
    logger.info("PERFORMANCE COMPARISON REPORT")
    logger.info(f"{'='*80}")
    
    print(f"{'Configuration':<30} {'Files/sec':<10} {'Success Rate':<12} {'Time (s)':<10}")
    print("-" * 80)
    
    for name, result in results.items():
        if 'error' in result:
            print(f"{name:<30} {'ERROR':<10} {'N/A':<12} {result['execution_time']:<10.2f}")
            continue
        
        performance = result.get('performance', {})
        file_stats = performance.get('file_statistics', {})
        
        files_per_sec = file_stats.get('files_per_second', 0)
        success_rate = file_stats.get('success_rate', 0)
        execution_time = result.get('execution_time', 0)
        
        print(f"{name:<30} {files_per_sec:<10.2f} {success_rate:<12.1f}% {execution_time:<10.2f}")
    
    # Find best configuration
    best_config = None
    best_throughput = 0
    
    for name, result in results.items():
        if 'error' not in result:
            performance = result.get('performance', {})
            file_stats = performance.get('file_statistics', {})
            throughput = file_stats.get('files_per_second', 0)
            
            if throughput > best_throughput:
                best_throughput = throughput
                best_config = name
    
    if best_config:
        logger.info(f"\n🏆 Best Configuration: {best_config}")
        logger.info(f"   Throughput: {best_throughput:.2f} files/second")
    
    # Save detailed report
    report_path = Path("performance_comparison_report.json")
    import json
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    logger.info(f"\n📊 Detailed report saved to: {report_path}")

if __name__ == "__main__":
    logger.info("Starting RBMF Performance Test")
    results = run_performance_test()
    logger.info("Performance test completed!")
