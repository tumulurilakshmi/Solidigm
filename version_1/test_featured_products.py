"""
Test Featured Products Validator
"""
from playwright.sync_api import sync_playwright
from featured_products_validator import FeaturedProductsValidator


def main():
    url = "https://www.solidigm.com/"
    
    print("=" * 80)
    print(" " * 20 + "FEATURED PRODUCTS VALIDATION TEST")
    print("=" * 80)
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(90000)
    
    try:
        print(f"\n[INFO] Navigating to {url}...")
        page.goto(url, timeout=90000, wait_until='domcontentloaded')
        page.wait_for_timeout(3000)
        
        title = page.title()
        print(f"[OK] Page loaded: {title}")
        
        # Run featured products validation
        validator = FeaturedProductsValidator(page)
        results = validator.validate_featured_products()
        
        print("\n" + "="*80)
        print("VALIDATION COMPLETE")
        print("="*80)
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()

