#!/usr/bin/env python3
"""
Pengu Enhanced Ping Module - Advanced ICMP ping with enhanced features
"""

import os
import sys
import time
import socket
import threading
import subprocess
import statistics
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import platform-specific modules
if os.name == 'nt':
    import msvcrt

# Global flag for stopping ping
stop_ping = False

class PingStats:
    """Class to track ping statistics"""
    def __init__(self):
        self.packets_sent = 0
        self.packets_received = 0
        self.response_times = []
        self.timeouts = 0
        
    def add_response(self, response_time):
        """Add a successful response"""
        self.packets_sent += 1
        self.packets_received += 1
        self.response_times.append(response_time)
        
    def add_timeout(self):
        """Add a timeout"""
        self.packets_sent += 1
        self.timeouts += 1
        
    def get_summary(self):
        """Get statistics summary"""
        if not self.response_times:
            return {
                'packets_sent': self.packets_sent,
                'packets_received': self.packets_received,
                'packet_loss': 100.0,
                'avg_time': 0,
                'min_time': 0,
                'max_time': 0,
                'timeouts': self.timeouts
            }
            
        return {
            'packets_sent': self.packets_sent,
            'packets_received': self.packets_received,
            'packet_loss': ((self.packets_sent - self.packets_received) / self.packets_sent * 100) if self.packets_sent > 0 else 0,
            'avg_time': statistics.mean(self.response_times),
            'min_time': min(self.response_times),
            'max_time': max(self.response_times),
            'timeouts': self.timeouts
        }

def check_for_q_key():
    """Monitor for 'Q' key press to stop ping"""
    global stop_ping
    
    if os.name == 'nt':  # Windows
        while not stop_ping:
            try:
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'q':
                        stop_ping = True
                        break
            except:
                pass
            time.sleep(0.1)
    else:  # Linux/Unix
        try:
            import select
            import termios
            import tty
            
            # Check if stdin is a TTY (interactive terminal)
            if not sys.stdin.isatty():
                return  # Not interactive, skip key monitoring
            
            old_settings = termios.tcgetattr(sys.stdin)
            try:
                tty.setraw(sys.stdin.fileno())
                while not stop_ping:
                    if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                        key = sys.stdin.read(1).lower()
                        if key == 'q':
                            stop_ping = True
                            break
            finally:
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        except Exception:
            # If there's any issue with terminal control, just skip key monitoring
            pass

def print_ping_header(hostname):
    """Print static header for ping output"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Pengu Pinger{Fore.CYAN}                     ║
{Fore.CYAN}║              {Fore.YELLOW}Press Q to stop{Fore.CYAN}                   ║
{Fore.CYAN}╚════════════════════════════════════════════════╝
{Fore.GREEN}Target: {Fore.WHITE}{hostname}
{Fore.YELLOW}═══════════════════════════════════════════════════
""")

def countdown_timer(seconds):
    """Show countdown before starting ping"""
    for i in range(seconds, 0, -1):
        print(f"{Fore.YELLOW}Starting ping in {i} seconds...", end='\r')
        time.sleep(1)
    print(f"{Fore.GREEN}Starting ping now!           ")

def parse_ping_output_with_stats(line, hostname):
    """Parse ping output and return formatted result with color coding and response time"""
    if "Request timed out" in line or "Destination Host Unreachable" in line:
        return f"{Fore.RED}✗ Request timed out", None
    elif "TTL expired" in line:
        return f"{Fore.RED}✗ TTL expired", None
    elif "time=" in line or "time<" in line:
        # Extract response time
        import re
        time_match = re.search(r'time[<=](\d+(?:\.\d+)?)ms', line)
        if time_match:
            response_time = float(time_match.group(1))
            
            # Color code based on response time
            if response_time <= 50:
                color = Fore.GREEN
                status = "✓"
            elif response_time <= 400:
                color = Fore.GREEN
                status = "✓"
            else:
                color = Fore.YELLOW
                status = "⚠"
            
            return f"{color}{status} Reply from {hostname}: time={response_time}ms", response_time
        else:
            return f"{Fore.GREEN}✓ Reply from {hostname}", 0.0
    else:
        return None, None

