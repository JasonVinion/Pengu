import requests
from colorama import init, Fore, Style
import os

# Initialize colorama
init(autoreset=True)

message = f"""
{Fore.GREEN} ╔════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Project Pengu Lookup{Fore.GREEN}       ╚════╗
{Fore.GREEN} ║                                 ║
{Fore.GREEN} ╚═════════════════════════════════╝
"""
print(message)

def get_geoip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Unable to fetch GeoIP data for IP {ip}"
    except Exception as e:
        return f"Error: {e}"

def get_whois_info(ip):
    try:
        response = requests.get(f"https://whois.arin.net/rest/ip/{ip}.json")
        if response.status_code == 200:
            return response.json()
        else:
            return f"Error: Unable to fetch Whois data for IP {ip}"
    except Exception as e:
        return f"Error: {e}"

def main():
    while True:
        ip = input("Enter IP address (or 'exit' to quit): ")
        if ip.lower() == 'exit':
            break
        
        print(f"{Fore.YELLOW}Performing lookups for {ip}...\n")
        
        geoip_result = get_geoip_info(ip)
        whois_result = get_whois_info(ip)
        
        if isinstance(geoip_result, str) and geoip_result.startswith("Error"):
            print(f"{Fore.RED}{geoip_result}")
        else:
            print(f"{Fore.GREEN}GeoIP Lookup Result for {ip}:\n")
            print(f"{Fore.CYAN}Hostname: {Fore.WHITE}{geoip_result.get('hostname', 'N/A')}")
            print(f"{Fore.CYAN}City: {Fore.WHITE}{geoip_result.get('city', 'N/A')}")
            print(f"{Fore.CYAN}Region: {Fore.WHITE}{geoip_result.get('region', 'N/A')}")
            print(f"{Fore.CYAN}Country: {Fore.WHITE}{geoip_result.get('country', 'N/A')}")
            print(f"{Fore.CYAN}Location: {Fore.WHITE}{geoip_result.get('loc', 'N/A')}")
            print(f"{Fore.CYAN}ISP: {Fore.WHITE}{geoip_result.get('org', 'N/A')}")
            print(f"{Fore.CYAN}Postal: {Fore.WHITE}{geoip_result.get('postal', 'N/A')}")
        
        if isinstance(whois_result, str) and whois_result.startswith("Error"):
            print(f"{Fore.RED}{whois_result}")
        else:
            print(f"{Fore.GREEN}\nWhois Lookup Result for {ip}:\n")
            whois_net = whois_result.get('net', {})
            print(f"{Fore.CYAN}Name: {Fore.WHITE}{whois_net.get('name', {}).get('$', 'N/A')}")
            print(f"{Fore.CYAN}Handle: {Fore.WHITE}{whois_net.get('handle', {}).get('$', 'N/A')}")
            print(f"{Fore.CYAN}Start Address: {Fore.WHITE}{whois_net.get('startAddress', {}).get('$', 'N/A')}")
            print(f"{Fore.CYAN}End Address: {Fore.WHITE}{whois_net.get('endAddress', {}).get('$', 'N/A')}")
            print(f"{Fore.CYAN}CIDR: {Fore.WHITE}{whois_net.get('cidr', 'N/A')}")
            print(f"{Fore.CYAN}Parent: {Fore.WHITE}{whois_net.get('parentNetRef', {}).get('@name', 'N/A')}")
            print(f"{Fore.CYAN}Organization: {Fore.WHITE}{whois_net.get('orgRef', {}).get('@name', 'N/A')}")
            print(f"{Fore.CYAN}Registration Date: {Fore.WHITE}{whois_net.get('registrationDate', 'N/A')}")
            print(f"{Fore.CYAN}Last Updated: {Fore.WHITE}{whois_net.get('updateDate', {}).get('$', 'N/A')}")

if __name__ == "__main__":
    main()
