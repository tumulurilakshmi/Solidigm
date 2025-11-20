# D3 Series - Hero Component Validation

## Overview
The hero component validator validates the hero section at the top of the D3 series page (https://www.solidigm.com/products/data-center/d3.html).

---

## What Gets Validated

### 1. ✅ Container Size
**What is checked:**
- Hero container dimensions (width x height in pixels)
- Container element is found and measurable

**Extracted Data:**
- Width (px)
- Height (px)
- Width as string (e.g., "1920px")
- Height as string (e.g., "1080px")

**Expected Output:**
```
[CONTAINER] Validating container size...
   [OK] Container size: 1920x600 px
```

---

### 2. ✅ Background Image
**What is checked:**
- Desktop background image exists
- Mobile background image exists (if present)
- Image source URL
- Image alt text
- Image dimensions (natural width/height)
- Image loading status

**Extracted Data:**
- Desktop image:
  - Source URL
  - Alt text
  - Width x Height
  - Loading attribute
  - Loaded status (complete)
- Mobile image:
  - Source URL
  - Alt text
  - Width x Height
  - Loading attribute

**Expected Output:**
```
[BACKGROUND] Validating background image...
   [OK] Desktop background image found
        Source: https://s7d9.scene7.com/is/image/Solidigm/solidigm-d3-tlc-nand-ssd?fmt=avif
        Size: 1920x600
        Loaded: True
   [OK] Mobile background image found
```

**Based on HTML:**
- Desktop: `.cmp-hero__background-image--desktop img`
- Mobile: `.cmp-hero__background-image--mobile img`
- Expected source: `https://s7d9.scene7.com/is/image/Solidigm/solidigm-d3-tlc-nand-ssd?fmt=avif`
- Expected alt: "Legacy data center with Solidigm D3 SSDs"

---

### 3. ✅ Breadcrumbs Details
**What is checked:**
- Breadcrumb navigation exists
- Number of breadcrumb levels
- Each level's text content
- Each level's clickability (all except last should be clickable)
- Each level's font details (size, color, family, weight)
- Each level's href (if clickable)
- Last level should NOT be clickable (current page indicator)

**Extracted Data for Each Level:**
- Level number (1, 2, 3, etc.)
- Text content
- Is clickable (Yes/No)
- Is last level (Yes/No)
- Font size
- Font color (RGB)
- Font family
- Font weight
- Href URL (if clickable)

**Expected Breadcrumbs for D3:**
1. **Level 1: "Data Center"**
   - Clickable: ✅ Yes
   - Href: `/products/data-center.html`
   - Is Last: ❌ No
   - Font details: Extracted from computed styles

2. **Level 2: "SSD D3 Series"**
   - Clickable: ❌ No (current page)
   - Href: None
   - Is Last: ✅ Yes (has `aria-current="page"` or `cmp-breadcrumb__item--active`)
   - Font details: Extracted from computed styles

**Expected Output:**
```
[BREADCRUMBS] Validating breadcrumbs...
   [OK] Breadcrumbs found: 2 levels
      [OK] Level 1: 'Data Center'
          Clickable: True, Last: False
          Font: 14px, Color: rgb(0, 0, 0)
      [OK] Level 2: 'SSD D3 Series'
          Clickable: False, Last: True
          Font: 14px, Color: rgb(0, 0, 0)
```

**Validation Rules:**
- ✅ All breadcrumb items except the last one MUST be clickable
- ✅ The last breadcrumb item (current page) MUST NOT be clickable
- ✅ Warnings are shown if these rules are violated

---

### 4. ✅ Hero Title Text
**What is checked:**
- Title element exists (h1.cmp-hero__title)
- Title text content
- Font size
- Font color (RGB)
- Font family
- Font weight
- Line height

**Extracted Data:**
- Text: "SSD D3 Series"
- Font size (e.g., "48px")
- Font color (e.g., "rgb(255, 255, 255)")
- Font family (e.g., "Arial, sans-serif")
- Font weight (e.g., "700" or "bold")
- Line height (e.g., "1.2")

**Expected Output:**
```
[TITLE] Validating hero title...
   [OK] Title: 'SSD D3 Series'
        Font Size: 48px
        Font Color: rgb(255, 255, 255)
        Font Family: "Solidigm Sans", Arial, sans-serif
        Font Weight: 700
```

**Based on HTML:**
- Selector: `h1.cmp-hero__title`
- Expected text: "SSD D3 Series"

---

### 5. ✅ Hero Description Text
**What is checked:**
- Description element exists (.cmp-hero__description)
- Description text content
- Font size
- Font color (RGB)
- Font family
- Font weight
- Line height

**Extracted Data:**
- Text: Full description text
- Font size (e.g., "16px")
- Font color (e.g., "rgb(255, 255, 255)")
- Font family (e.g., "Arial, sans-serif")
- Font weight (e.g., "400" or "normal")
- Line height (e.g., "1.5")

**Expected Output:**
```
[DESCRIPTION] Validating hero description...
   [OK] Description found
        Text: 'Drives in the value-optimized Solidigm D3 Series are engineered to accelerate storage performance and reduce Total Cost of Ownership while preserving legacy infrastructure with exceptional reliability.'
        Font Size: 16px
        Font Color: rgb(255, 255, 255)
        Font Family: "Solidigm Sans", Arial, sans-serif
```

**Based on HTML:**
- Selector: `.cmp-hero__description p` or `.cmp-hero__description`
- Expected text: "Drives in the value-optimized Solidigm D3 Series are engineered to accelerate storage performance and reduce Total Cost of Ownership while preserving legacy infrastructure with exceptional reliability."

---

## Complete Validation Flow

When running the D3 series validation, the hero component is validated first:

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
   [OK] Mobile background image found

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
        Font Family: "Solidigm Sans", Arial, sans-serif

================================================================================
HERO COMPONENT SUMMARY
================================================================================
Container Found: Yes
Background Found: Yes
Breadcrumbs Found: Yes
Title Found: Yes
Description Found: Yes
All Breadcrumbs Clickable (except last): Yes

Container Size: 1920x600 px
Breadcrumb Levels: 2
  Level 1: 'Data Center' - Clickable: True, Last: False
  Level 2: 'SSD D3 Series' - Clickable: False, Last: True
```

---

## Excel Report Output

The hero component data is included in the Excel report under the **"D3 Series"** sheet:

### Hero Component Section:
1. **Hero Found**: Yes/No
2. **Container Size**: Width x Height (px)
3. **Background Image**: 
   - Desktop image URL
   - Desktop image dimensions
4. **Breadcrumbs Table**:
   - Level | Text | Clickable | Is Last | Font Size | Font Color | Href
5. **Hero Title**:
   - Title Text
   - Font Size
   - Font Color
   - Font Family
   - Font Weight
6. **Hero Description**:
   - Description Text
   - Font Size
   - Font Color
   - Font Family
   - Font Weight

---

## Key Validation Points

1. ✅ **Container must be found** and have measurable dimensions
2. ✅ **Background images** (desktop and mobile) must exist and load
3. ✅ **Breadcrumbs** must have at least 2 levels for D3
4. ✅ **Breadcrumb rule**: All except last must be clickable
5. ✅ **Title** must be "SSD D3 Series" with proper font styling
6. ✅ **Description** must contain the expected text with proper font styling
7. ✅ **All font details** are extracted from computed styles (actual rendered values)

---

## CSS Selectors Used

- Hero container: `.cmp-hero, .hero`
- Desktop background: `.cmp-hero__background-image--desktop img`
- Mobile background: `.cmp-hero__background-image--mobile img`
- Breadcrumbs: `.cmp-breadcrumb, nav[aria-label*="breadcrumb"]`
- Breadcrumb items: `.cmp-breadcrumb__item, li[itemprop="itemListElement"]`
- Breadcrumb links: `.cmp-breadcrumb__item-link, a[itemprop="item"]`
- Title: `h1.cmp-hero__title, .cmp-hero__title`
- Description: `.cmp-hero__description, .cmp-hero__description p`

---

## Integration

The hero component validator is automatically called when validating any product series page (D3, D5, D7) using:

```python
python run_product_series_validation.py D3
```

The hero validation runs first, before other page validations.

