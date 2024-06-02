import dns.resolver
import itertools
import os

def find_subdomains(domain, wordlist):
    subdomains = []
    
    # Generate different patterns of subdomains
    patterns = [
        "{word}.{domain}",
        "{word1}.{word2}.{domain}",
        "{domain}.{word}",
        "{word1}-{word2}.{domain}",
        "{word1}-{word2}-{word3}.{domain}"
    ]
    
    for pattern in patterns:
        if "{domain}" not in pattern:
            continue
        
        for words in itertools.permutations(wordlist, pattern.count("{word}")):
            subdomain = pattern.format(
                domain=domain, 
                word=words[0] if len(words) > 0 else '',
                word1=words[0] if len(words) > 0 else '',
                word2=words[1] if len(words) > 1 else '',
                word3=words[2] if len(words) > 2 else ''
            )
            
            try:
                answers = dns.resolver.resolve(subdomain, 'A')
                for answer in answers:
                    subdomains.append(subdomain)
                    print(f"Found subdomain: {subdomain} -> {answer}")
            except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
                continue
            except Exception as e:
                print(f"An error occurred: {e}")
    
    return subdomains

def load_wordlist(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

if __name__ == "__main__":
    while True:
        domain = input("Enter the domain to find subdomains for (or 'q' to quit): ")
        if domain.lower() == 'q':
            break
        
        # Path to the wordlist file
        word_path = os.path.join(os.path.dirname(os.path.realpath(__file__)) + "\\" + "names.txt")
        wordlist_file = word_path
        
        try:
            wordlist = load_wordlist(wordlist_file)
        except FileNotFoundError:
            print(f"Wordlist file {wordlist_file} not found.")
            continue
        except Exception as e:
            print(f"An error occurred while loading the wordlist: {e}")
            continue
        
        subdomains = find_subdomains(domain, wordlist)
        
        print("\nSubdomains found:")
        for subdomain in subdomains:
            print(subdomain)
