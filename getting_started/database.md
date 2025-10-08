# Database Setup and Usage

## Overview

Boot_Lang uses SQLite with SQLAlchemy ORM for data persistence. The database file is `boot_lang.db` and is automatically created on first run.

## Database Location

```
/boot_lang.db
```

**Note**: The database file is tracked in version control to ensure proper deployment and bootstrapping. Initialize with `python3 database.py` or it will auto-initialize on first run.

## Database Schema

### Users Table

The main user authentication and authorization table.

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-increment |
| `username` | String(50) | Unique username for login |
| `email` | String(100) | Optional email address |
| `password_hash` | String(255) | Bcrypt hashed password |
| `is_admin` | Boolean | Admin privileges flag |
| `created_at` | DateTime | Account creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

## Initialization

The database is automatically initialized when the application starts:

```python
# Manual initialization
python3 database.py
```

This will create all tables defined in the schema.

## Adding Custom Tables

### Step 1: Define the Model

Add your model class to `database.py`:

```python
class Project(Base):
    """Example: Projects table"""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
```

### Step 2: Run Database Initialization

```bash
python3 database.py
```

This will create the new table without affecting existing data.

### Step 3: Import in Endpoints

```python
from database import get_db, User, Project

@app.get("/api/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return {"projects": projects}
```

## SQLAlchemy Query Basics

### Create a Record

```python
new_user = User(
    username="john",
    email="john@example.com",
    password_hash=hash_password("password"),
    is_admin=False
)
db.add(new_user)
db.commit()
db.refresh(new_user)  # Get the auto-generated ID
```

### Query Records

```python
# Get all users
users = db.query(User).all()

# Get by ID
user = db.query(User).filter(User.id == 1).first()

# Get by username
user = db.query(User).filter(User.username == "john").first()

# Filter with multiple conditions
admins = db.query(User).filter(
    User.is_admin == True,
    User.created_at > some_date
).all()
```

### Update Records

```python
user = db.query(User).filter(User.id == 1).first()
user.email = "newemail@example.com"
db.commit()
```

### Delete Records

```python
user = db.query(User).filter(User.id == 1).first()
db.delete(user)
db.commit()
```

## Database Sessions

Always use the `get_db()` dependency in FastAPI endpoints:

```python
from database import get_db
from sqlalchemy.orm import Session

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}
```

The session is automatically closed after the request completes.

## Testing the Database

Run the test script to verify database functionality:

```bash
python3 test_database.py
```

This will:
1. Initialize the database
2. Create a test user
3. Query the user back
4. Verify password hashing
5. Clean up test data

## Backup and Restore

### Backup

```bash
cp boot_lang.db boot_lang_backup.db
```

### Restore

```bash
cp boot_lang_backup.db boot_lang.db
```

## Viewing Database Contents

Use any SQLite browser or command line:

```bash
# Command line
sqlite3 boot_lang.db
sqlite> .tables
sqlite> SELECT * FROM users;
sqlite> .quit
```

Or use GUI tools:
- [DB Browser for SQLite](https://sqlitebrowser.org/)
- [TablePlus](https://tableplus.com/)
- VSCode SQLite extension

## Common Issues

### Database Locked

If you get "database is locked" errors:
- Ensure only one process is accessing the database
- Check that all sessions are properly closed
- Restart the application

### Table Not Found

If you get "no such table" errors:
- Run `python3 database.py` to create tables
- Check that you're using the correct database file
- Verify your model is defined correctly

## Best Practices

1. **Always use sessions**: Never create engine connections manually
2. **Close sessions**: Use `get_db()` dependency to auto-close
3. **Use transactions**: Commit after successful operations
4. **Handle errors**: Wrap database operations in try-except blocks
5. **Index frequently queried fields**: Add `index=True` to columns
6. **Backup regularly**: SQLite files are easy to copy and backup

