#!/usr/bin/env python3
"""
Pengu Enhanced Network Intelligence Module - Comprehensive Information Gathering
SSL/TLS Analysis • DNS Intelligence • Network Discovery • GeoIP & WHOIS
"""

import socket
import ssl
import re
import subprocess
import platform
import threading
import time
from datetime import datetime, timezone
from urllib.parse import urlparse
from colorama import init, Fore, Style
from session_logger import log_tool_usage

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the enhanced network intelligence banner"""
    message = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════════╗
{Fore.GREEN}║ {Fore.MAGENTA}Pengu Enhanced Network Intelligence{Fore.GREEN}                      ║
{Fore.GREEN}║ {Fore.CYAN}SSL/TLS • DNS • ARP • Network Discovery • GeoIP & WHOIS{Fore.GREEN} ║
{Fore.GREEN}╚══════════════════════════════════════════════════════════════╝
"""
    print(message)

def get_ssl_certificate_info(hostname, port=443):
    """Get SSL certificate information with improved error handling (Issue 15)"""
    import socket
    import ssl
    from urllib.parse import urlparse
    
    # Clean hostname if URL was provided
    if hostname.startswith(('http://', 'https://')):
        parsed = urlparse(hostname)
        hostname = parsed.hostname or parsed.netloc.split(':')[0]
    
    # Remove any port specification from hostname
    if ':' in hostname and not hostname.startswith('['):  # Not IPv6
        hostname = hostname.split(':')[0]
    
    print(f"{Fore.CYAN}Attempting SSL connection to {hostname}:{port}...")
    
    # Try multiple connection approaches (Issue 15)
    connection_attempts = [
        {'timeout': 15, 'context_type': 'default'},
        {'timeout': 30, 'context_type': 'unverified'},
        {'timeout': 45, 'context_type': 'minimal'}
    ]
    
    for attempt_num, attempt_config in enumerate(connection_attempts, 1):
        try:
            print(f"{Fore.YELLOW}Connection attempt {attempt_num}/3 (timeout: {attempt_config['timeout']}s)...")
            
            # Create appropriate SSL context based on attempt type
            if attempt_config['context_type'] == 'default':
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            elif attempt_config['context_type'] == 'unverified':
                context = ssl._create_unverified_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            else:  # minimal
                context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                context.set_ciphers('ALL:@SECLEVEL=0')
            
            # First, test basic connectivity to the port
            try:
                test_sock = socket.create_connection((hostname, port), timeout=attempt_config['timeout'])
                test_sock.close()
                print(f"{Fore.GREEN}Port {port} is open on {hostname}")
            except socket.timeout:
                print(f"{Fore.RED}Connection timeout to {hostname}:{port}")
                continue
            except ConnectionRefusedError:
                print(f"{Fore.RED}Connection refused to {hostname}:{port}")
                continue
            except Exception as e:
                print(f"{Fore.RED}Connection test failed: {e}")
                continue
            
            # Now attempt SSL connection
            with socket.create_connection((hostname, port), timeout=attempt_config['timeout']) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert(binary_form=False)
                    cert_der = ssock.getpeercert(binary_form=True)
                    cipher = ssock.cipher()
                    protocol = ssock.version()
                    
                    print(f"{Fore.GREEN}SSL connection successful!")
                    print(f"{Fore.CYAN}Protocol: {protocol}")
                    print(f"{Fore.CYAN}Cipher: {cipher[0] if cipher else 'Unknown'}")
                    
                    if cert:
                        return analyze_certificate(cert, cert_der, cipher, protocol, hostname)
                    else:
                        return None, "No certificate found in SSL handshake"
                        
        except socket.timeout:
            print(f"{Fore.RED}Attempt {attempt_num}: Connection timeout after {attempt_config['timeout']}s")
            continue
        except ssl.SSLError as e:
            print(f"{Fore.RED}Attempt {attempt_num}: SSL error - {str(e)}")
            continue
        except ConnectionRefusedError:
            print(f"{Fore.RED}Attempt {attempt_num}: Connection refused")
            continue
        except Exception as e:
            print(f"{Fore.RED}Attempt {attempt_num}: Connection error - {str(e)}")
            continue
    
    # All attempts failed
    error_msg = f"All SSL connection attempts failed for {hostname}:{port}"
    suggestions = [
        f"• Verify {hostname} supports HTTPS on port {port}",
        "• Check if the service is running and accessible",
        "• Try with a different port (like 8443 for alternate HTTPS)",
        "• Ensure no firewall is blocking the connection"
    ]
    
    print(f"{Fore.RED}{error_msg}")
    for suggestion in suggestions:
        print(f"{Fore.YELLOW}{suggestion}")
    
    return None, error_msg

