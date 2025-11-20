# Component Reuse Examples - Detailed Code Walkthrough

This document provides concrete code examples showing how components are reused across different pages, demonstrating **zero redundancy**.

---

## Example 1: Footer Component

### **The Reusable Validator**

**File:** `footer_validator.py`
```python
class FooterValidator:
    def __init__(self, page):
        self.page = page
    
    def validate_footer(self):
        """Validates footer component - works on ANY page"""
        footer = self.page.locator('footer, .cmp-footer')
        
        if footer.count() == 0:
            return {'found': False}
        
        # Extract footer data (same logic for all pages)
        result = {
            'found': True,
            'logo': {...},
            'social_icons': [...],
            'navigation_sections': [...],
            'copyright': {...}
        }
        return result
```

### **Usage Across Pages**

**1. Homepage** (`homepage_validator.py`)
```python
def validate_complete_homepage(self):
    # ... other validations ...
    
    # Use FooterValidator
    footer_validator = FooterValidator(self.page)
    footer_results = footer_validator.validate_footer()
    
    results['footer'] = footer_results
    return results
```

**2. Data Center Page** (`data_center_page_validator.py`)
```python
def validate_data_center_page(self, url):
    # ... other validations ...
    
    # Use SAME FooterValidator
    footer_validator = FooterValidator(self.page)  # Same class!
    footer_results = footer_validator.validate_footer()
    
    results['footer'] = footer_results
    return results
```

**3. Product Series Pages** (`product_series_validator.py`)
```python
def validate_series_page(self, url, series):
    # ... other validations ...
    
    # Use SAME FooterValidator
    footer_validator = FooterValidator(self.page)  # Same class!
    footer_results = footer_validator.validate_footer()
    
    results['footer'] = footer_results
    return results
```

**Result:** 
- ✅ **1 validator class** (FooterValidator)
- ✅ **Used on 6+ pages**
- ✅ **Zero code duplication**
- ✅ **Fix once, works everywhere**

---

## Example 2: Hero Component

### **The Reusable Validator**

**File:** `hero_component_validator.py`
```python
class HeroComponentValidator:
    def __init__(self, page):
        self.page = page
    
    def validate_hero(self, hero_selector='.cmp-hero'):
        """Validates hero component - works on ANY page"""
        hero = self.page.locator(hero_selector)
        
        if hero.count() == 0:
            return {'found': False}
        
        # Extract hero data (same logic for all pages)
        result = {
            'found': True,
            'title': {...},
            'description': {...},
            'breadcrumbs': [...],
            'background_image': {...}
        }
        return result
```

### **Usage Across Pages**

**1. Product Series Pages** (`product_series_validator.py`)
```python
def validate_series_page(self, url, series):
    hero_validator = HeroComponentValidator(self.page)
    hero_results = hero_validator.validate_hero()
    results['hero'] = hero_results
```

**2. PDP Pages** (`pdp_validator.py`)
```python
def validate_pdp_page(self, url):
    hero_validator = HeroComponentValidator(self.page)  # Same class!
    hero_results = hero_validator.validate_hero()
    results['hero'] = hero_results
```

**Result:**
- ✅ **1 validator class** (HeroComponentValidator)
- ✅ **Used on 4+ page types**
- ✅ **Zero code duplication**

---

## Example 3: Navigation Component

### **The Reusable Validator**

**File:** `navigation_validator.py`
```python
class NavigationValidator:
    def __init__(self, page):
        self.page = page
    
    def validate_navigation(self):
        """Validates navigation menu - works on ANY page"""
        nav = self.page.locator('nav, .cmp-navigation')
        
        # Extract navigation data
        result = {
            'main_menu_items': [...],
            'sub_menu_items': [...],
            'links': [...],
            'broken_links': [...]
        }
        return result
```

### **Usage Across Pages**

**Used on:** Homepage, Data Center, D3, D5, D7, PDP pages

**Code Pattern:**
```python
# In ANY page validator
nav_validator = NavigationValidator(self.page)
nav_results = nav_validator.validate_navigation()
```

**Result:**
- ✅ **1 validator class** (NavigationValidator)
- ✅ **Used on ALL pages** (navigation is on every page)
- ✅ **Zero code duplication**

---

## Example 4: Model List Component

### **The Reusable Validator**

