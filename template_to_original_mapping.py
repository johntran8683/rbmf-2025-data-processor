"""
Mapping Guide: 2025 Template Overview Tab → Original File Overview Tab
This shows how each table/field in the template maps to the original file structure.
"""

# ===== TEMPLATE TO ORIGINAL FIELD MAPPING =====
TEMPLATE_TO_ORIGINAL_MAPPING = {
    
    # ===== GENERAL OVERVIEW SECTION (Left Side) =====
    'general_overview': {
        'template_position': (0, 0),
        'original_position': (0, 0),
        'field_name': 'General Overview',
        'mapping_type': 'direct',
        'description': 'Section header - maps directly'
    },
    
    'country': {
        'template_position': (1, 0),
        'original_position': (2, 0),
        'template_value_position': (1, 1),
        'original_value_position': (2, 1),
        'field_name': 'Country',
        'mapping_type': 'value',
        'description': 'Country field - maps from original row 2, col 1'
    },
    
    'project_name': {
        'template_position': (2, 0),
        'original_position': (3, 0),
        'template_value_position': (2, 1),
        'original_value_position': (3, 1),
        'field_name': 'Project Name',
        'mapping_type': 'value',
        'description': 'Project name - maps from original row 3, col 1'
    },
    
    'project_id': {
        'template_position': (3, 0),
        'original_position': None,  # Not present in original
        'template_value_position': (3, 1),
        'original_value_position': None,
        'field_name': 'Project ID',
        'mapping_type': 'missing',
        'description': 'Project ID - not present in original file'
    },
    
    'implementing_partner': {
        'template_position': (4, 0),
        'original_position': (1, 0),
        'template_value_position': (4, 1),
        'original_value_position': (1, 1),
        'field_name': 'Implementing Partner/Retainer Name',
        'mapping_type': 'value',
        'description': 'Implementing partner - maps from original "Partner Name" (row 1, col 1)'
    },
    
    'implementation_period': {
        'template_position': (5, 0),
        'original_position': (5, 0),
        'template_value_position': (5, 1),  # From date
        'template_value_position_to': (5, 2),  # To date
        'original_value_position': (5, 1),
        'field_name': 'Implementation period',
        'mapping_type': 'parsed_value',
        'description': 'Implementation period - needs parsing from "July 2024 - November 2025"'
    },
    
    'post_implementation_monitoring': {
        'template_position': (6, 0),
        'original_position': None,  # Not present in original
        'template_value_position': (6, 1),
        'original_value_position': None,
        'field_name': 'Post Implementation Monitoring',
        'mapping_type': 'missing',
        'description': 'Post implementation monitoring - not present in original file'
    },
    
    # ===== PROJECT OVERVIEW SECTION (Right Side) =====
    'project_overview': {
        'template_position': (0, 4),
        'original_position': (0, 4),
        'field_name': 'Project overview',
        'mapping_type': 'direct',
        'description': 'Section header - maps directly'
    },
    
    'primary_strategic_outcome': {
        'template_position': (1, 4),
        'original_position': (1, 4),
        'template_value_position': (1, 5),
        'original_value_position': (1, 5),
        'field_name': 'Primary strategic outcome',
        'mapping_type': 'value',
        'description': 'Primary strategic outcome - maps from original row 1, col 5'
    },
    
    'impact': {
        'template_position': (2, 4),
        'original_position': (2, 4),
        'template_value_position': (2, 5),
        'original_value_position': (2, 5),
        'field_name': 'Impact',
        'mapping_type': 'value',
        'description': 'Impact - maps from original row 2, col 5'
    },
    
    'outcome': {
        'template_position': (3, 4),
        'original_position': (3, 4),
        'template_value_position': (3, 5),
        'original_value_position': (3, 5),
        'field_name': 'Outcome',
        'mapping_type': 'value',
        'description': 'Outcome - maps from original row 3, col 5'
    },
    
    'output': {
        'template_position': (4, 4),
        'original_position': (4, 4),
        'template_value_position': (4, 5),
        'original_value_position': (4, 5),
        'field_name': 'Output',
        'mapping_type': 'value',
        'description': 'Output - maps from original row 4, col 5'
    },
    
    # ===== IMPLEMENTATION PARTNER OVERVIEW TABLE =====
    'implementation_partner_overview': {
        'template_position': (8, 0),
        'original_position': (7, 0),
        'field_name': 'Implementation Partner Overview',
        'mapping_type': 'section_header',
        'description': 'Section header - maps directly'
    },
    
    'implementation_partner_header': {
        'template_position': (9, 0),
        'original_position': (8, 0),
        'template_position_total': (9, 1),
        'template_position_female': (9, 2),
        'original_position_total': (8, 1),
        'original_position_female': (8, 2),
        'field_name': 'Implementation Partner',
        'mapping_type': 'table_header',
        'description': 'Table header with Total/Female columns'
    },
    
    'project_team': {
        'template_position': (10, 0),
        'original_position': (9, 0),
        'template_position_total': (10, 1),
        'template_position_female': (10, 2),
        'original_position_total': (9, 1),
        'original_position_female': (9, 2),
        'field_name': 'Project Team',
        'mapping_type': 'table_row',
        'description': 'Project Team row - maps from original row 9'
    },
    
    'number_of_founders': {
        'template_position': (11, 0),
        'original_position': (10, 0),
        'template_position_total': (11, 1),
        'template_position_female': (11, 2),
        'original_position_total': (10, 1),
        'original_position_female': (10, 2),
        'field_name': 'Number of Founders',
        'mapping_type': 'table_row',
        'description': 'Number of Founders row - maps from original row 10'
    },
    
    'senior_management': {
        'template_position': (12, 0),
        'original_position': (11, 0),
        'template_position_total': (12, 1),
        'template_position_female': (12, 2),
        'original_position_total': (11, 1),
        'original_position_female': (11, 2),
        'field_name': 'Senior Management',
        'mapping_type': 'table_row',
        'description': 'Senior Management row - maps from original row 11'
    },
    
    # ===== STAKEHOLDER TABLE =====
    'project_stakeholders': {
        'template_position': (14, 0),
        'original_position': (13, 0),
        'template_position_quotes': (14, 4),
        'original_position_quotes': (13, 4),
        'field_name': 'Project Stakeholders',
        'mapping_type': 'section_header',
        'description': 'Section header - maps directly'
    },
    
    'stakeholder_table_header': {
        'template_position': (15, 0),
        'original_position': (14, 0),
        'template_position_name': (15, 0),
        'template_position_dept': (15, 1),
        'template_position_position': (15, 2),
        'template_position_quote': (15, 7),
        'original_position_name': (14, 0),
        'original_position_dept': (14, 1),
        'original_position_position': (14, 2),
        'original_position_quote': (14, 7),
        'field_name': 'Stakeholder Table Header',
        'mapping_type': 'table_header',
        'description': 'Stakeholder table header row'
    },
    
    'stakeholder_data': {
        'template_start_row': 16,
        'original_start_row': 15,
        'template_end_row': None,  # Dynamic
        'original_end_row': 20,
        'field_name': 'Stakeholder Data',
        'mapping_type': 'table_data',
        'description': 'Stakeholder data rows - maps from original rows 15-20'
    }
}

