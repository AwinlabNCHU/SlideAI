# 🚀 部署指南

## 📋 前置需求

- Docker 和 Docker Compose
- 至少 2GB RAM 和 10GB 磁碟空間
- 網域名稱（可選，用於 HTTPS）

## 🔧 部署步驟

### 1. 環境設定

```bash
# 複製環境變數範例
cp env.production.example .env.production

# 編輯環境變數
nano .env.production
```

**重要環境變數說明：**
- `DATABASE_URL`: PostgreSQL 連線字串
- `SECRET_KEY`: JWT 加密金鑰（請使用強密碼）
- `DAILY_USAGE_LIMIT`: 每日使用次數限制
- `CORS_ORIGINS`: 允許的前端網域

### 2. 執行部署

```bash
# 給予部署腳本執行權限
chmod +x deploy.sh

# 執行部署
./deploy.sh
```

### 3. 創建管理員帳號

```bash
# 創建管理員帳號
docker-compose -f docker-compose.prod.yml exec backend python create_admin.py admin@example.com your_password
```

### 4. 驗證部署

- 前端: http://localhost
- 後端 API: http://localhost:8000
- 健康檢查: http://localhost:8000/health

## 🔒 安全設定

### 1. 防火牆設定

```bash
# 只開放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH
sudo ufw enable
```

### 2. SSL 憑證（可選）

```bash
# 安裝 Certbot
sudo apt install certbot python3-certbot-nginx

# 取得 SSL 憑證
sudo certbot --nginx -d your-domain.com
```

### 3. 資料庫安全

```bash
# 修改預設密碼
docker-compose -f docker-compose.prod.yml exec db psql -U testuser -d testdb -c "ALTER USER testuser PASSWORD 'new_strong_password';"
```

## 📊 監控與維護

### 1. 查看服務狀態

```bash
# 查看所有服務狀態
docker-compose -f docker-compose.prod.yml ps

# 查看服務日誌
docker-compose -f docker-compose.prod.yml logs -f backend
```

### 2. 備份資料庫

```bash
# 創建備份腳本
cat > backup.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
docker-compose -f docker-compose.prod.yml exec -T db pg_dump -U testuser testdb > backup_$DATE.sql
gzip backup_$DATE.sql
echo "備份完成: backup_$DATE.sql.gz"
EOF

chmod +x backup.sh
```

### 3. 更新應用程式

```bash
# 拉取最新程式碼
git pull

# 重新建置並部署
./deploy.sh
```

## 🐛 故障排除

### 1. 常見問題

**服務無法啟動：**
```bash
# 檢查日誌
docker-compose -f docker-compose.prod.yml logs

# 檢查磁碟空間
df -h

# 檢查記憶體使用
free -h
```

**資料庫連線失敗：**
```bash
# 檢查資料庫狀態
docker-compose -f docker-compose.prod.yml exec db pg_isready -U testuser

# 重新啟動資料庫
docker-compose -f docker-compose.prod.yml restart db
```

**前端無法載入：**
```bash
# 檢查前端容器
docker-compose -f docker-compose.prod.yml logs frontend

# 檢查 nginx 配置
docker-compose -f docker-compose.prod.yml exec frontend nginx -t
```

### 2. 效能調優

**增加後端 worker 數量：**
```bash
# 編輯 backend/Dockerfile.prod
# 修改 CMD 中的 --workers 參數
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "8"]
```

**調整資料庫設定：**
```bash
# 在 docker-compose.prod.yml 中為 db 服務添加環境變數
environment:
  POSTGRES_SHARED_BUFFERS: 256MB
  POSTGRES_EFFECTIVE_CACHE_SIZE: 1GB
```

## 📈 擴展建議

### 1. 負載平衡

考慮使用 Nginx 或 HAProxy 進行負載平衡：

```yaml
# 在 docker-compose.prod.yml 中添加
services:
  nginx-lb:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx-lb.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
```

### 2. 快取層

添加 Redis 快取：

```yaml
services:
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
```

### 3. 監控系統

添加 Prometheus 和 Grafana：

```yaml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

## 📞 支援

如遇到問題，請檢查：
1. Docker 和 Docker Compose 版本
2. 系統資源使用情況
3. 網路連線狀態
4. 服務日誌

更多資訊請參考專案 README.md 