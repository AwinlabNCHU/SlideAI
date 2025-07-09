# 遠端資料庫監控指南

## 🎯 支援的遠端資料庫服務

### ✅ 完全支援的雲端服務商

| 服務商 | 服務名稱 | 連接方式 | SSL 要求 |
|--------|----------|----------|----------|
| **Render.com** | PostgreSQL | 自動檢測 | 否 |
| **AWS** | RDS PostgreSQL | 自動檢測 | 是 |
| **Google Cloud** | Cloud SQL | 自動檢測 | 是 |
| **Microsoft Azure** | Database for PostgreSQL | 自動檢測 | 是 |
| **DigitalOcean** | Managed Databases | 自動檢測 | 是 |
| **Heroku** | Postgres | 自動檢測 | 否 |
| **其他** | 自建 PostgreSQL | 通用連接 | 視情況 |

## 🔧 環境配置

### 1. 設置環境變數

在您的 `.env` 檔案中設置 `DATABASE_URL`：

```bash
# Render.com
DATABASE_URL=postgresql://username:password@host:port/database

# AWS RDS
DATABASE_URL=postgresql://username:password@your-instance.region.rds.amazonaws.com:5432/database

# Google Cloud SQL
DATABASE_URL=postgresql://username:password@/database?host=/cloudsql/project:region:instance

# Azure Database
DATABASE_URL=postgresql://username@server.postgres.database.azure.com:5432/database

# DigitalOcean
DATABASE_URL=postgresql://username:password@host:port/database

# Heroku
DATABASE_URL=postgresql://username:password@host:port/database
```

### 2. 安裝依賴

```bash
cd backend
pip install psycopg2-binary python-dotenv
```

## 🚀 快速開始

### 1. 測試連接

```bash
python db_query_tool.py test
```

這會自動檢測您的資料庫類型並測試連接。

### 2. 查看資料庫資訊

```bash
python db_query_tool.py info
```

顯示資料庫大小、資料表大小、連接數等詳細資訊。

### 3. 監控資料庫

```bash
# 查看統計
python db_query_tool.py stats

# 查看最近上傳
python db_query_tool.py recent 20

# 查看使用者活動
python db_query_tool.py user user@example.com

# 驗證檔案
python db_query_tool.py verify 123
```

## 🔍 各服務商特定配置

### Render.com PostgreSQL

**優點：**
- 免費版本可用
- 自動 SSL 處理
- 簡單的連接配置

**配置：**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### AWS RDS PostgreSQL

**優點：**
- 高可用性
- 自動備份
- 可擴展性強

**配置：**
```bash
# 需要 SSL
DATABASE_URL=postgresql://username:password@your-instance.region.rds.amazonaws.com:5432/database
```

**安全組設置：**
- 確保安全組允許您的 IP 訪問 5432 端口
- 啟用 SSL 連接

### Google Cloud SQL

**優點：**
- 與 GCP 生態系統整合
- 自動備份和維護
- 高安全性

**配置：**
```bash
# 使用 Cloud SQL Proxy
DATABASE_URL=postgresql://username:password@/database?host=/cloudsql/project:region:instance

# 或直接連接
DATABASE_URL=postgresql://username:password@host:port/database
```

### Azure Database for PostgreSQL

**優點：**
- 與 Azure 服務整合
- 企業級安全性
- 自動擴展

**配置：**
```bash
DATABASE_URL=postgresql://username@server.postgres.database.azure.com:5432/database
```

### DigitalOcean Managed Databases

**優點：**
- 簡單易用
- 成本效益高
- 自動備份

**配置：**
```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

## 🔒 安全考慮

### 1. 連接安全

**SSL 連接：**
```python
# 大多數雲端服務商需要 SSL
conn = psycopg2.connect(
    database_url,
    sslmode='require'  # 或 'verify-full' 用於更嚴格的安全
)
```

**防火牆設置：**
- 限制 IP 訪問範圍
- 使用 VPC 或私有網路
- 定期更新安全組規則

### 2. 憑證管理

**環境變數：**
```bash
# 不要在程式碼中硬編碼
DATABASE_URL=postgresql://username:password@host:port/database
```

**密鑰輪換：**
- 定期更換資料庫密碼
- 使用 IAM 角色（如果支援）
- 監控異常訪問

## 📊 監控指標

### 1. 連接監控

```bash
# 檢查連接數
python db_query_tool.py info
```

**重要指標：**
- 當前連接數
- 最大連接數
- 連接池使用率

### 2. 性能監控

**查詢執行時間：**
```sql
SELECT query, mean_time, calls 
FROM pg_stat_statements 
ORDER BY mean_time DESC 
LIMIT 10;
```

**資料庫大小：**
```sql
SELECT pg_size_pretty(pg_database_size(current_database()));
```

### 3. 錯誤監控

**常見錯誤：**
- 連接超時
- SSL 證書問題
- 權限不足
- 網路問題

## 🛠 故障排除

### 1. 連接問題

**錯誤：`connection refused`**
```bash
# 檢查網路連接
ping your-database-host

