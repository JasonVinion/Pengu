#!/usr/bin/env python3
"""
Pengu Session Logger - Master logging system for all tool usage
"""

import os
import json
import tempfile
from datetime import datetime
from colorama import init, Fore, Style

init(autoreset=True)

class SessionLogger:
    """Session logger to track all tool usage during a session"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.temp_dir = tempfile.gettempdir()
        self.temp_log_file = os.path.join(self.temp_dir, f"pengu_session_{self.session_id}.json")
        self.session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "tools_used": [],
            "session_summary": {
                "total_tools_run": 0,
                "unique_tools": set(),
                "total_duration": 0
            }
        }
        self._create_temp_log()
    
    def _create_temp_log(self):
        """Create initial temporary log file"""
        try:
            with open(self.temp_log_file, 'w') as f:
                # Convert set to list for JSON serialization
                data_copy = self.session_data.copy()
                data_copy["session_summary"]["unique_tools"] = list(data_copy["session_summary"]["unique_tools"])
                json.dump(data_copy, f, indent=2)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not create session log: {e}")
    
    def log_tool_usage(self, tool_name, details):
        """Log tool usage with important details"""
        timestamp = datetime.now().isoformat()
        tool_entry = {
            "tool": tool_name,
            "timestamp": timestamp,
            "details": details
        }
        
        self.session_data["tools_used"].append(tool_entry)
        self.session_data["session_summary"]["total_tools_run"] += 1
        
        # Ensure unique_tools is a set
        if isinstance(self.session_data["session_summary"]["unique_tools"], list):
            self.session_data["session_summary"]["unique_tools"] = set(self.session_data["session_summary"]["unique_tools"])
        
        self.session_data["session_summary"]["unique_tools"].add(tool_name)
        
        # Update temp log
        self._update_temp_log()
    
    def _update_temp_log(self):
        """Update the temporary log file"""
        try:
            # Convert set to list for JSON serialization
            data_copy = self.session_data.copy()
            data_copy["session_summary"]["unique_tools"] = list(data_copy["session_summary"]["unique_tools"])
            
            with open(self.temp_log_file, 'w') as f:
                json.dump(data_copy, f, indent=2)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not update session log: {e}")
    
    def finalize_session(self):
        """Finalize session with end time"""
        self.session_data["end_time"] = datetime.now().isoformat()
        start_time = datetime.fromisoformat(self.session_data["start_time"])
        end_time = datetime.fromisoformat(self.session_data["end_time"])
        self.session_data["session_summary"]["total_duration"] = (end_time - start_time).total_seconds()
        self._update_temp_log()
    
    def save_session_log(self, custom_title=None):
        """Save session log permanently with user-specified title"""
        try:
            # Finalize session
            self.finalize_session()
            
            # Create filename
            date_part = datetime.now().strftime("%Y-%m-%d-%H%M%S")
            if custom_title:
                # Sanitize title for filename
                safe_title = "".join(c for c in custom_title if c.isalnum() or c in " -_").strip()
                safe_title = safe_title.replace(" ", "_")
                filename = f"{date_part}_{safe_title}_pengu_session.json"
            else:
                filename = f"{date_part}_pengu_session.json"
            
            # Save to current directory
            permanent_file = os.path.join(os.getcwd(), filename)
            
            # Convert set to list for JSON serialization
            data_copy = self.session_data.copy()
            data_copy["session_summary"]["unique_tools"] = list(data_copy["session_summary"]["unique_tools"])
            
            with open(permanent_file, 'w') as f:
                json.dump(data_copy, f, indent=2)
            
            print(f"{Fore.GREEN}✓ Session log saved as: {permanent_file}")
            return permanent_file
            
        except Exception as e:
            print(f"{Fore.RED}Error saving session log: {e}")
            return None
    
    def get_session_summary(self):
        """Get current session summary"""
        unique_tools = list(self.session_data["session_summary"]["unique_tools"])
        return {
            "session_id": self.session_id,
            "tools_run": self.session_data["session_summary"]["total_tools_run"],
            "unique_tools": unique_tools,
            "temp_log_location": self.temp_log_file
        }
    
    def cleanup_temp_log(self):
        """Clean up temporary log file"""
        try:
            if os.path.exists(self.temp_log_file):
                os.remove(self.temp_log_file)
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not clean up temp log: {e}")

# Global session logger instance
session_logger = None

def get_session_logger():
    """Get or create global session logger"""
    global session_logger
    if session_logger is None:
        session_logger = SessionLogger()
    return session_logger

def log_tool_usage(tool_name, details):
    """Convenience function to log tool usage"""
    logger = get_session_logger()
    logger.log_tool_usage(tool_name, details)

def show_save_log_menu():
    """Show menu to save session log"""
    logger = get_session_logger()
    
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════╗
{Fore.CYAN}║                {Fore.MAGENTA}Save Session Log{Fore.CYAN}                      ║
{Fore.CYAN}╚══════════════════════════════════════════════════════╝

{Fore.GREEN}Current Session Summary:
{Fore.CYAN}  Session ID:       {Fore.WHITE}{logger.session_id}
{Fore.CYAN}  Tools Run:        {Fore.WHITE}{logger.session_data['session_summary']['total_tools_run']}
{Fore.CYAN}  Unique Tools:     {Fore.WHITE}{', '.join(logger.session_data['session_summary']['unique_tools'])}
{Fore.CYAN}  Temp Log:         {Fore.WHITE}{logger.temp_log_file}
""")
    
    while True:
        save_choice = input(f"{Fore.YELLOW}Would you like to save this session log? (y/N): ").strip().lower()
        
        if save_choice in ['y', 'yes']:
            title = input(f"{Fore.YELLOW}Enter a title for this session (optional): ").strip()
            saved_file = logger.save_session_log(title if title else None)
            if saved_file:
                print(f"{Fore.GREEN}Session log saved successfully!")
                
                # Ask about cleaning temp log
                clean_choice = input(f"{Fore.YELLOW}Clean up temporary log? (Y/n): ").strip().lower()
                if clean_choice not in ['n', 'no']:
                    logger.cleanup_temp_log()
                    print(f"{Fore.GREEN}Temporary log cleaned up.")
            break
        elif save_choice in ['n', 'no', '']:
            print(f"{Fore.YELLOW}Session log not saved. Temporary log will be deleted when Pengu exits.")
            break
        else:
            print(f"{Fore.RED}Please enter 'y' or 'n'")

def main():
    """Test function for session logger"""
    logger = get_session_logger()
    
    # Simulate some tool usage
    logger.log_tool_usage("ping", {
        "target": "google.com",
        "packets_sent": 10,
        "packets_received": 10,
        "avg_response_time": 25.5
    })
    
    logger.log_tool_usage("port_scan", {
        "target": "192.168.1.1",
        "ports_scanned": 1000,
        "open_ports": [22, 80, 443],
        "scan_duration": 45.2
    })
    
    # Show summary
    summary = logger.get_session_summary()
    print(f"Session Summary: {summary}")
    
    # Save log
    show_save_log_menu()

if __name__ == "__main__":
    main()