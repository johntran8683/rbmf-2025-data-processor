#!/usr/bin/env python3
"""
Remove the specific projects that were added
"""

import json
from pathlib import Path

def remove_added_projects():
    """Remove the projects that were added."""
    
    mapping_file = Path("data/2025-output/map_projectId_projectName.json")
    
    # Load current data
    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Remove the specific projects I added
    projects_to_remove = [
        "22393-001", "22393-002"
    ]
    
    # Also remove NO-ID projects that were added for entries with "-"
    # These have "has_original_id": true but are NO-ID format
    for project_id in list(data['projects'].keys()):
        if project_id in projects_to_remove:
            del data['projects'][project_id]
        elif project_id.startswith('NO-ID-') and data['projects'][project_id].get('has_original_id', False):
            # This is one of the NO-ID projects I added
            del data['projects'][project_id]
    
    # Update metadata
    data['total_projects'] = len(data['projects'])
    data['extraction_date'] = "2025-09-05T04:20:00Z"
    
    # Save the cleaned file
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Removed added projects from map_projectId_projectName.json")
    print(f"Now has {len(data['projects'])} projects")
    
    # Count by type
    etp_count = sum(1 for pid in data['projects'].keys() if pid.startswith('ETP-'))
    noid_count = sum(1 for pid in data['projects'].keys() if pid.startswith('NO-ID-'))
    print(f"ETP projects: {etp_count}")
    print(f"NO-ID projects: {noid_count}")

if __name__ == "__main__":
    remove_added_projects()
