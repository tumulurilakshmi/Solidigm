"""
Run Product Detail Page (PDP) validation
Validates individual product pages like D3-S4620, D7-P5520, etc.
"""
import sys
from playwright.sync_api import sync_playwright
from pdp_validator import PDPValidator
from pdp_report_generator import PDPReportGenerator


def main():
    # Default to D3-S4620 if no URL provided
    if len(sys.argv) > 1:
        product_url = sys.argv[1]
    else:
        product_url = "https://www.solidigm.com/products/data-center/d3/s4620.html"
    
    print("=" * 100)
    print(" " * 30 + "PRODUCT DETAIL PAGE (PDP) VALIDATION")
    print("=" * 100)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    try:
        # Run validation
        validator = PDPValidator(page)
        results = validator.validate_pdp_page(product_url)
        
        # Generate Excel report
        if 'error' not in results:
            try:
                report_gen = PDPReportGenerator()
                excel_file = report_gen.generate_excel_report(results)
                print(f"\n[SUCCESS] Excel report saved: {excel_file}")
            except Exception as report_error:
                print(f"\n[ERROR] Failed to generate Excel report: {str(report_error)}")
                import traceback
                traceback.print_exc()
        
        print("\n" + "="*100)
        print("VALIDATION COMPLETE")
        print("="*100)
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()


if __name__ == "__main__":
    main()

