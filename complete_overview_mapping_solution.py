"""
Complete Solution for Mapping All 5 Tables in Overview Tab
From Original RBMF File to 2025 Template
"""

import pandas as pd
import re
from typing import Dict, List, Tuple, Optional

class OverviewTableMapper:
    """
    Complete mapper for all 5 tables in Overview tab
    """
    
    def __init__(self):
        self.mapping_results = {}
    
    def map_all_tables(self, original_file_path: str, template_file_path: str, output_file_path: str):
        """
        Map all 5 tables from original to template
        """
        # Read both files
        df_original = pd.read_excel(original_file_path, sheet_name='Overview', header=None)
        df_template = pd.read_excel(template_file_path, sheet_name='Overview', header=None)
        
        # Create output dataframe
        df_output = df_template.copy()
        
        # Map all 5 tables
        self.map_table_1_general_overview(df_original, df_output)
        self.map_table_2_project_overview(df_original, df_output)
        self.map_table_3_implementation_partner(df_original, df_output)
        self.map_table_4_project_stakeholders(df_original, df_output)
        self.map_table_5_stakeholder_quotes(df_original, df_output)
        
        # Save result
        with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
            df_output.to_excel(writer, sheet_name='Overview', index=False, header=False)
        
        return df_output
    
    def map_table_1_general_overview(self, df_original: pd.DataFrame, df_output: pd.DataFrame):
        """
        TABLE 1: General Overview Section (Left Side)
        Template rows 0-7, Original rows 0-7
        """
        print("Mapping Table 1: General Overview Section")
        
        # Row 0: Section header
        df_output.iloc[0, 0] = df_original.iloc[0, 0]  # "General Overview"
        
        # Row 1: Country
        df_output.iloc[1, 0] = "Country"
        df_output.iloc[1, 1] = df_original.iloc[2, 1]  # "Indonesia"
        
        # Row 2: Project Name
        df_output.iloc[2, 0] = "Project Name"
        df_output.iloc[2, 1] = df_original.iloc[3, 1]  # Full project name
        
        # Row 3: Project ID
        df_output.iloc[3, 0] = "Project ID"
        df_output.iloc[3, 1] = ""  # Not present in original
        
        # Row 4: Implementing Partner
        df_output.iloc[4, 0] = "Implementing Partner/Retainer Name"
        df_output.iloc[4, 1] = df_original.iloc[1, 1]  # "Aquatera"
        
        # Row 5: Implementation period
        df_output.iloc[5, 0] = "Implementation period"
        period = df_original.iloc[5, 1]  # "July 2024 - November 2025"
        if ' - ' in period:
            from_date, to_date = period.split(' - ')
            df_output.iloc[5, 1] = from_date.strip()
            df_output.iloc[5, 2] = to_date.strip()
        
        # Row 6: Post Implementation Monitoring
        df_output.iloc[6, 0] = "Post Implementation Monitoring"
        df_output.iloc[6, 1] = ""  # Not present in original
        
        print("✓ Table 1 mapped successfully")
    
    def map_table_2_project_overview(self, df_original: pd.DataFrame, df_output: pd.DataFrame):
        """
        TABLE 2: Project Overview Section (Right Side)
        Template rows 0-7, Original rows 0-7 (right side columns)
        """
        print("Mapping Table 2: Project Overview Section")
        
        # Row 0: Section header
        df_output.iloc[0, 4] = df_original.iloc[0, 4]  # "Project overview"
        
        # Row 1: Primary strategic outcome
        df_output.iloc[1, 4] = "Primary strategic outcome"
        df_output.iloc[1, 5] = df_original.iloc[1, 5]  # "SO4 - Knowledge and Awareness Building"
        
        # Row 2: Impact
        df_output.iloc[2, 4] = "Impact"
        df_output.iloc[2, 5] = df_original.iloc[2, 5]  # Impact description
        
        # Row 3: Outcome
        df_output.iloc[3, 4] = "Outcome"
        df_output.iloc[3, 5] = df_original.iloc[3, 5]  # Outcome description
        
        # Row 4: Output
        df_output.iloc[4, 4] = "Output"
        df_output.iloc[4, 5] = df_original.iloc[4, 5]  # Output description
        
        print("✓ Table 2 mapped successfully")
    
    def map_table_3_implementation_partner(self, df_original: pd.DataFrame, df_output: pd.DataFrame):
        """
        TABLE 3: Implementation Partner Overview Table
        Template rows 8-12, Original rows 7-12
        """
        print("Mapping Table 3: Implementation Partner Overview Table")
        
        # Row 8: Section header
        df_output.iloc[8, 0] = df_original.iloc[7, 0]  # "Implementation Partner Overview"
        
        # Row 9: Table header
        df_output.iloc[9, 0] = df_original.iloc[8, 0]  # "Implementation Partner"
        df_output.iloc[9, 1] = df_original.iloc[8, 1]  # "Total"
        df_output.iloc[9, 2] = df_original.iloc[8, 2]  # "Female"
        
        # Row 10: Project Team
        df_output.iloc[10, 0] = df_original.iloc[9, 0]  # "Project Team"
        df_output.iloc[10, 1] = df_original.iloc[9, 1]  # "17"
        df_output.iloc[10, 2] = df_original.iloc[9, 2]  # "9"
        
        # Row 11: Number of Founders
        df_output.iloc[11, 0] = df_original.iloc[10, 0]  # "Number of Founders"
        df_output.iloc[11, 1] = df_original.iloc[10, 1]  # "1"
        df_output.iloc[11, 2] = df_original.iloc[10, 2]  # "0"
        
        # Row 12: Senior Management
        df_output.iloc[12, 0] = df_original.iloc[11, 0]  # "Senior Management"
        df_output.iloc[12, 1] = df_original.iloc[11, 1]  # "5 Directors"
        df_output.iloc[12, 2] = df_original.iloc[11, 2]  # "2"
        
        print("✓ Table 3 mapped successfully")
    
    def map_table_4_project_stakeholders(self, df_original: pd.DataFrame, df_output: pd.DataFrame):
        """
        TABLE 4: Project Stakeholders Table
        Template rows 14-15, Original rows 13-14
        """
        print("Mapping Table 4: Project Stakeholders Table")
        
        # Row 14: Section header
        df_output.iloc[14, 0] = df_original.iloc[13, 0]  # "Project Stakeholders"
        df_output.iloc[14, 4] = df_original.iloc[13, 4]  # "Project Stakeholders/Beneficiary Quotes"
        
        # Row 15: Table header
        df_output.iloc[15, 0] = df_original.iloc[14, 0]  # "Stakeholder Name"
        df_output.iloc[15, 1] = df_original.iloc[14, 1]  # "Department/Organisation Name"
        df_output.iloc[15, 2] = df_original.iloc[14, 2]  # "Position"
        df_output.iloc[15, 4] = df_original.iloc[14, 4]  # "Stakeholder/Beneficiary Name"
        df_output.iloc[15, 5] = df_original.iloc[14, 5]  # "Department/Organisation Name"
        df_output.iloc[15, 6] = df_original.iloc[14, 6]  # "Position"
        df_output.iloc[15, 7] = df_original.iloc[14, 7]  # "Quote"
        
        print("✓ Table 4 mapped successfully")
    
    def map_table_5_stakeholder_quotes(self, df_original: pd.DataFrame, df_output: pd.DataFrame):
        """
        TABLE 5: Project Stakeholders/Beneficiary Quotes Table
        Template rows 16+, Original rows 15-20
        """
        print("Mapping Table 5: Project Stakeholders/Beneficiary Quotes Table")
        
        # Copy stakeholder data rows
        template_row = 16
        for orig_row in range(15, 21):  # Rows 15-20 in original
            if orig_row < len(df_original):
                # Copy stakeholder data to template right side
                df_output.iloc[template_row, 4] = df_original.iloc[orig_row, 0]  # Name
                df_output.iloc[template_row, 5] = df_original.iloc[orig_row, 1]  # Department
                df_output.iloc[template_row, 6] = df_original.iloc[orig_row, 2]  # Position
                df_output.iloc[template_row, 7] = df_original.iloc[orig_row, 7]  # Quote (empty)
                template_row += 1
        
        print("✓ Table 5 mapped successfully")
    
    def get_mapping_summary(self) -> Dict:
        """
        Get summary of all mappings
        """
        return {
            "table_1": "General Overview Section (Left Side) - 7 fields",
            "table_2": "Project Overview Section (Right Side) - 5 fields",
            "table_3": "Implementation Partner Overview Table - 5 rows",
            "table_4": "Project Stakeholders Table - 2 rows",
            "table_5": "Project Stakeholders/Beneficiary Quotes Table - 6 data rows"
        }

# ===== USAGE EXAMPLE =====
def main():
    """
    Example usage of the complete mapping solution
    """
    mapper = OverviewTableMapper()
    
    # File paths
    original_file = 'data/test/INO_2024_Aquatera_Energy Transition Business and Change Management Centre of Excellence'
    template_file = 'data/Draft RBMF Template 2025.xlsx'
    output_file = 'data/2025-output/mapped_overview_output.xlsx'
    
    print("=== COMPLETE OVERVIEW TAB MAPPING SOLUTION ===")
    print()
    
    # Show mapping summary
    summary = mapper.get_mapping_summary()
    print("=== MAPPING SUMMARY ===")
    for table, description in summary.items():
        print(f"{table}: {description}")
    print()
    
    # Perform mapping
    try:
        result_df = mapper.map_all_tables(original_file, template_file, output_file)
        print("=== MAPPING COMPLETED SUCCESSFULLY ===")
        print(f"Output saved to: {output_file}")
        print(f"Result shape: {result_df.shape}")
        
    except Exception as e:
        print(f"Error during mapping: {e}")

if __name__ == "__main__":
    main()
