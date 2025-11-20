"""
Carousel Component Validator for Solidigm Website
Validates carousel components including images, text, buttons, navigation, and progress bar
"""
import time
from typing import Dict, List
from urllib.parse import urljoin
from playwright.sync_api import Page


class CarouselValidator:
    def __init__(self, page: Page):
        self.page = page
        self.validation_results = {
            'carousel_count': 0,
            'carousels': [],
            'links': [],
            'images': [],
            'texts': [],
            'buttons': [],
            'navigation': {},
            'progress_bar': {},
            'font_styles': []
        }
    
    def validate_carousel(self, selector: str = '.splide:has(.cmp-hero), .cmp-carousel:has(.cmp-hero), .hero-carousel') -> Dict:
        """Validate main hero carousel component only (4 cards)"""
        print("\n" + "="*80)
        print("HERO CAROUSEL VALIDATION (4 CARDS)")
        print("="*80)
        
        try:
            # Find carousel elements
            carousels = self.page.locator(selector)
            count = carousels.count()
            
            print(f"\n[HERO CAROUSEL] Found {count} hero carousel component(s)")
            
            if count == 0:
                print("[WARNING] No hero carousel found on page")
                print("[INFO] Looking for alternative selectors...")
                # Try alternative selectors
                alt_selectors = [
                    '.splide',
                    '.cmp-carousel', 
                    '[class*="carousel"]'
                ]
                for alt_selector in alt_selectors:
                    alt_carousels = self.page.locator(alt_selector)
                    alt_count = alt_carousels.count()
                    if alt_count > 0:
                        print(f"[INFO] Found {alt_count} carousel(s) with selector: {alt_selector}")
                        # Check if any contain hero content
                        for i in range(alt_count):
                            carousel = alt_carousels.nth(i)
                            hero_content = carousel.locator('.cmp-hero, .hero')
                            if hero_content.count() > 0:
                                print(f"[INFO] Carousel {i+1} contains hero content - this is likely the main carousel")
                                # Use this carousel
                                carousel_data = self._validate_single_carousel(carousel, 0)
                                self.validation_results['carousels'].append(carousel_data)
                                self.validation_results['carousel_count'] = 1
                                self._print_summary()
                                return self.validation_results
                return self.validation_results
            
            # Validate only the first hero carousel (should be the main one)
            carousel = carousels.first
            # Scroll into view for viewer context
            try:
                carousel.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except Exception:
                pass
            print(f"\n[INFO] Validating main hero carousel...")
            
            carousel_data = self._validate_single_carousel(carousel, 0)
            self.validation_results['carousels'].append(carousel_data)
            
            self.validation_results['carousel_count'] = 1  # Only main hero carousel
            
            # Print summary
            self._print_summary()
            
            return self.validation_results
            
        except Exception as e:
            print(f"[ERROR] Carousel validation failed: {str(e)}")
            return {'error': str(e)}
    
    def _validate_single_carousel(self, carousel, index: int) -> Dict:
        """Validate a single carousel component"""
        carousel_data = {
            'index': index + 1,
            'slides': [],
            'navigation': {},
            'images': [],
            'links': [],
            'texts': [],
            'buttons': [],
            'font_styles': [],
            'container': {},
            'progress_bar': {}
        }
        
        try:
            # 0. Get carousel title (e.g., "Featured Products")
            title_data = self._get_carousel_title(carousel)
            carousel_data['title'] = title_data
            if title_data.get('text'):
                print(f"   [TITLE] {title_data.get('text')} - Font: {title_data.get('font_size', '')}, Color: {title_data.get('font_color', '')}")
            
            # 1. Get container size
            container_info = self._get_container_size(carousel)
            carousel_data['container'] = container_info
            print(f"   [CONTAINER] Size: {container_info.get('width', 0)}x{container_info.get('height', 0)}")
            
            # 2. Count unique slides (excluding clones) - use pagination count as source of truth
            pagination_buttons = carousel.locator('.splide__pagination__page')
            pagination_count = pagination_buttons.count()
            
            # Also count actual slides for verification
            all_slides = carousel.locator('.splide__slide')
            unique_slides = carousel.locator('.splide__slide:not(.splide__slide--clone)')
            unique_slide_count = unique_slides.count()
            
            # Use pagination count as the definitive count (should match unique slides)
            actual_card_count = pagination_count if pagination_count > 0 else unique_slide_count
            carousel_data['slide_count'] = actual_card_count
            carousel_data['total_slides_including_clones'] = all_slides.count()
            carousel_data['pagination_count'] = pagination_count
            carousel_data['unique_slide_count'] = unique_slide_count
            
            print(f"   [SLIDES] Cards: {actual_card_count} (Pagination: {pagination_count}, Unique slides: {unique_slide_count}, Total with clones: {all_slides.count()})")
            
            # 3. Validate unique slides only (limit to actual card count)
            for slide_idx in range(min(actual_card_count, unique_slide_count)):
                slide = unique_slides.nth(slide_idx)
                slide_data = self._validate_slide(slide, slide_idx)
                
                # Check if image fits container (compare image size with container size)
                if slide_data.get('image_width') and slide_data.get('image_height'):
                    container_width = container_info.get('width', 0)
                    container_height = container_info.get('height', 0)
                    img_width = slide_data.get('image_width', 0)
                    img_height = slide_data.get('image_height', 0)
                    
                    # Check if image dimensions match or are close to container (within 10% tolerance)
                    width_fit = abs(img_width - container_width) / max(container_width, 1) <= 0.1 if container_width > 0 else False
                    height_fit = abs(img_height - container_height) / max(container_height, 1) <= 0.1 if container_height > 0 else False
                    
                    slide_data['image_fits_container'] = width_fit and height_fit
                    slide_data['container_size'] = {'width': container_width, 'height': container_height}
                else:
                    slide_data['image_fits_container'] = None  # Unknown
                
                carousel_data['slides'].append(slide_data)
                print(f"      Card {slide_idx+1}/{actual_card_count}: {slide_data.get('title', '')[:50]}")
            
            # 4. Validate navigation (chevrons)
            navigation = self._validate_navigation(carousel)
            carousel_data['navigation'] = navigation
            
            # 5. Validate progress bar
            progress_bar = self._validate_progress_bar(carousel)
            carousel_data['progress_bar'] = progress_bar
            
            # 6. Get font styles
            font_styles = self._get_font_styles(carousel)
            carousel_data['font_styles'] = font_styles
            
        except Exception as e:
            print(f"   [ERROR] Failed to validate carousel: {str(e)}")
            carousel_data['error'] = str(e)
        
        return carousel_data
    
    def _validate_slide(self, slide, index: int) -> Dict:
        """Validate a single slide"""
        slide_data = {
            'index': index + 1,
            'title': '',
            'description': '',
            'background_image': '',
            'background_image_present': False,
            'button_count': 0,
            'links': [],
            'buttons': []
        }
        
        try:
            # Get title with font styles
            title_element = slide.locator('.cmp-hero__title, h1, h2, h3, .title, [class*="title"]').first
            if title_element.count() > 0:
                slide_data['title'] = title_element.text_content() or ''
                print(f"      Card {index+1} - Title: {slide_data['title'][:50]}")
                
                # Get title font styles
                try:
                    title_font = title_element.evaluate("""
                        (el) => {
                            const styles = window.getComputedStyle(el);
                            return {
                                fontSize: styles.fontSize,
                                color: styles.color,
                                fontFamily: styles.fontFamily,
                                fontWeight: styles.fontWeight,
                                lineHeight: styles.lineHeight
                            };
                        }
                    """)
                    if title_font:
                        slide_data['title_font'] = {
                            'fontSize': title_font.get('fontSize', ''),
                            'color': title_font.get('color', ''),
                            'fontFamily': title_font.get('fontFamily', ''),
                            'fontWeight': title_font.get('fontWeight', ''),
                            'lineHeight': title_font.get('lineHeight', '')
                        }
                except Exception:
                    pass
            
            # Get description with font styles
            desc_element = slide.locator('.cmp-hero__description p, .cmp-hero__description, p, .description, [class*="description"]').first
            if desc_element.count() > 0:
                slide_data['description'] = desc_element.text_content() or ''
                print(f"      Card {index+1} - Description: {slide_data['description'][:80]}")
                
                # Get description font styles
                try:
                    desc_font = desc_element.evaluate("""
                        (el) => {
                            const styles = window.getComputedStyle(el);
                            return {
                                fontSize: styles.fontSize,
                                color: styles.color,
                                fontFamily: styles.fontFamily,
                                fontWeight: styles.fontWeight,
                                lineHeight: styles.lineHeight
                            };
                        }
                    """)
                    if desc_font:
                        slide_data['description_font'] = {
                            'fontSize': desc_font.get('fontSize', ''),
                            'color': desc_font.get('color', ''),
                            'fontFamily': desc_font.get('fontFamily', ''),
                            'fontWeight': desc_font.get('fontWeight', ''),
                            'lineHeight': desc_font.get('lineHeight', '')
                        }
                except Exception:
                    pass
            
            # Get background image from img tags (hero background images)
            bg_images = slide.locator('.cmp-hero__background-image img, .hero img')
            bg_image_urls = []
            
            for i in range(bg_images.count()):
                img = bg_images.nth(i)
                src = img.get_attribute('src') or ''
                if src:
                    bg_image_urls.append(src)
            
            # Also check CSS background-image as fallback
            css_bg_image = slide.evaluate("""
                (slide) => {
                    const styles = window.getComputedStyle(slide);
                    const bgImage = styles.backgroundImage;
                    if (bgImage && bgImage !== 'none') {
                        const match = bgImage.match(/url\\(['"]?(.*?)['"]?\\)/);
                        return match ? match[1] : '';
                    }
                    return '';
                }
            """)
            
            if css_bg_image:
                bg_image_urls.append(css_bg_image)
            
            slide_data['background_image'] = bg_image_urls[0] if bg_image_urls else ''
            slide_data['background_images'] = bg_image_urls
            slide_data['background_image_present'] = len(bg_image_urls) > 0
            
            if bg_image_urls:
                print(f"      Card {index+1} - Background Image: Present ({bg_image_urls[0][:60]})")
                if len(bg_image_urls) > 1:
                    print(f"      Card {index+1} - Additional images: {len(bg_image_urls)-1} more")
            else:
                print(f"      Card {index+1} - Background Image: NOT FOUND")
            
            # Get regular images (hero background images) with dimensions
            images = slide.locator('.cmp-hero__background-image img, img')
            if images.count() > 0:
                img = images.first
                src = img.get_attribute('src') or img.get_attribute('data-src') or ''
                slide_data['main_image'] = src
                slide_data['image_url'] = src  # For report
                
                # Get image dimensions and check if it loads
                try:
                    img_info = img.evaluate("""
                        (img) => {
                            return {
                                width: img.naturalWidth || img.width || 0,
                                height: img.naturalHeight || img.height || 0,
                                loaded: img.complete && img.naturalHeight !== 0,
                                src: img.src || img.getAttribute('data-src') || ''
                            };
                        }
                    """)
                    if img_info:
                        slide_data['image_width'] = int(img_info.get('width', 0))
                        slide_data['image_height'] = int(img_info.get('height', 0))
                        slide_data['image_loaded'] = bool(img_info.get('loaded', False))
                except:
                    # Fallback to attributes
                    try:
                        width_attr = img.get_attribute('width')
                        height_attr = img.get_attribute('height')
                        if width_attr:
                            slide_data['image_width'] = int(width_attr)
                        if height_attr:
                            slide_data['image_height'] = int(height_attr)
                    except:
                        pass
                    slide_data['image_loaded'] = False
            
            # Get and validate buttons with click testing
            buttons = slide.locator('.solidigm-btn, .cmp-hero__cta-container a, button, [class*="button"], .btn, a[class*="btn"]')
            button_count = buttons.count()
            slide_data['button_count'] = button_count
            
            print(f"      Card {index+1} - Button Count: {button_count}")
            
            for i in range(min(button_count, 2)):  # Test max 2 buttons per card
                btn = buttons.nth(i)
                text = btn.text_content() or ''
                href = btn.get_attribute('href') or ''
                is_visible = btn.is_visible()
                is_enabled = btn.is_enabled() if btn.get_attribute('disabled') is None else False
                
                # Get button font styles
                font_styles = {}
                try:
                    btn_styles = btn.evaluate("""
                        (btn) => {
                            const styles = window.getComputedStyle(btn);
                            return {
                                fontSize: styles.fontSize,
                                fontFamily: styles.fontFamily,
                                fontWeight: styles.fontWeight,
                                color: styles.color,
                                backgroundColor: styles.backgroundColor,
                                lineHeight: styles.lineHeight
                            };
                        }
                    """)
                    if btn_styles:
                        font_styles = {
                            'fontSize': btn_styles.get('fontSize', ''),
                            'fontFamily': btn_styles.get('fontFamily', ''),
                            'fontWeight': btn_styles.get('fontWeight', ''),
                            'color': btn_styles.get('color', ''),
                            'backgroundColor': btn_styles.get('backgroundColor', ''),
                            'lineHeight': btn_styles.get('lineHeight', '')
                        }
                except Exception:
                    pass
                
                button_data = {
                    'text': text[:50],
                    'href': href,
                    'is_visible': is_visible,
                    'is_enabled': is_enabled,
                    'click_tested': False,
                    'navigates_correctly': False,
                    'font_styles': font_styles
                }

                # Validate button link (HTTP status)
                try:
                    if href and href != '#':
                        # Resolve relative URLs against current page URL
                        absolute_href = href if href.startswith('http') else urljoin(self.page.url, href)
                        response = self.page.request.get(absolute_href, timeout=5000)
                        # store both forms
                        button_data['href_absolute'] = absolute_href
                        try:
                            from urllib.parse import urlparse
                            parsed = urlparse(absolute_href)
                            rel = parsed.path or '/'
                            if parsed.query:
                                rel += f"?{parsed.query}"
                        except Exception:
                            rel = href
                        button_data['href'] = rel
                        button_data['status_code'] = response.status
                        button_data['is_valid'] = 200 <= response.status < 400
                    else:
                        button_data['status_code'] = 0
                        button_data['is_valid'] = False
                except Exception as _e:
                    button_data['status_code'] = 0
                    button_data['is_valid'] = False
                
                # Test button click and navigation
                if is_visible and is_enabled:
                    try:
                        # Get current URL before click
                        current_url = self.page.url
                        
                        # Scroll to button if needed
                        btn.scroll_into_view_if_needed(timeout=5000)
                        time.sleep(0.5)
                        
                        # Click button
                        btn.click(timeout=5000)
                        time.sleep(1)  # Wait for navigation
                        
                        # Check if URL changed (navigation occurred)
                        new_url = self.page.url
                        navigation_occurred = new_url != current_url
                        
                        button_data['click_tested'] = True
                        button_data['navigates_correctly'] = navigation_occurred
                        button_data['original_url'] = current_url
                        button_data['new_url'] = new_url
                        
                        if navigation_occurred:
                            print(f"      Card {index+1} - Button {i+1} clicked: Navigated from {current_url} to {new_url}")
                        else:
                            print(f"      Card {index+1} - Button {i+1} clicked: No navigation occurred")
                        
                        # Store navigation details
                        button_data['navigation_details'] = {
                            'original_url': current_url,
                            'new_url': new_url,
                            'navigation_occurred': navigation_occurred
                        }
                        
                        # Go back to original page if navigated
                        if navigation_occurred:
                            self.page.go_back(wait_until='load', timeout=10000)
                            time.sleep(1)
                        
                    except Exception as e:
                        print(f"      Card {index+1} - Button {i+1} click test failed: {str(e)}")
                        button_data['error'] = str(e)
                
                slide_data['buttons'].append(button_data)
            
            # Also check links (some buttons might be implemented as links)
            links = slide.locator('a[href], button a')
            for i in range(min(links.count(), 5)):
                link = links.nth(i)
                href = link.get_attribute('href') or ''
                text = link.text_content() or ''
                
                if href and href != '#' and href != '':
                    # Validate link
                    try:
                        response = self.page.request.get(href, timeout=5000)
                        is_valid = 200 <= response.status < 400
                        slide_data['links'].append({
                            'text': text[:50],
                            'href': href,
                            'status_code': response.status,
                            'is_valid': is_valid
                        })
                    except:
                        slide_data['links'].append({
                            'text': text[:50],
                            'href': href,
                            'status_code': 0,
                            'is_valid': False
                        })
            
        except Exception as e:
            print(f"      [ERROR] Card {index+1} validation failed: {str(e)}")
            slide_data['error'] = str(e)
        
        return slide_data
    
    def _validate_navigation(self, carousel) -> Dict:
        """Validate navigation controls (left/right chevrons) with functionality testing"""
        navigation = {
            'has_left_chevron': False,
            'has_right_chevron': False,
            'left_chevron_visible': False,
            'right_chevron_visible': False,
            'left_clicks_tested': 0,
            'right_clicks_tested': 0,
            'left_clicks_successful': 0,
            'right_clicks_successful': 0,
            'test_details': []
        }
        
        try:
            # Find chevron buttons using Splide selectors
            left_chevron = carousel.locator('.splide__arrow--prev, [class*="prev"], [class*="left"], [aria-label*="prev"], [aria-label*="left"], .chevron-left')
            right_chevron = carousel.locator('.splide__arrow--next, [class*="next"], [class*="right"], [aria-label*="next"], [aria-label*="right"], .chevron-right')
            
            navigation['has_left_chevron'] = left_chevron.count() > 0
            navigation['has_right_chevron'] = right_chevron.count() > 0
            
            if left_chevron.count() > 0:
                navigation['left_chevron_visible'] = left_chevron.first.is_visible()
            
            if right_chevron.count() > 0:
                navigation['right_chevron_visible'] = right_chevron.first.is_visible()
            
            print(f"   [NAVIGATION] Left: {navigation['left_chevron_visible']}, Right: {navigation['right_chevron_visible']}")
            
            # Test chevron functionality with pagination tracking
            if navigation['left_chevron_visible'] or navigation['right_chevron_visible']:
                print(f"   [TESTING] Testing chevron functionality with pagination tracking...")
                
                # Test right chevron with 2 clicks
                if navigation['right_chevron_visible']:
                    print(f"   [TESTING] Testing right chevron...")
                    try:
                        right_btn = right_chevron.first
                        
                        # Test 2 clicks on right chevron
                        for click_num in range(1, 3):
                            right_btn.scroll_into_view_if_needed(timeout=5000)
                            time.sleep(0.3)
                            
                            # Get state before click
                            before_slide = self._get_active_slide_index(carousel)
                            before_pagination = self._get_active_pagination_index(carousel)
                            
                            right_btn.click(timeout=5000)
                            time.sleep(0.8)  # Wait for animation
                            
                            # Get state after click
                            after_slide = self._get_active_slide_index(carousel)
                            after_pagination = self._get_active_pagination_index(carousel)
                            
                            navigation['right_clicks_tested'] += 1
                            
                            # Check if both slide and pagination changed
                            slide_changed = after_slide != before_slide
                            pagination_changed = after_pagination != before_pagination
                            both_changed = slide_changed and pagination_changed
                            
                            if both_changed:
                                navigation['right_clicks_successful'] += 1
                                navigation['test_details'].append({
                                    'chevron': 'right',
                                    'click': click_num,
                                    'before_slide': before_slide,
                                    'after_slide': after_slide,
                                    'before_pagination': before_pagination,
                                    'after_pagination': after_pagination,
                                    'success': True
                                })
                                print(f"   [SUCCESS] Right click {click_num}: Slide {before_slide}→{after_slide}, Pagination {before_pagination}→{after_pagination}")
                            else:
                                navigation['test_details'].append({
                                    'chevron': 'right',
                                    'click': click_num,
                                    'before_slide': before_slide,
                                    'after_slide': after_slide,
                                    'before_pagination': before_pagination,
                                    'after_pagination': after_pagination,
                                    'success': False
                                })
                                print(f"   [FAIL] Right click {click_num}: Slide {before_slide}→{after_slide}, Pagination {before_pagination}→{after_pagination} (mismatch)")
                    
                    except Exception as e:
                        print(f"   [ERROR] Right chevron testing failed: {str(e)}")
                
                # Test left chevron with 2 clicks
                if navigation['left_chevron_visible']:
                    print(f"   [TESTING] Testing left chevron...")
                    try:
                        left_btn = left_chevron.first
                        
                        # Test 2 clicks on left chevron
                        for click_num in range(1, 3):
                            left_btn.scroll_into_view_if_needed(timeout=5000)
                            time.sleep(0.3)
                            
                            # Get state before click
                            before_slide = self._get_active_slide_index(carousel)
                            before_pagination = self._get_active_pagination_index(carousel)
                            
                            left_btn.click(timeout=5000)
                            time.sleep(0.8)  # Wait for animation
                            
                            # Get state after click
                            after_slide = self._get_active_slide_index(carousel)
                            after_pagination = self._get_active_pagination_index(carousel)
                            
                            navigation['left_clicks_tested'] += 1
                            
                            # Check if both slide and pagination changed
                            slide_changed = after_slide != before_slide
                            pagination_changed = after_pagination != before_pagination
                            both_changed = slide_changed and pagination_changed
                            
                            if both_changed:
                                navigation['left_clicks_successful'] += 1
                                navigation['test_details'].append({
                                    'chevron': 'left',
                                    'click': click_num,
                                    'before_slide': before_slide,
                                    'after_slide': after_slide,
                                    'before_pagination': before_pagination,
                                    'after_pagination': after_pagination,
                                    'success': True
                                })
                                print(f"   [SUCCESS] Left click {click_num}: Slide {before_slide}→{after_slide}, Pagination {before_pagination}→{after_pagination}")
                            else:
                                navigation['test_details'].append({
                                    'chevron': 'left',
                                    'click': click_num,
                                    'before_slide': before_slide,
                                    'after_slide': after_slide,
                                    'before_pagination': before_pagination,
                                    'after_pagination': after_pagination,
                                    'success': False
                                })
                                print(f"   [FAIL] Left click {click_num}: Slide {before_slide}→{after_slide}, Pagination {before_pagination}→{after_pagination} (mismatch)")
                    
                    except Exception as e:
                        print(f"   [ERROR] Left chevron testing failed: {str(e)}")
            
            # Print summary
            print(f"   [SUMMARY] Left chevron: {navigation['left_clicks_successful']}/{navigation['left_clicks_tested']} clicks successful")
            print(f"   [SUMMARY] Right chevron: {navigation['right_clicks_successful']}/{navigation['right_clicks_tested']} clicks successful")
            
        except Exception as e:
            print(f"   [ERROR] Navigation validation failed: {str(e)}")
        
        return navigation
    
    def _get_active_slide_index(self, carousel) -> int:
        """Get the index of the currently active slide"""
        try:
            # Method 1: Check for Splide active slide
            active_slides = carousel.locator('.splide__slide.is-active, .splide__slide.is-visible')
            if active_slides.count() > 0:
                # Get the slide index from the active slide
                active_slide = active_slides.first
                slide_id = active_slide.get_attribute('id') or ''
                if 'slide' in slide_id:
                    try:
                        # Extract slide number from ID like "carousel-xxx-slide02"
                        slide_num = int(slide_id.split('slide')[-1]) - 1
                        return slide_num
                    except:
                        pass
            
            # Method 2: Check pagination active state
            active_pagination = carousel.locator('.splide__pagination__page.is-active')
            if active_pagination.count() > 0:
                pagination_btn = active_pagination.first
                aria_label = pagination_btn.get_attribute('aria-label') or ''
                if 'slide' in aria_label.lower():
                    try:
                        # Extract slide number from aria-label like "Go to slide 2"
                        slide_num = int(aria_label.split()[-1]) - 1
                        return slide_num
                    except:
                        pass
            
            # Method 3: Check visibility of unique slides
            unique_slides = carousel.locator('.splide__slide:not(.splide__slide--clone)')
            for i in range(unique_slides.count()):
                slide = unique_slides.nth(i)
                if slide.is_visible(timeout=1000):
                    return i
            
            return 0
        except:
            return 0
    
    def _get_active_pagination_index(self, carousel) -> int:
        """Get the index of the currently active pagination button"""
        try:
            # Find active pagination button
            active_pagination = carousel.locator('.splide__pagination__page.is-active')
            if active_pagination.count() > 0:
                # Get all pagination buttons to find index
                all_pagination = carousel.locator('.splide__pagination__page')
                for i in range(all_pagination.count()):
                    if all_pagination.nth(i).get_attribute('class') and 'is-active' in all_pagination.nth(i).get_attribute('class'):
                        return i
            
            # Fallback: check aria-label
            active_pagination = carousel.locator('.splide__pagination__page.is-active')
            if active_pagination.count() > 0:
                aria_label = active_pagination.first.get_attribute('aria-label') or ''
                if 'slide' in aria_label.lower():
                    try:
                        # Extract slide number from aria-label like "Go to slide 2"
                        slide_num = int(aria_label.split()[-1]) - 1
                        return slide_num
                    except:
                        pass
            
            return 0
        except:
            return 0
    
    def _validate_progress_bar(self, carousel) -> Dict:
        """Validate pagination slider functionality"""
        progress_bar = {
            'exists': False,
            'is_visible': False,
            'indicator_count': 0,
            'pagination_moves_with_carousel': False,
            'test_details': []
        }
        
        try:
            # Find Splide pagination
            pagination = carousel.locator('.splide__pagination')
            
            if pagination.count() > 0:
                progress_bar['exists'] = True
                progress_bar['is_visible'] = pagination.first.is_visible()
                
                # Count pagination buttons
                pagination_buttons = pagination.locator('.splide__pagination__page')
                progress_bar['indicator_count'] = pagination_buttons.count()
                
                print(f"   [PAGINATION] Found: {progress_bar['indicator_count']} pagination buttons")
                
                # Track current focus alignment between slide and pagination
                current_pagination_index = self._get_active_pagination_index(carousel)
                current_slide_index = self._get_active_slide_index(carousel)
                progress_bar['active_pagination_index'] = current_pagination_index
                progress_bar['active_slide_index'] = current_slide_index
                progress_bar['active_matches_slide'] = current_pagination_index == current_slide_index

                # Test pagination movement with carousel
                if progress_bar['indicator_count'] > 1:
                    print(f"   [TESTING] Testing pagination movement...")
                    
                    # Get initial active pagination
                    initial_active = pagination.locator('.splide__pagination__page.is-active')
                    if initial_active.count() > 0:
                        initial_aria_label = initial_active.first.get_attribute('aria-label') or ''
                        print(f"   [PAGINATION] Initial active: {initial_aria_label}")
                        
                        # Test clicking next pagination button
                        next_pagination = pagination.locator('.splide__pagination__page:not(.is-active)').first
                        if next_pagination.count() > 0:
                            try:
                                before_slide = self._get_active_slide_index(carousel)
                                next_pagination.click(timeout=5000)
                                time.sleep(0.8)  # Wait for animation
                                after_slide = self._get_active_slide_index(carousel)
                                
                                progress_bar['pagination_moves_with_carousel'] = after_slide != before_slide
                                progress_bar['test_details'].append({
                                    'test': 'pagination_click',
                                    'before_slide': before_slide,
                                    'after_slide': after_slide,
                                    'success': progress_bar['pagination_moves_with_carousel']
                                })
                                
                                if progress_bar['pagination_moves_with_carousel']:
                                    print(f"   [SUCCESS] Pagination click: Slide changed from {before_slide} to {after_slide}")
                                else:
                                    print(f"   [FAIL] Pagination click: No slide change")
                                    
                            except Exception as e:
                                print(f"   [ERROR] Pagination testing failed: {str(e)}")
                
        except Exception as e:
            print(f"   [ERROR] Pagination validation failed: {str(e)}")
        
        return progress_bar
    
    def _get_carousel_title(self, carousel) -> Dict:
        """Get carousel title (e.g., 'Featured Products') with font styles"""
        title_data = {
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'font_weight': ''
        }
        
        try:
            # Use evaluate to find title - could be before carousel, in parent, or as sibling
            title_info = carousel.evaluate("""
                (carousel) => {
                    // First try: look inside carousel
                    let titleEl = carousel.querySelector('h2.cmp-carousel-title, .cmp-carousel-title, h2[class*="carousel-title"]');
                    
                    // Second try: check previous sibling
                    if (!titleEl) {
                        let prev = carousel.previousElementSibling;
                        while (prev && !titleEl) {
                            if (prev.matches('h2.cmp-carousel-title, .cmp-carousel-title, h2[class*="carousel-title"]')) {
                                titleEl = prev;
                            } else {
                                titleEl = prev.querySelector('h2.cmp-carousel-title, .cmp-carousel-title, h2[class*="carousel-title"]');
                            }
                            if (!titleEl) {
                                prev = prev.previousElementSibling;
                            }
                        }
                    }
                    
                    // Third try: check parent container
                    if (!titleEl) {
                        let parent = carousel.parentElement;
                        if (parent) {
                            titleEl = parent.querySelector('h2.cmp-carousel-title, .cmp-carousel-title, h2[class*="carousel-title"]');
                        }
                    }
                    
                    // Fourth try: check parent's previous sibling
                    if (!titleEl) {
                        let parent = carousel.parentElement;
                        if (parent && parent.previousElementSibling) {
                            titleEl = parent.previousElementSibling.querySelector('h2.cmp-carousel-title, .cmp-carousel-title, h2[class*="carousel-title"]');
                        }
                    }
                    
                    if (titleEl) {
                        const styles = window.getComputedStyle(titleEl);
                        return {
                            text: titleEl.textContent.trim(),
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight
                        };
                    }
                    return null;
                }
            """)
            
            if title_info:
                title_data['text'] = title_info.get('text', '')
                title_data['font_size'] = title_info.get('fontSize', '')
                title_data['font_color'] = title_info.get('color', '')
                title_data['font_family'] = title_info.get('fontFamily', '')
                title_data['font_weight'] = title_info.get('fontWeight', '')
        
        except Exception as e:
            print(f"   [WARNING] Could not extract carousel title: {str(e)}")
        
        return title_data
    
    def _get_font_styles(self, carousel) -> List[Dict]:
        """Get font styles of carousel text elements"""
        font_styles = []
        
        try:
            # Get title font styles
            titles = carousel.locator('h1, h2, h3, .title, [class*="title"]')
            if titles.count() > 0:
                title_styles = self.page.evaluate("""
                    () => {
                        const element = document.querySelector('.cmp-carousel__title, h1, h2, .title');
                        if (!element) return null;
                        const styles = window.getComputedStyle(element);
                        return {
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            color: styles.color
                        };
                    }
                """)
                
                if title_styles:
                    font_styles.append({
                        'element': 'title',
                        'font_size': title_styles['fontSize'],
                        'font_color': title_styles['color'],
                        'font_weight': title_styles['fontWeight'],
                        'font_family': title_styles['fontFamily']
                    })
                    print(f"   [FONT] Title: {title_styles['fontSize']}, Color: {title_styles['color']}")
            
            # Get description font styles
            descriptions = carousel.locator('p, .description')
            if descriptions.count() > 0:
                desc_styles = self.page.evaluate("""
                    () => {
                        const element = document.querySelector('.cmp-carousel__description, p');
                        if (!element) return null;
                        const styles = window.getComputedStyle(element);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color
                        };
                    }
                """)
                
                if desc_styles:
                    font_styles.append({
                        'element': 'description',
                        'font_size': desc_styles['fontSize'],
                        'font_color': desc_styles['color']
                    })
                    print(f"   [FONT] Description: {desc_styles['fontSize']}, Color: {desc_styles['color']}")

            # Get button font styles
            buttons = carousel.locator('.solidigm-btn, .cmp-hero__cta-container a, button, .btn')
            if buttons.count() > 0:
                btn_styles = self.page.evaluate("""
                    () => {
                        const element = document.querySelector('.solidigm-btn, .cmp-hero__cta-container a, button, .btn');
                        if (!element) return null;
                        const styles = window.getComputedStyle(element);
                        return {
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            color: styles.color,
                            textTransform: styles.textTransform
                        };
                    }
                """)
                if btn_styles:
                    font_styles.append({
                        'element': 'button',
                        'font_size': btn_styles['fontSize'],
                        'font_color': btn_styles['color'],
                        'font_weight': btn_styles['fontWeight'],
                        'font_family': btn_styles['fontFamily'],
                        'text_transform': btn_styles.get('textTransform', '')
                    })
                    print(f"   [FONT] Button: {btn_styles['fontSize']}, Color: {btn_styles['color']}")
            
        except Exception as e:
            print(f"   [ERROR] Font style extraction failed: {str(e)}")
        
        return font_styles
    
    def _get_container_size(self, carousel) -> Dict:
        """Get carousel container dimensions"""
        try:
            size = carousel.evaluate("""
                (carousel) => {
                    const rect = carousel.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            return size if size else {'width': 0, 'height': 0}
        except:
            return {'width': 0, 'height': 0}
    
    def _print_summary(self):
        """Print validation summary"""
        print("\n" + "="*80)
        print("HERO CAROUSEL VALIDATION SUMMARY")
        print("="*80)
        print(f"Total Hero Carousels: {self.validation_results['carousel_count']}")
        
        for i, carousel in enumerate(self.validation_results['carousels'], 1):
            print(f"\nMain Hero Carousel:")
            print(f"  Cards: {carousel.get('slide_count', 0)}")
            print(f"  Pagination Count: {carousel.get('pagination_count', 0)}")
            print(f"  Container: {carousel.get('container', {}).get('width', 0)}x{carousel.get('container', {}).get('height', 0)}")
            
            # Card details summary
            slides = carousel.get('slides', [])
            if slides:
                bg_images_present = sum(1 for s in slides if s.get('background_image_present'))
                print(f"  Background Images: {bg_images_present}/{len(slides)} cards have background images")
                
                # Button counts per card
                button_summary = {}
                for slide in slides:
                    count = slide.get('button_count', 0)
                    button_summary[count] = button_summary.get(count, 0) + 1
                if button_summary:
                    summary_text = ', '.join([f"{count} button(s): {freq} card(s)" for count, freq in sorted(button_summary.items())])
                    print(f"  Button Counts per Card: {summary_text}")
                
                # Check for 404 navigation issues
                navigation_issues = []
                for slide in slides:
                    for button in slide.get('buttons', []):
                        if button.get('click_tested') and not button.get('navigates_correctly'):
                            navigation_issues.append(f"Card {slide.get('index', 0)} - Button: {button.get('text', '')[:30]}")
                
                if navigation_issues:
                    print(f"  Navigation Issues: {len(navigation_issues)} buttons lead to 404 or invalid pages")
                    for issue in navigation_issues[:3]:  # Show first 3 issues
                        print(f"    - {issue}")
                else:
                    print(f"  Navigation: All buttons navigate correctly")
            
            # Navigation summary
            nav = carousel.get('navigation', {})
            if nav.get('left_clicks_tested', 0) > 0:
                print(f"  Left Chevron: {nav.get('left_clicks_successful', 0)}/{nav.get('left_clicks_tested', 0)} clicks successful")
            if nav.get('right_clicks_tested', 0) > 0:
                print(f"  Right Chevron: {nav.get('right_clicks_successful', 0)}/{nav.get('right_clicks_tested', 0)} clicks successful")
            
            # Pagination summary
            pb = carousel.get('progress_bar', {})
            print(f"  Pagination: {'Exists' if pb.get('exists') else 'Not Found'} ({pb.get('indicator_count', 0)} buttons)")
            if pb.get('pagination_moves_with_carousel'):
                print(f"  Pagination Movement: Working")
            print(f"  Font Styles: {len(carousel.get('font_styles', []))} captured")
