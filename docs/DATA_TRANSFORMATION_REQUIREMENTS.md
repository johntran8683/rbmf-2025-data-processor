# Data Transformation Requirements - RBMF 2025

## Document History
- **Created**: September 2, 2025
- **Version**: 1.0
- **Purpose**: Document requirements for transforming quarterly RBMF data to half-yearly format

## Overview
This document outlines the requirements for transforming RBMF (Result-Based Management Framework) data from quarterly reporting format to half-yearly reporting format for 2025.

## Source Data Structure
- **Location**: `data/` folder
- **Target Folders**: `1 INO`, `2 PHI`, `3 VIE`, `4 REG`, `5 Retainers`
- **Excluded Folder**: `0 Draft RBMF` (not processed)
- **Template File**: `Draft RBMF Template 2025.xlsx` (contains "Instructions" tab template)
- **File Format**: Excel files (.xlsx)
- **Required Tabs**: "Instructions" (from template) and "RBMF" (from source files)

## Output Data Structure
- **Location**: `2025-output/` folder
- **Subfolders**: Same as source (excluding `0 Draft RBMF`)
- **File Names**: Identical to source files
- **File Format**: Excel files (.xlsx) with same formatting/styling

## Data Transformation Logic

### 1. Tab Processing
- **"Instructions" tab**: Copy from "Draft RBMF Template 2025.xlsx" file in the data folder
- **"RBMF" tab**: Transform using aggregation rules

### 2. Aggregation Rules
**Current State**: Data organized by quarters (Q1, Q2, Q3, Q4)
**Target State**: Data organized by half-years (H1, H2)

**Aggregation Logic**:
- **H1 (First Half)**: Aggregate Q1 + Q2 data
- **H2 (Second Half)**: Aggregate Q3 + Q4 data

### 3. Column Transformations

| Current Column | New Column | Transformation Logic |
|---|---|---|
| `Reporting Year-Quarter` | `Target Reporting Cycle` | Parse year from "YYYY-Q" → "YYYY-H1" or "YYYY-H2" |
| `Completed Output Number` | `Periodical Result` | Sum available quarters for each half-year |
| `Project Status` | `Indicator Status` | If quarters same, use that value; else use last quarter in half-year |
| `Result Type Data` | `Indicator Category` | Copy from any quarter (should be same) |
| `Indicators` | `Indicator Name` | Copy from any quarter (should be same) |
| `Project Output` | `Indicator Description` | Copy from any quarter (should be same) |
| `Progress Notes/Comments` | `Result Notes/Comments` | Copy from any quarter (should be same) |
| `Output Target Number` | `Periodical Target` | Copy from any quarter (should be same) |

**Unchanged Columns**:
- `Primary Outcome Area`
- `Supporting Document` (moved after `Result Notes/Comments`)

### 4. Data Validation Rules

#### 4.1 Expected Consistency
The following columns should have identical values across quarters within the same half-year:
- `Primary Outcome Area`
- `Result Type Data` (Indicator Category)
- `Indicators` (Indicator Name)
- `Project Output` (Indicator Description)
- `Output Target Number` (Periodical Target)
- `Progress Notes/Comments` (Result Notes/Comments)

#### 4.2 Inconsistency Handling
- **Action**: Log inconsistencies to validation log file
- **Log Location**: `2025-output/{folder_name}/data_validation_log.txt`
- **Log Format**: Detailed description of inconsistencies found

#### 4.3 Missing Data Handling
- **Missing Quarters**: Calculate based on available data
- **Single Quarter**: Use that quarter's data for the half-year
- **No Quarters**: Skip file with warning

### 5. File Output Specifications

#### 5.1 File Structure
```
2025-output/
├── 1 INO/
│   ├── INO_2024_Example.xlsx
│   └── data_validation_log.txt (if needed)
├── 2 PHI/
│   ├── PHI_2024_Example.xlsx
│   └── data_validation_log.txt (if needed)
├── 3 VIE/
├── 4 REG/
└── 5 Retainers/
```

#### 5.2 File Properties
- **File Names**: Identical to source files
- **Excel Formatting**: Maintain original styling/formatting
- **Tab Structure**: Same as source (Instructions + RBMF)

### 6. Log File Format

#### 6.1 Validation Log Structure
```
=== Data Validation Log ===
Generated: [timestamp]
Source Folder: [folder_name]

File: [filename.xlsx]
Issue: [description of inconsistency]
Details: [specific details about the inconsistency]
Action Taken: [what was done to resolve]
Row/Column: [location of issue]

[Additional entries...]
```

#### 6.2 Example Log Entry
```
File: INO_2024_Example.xlsx
Issue: Column 'Primary Outcome Area' differs between quarters
Details: Q1='Energy', Q2='Environment' for row 5
Action: Used Q1 value 'Energy' for H1 aggregation
Row/Column: Row 5, Column 'Primary Outcome Area'
```

### 7. Edge Cases

#### 7.1 Missing Quarters
- **Only Q1**: H1 = Q1 data
- **Only Q1, Q3**: H1 = Q1, H2 = Q3
- **Only Q2, Q4**: H1 = Q2, H2 = Q4
- **No quarters**: Skip file with warning

#### 7.2 Data Parsing
- **Year-Quarter Format**: "YYYY-Q" (e.g., "2024-1", "2024-2")
- **Half-Year Format**: "YYYY-H1" or "YYYY-H2" (e.g., "2024-H1", "2024-H2")

#### 7.3 Aggregation Examples
- **H1 Calculation**: If Q1=5, Q2=3 → H1=8
- **H2 Calculation**: If Q3=2, Q4=4 → H2=6
- **Status Logic**: If Q1="Active", Q2="Completed" → H1="Completed"

### 8. Technical Implementation Notes

#### 8.1 Processing Order
1. Load "Instructions" tab from "Draft RBMF Template 2025.xlsx" in data folder
2. Scan source folders for Excel files
3. For each file:
   - Use template "Instructions" tab (from step 1)
   - Read "RBMF" tab (transform)
   - Validate data consistency
   - Apply transformations
   - Generate output file
   - Create validation log if needed

#### 8.2 Error Handling
- **File Access Errors**: Log and skip
- **Missing Tabs**: Log and skip
- **Data Parsing Errors**: Log and skip
- **Validation Errors**: Log and continue

#### 8.3 Performance Considerations
- Process files sequentially to avoid memory issues
- Log progress for large datasets
- Provide summary statistics at completion

### 9. Future Considerations

#### 9.1 Potential Enhancements
- Configuration file for column mappings
- Support for different aggregation periods
- Automated validation rule updates
- Integration with existing RBMF processing pipeline

#### 9.2 Maintenance Notes
- Update this document when requirements change
- Version control for transformation logic
- Regular validation of output data quality

## Approval
- **Requirements Confirmed**: September 2, 2025
- **Implementation Ready**: Yes
- **Next Step**: Implement transformation logic

---
*This document serves as the authoritative source for RBMF 2025 data transformation requirements.*
