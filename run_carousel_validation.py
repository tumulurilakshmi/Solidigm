"""
Run carousel validation for Solidigm home page
"""
from playwright.sync_api import sync_playwright
from carousel_validator import CarouselValidator
from carousel_report_generator import CarouselReportGenerator


def main():
    url = "https://www.solidigm.com/"
    
    print("=" * 80)
    print("CAROUSEL VALIDATION - SOLIDIGM HOME PAGE")
    print("=" * 80)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(90000)
    
    try:
        # Navigate to page
        print(f"\n[INFO] Navigating to {url}...")
        page.goto(url, timeout=60000, wait_until='domcontentloaded')
        page.wait_for_timeout(3000)
        
        title = page.title()
        print(f"[OK] Page loaded: {title}")
        
        # Validate carousel
        validator = CarouselValidator(page)
        results = validator.validate_carousel()
        
        # Generate Excel report
        if 'error' not in results:
            report_gen = CarouselReportGenerator()
            excel_file = report_gen.generate_excel_report(results)
            print(f"\n[SUCCESS] Excel report saved: {excel_file}")
            
            print("\n" + "="*80)
            print("VALIDATION COMPLETE")
            print("="*80)
            
            print("\n[REPORT] Validation results:")
            print(f"  Total Carousels: {results.get('carousel_count', 0)}")
            
            for i, carousel in enumerate(results.get('carousels', []), 1):
                print(f"\n  Carousel {i}:")
                print(f"    Slides: {carousel.get('slide_count', 0)}")
                print(f"    Container Size: {carousel.get('container', {}).get('width', 0)}x{carousel.get('container', {}).get('height', 0)}")
                
                nav = carousel.get('navigation', {})
                print(f"    Navigation: Left={nav.get('left_chevron_visible')}, Right={nav.get('right_chevron_visible')}")
                
                pb = carousel.get('progress_bar', {})
                print(f"    Progress Bar: {'Yes' if pb.get('exists') else 'No'} ({pb.get('indicator_count', 0)} indicators)")
                
                font_styles = carousel.get('font_styles', [])
                if font_styles:
                    for fs in font_styles:
                        print(f"    {fs.get('element').upper()}: {fs.get('font_size')}, {fs.get('font_color')}")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()

