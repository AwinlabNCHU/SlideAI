# 🔧 SlideAI 管理員設定指南

本指南將幫助你在 Render.com 的資料庫中設定管理員權限。

## 📋 前置需求

1. ✅ 已部署 SlideAI 後端到 Render.com
2. ✅ 已設定 PostgreSQL 資料庫
3. ✅ 至少有一個已註冊的使用者帳號

## 🚀 方法一：使用 Render.com Shell (推薦)

### 步驟 1: 部署管理員工具
```bash
cd backend
chmod +x deploy_admin_tools.sh
./deploy_admin_tools.sh
```

### 步驟 2: 使用 Render.com Shell
1. 前往 [Render.com 儀表板](https://dashboard.render.com)
2. 點擊你的後端服務 (例如: `slideai-backend`)
3. 點擊 `Shell` 標籤
4. 等待 Shell 載入完成

### 步驟 3: 執行管理員設定腳本
```bash
# 快速設定 (自動選擇第一個非管理員使用者)
python set_admin_render.py

# 或使用完整版腳本 (可選擇特定使用者)
python set_admin.py
```

### 步驟 4: 確認設定
腳本會顯示所有使用者列表，確認管理員權限已正確設定。

## 🛠️ 方法二：直接 SQL 查詢

### 步驟 1: 連接資料庫
1. 前往 [Render.com 儀表板](https://dashboard.render.com)
2. 點擊你的 PostgreSQL 資料庫
3. 點擊 `Connect` 標籤
4. 複製連接資訊

### 步驟 2: 執行 SQL 查詢
```sql
-- 查看所有使用者
SELECT id, email, is_admin, created_at FROM users;

-- 設定特定使用者為管理員 (替換 email)
UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';

-- 確認更新
SELECT id, email, is_admin FROM users WHERE email = 'your-email@example.com';
```

## 🔍 方法三：使用 psql 命令列

### 步驟 1: 獲取資料庫連接資訊
在 Render.com 資料庫頁面找到以下資訊：
- Host
- Database
- Username
- Password
- Port

### 步驟 2: 連接資料庫
```bash
psql "postgresql://username:password@host:port/database"
```

### 步驟 3: 執行查詢
```sql
-- 查看使用者
SELECT * FROM users;

-- 設定管理員
UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';

-- 確認
SELECT email, is_admin FROM users;
```

## ✅ 驗證管理員權限

### 方法 1: 透過前端測試
1. 使用管理員帳號登入
2. 檢查是否出現 "管理者介面" 連結
3. 點擊進入管理員儀表板

### 方法 2: 透過 API 測試
```bash
# 登入獲取 token
curl -X POST https://slideai.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com", "password": "your-password"}'

# 使用 token 檢查管理員狀態
curl -X GET https://slideai.onrender.com/api/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚨 常見問題

### Q: 找不到使用者怎麼辦？
A: 確保已經註冊帳號，然後再執行管理員設定腳本。

### Q: 資料庫連接失敗？
A: 檢查 DATABASE_URL 環境變數是否正確設定。

### Q: 權限不足？
A: 確保使用的是資料庫擁有者的帳號。

### Q: 設定後前端沒有反應？
A: 清除瀏覽器快取，重新登入。

## 🔐 安全注意事項

1. **定期更換密碼**: 管理員帳號密碼應定期更換
2. **限制管理員數量**: 只設定必要的人員為管理員
3. **監控使用情況**: 定期檢查管理員活動
4. **備份資料**: 重要操作前先備份資料庫

## 📞 支援

如果遇到問題，請檢查：
1. Render.com 服務日誌
2. 資料庫連接狀態
3. 環境變數設定
4. 網路連接

---

**注意**: 管理員權限具有重要功能，請謹慎設定！ 