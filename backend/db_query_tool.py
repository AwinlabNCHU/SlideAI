#!/usr/bin/env python3
"""
資料庫查詢工具
用於直接查詢遠端 PostgreSQL 資料庫
支援多種雲端服務商的資料庫
"""

import os
import sys
import psycopg2
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
import ssl

# 載入環境變數
load_dotenv()

def get_database_connection():
    """建立資料庫連接，支援多種遠端資料庫"""
    try:
        # 從環境變數獲取資料庫 URL
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("錯誤: 未找到 DATABASE_URL 環境變數")
            print("請在 .env 檔案中設置 DATABASE_URL")
            return None
        
        # 處理不同格式的資料庫 URL
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # 解析資料庫 URL 來判斷服務商
        if "render.com" in database_url:
            print("檢測到 Render.com 資料庫")
            return connect_to_render_db(database_url)
        elif "amazonaws.com" in database_url:
            print("檢測到 AWS RDS 資料庫")
            return connect_to_aws_db(database_url)
        elif "googleapis.com" in database_url:
            print("檢測到 Google Cloud SQL 資料庫")
            return connect_to_gcp_db(database_url)
        elif "azure.com" in database_url:
            print("檢測到 Azure Database 資料庫")
            return connect_to_azure_db(database_url)
        elif "digitalocean.com" in database_url:
            print("檢測到 DigitalOcean Managed Database")
            return connect_to_do_db(database_url)
        elif "herokuapp.com" in database_url:
            print("檢測到 Heroku Postgres 資料庫")
            return connect_to_heroku_db(database_url)
        else:
            print("使用通用 PostgreSQL 連接")
            return connect_to_generic_db(database_url)
            
    except Exception as e:
        print(f"連接資料庫失敗: {e}")
        return None

def connect_to_render_db(database_url):
    """連接 Render.com 資料庫"""
    try:
        conn = psycopg2.connect(database_url)
        print("✅ 成功連接到 Render.com 資料庫")
        return conn
    except Exception as e:
        print(f"❌ Render.com 連接失敗: {e}")
        return None

def connect_to_aws_db(database_url):
    """連接 AWS RDS 資料庫"""
    try:
        # AWS RDS 通常需要 SSL
        conn = psycopg2.connect(
            database_url,
            sslmode='require'
        )
        print("✅ 成功連接到 AWS RDS 資料庫")
        return conn
    except Exception as e:
        print(f"❌ AWS RDS 連接失敗: {e}")
        return None

def connect_to_gcp_db(database_url):
    """連接 Google Cloud SQL 資料庫"""
    try:
        # GCP 通常需要 SSL
        conn = psycopg2.connect(
            database_url,
            sslmode='require'
        )
        print("✅ 成功連接到 Google Cloud SQL 資料庫")
        return conn
    except Exception as e:
        print(f"❌ Google Cloud SQL 連接失敗: {e}")
        return None

def connect_to_azure_db(database_url):
    """連接 Azure Database 資料庫"""
    try:
        # Azure 通常需要 SSL
        conn = psycopg2.connect(
            database_url,
            sslmode='require'
        )
        print("✅ 成功連接到 Azure Database 資料庫")
        return conn
    except Exception as e:
        print(f"❌ Azure Database 連接失敗: {e}")
        return None

def connect_to_do_db(database_url):
    """連接 DigitalOcean Managed Database"""
    try:
        # DigitalOcean 通常需要 SSL
        conn = psycopg2.connect(
            database_url,
            sslmode='require'
        )
        print("✅ 成功連接到 DigitalOcean Managed Database")
        return conn
    except Exception as e:
        print(f"❌ DigitalOcean 連接失敗: {e}")
        return None

def connect_to_heroku_db(database_url):
    """連接 Heroku Postgres 資料庫"""
    try:
        conn = psycopg2.connect(database_url)
        print("✅ 成功連接到 Heroku Postgres 資料庫")
        return conn
    except Exception as e:
        print(f"❌ Heroku 連接失敗: {e}")
        return None

def connect_to_generic_db(database_url):
    """連接通用 PostgreSQL 資料庫"""
    try:
        conn = psycopg2.connect(database_url)
        print("✅ 成功連接到 PostgreSQL 資料庫")
        return conn
    except Exception as e:
        print(f"❌ 通用連接失敗: {e}")
        return None

def test_connection():
    """測試資料庫連接"""
    print("=== 測試資料庫連接 ===")
    conn = get_database_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"✅ 資料庫版本: {version[0]}")
            
            # 測試基本查詢
            cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
            table_count = cursor.fetchone()
            print(f"✅ 資料表數量: {table_count[0]}")
            
            conn.close()
            return True
        except Exception as e:
            print(f"❌ 連接測試失敗: {e}")
            return False
    return False

