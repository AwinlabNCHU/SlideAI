#!/bin/bash

echo "🚀 Deploying CORS fix v2 to Render.com..."

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# Check if remote is set up
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up git remote..."
    echo "Please enter your Render.com git repository URL:"
    read -r render_git_url
    git remote add origin "$render_git_url"
fi

# Add and commit changes
echo "📝 Committing CORS fixes v2..."
git add .
git commit -m "Fix CORS: explicit origins, removed custom OPTIONS handler, added test endpoint"

# Push to Render.com
echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ CORS fix v2 deployed! Your service should restart automatically."
echo "📊 Check the logs at: https://dashboard.render.com/web/srv-..."
echo ""
echo "🔍 The fix includes:"
echo "   - Explicit CORS origins including GitHub Pages"
echo "   - Removed custom OPTIONS handler (let FastAPI handle it)"
echo "   - Set allow_credentials=False for wildcard origins"
echo "   - Added /api/test-cors endpoint for testing"
echo ""
echo "🧪 Test CORS after deployment:"
echo "   - Visit: https://slideai.onrender.com/api/test-cors"
echo "   - Should return JSON with CORS origins"
echo ""
echo "⏳ Wait 1-2 minutes for the deployment to complete, then test your frontend." 