def analyze_certificate(cert, cert_der, cipher, protocol, hostname):
    """Analyze SSL certificate for security issues"""
    analysis = {
        'basic_info': {},
        'validity': {},
        'security_analysis': {},
        'cipher_info': {},
        'chain_info': {}
    }
    
    # Basic certificate information
    analysis['basic_info'] = {
        'subject': dict(x[0] for x in cert.get('subject', [])),
        'issuer': dict(x[0] for x in cert.get('issuer', [])),
        'version': cert.get('version', 'Unknown'),
        'serial_number': cert.get('serialNumber', 'Unknown'),
        'signature_algorithm': cert.get('signatureAlgorithm', 'Unknown')
    }
    
    # Certificate validity
    not_before = cert.get('notBefore')
    not_after = cert.get('notAfter')
    
    if not_before and not_after:
        try:
            not_before_dt = datetime.strptime(not_before, '%b %d %H:%M:%S %Y %Z')
            not_after_dt = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            now = datetime.now()
            
            days_until_expiry = (not_after_dt - now).days
            
            analysis['validity'] = {
                'not_before': not_before,
                'not_after': not_after,
                'days_until_expiry': days_until_expiry,
                'is_valid': not_before_dt <= now <= not_after_dt,
                'is_expired': now > not_after_dt,
                'expires_soon': days_until_expiry <= 30
            }
        except Exception as e:
            analysis['validity'] = {'error': f"Date parsing error: {e}"}
    
    # Cipher and protocol analysis
    if cipher:
        analysis['cipher_info'] = {
            'cipher_suite': cipher[0] if len(cipher) > 0 else 'Unknown',
            'protocol_version': cipher[1] if len(cipher) > 1 else 'Unknown',
            'key_bits': cipher[2] if len(cipher) > 2 else 'Unknown'
        }
    
    if protocol:
        analysis['cipher_info']['ssl_version'] = protocol
    
    # Security analysis
    security_issues = []
    recommendations = []
    
    # Check for weak protocols
    if protocol in ['SSLv2', 'SSLv3', 'TLSv1', 'TLSv1.1']:
        security_issues.append(f"Weak protocol: {protocol}")
        recommendations.append("Upgrade to TLS 1.2 or higher")
    
    # Check for weak ciphers
    if cipher and len(cipher) > 0:
        cipher_name = cipher[0].upper()
        weak_ciphers = ['RC4', 'DES', '3DES', 'MD5', 'SHA1']
        for weak in weak_ciphers:
            if weak in cipher_name:
                security_issues.append(f"Weak cipher component: {weak}")
                recommendations.append(f"Avoid {weak} in cipher suites")
    
    # Check certificate validity period
    if 'validity' in analysis and analysis['validity'].get('days_until_expiry'):
        days = analysis['validity']['days_until_expiry']
        if days <= 0:
            security_issues.append("Certificate has expired")
            recommendations.append("Renew certificate immediately")
        elif days <= 30:
            security_issues.append(f"Certificate expires in {days} days")
            recommendations.append("Schedule certificate renewal")
    
    # Check for hostname mismatch
    if hostname:
        subject_alt_names = []
        for ext in cert.get('subjectAltName', []):
            if ext[0] == 'DNS':
                subject_alt_names.append(ext[1])
        
        cn = analysis['basic_info']['subject'].get('commonName', '')
        hostname_match = (hostname.lower() == cn.lower() or 
                         hostname.lower() in [san.lower() for san in subject_alt_names])
        
        if not hostname_match:
            security_issues.append(f"Hostname mismatch: {hostname} not in certificate")
            recommendations.append("Ensure certificate matches the hostname")
    
    analysis['security_analysis'] = {
        'security_issues': security_issues,
        'recommendations': recommendations,
        'overall_rating': 'Poor' if len(security_issues) > 2 else 'Fair' if security_issues else 'Good'
    }
    
    return analysis, "success"

def display_ssl_analysis(analysis, hostname, port):
    """Display SSL certificate analysis results"""
    print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}SSL/TLS Certificate Analysis: {hostname}:{port}{Fore.GREEN}")
    print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════╝")
    
    # Basic information
    basic = analysis.get('basic_info', {})
    if basic:
        print(f"\n{Fore.YELLOW}Certificate Information:")
        print(f"{Fore.CYAN}  Common Name:       {Fore.WHITE}{basic.get('subject', {}).get('commonName', 'N/A')}")
        print(f"{Fore.CYAN}  Organization:      {Fore.WHITE}{basic.get('subject', {}).get('organizationName', 'N/A')}")
        print(f"{Fore.CYAN}  Issuer:            {Fore.WHITE}{basic.get('issuer', {}).get('commonName', 'N/A')}")
        print(f"{Fore.CYAN}  Serial Number:     {Fore.WHITE}{basic.get('serial_number', 'N/A')}")
        print(f"{Fore.CYAN}  Signature Alg:     {Fore.WHITE}{basic.get('signature_algorithm', 'N/A')}")
    
    # Validity information
    validity = analysis.get('validity', {})
    if validity and 'error' not in validity:
        print(f"\n{Fore.YELLOW}Certificate Validity:")
        print(f"{Fore.CYAN}  Valid From:        {Fore.WHITE}{validity.get('not_before', 'N/A')}")
        print(f"{Fore.CYAN}  Valid Until:       {Fore.WHITE}{validity.get('not_after', 'N/A')}")
        
        days = validity.get('days_until_expiry', 0)
        if days > 30:
            color = Fore.GREEN
        elif days > 0:
            color = Fore.YELLOW
        else:
            color = Fore.RED
        
        print(f"{Fore.CYAN}  Days Until Expiry: {color}{days}")
        print(f"{Fore.CYAN}  Status:            {color}{'Valid' if validity.get('is_valid') else 'Invalid'}")
    
    # Cipher information
    cipher = analysis.get('cipher_info', {})
    if cipher:
        print(f"\n{Fore.YELLOW}Cipher Information:")
        print(f"{Fore.CYAN}  Cipher Suite:      {Fore.WHITE}{cipher.get('cipher_suite', 'N/A')}")
        print(f"{Fore.CYAN}  Protocol Version:  {Fore.WHITE}{cipher.get('ssl_version', 'N/A')}")
        print(f"{Fore.CYAN}  Key Length:        {Fore.WHITE}{cipher.get('key_bits', 'N/A')} bits")
    
    # Security analysis
    security = analysis.get('security_analysis', {})
    if security:
        rating = security.get('overall_rating', 'Unknown')
        rating_color = Fore.GREEN if rating == 'Good' else Fore.YELLOW if rating == 'Fair' else Fore.RED
        
        print(f"\n{Fore.YELLOW}Security Analysis:")
        print(f"{Fore.CYAN}  Overall Rating:    {rating_color}{rating}")
        
        issues = security.get('security_issues', [])
        if issues:
            print(f"{Fore.RED}  Security Issues:")
            for issue in issues:
                print(f"{Fore.RED}    • {issue}")
        
        recommendations = security.get('recommendations', [])
        if recommendations:
            print(f"{Fore.YELLOW}  Recommendations:")
            for rec in recommendations:
                print(f"{Fore.YELLOW}    • {rec}")
        
        if not issues:
            print(f"{Fore.GREEN}  ✓ No major security issues detected")

def get_comprehensive_dns_records(hostname):
    """Get comprehensive DNS records for a hostname"""
    try:
        import dns.resolver
        import dns.zone
        import dns.query
        
        records = {}
        
        # Standard record types to query
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME', 'PTR']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(hostname, record_type)
                records[record_type] = []
                for answer in answers:
                    records[record_type].append(str(answer))
            except dns.resolver.NXDOMAIN:
                records[record_type] = ['NXDOMAIN']
            except dns.resolver.NoAnswer:
                records[record_type] = ['No Answer']
            except Exception as e:
                records[record_type] = [f'Error: {str(e)}']
        
        return records, "success"
        
    except ImportError:
        return None, "DNS module not available"
    except Exception as e:
        return None, f"DNS lookup error: {str(e)}"

