#!/usr/bin/env python3
"""
Pengu Terms of Service and Legal Disclaimer
"""

from colorama import init, Fore, Style

init(autoreset=True)

def show_terms_of_service():
    """Display comprehensive terms of service and disclaimer"""
    
    tos_text = f"""
{Fore.RED}╔════════════════════════════════════════════════════════════════════════╗
{Fore.RED}║                            {Fore.WHITE}⚠ TERMS OF SERVICE ⚠{Fore.RED}                          ║
{Fore.RED}║                      {Fore.WHITE}PENGU NETWORK SECURITY TOOLS{Fore.RED}                      ║
{Fore.RED}╚════════════════════════════════════════════════════════════════════════╝

{Fore.YELLOW}🚨 IMPORTANT LEGAL NOTICE 🚨

{Fore.WHITE}BY USING THESE TOOLS, YOU ACKNOWLEDGE AND AGREE TO THE FOLLOWING:

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

{Fore.CYAN}6. NO WARRANTY
{Fore.WHITE}   • These tools are provided "AS IS" without any warranty
   • No guarantee of accuracy, reliability, or fitness for purpose
   • Use at your own risk and discretion

{Fore.CYAN}7. INDEMNIFICATION
{Fore.WHITE}   • You agree to indemnify and hold harmless the developers from any
     claims, damages, or legal actions resulting from your use of these tools

{Fore.RED}⚠ WARNING: UNAUTHORIZED USE IS ILLEGAL ⚠

{Fore.YELLOW}If you do not agree to these terms or cannot ensure authorized use,
DO NOT USE THESE TOOLS.

{Fore.WHITE}Remember: With great power comes great responsibility.
Always act ethically and within the bounds of the law.

{Fore.GREEN}For questions about appropriate use, consult with:
• Your organization's legal counsel
• Local cybersecurity laws and regulations  
• Professional ethical guidelines
• The Computer Fraud and Abuse Act (if in the US)

{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════
{Fore.WHITE}By continuing to use Pengu, you acknowledge that you have read, understood,
and agree to comply with all terms and conditions stated above.
{Fore.CYAN}═══════════════════════════════════════════════════════════════════════════
"""
    
    print(tos_text)
    
    # Wait for user acknowledgment
    while True:
        response = input(f"\n{Fore.YELLOW}Do you acknowledge and agree to these terms? (yes/no): ").strip().lower()
        
        if response in ['yes', 'y']:
            print(f"{Fore.GREEN}✓ Terms acknowledged. Remember to use these tools responsibly.")
            break
        elif response in ['no', 'n']:
            print(f"{Fore.RED}Terms not accepted. Please do not use these tools without proper authorization.")
            break
        else:
            print(f"{Fore.YELLOW}Please enter 'yes' or 'no'")

def main():
    """Main function for standalone execution"""
    show_terms_of_service()

if __name__ == "__main__":
    main()