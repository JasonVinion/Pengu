

#!/usr/bin/env python3
"""
Pengu Port Scanner - Advanced port scanner with statistics and report generation
"""

import socket
import threading
import time
import json
import os
from queue import Queue
from colorama import init, Fore, Style
from datetime import datetime

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the port scanner banner"""
    message = f"""
{Fore.GREEN} ╔════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Project Pengu Port Scanner{Fore.GREEN} ╚════╗
{Fore.GREEN} ║                                 ║
{Fore.GREEN} ╚═════════════════════════════════╝
"""
    print(message)

# Thread queue
queue = Queue()

# Thread-safe print and statistics
print_lock = threading.Lock()
stats_lock = threading.Lock()

class PortScanStats:
    """Class to track port scanning statistics"""
    def __init__(self):
        self.total_ports = 0
        self.open_ports = []
        self.closed_ports = 0
        self.start_time = None
        self.end_time = None
        self.target_ip = ""
        self.threads_used = 0
        
    def start_scan(self, ip, total_ports, threads):
        """Initialize scan statistics"""
        self.target_ip = ip
        self.total_ports = total_ports
        self.threads_used = threads
        self.start_time = datetime.now()
        
    def add_open_port(self, port, service_name=""):
        """Add an open port to statistics"""
        with stats_lock:
            self.open_ports.append({
                'port': port,
                'service': service_name,
                'timestamp': datetime.now()
            })
            
    def add_closed_port(self):
        """Increment closed port count"""
        with stats_lock:
            self.closed_ports += 1
            
    def finish_scan(self):
        """Mark scan as finished"""
        self.end_time = datetime.now()
        
    def get_summary(self):
        """Get scan summary"""
        scan_duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        
        return {
            'target_ip': self.target_ip,
            'total_ports_scanned': self.total_ports,
            'open_ports_count': len(self.open_ports),
            'closed_ports_count': self.closed_ports,
            'open_ports': self.open_ports,
            'threads_used': self.threads_used,
            'scan_duration': scan_duration,
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "",
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else ""
        }

# Global statistics instance
scan_stats = PortScanStats()

# Common service names for ports
COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 993: "IMAPS",
    995: "POP3S", 587: "SMTP", 465: "SMTPS", 3389: "RDP", 5432: "PostgreSQL",
    3306: "MySQL", 1433: "MSSQL", 6379: "Redis", 27017: "MongoDB"
}

def get_service_name(port):
    """Get common service name for port"""
    return COMMON_SERVICES.get(port, "Unknown")

def scan_port(ip, port):
    """Scan a single port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
            service_name = get_service_name(port)
            with print_lock:
                print(f"{Fore.GREEN}Port {port} is open on {ip} ({service_name})")
            scan_stats.add_open_port(port, service_name)
        except:
            scan_stats.add_closed_port()

def worker(ip):
    """Worker thread function"""
    while True:
        port = queue.get()
        if port is None:
            break
        scan_port(ip, port)
        queue.task_done()

def show_scan_statistics(stats_summary):
    """Display scan statistics"""
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Port Scan Statistics{Fore.CYAN}                  ║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝

{Fore.GREEN}Scan Summary:
{Fore.CYAN}  Target:           {Fore.WHITE}{stats_summary['target_ip']}
{Fore.CYAN}  Ports Scanned:    {Fore.WHITE}{stats_summary['total_ports_scanned']}
{Fore.CYAN}  Open Ports:       {Fore.WHITE}{stats_summary['open_ports_count']}
{Fore.CYAN}  Closed Ports:     {Fore.WHITE}{stats_summary['closed_ports_count']}
{Fore.CYAN}  Threads Used:     {Fore.WHITE}{stats_summary['threads_used']}
{Fore.CYAN}  Scan Duration:    {Fore.WHITE}{stats_summary['scan_duration']:.2f} seconds

{Fore.GREEN}Open Ports Details:""")
    
    if stats_summary['open_ports']:
        for port_info in stats_summary['open_ports']:
            print(f"{Fore.CYAN}  Port {Fore.WHITE}{port_info['port']:<6} {Fore.CYAN}({Fore.WHITE}{port_info['service']}{Fore.CYAN})")
    else:
        print(f"{Fore.YELLOW}  No open ports found")

def generate_report(stats_summary, format_type="txt"):
    """Generate scan report in specified format"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"port_scan_{stats_summary['target_ip'].replace('.', '_')}_{timestamp}.{format_type}"
    
    try:
        if format_type == "txt":
            generate_txt_report(stats_summary, filename)
        elif format_type == "md":
            generate_md_report(stats_summary, filename)
        elif format_type == "html":
            generate_html_report(stats_summary, filename)
        elif format_type == "json":
            generate_json_report(stats_summary, filename)
        
        return filename
    except Exception as e:
        print(f"{Fore.RED}Error generating report: {e}")
        return None

