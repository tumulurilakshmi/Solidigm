"""
Hero Component Validator
Validates hero section including container size, background image, breadcrumbs, title, and description
"""
from typing import Dict, List
from playwright.sync_api import Page


class HeroComponentValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_hero_component(self, selector: str = '.cmp-hero, .hero') -> Dict:
        """Validate Hero component - Works for D3, D5, D7 series pages"""
        print("\n" + "="*80)
        print("HERO COMPONENT VALIDATION")
        print("="*80)
        
        try:
            # Find hero section
            hero = self.page.locator(selector).first
            
            if hero.count() == 0:
                print("[WARNING] Hero component not found")
                return {'found': False}
            
            print(f"\n[INFO] Hero component found")
            
            # Scroll hero into view
            try:
                hero.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except Exception:
                pass
            
            # Validate container size
            print("\n[CONTAINER] Validating container size...")
            container_data = self._validate_container_size(hero)
            
            # Validate background image
            print("\n[BACKGROUND] Validating background image...")
            background_data = self._validate_background_image(hero)
            
            # Validate breadcrumbs
            print("\n[BREADCRUMBS] Validating breadcrumbs...")
            breadcrumbs_data = self._validate_breadcrumbs(hero)
            
            # Validate title
            print("\n[TITLE] Validating hero title...")
            title_data = self._validate_title(hero)
            
            # Validate description
            print("\n[DESCRIPTION] Validating hero description...")
            description_data = self._validate_description(hero)
            
            # Identify series from extracted text
            identified_series = self._identify_series(title_data, breadcrumbs_data)
            
            results = {
                'found': True,
                'identified_series': identified_series,
                'container': container_data,
                'background': background_data,
                'breadcrumbs': breadcrumbs_data,
                'title': title_data,
                'description': description_data,
                'summary': {
                    'container_found': container_data.get('found', False),
                    'background_found': background_data.get('found', False),
                    'breadcrumbs_found': breadcrumbs_data.get('found', False),
                    'title_found': title_data.get('found', False),
                    'description_found': description_data.get('found', False),
                    'all_breadcrumbs_clickable': breadcrumbs_data.get('all_clickable_except_last', False),
                    'series_identified': identified_series.get('series', 'Unknown')
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Hero component validation failed: {str(e)}")
            return {'error': str(e)}
    
    def _identify_series(self, title_data: Dict, breadcrumbs_data: Dict) -> Dict:
        """Identify which series (D3, D5, D7) based on extracted text"""
        identified = {
            'series': 'Unknown',
            'confidence': 'low',
            'matched_by': []
        }
        
        try:
            # Check title text
            title_text = title_data.get('text', '').upper()
            breadcrumb_texts = [level.get('text', '').upper() for level in breadcrumbs_data.get('levels', [])]
            all_text = ' '.join([title_text] + breadcrumb_texts)
            
            # Check for D3 indicators
            if 'D3' in title_text or 'D3' in all_text:
                if 'SSD D3 SERIES' in title_text or 'D3 SERIES' in title_text:
                    identified['series'] = 'D3'
                    identified['confidence'] = 'high'
                    identified['matched_by'].append('title_text')
            
            # Check for D5 indicators
            if 'D5' in title_text or 'D5' in all_text:
                if 'D5 SERIES' in title_text or 'D5 SERIES SSDS' in title_text:
                    identified['series'] = 'D5'
                    identified['confidence'] = 'high'
                    identified['matched_by'].append('title_text')
            
            # Check for D7 indicators
            if 'D7' in title_text or 'D7' in all_text:
                if 'SSD D7 SERIES' in title_text or 'D7 SERIES' in title_text:
                    identified['series'] = 'D7'
                    identified['confidence'] = 'high'
                    identified['matched_by'].append('title_text')
            
            if identified['series'] != 'Unknown':
                print(f"\n[INFO] Series identified: {identified['series']} (confidence: {identified['confidence']})")
        
        except Exception as e:
            print(f"   [WARNING] Could not identify series: {str(e)}")
        
        return identified
    
    def _validate_container_size(self, hero) -> Dict:
        """Validate hero container size"""
        container_data = {
            'found': False,
            'width': 0,
            'height': 0,
            'width_px': '',
            'height_px': ''
        }
        
        try:
            # Get container dimensions
            size = hero.evaluate("""
                (hero) => {
                    const rect = hero.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            
            if size:
                container_data['found'] = True
                container_data['width'] = int(size.get('width', 0))
                container_data['height'] = int(size.get('height', 0))
                container_data['width_px'] = f"{container_data['width']}px"
                container_data['height_px'] = f"{container_data['height']}px"
                
                print(f"   [OK] Container size: {container_data['width']}x{container_data['height']} px")
        
        except Exception as e:
            print(f"   [ERROR] Container size validation failed: {str(e)}")
        
        return container_data
    
    def _validate_background_image(self, hero) -> Dict:
        """Validate background image"""
        background_data = {
            'found': False,
            'desktop_image': {},
            'mobile_image': {},
            'has_desktop': False,
            'has_mobile': False
        }
        
        try:
            # Check for desktop background image
            desktop_bg = hero.locator('.cmp-hero__background-image--desktop img').first
            if desktop_bg.count() > 0:
                background_data['has_desktop'] = True
                background_data['desktop_image']['src'] = desktop_bg.get_attribute('src') or ''
                background_data['desktop_image']['alt'] = desktop_bg.get_attribute('alt') or ''
                background_data['desktop_image']['loading'] = desktop_bg.get_attribute('loading') or ''
                
                # Get image dimensions
                img_size = desktop_bg.evaluate("""
                    (img) => {
                        return {
                            width: img.naturalWidth || img.width || 0,
                            height: img.naturalHeight || img.height || 0
                        };
                    }
                """)
                
                if img_size:
                    background_data['desktop_image']['width'] = img_size.get('width', 0)
                    background_data['desktop_image']['height'] = img_size.get('height', 0)
                
                # Check if image is loaded
                img_loaded = desktop_bg.evaluate("""
                    (img) => {
                        return img && img.complete && img.naturalHeight !== 0;
                    }
                """)
                background_data['desktop_image']['loaded'] = img_loaded
                
                print(f"   [OK] Desktop background image found")
                print(f"        Source: {background_data['desktop_image']['src'][:80]}...")
                print(f"        Size: {background_data['desktop_image'].get('width', 0)}x{background_data['desktop_image'].get('height', 0)}")
                print(f"        Loaded: {background_data['desktop_image'].get('loaded', False)}")
            
            # Check for mobile background image
            mobile_bg = hero.locator('.cmp-hero__background-image--mobile img').first
            if mobile_bg.count() > 0:
                background_data['has_mobile'] = True
                background_data['mobile_image']['src'] = mobile_bg.get_attribute('src') or ''
                background_data['mobile_image']['alt'] = mobile_bg.get_attribute('alt') or ''
                background_data['mobile_image']['loading'] = mobile_bg.get_attribute('loading') or ''
                
                # Get image dimensions
                img_size = mobile_bg.evaluate("""
                    (img) => {
                        return {
                            width: img.naturalWidth || img.width || 0,
                            height: img.naturalHeight || img.height || 0
                        };
                    }
                """)
                
                if img_size:
                    background_data['mobile_image']['width'] = img_size.get('width', 0)
                    background_data['mobile_image']['height'] = img_size.get('height', 0)
                
                print(f"   [OK] Mobile background image found")
            
            background_data['found'] = background_data['has_desktop'] or background_data['has_mobile']
        
        except Exception as e:
            print(f"   [ERROR] Background image validation failed: {str(e)}")
        
        return background_data
    
    def _validate_breadcrumbs(self, hero) -> Dict:
        """Validate breadcrumbs with levels, clickability, and font details"""
        breadcrumbs_data = {
            'found': False,
            'levels': [],
            'total_levels': 0,
            'all_clickable_except_last': False,
            'font_details': {}
        }
        
        try:
            # Find breadcrumb navigation
            breadcrumb_nav = hero.locator('.cmp-breadcrumb, nav[aria-label*="breadcrumb"]').first
            
            if breadcrumb_nav.count() > 0:
                breadcrumbs_data['found'] = True
                
                # Get all breadcrumb items
                items = breadcrumb_nav.locator('.cmp-breadcrumb__item, li[itemprop="itemListElement"]').all()
                breadcrumbs_data['total_levels'] = len(items)
                
                print(f"   [OK] Breadcrumbs found: {breadcrumbs_data['total_levels']} levels")
                
                # Validate each breadcrumb level
                for i, item in enumerate(items):
                    level_data = {
                        'level': i + 1,
                        'text': '',
                        'is_clickable': False,
                        'href': '',
                        'is_last': False,
                        'font_size': '',
                        'font_color': '',
                        'font_family': '',
                        'font_weight': ''
                    }
                    
                    # Get text
                    text_elem = item.locator('span[itemprop="name"], a').first
                    if text_elem.count() > 0:
                        level_data['text'] = (text_elem.text_content() or '').strip()
                    
                    # Check if it's the last item (active/current page)
                    is_active = item.get_attribute('aria-current') == 'page' or 'cmp-breadcrumb__item--active' in (item.get_attribute('class') or '')
                    level_data['is_last'] = is_active
                    
                    # Check if clickable (should have link, except last)
                    link = item.locator('a.cmp-breadcrumb__item-link, a[itemprop="item"]').first
                    if link.count() > 0:
                        level_data['is_clickable'] = True
                        level_data['href'] = link.get_attribute('href') or ''
                    
                    # Validate clickability rule: all except last should be clickable
                    if not is_active and not level_data['is_clickable']:
                        print(f"      [WARNING] Level {i+1} ('{level_data['text']}') should be clickable but link not found")
                    
                    if is_active and level_data['is_clickable']:
                        print(f"      [WARNING] Last level ('{level_data['text']}') should NOT be clickable but has link")
                    
                    # Get font details from the text element or link
                    font_elem = link if link.count() > 0 else text_elem
                    if font_elem.count() > 0:
                        font_styles = font_elem.evaluate("""
                            (elem) => {
                                const styles = window.getComputedStyle(elem);
                                return {
                                    fontSize: styles.fontSize,
                                    fontFamily: styles.fontFamily,
                                    fontWeight: styles.fontWeight,
                                    color: styles.color
                                };
                            }
                        """)
                        
                        if font_styles:
                            level_data['font_size'] = font_styles.get('fontSize', '')
                            level_data['font_color'] = font_styles.get('color', '')
                            level_data['font_family'] = font_styles.get('fontFamily', '')
                            level_data['font_weight'] = font_styles.get('fontWeight', '')
                    
                    breadcrumbs_data['levels'].append(level_data)
                    
                    print(f"      [OK] Level {i+1}: '{level_data['text']}'")
                    print(f"          Clickable: {level_data['is_clickable']}, Last: {level_data['is_last']}")
                    if level_data['font_size']:
                        print(f"          Font: {level_data['font_size']}, Color: {level_data['font_color']}")
                
                # Check if all except last are clickable
                clickable_count = sum(1 for level in breadcrumbs_data['levels'] if level['is_clickable'])
                last_count = sum(1 for level in breadcrumbs_data['levels'] if level['is_last'])
                breadcrumbs_data['all_clickable_except_last'] = (
                    clickable_count == (breadcrumbs_data['total_levels'] - last_count) and
                    all(not level['is_clickable'] for level in breadcrumbs_data['levels'] if level['is_last'])
                )
                
                # Get overall breadcrumb font details (from first item)
                if breadcrumbs_data['levels']:
                    first_level = breadcrumbs_data['levels'][0]
                    breadcrumbs_data['font_details'] = {
                        'font_size': first_level.get('font_size', ''),
                        'font_color': first_level.get('font_color', ''),
                        'font_family': first_level.get('font_family', ''),
                        'font_weight': first_level.get('font_weight', '')
                    }
            else:
                print(f"   [WARNING] Breadcrumbs not found")
        
        except Exception as e:
            print(f"   [ERROR] Breadcrumbs validation failed: {str(e)}")
        
        return breadcrumbs_data
    
    def _validate_title(self, hero) -> Dict:
        """Validate hero title with font details"""
        title_data = {
            'found': False,
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'font_weight': '',
            'line_height': ''
        }
        
        try:
            # Find title (h1 with cmp-hero__title class)
            title = hero.locator('h1.cmp-hero__title, .cmp-hero__title').first
            
            if title.count() > 0:
                title_data['found'] = True
                title_data['text'] = (title.text_content() or '').strip()
                
                # Get font styles
                font_styles = title.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
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
                    title_data['font_size'] = font_styles.get('fontSize', '')
                    title_data['font_color'] = font_styles.get('color', '')
                    title_data['font_family'] = font_styles.get('fontFamily', '')
                    title_data['font_weight'] = font_styles.get('fontWeight', '')
                    title_data['line_height'] = font_styles.get('lineHeight', '')
                
                print(f"   [OK] Title: '{title_data['text']}'")
                print(f"        Font Size: {title_data['font_size']}")
                print(f"        Font Color: {title_data['font_color']}")
                print(f"        Font Family: {title_data['font_family']}")
                print(f"        Font Weight: {title_data['font_weight']}")
            else:
                print(f"   [WARNING] Hero title not found")
        
        except Exception as e:
            print(f"   [ERROR] Title validation failed: {str(e)}")
        
        return title_data
    
    def _validate_description(self, hero) -> Dict:
        """Validate hero description with font details"""
        description_data = {
            'found': False,
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'font_weight': '',
            'line_height': ''
        }
        
        try:
            # Find description
            description = hero.locator('.cmp-hero__description, .cmp-hero__description p').first
            
            if description.count() > 0:
                description_data['found'] = True
                description_data['text'] = (description.text_content() or '').strip()
                
                # Get font styles (check the paragraph inside if it exists)
                desc_elem = description.locator('p').first
                if desc_elem.count() == 0:
                    desc_elem = description
                
                font_styles = desc_elem.evaluate("""
                    (desc) => {
                        const styles = window.getComputedStyle(desc);
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
                    description_data['font_size'] = font_styles.get('fontSize', '')
                    description_data['font_color'] = font_styles.get('color', '')
                    description_data['font_family'] = font_styles.get('fontFamily', '')
                    description_data['font_weight'] = font_styles.get('fontWeight', '')
                    description_data['line_height'] = font_styles.get('lineHeight', '')
                
                print(f"   [OK] Description found")
                print(f"        Text: '{description_data['text'][:80]}...'")
                print(f"        Font Size: {description_data['font_size']}")
                print(f"        Font Color: {description_data['font_color']}")
                print(f"        Font Family: {description_data['font_family']}")
            else:
                print(f"   [WARNING] Hero description not found")
        
        except Exception as e:
            print(f"   [ERROR] Description validation failed: {str(e)}")
        
        return description_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("HERO COMPONENT SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        identified = results.get('identified_series', {})
        
        print(f"Series Identified: {identified.get('series', 'Unknown')} (confidence: {identified.get('confidence', 'low')})")
        print(f"Container Found: {'Yes' if summary.get('container_found') else 'No'}")
        print(f"Background Found: {'Yes' if summary.get('background_found') else 'No'}")
        print(f"Breadcrumbs Found: {'Yes' if summary.get('breadcrumbs_found') else 'No'}")
        print(f"Title Found: {'Yes' if summary.get('title_found') else 'No'}")
        print(f"Description Found: {'Yes' if summary.get('description_found') else 'No'}")
        print(f"All Breadcrumbs Clickable (except last): {'Yes' if summary.get('all_breadcrumbs_clickable') else 'No'}")
        
        container = results.get('container', {})
        if container.get('found'):
            print(f"\nContainer Size: {container.get('width', 0)}x{container.get('height', 0)} px")
        
        # Print extracted text details
        title = results.get('title', {})
        if title.get('found'):
            print(f"\nExtracted Title Text: '{title.get('text', '')}'")
        
        description = results.get('description', {})
        if description.get('found'):
            desc_text = description.get('text', '')
            print(f"Extracted Description: '{desc_text[:100]}{'...' if len(desc_text) > 100 else ''}'")
        
        breadcrumbs = results.get('breadcrumbs', {})
        if breadcrumbs.get('found'):
            print(f"\nBreadcrumb Levels: {breadcrumbs.get('total_levels', 0)}")
            for level in breadcrumbs.get('levels', []):
                print(f"  Level {level.get('level')}: '{level.get('text')}' - Clickable: {level.get('is_clickable')}, Last: {level.get('is_last')}")
                if level.get('href'):
                    print(f"    → Link: {level.get('href')}")

