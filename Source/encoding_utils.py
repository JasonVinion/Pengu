#!/usr/bin/env python3
"""
Pengu Encoding/Decoding Utilities
Advanced text manipulation and encoding tools for security professionals
"""

import base64
import hashlib
import html
import urllib.parse
import re
import unicodedata
import os
from colorama import init, Fore, Style

init(autoreset=True)

def print_banner():
    """Print the encoding/decoding utilities banner"""
    banner = f"""
{Fore.GREEN}╔══════════════════════════════════════════════════════════╗
{Fore.GREEN}║ {Fore.MAGENTA}Pengu Encoding/Decoding & Text Utilities{Fore.GREEN}             ║
{Fore.GREEN}║ {Fore.CYAN}Advanced text manipulation for security analysis{Fore.GREEN}     ║
{Fore.GREEN}╚══════════════════════════════════════════════════════════╝
"""
    print(banner)

def base64_operations():
    """Base64 encoding and decoding operations"""
    print(f"\n{Fore.CYAN}═══ Base64 Operations ═══")
    
    while True:
        print(f"""
{Fore.YELLOW}Base64 Options:
{Fore.GREEN}1. {Fore.WHITE}Encode text to Base64
{Fore.GREEN}2. {Fore.WHITE}Decode Base64 to text
{Fore.GREEN}3. {Fore.WHITE}Encode file to Base64
{Fore.GREEN}4. {Fore.WHITE}Decode Base64 to file
{Fore.GREEN}5. {Fore.WHITE}Return to Utility Menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-5): ").strip()
        
        if choice == '1':
            text = input(f"{Fore.YELLOW}Enter text to encode: ")
            try:
                encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                print(f"{Fore.GREEN}Encoded: {Fore.WHITE}{encoded}")
                
                save_choice = input(f"{Fore.YELLOW}Save to file? (y/N): ").strip().lower()
                if save_choice == 'y':
                    filename = input(f"{Fore.YELLOW}Enter filename: ").strip()
                    try:
                        with open(filename, 'w') as f:
                            f.write(encoded)
                        print(f"{Fore.GREEN}✓ Saved to {filename}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving file: {e}")
                        
            except Exception as e:
                print(f"{Fore.RED}Encoding error: {e}")
        
        elif choice == '2':
            text = input(f"{Fore.YELLOW}Enter Base64 to decode: ")
            try:
                decoded = base64.b64decode(text).decode('utf-8')
                print(f"{Fore.GREEN}Decoded: {Fore.WHITE}{decoded}")
                
                save_choice = input(f"{Fore.YELLOW}Save to file? (y/N): ").strip().lower()
                if save_choice == 'y':
                    filename = input(f"{Fore.YELLOW}Enter filename: ").strip()
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(decoded)
                        print(f"{Fore.GREEN}✓ Saved to {filename}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving file: {e}")
                        
            except Exception as e:
                print(f"{Fore.RED}Decoding error: {e}")
        
        elif choice == '3':
            filename = input(f"{Fore.YELLOW}Enter file path to encode: ").strip()
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                encoded = base64.b64encode(content).decode('utf-8')
                print(f"{Fore.GREEN}File encoded to Base64:")
                print(f"{Fore.WHITE}{encoded[:200]}{'...' if len(encoded) > 200 else ''}")
                
                save_choice = input(f"{Fore.YELLOW}Save encoded content to file? (y/N): ").strip().lower()
                if save_choice == 'y':
                    output_filename = input(f"{Fore.YELLOW}Enter output filename: ").strip()
                    try:
                        with open(output_filename, 'w') as f:
                            f.write(encoded)
                        print(f"{Fore.GREEN}✓ Saved to {output_filename}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving file: {e}")
                        
            except Exception as e:
                print(f"{Fore.RED}Error reading file: {e}")
        
        elif choice == '4':
            base64_text = input(f"{Fore.YELLOW}Enter Base64 content: ")
            output_filename = input(f"{Fore.YELLOW}Enter output filename: ").strip()
            try:
                decoded_data = base64.b64decode(base64_text)
                with open(output_filename, 'wb') as f:
                    f.write(decoded_data)
                print(f"{Fore.GREEN}✓ Decoded and saved to {output_filename}")
            except Exception as e:
                print(f"{Fore.RED}Error decoding/saving: {e}")
        
        elif choice == '5':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-5.")

def url_operations():
    """URL encoding and decoding operations"""
    print(f"\n{Fore.CYAN}═══ URL Operations ═══")
    
    while True:
        print(f"""
{Fore.YELLOW}URL Options:
{Fore.GREEN}1. {Fore.WHITE}URL Encode text
{Fore.GREEN}2. {Fore.WHITE}URL Decode text
{Fore.GREEN}3. {Fore.WHITE}Return to Utility Menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
        
        if choice == '1':
            text = input(f"{Fore.YELLOW}Enter text to URL encode: ")
            try:
                encoded = urllib.parse.quote(text)
                print(f"{Fore.GREEN}URL Encoded: {Fore.WHITE}{encoded}")
            except Exception as e:
                print(f"{Fore.RED}Encoding error: {e}")
        
        elif choice == '2':
            text = input(f"{Fore.YELLOW}Enter URL encoded text to decode: ")
            try:
                decoded = urllib.parse.unquote(text)
                print(f"{Fore.GREEN}URL Decoded: {Fore.WHITE}{decoded}")
            except Exception as e:
                print(f"{Fore.RED}Decoding error: {e}")
        
        elif choice == '3':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-3.")

def html_operations():
    """HTML encoding and decoding operations"""
    print(f"\n{Fore.CYAN}═══ HTML Operations ═══")
    
    while True:
        print(f"""
{Fore.YELLOW}HTML Options:
{Fore.GREEN}1. {Fore.WHITE}HTML Encode text
{Fore.GREEN}2. {Fore.WHITE}HTML Decode text
{Fore.GREEN}3. {Fore.WHITE}Return to Utility Menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-3): ").strip()
        
        if choice == '1':
            text = input(f"{Fore.YELLOW}Enter text to HTML encode: ")
            try:
                encoded = html.escape(text)
                print(f"{Fore.GREEN}HTML Encoded: {Fore.WHITE}{encoded}")
            except Exception as e:
                print(f"{Fore.RED}Encoding error: {e}")
        
        elif choice == '2':
            text = input(f"{Fore.YELLOW}Enter HTML encoded text to decode: ")
            try:
                decoded = html.unescape(text)
                print(f"{Fore.GREEN}HTML Decoded: {Fore.WHITE}{decoded}")
            except Exception as e:
                print(f"{Fore.RED}Decoding error: {e}")
        
        elif choice == '3':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-3.")

def hash_operations():
    """Hash generation operations"""
    print(f"\n{Fore.CYAN}═══ Hash Generation ═══")
    
    while True:
        print(f"""
{Fore.YELLOW}Hash Options:
{Fore.GREEN}1. {Fore.WHITE}Generate MD5 hash
{Fore.GREEN}2. {Fore.WHITE}Generate SHA1 hash
{Fore.GREEN}3. {Fore.WHITE}Generate SHA256 hash
{Fore.GREEN}4. {Fore.WHITE}Generate SHA512 hash
{Fore.GREEN}5. {Fore.WHITE}Hash file
{Fore.GREEN}6. {Fore.WHITE}Return to Utility Menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-6): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            text = input(f"{Fore.YELLOW}Enter text to hash: ")
            try:
                text_bytes = text.encode('utf-8')
                
                if choice == '1':
                    hash_obj = hashlib.md5(text_bytes)
                    hash_name = "MD5"
                elif choice == '2':
                    hash_obj = hashlib.sha1(text_bytes)
                    hash_name = "SHA1"
                elif choice == '3':
                    hash_obj = hashlib.sha256(text_bytes)
                    hash_name = "SHA256"
                elif choice == '4':
                    hash_obj = hashlib.sha512(text_bytes)
                    hash_name = "SHA512"
                
                hash_value = hash_obj.hexdigest()
                print(f"{Fore.GREEN}{hash_name} Hash: {Fore.WHITE}{hash_value}")
                
                save_choice = input(f"{Fore.YELLOW}Save hash to file? (y/N): ").strip().lower()
                if save_choice == 'y':
                    filename = input(f"{Fore.YELLOW}Enter filename: ").strip()
                    try:
                        with open(filename, 'w') as f:
                            f.write(f"{hash_name}: {hash_value}\nOriginal: {text}\n")
                        print(f"{Fore.GREEN}✓ Saved to {filename}")
                    except Exception as e:
                        print(f"{Fore.RED}Error saving file: {e}")
                        
            except Exception as e:
                print(f"{Fore.RED}Hashing error: {e}")
        
        elif choice == '5':
            filename = input(f"{Fore.YELLOW}Enter file path to hash: ").strip()
            try:
                with open(filename, 'rb') as f:
                    content = f.read()
                
                print(f"{Fore.GREEN}File Hashes for: {filename}")
                print(f"{Fore.CYAN}MD5:    {Fore.WHITE}{hashlib.md5(content).hexdigest()}")
                print(f"{Fore.CYAN}SHA1:   {Fore.WHITE}{hashlib.sha1(content).hexdigest()}")
                print(f"{Fore.CYAN}SHA256: {Fore.WHITE}{hashlib.sha256(content).hexdigest()}")
                print(f"{Fore.CYAN}SHA512: {Fore.WHITE}{hashlib.sha512(content).hexdigest()}")
                
            except Exception as e:
                print(f"{Fore.RED}Error reading file: {e}")
        
        elif choice == '6':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-6.")

def hidden_character_analysis():
    """Analyze and detect hidden characters in text"""
    print(f"\n{Fore.CYAN}═══ Hidden Character Analysis ═══")
    
    # Store last analysis for potential export (Issue 8)
    last_analysis = None
    last_source = None
    
    while True:
        print(f"""
{Fore.YELLOW}Hidden Character Options:
{Fore.GREEN}1. {Fore.WHITE}Analyze text for hidden characters
{Fore.GREEN}2. {Fore.WHITE}Analyze file for hidden characters
{Fore.GREEN}3. {Fore.WHITE}Clean text (remove hidden characters)
{Fore.GREEN}4. {Fore.WHITE}Export last analysis results
{Fore.GREEN}5. {Fore.WHITE}Return to Utility Menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-5): ").strip()
        
        if choice == '1':
            text = input(f"{Fore.YELLOW}Enter text to analyze: ")
            last_analysis = analyze_hidden_chars(text)
            last_source = "Text Input"
        
        elif choice == '2':
            filename = input(f"{Fore.YELLOW}Enter file path to analyze: ").strip()
            try:
                with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                print(f"{Fore.GREEN}Analyzing file: {filename}")
                last_analysis = analyze_hidden_chars(text)
                last_source = f"File: {filename}"
            except Exception as e:
                print(f"{Fore.RED}Error reading file: {e}")
        
        elif choice == '3':
            text = input(f"{Fore.YELLOW}Enter text to clean: ")
            cleaned = clean_hidden_chars(text)
            print(f"{Fore.GREEN}Cleaned text: {Fore.WHITE}{cleaned}")
            
            save_choice = input(f"{Fore.YELLOW}Save cleaned text to file? (y/N): ").strip().lower()
            if save_choice == 'y':
                filename = input(f"{Fore.YELLOW}Enter filename: ").strip()
                try:
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(cleaned)
                    print(f"{Fore.GREEN}✓ Saved to {filename}")
                except Exception as e:
                    print(f"{Fore.RED}Error saving file: {e}")
        
        elif choice == '4':
            if last_analysis:
                export_hidden_char_analysis(last_analysis, last_source)
            else:
                print(f"{Fore.RED}No analysis results available to export. Please run an analysis first.")
        
        elif choice == '5':
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-5.")

def analyze_hidden_chars(text):
    """Analyze text for hidden and suspicious characters"""
    print(f"\n{Fore.CYAN}Hidden Character Analysis Results:")
    
    suspicious_chars = []
    char_counts = {}
    
    # Define problematic Unicode characters
    problematic_chars = {
        '\u200b': 'Zero Width Space',
        '\u200c': 'Zero Width Non-Joiner',
        '\u200d': 'Zero Width Joiner',
        '\u2060': 'Word Joiner',
        '\ufeff': 'Zero Width No-Break Space (BOM)',
        '\u00a0': 'Non-Breaking Space',
        '\u2009': 'Thin Space',
        '\u2014': 'Em Dash',
        '\u2013': 'En Dash',
        '\u201c': 'Left Double Quotation Mark',
        '\u201d': 'Right Double Quotation Mark',
        '\u2018': 'Left Single Quotation Mark',
        '\u2019': 'Right Single Quotation Mark',
    }
    
    # Analyze each character
    for i, char in enumerate(text):
        # Check for problematic characters
        if char in problematic_chars:
            suspicious_chars.append({
                'char': char,
                'name': problematic_chars[char],
                'position': i,
                'unicode': f'U+{ord(char):04X}'
            })
        
        # Count character categories
        category = unicodedata.category(char)
        char_counts[category] = char_counts.get(category, 0) + 1
        
        # Check for control characters
        if category.startswith('C') and char not in ['\n', '\r', '\t']:
            suspicious_chars.append({
                'char': repr(char),
                'name': f'Control Character ({category})',
                'position': i,
                'unicode': f'U+{ord(char):04X}'
            })
    
    # Display results
    print(f"{Fore.GREEN}Text Length: {Fore.WHITE}{len(text)} characters")
    
    if suspicious_chars:
        print(f"{Fore.RED}⚠ Found {len(suspicious_chars)} suspicious characters:")
        for char_info in suspicious_chars:
            print(f"  {Fore.YELLOW}Position {char_info['position']}: {Fore.WHITE}{char_info['name']} "
                  f"{Fore.CYAN}({char_info['unicode']})")
    else:
        print(f"{Fore.GREEN}✓ No suspicious hidden characters found")
    
    print(f"\n{Fore.CYAN}Character Categories:")
    for category, count in sorted(char_counts.items()):
        category_name = {
            'Ll': 'Lowercase Letters',
            'Lu': 'Uppercase Letters',
            'Lt': 'Titlecase Letters',
            'Nd': 'Decimal Numbers',
            'Nl': 'Letter Numbers',
            'No': 'Other Numbers',
            'Pc': 'Connector Punctuation',
            'Pd': 'Dash Punctuation',
            'Pe': 'Close Punctuation',
            'Pf': 'Final Punctuation',
            'Pi': 'Initial Punctuation',
            'Po': 'Other Punctuation',
            'Ps': 'Open Punctuation',
            'Sc': 'Currency Symbols',
            'Sk': 'Modifier Symbols',
            'Sm': 'Math Symbols',
            'So': 'Other Symbols',
            'Zl': 'Line Separators',
            'Zp': 'Paragraph Separators',
            'Zs': 'Space Separators',
            'Cc': 'Control Characters',
            'Cf': 'Format Characters',
            'Cn': 'Unassigned',
            'Co': 'Private Use',
            'Cs': 'Surrogate'
        }.get(category, category)
        
        color = Fore.RED if category.startswith('C') else Fore.WHITE
        print(f"  {Fore.CYAN}{category_name}: {color}{count}")
    
    # Return analysis data for potential export (Issue 8)
    return {
        'text_length': len(text),
        'suspicious_chars': suspicious_chars,
        'char_counts': char_counts,
        'original_text': text
    }

def export_hidden_char_analysis(analysis_data, source_description="Text Input"):
    """Export hidden character analysis results to file (Issue 8)"""
    try:
        from datetime import datetime
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"hidden_char_analysis_{timestamp}.txt"
        
        # Use new output directory structure
        try:
            from pengu import get_output_path
            full_path = get_output_path("reports", filename)
        except:
            # Fallback if import fails
            full_path = filename
        
        content = f"""Hidden Character Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source: {source_description}
{'='*60}

ANALYSIS SUMMARY
Text Length: {analysis_data['text_length']} characters
Suspicious Characters Found: {len(analysis_data['suspicious_chars'])}

"""
        
        if analysis_data['suspicious_chars']:
            content += "SUSPICIOUS CHARACTERS DETECTED:\n"
            content += "-" * 40 + "\n"
            for char_info in analysis_data['suspicious_chars']:
                content += f"Position {char_info['position']:4d}: {char_info['name']} ({char_info['unicode']})\n"
        else:
            content += "✓ No suspicious hidden characters found\n"
        
        content += f"\nCHARACTER CATEGORIES:\n"
        content += "-" * 40 + "\n"
        
        category_names = {
            'Ll': 'Lowercase Letters',
            'Lu': 'Uppercase Letters',
            'Lt': 'Titlecase Letters',
            'Nd': 'Decimal Numbers',
            'Nl': 'Letter Numbers',
            'No': 'Other Numbers',
            'Pc': 'Connector Punctuation',
            'Pd': 'Dash Punctuation',
            'Pe': 'Close Punctuation',
            'Pf': 'Final Punctuation',
            'Pi': 'Initial Punctuation',
            'Po': 'Other Punctuation',
            'Ps': 'Open Punctuation',
            'Sc': 'Currency Symbols',
            'Sk': 'Modifier Symbols',
            'Sm': 'Math Symbols',
            'So': 'Other Symbols',
            'Zl': 'Line Separators',
            'Zp': 'Paragraph Separators',
            'Zs': 'Space Separators',
            'Cc': 'Control Characters',
            'Cf': 'Format Characters',
            'Cn': 'Unassigned',
            'Co': 'Private Use',
            'Cs': 'Surrogate'
        }
        
        for category, count in sorted(analysis_data['char_counts'].items()):
            category_name = category_names.get(category, category)
            warning = " ⚠" if category.startswith('C') else ""
            content += f"{category_name:25}: {count:6d}{warning}\n"
        
        content += f"\nRECOMMENDATIONS:\n"
        content += "-" * 40 + "\n"
        if analysis_data['suspicious_chars']:
            content += "• Review the detected suspicious characters\n"
            content += "• Consider using the 'Clean text' option to remove problematic characters\n"
            content += "• Be cautious of potential data exfiltration or steganographic content\n"
        else:
            content += "• No immediate concerns with hidden characters\n"
            content += "• Text appears to be clean of problematic Unicode characters\n"
        
        content += f"\nReport generated by Pengu v2.1 Hidden Character Analysis\n"
        
        # Write with UTF-8 encoding
        with open(full_path, 'w', encoding='utf-8', errors='replace') as f:
            f.write(content)
        
        print(f"{Fore.GREEN}✓ Hidden character analysis exported to: {full_path}")
        return True
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting analysis: {e}")
        return False
        category_name = {
            'Ll': 'Lowercase Letters',
            'Lu': 'Uppercase Letters',
            'Lt': 'Titlecase Letters',
            'Nd': 'Decimal Numbers',
            'Nl': 'Letter Numbers',
            'No': 'Other Numbers',
            'Pc': 'Connector Punctuation',
            'Pd': 'Dash Punctuation',
            'Pe': 'Close Punctuation',
            'Pf': 'Final Punctuation',
            'Pi': 'Initial Punctuation',
            'Po': 'Other Punctuation',
            'Ps': 'Open Punctuation',
            'Sc': 'Currency Symbols',
            'Sk': 'Modifier Symbols',
            'Sm': 'Math Symbols',
            'So': 'Other Symbols',
            'Zl': 'Line Separators',
            'Zp': 'Paragraph Separators',
            'Zs': 'Space Separators',
            'Cc': 'Control Characters',
            'Cf': 'Format Characters',
            'Cn': 'Unassigned',
            'Co': 'Private Use',
            'Cs': 'Surrogate'
        }.get(category, category)
        
        color = Fore.RED if category.startswith('C') else Fore.WHITE
        print(f"  {Fore.CYAN}{category_name}: {color}{count}")

def clean_hidden_chars(text):
    """Remove hidden and problematic characters from text"""
    # Characters to remove
    chars_to_remove = [
        '\u200b',  # Zero Width Space
        '\u200c',  # Zero Width Non-Joiner
        '\u200d',  # Zero Width Joiner
        '\u2060',  # Word Joiner
        '\ufeff',  # Zero Width No-Break Space (BOM)
    ]
    
    # Characters to replace
    chars_to_replace = {
        '\u00a0': ' ',  # Non-Breaking Space -> Regular Space
        '\u2009': ' ',  # Thin Space -> Regular Space
        '\u2014': '-',  # Em Dash -> Hyphen
        '\u2013': '-',  # En Dash -> Hyphen
        '\u201c': '"',  # Left Double Quotation Mark
        '\u201d': '"',  # Right Double Quotation Mark
        '\u2018': "'",  # Left Single Quotation Mark
        '\u2019': "'",  # Right Single Quotation Mark
    }
    
    cleaned = text
    
    # Remove problematic characters
    for char in chars_to_remove:
        cleaned = cleaned.replace(char, '')
    
    # Replace problematic characters
    for old_char, new_char in chars_to_replace.items():
        cleaned = cleaned.replace(old_char, new_char)
    
    # Remove other control characters (except common ones like \n, \r, \t)
    cleaned = ''.join(char for char in cleaned 
                     if unicodedata.category(char)[0] != 'C' or char in '\n\r\t')
    
    return cleaned

def main():
    """Main function for encoding/decoding utilities"""
    print_banner()
    
    while True:
        print(f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════╗
{Fore.MAGENTA}║                    {Fore.CYAN}Utility Menu{Fore.MAGENTA}                         ║
{Fore.MAGENTA}╚══════════════════════════════════════════════════════════╝

{Fore.GREEN}1. {Fore.WHITE}Base64 Operations
{Fore.GREEN}2. {Fore.WHITE}URL Encoding/Decoding
{Fore.GREEN}3. {Fore.WHITE}HTML Encoding/Decoding
{Fore.GREEN}4. {Fore.WHITE}Hash Generation
{Fore.GREEN}5. {Fore.WHITE}Hidden Character Analysis
{Fore.GREEN}6. {Fore.WHITE}Exit to main menu
""")
        
        choice = input(f"{Fore.YELLOW}Select option (1-6): ").strip()
        
        if choice == '1':
            base64_operations()
        elif choice == '2':
            url_operations()
        elif choice == '3':
            html_operations()
        elif choice == '4':
            hash_operations()
        elif choice == '5':
            hidden_character_analysis()
        elif choice == '6':
            print(f"{Fore.GREEN}Returning to main menu...")
            break
        else:
            print(f"{Fore.RED}Invalid option. Please select 1-6.")

if __name__ == "__main__":
    main()