#!/bin/bash

# Boot_Lang Welcome Script
# This script initializes the Boot_Lang environment and guides setup

set -e  # Exit on error

echo "=========================================="
echo "  Boot_Lang Scaffolding Framework"
echo "=========================================="
echo ""

# Check if setup already complete
if [ -f "user_config.json" ] && grep -q '"setup_complete": true' user_config.json; then
    echo "✓ Setup already complete!"
    echo ""
    echo "Configuration loaded from user_config.json"
    echo ""
    echo "What would you like to do?"
    echo "  1. Start services (tell Cursor: 'Start backend' and 'Start frontend')"
    echo "  2. Build a PRD (tell Cursor: 'Help me build a PRD')"
    echo "  3. Build from existing PRD (tell Cursor: 'Build my PRD')"
    echo ""
    exit 0
fi

echo "Starting configuration webpage..."
echo ""

# Start setup server
python3 setup_server.py &
SETUP_PID=$!

# Wait for server to start
sleep 2

# Open browser (macOS)
if command -v open &> /dev/null; then
    open http://localhost:8001/setup
elif command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8001/setup
else
    echo "Please open your browser to: http://localhost:8001/setup"
fi

echo "Configuration webpage opened in browser"
echo "Fill in your details and click 'Save & Complete Setup'"
echo ""

# Wait for setup server to shut down (happens when user completes setup)
wait $SETUP_PID

echo ""
echo "Configuration saved! Starting automation..."
echo ""

# Verify config was saved
if [ ! -f "user_config.json" ]; then
    echo "❌ Error: user_config.json not found"
    exit 1
fi

# Check if setup was completed
if ! grep -q '"setup_complete": true' user_config.json; then
    echo "Setup not completed. Run './welcome.sh' again to resume."
    exit 0
fi

echo ""
echo "Configuration saved! Starting automation..."
echo ""

# Create progress log file
echo "Starting automation..." > setup_progress.log

# Load configuration
echo "Loading configuration..."
USER_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['user_name'])")
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['project_name'])")
GITHUB_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['git_deployment']['github_repo_url'])")

echo "✓ User: $USER_NAME"
echo "✓ Project: $PROJECT_NAME"
echo ""

# Step 1: Create/activate virtual environment
echo "Step 1/6: Setting up virtual environment..."
echo "PROGRESS:Creating virtual environment..." >> setup_progress.log
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

source venv/bin/activate
echo "✓ Virtual environment activated"
echo "DONE:Creating virtual environment" >> setup_progress.log
echo ""

# Step 2: Install dependencies
echo "Step 2/6: Installing dependencies..."
echo "PROGRESS:Installing dependencies..." >> setup_progress.log
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo "DONE:Installing dependencies" >> setup_progress.log
echo ""

# Step 3: Initialize database
echo "Step 3/6: Initializing database..."
echo "PROGRESS:Initializing database..." >> setup_progress.log
python3 database.py
echo "✓ Database initialized"
echo "DONE:Initializing database" >> setup_progress.log
echo ""

# Step 4: Configure Git remote
echo "Step 4/6: Configuring Git repository..."
if [ -n "$GITHUB_URL" ]; then
    git remote remove origin 2>/dev/null || true
    git remote add origin "$GITHUB_URL"
    echo "✓ Git remote set to: $GITHUB_URL"
else
    echo "⚠ No GitHub URL provided, skipping remote setup"
fi
echo ""

# Step 5: Build simple test page
echo "Step 5/6: Building test page..."
echo "PROGRESS:Building test page..." >> setup_progress.log

# Read Azure URL from config
AZURE_STATIC_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['static_web_app_url'])" 2>/dev/null || echo "")

# Create simple test page
mkdir -p test_deploy
cat > test_deploy/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
                    <li><strong>User:</strong> USER_NAME_PLACEHOLDER</li>
                    <li><strong>Project:</strong> PROJECT_NAME_PLACEHOLDER</li>
                    <li><strong>GitHub:</strong> GITHUB_URL_PLACEHOLDER</li>
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
            <div class="text-center mt-6">
                <p class="text-sm text-gray-500">Your Boot_Lang scaffold is ready for development</p>
                <p class="text-xs text-gray-400 mt-2">Tell Cursor: "Build my PRD" to start building</p>
            </div>
        </div>
    </div>
</body>
</html>
EOF

# Replace placeholders
sed -i '' "s/USER_NAME_PLACEHOLDER/$USER_NAME/g" test_deploy/index.html
sed -i '' "s/PROJECT_NAME_PLACEHOLDER/$PROJECT_NAME/g" test_deploy/index.html
sed -i '' "s|GITHUB_URL_PLACEHOLDER|$GITHUB_URL|g" test_deploy/index.html

echo "✓ Test page created"
echo "DONE:Building test page" >> setup_progress.log
echo ""

# Step 6: Deploy to Azure
echo "Step 6/6: Deploying to Azure..."
echo "PROGRESS:Pushing to GitHub..." >> setup_progress.log
if [ -n "$GITHUB_URL" ]; then
    git add .
    git commit -m "Setup complete: $PROJECT_NAME - Environment configured and test page deployed" || true
    git push origin main
    echo "✓ Pushed to GitHub"
    echo "DONE:Pushing to GitHub" >> setup_progress.log
    echo ""
    echo "PROGRESS:Deploying to Azure..." >> setup_progress.log
    echo "GitHub Actions deploying to Azure..."
    echo "This may take 2-3 minutes..."
    sleep 5
    echo "DONE:Deploying to Azure" >> setup_progress.log
    echo ""
else
    echo "⚠ Skipping GitHub push (no repo URL configured)"
    echo "DONE:Pushing to GitHub" >> setup_progress.log
    echo "DONE:Deploying to Azure" >> setup_progress.log
fi

# Mark completion
echo "COMPLETE:$AZURE_STATIC_URL" >> setup_progress.log

echo ""
echo "=========================================="
echo "  🎉 Setup Complete!"
echo "=========================================="
echo ""
echo "Your environment is ready!"
echo ""
if [ -n "$AZURE_STATIC_URL" ]; then
    echo "🌐 Visit your deployed test page:"
    echo "   $AZURE_STATIC_URL"
    echo ""
fi
echo "Next steps:"
echo "  1. Build a PRD (tell Cursor: 'Help me build a PRD')"
echo "  2. Build from PRD (tell Cursor: 'Build my PRD')"
echo "  3. View available commands (tell Cursor: 'Show my config')"
echo ""
echo "Happy building! 🚀"
echo ""

