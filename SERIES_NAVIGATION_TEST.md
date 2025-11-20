# Series Navigation Test Guide

## Overview
This test validates that users can navigate to D3, D5, and D7 series pages through the Product menu in the navigation.

## Navigation Paths Tested

1. **Product > D3 Series** → Should navigate to `/products/data-center/d3.html`
2. **Product > D5 Series** → Should navigate to `/products/data-center/d5.html`
3. **Product > D7 Series** → Should navigate to `/products/data-center/d7.html`

---

## How to Run

### Standalone Navigation Test
```bash
python run_series_navigation_test.py
```

This will:
1. Navigate to homepage
2. Test Product > D3 Series navigation
3. Return to homepage
4. Test Product > D5 Series navigation
5. Return to homepage
6. Test Product > D7 Series navigation
7. Report results

---

## What Gets Tested

### For Each Series (D3, D5, D7):

1. **Step 1: Find Product Menu**
   - Locates the "Product" menu item in navigation
   - Verifies menu is visible and accessible

2. **Step 2: Open Product Submenu**
   - Hovers over or clicks Product menu
   - Waits for submenu/mega menu to appear

3. **Step 3: Find Series Link**
   - Searches for series link (e.g., "D3 Series", "D5 Series", "D7 Series")
   - Tries multiple selectors to find the link
   - Verifies link is visible

4. **Step 4: Click Series Link**
   - Clicks the series link
   - Waits for page navigation

5. **Step 5: Verify Navigation**
   - Checks if URL changed
   - Verifies URL matches expected path:
     - D3: `/products/data-center/d3.html`
     - D5: `/products/data-center/d5.html`
     - D7: `/products/data-center/d7.html`

---

## Expected Output

```
================================================================================
SERIES NAVIGATION VALIDATION
================================================================================

[INFO] Navigating to https://www.solidigm.com/

[D3 SERIES] Testing Product > D3 Series navigation...
   [STEP 1] Finding Product menu...
      [OK] Product menu found
   [STEP 2] Finding D3 Series submenu...
      [OK] D3 Series submenu found
   [STEP 3] Clicking D3 Series link...
   [STEP 4] Verifying navigation...
      [OK] Navigation successful!
         Current URL: https://www.solidigm.com/products/data-center/d3.html
         Expected path: /products/data-center/d3.html

[D5 SERIES] Testing Product > D5 Series navigation...
   [STEP 1] Finding Product menu...
      [OK] Product menu found
   [STEP 2] Finding D5 Series submenu...
      [OK] D5 Series submenu found
   [STEP 3] Clicking D5 Series link...
   [STEP 4] Verifying navigation...
      [OK] Navigation successful!
         Current URL: https://www.solidigm.com/products/data-center/d5.html
         Expected path: /products/data-center/d5.html

[D7 SERIES] Testing Product > D7 Series navigation...
   [STEP 1] Finding Product menu...
      [OK] Product menu found
   [STEP 2] Finding D7 Series submenu...
      [OK] D7 Series submenu found
   [STEP 3] Clicking D7 Series link...
   [STEP 4] Verifying navigation...
      [OK] Navigation successful!
         Current URL: https://www.solidigm.com/products/data-center/d7.html
         Expected path: /products/data-center/d7.html

================================================================================
SERIES NAVIGATION SUMMARY
================================================================================
D3 Series Navigation: ✓ Success
D5 Series Navigation: ✓ Success
D7 Series Navigation: ✓ Success
All Navigations: ✓ Success
```

---

## Test Results

The test returns detailed results for each series:

- **Menu Found**: Whether Product menu was located
- **Submenu Found**: Whether series submenu was found
- **Navigation Success**: Whether click resulted in navigation
- **URL Matches**: Whether final URL matches expected path
- **Final URL**: The actual URL after navigation
- **Steps**: Detailed list of steps taken

---

## Integration

The navigation test can be integrated into the product series validation:

```python
from series_navigation_validator import SeriesNavigationValidator

# In your validation script
nav_validator = SeriesNavigationValidator(page)
nav_results = nav_validator.validate_series_navigation("https://www.solidigm.com/")
```

---

## Troubleshooting

### Issue: Product menu not found
**Solution**: 
- Check if navigation structure has changed
- Verify CSS selectors in `series_navigation_validator.py`
- Ensure page is fully loaded before testing

### Issue: Submenu not found
**Solution**:
- Menu may require hover to open
- Check if mega menu structure has changed
- Verify series link text matches expected format

### Issue: Navigation doesn't work
**Solution**:
- Check if links are JavaScript-based (may need different click method)
- Verify page load timeouts are sufficient
- Check browser console for JavaScript errors

---

## Notes

- The test navigates back to homepage after each series test
- Only one navigation per series is tested to avoid excessive page loads
- The test uses multiple selectors to find series links for robustness
- All navigation steps are logged for debugging