def attempt_dns_zone_transfer(hostname):
    """Attempt DNS zone transfer"""
    try:
        import dns.resolver
        import dns.zone
        import dns.query
        
        # Get NS records first
        try:
            ns_records = dns.resolver.resolve(hostname, 'NS')
            nameservers = [str(ns) for ns in ns_records]
        except:
            return None, "Could not get nameservers"
        
        transfer_results = {}
        
        for ns in nameservers:
            try:
                # Remove trailing dot if present
                ns_clean = ns.rstrip('.')
                
                # Attempt zone transfer
                zone = dns.zone.from_xfr(dns.query.xfr(ns_clean, hostname, timeout=10))
                
                if zone:
                    transfer_results[ns] = {
                        'status': 'SUCCESS',
                        'records': len(zone.nodes),
                        'warning': 'Zone transfer allowed - potential security risk'
                    }
                else:
                    transfer_results[ns] = {
                        'status': 'FAILED',
                        'error': 'No zone data returned'
                    }
                    
            except Exception as e:
                transfer_results[ns] = {
                    'status': 'FAILED',
                    'error': str(e)
                }
        
        return transfer_results, "completed"
        
    except ImportError:
        return None, "DNS module not available"
    except Exception as e:
        return None, f"Zone transfer error: {str(e)}"

def detect_dns_cache_poisoning(hostname):
    """Improved DNS cache poisoning detection that accounts for GeoDNS and load balancing"""
    try:
        import dns.resolver
        
        # Query multiple DNS servers and compare results
        public_dns_servers = [
            '8.8.8.8',      # Google
            '1.1.1.1',      # Cloudflare
            '208.67.222.222', # OpenDNS
            '9.9.9.9'       # Quad9
        ]
        
        results = {}
        a_records = {}
        
        for dns_server in public_dns_servers:
            try:
                resolver = dns.resolver.Resolver()
                resolver.nameservers = [dns_server]
                resolver.timeout = 5
                
                answers = resolver.resolve(hostname, 'A')
                ips = [str(answer) for answer in answers]
                a_records[dns_server] = sorted(ips)
                
            except Exception as e:
                a_records[dns_server] = f"Error: {str(e)}"
        
        # Improved analysis that considers GeoDNS and load balancing
        ip_sets = [set(ips) for ips in a_records.values() if isinstance(ips, list)]
        
        if len(ip_sets) > 1:
            # Check if all sets are the same
            all_same = all(ip_set == ip_sets[0] for ip_set in ip_sets)
            
            if not all_same:
                # Check if there's any overlap between sets (common for CDNs/GeoDNS)
                all_ips = set()
                for ip_set in ip_sets:
                    all_ips.update(ip_set)
                
                # Check if variations are within reasonable bounds for GeoDNS
                max_ips = max(len(ip_set) for ip_set in ip_sets)
                min_ips = min(len(ip_set) for ip_set in ip_sets)
                
                # More intelligent detection - only flag as suspicious if dramatically different
                if max_ips > min_ips * 3 or len(all_ips) > 20:
                    results['status'] = 'SUSPICIOUS'
                    results['warning'] = 'Significant DNS response variations detected - investigate manually'
                else:
                    results['status'] = 'NORMAL_VARIATION'
                    results['message'] = 'DNS responses vary (likely GeoDNS/CDN load balancing - normal behavior)'
            else:
                results['status'] = 'CONSISTENT'
                results['message'] = 'DNS responses consistent across servers'
        else:
            results['status'] = 'INSUFFICIENT_DATA'
            results['message'] = 'Not enough valid responses to compare'
        
        results['server_responses'] = a_records
        
        return results, "completed"
        
    except ImportError:
        return None, "DNS module not available"
    except Exception as e:
        return None, f"DNS poisoning detection error: {str(e)}"

def display_dns_analysis(records, zone_transfer, cache_poisoning, hostname):
    """Display comprehensive DNS analysis"""
    print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}DNS Intelligence Report: {hostname}{Fore.GREEN}")
    print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════╝")
    
    # DNS Records
    if records:
        print(f"\n{Fore.YELLOW}DNS Records:")
        for record_type, values in records.items():
            if values and values != ['No Answer']:
                print(f"{Fore.CYAN}  {record_type:6}: {Fore.WHITE}", end="")
                if len(values) == 1:
                    print(values[0])
                else:
                    print()
                    for value in values:
                        print(f"{Fore.WHITE}         {value}")
    
    # Zone Transfer Results
    if zone_transfer:
        print(f"\n{Fore.YELLOW}Zone Transfer Attempts:")
        for ns, result in zone_transfer.items():
            status = result.get('status', 'Unknown')
            color = Fore.RED if status == 'SUCCESS' else Fore.GREEN
            print(f"{Fore.CYAN}  {ns}: {color}{status}")
            
            if result.get('warning'):
                print(f"{Fore.RED}    ⚠ {result['warning']}")
            if result.get('error'):
                print(f"{Fore.YELLOW}    Error: {result['error']}")
    
    # Cache Poisoning Detection
    if cache_poisoning:
        print(f"\n{Fore.YELLOW}DNS Cache Poisoning Analysis:")
        status = cache_poisoning.get('status', 'Unknown')
        
        if status == 'SUSPICIOUS':
            print(f"{Fore.RED}  Status: {status}")
            print(f"{Fore.RED}  ⚠ {cache_poisoning.get('warning', '')}")
        elif status == 'NORMAL_VARIATION':
            print(f"{Fore.GREEN}  Status: {status}")
            print(f"{Fore.GREEN}  ✓ {cache_poisoning.get('message', '')}")
        elif status == 'CONSISTENT':
            print(f"{Fore.GREEN}  Status: {status}")
            print(f"{Fore.GREEN}  ✓ {cache_poisoning.get('message', '')}")
        else:
            print(f"{Fore.YELLOW}  Status: {status}")
            print(f"{Fore.YELLOW}  {cache_poisoning.get('message', '')}")
        
        print(f"\n{Fore.CYAN}  Server Responses:")
        for server, ips in cache_poisoning.get('server_responses', {}).items():
            if isinstance(ips, list):
                print(f"{Fore.CYAN}    {server}: {Fore.WHITE}{', '.join(ips)}")
            else:
                print(f"{Fore.CYAN}    {server}: {Fore.YELLOW}{ips}")

