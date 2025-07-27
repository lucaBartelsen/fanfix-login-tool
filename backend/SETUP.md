# Backend Setup Guide - FanFix Login Tool

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Chrome/Chromium browser (for Playwright)

## Step-by-Step Setup

### 1. Navigate to Backend Directory

```bash
cd fanfix-login-tool/backend
```

### 2. Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Set Up Environment Variables

**Option A: Copy and edit the example file**
```bash
cp .env.example .env
```

**Option B: Create .env file manually**
```bash
touch .env
```

Add the following content to `.env`:
```env
DATABASE_URL=sqlite:///./fanfix_login.db
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENCRYPTION_KEY=your-encryption-key-here-change-this
```

### 6. Generate Security Keys

Run this Python script to generate secure keys:

```bash
python3 -c "
import secrets
from cryptography.fernet import Fernet

# Generate SECRET_KEY
secret_key = secrets.token_urlsafe(32)
print(f'SECRET_KEY={secret_key}')

# Generate ENCRYPTION_KEY
encryption_key = Fernet.generate_key().decode()
print(f'ENCRYPTION_KEY={encryption_key}')
"
```

Copy the generated keys and update your `.env` file.

### 7. Initialize Database

```bash
python init_db.py
```

This will:
- Create the SQLite database
- Create all necessary tables
- Add default admin user (username: `admin`, password: `admin123`)
- Add test FanFix credential

### 8. Run the Backend Server

**Development mode (with auto-reload):**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Verify Installation

1. Open browser and go to `http://localhost:8000`
   - Should see: `{"message":"FanFix Login Tool API"}`

2. Check API documentation at `http://localhost:8000/docs`

3. Test login with admin credentials:
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

## Common Issues and Solutions

### Issue: Module not found errors
**Solution:** Make sure virtual environment is activated and all dependencies are installed.

### Issue: Playwright browser not found
**Solution:** Run `playwright install chromium` after installing packages.

### Issue: Permission denied on database file
**Solution:** Ensure the backend directory has write permissions.

### Issue: Port 8000 already in use
**Solution:** Either stop the other process or use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

## Security Recommendations

1. **Change Default Admin Password**
   - Login as admin
   - Use the API to update password

2. **Use Strong Keys**
   - Never use the example keys in production
   - Generate new keys for each deployment

3. **Database Security**
   - Keep database file in a secure location
   - Regular backups recommended

4. **HTTPS in Production**
   - Use a reverse proxy (nginx/Apache) with SSL
   - Or use uvicorn with SSL certificates

## Next Steps

1. Create additional users via API
2. Add FanFix credentials
3. Assign credentials to users
4. Install and configure the Chrome extension

## API Quick Reference

- **Docs**: `http://localhost:8000/docs`
- **Health Check**: `GET /`
- **Login**: `POST /token`
- **Users**: `/users/*`
- **Credentials**: `/credentials/*`