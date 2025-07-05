#!/bin/bash

echo "🚀 Deploying free tier admin setup solution to Render.com..."

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
echo "📝 Committing free tier admin setup..."
git add .
git commit -m "Add temporary admin setup endpoints for free tier"

# Push to Render.com
echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ Free tier admin setup deployed! Your service should restart automatically."
echo "📊 Check the logs at: https://dashboard.render.com/web/srv-..."
echo ""
echo "🔧 免費方案管理員設定方法:"
echo ""
echo "方法 1: 使用新增的 API 端點 (推薦)"
echo "   1. 部署完成後，使用以下命令:"
echo ""
echo "   # 查看所有使用者"
echo "   curl https://slideai.onrender.com/api/admin/list-users"
echo ""
echo "   # 設定管理員 (替換 your-email@example.com)"
echo "   curl -X POST 'https://slideai.onrender.com/api/admin/set-admin?email=your-email@example.com'"
echo ""
echo "方法 2: 使用 Render.com 資料庫查詢"
echo "   1. 前往 Render.com 儀表板"
echo "   2. 點擊你的 PostgreSQL 資料庫"
echo "   3. 點擊 'Connect' 標籤"
echo "   4. 執行 SQL 查詢:"
echo "      UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';"
echo ""
echo "方法 3: 使用 pgAdmin"
echo "   1. 下載 pgAdmin (免費)"
echo "   2. 使用 Render.com 提供的連接資訊"
echo "   3. 執行 SQL 查詢"
echo ""
echo "⚠️  重要提醒:"
echo "   - 設定完成後，建議移除臨時 API 端點"
echo "   - 這些端點沒有認證保護，僅用於初始設定"
echo ""
echo "⏳ 部署完成後，請使用上述方法之一來設定管理員。" 