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
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Step 2: Install dependencies
echo "Step 2/6: Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo "✓ Dependencies installed"
echo ""

# Step 3: Initialize database
echo "Step 3/6: Initializing database..."
python3 database.py
echo "✓ Database initialized"
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
echo "This requires Cursor AI to implement a simple test page."
echo "Please tell Cursor: 'Build a simple file upload test page'"
echo ""
echo "Press Enter when test page is ready and tested in localhost..."
read -r

# Step 6: Deploy to Azure
echo "Step 6/6: Deploying to Azure..."
if [ -n "$GITHUB_URL" ]; then
    git add .
    git commit -m "Initial setup: $PROJECT_NAME" || true
    git push -u origin main
    echo "✓ Pushed to GitHub"
    echo ""
    echo "GitHub Actions will deploy to Azure automatically"
    echo "Check your repo's Actions tab for deployment status"
else
    echo "⚠ Skipping GitHub push (no repo URL configured)"
fi

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Wait for Azure deployment to complete"
echo "  2. Build a PRD (tell Cursor: 'Help me build a PRD')"
echo "  3. Build from PRD (tell Cursor: 'Build my PRD')"
echo ""
echo "Available commands: Run 'Show my config' in Cursor to see all commands"
echo ""

