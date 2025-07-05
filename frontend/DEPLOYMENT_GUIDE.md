# 前端部署指南

## 環境變數設定

### 1. 創建生產環境變數文件

在 `frontend` 目錄下創建 `.env.production` 文件：

```bash
# 生產環境 API URL (Render.com 後端 URL)
# 請將 your-app-name 替換為您的 Render.com 應用程式名稱
VITE_API_URL=https://your-app-name.onrender.com
```

### 2. 更新您的 Render.com 後端 URL

請將上面的 `your-app-name` 替換為您在 Render.com 上實際的應用程式名稱。

例如，如果您的 Render.com 應用程式 URL 是 `https://slideai-backend.onrender.com`，那麼設定應該是：

```
VITE_API_URL=https://slideai-backend.onrender.com
```

### 3. 重新部署前端

設定好環境變數後，需要重新部署前端：

1. 提交更改到 GitHub：
```bash
git add .
git commit -m "Update API configuration for production"
git push origin main
```

2. GitHub Actions 會自動重新部署到 GitHub Pages

## 驗證部署

部署完成後，您可以：

1. 訪問您的 GitHub Pages 網站
2. 嘗試登入功能
3. 檢查瀏覽器開發者工具的 Network 標籤，確認 API 請求是否指向正確的後端 URL

## 故障排除

### 問題：登入時出現 CORS 錯誤

如果遇到 CORS 錯誤，請確認：

1. Render.com 後端的 CORS 設定是否正確
2. 環境變數 `VITE_API_URL` 是否設定正確
3. 後端是否正在運行

### 問題：API 請求失敗

檢查：
1. 瀏覽器開發者工具的 Console 標籤是否有錯誤訊息
2. Network 標籤中 API 請求的狀態碼
3. 確認後端 API 端點是否正確

## 開發環境

本地開發時，前端會自動使用 `http://localhost:8000` 作為 API URL，無需額外設定。 