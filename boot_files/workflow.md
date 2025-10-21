# Boot_Lang Development Workflow

## Overview
Boot_Lang is a Cursor AI-guided development environment that takes you from idea to deployed application. Non-technical users can build full-stack web apps by describing what they want.

---

## Prerequisites

### 1. Install Cursor AI
- Download from https://cursor.sh
- Install on your machine
- Get **Cursor Pro account** (required for max mode)
- Enable **Claude 4.5 Sonnet** or **Grok** in max mode settings

### 2. Download Boot_Lang Repository
```bash
# Clone the repository
git clone [repository-url]

# Open in Cursor
# File → Open Folder → Select boot_lang directory
```

**Critical:** The repository includes all `.mdc` rule files - these guide Cursor AI through every step.

---

## Initial Setup (One-Time Process)

### Step 1: Run Setup Script
```bash
./startup.sh
# or
python3 start.py
```

**What the script does:**
- Creates virtual environment (`venv/`)
- Installs all dependencies
- Verifies configuration
- Initiates setup workflow with Cursor

### Step 2: Build Test Page (Guided by Script)
The setup script instructs Cursor to build a simple test application:
- **Example:** File upload page or basic form
- **Purpose:** Verify entire workflow end-to-end
- **Cursor will:** Write code, show you progress

### Step 3: Test in Localhost
**Backend:**
```bash
http://localhost:8000
```

**Frontend:**
```bash
http://localhost:3000
```

**You verify:**
- Page loads correctly
- Functionality works (upload file, submit form, etc.)
- No errors in browser console

### Step 4: First Commit (Automated by Cursor)
Cursor will:
- Stage all files
- Create descriptive commit message
- Commit to git
- Show you what was committed

**You learn:** How commits work, what changes were made

### Step 5: Deploy Test Page to Azure
Setup script will:
- Create deployment branch (e.g., `test-deployment`)
- Configure Azure deployment pipeline
- Push code to trigger deployment
- Provide Azure URL

**You receive:** Link to deployed page (e.g., `https://boot-lang-test.azurewebsites.net`)

### Step 6: Verify Deployment
- Click the Azure link
- See your test page live on the internet
- Test functionality works in production

**Success:** End-to-end process proven working ✓

### Step 7: User Configuration
After successful deployment, Cursor asks setup questions:
- Your name/identifier
- Preferred stack preferences (if any)
- Default branch naming
- Azure resource names

**Saved to:** `user_config.json` (referenced by all rules)

---

## Main Development Workflow

### Phase 1: Define What You Want to Build

**Option A: Use PRD Builder Tool**
```bash
# Start the PRD builder
http://localhost:3000
```
- Chat with POC Agent
- Describe your application
- Upload wireframes or documents if you have them
- Agent generates structured PRD
- PRD saved to `/prd/your_app_name.md`

**Option B: Upload Existing PRD**
- Place your PRD document in `/prd/` folder
- Name it descriptively (e.g., `vocabulary_app.md`)

**Option C: Build PRD with Cursor in Terminal**
- Tell Cursor: "Help me build a PRD for [your idea]"
- Answer questions conversationally
- Cursor creates PRD in `/prd/`

### Phase 2: Build Your Application

**Tell Cursor:**
```
"Build my latest PRD"
```

**Cursor will:**
1. Check `/prd/` folder for most recent file
2. Read and analyze the PRD
3. Ask confirmation questions:
   - "You want to build [app name]?"
   - "This includes [list of features]?"
   - "Deploy to Azure branch: [branch-name]?"
4. Generate implementation plan in `/imp_plans/`
5. Show you the plan and ask to proceed

**You confirm:** "Yes, let's build it"

### Phase 3: Implementation (Phased Approach)

Cursor builds in phases with testing checkpoints:

#### Phase 1: Frontend
- React components
- Tailwind styling
- Basic UI layout

**Test checkpoint:**
```bash
http://localhost:3000
```
You verify: Pages load, UI looks correct

**Cursor commits** after your approval

#### Phase 2: Backend API
- FastAPI endpoints
- Business logic
- Authentication integration

**Test checkpoint:**
```bash
http://localhost:8000/docs
```
You verify: API endpoints work, data flows correctly

**Cursor commits** after your approval

#### Phase 3: Database
- SQLAlchemy models
- Database tables
- Data persistence

**Test checkpoint:**
- Create data in frontend
- Refresh page
- Verify data persists

**Cursor commits** after your approval

#### Phase 4: Integration Testing
- Full end-to-end testing
- Edge cases
- Error handling

**Test checkpoint:**
- Complete user workflows
- Test all features
- Verify everything works together

**Cursor commits** final working version

### Phase 4: Deploy to Azure

**Tell Cursor:**
```
"Deploy to Azure"
```

**Cursor will:**
1. Create deployment branch (e.g., `prod-vocabulary-app`)
2. Run final tests
3. Push to trigger Azure deployment
4. Monitor deployment status
5. Provide live URL

**You receive:** Link to your live application

### Phase 5: Verify Production

- Visit the live URL
- Test all functionality in production
- Share with users if ready

---

