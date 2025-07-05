# 🌐 Render.com Web Service 部署指南

## 📋 手動部署步驟 (無需信用卡)

### 1. 創建 PostgreSQL 資料庫

1. **登入 Render.com**
2. **點擊 "New +" → "PostgreSQL"**
3. **設定資料庫**:
   - **Name**: `slideai-db`
   - **Database**: `slideai`
   - **User**: `slideai_user`
   - **Plan**: Free
4. **點擊 "Create Database"**
5. **記錄連線資訊** (稍後會用到)

### 2. 創建 Web Service

1. **點擊 "New +" → "Web Service"**
2. **連接 GitHub 專案**:
   - 選擇您的 `SlideAI` 專案
   - 選擇 `main` 分支
3. **設定服務**:
   - **Name**: `SlideAI_BE`
   - **Environment**: Python 3
   - **Region**: 選擇離您最近的區域
   - **Branch**: `main`
   - **Root Directory**: `backend` (重要！)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
   - **Plan**: Free

### 3. 設定環境變數

在 Web Service 設定頁面中，添加以下環境變數：

| 變數名稱 | 值 | 說明 |
|----------|-----|------|
| `DATABASE_URL` | `postgresql://slideai_user:password@host:5432/slideai` | 從 PostgreSQL 服務獲取 |
| `SECRET_KEY` | `b005f3a3579e6172294cf3d47c7f7cd4` | 生成強密碼 |
| `ALGORITHM` | `HS256` | JWT 演算法 |
| `DAILY_USAGE_LIMIT` | `5` | 每日使用限制 |
| `CORS_ORIGINS` | `https://AwinlabNCHU.github.io` | 前端網域 |

### 4. 設定健康檢查

- **Health Check Path**: `/health`
- **Health Check Timeout**: 180 seconds

### 5. 部署

1. **點擊 "Create Web Service"**
2. **等待部署完成** (約 5-10 分鐘)
3. **記錄您的服務 URL** (例如: `https://slideai-be.onrender.com`)

## 🔧 獲取 DATABASE_URL

1. **前往 PostgreSQL 服務頁面**
2. **點擊 "Connect"**
3. **選擇 "External Database URL"**
4. **複製連線字串**
5. **貼到 Web Service 的環境變數中**

## 🚀 創建管理員帳號

部署完成後，創建管理員帳號：

1. **在 Web Service 頁面點擊 "Shell"**
2. **執行以下指令**:
   ```bash
   cd /opt/render/project/src
   python create_admin.py admin@example.com your_password
   ```

## 📊 驗證部署

1. **測試健康檢查**: `https://your-service.onrender.com/health`
2. **測試 API**: `https://your-service.onrender.com/api/me`
3. **更新前端配置**: 將 API URL 更新為您的服務 URL

## 🔄 更新前端配置

更新 `frontend/src/config/api.js`:

```javascript
production: {
  baseURL: import.meta.env.VITE_API_URL || 'https://your-service-name.onrender.com'
}
```

## ⚠️ 注意事項

1. **免費方案限制**:
   - 15分鐘無活動後休眠
   - 首次請求需要 30-60 秒啟動
   - 每月 750 小時使用時間

2. **檔案大小限制**:
   - 建議限制在 50MB 以下
   - 已在上傳端點中設定限制

3. **記憶體限制**:
   - 512MB RAM
   - 已添加記憶體監控

## 🆘 常見問題

### Q: 部署失敗怎麼辦？
A: 檢查：
- Root Directory 是否設為 `backend`
- 環境變數是否正確設定
- GitHub 專案是否公開或已授權

### Q: 資料庫連線失敗？
A: 確認：
- DATABASE_URL 格式正確
- PostgreSQL 服務已啟動
- 網路設定正確

### Q: CORS 錯誤？
A: 檢查：
- CORS_ORIGINS 是否包含前端 URL
- 前端是否使用正確的 API URL

## 📞 支援

- Render.com 文檔: https://render.com/docs
- 社群支援: https://community.render.com
- 免費方案限制: https://render.com/docs/free 