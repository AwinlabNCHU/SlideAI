#!/bin/bash

# 生產環境設定腳本
echo "=== SlideAI 前端生產環境設定 ==="
echo ""

# 檢查是否已經存在 .env.production
if [ -f ".env.production" ]; then
    echo "發現現有的 .env.production 文件"
    echo "當前內容："
    cat .env.production
    echo ""
    read -p "是否要重新設定？(y/n): " overwrite
    if [ "$overwrite" != "y" ]; then
        echo "取消設定"
        exit 0
    fi
fi

echo "請輸入您的 Render.com 後端 URL"
echo "例如：https://slideai-backend.onrender.com"
read -p "後端 URL: " backend_url

# 驗證 URL 格式
if [[ $backend_url =~ ^https://.*\.onrender\.com$ ]]; then
    echo "URL 格式正確"
else
    echo "警告：URL 格式可能不正確，請確認是否為 Render.com URL"
    read -p "是否繼續？(y/n): " continue_setup
    if [ "$continue_setup" != "y" ]; then
        echo "取消設定"
        exit 0
    fi
fi

# 創建 .env.production 文件
cat > .env.production << EOF
# 生產環境 API URL (Render.com 後端 URL)
VITE_API_URL=$backend_url
EOF

echo ""
echo "✅ 生產環境變數已設定完成！"
echo "後端 URL: $backend_url"
echo ""
echo "接下來請執行以下步驟："
echo "1. git add ."
echo "2. git commit -m 'Add production environment variables'"
echo "3. git push origin main"
echo ""
 