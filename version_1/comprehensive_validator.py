"""
Comprehensive Validator with detailed tracking for UI validation and link checking
"""
import json
import time
from typing import Dict, List, Tuple
from playwright.sync_api import Page, sync_playwright
from ui_validator import UIValidator
from link_validator import LinkValidator
from config import Config


class ComprehensiveValidator:
    def __init__(self, page: Page, base_url: str, locale: str = "US/EN"):
        self.page = page
        self.base_url = base_url
        self.locale = locale
        self.ui_validator = UIValidator(page)
        self.link_validator = LinkValidator(page, base_url)
        
        # Tracking variables
        self.ui_validation_results = []
        self.link_validation_results = []
        self.total_validations = 0
        self.passed_validations = 0
        self.failed_validations = 0
        self.validation_summary = {
            'font_size': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'font_color': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'element_size': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'images': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'buttons': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
            'navigation': {'total': 0, 'passed': 0, 'failed': 0, 'details': []},
        }
    
    def validate_comprehensive_ui(self) -> Dict:
        """Perform comprehensive UI validation with detailed tracking"""
        print(f"\n[UI VALIDATION] Starting for {self.base_url}")
        print(f"[LOCALE] {self.locale}")
        print("=" * 80)
        
        results = {
            'url': self.base_url,
            'locale': self.locale,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'validations': [],
            'summary': {}
        }
        
        try:
            # 1. Validate Font Sizes
            print("\n[FONT SIZES] Validating...")
            self._validate_font_sizes()
            
            # 2. Validate Font Colors
            print("\n[FONT COLORS] Validating...")
            self._validate_font_colors()
            
            # 3. Validate Element Sizes
            print("\n[ELEMENT SIZES] Validating...")
            self._validate_element_sizes()
            
            # 4. Validate Images
            print("\n[IMAGES] Validating...")
            self._validate_images()
            
            # 5. Validate Buttons/CTAs
            print("\n[BUTTONS] Validating...")
            self._validate_buttons()
            
            # 6. Validate Navigation
            print("\n[NAVIGATION] Validating...")
            self._validate_navigation()
            
            # Compile summary
            results['validations'] = self.ui_validation_results
            results['summary'] = {
                'total_validations': self.total_validations,
                'passed': self.passed_validations,
                'failed': self.failed_validations,
                'pass_percentage': round((self.passed_validations / self.total_validations * 100) if self.total_validations > 0 else 0, 2),
                'by_category': self.validation_summary
            }
            
            print("\n" + "=" * 80)
            print(f"[OK] UI Validation Complete: {self.passed_validations}/{self.total_validations} passed")
            
        except Exception as e:
            print(f"[ERROR] Error during UI validation: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def validate_comprehensive_links(self) -> Dict:
        """Perform comprehensive link validation"""
        print(f"\n[LINK VALIDATION] Starting for {self.base_url}")
        print("=" * 80)
        
        results = {
            'url': self.base_url,
            'locale': self.locale,
            'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            'total_links': 0,
            'valid_links': 0,
            'broken_links': 0,
            'broken_details': []
        }
        
        try:
            # Get all links
            all_links = self.link_validator.validate_all_links()
            results['total_links'] = len(all_links)
            
            valid_links = [link for link in all_links if link['is_valid']]
            broken_links = [link for link in all_links if not link['is_valid']]
            
            results['valid_links'] = len(valid_links)
            results['broken_links'] = len(broken_links)
            results['broken_details'] = [
                {
                    'url': link['url'],
                    'text': link['text'],
                    'status_code': link['status_code'],
                    'message': link['message']
                }
                for link in broken_links
            ]
            
            self.link_validation_results = all_links
            
            print(f"\n[OK] Link Validation Complete")
            print(f"   Total Links: {results['total_links']}")
            print(f"   Valid Links: {results['valid_links']}")
            print(f"   Broken Links: {results['broken_links']}")
            
        except Exception as e:
            print(f"[ERROR] Error during link validation: {str(e)}")
            results['error'] = str(e)
        
        return results
    
    def _validate_font_sizes(self):
        """Validate font sizes for key elements"""
        elements = [
            {'selector': 'h1', 'expected_size': '48px', 'tolerance': 10},
            {'selector': 'h2', 'expected_size': '36px', 'tolerance': 10},
            {'selector': 'h3', 'expected_size': '24px', 'tolerance': 10},
            {'selector': 'p', 'expected_size': '16px', 'tolerance': 4},
            {'selector': '.main-menu a, nav a', 'expected_size': '14px', 'tolerance': 4},
        ]
        
        for elem in elements:
            try:
                count = self.page.locator(elem['selector']).count()
                if count == 0:
                    continue
                
                # Check first occurrence
                is_valid, message = self.ui_validator.validate_font_size(
                    elem['selector'], 
                    elem['expected_size'], 
                    elem['tolerance']
                )
                
                self.total_validations += 1
                self.validation_summary['font_size']['total'] += 1
                
                result = {
                    'type': 'font_size',
                    'selector': elem['selector'],
                    'expected': elem['expected_size'],
                    'passed': is_valid,
                    'message': message,
                    'count_found': count
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['font_size']['passed'] += 1
                    print(f"   [OK] {elem['selector']}: {message}")
                else:
                    self.failed_validations += 1
                    self.validation_summary['font_size']['failed'] += 1
                    result['details'] = f"Font size failed for {elem['selector']}"
                    self.validation_summary['font_size']['details'].append(result)
                    print(f"   [FAIL] {elem['selector']}: {message}")
                
            except Exception as e:
                print(f"   [WARNING] Error validating {elem['selector']}: {str(e)}")
    
    def _validate_font_colors(self):
        """Validate font colors for key elements"""
        elements = [
            {'selector': 'h1', 'expected_color': 'rgb(0, 0, 0)'},
            {'selector': 'h2', 'expected_color': 'rgb(0, 0, 0)'},
            {'selector': 'p', 'expected_color': 'rgb(0, 0, 0)'},
        ]
        
        for elem in elements:
            try:
                count = self.page.locator(elem['selector']).count()
                if count == 0:
                    continue
                
                # Check first occurrence
                is_valid, message = self.ui_validator.validate_color(
                    elem['selector'], 
                    elem['expected_color'], 
                    tolerance=50  # More lenient for color
                )
                
                self.total_validations += 1
                self.validation_summary['font_color']['total'] += 1
                
                styles = self.ui_validator.get_element_styles(elem['selector'])
                actual_color = styles['color'] if styles else 'unknown'
                
                result = {
                    'type': 'font_color',
                    'selector': elem['selector'],
                    'expected': elem['expected_color'],
                    'actual': actual_color,
                    'passed': is_valid,
                    'message': message,
                    'count_found': count
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['font_color']['passed'] += 1
                    print(f"   [OK] {elem['selector']}: {message}")
                else:
                    self.failed_validations += 1
                    self.validation_summary['font_color']['failed'] += 1
                    result['details'] = f"Font color failed for {elem['selector']} - Expected: {elem['expected_color']}, Got: {actual_color}"
                    self.validation_summary['font_color']['details'].append(result)
                    print(f"   [FAIL] {elem['selector']}: {message}")
                
            except Exception as e:
                print(f"   [WARNING] Error validating {elem['selector']}: {str(e)}")
    
    def _validate_element_sizes(self):
        """Validate element sizes"""
        elements = [
            {'selector': 'header', 'expected_width': 1920, 'expected_height': 100, 'tolerance': 50},
            {'selector': 'footer', 'expected_width': 1920, 'expected_height': 200, 'tolerance': 100},
        ]
        
        for elem in elements:
            try:
                count = self.page.locator(elem['selector']).count()
                if count == 0:
                    continue
                
                position = self.ui_validator.get_element_position(elem['selector'])
                if not position:
                    continue
                
                actual_width = position['width']
                actual_height = position['height']
                
                width_valid = abs(actual_width - elem['expected_width']) <= elem['tolerance']
                height_valid = abs(actual_height - elem['expected_height']) <= elem['tolerance']
                is_valid = width_valid and height_valid
                
                self.total_validations += 1
                self.validation_summary['element_size']['total'] += 1
                
                result = {
                    'type': 'element_size',
                    'selector': elem['selector'],
                    'expected': f"{elem['expected_width']}x{elem['expected_height']}",
                    'actual': f"{actual_width}x{actual_height}",
                    'passed': is_valid,
                    'message': f"Size: {actual_width}x{actual_height} (expected: {elem['expected_width']}x{elem['expected_height']})",
                    'count_found': count
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['element_size']['passed'] += 1
                    print(f"   [OK] {elem['selector']}: {result['message']}")
                else:
                    self.failed_validations += 1
                    self.validation_summary['element_size']['failed'] += 1
                    result['details'] = f"Size mismatch for {elem['selector']} - Expected: {elem['expected_width']}x{elem['expected_height']}, Got: {actual_width}x{actual_height}"
                    self.validation_summary['element_size']['details'].append(result)
                    print(f"   [FAIL] {elem['selector']}: {result['message']}")
                
            except Exception as e:
                print(f"   [WARNING] Error validating {elem['selector']}: {str(e)}")
    
    def _validate_images(self):
        """Validate images"""
        try:
            images = self.page.locator('img')
            count = images.count()
            
            if count == 0:
                return
            
            checked = 0
            for i in range(min(5, count)):
                img = images.nth(i)
                if not img.is_visible():
                    continue
                
                is_valid, message = self.ui_validator.validate_image_presence(f'img:nth-of-type({i+1})')
                
                self.total_validations += 1
                self.validation_summary['images']['total'] += 1
                
                result = {
                    'type': 'image',
                    'index': i + 1,
                    'passed': is_valid,
                    'message': message
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['images']['passed'] += 1
                    print(f"   [OK] Image {i+1}: Loaded successfully")
                else:
                    self.failed_validations += 1
                    self.validation_summary['images']['failed'] += 1
                    result['details'] = f"Image {i+1} failed to load"
                    self.validation_summary['images']['details'].append(result)
                    print(f"   [FAIL] Image {i+1}: Failed to load")
                
                checked += 1
            
            if checked == 0:
                print(f"   [WARNING] No visible images found")
                
        except Exception as e:
                print(f"   [WARNING] Error validating images: {str(e)}")
    
    def _validate_buttons(self):
        """Validate buttons/CTAs"""
        try:
            buttons = self.page.locator('button, a[class*="button"], .btn')
            count = buttons.count()
            
            if count == 0:
                print(f"   [WARNING] No buttons found")
                return
            
            checked = 0
            for i in range(min(5, count)):
                button = buttons.nth(i)
                text = button.text_content() or ""
                is_visible = button.is_visible()
                is_enabled = button.is_enabled()
                is_valid = is_visible and is_enabled
                
                self.total_validations += 1
                self.validation_summary['buttons']['total'] += 1
                
                result = {
                    'type': 'button',
                    'index': i + 1,
                    'text': text[:50],
                    'passed': is_valid,
                    'visible': is_visible,
                    'enabled': is_enabled,
                    'message': f"Button '{text[:30]}...' - visible: {is_visible}, enabled: {is_enabled}"
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['buttons']['passed'] += 1
                    print(f"   [OK] Button {i+1}: {result['message']}")
                else:
                    self.failed_validations += 1
                    self.validation_summary['buttons']['failed'] += 1
                    result['details'] = f"Button {i+1} failed - visible: {is_visible}, enabled: {is_enabled}"
                    self.validation_summary['buttons']['details'].append(result)
                    print(f"   [FAIL] Button {i+1}: {result['message']}")
                
                checked += 1
                
        except Exception as e:
                print(f"   [WARNING] Error validating buttons: {str(e)}")
    
    def _validate_navigation(self):
        """Validate navigation"""
        try:
            nav_links = self.page.locator('nav a, .main-menu a, .navigation a')
            count = nav_links.count()
            
            if count == 0:
                print(f"   [WARNING] No navigation links found")
                return
            
            checked = 0
            for i in range(min(5, count)):
                link = nav_links.nth(i)
                text = link.text_content() or ""
                href = link.get_attribute('href') or ""
                is_visible = link.is_visible()
                
                # Quick validation if link is accessible
                is_valid = is_visible and href != "" and href != "#"
                
                self.total_validations += 1
                self.validation_summary['navigation']['total'] += 1
                
                result = {
                    'type': 'navigation',
                    'index': i + 1,
                    'text': text,
                    'href': href,
                    'passed': is_valid,
                    'visible': is_visible,
                    'message': f"Nav link '{text}' - href: {href}, visible: {is_visible}"
                }
                
                self.ui_validation_results.append(result)
                
                if is_valid:
                    self.passed_validations += 1
                    self.validation_summary['navigation']['passed'] += 1
                    print(f"   [OK] Nav link {i+1}: '{text}'")
                else:
                    self.failed_validations += 1
                    self.validation_summary['navigation']['failed'] += 1
                    result['details'] = f"Navigation link {i+1} failed - text: '{text}', href: {href}, visible: {is_visible}"
                    self.validation_summary['navigation']['details'].append(result)
                    print(f"   [FAIL] Nav link {i+1}: '{text}' - not valid")
                
                checked += 1
                
        except Exception as e:
                print(f"   [WARNING] Error validating navigation: {str(e)}")
    
    def run_complete_validation(self) -> Dict:
        """Run complete validation including UI and links"""
        print("\n" + "=" * 80)
        print("[STARTING] Complete Validation Suite")
        print("=" * 80)
        
        try:
            ui_results = self.validate_comprehensive_ui()
            link_results = self.validate_comprehensive_links()
        except Exception as e:
            print(f"[ERROR] Error during validation: {str(e)}")
            return {
                'validation_info': {
                    'url': self.base_url,
                    'locale': self.locale,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
                },
                'error': str(e)
            }
        
        combined_results = {
            'validation_info': {
                'url': self.base_url,
                'locale': self.locale,
                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
            },
            'ui_validation': ui_results,
            'link_validation': link_results,
            'overall_summary': {
                'total_ui_validations': self.total_validations,
                'passed_ui_validations': self.passed_validations,
                'failed_ui_validations': self.failed_validations,
                'total_links': link_results['total_links'],
                'valid_links': link_results['valid_links'],
                'broken_links': link_results['broken_links']
            }
        }
        
        return combined_results

