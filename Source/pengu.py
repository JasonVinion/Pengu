#!/usr/bin/env python3
"""
Pengu - Advanced Network Security Multi-Tool
Optimized version with automatic dependency management
"""

import sys
import os
import time
import subprocess
import importlib.util

# Try to import colorama, install if not available
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("Installing required dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
    from colorama import init, Fore, Style
    init(autoreset=True)

# Required dependencies with their pip names
REQUIRED_DEPENDENCIES = {
    'requests': 'requests',
    'dns.resolver': 'dnspython',
    'scapy': 'scapy',
}

def check_and_install_dependencies():
    """Check for required dependencies and install if missing"""
    missing_deps = []
    
    for module_name, pip_name in REQUIRED_DEPENDENCIES.items():
        try:
            if '.' in module_name:
                # Handle submodules like dns.resolver
                parent_module = module_name.split('.')[0]
                spec = importlib.util.find_spec(parent_module)
            else:
                spec = importlib.util.find_spec(module_name)
            
            if spec is None:
                missing_deps.append(pip_name)
        except ImportError:
            missing_deps.append(pip_name)
    
    if missing_deps:
        print(f"{Fore.YELLOW}Installing missing dependencies: {', '.join(missing_deps)}")
        for dep in missing_deps:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"{Fore.GREEN}✓ Installed {dep}")
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}✗ Failed to install {dep}")
                print(f"{Fore.YELLOW}Please install manually: pip install {dep}")

# Check dependencies on startup
check_and_install_dependencies()

# Import the tool modules
def import_tools():
    """Import tool modules with error handling"""
    tools = {}
    
    try:
        from . import port_scanner
        tools['port_scanner'] = port_scanner
    except ImportError:
        # Handle relative import in standalone execution
        import port_scanner
        tools['port_scanner'] = port_scanner
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import port_scanner: {e}")
    
    try:
        from . import subdomain
        tools['subdomain'] = subdomain
    except ImportError:
        import subdomain
        tools['subdomain'] = subdomain
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import subdomain: {e}")
    
    try:
        from . import whois
        tools['whois'] = whois  
    except ImportError:
        import whois
        tools['whois'] = whois
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import whois: {e}")
        
    try:
        from . import traceroute
        tools['traceroute'] = traceroute
    except ImportError:
        import traceroute  
        tools['traceroute'] = traceroute
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import traceroute: {e}")
    
    try:
        from . import enhanced_ping
        tools['enhanced_ping'] = enhanced_ping
    except ImportError:
        import enhanced_ping
        tools['enhanced_ping'] = enhanced_ping
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import enhanced_ping: {e}")
    
    try:
        from . import system_specs
        tools['system_specs'] = system_specs
    except ImportError:
        import system_specs
        tools['system_specs'] = system_specs
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import system_specs: {e}")
    
    try:
        from . import admin_utils
        tools['admin_utils'] = admin_utils
    except ImportError:
        import admin_utils
        tools['admin_utils'] = admin_utils
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import admin_utils: {e}")
    
    try:
        from . import proxy_checker
        tools['proxy_checker'] = proxy_checker
    except ImportError:
        import proxy_checker
        tools['proxy_checker'] = proxy_checker
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import proxy_checker: {e}")
    
    # Import new modules
    try:
        from . import session_logger
        tools['session_logger'] = session_logger
    except ImportError:
        import session_logger
        tools['session_logger'] = session_logger
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import session_logger: {e}")
    
    try:
        from . import terms_of_service
        tools['terms_of_service'] = terms_of_service
    except ImportError:
        import terms_of_service
        tools['terms_of_service'] = terms_of_service
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import terms_of_service: {e}")
    
    try:
        from . import encoding_utils
        tools['encoding_utils'] = encoding_utils
    except ImportError:
        import encoding_utils
        tools['encoding_utils'] = encoding_utils
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import encoding_utils: {e}")
    
    try:
        from . import proxy_manager
        tools['proxy_manager'] = proxy_manager
    except ImportError:
        import proxy_manager
        tools['proxy_manager'] = proxy_manager
    except Exception as e:
        print(f"{Fore.RED}Warning: Could not import proxy_manager: {e}")
    
    return tools

