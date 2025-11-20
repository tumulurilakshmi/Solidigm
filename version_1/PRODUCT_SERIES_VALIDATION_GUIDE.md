# Product Series Validation Guide

## Overview

This validator validates all three product series pages (D3, D5, D7) on the Solidigm website, checking for:
- Page structure (title, breadcrumbs, description)
- Product cards and their details
- Filter functionality (Interface, Form Factor, Capacity)
- Product links validity
- Product comparison feature
- Related articles section

---

## Quick Start

### Step 1: Ensure Dependencies are Installed
```bash
pip install -r requirements.txt
playwright install
```

### Step 2: Run Validation

#### Validate All Series (D3, D5, D7)
```bash
python run_product_series_validation.py
```

#### Validate Specific Series
```bash
# Validate only D3 series
python run_product_series_validation.py D3

# Validate only D5 series
python run_product_series_validation.py D5

# Validate only D7 series
python run_product_series_validation.py D7
```

---

## What Gets Validated

### 1. Page Structure
- ✅ Page loads successfully
- ✅ Main title (h1) exists and matches expected series name
- ✅ Breadcrumbs navigation present
- ✅ Series description found

### 2. Products
- ✅ Product cards are found on the page
- ✅ Expected products match the data in `product_series.json`
- ✅ Each product validated for:
  - Product ID/Name
  - Description
  - Interface type
  - Form Factor
  - Capacity range
  - "View Details" link
  - "Compare" button
  - Product image

### 3. Filters
- ✅ Filter section exists
- ✅ Interface filter present
- ✅ Form Factor filter present
- ✅ Capacity filter present

### 4. Links
- ✅ All "View Details" links are validated
- ✅ HTTP status codes checked (200-399 = valid)
- ✅ Broken links identified

### 5. Comparison Feature
- ✅ Comparison buttons found
- ✅ Maximum 5 products can be selected (as per website)

### 6. Related Articles
- ✅ Related articles section found
- ✅ Article count recorded

---

## Expected Products by Series

### D3 Series (2 products)
- D3-S4620
- D3-S4520

### D5 Series (3 products)
- D5-P5336
- D5-P5430
- D5-P5316

### D7 Series (5 products)
- D7-PS1030
- D7-PS1010
- D7-P5810
- D7-P5620
- D7-P5520

---

## Output

### Console Output
The validator prints real-time validation progress:
```
================================================================================
PRODUCT SERIES PAGE VALIDATION
================================================================================

[INFO] Navigating to https://www.solidigm.com/products/data-center/d3.html

[PAGE STRUCTURE] Validating page structure...
   [OK] Page loaded: SSD D3 Series | Solidigm
   [OK] Title: 'SSD D3 Series'
   [OK] Breadcrumbs found: Data Center > SSD D3 Series

[PRODUCTS] Validating products...
   [OK] Found 2 product cards
   [OK] Found 2/2 expected products
      [OK] Product 1: D3-S4620
      [OK] Product 2: D3-S4520

[FILTERS] Validating filter functionality...
   [OK] Filter section found
   [OK] Interface filter: True
   [OK] Form Factor filter: True
   [OK] Capacity filter: True

[LINKS] Validating product links...
   [OK] Validated 2 links
   [OK] Valid: 2, Invalid: 0

[COMPARISON] Validating product comparison...
   [OK] Comparison feature found

[ARTICLES] Validating related articles...
   [OK] Related articles section found: 1 articles
```

### Excel Report
After validation, an Excel report is generated in the `reports/` folder:
- **Filename**: `product_series_validation_report_[timestamp].xlsx`
- **Sheets**:
  1. **Summary** - Overview of all series
  2. **D3 Series** - Detailed validation for D3
  3. **D5 Series** - Detailed validation for D5
  4. **D7 Series** - Detailed validation for D7

Each sheet contains:
- Page structure details
- Product list with all attributes
- Filter status
- Link validation results
- Comparison feature status
- Related articles information

---

## Configuration

### Product Series Data
The validator uses `product_series.json` to determine expected products. To update:
1. Edit `product_series.json`
2. Add/remove products as needed
3. Run validation again

### Timeouts
Default timeout is 120 seconds. To change, edit `run_product_series_validation.py`:
```python
page.set_default_timeout(180000)  # 3 minutes
```

### Browser Settings
To run in headless mode, edit `run_product_series_validation.py`:
```python
browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
```

---

## Troubleshooting

### Issue: "Could not load series data"
**Solution**: Ensure `product_series.json` exists in the same directory

### Issue: Products not found
**Solution**: 
- Check if the page structure has changed
- Verify CSS selectors in `product_series_validator.py`
- Check if products are loaded dynamically (may need longer wait time)

### Issue: Links validation fails
**Solution**:
- Check network connectivity
- Some links may require authentication
- Increase timeout for slow-loading pages

### Issue: Filters not detected
**Solution**:
- Filters may be implemented differently on the page
- Check browser console for JavaScript errors
- Verify filter selectors in the validator

---

## Integration with Homepage Validator

The product series validator can be integrated into the main homepage validator. To add:

```python
from product_series_validator import ProductSeriesValidator

# In homepage_validator.py
product_series_validator = ProductSeriesValidator(page)
d3_results = product_series_validator.validate_series_page(
    "https://www.solidigm.com/products/data-center/d3.html", 
    "D3"
)
```

---

## Example Usage

### Validate all series and generate report
```bash
python run_product_series_validation.py
```

### Validate only D5 series
```bash
python run_product_series_validation.py D5
```

### Check report output
After running, check the `reports/` folder for the Excel file with detailed results.

---

## Notes

- The validator compares found products against `product_series.json`
- Product IDs are extracted using regex pattern matching
- All links are validated via HTTP requests
- The browser window remains open during validation (unless headless mode)
- Validation typically takes 2-5 minutes per series

