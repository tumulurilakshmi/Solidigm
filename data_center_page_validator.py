"""
Data Center Landing Page Validator
Validates the main data center page at /products/data-center.html
This page shows all three series (D3, D5, D7) together
"""
import time
from typing import Dict, List
from playwright.sync_api import Page
from hero_component_validator import HeroComponentValidator
from model_list_validator import ModelListValidator


class DataCenterPageValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_data_center_page(self, url: str = "https://www.solidigm.com/products/data-center.html", 
                                  filter_params: Dict = None) -> Dict:
        """Validate the Data Center landing page
        
        Args:
            url: URL of the data center page
            filter_params: Dictionary with filter configuration:
                - interface_index: Index for Interface dropdown (0-based)
                - form_factor_index: Index for Form Factor dropdown (0-based)
                - capacity_index: Index for Capacity dropdown (0-based, None to skip)
                - interface_text: Text value for Interface dropdown (overrides index)
                - form_factor_text: Text value for Form Factor dropdown (overrides index)
                - capacity_text: Text value for Capacity dropdown (overrides index)
        """
        print("\n" + "="*80)
        print("DATA CENTER LANDING PAGE VALIDATION")
        print("="*80)
        
        if filter_params is None:
            filter_params = {}
        
        try:
            # Navigate to page
            print(f"\n[INFO] Navigating to {url}")
            self.page.goto(url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(3000)
            
            # Check header and footer presence
            print("\n[HEADER/FOOTER] Checking header and footer presence...")
            header_footer_data = self._check_header_footer()
            
            # Validate hero component
            print("\n[HERO] Validating hero component...")
            hero_validator = HeroComponentValidator(self.page)
            hero_data = hero_validator.validate_hero_component()
            
            # Validate series cards/links
            print("\n[SERIES CARDS] Validating series cards...")
            series_cards_data = self._validate_series_cards()
            
            # Validate model list section
            print("\n[MODEL LIST] Validating model list section...")
            model_list_validator = ModelListValidator(self.page)
            model_list_data = model_list_validator.validate_model_list(filter_params=filter_params)
            
            # Validate related articles
            print("\n[RELATED ARTICLES] Validating related articles...")
            articles_data = self._validate_related_articles()
            
            results = {
                'url': url,
                'header_footer': header_footer_data,
                'hero': hero_data,
                'series_cards': series_cards_data,
                'model_list': model_list_data,
                'related_articles': articles_data,
                'summary': {
                    'header_found': header_footer_data.get('header_found', False),
                    'footer_found': header_footer_data.get('footer_found', False),
                    'hero_found': hero_data.get('found', False),
                    'series_cards_found': series_cards_data.get('found', False),
                    'all_series_present': series_cards_data.get('all_series_present', False),
                    'model_list_found': model_list_data.get('found', False),
                    'articles_found': articles_data.get('found', False)
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Data Center page validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _check_header_footer(self) -> Dict:
        """Check if header and footer are present on the page"""
        header_footer_data = {
            'header_found': False,
            'footer_found': False
        }
        
        try:
            # Check for header - look for navigation or header elements
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
            
            # Check for footer - look for footer elements
            footer_selectors = [
                'footer',
                '.footer',
                '[class*="footer"]',
                '.cmp-experiencefragment--footer'
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
    
    def _validate_series_cards(self) -> Dict:
        """Validate series cards (D7, D5, D3) on the data center page"""
        series_cards_data = {
            'found': False,
            'cards': [],
            'all_series_present': False,
            'expected_series': ['D7', 'D5', 'D3']
        }
        
        try:
            # Find series list container
            series_list = self.page.locator('.series-list, .serieslist').first
            
            if series_list.count() == 0:
                print(f"   [WARNING] Series list container not found")
                return series_cards_data
            
            found_series = []
            
            # Find series cards using the correct selector
            # Based on HTML: .series-list__serie
            series_cards = series_list.locator('.series-list__serie, a[href*="/d7.html"], a[href*="/d5.html"], a[href*="/d3.html"]').all()
            
            for card in series_cards:
                try:
                    # Get href to determine which series
                    href = card.get_attribute('href') or ''
                    series = None
                    
                    if '/d7.html' in href:
                        series = 'D7'
                    elif '/d5.html' in href:
                        series = 'D5'
                    elif '/d3.html' in href:
                        series = 'D3'
                    else:
                        # Try to determine from title text
                        title_elem = card.locator('.series-list__serie__text__title, h3').first
                        if title_elem.count() > 0:
                            title_text = (title_elem.text_content() or '').strip()
                            if 'D7' in title_text:
                                series = 'D7'
                            elif 'D5' in title_text:
                                series = 'D5'
                            elif 'D3' in title_text:
                                series = 'D3'
                    
                    if series and series not in found_series:
                        card_data = self._validate_series_card(card, series)
                        series_cards_data['cards'].append(card_data)
                        found_series.append(series)
                
                except Exception as e:
                    print(f"      [ERROR] Error validating series card: {str(e)}")
                    continue
            
            series_cards_data['found'] = len(found_series) > 0
            series_cards_data['all_series_present'] = len(found_series) == 3
            
            print(f"   [OK] Found {len(found_series)} series cards: {', '.join(found_series)}")
            if series_cards_data['all_series_present']:
                print(f"   [OK] All 3 series (D7, D5, D3) are present")
            else:
                missing = [s for s in series_cards_data['expected_series'] if s not in found_series]
                print(f"   [WARNING] Missing series: {', '.join(missing)}")
        
        except Exception as e:
            print(f"   [ERROR] Series cards validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return series_cards_data
    
    def _validate_series_card(self, card, series: str) -> Dict:
        """Validate a single series card"""
        card_data = {
            'series': series,
            'title': '',
            'description': '',
            'image': {},
            'href': '',
            'font_details': {},
            'url_format_valid': False
        }
        
        try:
            # Get href
            card_data['href'] = card.get_attribute('href') or ''
            
            # Get title from .series-list__serie__text__title or h3
            title_elem = card.locator('.series-list__serie__text__title, h3').first
            if title_elem.count() > 0:
                card_data['title'] = (title_elem.text_content() or '').strip()
            
            # Get description from .series-list__serie__text__description or p
            desc_elem = card.locator('.series-list__serie__text__description, p').first
            if desc_elem.count() > 0:
                card_data['description'] = (desc_elem.text_content() or '').strip()
            
            # Get image
            img = card.locator('.series-list__serie__image, img').first
            if img.count() > 0:
                card_data['image']['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                card_data['image']['alt'] = img.get_attribute('alt') or ''
            
            # Get font details from title
            if title_elem.count() > 0:
                font_styles = title_elem.evaluate("""
                    (elem) => {
                        const styles = window.getComputedStyle(elem);
                        return {
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            color: styles.color,
                            lineHeight: styles.lineHeight
                        };
                    }
                """)
                if font_styles:
                    card_data['font_details'] = font_styles
            
            # Validate URL format (without navigating to save time)
            if card_data['href']:
                try:
                    href = card_data['href']
                    
                    # Verify URL format matches expected pattern
                    # Expected: /products/data-center/{series}.html
                    # Example: /products/data-center/d7.html
                    
                    url_valid = False
                    if href and '/products/data-center/' in href and (href.endswith('/d7.html') or href.endswith('/d5.html') or href.endswith('/d3.html')):
                        url_valid = True
                        card_data['url_format_valid'] = True
                        print(f"         [OK] Series URL format valid: {href}")
                    else:
                        card_data['url_format_valid'] = False
                        print(f"         [WARNING] Series URL format unexpected: {href}")
                        
                except Exception as e:
                    card_data['url_format_error'] = str(e)
                    print(f"         [ERROR] URL format validation failed: {str(e)}")
            
            print(f"      [OK] {series} Series: '{card_data['title']}' -> {card_data['href']}")
            if card_data['description']:
                print(f"         Description: {card_data['description'][:80]}...")
        
        except Exception as e:
            print(f"      [ERROR] {series} Series card validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return card_data
    
    def _validate_related_articles(self) -> Dict:
        """Validate related articles section"""
        articles_data = {
            'found': False,
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find related articles section - look for .cmp-article-list or section with "Related Articles"
            articles_section = self.page.locator('.cmp-article-list, section:has-text("Related Articles"), .related-articles').first
            
            if articles_section.count() > 0:
                articles_data['found'] = True
                
                # Find article cards - use the correct selector for the carousel structure
                # Articles are in .splide__slide > .cmp-article-list__article
                article_cards = articles_section.locator('.cmp-article-list__article, .splide__slide .cmp-article-list__article').all()
                
                # If no cards found with that selector, try alternative
                if len(article_cards) == 0:
                    article_cards = articles_section.locator('.splide__list .splide__slide').all()
                
                articles_data['card_count'] = len(article_cards)
                
                print(f"   [OK] Related articles found: {articles_data['card_count']} cards")
                
                # Validate each article card (max 3)
                for i, card in enumerate(article_cards[:3]):
                    article_data = self._validate_single_article_card(card, i)
                    articles_data['cards'].append(article_data)
            else:
                print(f"   [INFO] Related articles section not found")
        
        except Exception as e:
            print(f"   [ERROR] Related articles validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return articles_data
    
    def _validate_single_article_card(self, card, index: int) -> Dict:
        """Validate a single article card"""
        article_data = {
            'index': index + 1,
            'container': {},
            'image': {},
            'category': '',
            'title': {},
            'link': '',
            'url_format_valid': False
        }
        
        try:
            # Find the actual article element (might be nested in splide slide)
            article_elem = card.locator('.cmp-article-list__article').first
            if article_elem.count() == 0:
                article_elem = card
            
            # Container size
            container_size = article_elem.evaluate("""
                (card) => {
                    const rect = card.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            if container_size:
                article_data['container'] = {
                    'width': int(container_size.get('width', 0)),
                    'height': int(container_size.get('height', 0))
                }
            
            # Image - look for image in .cmp-article-list__article-image
            img = article_elem.locator('.cmp-article-list__article-image img, img').first
            if img.count() > 0:
                article_data['image']['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                article_data['image']['alt'] = img.get_attribute('alt') or ''
                article_data['image']['height'] = img.get_attribute('height') or ''
                article_data['image']['width'] = img.get_attribute('width') or ''
            
            # Category - look for .cmp-article-list__article-category
            category = article_elem.locator('.cmp-article-list__article-category').first
            if category.count() > 0:
                article_data['category'] = (category.text_content() or '').strip()
            
            # Title - look for .cmp-article-list__article-title
            title = article_elem.locator('.cmp-article-list__article-title, h3').first
            if title.count() > 0:
                article_data['title']['text'] = (title.text_content() or '').strip()
                
                # Get font details
                title_font = title.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight
                        };
                    }
                """)
                if title_font:
                    article_data['title'].update(title_font)
            
            # Link - look for anchor tag
            link = article_elem.locator('a').first
            if link.count() > 0:
                article_data['link'] = link.get_attribute('href') or ''
                
                # Validate URL format (without navigating to save time)
                if article_data['link']:
                    try:
                        href = article_data['link']
                        article_title = article_data['title'].get('text', '')
                        
                        # Verify URL format matches expected pattern
                        # Expected: /products/technology/{article-slug}.html
                        
                        url_valid = False
                        url_matches_title = False
                        
                        if href and ('/products/technology/' in href or '/products/' in href):
                            url_valid = True
                            
                            # Check if URL contains article title keywords
                            if article_title:
                                title_variations = [
                                    article_title.lower().replace(' ', '-'),
                                    article_title.lower().replace(' ', '-').replace(':', '').replace(',', ''),
                                    article_title[:30].lower().replace(' ', '-'),
                                ]
                                
                                for variation in title_variations:
                                    if variation and variation in href.lower():
                                        url_matches_title = True
                                        break
                            
                            if url_valid and (url_matches_title or href.endswith('.html')):
                                article_data['url_format_valid'] = True
                                article_data['url_matches_title'] = url_matches_title
                                print(f"         [OK] Article URL format valid: {href}")
                            else:
                                article_data['url_format_valid'] = True  # URL format is valid
                                article_data['url_matches_title'] = False
                                print(f"         [WARNING] Article URL format valid but may not match title: {href}")
                        else:
                            article_data['url_format_valid'] = False
                            print(f"         [WARNING] Article URL format unexpected: {href}")
                            
                    except Exception as e:
                        article_data['url_format_error'] = str(e)
                        print(f"         [ERROR] Article URL format validation failed: {str(e)}")
            
            print(f"      [OK] Article {index+1}: '{article_data['title'].get('text', '')[:50]}'")
            if article_data['category']:
                print(f"         Category: {article_data['category']}")
        
        except Exception as e:
            print(f"      [ERROR] Article card {index+1} validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
        
        return article_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("DATA CENTER PAGE SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"Header Found: {'Yes' if summary.get('header_found') else 'No'}")
        print(f"Footer Found: {'Yes' if summary.get('footer_found') else 'No'}")
        print(f"Hero Found: {'Yes' if summary.get('hero_found') else 'No'}")
        print(f"Series Cards Found: {'Yes' if summary.get('series_cards_found') else 'No'}")
        print(f"All Series Present: {'Yes' if summary.get('all_series_present') else 'No'}")
        print(f"Model List Found: {'Yes' if summary.get('model_list_found') else 'No'}")
        print(f"Related Articles Found: {'Yes' if summary.get('articles_found') else 'No'}")
        
        series_cards = results.get('series_cards', {})
        if series_cards.get('found'):
            print(f"\nSeries Cards: {len(series_cards.get('cards', []))}")
            for card in series_cards.get('cards', []):
                print(f"  - {card.get('series')}: {card.get('text', '')[:50]}")

