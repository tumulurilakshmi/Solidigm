"""
Series Navigation Validator
Validates navigation through Product menu to D3, D5, D7 series pages
"""
from typing import Dict, List
from playwright.sync_api import Page


class SeriesNavigationValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_series_navigation(self, base_url: str = "https://www.solidigm.com/") -> Dict:
        """Validate navigation through Product menu to series pages"""
        print("\n" + "="*80)
        print("SERIES NAVIGATION VALIDATION")
        print("="*80)
        
        try:
            # Navigate to homepage
            print(f"\n[INFO] Navigating to {base_url}")
            self.page.goto(base_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(3000)
            
            results = {
                'd3_navigation': {},
                'd5_navigation': {},
                'd7_navigation': {},
                'summary': {}
            }
            
            # Test D3 Series navigation
            print("\n[D3 SERIES] Testing Product > D3 Series navigation...")
            results['d3_navigation'] = self._test_series_navigation('D3', 'D3 Series', '/products/data-center/d3.html')
            
            # Navigate back to homepage
            self.page.goto(base_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(2000)
            
            # Test D5 Series navigation
            print("\n[D5 SERIES] Testing Product > D5 Series navigation...")
            results['d5_navigation'] = self._test_series_navigation('D5', 'D5 Series', '/products/data-center/d5.html')
            
            # Navigate back to homepage
            self.page.goto(base_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(2000)
            
            # Test D7 Series navigation
            print("\n[D7 SERIES] Testing Product > D7 Series navigation...")
            results['d7_navigation'] = self._test_series_navigation('D7', 'D7 Series', '/products/data-center/d7.html')
            
            # Generate summary
            results['summary'] = {
                'd3_success': results['d3_navigation'].get('navigation_success', False),
                'd5_success': results['d5_navigation'].get('navigation_success', False),
                'd7_success': results['d7_navigation'].get('navigation_success', False),
                'all_success': (
                    results['d3_navigation'].get('navigation_success', False) and
                    results['d5_navigation'].get('navigation_success', False) and
                    results['d7_navigation'].get('navigation_success', False)
                )
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Series navigation validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _test_series_navigation(self, series: str, series_name: str, expected_path: str) -> Dict:
        """Test navigation to a specific series page"""
        nav_result = {
            'series': series,
            'menu_found': False,
            'submenu_found': False,
            'navigation_success': False,
            'url_matches': False,
            'final_url': '',
            'expected_url': '',
            'steps': []
        }
        
        try:
            # Step 1: Find and hover/click on Product menu
            print(f"   [STEP 1] Finding Product menu...")
            product_menu = self.page.locator('li.cmp-navigation__menu-items:has-text("Product"), nav:has-text("Product")').first
            
            if product_menu.count() == 0:
                # Try alternative selector
                product_menu = self.page.locator('a:has-text("Product"), button:has-text("Product")').first
            
            if product_menu.count() > 0:
                nav_result['menu_found'] = True
                nav_result['steps'].append('Product menu found')
                print(f"      [OK] Product menu found")
                
                # Hover or click to open submenu
                try:
                    product_menu.hover()
                    self.page.wait_for_timeout(500)
                    nav_result['steps'].append('Hovered over Product menu')
                except:
                    try:
                        product_menu.click()
                        self.page.wait_for_timeout(500)
                        nav_result['steps'].append('Clicked Product menu')
                    except:
                        pass
                
                # Step 2: Find Series submenu item
                print(f"   [STEP 2] Finding {series_name} submenu...")
                
                # Try multiple selectors for the series link
                series_selectors = [
                    f'a:has-text("{series_name}")',
                    f'a:has-text("D{series[-1]} Series")',
                    f'a[href*="/d{series[-1]}.html"]',
                    f'a[href*="/data-center/d{series[-1]}"]',
                    f'.cmp-navigation__mega-menu a:has-text("{series_name}")',
                    f'.cmp-navigation__mega-menu a:has-text("D{series[-1]}")'
                ]
                
                series_link = None
                for selector in series_selectors:
                    series_link = self.page.locator(selector).first
                    if series_link.count() > 0 and series_link.is_visible():
                        break
                
                if series_link and series_link.count() > 0:
                    nav_result['submenu_found'] = True
                    nav_result['steps'].append(f'{series_name} submenu found')
                    print(f"      [OK] {series_name} submenu found")
                    
                    # Get the href
                    href = series_link.get_attribute('href') or ''
                    nav_result['expected_url'] = href
                    
                    # Step 3: Click the series link
                    print(f"   [STEP 3] Clicking {series_name} link...")
                    current_url = self.page.url
                    
                    try:
                        series_link.click()
                        self.page.wait_for_timeout(3000)  # Wait for navigation
                        nav_result['steps'].append(f'Clicked {series_name} link')
                        
                        # Step 4: Verify navigation
                        print(f"   [STEP 4] Verifying navigation...")
                        new_url = self.page.url
                        nav_result['final_url'] = new_url
                        
                        # Check if URL changed
                        if new_url != current_url:
                            nav_result['navigation_success'] = True
                            nav_result['steps'].append('Navigation successful - URL changed')
                            
                            # Verify URL matches expected path
                            if expected_path in new_url or f'/d{series[-1]}.html' in new_url:
                                nav_result['url_matches'] = True
                                nav_result['steps'].append('URL matches expected path')
                                print(f"      [OK] Navigation successful!")
                                print(f"         Current URL: {new_url}")
                                print(f"         Expected path: {expected_path}")
                            else:
                                print(f"      [WARNING] URL doesn't match expected path")
                                print(f"         Current URL: {new_url}")
                                print(f"         Expected: {expected_path}")
                        else:
                            nav_result['steps'].append('Navigation failed - URL did not change')
                            print(f"      [WARNING] URL did not change after click")
                    except Exception as e:
                        nav_result['steps'].append(f'Click failed: {str(e)}')
                        print(f"      [ERROR] Click failed: {str(e)}")
                else:
                    nav_result['steps'].append(f'{series_name} submenu not found')
                    print(f"      [WARNING] {series_name} submenu not found or not visible")
            else:
                nav_result['steps'].append('Product menu not found')
                print(f"      [WARNING] Product menu not found")
        
        except Exception as e:
            nav_result['steps'].append(f'Error: {str(e)}')
            print(f"      [ERROR] Navigation test failed: {str(e)}")
        
        return nav_result
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("SERIES NAVIGATION SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"D3 Series Navigation: {'✓ Success' if summary.get('d3_success') else '✗ Failed'}")
        print(f"D5 Series Navigation: {'✓ Success' if summary.get('d5_success') else '✗ Failed'}")
        print(f"D7 Series Navigation: {'✓ Success' if summary.get('d7_success') else '✗ Failed'}")
        print(f"All Navigations: {'✓ Success' if summary.get('all_success') else '✗ Failed'}")
        
        # Print details for each
        for series in ['d3', 'd5', 'd7']:
            nav_data = results.get(f'{series}_navigation', {})
            if nav_data:
                print(f"\n{series.upper()} Details:")
                print(f"  Menu Found: {nav_data.get('menu_found', False)}")
                print(f"  Submenu Found: {nav_data.get('submenu_found', False)}")
                print(f"  Navigation Success: {nav_data.get('navigation_success', False)}")
                print(f"  URL Matches: {nav_data.get('url_matches', False)}")
                if nav_data.get('final_url'):
                    print(f"  Final URL: {nav_data['final_url']}")

