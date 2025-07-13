#!/usr/bin/env python3
"""
Pengu Report Generation Utilities
"""

import json
import os
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

def generate_ping_report(stats_summary, format_type="txt"):
    """Generate ping report in specified format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target_safe = stats_summary.get('target', 'unknown').replace(':', '_').replace('.', '_').replace('/', '_')
    ping_type = stats_summary.get('ping_type', 'ping')
    filename = f"{ping_type}_report_{target_safe}_{timestamp}.{format_type}"
    
    try:
        if format_type == "txt":
            generate_ping_txt_report(stats_summary, filename)
        elif format_type == "md":
            generate_ping_md_report(stats_summary, filename)
        elif format_type == "html":
            generate_ping_html_report(stats_summary, filename)
        elif format_type == "json":
            generate_ping_json_report(stats_summary, filename)
        
        return filename
    except Exception as e:
        print(f"{Fore.RED}Error generating report: {e}")
        return None

def generate_ping_txt_report(stats_summary, filename):
    """Generate plain text ping report"""
    with open(filename, 'w') as f:
        ping_type = stats_summary.get('ping_type', 'Ping').upper()
        f.write(f"PENGU {ping_type} REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Target:              {stats_summary.get('target', 'N/A')}\n")
        f.write(f"Test Date:           {stats_summary.get('start_time', 'N/A')}\n")
        f.write(f"Total Requests:      {stats_summary.get('total_requests', 0)}\n")
        f.write(f"Successful:          {stats_summary.get('successful_requests', 0)}\n")
        f.write(f"Failed:              {stats_summary.get('failed_requests', 0)}\n")
        f.write(f"Success Rate:        {stats_summary.get('success_rate', 0):.1f}%\n")
        f.write(f"Test Duration:       {stats_summary.get('duration', 0):.2f} seconds\n\n")
        
        f.write("RESPONSE TIME STATISTICS\n")
        f.write("-" * 30 + "\n")
        f.write(f"Average:             {stats_summary.get('avg_time', 0):.2f}ms\n")
        f.write(f"Minimum:             {stats_summary.get('min_time', 0):.2f}ms\n")
        f.write(f"Maximum:             {stats_summary.get('max_time', 0):.2f}ms\n")
        f.write(f"Timeouts:            {stats_summary.get('timeouts', 0)}\n")
        
        if 'status_codes' in stats_summary:
            f.write("\nSTATUS CODES\n")
            f.write("-" * 15 + "\n")
            for code, count in stats_summary['status_codes'].items():
                f.write(f"{code}: {count}\n")

def generate_ping_md_report(stats_summary, filename):
    """Generate Markdown ping report"""
    with open(filename, 'w') as f:
        ping_type = stats_summary.get('ping_type', 'Ping')
        f.write(f"# Pengu {ping_type} Report\n\n")
        f.write("## Test Summary\n\n")
        f.write(f"- **Target:** {stats_summary.get('target', 'N/A')}\n")
        f.write(f"- **Test Date:** {stats_summary.get('start_time', 'N/A')}\n")
        f.write(f"- **Total Requests:** {stats_summary.get('total_requests', 0)}\n")
        f.write(f"- **Successful:** {stats_summary.get('successful_requests', 0)}\n")
        f.write(f"- **Failed:** {stats_summary.get('failed_requests', 0)}\n")
        f.write(f"- **Success Rate:** {stats_summary.get('success_rate', 0):.1f}%\n")
        f.write(f"- **Test Duration:** {stats_summary.get('duration', 0):.2f} seconds\n\n")
        
        f.write("## Response Time Statistics\n\n")
        f.write(f"- **Average:** {stats_summary.get('avg_time', 0):.2f}ms\n")
        f.write(f"- **Minimum:** {stats_summary.get('min_time', 0):.2f}ms\n")
        f.write(f"- **Maximum:** {stats_summary.get('max_time', 0):.2f}ms\n")
        f.write(f"- **Timeouts:** {stats_summary.get('timeouts', 0)}\n\n")
        
        if 'status_codes' in stats_summary:
            f.write("## Status Codes\n\n")
            f.write("| Code | Count |\n")
            f.write("|------|-------|\n")
            for code, count in stats_summary['status_codes'].items():
                f.write(f"| {code} | {count} |\n")

def generate_ping_html_report(stats_summary, filename):
    """Generate HTML ping report"""
    with open(filename, 'w') as f:
        ping_type = stats_summary.get('ping_type', 'Ping')
        f.write(f"""<!DOCTYPE html>
