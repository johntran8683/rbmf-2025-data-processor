#!/usr/bin/env python3
"""
Improved script to recreate file_to_projectId_mapping.json using better project name extraction
and fuzzy matching with the updated map_projectId_projectName.json
"""

import json
import re
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
from datetime import datetime

def extract_project_name_from_filename(filename: str) -> str:
    """Extract project name from filename using the specified logic"""
    # Split by "_" and get the last part
    parts = filename.split("_")
    
    if len(parts) <= 1:
        return filename  # No underscores, return as is
    
    # Find the last part that contains the project name
    # The project name starts from the first word that doesn't have "_" behind it
    last_part = parts[-1]
    
    # If the last part is empty or just whitespace, look at the second to last
    if not last_part.strip():
        if len(parts) >= 2:
            last_part = parts[-2]
        else:
            return filename
    
    return last_part.strip()

def clean_project_name(name: str) -> str:
    """Clean project name for better matching"""
    # Remove common prefixes and suffixes
    name = re.sub(r'^\[(Completed|Cancelled|New|On-going|Approved|Under procurement|Unknown|PSA TAF)\]\s*', '', name)
    
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

def find_best_match(file_name: str, project_mappings: Dict[str, Dict]) -> Tuple[Optional[str], float, str]:
    """Find the best matching project ID for a given file name"""
    
    # Extract project name from filename
    extracted_project_name = extract_project_name_from_filename(file_name)
    
    best_match_id = None
    best_similarity = 0.0
    match_type = "none"
    
    # First try exact matching
    for project_id, project_data in project_mappings.items():
        project_name = project_data.get('project_name', '')
        
        # Clean both names for exact comparison
        clean_extracted = clean_project_name(extracted_project_name)
        clean_project = clean_project_name(project_name)
        
        if clean_extracted == clean_project:
            return project_id, 1.0, "exact"
        
        # Check if extracted name is contained in project name or vice versa
        if clean_extracted in clean_project or clean_project in clean_extracted:
            if len(clean_extracted) > 10 and len(clean_project) > 10:  # Only for substantial matches
                return project_id, 0.95, "exact_substring"
    
    # If no exact match, try fuzzy matching
    for project_id, project_data in project_mappings.items():
        project_name = project_data.get('project_name', '')
        similarity = calculate_similarity(extracted_project_name, project_name)
        
        if similarity > best_similarity:
            best_similarity = similarity
            best_match_id = project_id
            match_type = "fuzzy"
    
    return best_match_id, best_similarity, match_type

def create_improved_mapping(threshold: float = 0.6) -> Dict:
    """Create improved file_to_projectId_mapping.json using better project name extraction"""
    
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
        "matching_method": "improved_project_name_extraction",
        "matching_threshold": threshold,
        "total_files_processed": 0,
        "total_matches_found": 0,
        "exact_matches": 0,
        "fuzzy_matches": 0,
        "folders": {},
        "unmatched_count": 0,
        "unmatched_files": []
    }
    
    total_files = 0
    total_matches = 0
    exact_matches = 0
    fuzzy_matches = 0
    all_unmatched = []
    
    # Process each folder
    for folder_name, folder_data in project_names_data.get('folders', {}).items():
        folder_projects = folder_data.get('projects', [])
        folder_matches = {}
        folder_unmatched = []
        folder_exact = 0
        folder_fuzzy = 0
        
        for file_name in folder_projects:
            total_files += 1
            
            # Extract project name and find best match
            best_match_id, similarity, match_type = find_best_match(file_name, project_mappings)
            
            if match_type == "exact" or match_type == "exact_substring":
                folder_matches[file_name] = best_match_id
                total_matches += 1
                exact_matches += 1
                folder_exact += 1
            elif similarity >= threshold and best_match_id:
                folder_matches[file_name] = best_match_id
                total_matches += 1
                fuzzy_matches += 1
                folder_fuzzy += 1
            else:
                folder_unmatched.append(file_name)
                all_unmatched.append(f"{folder_name}: {file_name}")
        
        # Store folder results
        result["folders"][folder_name] = {
            "folder_name": folder_name,
            "total_files": len(folder_projects),
            "matched_files": len(folder_matches),
            "exact_matches": folder_exact,
            "fuzzy_matches": folder_fuzzy,
            "unmatched_files": len(folder_unmatched),
            "mappings": folder_matches,
            "unmatched_list": folder_unmatched
        }
    
    # Update summary statistics
    result["total_files_processed"] = total_files
    result["total_matches_found"] = total_matches
    result["exact_matches"] = exact_matches
    result["fuzzy_matches"] = fuzzy_matches
    result["unmatched_count"] = len(all_unmatched)
    result["unmatched_files"] = all_unmatched
    
    return result

def main():
    """Main function to create improved mapping file"""
    print("🔄 Creating improved file_to_projectId_mapping.json...")
    print("Using project name extraction: last part after splitting by '_'")
    print("Matching strategy: exact matches first, then fuzzy matching (60% threshold)")
    
    # Create improved mapping
    result = create_improved_mapping(0.6)
    
    # Save the result
    output_file = '/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/file_to_projectId_mapping.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Created improved mapping file")
    print(f"📁 Output saved to: {output_file}")
    print(f"📊 Total files processed: {result['total_files_processed']}")
    print(f"🎯 Total matches found: {result['total_matches_found']}")
    print(f"   - Exact matches: {result['exact_matches']}")
    print(f"   - Fuzzy matches: {result['fuzzy_matches']}")
    print(f"❌ Unmatched files: {result['unmatched_count']}")
    
    # Calculate improvement
    match_rate = result["total_matches_found"] / result["total_files_processed"] if result["total_files_processed"] > 0 else 0
    print(f"📈 Match rate: {match_rate:.1%}")
    
    # Show some examples of matches
    print(f"\n🔍 Sample matches:")
    for folder_name, folder_data in result["folders"].items():
        if folder_data["mappings"]:
            print(f"\n{folder_name}:")
            for file_name, project_id in list(folder_data["mappings"].items())[:3]:  # Show first 3 matches
                extracted_name = extract_project_name_from_filename(file_name)
                print(f"  {file_name}")
                print(f"    → Extracted: {extracted_name}")
                print(f"    → Matched to: {project_id}")

if __name__ == "__main__":
    main()
