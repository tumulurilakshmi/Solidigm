"""
UI Validation utilities for Playwright automation
"""
import re
from typing import Dict, List, Tuple, Optional
from playwright.sync_api import Page, Locator
from PIL import Image
import io

class UIValidator:
    def __init__(self, page: Page):
        self.page = page
    
    def get_element_styles(self, selector: str) -> Dict[str, str]:
        """Get computed styles for an element"""
        return self.page.evaluate(f"""
            () => {{
                const element = document.querySelector('{selector}');
                if (!element) return null;
                const styles = window.getComputedStyle(element);
                return {{
                    fontSize: styles.fontSize,
                    color: styles.color,
                    backgroundColor: styles.backgroundColor,
                    width: styles.width,
                    height: styles.height,
                    fontFamily: styles.fontFamily,
                    fontWeight: styles.fontWeight,
                    textAlign: styles.textAlign,
                    padding: styles.padding,
                    margin: styles.margin,
                    border: styles.border,
                    display: styles.display,
                    position: styles.position
                }};
            }}
        """)
    
    def validate_font_size(self, selector: str, expected_size: str, tolerance: int = 2) -> Tuple[bool, str]:
        """Validate font size of an element"""
        styles = self.get_element_styles(selector)
        if not styles:
            return False, f"Element not found: {selector}"
        
        actual_size = styles['fontSize']
        expected_px = float(re.findall(r'(\d+\.?\d*)', expected_size)[0])
        actual_px = float(re.findall(r'(\d+\.?\d*)', actual_size)[0])
        
        if abs(actual_px - expected_px) <= tolerance:
            return True, f"Font size valid: {actual_size} (expected: {expected_size})"
        else:
            return False, f"Font size mismatch: {actual_size} (expected: {expected_size})"
    
    def validate_color(self, selector: str, expected_color: str, tolerance: int = 10) -> Tuple[bool, str]:
        """Validate color of an element"""
        styles = self.get_element_styles(selector)
        if not styles:
            return False, f"Element not found: {selector}"
        
        actual_color = styles['color']
        expected_rgb = self._parse_color(expected_color)
        actual_rgb = self._parse_color(actual_color)
        
        if self._colors_match(expected_rgb, actual_rgb, tolerance):
            return True, f"Color valid: {actual_color} (expected: {expected_color})"
        else:
            return False, f"Color mismatch: {actual_color} (expected: {expected_color})"
    
    def validate_container_size(self, selector: str, expected_width: int, expected_height: int, tolerance: int = 5) -> Tuple[bool, str]:
        """Validate container dimensions"""
        styles = self.get_element_styles(selector)
        if not styles:
            return False, f"Element not found: {selector}"
        
        actual_width = float(re.findall(r'(\d+\.?\d*)', styles['width'])[0])
        actual_height = float(re.findall(r'(\d+\.?\d*)', styles['height'])[0])
        
        width_ok = abs(actual_width - expected_width) <= tolerance
        height_ok = abs(actual_height - expected_height) <= tolerance
        
        if width_ok and height_ok:
            return True, f"Container size valid: {actual_width}x{actual_height} (expected: {expected_width}x{expected_height})"
        else:
            return False, f"Container size mismatch: {actual_width}x{actual_height} (expected: {expected_width}x{expected_height})"
    
    def validate_text_content(self, selector: str, expected_text: str) -> Tuple[bool, str]:
        """Validate text content of an element"""
        try:
            element = self.page.locator(selector)
            actual_text = element.text_content()
            
            if expected_text.lower() in actual_text.lower():
                return True, f"Text content valid: '{actual_text}' contains '{expected_text}'"
            else:
                return False, f"Text content mismatch: '{actual_text}' (expected to contain: '{expected_text}')"
        except Exception as e:
            return False, f"Error validating text: {str(e)}"
    
    def validate_image_presence(self, selector: str) -> Tuple[bool, str]:
        """Validate if image is present and loaded"""
        try:
            img = self.page.locator(selector)
            if img.count() == 0:
                return False, f"Image not found: {selector}"
            
            # Check if image is loaded
            is_loaded = self.page.evaluate(f"""
                () => {{
                    const img = document.querySelector('{selector}');
                    return img && img.complete && img.naturalHeight !== 0;
                }}
            """)
            
            if is_loaded:
                return True, f"Image loaded successfully: {selector}"
            else:
                return False, f"Image not loaded: {selector}"
        except Exception as e:
            return False, f"Error validating image: {str(e)}"
    
    def validate_cta_button(self, selector: str, expected_text: str = None) -> Tuple[bool, str]:
        """Validate CTA button presence and properties"""
        try:
            button = self.page.locator(selector)
            if button.count() == 0:
                return False, f"CTA button not found: {selector}"
            
            # Check if button is visible and clickable
            is_visible = button.is_visible()
            is_enabled = button.is_enabled()
            
            if not is_visible:
                return False, f"CTA button not visible: {selector}"
            
            if not is_enabled:
                return False, f"CTA button not enabled: {selector}"
            
            # Check text content if provided
            if expected_text:
                actual_text = button.text_content()
                if expected_text.lower() not in actual_text.lower():
                    return False, f"CTA text mismatch: '{actual_text}' (expected: '{expected_text}')"
            
            return True, f"CTA button valid: {selector}"
        except Exception as e:
            return False, f"Error validating CTA: {str(e)}"
    
    def get_element_position(self, selector: str) -> Dict[str, float]:
        """Get element position and size"""
        return self.page.evaluate(f"""
            () => {{
                const element = document.querySelector('{selector}');
                if (!element) return null;
                const rect = element.getBoundingClientRect();
                return {{
                    x: rect.x,
                    y: rect.y,
                    width: rect.width,
                    height: rect.height,
                    top: rect.top,
                    left: rect.left,
                    right: rect.right,
                    bottom: rect.bottom
                }};
            }}
        """)
    
    def _parse_color(self, color: str) -> Tuple[int, int, int]:
        """Parse color string to RGB tuple"""
        # Handle rgb() format
        if 'rgb(' in color:
            rgb = re.findall(r'(\d+)', color)
            return (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        
        # Handle hex format
        if color.startswith('#'):
            hex_color = color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Handle named colors (basic)
        color_map = {
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'blue': (0, 0, 255),
        }
        return color_map.get(color.lower(), (0, 0, 0))
    
    def _colors_match(self, color1: Tuple[int, int, int], color2: Tuple[int, int, int], tolerance: int) -> bool:
        """Check if two colors match within tolerance"""
        return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))