def get_database_info():
    """獲取資料庫詳細資訊"""
    print("=== 資料庫詳細資訊 ===")
    
    conn = get_database_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # 獲取資料庫大小
        cursor.execute("""
            SELECT pg_size_pretty(pg_database_size(current_database())) as db_size;
        """)
        db_size = cursor.fetchone()
        print(f"資料庫大小: {db_size[0]}")
        
        # 獲取資料表大小
        cursor.execute("""
            SELECT 
                schemaname,
                tablename,
                pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
        """)
        tables = cursor.fetchall()
        print(f"\n資料表大小:")
        for table in tables:
            print(f"  {table[1]}: {table[2]}")
        
        # 獲取連接數
        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        connections = cursor.fetchone()
        print(f"\n當前連接數: {connections[0]}")
        
        conn.close()
        
    except Exception as e:
        print(f"獲取資料庫資訊失敗: {e}")

def execute_query(query, params=None):
    """執行 SQL 查詢"""
    conn = get_database_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # 獲取結果
        if query.strip().upper().startswith('SELECT'):
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            return columns, rows
        else:
            conn.commit()
            return cursor.rowcount
        
    except Exception as e:
        print(f"執行查詢失敗: {e}")
        return None
    finally:
        conn.close()

def get_database_stats():
    """獲取資料庫統計資訊"""
    print("=== 資料庫統計資訊 ===")
    
    # 使用者統計
    query = """
    SELECT 
        COUNT(*) as total_users,
        COUNT(CASE WHEN is_admin = true THEN 1 END) as admin_users,
        COUNT(CASE WHEN is_admin = false THEN 1 END) as regular_users
    FROM users
    """
    
    result = execute_query(query)
    if result:
        columns, rows = result
        print(f"使用者統計:")
        print(f"  總使用者: {rows[0][0]}")
        print(f"  管理員: {rows[0][1]}")
        print(f"  一般使用者: {rows[0][2]}")
    
    # 檔案統計
    query = """
    SELECT 
        COUNT(*) as total_files,
        COUNT(CASE WHEN status = 'processing' THEN 1 END) as processing_files,
        COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed_files,
        COUNT(CASE WHEN status = 'expired' THEN 1 END) as expired_files
    FROM user_files
    """
    
    result = execute_query(query)
    if result:
        columns, rows = result
        print(f"\n檔案統計:")
        print(f"  總檔案數: {rows[0][0]}")
        print(f"  處理中: {rows[0][1]}")
        print(f"  已完成: {rows[0][2]}")
        print(f"  已過期: {rows[0][3]}")
    
    # 使用記錄統計
    query = """
    SELECT 
        COUNT(*) as total_usage,
        COUNT(CASE WHEN service_type = 'video_abstract' THEN 1 END) as video_abstract_usage,
        COUNT(CASE WHEN service_type = 'ppt_to_video' THEN 1 END) as ppt_to_video_usage
    FROM usage_records
    """
    
    result = execute_query(query)
    if result:
        columns, rows = result
        print(f"\n使用記錄統計:")
        print(f"  總使用次數: {rows[0][0]}")
        print(f"  影片摘要: {rows[0][1]}")
        print(f"  語音簡報: {rows[0][2]}")

def get_recent_uploads(limit=10):
    """獲取最近上傳的檔案"""
    print(f"\n=== 最近 {limit} 個上傳檔案 ===")
    
    query = """
    SELECT 
        uf.id,
        uf.file_name,
        uf.file_type,
        uf.file_size,
        uf.status,
        uf.created_at,
        uf.expires_at,
        u.email as user_email
    FROM user_files uf
    JOIN users u ON uf.user_id = u.id
    ORDER BY uf.created_at DESC
    LIMIT %s
    """
    
    result = execute_query(query, (limit,))
    if result:
        columns, rows = result
        print(f"{'ID':<5} {'檔案名稱':<30} {'使用者':<25} {'類型':<12} {'大小':<10} {'狀態':<10} {'上傳時間'}")
        print("-" * 100)
        
        for row in rows:
            file_size_mb = row[3] / (1024 * 1024) if row[3] else 0
            created_time = row[5].strftime('%Y-%m-%d %H:%M') if row[5] else 'N/A'
            
            print(f"{row[0]:<5} {row[1][:28]:<30} {row[7][:23]:<25} {row[2]:<12} {file_size_mb:.1f}MB {row[4]:<10} {created_time}")