def perform_arp_scan(network_range):
    """Perform ARP scan for local network discovery with Windows compatibility (Issue 14)"""
    import platform
    import subprocess
    
    # Check for admin privileges since ARP scanning typically requires raw socket access
    try:
        from admin_utils import check_admin_for_tool
        admin_result = check_admin_for_tool('arp_scan')
        if admin_result is None:  # User chose to return to main menu
            return None, "User cancelled - admin privileges required"
        elif not admin_result:  # Continuing without admin
            print(f"{Fore.YELLOW}Warning: ARP scan may not work properly without admin privileges")
    except ImportError:
        print(f"{Fore.YELLOW}Warning: Cannot check admin privileges")
    
    # Handle Windows raw socket limitations (Issue 14)
    if platform.system() == "Windows":
        try:
            # Try to use native Windows ARP command first
            print(f"{Fore.CYAN}Using Windows ARP table for network discovery...")
            result = subprocess.run(['arp', '-a'], capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                devices = []
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'dynamic' in line.lower() or 'static' in line.lower():
                        parts = line.split()
                        if len(parts) >= 2:
                            ip = parts[0].strip()
                            mac = parts[1].strip()
                            if ip and mac and '-' in mac:
                                devices.append({'ip': ip, 'mac': mac})
                if devices:
                    return devices, "success (Windows ARP table)"
        except Exception as e:
            print(f"{Fore.YELLOW}Windows ARP table scan failed: {e}")
    
    # Try Scapy with Windows compatibility checks (Issue 14)
    try:
        from scapy.all import ARP, Ether, srp
        import ipaddress
        
        # Windows-specific Scapy checks
        if platform.system() == "Windows":
            try:
                # Check if Npcap is available
                from scapy.arch.windows import get_windows_if_list
                interfaces = get_windows_if_list()
                if not interfaces:
                    return None, "No network interfaces available. Please install Npcap or WinPcap"
                print(f"{Fore.GREEN}Npcap/WinPcap detected - proceeding with Scapy scan")
            except Exception as e:
                return None, f"Windows network driver issue: {e}. Please install Npcap"
        
        # Validate network range
        try:
            network = ipaddress.ip_network(network_range, strict=False)
        except ValueError:
            return None, f"Invalid network range: {network_range}"
        
        print(f"{Fore.CYAN}Scanning network: {network}")
        
        # Create ARP request with Windows-compatible timeout
        arp_request = ARP(pdst=str(network))
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        
        # Use longer timeout on Windows
        timeout_val = 5 if platform.system() == "Windows" else 2
        
        # Send packets and receive responses
        answered_list = srp(arp_request_broadcast, timeout=timeout_val, verbose=False)[0]
        
        devices = []
        for element in answered_list:
            device = {
                'ip': element[1].psrc,
                'mac': element[1].hwsrc
            }
            devices.append(device)
        
        return devices, "success"
        
    except ImportError:
        error_msg = "Scapy module not available"
        if platform.system() == "Windows":
            error_msg += ". For Windows, please install Npcap from https://nmap.org/npcap/"
        return None, error_msg
    except PermissionError:
        error_msg = "Permission denied - raw socket access requires administrator privileges"
        if platform.system() == "Windows":
            error_msg += ". Please run as Administrator and ensure Npcap is installed"
        return None, error_msg
    except Exception as e:
        error_msg = f"ARP scan error: {str(e)}"
        if platform.system() == "Windows" and "raw socket" in str(e).lower():
            error_msg += ". Please install Npcap and run as Administrator"
        return None, error_msg

def detect_os_fingerprint(ip_address):
    """Basic OS fingerprinting using various techniques"""
    # Check for admin privileges for advanced fingerprinting
    try:
        from admin_utils import check_admin_for_tool
        admin_result = check_admin_for_tool('os_fingerprinting')
        if admin_result is None:  # User chose to return to main menu
            return None, "User cancelled - admin privileges recommended"
        elif not admin_result:  # Continuing without admin
            print(f"{Fore.YELLOW}Warning: OS fingerprinting may be limited without admin privileges")
    except ImportError:
        print(f"{Fore.YELLOW}Warning: Cannot check admin privileges")
    
    try:
        fingerprint = {
            'ip': ip_address,
            'methods': {}
        }
        
        # TTL-based detection (NOTE: This method has limitations due to network hops)
        try:
            import subprocess
            import platform
            
            if platform.system().lower() == 'windows':
                result = subprocess.run(['ping', '-n', '1', ip_address], 
                                      capture_output=True, text=True, timeout=10)
            else:
                result = subprocess.run(['ping', '-c', '1', ip_address], 
                                      capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                # Extract TTL from ping output
                output = result.stdout
                ttl_match = re.search(r'ttl=(\d+)', output.lower())
                if ttl_match:
                    ttl = int(ttl_match.group(1))
                    
                    # Improved TTL analysis with ranges and confidence levels
                    confidence = "Low"
                    if ttl <= 32:
                        os_guess = "Linux/Unix (or through many hops)"
                        confidence = "Very Low" if ttl < 20 else "Low"
                    elif ttl <= 64:
                        os_guess = "Linux/Unix"
                        confidence = "Medium" if ttl > 50 else "Low"
                    elif ttl <= 128:
                        os_guess = "Windows"
                        confidence = "Medium" if ttl > 100 else "Low"
                    elif ttl <= 255:
                        os_guess = "Cisco/Network Device"
                        confidence = "Low"
                    else:
                        os_guess = "Unknown"
                        confidence = "None"
                    
                    fingerprint['methods']['ttl'] = {
                        'ttl_value': ttl,
                        'os_guess': os_guess,
                        'confidence': confidence,
                        'note': 'TTL-based detection is unreliable due to network hops decreasing TTL values'
                    }
        except Exception as e:
            fingerprint['methods']['ttl'] = {'error': str(e)}
        
        # TCP Window Size detection (requires scapy)
        try:
            from scapy.all import IP, TCP, sr1
            
            # Send SYN packet and analyze response
            packet = IP(dst=ip_address)/TCP(dport=80, flags="S")
            response = sr1(packet, timeout=3, verbose=False)
            
            if response and response.haslayer(TCP):
                window_size = response[TCP].window
                
                # Common window sizes for different OS
                if window_size == 65535:
                    os_guess = "Linux/Unix (2.6 kernel)"
                elif window_size == 8192:
                    os_guess = "Windows XP/2003"
                elif window_size == 16384:
                    os_guess = "Windows Vista/7/8/10"
                elif window_size == 5840:
                    os_guess = "Linux (older kernel)"
                else:
                    os_guess = f"Unknown (window: {window_size})"
                
                fingerprint['methods']['tcp_window'] = {
                    'window_size': window_size,
                    'os_guess': os_guess
                }
        except Exception as e:
            fingerprint['methods']['tcp_window'] = {'error': str(e)}
        
        return fingerprint, "completed"
        
    except Exception as e:
        return None, f"OS fingerprinting error: {str(e)}"

def detect_service_versions(ip_address, ports=None):
    """Enhanced service version detection"""
    if ports is None:
        ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]
    
    services = {}
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Increased timeout
            
            result = sock.connect_ex((ip_address, port))
            if result == 0:
                # Port is open, try to get banner
                service_info = {
                    'port': port,
                    'status': 'open',
                    'service': get_service_name(port)
                }
                
                # Enhanced banner grabbing for different service types
                try:
                    if port in [21, 22, 25, 110, 143, 993, 995]:  # Services with immediate banners
                        banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                        if banner:
                            service_info['banner'] = banner
                            service_info['version'] = extract_version_from_banner(banner)
                    
                    elif port in [80, 8080, 8000]:  # HTTP services
                        # Send HTTP request to get server header
                        http_request = f"HEAD / HTTP/1.1\r\nHost: {ip_address}\r\n\r\n"
                        sock.send(http_request.encode())
                        response = sock.recv(1024).decode('utf-8', errors='ignore')
                        if response:
                            # Extract Server header
                            server_match = re.search(r'Server:\s*([^\r\n]+)', response, re.IGNORECASE)
                            if server_match:
                                service_info['banner'] = server_match.group(1).strip()
                                service_info['version'] = extract_version_from_banner(server_match.group(1))
                            else:
                                service_info['banner'] = "HTTP server (no server header)"
                                service_info['version'] = "HTTP detected"
                    
                    elif port == 443:  # HTTPS service
                        service_info['banner'] = "HTTPS/SSL service"
                        service_info['version'] = "SSL/TLS detected"
                        # Could add SSL certificate analysis here
                    
                    elif port == 53:  # DNS service
                        service_info['banner'] = "DNS service"
                        service_info['version'] = "DNS detected"
                    
                except Exception as e:
                    # Even if banner grabbing fails, we know the port is open
                    service_info['banner_error'] = str(e)
                
                services[port] = service_info
            
            sock.close()
            
        except Exception:
            continue
    
    return services, "completed"

def get_service_name(port):
    """Get common service name for port"""
    common_ports = {
        21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
        80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS',
        993: 'IMAPS', 995: 'POP3S'
    }
    return common_ports.get(port, f'Unknown({port})')

def extract_version_from_banner(banner):
    """Extract version information from service banner"""
    # Common version patterns
    patterns = [
        r'(\w+)[\s/](\d+\.[\d\.]+)',  # Software/1.2.3
        r'(\w+)-(\d+\.[\d\.]+)',      # Software-1.2.3
        r'(\w+)\s+(\d+\.[\d\.]+)',    # Software 1.2.3
    ]
    
    for pattern in patterns:
        match = re.search(pattern, banner, re.IGNORECASE)
        if match:
            return f"{match.group(1)} {match.group(2)}"
    
    return "Version not detected"

def display_network_discovery(arp_results, os_fingerprint, service_detection, target):
    """Display network discovery results"""
    print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}Network Discovery Report: {target}{Fore.GREEN}")
    print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════╝")
    
    # ARP Scan Results
    if arp_results:
        print(f"\n{Fore.YELLOW}ARP Scan Results:")
        print(f"{Fore.CYAN}Found {len(arp_results)} active devices:")
        print(f"{Fore.CYAN}{'IP Address':<15} {'MAC Address':<18}")
        print(f"{Fore.CYAN}{'-'*15} {'-'*18}")
        for device in arp_results:
            print(f"{Fore.WHITE}{device['ip']:<15} {device['mac']:<18}")
    
    # OS Fingerprinting
    if os_fingerprint:
        print(f"\n{Fore.YELLOW}OS Fingerprinting:")
        methods = os_fingerprint.get('methods', {})
        
        if 'ttl' in methods and 'error' not in methods['ttl']:
            ttl_info = methods['ttl']
            confidence = ttl_info.get('confidence', 'Unknown')
            confidence_color = Fore.GREEN if confidence == 'High' else Fore.YELLOW if confidence == 'Medium' else Fore.RED
            print(f"{Fore.CYAN}  TTL Analysis:      {Fore.WHITE}{ttl_info['os_guess']} (TTL: {ttl_info['ttl_value']})")
            print(f"{Fore.CYAN}  Confidence:        {confidence_color}{confidence}")
            if 'note' in ttl_info:
                print(f"{Fore.YELLOW}  Note: {ttl_info['note']}")
        
        if 'tcp_window' in methods and 'error' not in methods['tcp_window']:
            window_info = methods['tcp_window']
            print(f"{Fore.CYAN}  TCP Window:        {Fore.WHITE}{window_info['os_guess']}")
    
    # Service Detection
    if service_detection:
        print(f"\n{Fore.YELLOW}Service Detection:")
        print(f"{Fore.CYAN}{'Port':<6} {'Service':<10} {'Version':<30}")
        print(f"{Fore.CYAN}{'-'*6} {'-'*10} {'-'*30}")
        
        for port, info in service_detection.items():
            service = info.get('service', 'Unknown')
            version = info.get('version', 'Not detected')
            if 'banner' in info:
                version = info['banner'][:30] + '...' if len(info['banner']) > 30 else info['banner']
            
            print(f"{Fore.WHITE}{port:<6} {service:<10} {version:<30}")

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
        
        # Check if proxy mode is enabled
        proxies = None
        try:
            from proxy_manager import get_proxy_for_requests
            proxies = get_proxy_for_requests()
            if proxies:
                print(f"{Fore.YELLOW}Using proxy for GeoIP lookup...")
        except ImportError:
            pass  # Proxy manager not available
        except Exception:
            pass  # No proxy configured
        
        # Primary source: ipinfo.io
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json", timeout=10, proxies=proxies)
            if response.status_code == 200:
                data = response.json()
                if 'error' not in data:
                    return data, "ipinfo.io"
        except:
            pass
        
        # Fallback source: ipapi.co
        try:
            response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10, proxies=proxies)
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
            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10, proxies=proxies)
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
        
        # Check if proxy mode is enabled
        proxies = None
        try:
            from proxy_manager import get_proxy_for_requests
            proxies = get_proxy_for_requests()
            if proxies:
                print(f"{Fore.YELLOW}Using proxy for WHOIS lookup...")
        except ImportError:
            pass  # Proxy manager not available
        except Exception:
            pass  # No proxy configured
        
        # Try ARIN REST API
        try:
            response = requests.get(f"https://whois.arin.net/rest/ip/{ip}.json", timeout=10, proxies=proxies)
            if response.status_code == 200:
                return response.json(), "ARIN"
        except:
            pass
            
        # Try alternative WHOIS service
        try:
            response = requests.get(f"https://ipwhois.app/json/{ip}", timeout=10, proxies=proxies)
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
    """Display WHOIS results in a formatted way (Enhanced for Issue 11)"""
    print(f"\n{Fore.GREEN}╔══════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}WHOIS Information (Source: {source}){Fore.GREEN}")
    print(f"{Fore.GREEN}╚══════════════════════════════════════╝")
    
    # Handle raw dictionary/JSON data by extracting meaningful fields
    if isinstance(data, dict):
        if source == "ARIN":
            # Handle ARIN format
            whois_net = data.get('net', {})
            
            # Try to extract ASN from ARIN data
            asn_info = "N/A"
            org_ref = whois_net.get('orgRef', {})
            if org_ref and '@handle' in org_ref:
                org_handle = org_ref.get('@handle', '')
                # ASN often appears in organization handles
                asn_match = re.search(r'AS(\d+)', org_handle)
                if asn_match:
                    asn_info = f"AS{asn_match.group(1)}"
            
            # Helper function to safely extract nested values
            def safe_extract(obj, default='N/A'):
                if isinstance(obj, dict):
                    if '$' in obj:
                        return obj['$']
                    elif 'value' in obj:
                        return obj['value']
                    elif '@name' in obj:
                        return obj['@name']
                    elif 'text' in obj:
                        return obj['text']
                    elif len(obj) == 1:
                        # If single key-value pair, return the value
                        return list(obj.values())[0]
                return str(obj) if obj else default
            
            fields = [
                ('Network Name', safe_extract(whois_net.get('name'))),
                ('Handle', safe_extract(whois_net.get('handle'))),
                ('Start Address', safe_extract(whois_net.get('startAddress'))),
                ('End Address', safe_extract(whois_net.get('endAddress'))),
                ('CIDR', safe_extract(whois_net.get('cidr'))),
                ('ASN', asn_info),
                ('Parent Network', org_ref.get('@name', 'N/A')),
                ('Organization', org_ref.get('@name', 'N/A')),
                ('Registration Date', safe_extract(whois_net.get('registrationDate'))),
                ('Last Updated', safe_extract(whois_net.get('updateDate')))
            ]
        else:
            # Handle ipwhois.app format and other sources
            fields = [
                ('Network', data.get('net', 'N/A')),
                ('CIDR', data.get('cidr', 'N/A')),
                ('Organization', data.get('org', 'N/A')),
                ('ISP', data.get('isp', 'N/A')),
                ('Country', data.get('country', 'N/A')),
                ('Region', data.get('region', 'N/A')),
                ('ASN', f"{data.get('asn', 'N/A')} - {data.get('asn_org', 'N/A')}")
            ]
        
        # Display formatted fields
        for label, value in fields:
            if value and value != 'N/A' and str(value).strip():
                # Clean up value - remove XML/JSON artifacts
                clean_value = str(value).replace('@xmlns', '').replace('$:', '').strip()
                if clean_value and clean_value != 'N/A':
                    print(f"{Fore.CYAN}{label:15}: {Fore.WHITE}{clean_value}")
    else:
        # Fallback for non-dictionary data
        print(f"{Fore.YELLOW}Raw data: {Fore.WHITE}{str(data)[:200]}...")
        print(f"{Fore.RED}Warning: Unexpected data format received from {source}")

