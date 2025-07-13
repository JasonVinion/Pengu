#!/usr/bin/env python3
"""
Pengu Universal Proxy Management System
Advanced proxy handling for all compatible tools
"""

import os
import time
import random
import threading
from urllib.parse import urlparse
from colorama import init, Fore, Style

init(autoreset=True)

class ProxyManager:
    """Universal proxy manager for Pengu tools"""
    
    def __init__(self):
        self.working_proxies = []
        self.failed_proxies = []
        self.proxy_index = 0
        self.lock = threading.Lock()
        self.timeout = 10  # Default timeout
        self.proxy_type = None
        
    def load_proxies_from_file(self, file_path):
        """Load proxies from file"""
        try:
            with open(file_path, 'r') as f:
                proxies = []
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        proxies.append(self.parse_proxy(line))
                return [p for p in proxies if p]  # Filter out None values
        except Exception as e:
            print(f"{Fore.RED}Error loading proxy file: {e}")
            return []
    
    def parse_proxy(self, proxy_string):
        """Parse different proxy formats"""
        proxy_string = proxy_string.strip()
        
        try:
            # Format: protocol://username:password@host:port
            if '://' in proxy_string:
                parsed = urlparse(proxy_string)
                return {
                    'protocol': parsed.scheme.lower(),
                    'host': parsed.hostname,
                    'port': parsed.port,
                    'username': parsed.username,
                    'password': parsed.password,
                    'raw': proxy_string
                }
            
            # Format: host:port:username:password
            elif proxy_string.count(':') == 3:
                parts = proxy_string.split(':')
                return {
                    'protocol': self.proxy_type or 'http',
                    'host': parts[0],
                    'port': int(parts[1]),
                    'username': parts[2],
                    'password': parts[3],
                    'raw': proxy_string
                }
            
            # Format: host:port
            elif proxy_string.count(':') == 1:
                host, port = proxy_string.split(':')
                return {
                    'protocol': self.proxy_type or 'http',
                    'host': host,
                    'port': int(port),
                    'username': None,
                    'password': None,
                    'raw': proxy_string
                }
            
            else:
                print(f"{Fore.YELLOW}Warning: Invalid proxy format: {proxy_string}")
                return None
                
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not parse proxy {proxy_string}: {e}")
            return None
    
    def validate_proxy(self, proxy):
        """Validate a proxy by testing connection"""
        try:
            import requests
            
            # Build proxy dict for requests
            auth = None
            if proxy['username'] and proxy['password']:
                auth = (proxy['username'], proxy['password'])
            
            proxy_url = f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # Test with a simple request
            response = requests.get(
                'http://httpbin.org/ip',
                proxies=proxies,
                auth=auth,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def get_next_proxy(self):
        """Get next working proxy with round-robin"""
        with self.lock:
            if not self.working_proxies:
                return None
            
            proxy = self.working_proxies[self.proxy_index]
            self.proxy_index = (self.proxy_index + 1) % len(self.working_proxies)
            return proxy
    
    def mark_proxy_failed(self, proxy):
        """Mark a proxy as failed and move to failed list"""
        with self.lock:
            if proxy in self.working_proxies:
                self.working_proxies.remove(proxy)
                self.failed_proxies.append(proxy)
                print(f"{Fore.YELLOW}Proxy marked as failed: {proxy['host']}:{proxy['port']}")
    
    def setup_proxy_session(self):
        """Interactive proxy setup"""
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Universal Proxy Setup{Fore.CYAN}                    ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝

{Fore.YELLOW}⚠ Recommendation: Run 'proxy' command first to validate proxies!

{Fore.GREEN}Proxy Input Options:
{Fore.GREEN}1. {Fore.WHITE}Load from file
{Fore.GREEN}2. {Fore.WHITE}Enter proxies manually (comma-separated)
{Fore.GREEN}3. {Fore.WHITE}Single proxy
{Fore.GREEN}4. {Fore.WHITE}Skip proxy setup
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-4): ").strip()
        
        if choice == '1':
            return self._setup_from_file()
        elif choice == '2':
            return self._setup_manual_list()
        elif choice == '3':
            return self._setup_single_proxy()
        elif choice == '4':
            return False
        else:
            print(f"{Fore.RED}Invalid option")
            return False
    
    def _setup_from_file(self):
        """Setup proxies from file"""
        file_path = input(f"{Fore.YELLOW}Enter proxy file path: ").strip()
        
        if not os.path.exists(file_path):
            print(f"{Fore.RED}File not found: {file_path}")
            return False
        
        # Get proxy type
        print(f"""
{Fore.YELLOW}Proxy type (if not specified in file):
{Fore.GREEN}1. {Fore.WHITE}HTTP
{Fore.GREEN}2. {Fore.WHITE}HTTPS
{Fore.GREEN}3. {Fore.WHITE}SOCKS4
{Fore.GREEN}4. {Fore.WHITE}SOCKS5
""")
        
        type_choice = input(f"{Fore.YELLOW}Select type (1-4, default 1): ").strip()
        type_map = {'1': 'http', '2': 'https', '3': 'socks4', '4': 'socks5'}
        self.proxy_type = type_map.get(type_choice, 'http')
        
        # Load proxies
        all_proxies = self.load_proxies_from_file(file_path)
        if not all_proxies:
            print(f"{Fore.RED}No valid proxies found in file")
            return False
        
        print(f"{Fore.GREEN}Loaded {len(all_proxies)} proxies from file")
        
        # Ask about validation
        validate_choice = input(f"{Fore.YELLOW}Validate proxies before use? (Y/n): ").strip().lower()
        
        if validate_choice not in ['n', 'no']:
            print(f"{Fore.CYAN}Validating proxies (this may take a while)...")
            self._validate_proxy_list(all_proxies)
        else:
            self.working_proxies = all_proxies
        
        if self.working_proxies:
            print(f"{Fore.GREEN}✓ {len(self.working_proxies)} working proxies loaded")
            return True
        else:
            print(f"{Fore.RED}No working proxies found")
            return False
    
    def _setup_manual_list(self):
        """Setup proxies from manual input"""
        proxy_input = input(f"{Fore.YELLOW}Enter proxies (comma-separated): ").strip()
        
        # Get proxy type
        print(f"""
{Fore.YELLOW}Proxy type:
{Fore.GREEN}1. {Fore.WHITE}HTTP
{Fore.GREEN}2. {Fore.WHITE}HTTPS
{Fore.GREEN}3. {Fore.WHITE}SOCKS4
{Fore.GREEN}4. {Fore.WHITE}SOCKS5
""")
        
        type_choice = input(f"{Fore.YELLOW}Select type (1-4, default 1): ").strip()
        type_map = {'1': 'http', '2': 'https', '3': 'socks4', '4': 'socks5'}
        self.proxy_type = type_map.get(type_choice, 'http')
        
        # Parse proxies
        proxy_strings = [p.strip() for p in proxy_input.split(',')]
        all_proxies = [self.parse_proxy(p) for p in proxy_strings]
        all_proxies = [p for p in all_proxies if p]  # Filter None values
        
        if not all_proxies:
            print(f"{Fore.RED}No valid proxies found")
            return False
        
        # Ask about validation
        validate_choice = input(f"{Fore.YELLOW}Validate proxies before use? (Y/n): ").strip().lower()
        
        if validate_choice not in ['n', 'no']:
            print(f"{Fore.CYAN}Validating proxies...")
            self._validate_proxy_list(all_proxies)
        else:
            self.working_proxies = all_proxies
        
        if self.working_proxies:
            print(f"{Fore.GREEN}✓ {len(self.working_proxies)} working proxies loaded")
            return True
        else:
            print(f"{Fore.RED}No working proxies found")
            return False
    
    def _setup_single_proxy(self):
        """Setup single proxy"""
        proxy_input = input(f"{Fore.YELLOW}Enter proxy (host:port or full URL): ").strip()
        
        # Get proxy type if needed
        if '://' not in proxy_input:
            print(f"""
{Fore.YELLOW}Proxy type:
{Fore.GREEN}1. {Fore.WHITE}HTTP
{Fore.GREEN}2. {Fore.WHITE}HTTPS
{Fore.GREEN}3. {Fore.WHITE}SOCKS4
{Fore.GREEN}4. {Fore.WHITE}SOCKS5
""")
            
            type_choice = input(f"{Fore.YELLOW}Select type (1-4, default 1): ").strip()
            type_map = {'1': 'http', '2': 'https', '3': 'socks4', '4': 'socks5'}
            self.proxy_type = type_map.get(type_choice, 'http')
        
        proxy = self.parse_proxy(proxy_input)
        if not proxy:
            print(f"{Fore.RED}Invalid proxy format")
            return False
        
        # Ask about validation
        validate_choice = input(f"{Fore.YELLOW}Validate proxy before use? (Y/n): ").strip().lower()
        
        if validate_choice not in ['n', 'no']:
            print(f"{Fore.CYAN}Validating proxy...")
            if self.validate_proxy(proxy):
                self.working_proxies = [proxy]
                print(f"{Fore.GREEN}✓ Proxy is working")
                return True
            else:
                print(f"{Fore.RED}Proxy validation failed")
                return False
        else:
            self.working_proxies = [proxy]
            print(f"{Fore.GREEN}✓ Proxy loaded (not validated)")
            return True
    
    def _validate_proxy_list(self, proxy_list):
        """Validate a list of proxies"""
        print(f"{Fore.CYAN}Testing {len(proxy_list)} proxies...")
        
        for i, proxy in enumerate(proxy_list, 1):
            print(f"{Fore.YELLOW}Testing proxy {i}/{len(proxy_list)}: {proxy['host']}:{proxy['port']}")
            
            if self.validate_proxy(proxy):
                self.working_proxies.append(proxy)
                print(f"{Fore.GREEN}✓ Working")
            else:
                self.failed_proxies.append(proxy)
                print(f"{Fore.RED}✗ Failed")
    
    def get_proxy_for_requests(self, proxy=None):
        """Get proxy configuration for requests library"""
        if not proxy:
            proxy = self.get_next_proxy()
        
        if not proxy:
            return None
        
        # Build proxy URL
        if proxy['username'] and proxy['password']:
            proxy_url = f"{proxy['protocol']}://{proxy['username']}:{proxy['password']}@{proxy['host']}:{proxy['port']}"
        else:
            proxy_url = f"{proxy['protocol']}://{proxy['host']}:{proxy['port']}"
        
        return {
            'http': proxy_url,
            'https': proxy_url
        }
    
    def get_proxy_stats(self):
        """Get current proxy statistics"""
        return {
            'working': len(self.working_proxies),
            'failed': len(self.failed_proxies),
            'total': len(self.working_proxies) + len(self.failed_proxies)
        }
    
    def show_proxy_status(self):
        """Display current proxy status"""
        stats = self.get_proxy_stats()
        
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════╗
{Fore.CYAN}║                   {Fore.MAGENTA}Proxy Status{Fore.CYAN}                         ║
{Fore.CYAN}╚══════════════════════════════════════════════════════════╝

