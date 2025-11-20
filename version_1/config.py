"""
Configuration settings for Playwright automation
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Target URL
    BASE_URL = "https://www.solidigm.com"
    
    # Browser settings
    BROWSER = os.getenv('BROWSER', 'chromium')  # chromium, firefox, webkit
    HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'
    VIEWPORT = {'width': 1920, 'height': 1080}
    
    # Timeouts (in milliseconds)
    TIMEOUT = 60000  # Increased to 60 seconds
    NAVIGATION_TIMEOUT = 60000  # Increased to 60 seconds
    
    # Screenshot settings
    SCREENSHOT_DIR = 'screenshots'
    SCREENSHOT_ON_FAILURE = True
    
    # Test data
    EXPECTED_TITLE = "Solidigm"
    EXPECTED_MAIN_NAVIGATION = [
        "Product", "Insights", "Support", "Partner", "Company"
    ]
    
    # UI Validation thresholds
    FONT_SIZE_TOLERANCE = 2  # pixels
    COLOR_TOLERANCE = 10  # RGB difference
    CONTAINER_SIZE_TOLERANCE = 5  # pixels
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'automation.log'
