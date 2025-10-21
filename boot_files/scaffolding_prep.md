# Boot_Lang Scaffolding - Architecture Decisions

## Overview
This document captures key architecture decisions for Phase 0 preparation before executing the full scaffolding build plan.

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
    "subscription_id": "",
    "region": "eastus2"
  },
  "git_deployment": {
    "github_repo_url": "",
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

**setup_complete:** Boolean - true when config webpage finished

**user_identity:**
- `user_name` - User's name or identifier
- `project_name` - What they're calling their project

**azure_settings:**
- `app_service_name` - Azure App Service name (backend)
- `static_web_app_url` - Frontend deployment URL
- `resource_group` - Azure resource group name
- `subscription_id` - Azure subscription ID (for CLI access)
- `region` - Deployment region (e.g., "eastus2", "westus2")

**git_deployment:**
- `github_repo_url` - User's GitHub repo (they create, we push to it)
- `deployment_branch` - Always "main" (triggers Azure deployment)

**preferences:**
- `use_prd_tool` - Boolean, use localhost:3000 PRD builder vs manual
- `auto_deploy` - Boolean, auto-deploy on commit vs manual trigger
- `openai_model_preference` - Which GPT model for PRD tool ("gpt-4", "gpt-3.5-turbo")
- `timezone` - For timestamps in logs/commits

---

## 2. Config Webpage Design

### How It Works

**Flow:**
1. User tells Cursor: "Run welcome"
2. Cursor runs `./welcome.sh`
3. Script starts minimal FastAPI server on localhost:8001
4. Opens browser to `http://localhost:8001/setup`
4. User fills form
5. Click "Save Progress" → partial config saved, can exit and resume
6. Click "Save & Complete Setup" → saves config + triggers automation

### UI Structure

**40/60 Split Layout:**

**Left Panel (40%):**
- Header: "Boot_Lang Configuration"
- Progress tracking:
  - Progress bar: "5/10 fields complete - 50%"
  - Visual checklist with status:
    - ✅ User name (completed)
    - ✅ Project name (completed)
    - ✅ GitHub repo URL (completed)
    - ⬜ Azure app service (not started)
    - ⬜ Resource group (not started)
    - etc.
- Current section: "Step 2 of 4: Azure Configuration"

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

**Section 2: Git Configuration (Required)**
- Your GitHub repo URL (text input with validation)
- Help text: "Create empty repo on GitHub first"

**Section 3: Azure Configuration (Required)**
- App Service name (text input)
- Static Web App URL (text input)
- Resource group (text input)
- Subscription ID (text input)
- Region (dropdown: eastus2, westus2, centralus, etc.)

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
5. Build welcome page with user info
6. Update GitHub workflows with user's app service name
7. Push to user's GitHub main branch
8. GitHub Actions automatically deploys to Azure (using secrets set via Azure Portal)
9. Poll Azure URL to verify deployment
10. Show success page with:
   - ✅ Configuration saved
   - ✅ Environment ready
   - ✅ Pushed to GitHub: [repo URL]
   - ✅ Test deployment: [Azure URL]
   - Next steps: "Build your first app"

---

## 3. Deployment Strategy

### Git Workflow
1. User clones boot_lang scaffold repo
2. Config webpage asks: "Your GitHub repo URL?"
3. Startup script changes remote to THEIR repo
4. All work pushes to their main branch
5. Main branch → deploys to Azure

**Branch naming:** Users can create feature branches but deploy from main

**No complex branching** - keep simple for non-technical users

---

## 4. Standard Commands

### 15 Core Commands (defined in startup_commands.mdc)

**Git/Version Control:**
1. "Commit the code"
2. "Roll back to last commit"
3. "Show recent commits"

**Deployment:**
4. "Deploy to Azure"
5. "Check deployment status"

**Services:**
6. "Restart services"
7. "Start backend"
8. "Start frontend"
9. "Stop all services"

**PRD/Development:**
10. "Build my PRD"
11. "Help me build a PRD"
12. "Show my config"

**Troubleshooting:**
13. "Check Azure logs"
14. "Check for errors"
15. "Test the app"

**All defined in:** `/cursor/rules/startup_commands.mdc` (always active)

---

## 5. LangChain & Langflow Integration

### Approach: Rules-Based, Not Pre-Built

**Decision:**
- ❌ No pre-built example agents in scaffold
- ✅ `langchain.mdc` rule guides building Python agents (already exists)
- ✅ `langflow.mdc` rule guides using visual flow builder (to be created)
- ✅ `guard.mdc` acts as router - detects when user wants to build agents

**When user says:** "I want to build an agent that..."

**guard.mdc detection logic:**
1. Detects "agent" keyword in user request
2. Asks: "Code-based (LangChain) or visual (Langflow)?"
3. Activates appropriate rule:
   - User chooses LangChain → `langchain.mdc` guides Python implementation
   - User chooses Langflow → `langflow.mdc` guides visual flow setup

**What exists:**
- ✅ POC Agent (internal - for PRD tool, not user-facing example)
- ✅ `langchain.mdc` (already in /cursor/rules/)
- ✅ File upload functionality (in poc_api.py)

**What to add:**
- ✅ `langflow.mdc` to /cursor/rules/
- ✅ Langflow to requirements.txt
- ✅ Agent detection in guard.mdc
- ✅ Langflow setup instructions in documentation

**Integration:**
- Langflow runs separately (localhost:7860 when user chooses it)
- Can export Langflow flows → LangChain code
- Both approaches available via rules
- User chooses based on comfort level

---

## 6. /prd/ Folder Structure

### Directory Layout
```
/prd/
  vocabulary_app_20251021.md
  customer_feedback_20251020.md
  expense_tracker_20251019.md
```

**Naming convention:** `<app_name>_<YYYYMMDD>.md`

**Cursor detection (in prd.mdc):**
- Checks `/prd/` folder exists
- Sorts files by date in filename
- Reads most recent file
- Confirms with user: "Build [app name]?"

**Created by:**
- PRD Builder tool (localhost:3000), OR
- User manually places PRD there, OR
- Cursor with prd.mdc guidance

---

## 7. Config Webpage - Multi-Deployment Support

### Future-Proof Design

**Deployment provider selection:**
- ☑ Azure (default, Phase 1)
- ☐ AWS (future)
- ☐ Google Cloud (future)
- ☐ Vercel (future)

**Form shows relevant fields based on selection:**

**Azure selected:**
- App Service name
- Static Web App URL
- Resource Group
- Subscription ID
- Region

**AWS selected (future):**
- Lambda function name
- S3 bucket
- Region
- AWS Access Key ID

**Benefits:**
- Add new deployment targets by creating new .mdc rules
- Config webpage collects provider-specific info
- GitHub Actions uses correct workflow
- Cursor loads correct rule (azure.mdc, aws.mdc, etc.)

---

## Decision Summary

| Decision | Choice | Status |
|----------|--------|--------|
| user_config.json schema | 4 sections, ~10 fields | ✅ Defined |
| Config collection method | Web page on localhost:8001 | ✅ Decided |
| Config webpage UI | 40/60 split, progress tracking, save buttons | ✅ Designed |
| Git workflow | User's GitHub repo, deploy from main | ✅ Defined |
| Standard commands | 15 core commands in startup_commands.mdc | ✅ Defined |
| PRD folder location | `/prd/` with timestamp naming | ✅ Defined |
| LangChain vs Langflow | Both via rules, no pre-built examples | ✅ Decided |
| Agent detection | guard.mdc routes to langchain.mdc or langflow.mdc | ✅ Defined |

**All Phase 0 architecture decisions made. Ready for implementation.**

---

## Next Steps - Phase 0 Implementation

### Before starting missing_claude.md execution:

1. ✅ Create `user_config.json` template
2. ✅ Create `/prd/` folder
3. ✅ Create `setup_server.py` and `templates/setup.html` (config webpage)
4. ✅ Build `welcome.sh` script (starts config webpage)
5. ✅ Add "Run welcome" command to startup_commands.mdc ✅ DONE
6. ✅ Update `guard.mdc` with agent detection logic
7. ✅ Create `langflow.mdc` rule
8. ✅ Add Langflow to requirements.txt

**Then proceed with missing_claude.md execution order.**

