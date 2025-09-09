#!/usr/bin/env python3
"""
Script to recreate map_projectId_projectName.json from the provided project data
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple

def parse_project_data(data_text: str) -> List[Tuple[str, str]]:
    """Parse the project data and extract project ID and name pairs"""
    projects = []
    lines = data_text.strip().split('\n')
    
    current_project_id = None
    current_project_name = ""
    
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or line == "Project ID\tProject name":
            continue
            
        # Check if line starts with a project ID (ETP-XXX-XXX-XX or NO-ID-XXXXXXXX)
        if re.match(r'^(ETP-[A-Z0-9-]+|NO-ID-[A-F0-9]+)\s+', line):
            # Save previous project if exists
            if current_project_id and current_project_name:
                projects.append((current_project_id, current_project_name.strip()))
            
            # Extract new project ID and name
            parts = line.split('\t', 1)
            if len(parts) == 2:
                current_project_id = parts[0].strip()
                current_project_name = parts[1].strip()
            else:
                # Handle case where ID and name are separated by spaces
                match = re.match(r'^(ETP-[A-Z0-9-]+|NO-ID-[A-F0-9]+)\s+(.+)', line)
                if match:
                    current_project_id = match.group(1)
                    current_project_name = match.group(2)
                else:
                    current_project_id = line
                    current_project_name = ""
        
        # Check if line starts with just a dash (indicating no ID)
        elif line.startswith('-') and '\t' in line:
            # Save previous project if exists
            if current_project_id and current_project_name:
                projects.append((current_project_id, current_project_name.strip()))
            
            # This is a project without ID
            parts = line.split('\t', 1)
            if len(parts) == 2:
                current_project_id = None
                current_project_name = parts[1].strip()
            else:
                current_project_id = None
                current_project_name = line[1:].strip()  # Remove the dash
        
        # Check if line starts with just spaces or tabs (continuation of previous project name)
        elif line.startswith('\t') or (line and not re.match(r'^(ETP-[A-Z0-9-]+|NO-ID-[A-F0-9]+)', line) and not line.startswith('-')):
            # This is a continuation of the project name
            if current_project_name:
                current_project_name += " " + line.strip()
            else:
                current_project_name = line.strip()
        
        # Check if this is a new project without ID (starts with tab or spaces)
        elif line and not line.startswith('-') and not re.match(r'^(ETP-[A-Z0-9-]+|NO-ID-[A-F0-9]+)', line):
            # Save previous project if exists
            if current_project_id and current_project_name:
                projects.append((current_project_id, current_project_name.strip()))
            
            # This is a new project without ID
            current_project_id = None
            current_project_name = line.strip()
    
    # Don't forget the last project
    if current_project_id and current_project_name:
        projects.append((current_project_id, current_project_name.strip()))
    elif current_project_name and not current_project_id:
        # Generate a NO-ID for projects without ID
        import hashlib
        project_hash = hashlib.md5(current_project_name.encode()).hexdigest()[:8].upper()
        projects.append((f"NO-ID-{project_hash}", current_project_name.strip()))
    
    return projects

def determine_project_status(project_id: str, project_name: str) -> str:
    """Determine project status based on project ID and name"""
    if not project_id:
        return "Unknown"
    
    # Check for specific patterns in project name
    if "[Completed]" in project_name or "Completed" in project_name:
        return "Completed"
    elif "[Cancelled]" in project_name or "Cancelled" in project_name:
        return "Cancelled"
    elif "[On-going]" in project_name or "On-going" in project_name:
        return "On-going"
    elif "[Approved]" in project_name or "Approved" in project_name:
        return "Approved"
    elif "[Under procurement]" in project_name or "Under procurement" in project_name:
        return "Under procurement"
    elif "PSA TAF" in project_name:
        return "PSA TAF"
    elif "EU" in project_id:
        return "On-going - EU"
    elif project_id.startswith("ETP-"):
        return "On-going"  # Default for ETP projects
    elif project_id.startswith("NO-ID-"):
        return "Unknown"  # Default for NO-ID projects
    else:
        return "Unknown"

def create_map_projectId_projectName(projects: List[Tuple[str, str]]) -> Dict:
    """Create the map_projectId_projectName.json structure"""
    
    # Count projects by status
    status_counts = {}
    for project_id, project_name in projects:
        status = determine_project_status(project_id, project_name)
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Create the main structure
    result = {
        "extraction_date": datetime.now().isoformat() + "Z",
        "total_projects": len(projects),
        "mapping_type": "Project ID to Project Name",
        "projects": {}
    }
    
    # Add each project
    for project_id, project_name in projects:
        if not project_id:
            continue
            
        # Clean project name (remove status prefixes)
        clean_name = project_name
        clean_name = re.sub(r'^\[(Completed|Cancelled|On-going|Approved|Under procurement|Unknown|PSA TAF)\]\s*', '', clean_name)
        clean_name = clean_name.strip()
        
        status = determine_project_status(project_id, project_name)
        has_original_id = project_id.startswith("ETP-") or project_id.startswith("NO-ID-")
        
        result["projects"][project_id] = {
            "project_name": clean_name,
            "status": status,
            "has_original_id": has_original_id
        }
    
    return result

def main():
    """Main function to recreate the mapping file"""
    
    # The provided project data
    project_data = """Project ID	Project name
