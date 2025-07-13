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
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Import platform-specific modules
if os.name == 'nt':
    import msvcrt

# Global flag for stopping ping
stop_ping = False

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
        import select
        import termios
        import tty
        
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

def parse_ping_output(line, hostname):
    """Parse ping output and return formatted result with color coding"""
    if "Request timed out" in line or "Destination Host Unreachable" in line:
        return f"{Fore.RED}✗ Request timed out"
    elif "TTL expired" in line:
        return f"{Fore.RED}✗ TTL expired"
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
            
            return f"{color}{status} Reply from {hostname}: time={response_time}ms"
        else:
            return f"{Fore.GREEN}✓ Reply from {hostname}"
    else:
        return None

def enhanced_icmp_ping(hostname):
    """Enhanced ICMP ping with color coding and Q to quit"""
    global stop_ping
    stop_ping = False
    
    print_ping_header(hostname)
    
    # Start countdown
    countdown_timer(3)
    
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
        
        ping_count = 0
        
        while not stop_ping:
            try:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                
                if line.strip():
                    ping_count += 1
                    formatted_output = parse_ping_output(line.strip(), hostname)
                    if formatted_output:
                        timestamp = time.strftime("%H:%M:%S")
                        print(f"[{Fore.CYAN}{timestamp}{Fore.WHITE}] {formatted_output}")
                
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
        
        print(f"\n{Fore.YELLOW}Ping stopped. Sent {ping_count} packets.")
        
    except FileNotFoundError:
        print(f"{Fore.RED}Error: ping command not found on this system")
    except Exception as e:
        print(f"{Fore.RED}Error during ping: {e}")

def enhanced_mass_ping(hostnames):
    """Enhanced mass ping with same features as single ping"""
    global stop_ping
    stop_ping = False
    
    if not hostnames:
        print(f"{Fore.RED}No hostnames provided for mass ping")
        return
    
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
    
    # Start key monitoring thread
    key_thread = threading.Thread(target=check_for_q_key, daemon=True)
    key_thread.start()
    
    # Start ping processes for each hostname
    processes = {}
    ping_counts = {hostname: 0 for hostname in hostnames}
    
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
                        ping_counts[hostname] += 1
                        formatted_output = parse_ping_output(line.strip(), hostname)
                        if formatted_output:
                            timestamp = time.strftime("%H:%M:%S")
                            print(f"[{Fore.CYAN}{timestamp}{Fore.WHITE}] {Fore.MAGENTA}{hostname[:15]:<15}{Fore.WHITE} {formatted_output}")
                    
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
        
        print(f"\n{Fore.YELLOW}Mass ping stopped.")
        for hostname, count in ping_counts.items():
            print(f"{Fore.CYAN}{hostname}: {Fore.WHITE}{count} packets sent")
        
    except Exception as e:
        print(f"{Fore.RED}Error during mass ping: {e}")

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
                    enhanced_icmp_ping(hostname)
                else:
                    print(f"{Fore.RED}Please enter a valid hostname/IP")
                    
            elif choice == '2':
                hostnames_input = input(f"{Fore.YELLOW}Enter hostnames/IPs (comma-separated): ").strip()
                if hostnames_input:
                    hostnames = [h.strip() for h in hostnames_input.split(',') if h.strip()]
                    if hostnames:
                        enhanced_mass_ping(hostnames)
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
        
        input(f"\n{Fore.YELLOW}Press Enter to continue...")

if __name__ == "__main__":
    main()