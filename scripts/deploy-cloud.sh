#!/bin/bash

# 雲端部署快速設定腳本
set -e

echo "☁️ 雲端部署設定工具"
echo "=================="

# 獲取用戶輸入
read -p "請輸入您的 GitHub 用戶名: " GITHUB_USERNAME
read -p "請輸入您的 GitHub 專案名稱: " REPO_NAME
read -p "請輸入您的 Render.com 應用程式名稱: " RENDER_APP_NAME

# 生成後端 URL
BACKEND_URL="https://${RENDER_APP_NAME}.onrender.com"
FRONTEND_URL="https://${GITHUB_USERNAME}.github.io/${REPO_NAME}"

echo ""
echo "📋 配置摘要："
echo "GitHub 用戶名: $GITHUB_USERNAME"
echo "專案名稱: $REPO_NAME"
echo "Render.com 應用程式: $RENDER_APP_NAME"
echo "後端 URL: $BACKEND_URL"
echo "前端 URL: $FRONTEND_URL"
echo ""

read -p "確認以上設定正確嗎？(y/N): " CONFIRM
if [[ $CONFIRM != "y" && $CONFIRM != "Y" ]]; then
    echo "❌ 取消設定"
    exit 1
fi

echo ""
echo "🔧 開始更新配置檔案..."

# 1. 更新 render.yaml
echo "更新 render.yaml..."
sed -i.bak "s/your-app-name/$RENDER_APP_NAME/g" render.yaml
sed -i.bak "s|https://your-username.github.io|$FRONTEND_URL|g" render.yaml

# 2. 更新 frontend/vite.config.js
echo "更新 frontend/vite.config.js..."
sed -i.bak "s/TestApp/$REPO_NAME/g" frontend/vite.config.js

# 3. 更新 frontend/src/config/api.js
echo "更新 frontend/src/config/api.js..."
sed -i.bak "s|https://your-app-name.onrender.com|$BACKEND_URL|g" frontend/src/config/api.js

# 4. 創建 .env.production 範例
echo "創建環境變數範例..."
cat > frontend/.env.production.example << EOF
# 生產環境 API URL
VITE_API_URL=$BACKEND_URL
EOF

echo ""
echo "✅ 配置更新完成！"
echo ""
echo "📝 接下來需要手動完成的步驟："
echo ""
echo "1. 推送到 GitHub："
echo "   git add ."
echo "   git commit -m 'Configure cloud deployment'"
echo "   git push origin main"
echo ""
echo "2. 在 Render.com 部署後端："
echo "   - 登入 https://render.com"
echo "   - 點擊 'New +' → 'Blueprint'"
echo "   - 連接您的 GitHub 專案"
echo "   - 選擇包含 render.yaml 的專案"
echo "   - 點擊 'Apply'"
echo ""
echo "3. 在 GitHub 設定 Secrets："
echo "   - 前往專案 Settings → Secrets and variables → Actions"
echo "   - 新增 VITE_API_URL: $BACKEND_URL"
echo ""
echo "4. 啟用 GitHub Pages："
echo "   - 前往專案 Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: gh-pages"
echo "   - 點擊 Save"
echo ""
echo "5. 創建管理員帳號："
echo "   - 在 Render.com 使用 Shell 功能"
echo "   - 執行: python create_admin.py admin@example.com your_password"
echo ""
echo "🌐 部署完成後的 URL："
echo "前端: $FRONTEND_URL"
echo "後端: $BACKEND_URL"
echo ""
echo "📚 詳細說明請參考 CLOUD_DEPLOYMENT.md" 