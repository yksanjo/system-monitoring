# System Monitoring

[![GitHub](https://img.shields.io/badge/GitHub-yksanjo%2Fsystem--monitoring-181717?logo=github)](https://github.com/yksanjo/system-monitoring)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![System](https://img.shields.io/badge/system-monitoring-95a5a6.svg?logo=linux)](https://shields.io/)
[![Status](https://img.shields.io/badge/status-stable-success.svg)](https://shields.io/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> Comprehensive system monitoring and workflow tracking tools

## 🚀 Overview

System Monitoring is a comprehensive suite of utilities for monitoring system resources, analyzing logs, tracking development workflows, and maintaining system health. These tools help developers understand system performance and identify potential issues before they become critical.

## ✨ Features

- **Resource Monitoring**: CPU, memory, disk, and network usage tracking
- **Process Monitoring**: Top processes identification by resource usage
- **Log Analysis**: Error detection and pattern matching in log files
- **Workflow Tracking**: Development workflow and project statistics
- **Data Export**: JSON and CSV export for analysis
- **Command-Line Interface**: Easy-to-use CLI for automation scripts

## 📸 Screenshots

![System Monitoring Demo](https://placehold.co/800x400/4a5568/ffffff?text=System+Monitoring+Demo)

*Example of system resource monitoring output*

![Process Monitoring](https://placehold.co/800x400/2d3748/ffffff?text=Process+Monitoring+Features)

*Top processes by CPU and memory usage*

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/yksanjo/system-monitoring.git
   cd system-monitoring
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install system monitoring dependencies:
   ```bash
   pip install psutil
   ```

4. The tools are now ready to use from the command line.

### Standalone Installation

You can also install the tools as a standalone package:

```bash
pip install system-monitoring
```

## 🎮 Usage

### Command-Line Interface

The tool provides a command-line interface for all operations:

#### Monitor System Resources

Monitor system resources for 5 minutes with 10-second intervals:

```bash
python sys_mon_tool.py system --duration 300 --interval 10 --output system_data.json
```

#### Check Top Processes

Show top 5 processes by memory usage:

```bash
python sys_mon_tool.py processes --count 5 --resource memory
```

#### Analyze Log Files

Analyze a log file for errors:

```bash
python sys_mon_tool.py log --log-path /path/to/app.log --pattern "error"
```

#### Monitor Development Workflow

Monitor a project's workflow and statistics:

```bash
python sys_mon_tool.py workflow --project-path /path/to/my/project
```

### Python API

For integration with other tools:

```python
from system_monitoring.system_monitor import SystemMonitoringTool

tool = SystemMonitoringTool()

# Run system monitoring
data = tool.run_system_monitor(duration=120, interval=10, output_file="monitoring.json")

# Show top processes
tool.show_top_processes(count=10, resource="memory")

# Analyze log file
tool.analyze_log_file("/path/to/logfile.log", pattern="exception")

# Monitor development workflow
tool.monitor_workflow(project_path="/path/to/project")
```

## 🧪 Examples

### Continuous System Monitoring

```bash
$ python sys_mon_tool.py system --duration 60 --interval 5 --output system_data.json
Starting system monitoring for 60 seconds (interval: 5s)...
Recorded system snapshot at 2023-07-15T10:30:45.123456
Recorded system snapshot at 2023-07-15T10:30:50.123456
...
Monitoring data saved to system_data.json
```

### Process Analysis

```bash
$ python sys_mon_tool.py processes --count 5 --resource cpu
Top 5 processes by CPU usage:
--------------------------------------------------------------------------------
PID      Name                      User            CPU      Mem%
--------------------------------------------------------------------------------
1234     python                   user            45.2     8.3
5678     chrome                   user            32.1     15.2
9012     code                     user            28.7     12.5
3456     firefox                  user            18.3     10.1
7890     docker                   user            15.6     5.7
```

### Log Analysis

```bash
$ python sys_mon_tool.py log --log-path app.log --pattern "error"
Log Analysis for: /path/to/app.log
Total lines: 1000
Error lines: 5
Error rate: 0.50%

Error patterns found:
  error: 3 occurrences
  exception: 2 occurrences

First few errors:
  Line 100: ERROR: Database connection failed
  Line 250: CRITICAL: Unable to connect to external service
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add examples/tests for your changes
5. Update documentation
6. Submit a pull request

### Development Setup

```bash
git clone https://github.com/yksanjo/system-monitoring.git
cd system-monitoring
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install psutil
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

- Check the [documentation](docs/)
- Open an [issue](https://github.com/yksanjo/system-monitoring/issues)
- Submit a [pull request](https://github.com/yksanjo/system-monitoring/pulls)

## 🙏 Acknowledgments

- Built with psutil for system monitoring
- Inspired by system monitoring tools in the development community
- Designed with developer workflow in mind

---

<div align="center">

**Made with ❤️ for system health**

[Back to Top](#system-monitoring)

</div>