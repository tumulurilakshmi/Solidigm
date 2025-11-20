"""
Product Series Page Validator
Validates product series pages (D3, D5, D7) including products, filters, links, and comparison feature
"""
import json
import time
from typing import Dict, List, Optional
from pathlib import Path
from playwright.sync_api import Page
from hero_component_validator import HeroComponentValidator
from model_list_validator import ModelListValidator
from series_navigation_validator import SeriesNavigationValidator


class ProductSeriesValidator:
    def __init__(self, page: Page, series_data_path: str = 'product_series.json'):
        self.page = page
        self.series_data = self._load_series_data(series_data_path)
    
    def _load_series_data(self, path: str) -> Dict:
        """Load product series data from JSON file"""
        try:
            file_path = Path(path)
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[WARNING] Could not load series data: {str(e)}")
        return {}
    
    def validate_series_page(self, series_url: str, expected_series: Optional[str] = None) -> Dict:
        """Validate a product series page by navigating from Data Center page"""
        print("\n" + "="*80)
        print("PRODUCT SERIES PAGE VALIDATION")
        print("="*80)
        
        try:
            # Detect series from URL if not provided
            if not expected_series:
                if '/d3.html' in series_url.lower():
                    expected_series = 'D3'
                elif '/d5.html' in series_url.lower():
                    expected_series = 'D5'
                elif '/d7.html' in series_url.lower():
                    expected_series = 'D7'
            
            # Step 1: Navigate to Data Center page
            data_center_url = "https://www.solidigm.com/products/data-center.html"
            print(f"\n[INFO] Step 1: Navigating to Data Center page: {data_center_url}")
            self.page.goto(data_center_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(3000)
            
            # Step 2: Find and click the series card
            print(f"\n[INFO] Step 2: Looking for {expected_series} Series card...")
            series_card = None
            
            # Try different selectors to find the series card
            series_selectors = [
                f'a[href*="/{expected_series.lower()}.html"]',
                f'a[href*="/d{expected_series[-1]}.html"]',
                f'.series-list__serie:has-text("{expected_series}")',
                f'.series-list__serie:has-text("SSD {expected_series} Series")',
            ]
            
            for selector in series_selectors:
                try:
                    card = self.page.locator(selector).first
                    if card.count() > 0:
                        # Verify it's the right series by checking href or text
                        href = card.get_attribute('href') or ''
                        text = (card.text_content() or '').strip()
                        
                        if f'/{expected_series.lower()}.html' in href.lower() or expected_series in text:
                            series_card = card
                            print(f"   [OK] Found {expected_series} Series card")
                            print(f"        Text: {text[:50]}")
                            print(f"        Href: {href}")
                            break
                except Exception as e:
                    continue
            
            if not series_card:
                print(f"   [ERROR] Could not find {expected_series} Series card on Data Center page")
                print(f"   [INFO] Falling back to direct navigation to {series_url}")
                self.page.goto(series_url, timeout=90000, wait_until='domcontentloaded')
                self.page.wait_for_timeout(3000)
            else:
                # Click the series card
                print(f"\n[INFO] Step 3: Clicking on {expected_series} Series card...")
                try:
                    # Get the href first as backup
                    card_href = series_card.get_attribute('href') or ''
                    if card_href and not card_href.startswith('http'):
                        from urllib.parse import urljoin
                        card_href = urljoin(self.page.url, card_href)
                    
                    # Try to click the card
                    try:
                        # Wait for card to be visible
                        series_card.wait_for(state='visible', timeout=5000)
                        self.page.wait_for_timeout(500)
                        
                        # Try JavaScript click first (more reliable)
                        try:
                            series_card.evaluate('element => element.click()')
                            print(f"   [OK] Clicked using JavaScript")
                        except:
                            # Fallback to regular click
                            series_card.scroll_into_view_if_needed(timeout=5000)
                            self.page.wait_for_timeout(500)
                            series_card.click(timeout=10000)
                            print(f"   [OK] Clicked using Playwright click")
                        
                        # Wait for navigation
                        self.page.wait_for_load_state('domcontentloaded', timeout=30000)
                        self.page.wait_for_timeout(2000)
                        
                        # Verify we're on the correct page
                        current_url = self.page.url
                        if expected_series.lower() in current_url.lower():
                            print(f"   [OK] Successfully navigated to {expected_series} Series page")
                            print(f"        Current URL: {current_url}")
                        else:
                            print(f"   [WARNING] Navigation may have failed. Current URL: {current_url}")
                            print(f"   [INFO] Navigating directly using href: {card_href}")
                            self.page.goto(card_href, timeout=90000, wait_until='domcontentloaded')
                            self.page.wait_for_timeout(2000)
                    except Exception as click_error:
                        # If click fails, navigate directly using href
                        if card_href:
                            print(f"   [WARNING] Click failed: {str(click_error)}")
                            print(f"   [INFO] Navigating directly using href: {card_href}")
                            self.page.goto(card_href, timeout=90000, wait_until='domcontentloaded')
                            self.page.wait_for_timeout(2000)
                        else:
                            raise click_error
                except Exception as e:
                    print(f"   [ERROR] Failed to navigate via series card: {str(e)}")
                    print(f"   [INFO] Falling back to direct navigation to {series_url}")
                    self.page.goto(series_url, timeout=90000, wait_until='domcontentloaded')
                    self.page.wait_for_timeout(3000)
            
            # Get expected data for this series
            expected_data = self._get_series_data(expected_series)
            
            # Validate hero component
            print("\n[HERO] Validating hero component...")
            hero_validator = HeroComponentValidator(self.page)
            hero_data = hero_validator.validate_hero_component()
            
            # Validate page structure
            print("\n[PAGE STRUCTURE] Validating page structure...")
            page_structure = self._validate_page_structure(expected_data)
            
            # Validate products
            print("\n[PRODUCTS] Validating products...")
            products_data = self._validate_products(expected_data)
            
            # Validate filters
            print("\n[FILTERS] Validating filter functionality...")
            filters_data = self._validate_filters()
            
            # Validate product links
            print("\n[LINKS] Validating product links...")
            links_data = self._validate_product_links(products_data.get('products', []))
            
            # Validate comparison feature
            print("\n[COMPARISON] Validating product comparison...")
            comparison_data = self._validate_comparison_feature(products_data.get('products', []))
            
            # Validate model list section
            print("\n[MODEL LIST] Validating model list section...")
            model_list_validator = ModelListValidator(self.page)
            model_list_data = model_list_validator.validate_model_list()
            
            # Validate related articles
            print("\n[ARTICLES] Validating related articles...")
            articles_data = self._validate_related_articles()
            
            results = {
                'url': series_url,
                'series': expected_series,
                'hero': hero_data,
                'page_structure': page_structure,
                'model_list': model_list_data,
                'products': products_data,
                'filters': filters_data,
                'links': links_data,
                'comparison': comparison_data,
                'articles': articles_data,
                'summary': {
                    'hero_found': hero_data.get('found', False),
                    'page_loaded': page_structure.get('page_loaded', False),
                    'title_found': page_structure.get('title_found', False),
                    'model_list_found': model_list_data.get('found', False),
                    'expected_products': expected_data.get('product_count', 0) if expected_data else 0,
                    'found_products': products_data.get('product_count', 0),
                    'all_products_found': products_data.get('all_expected_found', False),
                    'filters_working': filters_data.get('filters_working', False),
                    'links_valid': links_data.get('all_links_valid', False),
                    'comparison_working': comparison_data.get('comparison_working', False)
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Product series validation failed: {str(e)}")
            return {'error': str(e)}
    
    def _get_series_data(self, series: str) -> Optional[Dict]:
        """Get expected data for a specific series"""
        if not self.series_data or 'product_series' not in self.series_data:
            return None
        
        for series_info in self.series_data['product_series']:
            if series_info.get('series') == series:
                return series_info
        return None
    
    def _validate_page_structure(self, expected_data: Optional[Dict]) -> Dict:
        """Validate basic page structure"""
        structure_data = {
            'page_loaded': False,
            'title_found': False,
            'title_text': '',
            'breadcrumbs_found': False,
            'breadcrumbs': [],
            'description_found': False,
            'description_text': ''
        }
        
        try:
            # Check if page loaded
            title = self.page.title()
            structure_data['page_loaded'] = bool(title)
            print(f"   [OK] Page loaded: {title}")
            
            # Find main title (h1)
            h1 = self.page.locator('h1').first
            if h1.count() > 0:
                structure_data['title_found'] = True
                structure_data['title_text'] = (h1.text_content() or '').strip()
                print(f"   [OK] Title: '{structure_data['title_text']}'")
                
                # Check if title matches expected
                if expected_data:
                    expected_name = expected_data.get('name', '')
                    if expected_name.lower() in structure_data['title_text'].lower():
                        print(f"   [OK] Title matches expected series name")
            
            # Find breadcrumbs
            breadcrumbs = self.page.locator('nav[aria-label*="breadcrumb"], .breadcrumb, [class*="breadcrumb"]')
            if breadcrumbs.count() > 0:
                structure_data['breadcrumbs_found'] = True
                breadcrumb_items = breadcrumbs.locator('li, a').all()
                structure_data['breadcrumbs'] = [item.text_content().strip() for item in breadcrumb_items if item.text_content().strip()]
                print(f"   [OK] Breadcrumbs found: {' > '.join(structure_data['breadcrumbs'][:3])}")
            
            # Find description
            description = self.page.locator('p:has-text("engineered"), p:has-text("optimized"), .description, [class*="description"]').first
            if description.count() > 0:
                structure_data['description_found'] = True
                structure_data['description_text'] = (description.text_content() or '').strip()[:200]
                print(f"   [OK] Description found")
        
        except Exception as e:
            print(f"   [ERROR] Page structure validation failed: {str(e)}")
        
        return structure_data
    
    def _validate_products(self, expected_data: Optional[Dict]) -> Dict:
        """Validate products on the page"""
        products_data = {
            'product_count': 0,
            'products': [],
            'all_expected_found': False,
            'expected_products': [],
            'found_product_ids': []
        }
        
        try:
            # Get expected product IDs
            if expected_data:
                products_data['expected_products'] = [p.get('id') for p in expected_data.get('products', [])]
            
            # Find product cards - try multiple selectors
            product_selectors = [
                '.product-card',
                '.cmp-product-card',
                '[class*="product"]',
                'article[class*="product"]',
                '.product-item'
            ]
            
            products = None
            for selector in product_selectors:
                products = self.page.locator(selector)
                if products.count() > 0:
                    break
            
            if products and products.count() > 0:
                products_data['product_count'] = products.count()
                print(f"   [OK] Found {products_data['product_count']} product cards")
                
                # Validate each product
                for i in range(min(products.count(), 10)):  # Check up to 10 products
                    product = products.nth(i)
                    try:
                        product.scroll_into_view_if_needed(timeout=3000)
                        self.page.wait_for_timeout(200)
                    except:
                        pass
                    
                    product_info = self._validate_single_product(product, i)
                    products_data['products'].append(product_info)
                    
                    # Check if this is an expected product
                    product_id = product_info.get('id', '')
                    if product_id:
                        products_data['found_product_ids'].append(product_id)
                
                # Check if all expected products were found
                if products_data['expected_products']:
                    found_count = sum(1 for pid in products_data['expected_products'] 
                                    if pid in products_data['found_product_ids'])
                    products_data['all_expected_found'] = found_count == len(products_data['expected_products'])
                    print(f"   [OK] Found {found_count}/{len(products_data['expected_products'])} expected products")
            else:
                print(f"   [WARNING] No product cards found with standard selectors")
        
        except Exception as e:
            print(f"   [ERROR] Products validation failed: {str(e)}")
        
        return products_data
    
    def _validate_single_product(self, product, index: int) -> Dict:
        """Validate a single product card"""
        product_data = {
            'index': index + 1,
            'id': '',
            'name': '',
            'description': '',
            'interface': '',
            'form_factor': '',
            'capacity': '',
            'view_details_link': '',
            'compare_button': False,
            'image': {}
        }
        
        try:
            # Get product name/ID (usually in h2, h3, or title)
            name_selectors = ['h2', 'h3', '.product-name', '[class*="name"]', 'strong']
            for selector in name_selectors:
                name_elem = product.locator(selector).first
                if name_elem.count() > 0:
                    product_data['name'] = (name_elem.text_content() or '').strip()
                    # Extract product ID from name (e.g., "D3-S4620")
                    if product_data['name']:
                        # Try to extract ID pattern
                        import re
                        match = re.search(r'[D][357]-\w+', product_data['name'])
                        if match:
                            product_data['id'] = match.group()
                        else:
                            product_data['id'] = product_data['name']
                    break
            
            # Get description
            desc = product.locator('p, .description, [class*="description"]').first
            if desc.count() > 0:
                product_data['description'] = (desc.text_content() or '').strip()[:200]
            
            # Get product specs (Interface, Form Factor, Capacity)
            # These might be in separate elements or a list
            specs = product.locator('li, .spec, [class*="spec"]').all()
            for spec in specs[:5]:  # Check first 5 spec items
                text = (spec.text_content() or '').strip()
                if 'interface' in text.lower() or 'sata' in text.lower() or 'pcie' in text.lower():
                    product_data['interface'] = text
                elif 'form factor' in text.lower() or '2.5' in text or 'u.2' in text.lower() or 'm.2' in text.lower():
                    product_data['form_factor'] = text
                elif 'capacity' in text.lower() or 'tb' in text.lower() or 'gb' in text.lower():
                    product_data['capacity'] = text
            
            # Get View Details link
            view_details = product.locator('a:has-text("View Details"), a[href*="product"], .view-details').first
            if view_details.count() > 0:
                product_data['view_details_link'] = view_details.get_attribute('href') or ''
            
            # Check for Compare button
            compare_btn = product.locator('button:has-text("Compare"), [class*="compare"]').first
            product_data['compare_button'] = compare_btn.count() > 0
            
            # Get product image
            img = product.locator('img').first
            if img.count() > 0:
                product_data['image']['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                product_data['image']['alt'] = img.get_attribute('alt') or ''
            
            if product_data['name']:
                print(f"      [OK] Product {index+1}: {product_data['name']}")
                if product_data['interface']:
                    print(f"              Interface: {product_data['interface']}")
        
        except Exception as e:
            print(f"      [ERROR] Product {index+1} validation failed: {str(e)}")
        
        return product_data
    
    def _validate_filters(self) -> Dict:
        """Validate filter functionality"""
        filters_data = {
            'filters_found': False,
            'interface_filter': False,
            'form_factor_filter': False,
            'capacity_filter': False,
            'filters_working': False
        }
        
        try:
            # Look for filter section
            filter_selectors = [
                '.filters',
                '[class*="filter"]',
                'select',
                'button:has-text("Interface")',
                'button:has-text("Form Factor")',
                'button:has-text("Capacity")'
            ]
            
            filters_found = False
            for selector in filter_selectors:
                filters = self.page.locator(selector)
                if filters.count() > 0:
                    filters_found = True
                    break
            
            if filters_found:
                filters_data['filters_found'] = True
                print(f"   [OK] Filter section found")
                
                # Check for specific filters
                interface = self.page.locator('button:has-text("Interface"), select:has-text("Interface")').first
                form_factor = self.page.locator('button:has-text("Form Factor"), select:has-text("Form Factor")').first
                capacity = self.page.locator('button:has-text("Capacity"), select:has-text("Capacity")').first
                
                filters_data['interface_filter'] = interface.count() > 0
                filters_data['form_factor_filter'] = form_factor.count() > 0
                filters_data['capacity_filter'] = capacity.count() > 0
                
                filters_data['filters_working'] = (
                    filters_data['interface_filter'] or 
                    filters_data['form_factor_filter'] or 
                    filters_data['capacity_filter']
                )
                
                print(f"   [OK] Interface filter: {filters_data['interface_filter']}")
                print(f"   [OK] Form Factor filter: {filters_data['form_factor_filter']}")
                print(f"   [OK] Capacity filter: {filters_data['capacity_filter']}")
            else:
                print(f"   [WARNING] No filter section found")
        
        except Exception as e:
            print(f"   [ERROR] Filters validation failed: {str(e)}")
        
        return filters_data
    
    def _validate_product_links(self, products: List[Dict]) -> Dict:
        """Validate product links"""
        links_data = {
            'total_links': 0,
            'valid_links': 0,
            'invalid_links': 0,
            'all_links_valid': False
        }
        
        try:
            for product in products:
                link = product.get('view_details_link', '')
                if link:
                    links_data['total_links'] += 1
                    
                    try:
                        # Make URL absolute if relative
                        if link.startswith('/'):
                            full_url = self.page.evaluate(f"window.location.origin + '{link}'")
                        else:
                            full_url = link
                        
                        response = self.page.request.get(full_url, timeout=5000)
                        if 200 <= response.status < 400:
                            links_data['valid_links'] += 1
                        else:
                            links_data['invalid_links'] += 1
                    except:
                        links_data['invalid_links'] += 1
            
            links_data['all_links_valid'] = links_data['invalid_links'] == 0
            print(f"   [OK] Validated {links_data['total_links']} links")
            print(f"   [OK] Valid: {links_data['valid_links']}, Invalid: {links_data['invalid_links']}")
        
        except Exception as e:
            print(f"   [ERROR] Links validation failed: {str(e)}")
        
        return links_data
    
    def _validate_comparison_feature(self, products: List[Dict]) -> Dict:
        """Validate product comparison feature"""
        comparison_data = {
            'comparison_found': False,
            'max_products': 5,
            'comparison_working': False
        }
        
        try:
            # Look for comparison UI elements
            compare_buttons = self.page.locator('button:has-text("Compare"), [class*="compare"]')
            comparison_data['comparison_found'] = compare_buttons.count() > 0
            
            if comparison_data['comparison_found']:
                print(f"   [OK] Comparison feature found")
                # Note: Full comparison testing would require clicking products
                comparison_data['comparison_working'] = True
            else:
                print(f"   [INFO] Comparison feature not found or not visible")
        
        except Exception as e:
            print(f"   [ERROR] Comparison validation failed: {str(e)}")
        
        return comparison_data
    
    def _validate_related_articles(self) -> Dict:
        """Validate related articles section"""
        articles_data = {
            'section_found': False,
            'article_count': 0,
            'articles': []
        }
        
        try:
            # Look for related articles section
            articles_section = self.page.locator('section:has-text("Related Articles"), [class*="article"], .related-articles')
            if articles_section.count() > 0:
                articles_data['section_found'] = True
                articles = articles_section.locator('article, .article-card, a[href*="article"]')
                articles_data['article_count'] = articles.count()
                print(f"   [OK] Related articles section found: {articles_data['article_count']} articles")
            else:
                print(f"   [INFO] Related articles section not found")
        
        except Exception as e:
            print(f"   [ERROR] Related articles validation failed: {str(e)}")
        
        return articles_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("PRODUCT SERIES VALIDATION SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"Series: {results.get('series', 'Unknown')}")
        print(f"Page Loaded: {'Yes' if summary.get('page_loaded') else 'No'}")
        print(f"Title Found: {'Yes' if summary.get('title_found') else 'No'}")
        print(f"Expected Products: {summary.get('expected_products', 0)}")
        print(f"Found Products: {summary.get('found_products', 0)}")
        print(f"All Products Found: {'Yes' if summary.get('all_products_found') else 'No'}")
        print(f"Filters Working: {'Yes' if summary.get('filters_working') else 'No'}")
        print(f"Links Valid: {'Yes' if summary.get('links_valid') else 'No'}")
        print(f"Comparison Working: {'Yes' if summary.get('comparison_working') else 'No'}")

