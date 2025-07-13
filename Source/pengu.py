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
    
    return tools

# ASCII Art Banner
title_ascii = f"""
{Fore.CYAN}                                ########  ######## ##    ##  ######   ##     ## 
{Fore.CYAN}                                ##     ## ##       ###   ## ##    ##  ##     ## 
{Fore.CYAN}                                ##     ## ##       ####  ## ##        ##     ## 
{Fore.CYAN}                                ########  ######   ## ## ## ##   #### ##     ## 
{Fore.CYAN}                                ##        ##       ##  #### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ##       ##   ### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ######## ##    ##  ######    #######  
{Fore.YELLOW}                           Welcome to Pengu! Type 'help' to get started.
{Fore.GREEN}                              Optimized Python Version v2.0
"""

help_menu = f"""
{Fore.MAGENTA} ╔════════════════════════════════════════════════════════╗
{Fore.MAGENTA} ║ {Fore.CYAN}Project Pengu Multi-Tool - Optimized Edition{Fore.MAGENTA}           ║
{Fore.MAGENTA} ╠════════════════════════════════════════════════════════╣
{Fore.MAGENTA} ║ {Fore.GREEN}help       {Fore.WHITE}. Show this help menu{Fore.MAGENTA}                        ║
{Fore.MAGENTA} ║ {Fore.GREEN}home       {Fore.WHITE}. Return to home screen{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}ping       {Fore.WHITE}. Enhanced ICMP Ping utility{Fore.MAGENTA}                ║
{Fore.MAGENTA} ║ {Fore.GREEN}tcp        {Fore.WHITE}. TCP Port connectivity test{Fore.MAGENTA}                ║
{Fore.MAGENTA} ║ {Fore.GREEN}http       {Fore.WHITE}. HTTP/HTTPS connectivity test{Fore.MAGENTA}              ║
{Fore.MAGENTA} ║ {Fore.GREEN}port       {Fore.WHITE}. Advanced port scanner{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}subdomain  {Fore.WHITE}. Multi-threaded subdomain finder{Fore.MAGENTA}           ║
{Fore.MAGENTA} ║ {Fore.GREEN}tracker    {Fore.WHITE}. GeoIP & WHOIS lookup{Fore.MAGENTA}                      ║
{Fore.MAGENTA} ║ {Fore.GREEN}traceroute {Fore.WHITE}. Network path tracer {Fore.YELLOW}⚠{Fore.MAGENTA}                     ║
{Fore.MAGENTA} ║ {Fore.GREEN}proxy      {Fore.WHITE}. Multi-protocol proxy checker{Fore.MAGENTA}              ║
{Fore.MAGENTA} ║ {Fore.GREEN}specs      {Fore.WHITE}. System hardware information{Fore.MAGENTA}               ║
{Fore.MAGENTA} ║ {Fore.GREEN}credit     {Fore.WHITE}. Show credits{Fore.MAGENTA}                               ║
{Fore.MAGENTA} ║ {Fore.GREEN}exit       {Fore.WHITE}. Return to main menu{Fore.MAGENTA}                       ║
{Fore.MAGENTA} ╚════════════════════════════════════════════════════════╝
"""

def clear_screen():
    """Clear screen in a cross-platform way"""
    os.system('cls' if os.name == 'nt' else 'clear')

def return_to_home():
    """Clear screen and show banner"""
    clear_screen()
    print(title_ascii)

# Ping implementations
def icmp_ping():
    """ICMP ping implementation"""
    try:
        import subprocess
        while True:
            hostname = input(f"{Fore.YELLOW}Enter hostname/IP to ping (or 'exit'): ").strip()
            if hostname.lower() == 'exit':
                break
            
            if not hostname:
                print(f"{Fore.RED}Please enter a valid hostname/IP")
                continue
                
            print(f"{Fore.CYAN}Pinging {hostname}...")
            
            try:
                # Use system ping command
                if os.name == 'nt':  # Windows
                    result = subprocess.run(['ping', '-t', hostname], 
                                          capture_output=False, text=True)
                else:  # Linux/Unix
                    result = subprocess.run(['ping', hostname], 
                                          capture_output=False, text=True)
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Ping stopped by user")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
                
    except Exception as e:
        print(f"{Fore.RED}ICMP ping error: {e}")

