# 🚀 GitHub Pages 設定指南

## 📋 修復 GitHub Actions 權限問題

### 1. 啟用 GitHub Pages

1. **前往您的 GitHub 專案**
2. **點擊 Settings → Pages**
3. **設定 Source**:
   - **Source**: Deploy from a branch
   - **Branch**: `gh-pages` (如果不存在會自動創建)
   - **Folder**: `/ (root)`
4. **點擊 Save**

### 2. 設定 GitHub Actions 權限

1. **前往 Settings → Actions → General**
2. **在 "Workflow permissions" 區塊**:
   - 選擇 **"Read and write permissions"**
   - 勾選 **"Allow GitHub Actions to create and approve pull requests"**
3. **點擊 Save**

### 3. 設定 Secrets

1. **前往 Settings → Secrets and variables → Actions**
2. **點擊 "New repository secret"**
3. **添加以下 secret**:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://your-render-service.onrender.com`
4. **點擊 "Add secret"**

### 4. 手動觸發部署

如果自動部署失敗，可以手動觸發：

1. **前往 Actions 頁面**
2. **選擇 "Deploy to GitHub Pages" 工作流程**
3. **點擊 "Run workflow"**
4. **選擇 main 分支**
5. **點擊 "Run workflow"**

## 🔧 故障排除

### 問題 1: Permission denied to github-actions[bot]

**解決方案**:
1. 確認已設定 "Read and write permissions"
2. 確認 GitHub Pages 已啟用
3. 使用新的 `actions/deploy-pages@v4` 動作

### 問題 2: gh-pages 分支不存在

**解決方案**:
1. GitHub Actions 會自動創建 `gh-pages` 分支
2. 確保 GitHub Pages 設定為使用 `gh-pages` 分支

### 問題 3: 建置失敗

**解決方案**:
1. 檢查 Node.js 版本 (使用 18)
2. 確認 `package.json` 中的依賴版本
3. 檢查 `vite.config.js` 配置

## 📊 驗證部署

### 1. 檢查 Actions 狀態

1. **前往 Actions 頁面**
2. **查看最新的工作流程執行**
3. **確認所有步驟都成功**

### 2. 檢查 GitHub Pages

1. **前往 Settings → Pages**
2. **確認部署狀態為 "Your site is live"**
3. **點擊連結測試網站**

### 3. 測試功能

1. **訪問**: `https://AwinlabNCHU.github.io/SlideAI`
2. **測試註冊/登入功能**
3. **測試檔案上傳功能**
4. **檢查 API 連線**

## 🔄 更新流程

### 自動更新

每次推送到 `main` 分支時，GitHub Actions 會自動：
1. 建置前端應用程式
2. 部署到 GitHub Pages
3. 更新網站

### 手動更新

如果需要手動更新：
1. 推送程式碼到 `main` 分支
2. 前往 Actions 頁面
3. 手動觸發工作流程

## 📝 重要設定

### GitHub Pages 設定
- **Source**: Deploy from a branch
- **Branch**: `gh-pages`
- **Folder**: `/ (root)`

### Actions 權限
- **Workflow permissions**: Read and write permissions
- **Allow GitHub Actions to create and approve pull requests**: ✅

### Secrets
- `VITE_API_URL`: 您的 Render.com 後端 URL

## 🆘 常見錯誤

### Error 403: Permission denied
- 檢查 Actions 權限設定
- 確認 GitHub Pages 已啟用
- 使用正確的部署動作

### Build failed
- 檢查 Node.js 版本
- 確認依賴版本相容
- 查看建置日誌

### CORS error
- 確認 `VITE_API_URL` 設定正確
- 檢查後端 CORS 設定
- 確認前端和後端 URL 匹配

## 📞 支援

- GitHub Actions 文檔: https://docs.github.com/en/actions
- GitHub Pages 文檔: https://docs.github.com/en/pages
- Vite 部署文檔: https://vitejs.dev/guide/static-deploy.html 