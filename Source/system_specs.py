#!/usr/bin/env python3
"""
Pengu System Hardware Detection Module
"""

import os
import sys
import platform
import subprocess
import threading
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

class SystemSpecs:
    def __init__(self):
        self.cpu_cores = 0
        self.cpu_threads = 0
        self.cpu_model = "Unknown"
        self.ram_total = 0
        self.ram_available = 0
        self.gpu_info = "Unknown"
        self.motherboard = "Unknown"
        self.platform = platform.system()
        
    def detect_cpu_info(self):
        """Detect CPU information"""
        try:
            import multiprocessing
            self.cpu_cores = multiprocessing.cpu_count()
            
            if self.platform == "Windows":
                try:
                    # Get CPU model from wmic
                    result = subprocess.run(['wmic', 'cpu', 'get', 'name'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip() and 'Name' not in line:
                                self.cpu_model = line.strip()
                                break
                except:
                    pass
                    
                try:
                    # Get thread count
                    result = subprocess.run(['wmic', 'cpu', 'get', 'ThreadCount'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip() and 'ThreadCount' not in line:
                                self.cpu_threads = int(line.strip())
                                break
                except:
                    self.cpu_threads = self.cpu_cores
                    
            elif self.platform == "Linux":
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        cpuinfo = f.read()
                        for line in cpuinfo.split('\n'):
                            if 'model name' in line:
                                self.cpu_model = line.split(':')[1].strip()
                                break
                    
                    # Count threads
                    thread_count = cpuinfo.count('processor')
                    self.cpu_threads = thread_count if thread_count > 0 else self.cpu_cores
                except:
                    self.cpu_threads = self.cpu_cores
            else:
                self.cpu_threads = self.cpu_cores
                
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not detect CPU info: {e}")
    
    def detect_memory_info(self):
        """Detect memory information"""
        try:
            if self.platform == "Windows":
                try:
                    # Total RAM
                    result = subprocess.run(['wmic', 'computersystem', 'get', 'TotalPhysicalMemory'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip() and 'TotalPhysicalMemory' not in line:
                                self.ram_total = int(line.strip()) // (1024 ** 3)  # Convert to GB
                                break
                                
                    # Available RAM
                    result = subprocess.run(['wmic', 'OS', 'get', 'FreePhysicalMemory'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines:
                            if line.strip() and 'FreePhysicalMemory' not in line:
                                self.ram_available = int(line.strip()) // (1024 ** 2)  # Convert to GB
                                break
                except:
                    pass
                    
            elif self.platform == "Linux":
                try:
                    with open('/proc/meminfo', 'r') as f:
                        meminfo = f.read()
                        for line in meminfo.split('\n'):
                            if 'MemTotal:' in line:
                                self.ram_total = int(line.split()[1]) // (1024 ** 2)  # Convert to GB
                            elif 'MemAvailable:' in line:
                                self.ram_available = int(line.split()[1]) // (1024 ** 2)  # Convert to GB
                except:
                    pass
                    
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not detect memory info: {e}")
    
    def detect_gpu_info(self):
        """Detect GPU information"""
        try:
            if self.platform == "Windows":
                try:
                    result = subprocess.run(['wmic', 'path', 'win32_VideoController', 'get', 'name'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        gpus = []
                        for line in lines:
                            if line.strip() and 'Name' not in line:
                                gpus.append(line.strip())
                        if gpus:
                            self.gpu_info = ', '.join(gpus)
                except:
                    pass
                    
            elif self.platform == "Linux":
                try:
                    # Try lspci for GPU info
                    result = subprocess.run(['lspci', '-mm'], capture_output=True, text=True)
                    if result.returncode == 0:
                        gpus = []
                        for line in result.stdout.split('\n'):
                            if 'VGA compatible controller' in line or 'Display controller' in line:
                                parts = line.split('"')
                                if len(parts) >= 6:
                                    gpus.append(f"{parts[3]} {parts[5]}")
                        if gpus:
                            self.gpu_info = ', '.join(gpus)
                except:
                    pass
                    
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not detect GPU info: {e}")
    
    def detect_motherboard_info(self):
        """Detect motherboard information"""
        try:
            if self.platform == "Windows":
                try:
                    result = subprocess.run(['wmic', 'baseboard', 'get', 'Manufacturer,Product'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        lines = result.stdout.strip().split('\n')
                        for line in lines[1:]:  # Skip header
                            if line.strip():
                                parts = line.strip().split()
                                if len(parts) >= 2:
                                    self.motherboard = ' '.join(parts)
                                    break
                except:
                    pass
                    
            elif self.platform == "Linux":
                try:
                    # Try dmidecode for motherboard info
                    result = subprocess.run(['dmidecode', '-t', 'baseboard'], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        manufacturer = ""
                        product = ""
                        for line in result.stdout.split('\n'):
                            if 'Manufacturer:' in line:
                                manufacturer = line.split(':')[1].strip()
                            elif 'Product Name:' in line:
                                product = line.split(':')[1].strip()
                        if manufacturer and product:
                            self.motherboard = f"{manufacturer} {product}"
                except:
                    pass
                    
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not detect motherboard info: {e}")
    
    def scan_hardware(self):
        """Scan all hardware in background"""
        print(f"{Fore.YELLOW}Scanning system hardware...")
        
        # Create threads for concurrent scanning
        threads = [
            threading.Thread(target=self.detect_cpu_info, daemon=True),
            threading.Thread(target=self.detect_memory_info, daemon=True),
            threading.Thread(target=self.detect_gpu_info, daemon=True),
            threading.Thread(target=self.detect_motherboard_info, daemon=True)
        ]
        
        # Start all threads
        for thread in threads:
            thread.start()
        
        # Wait for all threads to complete with timeout
        for thread in threads:
            thread.join(timeout=5)  # 5 second timeout per thread
        
        print(f"{Fore.GREEN}Hardware scan complete!")
    
    def get_thread_recommendation(self, task_type="port_scanning"):
        """Get recommended thread count based on hardware"""
        if task_type == "port_scanning":
            # Conservative recommendation for port scanning
            if self.cpu_threads >= 16:
                return min(100, self.cpu_threads * 2)
            elif self.cpu_threads >= 8:
                return min(50, self.cpu_threads * 2)
            elif self.cpu_threads >= 4:
                return min(25, self.cpu_threads * 2)
            else:
                return min(10, max(4, self.cpu_threads))
        elif task_type == "subdomain":
            # More aggressive for subdomain scanning
            if self.cpu_threads >= 16:
                return min(200, self.cpu_threads * 4)
            elif self.cpu_threads >= 8:
                return min(100, self.cpu_threads * 3)
            elif self.cpu_threads >= 4:
                return min(50, self.cpu_threads * 2)
            else:
                return min(20, max(8, self.cpu_threads))
        else:
            return max(4, self.cpu_threads // 2)
    
    def display_specs(self):
        """Display system specifications"""
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}System Hardware Specs{Fore.CYAN}              ║
{Fore.CYAN}╚══════════════════════════════════════════════════╝

{Fore.GREEN}CPU Information:
{Fore.CYAN}  Model:        {Fore.WHITE}{self.cpu_model}
{Fore.CYAN}  Cores:        {Fore.WHITE}{self.cpu_cores}
{Fore.CYAN}  Threads:      {Fore.WHITE}{self.cpu_threads}

{Fore.GREEN}Memory Information:
{Fore.CYAN}  Total RAM:    {Fore.WHITE}{self.ram_total} GB
{Fore.CYAN}  Available:    {Fore.WHITE}{self.ram_available} GB

{Fore.GREEN}Graphics:
{Fore.CYAN}  GPU(s):       {Fore.WHITE}{self.gpu_info}

{Fore.GREEN}Motherboard:
{Fore.CYAN}  Board:        {Fore.WHITE}{self.motherboard}

{Fore.GREEN}Platform:
{Fore.CYAN}  OS:           {Fore.WHITE}{self.platform} {platform.release()}
{Fore.CYAN}  Architecture: {Fore.WHITE}{platform.machine()}

{Fore.YELLOW}╔══════════════════════════════════════════════════╗
{Fore.YELLOW}║              {Fore.MAGENTA}Performance Recommendations{Fore.YELLOW}         ║
{Fore.YELLOW}╚══════════════════════════════════════════════════╝

{Fore.GREEN}Recommended Thread Counts:
{Fore.CYAN}  Port Scanner:    {Fore.WHITE}{self.get_thread_recommendation('port_scanning')} threads
{Fore.CYAN}  Subdomain Finder:{Fore.WHITE}{self.get_thread_recommendation('subdomain')} threads
{Fore.CYAN}  General Tasks:   {Fore.WHITE}{self.get_thread_recommendation('general')} threads

{Fore.YELLOW}Note: These are conservative recommendations. You can adjust based on your needs.
{Fore.YELLOW}Higher thread counts may trigger rate limiting on target servers.
""")

# Global system specs instance
system_specs = SystemSpecs()

def print_banner():
    """Print the specs banner"""
    print(f"""
{Fore.CYAN}╔════════════════════════════════════════╗
{Fore.CYAN}║        {Fore.MAGENTA}Pengu System Specs{Fore.CYAN}            ║
{Fore.CYAN}║      {Fore.GREEN}Hardware Detection Tool{Fore.CYAN}          ║
{Fore.CYAN}╚════════════════════════════════════════╝
""")

def main():
    """Main specs function"""
    print_banner()
    
    # Scan hardware
    system_specs.scan_hardware()
    
    # Display results
    system_specs.display_specs()
    
    return system_specs

if __name__ == "__main__":
    main()