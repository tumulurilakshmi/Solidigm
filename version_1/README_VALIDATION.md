# Solidigm Website Validation Tool

A comprehensive automated testing tool for validating Solidigm website UI elements and link functionality.

## Features

- ✅ **Complete UI Validation** - Validates font sizes, font colors, element sizes, images, buttons, and navigation
- 🔗 **Broken Link Detection** - Checks all links on the page for validity
- 📊 **Detailed Reporting** - Generates multiple report formats (TXT, HTML, JSON)
- 🌍 **Locale Support** - Run validation for different locales (US/EN, etc.)
- 📝 **Batch Processing** - Process multiple URLs from a file

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install
```

## Usage

### Basic Usage

Create a text file (e.g., `urls.txt`) with URLs to validate:

```
# Format: URL | locale
https://www.solidigm.com/ | US/EN
https://www.solidigm.com/products | US/EN
```

Run the validation:
```bash
python run_validation.py urls.txt
```

### Input File Format

The input file supports the following format:

```
# Comments start with #
# Empty lines are ignored

# Format: URL | locale
https://www.solidigm.com/ | US/EN
https://www.solidigm.com/products | US/EN

# Without locale (defaults to US/EN)
https://www.solidigm.com/support
```

### Example Input File

See `urls.txt` for an example:

```
# Solidigm URL Validation List
https://www.solidigm.com/ | US/EN
```

## What Gets Validated

### UI Validation

1. **Font Sizes** (h1, h2, h3, p, navigation links)
   - Validates against expected sizes
   - Tracks failures with actual vs expected values

2. **Font Colors** (headings, paragraphs)
   - Validates text colors
   - Detailed color mismatch reporting

3. **Element Sizes** (header, footer)
   - Validates width and height
   - Tracks dimensional mismatches

4. **Images**
   - Checks image presence and load status
   - Validates image source links

5. **Buttons/CTAs**
   - Validates button visibility and enabled state
   - Checks button functionality

6. **Navigation**
   - Validates navigation links
   - Checks link accessibility

### Link Validation

- **Total Links** - Count of all links on page
- **Valid Links** - Links that return 200-399 status codes
- **Broken Links** - Links that return 4xx/5xx or timeout
- **Broken Link Details** - Includes URL, text, status code, and error message

## Reports

The tool generates three types of reports for each URL:

1. **Text Report** (`validation_report_TIMESTAMP.txt`)
   - Detailed text-based report
   - Easy to read and share
   - Includes failure details

2. **HTML Report** (`validation_report_TIMESTAMP.html`)
   - Beautiful web-based report
   - Color-coded success/failure indicators
   - Interactive and visual

3. **JSON Report** (`validation_report_TIMESTAMP.json`)
   - Machine-readable format
   - Easy integration with other tools
   - Contains all raw data

4. **Summary Report** (`summary_report_TIMESTAMP.txt`)
   - Overview of all URL validations
   - Quick summary of results

### Report Contents

Each report includes:

- **Validation Information**
  - URL tested
  - Locale used
  - Timestamp

- **Overall Summary**
  - Total UI validations performed
  - Passed/Failed counts
  - Total links checked
  - Valid/Broken link counts

- **Category Breakdown**
  - Font size validation results
  - Font color validation results
  - Element size validation results
  - Image validation results
  - Button validation results
  - Navigation validation results

- **Failure Details**
  - What failed (e.g., "Font size failed for h1")
  - Actual vs expected values
  - Specific error messages

- **Broken Links Details**
  - List of broken links with:
    - URL
    - Link text
    - HTTP status code
    - Error message

## Configuration

Edit `config.py` to customize settings:

- `BROWSER` - Browser to use (chromium, firefox, webkit)
- `HEADLESS` - Run in headless mode
- `VIEWPORT` - Browser viewport size
- `TIMEOUT` - Default timeout
- `NAVIGATION_TIMEOUT` - Navigation timeout

## Output Structure

```
e:\Solidigm\
├── run_validation.py          # Main validation script
├── comprehensive_validator.py  # Validation logic
├── report_generator.py        # Report generation
├── urls.txt                   # Input file
├── config.py                  # Configuration
├── reports/                   # Generated reports
│   ├── validation_report_*.txt
│   ├── validation_report_*.html
│   ├── validation_report_*.json
│   └── summary_report_*.txt
└── screenshots/               # Screenshots (if enabled)
```

## Example Usage Flow

1. **Prepare input file** (`urls.txt`):
```
https://www.solidigm.com/ | US/EN
```

2. **Run validation**:
```bash
python run_validation.py urls.txt
```

3. **Check results**:
```
reports/
├── validation_report_20250115_143022.txt
├── validation_report_20250115_143022.html
├── validation_report_20250115_143022.json
└── summary_report_20250115_143022.txt
```

## Report Example

### Overall Summary
```
Total UI Validations Performed: 25
UI Validations Passed: 23
UI Validations Failed: 2
Total Links Checked: 142
Valid Links: 138
Broken Links: 4
```

### Category Breakdown
```
FONT SIZE:
  Total: 5
  Passed: 4
  Failed: 1
  Failure Details:
    - Font size failed for h1 - Expected: 48px, Got: 42px

BROKEN LINKS:
  URL: https://www.solidigm.com/old-page
  Text: Learn More
  Status: 404
  Message: Link invalid: https://www.solidigm.com/old-page (Status: 404)
```

## Troubleshooting

### Browser Not Found
```bash
playwright install
```

### Connection Timeout
Increase timeout in `config.py`:
```python
TIMEOUT = 60000  # 60 seconds
NAVIGATION_TIMEOUT = 60000
```

### File Not Found Error
Make sure the input file exists and has the correct format.

## Requirements

- Python 3.8+
- Playwright
- requests
- Pillow

Install all requirements:
```bash
pip install -r requirements.txt
playwright install
```

