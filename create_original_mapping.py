#!/usr/bin/env python3
"""
Create the original map_projectId_projectName.json with exactly 117 projects
"""

import json
from pathlib import Path

def create_original_mapping():
    """Create the original mapping file with 117 projects."""
    
    # This is the original structure with 117 projects
    original_data = {
        "extraction_date": "2025-09-05T04:20:00Z",
        "total_projects": 117,
        "mapping_type": "Project ID to Project Name",
        "projects": {
            "NO-ID-6B82BC6A": {
                "project_name": "De-risking Instrument to Accelerate Energy-Efficiency Business Transaction with Danfoss Energy Management System (DEMS)",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-BA0D3512": {
                "project_name": "Energy Saving Insurance to De-risk Energy Efficiency Project",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-C50E56CB": {
                "project_name": "Decarbonization - Unlocking Investment Potential through Renewable Energy Integration (Under \"Decarbonization Strategy for the Industrial Sector \"/\"Advancing Industrial Sector Decarbonization\")",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-2F43D3AD": {
                "project_name": "Energy Transition Campaign and Public Awareness",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-220A2B2E": {
                "project_name": "Power System Planning Integrated with Geospatial Tool",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-9C9F0F47": {
                "project_name": "Roadmap of Indonesia Supergrid Development to Increase RE Development",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-D6EAD47B": {
                "project_name": "Roadmap of Smart Grid Development",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-806771A9": {
                "project_name": "Strengthening the Energy Transition Mechanism (ETM) Country Platform and Advancing Energy Transition Project Assessments",
                "status": "Cancelled",
                "has_original_id": False
            },
            "NO-ID-874D937B": {
                "project_name": "Unlocking Indonesia's Pumped Storage Hydropower Potential",
                "status": "Cancelled",
                "has_original_id": False
            },
            "ETP-002-INO-1": {
                "project_name": "PLN Main and Disaster Recovery Control Centers (Formerly: Upgrade of Java-Bali Electricity Control Centre through Expansion and Development of Smart Grids)",
                "status": "Completed",
                "has_original_id": True
            }
        }
    }
    
    # Since manually recreating all 117 projects would be very long,
    # let me instead restore from a backup approach
    print("Creating original mapping file...")
    print("This would require the complete original file structure.")
    print("Let me try a different approach...")

if __name__ == "__main__":
    create_original_mapping()
