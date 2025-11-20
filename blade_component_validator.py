"""
Blade Component Validator for Solidigm Website
Validates blade components with left/right image layouts
"""
import time
from typing import Dict, List
from urllib.parse import urljoin
from playwright.sync_api import Page


class BladeComponentValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_blade_components(self, selector: str = '.cmp-blade') -> Dict:
        """Validate all blade components on the page"""
        print("\n" + "="*80)
        print("BLADE COMPONENTS VALIDATION")
        print("="*80)
        
        results = {
            'component_exists': False,
            'blade_count': 0,
            'blades': []
        }
        
        try:
            # Find all blade components
            blades = self.page.locator(selector)
            blade_count = blades.count()
            
            if blade_count == 0:
                print("[WARNING] No blade components found")
                return results
            
            results['component_exists'] = True
            results['blade_count'] = blade_count
            print(f"[INFO] Found {blade_count} blade component(s)")
            
            # Validate each blade
            for i in range(blade_count):
                blade = blades.nth(i)
                print(f"\n[BLADE {i+1}] Validating blade component {i+1}...")
                
                # Scroll blade into view
                try:
                    blade.scroll_into_view_if_needed(timeout=5000)
                    self.page.wait_for_timeout(300)
                except Exception:
                    pass
                
                blade_data = self._validate_single_blade(blade, i)
                results['blades'].append(blade_data)
                
                print(f"   [OK] Blade {i+1}: {blade_data.get('layout', 'Unknown')} layout")
                print(f"   [OK] Title: {blade_data.get('title', {}).get('text', '')[:50]}")
                print(f"   [OK] Button: {blade_data.get('button', {}).get('text', '')[:30]}")
            
            print(f"\n[SUMMARY] Validated {blade_count} blade component(s)")
            
        except Exception as e:
            print(f"[ERROR] Blade components validation failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _validate_single_blade(self, blade, index: int) -> Dict:
        """Validate a single blade component"""
        blade_data = {
            'index': index + 1,
            'container': {},
            'layout': 'Unknown',
            'image': {},
            'title': {},
            'description': {},
            'button': {},
            'links': []
        }
        
        try:
            # 1. Get container size
            container_size = blade.evaluate("""
                (blade) => {
                    const rect = blade.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            if container_size:
                blade_data['container'] = {
                    'width': int(container_size.get('width', 0)),
                    'height': int(container_size.get('height', 0))
                }
            
            # 2. Determine layout (image left or right)
            layout = self._determine_layout(blade)
            blade_data['layout'] = layout
            
            # 3. Validate image
            image_data = self._validate_image(blade)
            blade_data['image'] = image_data
            
            # 4. Validate title
            title_data = self._validate_title(blade)
            blade_data['title'] = title_data
            
            # 5. Validate description
            description_data = self._validate_description(blade)
            blade_data['description'] = description_data
            
            # 6. Validate button/CTA
            button_data = self._validate_button(blade)
            blade_data['button'] = button_data
            
            # 7. Collect all links
            links_data = self._collect_links(blade)
            blade_data['links'] = links_data
            blade_data['link_count'] = len(links_data)
            
            # 8. Overall validation status
            blade_data['is_valid'] = (
                image_data.get('src', '') != '' and
                title_data.get('text', '') != '' and
                button_data.get('text', '') != ''
            )
            
        except Exception as e:
            print(f"   [ERROR] Blade {index+1} validation failed: {str(e)}")
            blade_data['error'] = str(e)
        
        return blade_data
    
    def _determine_layout(self, blade) -> str:
        """Determine if image is on left or right based on visual position"""
        try:
            # Check actual visual position on screen (not DOM order, as CSS can change it)
            layout_info = blade.evaluate("""
                (blade) => {
                    const media = blade.querySelector('.cmp-blade__media');
                    const content = blade.querySelector('.cmp-blade__content');
                    if (!media || !content) return 'Unknown';
                    
                    // Get actual visual position on screen
                    const mediaRect = media.getBoundingClientRect();
                    const contentRect = content.getBoundingClientRect();
                    
                    // Compare left positions - whichever has smaller left value is visually on the left
                    const mediaLeft = mediaRect.left;
                    const contentLeft = contentRect.left;
                    
                    // Also check if they're on the same row (similar top positions)
                    const topDiff = Math.abs(mediaRect.top - contentRect.top);
                    const sameRow = topDiff < 50; // Within 50px vertically means same row
                    
                    if (sameRow) {
                        // Same row - compare left positions
                        if (mediaLeft < contentLeft) {
                            return 'Image Left';
                        } else if (mediaLeft > contentLeft) {
                            return 'Image Right';
                        } else {
                            // Same position (shouldn't happen, but fallback)
                            return 'Unknown';
                        }
                    } else {
                        // Different rows - check which is higher (top value)
                        if (mediaRect.top < contentRect.top) {
                            // Media is above content - check if it's left or right aligned
                            if (mediaLeft < contentLeft) {
                                return 'Image Left';
                            } else {
                                return 'Image Right';
                            }
                        } else {
                            // Content is above media
                            if (contentLeft < mediaLeft) {
                                return 'Image Right';
                            } else {
                                return 'Image Left';
                            }
                        }
                    }
                }
            """)
            return layout_info
        except Exception as e:
            print(f"   [WARNING] Layout detection failed: {str(e)}")
            return 'Unknown'
    
    def _validate_image(self, blade) -> Dict:
        """Validate blade image"""
        image_data = {
            'src': '',
            'alt': '',
            'width': 0,
            'height': 0,
            'loaded': False
        }
        
        try:
            # Find image in .cmp-blade__media
            media = blade.locator('.cmp-blade__media')
            if media.count() > 0:
                # Try to find img tag (could be in picture or direct)
                img = media.locator('img').first
                if img.count() > 0:
                    image_data['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                    image_data['alt'] = img.get_attribute('alt') or ''
                    
                    # Get image dimensions
                    try:
                        img_info = img.evaluate("""
                            (img) => {
                                return {
                                    width: img.naturalWidth || img.width || 0,
                                    height: img.naturalHeight || img.height || 0,
                                    loaded: img.complete && img.naturalHeight !== 0
                                };
                            }
                        """)
                        if img_info:
                            image_data['width'] = int(img_info.get('width', 0))
                            image_data['height'] = int(img_info.get('height', 0))
                            image_data['loaded'] = bool(img_info.get('loaded', False))
                    except Exception:
                        # Fallback to attributes
                        width_attr = img.get_attribute('width')
                        height_attr = img.get_attribute('height')
                        if width_attr:
                            image_data['width'] = int(width_attr)
                        if height_attr:
                            image_data['height'] = int(height_attr)
        
        except Exception as e:
            print(f"      [ERROR] Image validation failed: {str(e)}")
        
        return image_data
    
    def _validate_title(self, blade) -> Dict:
        """Validate blade title"""
        title_data = {
            'text': '',
            'font_styles': {}
        }
        
        try:
            title_element = blade.locator('.cmp-blade__title, h2').first
            if title_element.count() > 0:
                title_data['text'] = (title_element.text_content() or '').strip()
                
                # Get font styles
                font_styles = title_element.evaluate("""
                    (el) => {
                        const styles = window.getComputedStyle(el);
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
                    title_data['font_styles'] = {
                        'fontSize': font_styles.get('fontSize', ''),
                        'fontFamily': font_styles.get('fontFamily', ''),
                        'fontWeight': font_styles.get('fontWeight', ''),
                        'color': font_styles.get('color', ''),
                        'lineHeight': font_styles.get('lineHeight', '')
                    }
        
        except Exception as e:
            print(f"      [ERROR] Title validation failed: {str(e)}")
        
        return title_data
    
    def _validate_description(self, blade) -> Dict:
        """Validate blade description"""
        description_data = {
            'text': '',
            'font_styles': {}
        }
        
        try:
            desc_element = blade.locator('.cmp-blade__description').first
            if desc_element.count() > 0:
                # Get text without the border span
                desc_text = desc_element.evaluate("""
                    (el) => {
                        const border = el.querySelector('.cmp-blade__description--border');
                        if (border) {
                            border.remove();
                        }
                        return el.textContent.trim();
                    }
                """)
                description_data['text'] = desc_text or (desc_element.text_content() or '').strip()
                
                # Get font styles
                font_styles = desc_element.evaluate("""
                    (el) => {
                        const styles = window.getComputedStyle(el);
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
                    description_data['font_styles'] = {
                        'fontSize': font_styles.get('fontSize', ''),
                        'fontFamily': font_styles.get('fontFamily', ''),
                        'fontWeight': font_styles.get('fontWeight', ''),
                        'color': font_styles.get('color', ''),
                        'lineHeight': font_styles.get('lineHeight', '')
                    }
        
        except Exception as e:
            print(f"      [ERROR] Description validation failed: {str(e)}")
        
        return description_data
    
    def _validate_button(self, blade) -> Dict:
        """Validate blade button/CTA"""
        button_data = {
            'text': '',
            'href': '',
            'target': '',
            'font_styles': {},
            'is_valid': False,
            'status_code': 0,
            'navigation_tested': False,
            'navigates_correctly': False
        }
        
        try:
            # Find button/CTA link
            button = blade.locator('.cmp-blade__cta-container a, .solidigm-btn').first
            if button.count() > 0:
                button_data['text'] = (button.text_content() or '').strip()
                button_data['href'] = button.get_attribute('href') or ''
                button_data['target'] = button.get_attribute('target') or '_self'
                
                # Get font styles
                font_styles = button.evaluate("""
                    (el) => {
                        const styles = window.getComputedStyle(el);
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
                if font_styles:
                    button_data['font_styles'] = {
                        'fontSize': font_styles.get('fontSize', ''),
                        'fontFamily': font_styles.get('fontFamily', ''),
                        'fontWeight': font_styles.get('fontWeight', ''),
                        'color': font_styles.get('color', ''),
                        'backgroundColor': font_styles.get('backgroundColor', ''),
                        'lineHeight': font_styles.get('lineHeight', '')
                    }
                
                # Validate link
                if button_data['href'] and button_data['href'] != '#':
                    try:
                        absolute_href = button_data['href'] if button_data['href'].startswith('http') else urljoin(self.page.url, button_data['href'])
                        response = self.page.request.get(absolute_href, timeout=3000)
                        button_data['status_code'] = response.status
                        button_data['is_valid'] = 200 <= response.status < 400
                    except Exception:
                        button_data['is_valid'] = False
                
                # Test navigation (optional - can be time-consuming)
                # Uncomment if needed:
                # try:
                #     current_url = self.page.url
                #     button.click(timeout=5000)
                #     time.sleep(1)
                #     new_url = self.page.url
                #     button_data['navigation_tested'] = True
                #     button_data['navigates_correctly'] = (new_url != current_url)
                #     if button_data['navigates_correctly']:
                #         self.page.go_back(wait_until='load', timeout=10000)
                #         time.sleep(1)
                # except Exception:
                #     pass
        
        except Exception as e:
            print(f"      [ERROR] Button validation failed: {str(e)}")
        
        return button_data
    
    def _collect_links(self, blade) -> List[Dict]:
        """Collect all links in the blade"""
        links = []
        
        try:
            all_links = blade.locator('a[href]')
            link_count = all_links.count()
            
            for i in range(min(link_count, 5)):  # Limit to first 5 links
                link = all_links.nth(i)
                href = link.get_attribute('href') or ''
                text = (link.text_content() or '').strip()
                
                if href and href != '#':
                    link_data = {
                        'text': text[:50],
                        'href': href,
                        'is_valid': False,
                        'status_code': 0
                    }
                    
                    # Validate link
                    try:
                        absolute_href = href if href.startswith('http') else urljoin(self.page.url, href)
                        response = self.page.request.get(absolute_href, timeout=3000)
                        link_data['status_code'] = response.status
                        link_data['is_valid'] = 200 <= response.status < 400
                    except Exception:
                        link_data['is_valid'] = False
                    
                    links.append(link_data)
        
        except Exception as e:
            print(f"      [ERROR] Link collection failed: {str(e)}")
        
        return links

