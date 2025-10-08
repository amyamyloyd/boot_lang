```markdown
# Boot_Lang Complete Build Instructions

Copy/paste each prompt into Cursor one at a time in order.

---

**Prompt 1: Database Setup**
```
Create database.py in root directory using SQLAlchemy with SQLite. Database file: boot_lang.db. Create Base class using declarative_base. Define User model with fields: id (primary key), username (unique), password_hash, created_at. Include init_db() function to create all tables. Add main block to run init_db() when executed directly.
```

---

**Prompt 2: Admin Backend**
```
Create admin.py in root directory. Import User model from database.py. Import bcrypt for password hashing. Create FastAPI router with prefix /admin. Add POST /admin/users endpoint that accepts username and password, hashes password with bcrypt, creates new user in database, returns success/error response. Add GET /admin/users endpoint that lists all users without passwords.
```

---

**Prompt 3: Update app.py**
```
Update app.py to include admin router. Import admin router from admin.py. Add app.include_router(admin.router) after CORS setup. Import init_db from database.py. Call init_db() on startup to ensure database exists.
```

---

**Prompt 4: Admin Frontend Component**
```
Create src/components/AdminPanel.tsx with 40/60 layout. Left panel (40%): form with username and password inputs, "Add User" button, list of existing users below. Right panel (60%): instructions on how to use admin panel, success/error messages. Use axios to call /admin/users endpoints. Style with Tailwind CSS.
```

---

**Prompt 5: Add Admin Route to App**
```
Update src/App.tsx. Install react-router-dom if needed. Create routes: / goes to POCBuilder, /admin goes to AdminPanel. Add simple navigation links at top.
```

---

**Prompt 6: Database Documentation**
```
Create getting_started/database.md. Explain SQLite setup and location (boot_lang.db). Show User model example. Provide step-by-step instructions to add custom tables: 1) Define new model in database.py, 2) Run python database.py to create tables, 3) Import model in endpoints. Include example of adding a "Projects" table. Explain SQLAlchemy query basics.
```

---

**Prompt 7: Admin Documentation**
```
Create getting_started/admin.md. Explain how to access admin panel (/admin route). Show how to add first user. Explain password hashing (bcrypt). Document admin API endpoints. Include curl examples for API calls.
```

---

**Prompt 8: Test Database**
```
Create test_database.py in root. Import database.py and models. Create test function that initializes database, creates a test user, queries the user back, prints success. Add instructions to run: python test_database.py.
```

---

End of instructions.
```