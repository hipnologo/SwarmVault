# SwarmVault 🔐

<div align="center">

![SwarmVault Logo](https://user-images.githubusercontent.com/your-image-path/swarmvault-logo.png)

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/hipnologo/swarmvault)](https://github.com/hipnologo/swarmvault/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![GitHub stars](https://img.shields.io/github/stars/hipnologo/swarmvault)](https://github.com/hipnologo/swarmvault/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/hipnologo/swarmvault)](https://github.com/hipnologo/swarmvault/issues)
[![GitHub forks](https://img.shields.io/github/forks/hipnologo/swarmvault)](https://github.com/hipnologo/swarmvault/network)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker Support](https://img.shields.io/badge/Docker-Support-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Seamless Docker Swarm Backup & Migration Suite**

[Key Features](#key-features) • [Quick Start](#quick-start) • [Documentation](#documentation) • [Contributing](#contributing) • [Support](#support)

</div>

## 📋 Overview

SwarmVault is a powerful, backup and migration tool for Docker Swarm environments. It provides seamless backup and restoration of your entire Docker infrastructure, including Portainer stacks, volumes, and Swarm configurations.

### Key Features

🔄 **Complete Environment Backup**
- Automated Portainer stack preservation
- Docker volume data protection
- Swarm configuration safeguarding
- Network settings preservation

🚀 **Easy Migration**
- One-command backup creation
- Simplified restoration process
- Cross-server migration support
- Minimal downtime

🛡️ **Enterprise Ready**
- Detailed logging
- Error handling
- Remote sync capabilities
- Compression for storage efficiency

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Docker Swarm environment
- Portainer (optional)

### Installation

```bash
# Clone the repository
git clone https://github.com/hipnologo/swarmvault.git
cd swarmvault

# Make the script executable
chmod +x swarmvault.py

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```bash
# Create a backup
./swarmvault.py

# Backup with custom directory
./swarmvault.py --backup-dir /path/to/backups

# Backup and sync to remote server
./swarmvault.py --remote-host user@server --sync-to /remote/backup/path
```

## 📖 Documentation

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--backup-dir` | Local backup directory | `/opt/swarmvault/backups` |
| `--remote-host` | Remote host for backup operations | None |
| `--sync-to` | Remote path to sync backups to | None |

### Backup Contents

SwarmVault creates a comprehensive backup including:

1. **Portainer Stacks**
   - Stack configurations
   - Docker compose files
   - Service definitions

2. **Docker Volumes**
   - Volume data
   - Volume metadata
   - Compressed archives

3. **Swarm Configuration**
   - Swarm settings
   - Network configurations
   - Node information

### Backup Structure

```
swarmvault-backup-20240130_123456.tar.gz
├── portainer/
│   └── stacks/
│       ├── stack1.json
│       └── stack1-compose.yml
├── volumes/
│   └── volume1.tar.gz
└── swarm/
    ├── swarm-config.json
    └── network-configs/
```

### Restoration Process

1. **Prepare Environment**
   ```bash
   tar -xzf swarmvault-backup-*.tar.gz
   ```

2. **Restore Volumes**
   ```bash
   # Script automatically handles volume restoration
   ./swarmvault.py --restore backup-archive.tar.gz
   ```

3. **Deploy Stacks**
   ```bash
   # Automatic stack deployment
   ./swarmvault.py --restore-stacks backup-archive.tar.gz
   ```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Docker community for inspiration and support
- All contributors who participate in this project
- Python community for excellent tools and libraries

## 📧 Support

- Create an [Issue](https://github.com/hipnologo/swarmvault/issues) for bug reports
- Start a [Discussion](https://github.com/hipnologo/swarmvault/discussions) for questions
- See our [Wiki](https://github.com/hipnologo/swarmvault/wiki) for detailed documentation

## 📈 Project Stats

![Alt](https://repobeats.axiom.co/api/embed/your-repobeats-hash.svg "Repobeats analytics image")

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=hipnologo/swarmvault&type=Date)](https://star-history.com/#hipnologo/swarmvault&Date)

## 📊 Activity

![Alt](https://repobeats.axiom.co/api/embed/your-activity-hash.svg "Repository activity graph")

---
<div align="center">
Made with ❤️ by the SwarmVault Team

[Website](https://github.com/hipnologo/swarmvault) • [Documentation](https://github.com/hipnologo/swarmvault/wiki) • [Report Bug](https://github.com/hipnologo/swarmvault/issues) • [Request Feature](https://github.com/hipnologo/swarmvault/issues)
</div>