def main():
    """Main function with enhanced network intelligence capabilities"""
    print_banner()
    
    session_start = time.time()
    
    while True:
        try:
            print(f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════╗
{Fore.MAGENTA}║                 {Fore.CYAN}Intelligence Menu{Fore.MAGENTA}                     ║
{Fore.MAGENTA}╚══════════════════════════════════════════════════════════╝

{Fore.GREEN}1. {Fore.WHITE}Standard GeoIP & WHOIS Lookup
{Fore.GREEN}2. {Fore.WHITE}SSL/TLS Certificate Analysis
{Fore.GREEN}3. {Fore.WHITE}Comprehensive DNS Intelligence
{Fore.GREEN}4. {Fore.WHITE}Network Discovery (ARP + OS + Services)
{Fore.GREEN}5. {Fore.WHITE}Complete Intelligence Report (All Above)
{Fore.GREEN}6. {Fore.WHITE}Exit to main menu
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-6): ").strip()
            
            if choice == '1':
                target = input(f"{Fore.YELLOW}Enter IP address or hostname: ").strip()
                if target:
                    perform_standard_lookup(target)
            
            elif choice == '2':
                target = input(f"{Fore.YELLOW}Enter hostname or IP: ").strip()
                port = input(f"{Fore.YELLOW}Enter port (default 443): ").strip()
                port = int(port) if port.isdigit() else 443
                if target:
                    perform_ssl_analysis(target, port)
            
            elif choice == '3':
                target = input(f"{Fore.YELLOW}Enter hostname: ").strip()
                if target:
                    perform_dns_intelligence(target)
            
            elif choice == '4':
                print(f"""
{Fore.YELLOW}Network Discovery Options:
{Fore.GREEN}1. {Fore.WHITE}Single IP analysis
{Fore.GREEN}2. {Fore.WHITE}Network range scan
""")
                disc_choice = input(f"{Fore.YELLOW}Select option (1-2): ").strip()
                
                if disc_choice == '1':
                    target = input(f"{Fore.YELLOW}Enter IP address: ").strip()
                    if target and validate_ip(target):
                        perform_network_discovery_single(target)
                    else:
                        print(f"{Fore.RED}Invalid IP address")
                
                elif disc_choice == '2':
                    network = input(f"{Fore.YELLOW}Enter network range (e.g., 192.168.1.0/24): ").strip()
                    if network:
                        perform_network_discovery_range(network)
            
            elif choice == '5':
                target = input(f"{Fore.YELLOW}Enter hostname or IP for complete analysis: ").strip()
                if target:
                    perform_complete_intelligence(target)
            
            elif choice == '6':
                # Log session summary
                session_duration = time.time() - session_start
                log_tool_usage("enhanced_tracker", {
                    "session_duration": round(session_duration, 2),
                    "analysis_type": "intelligence_session"
                })
                break
            
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-6.")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Analysis interrupted")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