def generate_txt_report(stats_summary, filename):
    """Generate plain text report"""
    with open(filename, 'w') as f:
        f.write("PENGU PORT SCAN REPORT\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Target IP:           {stats_summary['target_ip']}\n")
        f.write(f"Scan Date:           {stats_summary['start_time']}\n")
        f.write(f"Ports Scanned:       {stats_summary['total_ports_scanned']}\n")
        f.write(f"Open Ports Found:    {stats_summary['open_ports_count']}\n")
        f.write(f"Closed Ports:        {stats_summary['closed_ports_count']}\n")
        f.write(f"Threads Used:        {stats_summary['threads_used']}\n")
        f.write(f"Scan Duration:       {stats_summary['scan_duration']:.2f} seconds\n\n")
        
        f.write("OPEN PORTS DETAILS\n")
        f.write("-" * 30 + "\n")
        if stats_summary['open_ports']:
            for port_info in stats_summary['open_ports']:
                f.write(f"Port {port_info['port']:<6} - {port_info['service']}\n")
        else:
            f.write("No open ports found\n")

def generate_md_report(stats_summary, filename):
    """Generate Markdown report"""
    with open(filename, 'w') as f:
        f.write("# Pengu Port Scan Report\n\n")
        f.write("## Scan Summary\n\n")
        f.write(f"- **Target IP:** {stats_summary['target_ip']}\n")
        f.write(f"- **Scan Date:** {stats_summary['start_time']}\n")
        f.write(f"- **Ports Scanned:** {stats_summary['total_ports_scanned']}\n")
        f.write(f"- **Open Ports Found:** {stats_summary['open_ports_count']}\n")
        f.write(f"- **Closed Ports:** {stats_summary['closed_ports_count']}\n")
        f.write(f"- **Threads Used:** {stats_summary['threads_used']}\n")
        f.write(f"- **Scan Duration:** {stats_summary['scan_duration']:.2f} seconds\n\n")
        
        f.write("## Open Ports\n\n")
        if stats_summary['open_ports']:
            f.write("| Port | Service |\n")
            f.write("|------|--------|\n")
            for port_info in stats_summary['open_ports']:
                f.write(f"| {port_info['port']} | {port_info['service']} |\n")
        else:
            f.write("No open ports found.\n")

def generate_html_report(stats_summary, filename):
    """Generate HTML report"""
    with open(filename, 'w') as f:
        f.write("""<!DOCTYPE html>
<html>
<head>
    <title>Pengu Port Scan Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .summary { background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #3498db; color: white; }
        .open-port { color: #27ae60; font-weight: bold; }
        .closed-count { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🐧 Pengu Port Scan Report</h1>
    </div>
    
    <div class="summary">
        <h2>Scan Summary</h2>""")
        
        f.write(f"""
        <p><strong>Target IP:</strong> {stats_summary['target_ip']}</p>
        <p><strong>Scan Date:</strong> {stats_summary['start_time']}</p>
        <p><strong>Ports Scanned:</strong> {stats_summary['total_ports_scanned']}</p>
        <p><strong>Open Ports Found:</strong> <span class="open-port">{stats_summary['open_ports_count']}</span></p>
        <p><strong>Closed Ports:</strong> <span class="closed-count">{stats_summary['closed_ports_count']}</span></p>
        <p><strong>Threads Used:</strong> {stats_summary['threads_used']}</p>
        <p><strong>Scan Duration:</strong> {stats_summary['scan_duration']:.2f} seconds</p>
    </div>
    
    <h2>Open Ports Details</h2>""")
        
        if stats_summary['open_ports']:
            f.write("""
    <table>
        <tr>
            <th>Port</th>
            <th>Service</th>
            <th>Detection Time</th>
        </tr>""")
            for port_info in stats_summary['open_ports']:
                f.write(f"""
        <tr>
            <td class="open-port">{port_info['port']}</td>
            <td>{port_info['service']}</td>
            <td>{port_info['timestamp'].strftime('%H:%M:%S')}</td>
        </tr>""")
            f.write("\n    </table>")
        else:
            f.write("<p>No open ports found.</p>")
        
        f.write("""
</body>
</html>""")

