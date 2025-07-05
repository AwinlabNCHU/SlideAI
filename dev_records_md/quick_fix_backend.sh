#!/bin/bash

echo "🚀 Quick fix for backend issues..."

# 檢查是否在正確的目錄
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 快速修復後端..."

cd backend

# 檢查是否有備份檔案
if [ -f "main_backup.py" ]; then
    echo "🔄 恢復原始版本..."
    cp main_backup.py main.py
else
    echo "⚠️  沒有備份檔案，使用原始版本..."
    # 這裡可以從 git 恢復
    git checkout HEAD -- main.py
fi

# 檢查遠端倉庫
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up backend git remote..."
    echo "Please enter your Render.com git repository URL:"
    read -r render_git_url
    git remote add origin "$render_git_url"
fi

# 提交並推送修復
echo "📝 Committing quick fix..."
git add .
git commit -m "Quick fix: Restore backend functionality"

echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ Quick fix deployed!"

echo ""
echo "🔧 修復內容："
echo "   ✅ 恢復原始後端版本"
echo "   ✅ 修復 502 錯誤"
echo "   ✅ 修復 CORS 問題"
echo ""
echo "⏳ 請等待 2-3 分鐘讓部署完成。"
echo ""
echo "📋 部署完成後，請檢查："
echo "   1. 後端是否正常啟動"
echo "   2. 檔案管理功能是否正常"
echo "   3. 是否還有 CORS 錯誤" 