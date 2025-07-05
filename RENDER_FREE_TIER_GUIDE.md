# 🆓 Render.com 免費方案部署指南

## 📋 免費方案限制與對策

### ⏰ 休眠機制處理

**問題**: 15分鐘無活動後自動休眠，首次請求需要30-60秒啟動
**對策**:
1. **前端優化**: 添加載入狀態和重試機制
2. **健康檢查**: 定期 ping 後端保持活躍
3. **用戶體驗**: 告知用戶首次載入需要等待

### 💾 記憶體限制 (512MB)

**問題**: 記憶體有限，可能影響檔案處理
**對策**:
1. **檔案大小限制**: 限制上傳檔案大小
2. **記憶體優化**: 使用串流處理大檔案
3. **清理機制**: 及時清理暫存檔案

### 🗄️ 資料庫限制 (90小時/月)

**問題**: 資料庫使用時間有限
**對策**:
1. **連接池優化**: 減少資料庫連接數
2. **查詢優化**: 避免不必要的資料庫查詢
3. **快取機制**: 使用記憶體快取減少資料庫負載

## 🔧 免費方案優化配置

### 1. 後端優化

```python
# 在 main.py 中添加記憶體監控
import psutil
import gc

@app.get('/health')
def health_check():
    """健康檢查端點 - 包含記憶體使用情況"""
    memory = psutil.virtual_memory()
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "memory_usage": {
            "percent": memory.percent,
            "available_mb": memory.available // 1024 // 1024,
            "total_mb": memory.total // 1024 // 1024
        }
    }

# 檔案上傳大小限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (免費方案建議)
```

### 2. 前端優化

```javascript
// 添加重試機制和載入狀態
const apiCallWithRetry = async (url, options, maxRetries = 3) => {
  for (let i = 0; i < maxRetries; i++) {
    try {
      const response = await fetch(url, options);
      if (response.ok) return response;
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      // 等待後重試
      await new Promise(resolve => setTimeout(resolve, 2000 * (i + 1)));
    }
  }
};
```

### 3. 資料庫優化

```python
# 優化資料庫連接
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,  # 減少連接池大小
    max_overflow=10,
    pool_pre_ping=True,  # 自動檢查連接
    pool_recycle=3600  # 1小時後回收連接
)
```

## 🚀 部署步驟

### 1. 準備 Render.com 帳號

1. **註冊 Render.com 帳號**
2. **驗證 GitHub 帳號**
3. **確保有足夠的免費額度**

### 2. 部署後端

1. **使用 Blueprint 部署**:
   - 登入 Render.com
   - 點擊 "New +" → "Blueprint"
   - 連接 GitHub 專案
   - 選擇包含 `render.yaml` 的專案
   - 點擊 "Apply"

2. **設定環境變數**:
   - `SECRET_KEY`: 生成強密碼
   - `DAILY_USAGE_LIMIT`: 5 (或更少以節省資源)
   - `CORS_ORIGINS`: 您的前端 URL

### 3. 創建管理員帳號

```bash
# 在 Render.com 的 Shell 中執行
cd /opt/render/project/src
python create_admin.py admin@example.com your_password
```

## 📊 監控與維護

### 1. 資源監控

- **記憶體使用**: 保持在 400MB 以下
- **資料庫使用時間**: 監控剩餘時間
- **回應時間**: 首次請求可能較慢

### 2. 成本控制

- **檔案大小限制**: 50MB 以下
- **使用次數限制**: 每日 5 次
- **資料庫查詢**: 優化查詢減少負載

### 3. 用戶體驗

- **載入提示**: 告知用戶首次載入需要等待
- **錯誤處理**: 優雅的錯誤訊息
- **重試機制**: 自動重試失敗的請求

## 💡 免費方案使用技巧

### 1. 保持服務活躍

```bash
# 使用 cron job 定期 ping 服務
# 每 10 分鐘 ping 一次健康檢查端點
*/10 * * * * curl -s https://your-app.onrender.com/health > /dev/null
```

### 2. 檔案處理優化

```python
# 使用串流處理大檔案
async def process_large_file(file_path):
    chunk_size = 1024 * 1024  # 1MB chunks
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            # 處理檔案塊
            yield chunk
```

### 3. 資料庫查詢優化

```python
# 使用索引和限制查詢結果
@app.get('/api/admin/user-list')
def admin_user_list(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # 限制查詢結果數量
    users = db.query(User).limit(100).all()
    return [{"id": u.id, "email": u.email, "created_at": str(u.created_at)} for u in users]
```

## ⚠️ 注意事項

1. **休眠時間**: 首次請求會較慢，請告知用戶
2. **檔案限制**: 建議限制檔案大小在 50MB 以下
3. **使用頻率**: 避免過於頻繁的請求
4. **備份**: 定期備份重要資料
5. **升級**: 如果使用量增加，考慮升級到付費方案

## 🔄 升級到付費方案

當您的應用程式成長時，可以考慮升級：

- **Starter Plan**: $7/月，無休眠限制
- **Standard Plan**: $25/月，更多資源
- **Pro Plan**: $50/月，專用資源

## 📞 支援

- Render.com 文檔: https://render.com/docs
- 免費方案限制: https://render.com/docs/free
- 社群支援: https://community.render.com 