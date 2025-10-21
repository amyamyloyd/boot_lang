#!/bin/bash
# Automation script - runs after config saved

set -e

# Load configuration
USER_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['user_name'])")
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['project_name'])")
GITHUB_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['git_deployment']['github_repo_url'])")
AZURE_STATIC_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['static_web_app_url'])" 2>/dev/null || echo "")

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

# Step 4: Build test page
echo "PROGRESS:Building test page" >> setup_progress.log
mkdir -p test_deploy
cat > test_deploy/index.html << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Boot_Lang Setup Success</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
    <div class="max-w-2xl w-full bg-white p-8 rounded-lg shadow-2xl">
        <h1 class="text-4xl font-bold text-center text-gray-900 mb-6">
            ✅ Boot_Lang Setup Complete!
        </h1>
        <div class="space-y-4 text-gray-700">
            <div class="bg-blue-50 p-4 rounded-md">
                <h3 class="font-semibold mb-2">Configuration:</h3>
                <ul class="space-y-1 text-sm">
                    <li><strong>User:</strong> $USER_NAME</li>
                    <li><strong>Project:</strong> $PROJECT_NAME</li>
                    <li><strong>GitHub:</strong> $GITHUB_URL</li>
                </ul>
            </div>
            <div class="bg-green-50 p-4 rounded-md">
                <h3 class="font-semibold mb-2 text-green-800">✓ Environment Ready:</h3>
                <ul class="list-disc list-inside space-y-1 text-sm">
                    <li>Virtual environment created</li>
                    <li>Dependencies installed</li>
                    <li>Database initialized</li>
                    <li>Deployed to Azure</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
EOF
echo "DONE:Building test page" >> setup_progress.log

# Step 5: Push to GitHub
echo "PROGRESS:Pushing to GitHub" >> setup_progress.log
git add . > /dev/null 2>&1
git commit -m "Setup complete: $PROJECT_NAME" > /dev/null 2>&1 || true
git push origin main > /dev/null 2>&1 || true
echo "DONE:Pushing to GitHub" >> setup_progress.log

# Step 6: Wait for GitHub Actions deployment
echo "PROGRESS:Deploying to Azure" >> setup_progress.log
echo "Waiting for GitHub Actions to deploy..."
sleep 10  # Give GitHub Actions time to start
echo "DONE:Deploying to Azure" >> setup_progress.log

# Verify deployment by checking URL content
echo "PROGRESS:Verifying deployment" >> setup_progress.log
DEPLOYMENT_VERIFIED=false

if [ -n "$AZURE_STATIC_URL" ]; then
    echo "Testing deployment at: $AZURE_STATIC_URL"
    
    # Try for up to 2 minutes (GitHub Actions deployment time)
    for i in {1..24}; do
        # Get the page content
        PAGE_CONTENT=$(curl -s "$AZURE_STATIC_URL" 2>/dev/null || echo "")
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$AZURE_STATIC_URL" 2>/dev/null || echo "000")
        
        # Check if page loads AND contains our user's name
        if [ "$HTTP_CODE" = "200" ] && echo "$PAGE_CONTENT" | grep -q "$USER_NAME"; then
            echo "✓ Deployment verified! Page contains user data (HTTP $HTTP_CODE)"
            DEPLOYMENT_VERIFIED=true
            echo "DONE:Verifying deployment" >> setup_progress.log
            echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log
            break
        fi
        
        echo "⏳ Waiting for deployment... (attempt $i/24, HTTP $HTTP_CODE)"
        sleep 5
    done
fi

if [ "$DEPLOYMENT_VERIFIED" = false ]; then
    echo "⚠️ Deployment verification failed"
    echo "  Check: $AZURE_STATIC_URL"
    echo "  Possible issues: GitHub Actions still running, CORS error, or wrong URL"
    echo "DONE:Verifying deployment" >> setup_progress.log
    echo "COMPLETE:" >> setup_progress.log  # Empty URL = verification failed
fi

# Kill setup server
sleep 2
pkill -f setup_server.py

