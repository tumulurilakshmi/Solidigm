"""
Article List (Card List) Component Validator
Validates article cards, chevron navigation, hover effects, fonts, images, and sizes
Based on the provided HTML structure
"""
import time
from typing import Dict, List
from playwright.sync_api import Page


class ArticleListValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_article_list(self, selector: str = '.articlelist, .cmp-article-list, [class*="article-list"], .splide') -> Dict:
        """Validate Article List Card component"""
        print("\n" + "="*80)
        print("ARTICLE LIST (CARD LIST) VALIDATION")
        print("="*80)
        
        try:
            # Find article list section
            section = self.page.locator(selector)
            
            if section.count() == 0:
                print("[WARNING] Article List section not found")
                return {'found': False}
            
            print(f"\n[INFO] Article List section found")
            
            # Validate title
            print("\n[TITLE] Validating title and View All link...")
            title_data = self._validate_title_and_view_all(section)
            
            # Count and validate article cards
            print("\n[CARDS] Validating article cards...")
            cards_data = self._validate_article_cards(section)
            
            # Validate chevron navigation
            print("\n[CHEVRONS] Validating navigation chevrons...")
            chevron_data = self._validate_chevrons(section)
            
            # Validate hover effect
            print("\n[HOVER] Validating hover effect...")
            hover_data = self._validate_hover_effect(section, cards_data.get('card_count', 0))
            
            # Validate clickable links
            print("\n[LINKS] Validating clickable card links...")
            links_data = self._validate_card_links(section, cards_data.get('cards', []))
            
            results = {
                'found': True,
                'title': title_data,
                'cards': cards_data,
                'chevrons': chevron_data,
                'hover': hover_data,
                'links': links_data,
                'summary': {
                    'total_cards': cards_data.get('card_count', 0),
                    'title_exists': title_data.get('exists', False),
                    'view_all_link_valid': title_data.get('view_all_valid', False),
                    'chevrons_working': chevron_data.get('left_works') and chevron_data.get('right_works'),
                    'hover_working': hover_data.get('hover_effect_detected', False),
                    'all_links_valid': links_data.get('all_links_valid', False)
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Article List validation failed: {str(e)}")
            return {'error': str(e)}
    
    def _validate_title_and_view_all(self, section) -> Dict:
        """Validate title and View All link"""
        title_data = {
            'exists': False,
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'view_all_exists': False,
            'view_all_text': '',
            'view_all_href': '',
            'view_all_valid': False
        }
        
        try:
            # Find title
            title = section.locator('.section-title--with-link h2, h2').first
            
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
                
                print(f"   [OK] Title: '{title_data['text']}'")
                print(f"   [OK] Font: {title_data['font_size']}, Color: {title_data['font_color']}")
            
            # Find View All link
            view_all = section.locator('.section-title--with-link a, a[href*="technology"]').first
            
            if view_all.count() > 0:
                title_data['view_all_exists'] = True
                title_data['view_all_text'] = view_all.text_content() or ''
                title_data['view_all_href'] = view_all.get_attribute('href') or ''
                
                # Validate link
                try:
                    href = title_data['view_all_href']
                    if href.startswith('/'):
                        href = self.page.evaluate(f"window.location.origin + '{href}'")
                    
                    response = self.page.request.get(href, timeout=5000)
                    title_data['view_all_valid'] = 200 <= response.status < 400
                    
                    print(f"   [OK] View All link: '{title_data['view_all_text']}' -> {title_data['view_all_href']}")
                    print(f"   [OK] Link valid: {title_data['view_all_valid']}")
                except:
                    print(f"   [WARNING] Could not validate View All link")
        
        except Exception as e:
            print(f"   [ERROR] Title validation failed: {str(e)}")
        
        return title_data
    
    def _validate_article_cards(self, section) -> Dict:
        """Validate article cards"""
        cards_data = {
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find all splide slides (articles)
            cards = section.locator('.splide__slide, .cmp-article-list__article')
            cards_data['card_count'] = cards.count()
            
            print(f"   [OK] Found {cards_data['card_count']} article cards")
            
            # Validate each card in detail
            for i in range(min(cards.count(), 6)):  # First 6 cards
                card = cards.nth(i)
                card_data = self._validate_single_article_card(card, i)
                cards_data['cards'].append(card_data)
        
        except Exception as e:
            print(f"   [ERROR] Article cards validation failed: {str(e)}")
        
        return cards_data
    
    def _validate_single_article_card(self, card, index: int) -> Dict:
        """Validate a single article card"""
        card_data = {
            'index': index + 1,
            'title': '',
            'category': '',
            'image': {},
            'container': {},
            'font_styles': {},
            'link': ''
        }
        
        try:
            # Get card title
            title = card.locator('.cmp-article-list__article-title, h3').first
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
            
            # Get category/tag
            category = card.locator('.cmp-article-list__article-category, span').first
            if category.count() > 0:
                card_data['category'] = category.text_content() or ''
                
                # Get category font styles
                category_styles = category.evaluate("""
                    (category) => {
                        const styles = window.getComputedStyle(category);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color
                        };
                    }
                """)
                
                if category_styles:
                    card_data['font_styles']['category'] = category_styles
            
            # Get image
            img = card.locator('.cmp-article-list__article-image img, img').first
            if img.count() > 0:
                img_src = img.get_attribute('src') or img.get_attribute('data-src') or ''
                card_data['image']['src'] = img_src
                
                # Get image dimensions
                img_size = img.evaluate("""
                    (img) => {
                        return {
                            width: img.naturalWidth || img.width || 0,
                            height: img.naturalHeight || img.height || 0
                        };
                    }
                """)
                
                if img_size:
                    card_data['image']['width'] = img_size.get('width', 0)
                    card_data['image']['height'] = img_size.get('height', 0)
                
                # Check if image is loaded
                img_loaded = img.evaluate("""
                    (img) => {
                        return img && img.complete && img.naturalHeight !== 0;
                    }
                """)
                card_data['image']['loaded'] = img_loaded
            
            # Get link
            link = card.locator('a').first
            if link.count() > 0:
                card_data['link'] = link.get_attribute('href') or ''
            
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
            
            print(f"      [OK] Card {index+1}: '{card_data['title'][:40]}'")
            print(f"              Category: {card_data['category']}")
            print(f"              Container: {card_data['container'].get('width', 0)}x{card_data['container'].get('height', 0)}")
            if card_data.get('image'):
                print(f"              Image: {card_data['image'].get('width', 0)}x{card_data['image'].get('height', 0)}")
            if card_data.get('link'):
                print(f"              Link: {card_data['link']}")
        
        except Exception as e:
            print(f"      [ERROR] Card {index+1} validation failed: {str(e)}")
        
        return card_data
    
    def _validate_chevrons(self, section) -> Dict:
        """Validate chevron navigation functionality"""
        chevron_data = {
            'left_exists': False,
            'right_exists': False,
            'left_disabled_initially': False,
            'right_disabled_at_end': False,
            'left_works': False,
            'right_works': False
        }
        
        try:
            # Find chevrons using splide classes
            left_chevron = section.locator('.splide__arrow--prev, button[aria-label*="Previous"]')
            right_chevron = section.locator('.splide__arrow--next, button[aria-label*="Next"]')
            
            chevron_data['left_exists'] = left_chevron.count() > 0
            chevron_data['right_exists'] = right_chevron.count() > 0
            
            if left_chevron.count() > 0 and right_chevron.count() > 0:
                print(f"   [OK] Both chevrons found")
                
                # Check if left is initially disabled
                left_disabled = left_chevron.first.get_attribute('disabled') is not None
                chevron_data['left_disabled_initially'] = left_disabled
                print(f"   [OK] Left chevron initially disabled: {left_disabled}")
                
                # Test right chevron (should move cards)
                cards = section.locator('.splide__slide')
                initial_positions = self._get_cards_positions(cards)
                
                right_chevron.first.click()
                self.page.wait_for_timeout(1000)
                
                new_positions = self._get_cards_positions(cards)
                
                if new_positions != initial_positions:
                    chevron_data['right_works'] = True
                    print(f"   [OK] Right chevron works - cards moved")
                    
                    # Verify left chevron can move back
                    left_chevron.first.click()
                    self.page.wait_for_timeout(1000)
                    
                    final_positions = self._get_cards_positions(cards)
                    
                    if final_positions != new_positions:
                        chevron_data['left_works'] = True
                        print(f"   [OK] Left chevron works - cards moved back")
                
                # Check if right is disabled by clicking a few times (limit to 5 clicks to avoid loop)
                clicks = 0
                max_clicks = 5
                while clicks < max_clicks:
                    right_disabled = right_chevron.first.get_attribute('disabled') is not None
                    if right_disabled:
                        chevron_data['right_disabled_at_end'] = True
                        print(f"   [OK] Right chevron correctly disabled at end")
                        break
                    right_chevron.first.click()
                    self.page.wait_for_timeout(500)
                    clicks += 1
        
        except Exception as e:
            print(f"   [ERROR] Chevron validation failed: {str(e)}")
        
        return chevron_data
    
    def _get_cards_positions(self, cards) -> List[Dict]:
        """Get positions of all cards"""
        try:
            positions = []
            for i in range(min(cards.count(), 6)):
                card = cards.nth(i)
                pos = card.evaluate("""
                    (card) => {
                        const rect = card.getBoundingClientRect();
                        return {
                            left: rect.left,
                            top: rect.top,
                            visible: rect.width > 0 && rect.height > 0
                        };
                    }
                """)
                positions.append(pos)
            return positions
        except:
            return []
    
    def _validate_hover_effect(self, section, card_count: int) -> Dict:
        """Validate hover effect on cards"""
        hover_data = {
            'hover_effect_detected': False,
            'focus_behavior': '',
            'is_clickable': False
        }
        
        try:
            if card_count == 0:
                return hover_data
            
            # Get first visible card
            cards = section.locator('.splide__slide.is-visible, .splide__slide.is-active')
            if cards.count() > 0:
                first_card = cards.first
                
                # Get initial styles
                initial_styles = first_card.evaluate("""
                    (card) => {
                        const styles = window.getComputedStyle(card);
                        return {
                            transform: styles.transform,
                            transition: styles.transition
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
                            transition: styles.transition
                        };
                    }
                """)
                
                # Check if styles changed
                if hovered_styles != initial_styles:
                    hover_data['hover_effect_detected'] = True
                    hover_data['focus_behavior'] = 'Card focuses on hover'
                    print(f"   [OK] Hover effect detected on cards")
                
                # Check if card is clickable
                link = first_card.locator('a')
                if link.count() > 0:
                    hover_data['is_clickable'] = True
                    print(f"   [OK] Card is clickable")
        
        except Exception as e:
            print(f"   [ERROR] Hover effect validation failed: {str(e)}")
        
        return hover_data
    
    def _validate_card_links(self, section, cards) -> Dict:
        """Validate all card links"""
        links_data = {
            'total_links': 0,
            'valid_links': 0,
            'invalid_links': 0,
            'link_details': []
        }
        
        try:
            for card in cards:
                link_url = card.get('link', '')
                if link_url:
                    links_data['total_links'] += 1
                    
                    # Validate link
                    try:
                        if link_url.startswith('/'):
                            full_url = self.page.evaluate(f"window.location.origin + '{link_url}'")
                        else:
                            full_url = link_url
                        
                        response = self.page.request.get(full_url, timeout=5000)
                        is_valid = 200 <= response.status < 400
                        
                        if is_valid:
                            links_data['valid_links'] += 1
                        else:
                            links_data['invalid_links'] += 1
                        
                        links_data['link_details'].append({
                            'url': link_url,
                            'status_code': response.status,
                            'is_valid': is_valid
                        })
                    except:
                        links_data['invalid_links'] += 1
            
            print(f"   [OK] Validated {links_data['total_links']} links")
            print(f"   [OK] Valid: {links_data['valid_links']}, Invalid: {links_data['invalid_links']}")
            
            links_data['all_links_valid'] = links_data['invalid_links'] == 0
        
        except Exception as e:
            print(f"   [ERROR] Link validation failed: {str(e)}")
        
        return links_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("ARTICLE LIST SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"Total Cards: {summary.get('total_cards', 0)}")
        print(f"Title Exists: {'Yes' if summary.get('title_exists') else 'No'}")
        print(f"View All Link Valid: {'Yes' if summary.get('view_all_link_valid') else 'No'}")
        print(f"Chevrons Working: {'Yes' if summary.get('chevrons_working') else 'No'}")
        print(f"Hover Working: {'Yes' if summary.get('hover_working') else 'No'}")
        print(f"All Links Valid: {'Yes' if summary.get('all_links_valid') else 'No'}")
        
        if results.get('title'):
            title = results['title']
            print(f"\nTitle: {title.get('text', '')}")
            print(f"  Font Size: {title.get('font_size', '')}")
            print(f"  Font Color: {title.get('font_color', '')}")
            if title.get('view_all_exists'):
                print(f"  View All: {title.get('view_all_text', '')} -> {title.get('view_all_href', '')}")

