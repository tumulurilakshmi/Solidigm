"""
Run Series Navigation Test
Tests navigation through Product menu to D3, D5, D7 series pages
"""
from playwright.sync_api import sync_playwright
from series_navigation_validator import SeriesNavigationValidator


def main():
    base_url = "https://www.solidigm.com/"
    
    print("=" * 100)
    print(" " * 30 + "SERIES NAVIGATION TEST")
    print("=" * 100)
    print("\nTesting navigation: Product > D3/D5/D7 Series")
    print("=" * 100)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    try:
        validator = SeriesNavigationValidator(page)
        results = validator.validate_series_navigation(base_url)
        
        print("\n" + "="*100)
        print("NAVIGATION TEST COMPLETE")
        print("="*100)
        
        # Print final summary
        summary = results.get('summary', {})
        print(f"\n[FINAL RESULTS]")
        print(f"  D3 Series: {'✓ PASS' if summary.get('d3_success') else '✗ FAIL'}")
        print(f"  D5 Series: {'✓ PASS' if summary.get('d5_success') else '✗ FAIL'}")
        print(f"  D7 Series: {'✓ PASS' if summary.get('d7_success') else '✗ FAIL'}")
        print(f"  Overall: {'✓ ALL PASS' if summary.get('all_success') else '✗ SOME FAILED'}")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()


if __name__ == "__main__":
    main()

