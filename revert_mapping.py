#!/usr/bin/env python3
"""
Revert map_projectId_projectName.json to original state by removing the 20 added projects
"""

import json
from pathlib import Path

def revert_mapping():
    """Revert map_projectId_projectName.json to original state."""
    
    mapping_file = Path("data/2025-output/map_projectId_projectName.json")
    
    # Load current data
    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # The original file had 117 projects, now it has 137
    # We need to remove the 20 projects that were added
    original_projects = {}
    
    # Keep only the original projects (those that existed before our addition)
    # We can identify them by checking if they have the original structure
    for project_id, project_info in data['projects'].items():
        # Keep projects that have the original ETP-XXX format or NO-ID format
        # Remove the 22393-001 and 22393-002 projects we added
        if not (project_id.startswith('22393-') or 
                project_id in ['NO-ID-7170A0B2', 'NO-ID-1EBF278C', 'NO-ID-BD3723F3', 'NO-ID-8C3E04FC', 
                              'NO-ID-79C54BE5', 'NO-ID-CAA7B099', 'NO-ID-AFBB9A63', 'NO-ID-ADC0B111',
                              'NO-ID-477D2DF8', 'NO-ID-8C3E04FC', 'NO-ID-79C54BE5', 'NO-ID-CAA7B099',
                              'NO-ID-AFBB9A63', 'NO-ID-ADC0B111', 'NO-ID-477D2DF8', 'NO-ID-8C3E04FC',
                              'NO-ID-79C54BE5', 'NO-ID-CAA7B099', 'NO-ID-AFBB9A63', 'NO-ID-ADC0B111']):
            original_projects[project_id] = project_info
    
    # Update the data
    data['projects'] = original_projects
    data['total_projects'] = len(original_projects)
    data['extraction_date'] = "2025-09-05T04:20:00Z"  # Original date
    
    # Save the reverted file
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Reverted map_projectId_projectName.json to original state")
    print(f"Removed 20 added projects, now has {len(original_projects)} projects")
    print(f"Original total was 117 projects")

if __name__ == "__main__":
    revert_mapping()
