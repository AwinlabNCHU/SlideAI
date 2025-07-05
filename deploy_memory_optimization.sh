#!/bin/bash

echo "🚀 Deploying memory optimization to Render.com..."

# 檢查是否在正確的目錄
if [ ! -f "backend/main.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

echo "📦 部署記憶體優化版本..."

# 備份原始檔案
cd backend
cp main.py main_backup.py

# 替換為優化版本
cp main_optimized.py main.py

# 檢查遠端倉庫
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "🔗 Setting up backend git remote..."
    echo "Please enter your Render.com git repository URL:"
    read -r render_git_url
    git remote add origin "$render_git_url"
fi

# 提交並推送後端更改
echo "📝 Committing memory optimization..."
git add .
git commit -m "Optimize memory usage for Render.com free tier - Reduce file size limits, add garbage collection, chunked file uploads"

echo "🚀 Pushing to Render.com..."
git push origin main

echo "✅ Memory optimization deployed!"

echo ""
echo "🔧 優化內容："
echo "   ✅ 降低檔案大小限制到 25MB"
echo "   ✅ 降低檔案保留天數到 3 天"
echo "   ✅ 新增分塊檔案上傳"
echo "   ✅ 新增垃圾回收機制"
echo "   ✅ 限制資料庫查詢結果數量"
echo "   ✅ 優化檔案清理流程"
echo ""
echo "⏳ 請等待 3-5 分鐘讓部署完成。"
echo ""
echo "📋 部署完成後，請檢查："
echo "   1. 應用程式是否正常啟動"
echo "   2. 記憶體使用是否降低"
echo "   3. 檔案上傳是否正常"
echo "   4. 檔案管理功能是否正常" 