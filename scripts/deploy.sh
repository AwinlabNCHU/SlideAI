#!/bin/bash

# 部署腳本
set -e

echo "🚀 開始部署..."

# 檢查環境變數檔案
if [ ! -f .env.production ]; then
    echo "❌ 請先創建 .env.production 檔案"
    echo "💡 可以複製 env.production.example 作為範本"
    exit 1
fi

# 載入環境變數
source .env.production

echo "📦 建置 Docker 映像檔..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 停止現有服務..."
docker-compose -f docker-compose.prod.yml down

echo "🚀 啟動服務..."
docker-compose -f docker-compose.prod.yml up -d

echo "⏳ 等待服務啟動..."
sleep 30

echo "🔍 檢查服務狀態..."
docker-compose -f docker-compose.prod.yml ps

echo "✅ 部署完成！"
echo "🌐 前端: http://localhost"
echo "🔧 後端 API: http://localhost:8000"
echo "📊 資料庫: localhost:5432"

# 創建管理員帳號提示
echo ""
echo "💡 要創建管理員帳號，請執行："
echo "docker-compose -f docker-compose.prod.yml exec backend python create_admin.py <email> <password>" 