# D3 Series Validation Checklist

## URL Being Validated
**https://www.solidigm.com/products/data-center/d3.html**

---

## 1. Page Structure Validation

### ✅ Page Load
- **Check**: Page loads successfully
- **Validates**: Browser can navigate to the URL
- **Expected**: Page title should be present

### ✅ Main Title (H1)
- **Check**: H1 element exists on the page
- **Validates**: Title text matches expected series name
- **Expected**: "SSD D3 Series" should be in the title
- **Extracts**: Full title text

### ✅ Breadcrumbs Navigation
- **Check**: Breadcrumb navigation exists
- **Validates**: Breadcrumb trail is present
- **Expected**: Should show path like "Data Center > SSD D3 Series"
- **Extracts**: All breadcrumb items

### ✅ Series Description
- **Check**: Description paragraph exists
- **Validates**: Description text is present
- **Expected**: Should contain keywords like "engineered", "optimized", or "value-optimized"
- **Extracts**: First 200 characters of description

---

## 2. Products Validation

### ✅ Product Count
- **Check**: Number of product cards on the page
- **Expected**: **2 products** should be found
- **Validates**: Actual count matches expected count

### ✅ Expected Products Verification
The validator checks for these **2 specific products**:

#### Product 1: **D3-S4620**
- **Product ID**: D3-S4620
- **Name**: D3-S4620
- **Description**: "Mid-endurance SATA drives available in capacities up to 3.84 TB, designed to increase server efficiency and boost IOPS/TB performance over legacy hard disk drives (HDDs)."
- **Interface**: SATA 3.0 6Gb/s
- **Form Factor**: 2.5" 7mm
- **Capacity**: 3.84TB - 480GB

#### Product 2: **D3-S4520**
- **Product ID**: D3-S4520
- **Name**: D3-S4520
- **Description**: "Standard-endurance SATA drives with capacities up to 7.68 TB, designed to increase server efficiency and boost IOPS/TB performance over legacy hard disk drives (HDDs) for cloud storage."
- **Interface**: SATA 3.0 6Gb/s
- **Form Factor**: 2.5" 7mm / M.2 80mm
- **Capacity**: 7.68TB - 240GB

### ✅ Individual Product Card Validation
For each product card found, the validator checks:

1. **Product ID/Name**
   - Extracts product identifier (e.g., "D3-S4620")
   - Uses regex pattern: `[D][357]-\w+`
   - Checks if it matches expected product IDs

2. **Product Description**
   - Extracts description text
   - Captures first 200 characters

