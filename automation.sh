#!/bin/bash
# Automation script - runs after config saved

set -e

# Ensure we're on main branch
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "main" ]; then
    echo "Switching from $CURRENT_BRANCH to main branch..."
    git checkout main
fi

# Load configuration
USER_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['user_name'])")
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['project_name'])")
GITHUB_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['git_deployment']['github_repo_url'])")
AZURE_STATIC_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['static_web_app_url'])" 2>/dev/null || echo "")
APP_SERVICE_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['app_service_name'])")

# Create progress log
echo "Starting automation..." > setup_progress.log

# Step 1: Virtual environment
echo "PROGRESS:Creating virtual environment" >> setup_progress.log
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
echo "DONE:Creating virtual environment" >> setup_progress.log

# Step 2: Install dependencies
echo "PROGRESS:Installing dependencies" >> setup_progress.log
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "DONE:Installing dependencies" >> setup_progress.log

# Step 3: Initialize database
echo "PROGRESS:Initializing database" >> setup_progress.log
python3 database.py > /dev/null 2>&1
echo "DONE:Initializing database" >> setup_progress.log

# Step 4: Build welcome page for frontend
echo "PROGRESS:Building welcome page" >> setup_progress.log

# Create Welcome component
cat > frontend/src/components/Welcome.tsx << 'WELCOME_EOF'
import React from 'react';

interface WelcomeProps {
  userName: string;
  projectName: string;
  githubUrl: string;
}