<html>
<head>
    <title>Pengu {ping_type} Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .summary {{ background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        .stats {{ background-color: #f8f9fa; padding: 15px; margin: 20px 0; border-radius: 5px; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #3498db; color: white; }}
        .success {{ color: #27ae60; font-weight: bold; }}
        .error {{ color: #e74c3c; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐧 Pengu {ping_type} Report</h1>
    </div>
    
    <div class="summary">
        <h2>Test Summary</h2>
        <p><strong>Target:</strong> {stats_summary.get('target', 'N/A')}</p>
        <p><strong>Test Date:</strong> {stats_summary.get('start_time', 'N/A')}</p>
        <p><strong>Total Requests:</strong> {stats_summary.get('total_requests', 0)}</p>
        <p><strong>Successful:</strong> <span class="success">{stats_summary.get('successful_requests', 0)}</span></p>
        <p><strong>Failed:</strong> <span class="error">{stats_summary.get('failed_requests', 0)}</span></p>
        <p><strong>Success Rate:</strong> {stats_summary.get('success_rate', 0):.1f}%</p>
        <p><strong>Test Duration:</strong> {stats_summary.get('duration', 0):.2f} seconds</p>
    </div>
    
    <div class="stats">
        <h2>Response Time Statistics</h2>
        <p><strong>Average:</strong> {stats_summary.get('avg_time', 0):.2f}ms</p>
        <p><strong>Minimum:</strong> {stats_summary.get('min_time', 0):.2f}ms</p>
        <p><strong>Maximum:</strong> {stats_summary.get('max_time', 0):.2f}ms</p>
        <p><strong>Timeouts:</strong> {stats_summary.get('timeouts', 0)}</p>
    </div>""")
        
        if 'status_codes' in stats_summary:
            f.write("""
    <h2>Status Codes</h2>
    <table>
        <tr>
            <th>Status Code</th>
            <th>Count</th>
        </tr>""")
            for code, count in stats_summary['status_codes'].items():
                f.write(f"""
        <tr>
            <td>{code}</td>
            <td>{count}</td>
        </tr>""")
            f.write("\n    </table>")
        
        f.write("""
</body>
</html>""")

def generate_ping_json_report(stats_summary, filename):
    """Generate JSON ping report"""
    with open(filename, 'w') as f:
        json.dump(stats_summary, f, indent=2, default=str)

def show_report_generation_menu(stats_summary):
    """Show report generation menu"""
    while True:
        print(f"""
{Fore.YELLOW}Would you like to generate a report?
{Fore.GREEN}1. {Fore.WHITE}Text Report (.txt)
{Fore.GREEN}2. {Fore.WHITE}Markdown Report (.md)
{Fore.GREEN}3. {Fore.WHITE}HTML Report (.html)
{Fore.GREEN}4. {Fore.WHITE}JSON Report (.json)
{Fore.GREEN}5. {Fore.WHITE}Skip report generation
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-5): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            format_map = {'1': 'txt', '2': 'md', '3': 'html', '4': 'json'}
            format_type = format_map[choice]
            
            print(f"{Fore.CYAN}Generating {format_type.upper()} report...")
            filename = generate_ping_report(stats_summary, format_type)
            
            if filename:
                current_dir = os.getcwd()
                full_path = os.path.join(current_dir, filename)
                print(f"{Fore.GREEN}✓ Report saved as: {full_path}")
                
                # Option to open file
                try:
                    open_choice = input(f"{Fore.YELLOW}Would you like to try opening the file? (y/N): ").strip().lower()
                    if open_choice == 'y':
                        if os.name == 'nt':  # Windows
                            os.startfile(filename)
                        elif os.name == 'posix':  # Linux/Mac
                            os.system(f'xdg-open "{filename}" 2>/dev/null || open "{filename}" 2>/dev/null || echo "Please open {filename} manually"')
                except:
                    print(f"{Fore.YELLOW}Please open {filename} manually")
            break
        elif choice == '5':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-5.")