# ASCII Art Banner (will be generated dynamically)
def get_title_ascii(tools=None):
    """Generate title ASCII with admin warning box"""
    base_ascii = f"""
{Fore.CYAN}                                ########  ######## ##    ##  ######   ##     ## 
{Fore.CYAN}                                ##     ## ##       ###   ## ##    ##  ##     ## 
{Fore.CYAN}                                ##     ## ##       ####  ## ##        ##     ## 
{Fore.CYAN}                                ########  ######   ## ## ## ##   #### ##     ## 
{Fore.CYAN}                                ##        ##       ##  #### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ##       ##   ### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ######## ##    ##  ######    #######  
{Fore.YELLOW}                           Welcome to Pengu!
{Fore.GREEN}                              Enhanced Python Version v2.1
"""
    
    # Get admin warning box if tools are available
    if tools and 'admin_utils' in tools:
        return base_ascii + tools['admin_utils'].get_admin_warning_box()
    else:
        # Fallback - check admin status directly
        try:
            import admin_utils
            return base_ascii + admin_utils.get_admin_warning_box()
        except:
            return base_ascii + f"\n{Fore.YELLOW}Type 'help' to get started.\n"

def get_help_menu(tools=None):
    """Generate help menu with conditional admin warnings"""
    # Check admin status
    is_admin = False
    if tools and 'admin_utils' in tools:
        is_admin = tools['admin_utils'].is_admin()
    else:
        try:
            import admin_utils
            is_admin = admin_utils.is_admin()
        except:
            pass
    
    # Conditional warning for traceroute
    traceroute_warning = "" if is_admin else f" {Fore.YELLOW}⚠"
    
    return f"""
{Fore.MAGENTA} ╔════════════════════════════════════════════════════════╗
{Fore.MAGENTA} ║ {Fore.CYAN}Project Pengu Multi-Tool - Enhanced Edition{Fore.MAGENTA}           ║
{Fore.MAGENTA} ╠════════════════════════════════════════════════════════╣
{Fore.MAGENTA} ║ {Fore.GREEN}help       {Fore.WHITE}. Show this help menu{Fore.MAGENTA}                        ║
{Fore.MAGENTA} ║ {Fore.GREEN}home       {Fore.WHITE}. Return to home screen{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}ping       {Fore.WHITE}. Enhanced ICMP Ping utility{Fore.MAGENTA}                ║
{Fore.MAGENTA} ║ {Fore.GREEN}tcp        {Fore.WHITE}. TCP Port connectivity test{Fore.MAGENTA}                ║
{Fore.MAGENTA} ║ {Fore.GREEN}http       {Fore.WHITE}. HTTP/HTTPS connectivity test{Fore.MAGENTA}              ║
{Fore.MAGENTA} ║ {Fore.GREEN}port       {Fore.WHITE}. Advanced port scanner{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}subdomain  {Fore.WHITE}. Multi-threaded subdomain finder{Fore.MAGENTA}           ║
{Fore.MAGENTA} ║ {Fore.GREEN}intel      {Fore.WHITE}. Network Intelligence (SSL•DNS•ARP•OS){Fore.MAGENTA}     ║
{Fore.MAGENTA} ║ {Fore.GREEN}traceroute {Fore.WHITE}. Network path tracer{traceroute_warning}{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}proxy      {Fore.WHITE}. Multi-protocol proxy checker{Fore.MAGENTA}              ║
{Fore.MAGENTA} ║ {Fore.GREEN}proxymode  {Fore.WHITE}. Setup universal proxy mode{Fore.MAGENTA}               ║
{Fore.MAGENTA} ║ {Fore.GREEN}encode     {Fore.WHITE}. Encoding/Decoding utilities{Fore.MAGENTA}              ║
{Fore.MAGENTA} ║ {Fore.GREEN}specs      {Fore.WHITE}. System hardware information{Fore.MAGENTA}               ║
{Fore.MAGENTA} ║ {Fore.GREEN}enable_logging {Fore.WHITE}. Enable session logging{Fore.MAGENTA}               ║
{Fore.MAGENTA} ║ {Fore.GREEN}savelog    {Fore.WHITE}. Save session log to file{Fore.MAGENTA}                  ║
{Fore.MAGENTA} ║ {Fore.GREEN}tos        {Fore.WHITE}. Terms of service & disclaimer{Fore.MAGENTA}             ║
{Fore.MAGENTA} ║ {Fore.GREEN}credit     {Fore.WHITE}. Show credits{Fore.MAGENTA}                               ║
{Fore.MAGENTA} ║ {Fore.GREEN}exit       {Fore.WHITE}. Exit to quit{Fore.MAGENTA}                              ║
{Fore.MAGENTA} ╚════════════════════════════════════════════════════════╝
"""

