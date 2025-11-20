# Steps to Execute Home Page Validation

## Prerequisites

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- playwright (browser automation)
- pytest (testing framework)
- openpyxl (Excel report generation)
- requests (HTTP requests)
- Pillow (image processing)
- python-dotenv (environment variables)

### Step 2: Install Playwright Browsers
```bash
playwright install
```

This downloads the Chromium browser that will be used for validation.

---

## Execution Steps

### Step 3: Run Home Page Validation

#### Option A: Run with Default URL (https://www.solidigm.com/)
```bash
python run_homepage_validation.py
```

#### Option B: Run with Custom URL
```bash
python run_homepage_validation.py https://www.solidigm.com/
```

Or for a different URL:
```bash
python run_homepage_validation.py https://www.solidigm.com/products
```

---

## What Happens During Execution

1. **Browser Launch**: Opens Chromium browser (visible window by default)
2. **Page Navigation**: Navigates to the specified URL
3. **Component Validation**: Validates all homepage components:
   - Navigation menu
   - Carousels
   - Featured Products
   - Product Cards
   - Article List
   - Blade Components
   - Footer
4. **Report Generation**: Creates an Excel report with detailed validation results
5. **Summary Display**: Shows validation summary in the console

---

## Output Files

After execution, you'll find:

### Excel Report
- **Location**: `reports/` directory
- **Filename**: `homepage_validation_report_[timestamp].xlsx`
- **Contains**: Multiple sheets with detailed validation data for each component

### Console Output
- Real-time validation progress
- Component-by-component validation results
- Summary statistics

---

## Validation Components

The script validates:

1. ✅ **Navigation** - Menu items, fonts, colors, links
2. ✅ **Carousels** - Slides, images, navigation arrows, progress bar
3. ✅ **Featured Products** - Product count, details, links
4. ✅ **Product Cards** - Card information, images, links
5. ✅ **Article List** - Article cards, titles, categories, images
6. ✅ **Blade Components** - Left/right image layouts
7. ✅ **Footer** - Links, sections, structure

---

## Troubleshooting

### Issue: "playwright not found"
**Solution**: Run `playwright install` again

### Issue: "Module not found"
**Solution**: 
```bash
pip install -r requirements.txt
```

### Issue: Browser doesn't open
**Solution**: Check if headless mode is disabled in `run_homepage_validation.py` (line 21: `headless=False`)

### Issue: Timeout errors
**Solution**: The script has a 120-second timeout. If pages load slowly, you may need to increase the timeout in the script.

---

## Advanced Options

### Run in Headless Mode (No Browser Window)
Edit `run_homepage_validation.py` line 21:
```python
browser = playwright.chromium.launch(headless=True, args=['--no-sandbox'])
```

### Change Viewport Size
Edit `run_homepage_validation.py` line 22:
```python
page = browser.new_page(viewport={'width': 1920, 'height': 1080})
```

### Increase Timeout
Edit `run_homepage_validation.py` line 23:
```python
page.set_default_timeout(180000)  # 3 minutes
```

---

## Quick Reference

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install browsers
playwright install

# 3. Run validation
python run_homepage_validation.py

# 4. Check reports folder for Excel file
```

---

## Expected Console Output

```
====================================================================================================
                         SOLIDIGM HOMEPAGE COMPREHENSIVE VALIDATION
====================================================================================================

[INFO] Navigating to: https://www.solidigm.com/
[INFO] Page loaded successfully

[Navigation] Validating navigation menu...
[Carousel] Validating carousels...
[Featured Products] Validating featured products...
...

[SUCCESS] Excel report saved: reports/homepage_validation_report_20250115_143022.xlsx

====================================================================================================
VALIDATION COMPLETE
====================================================================================================

[SUMMARY]
  Carousels: 2
  Featured Products: 1
  Product Cards: 12
  Articles: 6
  Blade Components: 3
  Footer: Yes
```

---

## Notes

- The browser window will remain open during validation (unless headless mode is enabled)
- Validation may take 2-5 minutes depending on page complexity
- All reports are saved with timestamps for easy tracking
- The Excel report contains detailed validation data in multiple sheets

