#!/usr/bin/env python3
"""
Command-line interface for the System Monitoring Tool.
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from system_monitoring.system_monitor import SystemMonitoringTool


def main():
    """
    Main CLI function for the system monitoring tool.
    """
    if len(sys.argv) < 2:
        print("Usage: sys_mon_tool.py <command> [options]")
        print("Commands:")
        print("  system     - Monitor system resources")
        print("  processes  - Show top processes by resource usage")
        print("  log        - Analyze log files")
        print("  workflow   - Monitor development workflow")
        print("")
        print("Options:")
        print("  --duration SECONDS    - Duration for system monitoring [default: 60]")
        print("  --interval SECONDS  - Interval between measurements [default: 5]")
        print("  --output FILE       - Output file for monitoring data")
        print("  --count N           - Number of top processes to show [default: 10]")
        print("  --resource RESOURCE - Resource to sort by (cpu, memory) [default: cpu]")
        print("  --log-path PATH     - Path to log file for analysis")
        print("  --pattern PATTERN   - Pattern to search for in logs")
        print("  --project-path PATH - Path to project for workflow monitoring [default: .]")
        return

    command = sys.argv[1]
    monitor = SystemMonitoringTool()
    
    # Parse options
    duration = 60
    interval = 5
    output = None
    count = 10
    resource = "cpu"
    log_path = None
    pattern = None
    project_path = "."
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == "--duration" and i + 1 < len(sys.argv):
            try:
                duration = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Error: Invalid duration: {sys.argv[i + 1]}")
                return
        elif sys.argv[i] == "--interval" and i + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Error: Invalid interval: {sys.argv[i + 1]}")
                return
        elif sys.argv[i] == "--output" and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--count" and i + 1 < len(sys.argv):
            try:
                count = int(sys.argv[i + 1])
                i += 2
            except ValueError:
                print(f"Error: Invalid count: {sys.argv[i + 1]}")
                return
        elif sys.argv[i] == "--resource" and i + 1 < len(sys.argv):
            if sys.argv[i + 1] in ["cpu", "memory"]:
                resource = sys.argv[i + 1]
                i += 2
            else:
                print(f"Error: Invalid resource: {sys.argv[i + 1]}. Use 'cpu' or 'memory'.")
                return
        elif sys.argv[i] == "--log-path" and i + 1 < len(sys.argv):
            log_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--pattern" and i + 1 < len(sys.argv):
            pattern = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--project-path" and i + 1 < len(sys.argv):
            project_path = sys.argv[i + 1]
            i += 2
        else:
            print(f"Unknown option: {sys.argv[i]}")
            return
    
    if command == "system":
        monitor.run_system_monitor(
            duration=duration,
            interval=interval,
            output_file=output
        )
    
    elif command == "processes":
        monitor.show_top_processes(
            count=count,
            resource=resource
        )
    
    elif command == "log":
        if not log_path:
            print("Error: --log-path is required for log analysis")
            return
        
        monitor.analyze_log_file(
            log_path=log_path,
            pattern=pattern
        )
    
    elif command == "workflow":
        monitor.monitor_workflow(
            project_path=project_path
        )
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()