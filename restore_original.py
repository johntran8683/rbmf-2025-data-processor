#!/usr/bin/env python3
"""
Restore map_projectId_projectName.json to original state
"""

import json
from pathlib import Path

def restore_original():
    """Restore to original state by removing added projects."""
    
    mapping_file = Path("data/2025-output/map_projectId_projectName.json")
    
    # Load current data
    with open(mapping_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Keep only projects that were in the original file
    # Original file had 117 projects, mostly ETP-XXX format and some NO-ID with has_original_id: false
    original_projects = {}
    
    for project_id, project_info in data['projects'].items():
        # Keep ETP-XXX projects (these were original)
        if project_id.startswith('ETP-'):
            original_projects[project_id] = project_info
        # Keep NO-ID projects that have has_original_id: false (these were original)
        elif project_id.startswith('NO-ID-') and not project_info.get('has_original_id', False):
            original_projects[project_id] = project_info
        # Keep ETP-EU-XXX projects (these were original)
        elif project_id.startswith('ETP-EU-'):
            original_projects[project_id] = project_info
    
    # Update the data
    data['projects'] = original_projects
    data['total_projects'] = len(original_projects)
    data['extraction_date'] = "2025-09-05T04:20:00Z"
    
    # Save the restored file
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Restored map_projectId_projectName.json to original state")
    print(f"Now has {len(original_projects)} projects")
    
    # Count by type
    etp_count = sum(1 for pid in original_projects.keys() if pid.startswith('ETP-'))
    noid_count = sum(1 for pid in original_projects.keys() if pid.startswith('NO-ID-'))
    print(f"ETP projects: {etp_count}")
    print(f"NO-ID projects: {noid_count}")

if __name__ == "__main__":
    restore_original()
