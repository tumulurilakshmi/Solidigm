"""
Link validation utilities for Playwright automation
"""
import requests
from typing import List, Dict, Tuple
from playwright.sync_api import Page, Locator
from urllib.parse import urljoin, urlparse

class LinkValidator:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url
    
    def get_all_links(self) -> List[Dict[str, str]]:
        """Get all links from the page with their properties"""
        return self.page.evaluate("""
            () => {
                const links = Array.from(document.querySelectorAll('a[href]'));
                return links.map(link => ({
                    href: link.href,
                    text: link.textContent.trim(),
                    title: link.title || '',
                    target: link.target || '',
                    visible: link.offsetParent !== null,
                    x: link.getBoundingClientRect().x,
                    y: link.getBoundingClientRect().y,
                    width: link.getBoundingClientRect().width,
                    height: link.getBoundingClientRect().height
                }));
            }
        """)
    
    def validate_link_status(self, url: str) -> Tuple[bool, int, str]:
        """Validate if a link returns a valid HTTP status"""
        try:
            # Handle relative URLs
            if url.startswith('/'):
                url = urljoin(self.base_url, url)
            
            # Skip mailto, tel, and other non-HTTP links
            if not url.startswith(('http://', 'https://')):
                return True, 0, f"Skipped non-HTTP link: {url}"
            
            response = requests.head(url, timeout=10, allow_redirects=True)
            status_code = response.status_code
            
            if 200 <= status_code < 400:
                return True, status_code, f"Link valid: {url} (Status: {status_code})"
            else:
                return False, status_code, f"Link invalid: {url} (Status: {status_code})"
                
        except requests.exceptions.RequestException as e:
            return False, 0, f"Link error: {url} - {str(e)}"
    
    def validate_all_links(self) -> List[Dict[str, any]]:
        """Validate all links on the page"""
        links = self.get_all_links()
        results = []
        
        for link in links:
            is_valid, status_code, message = self.validate_link_status(link['href'])
            results.append({
                'url': link['href'],
                'text': link['text'],
                'title': link['title'],
                'target': link['target'],
                'visible': link['visible'],
                'position': {'x': link['x'], 'y': link['y']},
                'size': {'width': link['width'], 'height': link['height']},
                'is_valid': is_valid,
                'status_code': status_code,
                'message': message
            })
        
        return results
    
    def validate_navigation_links(self, expected_links: List[str]) -> List[Dict[str, any]]:
        """Validate main navigation links"""
        nav_links = self.page.locator('nav a, .navigation a, .main-menu a')
        results = []
        
        for i in range(nav_links.count()):
            link = nav_links.nth(i)
            href = link.get_attribute('href')
            text = link.text_content()
            
            is_valid, status_code, message = self.validate_link_status(href)
            is_expected = any(expected in text.lower() for expected in expected_links)
            
            results.append({
                'url': href,
                'text': text,
                'is_valid': is_valid,
                'status_code': status_code,
                'message': message,
                'is_expected': is_expected
            })
        
        return results
    
    def validate_external_links(self) -> List[Dict[str, any]]:
        """Validate external links (links to other domains)"""
        all_links = self.get_all_links()
        external_links = []
        base_domain = urlparse(self.base_url).netloc
        
        for link in all_links:
            link_domain = urlparse(link['href']).netloc
            if link_domain and link_domain != base_domain:
                is_valid, status_code, message = self.validate_link_status(link['href'])
                external_links.append({
                    'url': link['href'],
                    'text': link['text'],
                    'domain': link_domain,
                    'is_valid': is_valid,
                    'status_code': status_code,
                    'message': message
                })
        
        return external_links
    
    def validate_image_links(self) -> List[Dict[str, any]]:
        """Validate image source links"""
        img_links = self.page.evaluate("""
            () => {
                const images = Array.from(document.querySelectorAll('img[src]'));
                return images.map(img => ({
                    src: img.src,
                    alt: img.alt || '',
                    width: img.width,
                    height: img.height,
                    visible: img.offsetParent !== null
                }));
            }
        """)
        
        results = []
        for img in img_links:
            is_valid, status_code, message = self.validate_link_status(img['src'])
            results.append({
                'src': img['src'],
                'alt': img['alt'],
                'dimensions': {'width': img['width'], 'height': img['height']},
                'visible': img['visible'],
                'is_valid': is_valid,
                'status_code': status_code,
                'message': message
            })
        
        return results
    
    def get_broken_links(self) -> List[Dict[str, any]]:
        """Get all broken links (4xx, 5xx status codes)"""
        all_links = self.validate_all_links()
        return [link for link in all_links if not link['is_valid']]
    
    def get_duplicate_links(self) -> List[Dict[str, any]]:
        """Find duplicate links on the page"""
        all_links = self.get_all_links()
        url_counts = {}
        duplicates = []
        
        for link in all_links:
            url = link['href']
            if url in url_counts:
                url_counts[url].append(link)
            else:
                url_counts[url] = [link]
        
        for url, links in url_counts.items():
            if len(links) > 1:
                duplicates.append({
                    'url': url,
                    'count': len(links),
                    'locations': [{'text': link['text'], 'x': link['x'], 'y': link['y']} for link in links]
                })
        
        return duplicates
