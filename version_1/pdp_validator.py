"""
Product Detail Page (PDP) Validator
Validates individual product pages like D3-S4620, D7-P5520, etc.
"""
from typing import Dict, Optional
from playwright.sync_api import Page
from hero_component_validator import HeroComponentValidator


class PDPValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_pdp_page(self, product_url: str, expected_product_name: Optional[str] = None) -> Dict:
        """Validate a Product Detail Page (PDP)"""
        print("\n" + "="*80)
        print("PRODUCT DETAIL PAGE (PDP) VALIDATION")
        print("="*80)
        
        results = {
            'url': product_url,
            'product_name': expected_product_name,
            'hero': {},
            'filters': {},
            'cards': {},
            'related_articles': {},
            'search': {},
            'header_footer': {},
            'navigation_tested': False
        }
        
        try:
            # Navigate to PDP page
            print(f"\n[INFO] Navigating to PDP page: {product_url}")
            self.page.goto(product_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(3000)
            
            # Extract product name from URL if not provided
            if not expected_product_name:
                # Extract from URL: /d3/s4620.html -> D3-S4620
                url_parts = product_url.split('/')
                if len(url_parts) >= 2:
                    series = url_parts[-2].upper()  # d3 -> D3
                    product_id = url_parts[-1].replace('.html', '').upper()  # s4620.html -> S4620
                    expected_product_name = f"{series}-{product_id}"
                results['product_name'] = expected_product_name
                print(f"   [OK] Extracted product name: {expected_product_name}")
            
            # Validate Header and Footer
            print("\n[HEADER/FOOTER] Validating header and footer...")
            results['header_footer'] = self._validate_header_footer()
            
            # Validate Hero Component
            print("\n[HERO] Validating hero component...")
            hero_validator = HeroComponentValidator(self.page)
            results['hero'] = hero_validator.validate_hero_component()
            
            # Validate Filters (if present on PDP)
            print("\n[FILTERS] Validating filters...")
            results['filters'] = self._validate_filters()
            
            # Validate Product Cards (if present - for comparison/related products)
            print("\n[CARDS] Validating product cards...")
            results['cards'] = self._validate_cards()
            
            # Validate Related Articles
            print("\n[RELATED ARTICLES] Validating related articles...")
            results['related_articles'] = self._validate_related_articles()
            
            # Validate Search Section
            print("\n[SEARCH] Validating search section...")
            results['search'] = self._validate_search()
            
            print("\n" + "="*80)
            print("PDP VALIDATION SUMMARY")
            print("="*80)
            print(f"Product Name: {expected_product_name}")
            print(f"Hero Component: {'Found' if results['hero'].get('found') else 'Not Found'}")
            print(f"Filters: {'Found' if results['filters'].get('found') else 'Not Found'}")
            print(f"Cards: {results['cards'].get('card_count', 0)} found")
            print(f"Related Articles: {results['related_articles'].get('article_count', 0)} found")
            print(f"Search Component: {'Found' if results['search'].get('component_exists') else 'Not Found'}")
            print(f"Header/Footer: Header={results['header_footer'].get('header_found')}, Footer={results['header_footer'].get('footer_found')}")
            
        except Exception as e:
            print(f"\n[ERROR] PDP validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            results['error'] = str(e)
        
        return results
    
    def _validate_header_footer(self) -> Dict:
        """Validate header and footer presence"""
        header_footer_data = {
            'header_found': False,
            'footer_found': False
        }
        
        try:
            # Check for header
            header_selectors = [
                'header',
                '.cmp-navigation',
                'nav.cmp-navigation',
                '[class*="navigation"]',
                '[class*="header"]'
            ]
            
            for selector in header_selectors:
                header = self.page.locator(selector).first
                if header.count() > 0:
                    header_footer_data['header_found'] = True
                    print(f"   [OK] Header found using selector: {selector}")
                    break
            
            if not header_footer_data['header_found']:
                print(f"   [WARNING] Header not found")
            
            # Check for footer
            footer_selectors = [
                '.footer-content__main',
                '.footer-content',
                'footer',
                '[class*="footer"]'
            ]
            
            for selector in footer_selectors:
                footer = self.page.locator(selector).first
                if footer.count() > 0:
                    header_footer_data['footer_found'] = True
                    print(f"   [OK] Footer found using selector: {selector}")
                    break
            
            if not header_footer_data['footer_found']:
                print(f"   [WARNING] Footer not found")
        
        except Exception as e:
            print(f"   [ERROR] Header/Footer check failed: {str(e)}")
        
        return header_footer_data
    
    def _validate_filters(self) -> Dict:
        """Validate filters on PDP page (if present)"""
        filter_data = {
            'found': False,
            'filters': []
        }
        
        try:
            # Look for filter sections (may not be present on PDP)
            filter_section = self.page.locator('.filters, .filter-section, [class*="filter"]').first
            if filter_section.count() > 0:
                filter_data['found'] = True
                print(f"   [OK] Filter section found")
            else:
                print(f"   [INFO] No filter section found on PDP (this is expected)")
        
        except Exception as e:
            print(f"   [WARNING] Filter validation failed: {str(e)}")
        
        return filter_data
    
    def _validate_cards(self) -> Dict:
        """Validate product cards on PDP (for comparison/related products)"""
        cards_data = {
            'found': False,
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Look for product cards (may be in comparison section or related products)
            card_selectors = [
                '.cmp-product-cards__item',
                '.product-card',
                '.product-cards__item',
                '[class*="product-card"]'
            ]
            
            for selector in card_selectors:
                cards = self.page.locator(selector)
                count = cards.count()
                if count > 0:
                    cards_data['found'] = True
                    cards_data['card_count'] = count
                    print(f"   [OK] Found {count} product cards")
                    
                    # Validate first few cards
                    for i in range(min(5, count)):
                        card = cards.nth(i)
                        card_data = self._validate_single_card(card, i + 1)
                        cards_data['cards'].append(card_data)
                    break
            
            if not cards_data['found']:
                print(f"   [INFO] No product cards found on PDP (this may be expected)")
        
        except Exception as e:
            print(f"   [WARNING] Card validation failed: {str(e)}")
        
        return cards_data
    
    def _validate_single_card(self, card, index: int) -> Dict:
        """Validate a single product card"""
        card_data = {
            'index': index,
            'title': '',
            'view_details_link': {},
            'compare_button': {},
            'navigation_tested': False
        }
        
        try:
            # Get card title
            title_elem = card.locator('.cmp-product-cards__item-title, h3, .product-title').first
            if title_elem.count() > 0:
                card_data['title'] = (title_elem.text_content() or '').strip()
            
            # Get View Details button/link
            view_details = card.locator('.cmp-product-cards__details-btn, a[href*="/products/data-center"]').first
            if view_details.count() > 0:
                view_details_href = view_details.get_attribute('href') or ''
                view_details_text = (view_details.text_content() or '').strip()
                card_data['view_details_link'] = {
                    'text': view_details_text,
                    'href': view_details_href
                }
                
                # Test navigation if href is present
                if view_details_href and view_details_href != '#':
                    try:
                        from urllib.parse import urljoin
                        absolute_href = view_details_href if view_details_href.startswith('http') else urljoin(self.page.url, view_details_href)
                        
                        # Store current URL
                        current_url = self.page.url
                        
                        # Click View Details
                        view_details.click(timeout=5000)
                        self.page.wait_for_load_state('domcontentloaded', timeout=30000)
                        self.page.wait_for_timeout(2000)
                        
                        # Verify navigation
                        new_url = self.page.url
                        card_data['navigation_tested'] = True
                        card_data['navigation_success'] = new_url != current_url
                        card_data['navigated_to'] = new_url
                        
                        # Navigate back
                        self.page.goto(current_url, timeout=90000, wait_until='domcontentloaded')
                        self.page.wait_for_timeout(2000)
                        
                        if card_data['navigation_success']:
                            print(f"      [OK] Card {index} View Details navigation successful: {new_url}")
                        else:
                            print(f"      [WARNING] Card {index} View Details navigation may have failed")
                    except Exception as e:
                        print(f"      [WARNING] Card {index} View Details navigation test failed: {str(e)}")
                        card_data['navigation_error'] = str(e)
            
            # Get Compare button
            compare_btn = card.locator('.cmp-product-cards__configure-btn, button:has-text("Compare")').first
            if compare_btn.count() > 0:
                compare_text = (compare_btn.text_content() or '').strip()
                card_data['compare_button'] = {
                    'text': compare_text,
                    'found': True
                }
        
        except Exception as e:
            print(f"      [ERROR] Error validating card {index}: {str(e)}")
        
        return card_data
    
    def _validate_related_articles(self) -> Dict:
        """Validate related articles section"""
        articles_data = {
            'found': False,
            'article_count': 0,
            'articles': []
        }
        
        try:
            # Look for related articles section
            articles_section = self.page.locator('.cmp-article-list, .related-articles, [class*="article"]').first
            if articles_section.count() > 0:
                articles_data['found'] = True
                
                # Count article cards
                article_cards = articles_section.locator('.cmp-article-list__article, .article-card, a[href*="/products/"]')
                count = article_cards.count()
                articles_data['article_count'] = count
                print(f"   [OK] Found {count} related articles")
                
                # Validate first few articles
                for i in range(min(3, count)):
                    article = article_cards.nth(i)
                    article_data = self._validate_single_article(article, i + 1)
                    articles_data['articles'].append(article_data)
            else:
                print(f"   [INFO] No related articles section found")
        
        except Exception as e:
            print(f"   [WARNING] Related articles validation failed: {str(e)}")
        
        return articles_data
    
    def _validate_single_article(self, article, index: int) -> Dict:
        """Validate a single article card"""
        article_data = {
            'index': index,
            'title': '',
            'link': {},
            'image': {}
        }
        
        try:
            # Get article title
            title_elem = article.locator('.cmp-article-list__article-title, h3, .article-title').first
            if title_elem.count() > 0:
                article_data['title'] = (title_elem.text_content() or '').strip()
            
            # Get article link
            link_elem = article.locator('a').first
            if link_elem.count() > 0:
                link_href = link_elem.get_attribute('href') or ''
                article_data['link'] = {
                    'href': link_href
                }
            
            # Get article image
            img_elem = article.locator('img').first
            if img_elem.count() > 0:
                img_src = img_elem.get_attribute('src') or ''
                article_data['image'] = {
                    'src': img_src
                }
        
        except Exception as e:
            print(f"      [ERROR] Error validating article {index}: {str(e)}")
        
        return article_data
    
    def _validate_search(self) -> Dict:
        """Validate search component"""
        results = {
            'component_exists': False,
            'title': {},
            'form': {},
            'suggestions': []
        }
        
        try:
            # Find search component
            search_component = self.page.locator('.search-component').first
            
            if search_component.count() == 0:
                print("   [INFO] Search component not found")
                return results
            
            results['component_exists'] = True
            print(f"   [OK] Search component found")
            
            # Scroll to component
            try:
                search_component.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except:
                pass
            
            # Validate title
            title_element = search_component.locator('.search-component__title, h3').first
            if title_element.count() > 0:
                title_text = (title_element.text_content() or '').strip()
                results['title']['text'] = title_text
                print(f"      Title: {title_text}")
            
            # Validate search form
            form = search_component.locator('form.search-label').first
            if form.count() > 0:
                form_action = form.get_attribute('action') or ''
                form_method = form.get_attribute('method') or 'get'
                
                results['form']['action'] = form_action
                results['form']['method'] = form_method
                print(f"      Form action: {form_action}")
            
            # Validate search suggestions
            suggestions = search_component.locator('.search-component__suggestions__suggestion, a[class*="suggestion"]')
            suggestion_count = suggestions.count()
            results['suggestion_count'] = suggestion_count
            
            print(f"      Found {suggestion_count} suggestions")
        
        except Exception as e:
            print(f"   [ERROR] Search component validation failed: {str(e)}")
            results['error'] = str(e)
        
        return results

