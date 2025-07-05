# 前端故障排除指南

## 問題：註冊/登入按鈕沒有反應

### 快速診斷步驟

1. **訪問測試頁面**
   - 在瀏覽器中訪問：`https://your-username.github.io/your-repo/test`
   - 這會顯示調試面板和測試工具

2. **檢查環境資訊**
   - 確認 API URL 是否正確
   - 確認是否為生產環境

3. **執行 API 測試**
   - 點擊「測試連接」按鈕
   - 點擊「測試登入」按鈕
   - 點擊「測試註冊」按鈕

### 常見問題及解決方案

#### 問題 1：CORS 錯誤

**症狀**：
- 瀏覽器控制台顯示 CORS 錯誤
- 測試連接失敗

**解決方案**：
1. 確認 Render.com 後端的 CORS 設定
2. 檢查 `CORS_ORIGINS` 環境變數是否包含 GitHub Pages 域名

#### 問題 2：API URL 錯誤

**症狀**：
- 測試連接顯示 404 或連接失敗
- API URL 顯示錯誤的地址

**解決方案**：
1. 創建 `.env.production` 文件：
   ```bash
   cd frontend
   echo "VITE_API_URL=https://your-app-name.onrender.com" > .env.production
   ```

2. 重新部署：
   ```bash
   git add .
   git commit -m "Fix API URL"
   git push origin main
   ```

#### 問題 3：後端服務未運行

**症狀**：
- 所有 API 測試都失敗
- 顯示連接超時錯誤

**解決方案**：
1. 檢查 Render.com 後端是否正在運行
2. 查看 Render.com 的日誌
3. 確認資料庫連接正常

#### 問題 4：環境變數未生效

**症狀**：
- 生產環境仍使用 localhost URL
- 環境資訊顯示錯誤

**解決方案**：
1. 確認 `.env.production` 文件存在
2. 重新構建和部署前端
3. 清除瀏覽器緩存

### 調試工具使用

#### 調試面板
- 在開發環境中自動顯示
- 顯示環境資訊和錯誤日誌
- 提供快速測試按鈕

#### 測試頁面
- 訪問 `/test` 路由
- 提供詳細的 API 測試功能
- 顯示完整的錯誤資訊

### 手動測試步驟

1. **檢查瀏覽器控制台**
   - 按 F12 打開開發者工具
   - 查看 Console 標籤的錯誤訊息
   - 查看 Network 標籤的 API 請求

2. **測試 API 端點**
   ```bash
   # 測試後端是否可達
   curl https://your-app-name.onrender.com/api/me
   
   # 測試登入端點
   curl -X POST https://your-app-name.onrender.com/api/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"testpassword"}'
   ```

3. **檢查環境變數**
   ```bash
   # 在本地測試環境變數
   cd frontend
   npm run build
   # 檢查 dist 目錄中的檔案是否包含正確的 API URL
   ```

### 生產環境檢查清單

- [ ] Render.com 後端正在運行
- [ ] 資料庫連接正常
- [ ] CORS 設定正確
- [ ] 環境變數 `VITE_API_URL` 已設定
- [ ] 前端已重新部署
- [ ] 瀏覽器緩存已清除

### 聯繫支援

如果問題仍然存在，請提供以下資訊：

1. **錯誤截圖**：瀏覽器控制台的錯誤訊息
2. **測試結果**：測試頁面的輸出結果
3. **環境資訊**：測試頁面顯示的環境資訊
4. **後端日誌**：Render.com 的應用程式日誌

### 臨時解決方案

如果急需修復，可以：

1. **手動修改 API URL**：
   - 在 `frontend/src/config/api.js` 中直接修改預設 URL
   - 重新部署前端

2. **使用開發環境測試**：
   - 在本地運行前端和後端
   - 確認功能正常後再部署到生產環境 