def perform_standard_lookup(target):
    """Perform standard GeoIP and WHOIS lookup"""
    start_time = time.time()
    
    # Determine if input is IP or hostname
    if validate_ip(target):
        ip_address = target
        print(f"{Fore.CYAN}Analyzing IP: {ip_address}")
    else:
        print(f"{Fore.CYAN}Resolving hostname: {target}")
        ip_address = resolve_hostname(target)
        if not ip_address:
            print(f"{Fore.RED}Could not resolve hostname: {target}")
            return
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
    
    # Log the activity
    duration = time.time() - start_time
    log_tool_usage("enhanced_tracker", {
        "analysis_type": "standard_lookup",
        "target": target,
        "resolved_ip": ip_address,
        "duration": round(duration, 2),
        "geoip_success": geoip_result is not None,
        "whois_success": whois_result is not None
    })
    
    print()

def perform_ssl_analysis(hostname, port):
    """Perform SSL/TLS certificate analysis"""
    start_time = time.time()
    
    print(f"{Fore.CYAN}Analyzing SSL certificate for {hostname}:{port}...")
    
    analysis, status = get_ssl_certificate_info(hostname, port)
    
    if analysis:
        display_ssl_analysis(analysis, hostname, port)
        
        # Log the activity
        duration = time.time() - start_time
        security_rating = analysis.get('security_analysis', {}).get('overall_rating', 'Unknown')
        issues_count = len(analysis.get('security_analysis', {}).get('security_issues', []))
        
        log_tool_usage("enhanced_tracker", {
            "analysis_type": "ssl_analysis",
            "target": f"{hostname}:{port}",
            "duration": round(duration, 2),
            "security_rating": security_rating,
            "issues_found": issues_count,
            "certificate_valid": analysis.get('validity', {}).get('is_valid', False)
        })
    else:
        print(f"{Fore.RED}SSL analysis failed: {status}")

