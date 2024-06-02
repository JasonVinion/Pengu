

# compile to an exe so users can use it without python installed

import socket
import threading
from queue import Queue
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

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
    ip = input("Enter IP address: ")
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
    num_threads = int(input("Enter number of threads: "))
    print("scanning...")
    # Start worker threads
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(ip,))
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

    main()

if __name__ == "__main__":
    main()