3. **Product Specifications**
   - **Interface**: Extracts interface type (e.g., "SATA 3.0 6Gb/s")
   - **Form Factor**: Extracts form factor (e.g., "2.5" 7mm")
   - **Capacity**: Extracts capacity range (e.g., "3.84TB - 480GB")

4. **View Details Link**
   - Checks for "View Details" link/button
   - Extracts the href URL
   - Validates link exists

5. **Compare Button**
   - Checks if "Compare" button exists
   - Validates comparison feature is available

6. **Product Image**
   - Checks for product image
   - Extracts image source URL
   - Extracts alt text

### ✅ Product Matching
- **Check**: All expected products are found on the page
- **Expected Products**: D3-S4620, D3-S4520
- **Validates**: Found products match expected products list
- **Result**: Should find 2/2 expected products

---

## 3. Filters Validation

### ✅ Filter Section
- **Check**: Filter section exists on the page
- **Validates**: Filter UI is present

### ✅ Interface Filter
- **Check**: Interface filter button/select exists
- **Validates**: Filter for "Interface" is available
- **Expected**: Should be able to filter by interface type

### ✅ Form Factor Filter
- **Check**: Form Factor filter button/select exists
- **Validates**: Filter for "Form Factor" is available
- **Expected**: Should be able to filter by form factor

### ✅ Capacity Filter
- **Check**: Capacity filter button/select exists
- **Validates**: Filter for "Capacity" is available
- **Expected**: Should be able to filter by capacity range

---

## 4. Links Validation

### ✅ View Details Links
- **Check**: All "View Details" links are valid
- **Validates**: Each product's "View Details" link
- **HTTP Check**: Makes HTTP request to verify link status
- **Valid Status**: 200-399 status codes
- **Expected**: 2 links (one per product)

### ✅ Link Status
- **Valid Links**: Count of links returning 200-399
- **Invalid Links**: Count of links returning 400+ or errors
- **Result**: All links should be valid

---

## 5. Comparison Feature Validation

### ✅ Comparison UI
- **Check**: Comparison buttons/feature exists
- **Validates**: Product comparison functionality is available
- **Expected**: Maximum 5 products can be selected for comparison

### ✅ Comparison Buttons
- **Check**: "Compare" buttons are present on product cards
- **Validates**: Comparison feature is accessible

---

## 6. Related Articles Validation

### ✅ Articles Section
- **Check**: "Related Articles" section exists
- **Validates**: Related articles section is present on the page

### ✅ Article Count
- **Check**: Number of related articles
- **Extracts**: Count of article links/cards
- **Example**: Should find at least 1 related article

---

## Summary Validation Results

After validation, the following summary is generated:

- ✅ **Page Loaded**: Yes/No
- ✅ **Title Found**: Yes/No
- ✅ **Expected Products**: 2
- ✅ **Found Products**: Actual count
- ✅ **All Products Found**: Yes/No (should be Yes if both D3-S4620 and D3-S4520 are found)
- ✅ **Filters Working**: Yes/No
- ✅ **Links Valid**: Yes/No (all View Details links should be valid)
- ✅ **Comparison Working**: Yes/No

---

## Excel Report Output

The validation generates an Excel report with a **"D3 Series"** sheet containing:

1. **Page Structure Section**
   - Page Loaded status
   - Title text
   - Breadcrumbs trail
   - Description text

2. **Products Section**
   - Total products found
   - Expected product IDs
   - Found product IDs
   - **Detailed Product Table** with columns:
     - # (index)
     - Product ID
     - Name
     - Interface
     - Form Factor
     - Capacity
     - View Details Link

3. **Filters Section**
   - Filters found status
   - Interface filter status
   - Form Factor filter status
   - Capacity filter status

4. **Links Section**
   - Total links checked
   - Valid links count
   - Invalid links count

5. **Comparison Section**
   - Comparison feature found
   - Maximum products allowed

6. **Related Articles Section**
   - Section found status
   - Article count

---

## Expected Validation Output

```
================================================================================
PRODUCT SERIES PAGE VALIDATION
================================================================================

[INFO] Navigating to https://www.solidigm.com/products/data-center/d3.html

[PAGE STRUCTURE] Validating page structure...
   [OK] Page loaded: SSD D3 Series | Solidigm
   [OK] Title: 'SSD D3 Series'
   [OK] Title matches expected series name
   [OK] Breadcrumbs found: Data Center > SSD D3 Series
   [OK] Description found

[PRODUCTS] Validating products...
   [OK] Found 2 product cards
      [OK] Product 1: D3-S4620
              Interface: SATA 3.0 6Gb/s
      [OK] Product 2: D3-S4520
              Interface: SATA 3.0 6Gb/s
   [OK] Found 2/2 expected products

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

================================================================================
PRODUCT SERIES VALIDATION SUMMARY
================================================================================
Series: D3
Page Loaded: Yes
Title Found: Yes
Expected Products: 2
Found Products: 2
All Products Found: Yes
Filters Working: Yes
Links Valid: Yes
Comparison Working: Yes
```

---

## Key Validation Points for D3

1. **Must find exactly 2 products**: D3-S4620 and D3-S4520
2. **Both products should have SATA 3.0 6Gb/s interface**
3. **Both should have "View Details" links that are valid**
4. **Filters should be functional** (Interface, Form Factor, Capacity)
5. **Page title should contain "SSD D3 Series"**
6. **Breadcrumbs should show navigation path**