def get_host_enrichment_data(hostname):
    """Get enrichment data for ping reports (Issue 6)"""
    enrichment = {
        'hostname': hostname,
        'ip_address': 'N/A', 
        'reverse_dns': 'N/A',
        'isp': 'N/A',
        'organization': 'N/A'
    }
    
    try:
        # Resolve hostname to IP if needed
        import socket
        if hostname.replace('.', '').isdigit() or ':' in hostname:  # IP address
            enrichment['ip_address'] = hostname
            # Try reverse DNS lookup
            try:
                reverse_result = socket.gethostbyaddr(hostname)
                enrichment['reverse_dns'] = reverse_result[0]
            except:
                pass
        else:  # Hostname
            try:
                ip = socket.gethostbyname(hostname)
                enrichment['ip_address'] = ip
                enrichment['reverse_dns'] = hostname
            except:
                pass
        
        # Try to get ISP/Organization data via whois if available
        try:
            import subprocess
            result = subprocess.run(['whois', enrichment['ip_address']], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.lower()
                # Extract ISP/Organization
                for line in lines.split('\n'):
                    if 'org:' in line or 'orgname:' in line:
                        enrichment['organization'] = line.split(':', 1)[1].strip()
                        break
                    elif 'netname:' in line:
                        enrichment['isp'] = line.split(':', 1)[1].strip()
                        break
        except:
            pass
            
    except Exception:
        pass
    
    return enrichment

def show_ping_statistics(stats, hostname):
    """Display ping statistics with enrichment data (Issue 6)"""
    summary = stats.get_summary()
    enrichment = get_host_enrichment_data(hostname)
    
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Ping Statistics for {hostname:<15}{Fore.CYAN}     ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝

{Fore.GREEN}Host Information:
{Fore.CYAN}  Hostname:     {Fore.WHITE}{enrichment['reverse_dns']}
{Fore.CYAN}  IP Address:   {Fore.WHITE}{enrichment['ip_address']}
{Fore.CYAN}  ISP:          {Fore.WHITE}{enrichment['isp']}
{Fore.CYAN}  Organization: {Fore.WHITE}{enrichment['organization']}

{Fore.GREEN}Packets:
{Fore.CYAN}  Sent:         {Fore.WHITE}{summary['packets_sent']}
{Fore.CYAN}  Received:     {Fore.WHITE}{summary['packets_received']}
{Fore.CYAN}  Lost:         {Fore.WHITE}{summary['timeouts']} ({summary['packet_loss']:.1f}% loss)

{Fore.GREEN}Response Times:
{Fore.CYAN}  Average:      {Fore.WHITE}{summary['avg_time']:.2f}ms
{Fore.CYAN}  Minimum:      {Fore.WHITE}{summary['min_time']:.2f}ms
{Fore.CYAN}  Maximum:      {Fore.WHITE}{summary['max_time']:.2f}ms
{Fore.CYAN}  Timeouts:     {Fore.WHITE}{summary['timeouts']}
""")

def export_ping_results(stats, hostname, ping_type="ICMP"):
    """Export ping statistics with enrichment data to a file (Issue 6)"""
    try:
        from datetime import datetime
        import json
        import os
        
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hostname_safe = hostname.replace(':', '_').replace('.', '_').replace('/', '_')
        filename = f"ping_report_{hostname_safe}_{timestamp}.txt"
        
        # Get statistics summary and enrichment data
        summary = stats.get_summary()
        enrichment = get_host_enrichment_data(hostname)
        
        # Generate report content
        report_content = f"""PENGU {ping_type.upper()} PING REPORT
{'=' * 50}

Target:              {hostname}
Test Date:           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test Type:           {ping_type} Ping

HOST INFORMATION
{'-' * 30}
Hostname:            {enrichment['reverse_dns']}
IP Address:          {enrichment['ip_address']}
ISP:                 {enrichment['isp']}
Organization:        {enrichment['organization']}

PACKET STATISTICS
{'-' * 30}
Total Sent:          {summary['packets_sent']}
Received:            {summary['packets_received']}
Lost:                {summary['timeouts']}
Packet Loss:         {summary['packet_loss']:.1f}%

RESPONSE TIME STATISTICS
{'-' * 30}
Average:             {summary['avg_time']:.2f}ms
Minimum:             {summary['min_time']:.2f}ms
Maximum:             {summary['max_time']:.2f}ms
Timeouts:            {summary['timeouts']}

Report generated by Pengu v2.1
"""
        
        # Write to file
        with open(filename, 'w') as f:
            f.write(report_content)
        
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, filename)
        print(f"{Fore.GREEN}✓ Ping report exported to: {full_path}")
        
        return filename
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting report: {e}")
        return None

def export_mass_ping_results(host_stats):
    """Export mass ping statistics to a file (Fix for Issue 5)"""
    try:
        from datetime import datetime
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"mass_ping_report_{timestamp}.txt"
        
        # Use new output directory structure
        try:
            from pengu import get_output_path
            full_path = get_output_path("reports", filename)
        except:
            # Fallback if import fails
            full_path = filename
        
        content = f"""Mass Ping Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

"""
        
        for hostname, stats in host_stats.items():
            summary = stats.get_summary()
            enrichment = get_host_enrichment_data(hostname)
            content += f"""Host: {hostname}
  Hostname (Reverse DNS): {enrichment['reverse_dns']}
  IP Address: {enrichment['ip_address']}
  ISP: {enrichment['isp']}
  Organization: {enrichment['organization']}
  Packets Sent: {summary['packets_sent']}
  Packets Received: {summary['packets_received']}
  Packet Loss: {summary['packet_loss']:.1f}%
  Average Time: {summary['avg_time']:.2f}ms
  Minimum Time: {summary['min_time']:.2f}ms
  Maximum Time: {summary['max_time']:.2f}ms
  Timeouts: {summary['timeouts']}

"""
        
        content += f"Report generated by Pengu v2.1\n"
        
        # Write with UTF-8 encoding
        with open(full_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
        
        print(f"{Fore.GREEN}✓ Mass ping report exported to: {full_path}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting mass ping report: {e}")
        return False

def show_ping_exit_options(stats=None, hostname=None, ping_type="ICMP"):
    """Show exit options after ping completion"""
    while True:
        try:
            print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Go back to ping tools
{Fore.GREEN}2. {Fore.WHITE}Export results to file
{Fore.GREEN}3. {Fore.WHITE}Return to home menu
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
            
            if choice == '1':
                return 'ping_tools'
            elif choice == '2':
                if stats and hostname:
                    export_ping_results(stats, hostname, ping_type)
                else:
                    print(f"{Fore.RED}No statistics available to export")
                # Continue the loop to show options again
            elif choice == '3':
                return 'home'
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-3.")
                
        except KeyboardInterrupt:
            return 'home'
        except:
            return 'home'

def show_mass_ping_exit_options(host_stats=None):
    """Show exit options after mass ping completion (Fix for Issue 5)"""
    while True:
        try:
            print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Go back to ping tools
{Fore.GREEN}2. {Fore.WHITE}Export results to file
{Fore.GREEN}3. {Fore.WHITE}Return to home menu
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
            
            if choice == '1':
                return 'ping_tools'
            elif choice == '2':
                if host_stats:
                    export_mass_ping_results(host_stats)
                else:
                    print(f"{Fore.RED}No statistics available to export")
                # Continue the loop to show options again
            elif choice == '3':
                return 'home'
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-3.")
                
        except KeyboardInterrupt:
            return 'home'
        except:
            return 'home'
    """Show exit options after ping completion"""
    while True:
        try:
            print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Go back to ping tools
{Fore.GREEN}2. {Fore.WHITE}Export results to file
{Fore.GREEN}3. {Fore.WHITE}Return to home menu
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
            
            if choice == '1':
                return 'ping_tools'
            elif choice == '2':
                if stats and hostname:
                    export_ping_results(stats, hostname, ping_type)
                else:
                    print(f"{Fore.RED}No statistics available to export")
                # Continue the loop to show options again
            elif choice == '3':
                return 'home'
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-3.")
                
        except KeyboardInterrupt:
            return 'home'
        except:
            return 'home'

def enhanced_icmp_ping(hostname):
    """Enhanced ICMP ping with color coding, stats, and Q to quit"""
    global stop_ping
    stop_ping = False
    
    print_ping_header(hostname)
    
    # Start countdown
    countdown_timer(3)
    
    # Initialize statistics
    stats = PingStats()
    
    # Start key monitoring thread
    key_thread = threading.Thread(target=check_for_q_key, daemon=True)
    key_thread.start()
    
    try:
        # Prepare ping command
        if os.name == 'nt':  # Windows
            cmd = ['ping', '-t', hostname]
        else:  # Linux/Unix
            cmd = ['ping', hostname]
        
        # Start ping process
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                 text=True, bufsize=1, universal_newlines=True)
        
        while not stop_ping:
            try:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                
                if line.strip():
                    formatted_output, response_time = parse_ping_output_with_stats(line.strip(), hostname)
                    if formatted_output:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{Fore.CYAN}{timestamp}{Fore.WHITE}] {formatted_output}")
                        
                        # Update statistics
                        if response_time is not None:
                            stats.add_response(response_time)
                        else:
                            stats.add_timeout()
                
                # Add small delay to prevent overwhelming output
                time.sleep(0.1)
                
            except Exception as e:
                print(f"{Fore.RED}Error reading ping output: {e}")
                break
        
        # Clean shutdown
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # Show statistics
        show_ping_statistics(stats, hostname)
        
        # Exit options
        show_ping_exit_options(stats, hostname, "ICMP")
        
    except FileNotFoundError:
        print(f"{Fore.RED}Error: ping command not found on this system")
        show_ping_exit_options()
    except Exception as e:
        print(f"{Fore.RED}Error during ping: {e}")
        show_ping_exit_options()

def enhanced_mass_ping(hostnames):
    """Enhanced mass ping with same features as single ping"""
    global stop_ping
    stop_ping = False
    
    if not hostnames:
        print(f"{Fore.RED}No hostnames provided for mass ping")
        return show_ping_exit_options()
    
    # Clear screen and show header
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════════════╗
{Fore.CYAN}║               {Fore.MAGENTA}Pengu Mass Pinger{Fore.CYAN}                ║
{Fore.CYAN}║              {Fore.YELLOW}Press Q to stop{Fore.CYAN}                   ║
{Fore.CYAN}╚════════════════════════════════════════════════╝
{Fore.GREEN}Targets: {Fore.WHITE}{', '.join(hostnames)}
{Fore.YELLOW}═══════════════════════════════════════════════════
""")
    
    # Start countdown
    countdown_timer(3)
    
    # Initialize statistics for each host
    host_stats = {hostname: PingStats() for hostname in hostnames}
    
    # Start key monitoring thread
    key_thread = threading.Thread(target=check_for_q_key, daemon=True)
    key_thread.start()
    
    # Start ping processes for each hostname
    processes = {}
    
    try:
        for hostname in hostnames:
            if os.name == 'nt':  # Windows
                cmd = ['ping', '-t', hostname]
            else:  # Linux/Unix
                cmd = ['ping', hostname]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                     text=True, bufsize=1, universal_newlines=True)
            processes[hostname] = process
        
        # Monitor all processes
        while not stop_ping and processes:
            for hostname in list(processes.keys()):
                process = processes[hostname]
                
                try:
                    line = process.stdout.readline()
                    if line and line.strip():
                        formatted_output, response_time = parse_ping_output_with_stats(line.strip(), hostname)
                        if formatted_output:
                            timestamp = time.strftime("%H:%M:%S")
                            print(f"[{Fore.CYAN}{timestamp}{Fore.WHITE}] {Fore.MAGENTA}{hostname[:15]:<15}{Fore.WHITE} {formatted_output}")
                            
                            # Update statistics
                            if response_time is not None:
                                host_stats[hostname].add_response(response_time)
                            else:
                                host_stats[hostname].add_timeout()
                    
                    # Check if process ended
                    if process.poll() is not None:
                        del processes[hostname]
                        
                except Exception as e:
                    print(f"{Fore.RED}Error reading from {hostname}: {e}")
                    if hostname in processes:
                        del processes[hostname]
            
            time.sleep(0.1)
        
        # Clean shutdown of all processes
        for hostname, process in processes.items():
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
        
        # Show statistics for all hosts
        show_mass_ping_statistics(host_stats)
        
        # Exit options
        return show_mass_ping_exit_options(host_stats)  # Pass statistics for export
        
    except Exception as e:
        print(f"{Fore.RED}Error during mass ping: {e}")
        return show_mass_ping_exit_options()