def perform_dns_intelligence(hostname):
    """Perform comprehensive DNS intelligence gathering"""
    start_time = time.time()
    
    print(f"{Fore.CYAN}Performing DNS intelligence for {hostname}...")
    
    # Get DNS records
    print(f"{Fore.YELLOW}Gathering DNS records...")
    dns_records, dns_status = get_comprehensive_dns_records(hostname)
    
    # Attempt zone transfer
    print(f"{Fore.YELLOW}Attempting zone transfers...")
    zone_transfer, zt_status = attempt_dns_zone_transfer(hostname)
    
    # Check for cache poisoning
    print(f"{Fore.YELLOW}Checking for DNS cache poisoning...")
    cache_poisoning, cp_status = detect_dns_cache_poisoning(hostname)
    
    # Display results
    if dns_records or zone_transfer or cache_poisoning:
        display_dns_analysis(dns_records, zone_transfer, cache_poisoning, hostname)
        
        # Log the activity
        duration = time.time() - start_time
        log_tool_usage("enhanced_tracker", {
            "analysis_type": "dns_intelligence",
            "target": hostname,
            "duration": round(duration, 2),
            "dns_records_found": len(dns_records) if dns_records else 0,
            "zone_transfer_attempted": zone_transfer is not None,
            "cache_poisoning_checked": cache_poisoning is not None
        })
    else:
        print(f"{Fore.RED}DNS intelligence gathering failed")

def perform_network_discovery_single(ip_address):
    """Perform network discovery for a single IP"""
    start_time = time.time()
    
    print(f"{Fore.CYAN}Performing network discovery for {ip_address}...")
    
    # OS Fingerprinting
    print(f"{Fore.YELLOW}OS fingerprinting...")
    os_fingerprint, os_status = detect_os_fingerprint(ip_address)
    
    # Service Detection
    print(f"{Fore.YELLOW}Service detection...")
    services, service_status = detect_service_versions(ip_address)
    
    # Display results
    if os_fingerprint or services:
        display_network_discovery(None, os_fingerprint, services, ip_address)
        
        # Log the activity
        duration = time.time() - start_time
        log_tool_usage("enhanced_tracker", {
            "analysis_type": "network_discovery_single",
            "target": ip_address,
            "duration": round(duration, 2),
            "os_detection_attempted": os_fingerprint is not None,
            "services_found": len(services) if services else 0
        })
    else:
        print(f"{Fore.RED}Network discovery failed")

def perform_network_discovery_range(network_range):
    """Perform network discovery for a range"""
    start_time = time.time()
    
    print(f"{Fore.CYAN}Performing ARP scan for {network_range}...")
    
    # ARP Scan
    arp_results, arp_status = perform_arp_scan(network_range)
    
    if arp_results:
        display_network_discovery(arp_results, None, None, network_range)
        
        # Log the activity
        duration = time.time() - start_time
        log_tool_usage("enhanced_tracker", {
            "analysis_type": "network_discovery_range", 
            "target": network_range,
            "duration": round(duration, 2),
            "devices_found": len(arp_results)
        })
    else:
        print(f"{Fore.RED}ARP scan failed: {arp_status}")

