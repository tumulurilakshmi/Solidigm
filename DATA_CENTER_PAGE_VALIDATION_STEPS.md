# Data Center Page Validation Steps

## Overview
This guide provides step-by-step instructions for validating:
1. **Data Center Landing Page** (`/products/data-center.html`) - Shows all three series together
2. **Individual Series Pages** (D3, D5, D7) - Each series page separately

---

## Data Center Landing Page

**URL**: `https://www.solidigm.com/products/data-center.html`

This is the main landing page that shows all three series (D3, D5, D7) together.

### Quick Start for Landing Page:
```bash
python run_data_center_page_validation.py
```

### What Gets Validated on Landing Page:

1. ✅ **Hero Component**
   - Container size
   - Background image
   - Breadcrumbs (should show just "Data Center" as current page)
   - Title: "Modernize Your Data Center"
   - Description text

2. ✅ **Series Cards/Links**
   - D7 Series card/link present
   - D5 Series card/link present
   - D3 Series card/link present
   - Each card's text, href, font details
   - Navigation test (clicks D7 link to verify it works)

3. ✅ **Model List Section**
   - Title: "What Solidigm Data Center SSD Is Right For You?"
   - Three dropdowns (Interface, Form Factor, Capacity)
   - Product cards from ALL series (D3, D5, D7 combined)
   - Filtering functionality
   - View Details navigation

4. ✅ **Related Articles**
   - Article cards (max 3)
   - Container size, image, tags, title, links

---

## Individual Series Pages

**URLs**:
- D3: `https://www.solidigm.com/products/data-center/d3.html`
- D5: `https://www.solidigm.com/products/data-center/d5.html`
- D7: `https://www.solidigm.com/products/data-center/d7.html`

---

## Prerequisites

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

---

## Execution Steps

### Step 2: Run Data Center Page Validation

#### Option A: Validate All Series (D3, D5, D7)
```bash
python run_product_series_validation.py
```

#### Option B: Validate Specific Series
```bash
# Validate D3 series page
python run_product_series_validation.py D3

# Validate D5 series page
python run_product_series_validation.py D5

# Validate D7 series page
python run_product_series_validation.py D7
```

---

## Complete Validation Flow

When you run the validation, the following steps are executed in order:

### Step 1: Navigate to Series Page
- Navigates to the series URL (e.g., `https://www.solidigm.com/products/data-center/d3.html`)
- Waits for page to load
- Verifies page title

### Step 2: Validate Hero Component
**Validates:**
1. ✅ **Container Size** - Width x Height (pixels)
2. ✅ **Background Image** - Desktop and mobile images with dimensions
3. ✅ **Breadcrumbs** - All levels with:
   - Text content
   - Clickability (all except last should be clickable)
   - Font details (size, color, family, weight)
   - Href links
4. ✅ **Hero Title** - Text, font size, color, family, weight, line height
5. ✅ **Hero Description** - Text, font size, color, family, weight, line height

**Expected Breadcrumbs:**
- Level 1: "Data Center" (clickable → `/products/data-center.html`)
- Level 2: "SSD D3 Series" / "D5 Series SSDs" / "SSD D7 Series" (not clickable - current page)

### Step 3: Validate Page Structure
- ✅ Page loaded successfully
- ✅ Main title (H1) exists
- ✅ Title text matches expected series name
- ✅ Breadcrumbs navigation present
- ✅ Series description found

### Step 4: Validate Model List Section
**Validates:**

1. ✅ **Title**
   - Text content
   - Font size, color, family, weight

2. ✅ **Three Dropdowns**
   - **Interface Dropdown**: All options with text and font details
   - **Form Factor Dropdown**: All options with text and font details
   - **Capacity Dropdown**: All options with text and font details
   - Font details for each dropdown option

3. ✅ **Product Cards (Default State)**
   - Number of cards displayed when all filters are "Any"
   - For each card:
     - Container size (width x height)
     - Image (src, alt, dimensions)
     - Title (text, font size, color, family, weight)
     - Description (text, font size, color, family)
     - Interface (text, font size, color, family)
     - Form Factor (text, font size, color, family)
     - Capacity (text, font size, color, family)
     - View Details button (text, font details, background color)
     - Compare button (text, font details, background color)
     - View Details link URL

