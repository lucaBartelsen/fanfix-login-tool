# FanFix Login Tool

A centralized credential management system for FanFix accounts with a Chrome extension interface.

## Architecture

- **Backend**: FastAPI with SQLAlchemy, JWT authentication, and encrypted credential storage
- **Chrome Extension**: Account switching interface with secure API communication
- **Security**: Role-based access control (Admin/Normal users)

## Setup Instructions

### Backend Setup

1. Create virtual environment and install dependencies:
```bash
cd fanfix-login-tool/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env and update SECRET_KEY and ENCRYPTION_KEY
```

3. Initialize database:
```bash
python init_db.py
# This will:
# - Generate an encryption key (copy to .env)
# - Create admin user (username: admin, password: admin123)
# - Add test credential
```

4. Run backend:
```bash
uvicorn app.main:app --reload
```

### Chrome Extension Setup

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode"  
3. Click "Load unpacked"
4. Select the `chrome-extension` folder

## Usage

1. Click extension icon in Chrome toolbar
2. Login with your credentials
3. View assigned FanFix accounts
4. Click "Switch" to login to a FanFix account

## API Endpoints

- `POST /token` - Authenticate user
- `GET /users` - List users (admin only)
- `POST /users` - Create user (admin only)
- `GET /credentials` - List accessible credentials
- `POST /credentials` - Create credential (admin only)
- `POST /credentials/{id}/assign` - Assign credential to users (admin only)

## Security Features

- JWT token authentication
- Encrypted credential storage with Fernet (symmetric encryption)
- Role-based access control
- Secure extension-backend communication
- Password hashing with bcrypt