def clear_screen():
    """Clear screen in a cross-platform way"""
    os.system('cls' if os.name == 'nt' else 'clear')

def create_output_directories():
    """Create dedicated output directories (Issue 4)"""
    try:
        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_output_dir = os.path.join(script_dir, "pengu_output")
        
        # Create subdirectories
        directories = [
            base_output_dir,
            os.path.join(base_output_dir, "reports"),
            os.path.join(base_output_dir, "logs"),
            os.path.join(base_output_dir, "exports")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
        return base_output_dir
    except Exception as e:
        print(f"{Fore.YELLOW}Warning: Could not create output directories: {e}")
        return os.path.dirname(os.path.abspath(__file__))  # Fallback to script directory

def get_output_path(subfolder="", filename=""):
    """Get the path for output files in the appropriate subdirectory"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.join(script_dir, "pengu_output")
        
        if subfolder:
            output_dir = os.path.join(base_dir, subfolder)
        else:
            output_dir = base_dir
            
        if filename:
            return os.path.join(output_dir, filename)
        else:
            return output_dir
    except:
        # Fallback to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if filename:
            return os.path.join(script_dir, filename)
        else:
            return script_dir

def safe_write_file(filepath, content, mode='w'):
    """Write file with UTF-8 encoding to fix Issue 16"""
    try:
        with open(filepath, mode, encoding='utf-8', errors='replace') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"{Fore.RED}Error writing file {filepath}: {e}")
        return False

def safe_read_file(filepath, mode='r'):
    """Read file with UTF-8 encoding"""
    try:
        with open(filepath, mode, encoding='utf-8', errors='replace') as f:
            return f.read()
    except Exception as e:
        print(f"{Fore.RED}Error reading file {filepath}: {e}")
        return None

def return_to_home(tools=None):
    """Clear screen and show banner"""
    clear_screen()
    print(get_title_ascii(tools))

def return_to_main_menu(tools=None):
    """Standardized function to return to main menu (Issues 7 & 9)"""
    return_to_home(tools)

# Ping implementations
def icmp_ping():
    """ICMP ping implementation - deprecated, use enhanced_ping instead"""
    print(f"{Fore.YELLOW}Please use the 'ping' command for enhanced ICMP ping functionality")

def export_tcp_ping_results(hostname, port, total_attempts, successful_connections, failed_connections, avg_time, min_time, max_time):
    """Export TCP ping results to file"""
    try:
        from datetime import datetime
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hostname_safe = hostname.replace(':', '_').replace('.', '_').replace('/', '_')
        filename = f"tcp_ping_report_{hostname_safe}_{port}_{timestamp}.txt"
        
        success_rate = (successful_connections/total_attempts*100) if total_attempts > 0 else 0
        
        report_content = f"""PENGU TCP PING REPORT
{'=' * 50}

Target:              {hostname}:{port}
Test Date:           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test Type:           TCP Connectivity Test

CONNECTION STATISTICS
{'-' * 30}
Total Attempts:      {total_attempts}
Successful:          {successful_connections}
Failed:              {failed_connections}
Success Rate:        {success_rate:.1f}%

RESPONSE TIME STATISTICS
{'-' * 30}
Average:             {avg_time:.2f}ms
Minimum:             {min_time:.2f}ms
Maximum:             {max_time:.2f}ms

Report generated by Pengu v2.1
"""
        
        with open(filename, 'w') as f:
            f.write(report_content)
        
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, filename)
        print(f"{Fore.GREEN}✓ TCP ping report exported to: {full_path}")
        return filename
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting TCP ping report: {e}")
        return None

def export_http_ping_results(url, total_requests, successful_requests, failed_requests, avg_time, min_time, max_time, status_codes):
    """Export HTTP ping results to file"""
    try:
        from datetime import datetime
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        url_safe = url.replace('://', '_').replace('/', '_').replace('.', '_').replace(':', '_')
        filename = f"http_ping_report_{url_safe}_{timestamp}.txt"
        
        success_rate = (successful_requests/total_requests*100) if total_requests > 0 else 0
        
        report_content = f"""PENGU HTTP PING REPORT
{'=' * 50}

Target:              {url}
Test Date:           {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Test Type:           HTTP/HTTPS Connectivity Test

REQUEST STATISTICS
{'-' * 30}
Total Requests:      {total_requests}
Successful:          {successful_requests}
Failed:              {failed_requests}
Success Rate:        {success_rate:.1f}%

RESPONSE TIME STATISTICS
{'-' * 30}
Average:             {avg_time:.2f}ms
Minimum:             {min_time:.2f}ms
Maximum:             {max_time:.2f}ms

STATUS CODES
{'-' * 15}
"""
        
        for status_code, count in status_codes.items():
            report_content += f"{status_code}: {count}\n"
        
        report_content += "\nReport generated by Pengu v2.1\n"
        
        with open(filename, 'w') as f:
            f.write(report_content)
        
        current_dir = os.getcwd()
        full_path = os.path.join(current_dir, filename)
        print(f"{Fore.GREEN}✓ HTTP ping report exported to: {full_path}")
        return filename
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting HTTP ping report: {e}")
        return None

def tcp_ping():
    """TCP port connectivity test with stats and improved exit"""
    import socket
    import time
    import statistics
    
    while True:  # Main loop to restart TCP ping
        try:
            hostname = input(f"{Fore.YELLOW}Enter hostname/IP: ").strip()
            port = int(input(f"{Fore.YELLOW}Enter port: "))
            
            print(f"{Fore.CYAN}Testing TCP connectivity to {hostname}:{port}")
            print(f"{Fore.GREEN}Press 'q' to stop")
            
            # Statistics tracking
            response_times = []
            successful_connections = 0
            failed_connections = 0
            total_attempts = 0
            
            # Setup for non-blocking input
            stop_tcp_ping = False
            
            def check_for_q_tcp():
                nonlocal stop_tcp_ping
                if os.name == 'nt':  # Windows
                    import msvcrt
                    while not stop_tcp_ping:
                        try:
                            if msvcrt.kbhit():
                                key = msvcrt.getch().decode('utf-8').lower()
                                if key == 'q':
                                    stop_tcp_ping = True
                                    break
                        except:
                            pass
                        time.sleep(0.1)
                else:  # Linux/Unix
                    try:
                        import select
                        import termios
                        import tty
                        
                        if not sys.stdin.isatty():
                            return
                        
                        old_settings = termios.tcgetattr(sys.stdin)
                        try:
                            tty.setraw(sys.stdin.fileno())
                            while not stop_tcp_ping:
                                if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                                    key = sys.stdin.read(1).lower()
                                    if key == 'q':
                                        stop_tcp_ping = True
                                        break
                        finally:
                            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                    except Exception:
                        pass
            
            # Start key monitoring thread
            import threading
            key_thread = threading.Thread(target=check_for_q_tcp, daemon=True)
            key_thread.start()
            
            try:
                while not stop_tcp_ping:
                    start_time = time.time()
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)
                    result = sock.connect_ex((hostname, port))
                    end_time = time.time()
                    sock.close()
                    
                    total_attempts += 1
                    
                    if result == 0:
                        response_time = (end_time - start_time) * 1000
                        response_times.append(response_time)
                        successful_connections += 1
                        print(f"{Fore.GREEN}✓ Connection succeeded to {hostname}:{port} "
                              f"(Response Time: {response_time:.2f}ms)")
                    else:
                        failed_connections += 1
                        print(f"{Fore.RED}✗ Connection failed to {hostname}:{port}")
                    
                    # Short sleep but allow checking for 'q' key
                    for _ in range(10):  # 1 second total, checked in 0.1s intervals
                        if stop_tcp_ping:
                            break
                        time.sleep(0.1)
                    
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}TCP ping stopped")
            
            # Stop the key monitoring thread
            stop_tcp_ping = True
            
            # Show statistics
            if response_times:
                avg_time = statistics.mean(response_times)
                min_time = min(response_times)
                max_time = max(response_times)
            else:
                avg_time = min_time = max_time = 0
                
            print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}TCP Ping Statistics{Fore.CYAN}                   ║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝

{Fore.GREEN}Connection Summary:
{Fore.CYAN}  Target:           {Fore.WHITE}{hostname}:{port}
{Fore.CYAN}  Total Attempts:   {Fore.WHITE}{total_attempts}
{Fore.CYAN}  Successful:       {Fore.WHITE}{successful_connections}
{Fore.CYAN}  Failed:           {Fore.WHITE}{failed_connections}
{Fore.CYAN}  Success Rate:     {Fore.WHITE}{(successful_connections/total_attempts*100) if total_attempts > 0 else 0:.1f}%

{Fore.GREEN}Response Times:
{Fore.CYAN}  Average:          {Fore.WHITE}{avg_time:.2f}ms
{Fore.CYAN}  Minimum:          {Fore.WHITE}{min_time:.2f}ms
{Fore.CYAN}  Maximum:          {Fore.WHITE}{max_time:.2f}ms
""")
            
            # Exit options - use while loop instead of recursion
            while True:
                print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Go back to TCP ping
{Fore.GREEN}2. {Fore.WHITE}Export results to file
{Fore.GREEN}3. {Fore.WHITE}Return to home menu
""")
                
                choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
                
                if choice == '1':
                    break  # Break inner loop to restart TCP ping
                elif choice == '2':
                    export_tcp_ping_results(hostname, port, total_attempts, successful_connections, failed_connections, avg_time, min_time, max_time)
                    # Continue loop to show options again
                elif choice == '3':
                    return  # Exit function completely
                else:
                    print(f"{Fore.RED}Invalid option. Please select 1-3.")
                    
        except ValueError:
            print(f"{Fore.RED}Invalid port number")
            continue  # Continue the main loop for new input
        except Exception as e:
            print(f"{Fore.RED}TCP ping error: {e}")
            continue  # Continue the main loop for new input

def http_ping():
    """HTTP/HTTPS connectivity test with stats and improved exit"""
    try:
        import requests
        import time
        import statistics
        
        while True:  # Main loop to restart HTTP ping
            try:
                url = input(f"{Fore.YELLOW}Enter URL (e.g., https://example.com): ").strip()
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                    
                print(f"{Fore.CYAN}Testing HTTP(S) connectivity to {url}")
                print(f"{Fore.GREEN}Press 'q' to stop")
                
                # Statistics tracking
                response_times = []
                successful_requests = 0
                failed_requests = 0
                total_requests = 0
                status_codes = {}
                
                # Check if proxy mode is enabled
                proxies = None
                try:
                    from proxy_manager import get_proxy_for_requests
                    proxies = get_proxy_for_requests()
                    if proxies:
                        print(f"{Fore.YELLOW}Using proxy for HTTP ping...")
                except ImportError:
                    pass  # Proxy manager not available
                except Exception:
                    pass  # No proxy configured
                
                # Setup for non-blocking input
                stop_http_ping = False
                
                def check_for_q_http():
                    nonlocal stop_http_ping
                    if os.name == 'nt':  # Windows
                        import msvcrt
                        while not stop_http_ping:
                            try:
                                if msvcrt.kbhit():
                                    key = msvcrt.getch().decode('utf-8').lower()
                                    if key == 'q':
                                        stop_http_ping = True
                                        break
                            except:
                                pass
                            time.sleep(0.1)
                    else:  # Linux/Unix
                        try:
                            import select
                            import termios
                            import tty
                            
                            if not sys.stdin.isatty():
                                return
                            
                            old_settings = termios.tcgetattr(sys.stdin)
                            try:
                                tty.setraw(sys.stdin.fileno())
                                while not stop_http_ping:
                                    if select.select([sys.stdin], [], [], 0.1) == ([sys.stdin], [], []):
                                        key = sys.stdin.read(1).lower()
                                        if key == 'q':
                                            stop_http_ping = True
                                            break
                            finally:
                                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
                        except Exception:
                            pass
                
                # Start key monitoring thread
                import threading
                key_thread = threading.Thread(target=check_for_q_http, daemon=True)
                key_thread.start()
                
                try:
                    while not stop_http_ping:
                        start_time = time.time()
                        try:
                            response = requests.get(url, timeout=5, proxies=proxies)
                            end_time = time.time()
                            
                            total_requests += 1
                            response_time = (end_time - start_time) * 1000
                            response_times.append(response_time)
                            
                            # Track status codes
                            status_code = response.status_code
                            status_codes[status_code] = status_codes.get(status_code, 0) + 1
                            
                            if response.status_code == 200:
                                successful_requests += 1
                                print(f"{Fore.GREEN}✓ HTTP(S) connection succeeded to {url} "
                                      f"(Response Time: {response_time:.2f}ms, Status: {response.status_code})")
                            else:
                                failed_requests += 1
                                print(f"{Fore.YELLOW}⚠ HTTP(S) connection returned status {response.status_code} "
                                      f"(Response Time: {response_time:.2f}ms)")
                                
                        except requests.RequestException as e:
                            total_requests += 1
                            failed_requests += 1
                            print(f"{Fore.RED}✗ Connection failed: {e}")
                        
                        # Short sleep but allow checking for 'q' key
                        for _ in range(10):  # 1 second total, checked in 0.1s intervals
                            if stop_http_ping:
                                break
                            time.sleep(0.1)
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}HTTP ping stopped")
                
                # Stop the key monitoring thread
                stop_http_ping = True
                
                # Show statistics
                if response_times:
                    avg_time = statistics.mean(response_times)
                    min_time = min(response_times)
                    max_time = max(response_times)
                else:
                    avg_time = min_time = max_time = 0
                    
                print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}HTTP Ping Statistics{Fore.CYAN}                  ║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝

{Fore.GREEN}Request Summary:
{Fore.CYAN}  Target:           {Fore.WHITE}{url}
{Fore.CYAN}  Total Requests:   {Fore.WHITE}{total_requests}
{Fore.CYAN}  Successful:       {Fore.WHITE}{successful_requests}
{Fore.CYAN}  Failed:           {Fore.WHITE}{failed_requests}
{Fore.CYAN}  Success Rate:     {Fore.WHITE}{(successful_requests/total_requests*100) if total_requests > 0 else 0:.1f}%

{Fore.GREEN}Response Times:
{Fore.CYAN}  Average:          {Fore.WHITE}{avg_time:.2f}ms
{Fore.CYAN}  Minimum:          {Fore.WHITE}{min_time:.2f}ms
{Fore.CYAN}  Maximum:          {Fore.WHITE}{max_time:.2f}ms

{Fore.GREEN}Status Codes:""")
                
                for status_code, count in status_codes.items():
                    print(f"{Fore.CYAN}  {status_code}:              {Fore.WHITE}{count}")
                
                # Exit options - use while loop instead of recursion
                while True:
                    print(f"""
{Fore.YELLOW}What would you like to do next?
{Fore.GREEN}1. {Fore.WHITE}Go back to HTTP ping
{Fore.GREEN}2. {Fore.WHITE}Export results to file
{Fore.GREEN}3. {Fore.WHITE}Return to home menu
""")
                    
                    choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
                    
                    if choice == '1':
                        break  # Break inner loop to restart HTTP ping
                    elif choice == '2':
                        export_http_ping_results(url, total_requests, successful_requests, failed_requests, avg_time, min_time, max_time, status_codes)
                        # Continue loop to show options again
                    elif choice == '3':
                        return  # Exit function completely
                    else:
                        print(f"{Fore.RED}Invalid option. Please select 1-3.")
                        
            except Exception as e:
                print(f"{Fore.RED}HTTP ping error: {e}")
                continue  # Continue the main loop for new input
                
    except ImportError:
        print(f"{Fore.RED}Requests module not available for HTTP ping")

