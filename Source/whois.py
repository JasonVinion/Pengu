#!/usr/bin/env python3
"""
Pengu WHOIS & GeoIP Lookup Module - Optimized Information Gathering
"""

import socket
import re
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the whois/IP lookup banner"""
    message = f"""
{Fore.GREEN} ╔════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Project Pengu IP Lookup{Fore.GREEN}    ╚════╗
{Fore.GREEN} ║ {Fore.CYAN}Enhanced Multi-Source Data{Fore.GREEN}       ║
{Fore.GREEN} ╚═════════════════════════════════╝
"""
    print(message)

def validate_ip(ip):
    """Validate if the input is a valid IP address"""
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def resolve_hostname(hostname):
    """Resolve hostname to IP address"""
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def get_geoip_info(ip):
    """Get GeoIP information with error handling and multiple sources"""
    try:
        import requests
        
        # Primary source: ipinfo.io
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    return data, "ipinfo.io"
        except:
            pass
        
        # Fallback source: ipapi.co
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    # Convert to ipinfo.io format for consistency
                    converted = {
                        'ip': data.get('ip'),
                        'hostname': data.get('hostname'),
                        'city': data.get('city'),
                        'region': data.get('region'),
                        'country': data.get('country_name'),
                        'loc': f"{data.get('latitude', '')},{data.get('longitude', '')}",
                        'org': data.get('org'),
                        'postal': data.get('postal'),
                        'timezone': data.get('timezone')
                    }
                    return converted, "ipapi.co"
        except:
            pass
            
        # Fallback source: ip-api.com
        try:
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    # Convert to ipinfo.io format for consistency
                    converted = {
                        'ip': data.get('query'),
                        'city': data.get('city'),
                        'region': data.get('regionName'),
                        'country': data.get('country'),
                        'loc': f"{data.get('lat', '')},{data.get('lon', '')}",
                        'org': data.get('isp'),
                        'postal': data.get('zip'),
                        'timezone': data.get('timezone')
                    }
                    return converted, "ip-api.com"
        except:
            pass
            
        return None, "No service available"
        
    except ImportError:
        return None, "Requests module not available"
    except Exception as e:
        return None, f"Error: {str(e)}"

def get_basic_whois_info(ip):
    """Get basic WHOIS information using simple socket connection"""
    try:
        import requests
        
        # Try ARIN REST API
        try:
            response = requests.get(f"https://whois.arin.net/rest/ip/{ip}.json", timeout=10)
            if response.status_code == 200:
                return response.json(), "ARIN"
        except:
            pass
            
        # Try alternative WHOIS service
        try:
            response = requests.get(f"https://ipwhois.app/json/{ip}", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data, "ipwhois.app"
        except:
            pass
            
        return None, "No WHOIS service available"
        
    except ImportError:
        return None, "Requests module not available"
    except Exception as e:
        return None, f"Error: {str(e)}"

def display_geoip_results(data, source):
    """Display GeoIP results in a formatted way"""
    print(f"{Fore.GREEN}╔══════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}GeoIP Information (Source: {source}){Fore.GREEN}")
    print(f"{Fore.GREEN}╚══════════════════════════════════════╝")
    
    fields = [
        ('IP Address', data.get('ip', 'N/A')),
        ('Hostname', data.get('hostname', 'N/A')),
        ('City', data.get('city', 'N/A')),
        ('Region/State', data.get('region', 'N/A')),
        ('Country', data.get('country', 'N/A')),
        ('Location', data.get('loc', 'N/A')),
        ('ISP/Organization', data.get('org', 'N/A')),
        ('Postal Code', data.get('postal', 'N/A')),
        ('Timezone', data.get('timezone', 'N/A'))
    ]
    
    for label, value in fields:
        if value and value != 'N/A':
            print(f"{Fore.CYAN}{label:15}: {Fore.WHITE}{value}")

def display_whois_results(data, source):
    """Display WHOIS results in a formatted way"""
    print(f"\n{Fore.GREEN}╔══════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}WHOIS Information (Source: {source}){Fore.GREEN}")
    print(f"{Fore.GREEN}╚══════════════════════════════════════╝")
    
    if source == "ARIN":
        # Handle ARIN format
        whois_net = data.get('net', {})
        fields = [
            ('Network Name', whois_net.get('name', {}).get('$', 'N/A')),
            ('Handle', whois_net.get('handle', {}).get('$', 'N/A')),
            ('Start Address', whois_net.get('startAddress', {}).get('$', 'N/A')),
            ('End Address', whois_net.get('endAddress', {}).get('$', 'N/A')),
            ('CIDR', whois_net.get('cidr', 'N/A')),
            ('Parent Network', whois_net.get('parentNetRef', {}).get('@name', 'N/A')),
            ('Organization', whois_net.get('orgRef', {}).get('@name', 'N/A')),
            ('Registration Date', whois_net.get('registrationDate', 'N/A')),
            ('Last Updated', whois_net.get('updateDate', {}).get('$', 'N/A'))
        ]
    else:
        # Handle ipwhois.app format
        fields = [
            ('Network', data.get('net', 'N/A')),
            ('CIDR', data.get('cidr', 'N/A')),
            ('Organization', data.get('org', 'N/A')),
            ('ISP', data.get('isp', 'N/A')),
            ('Country', data.get('country', 'N/A')),
            ('Region', data.get('region', 'N/A')),
            ('ASN', f"{data.get('asn', 'N/A')} - {data.get('asn_org', 'N/A')}")
        ]
    
    for label, value in fields:
        if value and value != 'N/A':
            print(f"{Fore.CYAN}{label:15}: {Fore.WHITE}{value}")

def main():
    """Main function with enhanced input handling"""
    print_banner()
    while True:
        try:
            target = input(f"{Fore.YELLOW}Enter IP address or hostname (or 'exit' to quit): ").strip()
            
            if target.lower() == 'exit':
                break
                
            if not target:
                print(f"{Fore.RED}Please enter a valid IP address or hostname")
                continue
            
            # Determine if input is IP or hostname
            if validate_ip(target):
                ip_address = target
                print(f"{Fore.CYAN}Analyzing IP: {ip_address}")
            else:
                print(f"{Fore.CYAN}Resolving hostname: {target}")
                ip_address = resolve_hostname(target)
                if not ip_address:
                    print(f"{Fore.RED}Could not resolve hostname: {target}")
                    continue
                print(f"{Fore.GREEN}Resolved to IP: {ip_address}")
            
            print(f"{Fore.YELLOW}Gathering information for {ip_address}...")
            
            # Get GeoIP information
            geoip_result, geoip_source = get_geoip_info(ip_address)
            if geoip_result:
                display_geoip_results(geoip_result, geoip_source)
            else:
                print(f"{Fore.RED}GeoIP lookup failed: {geoip_source}")
            
            # Get WHOIS information
            whois_result, whois_source = get_basic_whois_info(ip_address)
            if whois_result:
                display_whois_results(whois_result, whois_source)
            else:
                print(f"{Fore.RED}WHOIS lookup failed: {whois_source}")
                
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Lookup interrupted")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    main()
