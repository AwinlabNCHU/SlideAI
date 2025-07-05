# ☁️ 雲端部署指南 (Render.com + GitHub Pages)

## 📋 部署架構

- **後端**: Render.com (FastAPI + PostgreSQL)
- **前端**: GitHub Pages (Vue.js)
- **資料庫**: Render.com PostgreSQL

## 🚀 部署步驟

### 1. 後端部署到 Render.com

#### 1.1 準備 Render.com 配置

1. **確保 `render.yaml` 檔案存在於專案根目錄**
2. **修改 `render.yaml` 中的設定：**
   ```yaml
   services:
     - type: web
       name: your-app-name  # 改為您的應用程式名稱
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
       envVars:
         - key: CORS_ORIGINS
           value: https://your-username.github.io,https://your-domain.com  # 改為您的 GitHub Pages URL
   ```

#### 1.2 部署到 Render.com

1. **登入 [Render.com](https://render.com)**
2. **點擊 "New +" → "Blueprint"**
3. **連接您的 GitHub 專案**
4. **選擇包含 `render.yaml` 的專案**
5. **點擊 "Apply" 開始部署**

#### 1.3 設定環境變數

在 Render.com 儀表板中設定以下環境變數：
- `SECRET_KEY`: 生成一個強密碼
- `DAILY_USAGE_LIMIT`: 5 (或您想要的限制)
- `CORS_ORIGINS`: 您的 GitHub Pages URL

### 2. 前端部署到 GitHub Pages

#### 2.1 準備 GitHub 專案

1. **確保專案已推送到 GitHub**
2. **在 GitHub 專案設定中啟用 GitHub Pages：**
   - 前往 Settings → Pages
   - Source: Deploy from a branch
   - Branch: gh-pages
   - 點擊 Save

#### 2.2 設定 GitHub Secrets

在 GitHub 專案設定中設定 Secrets：
- 前往 Settings → Secrets and variables → Actions
- 新增 `VITE_API_URL`: 您的 Render.com 後端 URL

#### 2.3 修改前端配置

1. **更新 `frontend/vite.config.js` 中的 base 路徑：**
   ```javascript
   base: process.env.NODE_ENV === 'production' ? '/your-repo-name/' : '/',
   ```

2. **更新 `frontend/src/config/api.js` 中的預設 URL：**
   ```javascript
   production: {
     baseURL: import.meta.env.VITE_API_URL || 'https://your-app-name.onrender.com'
   }
   ```

#### 2.4 自動部署

推送程式碼到 `main` 分支，GitHub Actions 會自動：
1. 建置前端應用程式
2. 部署到 GitHub Pages

### 3. 創建管理員帳號

部署完成後，創建管理員帳號：

```bash
# 使用 Render.com 的 Shell 功能
# 或透過 Render.com 的 Console

# 進入後端容器
cd /opt/render/project/src

# 創建管理員帳號
python create_admin.py admin@example.com your_password
```

## 🔧 配置檢查清單

### 後端 (Render.com)
- [ ] `render.yaml` 配置正確
- [ ] 環境變數設定完成
- [ ] CORS 設定包含前端 URL
- [ ] 資料庫連線正常
- [ ] 管理員帳號已創建

### 前端 (GitHub Pages)
- [ ] GitHub Pages 已啟用
- [ ] GitHub Secrets 設定完成
- [ ] Vite 配置正確
- [ ] API 配置指向正確的後端 URL
- [ ] 自動部署工作流程正常

## 🌐 URL 配置範例

### 假設您的配置：
- GitHub 用戶名: `your-username`
- GitHub 專案名: `TestApp`
- Render.com 應用程式名: `testapp-backend`

### 對應的 URL：
- **前端**: `https://your-username.github.io/TestApp/`
- **後端**: `https://testapp-backend.onrender.com`

### 需要更新的檔案：

1. **`render.yaml`**:
   ```yaml
   envVars:
     - key: CORS_ORIGINS
       value: https://your-username.github.io
   ```

2. **`frontend/vite.config.js`**:
   ```javascript
   base: process.env.NODE_ENV === 'production' ? '/TestApp/' : '/',
   ```

3. **`frontend/src/config/api.js`**:
   ```javascript
   production: {
     baseURL: import.meta.env.VITE_API_URL || 'https://testapp-backend.onrender.com'
   }
   ```

4. **GitHub Secrets**:
   - `VITE_API_URL`: `https://testapp-backend.onrender.com`

## 🔒 安全設定

### 1. 環境變數
- 使用強密碼作為 `SECRET_KEY`
- 設定適當的 `CORS_ORIGINS`
- 不要將敏感資訊提交到 Git

### 2. 資料庫安全
- Render.com 會自動處理資料庫安全
- 定期備份資料庫

### 3. HTTPS
- Render.com 和 GitHub Pages 都自動提供 HTTPS
- 確保所有 API 呼叫都使用 HTTPS

## 📊 監控與維護

### 1. Render.com 監控
- 在 Render.com 儀表板查看服務狀態
- 設定自動重啟和健康檢查
- 監控資源使用情況

### 2. GitHub Pages 監控
- 在 GitHub Actions 查看部署狀態
- 檢查 GitHub Pages 設定

### 3. 日誌查看
```bash
# Render.com 日誌
# 在 Render.com 儀表板查看

# 本地測試
curl https://your-app-name.onrender.com/health
```

## 🐛 常見問題

### 1. CORS 錯誤
**問題**: 前端無法連接到後端
**解決**: 檢查 `CORS_ORIGINS` 設定是否包含前端 URL

### 2. 404 錯誤 (GitHub Pages)
**問題**: 重新整理頁面出現 404
**解決**: 確保 Vue Router 使用 hash 模式或設定正確的 base 路徑

### 3. 環境變數未生效
**問題**: 前端無法讀取環境變數
**解決**: 確保 GitHub Secrets 設定正確，且變數名稱為 `VITE_API_URL`

### 4. 資料庫連線失敗
**問題**: 後端無法連接到資料庫
**解決**: 檢查 Render.com 的資料庫設定和連線字串

## 📈 擴展建議

### 1. 自定義網域
- 為 GitHub Pages 設定自定義網域
- 為 Render.com 設定自定義網域

### 2. CDN 優化
- 考慮使用 Cloudflare 等 CDN 服務
- 優化靜態資源載入

### 3. 監控工具
- 整合 Sentry 進行錯誤追蹤
- 使用 Google Analytics 進行流量分析

## 📞 支援

如遇到問題：
1. 檢查 Render.com 和 GitHub Pages 的官方文件
2. 查看服務日誌
3. 確認所有配置設定正確
4. 測試 API 端點是否正常運作 