def get_user_activity(email):
    """獲取特定使用者的活動記錄"""
    print(f"\n=== 使用者活動記錄: {email} ===")
    
    # 獲取使用者資訊
    query = """
    SELECT id, email, is_admin, created_at
    FROM users
    WHERE email = %s
    """
    
    result = execute_query(query, (email,))
    if not result or not result[1]:
        print(f"找不到使用者: {email}")
        return
    
    user_info = result[1][0]
    user_id = user_info[0]
    
    print(f"使用者 ID: {user_id}")
    print(f"Email: {user_info[1]}")
    print(f"管理員: {'是' if user_info[2] else '否'}")
    print(f"註冊時間: {user_info[3]}")
    
    # 獲取檔案記錄
    query = """
    SELECT file_name, file_type, file_size, status, created_at, expires_at
    FROM user_files
    WHERE user_id = %s
    ORDER BY created_at DESC
    """
    
    result = execute_query(query, (user_id,))
    if result:
        columns, rows = result
        print(f"\n檔案記錄 ({len(rows)} 個):")
        for row in rows:
            file_size_mb = row[2] / (1024 * 1024) if row[2] else 0
            created_time = row[4].strftime('%Y-%m-%d %H:%M') if row[4] else 'N/A'
            print(f"  - {row[0]} ({row[1]}, {file_size_mb:.1f}MB, {row[3]}, {created_time})")
    
    # 獲取使用記錄
    query = """
    SELECT service_type, usage_date
    FROM usage_records
    WHERE user_id = %s
    ORDER BY usage_date DESC
    """
    
    result = execute_query(query, (user_id,))
    if result:
        columns, rows = result
        print(f"\n使用記錄 ({len(rows)} 次):")
        for row in rows:
            usage_time = row[1].strftime('%Y-%m-%d %H:%M') if row[1] else 'N/A'
            print(f"  - {row[0]} ({usage_time})")

def verify_file_upload(file_id):
    """驗證特定檔案的上傳狀態"""
    print(f"\n=== 檔案驗證: ID {file_id} ===")
    
    query = """
    SELECT 
        uf.id,
        uf.file_name,
        uf.file_path,
        uf.file_type,
        uf.file_size,
        uf.status,
        uf.created_at,
        uf.expires_at,
        u.email as user_email
    FROM user_files uf
    JOIN users u ON uf.user_id = u.id
    WHERE uf.id = %s
    """
    
    result = execute_query(query, (file_id,))
    if not result or not result[1]:
        print(f"找不到檔案記錄: ID {file_id}")
        return
    
    file_info = result[1][0]
    
    print(f"檔案名稱: {file_info[1]}")
    print(f"檔案路徑: {file_info[2]}")
    print(f"檔案類型: {file_info[3]}")
    print(f"檔案大小: {file_info[4]} bytes ({file_info[4] / (1024 * 1024):.2f} MB)")
    print(f"狀態: {file_info[5]}")
    print(f"上傳時間: {file_info[6]}")
    print(f"過期時間: {file_info[7]}")
    print(f"使用者: {file_info[8]}")
    
    # 檢查是否過期
    now = datetime.utcnow()
    is_expired = now > file_info[7] if file_info[7] else True
    print(f"是否過期: {'是' if is_expired else '否'}")
    
    if not is_expired:
        days_until_expiry = (file_info[7] - now).days
        print(f"剩餘天數: {days_until_expiry} 天")

def main():
    """主函數"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python db_query_tool.py test                     # 測試資料庫連接")
        print("  python db_query_tool.py info                     # 顯示資料庫詳細資訊")
        print("  python db_query_tool.py stats                    # 顯示資料庫統計")
        print("  python db_query_tool.py recent [數量]            # 顯示最近上傳檔案")
        print("  python db_query_tool.py user <email>             # 顯示使用者活動")
        print("  python db_query_tool.py verify <file_id>         # 驗證檔案上傳")
        return
    
    command = sys.argv[1]
    
    if command == "test":
        test_connection()
    
    elif command == "info":
        get_database_info()
    
    elif command == "stats":
        get_database_stats()
    
    elif command == "recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        get_recent_uploads(limit)
    
    elif command == "user":
        if len(sys.argv) < 3:
            print("請提供使用者 email")
            return
        email = sys.argv[2]
        get_user_activity(email)
    
    elif command == "verify":
        if len(sys.argv) < 3:
            print("請提供檔案 ID")
            return
        file_id = int(sys.argv[2])
        verify_file_upload(file_id)
    
    else:
        print(f"未知命令: {command}")

if __name__ == "__main__":
    main() 