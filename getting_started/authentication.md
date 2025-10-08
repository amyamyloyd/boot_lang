# Authentication System

## Overview

Boot_Lang implements a complete JWT-based authentication system with user registration, login, password management, and admin capabilities.

## Features

- ✅ User registration with password validation
- ✅ JWT token-based authentication  
- ✅ Protected routes requiring authentication
- ✅ Password change with current password verification
- ✅ Profile updates (username, email)
- ✅ Role-based access control (admin/user)
- ✅ Secure password hashing with bcrypt

## Password Requirements

- **Minimum length**: 4 characters
- Enforced on both frontend and backend

## API Endpoints

### Authentication Endpoints

#### Register New User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "john",
  "password": "pass1234",
  "email": "john@example.com"  // optional
}

Response:
{
  "success": true,
  "message": "User registered successfully",
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  }
}
```

#### Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "john",
  "password": "pass1234"
}

Response:
{
  "success": true,
  "message": "Login successful",
  "token": "eyJhbGc...",
  "user": {
    "id": 1,
    "username": "john",
    "email": "john@example.com",
    "is_admin": false
  }
}
```

#### Get Current User Info

```bash
GET /api/auth/me
Authorization: Bearer <token>

Response:
{
  "id": 1,
  "username": "john",
  "email": "john@example.com",
  "is_admin": false,
  "created_at": "2025-10-08T12:00:00"
}
```

### User Management Endpoints

#### Change Password

```bash
PUT /api/user/password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "pass1234",
  "new_password": "newpass456"
}

Response:
{
  "success": true,
  "message": "Password changed successfully"
}
```

#### Update Profile

```bash
PUT /api/user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "username": "john_new",  // optional
  "email": "newemail@example.com"  // optional
}

Response:
{
  "success": true,
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "john_new",
    "email": "newemail@example.com",
    "is_admin": false
  }
}
```

## Frontend Usage

### Registration

Navigate to `/register` or click "Register" in the navigation.

1. Enter username (3-50 characters)
2. Enter password (minimum 4 characters)
3. Optionally enter email
4. Click "Create account"

### Login

Navigate to `/login` or click "Login" in the navigation.

1. Enter username
2. Enter password
3. Click "Sign in"

Upon successful login, you'll be redirected to the main application and your JWT token will be stored in localStorage.

### User Settings

Navigate to `/settings` to:

- **Update Profile**: Change username or email
- **Change Password**: Update your password (requires current password)

### Logout

Click "Logout" in the navigation to clear your session and return to the login page.

## JWT Token Management

### Token Storage

Tokens are stored in `localStorage`:
- Key: `boot_lang_token`
- Format: JWT string

### Token Expiration

- Default expiration: **24 hours**
- Configurable via `JWT_EXPIRATION_HOURS` environment variable

### Token Payload

```json
{
  "sub": "1",           // User ID
  "username": "john",   // Username
  "is_admin": false,    // Admin flag
  "exp": 1696867200     // Expiration timestamp
}
```

## Protected Routes

All routes except `/login` and `/register` require authentication:

- `/` - POC Builder (user)
- `/settings` - User Settings (user)
- `/admin` - Admin Panel (admin only)

If not authenticated, users are redirected to `/login`.

## Environment Variables

Add to `.env`:

```bash
# JWT Configuration
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**Important**: Change `JWT_SECRET_KEY` in production!

## Security Features

### Password Hashing

- Uses **bcrypt** for password hashing
- Automatic salt generation
- Industry-standard security

```python
from auth_utils import hash_password, verify_password

# Hash password
hashed = hash_password("mypassword")

# Verify password
is_valid = verify_password("mypassword", hashed)
```

### Token Validation

All protected endpoints automatically validate JWT tokens:

```python
from auth import get_current_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"user": current_user.username}
```

### CORS Configuration

CORS is pre-configured for local development:
- `http://localhost:3000` (React dev server)
- `http://localhost:5173` (Vite dev server)

## Creating First Admin User

### Method 1: Via Test Script

Create `create_admin.py`:

```python
from database import init_db, SessionLocal, User
from auth_utils import hash_password

init_db()
db = SessionLocal()

admin = User(
    username="admin",
    password_hash=hash_password("admin1234"),
    email="admin@bootlang.com",
    is_admin=True
)

db.add(admin)
db.commit()
print(f"✓ Admin user created: {admin.username}")
db.close()
```

Run:
```bash
python3 create_admin.py
```

### Method 2: Via API (if you're already logged in as admin)

Use the admin panel to create additional admin users.

## Testing Authentication

### Test Registration

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test1234"}'
```

### Test Login

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"test1234"}'
```

### Test Protected Endpoint

```bash
TOKEN="your-jwt-token-here"

curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## Common Issues

### "Invalid or expired token"

- Token has expired (24 hours default)
- Token is malformed
- Solution: Login again to get a new token

### "Invalid username or password"

- Check credentials are correct
- Check user exists in database
- Verify password meets minimum requirements

### CORS errors

- Ensure frontend is running on allowed origin
- Check CORS configuration in `app.py`
- Verify `allow_credentials=True` is set

## Best Practices

1. **Never log tokens**: Tokens contain sensitive information
2. **Use HTTPS in production**: Always use secure connections
3. **Rotate secret keys**: Change JWT secret periodically
4. **Handle token expiration**: Implement token refresh if needed
5. **Validate on both sides**: Check authentication on frontend AND backend
6. **Use strong passwords**: Enforce password requirements
7. **Limit login attempts**: Consider rate limiting (future enhancement)

## Next Steps

- See [admin.md](./admin.md) for admin panel documentation
- See [database.md](./database.md) for database management
- Implement token refresh mechanism for better UX
- Add password reset via email functionality
- Implement 2FA for enhanced security

