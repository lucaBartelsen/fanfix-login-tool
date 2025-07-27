# Upgrading to Python 3.10+ on Ubuntu

## Option 1: Using deadsnakes PPA (Recommended)

### 1. Add the deadsnakes PPA

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
```

### 2. Install Python 3.10 or 3.11

```bash
# For Python 3.10
sudo apt install python3.10 python3.10-venv python3.10-dev -y

# For Python 3.11 (recommended)
sudo apt install python3.11 python3.11-venv python3.11-dev -y
```

### 3. Verify Installation

```bash
python3.11 --version
```

### 4. Recreate Virtual Environment with Python 3.11

```bash
cd ~/fanfix-login-tool/backend

# Remove old virtual environment
rm -rf venv

# Create new virtual environment with Python 3.11
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Verify Python version in venv
python --version  # Should show Python 3.11.x

# Install requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the Application

```bash
# Initialize database again
python init_db.py

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Option 2: Using pyenv (For Multiple Python Versions)

If you need to manage multiple Python versions:

```bash
# Install dependencies
sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
    libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
    libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
    libffi-dev liblzma-dev

# Install pyenv
curl https://pyenv.run | bash

# Add to ~/.bashrc
echo 'export PATH="$HOME/.pyenv/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Reload shell
exec "$SHELL"

# Install Python 3.11
pyenv install 3.11.7
pyenv local 3.11.7

# Create virtual environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Update System Python (Not Recommended)

Changing the system Python can break system tools. Only do this if you know what you're doing:

```bash
# Set Python 3.11 as default (USE WITH CAUTION)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
sudo update-alternatives --config python3
```

## Troubleshooting

### Issue: pip not found in venv
```bash
# Install pip for Python 3.11
sudo apt install python3.11-distutils
curl https://bootstrap.pypa.io/get-pip.py | python3.11
```

### Issue: Package not found
```bash
# Update package list
sudo apt update
```

### Issue: Permission denied
```bash
# Make sure you own the directory
sudo chown -R $USER:$USER ~/fanfix-login-tool
```

## Benefits of Upgrading

1. **Modern syntax support**: Union types with `|`, match statements, etc.
2. **Performance improvements**: Python 3.11 is significantly faster
3. **Better error messages**: More descriptive error messages
4. **Security updates**: Latest security patches

## Note on Requirements

The current code uses Python 3.10+ syntax in several places:
- Type unions with `|` (e.g., `str | None`)
- Other modern Python features

By upgrading, you won't need to modify any code!