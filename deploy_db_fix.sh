#!/bin/bash

echo "🚀 Deploying database schema fix to Render.com..."

# 檢查是否在正確的目錄
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 部署資料庫架構修復..."

# 部署後端
cd backend
if [ ! -d ".git" ]; then
    echo "📁 Initializing backend git repository..."
    git init
    git add .
    git commit -m "Initial commit"
fi

# 檢查遠端倉庫
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up backend git remote..."
    echo "Please enter your Render.com git repository URL:"
    read -r render_git_url
    git remote add origin "$render_git_url"
fi

# 提交並推送後端更改
echo "📝 Committing database schema fixes..."
git add .
git commit -m "Add UserFile table and file management API endpoints"

echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ Backend deployed!"

echo ""
echo "🔧 修復內容："
echo "   ✅ 新增 UserFile 資料表"
echo "   ✅ 新增檔案管理 API 端點"
echo "   ✅ 修復資料庫架構問題"
echo "   ✅ 新增檔案清理功能"
echo ""
echo "⏳ 請等待 3-5 分鐘讓部署完成，然後測試檔案管理功能。"
echo ""
echo "📋 部署完成後，請檢查："
echo "   1. 檔案管理頁面是否正常載入"
echo "   2. 是否還有 CORS 錯誤"
echo "   3. 檔案列表是否正常顯示" 