-	De-risking Instrument to Accelerate Energy-Efficiency Business Transaction with Danfoss Energy Management System (DEMS)
-	Energy Saving Insurance to De-risk Energy Efficiency Project
-	"Decarbonization - Unlocking Investment Potential through Renewable Energy Integration
(Under ""Decarbonization Strategy for the Industrial Sector ""/""Advancing Industrial Sector Decarbonization"")"
-	Energy Transition Campaign and Public Awareness
-	Power System Planning Integrated with Geospatial Tool
-	Roadmap of Indonesia Supergrid Development to Increase RE Development
-	Roadmap of Smart Grid Development
-	Strengthening the Energy Transition Mechanism (ETM) Country Platform and Advancing Energy Transition Project Assessments 
-	Unlocking Indonesia's Pumped Storage Hydropower Potential
ETP-002-INO-1	"PLN Main and Disaster Recovery Control Centers
(Formerly: Upgrade of Java-Bali Electricity Control Centre through Expansion and Development of Smart Grids)"
ETP-007-INO-2	Energy Efficiency and Energy Conservation Awareness Raising in the Education Sector
ETP-009-INO-3	"Supporting Medium-term National Development Planning (RPJMN) 2025 – 2029 Background Study Indonesia
(General Energy Transition Consultancy Services in Indonesia)"
ETP-010-INO-4	"Assisting the Revision of the Indonesia Roadmap of Net Zero Emission (NZE) 2060
(General Energy Transition Consultancy Services in Indonesia)"
ETP-011-INO-5	"Preparation of the Indonesia's Enhanced Nationally Determined Contribution (NDC) Investment Roadmap for Energy Efficiency
(General Energy Transition Consultancy Services in Indonesia)"
ETP-014-INO-6	Study on the Financial Implications of the Early Retirement of Coal-fired Power Plants
ETP-024-INO-7	Wind Energy Development in Indonesia - Investment Plan
ETP-025-INO-8	Streamlining Government of Indonesia Plans as a Pathway to Achieve Net Zero Emissions Target
ETP-036-INO-9	Catalyzing Energy Efficiency as a Service
ETP-039-INO-11	1 GW Solar PV Mapping and Development Plan
ETP-049-INO-13	Supply Chain Integration of Battery Value Chain for Energy Transition
ETP-051-INO-14	"Advisory Services to Support Smart Grid Development and Implementation
(Extension of PLN Main and Disaster Recovery Control Centers)"
ETP-053-INO-15	Innovating New Incentives Mechanism for Energy Transition Projects
ETP-054-INO-16	"Energy Transition Business and Change Management Centre of Excellence
(Formerly: PLN Business Centre of Excellence Capacity Building Program)"
ETP-055-INO-17	"Decarbonize Captive Power Market for Industrial Decarbonization
(Under ""Decarbonization Strategy for the Industrial Sector ""/""Advancing Industrial Sector Decarbonization"")"
ETP-057-INO-19	"Leveraging Industrial Decarbonisation Options in Indonesia by Anticipating International Carbon Tariff
(Formerly: Mitigating the Impact of EU's CBAM on Industrial Sector in Indonesia)
(Under ""Decarbonization Strategy for the Industrial Sector ""/""Advancing Industrial Sector Decarbonization"")"
ETP-058-INO-20	Specialized Workforce Development to Support Energy Transition
ETP-061-INO-21	Strengthening Implementation of Government Regulation on Energy Conservation
ETP-063-INO-23	Operationalization of the Just Transition Framework in JETP Indonesia
ETP-076-INO-24	Integrating Battery Energy Storage System (BESS) into the Grid for Energy Transition
ETP-077-INO-25	"Preparation of the Mid-Term Strategic Plan (Renstra) 2025-2029
(Related to: Streamlining Government of Indonesia Plans as a Pathway to Achieve Net Zero Emissions Target)"
	"Transitioning Coal-Fired Power Plants in Indonesia
(Formerly: Transitioning Coal PPAs in Indonesia)"
	Smart Grids for Resilient Islands:  Piloting smart grid and microgrid frameworks in Bali's electricity system
	Floating Solar PV on Ministry of Public Works Dams
	Modernizing Distribution and Grid Codes
	Unlocking Indonesia's Offshore Wind Energy Potential
-	ERC's Role in Shaping the Energy Landscape
ETP-005-PHI-1	"Upgrading Design and Implementation of Battery Energy Storage Market Mechanism of the Philippines Electricity Market Mechanism
(Formerly: Philippines Energy Regulatory Improvement and Battery Energy Market Mechanism Support Program)"
ETP-008-PHI-3	ESCO-in-a-box for Southeast Asia
ETP-012-PHI-4	"Power Development Roadmap for the Bangsamoro Autonomous Region for Muslim Mindanao (BARMM)
(General Energy Transition Consultancy Service in Philippines)"
ETP-013-PHI-5	Investment-grade Audit (IGA) Financing Program
ETP-017-PHI-6	Philippines Grid Diagnostic and Roadmap for Smart Grid Development
ETP-030-PHI-8	Demand Side Management Policy
ETP-031-PHI-9	Permitting and Consenting to Offshore Wind Energy (part of Offshore Wind Development)
ETP-035-PHI-10	Marine Spatial Planning (part of Offshore Wind Development)
ETP-006-PHI-2	Upgrading Energy Regulations for the Energy Regulatory Commission of the Philippines (ERC) and Design
ETP-044-PHI-12	Enhancing the Spot Market to Attract Investments to Renewables
ETP-048-PHI-13	Accelerating the Clean Energy Scenario (ACES)
ETP-052-PHI-15	Enhancing Hydro Energy Storage Viability - De-risking Pump Storage Hydro Project Development
ETP-059-PHI-16	Formulation of the Bangsamoro Sustainable Energy Master Plan (BARRM)
ETP-067-PHI-18	Voluntary Renewable Energy Market (VREM)
ETP-074-PHI-19	"Smart Grid Transformation in the Power Distribution Sector
(Formerly: Smart grid pathway in Policy: Smart Grid Roadmap for the Distribution Sector)"
ETP-080-PHI-21	Enabling Investments for the Domestic Energy Transition Supply Chain
	Sustainable Energy Planning for Local Government Units
	Just Transition Pathways for the Coal Mining Sector in the Philippines
	Enhancing Regulations for Grid Governance
	Enhancing Grid Reliability and Advancing Smart Grid through Microgrid Systems
	Market Reforms of the Secondary Price Cap
	OSW EVOSS Integration and Guidelines Development
	Smart Grid Transformation Through Targeted DSM Program Design
	Nationwide Energy Efficiency Practice Institutionalized
-	Renewable Energy Quota System
	Just Transition In The Coal, Oil, And Gas Industries Toward Net-Zero By 2025 - Coal Industry
	"Development and Implementation of Sustainable Development Mechanism (SDM) Following Article 6.4
(Under ""Strengthening Investment Environment and Resource Mobilisation for Energy Transition"")"
ETP-001-VIE-1	Review and Gap Analysis of the Existing Coal Abatement Scenarios
ETP-015-VIE-2	"Consultancy Services for ETP of Wind Development
(Formerly: Consultancy Service for Setting up Criteria for Licensing Offshore Wind Development Survey)"
ETP-016-VIE-3	Roadmap for the Commission for Management of State Capital toward Net-Zero Emission in Energy State-Owned Enterprises (CMSC)
ETP-018-VIE-4	Impact Assessment of EU's Carbon Border Adjustment Mechanism (CBAM)
ETP-020-VIE-5	Legal Support to the Development of Power Generation Projects (EREA)
ETP-021-VIE-6	Diagnostic Study on Net-Zero for the Energy Sector
ETP-023-VIE-7	National Green Cooling Program
ETP-027-VIE-9	Development of 8 Key National Standards for E-vehicle Charging Infrastructure
ETP-032-VIE-10	Assessment of Country's Readiness and International Experience for Carbon Trade Exchange Design
ETP-033-VIE-11	Emission Trading System Piloting and Simulation
ETP-034-VIE-12	Vietnam Smart Grid Roadmap for Period up to Year 2030, with a Vision to 2045
ETP-060-VIE-16	"Advisory Services to Support the Strengthening of Green Financing Landscape
(Formerly: Technical Support for ETP's Stocktake Study on Green Finance Landscape)
(Under ""Strengthening Investment Environment and Resource Mobilisation for Energy Transition"")"
ETP-045-VIE-14	Public Awareness Campaign On Energy Transition On Multimedia Channels
ETP-026-VIE-8	Promotion of Energy Efficiency in Supporting and Food Processing Industries
ETP-043-VIE-13	Development of National Standards for Offshore Wind Power (OWP)
ETP-047-VIE-15	Development of the National Standards for Battery Energy Storage System (BESS)
ETP-064-VIE-17	"Technical Support for Development and Impacts Assessment of Carbon Credit and Allowance Governance Mechanism
(Formerly: Regulatory Framework for Carbon Credit Management - MONRE)"
ETP-065-VIE-18	"Dedicated Policy Framework for Investment and Development of Sustainable Energy Infrastructure
(Under ""Strengthening Investment Environment and Resource Mobilisation for Energy Transition"")"
ETP-070-VIE-19	"Enhancing Batteries' Supply Chain for Electric Vehicles, Solar PVs, and Energy Storage Systems
(Formerly: Supply Chain Integration)
(Under ""Strengthening Investment Environment and Resource Mobilisation for Energy Transition"")"
ETP-071-VIE-20	"Facilitating Private Sector's Access to and Engagement in Vietnam's Energy Sector 
(Formerly: Enhancing Energy Transition Investment and Business Engagement)
(Under ""Strengthening Investment Environment and Resource Mobilisation for Energy Transition"")"
ETP-073-VIE-21	"Vietnam Carbon Trade Exchange - Pilot Preparation with Ministry of Finance
(Formerly: Development of Legal Framework for Carbon Trade Exchange - MOF)"
ETP-075-VIE-22	"Technical Support for the Design and Pilot of the voluntary carbon labelling scheme
(Under ""Pilot of Voluntary Labelling Program Big Industrial Polluters (Steel, Cement and RE Plants) - MONRE"")"
ETP-078-VIE-23	Pilot Energy Investment and Planning for Industrial Parks and Economic Zones Initial Study for Thang Long II Industrial Park
ETP-084-VIE-24	Preliminary Study for Development of Clean Energy Complex in Ninh Thuan Province
	"Provincial Energy Strategies and Investment Frameworks for Industrial Parks in Vietnam
(Formerly: Green Energy Investment and Planning for Industrial Parks and Economic Zones)"
	Assessment of Potential and Roadmap for Deployment of Floating Solar in Irrigation and Hydro Power Reservoirs in Vietnam
	"Paris Agreement Article 6 Operationalization and Carbon Credit Offsetting Standards for the Vietnam's ETS
(Formerly: Vietnam's ETS and International Carbon Market Integration)"
	"Assessment on Energy Efficiency Policies and Recommendations for Promotion of Energy Transition in Vietnam
(Formerly: Review and Update Regulatory Guidance for Energy Efficiency)"
ETP-003-REG-1	Diagnostic Review of and Analysis of Energy Efficiency Development in SEA
ETP-004-REG-2	Energy Transition Round Table
ETP-019-REG-3	Donor Assistance Mapping on Energy Transition in SEA
ETP-028-REG-4	"Diagnostic for Competitive Arrangements for Energy Transition (DCAT)
(Formerly: Energy Market Mechanism Accelerator (EMMA) Regional)"
ETP-029-REG-5	Just Coal Transition Forum (Technical Support)
ETP-038-REG-6	ASEAN Power Grid Advancement Program (APG-AP) - Output 2 Roadmap Development
ETP-046-REG-8	Strengthening Regional Cooperation for the Implementation of the ASEAN Power Grid Advancement Programme (APG-AP) towards accelerating energy transition
ETP-EU-APG-03	"A Study to Develop A Proposed Methodology and Guidelines for ASEAN-wide Integrated Resource and Resilience Planning (IRRP)
(Under APG-AP Output 3 funded by EU)"
ETP-042-REG-7	TRANSEND - Provision of Advisory Services for a Coal Phase Out Initiative
ETP-EU-APG-01	"Studies on the Minimum Requirements for Multilateral Power Market and A Strategy to Establish A Multilateral Power Trade in ASEAN
(Under APG-AP Output 3 funded by EU)"
ETP-EU-APG-02	"A Study on the Proposed Harmonisation of Grid Codes and Minimum Operational Technical Standards for Interconnections under the ASEAN Power Grid
(Under APG-AP Output 3 funded by EU)"
ETP-068-REG-9	"Financial Advisory Services for the Early Retirement of a Coal-Fired Power Plant
(Formerly: Transcend Coal - Financial Advisors)"
ETP-069-REG-10	"Technical Advisory Services for the Early Retirement of a Coal-Fired Power Plant
(Formerly: Transcend Coal - Technical Team)"
ETP-072-REG-11	Twinning Arrangements for Decarbonization in SEA
ETP-081-REG-12	Energy Transition Thematic Report 1 - Southeast Asia Energy Transition Stocktake
ETP-082-REG-13	Sharing of Perspectives to Advance Regional Knowledge on Energy Transition in Southeast Asia (SPARK) - Finance and Investment
ETP-083-REG-14	Technical Assistance for the Establishment of the ASEAN School of Regulation (phase 1)
	Supporting Regional Energy Connectivity through the ASEAN Power Grid Initiative towards Accelerating Energy Transition 
	Energy Transition Thematic Report 2 - Accelerating a Just Coal Transition in Asia and the Pacific
	Energy Transition Thematic Report 3 - Workforce Development
	Sharing of Perspectives to Advance Regional Knowledge on Energy Transition in Southeast Asia (SPARK) - additional topics to be confirmed
	Technical Assistance for the Establishment of the ASEAN School of Regulation (phases 2 & 3)
	Supply Chain of Critical Minerals for Energy Transition in SEA
	
	
	"PSA TAF:
RE-BESS Hybrid in Philippines"
	"PSA TAF:
RE-BESS Hybrid in Vietnam"
	"PSA TAF:
Reconductoring for Vietnam, Indonesia, and Philippines"
"""
    
    print("Parsing project data...")
    projects = parse_project_data(project_data)
    
    print(f"Found {len(projects)} projects")
    
    print("Creating map_projectId_projectName.json structure...")
    result = create_map_projectId_projectName(projects)
    
    # Save the result
    output_file = '/home/john/Desktop/rbmf-2025-data-processor/data/2025-output/map_projectId_projectName.json'
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✅ Created map_projectId_projectName.json")
    print(f"📁 Output saved to: {output_file}")
    print(f"📊 Total projects: {result['total_projects']}")
    
    # Show some examples
    print("\n🔍 Sample projects:")
    count = 0
    for project_id, project_data in result["projects"].items():
        if count >= 5:
            break
        print(f"  {project_id}: {project_data['project_name'][:80]}...")
        count += 1

if __name__ == "__main__":
    main()
