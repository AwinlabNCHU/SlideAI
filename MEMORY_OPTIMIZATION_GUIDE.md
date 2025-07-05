# Render.com 記憶體優化指南

## 問題描述

Render.com 免費方案限制：
- **記憶體**: 512MB
- **CPU**: 0.1 CPU
- **磁碟空間**: 1GB
- **每月運行時間**: 750 小時

當應用程式使用超過 512MB 記憶體時，會出現 `Ran out of memory` 錯誤。

## 優化策略

### 1. 檔案大小限制
- **影片檔案**: 50MB → 25MB
- **PDF 檔案**: 50MB → 20MB
- **檔案保留天數**: 7 天 → 3 天

### 2. 記憶體管理優化
- **分塊檔案上傳**: 避免一次性載入大檔案到記憶體
- **垃圾回收**: 強制清理未使用的記憶體
- **資料庫連接池**: 優化資料庫連接管理
- **查詢限制**: 限制返回的資料量

### 3. 檔案清理優化
- **批次清理**: 每次只清理 10 個檔案
- **定期清理**: 在健康檢查時觸發
- **錯誤處理**: 避免清理失敗影響主程式

## 部署步驟

### 1. 自動部署（推薦）

```bash
chmod +x deploy_memory_optimization.sh
./deploy_memory_optimization.sh
```

### 2. 手動部署

```bash
cd backend
cp main_optimized.py main.py
git add .
git commit -m "Optimize memory usage for Render.com free tier"
git push origin main
```

## 優化內容詳解

### 檔案上傳優化

```python
def save_file_optimized(file: UploadFile, max_size: int) -> tuple:
    """優化的檔案保存函數"""
    # 分塊讀取和寫入，避免記憶體溢出
    with open(file_path, "wb") as buffer:
        chunk_size = 1024 * 1024  # 1MB chunks
        while True:
            chunk = file.file.read(chunk_size)
            if not chunk:
                break
            buffer.write(chunk)
```

### 垃圾回收

```python
import gc

# 在處理完成後強制垃圾回收
gc.collect()
```

### 資料庫查詢限制

```python
# 限制返回的檔案數量
files = db.query(UserFile).filter(...).limit(100).all()

# 限制清理的檔案數量
expired_files = db.query(UserFile).filter(...).limit(10).all()
```

### 檔案清理優化

```python
def cleanup_expired_files(db: Session):
    """清理過期檔案 - 優化版本"""
    try:
        # 限制每次清理的檔案數量
        expired_files = db.query(UserFile).filter(...).limit(10).all()
        
        for file_record in expired_files:
            # 處理檔案刪除
            pass
        
        # 強制垃圾回收
        gc.collect()
        
    except Exception as e:
        print(f"清理過期檔案時發生錯誤: {e}")
```

## 監控記憶體使用

### 健康檢查端點

```bash
curl https://slideai.onrender.com/health
```

回應包含記憶體使用情況：
```json
{
  "status": "healthy",
  "memory_usage": {
    "percent": 45,
    "available_mb": 280,
    "total_mb": 512
  }
}
```

## 常見問題

### Q: 優化後仍然出現記憶體錯誤怎麼辦？

A: 進一步降低限制：
- 檔案大小限制到 15MB
- 檔案保留天數到 1 天
- 減少同時處理的檔案數量

### Q: 如何監控記憶體使用？

A: 使用健康檢查端點或 Render.com 儀表板查看記憶體使用情況。

### Q: 可以升級到付費方案嗎？

A: 是的，Render.com 提供付費方案：
- **Starter**: $7/月，1GB 記憶體
- **Standard**: $25/月，2GB 記憶體
- **Pro**: $50/月，4GB 記憶體

## 最佳實踐

1. **定期清理**: 確保過期檔案及時刪除
2. **監控使用**: 定期檢查記憶體使用情況
3. **限制上傳**: 提醒用戶檔案大小限制
4. **錯誤處理**: 優雅處理記憶體不足的情況

## 部署時間

- **Render.com 部署**: 3-5 分鐘
- **優化生效**: 部署完成後立即生效

完成優化後，應用程式應該能夠在 512MB 記憶體限制內正常運行。 