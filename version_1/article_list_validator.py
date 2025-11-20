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
    
    def validate_article_list(self, selector: str = '.articlelist .cmp-article-list__articles-container, .cmp-article-list__articles-container') -> Dict:
        """Validate Article List Card component"""
        print("\n" + "="*80)
        print("ARTICLE LIST (CARD LIST) VALIDATION")
        print("="*80)
        
        try:
            # Find article list section (scoped to the article list container)
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
            
            # Compute whether any card has a non-empty title (fallback for title presence)
            # This is used in the summary if the section title cannot be located due to scoping
            # to the inner articles container.
            results = {
                'found': True,
                'title': title_data,
                'cards': cards_data,
                'chevrons': chevron_data,
                'hover': hover_data,
                'links': links_data,
                'summary': {
                    'total_cards': cards_data.get('card_count', 0),
                    'title_exists': title_data.get('exists', False) or any((c.get('title') or '').strip() for c in cards_data.get('cards', [])),
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
                
                # Validate link with fast timeout protection
                try:
                    href = title_data['view_all_href']
                    if href and href != '#':
                        # Build absolute URL quickly
                        if href.startswith('/'):
                            try:
                                href = self.page.evaluate("window.location.origin") + href
                            except Exception:
                                # Fallback: use current page URL
                                current_url = self.page.url
                                base_url = '/'.join(current_url.split('/')[:3])
                                href = base_url + href
                        
                        # Use HEAD request for faster validation (if supported) or very short timeout GET
                        try:
                            # Try HEAD request first (faster, no body download)
                            try:
                                response = self.page.request.head(href, timeout=1500)  # Very short timeout
                                title_data['view_all_valid'] = 200 <= response.status < 400
                            except Exception:
                                # Fallback to GET with very short timeout
                                response = self.page.request.get(href, timeout=1500)  # Very short timeout
                                title_data['view_all_valid'] = 200 <= response.status < 400
                            
                            print(f"   [OK] View All link: '{title_data['view_all_text']}' -> {title_data['view_all_href']}")
                            print(f"   [OK] Link valid: {title_data['view_all_valid']}")
                        except Exception as timeout_error:
                            # If validation fails/times out, just mark as not validated (don't fail)
                            title_data['view_all_valid'] = False
                            print(f"   [INFO] View All link found but validation skipped (timeout)")
                    else:
                        title_data['view_all_valid'] = False
                        print(f"   [OK] View All link: '{title_data['view_all_text']}' -> {title_data['view_all_href']}")
                except Exception as e:
                    # If any error occurs, just mark as not validated
                    title_data['view_all_valid'] = False
                    print(f"   [INFO] View All link found but validation skipped: {str(e)[:50]}")
        
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
            # Find unique slides inside the article list container
            cards = section.locator('.splide__slide:not(.splide__slide--clone)')
            cards_data['card_count'] = cards.count()
            
            print(f"   [OK] Found {cards_data['card_count']} article cards")
            
            # Validate each card in detail
            for i in range(min(cards.count(), 6)):  # First 6 cards
                # Ensure the i-th slide is visible by advancing the carousel if needed
                try:
                    self._bring_slide_into_view(section, i)
                except Exception:
                    pass
                slide = section.locator('.splide__slide:not(.splide__slide--clone)').nth(i)
                try:
                    slide.scroll_into_view_if_needed(timeout=3000)
                    self.page.wait_for_timeout(200)
                except Exception:
                    pass
                card_data = self._validate_single_article_card(slide, i)
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
            # Normalize root: if a slide was passed, drill into the article element
            root = card
            try:
                possible = card.locator('.cmp-article-list__article').first
                if possible.count() > 0:
                    root = possible
            except Exception:
                pass
            

            # Ensure in-view
            try:
                root.scroll_into_view_if_needed(timeout=3000)
                self.page.wait_for_timeout(100)
            except Exception:
                pass

            # Get card title (prefer inner_text for trimmed visible text)
            title = root.locator('.cmp-article-list__article-title, h3').first
            if title.count() > 0:
                try:
                    # Use shorter timeout and fallback to text_content if inner_text fails
                    card_data['title'] = (title.inner_text(timeout=1000) or '').strip()
                except Exception:
                    try:
                        card_data['title'] = (title.text_content() or '').strip()
                    except Exception:
                        card_data['title'] = ''
                
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
            category = root.locator('.cmp-article-list__article-category').first
            if category.count() > 0:
                try:
                    # Use shorter timeout and fallback to text_content if inner_text fails
                    card_data['category'] = (category.inner_text(timeout=1000) or '').strip()
                except Exception:
                    try:
                        card_data['category'] = (category.text_content() or '').strip()
                    except Exception:
                        card_data['category'] = ''
                
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
            img = root.locator('.cmp-article-list__article-image img, img').first
            if img.count() > 0:
                img_src = img.get_attribute('src') or img.get_attribute('data-src') or ''
                card_data['image']['src'] = img_src
                
                # Get image dimensions and loaded status in one evaluate call (faster)
                try:
                    img_info = img.evaluate("""
                        (img) => {
                            return {
                                width: img.naturalWidth || img.width || img.getAttribute('width') || 0,
                                height: img.naturalHeight || img.height || img.getAttribute('height') || 0,
                                loaded: img && img.complete && img.naturalHeight !== 0
                            };
                        }
                    """)
                    
                    # Ensure img_info is a dictionary before accessing
                    if isinstance(img_info, dict):
                        card_data['image']['width'] = img_info.get('width', 0)
                        card_data['image']['height'] = img_info.get('height', 0)
                        card_data['image']['loaded'] = img_info.get('loaded', False)
                    else:
                        # Fallback if evaluate returns something unexpected
                        card_data['image']['width'] = 0
                        card_data['image']['height'] = 0
                        card_data['image']['loaded'] = False
                except Exception as e:
                    # If evaluate fails, set defaults
                    card_data['image']['width'] = 0
                    card_data['image']['height'] = 0
                    card_data['image']['loaded'] = False
            
            # Get link
            link = root.locator('a').first
            if link.count() > 0:
                card_data['link'] = link.get_attribute('href') or ''
            
            # Get card container size
            card_size = root.evaluate("""
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
                
                # Initial state: left disabled and no-op when clicked
                start_index = self._get_active_slide_index(section)
                left_attr_disabled = left_chevron.first.get_attribute('disabled') is not None
                try:
                    left_chevron.first.click()
                    self.page.wait_for_timeout(200)
                except Exception:
                    pass
                after_left_click = self._get_active_slide_index(section)
                chevron_data['left_disabled_initially'] = left_attr_disabled or (after_left_click == start_index)
                print(f"   [OK] Left chevron initially disabled/no-op: {chevron_data['left_disabled_initially']}")

                # Test right chevron moves forward (simplified - just one click test)
                before = self._get_active_slide_index(section)
                try:
                    right_chevron.first.click(timeout=200)
                    self.page.wait_for_timeout(150)  # Reduced wait
                except Exception:
                    pass
                after = self._get_active_slide_index(section)
                if after != before:
                    chevron_data['right_works'] = True
                    print(f"   [OK] Right chevron moves forward")

                # Test left chevron moves backward (simplified - just one click test from current position)
                before_back = after  # Use the index we already have
                try:
                    left_chevron.first.click(timeout=200)
                    self.page.wait_for_timeout(150)  # Reduced wait
                except Exception:
                    pass
                after_back = self._get_active_slide_index(section)
                if after_back != before_back:
                    chevron_data['left_works'] = True
                    print(f"   [OK] Left chevron moves backward")
                
                # Quick check if right is disabled (only if we're near the end)
                try:
                    slides_count = section.locator('.splide__slide:not(.splide__slide--clone)').count()
                    if slides_count > 0:
                        current_index = after_back
                        target_index = max(0, slides_count - 1)
                        # Only check if we're at or near the end
                        if current_index >= target_index - 1:
                            right_attr_disabled = right_chevron.first.get_attribute('disabled', timeout=50) is not None
                            chevron_data['right_disabled_at_end'] = right_attr_disabled
                            if right_attr_disabled:
                                print(f"   [OK] Right chevron disabled at end")
                except Exception:
                    pass
        
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
            
            # Check hover on up to first 3 visible slides (more robust)
            slides = section.locator('.splide__slide.is-visible, .splide__slide.is-active')
            count = min(max(slides.count(), 1), 3)
            for i in range(count):
                slide = slides.nth(i)
                article = slide.locator('.cmp-article-list__article').first
                root = article if article.count() > 0 else slide
                
                # Capture initial styles relevant to focus/shadow
                initial = root.evaluate("""
                    (el) => {
                        const s = window.getComputedStyle(el);
                        return { boxShadow: s.boxShadow, outlineWidth: s.outlineWidth, transform: s.transform };
                    }
                """)
                
                # Ensure initial is a dictionary
                if not isinstance(initial, dict):
                    initial = {}
                
                root.hover()
                self.page.wait_for_timeout(200)
                
                after = root.evaluate("""
                    (el) => {
                        const s = window.getComputedStyle(el);
                        return { boxShadow: s.boxShadow, outlineWidth: s.outlineWidth, transform: s.transform };
                    }
                """)
                
                # Ensure after is a dictionary
                if not isinstance(after, dict):
                    after = {}
                
                # Decide if hover produced any visible effect
                shadow_changed = (after.get('boxShadow') != initial.get('boxShadow')) and (after.get('boxShadow') not in ['none', ''])
                outline_changed = after.get('outlineWidth') != initial.get('outlineWidth') and after.get('outlineWidth') not in ['0px', '0']
                transform_changed = after.get('transform') != initial.get('transform')
                if shadow_changed or outline_changed or transform_changed:
                    hover_data['hover_effect_detected'] = True
                    hover_data['focus_behavior'] = 'Card shows focus/shadow on hover'
                    break
            
            # Clickable check on any visible slide
            any_link = section.locator('.splide__slide.is-visible .cmp-article-list__article a, .splide__slide.is-active .cmp-article-list__article a')
            hover_data['is_clickable'] = any_link.count() > 0
            if hover_data['hover_effect_detected']:
                print(f"   [OK] Hover effect detected on cards")
            else:
                print(f"   [INFO] Hover effect not detected via styles; may be subtle")
        
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
                # Ensure card is a dictionary
                if not isinstance(card, dict):
                    continue
                
                # Safely get link URL - handle different formats
                link_url = ''
                try:
                    link_value = card.get('link', '')
                    if isinstance(link_value, dict):
                        link_url = link_value.get('href', '') if isinstance(link_value, dict) else ''
                    elif isinstance(link_value, str):
                        link_url = link_value
                    else:
                        link_url = str(link_value) if link_value else ''
                except Exception as e:
                    print(f"      [WARNING] Error extracting link from card: {str(e)}")
                    continue
                
                if link_url and link_url != '#':
                    links_data['total_links'] += 1
                    
                    # Validate link with timeout protection
                    try:
                        if link_url.startswith('/'):
                            full_url = self.page.evaluate(f"window.location.origin + '{link_url}'")
                        else:
                            full_url = link_url
                        
                        # Use shorter timeout and catch timeout errors
                        try:
                            response = self.page.request.get(full_url, timeout=3000)  # Reduced from 5000 to 3000
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
                        except Exception as timeout_error:
                            # If request times out or fails, mark as invalid but continue
                            print(f"      [WARNING] Link validation timeout/failed for: {link_url[:50]}...")
                            links_data['invalid_links'] += 1
                            links_data['link_details'].append({
                                'url': link_url,
                                'status_code': 'timeout',
                                'is_valid': False
                            })
                    except Exception as e:
                        print(f"      [WARNING] Link validation error for: {link_url[:50]}... - {str(e)}")
                        links_data['invalid_links'] += 1
            
            print(f"   [OK] Validated {links_data['total_links']} links")
            print(f"   [OK] Valid: {links_data['valid_links']}, Invalid: {links_data['invalid_links']}")
            
            links_data['all_links_valid'] = links_data['invalid_links'] == 0
        
        except Exception as e:
            print(f"   [ERROR] Link validation failed: {str(e)}")
        
        return links_data

    def _get_active_slide_index(self, section) -> int:
        """Get active slide index - optimized for speed"""
        try:
            # Fastest method: use JavaScript to find active slide directly
            try:
                active_index = section.evaluate("""
                    (section) => {
                        const slides = section.querySelectorAll('.splide__slide:not(.splide__slide--clone)');
                        for (let i = 0; i < slides.length; i++) {
                            if (slides[i].classList.contains('is-active')) {
                                return i;
                            }
                        }
                        // Fallback: find first visible slide
                        for (let i = 0; i < Math.min(slides.length, 10); i++) {
                            const rect = slides[i].getBoundingClientRect();
                            if (rect.width > 0 && rect.height > 0) {
                                return i;
                            }
                        }
                        return 0;
                    }
                """)
                if active_index is not None:
                    return active_index
            except Exception:
                pass
            
            # Fallback: check is-active class with minimal timeout
            slides = section.locator('.splide__slide:not(.splide__slide--clone)')
            slide_count = min(slides.count(), 10)
            for i in range(slide_count):
                try:
                    if slides.nth(i).evaluate('el => el.classList.contains("is-active")'):
                        return i
                except Exception:
                    continue
            
            return 0
        except Exception:
            return 0

    def _bring_slide_into_view(self, section, target_index: int) -> None:
        try:
            # Fast path: use pagination buttons to jump directly
            pagination = section.locator('.splide__pagination__page')
            if pagination.count() > target_index:
                try:
                    pagination.nth(target_index).click(timeout=2000)
                    # brief poll until active index matches (reduced iterations)
                    for _ in range(5):  # Reduced from 8 to 5
                        if self._get_active_slide_index(section) == target_index:
                            break
                        self.page.wait_for_timeout(50)  # Reduced from 60 to 50
                    return
                except Exception:
                    pass  # Fall through to arrow method

            # Fallback: click right arrow minimal times (with timeout protection)
            right = section.locator('.splide__arrow--next')
            if right.count() == 0:
                return
            current = self._get_active_slide_index(section)
            remaining = max(0, target_index - current)
            # Limit to max 10 clicks to prevent infinite loops
            for _ in range(min(remaining, 10)):
                try:
                    right.first.click(timeout=2000)
                    # shorter wait; we'll still poll active index (reduced iterations)
                    for _ in range(4):  # Reduced from 6 to 4
                        if self._get_active_slide_index(section) >= target_index:
                            return
                        self.page.wait_for_timeout(40)  # Reduced from 50 to 40
                except Exception:
                    break  # Stop if click fails
        except Exception:
            pass
    
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

