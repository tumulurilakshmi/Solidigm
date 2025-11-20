"""
Base Report Generator with common functionality
"""
import re
from typing import Dict


class BaseReportGenerator:
    """Base class for all report generators with common utility methods"""
    
    def _format_font_size(self, font_size_str: str) -> str:
        """Format font size to 2 decimal places (e.g., '32.0001px' -> '32.00px')"""
        if not font_size_str or not isinstance(font_size_str, str):
            return str(font_size_str) if font_size_str else ''
        
        # Extract numeric value and unit (e.g., "32.0001px" -> "32.00px")
        match = re.match(r'([\d.]+)(.*)', str(font_size_str).strip())
        if match:
            numeric_value = float(match.group(1))
            unit = match.group(2) if match.group(2) else ''
            return f"{numeric_value:.2f}{unit}"
        return str(font_size_str)
    
    def _format_dimension(self, width, height) -> str:
        """Format width x height to 2 decimal places"""
        try:
            w = float(width) if width else 0
            h = float(height) if height else 0
            return f"{w:.2f}x{h:.2f}"
        except (ValueError, TypeError):
            return ''