**File:** `model_list_validator.py`
```python
class ModelListValidator:
    def __init__(self, page):
        self.page = page
    
    def validate_model_list(self, filter_params=None):
        """Validates model list with filters - works on multiple pages"""
        # Extract dropdowns, product cards, filtering logic
        result = {
            'title': {...},
            'dropdowns': {...},
            'product_cards': [...],
            'filtering_works': True/False
        }
        return result
```

### **Usage Across Pages**

**1. Data Center Page** (`data_center_page_validator.py`)
```python
def validate_data_center_page(self, url, filter_params=None):
    model_list_validator = ModelListValidator(self.page)
    model_list_results = model_list_validator.validate_model_list(filter_params)
    results['model_list'] = model_list_results
```

**2. Product Series Pages** (`product_series_validator.py`)
```python
def validate_series_page(self, url, series):
    model_list_validator = ModelListValidator(self.page)  # Same class!
    model_list_results = model_list_validator.validate_model_list()
    results['model_list'] = model_list_results
```

**Result:**
- ✅ **1 validator class** (ModelListValidator)
- ✅ **Used on Data Center + 3 Series pages**
- ✅ **Zero code duplication**
- ✅ **Same filtering logic** works on all pages

---

## Example 5: Article List Component

### **The Reusable Validator**

**File:** `article_list_validator.py`
```python
class ArticleListValidator:
    def __init__(self, page):
        self.page = page
    
    def validate_article_list(self):
        """Validates article list - works on multiple pages"""
        # Extract articles, chevrons, links
        result = {
            'article_count': 3,
            'articles': [...],
            'chevrons_working': True,
            'links_valid': True
        }
        return result
```

### **Usage Across Pages**

**1. Homepage** (`homepage_validator.py`)
```python
def validate_complete_homepage(self):
    article_validator = ArticleListValidator(self.page)
    article_results = article_validator.validate_article_list()
    results['article_list'] = article_results
```

**2. Product Series Pages** (`product_series_validator.py`)
```python
def validate_series_page(self, url, series):
    article_validator = ArticleListValidator(self.page)  # Same class!
    article_results = article_validator.validate_article_list()
    results['related_articles'] = article_results
```

**Result:**
- ✅ **1 validator class** (ArticleListValidator)
- ✅ **Used on Homepage + Series pages**
- ✅ **Zero code duplication**

---

## 📊 Component Reuse Summary Table

| Component | Validator Class | Used On | Reuse Count |
|-----------|----------------|---------|-------------|
| Footer | `FooterValidator` | All pages | 6+ pages |
| Navigation | `NavigationValidator` | All pages | 6+ pages |
| Hero | `HeroComponentValidator` | Series, PDP | 4+ pages |
| Model List | `ModelListValidator` | Data Center, Series | 4 pages |
| Article List | `ArticleListValidator` | Homepage, Series | 4 pages |
| Carousel | `CarouselValidator` | Homepage, Article Lists | 2+ pages |
| Search | `SearchComponentValidator` | Homepage, PDP | 2+ pages |
| Blade | `BladeComponentValidator` | Homepage | 1 page |
| Tile List | `TileListValidator` | Homepage | 1 page |
| Featured Products | `FeaturedProductsValidator` | Homepage | 1 page |

**Total Validator Classes:** 10  
**Total Pages Validated:** 6+  
**Code Reuse Ratio:** ~80% (most components used on multiple pages)

---

## 🔄 Maintenance Example

### **Scenario: Footer HTML Structure Changes**

**Before (with redundancy):**
- Update footer validation in homepage_validator.py
- Update footer validation in data_center_page_validator.py
- Update footer validation in product_series_validator.py
- Update footer validation in pdp_validator.py
- **4 files to update** ❌

**After (with reusable component):**
- Update footer validation in `footer_validator.py`
- **1 file to update** ✅
- All pages automatically use the updated validation

---

## 💡 Key Takeaways

1. **Component validators are page-agnostic** - they work on any page
2. **Page validators are orchestrators** - they call component validators
3. **Zero redundancy** - each component validator written once
4. **Easy maintenance** - fix once, works everywhere
5. **Consistent validation** - same logic across all pages

---

**This architecture ensures:**
- ✅ No duplicate code
- ✅ Easy maintenance
- ✅ Consistent validation
- ✅ Scalable architecture
- ✅ Single source of truth for each component