def run_tool(tool_name, tools):
    """Run a specific tool module"""
    if tool_name in tools:
        try:
            # Call the main function of the tool
            if hasattr(tools[tool_name], 'main'):
                tools[tool_name].main()
            else:
                print(f"{Fore.YELLOW}Tool {tool_name} doesn't have a main function")
        except Exception as e:
            print(f"{Fore.RED}Error running {tool_name}: {e}")
    else:
        print(f"{Fore.RED}Tool {tool_name} not available")

def user_inputs():
    """Main user input loop with optimized tool integration"""
    # Import tools once at startup
    tools = import_tools()
    
    # Session logging is now disabled by default per security requirements
    # Users must explicitly enable it with the 'enable_logging' command
    
    commands = {
        "help": lambda: print(get_help_menu(tools)),
        "home": lambda: return_to_home(tools),
        "ping": lambda: run_tool('enhanced_ping', tools),
        "http": http_ping,
        "tcp": tcp_ping,
        "intel": lambda: run_tool('whois', tools),  # Enhanced intelligence module
        "port": lambda: run_tool('port_scanner', tools),
        "traceroute": lambda: run_traceroute_with_admin_check(tools),
        "subdomain": lambda: run_tool('subdomain', tools),
        "proxy": lambda: run_tool('proxy_checker', tools),
        "proxymode": lambda: setup_proxy_mode(tools),
        "encode": lambda: run_tool('encoding_utils', tools),
        "specs": lambda: run_tool('system_specs', tools),
        "enable_logging": lambda: enable_session_logging(tools),
        "savelog": lambda: save_session_log(tools),
        "tos": lambda: run_tool('terms_of_service', tools),
        "credit": lambda: print(f"""
{Fore.GREEN} ╔════════════════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Pengu Multi-Tool Credits{Fore.GREEN}                   ║
{Fore.GREEN} ║ {Fore.CYAN}Enhanced Python Version v2.1{Fore.GREEN}              ║
{Fore.GREEN} ║ {Fore.MAGENTA}GitHub: https://github.com/JasonVinion{Fore.GREEN}    ║
{Fore.GREEN} ║ {Fore.YELLOW}Enhanced with comprehensive features{Fore.GREEN}      ║
{Fore.GREEN} ╚════════════════════════════════════════╝
                  """)
    }

    while True:
        try:
            userinput = input(f"{Fore.GREEN}Pengu{Fore.WHITE}@{Fore.CYAN}Terminal{Fore.GREEN} >>> {Fore.MAGENTA}").strip().lower()
            
            if userinput in commands:
                commands[userinput]()
            elif userinput in ["exit", "quit"]:
                # Finalize session before exit
                try:
                    if 'session_logger' in tools:
                        logger = tools['session_logger'].get_session_logger()
                        logger.finalize_session()
                        print(f"{Fore.CYAN}Session log saved to: {logger.temp_log_file}")
                except:
                    pass
                print(f"{Fore.GREEN}Thanks for using Pengu! Goodbye...")
                time.sleep(1)
                break
            elif userinput == "":
                continue  # Empty input, just continue
            else:
                print(f"{Fore.RED}Unknown command: {userinput}")
                print(f"{Fore.YELLOW}Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Use 'exit' to quit Pengu")
        except EOFError:
            print(f"\n{Fore.GREEN}Goodbye!")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

