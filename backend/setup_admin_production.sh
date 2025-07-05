#!/bin/bash

# 生產環境管理員設定腳本
echo "=== SlideAI 生產環境管理員設定 ==="
echo ""

# 檢查是否提供了資料庫 URL
if [ -z "$DATABASE_URL" ]; then
    echo "❌ 錯誤：未設定 DATABASE_URL 環境變數"
    echo ""
    echo "請設定您的 Render.com 資料庫 URL："
    echo "export DATABASE_URL='postgresql://username:password@host:port/database'"
    echo ""
    echo "或者從 Render.com 控制台複製完整的資料庫連接字串"
    exit 1
fi

echo "🌐 檢測到生產環境"
echo "📊 資料庫: $DATABASE_URL"
echo ""

# 檢查 Python 環境
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤：未找到 Python3"
    echo "請確保已安裝 Python 3.7 或更高版本"
    exit 1
fi

# 檢查必要的 Python 套件
echo "🔍 檢查 Python 套件..."
python3 -c "import sqlalchemy, passlib, dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ 錯誤：缺少必要的 Python 套件"
    echo "請安裝：pip install sqlalchemy passlib python-dotenv psycopg2-binary"
    exit 1
fi

echo "✅ Python 環境檢查通過"
echo ""

# 執行管理員創建腳本
echo "🚀 開始創建管理員用戶..."
echo ""

python3 create_admin.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 管理員設定完成！"
    echo ""
    echo "接下來您可以："
    echo "1. 訪問您的 GitHub Pages 網站"
    echo "2. 使用剛創建的管理員帳戶登入"
    echo "3. 訪問 /admin 頁面查看管理員介面"
    echo ""
    echo "💡 提示：管理員可以無限制使用所有 AI 功能"
else
    echo ""
    echo "❌ 管理員創建失敗"
    echo "請檢查錯誤訊息並重試"
    exit 1
fi 