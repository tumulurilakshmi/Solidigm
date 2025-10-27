"""
Pytest test suite for Solidigm website validation
"""
import pytest
from playwright.sync_api import sync_playwright
from solidigm_automation import SolidigmAutomation
from config import Config

class TestSolidigmWebsite:
    @pytest.fixture(scope="class")
    def automation(self):
        """Setup automation instance"""
        automation = SolidigmAutomation()
        automation.setup_browser()
        automation.navigate_to_site()
        yield automation
        automation.close()
    
    def test_page_loads(self, automation):
        """Test that the page loads successfully"""
        title = automation.page.title()
        assert automation.config.EXPECTED_TITLE.lower() in title.lower()
    
    def test_main_navigation_present(self, automation):
        """Test that main navigation is present"""
        nav_selectors = ['nav', '.main-menu', '.navigation', '[role="navigation"]']
        nav_found = any(automation.page.locator(selector).count() > 0 for selector in nav_selectors)
        assert nav_found, "Main navigation not found"
    
    def test_navigation_links_valid(self, automation):
        """Test that navigation links are valid"""
        nav_results = automation.link_validator.validate_navigation_links(
            automation.config.EXPECTED_MAIN_NAVIGATION
        )
        
        # Check that at least some navigation links are valid
        valid_links = [result for result in nav_results if result['is_valid']]
        assert len(valid_links) > 0, "No valid navigation links found"
    
    def test_header_present(self, automation):
        """Test that header is present"""
        header_selectors = ['header', '.header', '.site-header']
        header_found = any(automation.page.locator(selector).count() > 0 for selector in header_selectors)
        assert header_found, "Header not found"
    
    def test_footer_present(self, automation):
        """Test that footer is present"""
        footer_selectors = ['footer', '.footer', '.site-footer']
        footer_found = any(automation.page.locator(selector).count() > 0 for selector in footer_selectors)
        assert footer_found, "Footer not found"
    
    def test_images_load(self, automation):
        """Test that images load properly"""
        images = automation.page.locator('img')
        assert images.count() > 0, "No images found on page"
        
        # Check first few images
        for i in range(min(3, images.count())):
            img = images.nth(i)
            is_loaded = automation.page.evaluate(f"""
                () => {{
                    const img = document.querySelectorAll('img')[{i}];
                    return img && img.complete && img.naturalHeight !== 0;
                }}
            """)
            assert is_loaded, f"Image {i+1} not loaded properly"
    
    def test_cta_buttons_present(self, automation):
        """Test that CTA buttons are present and functional"""
        cta_selectors = ['button', '.btn', '.button', '[class*="cta"]']
        total_buttons = sum(automation.page.locator(selector).count() for selector in cta_selectors)
        assert total_buttons > 0, "No CTA buttons found"
    
    def test_no_broken_links(self, automation):
        """Test that there are no broken links"""
        broken_links = automation.link_validator.get_broken_links()
        # Allow some broken links but not too many
        assert len(broken_links) < 10, f"Too many broken links found: {len(broken_links)}"
    
    def test_external_links_valid(self, automation):
        """Test that external links are valid"""
        external_links = automation.link_validator.validate_external_links()
        if external_links:
            valid_external = [link for link in external_links if link['is_valid']]
            # At least 50% of external links should be valid
            assert len(valid_external) / len(external_links) >= 0.5, "Too many broken external links"
    
    def test_responsive_design(self, automation):
        """Test responsive design elements"""
        # Test mobile viewport
        automation.page.set_viewport_size({'width': 375, 'height': 667})
        automation.page.wait_for_load_state('networkidle')
        
        # Check if navigation is still accessible
        nav_selectors = ['nav', '.main-menu', '.navigation']
        nav_accessible = any(automation.page.locator(selector).count() > 0 for selector in nav_selectors)
        assert nav_accessible, "Navigation not accessible on mobile viewport"
        
        # Reset to desktop viewport
        automation.page.set_viewport_size(automation.config.VIEWPORT)
    
    def test_page_performance(self, automation):
        """Test basic page performance metrics"""
        # Get performance metrics
        metrics = automation.page.evaluate("""
            () => {
                const navigation = performance.getEntriesByType('navigation')[0];
                return {
                    loadTime: navigation.loadEventEnd - navigation.loadEventStart,
                    domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
                    totalTime: navigation.loadEventEnd - navigation.fetchStart
                };
            }
        """)
        
        # Basic performance checks
        assert metrics['totalTime'] < 10000, f"Page load time too slow: {metrics['totalTime']}ms"
        assert metrics['domContentLoaded'] < 5000, f"DOM content loaded too slow: {metrics['domContentLoaded']}ms"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--html=report.html"])
