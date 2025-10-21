You're in ask mode - I can't create files. Switch to agent mode or here's the content to copy:

```markdown
# Boot_Lang Scaffolding - Architecture Decisions

## Overview
This document captures key architecture decisions needed before executing the scaffolding build plan.

---

## 1. User Configuration Schema

### user_config.json Structure

```json
{
  "setup_complete": false,
  "user_identity": {
    "user_name": "",
    "project_name": ""
  },
  "azure_settings": {
    "app_service_name": "",
    "static_web_app_url": "",
    "resource_group": "",
    "region": "eastus2"
  },
  "git_deployment": {
    "default_branch_prefix": "feature/",
    "deployment_branch": "main"
  },
  "preferences": {
    "use_prd_tool": true,
    "auto_deploy": false,
    "openai_model_preference": "gpt-4",
    "timezone": "UTC"
  }
}
```

### Field Descriptions

**setup_complete:** Boolean flag - true when setup wizard finished

**user_identity:**
- `user_name` - User's name or identifier
- `project_name` - What they're calling their project

**azure_settings:**
- `app_service_name` - Azure App Service name
- `static_web_app_url` - Frontend deployment URL
- `resource_group` - Azure resource group name
- `region` - Deployment region (e.g., "eastus2", "westus2")

**git_deployment:**
- `default_branch_prefix` - How to name feature branches (e.g., "feature/", "poc/")
- `deployment_branch` - Which branch triggers deployment (typically "main")

**preferences:**
- `use_prd_tool` - Boolean, use localhost:3000 PRD builder vs manual
- `auto_deploy` - Boolean, auto-deploy on commit vs manual trigger
- `openai_model_preference` - Which GPT model for PRD tool ("gpt-4", "gpt-3.5-turbo")
- `timezone` - For timestamps in logs/commits

---

## 2. Setup Web Page Design

### How It Works

**Flow:**
1. User runs `./startup.sh`
2. Script starts minimal FastAPI server on localhost:8001
3. Opens browser to `http://localhost:8001/setup`
4. User fills form
5. Click "Save Progress" → partial config saved, can exit and resume
6. Click "Save & Complete Setup" → saves config + triggers automation

### UI Structure

**40/60 Split Layout:**

**Left Panel (40%):**
- Header: "Boot_Lang Setup Wizard"
- Progress tracking:
  - Progress bar: "5/10 fields complete - 50%"
  - Visual checklist with status:
    - ✅ User name (completed)
    - ✅ Project name (completed)
    - ✅ Azure app service name (completed)
    - ⬜ Azure region (not started)
    - ⬜ Resource group (not started)
    - etc.
- Current step indicator: "Step 2 of 4: Azure Configuration"

**Right Panel (60%):**
- Form fields for current section
- Field validation and help text
- "Save Progress" button (bottom left)
- "Save & Complete Setup" button (bottom right, primary)
- Success/error messages

### Form Sections

**Section 1: User Identity (Required)**
- User name (text input)
- Project name (text input)

**Section 2: Azure Configuration (Required)**
- App Service name (text input with validation)
- Static Web App URL (auto-populated from Azure or manual)
- Resource group (text input)
- Region (dropdown: eastus2, westus2, etc.)

**Section 3: Git & Deployment (Required)**
- Branch prefix (text input, default: "feature/")
- Deployment branch (text input, default: "main")

**Section 4: Preferences (Optional)**
- Use PRD Tool (checkbox, default: true)
- Auto-deploy (checkbox, default: false)
- OpenAI model (dropdown: gpt-4, gpt-3.5-turbo)
- Timezone (dropdown, default: UTC)

### After "Save & Complete Setup"

**Automation sequence:**
1. Write `user_config.json` with `setup_complete: true`
2. Create/activate venv
3. Install dependencies
4. Initialize database
5. Build simple test page (file upload or form)
6. Deploy test page to Azure
7. Show success page with:
   - ✅ Configuration saved
   - ✅ Environment ready
   - ✅ Test deployment: [Azure URL]
   - Next steps: "Build your first app"

---

## 3. Branch Naming Strategy

### Convention
```
<type>/<description>
```

**Types:**
- `feature/` - New features
- `poc/` - POC applications
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Testing/experimentation

**Examples:**
- `feature/vocabulary-app`
- `poc/customer-feedback`
- `fix/login-redirect`

**Deployment triggers:**
- `main` branch → Production Azure instance
- Other branches → Can manually deploy to staging/test slots

**Stored in:** `user_config.json` → `git_deployment.default_branch_prefix`

---

