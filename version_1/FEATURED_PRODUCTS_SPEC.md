# Featured Products Validator - Complete Specification

## ✅ What Gets Validated

### 1. Title
- ✅ Text content
- ✅ Font size (px)
- ✅ Font color (RGB)
- ✅ Font family
- ✅ Font weight

### 2. Product Cards
- ✅ Number of cards (count)
- ✅ Each card validated for:
  - Image
    - Source URL
    - Width x Height dimensions
  - Title
    - Text
    - Font size
    - Font color
    - Font weight
  - Description
    - Text
    - Font size
    - Font color
  - Container size
    - Width x Height

### 3. Chevron Navigation
- ✅ Left chevron exists
- ✅ Right chevron exists
- ✅ Left chevron functionality:
  - ✅ DOES NOT move cards when on first card
  - ✅ Moves cards backwards when not on first card
- ✅ Right chevron functionality:
  - ✅ DOES NOT move cards when on last card
  - ✅ Moves cards forward when not on last card

### 4. Hover Effect
- ✅ Card focuses when hovered
- ✅ Transform/scale effects detected
- ✅ Z-index changes on hover

---

## 📊 Output Format

### Console Output
```
[TITLE] Validating title...
   [OK] Title: 'Featured Products'
   [OK] Font: 32px, Color: rgb(0, 0, 0)

[CARDS] Validating product cards...
   [OK] Found 6 product cards
      [OK] Card 1: 'D7-P5520'
              Container: 300x400
              Image: 300x200

[CHEVRONS] Validating navigation chevrons...
   [OK] Both chevrons found
   [OK] Right chevron works - cards moved
   [OK] Left chevron works - cards moved back
   [OK] Left chevron correctly disabled on first card

[HOVER] Validating hover effect...
   [OK] Hover effect detected on cards
```

### Results Dictionary
```python
{
    'found': True,
    'title': {
        'exists': True,
        'text': 'Featured Products',
        'font_size': '32px',
        'font_color': 'rgb(0, 0, 0)',
        'font_family': 'Arial',
        'font_weight': 'bold'
    },
    'cards': {
        'card_count': 6,
        'cards': [
            {
                'index': 1,
                'title': 'D7-P5520',
                'description': 'Description text',
                'image': {
                    'src': 'image.jpg',
                    'width': 300,
                    'height': 200
                },
                'container': {
                    'width': 300,
                    'height': 400
                },
                'font_styles': {
                    'title': {
                        'fontSize': '18px',
                        'color': 'rgb(0, 0, 0)',
                        'fontWeight': 'bold'
                    },
                    'description': {
                        'fontSize': '14px',
                        'color': 'rgb(80, 80, 80)'
                    }
                }
            }
            # ... more cards
        ]
    },
    'chevrons': {
        'left_exists': True,
        'right_exists': True,
        'left_works': True,
        'right_works': True,
        'left_disabled_on_first': True,
        'right_disabled_on_last': True
    },
    'hover': {
        'hover_effect_detected': True,
        'focus_behavior': 'Card focuses on hover'
    },
    'summary': {
        'total_cards': 6,
        'title_exists': True,
        'chevrons_working': True,
        'hover_working': True
    }
}
```

---

## 🎯 Key Features

### ✅ Complete Card Analysis
- Extract all card details (image, title, description)
- Measure container dimensions
- Measure image dimensions
- Extract font details (size, color, weight, family)

### ✅ Navigation Validation
- Test chevron clicks
- Verify left chevron disabled on first card
- Verify right chevron disabled on last card
- Measure card movement

### ✅ Hover Effects
- Detect focus behavior
- Check for transform/scale changes
- Verify z-index changes

---

## 🚀 Usage

### Standalone Test:
```bash
python test_featured_products.py
```

### Integrated in Homepage Validator:
```bash
python run_homepage_validation.py https://www.solidigm.com/
```

---

## 📄 Excel Report Integration

The validator will automatically add a "Featured Products" sheet to the Excel report with:
- Title details
- Card count
- Each card's details
- Font sizes and colors
- Image dimensions
- Container sizes
- Chevron functionality status
- Hover effect status

---

## ✅ Status: READY TO USE!

The Featured Products validator is complete and ready to validate any featured products component on the Solidigm website.


