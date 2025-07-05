#!/bin/bash

echo "🚀 Deploying authentication fix to GitHub Pages..."

# Check if we're in the frontend directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the frontend directory"
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
    echo "Please enter your GitHub repository URL:"
    read -r github_repo_url
    git remote add origin "$github_repo_url"
fi

# Add and commit changes
echo "📝 Committing authentication fixes..."
git add .
git commit -m "Fix authentication: improve token handling in apiRequest function"

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git push origin main

echo "✅ Authentication fix deployed! GitHub Actions will build and deploy to Pages."
echo "📊 Check the deployment at: https://github.com/awinlabnchu/awinlabnchu.github.io/actions"
echo ""
echo "🔍 The fix includes:"
echo "   - Fixed token handling in apiRequest function"
echo "   - Prevents localStorage token from overriding explicit Authorization headers"
echo "   - Ensures fresh tokens from login are used properly"
echo ""
echo "⏳ Wait 2-3 minutes for GitHub Actions to complete, then test your login." 