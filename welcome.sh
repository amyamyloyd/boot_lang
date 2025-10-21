#!/bin/bash

# Boot_Lang Welcome Script
# This script initializes the Boot_Lang environment and guides setup

set -e  # Exit on error

echo "=========================================="
echo "  Boot_Lang Scaffolding Framework"
echo "=========================================="
echo ""

# Check if config has all required data
HAS_USER=$(python3 -c "import json; c=json.load(open('user_config.json')); print('yes' if c.get('user_identity',{}).get('user_name') else 'no')" 2>/dev/null || echo "no")

if [ "$HAS_USER" == "yes" ] && grep -q '"setup_complete": true' user_config.json; then
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

# Wait for setup server to shut down (automation.sh kills it when complete)
wait $SETUP_PID

echo ""
echo "=========================================="
echo "  🎉 Setup Complete!"
echo "=========================================="
echo ""

# Verify config was saved
if [ ! -f "user_config.json" ]; then
    echo "❌ Error: user_config.json not found"
    echo "Setup was not completed. Run './welcome.sh' again to retry."
    exit 1
fi

# Check if setup was completed
if ! grep -q '"setup_complete": true' user_config.json; then
    echo "Setup not completed. Run './welcome.sh' again to resume."
    exit 0
fi

# Load configuration to show results
USER_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['user_name'])" 2>/dev/null || echo "User")
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('user_config.json'))['user_identity']['project_name'])" 2>/dev/null || echo "Project")
AZURE_STATIC_URL=$(python3 -c "import json; print(json.load(open('user_config.json'))['azure_settings']['static_web_app_url'])" 2>/dev/null || echo "")

echo "✓ Configuration complete for: $USER_NAME"
echo "✓ Project: $PROJECT_NAME"
echo ""

# Check if we have deployment URL from automation
if [ -f "setup_progress.log" ] && grep -q "COMPLETE:" setup_progress.log; then
    DEPLOYED_URL=$(grep "COMPLETE:" setup_progress.log | tail -1 | cut -d: -f2-)
    if [ -n "$DEPLOYED_URL" ]; then
        echo "🌐 Your site is deployed at:"
        echo "   $DEPLOYED_URL"
        echo ""
    fi
fi

echo "Your environment is ready!"
echo ""
echo "Next steps:"
echo "  1. Build a PRD (tell Cursor: 'Help me build a PRD')"
echo "  2. Build from PRD (tell Cursor: 'Build my PRD')"
echo "  3. Start services (tell Cursor: 'Start backend' and 'Start frontend')"
echo ""
echo "Happy building! 🚀"
echo ""

