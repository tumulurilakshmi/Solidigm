#!/usr/bin/env python3
"""
Script to validate only the Footer component on the homepage
"""

from playwright.sync_api import sync_playwright
from homepage_validator import HomePageValidator
from home_page_report_generator import HomePageReportGenerator
from datetime import datetime

def main():
    """Run footer validation only"""
    url = "https://www.solidigm.com"
    
    print(f"\n{'='*60}")
    print(f"FOOTER VALIDATION")
    print(f"{'='*60}")
    print(f"URL: {url}\n")
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    try:
        print(f"[INFO] Navigating to {url}...")
        page.goto(url, wait_until='load', timeout=60000)
        page.wait_for_timeout(3000)
        
        # Initialize validator
        validator = HomePageValidator(page, url)
        
        # Validate only footer
        print(f"\n[INFO] Starting Footer validation...")
        footer_results = validator._validate_footer()
        
        # Create results dictionary with only footer data
        results = {
            'url': url,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'footer': footer_results
        }
        
        # Generate Excel report
        print(f"\n[INFO] Generating Excel report...")
        report_gen = HomePageReportGenerator()
        
        try:
            filename = report_gen.generate_excel_report(results)
            print(f"\n[SUCCESS] Footer validation complete!")
            print(f"Report saved: {filename}")
        except Exception as e:
            print(f"\n[ERROR] Report generation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
    except Exception as e:
        print(f"\n[ERROR] Footer validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()

if __name__ == "__main__":
    main()