def tcp_ping():
    """TCP port connectivity test"""
    import socket
    import time
    
    try:
        hostname = input(f"{Fore.YELLOW}Enter hostname/IP: ").strip()
        port = int(input(f"{Fore.YELLOW}Enter port: "))
        
        print(f"{Fore.CYAN}Testing TCP connectivity to {hostname}:{port}")
        print(f"{Fore.GREEN}Press Ctrl+C to stop")
        
        while True:
            try:
                start_time = time.time()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((hostname, port))
                end_time = time.time()
                sock.close()
                
                if result == 0:
                    response_time = (end_time - start_time) * 1000
                    print(f"{Fore.GREEN}Connection succeeded to {hostname}:{port} "
                          f"(Response Time: {response_time:.2f}ms)")
                else:
                    print(f"{Fore.RED}Connection failed to {hostname}:{port}")
                    
                time.sleep(1)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}TCP ping stopped")
                break
            except Exception as e:
                print(f"{Fore.RED}Error: {e}")
                break
                
    except ValueError:
        print(f"{Fore.RED}Invalid port number")
    except Exception as e:
        print(f"{Fore.RED}TCP ping error: {e}")

def http_ping():
    """HTTP/HTTPS connectivity test"""
    try:
        import requests
        import time
        
        url = input(f"{Fore.YELLOW}Enter URL (e.g., https://example.com): ").strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        print(f"{Fore.CYAN}Testing HTTP(S) connectivity to {url}")
        print(f"{Fore.GREEN}Press Ctrl+C to stop")
        
        while True:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=5)
                end_time = time.time()
                
                response_time = (end_time - start_time) * 1000
                if response.status_code == 200:
                    print(f"{Fore.GREEN}HTTP(S) connection succeeded to {url} "
                          f"(Response Time: {response_time:.2f}ms, Status: {response.status_code})")
                else:
                    print(f"{Fore.YELLOW}HTTP(S) connection returned status {response.status_code} "
                          f"(Response Time: {response_time:.2f}ms)")
                    
                time.sleep(1)
                
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}HTTP ping stopped")
                break
            except Exception as e:
                print(f"{Fore.RED}Connection failed: {e}")
                time.sleep(1)
                
    except ImportError:
        print(f"{Fore.RED}Requests module not available for HTTP ping")
    except Exception as e:
        print(f"{Fore.RED}HTTP ping error: {e}")

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
    
    # Show admin status warning if needed
    if 'admin_utils' in tools:
        tools['admin_utils'].show_admin_warning()
    
    commands = {
        "help": lambda: print(help_menu),
        "home": return_to_home,
        "ping": lambda: run_tool('enhanced_ping', tools),
        "http": http_ping,
        "tcp": tcp_ping,
        "tracker": lambda: run_tool('whois', tools),
        "port": lambda: run_tool('port_scanner', tools),
        "traceroute": lambda: run_traceroute_with_admin_check(tools),
        "subdomain": lambda: run_tool('subdomain', tools),
        "proxy": lambda: run_tool('proxy_checker', tools),
        "specs": lambda: run_tool('system_specs', tools),
        "credit": lambda: print(f"""
{Fore.GREEN} ╔════════════════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Pengu Multi-Tool Credits{Fore.GREEN}                   ║
{Fore.GREEN} ║ {Fore.CYAN}Optimized Python Version v2.0{Fore.GREEN}             ║
{Fore.GREEN} ║ {Fore.MAGENTA}GitHub: https://github.com/JasonVinion{Fore.GREEN}    ║
{Fore.GREEN} ║ {Fore.YELLOW}Enhanced with auto-dependency management{Fore.GREEN}  ║
{Fore.GREEN} ╚════════════════════════════════════════╝
                  """)
    }

    while True:
        try:
            # Show admin status in prompt
            admin_indicator = ""
            if 'admin_utils' in tools:
                admin_indicator = tools['admin_utils'].get_admin_status_indicator()
            
            userinput = input(f"{admin_indicator} {Fore.GREEN}Pengu{Fore.WHITE}@{Fore.CYAN}Terminal{Fore.GREEN} >>> {Fore.BLUE}").strip().lower()
            
            if userinput in commands:
                commands[userinput]()
            elif userinput == "exit":
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
    # Import tools and start background hardware scan
    tools = import_tools()
    
    # Start background hardware scan if system_specs is available
    if 'system_specs' in tools:
        import threading
        scan_thread = threading.Thread(target=tools['system_specs'].system_specs.scan_hardware, daemon=True)
        scan_thread.start()
    
    print(title_ascii)
    user_inputs()

if __name__ == "__main__":
    main()
