"""
Excel Report Generator for Complete Home Page Validation
"""
import os
from datetime import datetime
from typing import Dict
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment


class HomePageReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_excel_report(self, results: Dict) -> str:
        """Generate comprehensive Excel report for home page validation"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/homepage_report_{timestamp}.xlsx"
        
        wb = Workbook()
        wb.remove(wb.active)
        
        # Summary Sheet
        self._create_summary_sheet(wb, results)
        
        # Navigation Sheet
        if results.get('navigation'):
            self._create_navigation_sheet(wb, results['navigation'])
        
        # Carousel Sheet
        if results.get('carousel'):
            self._create_carousel_sheet(wb, results['carousel'])
        
        # Featured Products Sheet
        if results.get('featured_products'):
            self._create_featured_products_sheet(wb, results['featured_products'])
        
        # Product Cards Sheet
        if results.get('product_cards'):
            self._create_product_cards_sheet(wb, results['product_cards'])
        
        # Article List Sheet
        if results.get('article_list'):
            self._create_article_list_sheet(wb, results['article_list'])
        
        # Blade Components Sheet
        if results.get('blade_components'):
            self._create_blade_components_sheet(wb, results['blade_components'])
        
        # Footer Sheet
        if results.get('footer'):
            self._create_footer_sheet(wb, results['footer'])
        
        wb.save(filename)
        print(f"\n[EXCEL] Complete homepage report generated: {filename}")
        return filename
    
    def _create_summary_sheet(self, wb: Workbook, results: Dict):
        """Create summary sheet"""
        ws = wb.create_sheet("Summary", 0)
        
        ws['A1'] = "SOLIDIGM HOMEPAGE VALIDATION REPORT"
        ws['A1'].font = Font(bold=True, size=16, color="366092")
        ws.merge_cells('A1:B1')
        
        row = 3
        ws.cell(row=row, column=1, value="URL:").font = Font(bold=True)
        ws.cell(row=row, column=2, value=results.get('url', ''))
        row += 1
        
        ws.cell(row=row, column=1, value="Timestamp:").font = Font(bold=True)
        ws.cell(row=row, column=2, value=results.get('timestamp', ''))
        row += 2
        
        summary = results.get('summary', {})
        ws.cell(row=row, column=1, value="COMPONENT VALIDATION SUMMARY").font = Font(bold=True, size=12)
        row += 2
        
        components = [
            ("Navigation", summary.get('navigation_validated', False)),
            ("Carousels", f"{summary.get('carousel_count', 0)} found"),
            ("Featured Products", f"{summary.get('featured_products_count', 0)} found"),
            ("Product Cards", f"{summary.get('product_cards_count', 0)} found"),
            ("Articles", f"{summary.get('article_count', 0)} found"),
            ("Blade Components", f"{summary.get('blade_count', 0)} found"),
            ("Footer", 'Yes' if summary.get('footer_exists') else 'No')
        ]
        
        for component, status in components:
            ws.cell(row=row, column=1, value=component + ":").font = Font(bold=True)
            ws.cell(row=row, column=2, value=status)
            row += 1
        
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 50
    
    def _create_navigation_sheet(self, wb: Workbook, nav_results: Dict):
        """Create navigation sheet"""
        ws = wb.create_sheet("Navigation")
        
        ws['A1'] = "Element Type"
        ws['B1'] = "Name"
        ws['C1'] = "Font Size"
        ws['D1'] = "Font Color"
        
        for cell in ['A1', 'B1', 'C1', 'D1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        # This would extract font styles from navigation
        # Placeholder implementation
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 40
        ws.column_dimensions['C'].width = 15
        ws.column_dimensions['D'].width = 30
    
    def _create_carousel_sheet(self, wb: Workbook, carousel_results: Dict):
        """Create carousel sheet"""
        ws = wb.create_sheet("Carousels")
        
        ws['A1'] = "Carousel"
        ws['B1'] = "Slides"
        ws['C1'] = "Container Size"
        ws['D1'] = "Progress Bar"
        ws['E1'] = "Navigation"
        
        for cell in ['A1', 'B1', 'C1', 'D1', 'E1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        row = 2
        for i, carousel in enumerate(carousel_results.get('carousels', []), 1):
            ws.cell(row=row, column=1, value=f"Carousel {i}")
            ws.cell(row=row, column=2, value=carousel.get('slide_count', 0))
            
            container = carousel.get('container', {})
            ws.cell(row=row, column=3, value=f"{container.get('width', 0)}x{container.get('height', 0)}")
            
            pb = carousel.get('progress_bar', {})
            ws.cell(row=row, column=4, value='Yes' if pb.get('exists') else 'No')
            
            nav = carousel.get('navigation', {})
            ws.cell(row=row, column=5, value=f"L:{nav.get('left_chevron_visible')}, R:{nav.get('right_chevron_visible')}")
            
            row += 1
        
        ws.column_dimensions['A'].width = 12
        ws.column_dimensions['B'].width = 10
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 15
        ws.column_dimensions['E'].width = 20
    
    def _create_featured_products_sheet(self, wb: Workbook, fp_results: Dict):
        """Create featured products sheet"""
        ws = wb.create_sheet("Featured Products")
        
        ws['A1'] = "Product Count"
        ws['B1'] = "Component Exists"
        
        for cell in ['A1', 'B1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        ws.cell(row=2, column=1, value=fp_results.get('product_count', 0))
        ws.cell(row=2, column=2, value='Yes' if fp_results.get('component_exists') else 'No')
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
    
    def _create_product_cards_sheet(self, wb: Workbook, pc_results: Dict):
        """Create product cards sheet"""
        ws = wb.create_sheet("Product Cards")
        
        ws['A1'] = "Card Count"
        ws['B1'] = "Component Exists"
        
        for cell in ['A1', 'B1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        ws.cell(row=2, column=1, value=pc_results.get('card_count', 0))
        ws.cell(row=2, column=2, value='Yes' if pc_results.get('component_exists') else 'No')
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
    
    def _create_article_list_sheet(self, wb: Workbook, al_results: Dict):
        """Create article list sheet"""
        ws = wb.create_sheet("Article List")
        
        ws['A1'] = "Article Count"
        ws['B1'] = "Component Exists"
        
        for cell in ['A1', 'B1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        ws.cell(row=2, column=1, value=al_results.get('article_count', 0))
        ws.cell(row=2, column=2, value='Yes' if al_results.get('component_exists') else 'No')
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
    
    def _create_blade_components_sheet(self, wb: Workbook, bc_results: Dict):
        """Create blade components sheet"""
        ws = wb.create_sheet("Blade Components")
        
        ws['A1'] = "Blade Count"
        ws['B1'] = "Component Exists"
        
        for cell in ['A1', 'B1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        ws.cell(row=2, column=1, value=bc_results.get('blade_count', 0))
        ws.cell(row=2, column=2, value='Yes' if bc_results.get('component_exists') else 'No')
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
    
    def _create_footer_sheet(self, wb: Workbook, footer_results: Dict):
        """Create footer sheet"""
        ws = wb.create_sheet("Footer")
        
        ws['A1'] = "Links Count"
        ws['B1'] = "Sections Count"
        ws['C1'] = "Component Exists"
        
        for cell in ['A1', 'B1', 'C1']:
            ws[cell].font = Font(bold=True, color="FFFFFF")
            ws[cell].fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        
        ws.cell(row=2, column=1, value=footer_results.get('links_count', 0))
        ws.cell(row=2, column=2, value=footer_results.get('section_count', 0))
        ws.cell(row=2, column=3, value='Yes' if footer_results.get('component_exists') else 'No')
        
        ws.column_dimensions['A'].width = 20
        ws.column_dimensions['B'].width = 20
        ws.column_dimensions['C'].width = 20