def generate_json_report(stats_summary, filename):
    """Generate JSON report"""
    # Convert datetime objects to strings for JSON serialization
    json_data = stats_summary.copy()
    for port_info in json_data['open_ports']:
        port_info['timestamp'] = port_info['timestamp'].isoformat()
    
    with open(filename, 'w') as f:
        json.dump(json_data, f, indent=2)

def show_report_options(stats_summary):
    """Show report generation options"""
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
            filename = generate_report(stats_summary, format_type)
            
            if filename:
                current_dir = os.getcwd()
                full_path = os.path.join(current_dir, filename)
                print(f"{Fore.GREEN}✓ Report saved as: {full_path}")
                
                # Option to open file (basic implementation)
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

def show_scan_exit_options():
    """Show exit options after scan completion"""
    while True:
        print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Run another port scan
{Fore.GREEN}2. {Fore.WHITE}Return to home menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-2): ").strip()
        
        if choice == '1':
            return 'scan_again'
        elif choice == '2':
            return 'home'
        else:
            print(f"{Fore.RED}Invalid option. Please select 1 or 2.")

def main():
    """Main port scanner function"""
    print_banner()
    global scan_stats
    
    while True:
        try:
            ip = input("Enter IP address (or 'exit' to quit): ").strip()
            if ip.lower() in ['exit', 'quit']:
                break
                
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            
            # Get thread count with hardware recommendation
            try:
                # Try to get hardware-based recommendation
                try:
                    import system_specs
                    recommended_threads = system_specs.system_specs.get_thread_recommendation('port_scanning')
                    print(f"{Fore.GREEN}Hardware-based recommendation: {recommended_threads} threads")
                except:
                    recommended_threads = 50
                    print(f"{Fore.YELLOW}Using default recommendation: {recommended_threads} threads")
                
                thread_input = input(f"{Fore.CYAN}Enter number of threads (default: {recommended_threads}): ").strip()
                if thread_input:
                    num_threads = int(thread_input)
                    if num_threads > 200:
                        print(f"{Fore.YELLOW}Warning: Very high thread count ({num_threads}) may overwhelm the target!")
                        confirm = input(f"{Fore.YELLOW}Continue anyway? (y/N): ").strip().lower()
                        if confirm != 'y':
                            continue
                else:
                    num_threads = recommended_threads
                    
            except ValueError:
                print(f"{Fore.RED}Invalid thread count. Using default: 50")
                num_threads = 50
                
            num_threads = min(num_threads, 200)  # Hard limit for safety
            
            # Initialize scan statistics
            total_ports = end_port - start_port + 1
            scan_stats = PortScanStats()
            scan_stats.start_scan(ip, total_ports, num_threads)
            
            print(f"{Fore.CYAN}Scanning {ip} ports {start_port}-{end_port} with {num_threads} threads...")
            
            # Start worker threads
            threads = []
            for _ in range(num_threads):
                t = threading.Thread(target=worker, args=(ip,))
                t.daemon = True  # Allow main thread to exit
                t.start()
                threads.append(t)

            # Put ports in queue
            for port in range(start_port, end_port + 1):
                queue.put(port)

            # Block until all tasks are done
            queue.join()

            # Stop workers
            for _ in range(num_threads):
                queue.put(None)
            for t in threads:
                t.join()
            
            # Finish scan and show statistics
            scan_stats.finish_scan()
            stats_summary = scan_stats.get_summary()
            
            print(f"{Fore.GREEN}Scan complete for {ip}!")
            show_scan_statistics(stats_summary)
            
            # Report generation options
            show_report_options(stats_summary)
            
            # Exit options
            result = show_scan_exit_options()
            if result == 'home':
                # Import and run home command
                try:
                    import pengu
                    pengu.return_to_home()
                    break
                except:
                    break
            elif result == 'scan_again':
                continue  # Start another scan
            
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter valid numbers.")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nScan interrupted by user.")
            # Show exit options even if interrupted
            result = show_scan_exit_options()
            if result == 'home':
                try:
                    import pengu
                    pengu.return_to_home()
                except:
                    pass
                break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    main()
