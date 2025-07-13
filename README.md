# Pengu Network Tools

Welcome to the Pengu Network Tools project! This repository contains a collection of advanced network security tools packaged with automatic dependency management and enhanced features.

## 🚀 New Features v2.0

### Enhanced Tools
- **Enhanced Ping**: Advanced ICMP ping with Q to quit, 3-second countdown, static header, and color-coded output
- **Mass Pinger**: Multi-target ping tool with same enhancements as standard pinger
- **System Hardware Detection**: Automatic hardware scanning with performance recommendations
- **Advanced Port Scanner**: Hardware-optimized threading with intelligent recommendations
- **Improved Subdomain Finder**: Better output, configurable threading, rate-limiting warnings
- **Enhanced Traceroute**: Better error handling, admin rights detection, Scapy bug fixes
- **Proxy Checker**: Multi-protocol proxy validation with anonymity detection and reporting

### Core Improvements
- **Admin Rights Detection**: Automatic detection with UAC prompts and clear warnings
- **Background Hardware Scanning**: System specs detected on startup for performance optimization
- **No Banner Spam**: Tool banners only appear when actively running tools
- **Enhanced Error Handling**: Better error messages and graceful fallbacks
- **Improved UI**: Clearer text and admin status indicators

## 🛠 Tools Included

### Network Analysis
1. **Enhanced Ping (ping)**
   - ICMP ping with advanced features
   - Press Q to stop functionality
   - 3-second countdown timer
   - Color-coded results (Green/Yellow/Red)
   - Static header with real-time updates

2. **Mass Pinger**
   - Multiple target ping testing
   - Same enhanced features as single ping
   - Real-time multi-target monitoring

3. **TCP Ping (tcp)**
   - TCP port connectivity testing
   - Response time measurement

4. **HTTP Ping (http)**
   - HTTP/HTTPS connectivity testing
   - Status code monitoring

### Scanning Tools
5. **Advanced Port Scanner (port)**
   - Multi-threaded port scanning
   - Hardware-based thread recommendations
   - Intelligent performance tuning

6. **Subdomain Finder (subdomain)**
   - Multi-threaded subdomain enumeration
   - Configurable thread counts
   - Rate-limiting warnings
   - Hardware-optimized performance

7. **Traceroute (traceroute)** ⚠ *Requires Admin*
   - Network path tracing
   - Automatic admin rights detection
   - UAC elevation prompts
   - Multiple fallback methods

### Information Gathering
8. **GeoIP & WHOIS Lookup (tracker)**
   - IP geolocation
   - WHOIS information
   - Multi-source data aggregation

9. **System Hardware Specs (specs)**
   - CPU, RAM, GPU detection
   - Performance recommendations
   - Background hardware scanning

### Security Tools
10. **Proxy Checker (proxy)**
    - Multi-protocol support (HTTP, HTTPS, SOCKS4, SOCKS5)
    - Anonymity level detection (Elite/Anonymous/Transparent)
    - Real-time validation
    - Detailed reporting and filtering
    - Working proxy export options

## 🖥 System Requirements

- **Python 3.6+** (auto-installs dependencies)
- **Administrator privileges** (optional, required for traceroute and some advanced features)
- **Internet connection** (for dependency installation and tool functionality)

## 📦 Installation & Usage

### Quick Start
```bash
# Clone the repository
git clone https://github.com/JasonVinion/Pengu.git
cd Pengu

# Run Pengu (auto-installs dependencies)
python3 Source/pengu.py
```

### Features Overview
- **Automatic Dependency Management**: No manual package installation required
- **Admin Detection**: Shows warnings when admin privileges are needed
- **Hardware Optimization**: Automatic performance tuning based on system specs
- **Enhanced UI**: Color-coded output with clear status indicators

## 🎯 Usage Examples

### Enhanced Ping
```
ping → Select single/mass ping → Enter target(s) → Press Q to stop
```

### Port Scanning with Hardware Optimization
```
port → Enter IP → Set port range → Use recommended thread count
```

### Proxy Checking
```
proxy → Specify proxy file → Set thread count → Save working proxies
```

### System Specs
```
specs → View hardware info and performance recommendations
```

## ⚠ Important Notes

### Administrator Privileges
- **Required for**: Traceroute (raw sockets), some hardware detection features
- **Optional for**: All other tools work without admin rights
- **Auto-detection**: Application shows clear warnings and elevation prompts

### Performance Recommendations
- **Thread Counts**: Based on CPU cores and system capabilities
- **Rate Limiting**: Conservative defaults to avoid triggering server protections
- **Resource Usage**: Optimized for efficiency and stability

### Proxy Checker Details
- **Supported Formats**: 
  - `IP:PORT`
  - `TYPE://IP:PORT`
  - `IP:PORT:USER:PASS`
  - `TYPE://USER:PASS@IP:PORT`
- **Protocols**: HTTP, HTTPS, SOCKS4, SOCKS5
- **Features**: Anonymity detection, connection time measurement, filtering

## 🔧 Advanced Configuration

### Subdomain Finder
- Custom thread counts with hardware recommendations
- Rate limiting warnings for high thread counts
- Progress tracking and real-time results

### Port Scanner
- Hardware-optimized thread recommendations
- Safety limits to prevent system overload
- Real-time open port discovery

## 📋 Command Reference

| Command | Description | Admin Required |
|---------|-------------|----------------|
| `help` | Show help menu | No |
| `ping` | Enhanced ping utility | No |
| `tcp` | TCP connectivity test | No |
| `http` | HTTP connectivity test | No |
| `port` | Advanced port scanner | No |
| `subdomain` | Subdomain finder | No |
| `tracker` | GeoIP & WHOIS lookup | No |
| `traceroute` | Network path tracer | Yes ⚠ |
| `proxy` | Proxy checker | No |
| `specs` | System hardware info | No |
| `exit` | Return to main menu | No |

## 🐛 Known Issues & Fixes

### Fixed Issues
- ✅ **Banner spam on startup** - Tools banners only appear when actively used
- ✅ **Scapy L3WinSocket bug** - Added specific error handling for Windows
- ✅ **Missing admin detection** - Comprehensive admin rights checking
- ✅ **Poor thread optimization** - Hardware-based recommendations
- ✅ **Verbose subdomain output** - Streamlined with progress indicators

### Current Limitations
- Some hardware detection features require admin rights
- Proxy checker requires internet access for validation
- High thread counts may trigger rate limiting on target servers

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## ⚠ Disclaimer

**Use these tools responsibly and only on systems you own or have explicit permission to test.**

The authors are not responsible for any misuse or damage caused by these tools. These tools are for educational and authorized security testing purposes only.

## 📊 Version History

### v2.0 (Latest)
- Enhanced ping tools with advanced features
- System hardware integration
- Admin rights detection and management
- Proxy checker tool
- Improved UI and error handling
- Background hardware scanning
- Performance optimizations

### v1.0
- Basic network tools
- Simple command interface
- Manual dependency management

---

**Developed by JasonVinion** | [GitHub](https://github.com/JasonVinion) | [Report Issues](https://github.com/JasonVinion/Pengu/issues)
