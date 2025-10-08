```markdown
# Azure Deployment Setup Instructions

## Prerequisites
You have created:
- App Service: boot-lang
- Static Web App: boot-lang-frontend
- Resource Group: boot-lang_group

**App Service (boot-lang):**
Python backend that runs your FastAPI application. Hosts all API endpoints (auth, database, POC generation, file uploads). Accessible at: boot-lang-gscvbveeg3dvgefh.eastus2-01.azurewebsites.net

**Static Web App (boot-lang-frontend):**
React frontend that serves your UI. Auto-deploys from GitHub when you push to main. Users access your app here. Accessible at: https://proud-smoke-02a8bab0f.1.azurestaticapps.net

Backend = API server. Frontend = User interface. They talk to each other via CORS.

## Cursor Instructions

**Prompt 1: Configure CORS**
```
Using Azure CLI, configure CORS for App Service "boot-lang" in resource group "boot-lang_group":
- Add allowed origin: https://proud-smoke-02a8bab0f.1.azurestaticapps.net
- Add allowed origin: http://localhost:3000
- Enable credentials
```

**Prompt 2: Configure Frontend API URL**
```
Create frontend/src/config.ts that:
- Exports API_URL constant
- Uses environment detection (window.location.hostname)
- Returns localhost:8000 for local development
- Returns Azure backend URL for production deployment
- Update all frontend components to import API_URL from config
```

**Prompt 3: GitHub Actions Workflow**
```
Create .github/workflows/deploy.yml that:
- Triggers on push to main branch
- Deploys backend to Azure App Service "boot-lang"
- Uses Azure credentials from GitHub secrets: AZURE_WEBAPP_PUBLISH_PROFILE
```

**Prompt 4: Add Deployment Documentation**
```
Create getting_started/deployment.md explaining:
- How Azure deployment works
- How to get Azure publish profile and add to GitHub secrets
- How to trigger deployment (git push)
- Static Web App deploys automatically via GitHub integration
```
```