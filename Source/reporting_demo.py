#!/usr/bin/env python3
"""
Enhanced Reporting System - Demo Implementation
Demonstrates advanced reporting capabilities for Pengu Network Tools
"""

import json
import csv
from datetime import datetime
from pathlib import Path
import webbrowser
import tempfile

try:
    from jinja2 import Template
    JINJA2_AVAILABLE = True
except ImportError:
    JINJA2_AVAILABLE = False
    print("Note: jinja2 not available. HTML reports will use basic template.")

class ReportGenerator:
    def __init__(self):
        self.templates_dir = Path(__file__).parent.parent / "templates"
        self.output_dir = Path.home() / "pengu_reports"
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_sample_data(self):
        """Generate sample scan data for demonstration"""
        return {
            'scan_target': 'example.com',
            'scan_duration': 45.7,
            'scan_types': ['Port Scan', 'DNS Enumeration', 'SSL Analysis'],
            'generated_at': datetime.now(),
            'tool_version': 'Pengu Network Tools v1.0 (Enhanced)',
            'summary': {
                'hosts_scanned': 1,
                'ports_open': 5,
                'services_identified': 4,
                'security_issues': 2
            },
            'results': {
                'port_scan': {
                    'example.com': [
                        {
                            'number': 22,
                            'protocol': 'tcp',
                            'status': 'open',
                            'service': 'SSH',
                            'version': 'OpenSSH 8.2'
                        },
                        {
                            'number': 80,
                            'protocol': 'tcp',
                            'status': 'open',
                            'service': 'HTTP',
                            'version': 'nginx/1.18.0'
                        },
                        {
                            'number': 443,
                            'protocol': 'tcp',
                            'status': 'open',
                            'service': 'HTTPS',
                            'version': 'nginx/1.18.0'
                        },
                        {
                            'number': 25,
                            'protocol': 'tcp',
                            'status': 'open',
                            'service': 'SMTP',
                            'version': 'Postfix'
                        },
                        {
                            'number': 993,
                            'protocol': 'tcp',
                            'status': 'open',
                            'service': 'IMAPS',
                            'version': 'Dovecot'
                        }
                    ]
                },
                'dns_enum': {
                    'subdomains': [
                        {'name': 'www.example.com', 'ips': ['93.184.216.34']},
                        {'name': 'mail.example.com', 'ips': ['93.184.216.35']},
                        {'name': 'ftp.example.com', 'ips': ['93.184.216.36']},
                        {'name': 'api.example.com', 'ips': ['93.184.216.37']}
                    ],
                    'records': {
                        'A': ['93.184.216.34'],
                        'MX': ['10 mail.example.com'],
                        'NS': ['ns1.example.com', 'ns2.example.com'],
                        'TXT': ['v=spf1 include:_spf.google.com ~all']
                    }
                },
                'ssl_analysis': {
                    'example.com:443': {
                        'subject': 'CN=example.com',
                        'issuer': 'CN=DigiCert SHA2 Secure Server CA',
                        'valid_from': '2023-01-01 00:00:00',
                        'valid_until': '2024-01-01 00:00:00',
                        'protocol': 'TLSv1.3',
                        'security_rating': 85,
                        'expired': False
                    }
                }
            },
            'recommendations': [
                {
                    'severity': 'Medium',
                    'description': 'SSH service detected on standard port 22',
                    'remediation': 'Consider changing SSH to a non-standard port and implementing key-based authentication'
                },
                {
                    'severity': 'Low',
                    'description': 'Multiple services exposed publicly',
                    'remediation': 'Review which services need to be publicly accessible and implement appropriate access controls'
                }
            ]
        }
    
    def generate_json_report(self, scan_data, filename=None):
        """Generate JSON format report"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f"pengu_report_{timestamp}.json"
        
        # Prepare data for JSON serialization
        json_data = scan_data.copy()
        json_data['generated_at'] = scan_data['generated_at'].isoformat()
        
        with open(filename, 'w') as f:
            json.dump(json_data, f, indent=2, sort_keys=True)
        
        return filename
    
    def generate_csv_report(self, scan_data, filename=None):
        """Generate CSV format report (simplified)"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f"pengu_report_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write metadata
            writer.writerow(['Report Metadata'])
            writer.writerow(['Generated At', scan_data['generated_at']])
            writer.writerow(['Target', scan_data['scan_target']])
            writer.writerow(['Duration (s)', scan_data['scan_duration']])
            writer.writerow([])
            
            # Write port scan results
            if 'port_scan' in scan_data['results']:
                writer.writerow(['Port Scan Results'])
                writer.writerow(['Host', 'Port', 'Protocol', 'Status', 'Service', 'Version'])
                
                for host, ports in scan_data['results']['port_scan'].items():
                    for port in ports:
                        writer.writerow([
                            host,
                            port['number'],
                            port['protocol'],
                            port['status'],
                            port.get('service', ''),
                            port.get('version', '')
                        ])
                writer.writerow([])
            
            # Write DNS results
            if 'dns_enum' in scan_data['results']:
                writer.writerow(['DNS Enumeration Results'])
                writer.writerow(['Type', 'Name', 'Value'])
                
                if 'subdomains' in scan_data['results']['dns_enum']:
                    for subdomain in scan_data['results']['dns_enum']['subdomains']:
                        writer.writerow(['Subdomain', subdomain['name'], ', '.join(subdomain['ips'])])
                
                if 'records' in scan_data['results']['dns_enum']:
                    for record_type, records in scan_data['results']['dns_enum']['records'].items():
                        for record in records:
                            writer.writerow(['DNS Record', record_type, record])
        
        return filename
    
    def generate_html_report(self, scan_data, filename=None):
        """Generate HTML format report"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f"pengu_report_{timestamp}.html"
        
        if JINJA2_AVAILABLE:
            # Use Jinja2 template
            template_file = self.templates_dir / "report_template.html"
            if template_file.exists():
                with open(template_file, 'r') as f:
                    template_content = f.read()
                
                template = Template(template_content)
                html_content = template.render(**scan_data)
            else:
                html_content = self.generate_basic_html_report(scan_data)
        else:
            html_content = self.generate_basic_html_report(scan_data)
        
        with open(filename, 'w') as f:
            f.write(html_content)
        
        return filename
    
    def generate_basic_html_report(self, scan_data):
        """Generate basic HTML report without Jinja2"""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Pengu Network Tools - Scan Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #4a90e2; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border-left: 4px solid #4a90e2; }}
        .port-open {{ color: green; font-weight: bold; }}
        .port-closed {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🐧 Pengu Network Tools</h1>
        <h2>Network Security Assessment Report</h2>
        <p>Generated: {scan_data['generated_at']}</p>
        <p>Target: {scan_data['scan_target']}</p>
    </div>
    
    <div class="section">
        <h3>📊 Summary</h3>
        <ul>
            <li>Hosts Scanned: {scan_data['summary']['hosts_scanned']}</li>
            <li>Open Ports: {scan_data['summary']['ports_open']}</li>
            <li>Services Identified: {scan_data['summary']['services_identified']}</li>
            <li>Security Issues: {scan_data['summary']['security_issues']}</li>
        </ul>
    </div>
"""
        
        # Add port scan results
        if 'port_scan' in scan_data['results']:
            html += '<div class="section"><h3>🔍 Port Scan Results</h3><table>'
            html += '<tr><th>Host</th><th>Port</th><th>Status</th><th>Service</th><th>Version</th></tr>'
            
            for host, ports in scan_data['results']['port_scan'].items():
                for port in ports:
                    status_class = 'port-open' if port['status'] == 'open' else 'port-closed'
                    html += f'''
                    <tr>
                        <td>{host}</td>
                        <td>{port['number']}</td>
                        <td class="{status_class}">{port['status']}</td>
                        <td>{port.get('service', 'Unknown')}</td>
                        <td>{port.get('version', 'Unknown')}</td>
                    </tr>
                    '''
            html += '</table></div>'
        
        # Add DNS enumeration results
        if 'dns_enum' in scan_data['results']:
            html += '<div class="section"><h3>🌐 DNS Enumeration</h3>'
            
            if 'subdomains' in scan_data['results']['dns_enum']:
                html += '<h4>Subdomains:</h4><ul>'
                for subdomain in scan_data['results']['dns_enum']['subdomains']:
                    html += f"<li>{subdomain['name']} → {', '.join(subdomain['ips'])}</li>"
                html += '</ul>'
            
            html += '</div>'
        
        html += """
    <div class="section">
        <h3>⚠️ Disclaimer</h3>
        <p>This report is generated by automated security scanning tools. Results should be verified manually and used responsibly.</p>
    </div>
</body>
</html>
"""
        return html
    
    def generate_text_report(self, scan_data, filename=None):
        """Generate plain text report"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.output_dir / f"pengu_report_{timestamp}.txt"
        
        report_lines = []
        report_lines.append("=" * 60)
        report_lines.append("PENGU NETWORK TOOLS - SCAN REPORT")
        report_lines.append("=" * 60)
        report_lines.append(f"Generated: {scan_data['generated_at']}")
        report_lines.append(f"Target: {scan_data['scan_target']}")
        report_lines.append(f"Duration: {scan_data['scan_duration']} seconds")
        report_lines.append(f"Tool Version: {scan_data['tool_version']}")
        report_lines.append("")
        
        # Summary
        report_lines.append("SUMMARY")
        report_lines.append("-" * 30)
        summary = scan_data['summary']
        report_lines.append(f"Hosts Scanned: {summary['hosts_scanned']}")
        report_lines.append(f"Open Ports: {summary['ports_open']}")
        report_lines.append(f"Services Identified: {summary['services_identified']}")
        report_lines.append(f"Security Issues: {summary['security_issues']}")
        report_lines.append("")
        
        # Port scan results
        if 'port_scan' in scan_data['results']:
            report_lines.append("PORT SCAN RESULTS")
            report_lines.append("-" * 30)
            for host, ports in scan_data['results']['port_scan'].items():
                report_lines.append(f"Host: {host}")
                for port in ports:
                    service = port.get('service', 'Unknown')
                    version = port.get('version', '')
                    report_lines.append(f"  {port['number']}/{port['protocol']} - {port['status']} - {service} {version}")
                report_lines.append("")
        
        # DNS enumeration
        if 'dns_enum' in scan_data['results']:
            report_lines.append("DNS ENUMERATION RESULTS")
            report_lines.append("-" * 30)
            
            if 'subdomains' in scan_data['results']['dns_enum']:
                report_lines.append("Subdomains:")
                for subdomain in scan_data['results']['dns_enum']['subdomains']:
                    report_lines.append(f"  {subdomain['name']} → {', '.join(subdomain['ips'])}")
                report_lines.append("")
            
            if 'records' in scan_data['results']['dns_enum']:
                report_lines.append("DNS Records:")
                for record_type, records in scan_data['results']['dns_enum']['records'].items():
                    report_lines.append(f"  {record_type}: {', '.join(records)}")
                report_lines.append("")
        
        # Recommendations
        if 'recommendations' in scan_data:
            report_lines.append("SECURITY RECOMMENDATIONS")
            report_lines.append("-" * 30)
            for i, rec in enumerate(scan_data['recommendations'], 1):
                report_lines.append(f"{i}. [{rec['severity']}] {rec['description']}")
                if 'remediation' in rec:
                    report_lines.append(f"   Remediation: {rec['remediation']}")
                report_lines.append("")
        
        report_lines.append("=" * 60)
        report_lines.append("End of Report")
        report_lines.append("=" * 60)
        
        with open(filename, 'w') as f:
            f.write('\n'.join(report_lines))
        
        return filename
    
    def generate_all_formats(self, scan_data):
        """Generate reports in all supported formats"""
        reports = {}
        
        print("Generating reports in all formats...")
        
        try:
            reports['json'] = self.generate_json_report(scan_data)
            print(f"✓ JSON report: {reports['json']}")
        except Exception as e:
            print(f"✗ JSON report failed: {e}")
        
        try:
            reports['csv'] = self.generate_csv_report(scan_data)
            print(f"✓ CSV report: {reports['csv']}")
        except Exception as e:
            print(f"✗ CSV report failed: {e}")
        
        try:
            reports['html'] = self.generate_html_report(scan_data)
            print(f"✓ HTML report: {reports['html']}")
        except Exception as e:
            print(f"✗ HTML report failed: {e}")
        
        try:
            reports['text'] = self.generate_text_report(scan_data)
            print(f"✓ Text report: {reports['text']}")
        except Exception as e:
            print(f"✗ Text report failed: {e}")
        
        return reports

def main():
    """Demo the reporting functionality"""
    print("🐧 Pengu Network Tools - Enhanced Reporting Demo")
    print("=" * 50)
    
    generator = ReportGenerator()
    
    # Generate sample data
    print("Generating sample scan data...")
    sample_data = generator.generate_sample_data()
    
    print(f"Sample data created for target: {sample_data['scan_target']}")
    print(f"Reports will be saved to: {generator.output_dir}")
    print()
    
    # Generate all report formats
    reports = generator.generate_all_formats(sample_data)
    
    print()
    print("Report generation complete!")
    print()
    
    # Ask if user wants to open HTML report
    if 'html' in reports:
        response = input("Would you like to open the HTML report in your browser? (y/n): ")
        if response.lower() == 'y':
            try:
                webbrowser.open(f"file://{reports['html']}")
                print("HTML report opened in browser.")
            except Exception as e:
                print(f"Could not open browser: {e}")
    
    print(f"\nAll reports saved to: {generator.output_dir}")
    print("You can find the generated files there.")

if __name__ == "__main__":
    main()