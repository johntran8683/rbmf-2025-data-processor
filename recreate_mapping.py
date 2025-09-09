#!/usr/bin/env python3
"""
Script to recreate file_to_projectId_mapping.json using fuzzy matching
between project names in project_names.json and map_projectId_projectName.json
"""

import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from datetime import datetime

def clean_project_name(name: str) -> str:
    """Clean project name for better matching"""
    # Remove common prefixes and suffixes
    name = re.sub(r'^\[(Completed|Cancelled|New|On-going|Approved|Under procurement|Unknown|PSA TAF)\]\s*', '', name)
    name = re.sub(r'^[A-Z]{3}_\d{4}_[^_]+_', '', name)  # Remove country_year_contractor_ prefix
    name = re.sub(r'^[A-Z]{3}_\d{4}_Retainer\|[^_]+_', '', name)  # Remove retainer prefix
    name = re.sub(r'^[A-Z]{3}_\d{4}_[^_]+_', '', name)  # Remove any remaining country_year_contractor_ prefix
    
    # Normalize whitespace and special characters
    name = re.sub(r'\s+', ' ', name.strip())
    name = re.sub(r'[^\w\s\-\(\)]', '', name)  # Remove special chars except hyphens and parentheses
    
    return name.lower()

def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity between two strings using multiple methods"""
    # Clean both strings
    clean1 = clean_project_name(str1)
    clean2 = clean_project_name(str2)
    
    # Method 1: SequenceMatcher similarity
    seq_similarity = SequenceMatcher(None, clean1, clean2).ratio()
    
    # Method 2: Check if one is contained in the other (substring match)
    substring_similarity = 0.0
    if clean1 in clean2 or clean2 in clean1:
        substring_similarity = min(len(clean1), len(clean2)) / max(len(clean1), len(clean2))
    
    # Method 3: Word overlap similarity
    words1 = set(clean1.split())
    words2 = set(clean2.split())
    if words1 and words2:
        word_overlap = len(words1.intersection(words2)) / len(words1.union(words2))
    else:
        word_overlap = 0.0
    
    # Method 4: Check for key terms match
    key_terms1 = set(re.findall(r'\b\w{4,}\b', clean1))  # Words with 4+ characters
    key_terms2 = set(re.findall(r'\b\w{4,}\b', clean2))
    if key_terms1 and key_terms2:
        key_terms_similarity = len(key_terms1.intersection(key_terms2)) / len(key_terms1.union(key_terms2))
    else:
        key_terms_similarity = 0.0
    
    # Weighted combination of all methods
    final_similarity = (
        seq_similarity * 0.3 +
        substring_similarity * 0.3 +
        word_overlap * 0.2 +
        key_terms_similarity * 0.2
    )
    
    return final_similarity

def find_best_match(file_name: str, project_mappings: Dict[str, Dict]) -> Tuple[Optional[str], float]:
    """Find the best matching project ID for a given file name"""
    best_match_id = None
    best_similarity = 0.0
    
    for project_id, project_data in project_mappings.items():
        project_name = project_data.get('project_name', '')
        similarity = calculate_similarity(file_name, project_name)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = project_id
    
    return best_match_id, best_similarity

def recreate_mapping(threshold: float = 0.6) -> Dict:
    """Recreate the file_to_projectId_mapping.json using fuzzy matching"""
    
    # Load the data files
    with open('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/project_names.json', 'r') as f:
        project_names_data = json.load(f)
    
    with open('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/map_projectId_projectName.json', 'r') as f:
        project_mappings_data = json.load(f)
    
    # Extract project mappings
    project_mappings = project_mappings_data.get('projects', {})
    
    # Initialize result structure
    result = {
        "creation_date": datetime.now().isoformat() + "Z",
        "matching_threshold": threshold,
        "total_files_processed": 0,
        "total_matches_found": 0,
        "folders": {},
        "unmatched_count": 0,
        "unmatched_files": []
    }
    
    total_files = 0
    total_matches = 0
    all_unmatched = []
    
    # Process each folder
    for folder_name, folder_data in project_names_data.get('folders', {}).items():
        folder_projects = folder_data.get('projects', [])
        folder_matches = {}
        folder_unmatched = []
        
        for file_name in folder_projects:
            total_files += 1
            
            # Find best match
            best_match_id, similarity = find_best_match(file_name, project_mappings)
            
            if similarity >= threshold and best_match_id:
                folder_matches[file_name] = best_match_id
                total_matches += 1
            else:
                folder_unmatched.append(file_name)
                all_unmatched.append(f"{folder_name}: {file_name}")
        
        # Store folder results
        result["folders"][folder_name] = {
            "folder_name": folder_name,
            "total_files": len(folder_projects),
            "matched_files": len(folder_matches),
            "unmatched_files": len(folder_unmatched),
            "mappings": folder_matches,
            "unmatched_list": folder_unmatched
        }
    
    # Update summary statistics
    result["total_files_processed"] = total_files
    result["total_matches_found"] = total_matches
    result["unmatched_count"] = len(all_unmatched)
    result["unmatched_files"] = all_unmatched
    
    return result

def main():
    """Main function to recreate the mapping file"""
    print("Recreating file_to_projectId_mapping.json using fuzzy matching...")
    
    # Try different thresholds to find the best balance
    thresholds = [0.5, 0.6, 0.7, 0.8]
    best_result = None
    best_threshold = 0.6
    
    for threshold in thresholds:
        print(f"\nTrying threshold: {threshold}")
        result = recreate_mapping(threshold)
        
        match_rate = result["total_matches_found"] / result["total_files_processed"] if result["total_files_processed"] > 0 else 0
        print(f"  Matches: {result['total_matches_found']}/{result['total_files_processed']} ({match_rate:.1%})")
        
        # Choose the threshold with the best balance of matches and quality
        if match_rate > 0.15:  # At least 15% match rate
            best_result = result
            best_threshold = threshold
    
    if best_result is None:
        best_result = recreate_mapping(0.6)
        best_threshold = 0.6
    
    # Save the result
    output_file = '/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping.json'
    with open(output_file, 'w') as f:
        json.dump(best_result, f, indent=2)
    
    print(f"\n✅ Recreated mapping file with threshold {best_threshold}")
    print(f"📁 Output saved to: {output_file}")
    print(f"📊 Total matches: {best_result['total_matches_found']}/{best_result['total_files_processed']} ({best_result['total_matches_found']/best_result['total_files_processed']:.1%})")
    
    # Show some examples of matches
    print("\n🔍 Sample matches:")
    for folder_name, folder_data in best_result["folders"].items():
        if folder_data["mappings"]:
            print(f"\n{folder_name}:")
            for file_name, project_id in list(folder_data["mappings"].items())[:3]:  # Show first 3 matches
                print(f"  {file_name} -> {project_id}")

if __name__ == "__main__":
    main()