# ===== MAPPING TYPES EXPLANATION =====
MAPPING_TYPES = {
    'direct': 'Direct copy of field value',
    'value': 'Copy value from original to template',
    'parsed_value': 'Parse and transform value (e.g., date range)',
    'missing': 'Field not present in original file',
    'section_header': 'Section header - maps directly',
    'table_header': 'Table header row - maps directly',
    'table_row': 'Table data row - maps values',
    'table_data': 'Multiple table data rows - maps all rows'
}

# ===== SPECIAL MAPPING RULES =====
SPECIAL_MAPPING_RULES = {
    'implementation_period': {
        'original_format': 'July 2024 - November 2025',
        'template_format': 'From date: July 2024, To date: November 2025',
        'parsing_rule': 'Split by " - " and extract dates'
    },
    
    'stakeholder_data': {
        'original_structure': 'Left side: Name, Dept, Position | Right side: Name, Dept, Position, Quote',
        'template_structure': 'Right side: Name, Dept, Position, Quote',
        'mapping_rule': 'Copy from original left side to template right side'
    },
    
    'missing_fields': {
        'project_id': 'Not present in original - needs to be populated separately',
        'post_implementation_monitoring': 'Not present in original - needs to be populated separately'
    }
}

def get_mapping_for_field(field_name):
    """Get mapping information for a specific field"""
    return TEMPLATE_TO_ORIGINAL_MAPPING.get(field_name)

def get_all_mappings():
    """Get all mapping information"""
    return TEMPLATE_TO_ORIGINAL_MAPPING

def get_mapping_types():
    """Get explanation of mapping types"""
    return MAPPING_TYPES

def get_special_rules():
    """Get special mapping rules"""
    return SPECIAL_MAPPING_RULES

if __name__ == "__main__":
    print("=== TEMPLATE TO ORIGINAL MAPPING GUIDE ===")
    print()
    
    print("=== FIELD MAPPINGS ===")
    for field_name, mapping in TEMPLATE_TO_ORIGINAL_MAPPING.items():
        print(f"Field: {field_name}")
        print(f"  Template Position: {mapping.get('template_position', 'N/A')}")
        print(f"  Original Position: {mapping.get('original_position', 'N/A')}")
        print(f"  Mapping Type: {mapping.get('mapping_type', 'N/A')}")
        print(f"  Description: {mapping.get('description', 'N/A')}")
        print()
    
    print("=== MAPPING TYPES ===")
    for mapping_type, description in MAPPING_TYPES.items():
        print(f"{mapping_type}: {description}")
    print()
    
    print("=== SPECIAL RULES ===")
    for rule_name, rule_info in SPECIAL_MAPPING_RULES.items():
        print(f"{rule_name}: {rule_info}")
    print()
