"""
Comprehensive Home Page Validator for Solidigm Website
Validates all home page components including Navigation, Carousel, Featured Products,
Product Cards, Article List, Blade Components, Tile List, Search, and Footer
"""
import time
from typing import Dict, List
from playwright.sync_api import Page
from navigation_validator import NavigationValidator
from blade_component_validator import BladeComponentValidator
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
            
            # Product Cards - Not present on homepage, skipping
            # print("\n" + "="*100)
            # print("COMPONENT 4: PRODUCT CARDS")
            # print("="*100)
            product_cards = {'component_exists': False, 'card_count': 0, 'cards': []}
            
            print("\n" + "="*100)
            print("COMPONENT 5: ARTICLE LIST")
            print("="*100)
            article_list = article_list_validator.validate_article_list()
            
            print("\n" + "="*100)
            print("COMPONENT 6: BLADE COMPONENTS")
            print("="*100)
            blade_components = self._validate_blade_components()
            
            print("\n" + "="*100)
            print("COMPONENT 7: TILE LIST")
            print("="*100)
            tile_list = self._validate_tile_list()
            
            print("\n" + "="*100)
            print("COMPONENT 8: SEARCH")
            print("="*100)
            search_component = self._validate_search_component()
            
            print("\n" + "="*100)
            print("COMPONENT 9: FOOTER")
            print("="*100)
            footer = self._validate_footer()
            
            # Compile all results first
            results_dict = {
                'url': self.base_url,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                'navigation': navigation_results,
                'carousel': carousel_results,
                'featured_products': featured_products,
                'product_cards': product_cards,
                'article_list': article_list,
                'blade_components': blade_components,
                'tile_list': tile_list,
                'search': search_component,
                'footer': footer
            }
            
            # Generate summary from the compiled results
            results_dict['summary'] = self._generate_summary(results_dict)
            self.results = results_dict
            
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
        validator = BladeComponentValidator(self.page)
        return validator.validate_blade_components()
    
    def _validate_tile_list(self) -> Dict:
        """Validate Tile List component (tile list with support tiles)"""
        print("\n[INFO] Validating Tile List component...")
        
        results = {
            'component_exists': False,
            'tile_count': 0,
            'big_container': {},
            'tiles': []
        }
        
        try:
            # Find the big container (.cmp-container that contains the tile list)
            big_container = self.page.locator('.cmp-container').filter(has=self.page.locator('.tilelistv2, .cmp-tilelist__support')).first
            
            if big_container.count() == 0:
                print("   [INFO] Tile List component not found")
                return results
            
                results['component_exists'] = True
            print(f"   [OK] Tile List component found")
            
            # Extract big container details
            try:
                container_info = big_container.evaluate("""
                    (el) => {
                        const rect = el.getBoundingClientRect();
                        const styles = window.getComputedStyle(el);
                        const inlineStyle = el.getAttribute('style') || '';
                        let bgColor = '';
                        
                        // Check inline style first
                        if (inlineStyle.includes('background-color')) {
                            const match = inlineStyle.match(/background-color:\\s*([^;]+)/);
                            if (match) bgColor = match[1].trim();
                        }
                        // Fall back to computed style
                        if (!bgColor) {
                            bgColor = styles.backgroundColor || '';
                        }
                        
                        return {
                            id: el.id || '',
                            width: rect.width,
                            height: rect.height,
                            background_color: bgColor
                        };
                    }
                """)
                if container_info:
                    results['big_container'] = {
                        'id': container_info.get('id', ''),
                        'width': container_info.get('width', 0),
                        'height': container_info.get('height', 0),
                        'background_color': container_info.get('background_color', '')
                    }
                    print(f"   [OK] Big container: {container_info.get('width', 0):.2f}x{container_info.get('height', 0):.2f}, bg: {container_info.get('background_color', '')[:20]}")
            except Exception as e:
                print(f"   [WARNING] Could not extract big container details: {str(e)}")
            
            # Find tile list container
            tile_list = big_container.locator('.tilelistv2, .cmp-tilelist__support, [class*="tilelist"]').first
            
            # Scroll to component
            try:
                big_container.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except:
                pass
            
            # Find all tiles - use specific selector for actual tile cards (anchor tags with support-tile class)
            # Only get <a> tags that are actual tile cards
            tiles = tile_list.locator('a.cmp-tilelist__support-tile')
            tile_count = tiles.count()
            
            # If no tiles found with that selector, try the broader selector but filter
            if tile_count == 0:
                all_elements = tile_list.locator('.cmp-tilelist__support-tile')
                tile_count = all_elements.count()
                print(f"   [INFO] Found {tile_count} elements, filtering for actual tile cards...")
            else:
                print(f"   [OK] Found {tile_count} tile cards")
            
            # Validate each tile
            valid_tiles = []
            for i in range(tile_count):
                tile = tiles.nth(i) if tile_count > 0 else all_elements.nth(i)
                
                # Quick check: ensure it's an actual tile card (has href or contains expected structure)
                try:
                    # Check if element has href (anchor tag) or contains title/icon
                    has_href = bool(tile.get_attribute('href') or '')
                    has_title_element = tile.locator('.cmp-tilelist__support-title').count() > 0
                    has_icon_element = tile.locator('.cmp-tilelist__support-icon').count() > 0
                    
                    # Only process if it looks like an actual tile card
                    if has_href or has_title_element or has_icon_element:
                        tile_data = self._validate_single_tile(tile, len(valid_tiles))
                        
                        # Only include tiles that have at least a title, icon, or link
                        has_title = bool(tile_data.get('title', {}).get('text', '').strip())
                        has_icon = bool(tile_data.get('icon', {}).get('url', ''))
                        has_link = bool(tile_data.get('link', {}).get('href', ''))
                        
                        if has_title or has_icon or has_link:
                            valid_tiles.append(tile_data)
                            print(f"      Tile {len(valid_tiles)}: {tile_data.get('title', {}).get('text', '')[:30] or 'No title'}")
                        else:
                            print(f"      [SKIP] Tile {i+1}: Empty tile (no title, icon, or link)")
                    else:
                        print(f"      [SKIP] Tile {i+1}: Not a valid tile card structure")
                except Exception as e:
                    print(f"      [WARNING] Error checking tile {i+1}: {str(e)}")
            
            results['tile_count'] = len(valid_tiles)
            results['tiles'] = valid_tiles
            
            if len(valid_tiles) < tile_count:
                print(f"   [INFO] Filtered {tile_count - len(valid_tiles)} invalid/empty tiles")
                
        except Exception as e:
            print(f"   [ERROR] Tile List validation failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _validate_single_tile(self, tile, index: int) -> Dict:
        """Validate a single tile in the tile list"""
        tile_data = {
            'index': index + 1,
            'container': {},
            'icon': {},
            'title': {},
            'link': {}
        }
        
        try:
            # Get tile container size and background color (the <a> tag itself)
            container_info = tile.evaluate("""
                (tile) => {
                    const rect = tile.getBoundingClientRect();
                    const styles = window.getComputedStyle(tile);
                    return {
                        width: rect.width,
                        height: rect.height,
                        background_color: styles.backgroundColor || ''
                    };
                }
            """)
            if container_info:
                tile_data['container'] = {
                    'width': container_info.get('width', 0),
                    'height': container_info.get('height', 0),
                    'background_color': container_info.get('background_color', '')
                }
            
            # Get icon (background-image) and its size
            icon_element = tile.locator('.cmp-tilelist__support-icon').first
            if icon_element.count() > 0:
                icon_info = icon_element.evaluate("""
                    (icon) => {
                        const styles = window.getComputedStyle(icon);
                        const bgImage = styles.backgroundImage;
                        let imageUrl = '';
                        if (bgImage && bgImage !== 'none') {
                            const match = bgImage.match(/url\\(['"]?(.*?)['"]?\\)/);
                            if (match) {
                                imageUrl = match[1];
                            }
                        }
                        // Also check inline style
                        if (!imageUrl && icon.style.backgroundImage) {
                            const match = icon.style.backgroundImage.match(/url\\(['"]?(.*?)['"]?\\)/);
                            if (match) {
                                imageUrl = match[1];
                            }
                        }
                        const rect = icon.getBoundingClientRect();
                        return {
                            url: imageUrl,
                            width: rect.width || icon.offsetWidth || 0,
                            height: rect.height || icon.offsetHeight || 0
                        };
                    }
                """)
                if icon_info:
                    tile_data['icon'] = {
                        'url': icon_info.get('url', ''),
                        'width': icon_info.get('width', 0),
                        'height': icon_info.get('height', 0)
                    }
            
            # Get title text and font styles (text color, text size)
            title_element = tile.locator('.cmp-tilelist__support-title, p').first
            if title_element.count() > 0:
                title_text = (title_element.text_content() or '').strip()
                tile_data['title']['text'] = title_text
                
                # Get font styles
                title_styles = title_element.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            lineHeight: styles.lineHeight
                        };
                    }
                """)
                if title_styles:
                    tile_data['title'].update({
                        'font_size': title_styles.get('fontSize', ''),
                        'font_color': title_styles.get('color', ''),
                        'font_family': title_styles.get('fontFamily', ''),
                        'font_weight': title_styles.get('fontWeight', ''),
                        'line_height': title_styles.get('lineHeight', '')
                    })
            
            # Get link (the tile itself is an <a> tag) and validate it's clickable and not broken
            href = tile.get_attribute('href') or ''
            target = tile.get_attribute('target') or '_self'
            
            # Check if tile is clickable
            is_clickable = False
            try:
                # Check if element is visible and enabled
                is_visible = tile.is_visible(timeout=500)
                is_enabled = True
                try:
                    disabled = tile.get_attribute('disabled')
                    is_enabled = disabled is None
                except:
                    pass
                is_clickable = is_visible and is_enabled and bool(href)
            except:
                pass
            
            tile_data['link']['is_clickable'] = is_clickable
            
            if href:
                tile_data['link']['href'] = href
                tile_data['link']['target'] = target
                
                # Validate link (should not navigate to broken link)
                if href and href != '#':
                    try:
                        from urllib.parse import urljoin
                        absolute_href = href if href.startswith('http') else urljoin(self.page.url, href)
                        response = self.page.request.get(absolute_href, timeout=3000)
                        tile_data['link']['status_code'] = response.status
                        tile_data['link']['is_valid'] = 200 <= response.status < 400
                        if not tile_data['link']['is_valid']:
                            print(f"      [WARNING] Tile {index+1} link is broken: {href} (Status: {response.status})")
                    except Exception as e:
                        tile_data['link']['status_code'] = 0
                        tile_data['link']['is_valid'] = False
                        print(f"      [WARNING] Tile {index+1} link validation failed: {str(e)}")
                else:
                    tile_data['link']['status_code'] = 0
                    tile_data['link']['is_valid'] = False
            else:
                tile_data['link']['status_code'] = 0
                tile_data['link']['is_valid'] = False
                tile_data['link']['is_clickable'] = False
                
        except Exception as e:
            print(f"      [ERROR] Tile {index+1} validation failed: {str(e)}")
            tile_data['error'] = str(e)
        
        return tile_data
    
    def _validate_search_component(self) -> Dict:
        """Validate Search component"""
        print("\n[INFO] Validating Search component...")
        
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
                
                # Get title font styles
                title_styles = title_element.evaluate("""
                    (title) => {
                        const styles = window.getComputedStyle(title);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            lineHeight: styles.lineHeight
                        };
                    }
                """)
                if title_styles:
                    results['title'].update({
                        'font_size': title_styles.get('fontSize', ''),
                        'font_color': title_styles.get('color', ''),
                        'font_family': title_styles.get('fontFamily', ''),
                        'font_weight': title_styles.get('fontWeight', ''),
                        'line_height': title_styles.get('lineHeight', '')
                    })
                print(f"      Title: {title_text}")
            
            # Validate search form
            form = search_component.locator('form.search-label').first
            if form.count() > 0:
                form_action = form.get_attribute('action') or ''
                form_method = form.get_attribute('method') or 'get'
                
                results['form']['action'] = form_action
                results['form']['method'] = form_method
                
                # Get input field details
                input_field = form.locator('input.search-input, input[type="text"]').first
                if input_field.count() > 0:
                    placeholder = input_field.get_attribute('placeholder') or ''
                    input_name = input_field.get_attribute('name') or ''
                    is_required = input_field.get_attribute('required') is not None
                    data_search_page = input_field.get_attribute('data-search-page') or ''
                    
                    results['form']['input'] = {
                        'placeholder': placeholder,
                        'name': input_name,
                        'required': is_required,
                        'data_search_page': data_search_page
                    }
                    print(f"      Form action: {form_action}")
                    print(f"      Placeholder: {placeholder}")
                
                # Get hidden input field
                hidden_input = form.locator('input[type="hidden"]').first
                if hidden_input.count() > 0:
                    hidden_name = hidden_input.get_attribute('name') or ''
                    hidden_value = hidden_input.get_attribute('value') or ''
                    results['form']['hidden_input'] = {
                        'name': hidden_name,
                        'value': hidden_value
                    }
            
            # Validate search suggestions
            suggestions = search_component.locator('.search-component__suggestions__suggestion, a[class*="suggestion"]')
            suggestion_count = suggestions.count()
            results['suggestion_count'] = suggestion_count
            
            print(f"      Found {suggestion_count} suggestions")
            
            for i in range(suggestion_count):
                suggestion = suggestions.nth(i)
                suggestion_text = (suggestion.text_content() or '').strip()
                suggestion_href = suggestion.get_attribute('href') or ''
                
                suggestion_data = {
                    'index': i + 1,
                    'text': suggestion_text,
                    'href': suggestion_href,
                    'is_valid': False,
                    'status_code': 0
                }
                
                # Validate link
                if suggestion_href and suggestion_href != '#':
                    try:
                        from urllib.parse import urljoin
                        absolute_href = suggestion_href if suggestion_href.startswith('http') else urljoin(self.page.url, suggestion_href)
                        response = self.page.request.get(absolute_href, timeout=3000)
                        suggestion_data['status_code'] = response.status
                        suggestion_data['is_valid'] = 200 <= response.status < 400
                    except Exception:
                        suggestion_data['is_valid'] = False
                
                results['suggestions'].append(suggestion_data)
                print(f"         Suggestion {i+1}: {suggestion_text}")
            
        except Exception as e:
            print(f"   [ERROR] Search component validation failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _validate_footer(self) -> Dict:
        """Validate Footer component"""
        print("\n[INFO] Validating Footer component...")
        
        results = {
            'component_exists': False,
            'container': {},
            'logo': {},
            'social_icons': [],
            'copyright': {},
            'sections': [],
            'trademark': {},
            'links_count': 0,
            'section_count': 0,
            'column_count': 0
        }
        
        try:
            # Try multiple selectors to find footer
            footer = None
            footer_selectors = [
                '.footer-content__main',
                '.footer-content',
                'footer',
                '[class*="footer"]'
            ]
            
            for selector in footer_selectors:
                footer = self.page.locator(selector).first
                if footer.count() > 0:
                    print(f"   [OK] Footer found using selector: {selector}")
                    break
            
            if footer is None or footer.count() == 0:
                print("   [INFO] Footer component not found")
                return results
            
                results['component_exists'] = True
                
            # Get container size
            try:
                container_info = footer.evaluate("""
                    (footer) => {
                        const rect = footer.getBoundingClientRect();
                        return {
                            width: rect.width,
                            height: rect.height
                        };
                    }
                """)
                if container_info:
                    results['container'] = {
                        'width': container_info.get('width', 0),
                        'height': container_info.get('height', 0)
                    }
                    print(f"      Container size: {container_info.get('width', 0):.2f}x{container_info.get('height', 0):.2f}")
            except Exception as e:
                print(f"      [WARNING] Could not extract container size: {str(e)}")
            
            # Scroll to footer
            try:
                footer.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except:
                pass
            
            # Validate logo
            logo = footer.locator('.footer-content__logo, a[class*="logo"]').first
            if logo.count() > 0:
                logo_href = logo.get_attribute('href') or ''
                logo_title = logo.get_attribute('title') or ''
                results['logo'] = {
                    'href': logo_href,
                    'title': logo_title
                }
                print(f"      Logo found: {logo_title}")
            
            # Validate social icons
            social_icons = footer.locator('.footer-content__social-icon, a[class*="social"]')
            icon_count = social_icons.count()
            results['social_icon_count'] = icon_count
            
            print(f"      Found {icon_count} social icons")
            
            for i in range(icon_count):
                icon = social_icons.nth(i)
                icon_href = icon.get_attribute('href') or ''
                icon_aria = icon.get_attribute('aria-label') or ''
                icon_target = icon.get_attribute('target') or '_self'
                
                # Check if link ends with valid Solidigm domains
                valid_domains = ['solidigm', 'solidigmtechnology', 'solidigmtechnologies']
                domain_valid = False
                domain_validation_message = ''
                
                if icon_href and icon_href.startswith('http'):
                    try:
                        from urllib.parse import urlparse
                        parsed_url = urlparse(icon_href)
                        domain = parsed_url.netloc.lower()
                        # Remove www. prefix if present
                        if domain.startswith('www.'):
                            domain = domain[4:]
                        # Check if domain ends with any of the valid domains
                        for valid_domain in valid_domains:
                            if domain.endswith(valid_domain) or domain == valid_domain:
                                domain_valid = True
                                domain_validation_message = f'Valid domain: {valid_domain}'
                                break
                        if not domain_valid:
                            domain_validation_message = f'Invalid domain: {domain} (should end with {", ".join(valid_domains)})'
                    except Exception as e:
                        domain_validation_message = f'Error parsing domain: {str(e)}'
                elif icon_href:
                    # Relative URL - skip domain validation
                    domain_validation_message = 'Relative URL (domain validation skipped)'
                    domain_valid = True  # Don't fail on relative URLs
                else:
                    domain_validation_message = 'No URL provided'
                
                icon_data = {
                    'index': i + 1,
                    'aria_label': icon_aria,
                    'href': icon_href,
                    'target': icon_target,
                    'is_valid': False,
                    'status_code': 0,
                    'domain_valid': domain_valid,
                    'domain_validation_message': domain_validation_message
                }
                
                # Validate link
                if icon_href and icon_href != '#' and not icon_href.startswith('#'):
                    try:
                        from urllib.parse import urljoin
                        absolute_href = icon_href if icon_href.startswith('http') else urljoin(self.page.url, icon_href)
                        response = self.page.request.get(absolute_href, timeout=3000)
                        icon_data['status_code'] = response.status
                        icon_data['is_valid'] = 200 <= response.status < 400
                    except Exception:
                        icon_data['is_valid'] = False
                
                results['social_icons'].append(icon_data)
                
                # Log domain validation result
                if domain_valid:
                    print(f"         Social icon {i+1} ({icon_aria}): Domain validation passed")
                else:
                    print(f"         [WARNING] Social icon {i+1} ({icon_aria}): {domain_validation_message}")
            
            # Validate copyright section
            copyright_section = footer.locator('.footer-content__copyright').first
            if copyright_section.count() > 0:
                copyright_text = (copyright_section.text_content() or '').strip()
                results['copyright']['text'] = copyright_text
                print(f"      Copyright text found")
            
            # Check if left column exists (logo, social icons, copyright)
            left_column = footer.locator('.footer-content__left').first
            has_left_column = left_column.count() > 0
            
            # Validate navigation sections (columns)
            nav_sections = footer.locator('nav')
            section_count = nav_sections.count()
            results['section_count'] = section_count
            
            # Column count: 1 (left column) + navigation sections
            column_count = (1 if has_left_column else 0) + section_count
            results['column_count'] = column_count
            
            print(f"      Found {section_count} navigation sections")
            if has_left_column:
                print(f"      Left column (logo, social icons, copyright) found - counted as Column 1")
            print(f"      Total columns: {column_count} (1 left column + {section_count} navigation sections)")
            
            for i in range(section_count):
                nav_section = nav_sections.nth(i)
                section_title = nav_section.locator('.footer-content__title, p.footer-content__title').first
                title_text = (section_title.text_content() or '').strip() if section_title.count() > 0 else ''
                
                # Get all links in this section - include nested links (like Cookie Preferences)
                # Get all anchor tags within the nav section
                all_links = nav_section.locator('a')
                links_data = []
                processed_links = set()  # To avoid duplicates based on text+href combination
                
                # Process all links found
                for j in range(all_links.count()):
                    link = all_links.nth(j)
                    link_text = (link.text_content() or '').strip()
                    link_href = link.get_attribute('href') or ''
                    link_target = link.get_attribute('target') or '_self'
                    
                    # Skip if no text (empty links)
                    if not link_text:
                        continue
                    
                    # Create a unique key for this link
                    link_key = f"{link_text}|{link_href}"
                    if link_key in processed_links:
                        continue
                    processed_links.add(link_key)
                    
                    # For links without href (like some Cookie Preferences links), keep as '#'
                    if not link_href:
                        link_href = '#'
                    
                    # Check if link is clickable
                    is_clickable = False
                    try:
                        is_visible = link.is_visible(timeout=500)
                        is_enabled = True
                        try:
                            disabled = link.get_attribute('disabled')
                            is_enabled = disabled is None
                        except:
                            pass
                        is_clickable = is_visible and is_enabled and bool(link_href)
                    except:
                        pass
                    
                    # Extract font styles
                    font_styles = {}
                    try:
                        link_font_styles = link.evaluate("""
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
                        if link_font_styles:
                            font_styles = link_font_styles
                    except Exception:
                        pass
                    
                    link_data = {
                        'text': link_text,
                        'href': link_href,
                        'target': link_target,
                        'is_clickable': is_clickable,
                        'is_valid': False,
                        'status_code': 0,
                        'font_styles': font_styles,
                        'font_size': font_styles.get('fontSize', ''),
                        'font_color': font_styles.get('color', '')
                    }
                    
                    # Validate link
                    if link_href and link_href != '#' and not link_href.startswith('#'):
                        try:
                            from urllib.parse import urljoin
                            absolute_href = link_href if link_href.startswith('http') else urljoin(self.page.url, link_href)
                            response = self.page.request.get(absolute_href, timeout=3000)
                            link_data['status_code'] = response.status
                            link_data['is_valid'] = 200 <= response.status < 400
                        except Exception:
                            link_data['is_valid'] = False
                    
                    links_data.append(link_data)
                
                # Column number: left column is 1, nav sections start from 2
                column_number = i + 2 if has_left_column else i + 1
                
                section_data = {
                    'index': column_number,  # Column number (2, 3, 4, etc.)
                    'section_index': i + 1,  # Section index within nav sections (1, 2, 3, etc.)
                    'title': title_text if title_text else '(No Title)',  # Show "(No Title)" for empty titles
                    'links': links_data,
                    'link_count': len(links_data)
                }
                
                results['sections'].append(section_data)
                results['links_count'] += len(links_data)
                title_display = title_text if title_text else '(No Title)'
                print(f"         Column {column_number} (Section {i+1}): {title_display} ({len(links_data)} links)")
            
            # Validate trademark section
            trademark_section = footer.locator('.footer-content__trademark').first
            if trademark_section.count() > 0:
                trademark_text = trademark_section.locator('.footer-content__text p').first
                if trademark_text.count() > 0:
                    results['trademark']['text'] = (trademark_text.text_content() or '').strip()
                
                trustarc_logo = trademark_section.locator('.footer-content__trustarc-logo').first
                if trustarc_logo.count() > 0:
                    trustarc_href = trustarc_logo.get_attribute('href') or ''
                    results['trademark']['trustarc_link'] = trustarc_href
                
                print(f"      Trademark section found")
            
            print(f"   [OK] Footer validated: {results['links_count']} total links in {section_count} sections")
                
        except Exception as e:
            print(f"   [ERROR] Footer validation failed: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _generate_summary(self, results_dict: Dict) -> Dict:
        """Generate validation summary from results dictionary"""
        # Get carousel count
        carousel_data = results_dict.get('carousel', {})
        carousel_count = carousel_data.get('carousel_count', 0)
        
        # Get featured products count - check nested structure
        featured_products_data = results_dict.get('featured_products', {})
        featured_products_count = 0
        if featured_products_data:
            # Check summary.total_cards first (most reliable)
            featured_summary = featured_products_data.get('summary', {})
            if featured_summary:
                featured_products_count = featured_summary.get('total_cards', 0)
            # Fallback to cards.card_count
            if not featured_products_count:
                cards_data = featured_products_data.get('cards', {})
                if cards_data:
                    featured_products_count = cards_data.get('card_count', 0)
            # Last fallback to direct card_count
            if not featured_products_count:
                featured_products_count = featured_products_data.get('card_count', 0) or featured_products_data.get('product_count', 0)
        
        # Get product cards count
        product_cards_data = results_dict.get('product_cards', {})
        product_cards_count = product_cards_data.get('card_count', 0)
        
        # Get article count - check nested structure
        article_list_data = results_dict.get('article_list', {})
        article_count = 0
        if article_list_data:
            # Check summary.total_cards first (most reliable)
            article_summary = article_list_data.get('summary', {})
            if article_summary:
                article_count = article_summary.get('total_cards', 0)
            # Fallback to cards.card_count
            if not article_count:
                cards_data = article_list_data.get('cards', {})
                if cards_data:
                    article_count = cards_data.get('card_count', 0)
            # Last fallback to direct card_count
            if not article_count:
                article_count = article_list_data.get('card_count', 0) or article_list_data.get('article_count', 0)
        
        # Get blade count
        blade_components_data = results_dict.get('blade_components', {})
        blade_count = blade_components_data.get('blade_count', 0)
        
        # Get footer status
        footer_data = results_dict.get('footer', {})
        footer_exists = footer_data.get('component_exists', False)
        
        # Get tile list count
        tile_list_data = results_dict.get('tile_list', {})
        tile_list_count = tile_list_data.get('tile_count', 0)
        
        return {
            'navigation_validated': 'navigation' in results_dict,
            'carousel_count': carousel_count,
            'featured_products_count': featured_products_count,
            'product_cards_count': product_cards_count,
            'article_count': article_count,
            'blade_count': blade_count,
            'tile_list_count': tile_list_count,
            'footer_exists': footer_exists
        }

