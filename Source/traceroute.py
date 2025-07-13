#!/usr/bin/env python3
"""
Pengu Traceroute Module - Optimized Network Path Tracer
"""

import os
import sys
import time
import socket
import struct
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the traceroute banner"""
    print(f"""
{Fore.YELLOW} ╔════════════════════════════╗
{Fore.YELLOW} ║ {Fore.BLUE}Project Pengu Traceroute{Fore.YELLOW}   ╚════╗
{Fore.YELLOW} ║ {Fore.GREEN}Optimized Cross-Platform{Fore.YELLOW}        ║
{Fore.YELLOW} ╚═════════════════════════════════╝
""")

def system_traceroute(target):
    """Use system traceroute command as fallback"""
    import subprocess
    
    try:
        if os.name == 'nt':  # Windows
            cmd = ['tracert', target]
        else:  # Linux/Unix
            cmd = ['traceroute', target]
            
        print(f"{Fore.CYAN}Running system traceroute to {target}...")
        subprocess.run(cmd)
        
    except FileNotFoundError:
        print(f"{Fore.RED}System traceroute command not found")
    except Exception as e:
        print(f"{Fore.RED}Error running system traceroute: {e}")

def simple_traceroute(target, max_hops=30):
    """Simple traceroute implementation using TCP connect"""
    print(f"{Fore.CYAN}Simple traceroute to {target} (max {max_hops} hops)")
    print(f"{Fore.YELLOW}Note: This shows connectivity, not actual routing path")
    
    try:
        # Resolve target IP
        target_ip = socket.gethostbyname(target)
        print(f"{Fore.GREEN}Target resolved to: {target_ip}")
        
        # Test connectivity with common ports
        test_ports = [80, 443, 22, 21, 25, 53, 3389, 23]
        
        for hop in range(1, max_hops + 1):
            print(f"{Fore.YELLOW}{hop:2d}: ", end="")
            
            connected = False
            for port in test_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(2)
                    start_time = time.time()
                    result = sock.connect_ex((target_ip, port))
                    end_time = time.time()
                    sock.close()
                    
                    if result == 0:
                        response_time = (end_time - start_time) * 1000
                        print(f"{Fore.GREEN}{target_ip} ({target}) port {port} "
                              f"- {response_time:.2f}ms")
                        connected = True
                        break
                        
                except Exception:
                    continue
            
            if connected:
                print(f"{Fore.GREEN}Reached destination!")
                break
            else:
                print(f"{Fore.RED}No response")
                
            time.sleep(0.5)
            
    except socket.gaierror:
        print(f"{Fore.RED}Could not resolve hostname: {target}")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}")

def advanced_traceroute(target, max_hops=30):
    """Advanced traceroute using raw sockets (requires admin/root)"""
    try:
        from scapy.all import IP, ICMP, sr1
        
        print(f"{Fore.CYAN}Advanced traceroute to {target} using ICMP")
        
        for ttl in range(1, max_hops + 1):
            try:
                pkt = IP(dst=target, ttl=ttl) / ICMP()
                start_time = time.time()
                reply = sr1(pkt, verbose=0, timeout=3)
                end_time = time.time()
                
                if reply is None:
                    print(f"{Fore.YELLOW}{ttl:2d}: {Fore.RED}* * * Request timed out")
                elif reply.type == 0:  # Echo reply (reached destination)
                    response_time = (end_time - start_time) * 1000
                    print(f"{Fore.YELLOW}{ttl:2d}: {Fore.GREEN}{reply.src} - {response_time:.2f}ms (Destination reached)")
                    break
                else:
                    response_time = (end_time - start_time) * 1000
                    try:
                        hostname = socket.gethostbyaddr(reply.src)[0]
                        print(f"{Fore.YELLOW}{ttl:2d}: {Fore.GREEN}{reply.src} ({hostname}) - {response_time:.2f}ms")
                    except:
                        print(f"{Fore.YELLOW}{ttl:2d}: {Fore.GREEN}{reply.src} - {response_time:.2f}ms")
                        
            except Exception as e:
                print(f"{Fore.YELLOW}{ttl:2d}: {Fore.RED}Error: {e}")
                
            time.sleep(0.1)  # Small delay between packets
            
    except ImportError:
        print(f"{Fore.YELLOW}Scapy not available, falling back to system traceroute")
        system_traceroute(target)
    except PermissionError:
        print(f"{Fore.YELLOW}Raw sockets require admin/root privileges")
        print(f"{Fore.YELLOW}Falling back to system traceroute")
        system_traceroute(target)
    except AttributeError as e:
        # Handle the specific L3WinSocket bug
        if "'L3WinSocket' object has no attribute 'ins'" in str(e):
            print(f"{Fore.RED}Known Scapy Windows compatibility issue detected.")
            print(f"{Fore.YELLOW}This is a bug in the Scapy library on Windows.")
            print(f"{Fore.YELLOW}Falling back to system traceroute...")
            system_traceroute(target)
        else:
            print(f"{Fore.RED}Advanced traceroute failed: {e}")
            print(f"{Fore.YELLOW}Falling back to simple traceroute")
            simple_traceroute(target)
    except Exception as e:
        print(f"{Fore.RED}Advanced traceroute failed: {e}")
        print(f"{Fore.YELLOW}Falling back to simple traceroute")
        simple_traceroute(target)

def traceroute():
    """Main traceroute function with multiple fallback options"""
    while True:
        try:
            target = input(f"{Fore.MAGENTA}Enter target IP/hostname (or 'exit'): ").strip()
            if target.lower() == 'exit':
                break
                
            if not target:
                print(f"{Fore.RED}Please enter a valid target")
                continue
            
            print(f"\n{Fore.CYAN}Starting traceroute to {target}...")
            
            # Try advanced method first, then fallback
            try:
                advanced_traceroute(target)
            except Exception as e:
                print(f"{Fore.YELLOW}Advanced traceroute failed, trying alternatives...")
                simple_traceroute(target)
                
            print()  # Empty line for readability
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Traceroute interrupted")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

def main():
    """Main entry point"""
    print_banner()
    traceroute()

if __name__ == "__main__":
    main()