4. ✅ **Filtering Test**
   - Selects 2nd option from Interface dropdown
   - Selects 2nd option from Form Factor dropdown
   - Selects 2nd option from Capacity dropdown
   - Verifies fewer products are shown
   - Validates filtered cards contain selected dropdown values

5. ✅ **View Details Navigation**
   - Clicks "View Details" on first product card
   - Verifies navigation to PDP page
   - Checks URL matches product title
   - Example: D7-P5520 → `/products/data-center/d7/p5520.html`
   - Navigates back

6. ✅ **Related Articles**
   - Finds related articles section
   - Counts article cards (max 3)
   - For each article:
     - Container size
     - Image (src, alt)
     - Tags (optional)
     - Title text
     - Link URL
     - Navigation test (clicks first article and verifies URL)

### Step 5: Validate Products (Legacy Validation)
- ✅ Product cards found on page
- ✅ Expected products match `product_series.json`
- ✅ Product details extracted

### Step 6: Validate Filters (Legacy Validation)
- ✅ Filter section exists
- ✅ Interface filter present
- ✅ Form Factor filter present
- ✅ Capacity filter present

### Step 7: Validate Product Links
- ✅ All "View Details" links validated
- ✅ HTTP status codes checked (200-399 = valid)
- ✅ Broken links identified

### Step 8: Validate Comparison Feature
- ✅ Comparison buttons found
- ✅ Maximum 5 products can be selected

### Step 9: Validate Related Articles (Legacy)
- ✅ Related articles section found
- ✅ Article count recorded

---

## Validation Order Summary

```
1. Navigate to Series Page
   ↓
2. Hero Component Validation
   - Container size
   - Background image
   - Breadcrumbs (with font details)
   - Title (with font details)
   - Description (with font details)
   ↓
3. Page Structure Validation
   ↓
4. Model List Section Validation
   - Title
   - Dropdowns (Interface, Form Factor, Capacity)
   - Product Cards (default - all products)
   - Filtering Test (select 2nd options)
   - View Details Navigation Test
   - Related Articles
   ↓
5. Products Validation (legacy)
   ↓
6. Filters Validation (legacy)
   ↓
7. Links Validation
   ↓
8. Comparison Feature Validation
   ↓
9. Related Articles Validation (legacy)
   ↓
10. Generate Excel Report
```

---

## Expected Results by Series

### D3 Series Page
- **URL**: `https://www.solidigm.com/products/data-center/d3.html`
- **Hero Title**: "SSD D3 Series"
- **Products**: 2 (D3-S4620, D3-S4520)
- **Breadcrumbs**: Data Center > SSD D3 Series

### D5 Series Page
- **URL**: `https://www.solidigm.com/products/data-center/d5.html`
- **Hero Title**: "D5 Series SSDs"
- **Products**: 3 (D5-P5336, D5-P5430, D5-P5316)
- **Breadcrumbs**: Data Center > D5 Series SSDs

### D7 Series Page
- **URL**: `https://www.solidigm.com/products/data-center/d7.html`
- **Hero Title**: "SSD D7 Series"
- **Products**: 5 (D7-PS1030, D7-PS1010, D7-P5810, D7-P5620, D7-P5520)
- **Breadcrumbs**: Data Center > SSD D7 Series

---

## Output Files

### Excel Report
**Location**: `reports/` folder  
**Filename**: `product_series_validation_report_[timestamp].xlsx`

**Sheets**:
1. **Summary** - Overview of all series
2. **D3 Series** - Detailed validation including:
   - Hero Component (container, background, breadcrumbs, title, description)
   - Model List (title, dropdowns, product cards, filtering, articles)
   - Page Structure
   - Products
   - Filters
   - Links
   - Comparison
3. **D5 Series** - Same structure as D3
4. **D7 Series** - Same structure as D3

---

## Console Output Example

