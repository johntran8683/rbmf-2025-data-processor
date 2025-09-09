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
    
    # Remove the projects we added (22393-001, 22393-002, and the NO-ID projects we generated)
    projects_to_remove = [
        "22393-001", "22393-002"
    ]
    
    # Also remove any NO-ID projects that were added (they have "has_original_id": true)
    for project_id, project_info in list(data['projects'].items()):
        if project_id in projects_to_remove:
            del data['projects'][project_id]
        elif project_id.startswith('NO-ID-') and project_info.get('has_original_id', False):
            # This is one of the NO-ID projects we added for entries with "-"
            del data['projects'][project_id]
    
    # Update metadata
    data['total_projects'] = len(data['projects'])
    data['extraction_date'] = "2025-09-05T04:20:00Z"  # Original date
    
    # Save the reverted file
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Reverted map_projectId_projectName.json to original state")
    print(f"Now has {len(data['projects'])} projects (should be 117)")

if __name__ == "__main__":
    revert_mapping()
