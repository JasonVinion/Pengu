

# compile to an exe so users can use it without python installed

import socket
import threading
from queue import Queue
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print the port scanner banner"""
    message = f"""
{Fore.GREEN} ╔════════════════════════════╗
{Fore.GREEN} ║ {Fore.MAGENTA}Project Pengu Port Scanner{Fore.GREEN} ╚════╗
{Fore.GREEN} ║                                 ║
{Fore.GREEN} ╚═════════════════════════════════╝
"""
    print(message)

# Thread queue
queue = Queue()

# Thread-safe print
print_lock = threading.Lock()

def scan_port(ip, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(1)
        try:
            sock.connect((ip, port))
            with print_lock:
                print(f"{Fore.GREEN}Port {port} is open on {ip}")
        except:
            pass

def worker(ip):
    while True:
        port = queue.get()
        if port is None:
            break
        scan_port(ip, port)
        queue.task_done()

def main():
    print_banner()
    while True:
        try:
            ip = input("Enter IP address (or 'exit' to quit): ").strip()
            if ip.lower() == 'exit':
                break
                
            start_port = int(input("Enter start port: "))
            end_port = int(input("Enter end port: "))
            
            # Get thread count with hardware recommendation
            try:
                # Try to get hardware-based recommendation
                try:
                    import system_specs
                    recommended_threads = system_specs.system_specs.get_thread_recommendation('port_scanning')
                    print(f"{Fore.GREEN}Hardware-based recommendation: {recommended_threads} threads")
                except:
                    recommended_threads = 50
                    print(f"{Fore.YELLOW}Using default recommendation: {recommended_threads} threads")
                
                thread_input = input(f"{Fore.CYAN}Enter number of threads (default: {recommended_threads}): ").strip()
                if thread_input:
                    num_threads = int(thread_input)
                    if num_threads > 200:
                        print(f"{Fore.YELLOW}Warning: Very high thread count ({num_threads}) may overwhelm the target!")
                        confirm = input(f"{Fore.YELLOW}Continue anyway? (y/N): ").strip().lower()
                        if confirm != 'y':
                            continue
                else:
                    num_threads = recommended_threads
                    
            except ValueError:
                print(f"{Fore.RED}Invalid thread count. Using default: 50")
                num_threads = 50
                
            num_threads = min(num_threads, 200)  # Hard limit for safety
            
            print(f"{Fore.CYAN}Scanning {ip} ports {start_port}-{end_port} with {num_threads} threads...")
            
            # Start worker threads
            threads = []
            for _ in range(num_threads):
                t = threading.Thread(target=worker, args=(ip,))
                t.daemon = True  # Allow main thread to exit
                t.start()
                threads.append(t)

            # Put ports in queue
            for port in range(start_port, end_port + 1):
                queue.put(port)

            # Block until all tasks are done
            queue.join()

            # Stop workers
            for _ in range(num_threads):
                queue.put(None)
            for t in threads:
                t.join()
                
            print(f"{Fore.GREEN}Scan complete for {ip}!")
            
        except ValueError:
            print(f"{Fore.RED}Invalid input. Please enter valid numbers.")
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nScan interrupted by user.")
            break
        except Exception as e:
            print(f"{Fore.RED}Error: {e}")

if __name__ == "__main__":
    main()