def show_mass_ping_statistics(host_stats):
    """Display mass ping statistics"""
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Mass Ping Statistics{Fore.CYAN}                  ║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝
""")
    
    for hostname, stats in host_stats.items():
        summary = stats.get_summary()
        print(f"""
{Fore.GREEN}Host: {Fore.WHITE}{hostname}
{Fore.CYAN}  Sent: {Fore.WHITE}{summary['packets_sent']} {Fore.CYAN}| Received: {Fore.WHITE}{summary['packets_received']} {Fore.CYAN}| Loss: {Fore.WHITE}{summary['packet_loss']:.1f}%
{Fore.CYAN}  Avg: {Fore.WHITE}{summary['avg_time']:.2f}ms {Fore.CYAN}| Min: {Fore.WHITE}{summary['min_time']:.2f}ms {Fore.CYAN}| Max: {Fore.WHITE}{summary['max_time']:.2f}ms {Fore.CYAN}| Timeouts: {Fore.WHITE}{summary['timeouts']}
""")

def main():
    """Main function for enhanced ping tools"""
    while True:
        try:
            print(f"""
{Fore.CYAN}╔════════════════════════════════╗
{Fore.CYAN}║      {Fore.MAGENTA}Enhanced Ping Tools{Fore.CYAN}       ║
{Fore.CYAN}╚════════════════════════════════╝

