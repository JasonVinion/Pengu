#!/usr/bin/env python3
"""
Pengu Terms of Service and Legal Disclaimer
"""

from colorama import init, Fore, Style
import requests
import socket

init(autoreset=True)

def get_user_location():
    """Get user's geolocation based on public IP (Issue 3)"""
    try:
        # Get public IP first
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        if response.status_code == 200:
            public_ip = response.json().get('ip')
            
            # Get location info
            location_response = requests.get(f'https://ipapi.co/{public_ip}/json/', timeout=5)
            if location_response.status_code == 200:
                location_data = location_response.json()
                return {
                    'ip': public_ip,
                    'country': location_data.get('country_name', 'Unknown'),
                    'country_code': location_data.get('country_code', 'Unknown'),
                    'region': location_data.get('region', 'Unknown'),
                    'city': location_data.get('city', 'Unknown')
                }
    except Exception as e:
        print(f"{Fore.YELLOW}Could not determine location: {e}")
    
    return None

def get_regional_legislation_info(location_data):
    """Get relevant legislation based on user location (Issue 3)"""
    if not location_data:
        return {
            'title': 'International Computer Security Guidelines',
            'description': 'General international computer use policies',
            'url': 'https://www.un.org/en/cybersecuritycompact/'
        }
    
    country_code = location_data.get('country_code', '').upper()
    
    # USA
    if country_code == 'US':
        return {
            'title': 'Computer Fraud and Abuse Act (CFAA)',
            'description': 'United States federal law governing computer security',
            'url': 'https://www.justice.gov/jm/criminal-resource-manual-1030-computer-fraud-and-abuse-act-18-usc-1030'
        }
    
    # European Union countries
    eu_countries = ['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 
                    'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 
                    'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE']
    if country_code in eu_countries:
        return {
            'title': 'EU NIS Directive & Cybersecurity Act',
            'description': 'European Union cybersecurity legislation',
            'url': 'https://digital-strategy.ec.europa.eu/en/policies/nis-directive'
        }
    
    # United Kingdom
    if country_code == 'GB':
        return {
            'title': 'Computer Misuse Act 1990',
            'description': 'United Kingdom computer security legislation',
            'url': 'https://www.legislation.gov.uk/ukpga/1990/18/contents'
        }
    
    # Canada
    if country_code == 'CA':
        return {
            'title': 'Personal Information Protection and Electronic Documents Act (PIPEDA)',
            'description': 'Canadian privacy and computer security legislation',
            'url': 'https://www.priv.gc.ca/en/privacy-topics/privacy-laws-in-canada/the-personal-information-protection-and-electronic-documents-act-pipeda/'
        }
    
    # Australia
    if country_code == 'AU':
        return {
            'title': 'Cybercrime Act 2001',
            'description': 'Australian cybercrime legislation',
            'url': 'https://www.legislation.gov.au/Details/C2017C00105'
        }
    
    # Asia - Japan
    if country_code == 'JP':
        return {
            'title': 'Unauthorized Computer Access Law',
            'description': 'Japanese cybersecurity legislation',
            'url': 'https://www.nisc.go.jp/eng/index.html'
        }
    
    # Asia - Singapore
    if country_code == 'SG':
        return {
            'title': 'Computer Misuse and Cybersecurity Act',
            'description': 'Singapore cybersecurity legislation',
            'url': 'https://www.csa.gov.sg/legislation/computer-misuse-act'
        }
    
    # Fallback for other countries
    return {
        'title': 'International Computer Security Guidelines',
        'description': f'General computer security guidelines for {location_data.get("country", "your region")}',
        'url': 'https://www.un.org/en/cybersecuritycompact/'
    }
def show_terms_of_service():
    """Display terms of service with geolocation-based legal information (Issue 3)"""
    
    tos_text = f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════╗
{Fore.RED}║                            {Fore.WHITE}⚠ TERMS OF SERVICE ⚠{Fore.RED}                          ║
{Fore.RED}║                      {Fore.WHITE}PENGU NETWORK SECURITY TOOLS{Fore.RED}                      ║
{Fore.RED}╚════════════════════════════════════════════════════════════════════════╝

{Fore.YELLOW}🚨 IMPORTANT LEGAL NOTICE 🚨

{Fore.WHITE}BY CONTINUING TO USE THIS TOOL, YOU AGREE TO THE TERMS OF SERVICE.

{Fore.CYAN}1. AUTHORIZED USE ONLY
{Fore.WHITE}   • These tools are intended EXCLUSIVELY for security professionals
   • You may ONLY use these tools on systems you own or have EXPLICIT 
     written permission to test
   • Unauthorized scanning, testing, or probing of networks or systems 
     is ILLEGAL and may violate local, state, and federal laws

