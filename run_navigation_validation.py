"""
Run navigation validation for Solidigm website
"""
import sys
from playwright.sync_api import sync_playwright
from navigation_validator import NavigationValidator


def main():
    url = "https://www.solidigm.com/"
    
    print("=" * 80)
    print("NAVIGATION MENU VALIDATION - SOLIDIGM WEBSITE")
    print("=" * 80)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(90000)
    
    try:
        # Run navigation validation
        validator = NavigationValidator(page, url)
        results = validator.validate_navigation_menu()
        
        # Generate Excel report
        if 'error' not in results:
            excel_file = validator.generate_excel_report(results)
            print(f"\n[SUCCESS] Excel report saved: {excel_file}")
        
        print("\n" + "=" * 80)
        print("VALIDATION COMPLETE")
        print("=" * 80)
        
        if 'error' not in results:
            print("\nExcel report contains:")
            print("  - Summary sheet")
            print("  - Main Menu sheet")
            print("  - Font Styles sheet (NEW!)")
            print("  - Sub-Menu Details sheet")
            print("  - Broken Links sheet")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()

