# Data Center Landing Page Validation Steps

## URL
**https://www.solidigm.com/products/data-center.html**

This is the main Data Center landing page that shows all three series (D3, D5, D7) together.

---

## Quick Start

```bash
python run_data_center_page_validation.py
```

---

## Complete Validation Flow

### Step 1: Navigate to Landing Page
- Navigates to `https://www.solidigm.com/products/data-center.html`
- Waits for page to load
- Verifies page title

### Step 2: Validate Hero Component
**Validates:**
1. ✅ **Container Size** - Width x Height (pixels)
2. ✅ **Background Image** - Desktop and mobile images
3. ✅ **Breadcrumbs** - Should show "Data Center" (current page, not clickable)
4. ✅ **Hero Title** - "Modernize Your Data Center" with font details
5. ✅ **Hero Description** - Description text with font details

**Expected Breadcrumbs:**
- Level 1: "Data Center" (not clickable - current page)

### Step 3: Validate Series Cards
**Validates:**
- ✅ **D7 Series Card/Link** - Text, href, font details
- ✅ **D5 Series Card/Link** - Text, href, font details
- ✅ **D3 Series Card/Link** - Text, href, font details
- ✅ **Navigation Test** - Clicks D7 link to verify navigation works

**Expected Series Links:**
- D7 Series → `/products/data-center/d7.html`
- D5 Series → `/products/data-center/d5.html`
- D3 Series → `/products/data-center/d3.html`

### Step 4: Validate Model List Section
**Validates:**

1. ✅ **Title**
   - Text: "What Solidigm Data Center SSD Is Right For You?"
   - Font size, color, family, weight

2. ✅ **Three Dropdowns**
   - **Interface Dropdown**: All options with font details
   - **Form Factor Dropdown**: All options with font details
   - **Capacity Dropdown**: All options with font details

3. ✅ **Product Cards (Default - All Products)**
   - Shows products from **ALL three series** (D3, D5, D7 combined)
   - Expected: **10 products total** (2 D3 + 3 D5 + 5 D7)
   - For each card:
     - Container size
     - Image
     - Title (e.g., "D7-P5520", "D5-P5336", "D3-S4620")
     - Description
     - Interface
     - Form Factor
     - Capacity
     - View Details button (text, font details, background color)
     - Compare button (text, font details, background color)
     - View Details link

4. ✅ **Filtering Test**
   - Selects 2nd option from Interface dropdown
   - Selects 2nd option from Form Factor dropdown
   - Selects 2nd option from Capacity dropdown
   - Verifies fewer products are shown
   - Validates filtered cards match selected criteria

5. ✅ **View Details Navigation**
   - Clicks "View Details" on first product card
   - Verifies navigation to PDP page
   - Example: D7-P5520 → `/products/data-center/d7/p5520.html`
   - Navigates back

### Step 5: Validate Related Articles
**Validates:**
- ✅ Article section found
- ✅ Article cards (max 3)
- ✅ For each article:
  - Container size
  - Image
  - Tags (optional)
  - Title
  - Link URL
  - Navigation test

---

## Expected Content

### Hero Section
- **Title**: "Modernize Your Data Center"
- **Description**: "Combining decades of innovation and deep industry insights..."

### Series Cards
The page should show three series:
- **SSD D7 Series** - "Our highest-performing SSDs, engineered for the most demanding workloads."
- **SSD D5 Series** - "Hyper-dense, cost-efficient SSDs optimized for read intensive workloads."
- **SSD D3 Series** - "SSDs designed to improve storage performance and costs on legacy SATA infrastructure."

### Model List Products
**All 10 products from all three series:**
- D7-PS1030, D7-PS1010, D7-P5810, D7-P5620, D7-P5520 (5 products)
- D5-P5336, D5-P5430, D5-P5316 (3 products)
- D3-S4620, D3-S4520 (2 products)

### Related Articles
Expected articles like:
- "How QLC SSDs Provide Value, Performance, and Density"
- "The Value of High-Density Storage at the Edge"
- "Emerging Use Cases for Data Center SSDs from Core to Edge"

---

## Console Output Example

```
================================================================================
DATA CENTER LANDING PAGE VALIDATION
================================================================================

[INFO] Navigating to https://www.solidigm.com/products/data-center.html

[HERO] Validating hero component...
[INFO] Hero component found
[CONTAINER] Container size: 1920x600 px
[BACKGROUND] Desktop background image found
[BREADCRUMBS] Breadcrumbs found: 1 level
   Level 1: 'Data Center' - Clickable: False, Last: True
[TITLE] Title: 'Modernize Your Data Center'
[DESCRIPTION] Description found

[SERIES CARDS] Validating series cards...
   [OK] Found 3 series cards: D7, D5, D3
   [OK] All 3 series (D7, D5, D3) are present
      [OK] D7 Series: 'SSD D7 Series' -> /products/data-center/d7.html
      [OK] D5 Series: 'SSD D5 Series' -> /products/data-center/d5.html
      [OK] D3 Series: 'SSD D3 Series' -> /products/data-center/d3.html

[MODEL LIST] Validating model list section...
[INFO] Model List section found
[TITLE] Title: 'What Solidigm Data Center SSD Is Right For You?'
[DROPDOWNS] All 3 dropdowns found
[PRODUCT CARDS] Found 10 product cards (all series combined)
[FILTERING] Testing filter functionality...
   [OK] Filtered cards count: 3
[RELATED ARTICLES] Related articles found: 3 cards

================================================================================
DATA CENTER PAGE SUMMARY
================================================================================
Hero Found: Yes
Series Cards Found: Yes
All Series Present: Yes
Model List Found: Yes
Related Articles Found: Yes
```

---

## Key Differences from Series Pages

| Feature | Landing Page | Series Page |
|---------|-------------|-------------|
| **URL** | `/products/data-center.html` | `/products/data-center/d3.html` |
| **Breadcrumbs** | 1 level (Data Center) | 2 levels (Data Center > Series) |
| **Hero Title** | "Modernize Your Data Center" | "SSD D3 Series" / "D5 Series SSDs" / "SSD D7 Series" |
| **Products Shown** | All 10 products (D3+D5+D7) | Only products from one series |
| **Series Cards** | Yes (3 cards linking to series pages) | No (already on series page) |

---

## Usage

```bash
# Validate Data Center landing page
python run_data_center_page_validation.py
```

This will validate:
- Hero component
- Series cards (D7, D5, D3)
- Model list with all products
- Filtering functionality
- Related articles

---

## Notes

- The landing page shows **all 10 products** from all three series
- Filters work across all series
- Series cards should navigate to individual series pages
- Model list title: "What Solidigm Data Center SSD Is Right For You?"

