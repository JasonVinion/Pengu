from colorama import init, Fore, Style
import time
import os
import subprocess

title_ascii = f"""
{Fore.CYAN}                                ########  ######## ##    ##  ######   ##     ## 
{Fore.CYAN}                                ##     ## ##       ###   ## ##    ##  ##     ## 
{Fore.CYAN}                                ##     ## ##       ####  ## ##        ##     ## 
{Fore.CYAN}                                ########  ######   ## ## ## ##   #### ##     ## 
{Fore.CYAN}                                ##        ##       ##  #### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ##       ##   ### ##    ##  ##     ## 
{Fore.CYAN}                                ##        ######## ##    ##  ######    #######  
{Fore.YELLOW}                                 Welcome to Pengu! Type 'help' to get started.
"""

# File Paths
script_dir = os.path.dirname(os.path.realpath(__file__))

# Path to the Tool Files
TCP_Pinger_path = os.path.join(script_dir, "Tools", "tcp_port_ping.bat")
icmp_ping_path = os.path.join(script_dir, "Tools", "ping.bat")
http_ping_path = os.path.join(script_dir, "Tools", "http_ping.bat")
whois_path = os.path.join(script_dir, "Tools", "whois.exe")
port_scanner_path = os.path.join(script_dir, "Tools", "port_scanner.exe")
traceroute_path = os.path.join(script_dir, "Tools", "traceroute.exe")
subdomain_path = os.path.join(script_dir, "Tools", "subdomain.exe")

# Initialize colorama
init(autoreset=True)

# Print the title
print(title_ascii)

help_menu = f"""
{Fore.MAGENTA} ╔════════════════════════╗
{Fore.MAGENTA} ║ {Fore.CYAN}Project Pengu MutiTool.{Fore.MAGENTA}╚═════════════════════════════╗
{Fore.MAGENTA} ║ {Fore.GREEN}Home       . Home Screen.{Fore.MAGENTA}                            ║
{Fore.MAGENTA} ║ {Fore.GREEN}Help       . Help Menu.{Fore.MAGENTA}                              ║
{Fore.MAGENTA} ║ {Fore.GREEN}TCP        . TCP Pinger.{Fore.MAGENTA}                             ║
{Fore.MAGENTA} ║ {Fore.GREEN}PING       . Normal (ICMP) Pinger.{Fore.MAGENTA}                   ║
{Fore.MAGENTA} ║ {Fore.GREEN}HTTP       . HTTP/HTTPS Pinger{Fore.MAGENTA}                       ║          
{Fore.MAGENTA} ║ {Fore.GREEN}Port       . Portscanner{Fore.MAGENTA}                             ║
{Fore.MAGENTA} ║ {Fore.GREEN}Credit     . Show Credits.{Fore.MAGENTA}                           ║
{Fore.MAGENTA} ║ {Fore.GREEN}Tracker    . GeoIP & Whois{Fore.MAGENTA}                           ║
{Fore.MAGENTA} ║ {Fore.GREEN}Traceroute . Trace Packets.{Fore.MAGENTA}                          ║
{Fore.MAGENTA} ║ {Fore.GREEN}Subdomain  . Subdomain Finder.{Fore.MAGENTA}                       ║
{Fore.MAGENTA} ║ {Fore.GREEN}Exit       . Exit Pengu.{Fore.MAGENTA}                             ║
{Fore.MAGENTA} ╚══════════════════════════════════════════════════════╝
"""

# Banner grabbing
def rtn_to_home():
    os.system('cls')
    print(title_ascii)

def run_subprocess(path):
    subprocess.Popen(['start', 'cmd', '/k', path], shell=True)
    rtn_to_home()

def user_inputs():
    commands = {
        "help": lambda: print(help_menu),
        "home": rtn_to_home,
        "ping": lambda: run_subprocess(icmp_ping_path),
        "http": lambda: run_subprocess(http_ping_path),
        "tcp": lambda: run_subprocess(TCP_Pinger_path),
        "tracker": lambda: run_subprocess(whois_path),
        "port": lambda: run_subprocess(port_scanner_path),
        "traceroute": lambda: run_subprocess(traceroute_path),
        "subdomain": lambda: run_subprocess(subdomain_path),
        "credit": lambda: print(f"""
{Fore.GREEN} ╔════════════════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Pengu MutiTool Credit{Fore.GREEN}                  ║
{Fore.GREEN} ║ {Fore.MAGENTA}Github: https://github.com/JasonVinion{Fore.GREEN} ║
{Fore.GREEN} ╚════════════════════════════════════════╝
                  """)
    }

    while True:
        userinput = input(Fore.GREEN + ">>> " + Fore.BLUE).strip().lower()
        if userinput in commands:
            commands[userinput]()
        elif userinput == "exit":
            print(Fore.GREEN + "Exiting Pengu...")
            time.sleep(1)
            break
        else:
            print(Fore.RED + "Invalid command")

user_inputs()
