"""
Run Product Series validation for all series (D3, D5, D7)
"""
import sys
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from product_series_validator import ProductSeriesValidator
from product_series_report_generator import ProductSeriesReportGenerator


def main():
    # Load series data
    series_data_path = 'product_series.json'
    try:
        with open(series_data_path, 'r', encoding='utf-8') as f:
            series_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Could not load series data: {str(e)}")
        return
    
    # Get series to validate
    if len(sys.argv) > 1:
        # Validate specific series
        series_arg = sys.argv[1].upper()
        series_to_validate = [s for s in series_data['product_series'] if s['series'] == series_arg]
        if not series_to_validate:
            print(f"[ERROR] Series '{series_arg}' not found. Available: D3, D5, D7")
            return
    else:
        # Validate all series
        series_to_validate = series_data['product_series']
    
    print("=" * 100)
    print(" " * 30 + "PRODUCT SERIES VALIDATION")
    print("=" * 100)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    all_results = []
    
    try:
        for series_info in series_to_validate:
            series = series_info['series']
            url = series_info['url']
            
            print(f"\n{'='*100}")
            print(f"VALIDATING {series} SERIES")
            print(f"{'='*100}")
            
            validator = ProductSeriesValidator(page, series_data_path)
            results = validator.validate_series_page(url, series)
            results['series_info'] = series_info
            all_results.append(results)
            
            # Small delay between series
            page.wait_for_timeout(2000)
        
        # Generate Excel report
        if all_results:
            report_gen = ProductSeriesReportGenerator()
            excel_file = report_gen.generate_excel_report(all_results)
            print(f"\n[SUCCESS] Excel report saved: {excel_file}")
        
        print("\n" + "="*100)
        print("VALIDATION COMPLETE")
        print("="*100)
        
        # Print overall summary
        print("\n[OVERALL SUMMARY]")
        for result in all_results:
            summary = result.get('summary', {})
            series = result.get('series', 'Unknown')
            print(f"  {series} Series:")
            print(f"    Products Found: {summary.get('found_products', 0)}/{summary.get('expected_products', 0)}")
            print(f"    All Products Found: {'Yes' if summary.get('all_products_found') else 'No'}")
            print(f"    Filters Working: {'Yes' if summary.get('filters_working') else 'No'}")
            print(f"    Links Valid: {'Yes' if summary.get('links_valid') else 'No'}")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()


if __name__ == "__main__":
    main()