def setup_proxy_mode(tools):
    """Setup universal proxy mode"""
    if 'proxy_manager' in tools:
        tools['proxy_manager'].setup_proxy_mode()
    else:
        print(f"{Fore.RED}Proxy manager not available")

def enable_session_logging(tools):
    """Enable session logging (disabled by default for security)"""
    if 'session_logger' in tools:
        try:
            logger = tools['session_logger'].get_session_logger()
            print(f"{Fore.GREEN}✓ Session logging enabled")
            print(f"{Fore.CYAN}Session log will be saved to: {logger.temp_log_file}")
        except Exception as e:
            print(f"{Fore.RED}Failed to enable session logging: {e}")
    else:
        print(f"{Fore.RED}Session logger not available")

def save_session_log(tools):
    """Save session log to file"""
    if 'session_logger' in tools:
        tools['session_logger'].show_save_log_menu()
    else:
        print(f"{Fore.RED}Session logger not available")

def run_traceroute_with_admin_check(tools):
    """Run traceroute with admin rights check"""
    if 'admin_utils' in tools:
        result = tools['admin_utils'].check_admin_for_tool('traceroute')
        if result is None:  # User chose to return to main menu
            return
        elif not result:  # Continuing without admin
            print(f"{Fore.YELLOW}Running traceroute with limited functionality...")
    
    run_tool('traceroute', tools)

def main():
    """Main entry point"""
    # Import tools (no hardware scan on startup)
    tools = import_tools()
    
    # Create output directories (Issue 4)
    create_output_directories()
    
    print(get_title_ascii(tools))
    
    # Display initial Terms of Service notification (Issue 2)
    print(f"{Fore.YELLOW}By using this tool, you agree to the Terms of Service.")
    print(f"{Fore.YELLOW}For more information, please enter the 'tos' command.\n")
    
    user_inputs()

if __name__ == "__main__":
    main()
