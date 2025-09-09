#!/usr/bin/env python3
"""
Script to append new project data to the existing map_projectId_projectName.json
"""

import json
import re
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple

def parse_new_project_data() -> List[Tuple[str, str]]:
    """Parse the new project data and extract project ID and name pairs"""
    projects = []
    
    # Define the new projects based on the provided data
    new_project_entries = [
        # Projects without IDs (marked with -)
        (None, "ETP M&E Work"),
        (None, "Support to NREP"),
        (None, "Vietnam Energy Transition Expert (QA/QC)"),
        (None, "PSA TAF coordination support"),
        (None, "General support to ETP (pooled fund)"),
        (None, "General support to ETP (EU project)"),
        (None, "2025 semi-annual report for pooled fund 2024 annual reports for pooled fund and EU"),
        (None, "QA/QC support to ETP"),
        (None, "QA/QC support to ETP"),  # Duplicate entry
        (None, "General support to ETP"),
        (None, "ETP Dashboards Development and Maintenance"),
        (None, "-"),  # Empty entry
        
        # Projects with ETP IDs
        ("ETP-041-INO-12", "Supporting JETP Secretariat"),
        ("ETP-056-INO-18", "Financial Expertise for PT. SMI (Sarana Multi Infrastruktur (Persero), a Special Mission Vehicle under the Ministry of Finance)"),
        ("ETP-066-PHI-17", "NREP Update"),
        ("ETP-078-PHI-20", "Streamlining Regulations to Support Energy Transition"),
        ("ETP-022-PHI-7", "Support to Renewable Energy Procurement Mechanisms (including GEAP)"),
        ("ETP-037-INO-10", "Integrated Eco-friendly Public Transport"),
        ("ETP-062-INO-22", "JETP Power System Analysis"),
        ("ETP-040-PHI-11", "Energy Regulation Development for RE Integration"),
        ("ETP-050-PHI-14", "Legal Assessment for Preparing the Carbon Pricing Instrument for the Philippines"),
        
        # Existing project references (these should not be added as new projects)
        # ("ETP-072-REG-11", "Existing project: Twinning Arrangements for Decarbonization in Southeast Asia"),
        # ("ETP-061-INO-21", "Existing project: Strengthening Implementation of Government Regulation on Energy Conservation in Indonesia"),
    ]
    
    # Process each project entry
    for project_id, project_name in new_project_entries:
        if project_name and project_name.strip() != "-":  # Only add if project name exists and is not just a dash
            if not project_id:  # Generate NO-ID for projects without ID
                project_hash = hashlib.md5(project_name.encode()).hexdigest()[:8].upper()
                project_id = f"NO-ID-{project_hash}"
            projects.append((project_id, project_name))
    
    return projects

def determine_project_status(project_id: str, project_name: str) -> str:
    """Determine project status based on project ID and name"""
    if not project_id:
        return "Unknown"
    
    # Check for specific patterns in project name
    if "M&E" in project_name or "Monitoring" in project_name or "Evaluation" in project_name:
        return "On-going"
    elif "Support" in project_name or "support" in project_name:
        return "On-going"
    elif "Expert" in project_name or "QA/QC" in project_name:
        return "On-going"
    elif "Development" in project_name or "Maintenance" in project_name:
        return "On-going"
    elif "Report" in project_name or "report" in project_name:
        return "On-going"
    elif "coordination" in project_name.lower():
        return "On-going"
    elif project_id.startswith("ETP-"):
        return "On-going"  # Default for ETP projects
    elif project_id.startswith("NO-ID-"):
        return "Unknown"  # Default for NO-ID projects
    else:
        return "Unknown"

def append_to_map_projectId():
    """Append new projects to the existing map_projectId_projectName.json"""
    
    # Load existing data
    with open('/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/map_projectId_projectName.json', 'r') as f:
        existing_data = json.load(f)
    
    print("📊 EXISTING DATA ANALYSIS:")
    print(f"  Current total projects: {existing_data['total_projects']}")
    
    # Parse new project data
    print("\n📝 PARSING NEW PROJECT DATA...")
    new_projects = parse_new_project_data()
    print(f"  Found {len(new_projects)} new projects")
    
    # Check for duplicates
    existing_project_ids = set(existing_data['projects'].keys())
    existing_project_names = set(project['project_name'] for project in existing_data['projects'].values())
    
    duplicates = []
    new_unique_projects = []
    
    for project_id, project_name in new_projects:
        if project_id in existing_project_ids:
            duplicates.append(f"ID {project_id}: {project_name[:50]}...")
        elif project_name in existing_project_names:
            duplicates.append(f"Name: {project_name[:50]}...")
        else:
            new_unique_projects.append((project_id, project_name))
    
    if duplicates:
        print(f"\n⚠️  DUPLICATES FOUND ({len(duplicates)}):")
        for dup in duplicates[:5]:  # Show first 5 duplicates
            print(f"    {dup}")
        if len(duplicates) > 5:
            print(f"    ... and {len(duplicates) - 5} more")
    
    print(f"\n✅ UNIQUE NEW PROJECTS: {len(new_unique_projects)}")
    
    # Add new projects to existing data
    for project_id, project_name in new_unique_projects:
        # Clean project name
        clean_name = project_name.strip()
        clean_name = re.sub(r'^\[(Completed|Cancelled|On-going|Approved|Under procurement|Unknown|PSA TAF)\]\s*', '', clean_name)
        
        status = determine_project_status(project_id, project_name)
        has_original_id = project_id.startswith("ETP-") or project_id.startswith("NO-ID-")
        
        existing_data['projects'][project_id] = {
            "project_name": clean_name,
            "status": status,
            "has_original_id": has_original_id
        }
    
    # Update metadata
    existing_data['total_projects'] = len(existing_data['projects'])
    existing_data['extraction_date'] = datetime.now().isoformat() + "Z"
    existing_data['last_updated'] = datetime.now().isoformat() + "Z"
    
    # Save updated data
    output_file = '/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/map_projectId_projectName.json'
    with open(output_file, 'w') as f:
        json.dump(existing_data, f, indent=2)
    
    print(f"\n✅ UPDATED MAP_PROJECTID_PROJECTNAME.JSON")
    print(f"📁 Output saved to: {output_file}")
    print(f"📊 New total projects: {existing_data['total_projects']}")
    print(f"➕ Added {len(new_unique_projects)} new projects")
    
    # Show some examples of new projects
    print(f"\n🔍 SAMPLE NEW PROJECTS:")
    for i, (project_id, project_name) in enumerate(new_unique_projects[:5]):
        print(f"  {project_id}: {project_name[:60]}...")
    
    if len(new_unique_projects) > 5:
        print(f"  ... and {len(new_unique_projects) - 5} more")

def main():
    """Main function to append new projects"""
    print("🔄 APPENDING NEW PROJECTS TO MAP_PROJECTID_PROJECTNAME.JSON")
    print("=" * 60)
    
    append_to_map_projectId()

if __name__ == "__main__":
    main()