{Fore.CYAN}2. PROFESSIONAL USE
{Fore.WHITE}   • These tools are designed for:
     - Authorized penetration testing
     - Security audits with proper documentation
     - Network administration of owned systems
     - Educational purposes in controlled environments
     - Bug bounty programs with explicit scope

{Fore.CYAN}3. PROHIBITED ACTIVITIES
{Fore.WHITE}   • Scanning or testing systems without explicit permission
   • Using tools for malicious purposes
   • Violating terms of service of target systems
   • Bypassing security measures without authorization
   • Any activity that may be considered hacking or unauthorized access

{Fore.CYAN}4. DISCLAIMER OF LIABILITY
{Fore.WHITE}   • The developers of Pengu are NOT RESPONSIBLE for any:
     - Damage caused by the use or misuse of these tools
     - Legal consequences resulting from unauthorized use
     - Network disruptions or system failures
     - Data loss or security breaches
     - Violations of laws or regulations

{Fore.CYAN}5. LEGAL COMPLIANCE
{Fore.WHITE}   • You are solely responsible for ensuring your use complies with:
     - All applicable local, state, and federal laws
     - International cybersecurity regulations
     - Terms of service of target systems
     - Professional ethical standards
     - Organizational policies and procedures

{Fore.RED}⚠ WARNING: UNAUTHORIZED USE IS ILLEGAL ⚠

{Fore.YELLOW}If you cannot ensure authorized use, DO NOT USE THESE TOOLS.

{Fore.WHITE}Remember: With great power comes great responsibility.
Always act ethically and within the bounds of the law.

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════
{Fore.WHITE}By continuing to use Pengu, you acknowledge that you have read, understood,
and agree to comply with all terms and conditions stated above.
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════
"""
    
    print(tos_text)
    
    # New geolocation-based menu (Issue 3)
    while True:
        try:
            print(f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════╗
{Fore.MAGENTA}║                     {Fore.CYAN}Options{Fore.MAGENTA}                         ║
{Fore.MAGENTA}╚══════════════════════════════════════════════════════════╝

{Fore.GREEN}1. {Fore.WHITE}Return to Home Menu
{Fore.GREEN}2. {Fore.WHITE}View Relevant Regional Computer Security Legislation
""")
            
            choice = input(f"{Fore.YELLOW}Select option (1-2): ").strip()
            
            if choice == '1':
                return 'home'
            elif choice == '2':
                show_regional_legislation()
                # Continue loop to show options again
            else:
                print(f"{Fore.RED}Invalid option. Please select 1 or 2.")
                
        except KeyboardInterrupt:
            return 'home'
        except:
            return 'home'

def show_regional_legislation():
    """Show regional legislation based on user's location (Issue 3)"""
    print(f"\n{Fore.CYAN}Detecting your location for relevant legislation...")
    
    location_data = get_user_location()
    legislation = get_regional_legislation_info(location_data)
    
    if location_data:
        print(f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════╗
{Fore.GREEN}║              {Fore.CYAN}Regional Legislation Information{Fore.GREEN}          ║
{Fore.GREEN}╚══════════════════════════════════════════════════════════╝

{Fore.CYAN}Your Location: {Fore.WHITE}{location_data.get('city', 'Unknown')}, {location_data.get('country', 'Unknown')}
{Fore.CYAN}Your Public IP: {Fore.WHITE}{location_data.get('ip', 'Unknown')}

{Fore.CYAN}Relevant Legislation:
{Fore.YELLOW}{legislation['title']}

{Fore.WHITE}{legislation['description']}

{Fore.CYAN}More Information: {Fore.BLUE}{legislation['url']}
""")
    else:
        print(f"""
{Fore.YELLOW}╔══════════════════════════════════════════════════════════╗
{Fore.YELLOW}║              {Fore.WHITE}Location Detection Failed{Fore.YELLOW}             ║
{Fore.YELLOW}╚══════════════════════════════════════════════════════════╝

{Fore.WHITE}Could not determine your location due to network connectivity issues.
Displaying general international guidelines:

{Fore.CYAN}Relevant Guidelines:
{Fore.YELLOW}{legislation['title']}

{Fore.WHITE}{legislation['description']}

{Fore.CYAN}More Information: {Fore.BLUE}{legislation['url']}
""")
    
    input(f"\n{Fore.YELLOW}Press Enter to continue...")

def main():
    """Main function for standalone execution"""
    result = show_terms_of_service()
    return result

if __name__ == "__main__":
    main()