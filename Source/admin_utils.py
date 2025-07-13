#!/usr/bin/env python3
"""
Pengu Admin Rights Detection Module
"""

import os
import sys
import ctypes
import subprocess
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def is_admin():
    """Check if the current process has administrator privileges"""
    try:
        if os.name == 'nt':  # Windows
            return ctypes.windll.shell32.IsUserAnAdmin()
        else:  # Linux/Unix
            return os.geteuid() == 0
    except:
        return False

def request_admin_elevation():
    """Request admin elevation via UAC (Windows) or sudo (Linux)"""
    try:
        if os.name == 'nt':  # Windows
            # Get current script path
            script_path = sys.argv[0]
            
            # Use UAC to elevate
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{script_path}"', 
                None, 
                1
            )
            return True
        else:  # Linux/Unix
            # Use sudo to elevate
            args = ['sudo'] + sys.argv
            subprocess.call(args)
            return True
    except Exception as e:
        print(f"{Fore.RED}Failed to request elevation: {e}")
        return False

def get_admin_warning_box():
    """Get admin warning in a box format similar to help menu"""
    if not is_admin():
        return f"""
{Fore.MAGENTA} ╔════════════════════════════════════════════════════════╗
{Fore.MAGENTA} ║ {Fore.YELLOW}⚠  Admin privileges not detected{Fore.MAGENTA}                      ║
{Fore.MAGENTA} ║ {Fore.WHITE}Features requiring admin will be marked with {Fore.YELLOW}⚠{Fore.MAGENTA}         ║
{Fore.MAGENTA} ╚════════════════════════════════════════════════════════╝

{Fore.YELLOW}Type 'help' to get started.
"""
    return f"""
{Fore.YELLOW}Type 'help' to get started.
"""

def get_admin_status_indicator():
    """Get admin status indicator for UI"""
    if is_admin():
        return f"{Fore.GREEN}[ADMIN]"
    else:
        return f"{Fore.YELLOW}⚠ [NO ADMIN]"

def check_admin_for_tool(tool_name):
    """Check if admin rights are needed for a specific tool and prompt if needed"""
    admin_required_tools = ['traceroute']
    
    if tool_name.lower() in admin_required_tools and not is_admin():
        print(f"""
{Fore.YELLOW}⚠ Administrator privileges required for {tool_name}
{Fore.YELLOW}
{Fore.YELLOW}This tool requires raw socket access which needs admin rights.
{Fore.YELLOW}
{Fore.WHITE}Options:
{Fore.GREEN}1. Request elevation now (will restart application)
{Fore.GREEN}2. Continue without elevation (limited functionality)
{Fore.GREEN}3. Return to main menu
""")
        
        while True:
            choice = input(f"{Fore.CYAN}Select option (1-3): ").strip()
            
            if choice == '1':
                print(f"{Fore.YELLOW}Requesting administrator elevation...")
                if request_admin_elevation():
                    print(f"{Fore.GREEN}Please approve the UAC prompt and restart the application.")
                    sys.exit(0)
                else:
                    print(f"{Fore.RED}Failed to request elevation. Continuing with limited functionality.")
                    return False
            elif choice == '2':
                print(f"{Fore.YELLOW}Continuing with limited functionality...")
                return False
            elif choice == '3':
                return None  # Signal to return to main menu
            else:
                print(f"{Fore.RED}Invalid option. Please select 1-3.")
    
    return True  # Admin not required or already admin

def print_admin_status():
    """Print current admin status"""
    if is_admin():
        print(f"{Fore.GREEN}✓ Running with administrator privileges")
    else:
        print(f"{Fore.YELLOW}⚠ Running without administrator privileges")
        print(f"{Fore.YELLOW}  Some features may be limited")

if __name__ == "__main__":
    print_admin_status()