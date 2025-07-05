# 🆓 免費方案管理員設定指南

由於 Render.com 免費方案不支援 Shell 功能，我們提供以下替代方案來設定管理員。

## 🚀 快速設定方法

### 方法一：使用 API 端點 (最簡單)

#### 步驟 1: 部署臨時端點
```bash
cd backend
chmod +x deploy_free_admin_fix.sh
./deploy_free_admin_fix.sh
```

#### 步驟 2: 查看所有使用者
```bash
curl https://slideai.onrender.com/api/admin/list-users
```

#### 步驟 3: 設定管理員
```bash
# 替換 your-email@example.com 為你的實際 email
curl -X POST 'https://slideai.onrender.com/api/admin/set-admin?email=your-email@example.com'
```

### 方法二：使用 Render.com 資料庫查詢

#### 步驟 1: 連接資料庫
1. 前往 [Render.com 儀表板](https://dashboard.render.com)
2. 點擊你的 **PostgreSQL 資料庫**
3. 點擊 `Connect` 標籤
4. 複製連接資訊

#### 步驟 2: 執行 SQL 查詢
```sql
-- 查看所有使用者
SELECT id, email, is_admin, created_at FROM users;

-- 設定管理員 (替換你的 email)
UPDATE users SET is_admin = true WHERE email = 'your-email@example.com';

-- 確認更新
SELECT id, email, is_admin FROM users WHERE email = 'your-email@example.com';
```

### 方法三：使用 pgAdmin

#### 步驟 1: 下載 pgAdmin
- 前往 [pgAdmin 官網](https://www.pgadmin.org/)
- 下載並安裝 pgAdmin

#### 步驟 2: 連接資料庫
1. 開啟 pgAdmin
2. 右鍵點擊 "Servers" → "Register" → "Server"
3. 填入 Render.com 提供的連接資訊：
   - Host: 你的資料庫主機
   - Port: 5432
   - Database: 你的資料庫名稱
   - Username: 你的資料庫用戶名
   - Password: 你的資料庫密碼

#### 步驟 3: 執行查詢
1. 連接成功後，展開你的資料庫
2. 點擊 "Query Tool"
3. 執行上述 SQL 查詢

## ✅ 驗證設定

### 前端驗證
1. 使用管理員帳號登入
2. 檢查是否出現 "管理者介面" 連結
3. 點擊進入管理員儀表板

### API 驗證
```bash
# 登入獲取 token
curl -X POST https://slideai.onrender.com/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email@example.com", "password": "your-password"}'

# 檢查管理員狀態
curl -X GET https://slideai.onrender.com/api/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 🚨 常見問題

### Q: API 端點返回 404？
A: 確保已經部署了臨時端點，等待 1-2 分鐘讓服務重啟。

### Q: 資料庫連接失敗？
A: 檢查連接資訊是否正確，特別是密碼和主機地址。

### Q: 設定後前端沒有反應？
A: 清除瀏覽器快取，重新登入。

### Q: 找不到使用者？
A: 確保已經註冊帳號，然後再執行設定。

## 🔐 安全提醒

1. **臨時端點**: 設定完成後建議移除臨時 API 端點
2. **密碼安全**: 使用強密碼保護管理員帳號
3. **定期檢查**: 定期檢查管理員權限設定

## 🧹 清理步驟

設定完成後，建議移除臨時端點：

1. 編輯 `backend/main.py`
2. 刪除以下兩個函數：
   - `set_admin_user()`
   - `list_users()`
3. 重新部署

## 📞 支援

如果遇到問題：
1. 檢查 Render.com 服務日誌
2. 確認資料庫連接正常
3. 驗證 email 地址是否正確

---

**注意**: 這些方法專為免費方案設計，不需要升級到付費方案！ 