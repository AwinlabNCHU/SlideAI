#!/bin/bash

echo "🚀 Deploying admin tools to Render.com..."

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
echo "📝 Committing admin tools..."
git add .
git commit -m "Add admin setup tools: set_admin.py and set_admin_render.py"

# Push to Render.com
echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ Admin tools deployed! Your service should restart automatically."
echo "📊 Check the logs at: https://dashboard.render.com/web/srv-..."
echo ""
echo "🔧 管理員設定方法:"
echo ""
echo "方法 1: 使用 Render.com Shell (推薦)"
echo "   1. 前往 Render.com 儀表板"
echo "   2. 點擊你的後端服務"
echo "   3. 點擊 'Shell' 標籤"
echo "   4. 執行: python set_admin_render.py"
echo ""
echo "方法 2: 使用完整版腳本"
echo "   1. 在 Shell 中執行: python set_admin.py"
echo "   2. 選擇選項 1 或 2 來設定管理員"
echo ""
echo "方法 3: 直接 SQL 查詢"
echo "   1. 前往 Render.com 儀表板"
echo "   2. 點擊你的 PostgreSQL 資料庫"
echo "   3. 點擊 'Connect' 標籤"
echo "   4. 執行: UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';"
echo ""
echo "⏳ 部署完成後，請使用上述方法之一來設定管理員。" 