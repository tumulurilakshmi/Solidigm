"""
Report Generator for validation results
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class ReportGenerator:
    def __init__(self, output_dir: str = "reports"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def generate_report(self, validation_results: Dict) -> str:
        """Generate comprehensive external report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/validation_report_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(self._generate_text_report(validation_results))
        
        # Also generate JSON report
        json_filename = f"{self.output_dir}/validation_report_{timestamp}.json"
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(validation_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n[REPORT] Generated: {filename}")
        print(f"[REPORT] JSON report generated: {json_filename}")
        
        return filename
    
    def _generate_text_report(self, results: Dict) -> str:
        """Generate text-based report"""
        report_lines = []
        
        # Header
        report_lines.append("=" * 100)
        report_lines.append(" " * 30 + "SOLIDIGM VALIDATION REPORT")
        report_lines.append("=" * 100)
        report_lines.append("")
        
        # Validation Info
        report_lines.append("VALIDATION INFORMATION")
        report_lines.append("-" * 100)
        if 'validation_info' in results:
            report_lines.append(f"URL: {results['validation_info'].get('url', 'N/A')}")
            report_lines.append(f"Locale: {results['validation_info'].get('locale', 'N/A')}")
            report_lines.append(f"Timestamp: {results['validation_info'].get('timestamp', 'N/A')}")
        else:
            report_lines.append("URL: N/A")
            report_lines.append("Locale: N/A")
            report_lines.append("Timestamp: N/A")
        report_lines.append("")
        
        # Check if there was an error
        if 'error' in results:
            report_lines.append("ERROR OCCURRED")
            report_lines.append("-" * 100)
            report_lines.append(f"Error Message: {results['error']}")
            report_lines.append("")
            report_lines.append("=" * 100)
            report_lines.append(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            report_lines.append("=" * 100)
            return "\n".join(report_lines)
        
        # Overall Summary
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 100)
        summary = results.get('overall_summary', {})
        report_lines.append(f"Total UI Validations Performed: {summary.get('total_ui_validations', 0)}")
        report_lines.append(f"UI Validations Passed: {summary.get('passed_ui_validations', 0)}")
        report_lines.append(f"UI Validations Failed: {summary.get('failed_ui_validations', 0)}")
        report_lines.append(f"Total Links Checked: {summary.get('total_links', 0)}")
        report_lines.append(f"Valid Links: {summary.get('valid_links', 0)}")
        report_lines.append(f"Broken Links: {summary.get('broken_links', 0)}")
        report_lines.append("")
        
        # UI Validation Details
        ui_result = results.get('ui_validation', {})
        if 'summary' in ui_result:
            ui_summary = ui_result['summary']
            report_lines.append("UI VALIDATION DETAILS")
            report_lines.append("-" * 100)
            report_lines.append(f"Total UI Checks: {ui_summary['total_validations']}")
            report_lines.append(f"Passed: {ui_summary['passed']}")
            report_lines.append(f"Failed: {ui_summary['failed']}")
            report_lines.append(f"Pass Percentage: {ui_summary['pass_percentage']}%")
            report_lines.append("")
            
            # Category Breakdown
            report_lines.append("CATEGORY BREAKDOWN")
            report_lines.append("-" * 100)
            for category, data in ui_summary['by_category'].items():
                if data['total'] > 0:
                    report_lines.append(f"\n{category.upper().replace('_', ' ')}:")
                    report_lines.append(f"  Total: {data['total']}")
                    report_lines.append(f"  Passed: {data['passed']}")
                    report_lines.append(f"  Failed: {data['failed']}")
                    
                    # Show failure details
                    if data['failed'] > 0 and data['details']:
                        report_lines.append("  Failure Details:")
                        for detail in data['details'][:5]:  # Show first 5 failures
                            if isinstance(detail, dict) and 'details' in detail:
                                report_lines.append(f"    - {detail['details']}")
            report_lines.append("")
        
        # Link Validation Details
        link_result = results.get('link_validation', {})
        report_lines.append("LINK VALIDATION DETAILS")
        report_lines.append("-" * 100)
        report_lines.append(f"Total Links: {link_result.get('total_links', 0)}")
        report_lines.append(f"Valid Links: {link_result.get('valid_links', 0)}")
        report_lines.append(f"Broken Links: {link_result.get('broken_links', 0)}")
        
        # Show broken links
        if link_result.get('broken_links', 0) > 0 and link_result.get('broken_details', []):
            broken_details = link_result.get('broken_details', [])
            report_lines.append("\nBROKEN LINKS:")
            report_lines.append("-" * 100)
            for broken in broken_details[:10]:  # Show first 10
                report_lines.append(f"  URL: {broken['url']}")
                report_lines.append(f"  Text: {broken['text']}")
                report_lines.append(f"  Status: {broken['status_code']}")
                report_lines.append(f"  Message: {broken['message']}")
                report_lines.append("")
        
        # Failure Summary
        if summary.get('failed_ui_validations', 0) > 0 or summary.get('broken_links', 0) > 0:
            report_lines.append("")
            report_lines.append("FAILURE SUMMARY")
            report_lines.append("-" * 100)
            
            ui_details = ui_result['summary']['by_category']
            failures = []
            
            for category, data in ui_details.items():
                if data['failed'] > 0:
                    failures.append({
                        'category': category,
                        'count': data['failed'],
                        'issues': [d.get('details', '') for d in data['details'] if d.get('details')]
                    })
            
            for failure in failures:
                report_lines.append(f"\n{failure['category'].upper().replace('_', ' ')} - {failure['count']} failures:")
                for issue in failure['issues'][:3]:  # Show first 3 issues
                    report_lines.append(f"  • {issue}")
        
        # Footer
        report_lines.append("")
        report_lines.append("=" * 100)
        report_lines.append(f"Report generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("=" * 100)
        
        return "\n".join(report_lines)
    
    def generate_html_report(self, validation_results: Dict) -> str:
        """Generate HTML-based report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/validation_report_{timestamp}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
        <title>Solidigm Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                h2 {{ color: #555; margin-top: 30px; }}
                .summary {{ background: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0; }}
                .metric {{ display: inline-block; margin: 10px 20px; padding: 10px 20px; background: #fff; border-radius: 5px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
                .metric-label {{ font-size: 14px; color: #666; }}
                .passed {{ color: #28a745; }}
                .failed {{ color: #dc3545; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background: #007bff; color: white; }}
                tr:hover {{ background: #f5f5f5; }}
                .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 12px; }}
                .badge-success {{ background: #d4edda; color: #155724; }}
                .badge-danger {{ background: #f8d7da; color: #721c24; }}
                ul {{ line-height: 1.8; }}
                li {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔍 Solidigm Validation Report</h1>
                <p><strong>Generated:</strong> {validation_results['validation_info']['timestamp']}</p>
                <p><strong>URL:</strong> {validation_results['validation_info']['url']}</p>
                <p><strong>Locale:</strong> {validation_results['validation_info']['locale']}</p>
                
                <h2>Summary</h2>
                <div class="summary">
        """
        
        # Check if there was an error
        if 'error' in validation_results:
            html_content += f"""
                <div style="background: #f8d7da; color: #721c24; padding: 20px; border-radius: 5px; margin: 20px 0;">
                    <h3>Error Occurred</h3>
                    <p><strong>Error Message:</strong> {validation_results['error']}</p>
                </div>
            """
        else:
            overall_summary = validation_results.get('overall_summary', {})
            html_content += f"""
                    <div class="metric">
                        <div class="metric-value">{overall_summary.get('total_ui_validations', 0)}</div>
                        <div class="metric-label">UI Validations</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value passed">{overall_summary.get('passed_ui_validations', 0)}</div>
                        <div class="metric-label">Passed</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value failed">{overall_summary.get('failed_ui_validations', 0)}</div>
                        <div class="metric-label">Failed</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value">{overall_summary.get('total_links', 0)}</div>
                        <div class="metric-label">Total Links</div>
                    </div>
                    <div class="metric">
                        <div class="metric-value failed">{overall_summary.get('broken_links', 0)}</div>
                        <div class="metric-label">Broken Links</div>
                    </div>
                </div>
        """
        
        if 'error' in validation_results:
            html_content += """
            </div>
        </body>
        </html>
        """
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"[REPORT] HTML report generated: {filename}")
            return filename
        
        html_content += """
        """
        
        # Add details sections
        html_content += """
                <h2>UI Validation Details</h2>
                <table>
                    <tr>
                        <th>Category</th>
                        <th>Total</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Status</th>
                    </tr>
        """
        
        ui_summary = validation_results.get('ui_validation', {}).get('summary', {}).get('by_category', {})
        for category, data in ui_summary.items():
            if data['total'] > 0:
                status_class = 'passed' if data['failed'] == 0 else 'failed'
                html_content += f"""
                    <tr>
                        <td>{category.replace('_', ' ').title()}</td>
                        <td>{data['total']}</td>
                        <td>{data['passed']}</td>
                        <td>{data['failed']}</td>
                        <td><span class="badge badge-{status_class}">{'✓ Pass' if data['failed'] == 0 else '✗ Fail'}</span></td>
                    </tr>
                """
        
        html_content += "</table>"
        
        # Add broken links section
        broken_details = validation_results.get('link_validation', {}).get('broken_details', [])
        if broken_details:
            html_content += """
                <h2>Broken Links</h2>
                <ul>
            """
            for broken in broken_details[:10]:
                html_content += f"""
                    <li>
                        <strong>{broken['text']}</strong><br>
                        <small>{broken['url']}</small><br>
                        <span class="badge badge-danger">Status: {broken['status_code']}</span>
                    </li>
                """
            html_content += "</ul>"
        
        html_content += """
            </div>
        </body>
        </html>
        """
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"[REPORT] HTML report generated: {filename}")
        return filename

