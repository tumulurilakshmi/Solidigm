# Quick Start Guide

## Step 1: Update the URLs File

Edit `urls.txt` and add your URLs:

```
https://www.solidigm.com/ | US/EN
```

## Step 2: Run the Validation

```bash
python run_validation.py urls.txt
```

## Step 3: Check the Reports

After running, you'll find reports in the `reports/` folder:

1. **validation_report_TIMESTAMP.txt** - Text report
2. **validation_report_TIMESTAMP.html** - HTML report (open in browser)
3. **validation_report_TIMESTAMP.json** - JSON data
4. **summary_report_TIMESTAMP.txt** - Summary of all URLs

## Report Sections

The reports include:

### 📊 Overall Summary
- Total UI validations performed
- How many passed/failed
- Total links checked
- How many are broken

### 🎨 UI Validation Details by Category

**Font Size Validations:**
- Checks h1, h2, h3, paragraph, navigation fonts
- Shows failures like: "Font size mismatch: 42px (expected: 48px)"

**Font Color Validations:**
- Validates text colors
- Shows failures like: "Color mismatch: rgb(50, 50, 50) (expected: rgb(0, 0, 0))"

**Element Size Validations:**
- Checks header/footer dimensions
- Shows failures like: "Size mismatch: 1800x95 (expected: 1920x100)"

**Images:**
- Validates image loading
- Shows broken images

**Buttons:**
- Checks if buttons are visible and enabled
- Shows disabled/hidden buttons

**Navigation:**
- Validates navigation links
- Shows invalid links

### 🔗 Link Validation Details

- **List of broken links** with:
  - URL
  - Link text
  - HTTP status code
  - Error message

### ❌ Failure Summary

Shows what is failing with respect to UI:
- Font sizes that don't match expected values
- Font colors that are different
- Element sizes that are incorrect
- Images that failed to load
- Buttons that are disabled/hidden

## Example Report Output

```
===============================================================================
                              SOLIDIGM VALIDATION REPORT
===============================================================================

VALIDATION INFORMATION
-----------------------------------------------------------------------------------------------
URL: https://www.solidigm.com/
Locale: US/EN
Timestamp: 2025-01-15 14:30:22

OVERALL SUMMARY
-----------------------------------------------------------------------------------------------
Total UI Validations Performed: 25
UI Validations Passed: 23
UI Validations Failed: 2
Total Links Checked: 142
Valid Links: 138
Broken Links: 4

CATEGORY BREAKDOWN
-----------------------------------------------------------------------------------------------

FONT SIZE:
  Total: 5
  Passed: 4
  Failed: 1
  Failure Details:
    - Font size failed for h1 - Expected: 48px, Got: 42px

FONT COLOR:
  Total: 3
  Passed: 3
  Failed: 0

ELEMENT SIZE:
  Total: 2
  Passed: 1
  Failed: 1
  Failure Details:
    - Size mismatch for header - Expected: 1920x100, Got: 1800x95

BROKEN LINKS:
-----------------------------------------------------------------------------------------------
  URL: https://www.solidigm.com/old-link
  Text: Learn More
  Status: 404
  Message: Link invalid: https://www.solidigm.com/old-link (Status: 404)
```

## Testing Multiple Pages

Add multiple URLs to `urls.txt`:

```
https://www.solidigm.com/ | US/EN
https://www.solidigm.com/products | US/EN
https://www.solidigm.com/support | US/EN
```

Each URL will get its own report plus a summary report.

