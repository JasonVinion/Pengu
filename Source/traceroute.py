import os
from scapy.all import *
from colorama import init, Fore, Style

print(f"""
{Fore.YELLOW} ╔════════════════════════════╗
{Fore.YELLOW} ║ {Fore.BLUE}Project Pengu Traceroute{Fore.YELLOW}   ╚════╗
{Fore.YELLOW} ║                                 ║
{Fore.YELLOW} ╚═════════════════════════════════╝
""")

# Initialize colorama
init(autoreset=True)

def traceroute():
    while True:
        ip = input(Fore.MAGENTA + "Enter the IP address to traceroute: ")
        ttl = 1
        max_hops = 30
        timeout = 2

        while ttl <= max_hops:
            pkt = IP(dst=ip, ttl=ttl) / ICMP()
            reply = sr1(pkt, verbose=0, timeout=timeout)

            if reply is None:
                print(f"{Fore.YELLOW}{ttl}: {Fore.RED}No reply")
            elif reply.type == 0:  # Echo reply (ICMP type 0)
                print(f"{Fore.YELLOW}{ttl}: {Fore.GREEN}{reply.src} (Reached destination)")
                break
            else:
                print(f"{Fore.YELLOW}{ttl}: {Fore.GREEN}{reply.src}")

            ttl += 1

if __name__ == "__main__":
    traceroute()
