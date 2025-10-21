# What's Missing from Boot_Lang

## Existing Cursor Rules (in /cursor/rules/)

✅ guard.mdc (master ruleset)  
✅ git.mdc (commit discipline)  
✅ documentation.mdc (architecture docs)  
✅ python.mdc (Python coding standards)  
✅ react.mdc (React component patterns)  
✅ langchain.mdc (LangChain agent standards)  
✅ imp.mdc (PRD to implementation plan)

**Note:** Existing rules need review for delivery focus and clarity

---

## Missing Cursor Rules

### 1. authentication.mdc
**Purpose:** Guide Cursor on how to implement authentication in user apps

**Should include:**
- When to activate (user says "add login", "add auth", "user management")
- How to import from base auth system (`from auth import get_current_user`)
- How to protect routes with `Depends(get_current_user)`
- How to use JWT tokens
- Frontend: How to use AuthContext
- Examples of protected endpoints
- Examples of login/register pages

**Location:** `/cursor/rules/authentication.mdc`

---

### 2. sqlite.mdc  
**Purpose:** Guide Cursor on database usage

**Should include:**
- When to activate (user says "add database", "create table", "store data")
- How to define SQLAlchemy models
- Table naming conventions
- How to use `get_db()` dependency
- CRUD operation patterns
- How to run migrations (`python3 database.py`)
- Query examples
- Foreign key relationships to User table

**Location:** `/cursor/rules/sqlite.mdc`

---

### 3. azure.mdc
**Purpose:** Guide Cursor on Azure deployment

**Should include:**
- When to activate (user says "deploy", "Azure setup", "production")
- How to configure CORS for Azure
- Environment variables needed
- GitHub Actions workflow setup
- Branch strategy
- How to get publish profile
- Static Web App + App Service setup
- Testing deployment
- How to check Azure logs

**Location:** `/cursor/rules/azure.mdc`

---

### 4. python_libraries.mdc
**Purpose:** Guide how to add new Python dependencies

**Should include:**
- When to activate (user says "install", "add package", "need library")
- How to add to `requirements.txt` with version pinning
- How to install in venv (`venv/bin/pip install`)
- How to document what library does in code comments
- How to update `requirements.txt` after adding dependency
- Common libraries for this stack (FastAPI, LangChain, pandas, etc.)
- Never install globally, always in venv

**Location:** `/cursor/rules/python_libraries.mdc`

---

### 5. prd.mdc
**Purpose:** Guide Cursor on building PRDs with user

**Should include:**
- When to activate (user says "help me build a PRD", "create requirements")
- Questions to ask user about their idea
- PRD template structure
- Where to save PRD (`/prd/` folder)
- How to validate PRD completeness

**Location:** `/cursor/rules/prd.mdc`

---

## Missing Startup Script

### startup.sh or start.py
**Purpose:** Initialize environment and present workflow options

**Should do:**
1. Create/activate venv
2. Install dependencies from requirements.txt
3. Initialize database
4. Run test page deployment workflow
5. Capture user configuration
6. Present workflow options to Cursor agent

**Location:** Root directory

---

## Missing Infrastructure

### User Configuration System
- ❌ `user_config.json` - Store user preferences, Azure settings, branch names
- ❌ Code to read/write config in rules

### Azure Deployment
- ❌ `.github/workflows/deploy.yml` - GitHub Actions workflow
- ❌ Azure pipeline configuration
- ❌ Branch-to-deployment mapping

### Command Recognition
- ❌ "Build my latest PRD" command handler
- ❌ PRD folder monitoring in rules
- ❌ Automatic PRD detection from `/prd/` directory

---

## Notes
- PRD workflow still being decided
- Agent should present these 3 options on startup
- Users may not need the PRD tool at all (can work directly with Cursor)
- Existing rules need delivery-focused revision before release

