# API Usage Guide - FanFix Login Tool

## Authentication

All API endpoints (except `/token`) require authentication via JWT token.

### Get Access Token

```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Use this token in subsequent requests:
```bash
-H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## User Management (Admin Only)

### Create New User

```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "secure_password123",
    "role": "normal"
  }'
```

Roles: `"admin"` or `"normal"`

### List All Users

```bash
curl -X GET "http://localhost:8000/users/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Current User Info

```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Update User

```bash
curl -X PATCH "http://localhost:8000/users/2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "password": "new_password123",
    "is_active": true
  }'
```

### Delete User

```bash
curl -X DELETE "http://localhost:8000/users/2" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Credential Management

### Add New FanFix Credential (Admin Only)

```bash
curl -X POST "http://localhost:8000/credentials/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John's FanFix Account",
    "username": "john@fanfix.com",
    "password": "fanfix_password123"
  }'
```

### List Available Credentials

Normal users see only assigned credentials, admins see all.

```bash
curl -X GET "http://localhost:8000/credentials/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Credential with Decrypted Password

```bash
curl -X GET "http://localhost:8000/credentials/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response includes decrypted password:
```json
{
  "id": 1,
  "name": "Kelly Test Account",
  "username": "kelly@unleashmgmt.family",
  "password": "kersdd76_a9s8",
  "owner_id": 1,
  "created_at": "2024-01-15T10:00:00",
  "updated_at": "2024-01-15T10:00:00"
}
```

### Update Credential (Admin Only)

```bash
curl -X PATCH "http://localhost:8000/credentials/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Account Name",
    "password": "new_password123"
  }'
```

### Assign Credential to Users (Admin Only)

```bash
curl -X POST "http://localhost:8000/credentials/1/assign" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [2, 3, 4]
  }'
```

### Delete Credential (Admin Only)

```bash
curl -X DELETE "http://localhost:8000/credentials/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## FanFix Integration

### Login to FanFix via Playwright

```bash
curl -X POST "http://localhost:8000/fanfix/login" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "kelly@unleashmgmt.family",
    "password": "kersdd76_a9s8"
  }'
```

Returns session cookies for the FanFix session.

## Example Workflow

### 1. Admin Creates a New User

```bash
# Get admin token
TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r .access_token)

# Create new user
curl -X POST "http://localhost:8000/users/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "sarah",
    "email": "sarah@company.com",
    "password": "sarah_password123",
    "role": "normal"
  }'
```

### 2. Admin Adds a FanFix Credential

```bash
curl -X POST "http://localhost:8000/credentials/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Marketing Team Account",
    "username": "marketing@fanfix.com",
    "password": "marketing_pass123"
  }'
```

### 3. Admin Assigns Credential to User

```bash
# Assuming the credential ID is 2 and user ID is 2
curl -X POST "http://localhost:8000/credentials/2/assign" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [2]
  }'
```

### 4. User Accesses Their Credentials

```bash
# User logs in
USER_TOKEN=$(curl -s -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=sarah&password=sarah_password123" | jq -r .access_token)

# User lists their credentials
curl -X GET "http://localhost:8000/credentials/" \
  -H "Authorization: Bearer $USER_TOKEN"

# User gets credential details
curl -X GET "http://localhost:8000/credentials/2" \
  -H "Authorization: Bearer $USER_TOKEN"
```

## Testing with HTTPie (Alternative)

If you prefer HTTPie over curl:

```bash
# Login
http POST localhost:8000/token username=admin password=admin123

# Create user
http POST localhost:8000/users/ \
  "Authorization: Bearer TOKEN" \
  username=test email=test@example.com password=test123 role=normal

# List credentials
http GET localhost:8000/credentials/ "Authorization: Bearer TOKEN"
```

## Postman Collection

Import this collection to Postman for easy testing:

1. Create new collection "FanFix Login Tool"
2. Add variable `base_url` = `http://localhost:8000`
3. Add variable `token` (update after login)
4. Import the endpoints with proper auth headers