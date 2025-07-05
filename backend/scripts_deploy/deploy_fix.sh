#!/bin/bash

# 後端 CORS 修復部署腳本
echo "=== SlideAI 後端 CORS 修復部署 ==="
echo ""

# 檢查是否在正確的目錄
if [ ! -f "main.py" ]; then
    echo "❌ 錯誤：請在 backend 目錄中執行此腳本"
    exit 1
fi

echo "🔧 修復內容："
echo "1. 添加根路徑處理 (/)
echo "2. 改進 CORS 設定
echo "3. 添加 OPTIONS 請求處理
echo ""

# 檢查 Git 狀態
if [ -d ".git" ]; then
    echo "📊 Git 狀態："
    git status --porcelain
    echo ""
    
    # 提交更改
    echo "💾 提交更改..."
    git add .
    git commit -m "Fix CORS and add root endpoint for production"
    
    echo "🚀 推送到遠端倉庫..."
    git push origin main
    
    echo ""
    echo "✅ 代碼已推送到 GitHub"
    echo "🔄 Render.com 將自動重新部署"
    echo ""
    echo "⏳ 請等待 2-3 分鐘讓部署完成"
    echo "📊 您可以在 Render.com 控制台查看部署進度"
else
    echo "⚠️  警告：未檢測到 Git 倉庫"
    echo "請手動提交並推送更改到 GitHub"
fi

echo ""
echo "🔍 部署完成後，請測試以下端點："
echo "1. 根路徑: https://your-app-name.onrender.com/"
echo "2. 健康檢查: https://your-app-name.onrender.com/health"
echo "3. API 文檔: https://your-app-name.onrender.com/docs"
echo ""
echo "📱 前端測試頁面: https://your-username.github.io/your-repo/test" 