{Fore.GREEN}1. {Fore.WHITE}Single Host Ping
{Fore.GREEN}2. {Fore.WHITE}Mass Ping (Multiple Hosts)
{Fore.GREEN}3. {Fore.WHITE}Return to Main Menu
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
            
            if choice == '1':
                hostname = input(f"{Fore.YELLOW}Enter hostname/IP to ping: ").strip()
                if hostname:
                    result = enhanced_icmp_ping(hostname)
                    if result == 'home':
                        # Import and run home command
                        try:
                            import pengu
                            pengu.return_to_home()
                        except:
                            break
                    elif result == 'ping_tools':
                        continue  # Stay in ping tools menu
                else:
                    print(f"{Fore.RED}Please enter a valid hostname/IP")
                    
            elif choice == '2':
                hostnames_input = input(f"{Fore.YELLOW}Enter hostnames/IPs (comma-separated): ").strip()
                if hostnames_input:
                    hostnames = [h.strip() for h in hostnames_input.split(',') if h.strip()]
                    if hostnames:
                        result = enhanced_mass_ping(hostnames)
                        if result == 'home':
                            # Import and run home command
                            try:
                                import pengu
                                pengu.return_to_home()
                            except:
                                break
                        elif result == 'ping_tools':
                            continue  # Stay in ping tools menu
                    else:
                        print(f"{Fore.RED}Please enter valid hostnames/IPs")
                else:
                    print(f"{Fore.RED}Please enter hostnames/IPs")
                    
            elif choice == '3':
                break
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-3.")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Returning to main menu...")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")
        
        # Only show "Press Enter" if staying in ping tools
        if choice not in ['1', '2'] or choice == '3':
            input(f"\n{Fore.YELLOW}Press Enter to continue...")

if __name__ == "__main__":
    main()