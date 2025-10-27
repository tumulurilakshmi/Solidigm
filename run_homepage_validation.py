"""
Run complete home page validation
"""
import sys
from playwright.sync_api import sync_playwright
from homepage_validator import HomePageValidator
from home_page_report_generator import HomePageReportGenerator


def main():
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = "https://www.solidigm.com/"
    
    print("=" * 100)
    print(" " * 25 + "SOLIDIGM HOMEPAGE COMPREHENSIVE VALIDATION")
    print("=" * 100)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    try:
        # Run validation
        validator = HomePageValidator(page, url)
        results = validator.validate_complete_homepage()
        
        # Generate Excel report
        if 'error' not in results:
            report_gen = HomePageReportGenerator()
            excel_file = report_gen.generate_excel_report(results)
            print(f"\n[SUCCESS] Excel report saved: {excel_file}")
        
        print("\n" + "="*100)
        print("VALIDATION COMPLETE")
        print("="*100)
        
        if 'error' not in results:
            summary = results.get('summary', {})
            print("\n[SUMMARY]")
            print(f"  Carousels: {summary.get('carousel_count', 0)}")
            print(f"  Featured Products: {summary.get('featured_products_count', 0)}")
            print(f"  Product Cards: {summary.get('product_cards_count', 0)}")
            print(f"  Articles: {summary.get('article_count', 0)}")
            print(f"  Blade Components: {summary.get('blade_count', 0)}")
            print(f"  Footer: {'Yes' if summary.get('footer_exists') else 'No'}")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()


