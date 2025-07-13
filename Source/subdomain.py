import dns.resolver
import threading
import os
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Thread-safe print lock
print_lock = threading.Lock()

def check_subdomain(subdomain):
    """Check if a subdomain exists and return result"""
    try:
        answers = dns.resolver.resolve(subdomain, 'A')
        ips = [str(answer) for answer in answers]
        return subdomain, ips
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout):
        return None, None
    except Exception:
        return None, None

def find_subdomains_threaded(domain, wordlist, max_workers=50):
    """Find subdomains using efficient threading"""
    found_subdomains = []
    
    # Generate subdomain candidates more efficiently
    subdomain_candidates = set()
    
    # Basic patterns - most common first
    for word in wordlist:
        subdomain_candidates.add(f"{word}.{domain}")
    
    # Two-word combinations (limited to avoid explosion)
    common_words = wordlist[:100]  # Limit to first 100 for combinations
    for word1 in common_words:
        for word2 in common_words[:20]:  # Even more limited for second word
            subdomain_candidates.add(f"{word1}.{word2}.{domain}")
            subdomain_candidates.add(f"{word1}-{word2}.{domain}")
    
    total_candidates = len(subdomain_candidates)
    checked = 0
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_subdomain = {
            executor.submit(check_subdomain, subdomain): subdomain 
            for subdomain in subdomain_candidates
        }
        
        # Process results as they complete
        for future in as_completed(future_to_subdomain):
            subdomain, ips = future.result()
            checked += 1
            
            if subdomain and ips:
                with print_lock:
                    print(f"{Fore.GREEN}[{checked}/{total_candidates}] Found: {subdomain} -> {', '.join(ips)}")
                found_subdomains.append((subdomain, ips))
            else:
                if checked % 100 == 0:  # Progress indicator
                    with print_lock:
                        print(f"{Fore.YELLOW}[{checked}/{total_candidates}] Checking...")
    
    return found_subdomains

def load_wordlist(filename):
    """Load wordlist efficiently with error handling"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            # Remove duplicates and empty lines, strip whitespace
            words = [line.strip() for line in file if line.strip()]
            return list(set(words))  # Remove duplicates
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Wordlist file {filename} not found.")
        return []
    except Exception as e:
        print(f"{Fore.RED}Error loading wordlist: {e}")
        return []

def print_banner():
    """Print the subdomain scanner banner"""
    print(f"""
{Fore.CYAN} ╔════════════════════════════╗
{Fore.CYAN} ║ {Fore.MAGENTA}Project Pengu Subdomain Scanner{Fore.CYAN} ║
{Fore.CYAN} ║ {Fore.GREEN}Optimized Multi-threaded Version{Fore.CYAN}   ║
{Fore.CYAN} ╚════════════════════════════╝
""")

def main():
    """Main entry point"""
    print_banner()
    
    while True:
        domain = input(f"{Fore.YELLOW}Enter domain to scan (or 'exit' to quit): ").strip()
        if domain.lower() == 'exit':
            break
        
        if not domain:
            print(f"{Fore.RED}Please enter a valid domain.")
            continue
            
        # Remove protocol if present
        domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        
        # Path to the wordlist file (now in Source directory)
        wordlist_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "names.txt")
        
        print(f"{Fore.CYAN}Loading wordlist...")
        wordlist = load_wordlist(wordlist_file)
        
        if not wordlist:
            print(f"{Fore.RED}No wordlist loaded. Cannot proceed.")
            continue
            
        print(f"{Fore.GREEN}Loaded {len(wordlist)} words from wordlist.")
        print(f"{Fore.YELLOW}Starting subdomain enumeration for {domain}...")
        
        try:
            found_subdomains = find_subdomains_threaded(domain, wordlist)
            
            print(f"\n{Fore.GREEN}╔═══════════════════════════╗")
            print(f"{Fore.GREEN}║ {Fore.CYAN}SCAN RESULTS SUMMARY{Fore.GREEN}      ║")
            print(f"{Fore.GREEN}╚═══════════════════════════╝")
            
            if found_subdomains:
                print(f"{Fore.GREEN}Found {len(found_subdomains)} subdomains:")
                for subdomain, ips in found_subdomains:
                    print(f"{Fore.CYAN}{subdomain} {Fore.WHITE}-> {Fore.GREEN}{', '.join(ips)}")
            else:
                print(f"{Fore.YELLOW}No subdomains found for {domain}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Scan interrupted by user.")
        except Exception as e:
            print(f"{Fore.RED}Error during scan: {e}")
            
        print()  # Empty line for readability

if __name__ == "__main__":
    main()
