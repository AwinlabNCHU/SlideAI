# ✅ 部署檢查清單

## 🗄️ PostgreSQL 資料庫設定

- [ ] 創建 PostgreSQL 服務
- [ ] 記錄資料庫名稱: `slideai`
- [ ] 記錄用戶名稱: `slideai_user`
- [ ] 複製 External Database URL
- [ ] 確認資料庫狀態為 "Active"

## 🌐 Web Service 設定

- [ ] 創建 Web Service
- [ ] 連接 GitHub 專案: `SlideAI`
- [ ] 設定 Root Directory: `backend`
- [ ] 設定 Build Command: `pip install -r requirements.txt`
- [ ] 設定 Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1`
- [ ] 選擇 Free Plan

## 🔧 環境變數設定

- [ ] `DATABASE_URL`: PostgreSQL 連線字串
- [ ] `SECRET_KEY`: 強密碼 (至少 32 字元)
- [ ] `ALGORITHM`: `HS256`
- [ ] `DAILY_USAGE_LIMIT`: `5`
- [ ] `CORS_ORIGINS`: `https://AwinlabNCHU.github.io`

## 🏥 健康檢查設定

- [ ] Health Check Path: `/health`
- [ ] Health Check Timeout: 180 seconds
- [ ] 測試健康檢查端點

## 👤 管理員帳號

- [ ] 使用 Shell 功能
- [ ] 執行: `python create_admin.py admin@example.com your_password`
- [ ] 確認管理員帳號創建成功

## 🔗 前端配置更新

- [ ] 更新 `frontend/src/config/api.js` 中的後端 URL
- [ ] 設定 GitHub Secrets: `VITE_API_URL`
- [ ] 推送程式碼觸發 GitHub Actions 部署

## 🧪 測試驗證

- [ ] 後端健康檢查: `https://your-service.onrender.com/health`
- [ ] 前端部署: `https://AwinlabNCHU.github.io/SlideAI`
- [ ] 用戶註冊/登入功能
- [ ] 檔案上傳功能
- [ ] 管理員功能

## 📊 監控設定

- [ ] 檢查記憶體使用情況
- [ ] 監控回應時間
- [ ] 設定錯誤通知 (可選)

## 🔒 安全檢查

- [ ] 確認 HTTPS 已啟用
- [ ] 檢查 CORS 設定
- [ ] 驗證 JWT Token 功能
- [ ] 測試檔案上傳限制

## 📝 記錄資訊

### 後端服務
- **URL**: `https://your-service-name.onrender.com`
- **健康檢查**: `https://your-service-name.onrender.com/health`

### 前端服務
- **URL**: `https://AwinlabNCHU.github.io/SlideAI`
- **GitHub Actions**: 查看部署狀態

### 資料庫
- **名稱**: `slideai-db`
- **資料庫**: `slideai`
- **用戶**: `slideai_user`

### 管理員帳號
- **Email**: `admin@example.com`
- **密碼**: `your_password`

## 🆘 故障排除

### 如果部署失敗
1. 檢查 Root Directory 是否為 `backend`
2. 確認環境變數格式正確
3. 查看建置日誌
4. 確認 GitHub 專案權限

### 如果資料庫連線失敗
1. 檢查 DATABASE_URL 格式
2. 確認 PostgreSQL 服務狀態
3. 驗證網路設定

### 如果前端無法連接到後端
1. 檢查 CORS_ORIGINS 設定
2. 確認 API URL 正確
3. 測試後端健康檢查

## 📞 支援資源

- Render.com 文檔: https://render.com/docs
- GitHub Actions 文檔: https://docs.github.com/en/actions
- Vue.js 部署文檔: https://vuejs.org/guide/best-practices/production-deployment.html