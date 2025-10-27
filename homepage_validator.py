"""
Comprehensive Home Page Validator for Solidigm Website
Validates all home page components including Navigation, Carousel, Featured Products,
Product Cards, Article List, Blade Components, Title List, Search, and Footer
"""
import time
from typing import Dict, List
from playwright.sync_api import Page
from navigation_validator import NavigationValidator
from carousel_validator import CarouselValidator
from link_validator import LinkValidator
from featured_products_validator import FeaturedProductsValidator
from article_list_validator import ArticleListValidator


class HomePageValidator:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
        self.results = {}
    
    def validate_complete_homepage(self) -> Dict:
        """Validate all home page components"""
        print("\n" + "="*100)
        print(" " * 30 + "HOMEPAGE COMPREHENSIVE VALIDATION")
        print("="*100)
        
        try:
            # Navigate to home page
            print(f"\n[INFO] Navigating to {self.base_url}")
            self.page.goto(self.base_url, timeout=90000, wait_until='domcontentloaded')
            self.page.wait_for_timeout(3000)
            
            title = self.page.title()
            print(f"[OK] Page loaded: {title}")
            
            # Initialize validators
            nav_validator = NavigationValidator(self.page, self.base_url)
            carousel_validator = CarouselValidator(self.page)
            link_validator = LinkValidator(self.page, self.base_url)
            featured_products_validator = FeaturedProductsValidator(self.page)
            article_list_validator = ArticleListValidator(self.page)
            
            # Validate each component
            print("\n" + "="*100)
            print("COMPONENT 1: NAVIGATION")
            print("="*100)
            navigation_results = nav_validator.validate_navigation_menu()
            
            print("\n" + "="*100)
            print("COMPONENT 2: CAROUSEL")
            print("="*100)
            carousel_results = carousel_validator.validate_carousel()
            
            print("\n" + "="*100)
            print("COMPONENT 3: FEATURED PRODUCTS")
            print("="*100)
            featured_products = featured_products_validator.validate_featured_products()
            
            print("\n" + "="*100)
            print("COMPONENT 4: PRODUCT CARDS")
            print("="*100)
            product_cards = self._validate_product_cards()
            
            print("\n" + "="*100)
            print("COMPONENT 5: ARTICLE LIST")
            print("="*100)
            article_list = article_list_validator.validate_article_list()
            
            print("\n" + "="*100)
            print("COMPONENT 6: BLADE COMPONENTS")
            print("="*100)
            blade_components = self._validate_blade_components()
            
            print("\n" + "="*100)
            print("COMPONENT 7: TITLE LIST")
            print("="*100)
            title_list = self._validate_title_list()
            
            print("\n" + "="*100)
            print("COMPONENT 8: SEARCH")
            print("="*100)
            search_component = self._validate_search_component()
            
            print("\n" + "="*100)
            print("COMPONENT 9: FOOTER")
            print("="*100)
            footer = self._validate_footer()
            
            # Compile all results
            self.results = {
                'url': self.base_url,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'navigation': navigation_results,
                'carousel': carousel_results,
                'featured_products': featured_products,
                'product_cards': product_cards,
                'article_list': article_list,
                'blade_components': blade_components,
                'title_list': title_list,
                'search': search_component,
                'footer': footer,
                'summary': self._generate_summary()
            }
            
            print("\n" + "="*100)
            print("✅ HOMEPAGE VALIDATION COMPLETE")
            print("="*100)
            
            return self.results
            
        except Exception as e:
            print(f"\n[ERROR] Homepage validation failed: {str(e)}")
            return {'error': str(e)}
    
    
    def _validate_product_cards(self) -> Dict:
        """Validate Product Cards component"""
        print("[INFO] Validating Product Cards...")
        
        results = {
            'component_exists': False,
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find product cards
            cards = self.page.locator('.product-card, [class*="card"], .card-product')
            
            if cards.count() > 0:
                results['component_exists'] = True
                results['card_count'] = cards.count()
                print(f"   [OK] Found {results['card_count']} product cards")
                
        except Exception as e:
            print(f"   [ERROR] Product Cards validation failed: {str(e)}")
        
        return results
    
    
    def _validate_blade_components(self) -> Dict:
        """Validate Blade Components (left/right image layouts)"""
        print("[INFO] Validating Blade Components...")
        
        results = {
            'component_exists': False,
            'blade_count': 0,
            'blades': []
        }
        
        try:
            # Find blade components
            blades = self.page.locator('.blade, [class*="blade"], [class*="image-text"]')
            
            if blades.count() > 0:
                results['component_exists'] = True
                results['blade_count'] = blades.count()
                print(f"   [OK] Found {results['blade_count']} blade components")
                
        except Exception as e:
            print(f"   [ERROR] Blade Components validation failed: {str(e)}")
        
        return results
    
    def _validate_title_list(self) -> Dict:
        """Validate Title List component"""
        print("[INFO] Validating Title List...")
        
        results = {
            'component_exists': False,
            'titles': []
        }
        
        try:
            # Find title lists
            title_lists = self.page.locator('[class*="title-list"], .title-list, [class*="heading-list"]')
            
            if title_lists.count() > 0:
                results['component_exists'] = True
                print(f"   [OK] Title List component found")
                
        except Exception as e:
            print(f"   [ERROR] Title List validation failed: {str(e)}")
        
        return results
    
    def _validate_search_component(self) -> Dict:
        """Validate Search component (already done in navigation)"""
        print("[INFO] Validating Search component...")
        
        results = {
            'component_exists': False,
            'is_visible': False,
            'modal_opens': False
        }
        
        try:
            search_button = self.page.locator('.c-search__button, [class*="search"]')
            
            if search_button.count() > 0 and search_button.first.is_visible():
                results['component_exists'] = True
                results['is_visible'] = True
                
                # Test if modal opens
                search_button.first.click()
                self.page.wait_for_timeout(500)
                
                modal = self.page.locator('.c-search__modal')
                results['modal_opens'] = modal.is_visible() if modal.count() > 0 else False
                
                # Close modal
                close_btn = self.page.locator('.c-search__modal-close')
                if close_btn.count() > 0:
                    close_btn.first.click()
                    self.page.wait_for_timeout(300)
                
                print(f"   [OK] Search component validated")
            
        except Exception as e:
            print(f"   [ERROR] Search component validation failed: {str(e)}")
        
        return results
    
    def _validate_footer(self) -> Dict:
        """Validate Footer component"""
        print("[INFO] Validating Footer...")
        
        results = {
            'component_exists': False,
            'links_count': 0,
            'sections': []
        }
        
        try:
            footer = self.page.locator('footer, .footer, [class*="footer"]')
            
            if footer.count() > 0:
                results['component_exists'] = True
                
                # Count links
                links = footer.locator('a')
                results['links_count'] = links.count()
                
                # Count sections
                sections = footer.locator('section, [class*="section"], ul')
                results['section_count'] = sections.count()
                
                print(f"   [OK] Footer found with {results['links_count']} links in {results['section_count']} sections")
                
        except Exception as e:
            print(f"   [ERROR] Footer validation failed: {str(e)}")
        
        return results
    
    def _generate_summary(self) -> Dict:
        """Generate validation summary"""
        return {
            'navigation_validated': 'navigation' in self.results,
            'carousel_count': self.results.get('carousel', {}).get('carousel_count', 0),
            'featured_products_count': self.results.get('featured_products', {}).get('product_count', 0),
            'product_cards_count': self.results.get('product_cards', {}).get('card_count', 0),
            'article_count': self.results.get('article_list', {}).get('article_count', 0),
            'blade_count': self.results.get('blade_components', {}).get('blade_count', 0),
            'footer_exists': self.results.get('footer', {}).get('component_exists', False)
        }

