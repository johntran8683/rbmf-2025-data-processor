#!/usr/bin/env python3
"""
Script to compare the original and improved mapping files
"""

import json
from datetime import datetime

def load_json_file(filepath):
    """Load JSON file safely"""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def compare_mappings():
    """Compare original and improved mappings"""
    
    # Load both files
    original = load_json_file('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping_backup.json')
    improved = load_json_file('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping.json')
    
    if not original or not improved:
        print("❌ Could not load one or both files")
        return
    
    print("📊 IMPROVED MAPPING COMPARISON REPORT")
    print("=" * 60)
    
    # Overall statistics
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"Original mapping:")
    print(f"  - Total files: {original.get('total_files_processed', 0)}")
    print(f"  - Matches found: {original.get('total_matches_found', 0)}")
    print(f"  - Match rate: {original.get('total_matches_found', 0)/original.get('total_files_processed', 1):.1%}")
    print(f"  - Threshold: {original.get('matching_threshold', 'N/A')}")
    
    print(f"\nImproved mapping:")
    print(f"  - Total files: {improved.get('total_files_processed', 0)}")
    print(f"  - Matches found: {improved.get('total_matches_found', 0)}")
    print(f"  - Match rate: {improved.get('total_matches_found', 0)/improved.get('total_files_processed', 1):.1%}")
    print(f"  - Exact matches: {improved.get('exact_matches', 0)}")
    print(f"  - Fuzzy matches: {improved.get('fuzzy_matches', 0)}")
    print(f"  - Threshold: {improved.get('matching_threshold', 'N/A')}")
    
    # Calculate improvement
    orig_matches = original.get('total_matches_found', 0)
    new_matches = improved.get('total_matches_found', 0)
    improvement = new_matches - orig_matches
    improvement_pct = (improvement / orig_matches * 100) if orig_matches > 0 else 0
    
    print(f"\n🚀 IMPROVEMENT:")
    print(f"  - Additional matches: +{improvement}")
    print(f"  - Improvement: {improvement_pct:+.1f}%")
    print(f"  - Match rate improvement: {new_matches/improved.get('total_files_processed', 1) - orig_matches/original.get('total_files_processed', 1):+.1%}")
    
    # Folder-by-folder comparison
    print(f"\n📁 FOLDER-BY-FOLDER COMPARISON:")
    print("-" * 60)
    
    for folder_name in improved.get('folders', {}):
        orig_folder = original.get('folders', {}).get(folder_name, {})
        new_folder = improved.get('folders', {}).get(folder_name, {})
        
        orig_matches = orig_folder.get('matched_files', 0)
        new_matches = new_folder.get('matched_files', 0)
        total_files = new_folder.get('total_files', 0)
        
        print(f"\n{folder_name}:")
        print(f"  Original: {orig_matches}/{total_files} ({orig_matches/total_files:.1%})")
        print(f"  Improved: {new_matches}/{total_files} ({new_matches/total_files:.1%})")
        print(f"  Improvement: +{new_matches - orig_matches} matches")
        
        # Show exact vs fuzzy breakdown for improved mapping
        exact_matches = new_folder.get('exact_matches', 0)
        fuzzy_matches = new_folder.get('fuzzy_matches', 0)
        print(f"    - Exact matches: {exact_matches}")
        print(f"    - Fuzzy matches: {fuzzy_matches}")
        
        # Show new matches
        orig_mappings = orig_folder.get('mappings', {})
        new_mappings = new_folder.get('mappings', {})
        
        new_only = set(new_mappings.keys()) - set(orig_mappings.keys())
        if new_only:
            print(f"  New matches found:")
            for file_name in list(new_only)[:3]:  # Show first 3
                project_id = new_mappings[file_name]
                print(f"    {file_name} -> {project_id}")
            if len(new_only) > 3:
                print(f"    ... and {len(new_only) - 3} more")
    
    # Show unmatched files
    print(f"\n❌ UNMATCHED FILES ({improved.get('unmatched_count', 0)}):")
    unmatched_files = improved.get('unmatched_files', [])
    for i, file_name in enumerate(unmatched_files[:10]):  # Show first 10
        print(f"  {i+1}. {file_name}")
    if len(unmatched_files) > 10:
        print(f"  ... and {len(unmatched_files) - 10} more")

if __name__ == "__main__":
    compare_mappings()