{Fore.GREEN}Working Proxies: {Fore.WHITE}{stats['working']}
{Fore.RED}Failed Proxies:  {Fore.WHITE}{stats['failed']}
{Fore.CYAN}Total Loaded:    {Fore.WHITE}{stats['total']}
{Fore.YELLOW}Current Index:   {Fore.WHITE}{self.proxy_index}
""")
        
        if self.working_proxies:
            print(f"{Fore.GREEN}Working Proxies List:")
            for i, proxy in enumerate(self.working_proxies[:5], 1):  # Show first 5
                status = "→ CURRENT" if i-1 == self.proxy_index else ""
                print(f"{Fore.CYAN}  {i}. {proxy['host']}:{proxy['port']} {Fore.YELLOW}{status}")
            
            if len(self.working_proxies) > 5:
                print(f"{Fore.YELLOW}  ... and {len(self.working_proxies) - 5} more")

# Global proxy manager instance
proxy_manager = None

def get_proxy_manager():
    """Get or create global proxy manager"""
    global proxy_manager
    if proxy_manager is None:
        proxy_manager = ProxyManager()
    return proxy_manager

def setup_proxy_mode():
    """Setup proxy mode for tools"""
    manager = get_proxy_manager()
    return manager.setup_proxy_session()

def get_next_proxy():
    """Get next available proxy"""
    manager = get_proxy_manager()
    return manager.get_next_proxy()

def mark_proxy_failed(proxy):
    """Mark a proxy as failed"""
    manager = get_proxy_manager()
    manager.mark_proxy_failed(proxy)

def get_proxy_for_requests(proxy=None):
    """Get proxy configuration for requests"""
    manager = get_proxy_manager()
    return manager.get_proxy_for_requests(proxy)

def show_proxy_status():
    """Show current proxy status"""
    manager = get_proxy_manager()
    manager.show_proxy_status()

def main():
    """Test function for proxy manager"""
    manager = ProxyManager()
    
    print(f"{Fore.GREEN}Testing Proxy Manager...")
    
    # Test setup
    if manager.setup_proxy_session():
        manager.show_proxy_status()
        
        # Test getting proxies
        for i in range(3):
            proxy = manager.get_next_proxy()
            if proxy:
                print(f"{Fore.CYAN}Got proxy: {proxy['host']}:{proxy['port']}")
            else:
                print(f"{Fore.RED}No proxy available")
    else:
        print(f"{Fore.YELLOW}Proxy setup skipped or failed")

if __name__ == "__main__":
    main()