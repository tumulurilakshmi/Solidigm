# Excel Report Guide

The validation script now generates Excel reports with detailed validation results in an easy-to-read spreadsheet format.

## Excel Report Structure

Each Excel report contains **4 sheets**:

### 1. Summary Sheet
- **Validation Information**: URL, Locale, Timestamp
- **Overall Summary**: 
  - Total UI Validations
  - UI Validations Passed/Failed
  - Total Links
  - Valid/Broken Links count

### 2. UI Validation Details Sheet
- **Category**: Type of validation (Font Size, Font Color, Element Size, Images, Buttons, Navigation)
- **Total**: Number of validations performed
- **Passed**: Number that passed
- **Failed**: Number that failed
- **Pass %**: Percentage passed
- **Status**: PASS or FAIL indicator

### 3. Link Validation Sheet
- **URL**: The link URL
- **Text**: Link text/description
- **Status Code**: HTTP status code
- **Is Valid**: YES or NO
- **Message**: Error message if broken

### 4. Failure Details Sheet
- **Category**: Type of failure
- **Failure Details**: Specific information about what failed (e.g., "Font size failed for h1 - Expected: 48px, Got: 64px")

## How to View the Report

1. Run the validation:
   ```bash
   python run_validation.py urls.txt
   ```

2. The Excel file will be generated in the `reports/` folder with filename:
   `validation_report_YYYYMMDD_HHMMSS.xlsx`

3. Open the Excel file in Microsoft Excel, Google Sheets, or any spreadsheet application

## Color Coding

- **Green Background**: Passed validations or valid links
- **Red Background**: Failed validations or broken links
- **Blue Header**: Sheet headers
- **Gray Header**: Row headers in tables

## Example Output

The Summary sheet shows:
- **Total UI Validations**: 23
- **UI Validations Passed**: 10
- **UI Validations Failed**: 13
- **Total Links**: 108
- **Valid Links**: 104
- **Broken Links**: 4

## Filtering and Sorting

You can use Excel's built-in features to:
- Filter by status (PASS/FAIL)
- Sort by category
- Count failures per category
- Export to CSV for further analysis

## Benefits

- ✅ Easy to share with stakeholders
- ✅ Visual representation with colors
- ✅ Sortable and filterable data
- ✅ Professional appearance
- ✅ Multiple sheets for different aspects
- ✅ Can be imported into other tools