```
================================================================================
PRODUCT SERIES PAGE VALIDATION
================================================================================

[INFO] Navigating to https://www.solidigm.com/products/data-center/d3.html

[HERO] Validating hero component...
================================================================================
HERO COMPONENT VALIDATION
================================================================================
[INFO] Hero component found

[CONTAINER] Validating container size...
   [OK] Container size: 1920x600 px

[BACKGROUND] Validating background image...
   [OK] Desktop background image found
        Source: https://s7d9.scene7.com/is/image/Solidigm/solidigm-d3-tlc-nand-ssd?fmt=avif
        Size: 1920x600
        Loaded: True

[BREADCRUMBS] Validating breadcrumbs...
   [OK] Breadcrumbs found: 2 levels
      [OK] Level 1: 'Data Center'
          Clickable: True, Last: False
          Font: 14px, Color: rgb(0, 0, 0)
      [OK] Level 2: 'SSD D3 Series'
          Clickable: False, Last: True
          Font: 14px, Color: rgb(0, 0, 0)

[TITLE] Validating hero title...
   [OK] Title: 'SSD D3 Series'
        Font Size: 48px
        Font Color: rgb(255, 255, 255)

[DESCRIPTION] Validating hero description...
   [OK] Description found
        Text: 'Drives in the value-optimized Solidigm D3 Series...'
        Font Size: 16px
        Font Color: rgb(255, 255, 255)

[INFO] Series identified: D3 (confidence: high)

[MODEL LIST] Validating model list section...
================================================================================
MODEL LIST VALIDATION
================================================================================
[INFO] Model List section found

[TITLE] Validating title...
   [OK] Title: 'Which Solidigm Data Center D3 Series SSD is Right for You?'
        Font Size: 24px
        Font Color: rgb(0, 0, 0)

[DROPDOWNS] Validating dropdowns...
      [OK] Interface dropdown: 3 options
          Default: 'Any Interface'
          Options: Any Interface, SATA 3.0 6Gb/s, ...
      [OK] Form Factor dropdown: 3 options
      [OK] Capacity dropdown: 4 options

[PRODUCT CARDS] Validating product cards (default filters)...
   [OK] Found 2 product cards
      [OK] Card 1: D3-S4620
      [OK] Card 2: D3-S4520

[FILTERING] Testing filter functionality...
      [OK] Selected Interface: SATA 3.0 6Gb/s
      [OK] Selected Form Factor: 2.5" 7mm
      [OK] Selected Capacity: 3.84TB
      [OK] Filtered cards count: 1

[RELATED ARTICLES] Validating related articles...
   [OK] Related articles found: 1 cards
```

---

## Key Validation Points

1. ✅ **Hero Component** must be present with all elements
2. ✅ **Breadcrumbs** must have 2 levels (Data Center > Series Name)
3. ✅ **All breadcrumbs except last** must be clickable
4. ✅ **Model List Title** must be present
5. ✅ **All 3 dropdowns** must be present and functional
6. ✅ **Product cards** must match expected count for series
7. ✅ **Filtering** must reduce product count when options selected
8. ✅ **View Details** must navigate to correct PDP page
9. ✅ **Related Articles** must be present (max 3 cards)

---

## Troubleshooting

### Issue: Hero component not found
**Solution**: Check if page structure changed, verify CSS selectors

### Issue: Dropdowns not found
**Solution**: Check if model list section loaded, verify selectors

### Issue: Filtering doesn't work
**Solution**: 
- Check if JavaScript is enabled
- Verify dropdown options are clickable
- Increase wait times after selecting options

### Issue: Navigation test fails
**Solution**:
- Check if links are JavaScript-based
- Verify product URLs match expected pattern
- Increase navigation timeout

---

## Quick Reference

```bash
# Validate all data center pages
python run_product_series_validation.py

# Validate specific series
python run_product_series_validation.py D3
python run_product_series_validation.py D5
python run_product_series_validation.py D7

# Check reports folder for Excel file
```

---

## Validation Time

- **Per Series**: 2-5 minutes
- **All Series**: 6-15 minutes
- **Total**: Includes navigation, filtering tests, and report generation

