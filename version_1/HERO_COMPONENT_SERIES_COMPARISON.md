# Hero Component - Series Comparison (D3, D5, D7)

## Overview
The hero component validator uses the **same code** for all three series (D3, D5, D7). It dynamically extracts and identifies the text and details specific to each series.

---

## What Gets Extracted (Same for All Series)

### 1. Container Size
- **Extracted**: Width x Height (pixels)
- **Same for all**: Yes - dynamically measured

### 2. Background Image
- **Extracted**: 
  - Desktop image URL
  - Mobile image URL
  - Image dimensions
  - Alt text
  - Loading status
- **Different per series**: Yes - each series has different image URLs

### 3. Breadcrumbs
- **Extracted for each level**:
  - Text content
  - Clickability status
  - Href (if clickable)
  - Font size, color, family, weight
- **Different per series**: 
  - **Level 1**: Same for all ("Data Center")
  - **Level 2**: Different text per series

### 4. Hero Title
- **Extracted**:
  - Text content
  - Font size, color, family, weight, line height
- **Different per series**: Yes - different title text

### 5. Hero Description
- **Extracted**:
  - Text content
  - Font size, color, family, weight, line height
- **Different per series**: Yes - different description text

---

## Series-Specific Text Details

### D3 Series
**URL**: https://www.solidigm.com/products/data-center/d3.html

**Breadcrumbs**:
- Level 1: "Data Center" (clickable → `/products/data-center.html`)
- Level 2: "SSD D3 Series" (not clickable - current page)

**Title**: "SSD D3 Series"

**Description**: "Drives in the value-optimized Solidigm D3 Series are engineered to accelerate storage performance and reduce Total Cost of Ownership while preserving legacy infrastructure with exceptional reliability."

**Background Image**: 
- Desktop: `https://s7d9.scene7.com/is/image/Solidigm/solidigm-d3-tlc-nand-ssd?fmt=avif`
- Alt: "Legacy data center with Solidigm D3 SSDs"

---

### D5 Series
**URL**: https://www.solidigm.com/products/data-center/d5.html

**Breadcrumbs**:
- Level 1: "Data Center" (clickable → `/products/data-center.html`)
- Level 2: "D5 Series SSDs" (not clickable - current page)

**Title**: "D5 Series SSDs" (or "D5 Series SSDs")

**Description**: "Hyper-dense, power-efficient SSDs optimized for read-intensive, data-intensive, and mainstream workloads. Maximize space, power, and capacity with our flagship, industry-leading 122TB D5-P5336 SSDs."

**Background Image**: 
- Desktop: Different image URL (D5-specific)
- Alt: D5-specific alt text

---

### D7 Series
**URL**: https://www.solidigm.com/products/data-center/d7.html

**Breadcrumbs**:
- Level 1: "Data Center" (clickable → `/products/data-center.html`)
- Level 2: "SSD D7 Series" (not clickable - current page)

**Title**: "SSD D7 Series" (or "D7 Series SSDs")

**Description**: "Our highest-performing family of SSDs, the Solidigm D7 Series is engineered for the most demanding workloads."

**Background Image**: 
- Desktop: Different image URL (D7-specific)
- Alt: D7-specific alt text

---

## How Series Identification Works

The validator automatically identifies which series it's validating by:

1. **Checking Title Text**:
   - If title contains "SSD D3 Series" → Identifies as **D3**
   - If title contains "D5 Series SSDs" → Identifies as **D5**
   - If title contains "SSD D7 Series" → Identifies as **D7**

2. **Confidence Level**:
   - **High**: When title text clearly matches a series pattern
   - **Low**: When series cannot be determined from text

3. **Output**:
   ```
   [INFO] Series identified: D3 (confidence: high)
   ```

---

## Validation Output Comparison

### D3 Series Output
```
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
        Font Family: "Solidigm Sans", Arial, sans-serif
        Font Weight: 700

[DESCRIPTION] Validating hero description...
   [OK] Description found
        Text: 'Drives in the value-optimized Solidigm D3 Series are engineered...'
        Font Size: 16px
        Font Color: rgb(255, 255, 255)

[INFO] Series identified: D3 (confidence: high)

================================================================================
HERO COMPONENT SUMMARY
================================================================================
Series Identified: D3 (confidence: high)
Container Found: Yes
Background Found: Yes
Breadcrumbs Found: Yes
Title Found: Yes
Description Found: Yes
All Breadcrumbs Clickable (except last): Yes

Container Size: 1920x600 px

Extracted Title Text: 'SSD D3 Series'
Extracted Description: 'Drives in the value-optimized Solidigm D3 Series are engineered to accelerate storage performance and reduce Total Cost of Ownership while preserving legacy infrastructure with exceptional reliability.'

Breadcrumb Levels: 2
  Level 1: 'Data Center' - Clickable: True, Last: False
    → Link: /products/data-center.html
  Level 2: 'SSD D3 Series' - Clickable: False, Last: True
```

### D5 Series Output
```
[INFO] Series identified: D5 (confidence: high)
...
Extracted Title Text: 'D5 Series SSDs'
Extracted Description: 'Hyper-dense, power-efficient SSDs optimized for read-intensive, data-intensive, and mainstream workloads. Maximize space, power, and capacity with our flagship, industry-leading 122TB D5-P5336 SSDs.'
...
  Level 2: 'D5 Series SSDs' - Clickable: False, Last: True
```

### D7 Series Output
```
[INFO] Series identified: D7 (confidence: high)
...
Extracted Title Text: 'SSD D7 Series'
Extracted Description: 'Our highest-performing family of SSDs, the Solidigm D7 Series is engineered for the most demanding workloads.'
...
  Level 2: 'SSD D7 Series' - Clickable: False, Last: True
```

---

## Key Points

1. ✅ **Same Code**: The validator uses identical code for D3, D5, and D7
2. ✅ **Dynamic Extraction**: All text and details are extracted dynamically from the page
3. ✅ **Series Identification**: Automatically identifies which series based on extracted text
4. ✅ **No Hardcoded Values**: No series-specific hardcoded text or values
5. ✅ **Consistent Structure**: All series have the same structure:
   - Same container size measurement
   - Same breadcrumb validation logic
   - Same title/description extraction
   - Same font detail extraction

---

## Excel Report Output

The Excel report includes all extracted details for each series:

**D3 Series Sheet**:
- Extracted Title: "SSD D3 Series"
- Extracted Description: "Drives in the value-optimized..."
- Breadcrumb Level 2: "SSD D3 Series"

**D5 Series Sheet**:
- Extracted Title: "D5 Series SSDs"
- Extracted Description: "Hyper-dense, power-efficient..."
- Breadcrumb Level 2: "D5 Series SSDs"

**D7 Series Sheet**:
- Extracted Title: "SSD D7 Series"
- Extracted Description: "Our highest-performing family..."
- Breadcrumb Level 2: "SSD D7 Series"

---

## Usage

The same validator works for all series:

```bash
# Validates D3 - automatically identifies and extracts D3-specific text
python run_product_series_validation.py D3

# Validates D5 - automatically identifies and extracts D5-specific text
python run_product_series_validation.py D5

# Validates D7 - automatically identifies and extracts D7-specific text
python run_product_series_validation.py D7

# Validates all - extracts text for each series separately
python run_product_series_validation.py
```

The validator will automatically:
1. Extract the correct title text for each series
2. Extract the correct description text for each series
3. Extract the correct breadcrumb text for each series
4. Identify which series it's validating
5. Report all details in the Excel report