def export_intelligence_report(target, duration, completed, analysis_results):
    """Export complete intelligence analysis to file"""
    try:
        from datetime import datetime
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        target_safe = target.replace(':', '_').replace('.', '_').replace('/', '_')
        filename = f"intelligence_report_{target_safe}_{timestamp}.txt"
        
        report_content = f"""PENGU COMPLETE INTELLIGENCE REPORT
{'=' * 50}

Target:              {target}
Analysis Date:       {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Analysis Duration:   {duration:.2f} seconds
Modules Completed:   {completed}/4

ANALYSIS SUMMARY
{'-' * 30}
"""
        
        # Add module completion status
        modules = ['GeoIP & WHOIS', 'SSL/TLS Analysis', 'DNS Intelligence', 'Network Discovery']
        module_keys = ['geoip', 'ssl', 'dns', 'network_discovery']
        
        for i, (module_name, key) in enumerate(zip(modules, module_keys)):
            status = "✓ COMPLETED" if key in analysis_results else "✗ SKIPPED/FAILED"
            report_content += f"{module_name:20} : {status}\n"
        
        report_content += f"""
DETAILED RESULTS
{'-' * 30}
For detailed results, please run the individual analysis modules:
- Standard GeoIP & WHOIS Lookup
- SSL/TLS Certificate Analysis  
- Comprehensive DNS Intelligence
- Network Discovery (ARP + OS + Services)

This summary report shows which modules completed successfully.
For full technical details, use the individual analysis options.

Report generated by Pengu v2.1
"""
        
        with open(filename, 'w') as f:
            f.write(report_content)
        
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, filename)
        print(f"{Fore.GREEN}✓ Intelligence report exported to: {full_path}")
        return filename
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting intelligence report: {e}")
        return None

def perform_complete_intelligence(target):
    """Perform complete intelligence gathering"""
    start_time = time.time()
    
    print(f"{Fore.CYAN}Performing complete intelligence analysis for {target}...")
    print(f"{Fore.YELLOW}This may take several minutes...")
    
    # Determine target type and resolve if needed
    if validate_ip(target):
        ip_address = target
        hostname = target
    else:
        hostname = target
        ip_address = resolve_hostname(target)
        if not ip_address:
            print(f"{Fore.RED}Could not resolve hostname: {target}")
            return
    
    analysis_results = {}
    
    # 1. Standard lookup
    print(f"\n{Fore.MAGENTA}[1/4] Standard GeoIP & WHOIS Lookup... {Fore.CYAN}[Starting]")
    geoip_result, _ = get_geoip_info(ip_address)
    whois_result, _ = get_basic_whois_info(ip_address)
    
    if geoip_result:
        display_geoip_results(geoip_result, "Complete Analysis")
        analysis_results['geoip'] = True
    if whois_result:
        display_whois_results(whois_result, "Complete Analysis")
        analysis_results['whois'] = True
    print(f"{Fore.GREEN}[1/4] Standard GeoIP & WHOIS Lookup... [Completed]")
    
    # 2. SSL Analysis (if hostname provided)
    if not validate_ip(target):
        print(f"\n{Fore.MAGENTA}[2/4] SSL/TLS Certificate Analysis... {Fore.CYAN}[Starting]")
        ssl_analysis, ssl_status = get_ssl_certificate_info(hostname, 443)
        if ssl_analysis:
            display_ssl_analysis(ssl_analysis, hostname, 443)
            analysis_results['ssl'] = True
            print(f"{Fore.GREEN}[2/4] SSL/TLS Certificate Analysis... [Completed]")
        else:
            print(f"{Fore.YELLOW}[2/4] SSL/TLS Certificate Analysis... [Skipped: {ssl_status}]")
            print(f"{Fore.YELLOW}Possible reasons: Port 443 not open, no SSL service, or connection timeout")
    else:
        print(f"\n{Fore.YELLOW}[2/4] SSL/TLS Certificate Analysis... [Skipped: Target is IP address only]")
    
    # 3. DNS Intelligence (if hostname provided)
    if not validate_ip(target):
        print(f"\n{Fore.MAGENTA}[3/4] Comprehensive DNS Intelligence... {Fore.CYAN}[Starting]")
        dns_records, _ = get_comprehensive_dns_records(hostname)
        zone_transfer, _ = attempt_dns_zone_transfer(hostname)
        cache_poisoning, _ = detect_dns_cache_poisoning(hostname)
        
        if dns_records or zone_transfer or cache_poisoning:
            display_dns_analysis(dns_records, zone_transfer, cache_poisoning, hostname)
            analysis_results['dns'] = True
            print(f"{Fore.GREEN}[3/4] Comprehensive DNS Intelligence... [Completed]")
        else:
            print(f"{Fore.YELLOW}[3/4] Comprehensive DNS Intelligence... [Failed: No DNS data available]")
    else:
        print(f"\n{Fore.YELLOW}[3/4] Comprehensive DNS Intelligence... [Skipped: Target is IP address only]")
    
    # 4. Network Discovery
    print(f"\n{Fore.MAGENTA}[4/4] Network Discovery... {Fore.CYAN}[Starting]")
    os_fingerprint, _ = detect_os_fingerprint(ip_address)
    services, _ = detect_service_versions(ip_address)
    
    if os_fingerprint or services:
        display_network_discovery(None, os_fingerprint, services, ip_address)
        analysis_results['network_discovery'] = True
        print(f"{Fore.GREEN}[4/4] Network Discovery... [Completed]")
    else:
        print(f"{Fore.YELLOW}[4/4] Network Discovery... [Limited: Partial data available]")
    
    # Summary
    duration = time.time() - start_time
    completed = len(analysis_results)
    
    print(f"\n{Fore.GREEN}╔═══════════════════════════════════════════════════════════╗")
    print(f"{Fore.GREEN}║ {Fore.CYAN}Complete Intelligence Analysis Summary{Fore.GREEN}")
    print(f"{Fore.GREEN}╚═══════════════════════════════════════════════════════════╝")
    print(f"{Fore.CYAN}Target:           {Fore.WHITE}{target}")
    print(f"{Fore.CYAN}Analysis Time:    {Fore.WHITE}{duration:.2f} seconds")
    print(f"{Fore.CYAN}Modules Completed: {Fore.WHITE}{completed}/4")
    
    # Ask user if they want to export the summary
    while True:
        export_choice = input(f"\n{Fore.YELLOW}Would you like to export this analysis summary? (y/N): ").strip().lower()
        if export_choice in ['y', 'yes']:
            export_intelligence_report(target, duration, completed, analysis_results)
            break
        elif export_choice in ['n', 'no', '']:
            break
        else:
            print(f"{Fore.RED}Please enter 'y' or 'n'")
    
    # Log the complete analysis
    log_tool_usage("enhanced_tracker", {
        "analysis_type": "complete_intelligence",
        "target": target,
        "resolved_ip": ip_address if not validate_ip(target) else None,
        "duration": round(duration, 2),
        "modules_completed": completed,
        "analysis_results": analysis_results
    })

if __name__ == "__main__":
    main()
