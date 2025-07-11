#!/usr/bin/env python3
"""
DNS Enumeration Tool - Demo Implementation
A demonstration of enhanced DNS enumeration capabilities for Pengu Network Tools
"""

import dns.resolver
import socket
import sys
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import itertools

# Initialize colorama
init(autoreset=True)

class DNSEnumerator:
    def __init__(self):
        self.record_types = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'SOA', 'CNAME', 'PTR']
        self.common_subdomains = [
            'www', 'mail', 'webmail', 'ftp', 'localhost', 'webdisk', 'ns1', 'ns2',
            'cpanel', 'whm', 'autodiscover', 'autoconfig', 'mx', 'test', 'mx1', 'mx2',
            'ns', 'secure', 'vpn', 'admin', 'server', 'smtp', 'pop', 'imap', 'blog',
            'dev', 'staging', 'api', 'cdn', 'shop', 'store', 'mobile', 'app'
        ]
    
    def print_banner(self):
        banner = f"""
{Fore.CYAN} ╔════════════════════════════════════════╗
{Fore.CYAN} ║ {Fore.YELLOW}Pengu DNS Enumeration Tool (Demo){Fore.CYAN}     ║
{Fore.CYAN} ║ {Fore.GREEN}Enhanced DNS Discovery & Analysis{Fore.CYAN}      ║
{Fore.CYAN} ╚════════════════════════════════════════╝
        """
        print(banner)
    
    def enumerate_dns_records(self, domain):
        """Enumerate all DNS record types for a domain"""
        print(f"\n{Fore.YELLOW}[+] Enumerating DNS records for: {domain}")
        print(f"{Fore.CYAN}{'='*50}")
        
        results = {}
        for record_type in self.record_types:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                record_list = []
                for answer in answers:
                    record_list.append(str(answer))
                
                if record_list:
                    results[record_type] = record_list
                    print(f"{Fore.GREEN}[{record_type}] Records found:")
                    for record in record_list:
                        print(f"  {Fore.WHITE}→ {record}")
                
            except dns.resolver.NXDOMAIN:
                print(f"{Fore.RED}[{record_type}] Domain not found")
            except dns.resolver.NoAnswer:
                print(f"{Fore.YELLOW}[{record_type}] No records found")
            except Exception as e:
                print(f"{Fore.RED}[{record_type}] Error: {str(e)}")
        
        return results
    
    def check_subdomain(self, subdomain):
        """Check if a subdomain exists"""
        try:
            answers = dns.resolver.resolve(subdomain, 'A')
            ips = [str(answer) for answer in answers]
            return subdomain, ips
        except:
            return None, None
    
    def discover_subdomains(self, domain, use_wordlist=True, max_workers=50):
        """Discover subdomains using various techniques"""
        print(f"\n{Fore.YELLOW}[+] Discovering subdomains for: {domain}")
        print(f"{Fore.CYAN}{'='*50}")
        
        found_subdomains = []
        test_subdomains = []
        
        if use_wordlist:
            # Use common subdomain wordlist
            test_subdomains.extend([f"{sub}.{domain}" for sub in self.common_subdomains])
        
        # Add some common patterns
        patterns = ['mail', 'www', 'ftp', 'admin', 'test', 'dev', 'api']
        for pattern in patterns:
            test_subdomains.append(f"{pattern}.{domain}")
        
        # Remove duplicates
        test_subdomains = list(set(test_subdomains))
        
        print(f"{Fore.CYAN}[*] Testing {len(test_subdomains)} potential subdomains...")
        
        # Use threading for faster discovery
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_subdomain = {
                executor.submit(self.check_subdomain, subdomain): subdomain 
                for subdomain in test_subdomains
            }
            
            for future in as_completed(future_to_subdomain):
                subdomain, ips = future.result()
                if subdomain and ips:
                    found_subdomains.append((subdomain, ips))
                    print(f"{Fore.GREEN}[✓] Found: {subdomain} → {', '.join(ips)}")
        
        return found_subdomains
    
    def reverse_dns_lookup(self, ip):
        """Perform reverse DNS lookup for an IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return None
    
    def analyze_mx_records(self, domain):
        """Analyze MX records for email security"""
        print(f"\n{Fore.YELLOW}[+] Analyzing MX records for: {domain}")
        print(f"{Fore.CYAN}{'='*50}")
        
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            for mx in mx_records:
                mx_host = str(mx).split()[-1].rstrip('.')
                print(f"{Fore.GREEN}[MX] Priority: {mx.preference}, Host: {mx_host}")
                
                # Try to get IP for MX record
                try:
                    mx_ips = dns.resolver.resolve(mx_host, 'A')
                    for ip in mx_ips:
                        reverse_name = self.reverse_dns_lookup(str(ip))
                        if reverse_name:
                            print(f"  {Fore.WHITE}→ IP: {ip} (Reverse: {reverse_name})")
                        else:
                            print(f"  {Fore.WHITE}→ IP: {ip}")
                except:
                    print(f"  {Fore.RED}→ Could not resolve IP for {mx_host}")
        
        except Exception as e:
            print(f"{Fore.RED}[!] Error analyzing MX records: {str(e)}")
    
    def check_dns_security(self, domain):
        """Check for DNS security features"""
        print(f"\n{Fore.YELLOW}[+] Checking DNS security features for: {domain}")
        print(f"{Fore.CYAN}{'='*50}")
        
        security_checks = {
            'SPF': '_spf',
            'DMARC': '_dmarc',
            'DKIM': 'default._domainkey'
        }
        
        for check_name, prefix in security_checks.items():
            test_domain = f"{prefix}.{domain}"
            try:
                txt_records = dns.resolver.resolve(test_domain, 'TXT')
                for record in txt_records:
                    print(f"{Fore.GREEN}[{check_name}] Found: {record}")
            except:
                print(f"{Fore.RED}[{check_name}] Not configured")
    
    def comprehensive_scan(self, domain):
        """Perform comprehensive DNS enumeration"""
        self.print_banner()
        
        print(f"{Fore.MAGENTA}Starting comprehensive DNS enumeration for: {domain}")
        
        # Basic DNS record enumeration
        dns_records = self.enumerate_dns_records(domain)
        
        # Subdomain discovery
        subdomains = self.discover_subdomains(domain)
        
        # MX record analysis
        self.analyze_mx_records(domain)
        
        # DNS security checks
        self.check_dns_security(domain)
        
        # Summary
        print(f"\n{Fore.YELLOW}[+] Scan Summary:")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.GREEN}[*] DNS record types found: {len(dns_records)}")
        print(f"{Fore.GREEN}[*] Subdomains discovered: {len(subdomains)}")
        
        return {
            'dns_records': dns_records,
            'subdomains': subdomains
        }

def main():
    """Main function for the DNS enumeration demo"""
    enumerator = DNSEnumerator()
    
    while True:
        enumerator.print_banner()
        
        print(f"{Fore.GREEN}DNS Enumeration Options:")
        print(f"{Fore.CYAN}1. {Fore.WHITE}Comprehensive scan")
        print(f"{Fore.CYAN}2. {Fore.WHITE}DNS records only")
        print(f"{Fore.CYAN}3. {Fore.WHITE}Subdomain discovery only")
        print(f"{Fore.CYAN}4. {Fore.WHITE}MX record analysis")
        print(f"{Fore.CYAN}5. {Fore.WHITE}DNS security check")
        print(f"{Fore.CYAN}6. {Fore.WHITE}Exit")
        
        choice = input(f"\n{Fore.GREEN}Select option [1-6]: {Fore.WHITE}").strip()
        
        if choice == '6':
            print(f"{Fore.GREEN}Exiting DNS Enumerator...")
            break
        
        if choice in ['1', '2', '3', '4', '5']:
            domain = input(f"{Fore.GREEN}Enter domain name: {Fore.WHITE}").strip()
            
            if not domain:
                print(f"{Fore.RED}[!] Please enter a valid domain name")
                continue
            
            try:
                if choice == '1':
                    enumerator.comprehensive_scan(domain)
                elif choice == '2':
                    enumerator.enumerate_dns_records(domain)
                elif choice == '3':
                    enumerator.discover_subdomains(domain)
                elif choice == '4':
                    enumerator.analyze_mx_records(domain)
                elif choice == '5':
                    enumerator.check_dns_security(domain)
                
                input(f"\n{Fore.YELLOW}Press Enter to continue...")
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}[!] Operation cancelled by user")
            except Exception as e:
                print(f"{Fore.RED}[!] Error: {str(e)}")
        else:
            print(f"{Fore.RED}[!] Invalid option selected")

if __name__ == "__main__":
    main()