#!/usr/bin/env python3
"""
Pengu Proxy Checker Module - Multi-protocol proxy validation tool
"""

import os
import sys
import time
import socket
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Thread-safe print lock
print_lock = threading.Lock()

class ProxyChecker:
    def __init__(self):
        self.working_proxies = []
        self.tested_proxies = []
        
    def print_banner(self):
        """Print the proxy checker banner"""
        print(f"""
{Fore.MAGENTA}╔════════════════════════════════════════════════╗
{Fore.MAGENTA}║             {Fore.CYAN}Pengu Proxy Checker{Fore.MAGENTA}              ║
{Fore.MAGENTA}║        {Fore.GREEN}Multi-Protocol Validation Tool{Fore.MAGENTA}       ║
{Fore.MAGENTA}╚════════════════════════════════════════════════╝
""")
    
    def parse_proxy_file(self, file_path):
        """Parse proxy file and return list of proxies"""
        proxies = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    # Support various formats:
                    # IP:PORT
                    # TYPE://IP:PORT
                    # IP:PORT:USER:PASS
                    # TYPE://USER:PASS@IP:PORT
                    
                    proxy_info = self.parse_proxy_line(line)
                    if proxy_info:
                        proxies.append(proxy_info)
                    else:
                        with print_lock:
                            print(f"{Fore.YELLOW}Warning: Skipping invalid proxy at line {line_num}: {line}")
                            
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Proxy file '{file_path}' not found.")
            return []
        except Exception as e:
            print(f"{Fore.RED}Error reading proxy file: {e}")
            return []
        
        return proxies
    
    def parse_proxy_line(self, line):
        """Parse a single proxy line and return proxy info"""
        try:
            # Handle different formats
            if '://' in line:
                # Format: type://[user:pass@]ip:port
                parts = line.split('://', 1)
                proxy_type = parts[0].lower()
                rest = parts[1]
                
                if '@' in rest:
                    auth_part, addr_part = rest.rsplit('@', 1)
                    if ':' in auth_part:
                        username, password = auth_part.split(':', 1)
                    else:
                        username, password = auth_part, ""
                else:
                    addr_part = rest
                    username, password = None, None
                
                if ':' in addr_part:
                    ip, port = addr_part.rsplit(':', 1)
                    port = int(port)
                else:
                    return None
                    
            else:
                # Format: ip:port[:user:pass]
                parts = line.split(':')
                if len(parts) >= 2:
                    ip = parts[0]
                    port = int(parts[1])
                    proxy_type = 'http'  # Default type
                    
                    if len(parts) >= 4:
                        username, password = parts[2], parts[3]
                    else:
                        username, password = None, None
                else:
                    return None
            
            return {
                'ip': ip,
                'port': port,
                'type': proxy_type,
                'username': username,
                'password': password,
                'original': line
            }
            
        except Exception:
            return None
    
    def test_proxy(self, proxy_info, test_url="http://httpbin.org/ip", timeout=10):
        """Test a single proxy"""
        try:
            start_time = time.time()
            
            # Build proxy URL
            if proxy_info['username'] and proxy_info['password']:
                proxy_url = f"{proxy_info['type']}://{proxy_info['username']}:{proxy_info['password']}@{proxy_info['ip']}:{proxy_info['port']}"
            else:
                proxy_url = f"{proxy_info['type']}://{proxy_info['ip']}:{proxy_info['port']}"
            
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test the proxy
            response = requests.get(test_url, proxies=proxies, timeout=timeout)
            end_time = time.time()
            
            if response.status_code == 200:
                connection_time = (end_time - start_time) * 1000
                
                # Try to determine anonymity level
                try:
                    response_data = response.json()
                    proxy_ip = response_data.get('origin', '')
                    
                    # Check if our real IP is hidden
                    if proxy_info['ip'] in proxy_ip:
                        anonymity = "Transparent"
                        anonymity_color = Fore.RED
                    elif ',' in proxy_ip:
                        anonymity = "Anonymous"
                        anonymity_color = Fore.YELLOW
                    else:
                        anonymity = "Elite"
                        anonymity_color = Fore.GREEN
                except:
                    anonymity = "Unknown"
                    anonymity_color = Fore.WHITE
                
                result = {
                    'proxy': proxy_info,
                    'status': 'working',
                    'connection_time': connection_time,
                    'anonymity': anonymity,
                    'anonymity_color': anonymity_color,
                    'response_ip': proxy_ip if 'proxy_ip' in locals() else 'N/A'
                }
                
                with print_lock:
                    print(f"{Fore.GREEN}[✓] {proxy_info['ip']}:{proxy_info['port']} ({proxy_info['type'].upper()}) - "
                          f"{connection_time:.0f}ms - {anonymity_color}{anonymity}")
                
                return result
            else:
                result = {
                    'proxy': proxy_info,
                    'status': 'failed',
                    'error': f"HTTP {response.status_code}",
                    'connection_time': None,
                    'anonymity': None
                }
                return result
                
        except requests.exceptions.ConnectTimeout:
            return {
                'proxy': proxy_info,
                'status': 'failed',
                'error': 'Connection timeout',
                'connection_time': None,
                'anonymity': None
            }
        except requests.exceptions.ProxyError:
            return {
                'proxy': proxy_info,
                'status': 'failed',
                'error': 'Proxy error',
                'connection_time': None,
                'anonymity': None
            }
        except Exception as e:
            return {
                'proxy': proxy_info,
                'status': 'failed',
                'error': str(e),
                'connection_time': None,
                'anonymity': None
            }
    
    def check_proxies(self, proxies, max_workers=50):
        """Check multiple proxies concurrently"""
        print(f"{Fore.CYAN}Testing {len(proxies)} proxies with {max_workers} threads...")
        print(f"{Fore.YELLOW}Real-time results:")
        print(f"{Fore.CYAN}{'='*80}")
        
        working_count = 0
        failed_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all proxy tests
            future_to_proxy = {
                executor.submit(self.test_proxy, proxy): proxy 
                for proxy in proxies
            }
            
            # Process results as they complete
            for future in as_completed(future_to_proxy):
                result = future.result()
                self.tested_proxies.append(result)
                
                if result['status'] == 'working':
                    self.working_proxies.append(result)
                    working_count += 1
                else:
                    failed_count += 1
                
                # Show progress
                total_tested = working_count + failed_count
                progress = (total_tested / len(proxies)) * 100
                
                with print_lock:
                    if result['status'] != 'working':  # Only show failed in quiet mode
                        if failed_count % 10 == 0:  # Show every 10th failure
                            print(f"{Fore.RED}[✗] Failed: {failed_count}, Working: {working_count} "
                                  f"({progress:.1f}% complete)")
        
        return self.working_proxies
    
    def save_working_proxies(self, filename, proxy_type_filter=None, anonymity_filter=None):
        """Save working proxies to file with optional filters"""
        try:
            filtered_proxies = self.working_proxies
            
            # Apply filters
            if proxy_type_filter:
                filtered_proxies = [p for p in filtered_proxies 
                                  if p['proxy']['type'].lower() == proxy_type_filter.lower()]
            
            if anonymity_filter:
                filtered_proxies = [p for p in filtered_proxies 
                                  if p['anonymity'] and p['anonymity'].lower() == anonymity_filter.lower()]
            
            with open(filename, 'w') as f:
                f.write(f"# Working Proxies - Generated by Pengu Proxy Checker\n")
                f.write(f"# Total: {len(filtered_proxies)} proxies\n")
                f.write(f"# Filters: Type={proxy_type_filter or 'All'}, Anonymity={anonymity_filter or 'All'}\n\n")
                
                for result in filtered_proxies:
                    proxy = result['proxy']
                    f.write(f"{proxy['original']} # {result['connection_time']:.0f}ms - {result['anonymity']}\n")
            
            print(f"{Fore.GREEN}Saved {len(filtered_proxies)} working proxies to {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}Error saving proxies: {e}")
    
    def generate_detailed_report(self, filename):
        """Generate detailed report of all tested proxies"""
        try:
            with open(filename, 'w') as f:
                f.write("# Pengu Proxy Checker - Detailed Report\n")
                f.write(f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"# Total Tested: {len(self.tested_proxies)}\n")
                f.write(f"# Working: {len(self.working_proxies)}\n")
                f.write(f"# Failed: {len(self.tested_proxies) - len(self.working_proxies)}\n\n")
                
                # Working proxies section
                f.write("=== WORKING PROXIES ===\n")
                for result in self.working_proxies:
                    proxy = result['proxy']
                    f.write(f"IP: {proxy['ip']}:{proxy['port']}\n")
                    f.write(f"Type: {proxy['type'].upper()}\n")
                    f.write(f"Connection Time: {result['connection_time']:.0f}ms\n")
                    f.write(f"Anonymity: {result['anonymity']}\n")
                    f.write(f"Response IP: {result.get('response_ip', 'N/A')}\n")
                    f.write(f"Original Line: {proxy['original']}\n")
                    f.write("-" * 40 + "\n")
                
                # Failed proxies section
                f.write("\n=== FAILED PROXIES ===\n")
                failed_proxies = [p for p in self.tested_proxies if p['status'] == 'failed']
                for result in failed_proxies:
                    proxy = result['proxy']
                    f.write(f"IP: {proxy['ip']}:{proxy['port']}\n")
                    f.write(f"Type: {proxy['type'].upper()}\n")
                    f.write(f"Error: {result['error']}\n")
                    f.write(f"Original Line: {proxy['original']}\n")
                    f.write("-" * 40 + "\n")
            
            print(f"{Fore.GREEN}Detailed report saved to {filename}")
            
        except Exception as e:
            print(f"{Fore.RED}Error generating report: {e}")
    
    def show_summary(self):
        """Show summary of proxy check results"""
        total = len(self.tested_proxies)
        working = len(self.working_proxies)
        failed = total - working
        
        print(f"""
{Fore.GREEN}╔══════════════════════════════════════════════════╗
{Fore.GREEN}║                 {Fore.CYAN}PROXY CHECK SUMMARY{Fore.GREEN}                ║
{Fore.GREEN}╚══════════════════════════════════════════════════╝

{Fore.CYAN}Total Tested:    {Fore.WHITE}{total}
{Fore.GREEN}Working:         {Fore.WHITE}{working} ({(working/total*100 if total > 0 else 0):.1f}%)
{Fore.RED}Failed:          {Fore.WHITE}{failed} ({(failed/total*100 if total > 0 else 0):.1f}%)

{Fore.YELLOW}╔══════════════════════════════════════════════════╗
{Fore.YELLOW}║               {Fore.CYAN}WORKING PROXIES BY TYPE{Fore.YELLOW}            ║
{Fore.YELLOW}╚══════════════════════════════════════════════════╝
""")
        
        # Count by type
        type_counts = {}
        for result in self.working_proxies:
            proxy_type = result['proxy']['type'].upper()
            type_counts[proxy_type] = type_counts.get(proxy_type, 0) + 1
        
        for proxy_type, count in type_counts.items():
            print(f"{Fore.CYAN}{proxy_type}:            {Fore.WHITE}{count}")
        
        # Count by anonymity
        print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════╗
{Fore.YELLOW}║            {Fore.CYAN}WORKING PROXIES BY ANONYMITY{Fore.YELLOW}         ║
{Fore.YELLOW}╚══════════════════════════════════════════════════╝
""")
        
        anonymity_counts = {}
        for result in self.working_proxies:
            anonymity = result.get('anonymity', 'Unknown')
            anonymity_counts[anonymity] = anonymity_counts.get(anonymity, 0) + 1
        
        for anonymity, count in anonymity_counts.items():
            print(f"{Fore.CYAN}{anonymity}:         {Fore.WHITE}{count}")

def main():
    """Main proxy checker function"""
    checker = ProxyChecker()
    checker.print_banner()
    
    while True:
        try:
            # Get proxy file path
            default_file = "proxies.txt"
            file_path = input(f"{Fore.YELLOW}Enter proxy file path (default: {default_file}): ").strip()
            if not file_path:
                file_path = default_file
            
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"{Fore.RED}File '{file_path}' not found.")
                continue
            
            # Parse proxies
            print(f"{Fore.CYAN}Loading proxies from {file_path}...")
            proxies = checker.parse_proxy_file(file_path)
            
            if not proxies:
                print(f"{Fore.RED}No valid proxies found in file.")
                continue
            
            print(f"{Fore.GREEN}Loaded {len(proxies)} proxies.")
            
            # Get thread count
            try:
                thread_input = input(f"{Fore.CYAN}Enter number of threads (default: 50): ").strip()
                if thread_input:
                    max_workers = int(thread_input)
                else:
                    max_workers = 50
            except ValueError:
                max_workers = 50
                print(f"{Fore.YELLOW}Using default: 50 threads")
            
            # Check proxies
            working_proxies = checker.check_proxies(proxies, max_workers)
            
            # Show summary
            checker.show_summary()
            
            # Ask user what to do with results
            while True:
                print(f"""
{Fore.CYAN}What would you like to do with the results?
{Fore.GREEN}1. {Fore.WHITE}Save working proxies to file
{Fore.GREEN}2. {Fore.WHITE}Save filtered proxies (by type/anonymity)
{Fore.GREEN}3. {Fore.WHITE}Generate detailed report
{Fore.GREEN}4. {Fore.WHITE}Check more proxies
{Fore.GREEN}5. {Fore.WHITE}Return to main menu
""")
                
                choice = input(f"{Fore.YELLOW}Select option (1-5): ").strip()
                
                if choice == '1':
                    filename = input(f"{Fore.CYAN}Enter filename (default: working_proxies.txt): ").strip()
                    if not filename:
                        filename = "working_proxies.txt"
                    checker.save_working_proxies(filename)
                    
                elif choice == '2':
                    filename = input(f"{Fore.CYAN}Enter filename (default: filtered_proxies.txt): ").strip()
                    if not filename:
                        filename = "filtered_proxies.txt"
                    
                    type_filter = input(f"{Fore.CYAN}Filter by type (http/https/socks4/socks5, or Enter for all): ").strip()
                    if not type_filter:
                        type_filter = None
                    
                    anonymity_filter = input(f"{Fore.CYAN}Filter by anonymity (elite/anonymous/transparent, or Enter for all): ").strip()
                    if not anonymity_filter:
                        anonymity_filter = None
                    
                    checker.save_working_proxies(filename, type_filter, anonymity_filter)
                    
                elif choice == '3':
                    filename = input(f"{Fore.CYAN}Enter filename (default: proxy_report.txt): ").strip()
                    if not filename:
                        filename = "proxy_report.txt"
                    checker.generate_detailed_report(filename)
                    
                elif choice == '4':
                    break  # Go back to main loop
                    
                elif choice == '5':
                    return
                    
                else:
                    print(f"{Fore.RED}Invalid option. Please select 1-5.")
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Proxy checking interrupted.")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    main()