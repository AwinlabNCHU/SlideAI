#!/bin/bash

# GitHub Actions 權限修復腳本
echo "🔧 修復 GitHub Actions 權限問題..."

# 檢查是否在正確的目錄
if [ ! -f ".github/workflows/deploy.yml" ]; then
    echo "❌ 請在專案根目錄執行此腳本"
    exit 1
fi

echo "✅ 已更新 GitHub Actions 工作流程"
echo ""
echo "📋 接下來需要手動完成的步驟："
echo ""
echo "1. 前往 GitHub 專案設定："
echo "   https://github.com/AwinlabNCHU/SlideAI/settings"
echo ""
echo "2. 設定 GitHub Pages："
echo "   - 前往 Settings → Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: gh-pages"
echo "   - Folder: / (root)"
echo "   - 點擊 Save"
echo ""
echo "3. 設定 Actions 權限："
echo "   - 前往 Settings → Actions → General"
echo "   - Workflow permissions: Read and write permissions"
echo "   - 勾選 'Allow GitHub Actions to create and approve pull requests'"
echo "   - 點擊 Save"
echo ""
echo "4. 設定 Secrets："
echo "   - 前往 Settings → Secrets and variables → Actions"
echo "   - 新增 VITE_API_URL: https://your-render-service.onrender.com"
echo ""
echo "5. 推送程式碼："
echo "   git add ."
echo "   git commit -m 'Fix GitHub Actions permissions'"
echo "   git push origin main"
echo ""
echo "6. 檢查部署："
echo "   - 前往 Actions 頁面查看部署狀態"
echo "   - 訪問 https://AwinlabNCHU.github.io/SlideAI"
echo ""
echo "📚 詳細說明請參考 github-pages-setup.md" 