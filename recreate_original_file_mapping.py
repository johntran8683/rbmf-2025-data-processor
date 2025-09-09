#!/usr/bin/env python3
"""
Recreate file_to_projectId_mapping.json using the original map_projectId_projectName.json data
"""

import json
import uuid
from pathlib import Path
from collections import defaultdict
from datetime import datetime
from fuzzywuzzy import fuzz

def recreate_file_mapping():
    """Recreate file_to_projectId_mapping.json using original data."""
    
    # File paths
    data_dir = Path("data/2025-output")
    project_names_file = data_dir / "project_names.json"
    project_mapping_file = data_dir / "map_projectId_projectName.json"
    output_file = data_dir / "file_to_projectId_mapping.json"
    
    # Load project names
    print("Loading project names...")
    with open(project_names_file, 'r', encoding='utf-8') as f:
        project_names_data = json.load(f)
    
    # Load project ID mappings
    print("Loading project ID mappings...")
    with open(project_mapping_file, 'r', encoding='utf-8') as f:
        project_mapping_data = json.load(f)
    
    # Create a lookup dictionary: project_name -> project_id
    project_name_to_id = {}
    for project_id, project_info in project_mapping_data['projects'].items():
        project_name = project_info['project_name']
        project_name_to_id[project_name] = project_id
    
    print(f"Loaded {len(project_name_to_id)} project names for matching")
    
    # Process each folder
    results = {
        'creation_date': datetime.now().isoformat() + 'Z',
        'matching_threshold': 90,
        'total_files_processed': 0,
        'total_matches_found': 0,
        'folders': {}
    }
    
    unmatched_files = []
    
    for folder_name, folder_data in project_names_data['folders'].items():
        print(f"\nProcessing folder: {folder_name}")
        
        folder_results = {
            'folder_name': folder_name,
            'total_files': len(folder_data['projects']),
            'matched_files': 0,
            'unmatched_files': 0,
            'mappings': {},
            'unmatched_list': []
        }
        
        for file_name in folder_data['projects']:
            results['total_files_processed'] += 1
            
            # Try fuzzy matching
            best_match = None
            best_score = 0
            
            for project_name, project_id in project_name_to_id.items():
                # Calculate similarity score
                score = fuzz.ratio(file_name.lower(), project_name.lower())
                
                if score > best_score and score >= 90:  # 90% threshold
                    best_score = score
                    best_match = (project_name, project_id)
            
            if best_match:
                project_name, project_id = best_match
                folder_results['mappings'][file_name] = project_id
                folder_results['matched_files'] += 1
                results['total_matches_found'] += 1
                print(f"  ✓ {file_name} -> {project_id} (score: {best_score})")
            else:
                folder_results['unmatched_files'] += 1
                folder_results['unmatched_list'].append(file_name)
                unmatched_files.append(f"{folder_name}: {file_name}")
                print(f"  ✗ {file_name} (no match found)")
        
        results['folders'][folder_name] = folder_results
    
    # Add summary
    results['unmatched_count'] = len(unmatched_files)
    results['unmatched_files'] = unmatched_files
    
    # Save results
    print(f"\nSaving results to {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n📊 File Mapping Summary (Original Data):")
    print(f"Total files processed: {results['total_files_processed']}")
    print(f"Total matches found: {results['total_matches_found']}")
    print(f"Unmatched files: {results['unmatched_count']}")
    print(f"Success rate: {(results['total_matches_found']/results['total_files_processed']*100):.1f}%")
    
    print(f"\n📁 Results by folder:")
    for folder_name, folder_data in results['folders'].items():
        print(f"  {folder_name}: {folder_data['matched_files']}/{folder_data['total_files']} matched")

if __name__ == "__main__":
    recreate_file_mapping()
