#!/usr/bin/env python3
"""Script to run optimized transformation and compare performance."""

import time
import json
from pathlib import Path
from src.rbmf_processor.optimized_transformer import OptimizedRBMFTransformer

def run_optimized_transformation():
    """Run the optimized transformation on 1 INO folder."""
    print("🚀 Starting Optimized RBMF Transformation")
    print("=" * 50)
    
    # Initialize optimized transformer
    data_dir = Path("data")
    transformer = OptimizedRBMFTransformer(
        data_dir=data_dir,
        include_steps=False,  # Final mode only
        target_folders=["1 INO"]
    )
    
    # Record start time
    start_time = time.time()
    
    # Run optimized processing
    results = transformer.process_folders_optimized()
    
    # Record end time
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print results
    print(f"\n✅ Optimized Transformation Completed!")
    print(f"⏱️  Total Time: {total_time:.2f} seconds")
    print(f"📊 Files Processed: {results['total_files']}")
    print(f"✅ Successfully Created: {results['created_files']}")
    print(f"❌ Failed: {results['failed_files']}")
    
    if 'performance_stats' in results:
        stats = results['performance_stats']
        print(f"\n📈 Performance Statistics:")
        print(f"   • Files per second: {stats.get('files_per_second', 0):.2f}")
        print(f"   • Average time per file: {stats.get('average_time_per_file', 0):.2f}s")
        print(f"   • Peak memory usage: {stats.get('peak_memory_mb', 0):.2f} MB")
        print(f"   • System memory usage: {stats.get('system_memory_usage', 0):.1%}")
    
    # Save results for comparison
    with open("optimized_transformation_report.json", "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n💾 Results saved to: optimized_transformation_report.json")
    
    return results, total_time

if __name__ == "__main__":
    run_optimized_transformation()
