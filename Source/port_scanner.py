

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
            num_threads = min(int(input("Enter number of threads: ")), 100)  # Limit threads for efficiency
            
            print("Scanning...")
            
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
