"""
Carousel Component Validator for Solidigm Website
Validates carousel components including images, text, buttons, navigation, and progress bar
"""
import time
from typing import Dict, List
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
    
    def validate_carousel(self, selector: str = '.cmp-carousel, .carousel, [class*="carousel"]') -> Dict:
        """Validate carousel component"""
        print("\n" + "="*80)
        print("CAROUSEL VALIDATION")
        print("="*80)
        
        try:
            # Find carousel elements
            carousels = self.page.locator(selector)
            count = carousels.count()
            
            print(f"\n[CAROUSEL] Found {count} carousel component(s)")
            
            if count == 0:
                print("[WARNING] No carousel found on page")
                return self.validation_results
            
            # Validate each carousel
            for i in range(count):
                carousel = carousels.nth(i)
                print(f"\n[INFO] Validating carousel {i+1}...")
                
                carousel_data = self._validate_single_carousel(carousel, i)
                self.validation_results['carousels'].append(carousel_data)
            
            self.validation_results['carousel_count'] = count
            
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
            # 1. Get container size
            container_info = self._get_container_size(carousel)
            carousel_data['container'] = container_info
            print(f"   [CONTAINER] Size: {container_info.get('width', 0)}x{container_info.get('height', 0)}")
            
            # 2. Count slides
            slides = carousel.locator('.cmp-carousel__slide, [class*="slide"], .slide')
            slide_count = slides.count()
            carousel_data['slide_count'] = slide_count
            print(f"   [SLIDES] Total: {slide_count}")
            
            # 3. Validate slides
            for slide_idx in range(min(slide_count, 20)):  # First 20 slides max to avoid too much output
                slide = slides.nth(slide_idx)
                slide_data = self._validate_slide(slide, slide_idx)
                carousel_data['slides'].append(slide_data)
                print(f"      Slide {slide_idx+1}/{slide_count}: {slide_data.get('title', '')[:50]}")
            
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
            # Get title
            title_element = slide.locator('h1, h2, h3, .title, [class*="title"]').first
            if title_element.count() > 0:
                slide_data['title'] = title_element.text_content() or ''
                print(f"      Slide {index+1} - Title: {slide_data['title'][:50]}")
            
            # Get description
            desc_element = slide.locator('p, .description, [class*="description"]').first
            if desc_element.count() > 0:
                slide_data['description'] = desc_element.text_content() or ''
                print(f"      Slide {index+1} - Description: {slide_data['description'][:80]}")
            
            # Get background image
            bg_image = slide.evaluate("""
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
            slide_data['background_image'] = bg_image or ''
            slide_data['background_image_present'] = bool(bg_image)
            
            if bg_image:
                print(f"      Slide {index+1} - Background Image: Present ({bg_image[:60]})")
            else:
                print(f"      Slide {index+1} - Background Image: NOT FOUND")
            
            # Get regular images
            images = slide.locator('img')
            if images.count() > 0:
                img = images.first
                src = img.get_attribute('src') or ''
                slide_data['main_image'] = src
                
                # Check if image loads
                try:
                    img_loaded = slide.evaluate("""
                        (slide) => {
                            const img = slide.querySelector('img');
                            return img && img.complete && img.naturalHeight !== 0;
                        }
                    """)
                    slide_data['image_loaded'] = img_loaded
                except:
                    slide_data['image_loaded'] = False
            
            # Get and validate buttons with click testing
            buttons = slide.locator('button, [class*="button"], .btn, a[class*="btn"]')
            button_count = buttons.count()
            slide_data['button_count'] = button_count
            
            print(f"      Slide {index+1} - Button Count: {button_count}")
            
            for i in range(min(button_count, 2)):  # Test max 2 buttons per card
                btn = buttons.nth(i)
                text = btn.text_content() or ''
                is_visible = btn.is_visible()
                is_enabled = btn.is_enabled() if btn.get_attribute('disabled') is None else False
                
                button_data = {
                    'text': text[:50],
                    'is_visible': is_visible,
                    'is_enabled': is_enabled,
                    'click_tested': False,
                    'navigates_correctly': False
                }
                
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
                            print(f"      Slide {index+1} - Button {i+1} clicked: Navigated from {current_url} to {new_url}")
                        else:
                            print(f"      Slide {index+1} - Button {i+1} clicked: No navigation occurred")
                        
                        # Go back to original page if navigated
                        if navigation_occurred:
                            self.page.go_back(wait_until='load', timeout=10000)
                            time.sleep(1)
                        
                    except Exception as e:
                        print(f"      Slide {index+1} - Button {i+1} click test failed: {str(e)}")
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
            print(f"      [ERROR] Slide {index+1} validation failed: {str(e)}")
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
            # Find chevron buttons
            left_chevron = carousel.locator('[class*="prev"], [class*="left"], [aria-label*="prev"], [aria-label*="left"], .chevron-left')
            right_chevron = carousel.locator('[class*="next"], [class*="right"], [aria-label*="next"], [aria-label*="right"], .chevron-right')
            
            navigation['has_left_chevron'] = left_chevron.count() > 0
            navigation['has_right_chevron'] = right_chevron.count() > 0
            
            if left_chevron.count() > 0:
                navigation['left_chevron_visible'] = left_chevron.first.is_visible()
            
            if right_chevron.count() > 0:
                navigation['right_chevron_visible'] = right_chevron.first.is_visible()
            
            print(f"   [NAVIGATION] Left: {navigation['left_chevron_visible']}, Right: {navigation['right_chevron_visible']}")
            
            # Test chevron functionality
            if navigation['left_chevron_visible'] or navigation['right_chevron_visible']:
                print(f"   [TESTING] Testing chevron functionality...")
                
                # Test right chevron with 2 clicks
                if navigation['right_chevron_visible']:
                    print(f"   [TESTING] Testing right chevron...")
                    try:
                        right_btn = right_chevron.first
                        
                        # Get initial active slide
                        initial_slide = self._get_active_slide_index(carousel)
                        
                        # Test 2 clicks on right chevron
                        for click_num in range(1, 3):
                            right_btn.scroll_into_view_if_needed(timeout=5000)
                            time.sleep(0.3)
                            
                            before_slide = self._get_active_slide_index(carousel)
                            right_btn.click(timeout=5000)
                            time.sleep(0.5)  # Wait for animation
                            after_slide = self._get_active_slide_index(carousel)
                            
                            navigation['right_clicks_tested'] += 1
                            
                            # Check if slide changed
                            if after_slide != before_slide:
                                navigation['right_clicks_successful'] += 1
                                navigation['test_details'].append({
                                    'chevron': 'right',
                                    'click': click_num,
                                    'before': before_slide,
                                    'after': after_slide,
                                    'success': True
                                })
                                print(f"   [SUCCESS] Right click {click_num}: Slide changed from {before_slide} to {after_slide}")
                            else:
                                navigation['test_details'].append({
                                    'chevron': 'right',
                                    'click': click_num,
                                    'before': before_slide,
                                    'after': after_slide,
                                    'success': False
                                })
                                print(f"   [FAIL] Right click {click_num}: No slide change")
                    
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
                            
                            before_slide = self._get_active_slide_index(carousel)
                            left_btn.click(timeout=5000)
                            time.sleep(0.5)  # Wait for animation
                            after_slide = self._get_active_slide_index(carousel)
                            
                            navigation['left_clicks_tested'] += 1
                            
                            # Check if slide changed
                            if after_slide != before_slide:
                                navigation['left_clicks_successful'] += 1
                                navigation['test_details'].append({
                                    'chevron': 'left',
                                    'click': click_num,
                                    'before': before_slide,
                                    'after': after_slide,
                                    'success': True
                                })
                                print(f"   [SUCCESS] Left click {click_num}: Slide changed from {before_slide} to {after_slide}")
                            else:
                                navigation['test_details'].append({
                                    'chevron': 'left',
                                    'click': click_num,
                                    'before': before_slide,
                                    'after': after_slide,
                                    'success': False
                                })
                                print(f"   [FAIL] Left click {click_num}: No slide change")
                    
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
            # Try different methods to find active slide
            # Method 1: Check for 'active' class
            active_slides = carousel.locator('.active, [class*="active"], [data-active="true"]')
            if active_slides.count() > 0:
                return 0  # Return 0 as placeholder
            
            # Method 2: Check visibility
            slides = carousel.locator('.cmp-carousel__slide, [class*="slide"], .slide')
            for i in range(slides.count()):
                slide = slides.nth(i)
                if slide.is_visible(timeout=1000):
                    return i
            
            return 0
        except:
            return 0
    
    def _validate_progress_bar(self, carousel) -> Dict:
        """Validate progress bar functionality"""
        progress_bar = {
            'exists': False,
            'is_visible': False,
            'animated': False
        }
        
        try:
            # Find progress indicators
            progress_indicators = carousel.locator('[class*="progress"], [class*="indicator"], [class*="dot"], [role="tablist"]')
            
            if progress_indicators.count() > 0:
                progress_bar['exists'] = True
                progress_bar['is_visible'] = progress_indicators.first.is_visible()
                
                # Count indicators
                dots = progress_indicators.locator('li, button, [class*="dot"]')
                progress_bar['indicator_count'] = dots.count()
                
                print(f"   [PROGRESS BAR] Found: {progress_bar['indicator_count']} indicators")
                
        except Exception as e:
            print(f"   [ERROR] Progress bar validation failed: {str(e)}")
        
        return progress_bar
    
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
        print("CAROUSEL VALIDATION SUMMARY")
        print("="*80)
        print(f"Total Carousels: {self.validation_results['carousel_count']}")
        
        for i, carousel in enumerate(self.validation_results['carousels'], 1):
            print(f"\nCarousel {i}:")
            print(f"  Total Slides/Cards: {carousel.get('slide_count', 0)}")
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
            
            # Navigation summary
            nav = carousel.get('navigation', {})
            if nav.get('left_clicks_tested', 0) > 0:
                print(f"  Left Chevron: {nav.get('left_clicks_successful', 0)}/{nav.get('left_clicks_tested', 0)} clicks successful")
            if nav.get('right_clicks_tested', 0) > 0:
                print(f"  Right Chevron: {nav.get('right_clicks_successful', 0)}/{nav.get('right_clicks_tested', 0)} clicks successful")
            
            print(f"  Progress Bar: {'Exists' if carousel.get('progress_bar', {}).get('exists') else 'Not Found'}")
            print(f"  Font Styles: {len(carousel.get('font_styles', []))} captured")
