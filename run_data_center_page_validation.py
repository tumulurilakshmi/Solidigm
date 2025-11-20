"""
Run Data Center Landing Page validation
Validates the main data center page at /products/data-center.html

Usage:
    python run_data_center_page_validation.py                    # Use default filters (1st, 1st, None)
    python run_data_center_page_validation.py 2,2,1               # Use indices: Interface=2, Form Factor=2, Capacity=1
    python run_data_center_page_validation.py "PCIe 5.0 x4, NVMe","E1.S 9.5mm","15.36TB"  # Use text values
"""
import sys
from playwright.sync_api import sync_playwright
from data_center_page_validator import DataCenterPageValidator
from data_center_page_report_generator import DataCenterPageReportGenerator


def parse_filter_args(args):
    """Parse filter arguments from command line
    Args can be:
    - Indices: "2,2,1" -> interface_index=2, form_factor_index=2, capacity_index=1
    - Text values: "PCIe 5.0 x4, NVMe","E1.S 9.5mm","15.36TB" -> interface_text, form_factor_text, capacity_text
    - Mixed: Can combine indices and text values
    """
    filter_params = {
        'interface_index': 0,
        'form_factor_index': 0,
        'capacity_index': None,
        'interface_text': None,
        'form_factor_text': None,
        'capacity_text': None
    }
    
    if len(args) > 1:
        filter_arg = args[1]
        
        # Check if it's comma-separated values
        if ',' in filter_arg:
            # Split by comma, but handle quoted strings that may contain commas
            parts = []
            current_part = ""
            in_quotes = False
            quote_char = None
            
            for char in filter_arg:
                if char in ['"', "'"] and not in_quotes:
                    in_quotes = True
                    quote_char = char
                    current_part += char
                elif char == quote_char and in_quotes:
                    in_quotes = False
                    quote_char = None
                    current_part += char
                elif char == ',' and not in_quotes:
                    parts.append(current_part.strip())
                    current_part = ""
                else:
                    current_part += char
            
            if current_part:
                parts.append(current_part.strip())
            
            # Process each part
            for i, part in enumerate(parts):
                part = part.strip().strip('"\'')
                
                if i == 0:  # Interface
                    if part.isdigit():
                        filter_params['interface_index'] = int(part)
                    elif part:
                        filter_params['interface_text'] = part
                elif i == 1:  # Form Factor
                    if part.isdigit():
                        filter_params['form_factor_index'] = int(part)
                    elif part:
                        filter_params['form_factor_text'] = part
                elif i == 2:  # Capacity
                    if part.lower() == 'none' or not part:
                        filter_params['capacity_index'] = None
                    elif part.isdigit():
                        filter_params['capacity_index'] = int(part)
                    elif part:
                        filter_params['capacity_text'] = part
    
    return filter_params


def main():
    url = "https://www.solidigm.com/products/data-center.html"
    
    # Parse filter arguments
    filter_params = parse_filter_args(sys.argv)
    
    print("=" * 100)
    print(" " * 30 + "DATA CENTER LANDING PAGE VALIDATION")
    print("=" * 100)
    
    if filter_params['interface_text'] or filter_params['form_factor_text'] or filter_params['capacity_text']:
        print("\n[FILTER CONFIGURATION] Using text values:")
        if filter_params['interface_text']:
            print(f"  Interface: '{filter_params['interface_text']}'")
        if filter_params['form_factor_text']:
            print(f"  Form Factor: '{filter_params['form_factor_text']}'")
        if filter_params['capacity_text']:
            print(f"  Capacity: '{filter_params['capacity_text']}'")
    else:
        print("\n[FILTER CONFIGURATION] Using indices:")
        print(f"  Interface: index {filter_params['interface_index']} (1st option)")
        print(f"  Form Factor: index {filter_params['form_factor_index']} (1st option from updated list)")
        if filter_params['capacity_index'] is not None:
            print(f"  Capacity: index {filter_params['capacity_index']}")
        else:
            print(f"  Capacity: Not selected")
    
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False, args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page.set_default_timeout(120000)
    
    try:
        validator = DataCenterPageValidator(page)
        results = validator.validate_data_center_page(url, filter_params=filter_params)
        
        # Generate Excel report
        if 'error' not in results:
            report_gen = DataCenterPageReportGenerator()
            excel_file = report_gen.generate_excel_report(results)
        
        print("\n" + "="*100)
        print("VALIDATION COMPLETE")
        print("="*100)
        
        summary = results.get('summary', {})
        print("\n[SUMMARY]")
        print(f"  Header: {'✓ Found' if summary.get('header_found') else '✗ Not Found'}")
        print(f"  Footer: {'✓ Found' if summary.get('footer_found') else '✗ Not Found'}")
        print(f"  Hero Component: {'✓ Found' if summary.get('hero_found') else '✗ Not Found'}")
        print(f"  Series Cards: {'✓ Found' if summary.get('series_cards_found') else '✗ Not Found'}")
        print(f"  All Series Present: {'✓ Yes' if summary.get('all_series_present') else '✗ No'}")
        print(f"  Model List: {'✓ Found' if summary.get('model_list_found') else '✗ Not Found'}")
        print(f"  Related Articles: {'✓ Found' if summary.get('articles_found') else '✗ Not Found'}")
        
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        browser.close()


if __name__ == "__main__":
    main()

