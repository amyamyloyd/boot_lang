# Admin Panel Documentation

## Overview

The Admin Panel provides administrators with complete user management capabilities including creating users, viewing all users, deleting users, and resetting passwords.

## Access

**URL**: `/admin`

**Requirements**: 
- Must be logged in
- Must have `is_admin=True` flag on user account

Non-admin users attempting to access this page will be redirected to the home page.

## Features

### 40/60 Layout

The admin panel uses a split layout:

- **Left Panel (40%)**: Actions and forms
  - Add new user form
  - Reset password form (when triggered)
  - Instructions panel

- **Right Panel (60%)**: User list and messages
  - User table with all users
  - Success/error message displays
  - Refresh button

## Admin Capabilities

### 1. View All Users

The user table displays:
- User ID
- Username
- Email address
- Role (Admin/User badge)
- Creation date
- Action buttons

Click **Refresh** to reload the user list at any time.

### 2. Add New Users

Fill out the form in the left panel:

1. **Username** (required): 3-50 characters
2. **Password** (required): Minimum 4 characters
3. **Email** (optional): Valid email address
4. **Admin Privileges**: Check box to grant admin rights

Click **Add User** to create the account.

**Note**: Admins can create other admin accounts.

### 3. Delete Users

Click **Delete** next to any user in the table.

**Restrictions**:
- Cannot delete yourself
- Confirmation dialog appears before deletion
- Deletion is permanent

### 4. Reset User Passwords

Click **Reset Password** next to any user:

1. Reset password form appears in left panel
2. Enter new password (minimum 4 characters)
3. Click **Reset Password** to apply
4. User can immediately login with new password

**Note**: No current password required when admin resets password.

## API Endpoints (Admin Only)

All admin endpoints require:
- Valid JWT token
- User account with `is_admin=True`

### List All Users

```bash
GET /api/admin/users
Authorization: Bearer <admin-token>

Response:
{
  "success": true,
  "message": "Found 5 users",
  "users": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "is_admin": true,
      "created_at": "2025-10-08T12:00:00",
      "updated_at": "2025-10-08T12:00:00"
    },
    ...
  ]
}
```

### Create User

```bash
POST /api/admin/users
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "username": "newuser",
  "password": "pass1234",
  "email": "user@example.com",
  "is_admin": false
}

Response:
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": 6,
    "username": "newuser",
    "email": "user@example.com",
    "is_admin": false
  }
}
```

### Delete User

```bash
DELETE /api/admin/users/{user_id}
Authorization: Bearer <admin-token>

Response:
{
  "success": true,
  "message": "User 'username' deleted successfully"
}
```

### Reset User Password

```bash
PUT /api/admin/users/{user_id}/reset-password
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "new_password": "newpass1234"
}

Response:
{
  "success": true,
  "message": "Password reset successfully for user 'username'"
}
```

## Creating the First Admin

Since the admin panel requires an existing admin account, you need to create the first admin manually.

### Method 1: Direct Database Script

Create `create_admin.py`:

```python
from database import init_db, SessionLocal, User
from auth_utils import hash_password

# Initialize database
init_db()

# Create session
db = SessionLocal()

try:
    # Check if admin already exists
    existing = db.query(User).filter(User.username == "admin").first()
    if existing:
        print("Admin user already exists")
    else:
        # Create admin user
        admin = User(
            username="admin",
            password_hash=hash_password("admin1234"),
            email="admin@bootlang.com",
            is_admin=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        print(f"✓ Admin user created successfully")
        print(f"  Username: {admin.username}")
        print(f"  Password: admin1234")
        print(f"  Please change the password after first login!")
finally:
    db.close()
```

Run:
```bash
python3 create_admin.py
```

### Method 2: Modify Existing User

If you already have a user account, you can make it admin:

```python
from database import SessionLocal, User

db = SessionLocal()

try:
    user = db.query(User).filter(User.username == "your-username").first()
    if user:
        user.is_admin = True
        db.commit()
        print(f"✓ {user.username} is now an admin")
    else:
        print("User not found")
finally:
    db.close()
```

## Security Considerations

### Admin Privileges

- Admin users can see all user data (except passwords)
- Admins can delete any user except themselves
- Admins can reset passwords without knowing current password
- Admins can create other admin accounts

### Access Control

Admin endpoints are protected by the `get_admin_user` dependency:

```python
from auth import get_current_user
from admin import get_admin_user

# Regular protected endpoint
@router.get("/user-only")
async def user_endpoint(current_user: User = Depends(get_current_user)):
    return {"message": "Any authenticated user"}

# Admin-only endpoint
@router.get("/admin-only")
async def admin_endpoint(admin: User = Depends(get_admin_user)):
    return {"message": "Admin users only"}
```

### Audit Trail

Consider adding logging for admin actions:

```python
import logging

logger = logging.getLogger(__name__)

# In admin endpoints:
logger.info(f"Admin {admin_user.username} deleted user {user_id}")
```

## Error Handling

### 403 Forbidden

If non-admin tries to access admin endpoints:
```json
{
  "detail": "Admin privileges required"
}
```

### 400 Bad Request

Common validation errors:
- Username already exists
- Email already registered
- Invalid password (too short)
- Cannot delete yourself

### 404 Not Found

User doesn't exist when trying to delete/reset password.

## Testing Admin Endpoints

### Create Admin Token

```bash
# Login as admin
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin1234"}' \
  | jq -r '.token')
```

### List Users

```bash
curl -X GET http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer $TOKEN"
```

### Create User

```bash
curl -X POST http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "test1234",
    "email": "test@example.com",
    "is_admin": false
  }'
```

### Delete User

```bash
curl -X DELETE http://localhost:8000/api/admin/users/5 \
  -H "Authorization: Bearer $TOKEN"
```

### Reset Password

```bash
curl -X PUT http://localhost:8000/api/admin/users/5/reset-password \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"new_password": "newpass1234"}'
```

## Best Practices

1. **Create Strong Admin Passwords**: Admins have full control
2. **Limit Admin Accounts**: Only create admin accounts when necessary
3. **Change Default Passwords**: Always change initial admin password
4. **Regular Audits**: Periodically review user list
5. **Backup Before Deletion**: Users cannot be recovered after deletion
6. **Use Reset Carefully**: Resetting passwords should be rare
7. **Log Admin Actions**: Consider implementing audit logging

## Common Tasks

### Bulk User Creation

For creating multiple users, you can script it:

```python
import requests

API_URL = "http://localhost:8000"
TOKEN = "your-admin-token"

users_to_create = [
    {"username": "user1", "password": "pass1234"},
    {"username": "user2", "password": "pass1234"},
    {"username": "user3", "password": "pass1234"},
]

for user_data in users_to_create:
    response = requests.post(
        f"{API_URL}/api/admin/users",
        json=user_data,
        headers={"Authorization": f"Bearer {TOKEN}"}
    )
    print(f"Created {user_data['username']}: {response.json()}")
```

### Export User List

```bash
curl -X GET http://localhost:8000/api/admin/users \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.users' > users.json
```

## Future Enhancements

Consider adding:
- User activity logs
- Bulk operations (delete multiple, export)
- User search and filtering
- Pagination for large user lists
- Email notifications for password resets
- Temporary account suspension
- Role-based permissions beyond admin/user

## Troubleshooting

### Can't Access Admin Panel

- Verify you're logged in
- Check `is_admin` flag in database
- Check browser console for errors
- Verify token is valid and not expired

### Admin Actions Failing

- Check token hasn't expired
- Verify admin privileges in database
- Check backend logs for errors
- Test with curl to isolate frontend/backend issue

## Related Documentation

- [authentication.md](./authentication.md) - Authentication system
- [database.md](./database.md) - Database structure and queries