## How Cursor Rules Activate

Rules automatically guide Cursor based on what you ask:

| You say | Rule activates | Cursor does |
|---------|---------------|-------------|
| "Add login" | `authentication.mdc` | Implements auth using base system |
| "Create a users table" | `sqlite.mdc` | Creates SQLAlchemy model, runs migration |
| "Install pandas" | `python_libraries.mdc` | Adds to requirements.txt, installs in venv |
| "Deploy this" | `azure.mdc` | Configures Azure, creates pipeline |
| Any code change | `git.mdc` | Commits after testing |
| "Add a button" | `react.mdc` | Creates React component with Tailwind |
| "Build an agent" | `langchain.mdc` | Structures LangChain agent properly |

**You don't need to know the rules** - just describe what you want in plain language.

---

## Testing at Each Step

### Localhost Testing

**Backend (port 8000):**
- FastAPI auto-documentation: http://localhost:8000/docs
- Test API endpoints directly
- See request/response data

**Frontend (port 3000):**
- React app with hot reload
- Changes appear instantly
- Test in browser like normal website

**Database:**
- SQLite browser or command line
- Verify data stored correctly
- Check table structure

### Production Testing
- Same tests as localhost
- Plus: Performance, real users, mobile devices

---

## Monitoring & Debugging

### Check Azure Logs
**Tell Cursor:**
```
"Check Azure logs for errors"
```

**Cursor will:**
- Access Azure deployment logs
- Show recent errors or warnings
- Suggest fixes if issues found

### Common Issues

**Deployment fails:**
- Cursor checks logs automatically
- Identifies issue (missing env var, dependency error, etc.)
- Fixes and redeploys

**Localhost won't start:**
- Cursor verifies venv activated
- Checks dependencies installed
- Runs diagnostic commands

**Feature not working:**
- Cursor reviews recent commits
- Runs tests to isolate issue
- Fixes and tests again

---

## Built-in Features (Already Working)

### Authentication System
Every app you build includes:
- User registration/login
- JWT token security
- Protected routes
- Admin panel
- Password management

**No setup required** - just use it:
```python
from auth import get_current_user
```

### Database Ready
- SQLite configured
- User model exists
- Migration system ready
- Just add your tables

### Coding Standards Enforced
- Python: FastAPI patterns, proper imports, docstrings
- React: Functional components, hooks, Tailwind CSS
- Git: Descriptive commits, small frequent saves
- LangChain: Proper agent structure, tool organization

---

## File Structure

```
boot_lang/
├── boot_files/          # Cursor rules (.mdc files) - AI guidance
├── prd/                 # Your PRD documents go here
├── imp_plans/           # Generated implementation plans
├── frontend/            # React application
│   ├── src/
│   │   ├── components/  # React components
│   │   └── contexts/    # Auth, state management
│   └── package.json
├── backend files/       # FastAPI (root level)
│   ├── app.py           # Main server
│   ├── auth.py          # Authentication
│   ├── database.py      # SQLite models
│   └── agents/          # LangChain agents (optional)
├── venv/                # Virtual environment
├── user_config.json     # Your preferences (created at setup)
└── startup.sh           # Setup script
```

---

## Commands You'll Use

### Working with Cursor (Natural Language)
```
"Build my latest PRD"
"Add login to this page"
"Create a table for storing tasks"
"Deploy to Azure"
"Check Azure logs"
"Test the API endpoints"
"Commit this code"
```

### Terminal Commands (Rarely Needed)
```bash
# Start backend
venv/bin/python app.py

# Start frontend
cd frontend && npm start

# Run tests
venv/bin/pytest

# Manual commit (Cursor usually does this)
git add . && git commit -m "message"
```

---

## Happy Path Summary

1. ✅ Install Cursor Pro with Claude 4.5 Sonnet
2. ✅ Download boot_lang repo
3. ✅ Run `startup.sh`
4. ✅ Build test page with Cursor
5. ✅ Test in localhost
6. ✅ Deploy test page to Azure
7. ✅ Verify deployment works
8. ✅ Configure user settings
9. ✅ Build PRD (tool, upload, or with Cursor)
10. ✅ Say "Build my latest PRD"
11. ✅ Test each phase in localhost
12. ✅ Deploy to Azure when complete
13. ✅ Share live application

---

## What Makes This Special

**Traditional coding:**
- Learn frameworks
- Set up auth from scratch
- Figure out deployment
- Debug obscure errors
- Weeks or months

**Boot_Lang + Cursor:**
- Describe what you want
- AI handles implementation
- Standards enforced automatically
- Testing guided at each step
- Deploy with one command
- Days or hours

---

## Getting Help

- **Stuck?** Ask Cursor: "What should I do next?"
- **Error?** Cursor will read logs and suggest fixes
- **Confused?** Review this workflow.md
- **Need examples?** Check `tenant/tenant_1/` for working code

---

## Next Steps

1. Install Cursor AI (Pro account)
2. Download this repository
3. Run `startup.sh`
4. Follow the prompts
5. Build your first test page
6. See it deployed
7. Start building your real application

**The setup script will guide you through everything.**