# 檢查端口
telnet your-database-host 5432
```

**錯誤：`SSL connection required`**
```python
# 添加 SSL 參數
conn = psycopg2.connect(
    database_url,
    sslmode='require'
)
```

### 2. 權限問題

**錯誤：`permission denied`**
```sql
-- 檢查使用者權限
SELECT usename, usesuper, usecreatedb 
FROM pg_user 
WHERE usename = 'your_username';
```

### 3. 性能問題

**慢查詢：**
```sql
-- 查看慢查詢
SELECT query, mean_time, calls 
FROM pg_stat_statements 
WHERE mean_time > 1000;
```

## 🔄 自動化監控

### 1. 定期檢查腳本

```bash
#!/bin/bash
# 每天檢查資料庫狀態
cd /path/to/backend
python db_query_tool.py stats >> /var/log/db_monitor.log
python db_query_tool.py info >> /var/log/db_info.log
```

### 2. 警報設置

```python
# 檢查連接數
def check_connections():
    conn = get_database_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        connections = cursor.fetchone()[0]
        
        if connections > 80:  # 假設最大連接數為 100
            send_alert("資料庫連接數過高")
```

### 3. 備份監控

```bash
# 檢查備份狀態
python db_query_tool.py info | grep "backup"
```

## 📈 最佳實踐

### 1. 連接池管理

```python
# 使用連接池
from psycopg2 import pool

connection_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20,  # 最小和最大連接數
    database_url
)
```

### 2. 查詢優化

```sql
-- 添加索引
CREATE INDEX idx_user_files_user_id ON user_files(user_id);
CREATE INDEX idx_usage_records_user_id ON usage_records(user_id);
```

### 3. 監控儀表板

使用提供的管理員儀表板：
- 即時監控資料庫狀態
- 檔案上傳驗證
- 使用者活動追蹤

## 🆘 緊急情況處理

### 1. 資料庫無法連接

```bash
# 1. 檢查網路連接
ping database-host

# 2. 檢查服務狀態
python db_query_tool.py test

# 3. 檢查憑證
echo $DATABASE_URL

# 4. 聯繫服務商支援
```

### 2. 性能問題

```bash
# 1. 檢查連接數
python db_query_tool.py info

# 2. 檢查慢查詢
python db_query_tool.py stats

# 3. 考慮升級服務計劃
```

### 3. 資料丟失

```bash
# 1. 檢查備份
# 2. 恢復最近的備份
# 3. 檢查日誌找出原因
# 4. 實施預防措施
```

## 📞 支援聯繫

### 各服務商支援

| 服務商 | 支援文檔 | 聯繫方式 |
|--------|----------|----------|
| Render.com | [Render Docs](https://render.com/docs) | 內建支援 |
| AWS | [RDS Docs](https://aws.amazon.com/rds/postgresql/) | AWS Support |
| Google Cloud | [Cloud SQL Docs](https://cloud.google.com/sql/docs/postgres) | Google Support |
| Azure | [Azure Database Docs](https://docs.microsoft.com/azure/postgresql/) | Azure Support |
| DigitalOcean | [Managed Databases Docs](https://docs.digitalocean.com/products/databases/postgresql/) | DO Support |
| Heroku | [Heroku Postgres Docs](https://devcenter.heroku.com/categories/heroku-postgres) | Heroku Support |

### 本地故障排除

```bash
# 檢查工具是否正常工作
python db_query_tool.py test

# 查看詳細錯誤信息
python db_query_tool.py info

# 檢查環境變數
echo $DATABASE_URL
```

這個指南涵蓋了所有主要的遠端資料庫服務，並提供了完整的配置和監控解決方案！ 