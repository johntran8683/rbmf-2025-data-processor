#!/usr/bin/env python3
"""
Script to compare the original and recreated mapping files
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
    """Compare original and recreated mappings"""
    
    # Load both files
    original = load_json_file('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping_backup.json')
    recreated = load_json_file('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping.json')
    
    if not original or not recreated:
        print("❌ Could not load one or both files")
        return
    
    print("📊 MAPPING COMPARISON REPORT")
    print("=" * 50)
    
    # Overall statistics
    print(f"\n📈 OVERALL STATISTICS:")
    print(f"Original mapping:")
    print(f"  - Total files: {original.get('total_files_processed', 0)}")
    print(f"  - Matches found: {original.get('total_matches_found', 0)}")
    print(f"  - Match rate: {original.get('total_matches_found', 0)/original.get('total_files_processed', 1):.1%}")
    print(f"  - Threshold: {original.get('matching_threshold', 'N/A')}")
    
    print(f"\nRecreated mapping:")
    print(f"  - Total files: {recreated.get('total_files_processed', 0)}")
    print(f"  - Matches found: {recreated.get('total_matches_found', 0)}")
    print(f"  - Match rate: {recreated.get('total_matches_found', 0)/recreated.get('total_files_processed', 1):.1%}")
    print(f"  - Threshold: {recreated.get('matching_threshold', 'N/A')}")
    
    # Calculate improvement
    orig_matches = original.get('total_matches_found', 0)
    new_matches = recreated.get('total_matches_found', 0)
    improvement = new_matches - orig_matches
    improvement_pct = (improvement / orig_matches * 100) if orig_matches > 0 else 0
    
    print(f"\n🚀 IMPROVEMENT:")
    print(f"  - Additional matches: +{improvement}")
    print(f"  - Improvement: {improvement_pct:+.1f}%")
    
    # Folder-by-folder comparison
    print(f"\n📁 FOLDER-BY-FOLDER COMPARISON:")
    print("-" * 50)
    
    for folder_name in recreated.get('folders', {}):
        orig_folder = original.get('folders', {}).get(folder_name, {})
        new_folder = recreated.get('folders', {}).get(folder_name, {})
        
        orig_matches = orig_folder.get('matched_files', 0)
        new_matches = new_folder.get('matched_files', 0)
        total_files = new_folder.get('total_files', 0)
        
        print(f"\n{folder_name}:")
        print(f"  Original: {orig_matches}/{total_files} ({orig_matches/total_files:.1%})")
        print(f"  Recreated: {new_matches}/{total_files} ({new_matches/total_files:.1%})")
        print(f"  Improvement: +{new_matches - orig_matches} matches")
        
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
    
    # Show some examples of the fuzzy matching quality
    print(f"\n🔍 SAMPLE FUZZY MATCHES:")
    print("-" * 30)
    
    sample_count = 0
    for folder_name, folder_data in recreated.get('folders', {}).items():
        if sample_count >= 5:
            break
        for file_name, project_id in folder_data.get('mappings', {}).items():
            if sample_count >= 5:
                break
            print(f"{file_name}")
            print(f"  -> {project_id}")
            sample_count += 1

if __name__ == "__main__":
    compare_mappings()
