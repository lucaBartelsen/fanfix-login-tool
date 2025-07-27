# Ubuntu Server Setup Guide - FanFix Login Tool

## Prerequisites

- Python 3.10 or higher (3.11 recommended for best performance)
- pip (Python package manager)

**Important**: This project requires Python 3.10+ due to modern syntax usage. If you have an older version, see PYTHON_UPGRADE.md for upgrade instructions.

## Fix Python venv Issue

If you get an error when running `python3 -m venv venv`, you need to install the venv package:

```bash
# Update package list
sudo apt update

# Install Python3 venv package
sudo apt install python3-venv -y

# Also install pip if not already installed
sudo apt install python3-pip -y
```

## Complete Ubuntu Setup

### 1. Install System Dependencies

```bash
# Install Python and development tools
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev

# Install build dependencies for Python packages
sudo apt install -y build-essential libssl-dev libffi-dev
```

### 2. Clone Repository

```bash
# Using gh CLI
gh repo clone lucaBartelsen/fanfix-login-tool

# OR using git
git clone https://github.com/lucaBartelsen/fanfix-login-tool.git

cd fanfix-login-tool/backend
```

### 3. Create Virtual Environment (Now it should work)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Set Up Environment

```bash
cp .env.example .env

# Generate secure keys
python3 << 'EOF'
import secrets
from cryptography.fernet import Fernet

print("Add these to your .env file:")
print(f"SECRET_KEY={secrets.token_urlsafe(32)}")
print(f"ENCRYPTION_KEY={Fernet.generate_key().decode()}")
EOF
```

Edit `.env` with nano or vim:
```bash
nano .env
```

### 6. Initialize Database

```bash
python init_db.py
```

### 7. Run the Server

```bash
# For development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# For production (with systemd service)
# See below for systemd setup
```

## Optional: Set Up as Systemd Service

Create service file:
```bash
sudo nano /etc/systemd/system/fanfix-backend.service
```

Add this content:
```ini
[Unit]
Description=FanFix Login Tool Backend
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/fanfix-login-tool/backend
Environment="PATH=/home/ubuntu/fanfix-login-tool/backend/venv/bin"
ExecStart=/home/ubuntu/fanfix-login-tool/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl enable fanfix-backend
sudo systemctl start fanfix-backend
sudo systemctl status fanfix-backend
```

## Firewall Configuration

If using UFW:
```bash
sudo ufw allow 8000/tcp
```

## Troubleshooting

### Issue: Permission denied
```bash
# Make sure you own the directory
sudo chown -R $USER:$USER ~/fanfix-login-tool
```

### Issue: Module not found
```bash
# Make sure venv is activated
source venv/bin/activate
# Reinstall requirements
pip install -r requirements.txt
```