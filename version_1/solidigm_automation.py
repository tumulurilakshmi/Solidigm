"""
Main automation script for Solidigm website validation
"""
import os
import time
from playwright.sync_api import sync_playwright, Browser, Page
from config import Config
from ui_validator import UIValidator
from link_validator import LinkValidator

class SolidigmAutomation:
    def __init__(self):
        self.config = Config()
        self.browser = None
        self.page = None
        self.ui_validator = None
        self.link_validator = None
        
    def setup_browser(self):
        """Initialize browser and page"""
        playwright = sync_playwright().start()
        
        # Choose browser
        if self.config.BROWSER == 'chromium':
            browser = playwright.chromium
        elif self.config.BROWSER == 'firefox':
            browser = playwright.firefox
        elif self.config.BROWSER == 'webkit':
            browser = playwright.webkit
        else:
            browser = playwright.chromium
        
        # Launch browser
        self.browser = browser.launch(
            headless=self.config.HEADLESS,
            args=['--no-sandbox', '--disable-dev-shm-usage']
        )
        
        # Create page
        self.page = self.browser.new_page(viewport=self.config.VIEWPORT)
        self.page.set_default_timeout(self.config.TIMEOUT)
        
        # Initialize validators
        self.ui_validator = UIValidator(self.page)
        self.link_validator = LinkValidator(self.page, self.config.BASE_URL)
        
        print(f"Browser initialized: {self.config.BROWSER}")
    
    def navigate_to_site(self):
        """Navigate to Solidigm website"""
        print(f"Navigating to: {self.config.BASE_URL}")
        self.page.goto(self.config.BASE_URL, timeout=self.config.NAVIGATION_TIMEOUT)
        self.page.wait_for_load_state('networkidle')
        
        # Verify page loaded
        title = self.page.title()
        print(f"Page title: {title}")
        
        if self.config.EXPECTED_TITLE.lower() in title.lower():
            print("✓ Page title validation passed")
        else:
            print(f"⚠ Page title validation failed: Expected '{self.config.EXPECTED_TITLE}' in '{title}'")
    
    def validate_main_navigation(self):
        """Validate main navigation elements"""
        print("\n=== Validating Main Navigation ===")
        
        # Check if main navigation exists
        nav_selectors = [
            'nav',
            '.main-menu',
            '.navigation',
            '[role="navigation"]'
        ]
        
        nav_found = False
        for selector in nav_selectors:
            if self.page.locator(selector).count() > 0:
                nav_found = True
                print(f"✓ Navigation found: {selector}")
                break
        
        if not nav_found:
            print("⚠ No main navigation found")
            return
        
        # Validate navigation links
        nav_results = self.link_validator.validate_navigation_links(self.config.EXPECTED_MAIN_NAVIGATION)
        
        for result in nav_results:
            status = "✓" if result['is_valid'] else "✗"
            expected = "✓" if result['is_expected'] else "⚠"
            print(f"{status} {result['text']} - {result['message']} {expected}")
    
    def validate_ui_elements(self):
        """Validate UI elements like fonts, colors, containers"""
        print("\n=== Validating UI Elements ===")
        
        # Validate header/footer
        self._validate_header()
        self._validate_footer()
        
        # Validate main content areas
        self._validate_main_content()
        
        # Validate CTAs
        self._validate_cta_buttons()
        
        # Validate images
        self._validate_images()
    
    def _validate_header(self):
        """Validate header elements"""
        print("\n--- Header Validation ---")
        
        header_selectors = ['header', '.header', '.site-header']
        for selector in header_selectors:
            if self.page.locator(selector).count() > 0:
                print(f"✓ Header found: {selector}")
                
                # Validate logo
                logo_selectors = [f'{selector} img', f'{selector} .logo', f'{selector} [class*="logo"]']
                for logo_sel in logo_selectors:
                    if self.page.locator(logo_sel).count() > 0:
                        is_valid, message = self.ui_validator.validate_image_presence(logo_sel)
                        status = "✓" if is_valid else "✗"
                        print(f"{status} Logo: {message}")
                        break
                break
    
    def _validate_footer(self):
        """Validate footer elements"""
        print("\n--- Footer Validation ---")
        
        footer_selectors = ['footer', '.footer', '.site-footer']
        for selector in footer_selectors:
            if self.page.locator(selector).count() > 0:
                print(f"✓ Footer found: {selector}")
                
                # Check footer links
                footer_links = self.page.locator(f'{selector} a')
                link_count = footer_links.count()
                print(f"✓ Footer links count: {link_count}")
                break
    
    def _validate_main_content(self):
        """Validate main content area"""
        print("\n--- Main Content Validation ---")
        
        # Check for main content area
        main_selectors = ['main', '.main-content', '.content', '#main']
        for selector in main_selectors:
            if self.page.locator(selector).count() > 0:
                print(f"✓ Main content found: {selector}")
                
                # Validate hero section
                hero_selectors = [f'{selector} .hero', f'{selector} .banner', f'{selector} h1']
                for hero_sel in hero_selectors:
                    if self.page.locator(hero_sel).count() > 0:
                        print(f"✓ Hero section found: {hero_sel}")
                        break
                break
    
    def _validate_cta_buttons(self):
        """Validate CTA buttons"""
        print("\n--- CTA Button Validation ---")
        
        cta_selectors = [
            'button',
            '.btn',
            '.button',
            '[class*="cta"]',
            'a[class*="button"]'
        ]
        
        for selector in cta_selectors:
            buttons = self.page.locator(selector)
            count = buttons.count()
            if count > 0:
                print(f"✓ Found {count} buttons with selector: {selector}")
                
                # Validate first few buttons
                for i in range(min(3, count)):
                    button = buttons.nth(i)
                    text = button.text_content()
                    is_visible = button.is_visible()
                    is_enabled = button.is_enabled()
                    
                    status = "✓" if (is_visible and is_enabled) else "✗"
                    print(f"{status} Button {i+1}: '{text}' (visible: {is_visible}, enabled: {is_enabled})")
    
    def _validate_images(self):
        """Validate images"""
        print("\n--- Image Validation ---")
        
        images = self.page.locator('img')
        count = images.count()
        print(f"✓ Found {count} images")
        
        # Validate first few images
        for i in range(min(5, count)):
            img = images.nth(i)
            src = img.get_attribute('src')
            alt = img.get_attribute('alt')
            is_visible = img.is_visible()
            
            is_valid, message = self.ui_validator.validate_image_presence(f'img:nth-of-type({i+1})')
            status = "✓" if is_valid else "✗"
            print(f"{status} Image {i+1}: {message}")
            if src:
                print(f"    Source: {src[:50]}...")
            if alt:
                print(f"    Alt text: {alt}")
    
    def validate_links(self):
        """Validate all links on the page"""
        print("\n=== Validating Links ===")
        
        # Get all links
        all_links = self.link_validator.validate_all_links()
        print(f"✓ Found {len(all_links)} total links")
        
        # Categorize results
        valid_links = [link for link in all_links if link['is_valid']]
        broken_links = [link for link in all_links if not link['is_valid']]
        
        print(f"✓ Valid links: {len(valid_links)}")
        print(f"✗ Broken links: {len(broken_links)}")
        
        # Show broken links
        if broken_links:
            print("\n--- Broken Links ---")
            for link in broken_links[:10]:  # Show first 10
                print(f"✗ {link['text']} - {link['message']}")
        
        # Check for duplicates
        duplicates = self.link_validator.get_duplicate_links()
        if duplicates:
            print(f"\n⚠ Found {len(duplicates)} duplicate links")
            for dup in duplicates[:5]:  # Show first 5
                print(f"⚠ {dup['url']} appears {dup['count']} times")
        
        # Validate external links
        external_links = self.link_validator.validate_external_links()
        print(f"\n✓ External links: {len(external_links)}")
        
        # Validate image links
        image_links = self.link_validator.validate_image_links()
        valid_images = [img for img in image_links if img['is_valid']]
        broken_images = [img for img in image_links if not img['is_valid']]
        print(f"✓ Valid image links: {len(valid_images)}")
        print(f"✗ Broken image links: {len(broken_images)}")
    
    def take_screenshot(self, name: str = "screenshot"):
        """Take a screenshot"""
        if not os.path.exists(self.config.SCREENSHOT_DIR):
            os.makedirs(self.config.SCREENSHOT_DIR)
        
        timestamp = int(time.time())
        filename = f"{self.config.SCREENSHOT_DIR}/{name}_{timestamp}.png"
        self.page.screenshot(path=filename, full_page=True)
        print(f"✓ Screenshot saved: {filename}")
    
    def run_full_validation(self):
        """Run complete validation suite"""
        print("🚀 Starting Solidigm Website Validation")
        print("=" * 50)
        
        try:
            # Setup
            self.setup_browser()
            
            # Navigate
            self.navigate_to_site()
            
            # Take initial screenshot
            self.take_screenshot("initial_page")
            
            # Run validations
            self.validate_main_navigation()
            self.validate_ui_elements()
            self.validate_links()
            
            # Take final screenshot
            self.take_screenshot("final_page")
            
            print("\n" + "=" * 50)
            print("✅ Validation completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Error during validation: {str(e)}")
            if self.config.SCREENSHOT_ON_FAILURE:
                self.take_screenshot("error_page")
        
        finally:
            if self.browser:
                self.browser.close()
    
    def close(self):
        """Close browser"""
        if self.browser:
            self.browser.close()

if __name__ == "__main__":
    automation = SolidigmAutomation()
    automation.run_full_validation()
