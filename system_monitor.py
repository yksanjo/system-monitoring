"""
System Monitoring Tool

This script provides tools for monitoring system resources and development workflows.
Features include:
- CPU, memory, and disk usage monitoring
- Process monitoring
- Log analysis
- Performance tracking
"""

import psutil
import time
import json
import argparse
import csv
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import os
import re


class SystemMonitor:
    """
    A class to monitor system resources and performance.
    """
    
    def __init__(self):
        self.monitoring_data = []
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get current system information.
        
        Returns:
            Dictionary containing system information
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": psutil.cpu_percent(interval=1),
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
                "used": psutil.virtual_memory().used
            },
            "disk": {
                "total": psutil.disk_usage('/').total,
                "used": psutil.disk_usage('/').used,
                "free": psutil.disk_usage('/').free,
                "percent": psutil.disk_usage('/').percent
            },
            "network": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            }
        }
    
    def monitor_system(self, duration: int = 60, interval: int = 5) -> List[Dict[str, Any]]:
        """
        Monitor system resources for a specified duration.
        
        Args:
            duration: Duration to monitor in seconds
            interval: Interval between measurements in seconds
            
        Returns:
            List of system information snapshots
        """
        self.monitoring_data = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            snapshot = self.get_system_info()
            self.monitoring_data.append(snapshot)
            print(f"Recorded system snapshot at {snapshot['timestamp']}")
            time.sleep(interval)
        
        return self.monitoring_data
    
    def get_process_info(self, name_pattern: str = None) -> List[Dict[str, Any]]:
        """
        Get information about running processes.
        
        Args:
            name_pattern: Optional pattern to filter processes by name
            
        Returns:
            List of process information
        """
        processes = []
        
        for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'create_time']):
            try:
                pinfo = proc.info
                
                # Filter by name pattern if provided
                if name_pattern and not re.search(name_pattern, pinfo['name'], re.IGNORECASE):
                    continue
                
                processes.append({
                    "pid": pinfo['pid'],
                    "name": pinfo['name'],
                    "username": pinfo['username'],
                    "cpu_percent": pinfo['cpu_percent'],
                    "memory_percent": pinfo['memory_percent'],
                    "create_time": datetime.fromtimestamp(pinfo['create_time']).isoformat()
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # Process may have terminated during iteration
                pass
        
        return processes
    
    def get_top_processes(self, count: int = 10, resource: str = "cpu") -> List[Dict[str, Any]]:
        """
        Get top processes by CPU or memory usage.
        
        Args:
            count: Number of top processes to return
            resource: Resource to sort by ('cpu' or 'memory')
            
        Returns:
            List of top processes
        """
        processes = self.get_process_info()
        
        if resource == "cpu":
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        elif resource == "memory":
            processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        else:
            raise ValueError("Resource must be 'cpu' or 'memory'")
        
        return processes[:count]
    
    def save_monitoring_data(self, filename: str) -> None:
        """
        Save monitoring data to a file.
        
        Args:
            filename: Name of the file to save data to
        """
        filepath = Path(filename)
        
        if filepath.suffix.lower() == '.json':
            with open(filepath, 'w') as f:
                json.dump(self.monitoring_data, f, indent=2)
        elif filepath.suffix.lower() == '.csv':
            if not self.monitoring_data:
                return
            
            with open(filepath, 'w', newline='') as f:
                fieldnames = list(self.monitoring_data[0].keys()) + list(self.monitoring_data[0]['memory'].keys()) + list(self.monitoring_data[0]['disk'].keys()) + list(self.monitoring_data[0]['network'].keys())
                # Remove nested keys and add flattened versions
                fieldnames = [f for f in fieldnames if f not in ['memory', 'disk', 'network']]
                fieldnames.extend(['memory_total', 'memory_available', 'memory_percent', 'memory_used'])
                fieldnames.extend(['disk_total', 'disk_used', 'disk_free', 'disk_percent'])
                fieldnames.extend(['network_bytes_sent', 'network_bytes_recv'])
                
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                
                for row in self.monitoring_data:
                    flat_row = {k: v for k, v in row.items() if k not in ['memory', 'disk', 'network']}
                    flat_row.update({f"memory_{k}": v for k, v in row['memory'].items()})
                    flat_row.update({f"disk_{k}": v for k, v in row['disk'].items()})
                    flat_row.update({f"network_{k}": v for k, v in row['network'].items()})
                    writer.writerow(flat_row)
    
    def analyze_logs(self, log_path: str, pattern: str = None) -> Dict[str, Any]:
        """
        Analyze log files for specific patterns or errors.
        
        Args:
            log_path: Path to the log file
            pattern: Optional pattern to search for
            
        Returns:
            Dictionary containing log analysis results
        """
        log_path = Path(log_path)
        if not log_path.exists():
            return {"error": f"Log file {log_path} does not exist"}
        
        # Common error patterns
        error_patterns = [
            r'error',
            r'exception',
            r'fail',
            r'traceback',
            r'critical',
            r'fatal'
        ]
        
        if pattern:
            error_patterns.append(pattern)
        
        results = {
            "file": str(log_path),
            "total_lines": 0,
            "error_lines": 0,
            "errors": [],
            "error_patterns_found": {}
        }
        
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                results["total_lines"] += 1
                line_lower = line.lower()
                
                for pattern in error_patterns:
                    if re.search(pattern, line_lower, re.IGNORECASE):
                        results["error_lines"] += 1
                        results["errors"].append({
                            "line_number": line_num,
                            "line": line.strip(),
                            "pattern": pattern
                        })
                        
                        if pattern not in results["error_patterns_found"]:
                            results["error_patterns_found"][pattern] = 0
                        results["error_patterns_found"][pattern] += 1
        
        return results


class WorkflowMonitor:
    """
    A class to monitor development workflows.
    """
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path).resolve()
        self.git_enabled = (self.project_path / ".git").exists()
    
    def get_git_status(self) -> Dict[str, Any]:
        """
        Get Git repository status if available.
        
        Returns:
            Dictionary containing Git status information
        """
        if not self.git_enabled:
            return {"error": "Not a Git repository"}
        
        try:
            import subprocess
            # Get current branch
            branch_result = subprocess.run(
                ["git", "branch", "--show-current"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            current_branch = branch_result.stdout.strip() if branch_result.returncode == 0 else "unknown"
            
            # Get status
            status_result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            has_changes = bool(status_result.stdout.strip())
            
            # Get last commit
            last_commit_result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%h - %an, %ar : %s"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            last_commit = last_commit_result.stdout.strip() if last_commit_result.returncode == 0 else "unknown"
            
            return {
                "branch": current_branch,
                "has_changes": has_changes,
                "last_commit": last_commit
            }
        except Exception as e:
            return {"error": f"Error getting Git status: {str(e)}"}
    
    def get_project_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the project.
        
        Returns:
            Dictionary containing project statistics
        """
        stats = {
            "total_files": 0,
            "total_lines": 0,
            "file_types": {},
            "largest_files": []
        }
        
        # Walk through all files in the project
        all_files = []
        for file_path in self.project_path.rglob("*"):
            if file_path.is_file() and not any(part.startswith('.') for part in file_path.parts):
                all_files.append(file_path)
        
        for file_path in all_files:
            stats["total_files"] += 1
            
            # Count file types
            ext = file_path.suffix.lower()
            if ext in stats["file_types"]:
                stats["file_types"][ext] += 1
            else:
                stats["file_types"][ext] = 1
            
            # Count lines if it's a text file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = sum(1 for _ in f)
                    stats["total_lines"] += lines
                    # Track largest files
                    stats["largest_files"].append({
                        "path": str(file_path.relative_to(self.project_path)),
                        "lines": lines
                    })
            except:
                # Skip binary files or files that can't be read
                pass
        
        # Sort largest files and keep top 10
        stats["largest_files"].sort(key=lambda x: x["lines"], reverse=True)
        stats["largest_files"] = stats["largest_files"][:10]
        
        return stats


class SystemMonitoringTool:
    """
    Main class for system monitoring.
    """
    
    def __init__(self):
        self.system_monitor = SystemMonitor()
    
    def run_system_monitor(self, duration: int = 60, interval: int = 5, output_file: str = None) -> List[Dict[str, Any]]:
        """
        Run system monitoring for specified duration.
        
        Args:
            duration: Duration to monitor in seconds
            interval: Interval between measurements in seconds
            output_file: Optional file to save results
            
        Returns:
            List of system information snapshots
        """
        print(f"Starting system monitoring for {duration} seconds (interval: {interval}s)...")
        data = self.system_monitor.monitor_system(duration, interval)
        
        if output_file:
            self.system_monitor.save_monitoring_data(output_file)
            print(f"Monitoring data saved to {output_file}")
        
        return data
    
    def show_top_processes(self, count: int = 10, resource: str = "cpu") -> List[Dict[str, Any]]:
        """
        Show top processes by CPU or memory usage.
        
        Args:
            count: Number of top processes to show
            resource: Resource to sort by ('cpu' or 'memory')
            
        Returns:
            List of top processes
        """
        processes = self.system_monitor.get_top_processes(count, resource)
        
        print(f"Top {count} processes by {resource.upper()} usage:")
        print("-" * 80)
        print(f"{'PID':<8} {'Name':<25} {'User':<15} {resource.upper():<8} Mem%")
        print("-" * 80)
        
        for proc in processes:
            print(f"{proc['pid']:<8} {proc['name'][:24]:<25} {proc['username'] or 'N/A':<15} {proc[f'{resource}_percent']:<8.1f} {proc['memory_percent']:<5.1f}")
        
        return processes
    
    def analyze_log_file(self, log_path: str, pattern: str = None) -> Dict[str, Any]:
        """
        Analyze a log file for errors or specific patterns.
        
        Args:
            log_path: Path to the log file
            pattern: Optional pattern to search for
            
        Returns:
            Dictionary containing log analysis results
        """
        results = self.system_monitor.analyze_logs(log_path, pattern)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            return results
        
        print(f"Log Analysis for: {results['file']}")
        print(f"Total lines: {results['total_lines']}")
        print(f"Error lines: {results['error_lines']}")
        print(f"Error rate: {results['error_lines']/results['total_lines']*100:.2f}%")
        
        if results['error_patterns_found']:
            print("\nError patterns found:")
            for pattern, count in results['error_patterns_found'].items():
                print(f"  {pattern}: {count} occurrences")
        
        if results['errors']:
            print(f"\nFirst few errors:")
            for error in results['errors'][:5]:  # Show first 5 errors
                print(f"  Line {error['line_number']}: {error['line']}")
        
        return results
    
    def monitor_workflow(self, project_path: str = ".") -> Dict[str, Any]:
        """
        Monitor development workflow in a project.
        
        Args:
            project_path: Path to the project directory
            
        Returns:
            Dictionary containing workflow information
        """
        workflow_monitor = WorkflowMonitor(project_path)
        
        # Get Git status if available
        git_status = workflow_monitor.get_git_status()
        
        # Get project statistics
        project_stats = workflow_monitor.get_project_stats()
        
        results = {
            "git_status": git_status,
            "project_stats": project_stats,
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"Workflow monitoring for: {project_path}")
        print("=" * 50)
        
        if "error" not in git_status:
            print(f"Git branch: {git_status['branch']}")
            print(f"Has uncommitted changes: {git_status['has_changes']}")
            print(f"Last commit: {git_status['last_commit']}")
        
        print(f"\nProject stats:")
        print(f"  Total files: {project_stats['total_files']}")
        print(f"  Total lines: {project_stats['total_lines']}")
        
        print(f"\nFile types:")
        for ext, count in sorted(project_stats['file_types'].items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {ext or 'no extension'}: {count}")
        
        print(f"\nLargest files:")
        for file_info in project_stats['largest_files'][:5]:
            print(f"  {file_info['path']}: {file_info['lines']} lines")
        
        return results


def main():
    """
    Main function to demonstrate the SystemMonitoringTool capabilities.
    """
    parser = argparse.ArgumentParser(description='System Monitoring Tool')
    parser.add_argument('command', choices=['system', 'processes', 'log', 'workflow'], 
                       help='Command to execute')
    parser.add_argument('--duration', type=int, default=60, help='Duration for system monitoring in seconds')
    parser.add_argument('--interval', type=int, default=5, help='Interval between measurements in seconds')
    parser.add_argument('--output', help='Output file for monitoring data')
    parser.add_argument('--count', type=int, default=10, help='Number of top processes to show')
    parser.add_argument('--resource', choices=['cpu', 'memory'], default='cpu', help='Resource to sort processes by')
    parser.add_argument('--log-path', help='Path to log file for analysis')
    parser.add_argument('--pattern', help='Pattern to search for in logs')
    parser.add_argument('--project-path', default='.', help='Path to project for workflow monitoring')
    
    args = parser.parse_args()
    
    monitor = SystemMonitoringTool()
    
    if args.command == 'system':
        monitor.run_system_monitor(
            duration=args.duration,
            interval=args.interval,
            output_file=args.output
        )
    
    elif args.command == 'processes':
        monitor.show_top_processes(
            count=args.count,
            resource=args.resource
        )
    
    elif args.command == 'log':
        if not args.log_path:
            print("Error: --log-path is required for log analysis")
            return
        
        monitor.analyze_log_file(
            log_path=args.log_path,
            pattern=args.pattern
        )
    
    elif args.command == 'workflow':
        monitor.monitor_workflow(
            project_path=args.project_path
        )


if __name__ == "__main__":
    main()