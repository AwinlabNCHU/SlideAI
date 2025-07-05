# 🔧 GitHub Pages 路由問題修復指南

## 🐛 問題描述

GitHub Pages 部署後網站內容不顯示，通常是因為 Vue Router 的路由模式與 GitHub Pages 不相容。

## 🔍 問題原因

1. **HTML5 History 模式**: GitHub Pages 不支援 `createWebHistory()`
2. **路徑重定向**: 需要特殊處理 SPA 路由
3. **Base 路徑**: 需要正確設定 `/SlideAI/` 路徑

## ✅ 已修復的問題

### 1. Vue Router 模式切換

```javascript
// 根據環境選擇路由模式
const isProduction = import.meta.env.PROD;
const router = createRouter({
  // 生產環境使用 hash 模式，開發環境使用 history 模式
  history: isProduction ? createWebHashHistory() : createWebHistory(),
  routes,
});
```

### 2. 404 重定向頁面

創建 `frontend/public/404.html` 處理路由重定向。

### 3. 主頁面路由處理

在 `index.html` 中添加路由重定向腳本。

### 4. Vite 配置優化

確保正確的 base 路徑和建置設定。

## 🚀 部署步驟

### 1. 推送修復

```bash
git add .
git commit -m "Fix GitHub Pages routing - use hash mode for production"
git push origin main
```

### 2. 等待 GitHub Actions 部署

- 前往 Actions 頁面查看部署狀態
- 等待部署完成

### 3. 測試路由

訪問以下 URL 測試：
- `https://AwinlabNCHU.github.io/SlideAI/` (首頁)
- `https://AwinlabNCHU.github.io/SlideAI/#/login` (登入頁)
- `https://AwinlabNCHU.github.io/SlideAI/#/register` (註冊頁)

## 🔧 路由模式說明

### 開發環境 (localhost)
- 使用 `createWebHistory()` (HTML5 History 模式)
- URL: `http://localhost:5173/login`
- 更好的 SEO 和用戶體驗

### 生產環境 (GitHub Pages)
- 使用 `createWebHashHistory()` (Hash 模式)
- URL: `https://AwinlabNCHU.github.io/SlideAI/#/login`
- 相容 GitHub Pages 靜態託管

## 📊 測試清單

- [ ] 首頁載入正常
- [ ] 路由導航正常
- [ ] 重新整理頁面不 404
- [ ] 直接訪問子頁面正常
- [ ] 瀏覽器前進/後退正常

## 🆘 故障排除

### 問題 1: 頁面空白

**解決方案**:
1. 檢查瀏覽器控制台錯誤
2. 確認 base 路徑設定正確
3. 檢查 API 連線是否正常

### 問題 2: 路由不工作

**解決方案**:
1. 確認使用 hash 模式 (`#/`)
2. 檢查 404.html 是否正確
3. 清除瀏覽器快取

### 問題 3: API 連線失敗

**解決方案**:
1. 檢查 `VITE_API_URL` 設定
2. 確認後端服務正常運行
3. 檢查 CORS 設定

## 🔄 路由對比

| 環境 | 模式 | URL 範例 | 優點 |
|------|------|----------|------|
| 開發 | History | `/login` | 乾淨的 URL |
| 生產 | Hash | `/#/login` | GitHub Pages 相容 |

## 📝 重要注意事項

1. **Hash 模式**: 生產環境使用 `#` 前綴
2. **Base 路徑**: 必須包含 `/SlideAI/`
3. **404 處理**: 需要特殊重定向
4. **API 連線**: 確保後端 URL 正確

## 🎯 預期結果

修復後，您的網站應該：
- ✅ 正常載入首頁
- ✅ 所有路由正常工作
- ✅ 重新整理頁面不 404
- ✅ API 連線正常
- ✅ 用戶體驗流暢

## 📞 支援

如果問題持續存在：
1. 檢查瀏覽器開發者工具
2. 查看 GitHub Actions 日誌
3. 確認所有配置正確
4. 清除瀏覽器快取 