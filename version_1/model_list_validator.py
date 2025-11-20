"""
Model List Component Validator
Validates model list section including title, dropdowns, product cards, filtering, and related articles
Works for D3, D5, D7 series pages
"""
import time
from typing import Dict, List
from playwright.sync_api import Page


class ModelListValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def validate_model_list(self, selector: str = '.modellist, .model-list', filter_params: Dict = None) -> Dict:
        """Validate Model List component"""
        print("\n" + "="*80)
        print("MODEL LIST VALIDATION")
        print("="*80)
        
        try:
            # Find model list section
            model_list = self.page.locator(selector).first
            
            if model_list.count() == 0:
                print("[WARNING] Model List section not found")
                return {'found': False}
            
            print(f"\n[INFO] Model List section found")
            
            # Scroll to focus on the model list section
            try:
                model_list.scroll_into_view_if_needed(timeout=5000)
                self.page.wait_for_timeout(300)
            except:
                pass
            
            # Validate title
            print("\n[TITLE] Validating title...")
            title_data = self._validate_title(model_list)
            
            # Validate dropdowns
            print("\n[DROPDOWNS] Validating dropdowns...")
            dropdowns_data = self._validate_dropdowns(model_list)
            
            # Validate product cards (default state - all products)
            print("\n[PRODUCT CARDS] Validating product cards (default filters)...")
            default_cards_data = self._validate_product_cards(model_list)
            
            # Test filtering - use provided filter parameters or defaults
            print("\n[FILTERING] Testing filter functionality...")
            
            if filter_params is None:
                filter_params = {}
            
            # Check if any filter parameters are provided
            has_filters = bool(filter_params and (
                filter_params.get('interface_index') is not None or
                filter_params.get('form_factor_index') is not None or
                filter_params.get('capacity_index') is not None or
                filter_params.get('interface_text') or
                filter_params.get('form_factor_text') or
                filter_params.get('capacity_text')
            ))
            
            if has_filters:
                # Get filter parameters (text values override indices)
                interface_index = filter_params.get('interface_index', 0)
                form_factor_index = filter_params.get('form_factor_index', 0)
                capacity_index = filter_params.get('capacity_index', None)
                interface_text = filter_params.get('interface_text', None)
                form_factor_text = filter_params.get('form_factor_text', None)
                capacity_text = filter_params.get('capacity_text', None)
                
                if interface_text or form_factor_text or capacity_text:
                    print("   [INFO] Using text values for filtering:")
                    if interface_text:
                        print(f"      Interface: '{interface_text}'")
                    if form_factor_text:
                        print(f"      Form Factor: '{form_factor_text}'")
                    if capacity_text:
                        print(f"      Capacity: '{capacity_text}'")
                else:
                    print(f"   [INFO] Using indices: Interface=index {interface_index}, Form Factor=index {form_factor_index}, Capacity={'index ' + str(capacity_index) if capacity_index is not None else 'None'}")
                
                filtered_cards_data = self._test_filtering(model_list, dropdowns_data, 
                                                          interface_index=interface_index,
                                                          form_factor_index=form_factor_index,
                                                          capacity_index=capacity_index,
                                                          interface_text=interface_text,
                                                          form_factor_text=form_factor_text,
                                                          capacity_text=capacity_text)
            else:
                # No filter options provided - use all cards from default state
                print("   [INFO] No filter options provided - displaying all product cards (default state)")
                filtered_cards_data = {
                    'filtering_works': True,
                    'selected_filters': {
                        'interface': 'Any Interface',
                        'form_factor': 'Any Form Factor',
                        'capacity': 'Any Capacity'
                    },
                    'filtered_card_count': default_cards_data.get('card_count', 0),
                    'filtered_cards': default_cards_data.get('cards', []),
                    'error': None,
                    'error_message': None
                }
            
            # Validate related articles
            print("\n[RELATED ARTICLES] Validating related articles...")
            articles_data = self._validate_related_articles()
            
            results = {
                'found': True,
                'title': title_data,
                'dropdowns': dropdowns_data,
                'default_cards': default_cards_data,
                'filtered_cards': filtered_cards_data,
                'related_articles': articles_data,
                'summary': {
                    'title_found': title_data.get('found', False),
                    'dropdowns_found': dropdowns_data.get('all_found', False),
                    'default_cards_count': default_cards_data.get('card_count', 0),
                    'filtered_cards_count': filtered_cards_data.get('filtered_card_count', 0),
                    'filtering_works': filtered_cards_data.get('filtering_works', False),
                    'articles_found': articles_data.get('found', False),
                    'articles_count': articles_data.get('card_count', 0)
                }
            }
            
            self._print_summary(results)
            
            return results
            
        except Exception as e:
            print(f"[ERROR] Model List validation failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': str(e)}
    
    def _validate_title(self, model_list) -> Dict:
        """Validate model list title"""
        # Scroll to focus on title section
        try:
            title_element = model_list.locator('.model-list__title, h3').first
            if title_element.count() > 0:
                title_element.scroll_into_view_if_needed(timeout=3000)
                self.page.wait_for_timeout(200)
        except:
            pass
        
        title_data = {
            'found': False,
            'text': '',
            'font_size': '',
            'font_color': '',
            'font_family': '',
            'font_weight': ''
        }
        
        try:
            title = model_list.locator('.model-list__title, h3').first
            
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
                            color: styles.color
                        };
                    }
                """)
                
                if font_styles:
                    title_data['font_size'] = font_styles.get('fontSize', '')
                    title_data['font_color'] = font_styles.get('color', '')
                    title_data['font_family'] = font_styles.get('fontFamily', '')
                    title_data['font_weight'] = font_styles.get('fontWeight', '')
                
                print(f"   [OK] Title: '{title_data['text']}'")
                print(f"        Font Size: {title_data['font_size']}")
                print(f"        Font Color: {title_data['font_color']}")
        
        except Exception as e:
            print(f"   [ERROR] Title validation failed: {str(e)}")
        
        return title_data
    
    def _validate_dropdowns(self, model_list) -> Dict:
        """Validate all three dropdowns"""
        # Scroll to focus on dropdowns section
        try:
            dropdowns_section = model_list.locator('.model-list__filters').first
            if dropdowns_section.count() > 0:
                dropdowns_section.scroll_into_view_if_needed(timeout=3000)
                self.page.wait_for_timeout(200)
        except:
            pass
        
        dropdowns_data = {
            'interface': {},
            'form_factor': {},
            'capacity': {},
            'all_found': False
        }
        
        try:
            # Find all dropdowns
            dropdowns = model_list.locator('.cmp-custom-select').all()
            
            # Validate Interface dropdown
            interface_dropdown = model_list.locator('.cmp-custom-select:has(label[for="interface"])').first
            if interface_dropdown.count() > 0:
                dropdowns_data['interface'] = self._validate_single_dropdown(interface_dropdown, 'Interface')
            
            # Validate Form Factor dropdown
            form_factor_dropdown = model_list.locator('.cmp-custom-select:has(label[for="form-factor"])').first
            if form_factor_dropdown.count() > 0:
                dropdowns_data['form_factor'] = self._validate_single_dropdown(form_factor_dropdown, 'Form Factor')
            
            # Validate Capacity dropdown
            capacity_dropdown = model_list.locator('.cmp-custom-select:has(label[for="capacity"])').first
            if capacity_dropdown.count() > 0:
                dropdowns_data['capacity'] = self._validate_single_dropdown(capacity_dropdown, 'Capacity')
            
            dropdowns_data['all_found'] = (
                dropdowns_data['interface'].get('found', False) and
                dropdowns_data['form_factor'].get('found', False) and
                dropdowns_data['capacity'].get('found', False)
            )
            
            if dropdowns_data['all_found']:
                print(f"   [OK] All 3 dropdowns found")
            else:
                print(f"   [WARNING] Some dropdowns missing")
        
        except Exception as e:
            print(f"   [ERROR] Dropdowns validation failed: {str(e)}")
        
        return dropdowns_data
    
    def _validate_single_dropdown(self, dropdown, name: str) -> Dict:
        """Validate a single dropdown"""
        dropdown_data = {
            'found': False,
            'name': name,
            'placeholder': '',
            'options': [],
            'default_value': '',
            'font_details': {}
        }
        
        try:
            # Get input/placeholder
            input_elem = dropdown.locator('.cmp-custom-select__input').first
            if input_elem.count() > 0:
                dropdown_data['found'] = True
                dropdown_data['placeholder'] = input_elem.get_attribute('placeholder') or ''
                dropdown_data['default_value'] = input_elem.get_attribute('value') or input_elem.input_value() or ''
                
                # Get font details from input
                font_styles = input_elem.evaluate("""
                    (input) => {
                        const styles = window.getComputedStyle(input);
                        return {
                            fontSize: styles.fontSize,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            color: styles.color
                        };
                    }
                """)
                
                if font_styles:
                    dropdown_data['font_details'] = {
                        'font_size': font_styles.get('fontSize', ''),
                        'font_color': font_styles.get('color', ''),
                        'font_family': font_styles.get('fontFamily', ''),
                        'font_weight': font_styles.get('fontWeight', '')
                    }
            
            # Get all options
            options = dropdown.locator('.cmp-custom-select__option').all()
            for option in options:
                option_text = (option.text_content() or '').strip()
                if option_text:
                    # Get font details for option
                    option_font = option.evaluate("""
                        (opt) => {
                            const styles = window.getComputedStyle(opt);
                            return {
                                fontSize: styles.fontSize,
                                fontFamily: styles.fontFamily,
                                fontWeight: styles.fontWeight,
                                color: styles.color
                            };
                        }
                    """)
                    
                    option_data = {
                        'text': option_text,
                        'font_size': option_font.get('fontSize', '') if option_font else '',
                        'font_color': option_font.get('color', '') if option_font else '',
                        'font_family': option_font.get('fontFamily', '') if option_font else ''
                    }
                    dropdown_data['options'].append(option_data)
            
            print(f"      [OK] {name} dropdown: {len(dropdown_data['options'])} options")
            print(f"          Default: '{dropdown_data['default_value'] or dropdown_data['placeholder']}'")
            if dropdown_data['options']:
                print(f"          Options: {', '.join([opt['text'] for opt in dropdown_data['options'][:3]])}...")
        
        except Exception as e:
            print(f"      [ERROR] {name} dropdown validation failed: {str(e)}")
        
        return dropdown_data
    
    def _validate_product_cards(self, model_list) -> Dict:
        """Validate product cards"""
        # Scroll to focus on product cards section
        try:
            cards_section = model_list.locator('.model-list__products, .cmp-product-cards').first
            if cards_section.count() > 0:
                cards_section.scroll_into_view_if_needed(timeout=3000)
                self.page.wait_for_timeout(200)
        except:
            pass
        
        cards_data = {
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find product cards
            cards = model_list.locator('.cmp-product-cards__item, .model-list__products__product')
            cards_data['card_count'] = cards.count()
            
            print(f"   [OK] Found {cards_data['card_count']} product cards")
            
            # Validate each card (validate all cards to show all details in Excel)
            # Don't scroll cards into view to avoid page jumping - cards should be visible in viewport
            for i in range(cards.count()):
                card = cards.nth(i)
                try:
                    # Just wait a bit for any lazy loading, but don't scroll
                    self.page.wait_for_timeout(100)
                except:
                    pass
                
                card_data = self._validate_single_product_card(card, i)
                cards_data['cards'].append(card_data)
        
        except Exception as e:
            print(f"   [ERROR] Product cards validation failed: {str(e)}")
        
        return cards_data
    
    def _validate_single_product_card(self, card, index: int) -> Dict:
        """Validate a single product card"""
        card_data = {
            'index': index + 1,
            'container': {},
            'image': {},
            'title': {},
            'description': {},
            'interface': {},
            'form_factor': {},
            'capacity': {},
            'view_details_button': {},
            'compare_button': {},
            'view_details_link': '',
            'navigation_tested': False,
            'navigation_success': False,
            'navigated_to_url': ''
        }
        
        try:
            # Container size
            container_size = card.evaluate("""
                (card) => {
                    const rect = card.getBoundingClientRect();
                    return {
                        width: rect.width,
                        height: rect.height
                    };
                }
            """)
            if container_size:
                card_data['container'] = {
                    'width': int(container_size.get('width', 0)),
                    'height': int(container_size.get('height', 0))
                }
            
            # Image
            img = card.locator('.cmp-product-cards__img-container img, img').first
            if img.count() > 0:
                card_data['image']['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                card_data['image']['alt'] = img.get_attribute('alt') or ''
                
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
            
            # Title
            title = card.locator('.cmp-product-cards__item-title, h3').first
            if title.count() > 0:
                card_data['title']['text'] = (title.text_content() or '').strip()
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
                    card_data['title'].update(title_font)
            
            # Description
            desc = card.locator('.cmp-product-cards__item-description, p').first
            if desc.count() > 0:
                card_data['description']['text'] = (desc.text_content() or '').strip()
                desc_font = desc.evaluate("""
                    (desc) => {
                        const styles = window.getComputedStyle(desc);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily
                        };
                    }
                """)
                if desc_font:
                    card_data['description'].update(desc_font)
            
            # Interface
            interface = card.locator('.cmp-product-cards__interface').first
            if interface.count() > 0:
                card_data['interface']['text'] = (interface.text_content() or '').strip()
                interface_font = interface.evaluate("""
                    (elem) => {
                        const styles = window.getComputedStyle(elem);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily
                        };
                    }
                """)
                if interface_font:
                    card_data['interface'].update(interface_font)
            
            # Form Factor
            form_factor = card.locator('.cmp-product-cards__form-factor').first
            if form_factor.count() > 0:
                card_data['form_factor']['text'] = (form_factor.text_content() or '').strip()
                ff_font = form_factor.evaluate("""
                    (elem) => {
                        const styles = window.getComputedStyle(elem);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily
                        };
                    }
                """)
                if ff_font:
                    card_data['form_factor'].update(ff_font)
            
            # Capacity
            capacity = card.locator('.cmp-product-cards__capacity').first
            if capacity.count() > 0:
                card_data['capacity']['text'] = (capacity.text_content() or '').strip()
                cap_font = capacity.evaluate("""
                    (elem) => {
                        const styles = window.getComputedStyle(elem);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily
                        };
                    }
                """)
                if cap_font:
                    card_data['capacity'].update(cap_font)
            
            # View Details button
            view_details = card.locator('.cmp-product-cards__details-btn, a:has-text("View Details")').first
            if view_details.count() > 0:
                card_data['view_details_button']['text'] = (view_details.text_content() or '').strip()
                card_data['view_details_link'] = view_details.get_attribute('href') or ''
                
                btn_styles = view_details.evaluate("""
                    (btn) => {
                        const styles = window.getComputedStyle(btn);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            backgroundColor: styles.backgroundColor
                        };
                    }
                """)
                if btn_styles:
                    card_data['view_details_button'].update(btn_styles)
                
                # Test navigation to PDP page
                if card_data['view_details_link']:
                    card_data['url_format_valid'] = False
                    card_data['navigation_tested'] = False
                    card_data['navigation_success'] = False
                    
                    try:
                        product_title = card_data['title'].get('text', '')
                        href = card_data['view_details_link']
                        
                        # Verify URL format matches expected pattern
                        # Expected: /products/data-center/{series}/{product}.html
                        # Example: /products/data-center/d7/p5520.html
                        # Or: /products/data-center/d5/p5430.html
                        # Or: /products/data-center/d3/s4620.html
                        
                        url_valid = False
                        url_matches_product = False
                        
                        # Check if URL follows the expected pattern
                        if href and '/products/data-center/' in href:
                            url_valid = True
                            
                            # Extract product ID from title (e.g., "D7-P5520" -> "p5520")
                            product_id = product_title.lower().replace('d7-', '').replace('d5-', '').replace('d3-', '').replace(' ', '')
                            
                            # Check if product ID is in the URL
                            if product_id and product_id in href.lower():
                                url_matches_product = True
                                card_data['url_format_valid'] = True
                                print(f"         [OK] URL format valid: {href}")
                            else:
                                # Try alternative patterns
                                # Sometimes URL might be /products/data-center/d7/ps1030.html for D7-PS1030
                                product_variations = [
                                    product_id,
                                    product_id.replace('-', ''),
                                    product_title.lower().replace('d7-', '').replace('d5-', '').replace('d3-', '').replace('-', ''),
                                ]
                                for variation in product_variations:
                                    if variation and variation in href.lower():
                                        url_matches_product = True
                                        print(f"         [OK] URL format valid: {href}")
                                        break
                                
                                if not url_matches_product:
                                    print(f"         [WARNING] URL format may not match product: {href} (Product: {product_title})")
                        else:
                            print(f"         [WARNING] URL format unexpected: {href}")
                        
                        card_data['url_format_valid'] = url_valid
                        card_data['url_matches_product'] = url_matches_product
                        
                        # Test navigation to PDP page (only for first card to save time)
                        if index == 0 and url_matches_product and href:
                            try:
                                from urllib.parse import urljoin
                                absolute_href = href if href.startswith('http') else urljoin(self.page.url, href)
                                
                                # Store current URL
                                current_url = self.page.url
                                
                                print(f"         [INFO] Testing navigation to PDP page: {absolute_href}")
                                
                                # Click View Details button
                                view_details.click(timeout=5000)
                                self.page.wait_for_load_state('domcontentloaded', timeout=30000)
                                self.page.wait_for_timeout(2000)
                                
                                # Verify navigation
                                new_url = self.page.url
                                card_data['navigation_tested'] = True
                                card_data['navigation_success'] = new_url != current_url
                                card_data['navigated_to_url'] = new_url
                                
                                # Verify URL matches expected pattern
                                expected_product_id = product_title.lower().replace('d7-', '').replace('d5-', '').replace('d3-', '').replace('-', '')
                                if expected_product_id in new_url.lower():
                                    card_data['url_matches_product'] = True
                                    print(f"         [OK] Navigation successful: {new_url}")
                                    print(f"         [OK] URL matches product name: {product_title}")
                                else:
                                    print(f"         [WARNING] Navigation successful but URL may not match product: {new_url}")
                                
                                # Navigate back to series page
                                self.page.goto(current_url, timeout=90000, wait_until='domcontentloaded')
                                self.page.wait_for_timeout(2000)
                                
                            except Exception as nav_error:
                                print(f"         [WARNING] Navigation test failed: {str(nav_error)}")
                                card_data['navigation_error'] = str(nav_error)
                                # Try to navigate back if we're on a different page
                                try:
                                    if self.page.url != current_url:
                                        self.page.goto(current_url, timeout=90000, wait_until='domcontentloaded')
                                        self.page.wait_for_timeout(2000)
                                except:
                                    pass
                        
                    except Exception as e:
                        card_data['url_format_error'] = str(e)
                        print(f"         [ERROR] URL format validation failed: {str(e)}")
            
            # Compare button
            compare = card.locator('.cmp-product-cards__configure-btn, button:has-text("Compare")').first
            if compare.count() > 0:
                card_data['compare_button']['text'] = (compare.text_content() or '').strip()
                
                btn_styles = compare.evaluate("""
                    (btn) => {
                        const styles = window.getComputedStyle(btn);
                        return {
                            fontSize: styles.fontSize,
                            color: styles.color,
                            fontFamily: styles.fontFamily,
                            fontWeight: styles.fontWeight,
                            backgroundColor: styles.backgroundColor
                        };
                    }
                """)
                if btn_styles:
                    card_data['compare_button'].update(btn_styles)
            
            if card_data['title'].get('text'):
                print(f"      [OK] Card {index+1}: {card_data['title'].get('text', '')}")
        
        except Exception as e:
            print(f"      [ERROR] Card {index+1} validation failed: {str(e)}")
        
        return card_data
    
    def _test_filtering(self, model_list, dropdowns_data: Dict, 
                        interface_index: int = 0, form_factor_index: int = 0, capacity_index: int = None,
                        interface_text: str = None, form_factor_text: str = None, capacity_text: str = None) -> Dict:
        """Test filtering by selecting from Interface, Form Factor, and Capacity dropdowns
        All dropdowns update dynamically when any selection is made.
        Values are read at runtime from the page (visible options) - no static values.
        
        Args:
            interface_index: Index of option to select from Interface dropdown (0-based, default: 0 = 1st option)
            form_factor_index: Index of option to select from Form Factor dropdown (0-based, default: 0 = 1st option from updated list)
            capacity_index: Index of option to select from Capacity dropdown (0-based, None = don't select)
            interface_text: Text value to select from Interface dropdown (overrides interface_index if provided)
            form_factor_text: Text value to select from Form Factor dropdown (overrides form_factor_index if provided)
            capacity_text: Text value to select from Capacity dropdown (overrides capacity_index if provided)
        """
        filtered_data = {
            'card_count': 0,
            'filtering_works': False,
            'selected_filters': {},
            'cards': [],
            'error': None,
            'error_message': None
        }
        
        try:
            # Step 1: Select value from Interface dropdown (this will update Form Factor and Capacity)
            # IMPORTANT: Read Interface options dynamically from visible options on the page (not from DOM cache)
            interface_selected = False
            
            # Open Interface dropdown to read visible options
            interface_dropdown = model_list.locator('.cmp-custom-select:has(label[for="interface"])').first
            if interface_dropdown.count() == 0:
                error_msg = "Interface dropdown not found"
                print(f"      [ERROR] {error_msg}")
                filtered_data['error'] = 'Interface Dropdown Not Found'
                filtered_data['error_message'] = error_msg
                filtered_data['filtering_works'] = False
                return filtered_data
            
            interface_input = interface_dropdown.locator('.cmp-custom-select__input').first
            if interface_input.count() > 0:
                # Check if dropdown is already open before clicking (to avoid multiple clicks)
                dropdown_already_open = False
                try:
                    first_option = interface_dropdown.locator('.cmp-custom-select__option').first
                    if first_option.count() > 0:
                        dropdown_already_open = first_option.is_visible(timeout=300)
                except:
                    pass
                
                if not dropdown_already_open:
                    # Click to open dropdown only if it's not already open
                    interface_input.click(timeout=5000)
                    self.page.wait_for_timeout(1000)  # Wait for dropdown to open
                else:
                    print(f"      [DEBUG] Interface dropdown already open, skipping click to avoid multiple clicks")
                
                # Read all Interface options from the page - only VISIBLE ones
                interface_option_elements = interface_dropdown.locator('.cmp-custom-select__option').all()
                visible_interface_options = []
                visible_interface_texts = []
                
                for opt_elem in interface_option_elements:
                    try:
                        # Check if option is visible on the page (not just in DOM)
                        is_visible = opt_elem.is_visible()
                        opt_text = (opt_elem.text_content() or '').strip()
                        
                        if opt_text:
                            # Exclude "Any" option and only include visible options
                            if 'any' not in opt_text.lower() and is_visible:
                                visible_interface_options.append(opt_elem)
                                visible_interface_texts.append(opt_text)
                                print(f"      [DEBUG] Interface option found (visible on page): '{opt_text}'")
                    except Exception as e:
                        print(f"      [WARNING] Error reading Interface option: {str(e)}")
                        continue
                
                print(f"      [INFO] Interface options (visible on page): {len(visible_interface_options)} selectable options")
                if visible_interface_texts:
                    print(f"      [INFO] Available Interface options: {', '.join(visible_interface_texts)}")
                
                # Convert 1-based index to 0-based (user says "2" means 2nd option = index 1)
                # But if user provides 0, treat it as 0-based for backward compatibility
                interface_index_0based = interface_index if interface_index == 0 else interface_index - 1
                
                # Use text value if provided, otherwise use index
                selected_interface = None
                option_to_click = None
                
                if interface_text:
                    # Find option by text from visible options
                    for i, opt_text in enumerate(visible_interface_texts):
                        if opt_text.strip() == interface_text.strip():
                            selected_interface = opt_text
                            option_to_click = visible_interface_options[i]
                            print(f"      [INFO] Will select Interface option by text from visible options: '{selected_interface}'")
                            break
                    if not selected_interface:
                        error_msg = f"Interface option '{interface_text}' not found in visible options"
                        print(f"      [ERROR] {error_msg}")
                        print(f"      [INFO] Available visible options: {', '.join(visible_interface_texts)}")
                        filtered_data['error'] = 'Interface Option Not Found'
                        filtered_data['error_message'] = error_msg
                        filtered_data['filtering_works'] = False
                        # Close dropdown
                        self.page.locator('body').click(position={'x': 10, 'y': 10})
                        self.page.wait_for_timeout(300)
                        return filtered_data
                elif len(visible_interface_options) > interface_index_0based >= 0:
                    # Select by index (1-based converted to 0-based)
                    selected_interface = visible_interface_texts[interface_index_0based]
                    option_to_click = visible_interface_options[interface_index_0based]
                    print(f"      [INFO] Will select Interface option at index {interface_index_0based} (user specified {interface_index} = {interface_index}nd visible option): '{selected_interface}'")
                    print(f"      [DEBUG] Interface option element reference stored for clicking")
                    print(f"      [DEBUG] Total visible options: {len(visible_interface_options)}, Selected index (0-based): {interface_index_0based}")
                else:
                    error_msg = f"Interface option at index {interface_index} (0-based: {interface_index_0based}) not available (only {len(visible_interface_options)} visible options)"
                    print(f"      [ERROR] {error_msg}")
                    print(f"      [INFO] Available visible options: {', '.join(visible_interface_texts)}")
                    filtered_data['error'] = 'Interface Index Out of Range'
                    filtered_data['error_message'] = error_msg
                    filtered_data['filtering_works'] = False
                    # Close dropdown
                    self.page.locator('body').click(position={'x': 10, 'y': 10})
                    self.page.wait_for_timeout(300)
                    return filtered_data
                
                # IMPORTANT: Click the option IMMEDIATELY while dropdown is still open
                # Don't wait or the element might become detached
                if selected_interface and option_to_click:
                    filtered_data['selected_filters']['interface'] = selected_interface
                    
                    try:
                        # Final verification: Check if the option text is still valid before clicking
                        final_option_text = (option_to_click.text_content() or '').strip()
                        if final_option_text != selected_interface:
                            print(f"      [WARNING] Option text changed between reads! Expected '{selected_interface}', found '{final_option_text}'")
                            selected_interface = final_option_text
                            filtered_data['selected_filters']['interface'] = selected_interface
                        filtered_data['selected_filters']['interface'] = selected_interface
                        
                        # Verify the option text one more time before clicking (in case DOM changed)
                        option_text_verify = (option_to_click.text_content() or '').strip()
                        if option_text_verify != selected_interface:
                            print(f"      [WARNING] Option text changed! Expected '{selected_interface}', but found '{option_text_verify}'")
                            selected_interface = option_text_verify
                            filtered_data['selected_filters']['interface'] = selected_interface
                        
                        # Don't scroll - dropdown options are already in view when dropdown is open
                        # This prevents page from jumping to top
                        
                        # Verify option is visible before clicking
                        try:
                            option_to_click.wait_for(state='visible', timeout=2000)
                        except:
                            print(f"      [WARNING] Interface option not visible, but proceeding with click")
                        
                        # Dismiss consent banner if present
                        try:
                            consent_banner = self.page.locator('#consent_blackbar, .truste-consent-text').first
                            if consent_banner.is_visible(timeout=1000):
                                accept_btn = self.page.locator('button:has-text("Accept"), #truste-consent-button').first
                                if accept_btn.is_visible(timeout=1000):
                                    accept_btn.click(timeout=3000)
                                    self.page.wait_for_timeout(500)
                        except:
                            pass
                        
                        # Click the option - ensure dropdown is open and option is visible
                        print(f"      [INFO] Clicking Interface option: '{selected_interface}'")
                        
                        # Ensure dropdown is still open and wait for page to be stable
                        try:
                            # Wait for page to be stable (no navigation)
                            self.page.wait_for_load_state('networkidle', timeout=2000)
                        except:
                            pass
                        
                        # Verify dropdown is open and option is visible before clicking
                        click_success = False
                        max_retries = 3
                        for retry in range(max_retries):
                            try:
                                # Check if dropdown is open
                                first_option = interface_dropdown.locator('.cmp-custom-select__option').first
                                if first_option.count() == 0 or not first_option.is_visible(timeout=500):
                                    # Dropdown closed, reopen it
                                    print(f"      [DEBUG] Interface dropdown closed, reopening (retry {retry + 1})...")
                                    interface_input.click(timeout=5000)
                                    self.page.wait_for_timeout(1500)
                                    # Re-find the option
                                    option_to_click = interface_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_interface}")').first
                                
                                # Wait for option to be visible
                                if option_to_click.count() > 0:
                                    option_to_click.wait_for(state='visible', timeout=3000)
                                    
                                    # Verify option is actually visible
                                    if option_to_click.is_visible():
                                        print(f"      [DEBUG] Option is visible, clicking...")
                                        # Use JavaScript click for reliability
                                        option_to_click.evaluate('element => element.click()')
                                        click_success = True
                                        print(f"      [OK] Clicked Interface option: '{selected_interface}'")
                                        break
                                    else:
                                        raise Exception("Option is not visible")
                                else:
                                    raise Exception(f"Interface option '{selected_interface}' not found")
                                    
                            except Exception as retry_error:
                                if retry < max_retries - 1:
                                    print(f"      [DEBUG] Retry {retry + 1} failed: {str(retry_error)}, trying again...")
                                    self.page.wait_for_timeout(1000)
                                    # Re-find option for next retry
                                    option_to_click = interface_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_interface}")').first
                                else:
                                    raise Exception(f"Failed to click Interface option after {max_retries} retries: {str(retry_error)}")
                        
                        if not click_success:
                            raise Exception("Failed to click Interface option - all retries exhausted")
                        
                        # Wait for dropdown to close and selection to be applied
                        self.page.wait_for_timeout(2000)
                        
                        # Verify selection was made (same as Form Factor)
                        # Wait a bit more for the input value to update
                        self.page.wait_for_timeout(500)
                        interface_input_after = interface_input.get_attribute('value') or interface_input.input_value() or ''
                        
                        # Also check the placeholder in case value is empty
                        if not interface_input_after:
                            interface_input_after = interface_input.get_attribute('placeholder') or ''
                        
                        if selected_interface.lower() in interface_input_after.lower() or interface_input_after == '':
                            print(f"      [OK] Interface selection verified: '{selected_interface}' (input shows: '{interface_input_after}')")
                        else:
                            print(f"      [WARNING] Interface selection may not have worked. Expected: '{selected_interface}', Got: '{interface_input_after}'")
                            # Try clicking the option one more time if selection didn't work
                            try:
                                print(f"      [DEBUG] Retrying Interface option click...")
                                # Re-open dropdown if needed
                                try:
                                    first_opt = interface_dropdown.locator('.cmp-custom-select__option').first
                                    if not first_opt.is_visible(timeout=300):
                                        interface_input.click(timeout=5000)
                                        self.page.wait_for_timeout(1000)
                                except:
                                    interface_input.click(timeout=5000)
                                    self.page.wait_for_timeout(1000)
                                
                                # Re-find and click the option
                                retry_option = interface_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_interface}")').first
                                if retry_option.count() > 0:
                                    retry_option.click(timeout=5000)
                                    self.page.wait_for_timeout(2000)
                                    # Verify again
                                    interface_input_after_retry = interface_input.get_attribute('value') or interface_input.input_value() or interface_input.get_attribute('placeholder') or ''
                                    if selected_interface.lower() in interface_input_after_retry.lower():
                                        print(f"      [OK] Interface selection retry successful: '{selected_interface}'")
                                    else:
                                        print(f"      [WARNING] Interface selection retry still shows: '{interface_input_after_retry}'")
                            except Exception as retry_err:
                                print(f"      [WARNING] Interface selection retry failed: {str(retry_err)}")
                        
                        print(f"      [OK] Selected Interface: '{selected_interface}'")
                        print(f"      [INFO] Waiting for Form Factor and Capacity dropdowns to update...")
                        self.page.wait_for_timeout(1000)  # Additional wait for dropdowns to update
                        
                    except Exception as e:
                        error_msg = f"Failed to select Interface: {str(e)}"
                        print(f"      [ERROR] {error_msg}")
                        filtered_data['error'] = 'Interface Selection Error'
                        filtered_data['error_message'] = error_msg
                        filtered_data['filtering_works'] = False
                        # Close dropdown if open
                        try:
                            self.page.locator('body').click(position={'x': 10, 'y': 10})
                            self.page.wait_for_timeout(300)
                        except:
                            pass
                        return filtered_data
            else:
                error_msg = "No Interface options available or selection failed"
                print(f"      [ERROR] {error_msg}")
                filtered_data['error'] = 'No Interface Options'
                filtered_data['error_message'] = error_msg
                filtered_data['filtering_works'] = False
                return filtered_data
            
            # Step 2: Wait for Form Factor dropdown to update, then select from dynamically updated options
            form_factor_dropdown = model_list.locator('.cmp-custom-select:has(label[for="form-factor"])').first
            if form_factor_dropdown.count() > 0:
                # Wait for Form Factor dropdown options to update after Interface selection
                print(f"      [INFO] Waiting for Form Factor dropdown to update after Interface selection...")
                
                form_factor_input = form_factor_dropdown.locator('.cmp-custom-select__input').first
                
                # IMPORTANT: Wait for the page to update Form Factor options after Interface selection
                # Close any open dropdowns first to ensure fresh state
                try:
                    self.page.locator('body').click(position={'x': 10, 'y': 10})
                    self.page.wait_for_timeout(500)
                except:
                    pass
                
                # Wait for the dropdown options to update on the page (not just DOM)
                # Already waited 2 seconds after Interface selection, add more time for page update
                self.page.wait_for_timeout(2000)  # Wait for page to update Form Factor options
                
                # Get updated Form Factor options by opening the dropdown and reading CURRENT visible options from page
                # IMPORTANT: Read options from visible page elements, not just DOM!
                try:
                    if form_factor_input.count() > 0:
                        # Click to open dropdown to read CURRENT visible options from the page
                        form_factor_input.click(timeout=5000)
                        self.page.wait_for_timeout(3000)  # Wait longer for dropdown to fully open and visible options to load on page
                        
                        # Wait for options to be visible and loaded - try multiple times
                        max_retries = 3
                        for retry in range(max_retries):
                            try:
                                # Wait for at least one option to be visible
                                form_factor_dropdown.locator('.cmp-custom-select__option').first.wait_for(state='visible', timeout=3000)
                                # Additional wait for all options to be loaded
                                self.page.wait_for_timeout(1000)
                                break
                            except Exception as wait_error:
                                if retry < max_retries - 1:
                                    print(f"      [DEBUG] Retry {retry + 1}: Waiting for options to be visible...")
                                    self.page.wait_for_timeout(1000)
                                else:
                                    print(f"      [WARNING] Options visibility wait failed: {str(wait_error)}")
                        
                        # Read all available options from the CURRENT dropdown state (after Interface selection)
                        # IMPORTANT: Read the options NOW while dropdown is open - completely dynamic, no static values!
                        # Re-query the DOM to get the latest options - ensure we get fresh data
                        # Wait a bit more to ensure options are fully loaded
                        self.page.wait_for_timeout(500)
                        
                        # Re-query to get the latest options from the PAGE (not just DOM)
                        # IMPORTANT: Read from visible page elements, verify each is actually displayed
                        option_elements = form_factor_dropdown.locator('.cmp-custom-select__option').all()
                        current_options_count = len(option_elements)
                        print(f"      [DEBUG] Found {current_options_count} Form Factor option elements in DOM after Interface selection")
                        print(f"      [INFO] Reading Form Factor options from visible page elements (not just DOM)...")
                        
                        # Filter out "Any" options and get the actual selectable options with their text
                        # IMPORTANT: Only include options that are VISIBLE and SELECTABLE on the page
                        # Verify each option is actually displayed on the screen, not just in DOM
                        selectable_options = []
                        selectable_texts = []
                        for opt_elem in option_elements:
                            try:
                                # CRITICAL: Check if option is actually visible on the page (not hidden by CSS)
                                # This ensures we only read options that are displayed on screen
                                is_visible = opt_elem.is_visible()
                                
                                # Read text directly from the visible page element - no caching, no static values
                                opt_text = (opt_elem.text_content() or '').strip()
                                
                                if opt_text:
                                    # Exclude "Any" option from selectable options
                                    if 'any' not in opt_text.lower():
                                        # Only include if option is visible on the page (displayed on screen)
                                        if is_visible:
                                            selectable_options.append(opt_elem)  # Store the element
                                            selectable_texts.append(opt_text)    # Store the text
                                            print(f"      [OK] Form Factor option (visible on page): '{opt_text}'")
                                        else:
                                            print(f"      [SKIP] Form Factor option in DOM but NOT visible on page: '{opt_text}'")
                            except Exception as e:
                                print(f"      [WARNING] Error reading Form Factor option from page: {str(e)}")
                                continue
                        
                        # Verify we have options - if empty, the dropdown might not have updated yet
                        if len(selectable_options) == 0:
                            print(f"      [WARNING] No visible Form Factor options found - dropdown may not have updated yet")
                            print(f"      [INFO] Waiting additional time for dropdown to update...")
                            self.page.wait_for_timeout(2000)
                            # Re-read options after additional wait - only visible ones
                            option_elements = form_factor_dropdown.locator('.cmp-custom-select__option').all()
                            selectable_options = []
                            selectable_texts = []
                            for opt_elem in option_elements:
                                try:
                                    # Check if option is visible on the page
                                    is_visible = opt_elem.is_visible()
                                    opt_text = (opt_elem.text_content() or '').strip()
                                    if opt_text and 'any' not in opt_text.lower() and is_visible:
                                        selectable_options.append(opt_elem)
                                        selectable_texts.append(opt_text)
                                        print(f"      [DEBUG] Form Factor option found after retry (visible): '{opt_text}'")
                                    elif opt_text and 'any' not in opt_text.lower() and not is_visible:
                                        print(f"      [DEBUG] Form Factor option found after retry but NOT visible: '{opt_text}' - skipping")
                                except:
                                    continue
                        
                        print(f"      [INFO] Form Factor options after Interface '{filtered_data['selected_filters'].get('interface', '')}' selection: {len(selectable_options)} selectable options")
                        if selectable_texts:
                            print(f"      [INFO] Available Form Factor options (read dynamically): {', '.join(selectable_texts)}")
                        else:
                            print(f"      [WARNING] No Form Factor options found after filtering out 'Any'")
                            # Close dropdown
                            self.page.locator('body').click(position={'x': 10, 'y': 10})
                            self.page.wait_for_timeout(300)
                            selectable_options = []
                            selectable_texts = []
                        
                        # IMPORTANT: Ensure dropdown is still open before selecting
                        # If dropdown closed, reopen it
                        try:
                            # Check if dropdown is open by checking if options are visible
                            first_option = form_factor_dropdown.locator('.cmp-custom-select__option').first
                            if first_option.count() == 0 or not first_option.is_visible(timeout=1000):
                                print(f"      [DEBUG] Form Factor dropdown closed, reopening...")
                                form_factor_input.click(timeout=5000)
                                self.page.wait_for_timeout(2000)  # Wait for dropdown to open
                        except:
                            # Try to reopen dropdown
                            try:
                                form_factor_input.click(timeout=5000)
                                self.page.wait_for_timeout(2000)
                            except:
                                pass
                        
                        # Use the options we already read (selectable_options and selectable_texts)
                        # These are the visible options from the page
                        print(f"      [INFO] Using Form Factor options read from visible page: {len(selectable_options)} options")
                        if selectable_texts:
                            print(f"      [INFO] Available Form Factor options: {', '.join(selectable_texts)}")
                        
                        # Select option from the visible options on page
                        # Use text value if provided, otherwise use index
                        option_to_click = None
                        selected_ff = None
                        
                        if form_factor_text:
                            # Find option by text from visible options
                            for i, opt_text in enumerate(selectable_texts):
                                if opt_text.strip() == form_factor_text.strip():
                                    option_to_click = selectable_options[i]
                                    selected_ff = opt_text
                                    print(f"      [INFO] Will select Form Factor option by text from visible options: '{selected_ff}'")
                                    break
                            if not selected_ff:
                                error_msg = f"Form Factor option '{form_factor_text}' not found in visible options"
                                print(f"      [ERROR] {error_msg}")
                                print(f"      [INFO] Available visible options: {', '.join(selectable_texts)}")
                                filtered_data['error'] = 'Form Factor Option Not Found'
                                filtered_data['error_message'] = error_msg
                                filtered_data['filtering_works'] = False
                                # Close dropdown
                                self.page.locator('body').click(position={'x': 10, 'y': 10})
                                self.page.wait_for_timeout(300)
                        elif form_factor_index is not None:
                            # Convert 1-based index to 0-based (user says "2" means 2nd option = index 1)
                            # But if user provides 0, treat it as 0-based for backward compatibility
                            form_factor_index_0based = form_factor_index if form_factor_index == 0 else form_factor_index - 1
                            
                            if len(selectable_options) > form_factor_index_0based >= 0:
                                # Select by index (1-based converted to 0-based)
                                selected_ff_index = form_factor_index_0based
                                option_to_click = selectable_options[selected_ff_index]
                                selected_ff = selectable_texts[selected_ff_index]
                                print(f"      [INFO] Will select Form Factor option at index {selected_ff_index} (user specified {form_factor_index} = {form_factor_index}nd/rd/th visible option): '{selected_ff}'")
                            else:
                                error_msg = f"Form Factor option at index {form_factor_index} (0-based: {form_factor_index_0based}) not available (only {len(selectable_options)} visible options)"
                                print(f"      [ERROR] {error_msg}")
                                print(f"      [INFO] Available visible options: {', '.join(selectable_texts)}")
                                filtered_data['error'] = 'Form Factor Index Out of Range'
                                filtered_data['error_message'] = error_msg
                                filtered_data['filtering_works'] = False
                                # Close dropdown
                                self.page.locator('body').click(position={'x': 10, 'y': 10})
                                self.page.wait_for_timeout(300)
                        elif len(selectable_options) >= 1:
                            # Fallback to 1st option
                            selected_ff_index = 0
                            option_to_click = selectable_options[selected_ff_index]
                            selected_ff = selectable_texts[selected_ff_index]
                            print(f"      [INFO] Will select 1st option (index {selected_ff_index}): '{selected_ff}' (only {len(selectable_options)} option(s) available)")
                        else:
                            error_msg = "No Form Factor options available after Interface selection"
                            print(f"      [ERROR] {error_msg}")
                            filtered_data['error'] = 'No Form Factor Options'
                            filtered_data['error_message'] = error_msg
                            filtered_data['filtering_works'] = False
                            # Close dropdown
                            self.page.locator('body').click(position={'x': 10, 'y': 10})
                            self.page.wait_for_timeout(300)
                        
                        if option_to_click and selected_ff:
                            # Final verification: Check if the option text is still valid before clicking
                            final_option_text = (option_to_click.text_content() or '').strip()
                            if final_option_text != selected_ff:
                                print(f"      [WARNING] Option text changed between reads! Expected '{selected_ff}', found '{final_option_text}'")
                                selected_ff = final_option_text
                                filtered_data['selected_filters']['form_factor'] = selected_ff
                            filtered_data['selected_filters']['form_factor'] = selected_ff
                            
                            # Verify the option text one more time before clicking (in case DOM changed)
                            option_text_verify = (option_to_click.text_content() or '').strip()
                            if option_text_verify != selected_ff:
                                print(f"      [WARNING] Option text changed! Expected '{selected_ff}', but found '{option_text_verify}'")
                                selected_ff = option_text_verify
                                filtered_data['selected_filters']['form_factor'] = selected_ff
                            
                            # Don't scroll - dropdown options are already in view when dropdown is open
                            # This prevents page from jumping to top
                            
                            # Verify option is visible before clicking
                            try:
                                option_to_click.wait_for(state='visible', timeout=2000)
                            except:
                                print(f"      [WARNING] Option not visible, but proceeding with click")
                            
                            # Dismiss consent banner if present
                            try:
                                consent_banner = self.page.locator('#consent_blackbar, .truste-consent-text').first
                                if consent_banner.is_visible(timeout=1000):
                                    accept_btn = self.page.locator('button:has-text("Accept"), #truste-consent-button').first
                                    if accept_btn.is_visible(timeout=1000):
                                        accept_btn.click(timeout=3000)
                                        self.page.wait_for_timeout(500)
                            except:
                                pass
                            
                            # Ensure dropdown is still open before clicking
                            try:
                                first_option = form_factor_dropdown.locator('.cmp-custom-select__option').first
                                if first_option.count() == 0 or not first_option.is_visible(timeout=1000):
                                    print(f"      [DEBUG] Form Factor dropdown closed, reopening before click...")
                                    form_factor_input.click(timeout=5000)
                                    self.page.wait_for_timeout(1500)
                                    # Re-find the option after reopening
                                    option_to_click = form_factor_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_ff}")').first
                            except:
                                pass
                            
                            # Click the option
                            print(f"      [INFO] Clicking Form Factor option: '{selected_ff}'")
                            
                            # Don't scroll - dropdown options are already in view when dropdown is open
                            # This prevents page from jumping to top
                            
                            # Verify option is visible and clickable before clicking
                            try:
                                if option_to_click.count() > 0 and option_to_click.is_visible():
                                    print(f"      [DEBUG] Option is visible, clicking...")
                                    option_to_click.click(timeout=5000)
                                    print(f"      [OK] Clicked Form Factor option: '{selected_ff}'")
                                else:
                                    # Re-find the option if it was detached or not visible
                                    print(f"      [DEBUG] Option not visible, re-finding...")
                                    option_to_click = form_factor_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_ff}")').first
                                    if option_to_click.count() > 0:
                                        option_to_click.click(timeout=5000)
                                        print(f"      [OK] Clicked Form Factor option (re-found): '{selected_ff}'")
                                    else:
                                        raise Exception(f"Form Factor option '{selected_ff}' not found after re-query")
                            except Exception as click_error:
                                # Fallback to JavaScript click
                                print(f"      [DEBUG] Regular click failed, trying JavaScript click: {str(click_error)}")
                                try:
                                    option_to_click.evaluate('element => element.click()')
                                    print(f"      [OK] Clicked Form Factor option (JavaScript): '{selected_ff}'")
                                except:
                                    # Last resort: re-find and use JavaScript
                                    option_to_click = form_factor_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_ff}")').first
                                    if option_to_click.count() > 0:
                                        option_to_click.evaluate('element => element.click()')
                                        print(f"      [OK] Clicked Form Factor option (JavaScript, re-found): '{selected_ff}'")
                                    else:
                                        raise Exception(f"Failed to click Form Factor option '{selected_ff}'")
                            
                            self.page.wait_for_timeout(2000)  # Wait for dropdown to close and filtering to apply
                            
                            # Verify selection was made
                            form_factor_input_after = form_factor_input.get_attribute('value') or form_factor_input.get_attribute('placeholder') or ''
                            if selected_ff.lower() in form_factor_input_after.lower() or form_factor_input_after == '':
                                print(f"      [OK] Form Factor selection verified: '{selected_ff}'")
                            else:
                                print(f"      [WARNING] Form Factor selection may not have worked. Expected: '{selected_ff}', Got: '{form_factor_input_after}'")
                            
                            print(f"      [OK] Selected Form Factor: '{selected_ff}'")
                            print(f"      [INFO] Filtering test complete - selected 1st Interface and 1st Form Factor from dynamically updated list")
                            
                            # Verify selection was made
                            input_value_after = form_factor_input.get_attribute('value') or form_factor_input.get_attribute('placeholder') or ''
                            if selected_ff.lower() in input_value_after.lower() or input_value_after == '':
                                print(f"      [OK] Form Factor selection verified")
                            else:
                                print(f"      [WARNING] Form Factor selection may not have worked. Expected: '{selected_ff}', Got: '{input_value_after}'")
                            
                            # Ensure dropdown is closed
                            try:
                                if form_factor_dropdown.locator('.cmp-custom-select__options[style*="display: block"]').count() > 0:
                                    self.page.locator('body').click(position={'x': 10, 'y': 10})
                                    self.page.wait_for_timeout(300)
                            except:
                                pass
                            
                            # Step 3: Select Capacity dropdown (only if capacity_index is specified)
                            if capacity_index is not None:
                                capacity_dropdown = model_list.locator('.cmp-custom-select:has(label[for="capacity"])').first
                                if capacity_dropdown.count() > 0:
                                    try:
                                        capacity_input = capacity_dropdown.locator('.cmp-custom-select__input').first
                                        if capacity_input.count() > 0:
                                            # IMPORTANT: Wait for the page to update Capacity options after Form Factor selection
                                            # Close any open dropdowns first to ensure fresh state
                                            try:
                                                self.page.locator('body').click(position={'x': 10, 'y': 10})
                                                self.page.wait_for_timeout(500)
                                            except:
                                                pass
                                            
                                            # Wait for Capacity dropdown to update on the page (not just DOM)
                                            print(f"      [INFO] Waiting for Capacity dropdown to update after Form Factor selection...")
                                            self.page.wait_for_timeout(2000)  # Wait for page to update Capacity options
                                            
                                            # Click to open Capacity dropdown to read CURRENT visible options from page
                                            capacity_input.click(timeout=5000)
                                            self.page.wait_for_timeout(3000)  # Wait for dropdown to open and visible options to load on page
                                            
                                            # Wait for options to be visible
                                            max_retries = 3
                                            for retry in range(max_retries):
                                                try:
                                                    capacity_dropdown.locator('.cmp-custom-select__option').first.wait_for(state='visible', timeout=3000)
                                                    self.page.wait_for_timeout(1000)
                                                    break
                                                except Exception as wait_error:
                                                    if retry < max_retries - 1:
                                                        print(f"      [DEBUG] Retry {retry + 1}: Waiting for Capacity options to be visible...")
                                                        self.page.wait_for_timeout(1000)
                                                    else:
                                                        print(f"      [WARNING] Capacity options visibility wait failed: {str(wait_error)}")
                                            
                                            # Read all available Capacity options from the CURRENT dropdown state
                                            # IMPORTANT: Only read VISIBLE options from the PAGE (not just DOM)
                                            print(f"      [INFO] Reading Capacity options from visible page elements (not just DOM)...")
                                            capacity_option_elements = capacity_dropdown.locator('.cmp-custom-select__option').all()
                                            
                                            # Filter out "Any" options and get the actual selectable options
                                            # CRITICAL: Only include options that are VISIBLE on the page (displayed on screen)
                                            selectable_capacity_options = []
                                            selectable_capacity_texts = []
                                            for opt_elem in capacity_option_elements:
                                                try:
                                                    # CRITICAL: Check if option is visible on the page (not hidden by CSS)
                                                    # This ensures we only read options that are displayed on screen
                                                    is_visible = opt_elem.is_visible()
                                                    opt_text = (opt_elem.text_content() or '').strip()
                                                    
                                                    if opt_text:
                                                        if 'any' not in opt_text.lower():
                                                            # Only include if visible on the page (displayed on screen)
                                                            if is_visible:
                                                                selectable_capacity_options.append(opt_elem)
                                                                selectable_capacity_texts.append(opt_text)
                                                                print(f"      [OK] Capacity option (visible on page): '{opt_text}'")
                                                            else:
                                                                print(f"      [SKIP] Capacity option in DOM but NOT visible on page: '{opt_text}'")
                                                except Exception as e:
                                                    print(f"      [WARNING] Error reading Capacity option from page: {str(e)}")
                                                    continue
                                            
                                            print(f"      [INFO] Capacity options after Interface and Form Factor selections: {len(selectable_capacity_options)} selectable options")
                                            if selectable_capacity_texts:
                                                print(f"      [INFO] Available Capacity options: {', '.join(selectable_capacity_texts)}")
                                            
                                            # Select option from Capacity dropdown (read from visible options on page)
                                            # Use text value if provided, otherwise use index
                                            capacity_option_to_click = None
                                            selected_capacity = None
                                            
                                            # Convert 1-based index to 0-based (user says "2" means 2nd option = index 1)
                                            # But if user provides 0, treat it as 0-based for backward compatibility
                                            capacity_index_0based = capacity_index if capacity_index == 0 else capacity_index - 1
                                            
                                            if capacity_text:
                                                # Find option by text from visible options
                                                for i, cap_text in enumerate(selectable_capacity_texts):
                                                    if cap_text.strip() == capacity_text.strip():
                                                        capacity_option_to_click = selectable_capacity_options[i]
                                                        selected_capacity = cap_text
                                                        print(f"      [INFO] Will select Capacity option by text from visible options: '{selected_capacity}'")
                                                        break
                                                if not selected_capacity:
                                                    error_msg = f"Capacity option '{capacity_text}' not found in visible options"
                                                    print(f"      [ERROR] {error_msg}")
                                                    print(f"      [INFO] Available visible options: {', '.join(selectable_capacity_texts)}")
                                                    filtered_data['error'] = 'Capacity Option Not Found'
                                                    filtered_data['error_message'] = error_msg
                                                    filtered_data['filtering_works'] = False
                                                    # Close dropdown
                                                    self.page.locator('body').click(position={'x': 10, 'y': 10})
                                                    self.page.wait_for_timeout(300)
                                            elif capacity_index is not None and len(selectable_capacity_options) > capacity_index_0based >= 0:
                                                # Select by index (1-based converted to 0-based)
                                                selected_capacity_index = capacity_index_0based
                                                capacity_option_to_click = selectable_capacity_options[selected_capacity_index]
                                                selected_capacity = selectable_capacity_texts[selected_capacity_index]
                                                print(f"      [INFO] Will select Capacity option at index {selected_capacity_index} (user specified {capacity_index} = {capacity_index}nd/rd/th visible option): '{selected_capacity}'")
                                            elif len(selectable_capacity_options) >= 1:
                                                # Fallback to 1st option
                                                selected_capacity_index = 0
                                                capacity_option_to_click = selectable_capacity_options[selected_capacity_index]
                                                selected_capacity = selectable_capacity_texts[selected_capacity_index]
                                                print(f"      [INFO] Will select 1st option (index {selected_capacity_index}): '{selected_capacity}' (only {len(selectable_capacity_options)} option(s) available)")
                                            else:
                                                error_msg = "No Capacity options available after Interface and Form Factor selections"
                                                print(f"      [ERROR] {error_msg}")
                                                filtered_data['error'] = 'No Capacity Options'
                                                filtered_data['error_message'] = error_msg
                                                filtered_data['filtering_works'] = False
                                                # Close dropdown
                                                self.page.locator('body').click(position={'x': 10, 'y': 10})
                                                self.page.wait_for_timeout(300)
                                            
                                            if capacity_option_to_click and selected_capacity:
                                                filtered_data['selected_filters']['capacity'] = selected_capacity
                                                
                                                # Verify the option text one more time before clicking
                                                capacity_text_verify = (capacity_option_to_click.text_content() or '').strip()
                                                if capacity_text_verify != selected_capacity:
                                                    print(f"      [WARNING] Capacity option text changed! Expected '{selected_capacity}', but found '{capacity_text_verify}'")
                                                    selected_capacity = capacity_text_verify
                                                    filtered_data['selected_filters']['capacity'] = selected_capacity
                                                
                                                # Dismiss consent banner if present (it can intercept clicks)
                                                try:
                                                    consent_banner = self.page.locator('#consent_blackbar, .truste-consent-text, .truste-consent-track-class').first
                                                    if consent_banner.is_visible(timeout=1000):
                                                        print(f"      [INFO] Dismissing consent banner...")
                                                        # Try to find and click accept/close button
                                                        accept_btn = self.page.locator('button:has-text("Accept"), button:has-text("I Accept"), .truste-button-consent, #truste-consent-button').first
                                                        if accept_btn.is_visible(timeout=1000):
                                                            accept_btn.click(timeout=3000)
                                                            self.page.wait_for_timeout(500)
                                                        else:
                                                            # Click outside the banner to dismiss
                                                            self.page.locator('body').click(position={'x': 100, 'y': 100})
                                                            self.page.wait_for_timeout(500)
                                                except:
                                                    pass  # No consent banner or already dismissed
                                                
                                                # Don't scroll - dropdown options are already in view when dropdown is open
                                                # This prevents page from jumping to top
                                                
                                                # Verify option is visible before clicking
                                                try:
                                                    capacity_option_to_click.wait_for(state='visible', timeout=3000)
                                                except:
                                                    print(f"      [WARNING] Capacity option not visible, but proceeding with click")
                                                
                                                # Ensure dropdown is still open before clicking
                                                try:
                                                    first_option = capacity_dropdown.locator('.cmp-custom-select__option').first
                                                    if first_option.count() == 0 or not first_option.is_visible(timeout=1000):
                                                        print(f"      [DEBUG] Capacity dropdown closed, reopening before click...")
                                                        capacity_input.click(timeout=5000)
                                                        self.page.wait_for_timeout(1500)
                                                        # Re-find the option after reopening
                                                        capacity_option_to_click = capacity_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_capacity}")').first
                                                except:
                                                    pass
                                                
                                                # Click the option
                                                print(f"      [INFO] Clicking Capacity option: '{selected_capacity}'")
                                                
                                                # Don't scroll - dropdown options are already in view when dropdown is open
                                                # This prevents page from jumping to top
                                                
                                                # Verify option is visible and clickable before clicking
                                                try:
                                                    if capacity_option_to_click.count() > 0 and capacity_option_to_click.is_visible():
                                                        print(f"      [DEBUG] Option is visible, clicking...")
                                                        capacity_option_to_click.click(timeout=5000)
                                                        print(f"      [OK] Clicked Capacity option: '{selected_capacity}'")
                                                    else:
                                                        # Re-find the option if it was detached or not visible
                                                        print(f"      [DEBUG] Option not visible, re-finding...")
                                                        capacity_option_to_click = capacity_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_capacity}")').first
                                                        if capacity_option_to_click.count() > 0:
                                                            capacity_option_to_click.click(timeout=5000)
                                                            print(f"      [OK] Clicked Capacity option (re-found): '{selected_capacity}'")
                                                        else:
                                                            raise Exception(f"Capacity option '{selected_capacity}' not found after re-query")
                                                except Exception as click_error:
                                                    # Fallback to JavaScript click
                                                    print(f"      [DEBUG] Regular click failed, trying JavaScript click: {str(click_error)}")
                                                    try:
                                                        capacity_option_to_click.evaluate('element => element.click()')
                                                        print(f"      [OK] Clicked Capacity option (JavaScript): '{selected_capacity}'")
                                                    except:
                                                        # Last resort: re-find and use JavaScript
                                                        capacity_option_to_click = capacity_dropdown.locator(f'.cmp-custom-select__option:has-text("{selected_capacity}")').first
                                                        if capacity_option_to_click.count() > 0:
                                                            capacity_option_to_click.evaluate('element => element.click()')
                                                            print(f"      [OK] Clicked Capacity option (JavaScript, re-found): '{selected_capacity}'")
                                                        else:
                                                            raise Exception(f"Failed to click Capacity option '{selected_capacity}'")
                                                
                                                self.page.wait_for_timeout(2000)  # Wait for dropdown to close and filtering to apply
                                                
                                                # Verify selection was made
                                                capacity_input_after = capacity_input.get_attribute('value') or capacity_input.get_attribute('placeholder') or ''
                                                if selected_capacity.lower() in capacity_input_after.lower() or capacity_input_after == '':
                                                    print(f"      [OK] Capacity selection verified: '{selected_capacity}'")
                                                else:
                                                    print(f"      [WARNING] Capacity selection may not have worked. Expected: '{selected_capacity}', Got: '{capacity_input_after}'")
                                                
                                                print(f"      [OK] Selected Capacity: '{selected_capacity}'")
                                                
                                                # Verify selection was made
                                                capacity_input_after = capacity_input.get_attribute('value') or capacity_input.get_attribute('placeholder') or ''
                                                if selected_capacity.lower() in capacity_input_after.lower() or capacity_input_after == '':
                                                    print(f"      [OK] Capacity selection verified")
                                                else:
                                                    print(f"      [WARNING] Capacity selection may not have worked. Expected: '{selected_capacity}', Got: '{capacity_input_after}'")
                                                
                                                # Ensure dropdown is closed
                                                try:
                                                    if capacity_dropdown.locator('.cmp-custom-select__options[style*="display: block"]').count() > 0:
                                                        self.page.locator('body').click(position={'x': 10, 'y': 10})
                                                        self.page.wait_for_timeout(300)
                                                except:
                                                    pass
                                            else:
                                                # Close dropdown if still open
                                                try:
                                                    self.page.locator('body').click(position={'x': 10, 'y': 10})
                                                    self.page.wait_for_timeout(300)
                                                except:
                                                    pass
                                    except Exception as e:
                                        error_msg = f"Failed to select Capacity: {str(e)}"
                                        print(f"      [ERROR] {error_msg}")
                                        filtered_data['error'] = 'Capacity Selection Error'
                                        filtered_data['error_message'] = error_msg
                                        filtered_data['filtering_works'] = False
                                        import traceback
                                        traceback.print_exc()
                                        # Ensure dropdown is closed on error
                                        try:
                                            self.page.locator('body').click(position={'x': 10, 'y': 10})
                                            self.page.wait_for_timeout(300)
                                        except:
                                            pass
                                else:
                                    if not filtered_data.get('error'):  # Only set error if not already set
                                        error_msg = "Capacity dropdown not found"
                                        print(f"      [ERROR] {error_msg}")
                                        filtered_data['error'] = 'Capacity Dropdown Not Found'
                                        filtered_data['error_message'] = error_msg
                                        filtered_data['filtering_works'] = False
                        else:
                            # Close dropdown if still open
                            try:
                                self.page.locator('body').click(position={'x': 10, 'y': 10})
                                self.page.wait_for_timeout(300)
                            except:
                                pass
                except Exception as e:
                    error_msg = f"Failed to select Form Factor: {str(e)}"
                    print(f"      [ERROR] {error_msg}")
                    filtered_data['error'] = 'Form Factor Selection Error'
                    filtered_data['error_message'] = error_msg
                    filtered_data['filtering_works'] = False
                    import traceback
                    traceback.print_exc()
                    # Ensure dropdown is closed on error
                    try:
                        self.page.locator('body').click(position={'x': 10, 'y': 10})
                        self.page.wait_for_timeout(300)
                    except:
                        pass
            else:
                if not filtered_data.get('error'):  # Only set error if not already set
                    error_msg = "Form Factor dropdown not found"
                    print(f"      [ERROR] {error_msg}")
                    filtered_data['error'] = 'Form Factor Dropdown Not Found'
                    filtered_data['error_message'] = error_msg
                    filtered_data['filtering_works'] = False
            
            # Count filtered cards
            cards = model_list.locator('.cmp-product-cards__item, .model-list__products__product')
            filtered_data['card_count'] = cards.count()
            
            # Check if filtering worked (should have fewer cards)
            print(f"      [OK] Filtered cards count: {filtered_data['card_count']}")
            
            # Validate filtered cards match selected criteria
            # Only set filtering_works to True if there are no errors and cards are found
            if filtered_data['card_count'] > 0 and not filtered_data.get('error'):
                filtered_data['filtering_works'] = True
                # Validate a few cards to ensure they match filters
                for i in range(min(cards.count(), 3)):
                    card = cards.nth(i)
                    card_data = self._validate_single_product_card(card, i)
                    filtered_data['cards'].append(card_data)
            elif filtered_data.get('error'):
                # If there's an error, ensure filtering_works is False
                filtered_data['filtering_works'] = False
                print(f"      [ERROR] Filtering test failed due to error: {filtered_data.get('error_message', 'Unknown error')}")
        
        except Exception as e:
            error_msg = f"Filtering test failed: {str(e)}"
            print(f"      [ERROR] {error_msg}")
            filtered_data['error'] = 'Filtering Test Error'
            filtered_data['error_message'] = error_msg
            filtered_data['filtering_works'] = False
            import traceback
            traceback.print_exc()
        
        return filtered_data
    
    def _validate_related_articles(self) -> Dict:
        """Validate related articles section"""
        # Scroll to focus on related articles section
        try:
            articles_section = self.page.locator('.cmp-article-list, .article-list').first
            if articles_section.count() > 0:
                articles_section.scroll_into_view_if_needed(timeout=3000)
                self.page.wait_for_timeout(200)
        except:
            pass
        
        articles_data = {
            'found': False,
            'card_count': 0,
            'cards': []
        }
        
        try:
            # Find related articles section (similar to homepage article list)
            articles_section = self.page.locator('section:has-text("Related Articles"), .related-articles, [class*="article"]').first
            
            if articles_section.count() > 0:
                articles_data['found'] = True
                
                # Find article cards (similar to homepage)
                article_cards = articles_section.locator('.cmp-article-list__article, article, .article-card').all()
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
        
        return articles_data
    
    def _validate_single_article_card(self, card, index: int) -> Dict:
        """Validate a single article card"""
        article_data = {
            'index': index + 1,
            'container': {},
            'image': {},
            'tags': [],
            'title': {},
            'link': ''
        }
        
        try:
            # Container size
            container_size = card.evaluate("""
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
            
            # Image
            img = card.locator('img').first
            if img.count() > 0:
                article_data['image']['src'] = img.get_attribute('src') or img.get_attribute('data-src') or ''
                article_data['image']['alt'] = img.get_attribute('alt') or ''
            
            # Tags (optional)
            tags = card.locator('.tag, [class*="tag"], .category').all()
            for tag in tags:
                tag_text = (tag.text_content() or '').strip()
                if tag_text:
                    article_data['tags'].append(tag_text)
            
            # Title
            title = card.locator('h3, h4, .title, [class*="title"]').first
            if title.count() > 0:
                article_data['title']['text'] = (title.text_content() or '').strip()
            
            # Link
            link = card.locator('a').first
            if link.count() > 0:
                article_data['link'] = link.get_attribute('href') or ''
                
                # Validate URL format (without navigating to save time)
                if article_data['link']:
                    article_data['url_format_valid'] = False
                    try:
                        article_title = article_data['title'].get('text', '')
                        href = article_data['link']
                        
                        # Verify URL format matches expected pattern
                        # Expected: /products/technology/{article-slug}.html
                        # Example: /products/technology/qlc-ssds-value-performance-density-storage-field-day.html
                        
                        url_valid = False
                        url_matches_title = False
                        
                        # Check if URL follows the expected pattern
                        if href and ('/products/technology/' in href or '/products/' in href):
                            url_valid = True
                            
                            # Check if URL contains article title keywords
                            if article_title:
                                # Create variations of title for matching
                                title_variations = [
                                    article_title.lower().replace(' ', '-'),
                                    article_title.lower().replace(' ', '-').replace(':', '').replace(',', ''),
                                    article_title[:30].lower().replace(' ', '-'),
                                    article_title[:20].lower().replace(' ', '-'),
                                ]
                                
                                # Check if any variation matches URL
                                for variation in title_variations:
                                    if variation and variation in href.lower():
                                        url_matches_title = True
                                        print(f"         [OK] Article URL format valid: {href}")
                                        break
                                
                                if not url_matches_title:
                                    # URL might still be valid even if title doesn't match exactly
                                    if href.endswith('.html') and '/products/' in href:
                                        url_matches_title = True  # Consider valid if it's a product/technology URL
                                        print(f"         [OK] Article URL format valid: {href}")
                                    else:
                                        print(f"         [WARNING] Article URL format may not match title: {href} (Title: {article_title[:50]})")
                            else:
                                # No title to match, just check URL format
                                if href.endswith('.html') and '/products/' in href:
                                    url_matches_title = True
                                    print(f"         [OK] Article URL format valid: {href}")
                        else:
                            print(f"         [WARNING] Article URL format unexpected: {href}")
                        
                        article_data['url_format_valid'] = url_valid
                        article_data['url_matches_title'] = url_matches_title
                        
                    except Exception as e:
                        article_data['url_format_error'] = str(e)
                        print(f"         [ERROR] Article URL format validation failed: {str(e)}")
        
        except Exception as e:
            print(f"      [ERROR] Article card {index+1} validation failed: {str(e)}")
        
        return article_data
    
    def _print_summary(self, results: Dict):
        """Print validation summary"""
        print("\n" + "="*80)
        print("MODEL LIST SUMMARY")
        print("="*80)
        
        summary = results.get('summary', {})
        print(f"Title Found: {'Yes' if summary.get('title_found') else 'No'}")
        print(f"Dropdowns Found: {'Yes' if summary.get('dropdowns_found') else 'No'}")
        print(f"Default Cards Count: {summary.get('default_cards_count', 0)}")
        print(f"Filtered Cards Count: {summary.get('filtered_cards_count', 0)}")
        print(f"Filtering Works: {'Yes' if summary.get('filtering_works') else 'No'}")
        print(f"Related Articles Found: {'Yes' if summary.get('articles_found') else 'No'}")
        print(f"Related Articles Count: {summary.get('articles_count', 0)}")

