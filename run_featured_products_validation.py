"""
Run Featured Products validation on Solidigm home page
"""
from playwright.sync_api import sync_playwright
from featured_products_validator import FeaturedProductsValidator
from featured_products_report_generator import FeaturedProductsReportGenerator


def main():
    url = "https://www.solidigm.com/"

    print("=" * 80)
    print("FEATURED PRODUCTS VALIDATION - SOLIDIGM HOME PAGE")
    print("=" * 80)

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)

    try:
        print(f"\n[INFO] Navigating to {url}...")
        page.goto(url, wait_until='domcontentloaded', timeout=90000)
        page.wait_for_timeout(3000)

        validator = FeaturedProductsValidator(page)
        results = validator.validate_featured_products()

        # Generate Excel report
        if results.get('found') and 'error' not in results:
            report = FeaturedProductsReportGenerator()
            report_file = report.generate_excel_report(results)
            print(f"\n[SUCCESS] Excel report: {report_file}")

        print("\n" + "=" * 80)
        print("VALIDATION FINISHED")
        print("=" * 80)

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
    finally:
        browser.close()


if __name__ == "__main__":
    main()