## 4. Command Syntax

### PRD Commands

**Primary command:**
```
"Build my latest PRD"
```

**How it works:**
1. Cursor checks `/prd/` folder
2. Finds most recent .md file by timestamp
3. Reads and analyzes PRD
4. Confirms intent with user
5. Generates implementation plan
6. Begins phased build

**Alternative commands (all work the same):**
- "Implement my latest PRD"
- "Build the PRD"
- "Start building from PRD"

**Specific PRD command:**
```
"Build the vocabulary app PRD"
```
Cursor searches `/prd/` for file matching "vocabulary"

### Setup Commands

**During setup wizard:**
```
"Run setup wizard"
"Configure Boot_Lang"
"Start setup"
```

**After setup:**
```
"Show my configuration"
"Update configuration"
```

### Deployment Commands

```
"Deploy to Azure"
"Deploy this to production"
"Push to Azure"
```

**All trigger:** azure.mdc rule → creates branch → pushes → monitors deployment

---

## 5. LangChain vs Langflow Decision

### Both - Here's Why:

**LangChain (Code-Based):**
- For developers comfortable with Python
- Full control and customization
- Better for complex logic
- Examples: `agents/poc_agent.py`

**Langflow (Visual Flow Builder):**
- For non-developers or rapid prototyping
- Drag-and-drop interface
- Quick iterations
- Export to LangChain code

**Integration:**
- Langflow runs separately (localhost:7860)
- Export Langflow flows → LangChain code
- Both approaches available in scaffold
- User chooses based on comfort level

**Requirements.txt includes both:**
- `langchain>=0.1.0`
- `langflow>=1.0.0` (to be added)

---

## 6. Setup Web Page Implementation

### Technical Specs

**Backend:**
- Minimal FastAPI app: `setup_server.py`
- Single route: `/setup` (GET for page, POST for save)
- Port: 8001 (avoids conflict with main app on 8000)
- Auto-shutdown after "Save & Complete"

**Frontend:**
- Single HTML file with inline CSS/JS (no build step)
- Tailwind via CDN
- Progressive form (show/hide sections)
- Local storage for draft saves
- AJAX POST to save config

**Files:**
- `setup_server.py` - FastAPI server for setup
- `templates/setup.html` - Setup wizard page
- Called by `startup.sh`

### Startup Script Flow

```bash
#!/bin/bash

# 1. Check if user_config.json exists and setup_complete=true
if [ -f "user_config.json" ] && grep -q '"setup_complete": true' user_config.json; then
  echo "Setup already complete. Starting services..."
  # Skip to venv activation and service start
else
  echo "Starting setup wizard..."
  # 2. Start setup server
  python3 setup_server.py &
  SETUP_PID=$!
  
  # 3. Open browser
  sleep 2
  open http://localhost:8001/setup
  
  # 4. Wait for setup to complete (server shuts down when done)
  wait $SETUP_PID
  
  echo "Setup complete. Continuing with automation..."
fi

# 5. Create/activate venv
# 6. Install dependencies
# 7. Initialize database
# 8. Build test page
# 9. Deploy test page
# 10. Present workflow options
```

---

## 7. /prd/ Folder Structure

### Directory Layout
```
/prd/
  vocabulary_app_20251021.md
  customer_feedback_20251020.md
  expense_tracker_20251019.md
  .latest -> vocabulary_app_20251021.md (symlink)
```

**Naming convention:** `<app_name>_<YYYYMMDD>.md`

**Cursor detection:**
- Checks `/prd/` folder
- Sorts by timestamp in filename
- Reads most recent OR follows `.latest` symlink
- Confirms with user before proceeding

---

## Decision Summary

| Decision | Choice | Status |
|----------|--------|--------|
| user_config.json schema | 10-12 fields across 4 sections | ✅ Defined |
| Config collection | Web page on localhost:8001 | ✅ Decided |
| Setup wizard UI | 40/60 split, progress tracking | ✅ Designed |
| Branch naming | `<type>/<description>` | ✅ Defined |
| PRD command | "Build my latest PRD" | ✅ Defined |
| PRD folder | `/prd/` with timestamp naming | ✅ Defined |
| LangChain vs Langflow | Both included | ✅ Decided |

**All architecture decisions made. Ready for implementation.**

---

## Next Steps

1. Create `setup_server.py` and `templates/setup.html`
2. Build `startup.sh` script
3. Implement `/prd/` folder monitoring in rules
4. Create 5 missing .mdc rules
5. Follow execution order in missing_claude.md
```

Create this as `boot_files/scaffolding.md`?