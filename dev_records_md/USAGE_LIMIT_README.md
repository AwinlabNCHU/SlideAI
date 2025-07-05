# 使用者次數限制功能說明

## 功能概述

本專案已新增使用者次數限制功能，每個使用者每天最多可以使用5次服務，隔天會重新計算。

## 新增功能

### 1. 資料庫更新
- 在 `User` 模型中新增 `reset_token` 欄位（用於密碼重設功能）
- 新增 `UsageRecord` 模型來記錄使用者每日的使用次數
- 包含以下欄位：
  - `user_id`: 使用者ID
  - `usage_date`: 使用日期
  - `service_type`: 服務類型（'video_abstract' 或 'ppt_to_video'）
  - `created_at`: 記錄創建時間

### 2. 後端API更新

#### 新增API端點：
- `GET /api/usage-status`: 獲取使用者今日使用狀態
- `GET /api/admin/usage-statistics`: 管理者查看所有使用者的使用統計
- `GET /api/admin/daily-usage-summary`: 管理者查看今日使用摘要

#### 更新的API端點：
- `POST /api/video-abstract`: 新增使用次數檢查和記錄
- `POST /api/ppt-to-video`: 新增使用次數檢查和記錄

### 3. 前端更新

#### Dashboard頁面：
- 新增使用次數統計卡片
- 顯示今日已使用次數、剩餘次數和每日限制
- 重新設計服務卡片，提供直接連結到各服務

#### 服務頁面（VideoAbstract & PPTGenerator）：
- 新增使用次數顯示區域
- 當達到每日限制時禁用上傳按鈕
- 顯示相應的錯誤訊息

#### 管理者儀表板：
- 新增今日使用摘要統計
- 新增使用者使用統計表格
- 顯示各使用者的總使用次數、各服務使用次數和今日使用次數

## 使用方式

### 1. 執行資料庫遷移
```bash
cd backend
python migrate_db.py
```

### 2. 啟動服務
```bash
# 後端
cd backend
python main.py

# 前端
cd frontend
npm run dev
```

### 3. 功能驗證
1. 註冊/登入使用者帳號
2. 在Dashboard頁面查看使用次數統計
3. 使用AI影片摘要或AI語音簡報服務
4. 觀察使用次數的變化
5. 當達到5次限制時，服務會被禁用
6. 管理者可以在管理後台查看所有使用者的使用統計

## 技術實現

### 使用次數檢查邏輯
```python
def check_daily_usage_limit(user_id: int, db: Session):
    """檢查使用者今日使用次數是否超過限制"""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    today_usage = db.query(UsageRecord).filter(
        UsageRecord.user_id == user_id,
        UsageRecord.usage_date >= today_start,
        UsageRecord.usage_date <= today_end
    ).count()
    
    return today_usage < DAILY_USAGE_LIMIT
```

### 使用記錄邏輯
```python
def record_usage(user_id: int, service_type: str, db: Session):
    """記錄使用者使用服務"""
    usage_record = UsageRecord(
        user_id=user_id,
        service_type=service_type,
        usage_date=datetime.utcnow()
    )
    db.add(usage_record)
    db.commit()
```

## 配置選項

在 `backend/main.py` 中可以調整以下設定：
- `DAILY_USAGE_LIMIT = 5`: 每日使用次數限制

## 注意事項

1. 使用次數限制是按日計算的，每天00:00重新開始計算
2. 使用記錄會永久保存在資料庫中，用於統計分析
3. 管理者可以查看所有使用者的詳細使用統計
4. 當使用者達到每日限制時，會顯示相應的錯誤訊息並禁用服務

## 未來擴展

1. 可以考慮新增不同等級的使用者，提供不同的使用次數限制
2. 可以新增使用次數購買或升級功能
3. 可以新增更詳細的使用統計圖表
4. 可以新增使用次數重置功能（管理者手動重置） 