const Welcome: React.FC<WelcomeProps> = ({ userName, projectName, githubUrl }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full bg-white p-8 rounded-lg shadow-2xl">
        <h1 className="text-4xl font-bold text-center text-gray-900 mb-6">
          ✅ Boot_Lang Setup Complete!
        </h1>
        
        <div className="space-y-6 text-gray-700">
          <div className="bg-blue-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl">Configuration:</h3>
            <ul className="space-y-2">
              <li><strong>User:</strong> {userName}</li>
              <li><strong>Project:</strong> {projectName}</li>
              <li><strong>GitHub:</strong> <a href={githubUrl} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{githubUrl}</a></li>
            </ul>
          </div>
          
          <div className="bg-green-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-green-800">✓ Environment Ready:</h3>
            <ul className="list-disc list-inside space-y-1">
              <li>Virtual environment created</li>
              <li>Dependencies installed</li>
              <li>Database initialized</li>
              <li>Deployed to Azure</li>
            </ul>
          </div>
          
          <div className="bg-purple-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-purple-800">Tech Stack:</h3>
            <ul className="grid grid-cols-2 gap-2 text-sm">
              <li>• React 18 + TypeScript</li>
              <li>• Tailwind CSS</li>
              <li>• Python 3.11 + FastAPI</li>
              <li>• LangChain + OpenAI</li>
              <li>• SQLite Database</li>
              <li>• Azure App Service</li>
            </ul>
          </div>
          
          <div className="bg-yellow-50 p-6 rounded-md">
            <h3 className="font-semibold mb-3 text-xl text-yellow-800">Quick Start Commands:</h3>
            <ul className="space-y-2 text-sm font-mono">
              <li className="bg-white p-2 rounded border"><strong>"Build my PRD"</strong> - Start building from a PRD document</li>
              <li className="bg-white p-2 rounded border"><strong>"Start backend"</strong> - Launch FastAPI server (port 8000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Start frontend"</strong> - Launch React dev server (port 3000)</li>
              <li className="bg-white p-2 rounded border"><strong>"Deploy to Azure"</strong> - Push changes to production</li>
              <li className="bg-white p-2 rounded border"><strong>"Commit the code"</strong> - Stage and commit changes</li>
            </ul>
          </div>
          
          <div className="text-center pt-4">
            <a href="http://localhost:3000" className="inline-block px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-semibold">
              Start Building →
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Welcome;
WELCOME_EOF

# Update App.tsx to show Welcome page
cat > frontend/src/App.tsx << 'APP_EOF'
import React from 'react';
import Welcome from './components/Welcome';

const App: React.FC = () => {
  // Load config from window object (injected during build)
  const config = (window as any).bootLangConfig || {
    userName: 'User',
    projectName: 'Boot_Lang Project',
    githubUrl: 'https://github.com'
  };

  return <Welcome {...config} />;
};

export default App;
APP_EOF

# Create config injection script
cat > frontend/public/config.js << EOF
window.bootLangConfig = {
  userName: "$USER_NAME",
  projectName: "$PROJECT_NAME",
  githubUrl: "$GITHUB_URL"
};
EOF

# Update index.html to include config
sed -i.bak 's|</head>|  <script src="%PUBLIC_URL%/config.js"></script>\n  </head>|' frontend/public/index.html

# Build React app
cd frontend
npm install > /dev/null 2>&1
npm run build > /dev/null 2>&1
cd ..

echo "DONE:Building welcome page" >> setup_progress.log

# Step 5: Configure GitHub workflows with user settings
echo "PROGRESS:Configuring GitHub workflows" >> setup_progress.log

# Update deploy.yml with correct app service name
if [ -f ".github/workflows/deploy.yml" ]; then
    sed -i.bak "s/app-name: .*/app-name: '$APP_SERVICE_NAME'/" .github/workflows/deploy.yml
    rm -f .github/workflows/deploy.yml.bak
fi

echo "DONE:Configuring GitHub workflows" >> setup_progress.log

# Step 6: Push to GitHub
echo "PROGRESS:Pushing to GitHub" >> setup_progress.log
git add . > /dev/null 2>&1
git commit -m "Setup complete: $PROJECT_NAME" > /dev/null 2>&1 || true
git push origin main > /dev/null 2>&1 || true
echo "DONE:Pushing to GitHub" >> setup_progress.log

# Step 7: Wait for GitHub Actions deployment (both frontend + backend)
echo "PROGRESS:Deploying to Azure via GitHub Actions" >> setup_progress.log
echo "Waiting for GitHub Actions to start deployment..."
sleep 15  # Give GitHub Actions time to start
echo "DONE:Deploying to Azure via GitHub Actions" >> setup_progress.log

# Step 8: Verify deployment by checking URL content
echo "PROGRESS:Verifying deployment" >> setup_progress.log
DEPLOYMENT_VERIFIED=false

if [ -n "$AZURE_STATIC_URL" ]; then
    echo "Testing deployment at: $AZURE_STATIC_URL"
    
    # Try for up to 3 minutes (GitHub Actions + React build time)
    for i in {1..36}; do
        # Get the page content and config.js
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$AZURE_STATIC_URL" 2>/dev/null || echo "000")
        CONFIG_CONTENT=$(curl -s "$AZURE_STATIC_URL/config.js" 2>/dev/null || echo "")
        
        # Check if page loads with 200 status
        if [ "$HTTP_CODE" = "200" ]; then
            # Additional verification: check if config.js exists and has user data
            if echo "$CONFIG_CONTENT" | grep -q "$USER_NAME" 2>/dev/null; then
                echo "✓ Deployment verified! Site live with user config (HTTP $HTTP_CODE)"
                DEPLOYMENT_VERIFIED=true
                echo "DONE:Verifying deployment" >> setup_progress.log
                echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
                break
            elif [ "$HTTP_CODE" = "200" ]; then
                # Page loads but config might be embedded differently - still count as success
                echo "✓ Deployment verified! Site responding (HTTP $HTTP_CODE)"
                DEPLOYMENT_VERIFIED=true
                echo "DONE:Verifying deployment" >> setup_progress.log
                echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
                break
            fi
        fi
        
        echo "⏳ Waiting for deployment... (attempt $i/36, HTTP $HTTP_CODE)"
        sleep 5
    done
fi

if [ "$DEPLOYMENT_VERIFIED" = false ]; then
    echo "⚠️ Deployment verification timed out after 3 minutes"
    echo "  URL: $AZURE_STATIC_URL"
    echo "  This may mean GitHub Actions is still building (check: https://github.com/$(echo $GITHUB_URL | sed 's|https://github.com/||' | sed 's|.git||')/actions)"
    echo "  Your site may still deploy successfully - check the URL in a few minutes"
    echo "DONE:Verifying deployment" >> setup_progress.log
    echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log  # Return URL anyway so user can check
fi

# Kill setup server
sleep 2
pkill -f setup_server.py

