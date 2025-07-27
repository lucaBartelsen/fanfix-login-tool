# Quick Start Guide - FanFix Login Tool Backend

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd fanfix-login-tool/backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
```

### 2. Create Environment File

```bash
cat > .env << EOF
DATABASE_URL=sqlite:///./fanfix_login.db
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_KEY=$(python3 -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())')
EOF
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Start Server

```bash
uvicorn app.main:app --reload
```

## Test It's Working

```bash
# Test API is running
curl http://localhost:8000/

# Login as admin
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

## What's Next?

- API Documentation: http://localhost:8000/docs
- Default admin login: `admin` / `admin123`
- Test credential pre-loaded: `kelly@unleashmgmt.family`

## Chrome Extension

1. Open Chrome → Extensions → Developer mode ON
2. Load unpacked → Select `chrome-extension` folder
3. Click extension icon → Login with admin credentials
4. Switch between FanFix accounts with one click!