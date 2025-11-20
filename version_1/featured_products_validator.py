"""
Featured Products Component Validator
Validates product cards, chevron navigation, hover effects, fonts, images, and sizes
"""
import time
from typing import Dict, List
from playwright.sync_api import Page


class FeaturedProductsValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_featured_products(self, selector: str = '.cmp-carousel.splide.product') -> Dict:
        """Validate Featured Products carousel (cards, links, images, chevrons)."""
        print("\n" + "="*80)
        print("FEATURED PRODUCTS VALIDATION")
        print("="*80)
        
        try:
            # Find featured products section
            section = self.page.locator(selector)
            
            if section.count() == 0:
                print("[WARNING] Featured Products section not found")
                return {'found': False}
            
            print(f"\n[INFO] Featured Products section found")
            
            # Scroll Featured Products into view for the viewer
            try:
                target = section.first
                target.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except Exception:
                pass
            
            # Validate title
            print("\n[TITLE] Validating title...")
            title_data = self._validate_title(section)
            
            # Count and validate product cards
            print("\n[CARDS] Validating product cards...")
            cards_data = self._validate_product_cards(section)
            
            # Validate chevron navigation
            print("\n[CHEVRONS] Validating navigation chevrons...")
            chevron_data = self._validate_chevrons(section)
            
            # Validate hover effect
            print("\n[HOVER] Validating hover effect...")
            hover_data = self._validate_hover_effect(section, cards_data.get('card_count', 0))
            
            results = {
                'found': True,
                'title': title_data,
                'cards': cards_data,
                'chevrons': chevron_data,
                'hover': hover_data,
                'summary': {
                    'total_cards': cards_data.get('card_count', 0),
                    'title_exists': title_data.get('exists', False),
                    'chevrons_working': chevron_data.get('left_works') and chevron_data.get('right_works'),
                    'hover_working': hover_data.get('hover_effect_detected', False)
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Featured Products validation failed: {str(e)}")
            return {'error': str(e)}
    
    def _validate_title(self, section) -> Dict:
        """Validate title of featured products"""
        title_data = {
            'exists': False,
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'font_weight': ''
        }
        
        try:
            # Find title
            title = section.locator('h1, h2, h3, .title, [class*="title"]').first
            
            if title.count() > 0:
                title_data['exists'] = True
                title_data['text'] = title.text_content() or ''
                
                # Get font styles
                styles = title.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
                        return {
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            color: styles.color
                        };
                    }
                """)
                
                if styles:
                    title_data['font_size'] = styles['fontSize']
                    title_data['font_color'] = styles['color']
                    title_data['font_family'] = styles['fontFamily']
                    title_data['font_weight'] = styles['fontWeight']
                
                print(f"   [OK] Title: '{title_data['text'][:50]}'")
                print(f"   [OK] Font: {title_data['font_size']}, Color: {title_data['font_color']}")
        
        except Exception as e:
            print(f"   [ERROR] Title validation failed: {str(e)}")
        
        return title_data
    
    def _validate_product_cards(self, section) -> Dict:
        """Validate product cards within the Featured Products carousel."""
        cards_data = {
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find unique slides (exclude clones) and their product cards
            slides = section.locator('.splide__slide:not(.splide__slide--clone)')
            cards_data['card_count'] = slides.count()
            
            print(f"   [OK] Found {cards_data['card_count']} product cards")
            
            # Validate first few cards in detail
            for i in range(min(slides.count(), 6)):  # First 6 cards (expected total)
                slide = slides.nth(i)
                # product card content inside slide
                card = slide.locator('.cmp-product-card, .productcard').first
                card_data = self._validate_single_card(card, i)
                cards_data['cards'].append(card_data)
        
        except Exception as e:
            print(f"   [ERROR] Product cards validation failed: {str(e)}")
        
        return cards_data
    
    def _validate_single_card(self, card, index: int) -> Dict:
        """Validate a single product card"""
        card_data = {
            'index': index + 1,
            'title': '',
            'description': '',
            'image': {},
            'container': {},
            'font_styles': {},
            'link': {
                'href': '',
                'status_code': 0,
                'is_valid': False
            }
        }
        
        try:
            # Get card title
            title = card.locator('.cmp-product-card__title, h3, h4, .title, [class*="title"], [class*="heading"]').first
            if title.count() > 0:
                card_data['title'] = title.text_content() or ''
                
                # Get title font styles
                title_styles = title.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontWeight: styles.fontWeight
                        };
                    }
                """)
                
                if title_styles:
                    card_data['font_styles']['title'] = title_styles
            
            # Get description
            desc = card.locator('.cmp-product-card__description, p, .description, [class*="description"]').first
            if desc.count() > 0:
                card_data['description'] = desc.text_content() or ''
                
                # Get description font styles
                desc_styles = desc.evaluate("""
                    (desc) => {
                        const styles = window.getComputedStyle(desc);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color
                        };
                    }
                """)
                
                if desc_styles:
                    card_data['font_styles']['description'] = desc_styles
            
            # Get image
            img = card.locator('.cmp-product-card__image img, img').first
            if img.count() > 0:
                img_src = img.get_attribute('src') or img.get_attribute('data-src') or ''
                card_data['image']['src'] = img_src
                
                # Get image dimensions
                img_size = img.evaluate("""
                    (img) => {
                        return {
                            width: img.naturalWidth || img.width,
                            height: img.naturalHeight || img.height
                        };
                    }
                """)
                
                if img_size:
                    card_data['image']['width'] = img_size.get('width', 0)
                    card_data['image']['height'] = img_size.get('height', 0)
            
            # Link on card (anchor wraps card)
            link = card.locator('a[href]').first
            if link.count() > 0:
                href = link.get_attribute('href') or ''
                card_data['link']['href'] = href
                try:
                    from urllib.parse import urljoin
                    absolute_href = href if href.startswith('http') else urljoin(self.page.url, href)
                    response = self.page.request.get(absolute_href, timeout=5000)
                    card_data['link']['status_code'] = response.status
                    card_data['link']['is_valid'] = 200 <= response.status < 400
                except Exception:
                    card_data['link']['status_code'] = 0
                    card_data['link']['is_valid'] = False

                # Capture link font styles (from the anchor or its visible text element)
                try:
                    link_styles = link.evaluate("""
                        (a) => {
                            const styles = window.getComputedStyle(a);
                            return {
                                fontSize: styles.fontSize,
                                color: styles.color,
                                fontWeight: styles.fontWeight,
                                fontFamily: styles.fontFamily,
                                textTransform: styles.textTransform,
                                textDecorationLine: styles.textDecorationLine
                            };
                        }
                    """)
                    if link_styles:
                        card_data['font_styles']['link'] = link_styles
                except Exception:
                    pass

            # Click-anywhere behavior: clicking the whole card should navigate to a valid page
            try:
                current_url = self.page.url
                card.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(200)
                # Try clicking the card container
                card.click(timeout=5000)
                self.page.wait_for_timeout(800)
                new_url = self.page.url
                card_click_navigated = new_url != current_url
                
                card_data['card_click'] = {
                    'attempted': True,
                    'navigated': card_click_navigated,
                    'original_url': current_url,
                    'new_url': new_url
                }
                
                # If navigation happened, go back
                if card_click_navigated:
                    self.page.go_back(wait_until='load', timeout=15000)
                    self.page.wait_for_timeout(800)
            except Exception as _e:
                card_data['card_click'] = { 'attempted': True, 'navigated': False }

            # Get card container size
            card_size = card.evaluate("""
                (card) => {
                    const rect = card.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            
            if card_size:
                card_data['container'] = card_size
            
            print(f"      [OK] Card {index+1}: '{card_data['title'][:30]}'")
            print(f"              Container: {card_data['container'].get('width', 0)}x{card_data['container'].get('height', 0)}")
            if card_data.get('image'):
                print(f"              Image: {card_data['image'].get('width', 0)}x{card_data['image'].get('height', 0)}")
        
        except Exception as e:
            print(f"      [ERROR] Card {index+1} validation failed: {str(e)}")
        
        return card_data
    
    def _validate_chevrons(self, section) -> Dict:
        """Validate chevron navigation functionality (2 clicks each direction)."""
        chevron_data = {
            'left_exists': False,
            'right_exists': False,
            'left_works': False,
            'right_works': False,
            'left_disabled_on_first': False,
            'right_disabled_on_last': False
        }
        
        try:
            # Find chevrons (Splide)
            left_chevron = section.locator('.splide__arrow--prev, [aria-label*="Previous"]')
            right_chevron = section.locator('.splide__arrow--next, [aria-label*="Next"]')
            
            chevron_data['left_exists'] = left_chevron.count() > 0
            chevron_data['right_exists'] = right_chevron.count() > 0
            
            if left_chevron.count() > 0 and right_chevron.count() > 0:
                print(f"   [OK] Both chevrons found")
                
                # Helper: get active slide index
                def active_index():
                    active = section.locator('.splide__slide.is-active, .splide__slide.is-visible')
                    if active.count() > 0:
                        # Find index among unique slides
                        slides = section.locator('.splide__slide:not(.splide__slide--clone)')
                        for i in range(slides.count()):
                            if slides.nth(i).is_visible():
                                return i
                    return 0

                # Test right chevron 2 clicks
                before = active_index()
                for _ in range(2):
                    right_chevron.first.click()
                    self.page.wait_for_timeout(600)
                after = active_index()
                if after != before:
                    chevron_data['right_works'] = True
                    print("   [OK] Right chevron moves the carousel")

                # Test left chevron 2 clicks
                before = active_index()
                for _ in range(2):
                    left_chevron.first.click()
                    self.page.wait_for_timeout(600)
                after = active_index()
                if after != before:
                    chevron_data['left_works'] = True
                    print("   [OK] Left chevron moves the carousel back")
                
                # Navigate back to start and check if left button is disabled
                # Simply check if disabled attribute exists on first load
                initial_left_disabled = left_chevron.first.get_attribute('disabled') is not None
                if initial_left_disabled:
                    chevron_data['left_disabled_on_first'] = True
                    print(f"   [OK] Left chevron is disabled on first card")
                else:
                    print(f"   [INFO] Left chevron is enabled initially")
        
        except Exception as e:
            print(f"   [ERROR] Chevron validation failed: {str(e)}")
        
        return chevron_data
    
    def _get_cards_positions(self, section) -> List[float]:
        """Get horizontal positions of all cards"""
        try:
            cards = section.locator('.card, [class*="card"]')
            positions = cards.evaluate_all("""
                (cards) => {
                    return cards.map(card => card.getBoundingClientRect().left);
                }
            """)
            return positions if positions else []
        except:
            return []
    
    def _validate_hover_effect(self, section, card_count: int) -> Dict:
        """Validate hover effect on cards"""
        hover_data = {
            'hover_effect_detected': False,
            'focus_behavior': ''
        }
        
        try:
            if card_count == 0:
                return hover_data
            
            cards = section.locator('.card, [class*="card"]')
            first_card = cards.first
            
            # Get initial styles
            initial_styles = first_card.evaluate("""
                (card) => {
                    const styles = window.getComputedStyle(card);
                    return {
                        transform: styles.transform,
                        scale: styles.transform.includes('scale'),
                        zIndex: styles.zIndex
                    };
                }
            """)
            
            # Hover over the card
            first_card.hover()
            self.page.wait_for_timeout(500)
            
            # Get styles after hover
            hovered_styles = first_card.evaluate("""
                (card) => {
                    const styles = window.getComputedStyle(card);
                    return {
                        transform: styles.transform,
                        scale: styles.transform.includes('scale'),
                        zIndex: styles.zIndex
                    };
                }
            """)
            
            # Check if styles changed
            if hovered_styles != initial_styles:
                hover_data['hover_effect_detected'] = True
                hover_data['focus_behavior'] = 'Card focuses on hover'
                print(f"   [OK] Hover effect detected on cards")
            
        except Exception as e:
            print(f"   [ERROR] Hover effect validation failed: {str(e)}")
        
        return hover_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("FEATURED PRODUCTS SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"Total Cards: {summary.get('total_cards', 0)}")
        print(f"Title Exists: {'Yes' if summary.get('title_exists') else 'No'}")
        print(f"Chevrons Working: {'Yes' if summary.get('chevrons_working') else 'No'}")
        print(f"Hover Working: {'Yes' if summary.get('hover_working') else 'No'}")
        
        if results.get('title'):
            title = results['title']
            print(f"\nTitle:")
            print(f"  Text: {title.get('text', '')}")
            print(f"  Font Size: {title.get('font_size', '')}")
            print(f"  Font Color: {title.get('font_color', '')}")
        
        if results.get('cards'):
            cards_wrapper = results['cards']
            cards = cards_wrapper.get('cards', []) if isinstance(cards_wrapper, dict) else cards_wrapper
            print(f"\nFirst {len(cards)} Cards:")
            for card in cards:
                print(f"  Card {card.get('index', 0)}:")
                print(f"    Title: {card.get('title', '')[:30]}")
                print(f"    Container: {card.get('container', {}).get('width', 0)}x{card.get('container', {}).get('height', 0)}")
                if card.get('image'):
                    print(f"    Image: {card.get('image', {}).get('width', 0)}x{card.get('image', {}).get('height', 0)}")

