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
    """Enhanced session logger with real-time logging and dedicated output directory (Issue 10)"""
    
    def __init__(self):
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Use dedicated output directory structure (Issue 10)
        self.output_dir = "pengu_output"
        self.logs_dir = os.path.join(self.output_dir, "logs")
        
        # Create output directories if they don't exist
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Real-time log file in dedicated directory
        self.log_file = os.path.join(self.logs_dir, f"session_{self.session_id}.log")
        
        self.session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "commands_executed": [],
            "tools_used": [],
            "reports_generated": [],
            "session_summary": {
                "total_commands": 0,
                "total_tools_run": 0,
                "unique_tools": set(),
                "total_duration": 0
            }
        }
        self._initialize_log_file()
    
    def _initialize_log_file(self):
        """Initialize log file with session start information (Issue 10)"""
        try:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                f.write(f"PENGU SESSION LOG\n")
                f.write(f"{'=' * 50}\n")
                f.write(f"Session ID: {self.session_id}\n")
                f.write(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Log File: {self.log_file}\n")
                f.write(f"{'=' * 50}\n\n")
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not initialize session log: {e}")
    
    def log_command(self, command, output=None):
        """Log user commands in real-time (Issue 10)"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] COMMAND: {command}\n")
                if output:
                    f.write(f"[{timestamp}] OUTPUT: {output}\n")
                f.write(f"{'-' * 30}\n")
            
            # Update session data
            self.session_data["commands_executed"].append({
                "timestamp": timestamp,
                "command": command,
                "output": output if output else "No output captured"
            })
            self.session_data["session_summary"]["total_commands"] += 1
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not log command: {e}")
    
    def log_tool_usage(self, tool_name, details):
        """Log tool usage with comprehensive details in real-time (Issue 10)"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] TOOL: {tool_name}\n")
                f.write(f"[{timestamp}] DETAILS: {details}\n")
                f.write(f"{'-' * 30}\n")
            
            # Update session data
            tool_entry = {
                "tool": tool_name,
                "timestamp": timestamp,
                "details": details
            }
            
            self.session_data["tools_used"].append(tool_entry)
            self.session_data["session_summary"]["total_tools_run"] += 1
            self.session_data["session_summary"]["unique_tools"].add(tool_name)
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not log tool usage: {e}")
    
    def log_report_generation(self, report_type, report_path, content_summary=None):
        """Log report generation in real-time (Issue 10)"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"[{timestamp}] REPORT GENERATED: {report_type}\n")
                f.write(f"[{timestamp}] REPORT PATH: {report_path}\n")
                if content_summary:
                    f.write(f"[{timestamp}] CONTENT SUMMARY: {content_summary}\n")
                f.write(f"{'-' * 30}\n")
            
            # Update session data
            self.session_data["reports_generated"].append({
                "timestamp": timestamp,
                "report_type": report_type,
                "report_path": report_path,
                "content_summary": content_summary or "No summary provided"
            })
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not log report generation: {e}")
    
    def finalize_session(self):
        """Finalize session with end time and summary (Issue 10)"""
        try:
            end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"\n{'=' * 50}\n")
                f.write(f"SESSION ENDED: {end_time}\n")
                f.write(f"TOTAL COMMANDS: {self.session_data['session_summary']['total_commands']}\n")
                f.write(f"TOTAL TOOLS USED: {self.session_data['session_summary']['total_tools_run']}\n")
                f.write(f"UNIQUE TOOLS: {len(self.session_data['session_summary']['unique_tools'])}\n")
                f.write(f"REPORTS GENERATED: {len(self.session_data['reports_generated'])}\n")
                f.write(f"{'=' * 50}\n")
            
            return self.log_file
            
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not finalize session log: {e}")
            return None

# Global session logger instance
session_logger = None

def get_session_logger():
    """Get or create global session logger instance"""
    global session_logger
    if session_logger is None:
        session_logger = SessionLogger()
    return session_logger

def log_tool_usage(tool_name, details):
    """Global function to log tool usage"""
    logger = get_session_logger()
    logger.log_tool_usage(tool_name, details)

def log_command(command, output=None):
    """Global function to log commands"""
    logger = get_session_logger()
    logger.log_command(command, output)

def log_report_generation(report_type, report_path, content_summary=None):
    """Global function to log report generation"""
    logger = get_session_logger()
    logger.log_report_generation(report_type, report_path, content_summary)

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