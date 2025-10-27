# Solidigm Website Automation

A comprehensive Playwright-based automation suite for validating the Solidigm website (https://www.solidigm.com/). This project includes UI validation, link checking, and responsive design testing.

## Features

- **UI Validation**: Font sizes, colors, container dimensions, text content, images, and CTA buttons
- **Link Validation**: All internal and external links, image sources, and navigation links
- **Responsive Testing**: Mobile and desktop viewport validation
- **Performance Testing**: Page load times and performance metrics
- **Screenshot Capture**: Automatic screenshots for debugging and documentation

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install
```

### 3. Create Environment File (Optional)

Create a `.env` file to customize settings:

```env
BROWSER=chromium
HEADLESS=false
LOG_LEVEL=INFO
```

## Usage

### Quick Start

Run the main automation script:

```bash
python solidigm_automation.py
```

### Run Tests

Run the pytest test suite:

```bash
pytest test_solidigm.py -v
```

Generate HTML report:

```bash
pytest test_solidigm.py -v --html=report.html
```

### Run Specific Tests

```bash
# Test only UI elements
pytest test_solidigm.py::TestSolidigmWebsite::test_ui_elements -v

# Test only links
pytest test_solidigm.py::TestSolidigmWebsite::test_no_broken_links -v

# Test responsive design
pytest test_solidigm.py::TestSolidigmWebsite::test_responsive_design -v
```

## Configuration

Edit `config.py` to customize:

- **Browser settings**: Choose between chromium, firefox, or webkit
- **Viewport size**: Default is 1920x1080
- **Timeouts**: Adjust wait times for different elements
- **Validation thresholds**: Font size, color, and container size tolerances
- **Expected elements**: Navigation items and page titles

## Project Structure

```
├── solidigm_automation.py    # Main automation script
├── test_solidigm.py         # Pytest test suite
├── ui_validator.py          # UI validation utilities
├── link_validator.py        # Link validation utilities
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── screenshots/           # Screenshots (created automatically)
```

## Validation Types

### UI Validation
- Font sizes and families
- Colors (text, background, borders)
- Container dimensions
- Text content verification
- Image loading and presence
- CTA button functionality

### Link Validation
- Internal link status checking
- External link validation
- Image source verification
- Navigation link testing
- Duplicate link detection
- Broken link identification

### Responsive Testing
- Mobile viewport (375x667)
- Desktop viewport (1920x1080)
- Navigation accessibility
- Element visibility

### Performance Testing
- Page load times
- DOM content loaded time
- Network performance metrics

## Customization

### Adding New UI Validations

```python
# In solidigm_automation.py
def validate_custom_element(self):
    selector = ".custom-element"
    is_valid, message = self.ui_validator.validate_font_size(selector, "16px")
    print(f"Custom element: {message}")
```

### Adding New Link Validations

```python
# In solidigm_automation.py
def validate_custom_links(self):
    custom_links = self.page.locator('.custom-links a')
    for i in range(custom_links.count()):
        link = custom_links.nth(i)
        href = link.get_attribute('href')
        is_valid, status, message = self.link_validator.validate_link_status(href)
        print(f"Custom link: {message}")
```

## Troubleshooting

### Common Issues

1. **Browser not found**: Run `playwright install`
2. **Timeout errors**: Increase timeout values in `config.py`
3. **Element not found**: Check selectors in validation methods
4. **Permission errors**: Ensure write permissions for screenshots directory

### Debug Mode

Run with debug logging:

```bash
LOG_LEVEL=DEBUG python solidigm_automation.py
```

### Screenshots

Screenshots are automatically saved to the `screenshots/` directory:
- `initial_page_[timestamp].png` - Page after initial load
- `final_page_[timestamp].png` - Page after all validations
- `error_page_[timestamp].png` - Page when errors occur

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your validations
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and testing purposes.
