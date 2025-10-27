"""
Main script to run validation from notepad/input file
"""
import sys
import os
from playwright.sync_api import sync_playwright
from comprehensive_validator import ComprehensiveValidator
from report_generator import ReportGenerator
from excel_report_generator import ExcelReportGenerator
from config import Config


class ValidationRunner:
    def __init__(self):
        self.config = Config()
        self.browser = None
        self.page = None
        self.results = []
    
    def read_urls_from_file(self, filename: str) -> list:
        """Read URLs and locales from input file"""
        urls_config = []
        
        if not os.path.exists(filename):
            print(f"[ERROR] File not found: {filename}")
            return urls_config
        
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Format: URL | locale
            # Example: https://www.solidigm.com/ | US/EN
            if '|' in line:
                parts = line.split('|')
                url = parts[0].strip()
                locale = parts[1].strip() if len(parts) > 1 else "US/EN"
            else:
                url = line.strip()
                locale = "US/EN"  # Default locale
            
            if url:
                urls_config.append({
                    'url': url,
                    'locale': locale,
                    'line': line_num
                })
        
        return urls_config
    
    def setup_browser(self):
        """Initialize browser"""
        playwright = sync_playwright().start()
        
        if self.config.BROWSER == 'chromium':
            browser = playwright.chromium
        elif self.config.BROWSER == 'firefox':
            browser = playwright.firefox
        elif self.config.BROWSER == 'webkit':
            browser = playwright.webkit
        else:
            browser = playwright.chromium
        
        self.browser = browser.launch(
            headless=self.config.HEADLESS,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        self.page = self.browser.new_page(viewport=self.config.VIEWPORT)
        self.page.set_default_timeout(self.config.TIMEOUT)
    
    def close_browser(self):
        """Close browser"""
        if self.browser:
            self.browser.close()
    
    def validate_url(self, url: str, locale: str = "US/EN") -> dict:
        """Validate a single URL"""
        print(f"\n{'='*100}")
        print(f"[VALIDATING] {url}")
        print(f"[LOCALE] {locale}")
        print(f"{'='*100}")
        
        try:
            # Navigate to the page
            print(f"\n[NAVIGATING] {url}...")
            self.page.goto(url, timeout=self.config.NAVIGATION_TIMEOUT, wait_until='domcontentloaded')
            # Wait a bit for page to fully load
            self.page.wait_for_timeout(3000)
            
            title = self.page.title()
            print(f"[OK] Page loaded: {title}")
            
            # Run comprehensive validation
            validator = ComprehensiveValidator(self.page, url, locale)
            results = validator.run_complete_validation()
            
            # Convert base_url to actual URL
            results['validation_info']['url'] = url
            
            print(f"\n[OK] Validation completed for {url}")
            
            return results
            
        except Exception as e:
            print(f"\n[ERROR] Error validating {url}: {str(e)}")
            return {
                'validation_info': {
                    'url': url,
                    'locale': locale,
                    'timestamp': '',
                },
                'error': str(e)
            }
    
    def run_from_file(self, input_file: str):
        """Run validation from input file"""
        print("\n" + "="*100)
        print(" " * 30 + "SOLIDIGM VALIDATION AUTOMATION")
        print("="*100)
        
        # Read URLs from file
        print(f"\n[INFO] Reading URLs from: {input_file}")
        urls_config = self.read_urls_from_file(input_file)
        
        if not urls_config:
            print("[ERROR] No valid URLs found in file")
            return
        
        print(f"[OK] Found {len(urls_config)} URL(s) to validate")
        
        # Setup browser
        print("\n[INFO] Initializing browser...")
        self.setup_browser()
        
        # Generate reports directory
        report_gen = ReportGenerator()
        
        # Validate each URL
        for idx, url_config in enumerate(urls_config, 1):
            print(f"\n[{idx}/{len(urls_config)}] Processing URL...")
            
            result = self.validate_url(url_config['url'], url_config['locale'])
            self.results.append(result)
            
            # Generate individual reports
            report_gen.generate_report(result)
            report_gen.generate_html_report(result)
            
            # Generate Excel report
            excel_gen = ExcelReportGenerator()
            excel_gen.generate_excel_report(result)
        
        # Generate summary report
        self._generate_summary_report(report_gen)
        
        # Cleanup
        self.close_browser()
        
        # Print final summary
        print("\n" + "="*100)
        print("[SUCCESS] VALIDATION COMPLETE")
        print("="*100)
        self._print_summary()
    
    def _generate_summary_report(self, report_gen: ReportGenerator):
        """Generate summary report for all URLs"""
        import json
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"reports/summary_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("="*100 + "\n")
            f.write(" " * 30 + "VALIDATION SUMMARY REPORT\n")
            f.write("="*100 + "\n\n")
            
            for idx, result in enumerate(self.results, 1):
                if 'error' in result:
                    f.write(f"\n[{idx}] {result['validation_info']['url']}\n")
                    f.write(f"    [ERROR] Error: {result['error']}\n\n")
                else:
                    summary = result['overall_summary']
                    f.write(f"\n[{idx}] {result['validation_info']['url']}\n")
                    f.write(f"    Locale: {result['validation_info']['locale']}\n")
                    f.write(f"    UI Validations: {summary['total_ui_validations']} total, "
                            f"{summary['passed_ui_validations']} passed, "
                            f"{summary['failed_ui_validations']} failed\n")
                    f.write(f"    Links: {summary['total_links']} total, "
                            f"{summary['valid_links']} valid, "
                            f"{summary['broken_links']} broken\n\n")
        
        print(f"\n[REPORT] Summary report generated: {filename}")
    
    def _print_summary(self):
        """Print summary to console"""
        print("\nSUMMARY:")
        print("-"*100)
        
        for idx, result in enumerate(self.results, 1):
            if 'error' in result:
                print(f"[{idx}] [ERROR] {result['validation_info']['url']} - Error: {result['error']}")
            else:
                summary = result['overall_summary']
                status = "[OK]" if summary['failed_ui_validations'] == 0 and summary['broken_links'] == 0 else "[FAIL]"
                print(f"[{idx}] {status} {result['validation_info']['url']}")
                print(f"     UI: {summary['passed_ui_validations']}/{summary['total_ui_validations']} passed, "
                      f"{summary['failed_ui_validations']} failed")
                print(f"     Links: {summary['valid_links']} valid, {summary['broken_links']} broken")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python run_validation.py <input_file.txt>")
        print("\nExample input_file.txt:")
        print("  https://www.solidigm.com/ | US/EN")
        print("  https://www.solidigm.com/products | US/EN")
        print("  https://www.solidigm.com/support | US/EN")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    runner = ValidationRunner()
    runner.run_from_file(input_file)


if __name__ == "__main__":
    main()

