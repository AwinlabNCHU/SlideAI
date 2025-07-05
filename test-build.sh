#!/bin/bash

# 本地建置測試腳本
set -e

echo "🧪 測試前端建置..."

cd frontend

echo "📦 清理舊的依賴..."
rm -rf node_modules package-lock.json

echo "🔧 安裝依賴..."
npm install

echo "🏗️ 建置專案..."
npm run build

echo "✅ 建置成功！"
echo "📁 建置結果位於: frontend/dist/"

# 檢查建置結果
if [ -d "dist" ]; then
    echo "📊 建置檔案統計："
    find dist -type f | wc -l
    echo "📋 主要檔案："
    ls -la dist/
else
    echo "❌ 建置失敗：dist 目錄不存在"
    exit 1
fi 