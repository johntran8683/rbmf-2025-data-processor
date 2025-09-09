#!/usr/bin/env python3
"""
Script to show summary statistics of the recreated map_projectId_projectName.json
"""

import json
from collections import Counter

def analyze_map_projectId():
    """Analyze the recreated map_projectId_projectName.json file"""
    
    # Load the file
    with open('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/map_projectId_projectName.json', 'r') as f:
        data = json.load(f)
    
    print("📊 MAP_PROJECTID_PROJECTNAME.JSON ANALYSIS")
    print("=" * 50)
    
    # Basic statistics
    print(f"\n📈 BASIC STATISTICS:")
    print(f"  Total projects: {data['total_projects']}")
    print(f"  Extraction date: {data['extraction_date']}")
    print(f"  Mapping type: {data['mapping_type']}")
    
    # Analyze project IDs
    projects = data['projects']
    project_ids = list(projects.keys())
    
    # Count by ID type
    etp_count = len([pid for pid in project_ids if pid.startswith('ETP-')])
    no_id_count = len([pid for pid in project_ids if pid.startswith('NO-ID-')])
    
    print(f"\n🔍 PROJECT ID ANALYSIS:")
    print(f"  ETP projects: {etp_count}")
    print(f"  NO-ID projects: {no_id_count}")
    
    # Analyze by country/region
    ino_count = len([pid for pid in project_ids if 'INO' in pid])
    phi_count = len([pid for pid in project_ids if 'PHI' in pid])
    vie_count = len([pid for pid in project_ids if 'VIE' in pid])
    reg_count = len([pid for pid in project_ids if 'REG' in pid])
    eu_count = len([pid for pid in project_ids if 'EU' in pid])
    
    print(f"\n🌍 PROJECTS BY COUNTRY/REGION:")
    print(f"  Indonesia (INO): {ino_count}")
    print(f"  Philippines (PHI): {phi_count}")
    print(f"  Vietnam (VIE): {vie_count}")
    print(f"  Regional (REG): {reg_count}")
    print(f"  EU projects: {eu_count}")
    
    # Analyze by status
    statuses = [project['status'] for project in projects.values()]
    status_counts = Counter(statuses)
    
    print(f"\n📋 PROJECTS BY STATUS:")
    for status, count in status_counts.most_common():
        print(f"  {status}: {count}")
    
    # Show some examples
    print(f"\n🔍 SAMPLE PROJECTS:")
    print("  ETP Projects:")
    etp_samples = [pid for pid in project_ids if pid.startswith('ETP-')][:3]
    for pid in etp_samples:
        project = projects[pid]
        print(f"    {pid}: {project['project_name'][:60]}...")
    
    print("  NO-ID Projects:")
    no_id_samples = [pid for pid in project_ids if pid.startswith('NO-ID-')][:3]
    for pid in no_id_samples:
        project = projects[pid]
        print(f"    {pid}: {project['project_name'][:60]}...")
    
    # Check for any issues
    print(f"\n✅ VALIDATION:")
    issues = []
    
    # Check for empty project names
    empty_names = [pid for pid, project in projects.items() if not project['project_name'].strip()]
    if empty_names:
        issues.append(f"Projects with empty names: {len(empty_names)}")
    
    # Check for duplicate project names
    project_names = [project['project_name'] for project in projects.values()]
    duplicate_names = [name for name, count in Counter(project_names).items() if count > 1]
    if duplicate_names:
        issues.append(f"Duplicate project names: {len(duplicate_names)}")
    
    if issues:
        print("  Issues found:")
        for issue in issues:
            print(f"    ⚠️  {issue}")
    else:
        print("  ✅ No issues found - file structure is valid!")

if __name__ == "__main__":
    analyze_map_projectId()
